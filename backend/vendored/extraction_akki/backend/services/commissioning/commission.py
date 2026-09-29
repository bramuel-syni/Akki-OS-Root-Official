"""Freeze: draft → frozen DAP request + signed Plan + approvals + durable work order.

Approval seating rule: the scope group is always the requester's own operator standing, built at
freeze from the request; expenditure and purpose groups come from the estate's admission record.
A needed group with no seated member is filled by the estate's admitted interim-pilot stand-in —
and the work order, the approval receipt and the run view all say so. The Plan's request is
byte-identical to what `portal_operational.execution.frozen_request` rebuilds at advance time.
"""
import json
import time
from datetime import datetime, timezone
from fastapi import HTTPException
from services.activation.approvals import approved_plan
from services.activation.record_shapes import Plan
from services.commissioning import shaping
from services.estate_admission import signing
from services.estate_admission.ceremony import receipts_for
from services.estate_admission.records import latest
from services.estate_admission.runtimes import select
from services.ledger_writer.mongo_control import digest
from services.northena import portal_work
from services.northena.execution_models import Held, Request
from services.portal_operational.entitlements import read_view
from services.portal_operational.models import SubmitRequest
from services.work_orders import packaging
from services.work_orders.kind_profiles import profile_for_operation

DEADLINE_SECONDS = 24 * 3600
PLANNER_KEY = 'northena-planner'
SCOPE_GROUP = 'scope.requester'
STAND_IN_REASON = 'INTERIM_PILOT_ADMISSION_STAND_IN'


def approver_key(principal_id):
    return 'approver-' + principal_id


async def _estate(db, tenant):
    values = {}
    for kind in ('approval_groups', 'dials', 'allocation_binding', 'principal_admission'):
        values[kind] = await latest(db, tenant, kind)
    missing = [k for k in ('approval_groups', 'dials', 'allocation_binding') if not values[k]]
    if missing:
        raise Held('ESTATE_ADMISSION_INCOMPLETE:' + ','.join(missing))
    planner = next((e['payload']['record'] for e in values['principal_admission'].values()
                    if e['payload']['record'].get('kind') == 'agent' and e['payload']['record'].get('autonomy_scope') == 'northena:planner'), None)
    if planner is None or not signing.has_key(tenant, PLANNER_KEY):
        raise Held('PLANNER_SIGNER_UNADMITTED')
    return (values['approval_groups']['default']['payload']['record'],
            values['dials']['default']['payload']['record'], values['allocation_binding']['default']['payload']['record'], planner)


def seat_groups(estate_groups, controlled, requester):
    """Returns (plan groups, stand-ins). The scope group is the requester; unseated groups take the stand-in."""
    needed = ['expenditure'] + (['extraction'] if controlled else [])
    groups = [{'group': SCOPE_GROUP, 'purpose': 'scope', 'members': [requester], 'quorum': 1}]
    stand_ins = []
    stand_in = estate_groups.get('interim_stand_in')
    for purpose in needed:
        seated = next((g for g in estate_groups['groups'] if g['purpose'] == purpose and g.get('members')), None)
        if seated is not None:
            groups.append({'group': seated['group'], 'purpose': purpose, 'members': list(seated['members']), 'quorum': int(seated['quorum'])})
            continue
        if not stand_in:
            raise Held('APPROVAL_GROUP_UNSEATED:' + purpose)
        name = next((g['group'] for g in estate_groups['groups'] if g['purpose'] == purpose), purpose + '.unseated')
        groups.append({'group': name, 'purpose': purpose, 'members': [stand_in['principal_id']], 'quorum': 1})
        stand_ins.append({'group': name, 'purpose': purpose, 'principal_id': stand_in['principal_id'], 'basis': stand_in['basis']})
    return groups, stand_ins


async def sign_approvals(db, receipts, scope, request, plan, plan_ref, stand_ins):
    """Requester signs the scope group with the custody key admitted to them; stand-ins sign theirs, saying so."""
    signed = []
    key_id = approver_key(scope['principal_id'])
    for group in plan.groups:
        if group.group == SCOPE_GROUP and scope['principal_id'] in group.members:
            if not signing.has_key(scope['tenant_id'], key_id):
                raise Held('APPROVER_KEY_NOT_IN_CUSTODY')
            receipt = signing.sign_receipt(scope['tenant_id'], scope['principal_id'], key_id, 'approval',
                {'plan_ref': plan_ref, 'group': group.group, 'decision': 'approved', 'reason': 'REQUESTER_OPERATOR_STANDING'},
                scope_refs=request.scope_refs, request_sha256=request.digest(), ttl_seconds=30 * 86400)
            signed.append({'group': group.group, 'by': 'requester', 'receipt_ref': await receipts.record(receipt)})
    for item in stand_ins:
        stand_key = approver_key(item['principal_id'])
        if not signing.has_key(scope['tenant_id'], stand_key):
            raise Held('STAND_IN_KEY_NOT_IN_CUSTODY')
        receipt = signing.sign_receipt(scope['tenant_id'], item['principal_id'], stand_key, 'approval',
            {'plan_ref': plan_ref, 'group': item['group'], 'decision': 'approved', 'reason': STAND_IN_REASON},
            scope_refs=request.scope_refs, request_sha256=request.digest(), ttl_seconds=30 * 86400)
        signed.append({'group': item['group'], 'by': 'interim_pilot_stand_in', 'receipt_ref': await receipts.record(receipt)})
    return signed


