"""Answer-quality evaluation (M4-T4): a protected-reference benchmark run through the SAME journey the chat uses.

Every task is one real governed turn (`journey.ask`) in its own session, so the two paths — warm (qualified
units) and fresh/refused (nothing qualified) — are measured as they behave for a requester. References are
protected: each reference task is built from a qualified unit the requester may already read and graded by
whether that exact unit (by content digest) is cited. Every task ends in exactly one accounted outcome
(answered · narrow · refused · fresh · held · timeout · error); the buckets must sum to the task count.
Zero estate reads are asserted on every turn. Nothing here admits a model or changes the answering rule.
"""
import asyncio
import contextvars
import os
import random
import statistics
import uuid
from datetime import datetime, timezone

from core import db
from services.census_autonomy.operational_scope import sources_for
from services.chat import journey, sessions, spine
from services.commissioning import census_profile
from services.enforce.control_scope import bind_authenticated_request_scope
from services.enforce.principal_context_adapter import principal_context
from services.northena.execution_models import Held

COLLECTION = 'chat_evaluations'
RULE = 'chat.evaluation.v1'
TASK_TIMEOUT_S = int(os.environ.get('AKKI_CHAT_EVAL_TASK_TIMEOUT_S') or 120)
STALE_AFTER_S = 300
MIN_SIZE, MAX_SIZE, MAX_FRESH = 20, 400, 8
SEED_TERMS = [['cow', 'milk'], ['feed', 'minerals'], ['calf', 'breed'], ['disease', 'treatment'], ['price', 'market'],
              ['vaccine', 'vaccination'], ['pregnancy', 'insemination'], ['grass', 'fodder', 'water'], ['insurance', 'loan'],
              ['service', 'request'], ['farmer', 'training'], ['goat', 'chicken', 'poultry']]
OUT_OF_SCOPE = ['What is the weather forecast for Paris tomorrow?', 'Who won the football world cup in 2018?', 'How do I bake sourdough bread at home?',
                'What is the distance from the Earth to the Moon?', 'Explain how a jet engine works.', 'Which planet has the most moons?',
                'What is the capital city of Mongolia?', 'How tall is Mount Kilimanjaro?', 'Translate good morning into Japanese.',
                'What year did the Berlin Wall fall?', 'How many strings does a violin have?', 'What is the boiling point of mercury?',
                'Recommend a novel about sailing.', 'How do tides form in the ocean?', 'What is the square root of 1764?',
                'Describe the rules of chess castling.', 'Why is the sky blue at noon?', 'How long is a marathon in kilometres?',
                'What is the population of Iceland?', 'Name three composers of the baroque period.']
WEAK_MATCH = ['What is the best price for a used laptop?', 'How do I request a passport renewal?', 'Which breed of dog is calmest for apartments?',
              'How often should a car engine get an oil service?', 'What minerals are mined in Chile?', 'How much water does a swimming pool hold?',
              'What is the market cap of a technology company?', 'How do I treat a sunburn?', 'When is the best time to feed goldfish?',
              'Which insurance covers a rented bicycle?']
UNANSWERABLE = ('According to the training question record {region} {pk}={key}, how many litres of milk per day did the farmer report? '
                'Give the exact number from the record.')
FRESH = 'What does the {table} table in {database} hold? Summarise its {columns} columns.'
MIX = (('reference', 0.5), ('unanswerable', 0.15), ('out_of_scope', 0.15), ('weak_match', 0.10), ('fresh', 0.10))


def now():
    return datetime.now(timezone.utc).isoformat()


def _public(doc):
    doc = dict(doc)
    doc.pop('_id', None)
    return doc


def _record_text(unit):
    values = [str(v) for v in (unit.get('record') or {}).values() if isinstance(v, str)]
    return max(values, key=len) if values else ''


