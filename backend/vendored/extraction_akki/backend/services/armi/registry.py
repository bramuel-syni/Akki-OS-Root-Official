"""ARMI — Agent Resource Management Interface. One operational profile per admitted agent, model, LLM role, worker or skill: job description,
objective served, capabilities and limits, admission record, compliance (share of governed crossings and gates passed), resources consumed,
work completed, collaborators and contribution. Every displayed score names its evidence basis and sample size. Watch behavioural profiles
are never exported here (Watch W13) and no malicious-conduct probability is invented. Lifecycle: onboard → bind versions → assign → complete →
score → suspend/revoke; every transition is on the record. Tenant-scoped throughout."""
import glob
import hashlib
import json
import logging
import re
import uuid

from services.training_lab import store as lab

log = logging.getLogger(__name__)
STATUSES = ('onboarded', 'active', 'suspended', 'revoked')
NOT_COMPUTED = 'not computed — Watch W13 prohibits repurposing protected behavioural profiles for management scoring; no probability is invented'


def db():
    database = lab.db()
    database.armi_agents.create_index([('tenant_id', 1), ('agent_id', 1)], unique=True)
    database.armi_assignments.create_index([('tenant_id', 1), ('assignment_id', 1)], unique=True)
    database.armi_assignments.create_index([('tenant_id', 1), ('agent_id', 1), ('at', -1)])
    return database


def now():
    return lab.now()


def _score(passed, total, basis):
    return {'value': round(passed / total, 4) if total else None, 'passed': passed, 'n': total, 'basis': basis, 'evidence_class': 'measured' if total else 'not_measured'}


def _profile(tenant, agent_id, kind, name, **fields):
    base = {'agent_id': agent_id, 'tenant_id': tenant, 'kind': kind, 'name': name, 'status': 'active',
            'behaviour': {'watch_profile_exported': False, 'malicious_conduct_probability': NOT_COMPUTED},
            'contribution': {'revenue_attributed_usd': None, 'revenue_note': 'no attributed revenue is on the Cost Ledger yet; nothing is estimated here'}}
    base.update(fields)
    return base


# ----------------------------------------------------------------------------- derivation from native records (evidence-backed, never invented)
def _caas_contribution(tenant):
    """Business contribution from metered CaaS deliveries. Rule: one delivery credits at most ONE identity — the authoring LLM role named on the delivery
    record; deterministic aggregates credit no agent. Amounts are the rates frozen on the metered events, so shares can never exceed what was metered."""
    from services.caas import service as caas
    rows = list(caas.db().caas_deliveries.find({'tenant_id': tenant}, {'_id': 0, 'delivery_id': 1, 'product': 1, 'accepted': 1, 'authored': 1, 'meter_id': 1}))
    meters = {m['meter_id']: m for m in caas.db().caas_meter.find({'tenant_id': tenant}, {'_id': 0, 'meter_id': 1, 'cost_usd': 1})}
    by_agent, unattributed = {}, {'deliveries': 0, 'amount_usd': 0.0, 'priced': 0}
    for d in rows:
        cost = (meters.get(d.get('meter_id')) or {}).get('cost_usd')
        model = (d.get('authored') or {}).get('model')
        if not model: unattributed['deliveries'] += 1; unattributed['amount_usd'] += cost or 0; unattributed['priced'] += cost is not None; continue
        c = by_agent.setdefault(f'llm:planner:{model}', {'deliveries': 0, 'accepted': 0, 'priced': 0, 'metered_amount_usd': 0.0, 'tokens_in': 0, 'tokens_out': 0})
        c['deliveries'] += 1; c['accepted'] += 1 if d.get('accepted') else 0; c['tokens_in'] += (d['authored'].get('tokens_in') or 0); c['tokens_out'] += (d['authored'].get('tokens_out') or 0)
        if cost is not None: c['priced'] += 1; c['metered_amount_usd'] += cost
    return by_agent, unattributed


