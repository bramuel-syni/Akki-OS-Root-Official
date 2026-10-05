"""Measured routing (Mα MA-08 / Doc 11 LC2). A role's model is chosen on measured task evidence, not catalogue rank: every eligible candidate
runs the SAME fixed, versioned task set through the SAME Shield chokepoint (purpose `routing.candidate_trial`; licensed aggregates and
SYNTHETIC briefs only — Mode B, no privileged originals), is scored by the deterministic acceptance the production purpose already uses,
and is measured for latency and tokens. Cost is the owner-supplied token rate when one exists, otherwise honestly unknown. The lowest-cost
candidate that meets every floor is RECOMMENDED; an operator ADOPTS it (planner/reviewer families must stay distinct). Decisions are
reproducible from the stored trial; nothing in the trial changes production routing by itself."""
import asyncio
import json
import logging
import os
import time
import uuid

from services.training_lab import store as lab

log = logging.getLogger(__name__)
PURPOSE = 'routing.candidate_trial'
TASK_SET_VERSION = 'planner-caas-v2'  # v2: acceptance gate normalises figures numerically and ignores clock times (06:00)
FLOORS = {'pass_rate': 1.0, 'json_rate': 1.0, 'latency_ms_p50_max': 120000, 'refusals_max': 0}
DEFAULT_CANDIDATES = {
    'planner': [{'model': 'gpt-6-astra', 'provider': 'openai'}, {'model': 'gpt-5.4-mini', 'provider': 'openai'}, {'model': 'claude-sonnet-5-5', 'provider': 'anthropic'},
                {'model': 'claude-haiku-4-5-20251001', 'provider': 'anthropic'}, {'model': 'gemini-3-flash-preview', 'provider': 'gemini'}],
}
# SYNTHETIC briefs — fixed so every candidate sees identical work; figures inside are deliberately absent so acceptance can catch invented numbers.
TASKS = {
    'planner': [
        {'task_id': 'T08-1', 'product': 'domain.marketing_brief', 'brief': {'objective': 'Launch a mobile-money savings product to rural listeners in Kikuyu and Kamba', 'brand': 'SYNTHETIC Akiba Save', 'period': 'next quarter', 'constraint': 'radio only; no presenter endorsements'}},
        {'task_id': 'T08-2', 'product': 'domain.media_plan', 'brief': {'objective': 'Allocate a radio schedule across Kiswahili, Kikuyu and Kamba stations for a cooking-oil brand', 'brand': 'SYNTHETIC Golden Drop', 'period': 'eight weeks', 'constraint': 'morning and evening dayparts only'}},
        {'task_id': 'T08-3', 'product': 'domain.campaign_strategy', 'brief': {'objective': 'Grow brand recall for an agricultural input retailer among smallholder farmers', 'brand': 'SYNTHETIC Shamba Plus', 'period': 'planting season', 'constraint': 'three languages; measurable through radio brand mentions'}},
    ],
}


def db():
    database = lab.db()
    database.routing_trials.create_index([('tenant_id', 1), ('trial_id', 1)], unique=True)
    database.routing_decisions.create_index('role', unique=True)  # one adopted decision per role for the deployment's licensing estate
    return database


def now():
    return lab.now()


def candidates(role):
    raw = os.environ.get(f'ROUTING_CANDIDATES_{role.upper()}')
    return json.loads(raw) if raw else DEFAULT_CANDIDATES.get(role, [])


def _cost(model, tokens_in, tokens_out):
    from services.cost_ledger.rates import rate_for_model
    rate = rate_for_model(model) or {}
    if not rate or 'placeholder' in str(rate.get('source', '')).lower(): return None, 'no owner-supplied token rate for this model; tokens are measured, money is not invented'
    usd = tokens_in / 1e6 * float(rate.get('rate_per_million_tokens_in', 0)) + tokens_out / 1e6 * float(rate.get('rate_per_million_tokens_out', 0))
    return round(usd, 6), f"owner-supplied rate ({rate.get('source')})"


