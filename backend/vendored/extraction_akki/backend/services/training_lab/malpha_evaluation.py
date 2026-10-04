"""Versioned evidence rules, separate from the owner's unchanged point targets.

Intervals quantify sampling uncertainty, not label correctness or universal generality.
No raw text, segment identifiers or resampling group identifiers leave this module.
"""
import hashlib
import json
import math
import random
from statistics import NormalDist

LISTENER_PROTOCOL = {
    'version': 'malpha-listener-evidence-v1', 'target': 0.90, 'confidence': 0.95,
    'minimum_positive_segments': 100, 'minimum_negative_segments': 100,
    'minimum_groups': 20, 'bootstrap_draws': 1000,
    'policy_basis': 'preregistered engineering evidence requirements; not a replacement for owner targets',
    'reference_requirement': 'independently_verified_brand_annotations',
}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def wilson(successes, total, confidence=0.95):
    if type(total) is not int or total <= 0 or type(successes) is not int or not 0 <= successes <= total: return None
    z = NormalDist().inv_cdf((1 + confidence) / 2); p = successes / total; d = 1 + z*z/total
    middle = (p + z*z/(2*total))/d
    half = z*math.sqrt(p*(1-p)/total + z*z/(4*total*total))/d
    return [max(0.0, middle-half), min(1.0, middle+half)]


def grouped_intervals(groups, seed, draws=1000):
    """Resample complete recording-session count triples; never bootstrap flat tokens."""
    if len(groups) < 2: return {'precision': None, 'recall': None, 'valid_draws': 0}
    rng = random.Random(seed); estimates = {'precision': [], 'recall': []}
    for _ in range(draws):
        sample = [rng.choice(groups) for _ in groups]
        tp, fp, fn = (sum(g[i] for g in sample) for i in range(3))
        if tp + fp: estimates['precision'].append(tp / (tp + fp))
        if tp + fn: estimates['recall'].append(tp / (tp + fn))
    out = {}
    for name, values in estimates.items():
        values.sort()
        out[name] = [values[int((len(values)-1)*.025)], values[int((len(values)-1)*.975)]] if len(values) >= .95*draws else None
    out['valid_draws'] = min(len(v) for v in estimates.values())
    return out


def population_support(positives, negatives, groups=None):
    issues = []
    for value, key, label in ((positives, 'minimum_positive_segments', 'positive_segments'),
                               (negatives, 'minimum_negative_segments', 'negative_segments'),
                               (groups, 'minimum_groups', 'recording_groups')):
        if type(value) is not int or value < LISTENER_PROTOCOL[key]: issues.append(label)
    return {'sufficient': not issues, 'missing_support': issues,
            'positive_segments': positives, 'negative_segments': negatives, 'recording_groups': groups}


def listener_evidence(metrics, *, group_counts=None, seed=1029, reference_verified=False):
    groups = group_counts or []
    support = population_support(metrics.get('segments_with_mentions'),
                                 metrics.get('segments_without_mentions'), len(groups))
    tp, fp, fn = (metrics.get(k) for k in ('tp', 'fp', 'fn'))
    valid = all(type(v) is int and v >= 0 for v in (tp, fp, fn))
    group_valid = all(isinstance(g, (list, tuple)) and len(g) == 3 and all(type(v) is int and v >= 0 for v in g) for g in groups)
    aligned = bool(valid and group_valid and tuple(sum(g[i] for g in groups) for i in range(3)) == (tp, fp, fn))
    p = wilson(tp, tp+fp) if valid else None; r = wilson(tp, tp+fn) if valid else None
    cluster = grouped_intervals(groups, seed, LISTENER_PROTOCOL['bootstrap_draws']) if aligned else {'precision': None, 'recall': None, 'valid_draws': 0}
    intervals = [p, r, cluster['precision'], cluster['recall']]
    target = LISTENER_PROTOCOL['target']
    point = bool(valid and tp+fp and tp+fn and tp/(tp+fp) >= target and tp/(tp+fn) >= target)
    supported = support['sufficient'] and all(v is not None and v[0] >= target for v in intervals)
    reasons = list(support['missing_support'])
    if not valid: reasons.append('invalid_counts')
    if not aligned: reasons.append('group_counts_do_not_match_observed_counts')
    if not reference_verified: reasons.append('brand_reference_not_independently_verified')
    if not supported: reasons.append('confidence_not_established')
    if not point: reasons.append('point_target_not_met')
    return {'protocol': dict(LISTENER_PROTOCOL), 'protocol_sha256': fingerprint(LISTENER_PROTOCOL),
            'point_target_met': point, 'supported_target_met': bool(supported),
            'acceptance_ready': bool(point and supported and reference_verified),
            'status': 'supported' if point and supported and reference_verified else 'inconclusive' if point else 'below_target',
            'support': support, 'precision_wilson_ci95': p, 'recall_wilson_ci95': r,
            'session_bootstrap_ci95': cluster, 'reference_verified': reference_verified, 'reasons': reasons,
            'limitations': 'Session blocks assume exchangeable independent recordings; intervals do not validate transcript-derived alias labels. Stratified development precision is not production-prevalence precision.'}


def admission_preflight(records, languages=('kik', 'kam', 'swa')):
    """Uses only already-recorded aggregate seal/support metadata, never opens test content."""
    # The latest relabel result may reduce support. Do not choose a larger old count.
    latest = next((j for j in reversed(records) if j.get('phase') == 'malpha_aip_relabel' and j.get('status') == 'completed'), None)
    result = (latest or {}).get('result') or {}; report = result.get('report') or {}; seals = result.get('seals') or {}
    per = {}
    for lang in languages:
        positives = ((report.get(lang) or {}).get('by_split') or {}).get('admission')
        per[lang] = population_support(positives, None, None)
    seal_values = [seals.get(l, {}).get('admission_seg_ids_sha256') for l in languages]
    known_seal = all(isinstance(v, str) and len(v) == 64 for v in seal_values)
    audits = [j for j in records if j.get('phase') == 'malpha_corpus_audit' and j.get('status') == 'completed']
    audit = (audits[-1].get('result') or {}) if audits else {}
    audited = audit.get('per_language') or {}
    matches = known_seal and all(audited.get(l, {}).get('admission_seal_sha256') == seals.get(l, {}).get('admission_seg_ids_sha256') for l in languages)
    if matches:
        per = {l: audited[l]['support'] for l in languages}
    ready = bool(matches and audit.get('independence_verified') is True and audit.get('reference_verified') is True and all(per[l]['sufficient'] for l in languages))
    return {'protocol': dict(LISTENER_PROTOCOL), 'per_language': per, 'ready': ready,
            'panel_id': fingerprint(seal_values) if known_seal else None,
            'independence_verified': bool(matches and audit.get('independence_verified') is True),
            'reference_verified': bool(matches and audit.get('reference_verified') is True),
            'audit_job_id': audits[-1]['job_id'] if audits else None,
            'reason': 'Qualified for a single confirmation read.' if ready else 'Independent reference qualification and complete positive/negative/group support must be recorded before a confirmation read.',
            'source_job_id': (latest or {}).get('job_id'), 'test_content_read': False, 'raw_data_exported': False}