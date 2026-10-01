"""Skill commission: freeze the Plan for one recorded query intent and bank the native governance receipts the gates
require, then advance through the ordinary execution spine.

Mirrors `commissioning.commission` for `kind=skill`: the scope group is the requester's own standing; expenditure and
answering groups come from the estate's admission record (the admitted interim stand-in when unseated). Quality and
context metadata are measured by the admitted worker over the sealed corpus and signed there; the two policy receipts
are signed by the estate's quality authority from custody; the caller's question receives its rights proof from the
rights authority under the lawful-basis anchor. Every step is idempotent per request identity.
"""
import json
from services.activation.approvals import approved_plan
from services.activation.record_shapes import Plan
from services.commissioning.commission import PLANNER_KEY, PLAN_TTL_SECONDS, SCOPE_GROUP, _estate, sign_approvals
from services.estate_admission import signing
from services.estate_admission.ceremony import QUALITY_AUTHORITY_KEY, QUALITY_AUTHORITY_SCOPE, receipts_for
from services.estate_admission.records import latest
from services.estate_admission.runtimes import runtime_by_id, select
from services.extraction_runtime import derived_rights, remote
from services.extraction_runtime.adapter import CALL_SECONDS, object_store_secrets
from services.extraction_runtime.skill_adapter import corpus_object, offer_terms
from services.extraction_runtime.skill_worker import MODEL_ID, context_policy_committed, quality_pack, snapshot_sha256
from services.extraction_runtime.structured_records_worker import unit_terms
from services.extraction_runtime.worker_bundle import bundle
from services.ledger_writer.mongo_control import digest
from services.non_gpu_governance import proofs
from services.non_gpu_governance.lineage import Rights
from services.northena.execution_builders import skill_request
from services.northena.execution_models import Held
from services.portal_operational.entitlements import read_view

DEADLINE_SECONDS = 24 * 3600
CATALOG_ACCESS_CLASS = 'local_served'
QUERY_RIGHTS_REASON = 'CALLER_QUERY_UNDER_KEY_GRANT'
LIMITS = [{'dimension': 'spend', 'unit': 'USD', 'quantity': '0'}, {'dimension': 'wall_clock', 'unit': 'seconds', 'quantity': '600'},
          {'dimension': 'bytes_read', 'unit': 'bytes', 'quantity': '4000000'},
          {'dimension': 'returned_records', 'unit': 'records', 'quantity': '100'},
          {'dimension': 'active_compute', 'unit': 'cpu_seconds', 'quantity': '120'}]
ACCEPTANCE_RULES = ('answer_is_a_subset_of_the_sealed_corpus', 'every_anchor_is_one_whole_unit_present_in_answer_and_corpus',
                    'anchors_are_attested_on_an_independent_admitted_runtime', 'no_model_no_paraphrase_no_source_read')


def query_ref_for(tenant, request_id):
    return f'akki://query/{tenant}/{request_id}'


def request_for(scope, provisioning, intent):
    request_id = intent['row']['run_id']
    return skill_request(provisioning, request_id=request_id, tenant_id=scope['tenant_id'], principal_id=scope['principal_id'],
                         query_ref=query_ref_for(scope['tenant_id'], request_id), query_sha256=intent['payload']['query_sha256'],
                         deadline_epoch=int(intent['row']['at']['epoch_s']) + DEADLINE_SECONDS)


async def ensure(db, scope, provisioning, intent, query_text):
    """Plan + approvals + governance receipts for this intent; returns the frozen request."""
    request = request_for(scope, provisioning, intent)
    offer_terms(request.digest(), unit_terms(query_text), intent['row']['hash'])
    receipts = receipts_for(db)
    try:
        plan, _, _, _, events = await approved_plan(receipts, request)
    except Held as exc:
        if exc.reason_code != 'ACTIVATION_PLAN_MISSING_OR_AMBIGUOUS':
            raise
        plan = await _freeze(db, receipts, scope, request, provisioning)
        events = await receipts.events()
    try:
        await _governance(db, receipts, request, plan, events)
    except (TimeoutError, ConnectionError, OSError):
        raise Held('SKILL_COMMISSION_RUNTIME_UNAVAILABLE') from None
    return request