async def _run_task(tenant, actor, trial_id, cand, task, context):
    from services.caas import service as caas
    from services.chokepoint.llm import invoke
    from services.synisense.shield import stage
    spec = caas.PRODUCTS[task['product']]
    system = ('You produce a ' + spec['title'] + ' for a radio advertiser. Answer as strict JSON with exactly these top-level keys: ' + ', '.join(spec['sections']) +
              '. Each value is a short British-English paragraph or a list of short items. Use ONLY the figures given in context; if a figure is not given, say so rather than estimate. '
              'Never name an individual presenter or quote any recording. Answer with the JSON object only.')
    t0 = time.perf_counter(); row = {'task_id': task['task_id'], 'product': task['product']}
    try:
        artifact = await stage.stage(question=json.dumps({'brief': task['brief'], 'required_sections': spec['sections']}, default=str), data=json.dumps({'licensed_context': context}, default=str), tenant_id=tenant, purpose=PURPOSE, actor=actor, system_message=system,
                                     session_id=f"routing:{trial_id}:{cand['model']}:{task['task_id']}")
        r = await invoke(purpose=PURPOSE, safe_artifact=artifact, masking_tier='llm_prompt_governed_text', actor=actor, model=cand['model'], provider='emergent', tenant_id=tenant, custody_class='tenant_estate', session_id=f"routing:{trial_id}:{cand['model']}:{task['task_id']}")
        raw = (r.text or '').strip()
        if raw.startswith('```'): raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
        start, end = raw.find('{'), raw.rfind('}')
        try: deliverable = json.loads(raw[start:end + 1])
        except ValueError:
            from json_repair import repair_json
            try: deliverable = json.loads(repair_json(raw[start:end + 1]))
            except Exception: deliverable = None
        acceptance = caas.accept(task['product'], deliverable, {'brief': task['brief'], 'context': context})
        row.update(status='answered', json_valid=isinstance(deliverable, dict), accepted=acceptance['accepted'], findings=acceptance['findings'], tokens_in=r.tokens_in, tokens_out=r.tokens_out, latency_ms=r.latency_ms or int((time.perf_counter() - t0) * 1000), receipt_id=r.receipt_id, model_id=r.model_id)
    except Exception as exc:
        row.update(status='refused', json_valid=False, accepted=False, findings=[f'{type(exc).__name__}: {str(exc)[:200]}'], tokens_in=0, tokens_out=0, latency_ms=int((time.perf_counter() - t0) * 1000), receipt_id=None)
    return row


