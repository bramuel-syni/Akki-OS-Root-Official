"""Shaping: durable drafts, the commit review and the pilot quote. No effect until Freeze."""
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from fastapi import HTTPException
from services.commissioning import feasibility
from services.enforce.control_scope import require_control_scope
from services.estate_admission.records import latest
from services.estate_admission import signing
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events

RESOURCE = 'dap_shaping'
OPERATIONS = Literal['browse_estate', 'connect_workspace', 'processed_intelligence', 'fine_tune_model',
                     'develop_skills', 'download_raw_data']


class Reach(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    database: str = Field(min_length=1, max_length=128)
    table: str = Field(min_length=1, max_length=128)


class Bounds(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    max_records: int | None = Field(default=None, ge=1, le=20000)
    max_seconds: int | None = Field(default=None, ge=120, le=7200)


class DraftBody(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    objective_text: str = Field(min_length=1, max_length=8000)
    operation: OPERATIONS
    units: list[str] = Field(min_length=1, max_length=1)
    reach: Reach | None = None
    bounds: Bounds | None = None
    done_condition: str | None = Field(default=None, max_length=1000)
    draft_id: str | None = Field(default=None, min_length=8, max_length=80)


async def events_for(db, scope, draft_id=None):
    query = {'row.tenant_id': scope['tenant_id'], 'row.resource_type': RESOURCE, 'payload.principal_id': scope['principal_id']}
    if draft_id is not None:
        query['row.run_id'] = draft_id
    return await read_events(db, query)


async def _append(db, scope, draft_id, kind, payload):
    return await append_event(db, tenant_id=scope['tenant_id'], run_id=draft_id,
        command_id=digest({'shaping': draft_id, 'kind': kind, 'payload': payload}), event_type='dap.shaping.' + kind,
        resource_type=RESOURCE, decision=kind, reason_code='SHAPING_RECORDED',
        payload={'principal_id': scope['principal_id'], 'draft_id': draft_id, 'kind': kind, **payload})


def envelope_of(body):
    return {'objective_text': body.objective_text, 'operation': body.operation, 'units': list(body.units),
            'reach': body.reach.model_dump() if body.reach else None,
            'bounds': body.bounds.model_dump(exclude_none=True) if body.bounds else {},
            'done_condition': body.done_condition, 'output': {'form': 'qualified_units_jsonl'}}


async def save(db, scope, body):
    """Create or revise; every revision is a new immutable version, never an edit."""
    draft_id = body.draft_id or 'drf-' + digest([scope['tenant_id'], scope['principal_id'], body.objective_text, datetime.now(timezone.utc).isoformat()])[:24]
    events = await events_for(db, scope, draft_id)
    if events and current(events)['state'] != 'draft':
        raise HTTPException(409, 'A commissioned, refused or withdrawn draft cannot be revised; start a new draft.')
    version = 1 + sum(1 for e in events if e['payload']['kind'] == 'version')
    await _append(db, scope, draft_id, 'version', {'version': version, 'envelope': envelope_of(body),
                                                    'saved_at': datetime.now(timezone.utc).isoformat()})
    return await view(db, scope, draft_id)


def current(events):
    state, versions, extra = 'draft', [], {}
    for e in events:
        p = e['payload']
        if p['kind'] == 'version':
            versions.append({'version': p['version'], 'envelope': p['envelope'], 'saved_at': p['saved_at'], 'receipt_hash': e['row']['hash']})
        elif p['kind'] in ('commissioned', 'refused', 'withdrawn'):
            state = p['kind']
            extra = {k: v for k, v in p.items() if k not in ('principal_id', 'draft_id', 'kind')}
    return {'state': state, 'versions': versions, 'envelope': versions[-1]['envelope'] if versions else None, **extra}


async def load(db, scope, draft_id):
    events = await events_for(db, scope, draft_id)
    if not events:
        raise HTTPException(404, 'Draft not found.')
    return current(events)


def quote_for(profile, verdict):
    """Pilot zero-rate line, non-precedent, stamped; measured in the three units. Metering still applies."""
    estimate = verdict.get('estimate') or {}
    lines = [{'unit': 'records_scanned', 'estimated_quantity': estimate.get('scanned_records', 0), 'rate': '0', 'currency': 'USD'},
             {'unit': 'records_returned', 'estimated_quantity': estimate.get('returned_records', 0), 'rate': '0', 'currency': 'USD'},
             {'unit': 'seconds', 'estimated_quantity': verdict.get('bounds', {}).get('max_seconds', 0), 'rate': '0', 'currency': 'USD'}]
    for cls, sized in (verdict.get('sizing') or {}).get('classes', {}).items():
        lines.append({'unit': sized['unit'], 'estimated_quantity': sized['estimate_seconds'], 'reserved_quantity': sized['reservation_seconds'],
                      'rate': '0', 'currency': 'USD', 'compute_class': cls, 'rate_basis': sized['rate_basis']})
    return {'price_line': profile.price_line, 'model': 'pilot.zero_rate', 'precedent': False, 'line_items': lines,
            'total': '0', 'currency': 'USD', 'validity_seconds': 86400,
            'cancellation_liability': 'Charged only to the point of stop; nothing partial is delivered or settled.',
            'rate_card_status': 'Rate card not yet ruled; this pilot line settles at zero and sets no precedent.'}


async def routing_for(db, scope, verdict):
    """Seating as the freeze will apply it: scope = the requester's standing; other groups from the estate
    record; a needed group with no members is filled by the admitted interim-pilot stand-in, named here."""
    from services.commissioning.commission import SCOPE_GROUP, approver_key
    groups_record = await latest(db, scope['tenant_id'], 'approval_groups', 'default')
    estate = groups_record['payload']['record'] if groups_record else {'groups': []}
    stand_in = estate.get('interim_stand_in')
    needed = ['expenditure'] + (['extraction'] if verdict.get('controlled') else [])
    tenant, me = scope['tenant_id'], scope['principal_id']
    routed = [{'group': SCOPE_GROUP, 'purpose': 'scope', 'quorum': 1, 'members': 1, 'requester_is_member': True,
               'requester_key_in_custody': signing.has_key(tenant, approver_key(me)), 'seating': 'requester_operator_standing'}]
    missing = []
    for purpose in needed:
        seated = next((g for g in estate['groups'] if g['purpose'] == purpose and g.get('members')), None)
        if seated is not None:
            member = me in seated['members']
            routed.append({'group': seated['group'], 'purpose': purpose, 'quorum': seated['quorum'], 'members': len(seated['members']),
                           'requester_is_member': member, 'requester_key_in_custody': member and signing.has_key(tenant, approver_key(me)),
                           'seating': 'estate_admission_record'})
        elif stand_in:
            name = next((g['group'] for g in estate['groups'] if g['purpose'] == purpose), purpose + '.unseated')
            routed.append({'group': name, 'purpose': purpose, 'quorum': 1, 'members': 1, 'requester_is_member': False,
                           'requester_key_in_custody': False, 'seating': 'interim_pilot_stand_in',
                           'stand_in': {'principal_id': stand_in['principal_id'], 'basis': stand_in['basis']}})
        else:
            missing.append(purpose)
    return {'controlled': bool(verdict.get('controlled')), 'groups': routed, 'unseated_groups': missing,
            'requires_other_approver': any(not g['requester_key_in_custody'] and g['seating'] == 'estate_admission_record' for g in routed),
            'requester_key_in_custody': routed[0]['requester_key_in_custody']}


async def view(db, scope, draft_id):
    from services.work_orders.kind_profiles import profile_for_operation
    state = await load(db, scope, draft_id)
    envelope = state['envelope']
    verdict = await feasibility.assess(db, scope['tenant_id'], envelope)
    profile = profile_for_operation(envelope['operation'])
    supplied = [k for k in ('objective_text', 'operation', 'units', 'reach', 'bounds', 'done_condition') if envelope.get(k)]
    assumed = []
    if verdict.get('verdict') == 'warm':
        if 'reach' in verdict.get('assumed', []):
            t = verdict['table']
            assumed.append({'field': 'reach', 'value': f"{t['database']}.{t['table']}", 'basis': verdict['basis']})
        for key, value in verdict['bounds'].items():
            if key not in (envelope.get('bounds') or {}):
                assumed.append({'field': f'bounds.{key}', 'value': value, 'basis': f'kind profile {verdict["job_kind"]} default'})
        if not envelope.get('done_condition'):
            assumed.append({'field': 'done_condition', 'value': f"up to {verdict['bounds']['max_records']} qualified units sealed, inspected and delivered through custody",
                            'basis': 'kind profile output contract'})
        assumed.append({'field': 'floor', 'value': verdict['floor'], 'basis': 'census role signals and column names; personal columns are redacted on the worker'})
        assumed.append({'field': 'compute', 'value': {cls: f"{c['reservation_seconds']} {c['unit']}" for cls, c in verdict['sizing']['classes'].items()},
                        'basis': verdict['sizing']['basis']})
    routing = await routing_for(db, scope, verdict) if verdict.get('verdict') == 'warm' else None
    return {'draft_id': draft_id, 'state': state['state'], 'version': len(state['versions']), 'versions': state['versions'],
            'envelope': envelope, 'supplied': supplied, 'assumed': assumed, 'feasibility': verdict,
            'quote': quote_for(profile, verdict) if profile and verdict.get('verdict') == 'warm' else None,
            'routing': routing, 'freeze_ready': verdict.get('verdict') == 'warm' and state['state'] == 'draft'
                                                and bool(routing) and not routing['unseated_groups'],
            **{k: v for k, v in state.items() if k not in ('state', 'versions', 'envelope')}}


async def listing(db, scope):
    by_id = {}
    for e in await events_for(db, scope):
        by_id.setdefault(e['payload']['draft_id'], []).append(e)
    rows = []
    for draft_id, events in by_id.items():
        state = current(events)
        rows.append({'draft_id': draft_id, 'state': state['state'], 'version': len(state['versions']),
                     'objective_text': (state['envelope'] or {}).get('objective_text'), 'operation': (state['envelope'] or {}).get('operation'),
                     'units': (state['envelope'] or {}).get('units'), 'saved_at': state['versions'][-1]['saved_at'] if state['versions'] else None,
                     'request_id': state.get('request_id')})
    return sorted(rows, key=lambda r: r['saved_at'] or '', reverse=True)


async def mark(db, scope, draft_id, kind, payload):
    return await _append(db, scope, draft_id, kind, payload)
