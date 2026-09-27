"""Idempotent skill intent and history; raw questions are not persisted/forwarded."""
import hashlib
from pydantic import Field
from services.portal_operational.skill_query import SkillQuery
from services.ledger_writer.principal_control import append_event, read_events, CommandConflict
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held

RESOURCE = 'skill_query_intent'


class QueryIntentBody(SkillQuery):
    idempotency_key: str = Field(min_length=8, max_length=128, pattern=r'^[A-Za-z0-9._-]+$')


async def submit(db, scope, skill_id, provisioning, body):
    if provisioning.skill_id != skill_id or provisioning.revoked_at is not None:
        raise Held('SKILL_PROVISIONING_CHANGED')
    query_id = 'skill-query-' + digest({'tenant': scope['tenant_id'], 'principal': scope['principal_id'],
                                      'skill': skill_id, 'idempotency': body.idempotency_key})
    payload = {'principal_id': scope['principal_id'], 'skill_id': skill_id, 'query_id': query_id,
               'query_sha256': hashlib.sha256(body.query.encode()).hexdigest(),
               'provisioning_sha256': digest(provisioning.model_dump(mode='json'))}
    try:
        return await append_event(db, tenant_id=scope['tenant_id'], run_id=query_id,
            command_id=digest({'query_intent': query_id}), resource_type=RESOURCE, event_type='skill.query.intent',
            decision='recorded', reason_code='SKILL_QUERY_INTENT_RECORDED', payload=payload)
    except CommandConflict:
        raise Held('SKILL_QUERY_IDEMPOTENCY_CONFLICT') from None


async def events(db, scope, skill_id, query_id):
    rows = await read_events(db, {'row.tenant_id': scope['tenant_id'], 'row.resource_type': RESOURCE,
        'row.run_id': query_id, 'payload.principal_id': scope['principal_id']})
    if not rows or rows[0]['payload'].get('skill_id') != skill_id:
        raise Held('SKILL_QUERY_NOT_FOUND')
    return rows


async def record_view(db, scope, intent, view):
    data = dict(view)
    await append_event(db, tenant_id=scope['tenant_id'], run_id=intent['row']['run_id'],
        command_id=digest({'query_view': intent['row']['hash'], 'view': data}), resource_type=RESOURCE,
        event_type='skill.query.view', decision=data['outcome'], reason_code=data['reason_code'],
        payload={'principal_id': scope['principal_id'], 'skill_id': intent['payload']['skill_id'], 'view': data})


def status(rows):
    intent = rows[0]
    last = next((e['payload']['view'] for e in reversed(rows) if 'view' in e['payload']), None)
    return {'query_id': intent['row']['run_id'], 'skill_id': intent['payload']['skill_id'],
            'query_sha256': intent['payload']['query_sha256'], 'intent_receipt_ref': intent['row']['hash'],
            **(last or {'outcome': 'held', 'reason_code': 'SKILL_NATIVE_PLAN_REQUIRED', 'execution_verified': False,
                       'delivery_verified': False}),
            'history': [{'receipt_ref': e['row']['hash'], 'event': e['row']['event_type'],
                         'reason_code': e['row']['reason_code']} for e in rows]}


def require_current_provisioning(intent, provisioning):
    if (provisioning.revoked_at is not None or provisioning.skill_id != intent['payload']['skill_id']
            or digest(provisioning.model_dump(mode='json')) != intent['payload']['provisioning_sha256']):
        raise Held('SKILL_PROVISIONING_CHANGED')