def _summarise(cand, rows, incumbent):
    answered = [r for r in rows if r['status'] == 'answered']; lat = sorted(r['latency_ms'] for r in rows)
    tin, tout = sum(r['tokens_in'] for r in rows), sum(r['tokens_out'] for r in rows)
    cost, cost_basis = _cost(cand['model'], tin, tout)
    s = {'model': cand['model'], 'provider': cand['provider'], 'incumbent': cand['model'] == incumbent, 'tasks': rows, 'n': len(rows), 'pass_rate': round(sum(1 for r in rows if r['accepted']) / len(rows), 4) if rows else None,
         'json_rate': round(sum(1 for r in rows if r['json_valid']) / len(rows), 4) if rows else None, 'refusals': len(rows) - len(answered), 'latency_ms_p50': lat[len(lat) // 2] if lat else None, 'tokens_in': tin, 'tokens_out': tout, 'cost_usd': cost, 'cost_basis': cost_basis}
    s['meets_floors'] = bool(rows) and s['pass_rate'] >= FLOORS['pass_rate'] and s['json_rate'] >= FLOORS['json_rate'] and s['latency_ms_p50'] <= FLOORS['latency_ms_p50_max'] and s['refusals'] <= FLOORS['refusals_max']
    return s


def _recommend(summaries):
    """Lowest known cost among candidates meeting every floor; when no cost is known, fewest output tokens is the disclosed proxy (never a quality claim)."""
    eligible = [s for s in summaries if s['meets_floors']]
    if not eligible: return {'model': None, 'basis': 'no candidate met every floor on this task set; the incumbent assignment stands', 'eligible': []}
    priced = [s for s in eligible if s['cost_usd'] is not None]
    if priced and len(priced) == len(eligible):
        best = min(priced, key=lambda s: (s['cost_usd'], s['latency_ms_p50'])); basis = 'lowest owner-priced cost among candidates meeting every floor (Doc 11 LC2)'
    else:
        best = min(eligible, key=lambda s: (s['tokens_out'] + s['tokens_in'], s['latency_ms_p50'])); basis = 'cost unknown for at least one eligible candidate (no owner token rate): fewest measured tokens is the disclosed proxy, then latency'
    return {'model': best['model'], 'provider': best['provider'], 'basis': basis, 'eligible': [s['model'] for s in eligible], 'cost_known_for_all': bool(priced) and len(priced) == len(eligible)}


async def _execute(tenant, actor, trial_id, role, cands, tasks, context, incumbent):
    try:
        results = await asyncio.gather(*[asyncio.gather(*[_run_task(tenant, actor, trial_id, c, t, context) for t in tasks]) for c in cands])
        summaries = [_summarise(c, list(rows), incumbent) for c, rows in zip(cands, results)]
        db().routing_trials.update_one({'tenant_id': tenant, 'trial_id': trial_id}, {'$set': {'candidates': summaries, 'recommendation': _recommend(summaries), 'finished_at': now(), 'status': 'measured'}})
    except Exception as exc:  # the trial record keeps the failure; nothing is retried silently
        log.exception('routing trial %s failed', trial_id)
        db().routing_trials.update_one({'tenant_id': tenant, 'trial_id': trial_id}, {'$set': {'status': 'failed', 'reason': f'{type(exc).__name__}: {str(exc)[:300]}', 'finished_at': now()}})


async def run_trial(tenant, actor, role):
    """Records the trial at once (state `running`) and measures in the background: 15 metered calls take longer than the ingress allows."""
    from services.caas import service as caas
    from services.chokepoint.model_roles import resolve
    tasks = TASKS.get(role)
    if not tasks: raise ValueError(f'No fixed task set is defined for the {role} role yet; a trial without a task set would be catalogue rank, not evidence')
    cands = candidates(role)
    if len(cands) < 2: raise ValueError('A trial needs at least two eligible candidates')
    _settle_stale(tenant)
    if db().routing_trials.find_one({'tenant_id': tenant, 'role': role, 'status': 'running'}): raise ValueError('A trial for this role is already running; wait for it to settle')
    incumbent = resolve(role)['model']
    context = {'estate_language_inventory': caas._language_inventory(tenant), 'brand_mention_inventory': caas._brand_inventory(tenant), 'prior_deliveries': []}
    trial_id = 'rt-' + uuid.uuid4().hex[:10]
    doc = {'trial_id': trial_id, 'tenant_id': tenant, 'role': role, 'purpose_measured': 'caas.domain_deliverable', 'task_set_version': TASK_SET_VERSION, 'tasks': [{'task_id': t['task_id'], 'product': t['product'], 'brief': t['brief']} for t in tasks],
           'floors': FLOORS, 'incumbent': incumbent, 'candidates': [{'model': c['model'], 'provider': c['provider'], 'incumbent': c['model'] == incumbent, 'meets_floors': None} for c in cands], 'recommendation': None,
           'context_basis': {k: (v.get('source') if isinstance(v, dict) else None) for k, v in context.items() if k != 'prior_deliveries'},
           'shield': 'every call crosses the sole chokepoint under purpose routing.candidate_trial with the governed-text masking tier; briefs are SYNTHETIC; context is licensed aggregates only',
           'started_at': now(), 'finished_at': None, 'run_by': actor, 'status': 'running', 'adopted': None}
    db().routing_trials.insert_one(dict(doc))
    asyncio.create_task(_execute(tenant, actor, trial_id, role, cands, tasks, context, incumbent))
    return {k: v for k, v in doc.items() if k != '_id'}


STALE_RUNNING_SECONDS = 600


def _settle_stale(tenant):
    """A trial runs inside the API process; a restart before it settles leaves `running` behind. Reads mark it interrupted so it can be re-run."""
    from datetime import datetime, timedelta, timezone
    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=STALE_RUNNING_SECONDS)).isoformat()
    db().routing_trials.update_many({'tenant_id': tenant, 'status': 'running', 'started_at': {'$lt': cutoff}}, {'$set': {'status': 'interrupted', 'reason': 'process restarted before the trial settled; no result was recorded — run it again', 'finished_at': now()}})


