"""Durable work records on the ONE control ledger: tasks, documents, goals and the board are append-only event
streams reconstructed on read (the same discipline as commissioning drafts). Nothing here is tenant-specific: scope
comes from the signed-in identity; evidence comes from the qualified-memory spine (session turns)."""
from datetime import datetime, timezone

from services.ledger_writer.control_commands import COMMAND_KEY
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import append_event, read_events

RESOURCES = {'task': 'work_task', 'document': 'work_document', 'goal': 'work_goal', 'board': 'work_board'}
WRITE_ROLES = {'operator', 'master_admin'}


def now():
    return datetime.now(timezone.utc).isoformat()


def is_operator(scope):
    return bool(WRITE_ROLES & set(scope['roles']))


async def append(db, scope, resource, run_id, kind, payload, *, idempotent=False):
    body = {'principal_id': scope['principal_id'], 'kind': kind, 'at': now(), **payload}
    if idempotent:  # the same act recorded once: an identical body (time and actor aside) is the existing event
        skip = ('at', 'principal_id', COMMAND_KEY)
        same = {k: v for k, v in body.items() if k not in skip}
        for e in await events(db, scope, resource, run_id):
            if {k: v for k, v in e['payload'].items() if k not in skip} == same:
                return e
    return await append_event(db, tenant_id=scope['tenant_id'], run_id=run_id, command_id=digest({'work': resource, 'run': run_id, 'body': body}),
                              event_type=f'work.{resource}.{kind}', resource_type=RESOURCES[resource], decision=kind,
                              reason_code='WORK_RECORDED', payload=body)


async def events(db, scope, resource, run_id=None):
    query = {'row.tenant_id': scope['tenant_id'], 'row.resource_type': RESOURCES[resource]}
    if run_id is not None:
        query['row.run_id'] = run_id
    return await read_events(db, query)


def grouped(rows):
    by_id = {}
    for e in rows:
        by_id.setdefault(e['row']['run_id'], []).append(e)
    return by_id


def history_entry(e):
    p = e['payload']
    return {'kind': p['kind'], 'at': p['at'], 'principal_id': p['principal_id'], 'receipt_hash': e['row']['hash']}


def evidence_from_turn(session, turn):
    """What a turn hands over: objective, citations, receipt, ledger row, sources (artefact + version + rights) and loss."""
    ev = turn.get('evidence') or {}
    cited = list(ev.get('cited_refs') or [])
    selected = list((ev.get('window') or {}).get('selected_refs') or [])
    used_requests = {ref.split('/')[-2] for ref in (cited or selected)}
    sources = [{k: a.get(k) for k in ('artifact_ref', 'sha256', 'region', 'rights_receipt_ref', 'inspection_ref', 'request_id')}
               for a in ev.get('artefacts') or [] if a.get('request_id') in used_requests]
    return {'session_id': session['session_id'], 'turn_id': turn['turn_id'], 'objective': session['objective'], 'question': turn['question'],
            'decision': turn['decision'], 'refused': bool(turn.get('refused')), 'text': turn.get('answer') or turn.get('refusal_reason') or '',
            'cited_refs': cited, 'receipt_id': turn.get('receipt_id'), 'ledger_row_id': (turn.get('decision_detail') or {}).get('ledger_row_id'),
            'qualified_set_ref': ev.get('qualified_set_ref'), 'sources': sources, 'loss_statement': (ev.get('window') or {}).get('loss_statement'),
            'grounding': ev.get('grounding'), 'compaction_artefact': (session.get('compaction') or {}).get('artefact_hash')}


async def team(db, scope):
    """Admitted members of the requester's tenant — identity only, never credentials."""
    rows = []
    async for u in db.users.find({'tenant_id': scope['tenant_id']}, {'_id': 1, 'email': 1, 'name': 1, 'roles': 1}):
        rows.append({'principal_id': str(u['_id']), 'email': u.get('email'), 'name': u.get('name') or u.get('email'), 'roles': u.get('roles', [])})
    return sorted(rows, key=lambda r: r['email'] or '')


async def member(db, scope, principal_id):
    return next((m for m in await team(db, scope) if m['principal_id'] == principal_id), None)