async def reference_pool(scope, artefacts):
    """Distinct qualified units (by content digest) the requester may already read; metadata plus the farmer text only."""
    pool = {}
    for terms in SEED_TERMS:
        read = await spine.read_candidates(db, scope, artefacts, terms)
        for c in read['candidates']:
            text = _record_text(c['unit'])
            if len(text) < 15 or c['content_sha256'] in pool:
                continue
            locator = c['unit']['provenance']['locator']
            pool[c['content_sha256']] = {'ref': c['ref'], 'content_sha256': c['content_sha256'], 'region': c['region'], 'text': text[:300],
                                         'pk': locator['primary_key'], 'key': locator['key_value']}
    return list(pool.values())


async def fresh_slices(scope, artefacts):
    qualified = {a['region'] for a in artefacts}
    out = []
    for source_id in sources_for(scope['tenant_id']):
        for row in (await census_profile.tables_for(scope['tenant_id'], source_id)) or []:
            if f"{row['database']}.{row['table']}" not in qualified and row['row_count'] > 0 and len(row['columns']) >= 2:
                out.append(row)
    return out


def _counts(size):
    counts = {name: int(size * share) for name, share in MIX}
    counts['fresh'] = min(counts['fresh'], MAX_FRESH)
    counts['reference'] += size - sum(counts.values())
    return counts


def build_tasks(size, seed, pool, slices):
    """Deterministic task set for a seed; references are drawn without replacement while the pool lasts."""
    rng = random.Random(seed)
    counts = _counts(size)
    refs = pool[:]
    rng.shuffle(refs)
    slices = slices[:]
    rng.shuffle(slices)
    tasks = []
    for i in range(counts['reference']):
        unit = refs[i % len(refs)] if refs else None
        if unit is None:
            tasks.append({'class': 'reference', 'question': 'No qualified unit was available to build a reference task.', 'expected': 'refused'})
            continue
        tasks.append({'class': 'reference', 'question': unit['text'], 'expected': 'warm', 'reference_sha256': unit['content_sha256'], 'reference_region': unit['region']})
    for i in range(counts['unanswerable']):
        unit = refs[(counts['reference'] + i) % len(refs)] if refs else None
        question = UNANSWERABLE.format(region=unit['region'], pk=unit['pk'], key=unit['key']) if unit else UNANSWERABLE.format(region='the estate', pk='id', key='?')
        tasks.append({'class': 'unanswerable', 'question': question, 'expected': 'not_sufficient', 'reference_region': unit['region'] if unit else None})
    tasks += [{'class': 'out_of_scope', 'question': OUT_OF_SCOPE[i % len(OUT_OF_SCOPE)], 'expected': 'refused'} for i in range(counts['out_of_scope'])]
    tasks += [{'class': 'weak_match', 'question': WEAK_MATCH[i % len(WEAK_MATCH)], 'expected': 'refused'} for i in range(counts['weak_match'])]
    for i in range(min(counts['fresh'], len(slices))):
        row = slices[i]
        tasks.append({'class': 'fresh', 'question': FRESH.format(table=row['table'], database=row['database'], columns=' and '.join(row['columns'][:2])),
                      'expected': 'fresh', 'reference_region': f"{row['database']}.{row['table']}"})
    for i, task in enumerate(tasks):
        task['task_id'] = f't{i + 1:03d}'
    return tasks


def bucket(turn):
    if turn.get('refused'):
        return 'refused'
    if turn['decision'] == 'fresh':
        return 'fresh'
    return 'answered' if turn.get('sufficient') else 'narrow'


