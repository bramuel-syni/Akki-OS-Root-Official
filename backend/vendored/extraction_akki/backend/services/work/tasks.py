"""Tasks: durable work items with an owner, permitted contributors, evidence items, open questions and attached
documents. A task can begin from a chat turn (handoff keeps objective, citations, receipt, sources and loss) or from
a stated objective. State is reconstructed from the ledger; nothing is edited in place."""
import hashlib

from fastapi import HTTPException

from services.chat import sessions
from services.work import records

STATES = ('open', 'in_progress', 'done', 'withdrawn')


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def current(rows):
    task = None
    for e in rows:
        p = e['payload']
        kind = p['kind']
        if kind == 'created':
            task = {'task_id': e['row']['run_id'], 'created_by': p['principal_id'], 'created_at': p['at'], 'title': p['title'],
                    'objective': p['objective'], 'origin': p.get('origin'), 'evidence': list(p.get('evidence') or []), 'sources': list(p.get('sources') or []),
                    'owner': p.get('owner') or p['principal_id'], 'contributors': [], 'items': [], 'questions': [], 'documents': [], 'goal_ids': [],
                    'state': 'open', 'stale': None, 'due': p.get('due'), 'history': []}
        if task is None:
            continue
        if kind == 'assigned':
            task['owner'] = p['owner']
        elif kind == 'contributor_added':
            task['contributors'] = [c for c in task['contributors'] if c['principal_id'] != p['contributor']] + [{'principal_id': p['contributor'], 'role': p['role'], 'added_by': p['principal_id']}]
        elif kind == 'item_added':
            task['items'].append({'item_id': p['item_id'], 'label': p['label'], 'evidence_ref': p.get('evidence_ref'), 'state': 'open', 'by': p['principal_id'], 'at': p['at']})
        elif kind == 'item_state':
            for item in task['items']:
                if item['item_id'] == p['item_id']:
                    item.update({'state': p['state'], 'evidence_ref': p.get('evidence_ref') or item.get('evidence_ref')})
        elif kind == 'evidence_added':
            task['evidence'].append({'kind': p['evidence_kind'], 'ref': p['ref'], 'note': p.get('note'), 'by': p['principal_id'], 'at': p['at']})
        elif kind == 'question_added':
            task['questions'].append({'question_id': p['question_id'], 'text': p['text'], 'open': True, 'by': p['principal_id'], 'at': p['at']})
        elif kind == 'question_closed':
            for q in task['questions']:
                if q['question_id'] == p['question_id']:
                    q.update({'open': False, 'closed_by': p['principal_id'], 'answer': p.get('answer')})
        elif kind == 'document_attached':
            if p['doc_id'] not in task['documents']:
                task['documents'].append(p['doc_id'])
        elif kind == 'goal_linked':
            if p['goal_id'] not in task['goal_ids']:
                task['goal_ids'].append(p['goal_id'])
        elif kind == 'state':
            task['state'] = p['state']
        elif kind == 'stale':
            task['stale'] = {'reason_code': p['reason_code'], 'artifact_refs': p['artifact_refs'], 'revocation_ref': p.get('revocation_ref'), 'at': p['at']}
        task['history'].append(records.history_entry(e))
    return task


def can_edit(scope, task):
    people = {task['created_by'], task['owner'], *(c['principal_id'] for c in task['contributors'])}
    return scope['principal_id'] in people or records.is_operator(scope)


async def load(db, scope, task_id):
    task = current(await records.events(db, scope, 'task', task_id))
    if task is None:
        raise HTTPException(404, 'No such task in your estate.')
    return task


async def listing(db, scope):
    rows = [current(evs) for evs in records.grouped(await records.events(db, scope, 'task')).values()]
    return sorted((t for t in rows if t), key=lambda t: t['created_at'], reverse=True)


async def create(db, scope, *, title, objective_text=None, session_id=None, turn_id=None, owner=None, due=None):
    """From a turn (idempotent per turn) or from a stated objective."""
    if session_id:
        session = await sessions.get(scope, session_id)
        turn = next((t for t in (session or {}).get('turns', []) if t['turn_id'] == turn_id), None)
        if turn is None:
            raise HTTPException(404, 'No such turn in your conversations.')
        handoff = records.evidence_from_turn(session, turn)
        task_id = 'task-' + records.digest([scope['tenant_id'], session_id, turn_id])[:24]
        payload = {'title': (title or turn['question'])[:200], 'objective': session['objective'], 'origin': handoff,
                   'evidence': [{'kind': 'qualified_unit', 'ref': r} for r in handoff['cited_refs']] + ([{'kind': 'receipt', 'ref': handoff['receipt_id']}] if handoff['receipt_id'] else []),
                   'sources': handoff['sources']}
    else:
        if not objective_text:
            raise HTTPException(422, 'A task needs an objective or a turn to begin from.')
        task_id = 'task-' + records.digest([scope['tenant_id'], scope['principal_id'], objective_text, records.now()])[:24]
        payload = {'title': (title or objective_text)[:200], 'objective': {'text': objective_text, 'sha256': _sha(objective_text), 'frozen_at': records.now()},
                   'origin': None, 'evidence': [], 'sources': []}
    if owner and owner != scope['principal_id'] and not records.is_operator(scope):
        raise HTTPException(403, 'Only an admitted operator can assign work to someone else.')
    if owner and await records.member(db, scope, owner) is None:
        raise HTTPException(404, 'That person is not a member of your estate.')
    await records.append(db, scope, 'task', task_id, 'created', {**payload, 'owner': owner or scope['principal_id'], 'due': due}, idempotent=True)
    return await load(db, scope, task_id)


async def mutate(db, scope, task_id, kind, payload):
    task = await load(db, scope, task_id)
    if not can_edit(scope, task):
        raise HTTPException(403, 'Only the owner, a listed contributor or an admitted operator can change this task.')
    if kind == 'assigned':
        if scope['principal_id'] not in (task['owner'], task['created_by']) and not records.is_operator(scope):
            raise HTTPException(403, 'Only the owner or an admitted operator can reassign work.')
        if await records.member(db, scope, payload['owner']) is None:
            raise HTTPException(404, 'That person is not a member of your estate.')
    if kind == 'contributor_added' and await records.member(db, scope, payload['contributor']) is None:
        raise HTTPException(404, 'That person is not a member of your estate.')
    if kind == 'state' and payload['state'] not in STATES:
        raise HTTPException(422, f'State must be one of {STATES}.')
    if kind in ('item_added', 'question_added'):
        payload = {**payload, f"{'item' if kind == 'item_added' else 'question'}_id": 'wi-' + records.digest([task_id, kind, payload.get('label') or payload.get('text'), records.now()])[:12]}
    await records.append(db, scope, 'task', task_id, kind, payload)
    return await load(db, scope, task_id)


async def mark_stale(db, scope, task, *, reason_code, artifact_refs, revocation_ref):
    await records.append(db, scope, 'task', task['task_id'], 'stale', {'reason_code': reason_code, 'artifact_refs': artifact_refs, 'revocation_ref': revocation_ref})
