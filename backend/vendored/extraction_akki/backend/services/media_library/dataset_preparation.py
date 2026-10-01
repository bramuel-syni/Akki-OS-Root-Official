"""Bind media readiness to a training objective, without promoting declared metadata into labels."""
import hashlib
import json
from services.media_library import store, assessment
from services.training_lab import production, store as lab


def prepare(actor, plan_id, file_ids):
    tenant = actor['tenant_id']
    plan = production.get(tenant, plan_id)
    if not plan: raise LookupError('No training plan with that reference is available in this estate.')
    if not file_ids or len(file_ids) > 200 or len(set(file_ids)) != len(file_ids):
        raise ValueError('Select between one and 200 distinct library files.')
    rows = [store.get(tenant, ref) for ref in file_ids]
    if any(not r or r.get('is_deleted') or r.get('status') != 'available' for r in rows):
        raise LookupError('A selected library file is no longer available in this estate.')
    snapshot = assessment.snapshot(rows)
    outcome = plan['definition']['target_outcome']
    snapshot.update(plan_id=plan_id, objective_ref=plan['run_id'], collection_schema=plan['artifacts']['CollectionSchema'],
        per_stratum_acceptance=outcome['acceptance'], final_test_set_ref=outcome['test_set_ref'],
        annotation_contract={'speech_present': 'independent label', 'music_present': 'independent label',
            'mixed_allowed': True, 'unknowns': 'masked, never treated as negative labels'},
        split_requirements=['group by speaker, session and source', 'deduplicate across partitions', 'reserve independent sealed final material'],
        declared_labels_are_reference_truth=False)
    request = {'title': 'Dataset preparation for ' + plan['run_id'], 'plan_id': plan_id,
               'files': [{'file_id': r['file_id'], 'revision': r['revision']} for r in rows]}
    key = 'dataset-' + hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
    run, _ = lab.enqueue(tenant, actor['principal_id'], key, request, kind='dataset_readiness', dataset_assessment=snapshot)
    production.collection().update_one({'tenant_id': tenant, 'plan_id': plan_id}, {'$set': {'dataset_preparation_ref': run['run_id']}})
    return lab.public(run)