def grade(task, turn):
    """Mechanical grading against the protected expectation; the reason is always stated."""
    detail = turn.get('decision_detail') or {}
    grounding = (turn.get('evidence') or {}).get('grounding') or {}
    cited = (turn.get('evidence') or {}).get('cited_refs') or []
    selected = ((turn.get('evidence') or {}).get('window') or {}).get('selected') or []
    if task['class'] == 'reference':
        hit = any(s['content_sha256'] == task['reference_sha256'] for s in selected if s['ref'] in cited)
        in_window = any(s['content_sha256'] == task['reference_sha256'] for s in selected)
        if turn.get('refused'):
            return False, f"refused: {turn.get('refusal_reason', '')[:160]}", {'reference_in_window': in_window, 'reference_cited': False}
        if turn['decision'] != 'warm':
            return False, f"routed {turn['decision']} instead of warm", {'reference_in_window': False, 'reference_cited': False}
        return hit, 'reference unit cited' if hit else ('reference in window but not cited' if in_window else 'reference not retrieved into the window'), \
            {'reference_in_window': in_window, 'reference_cited': hit}
    if task['class'] == 'unanswerable':
        if turn.get('refused'):
            return True, 'refused rather than invented', {}
        invented = bool(turn.get('sufficient')) and not grounding.get('unsupported')
        return not invented, 'declared insufficient or unsupported' if not invented else 'answered as sufficient with nothing in the window to support a figure', {}
    if task['class'] in ('out_of_scope', 'weak_match'):
        if turn.get('refused') and turn['decision'] == 'refused':
            aside = (detail.get('subject_match') or {}).get('weak_regions') or []
            return True, f"refused; {len(aside)} loose region(s) set aside" if aside else 'refused', {'set_aside': aside}
        return False, f"routed {turn['decision']} for an off-subject question", {}
    if task['class'] == 'fresh':
        draft = detail.get('draft') or {}
        if turn['decision'] == 'fresh' and draft.get('draft_id'):
            return True, f"fresh slice drafted ({draft['draft_id']})", {'draft_id': draft['draft_id']}
        return False, f"decision {turn['decision']} without a draft", {}
    return False, 'unknown task class', {}


def _percentile(values, p):
    if not values:
        return None
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round((p / 100) * (len(ordered) - 1))))]


def summarize(tasks):
    buckets = {b: 0 for b in ('answered', 'narrow', 'refused', 'fresh', 'held', 'timeout', 'error')}
    by_class = {}
    latencies, tokens_in, tokens_out, hits, misses = [], 0, 0, 0, 0
    grounding = {}
    for t in tasks:
        buckets[t['outcome']] += 1
        c = by_class.setdefault(t['class'], {'tasks': 0, 'passed': 0})
        c['tasks'] += 1
        c['passed'] += 1 if t.get('passed') else 0
        if t.get('latency_ms') is not None:
            latencies.append(t['latency_ms'])
        tokens_in += t.get('tokens_in') or 0
        tokens_out += t.get('tokens_out') or 0
        hits += (t.get('memory') or {}).get('hits') or 0
        misses += (t.get('memory') or {}).get('misses') or 0
        if t.get('grounding'):
            grounding[t['grounding']] = grounding.get(t['grounding'], 0) + 1
    refs = [t for t in tasks if t['class'] == 'reference' and t['outcome'] not in ('timeout', 'error', 'held')]
    return {'tasks': len(tasks), 'buckets': buckets, 'accounted': sum(buckets.values()) == len(tasks), 'by_class': by_class,
            'passed': sum(1 for t in tasks if t.get('passed')), 'pass_rate': round(sum(1 for t in tasks if t.get('passed')) / len(tasks), 4) if tasks else None,
            'reference_hit_rate': round(sum(1 for t in refs if t.get('reference_cited')) / len(refs), 4) if refs else None,
            'reference_retrieval_rate': round(sum(1 for t in refs if t.get('reference_in_window')) / len(refs), 4) if refs else None,
            'paths': {'warm': sum(1 for t in tasks if t.get('decision') == 'warm'), 'fresh_or_refused': sum(1 for t in tasks if t.get('decision') in ('fresh', 'refused'))},
            'latency_ms': {'p50': _percentile(latencies, 50), 'p95': _percentile(latencies, 95), 'max': max(latencies) if latencies else None,
                           'mean': round(statistics.fmean(latencies)) if latencies else None},
            'tokens': {'in': tokens_in, 'out': tokens_out}, 'memory': {'hits': hits, 'misses': misses, 'hit_ratio': round(hits / (hits + misses), 4) if hits + misses else None},
            'grounding': grounding, 'source_dispatches': sum((t.get('reads') or {}).get('source_dispatches') or 0 for t in tasks),
            'source_rows_read': sum((t.get('reads') or {}).get('source_rows_read') or 0 for t in tasks)}


