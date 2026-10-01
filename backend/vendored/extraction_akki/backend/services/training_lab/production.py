"""Evidence-linked training production manager; existing workers and admission stay authoritative."""
import hashlib
import json
from dataclasses import asdict
from pymongo import ReturnDocument
from services.training_lab import store, board_runs
from services.training_lab.production_contracts import Definition
from services.training_lab.production_evidence import measured_job, measured_strata, quote


def collection():
    coll = store.db().training_production_plans
    coll.create_index([('tenant_id', 1), ('plan_id', 1)], unique=True)
    return coll


def get(tenant, plan_id):
    return collection().find_one({'tenant_id': tenant, 'plan_id': plan_id}, {'_id': 0})


def for_run(tenant, run_id):
    return collection().find_one({'tenant_id': tenant, 'run_id': run_id}, {'_id': 0}, sort=[('created_at', -1)])


def validate_definition(tenant, value):
    definition = Definition.model_validate(value).model_dump()
    outcome, schema = definition['target_outcome'], definition['collection_schema']
    source_job, register = measured_job(tenant, outcome['population_register_ref'], 'assemble')
    if (source_job.get('params') or {}).get('kind') != 'transcript_text':
        raise ValueError('This register is not a qualified training population for this estate; comparison-only material cannot be repurposed.')
    seal = register.get('test_set_seal') or {}
    if set(outcome['stratum_refs']) != set(register.get('per_stratum') or {}):
        raise ValueError('Population must resolve to the complete named register strata; exclusions cannot be silent.')
    if seal.get('held_ids_sha256') != outcome['test_set_ref'] or not seal.get('sealed_at'):
        raise ValueError('The test-set reference must resolve to the existing sealed set.')
    from services.wizard.objective_compile import compile_target_outcome, compile_collection_schema
    from services.wizard.objective_compile import ObjectiveCompileError
    try:
        compiled_outcome = compile_target_outcome(task=outcome['task'], domain=outcome['domain'],
            population=outcome['population_register_ref'], acceptance=outcome['acceptance'],
            gate_policy=outcome['gate_policy'].replace('_', ' '), test_set_ref=outcome['test_set_ref'], constraints=outcome['constraints'])
        compiled_schema = compile_collection_schema(baseline_tier=tuple(schema['baseline_tier']), objective_tier=tuple(schema['objective_tier']))
    except ObjectiveCompileError as exc:
        raise ValueError(str(exc)) from None
    return definition, register, {'TargetOutcome': asdict(compiled_outcome), 'CollectionSchema': asdict(compiled_schema)}


def compile_plan(tenant, actor, run_id, value):
    if not board_runs.get(tenant, run_id):
        raise LookupError('No objective with that reference is available in this estate.')
    definition, register, artifacts = validate_definition(tenant, value)
    digest = hashlib.sha256(json.dumps([tenant, run_id, definition], sort_keys=True).encode()).hexdigest()
    plan_id = 'tp-' + digest[:24]
    doc = {'tenant_id': tenant, 'plan_id': plan_id, 'run_id': run_id, 'definition': definition,
           'artifacts': artifacts, 'corpus_id': register['corpus_id'], 'manifest_sha256': register['manifest_sha256'],
           'test_set_seal': register['test_set_seal'], 'train_units': register['splits']['train'],
           'created_at': store.now(), 'created_by': actor['principal_id'], 'revision': 0, 'recipe_revisions': [], 'stages': {},
           'status': 'calibration_required', 'training_started': False,
           'evidence_manifest': [{'artifact': k, 'class': 'owner_declared', 'source_ref': run_id} for k in artifacts]
                       + [{'artifact': 'population_and_test_set', 'class': 'measured', 'source_ref': definition['target_outcome']['population_register_ref']}],
           'definition_sha256': digest}
    collection().update_one({'tenant_id': tenant, 'plan_id': plan_id}, {'$setOnInsert': doc}, upsert=True)
    board_runs.collection().update_one({'tenant_id': tenant, 'run_id': run_id}, {'$set': {'plan_id': plan_id}})
    return get(tenant, plan_id)