def seat_groups(estate_groups, requester):
    groups = [{'group': SCOPE_GROUP, 'purpose': 'scope', 'members': [requester], 'quorum': 1}]
    stand_ins = []
    stand_in = estate_groups.get('interim_stand_in')
    for purpose in ('expenditure', 'answering'):
        seated = next((g for g in estate_groups['groups'] if g['purpose'] == purpose and g.get('members')), None)
        if seated is not None:
            groups.append({'group': seated['group'], 'purpose': purpose, 'members': list(seated['members']), 'quorum': int(seated['quorum'])})
            continue
        name = next((g['group'] for g in estate_groups['groups'] if g['purpose'] == purpose), None)
        if not stand_in or name is None:
            raise Held('APPROVAL_GROUP_UNSEATED:' + purpose)
        groups.append({'group': name, 'purpose': purpose, 'members': [stand_in['principal_id']], 'quorum': 1})
        stand_ins.append({'group': name, 'purpose': purpose, 'principal_id': stand_in['principal_id'], 'basis': stand_in['basis']})
    return groups, stand_ins


async def _freeze(db, receipts, scope, request, provisioning):
    tenant = scope['tenant_id']
    estate_groups, dials, allocation, planner = await _estate(db, tenant)
    licence = await read_view(db, scope)
    if licence.status != 'resolved' or licence.licence is None:
        raise Held(licence.reason_code or 'LICENCE_NOT_ADMITTED')
    if allocation['terms_ref'] != licence.licence.terms_identifier:
        raise Held('ALLOCATION_TERMS_MISMATCH')
    if not any(r.model_identifier == MODEL_ID and r.access_class == CATALOG_ACCESS_CLASS for r in licence.rows):
        raise Held('SKILL_EXECUTOR_NOT_IN_CATALOGUE')
    worker, _ = await select(db, tenant, 'worker', 'skill', ())
    await select(db, tenant, 'inspector', 'skill', (), exclude=(worker['runtime_id'],))
    corpus = await corpus_object(db, tenant, provisioning.corpus_slice_ref)
    groups, stand_ins = seat_groups(estate_groups, scope['principal_id'])
    plan = Plan.model_validate_json(json.dumps({
        'request': request.model_dump(mode='json'), 'groups': groups, 'purposes': ['answering'],
        'acceptance_script_sha256': digest(list(ACCEPTANCE_RULES)),
        'snapshot_hashes': [snapshot_sha256(corpus), digest(provisioning.model_dump(mode='json'))],
        'limits': LIMITS, 'allocation_ref': allocation['allocation_ref'], 'worker_ref': worker['worker_receipt_ref'],
        'terms_ref': licence.licence.terms_identifier, 'policy_epoch': dials['policy_epoch'],
        'dial_versions': dials['dial_versions'], 'policy_versions': dials['policy_versions'], 'termination_grace_seconds': 60,
        'catalog_model_identifier': MODEL_ID, 'catalog_access_class': CATALOG_ACCESS_CLASS}))
    receipt = signing.sign_receipt(tenant, planner['principal_id'], PLANNER_KEY, 'plan', plan.model_dump(mode='json'),
                                   scope_refs=request.scope_refs, request_sha256=request.digest(), ttl_seconds=PLAN_TTL_SECONDS)
    plan_ref = await receipts.record(receipt)
    await sign_approvals(db, receipts, scope, request, plan, plan_ref, stand_ins)
    return plan


async def _quality_authority(db, tenant):
    admissions = await latest(db, tenant, 'principal_admission')
    record = next((e['payload']['record'] for e in admissions.values()
                   if e['payload']['record'].get('kind') == 'agent' and e['payload']['record'].get('autonomy_scope') == QUALITY_AUTHORITY_SCOPE), None)
    if record is None or not signing.has_key(tenant, QUALITY_AUTHORITY_KEY):
        raise Held('QUALITY_AUTHORITY_UNADMITTED')
    return record['principal_id']


def _one(events, category, request):
    rows = proofs.observations(events, category, request)
    if len(rows) > 1:
        raise Held(category.upper() + '_AMBIGUOUS')
    return rows[0]['row']['hash'] if rows else None