def _contribution(by_agent, agent_id):
    c = by_agent.get(agent_id)
    if not c: return {'revenue_attributed_usd': None, 'deliveries': 0, 'evidence_class': 'not_measured', 'basis': 'no CaaS delivery names this identity as its author', 'rule': 'one delivery → one identity (the authoring role); aggregates credit no agent'}
    return {'revenue_attributed_usd': round(c['metered_amount_usd'], 2) if c['priced'] else None, 'deliveries': c['deliveries'], 'accepted': c['accepted'], 'priced_deliveries': c['priced'], 'unpriced_deliveries': c['deliveries'] - c['priced'], 'evidence_class': 'measured',
            'basis': f"{c['deliveries']} metered CaaS deliveries authored by this role ({c['accepted']} accepted); amounts are the rates frozen on the metered events", 'rule': 'one delivery → one identity (the authoring role); aggregates credit no agent',
            'revenue_note': None if c['priced'] else 'deliveries metered before a CaaS rate existed; count is measured, money is not invented'}


def _llm_roles(tenant):
    from services.chokepoint.model_roles import assignments
    from services.transform_forms.doc_studio import service as studio
    table = assignments(); out = []
    commissions = studio.list_commissions(tenant)
    released = sum(1 for c in commissions if (c.get('release') or {}).get('state') == 'clear'); total = len(commissions)
    receipts = glob.glob('/app/assessment_workspace/phase0/llm_crossings/**/*.json', recursive=True)
    by_agent, _ = _caas_contribution(tenant)
    for role in table['roles']:
        involved = {'planner': total, 'writer': total, 'reviewer': total, 'assistant': 0}[role['role']]
        agent_id = f"llm:{role['role']}:{role['model']}"; caas_c = by_agent.get(agent_id) or {}
        out.append(_profile(tenant, agent_id, 'llm', f"{role['model']} as {role['role']}", provider=role['sdk_provider'], version=role['model'],
                            jd={'role': role['role'], 'job': role['job'], 'strengths': [role['strength']], 'can_do': [role['job']], 'cannot_do': ['see privileged originals (Shield chokepoint, masked tiers only)', 'bind actual estate values (internal workers do)', 'start compute or admit models']},
                            objectives=['document studio releases', 'training-lab advisory'] + (['CaaS authored deliverables'] if caas_c else []), capabilities=[role['strength']], limits=['sole chokepoint; purpose allow-list; masking tier llm_prompt_governed_text'],
                            admission={'record': 'services/chokepoint/model_roles.py assignment table', 'decision': 'configured role', 'evaluation': table['evaluation']},
                            compliance=_score(released, involved, 'document commissions involving this role that reached release state clear') if involved else _score(0, 0, 'no commissions recorded for this role'),
                            resources={'crossing_receipts_on_disk': len(receipts), 'gpu_hours': 0.0, 'tokens_in': caas_c.get('tokens_in', 0), 'tokens_out': caas_c.get('tokens_out', 0), 'cost_usd': None, 'cost_note': 'token counts are from CaaS delivery receipts; no owner-supplied token rate for this model'},
                            work={'assignments_completed': released + caas_c.get('deliveries', 0), 'assignments_total': involved + caas_c.get('deliveries', 0), 'kind': 'document commissions' + (' and CaaS deliveries' if caas_c else '')},
                            contribution=_contribution(by_agent, agent_id),
                            collaborators=[{'agent_id': f"llm:{o['role']}:{o['model']}", 'shared': 'same commission pipeline'} for o in table['roles'] if o['role'] != role['role'] and o['role'] != 'assistant']))
    return out


def _trained_models(tenant):
    from services.training_runner import m9_serving
    out = []
    for a in m9_serving.models_view()['trained_adapters']:
        status = 'active' if (a.get('serving') or {}).get('status') == 'running' else ('revoked' if a.get('withdrawal') else 'onboarded')
        base = a.get('base'); base_label = base if isinstance(base, str) else (base or {}).get('registry_id') or 'registered base'
        name = f"Language identification · {'reduced' if a.get('variant') == 'pruned' else 'full'} adapter on {base_label}"
        out.append(_profile(tenant, f"model:{a['model_id']}", 'model', name, status=status, version=(a.get('artefact_sha256') or '')[:16], base=a.get('base'), host=a.get('host'), training_job_id=a['model_id'],
                            jd={'role': 'trained adapter', 'job': f"{a.get('variant') or 'adapter'} on {a.get('base')}", 'strengths': [], 'can_do': ['serve its admitted scope'], 'cannot_do': ['serve outside the admitted classes', 'be re-used without re-check']},
                            objectives=['estate language reading'], capabilities=[a.get('variant') or 'adapter'], limits=[f"re-check due {a.get('re_check_due_at')}" if a.get('re_check_due_at') else 'no re-check date recorded'],
                            admission={'record': a.get('training_job_id'), 'decision': a.get('status'), 'owner_ruling_ref': a.get('owner_ruling_ref'), 'connected_at': a.get('connected_at')},
                            compliance=_score(1 if a.get('status') in ('admitted', 'in_service', 'connected') else 0, 1, 'admission ceremony outcome for this artefact'),
                            resources={'gpu_hours': None, 'cited_units': a.get('cited_units'), 'cost_usd': None}, work={'assignments_completed': 0, 'kind': 'serving'}, collaborators=[]))
    return out