def _row(task, turn, started):
    evidence = turn.get('evidence') or {}
    passed, reason, extra = grade(task, turn)
    return {**task, 'outcome': bucket(turn), 'decision': turn['decision'], 'refused': bool(turn.get('refused')), 'passed': passed, 'reason': reason, **extra,
            'grounding': (evidence.get('grounding') or {}).get('grounding'), 'sufficient': turn.get('sufficient'), 'cited': len(evidence.get('cited_refs') or []),
            'candidates': (evidence.get('reads') or {}).get('candidates_returned'), 'reads': {k: (evidence.get('reads') or {}).get(k) for k in ('source_dispatches', 'source_rows_read', 'qualified_store_calls')},
            'memory': {k: (evidence.get('memory') or {}).get(k) for k in ('hits', 'misses')} if evidence.get('memory') else None,
            'latency_ms': turn.get('latency_ms_total'), 'tokens_in': turn.get('tokens_in'), 'tokens_out': turn.get('tokens_out'),
            'turn_id': turn['turn_id'], 'ledger_row_id': (turn.get('decision_detail') or {}).get('ledger_row_id'), 'receipt_id': turn.get('receipt_id'),
            'started_at': started, 'finished_at': now()}


async def _run_task(scope, task):
    started = now()
    session = await sessions.create(scope, task['question'], title=f"Evaluation · {task['task_id']} · {task['class']}")
    await sessions.update(scope, session['session_id'], {'archived': True, 'evaluation': True})
    try:
        result = await asyncio.wait_for(journey.ask(db, scope, question=task['question'], session_id=session['session_id']), TASK_TIMEOUT_S)
        row = _row(task, result['turn'], started)
    except asyncio.TimeoutError:
        row = {**task, 'outcome': 'timeout', 'passed': False, 'reason': f'no decision within {TASK_TIMEOUT_S} s', 'started_at': started, 'finished_at': now()}
    except Held as exc:
        row = {**task, 'outcome': 'held', 'passed': False, 'reason': exc.reason_code, 'started_at': started, 'finished_at': now()}
    except Exception as exc:  # accounted, never swallowed: the error is the result of this task
        row = {**task, 'outcome': 'error', 'passed': False, 'reason': f'{type(exc).__name__}: {str(exc)[:160]}', 'started_at': started, 'finished_at': now()}
    row['session_id'] = session['session_id']
    return row


async def _run(evaluation_id, scope, size, seed):
    with principal_context(scope['principal_id']), bind_authenticated_request_scope(scope):
        try:
            doc = await db[COLLECTION].find_one({'evaluation_id': evaluation_id})
            if not doc.get('plan'):
                artefacts = await spine.verified_artefacts(db, scope)
                pool = await reference_pool(scope, artefacts)
                slices = await fresh_slices(scope, artefacts)
                plan = build_tasks(size, seed, pool, slices)
                await db[COLLECTION].update_one({'evaluation_id': evaluation_id}, {'$set': {
                    'plan': plan, 'planned': len(plan), 'artefacts': len(artefacts), 'reference_pool': len(pool), 'fresh_candidates': len(slices), 'updated_at': now()}})
            else:
                plan = doc['plan']
            done = len(doc.get('tasks') or [])
            for task in plan[done:]:
                row = await _run_task(scope, task)
                await db[COLLECTION].update_one({'evaluation_id': evaluation_id}, {'$push': {'tasks': row}, '$set': {'updated_at': now()}})
            doc = await db[COLLECTION].find_one({'evaluation_id': evaluation_id})
            summary = summarize(doc['tasks'])
            await db[COLLECTION].update_one({'evaluation_id': evaluation_id}, {'$set': {'state': 'completed', 'summary': summary, 'finished_at': now(), 'updated_at': now()}})
        except Exception as exc:
            await db[COLLECTION].update_one({'evaluation_id': evaluation_id}, {'$set': {'state': 'aborted', 'reason': f'{type(exc).__name__}: {str(exc)[:200]}', 'finished_at': now(), 'updated_at': now()}})


