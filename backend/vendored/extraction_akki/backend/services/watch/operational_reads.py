"""Tenant-scoped projection of existing records; not a new Watch or ledger.

Census observations are NOT detector verdicts. A persisted action is NOT proof
that its effector ran. Unassigned historical records never enter this reader.
"""
from services.census_autonomy import operational_store
from services.watch.router import _load_kind


def state_for(actor):
    tenant = actor['tenant_id']
    runs = operational_store.runs(tenant)
    run_ids = {run['census_run_id'] for run in runs}
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
            # Ownership must be explicit or trace to an existing tenant-owned
            # commission, never an email suffix or an arbitrary subject label.
            owner = record.get('tenant_id')
            linked = record.get('census_run_id') in run_ids
            if owner != tenant and not (owner is None and linked):
                continue
            visible.append(record)
            if kind not in ('verdicts', 'actions'):
                continue
            rows.append({
                'record_id': record['record_id'],
                'kind': 'verdict' if kind == 'verdicts' else 'action',
                'title': record.get('verdict_class') or record.get('action_class') or kind,
                'actor': record.get('subject_ref') or 'Not recorded',
                'state': 'Recorded', 'observed_at': record.get('asserted_at') or record.get('issued_at') or record.get('at_iso'),
                'evidence_ref': record.get('evidence_ref') or record.get('verdict_ref'),
                'census_run_id': record.get('census_run_id'), 'effect_verified': False,
                'basis': 'Retained Watch record; enforcement and independent witness require separate evidence',
            })
        counts[kind] = len(visible)
    return {
        'tenant_id': tenant, 'records': sorted(rows, key=lambda r: r.get('observed_at') or '', reverse=True),
        'counts': {'observations': len(runs), **counts},
        'coverage': 'Census commissions and explicitly tenant-owned Watch records only',
        'enforcement_status': 'Not qualified by this read model',
        'detector_status': 'End-to-end detector qualification pending',
        'witness_status': 'Independent witness placement and effects not verified here',
    }