def _malpha(tenant):
    from services.training_lab import malpha
    out = []
    for c in malpha.commissions():
        for lane in c['lanes']:
            jobs = malpha.jobs(commission_id=c['commission_id'], lane=lane)
            done = [j for j in jobs if j['status'] == 'completed']; failed = [j for j in jobs if j['status'] in ('failed', 'interrupted', 'refused')]
            state = (c.get('lane_state') or {}).get(lane) or {}; priced = malpha.price_gpu(jobs)
            out.append(_profile(tenant, f"model:malpha:{c['commission_id']}:{lane}", 'model', f"{c['title']} — {lane}", status='active' if state.get('status') not in ('held',) else 'suspended', version=f"iteration {state.get('iteration', 0)}",
                                jd={'role': 'commissioned model under training', 'job': c['product'], 'strengths': [], 'can_do': ['improve autonomously against its frozen target'], 'cannot_do': ['read the sealed admission split', 'serve before independent admission']},
                                objectives=[c['title']], capabilities=c['languages'], limits=[f"budget {c['budget']['mode']}", 'speaker-cluster-disjoint sealed splits'],
                                admission={'record': (c.get('admitted') or {}).get(lane), 'decision': 'admitted' if (c.get('admitted') or {}).get(lane) else f"not yet admitted · lane {state.get('status', 'not started')}", 'target': c['target_outcome']['admission'] if lane == 'listener' else c['target_outcome']['admission'].get(lane)},
                                compliance=_score(len(done), len(done) + len(failed), 'lane jobs that settled with a verified receipt'), resources={'gpu_hours': round(sum((j.get('gpu_seconds') or 0) for j in jobs) / 3600, 3), 'cost_usd': priced['cost_usd'], 'cost_note': priced['cost_note'], 'jobs': len(jobs)},
                                work={'assignments_completed': len(done), 'assignments_failed': len(failed), 'latest_summary': state.get('summary'), 'kind': 'training iterations'},
                                collaborators=[{'agent_id': 'agent:akki-autopilot', 'shared': 'dispatch and settlement'}] + [{'agent_id': f"model:malpha:{c['commission_id']}:{o}", 'shared': 'same commission'} for o in c['lanes'] if o != lane]))
    return out


def _skills(tenant):
    from services.training_lab.reviewers import CATALOGUE
    out = []
    for name, call in (('evaluation-statistics', 'POST /api/training/lab/skills/statistics/invoke'), ('speech-music-decision', 'POST /api/training/lab/skills/music/invoke'), ('investment-scenarios', 'POST /api/training/lab/skills/value/invoke'), ('forecast-postmortem', 'POST /api/training/lab/skills/postmortem/invoke')):
        out.append(_profile(tenant, f'skill:{name}', 'skill', name, version=CATALOGUE['version'], jd={'role': 'deterministic callable skill', 'job': call, 'strengths': ['deterministic', 'no model spend'], 'can_do': [call], 'cannot_do': ['admit models', 'author prose']},
                            objectives=['training laboratory'], capabilities=['deterministic computation'], limits=['operator identity required'], admission={'record': 'training_lab skills catalogue', 'decision': 'installed'},
                            compliance=_score(0, 0, 'no invocation receipts aggregated yet'), resources={'gpu_hours': 0.0, 'cost_usd': 0.0}, work={'assignments_completed': 0, 'kind': 'invocations'}, collaborators=[]))
    return out


def _report_rate(d):
    """Testing-agent reports carry success_rate as a string or a per-surface dict ('100% (46/46 …)', 'N/A …'); the lowest reported surface counts."""
    raw = d.get('success_rate'); values = raw.values() if isinstance(raw, dict) else [raw]
    found = []
    for v in values:
        m = re.search(r'(\d+(?:\.\d+)?)\s*%', str(v or ''))
        if m: found.append(min(float(m.group(1)) / 100, 1.0))
    return min(found) if found else None


