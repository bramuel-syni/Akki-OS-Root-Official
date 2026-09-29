"""Tenant-scoped projection of existing records; not a new Watch or ledger.

Census observations are NOT detector verdicts. A persisted action is NOT proof
that its effector ran — only a gate `effect` receipt is. Unassigned historical
records never enter this reader. Every read reconciles expired containments,
receipts the console session, and carries each acted row's evidence walk.
"""
from datetime import datetime, timezone

from services.census_autonomy import operational_store
from services.watch import commission_gate, console_projection, decisions, notices, witness_binding
from services.watch.router import _load_kind

LANE = {"annotate": "noted", "shape": "acted", "contain": "acted", "sever": "held"}


def state_for(actor):
    tenant = actor['tenant_id']
    now = datetime.now(timezone.utc)
    commission_gate.reconcile_expired(tenant, now)
    commission_gate.receipt_console(actor)
    runs = operational_store.runs(tenant)
    run_ids = {run['census_run_id'] for run in runs}
    gate = commission_gate.owned_records(tenant)
    feed = commission_gate.rows(tenant)
    items = decisions.fold(tenant)
    walks = console_projection.record_walks(tenant, gate, feed)
    rows = []
    for run in runs:
        rows.append({
            'record_id': run['census_run_id'], 'kind': 'observation', 'lane': 'noted',
            'title': 'Census · ' + ', '.join(run['source_ids']),
            'actor': run['principal_id'], 'state': run['status'],
            'observed_at': run.get('finished_at') or run.get('started_at') or run['created_at'],
            'evidence_ref': run.get('proof_ref'), 'census_run_id': run['census_run_id'],
            'basis': 'Existing census commission record; not a Watch detector verdict',
            'worker_id': run.get('worker_id'), 'effect_verified': False,
        })
    counts = {}
    for kind in ('verdicts', 'actions', 'containments', 'containment_reconciliations',
                 'witness_attestations', 'tamper_alarms', 'marks'):
        visible = []
        for record in _load_kind(kind):
            owner = record.get('tenant_id')
            linked = record.get('census_run_id') in run_ids
            gate_owned = record['record_id'] in gate['verdict_ids'] or record['record_id'] in gate['action_ids'] or record['record_id'] in gate['mark_ids']
            if owner != tenant and not (owner is None and (linked or gate_owned)):
                continue
            visible.append(record)
            if kind not in ('verdicts', 'actions'):
                continue
            detection = gate['verdict_ids'].get(record['record_id']) or gate['action_ids'].get(record['record_id'])
            effects = gate['effects'].get(record['record_id'], [])
            release = gate['releases'].get(record['record_id'])
            state = 'Recorded'
            if kind == 'actions' and release:
                state = 'Released'
            elif kind == 'actions' and effects:
                state = 'Held' if record.get('action_class') == 'sever' else 'In effect'
            notice = notices.by_ref(tenant, 'action_ref', record['record_id']) if kind == 'actions' else []
            rows.append({
                'record_id': record['record_id'],
                'kind': 'verdict' if kind == 'verdicts' else 'action',
                'lane': LANE.get(detection['action_class'], 'noted') if detection else 'noted',
                'title': record.get('verdict_class') or record.get('action_class') or kind,
                'actor': record.get('subject_ref') or 'Not recorded',
                'state': state, 'observed_at': record.get('asserted_at') or record.get('issued_at') or record.get('at_iso'),
                'evidence_ref': record.get('evidence_ref') or record.get('verdict_ref'),
                'census_run_id': record.get('census_run_id'),
                'detector': detection['detector'] if detection else None,
                'boundary': detection['boundary'] if detection else None,
                'effect_verified': bool(effects), 'effects': len(effects),
                'walk': walks.get(record['record_id']),
                'notice': notice[-1] if notice else None,
                'basis': (('Commission-gate detection; effect receipts prove the gate enforced it'
                           + (f"; release: {release['outcome'].replace('_', ' ')} at {release.get('expired_at') or release['at']}" if release else '')) if detection
                          else 'Retained Watch record; enforcement and independent witness require separate evidence'),
            })
        counts[kind] = len(visible)
    for d in console_projection.panel(tenant, items):
        rows.append({'record_id': d['decision_id'], 'kind': 'decision', 'lane': 'held' if d['klass'] == 'demark_release' else 'noted', 'title': d['title'],
                     'actor': d['subject_ref'], 'state': d['state'].capitalize(), 'observed_at': d['opened_at'], 'evidence_ref': d['refs'].get('action_ref') or d['refs'].get('proposal_id'),
                     'census_run_id': None, 'effect_verified': bool(d['executed']), 'walk': None, 'notice': None,
                     'basis': f"Reserved human decision · {len(d['approvers'])} of {d['approvals_needed']} approvals · blast {d['blast']}"})
    live_requirements = console_projection.learning(feed)
    return {
        'tenant_id': tenant, 'records': sorted(rows, key=lambda r: r.get('observed_at') or '', reverse=True),
        'counts': {'observations': len(runs), 'gate_crossings': gate['counts']['crossings'], 'gate_admitted': gate['counts']['admitted'],
                   'gate_refusals': gate['counts']['refusals'], 'gate_effects': gate['counts']['effects'],
                   'gate_releases': gate['counts']['releases'], 'decisions_open': sum(1 for d in items.values() if d['state'] == 'open'),
                   'console_reads': gate['counts']['console'], 'exceptions': gate['counts']['exceptions'], **counts},
        'tiles': console_projection.tiles(feed, items, now), 'charts': console_projection.charts(feed),
        'patterns': console_projection.patterns(feed, now), 'mirage': console_projection.mirage(feed, now),
        'marked': console_projection.marked(tenant, feed), 'decisions': console_projection.panel(tenant, items),
        'witness': witness_binding.summary(), 'learning': live_requirements,
        'protected_boundaries': commission_gate.boundary_register(),
        'coverage': 'Census commissions, commission-gate crossings and explicitly tenant-owned Watch records only',
        'enforcement_status': 'Commission gates enforce sever/contain/shape with effect receipts and evaluate mark state on every pass; other effectors not qualified',
        'detector_status': f"Deterministic gate detectors (fast_violation, slow_play, permitted_but_misused) under {live_requirements['label']}; tripwire conviction is structural; learned detectors not wired",
        'witness_status': 'Record witness attests gate action digests and runs the break-in test from the application pod; a separately deployed watchdog is not yet placed',
        'never_all_clear': 'Detection thresholds are seam defaults until ruled; the independent watchdog is not placed; this panel is built never to render all-clear.',
    }