async def commission(db, scope, draft_id, idempotency_key):
    view = await shaping.view(db, scope, draft_id)
    if view['state'] != 'draft':
        raise HTTPException(409, f"Draft is {view['state']}; a new commission requires a new draft.")
    verdict = view['feasibility']
    if verdict.get('verdict') != 'warm':
        raise HTTPException(409, {'reason_code': verdict.get('reason_code'), 'reason': verdict.get('basis')})
    if view['routing']['unseated_groups']:
        raise HTTPException(409, {'reason_code': 'APPROVAL_GROUP_UNSEATED', 'reason': 'An approval group this request needs has neither seated members nor an admitted stand-in.'})
    envelope, profile, table = view['envelope'], profile_for_operation(view['envelope']['operation']), verdict['table']
    tenant = scope['tenant_id']
    estate_groups, dials, allocation, planner = await _estate(db, tenant)
    licence = await read_view(db, scope)
    if licence.status != 'resolved' or licence.licence is None:
        raise HTTPException(409, {'reason_code': licence.reason_code or 'LICENCE_NOT_ADMITTED', 'reason': 'No active licence resolves for this principal.'})
    if allocation['terms_ref'] != licence.licence.terms_identifier:
        raise HTTPException(409, {'reason_code': 'ALLOCATION_TERMS_MISMATCH', 'reason': 'The estate allocation cites different terms than the licence.'})
    sized = verdict['sizing']
    worker, worker_basis = await select(db, tenant, 'worker', profile.request_kind, envelope['units'], sizing=sized)
    inspector, inspector_basis = await select(db, tenant, 'inspector', profile.request_kind, (), exclude=(worker['runtime_id'],))
    submitted = await portal_work.submit(db, scope, SubmitRequest(objective_text=envelope['objective_text'],
        operation=envelope['operation'], units=list(envelope['units']), idempotency_key=idempotency_key))
    deadline = int(time.time()) + DEADLINE_SECONDS
    request = Request(request_id=submitted.request_id, tenant_id=tenant, principal_id=scope['principal_id'],
                      kind=profile.request_kind, engine=profile.engine, objective_sha256=digest(envelope['objective_text']),
                      input_refs=tuple('akki://source/' + u for u in envelope['units']), scope_refs=tuple(envelope['units']),
                      deadline_epoch=deadline)
    receipts = receipts_for(db)
    try:
        await approved_plan(receipts, request)
        return await shaping.view(db, scope, draft_id)
    except Held as exc:
        if exc.reason_code != 'ACTIVATION_PLAN_MISSING_OR_AMBIGUOUS':
            raise
    bounds = dict(verdict['bounds'])
    limits = profile.limits(bounds, sized)
    groups, stand_ins = seat_groups(estate_groups, verdict['controlled'], scope['principal_id'])
    plan = Plan.model_validate_json(json.dumps({
        'request': request.model_dump(mode='json'), 'groups': groups,
        'purposes': list(profile.purposes), 'acceptance_script_sha256': digest(list(profile.acceptance_rules)),
        'snapshot_hashes': [digest(envelope), digest({'census_run_id': table['census_run_id'], 'source_ref': table['source_ref'],
                                                       'table': f"{table['database']}.{table['table']}", 'row_count': table['row_count']}),
                            digest(sized)],
        'limits': limits, 'allocation_ref': allocation['allocation_ref'], 'worker_ref': worker['worker_receipt_ref'],
        'terms_ref': licence.licence.terms_identifier, 'policy_epoch': dials['policy_epoch'],
        'dial_versions': dials['dial_versions'], 'policy_versions': dials['policy_versions'],
        'termination_grace_seconds': int(bounds.get('termination_grace_seconds', 60))}))
    plan_receipt = signing.sign_receipt(tenant, planner['principal_id'], PLANNER_KEY, 'plan', plan.model_dump(mode='json'),
                                        scope_refs=request.scope_refs, request_sha256=request.digest(), ttl_seconds=DEADLINE_SECONDS + 3600)
    plan_ref = await receipts.record(plan_receipt)
    approvals = await sign_approvals(db, receipts, scope, request, plan, plan_ref, stand_ins)
    selection = {'source_id': envelope['units'][0], 'source_ref': table['source_ref'], 'database': table['database'],
                 'table': table['table'], 'columns': table['columns'], 'primary_key': table['primary_key'],
                 'role_signals': table['role_signals'], 'max_records': int(bounds['max_records']),
                 'batch_size': int(bounds['batch_size']), 'estimated_row_bytes': int(bounds['estimated_row_bytes']),
                 'census_run_id': table['census_run_id']}
    order = {'job_kind': profile.job_kind, 'selection': selection, 'floor': verdict['floor'],
             'artifact_ref': f'akki://artifact/{tenant}/{request.request_id}/qualified-units',
             'manifest': packaging.build_manifest(profile, request, selection, worker['runtime_id']),
             'worker_runtime_id': worker['runtime_id'], 'inspector_runtime_id': inspector['runtime_id'],
             'selection_basis': {'worker': worker_basis, 'inspector': inspector_basis, 'scope': verdict['basis']},
             'sizing': sized, 'stand_ins': stand_ins, 'groups': groups,
             'plan_ref': plan_ref, 'deadline_epoch': deadline, 'quote': view['quote']}
    order_ref = await packaging.record(db, request, order)
    await shaping.mark(db, scope, draft_id, 'commissioned', {
        'request_id': request.request_id, 'request_sha256': request.digest(), 'plan_ref': plan_ref, 'work_order_ref': order_ref,
        'deadline_epoch': deadline, 'approvals_signed': approvals, 'stand_ins': stand_ins, 'controlled': verdict['controlled'],
        'quote': view['quote'], 'sizing': sized, 'selection_basis': order['selection_basis'],
        'dispatch_intent': order['manifest']['dispatch_intent'], 'commissioned_at': datetime.now(timezone.utc).isoformat()})
    return await shaping.view(db, scope, draft_id)
