"""Tenant-scoped projection of existing records; not a new Watch or ledger.

Census observations are NOT detector verdicts. A persisted action is NOT proof
that its effector ran — only a gate `effect` receipt is. Unassigned historical
records never enter this reader.
"""
from services.census_autonomy import operational_store
from services.watch import commission_gate
from services.watch.router import _load_kind


def state_for(actor):
    tenant = actor['tenant_id']
    runs = operational_store.runs(tenant)
    run_ids = {run['census_run_id'] for run in runs}
    gate = commission_gate.owned_records(tenant)
    rows = []
    for run in runs:
        rows.append({
            'record_id': run['census_run_id'], 'kind': 'observation',
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
            # Ownership must be explicit, trace to an existing tenant-owned commission,
            # or be bound by a commission-gate detection — never an email suffix.
            owner = record.get('tenant_id')
            linked = record.get('census_run_id') in run_ids
            gate_owned = record['record_id'] in gate['verdict_ids'] or record['record_id'] in gate['action_ids']
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
                state = 'In effect'
            rows.append({
                'record_id': record['record_id'],
                'kind': 'verdict' if kind == 'verdicts' else 'action',
                'title': record.get('verdict_class') or record.get('action_class') or kind,
                'actor': record.get('subject_ref') or 'Not recorded',
                'state': state, 'observed_at': record.get('asserted_at') or record.get('issued_at') or record.get('at_iso'),
                'evidence_ref': record.get('evidence_ref') or record.get('verdict_ref'),
                'census_run_id': record.get('census_run_id'),
                'detector': detection['detector'] if detection else None,
                'boundary': detection['boundary'] if detection else None,
                'effect_verified': bool(effects), 'effects': len(effects),
                'basis': (('Commission-gate detection; effect receipts prove the gate enforced it'
                           + (f"; released {release['outcome']} at {release['expired_at']}" if release else '')) if detection
                          else 'Retained Watch record; enforcement and independent witness require separate evidence'),
            })
        counts[kind] = len(visible)
    return {
        'tenant_id': tenant, 'records': sorted(rows, key=lambda r: r.get('observed_at') or '', reverse=True),
        'counts': {'observations': len(runs), 'gate_crossings': gate['counts']['crossings'],
                   'gate_refusals': gate['counts']['refusals'], 'gate_effects': gate['counts']['effects'],
                   'gate_releases': gate['counts']['releases'], **counts},
        'protected_boundaries': commission_gate.boundary_register(),
        'coverage': 'Census commissions, commission-gate crossings and explicitly tenant-owned Watch records only',
        'enforcement_status': 'Commission gates enforce contain/shape with effect receipts; other effectors not qualified',
        'detector_status': 'Deterministic gate detectors (fast_violation, slow_play, permitted_but_misused) at DEFAULT thresholds pending ruling; learned detectors not wired',
        'witness_status': 'Independent witness placement and effects not verified here',
    }
