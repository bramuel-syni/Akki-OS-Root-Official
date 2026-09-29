"""Goals with a STATED measure. Progress changes only when a permitted person records a measured value with its
evidence reference; task completion never moves a goal (unmeasured performance is not fabricated). Tasks link to
goals as initiatives; the link is visible, not a number."""
from fastapi import HTTPException

from services.work import records

STATUSES = ('unmeasured', 'behind', 'on_track', 'met')


def status_of(measure, now):
    if now is None or measure.get('target') is None:
        return 'unmeasured'
    target, value, direction = float(measure['target']), float(now['value']), measure.get('direction', 'at_least')
    met = value >= target if direction == 'at_least' else value <= target
    if met:
        return 'met'
    baseline = measure.get('baseline')
    if baseline is None or float(baseline) == target:
        return 'behind'
    progress = (value - float(baseline)) / (target - float(baseline))
    return 'on_track' if progress >= float(measure.get('on_track_from') or 0.5) else 'behind'


def current(rows):
    goal = None
    for e in rows:
        p = e['payload']
        if p['kind'] == 'created':
            goal = {'goal_id': e['row']['run_id'], 'created_by': p['principal_id'], 'created_at': p['at'], 'title': p['title'], 'type': p.get('type') or 'objective',
                    'measure': p['measure'], 'owner': p.get('owner') or p['principal_id'], 'by_date': p.get('by_date'), 'measurements': [], 'task_ids': [],
                    'contributors': [], 'history': []}
        if goal is None:
            continue
        if p['kind'] == 'measured':
            goal['measurements'].append({'value': p['value'], 'evidence_ref': p['evidence_ref'], 'note': p.get('note'), 'by': p['principal_id'], 'at': p['at'], 'receipt_hash': e['row']['hash']})
        elif p['kind'] == 'task_linked' and p['task_id'] not in goal['task_ids']:
            goal['task_ids'].append(p['task_id'])
        elif p['kind'] == 'contributor_added':
            goal['contributors'] = [c for c in goal['contributors'] if c['principal_id'] != p['contributor']] + [{'principal_id': p['contributor'], 'role': p['role']}]
        elif p['kind'] == 'owner':
            goal['owner'] = p['owner']
        goal['history'].append(records.history_entry(e))
    if goal:
        now = goal['measurements'][-1] if goal['measurements'] else None
        goal.update({'now': now, 'status': status_of(goal['measure'], now)})
    return goal


async def load(db, scope, goal_id):
    goal = current(await records.events(db, scope, 'goal', goal_id))
    if goal is None:
        raise HTTPException(404, 'No such goal in your estate.')
    return goal


async def listing(db, scope):
    rows = [current(evs) for evs in records.grouped(await records.events(db, scope, 'goal')).values()]
    return sorted((g for g in rows if g), key=lambda g: g['created_at'], reverse=True)


def _permitted(scope, goal):
    return scope['principal_id'] in {goal['owner'], goal['created_by'], *(c['principal_id'] for c in goal['contributors'])} or records.is_operator(scope)


async def create(db, scope, *, title, measure, type_='objective', owner=None, by_date=None):
    if not records.is_operator(scope):
        raise HTTPException(403, 'Only an admitted operator can state a company goal.')
    if not measure.get('name') or measure.get('target') is None:
        raise HTTPException(422, 'A goal needs a named measure and a target; progress is never inferred.')
    if owner and await records.member(db, scope, owner) is None:
        raise HTTPException(404, 'That person is not a member of your estate.')
    goal_id = 'goal-' + records.digest([scope['tenant_id'], title, measure, records.now()])[:24]
    await records.append(db, scope, 'goal', goal_id, 'created', {'title': title[:200], 'type': type_, 'measure': measure, 'owner': owner or scope['principal_id'], 'by_date': by_date})
    return await load(db, scope, goal_id)


async def measure(db, scope, goal_id, *, value, evidence_ref, note=None):
    goal = await load(db, scope, goal_id)
    if not _permitted(scope, goal):
        raise HTTPException(403, 'Only the goal owner, a listed contributor or an admitted operator can record a measurement.')
    if not evidence_ref:
        raise HTTPException(422, 'A measurement needs the evidence it was read from.')
    await records.append(db, scope, 'goal', goal_id, 'measured', {'value': float(value), 'evidence_ref': evidence_ref, 'note': note})
    return await load(db, scope, goal_id)


async def mutate(db, scope, goal_id, kind, payload):
    goal = await load(db, scope, goal_id)
    if not _permitted(scope, goal):
        raise HTTPException(403, 'Only the goal owner or an admitted operator can change this goal.')
    for key in ('contributor', 'owner'):
        if key in payload and await records.member(db, scope, payload[key]) is None:
            raise HTTPException(404, 'That person is not a member of your estate.')
    await records.append(db, scope, 'goal', goal_id, kind, payload)
    return await load(db, scope, goal_id)