def _launch(evaluation_id, scope, size, seed):
    asyncio.get_running_loop().create_task(_run(evaluation_id, dict(scope), size, seed), context=contextvars.Context())


async def resume_all():
    """At process start every run still marked running continues from its next planned task (process restarts are
    recorded as `resumed`, never hidden); nothing completed is re-run."""
    resumed = []
    async for doc in db[COLLECTION].find({'state': 'running'}):
        if not doc.get('scope'):
            await db[COLLECTION].update_one({'evaluation_id': doc['evaluation_id']}, {'$set': {'state': 'aborted', 'reason': 'no requester scope recorded; cannot resume', 'updated_at': now()}})
            continue
        await db[COLLECTION].update_one({'evaluation_id': doc['evaluation_id']}, {'$inc': {'resumed': 1}, '$set': {'updated_at': now()}})
        _launch(doc['evaluation_id'], doc['scope'], doc['requested'], doc['seed'])
        resumed.append(doc['evaluation_id'])
    return resumed


def _effective_state(doc):
    if doc['state'] == 'running':
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(doc['updated_at'])).total_seconds()
        if age > STALE_AFTER_S:
            return 'interrupted'
    return doc['state']


def view(doc, *, tasks=False):
    out = {k: v for k, v in _public(doc).items() if k not in ('plan', 'scope') and (tasks or k != 'tasks')}
    out['state'] = _effective_state(doc)
    out['completed_tasks'] = len(doc.get('tasks') or [])
    if out['state'] == 'interrupted':
        out['reason'] = 'The evaluation stopped reporting; it resumes from its next planned task when the service restarts. Completed tasks are kept.'
        out['summary'] = summarize(doc['tasks']) if doc.get('tasks') else None
    return out


async def listing(scope):
    cursor = db[COLLECTION].find({'tenant_id': scope['tenant_id']}).sort('created_at', -1).limit(20)
    return [view(doc) async for doc in cursor]


async def get(scope, evaluation_id):
    doc = await db[COLLECTION].find_one({'evaluation_id': evaluation_id, 'tenant_id': scope['tenant_id']})
    return view(doc, tasks=True) if doc else None


async def start(scope, *, size, seed):
    size = max(MIN_SIZE, min(MAX_SIZE, int(size)))
    running = await db[COLLECTION].find_one({'tenant_id': scope['tenant_id'], 'state': 'running'})
    if running and _effective_state(running) == 'running':
        raise Held('CHAT_EVALUATION_ALREADY_RUNNING')
    doc = {'evaluation_id': 'ce-' + uuid.uuid4().hex[:12], 'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id'], 'rule': RULE,
           'scope': {'tenant_id': scope['tenant_id'], 'principal_id': scope['principal_id'], 'roles': list(scope.get('roles') or [])},
           'requested': size, 'seed': seed, 'state': 'running', 'tasks': [], 'summary': None, 'created_at': now(), 'updated_at': now(),
           'model': journey.DEFAULT_MODEL, 'provider': journey.DEFAULT_PROVIDER, 'task_timeout_s': TASK_TIMEOUT_S,
           'mix': dict(MIX), 'grading': 'mechanical: reference unit cited by content digest · unanswerable not answered as sufficient · '
                                      'off-subject refused · fresh slice drafted; model text quality is not judged'}
    await db[COLLECTION].insert_one(dict(doc))
    _launch(doc['evaluation_id'], doc['scope'], size, seed)
    return view(doc)