def attach(tenant, plan_id, stage, job_id):
    plan = get(tenant, plan_id)
    if not plan:
        raise LookupError('No production plan with that reference is available in this estate.')
    phases = {'calibration': 'calibrate', 'comparison': 'compare_optimizers', 'training': 'train'}
    if stage not in phases:
        raise ValueError('Unknown production stage.')
    job, result = measured_job(tenant, job_id, phases[stage])
    if result.get('manifest_sha256') != plan['manifest_sha256']:
        raise ValueError('Evidence belongs to a different sealed dataset.')
    existing = plan['stages'].get(stage)
    if existing:
        if existing['job_id'] == job_id: return plan
        raise ValueError('This stage is already bound. Open a new version instead of replacing its evidence.')
    patch, entry = {}, {'job_id': job_id, 'receipt_sha256': job['receipt']['receipt_sha256'], 'class': 'measured', 'finished_at': job.get('finished_at')}
    if stage == 'calibration':
        base = result['base_selected_by_calibration']
        entry.update(base=base, quote=quote(result, base, plan['train_units'], plan['definition']['planned_epochs']))
        entry['within_budget'] = entry['quote']['confidence_interval_gpu_hours'][1] <= plan['definition']['gpu_hour_cap']
        patch['status'] = 'comparison_required' if entry['within_budget'] else 'budget_exceeded'
    elif stage == 'comparison':
        calibration = plan['stages'].get('calibration')
        if not calibration or result.get('base') != calibration['base']:
            raise ValueError('Compare the calibrated base before full training.')
        if not calibration.get('within_budget'):
            raise ValueError('The calibrated upper compute quote exceeds the recorded budget. Revise the objective rather than widening its cap silently.')
        if set(result.get('arms') or {}) != {'baseline', 'muon'}:
            raise ValueError('Both controlled recipe arms are required.')
        entry.update(arms=result['arms'], quality_parity=result.get('quality_parity'), recommendation=result.get('recommended_verdict'))
        patch['status'] = 'recipe_required'
    else:
        if not plan['stages'].get('comparison') or not plan['recipe_revisions']:
            raise ValueError('Calibration, comparison and an evidence-linked recipe are required first.')
        if (job.get('params') or {}).get('base') != plan['stages']['calibration']['base']:
            raise ValueError('Training must use the same calibrated and compared base.')
        manifest = result.get('artefact') or {}
        if not manifest.get('training_manifest_sha256') or not manifest.get('cited_units'):
            raise ValueError('The hashed per-example training manifest is missing.')
        actual_recipe = (result.get('training') or {}).get('recipe') or {}
        selected = plan['recipe_revisions'][-1]['recipe']
        if any(actual_recipe.get(k) != v for k, v in selected.items()):
            raise ValueError('The worker recipe does not match this plan revision.')
        entry.update(strata=measured_strata(result, plan['definition']['target_outcome']), moac=result.get('moac'),
                     training_manifest=result.get('artefact'), admission=(job.get('run_certificate') or {}).get('admission'))
        patch.update(status='evidence_assembled', training_started=True)
    entry['provenance'] = 'historical_evidence' if (job.get('submitted_at') or '') < plan['created_at'] else 'commissioned_evidence'
    patch[f'stages.{stage}'] = entry
    patch['updated_at'] = store.now()
    manifest = {'artifact': stage, 'class': 'measured', 'source_ref': job_id}
    result = collection().find_one_and_update({'tenant_id': tenant, 'plan_id': plan_id, 'revision': plan['revision']},
        {'$set': patch, '$inc': {'revision': 1}, '$push': {'evidence_manifest': manifest}}, projection={'_id': 0}, return_document=ReturnDocument.AFTER)
    if result is None: raise ValueError('The plan changed; reload before attaching evidence.')
    return result


def revise_recipe(tenant, plan_id, actor, body):
    plan = get(tenant, plan_id)
    if not plan: raise LookupError('No production plan with that reference is available in this estate.')
    if not plan['stages'].get('comparison'): raise ValueError('The controlled comparison must be recorded before selecting a recipe.')
    if plan['stages'].get('training'): raise ValueError('A completed run is immutable; open a new version.')
    if not body.recipe: raise ValueError('A recipe cannot be empty.')
    required = {'optimizer', 'lr', 'epochs', 'batch_size', 'grad_accum', 'max_seq_len'}
    if not required.issubset(body.recipe):
        raise ValueError('Record the complete optimizer, learning rate, epochs, batch, accumulation and sequence-length recipe; a partial recipe cannot control a run.')
    if body.recipe['epochs'] != plan['definition']['planned_epochs']:
        raise ValueError('The selected epochs differ from the calibrated quote; revise the plan and re-quote first.')
    allowed = {s['job_id'] for s in plan['stages'].values()}
    if not set(body.evidence_refs).issubset(allowed): raise ValueError('Recipe evidence must resolve within this plan.')
    row = {'recipe': body.recipe, 'reason': body.reason, 'evidence_refs': body.evidence_refs, 'at': store.now(), 'by': actor['principal_id']}
    result = collection().find_one_and_update({'tenant_id': tenant, 'plan_id': plan_id, 'revision': body.expected_revision},
        {'$push': {'recipe_revisions': row, 'evidence_manifest': {'artifact': 'recipe_revision', 'class': 'owner_declared', 'source_ref': body.evidence_refs}},
         '$set': {'status': 'ready_for_existing_execution_controls'}, '$inc': {'revision': 1}}, projection={'_id': 0}, return_document=ReturnDocument.AFTER)
    if result is None: raise ValueError('The plan changed; reload before revising its recipe.')
    return result


def moac_request(tenant, plan_id):
    plan = get(tenant, plan_id)
    if not plan: raise LookupError('No production plan with that reference is available in this estate.')
    trained = plan['stages'].get('training')
    if not trained: raise ValueError('A measured training record is required before assembling the MOAC request.')
    return {'plan_id': plan_id, 'definition_sha256': plan['definition_sha256'], 'artifacts': plan['artifacts'],
        'evidence_manifest': plan['evidence_manifest'], 'data_manifest_sha256': plan['manifest_sha256'],
        'sealed_test_set': plan['test_set_seal'], 'calibration_and_quote': plan['stages']['calibration'],
        'comparison': plan['stages']['comparison'], 'recipe_revisions': plan['recipe_revisions'],
        'per_stratum': trained['strata'], 'native_moac_evidence': trained['moac'],
        'training_manifest': trained['training_manifest'], 'recorded_admission': trained['admission'],
        'request_only': True, 'new_admission_issued': False,
        'independent_final_acceptance_established': False,
        'limits': ['A MOAC request does not issue admission.', 'Previously inspected or recipe-selection material is not an independent final evaluation.']}