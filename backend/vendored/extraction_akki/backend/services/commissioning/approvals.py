"""Approver decisions: any-one within a seated group signs with a custody-held key; refusals keep the job."""
import json
from fastapi import HTTPException
from services.activation.approvals import approved_plan
from services.activation.receipts import RESOURCE
from services.activation.record_shapes import Plan
from services.estate_admission import signing
from services.estate_admission.ceremony import receipts_for
from services.northena.execution_models import Held, Request


async def _plans(receipts, tenant):
    events = await receipts.events()
    plans = {}
    for e in events:
        raw = e['payload'].get('receipt', {})
        if e['row']['resource_type'] == RESOURCE and raw.get('kind') == 'plan':
            plans[raw['claims']['request']['request_id']] = (e, Plan.model_validate_json(json.dumps(raw['claims'])))
    return plans, events


def _decisions(events, plan_ref):
    rows = {}
    for e in events:
        raw = e['payload'].get('receipt', {})
        if e['row']['resource_type'] == RESOURCE and raw.get('kind') == 'approval' and raw['claims'].get('plan_ref') == plan_ref:
            rows[(raw['claims']['group'], raw['signer_id'])] = {'group': raw['claims']['group'], 'principal_id': raw['signer_id'],
                'decision': raw['claims']['decision'], 'reason': raw['claims']['reason'], 'at_epoch': raw['issued_epoch'],
                'receipt_ref': e['row']['hash']}
    return list(rows.values())


def _routing(plan, plan_ref, events, viewer):
    decisions = _decisions(events, plan_ref)
    groups = []
    for g in plan.groups:
        mine = [d for d in decisions if d['group'] == g.group]
        approved = [d for d in mine if d['decision'] == 'approved']
        refused = [d for d in mine if d['decision'] == 'refused']
        groups.append({'group': g.group, 'purpose': g.purpose, 'quorum': g.quorum, 'members': len(g.members),
                       'approved': len(approved), 'refused': len(refused), 'satisfied': len(approved) >= g.quorum,
                       'viewer_is_member': viewer in g.members, 'viewer_decided': any(d['principal_id'] == viewer for d in mine),
                       'decisions': [{k: v for k, v in d.items() if k != 'principal_id'} | {'by': 'you' if d['principal_id'] == viewer else 'another member'} for d in mine]})
    state = 'refused' if any(g['refused'] for g in groups) else 'approved' if all(g['satisfied'] for g in groups) else 'pending'
    return {'state': state, 'groups': groups}


async def routing(db, scope, request_id):
    receipts = receipts_for(db)
    plans, events = await _plans(receipts, scope['tenant_id'])
    if request_id not in plans:
        raise HTTPException(404, 'No signed plan exists for this request.')
    event, plan = plans[request_id]
    return {'request_id': request_id, 'plan_ref': event['row']['hash'], 'requester_is_you': plan.request.principal_id == scope['principal_id'],
            'objective_sha256': plan.request.objective_sha256, 'scope_refs': list(plan.request.scope_refs),
            'deadline_epoch': plan.request.deadline_epoch, **_routing(plan, event['row']['hash'], events, scope['principal_id'])}


async def queue(db, scope):
    """Requests whose pending groups seat this approver; nothing about other tenants or members."""
    receipts = receipts_for(db)
    plans, events = await _plans(receipts, scope['tenant_id'])
    rows = []
    for request_id, (event, plan) in plans.items():
        view = _routing(plan, event['row']['hash'], events, scope['principal_id'])
        if any(g['viewer_is_member'] for g in view['groups']) and plan.request.deadline_epoch > __import__('time').time():
            rows.append({'request_id': request_id, 'plan_ref': event['row']['hash'], 'state': view['state'],
                         'pending_for_you': [g['group'] for g in view['groups'] if g['viewer_is_member'] and not g['satisfied'] and not g['viewer_decided']],
                         'requester_is_you': plan.request.principal_id == scope['principal_id'], 'kind': plan.request.kind,
                         'scope_refs': list(plan.request.scope_refs), 'deadline_epoch': plan.request.deadline_epoch,
                         'groups': view['groups']})
    return sorted(rows, key=lambda r: (r['state'] != 'pending', -r['deadline_epoch']))


async def decide(db, scope, request_id, group, decision, reason):
    receipts = receipts_for(db)
    plans, events = await _plans(receipts, scope['tenant_id'])
    if request_id not in plans:
        raise HTTPException(404, 'No signed plan exists for this request.')
    event, plan = plans[request_id]
    target = next((g for g in plan.groups if g.group == group), None)
    if target is None or scope['principal_id'] not in target.members:
        raise HTTPException(403, 'You are not a seated member of that approval group.')
    key_id = 'approver-' + scope['principal_id']
    if not signing.has_key(scope['tenant_id'], key_id):
        raise HTTPException(409, {'reason_code': 'APPROVER_KEY_NOT_IN_CUSTODY', 'reason': 'Your approval key is not in estate custody; a ceremony is required.'})
    if not reason or not reason.strip():
        raise HTTPException(422, 'A reason is required with every decision; it is preserved with the job.')
    receipt = signing.sign_receipt(scope['tenant_id'], scope['principal_id'], key_id, 'approval',
        {'plan_ref': event['row']['hash'], 'group': group, 'decision': decision, 'reason': reason.strip()[:200]},
        scope_refs=plan.request.scope_refs, request_sha256=plan.request.digest(), ttl_seconds=30 * 86400)
    try:
        await receipts.record(receipt)
    except Held as exc:
        raise HTTPException(409, {'reason_code': exc.reason_code, 'reason': 'The decision could not be recorded under your admitted mandate.'}) from None
    return await routing(db, scope, request_id)