def trials(tenant, role=None, limit=20):
    _settle_stale(tenant)
    q = {'tenant_id': tenant, **({'role': role} if role else {})}
    return list(db().routing_trials.find(q, {'_id': 0, 'candidates.tasks': 0}, sort=[('started_at', -1)], limit=limit))


def trial(tenant, trial_id):
    _settle_stale(tenant)
    return db().routing_trials.find_one({'tenant_id': tenant, 'trial_id': trial_id}, {'_id': 0})


def adopt(tenant, actor, trial_id, model, note=None):
    from services.chokepoint.model_roles import ROLES, resolve
    t = trial(tenant, trial_id)
    if not t: raise LookupError('No routing trial with that reference in this estate')
    if t['status'] != 'measured': raise ValueError(f"Only a measured trial can be adopted; this one is {t['status']}")
    s = next((c for c in t['candidates'] if c['model'] == model), None)
    if not s: raise ValueError('That model was not a candidate in this trial')
    if not s['meets_floors']: raise ValueError('A candidate that did not meet every floor cannot be adopted; the floors are the task contract')
    others = {r: resolve(r) for r in ROLES if r != t['role']}
    if t['role'] == 'planner' and others['reviewer']['sdk_provider'] == s['provider']: raise ValueError('Planner and reviewer must come from different families (owner order 2026-10-02)')
    if t['role'] == 'reviewer' and (others['planner']['sdk_provider'] == s['provider'] or others['assistant']['sdk_provider'] == s['provider']): raise ValueError('Reviewer must differ in family from planner and assistant (owner order 2026-10-02)')
    decision = {'tenant_id': tenant, 'role': t['role'], 'model': model, 'sdk_provider': s['provider'], 'trial_id': trial_id, 'task_set_version': t['task_set_version'], 'measured': {k: s[k] for k in ('pass_rate', 'json_rate', 'latency_ms_p50', 'tokens_in', 'tokens_out', 'cost_usd', 'cost_basis')},
                'adopted_by': actor, 'adopted_at': now(), 'note': note, 'supersedes': (db().routing_decisions.find_one({'role': t['role']}, {'_id': 0, 'model': 1, 'trial_id': 1, 'adopted_at': 1}) or None)}
    db().routing_decisions.replace_one({'role': t['role']}, decision, upsert=True)
    db().routing_trials.update_one({'tenant_id': tenant, 'trial_id': trial_id}, {'$set': {'adopted': {'model': model, 'by': actor, 'at': decision['adopted_at']}}})
    return {k: v for k, v in decision.items() if k != '_id'}


def revert(tenant, actor, role, note=None):
    d = db().routing_decisions.find_one_and_delete({'role': role, 'tenant_id': tenant}, {'_id': 0})
    if not d: raise LookupError('No adopted routing decision for that role')
    db().routing_trials.update_one({'tenant_id': tenant, 'trial_id': d['trial_id']}, {'$set': {'adopted': None, 'reverted': {'by': actor, 'at': now(), 'note': note}}})
    return d


def decision(role):
    try: return lab.db().routing_decisions.find_one({'role': role}, {'_id': 0})
    except Exception as exc:  # the register must never take the chokepoint down
        log.warning('routing decision read failed: %s', exc); return None


def assignments(tenant):
    from services.chokepoint.model_roles import assignments as configured
    table = configured()
    out = []
    for r in table['roles']:
        d = decision(r['role'])
        out.append({**r, 'decision': d, 'task_set_defined': r['role'] in TASKS, 'candidates': candidates(r['role'])})
    return {**table, 'roles': out, 'floors': FLOORS, 'task_set_version': TASK_SET_VERSION}