async def _sign_policy(receipts, tenant, authority, request, category, claim_body, typed=None):
    claim = {'category': category, 'context_sha256': request.digest(), 'claim_sha256': digest(claim_body),
             'evidence_mode': 'measured', **(typed or {})}
    return await receipts.record(signing.sign_receipt(tenant, authority, QUALITY_AUTHORITY_KEY, 'observation', claim,
                                                      scope_refs=request.scope_refs, request_sha256=request.digest(),
                                                      ttl_seconds=PLAN_TTL_SECONDS))


async def _query_rights(db, receipts, request, events):
    query_ref = request.input_refs[-1]
    if derived_rights.existing(events, query_ref) is not None:
        return
    anchor = await latest(db, request.tenant_id, 'rights_anchor', 'default')
    if anchor is None:
        raise Held('RIGHTS_ANCHOR_UNRESOLVED')
    anchor_ref = anchor['payload']['record']['anchor_ref']
    authority = await receipts.resolve(anchor_ref, kind='observation', events=events)
    if not signing.has_key(request.tenant_id, authority.key_id):
        raise Held('RIGHTS_AUTHORITY_KEY_NOT_IN_CUSTODY')
    rights = Rights(version='akki.rights.metadata/1', unit_ref=query_ref, status='active', policy_ref=anchor_ref, reason_code=QUERY_RIGHTS_REASON)
    claim = {'category': 'rights', 'context_sha256': request.digest(), 'evidence_mode': 'measured',
             'claim_sha256': digest(rights.model_dump(mode='json')), 'rights': rights.model_dump(mode='json')}
    await receipts.record(signing.sign_receipt(request.tenant_id, authority.signer_id, authority.key_id, 'observation', claim,
                                               scope_refs=authority.scope_refs, request_sha256=request.digest(), ttl_seconds=derived_rights.YEAR))


async def _governance(db, receipts, request, plan, events):
    tenant = request.tenant_id
    await _query_rights(db, receipts, request, events)
    worker = await receipts.resolve(plan.worker_ref, kind='worker', events=events)
    descriptor = await runtime_by_id(db, tenant, worker.claims['runtime_id'])
    authority = await _quality_authority(db, tenant)
    custody = await latest(db, tenant, 'custody_descriptor', 'default')
    if custody is None:
        raise Held('CUSTODY_DESCRIPTOR_UNRESOLVED')
    corpus = await corpus_object(db, tenant, request.input_refs[0])
    pack = quality_pack(plan.policy_versions['cleanliness_pack'])
    base = {'tenant_id': tenant, 'request_id': request.request_id, 'request_sha256': request.digest(),
            'operation_key': 'skill-commission-' + request.request_id, 'fence': 0, 'scope_refs': list(request.scope_refs),
            'job_kind': 'skill.unit_retrieval'}

    async def worker_receipt(mode, **extra):
        value = await remote.call_async(descriptor, {**base, 'mode': mode, **extra}, deadline_seconds=CALL_SECONDS)
        if value.get('status') != 'complete':
            raise Held('SKILL_COMMISSION_' + str(value.get('reason_code') or mode.upper()))
        return await receipts.record(signing.runtime_receipt(value['receipt']))

    policy_ref = _one(events, 'quality_policy', request) or await _sign_policy(
        receipts, tenant, authority, request, 'quality_policy', pack, typed={'quality_pack': pack})
    population_ref = _one(events, 'quality_population', request) or await worker_receipt(
        'skill_prepare', corpus=corpus, secrets={'object_store': object_store_secrets(tenant, custody['payload']['record'])})
    quality_ref = _one(events, 'quality_register', request) or await worker_receipt(
        'skill_register', quality_pack=pack, policy_receipt_ref=policy_ref, population_receipt_ref=population_ref)
    committed = context_policy_committed(bundle()[1], corpus['ref'])
    ranking_ref = _one(events, 'context_policy', request) or await _sign_policy(receipts, tenant, authority, request, 'context_policy', committed)
    if _one(events, 'context_window', request) is None:
        await worker_receipt('skill_window', ranking_rule_ref=ranking_ref, qualified_set_receipt_ref=quality_ref,
                             objective_sha256=request.objective_sha256)