def _agents(tenant):
    reports = sorted(glob.glob('/app/test_reports/iteration_*.json'))
    passed = 0; rates = []
    for p in reports:
        try: d = json.load(open(p))
        except Exception: continue
        rate = _report_rate(d)
        if rate is not None: rates.append(rate); passed += 1 if rate >= 0.9 and not d.get('retest_needed') else 0
    e1 = _profile(tenant, 'agent:E1', 'agent', 'E1 (Emergent full-stack engineer)', version='E1', jd={'role': 'software developer', 'job': 'builds and verifies Akki OS features under owner orders; dispatches governed training; never a data path',
                  'strengths': ['full-stack implementation', 'test-first verification', 'governed dispatch'], 'can_do': ['implement', 'test', 'dispatch signed/authorised work'], 'cannot_do': ['sign off as owner', 'move estate data through E1', 'change canon']},
                  objectives=['Mα five-promise delivery'], capabilities=['python', 'react', 'gpu dispatch'], limits=['owner approval for scope; Watch and Shield boundaries'],
                  admission={'record': 'platform operator identity', 'decision': 'admitted developer'}, compliance=_score(passed, len(rates), 'independent testing-agent iterations with ≥90% success and no retest required'),
                  resources={'gpu_hours': 0.0, 'cost_usd': None}, work={'assignments_completed': len(reports), 'kind': 'verified iterations', 'mean_success_rate': round(sum(rates) / len(rates), 4) if rates else None}, collaborators=[{'agent_id': 'agent:akki-autopilot', 'shared': 'training lab'}])
    auto = _profile(tenant, 'agent:akki-autopilot', 'worker', 'Akki autopilot', version='training_lab.autopilot', jd={'role': 'autonomous executor', 'job': 'refreshes running jobs, dispatches signed plans and Mα lanes, judges finished runs against signed acceptance',
                    'strengths': ['deterministic', 'idempotent leases'], 'can_do': ['dispatch authorised work', 'settle receipts'], 'cannot_do': ['sign plans', 'widen caps', 'evict resident workloads']},
                    objectives=['training continuity'], capabilities=['dispatch', 'settlement'], limits=['15-minute cron floor', 'resident GPU protection'], admission={'record': 'services/training_lab/autopilot.py', 'decision': 'platform worker'},
                    compliance=_score(0, 0, 'tick receipts not yet aggregated'), resources={'gpu_hours': 0.0, 'cost_usd': 0.0}, work={'assignments_completed': 0, 'kind': 'ticks'}, collaborators=[])
    return [e1, auto]


