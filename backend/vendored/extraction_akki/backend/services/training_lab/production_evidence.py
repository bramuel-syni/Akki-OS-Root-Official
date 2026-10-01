"""Read retained, verified measurements only. No GPU/SSH dispatch on a read."""
import math
from statistics import mean, stdev
from services.training_runner import m9_dispatch


def measured_job(tenant, job_id, phase=None):
    if tenant != 'RMS':
        raise LookupError('That training evidence is not available in this estate.')
    job = m9_dispatch.load_job(job_id)
    receipt = (job or {}).get('receipt') or {}
    if not job or job.get('status') != 'completed' or not receipt.get('digest_verified'):
        raise ValueError('A completed, digest-verified worker record is required.')
    if phase and job.get('phase') != phase:
        raise ValueError('The worker record does not measure the requested stage.')
    return job, receipt.get('result') or {}


def quote(calibration, base, train_units, epochs):
    """Conditional 95% t interval for mean throughput, inverted to projected GPU time.

    Historical ±2σ throughput spreads are NOT confidence intervals. This interval
    states its independent-rate/stable-conditions assumption; it is not a promise.
    """
    from scipy.stats import t
    rows = [r for r in calibration.get('runs', []) if r.get('base') == base]
    if len({r.get('fraction') for r in rows}) < 3:
        raise ValueError('Calibration must cover at least three measured data volumes.')
    rates = [float(r['tokens_per_second']) for r in rows]
    if any(not math.isfinite(x) or x <= 0 for x in rates):
        raise ValueError('Calibration throughput must be finite and positive.')
    units = sum(r['train_units'] for r in rows)
    if units <= 0:
        raise ValueError('Calibration has no training units.')
    full_tokens = sum(r['train_tokens'] for r in rows) / units * train_units * epochs
    centre = mean(rates)
    margin = float(t.ppf(.975, len(rates) - 1)) * stdev(rates) / math.sqrt(len(rates))
    if centre - margin <= 0:
        raise ValueError('Calibration uncertainty is too wide for a finite upper compute quote; measure again.')
    return {'estimate_gpu_hours': full_tokens / centre / 3600,
            'confidence_interval_gpu_hours': [full_tokens / (centre + margin) / 3600, full_tokens / (centre - margin) / 3600],
            'confidence': .95, 'observations': len(rates), 'planned_epochs': epochs,
            'method': 'Student t interval for mean measured throughput, inverted for fixed projected token work',
            'assumptions': 'Independent calibration rate observations; unchanged hardware, recipe and workload mix. Does not include model-quality uncertainty.',
            'class': 'estimated'}


def measured_strata(result, outcome):
    held = (result.get('adapter_eval') or {}).get('held') or {}
    actual = held.get('per_stratum') or {}
    rows = {}
    for ref, bar in outcome['acceptance'].items():
        reading = actual.get(ref) or {}
        accuracy, abstention = reading.get('accuracy'), reading.get('abstention_rate')
        coverage = 1 - abstention if isinstance(abstention, (int, float)) else None
        rows[ref] = {'accuracy': accuracy, 'coverage': coverage, 'units': reading.get('units'),
                     'acceptance': bar, 'passes': None if accuracy is None or coverage is None else accuracy >= bar['accuracy'] and coverage >= bar['coverage']}
    return rows


def catalogue(tenant):
    if tenant != 'RMS':
        return []
    result = []
    for job in m9_dispatch.list_jobs():
        receipt = job.get('receipt') or {}
        if job.get('phase') != 'assemble' or job.get('status') != 'completed' or not receipt.get('digest_verified') or (job.get('params') or {}).get('kind') != 'transcript_text':
            continue
        record = receipt.get('result') or {}
        result.append({'register_ref': job['job_id'], 'corpus_id': record.get('corpus_id'), 'kind': record.get('kind'),
                       'strata': record.get('per_stratum'), 'test_set': record.get('test_set_seal'),
                       'manifest_sha256': record.get('manifest_sha256'), 'rights_ref': record.get('rights_ref'),
                       'source_class': 'measured', 'acceptance_use': 'Previously inspected results are exploratory; a fresh sealed final set is required after recipe selection.'})
    return result