def sync(tenant):
    """Re-derive every evidence-backed profile; owner lifecycle fields (status overrides, lifecycle log, manual assignments) are preserved."""
    derived = []
    for fn in (_llm_roles, _trained_models, _malpha, _skills, _agents):
        try: derived.extend(fn(tenant))
        except Exception as exc: log.warning('armi derivation %s failed: %s', fn.__name__, exc)
    coll = db().armi_agents
    for p in derived:
        existing = coll.find_one({'tenant_id': tenant, 'agent_id': p['agent_id']}) or {}
        p['lifecycle'] = existing.get('lifecycle') or [{'at': now(), 'action': 'onboarded', 'by': 'armi.sync', 'note': 'derived from native records'}]
        if existing.get('status_override'): p['status'] = existing['status_override']; p['status_override'] = existing['status_override']
        p['manual_assignments'] = existing.get('manual_assignments') or 0
        p['synced_at'] = now(); p['profile_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in p.items() if k not in ('synced_at', 'profile_sha256', 'lifecycle')}, sort_keys=True, default=str).encode()).hexdigest()
        coll.update_one({'tenant_id': tenant, 'agent_id': p['agent_id']}, {'$set': p}, upsert=True)
    return len(derived)


def list_agents(tenant):
    _merge_assignments(tenant)
    return list(db().armi_agents.find({'tenant_id': tenant}, {'_id': 0}, sort=[('kind', 1), ('name', 1)]))


def get(tenant, agent_id):
    _merge_assignments(tenant, agent_id)
    doc = db().armi_agents.find_one({'tenant_id': tenant, 'agent_id': agent_id}, {'_id': 0})
    if doc: doc['assignments'] = list(db().armi_assignments.find({'tenant_id': tenant, 'agent_id': agent_id}, {'_id': 0}, sort=[('at', -1)], limit=50))
    return doc


def _merge_assignments(tenant, agent_id=None):
    """Manual assignments fold into the compliance and work figures as their own evidence line, never mixed silently with derived counts."""
    query = {'tenant_id': tenant, **({'agent_id': agent_id} if agent_id else {})}
    for a in db().armi_agents.find(query, {'_id': 0, 'agent_id': 1}):
        rows = list(db().armi_assignments.find({'tenant_id': tenant, 'agent_id': a['agent_id']}, {'_id': 0}))
        if not rows: continue
        done = [r for r in rows if r['status'] == 'completed']; scored = [r for r in done if r.get('score')]
        compliant = sum(1 for r in scored if r['score'].get('compliant'))
        db().armi_agents.update_one({'tenant_id': tenant, 'agent_id': a['agent_id']}, {'$set': {'manual_assignments': len(rows), 'assignment_summary': {'assigned': sum(1 for r in rows if r['status'] == 'assigned'), 'completed': len(done), 'failed': sum(1 for r in rows if r['status'] == 'failed'),
                                                                                                  'compliance': _score(compliant, len(scored), 'scored ARMI assignments marked compliant'), 'mean_quality': round(sum(r['score']['quality'] for r in scored) / len(scored), 3) if scored else None}}})


# ----------------------------------------------------------------------------- lifecycle (owner/operator actions, every one recorded)
def onboard(tenant, actor, body):
    agent_id = body.get('agent_id') or f"{body['kind']}:{re.sub(r'[^a-z0-9]+', '-', body['name'].lower()).strip('-')}"
    if db().armi_agents.find_one({'tenant_id': tenant, 'agent_id': agent_id}): raise ValueError('An agent with that identity is already on the register')
    p = _profile(tenant, agent_id, body['kind'], body['name'], status='onboarded', version=body.get('version'), jd=body['jd'], objectives=body.get('objectives') or [], capabilities=body.get('capabilities') or [], limits=body.get('limits') or [],
                 admission={'record': body.get('admission_ref'), 'decision': 'onboarded, not yet admitted'}, compliance=_score(0, 0, 'no assignments yet'), resources={'gpu_hours': 0.0, 'cost_usd': None}, work={'assignments_completed': 0, 'kind': 'assignments'}, collaborators=[],
                 lifecycle=[{'at': now(), 'action': 'onboarded', 'by': actor, 'note': body.get('note')}], synced_at=now())
    db().armi_agents.insert_one(dict(p)); return get(tenant, agent_id)


def transition(tenant, actor, agent_id, action, note=None, version=None):
    doc = db().armi_agents.find_one({'tenant_id': tenant, 'agent_id': agent_id})
    if not doc: raise LookupError('No agent with that identity in this estate')
    target = {'activate': 'active', 'suspend': 'suspended', 'revoke': 'revoked', 'bind_version': doc['status']}[action]
    if doc['status'] == 'revoked' and action != 'revoke': raise ValueError('A revoked agent cannot be reactivated; onboard a new identity with its own record')
    fields = {'status': target, 'status_override': target if action != 'bind_version' else doc.get('status_override')}
    if action == 'bind_version':
        if not version: raise ValueError('bind_version requires the version or artefact digest to bind')
        fields['version'] = version
    db().armi_agents.update_one({'tenant_id': tenant, 'agent_id': agent_id}, {'$set': fields, '$push': {'lifecycle': {'at': now(), 'action': action, 'by': actor, 'note': note, 'version': version}}})
    if action in ('suspend', 'revoke'):
        db().armi_assignments.update_many({'tenant_id': tenant, 'agent_id': agent_id, 'status': 'assigned'}, {'$set': {'status': 'cancelled', 'cancelled_reason': f'agent {target}', 'updated_at': now()}})
    return get(tenant, agent_id)


def assign(tenant, actor, agent_id, body):
    doc = db().armi_agents.find_one({'tenant_id': tenant, 'agent_id': agent_id})
    if not doc: raise LookupError('No agent with that identity in this estate')
    if doc['status'] not in ('active', 'onboarded'): raise ValueError(f"An agent that is {doc['status']} cannot take new work")
    for dep in body.get('depends_on') or []:
        d = db().armi_agents.find_one({'tenant_id': tenant, 'agent_id': dep}, {'status': 1})
        if not d or d['status'] in ('suspended', 'revoked'): raise ValueError(f'Dependency {dep} is not available in this estate')
    row = {'assignment_id': 'asg-' + uuid.uuid4().hex[:12], 'tenant_id': tenant, 'agent_id': agent_id, 'task': body['task'], 'objective_ref': body.get('objective_ref'), 'collaborators': body.get('collaborators') or [], 'depends_on': body.get('depends_on') or [],
           'status': 'assigned', 'assigned_by': actor, 'at': now(), 'updated_at': now()}
    db().armi_assignments.insert_one(dict(row))
    db().armi_agents.update_one({'tenant_id': tenant, 'agent_id': agent_id}, {'$push': {'lifecycle': {'at': now(), 'action': 'assigned', 'by': actor, 'note': body['task'][:200], 'assignment_id': row['assignment_id']}}})
    return {k: v for k, v in row.items() if k != '_id'}


def complete(tenant, actor, assignment_id, body):
    row = db().armi_assignments.find_one({'tenant_id': tenant, 'assignment_id': assignment_id})
    if not row: raise LookupError('No assignment with that reference in this estate')
    if row['status'] != 'assigned': raise ValueError(f"Assignment is {row['status']}")
    status = 'completed' if body.get('outcome', 'completed') == 'completed' else 'failed'
    db().armi_assignments.update_one({'assignment_id': assignment_id, 'tenant_id': tenant}, {'$set': {'status': status, 'result_ref': body.get('result_ref'), 'completed_by': actor, 'completed_at': now(), 'updated_at': now(), 'resources': body.get('resources')}})
    return db().armi_assignments.find_one({'assignment_id': assignment_id}, {'_id': 0})


def score(tenant, actor, assignment_id, body):
    row = db().armi_assignments.find_one({'tenant_id': tenant, 'assignment_id': assignment_id})
    if not row: raise LookupError('No assignment with that reference in this estate')
    if row['status'] != 'completed': raise ValueError('Only a completed assignment can be scored')
    sc = {'quality': float(body['quality']), 'compliant': bool(body['compliant']), 'evidence_ref': body.get('evidence_ref'), 'scored_by': actor, 'at': now()}
    if not 0 <= sc['quality'] <= 1: raise ValueError('quality is a share in [0, 1]')
    if not sc['evidence_ref']: raise ValueError('A score without an evidence reference is an opinion; give the gate, test or review it rests on')
    db().armi_assignments.update_one({'assignment_id': assignment_id, 'tenant_id': tenant}, {'$set': {'score': sc, 'updated_at': now()}})
    _merge_assignments(tenant, row['agent_id'])
    return db().armi_assignments.find_one({'assignment_id': assignment_id}, {'_id': 0})


def overview(tenant):
    agents = list_agents(tenant)
    from services.cost_ledger.rates import load_rates
    rates = load_rates(); priced = [a for a in agents if (a.get('resources') or {}).get('cost_usd') is not None and (a.get('resources') or {}).get('gpu_hours')]
    try: by_agent, unattributed = _caas_contribution(tenant)
    except Exception as exc: log.warning('armi contribution derivation failed: %s', exc); by_agent, unattributed = {}, {'deliveries': 0, 'amount_usd': 0.0, 'priced': 0}
    attributed = sum(c['deliveries'] for c in by_agent.values()); amount = sum(c['metered_amount_usd'] for c in by_agent.values()); any_priced = any(c['priced'] for c in by_agent.values())
    return {'agents': len(agents), 'by_kind': {k: sum(1 for a in agents if a['kind'] == k) for k in sorted({a['kind'] for a in agents})}, 'by_status': {s: sum(1 for a in agents if a['status'] == s) for s in STATUSES},
            'gpu_hours_total': round(sum((a.get('resources') or {}).get('gpu_hours') or 0 for a in agents), 3), 'cost_usd': round(sum(a['resources']['cost_usd'] for a in priced), 2) if priced else None,
            'cost_note': 'owner-supplied GPU-hour rate applied to measured hours' if priced else 'no governed rate card; money is not estimated here',
            'rate_card': {lane: len(rows) for lane, rows in rates.items()},
            'contribution': {'deliveries_total': attributed + unattributed['deliveries'], 'attributed': attributed, 'unattributed': unattributed['deliveries'], 'amount_usd': round(amount, 2) if any_priced else None,
                             'rule': 'one CaaS delivery credits at most one identity (its authoring role); deterministic aggregates credit no agent; amounts are the rates frozen on metered events'},
            'protected': {'watch_profiles_exported': False, 'malicious_probability': NOT_COMPUTED}}
