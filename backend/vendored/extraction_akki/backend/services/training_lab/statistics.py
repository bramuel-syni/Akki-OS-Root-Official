"""Small-sample honest statistics. Forecast ranges are scenarios, not confidence intervals."""
import math
from statistics import NormalDist

import numpy as np


def wilson_interval(successes, n, confidence=0.95):
    if type(n) is not int or n <= 0 or type(successes) is not int or not 0 <= successes <= n or not 0 < confidence < 1:
        raise ValueError("Valid integer counts and confidence required")
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    p, d = successes / n, 1 + z * z / n
    mid = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1-p) / n + z*z / (4*n*n)) / d
    return {"method": "wilson_score", "estimate": p, "low": max(0, mid-half), "high": min(1, mid+half), "confidence": confidence, "n": n}


def bootstrap_interval(values, *, seed, confidence=0.95, draws=1000, groups=None, paired=None):
    """Percentile bootstrap of actual observations (paired differences / whole groups)."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or not 2 <= len(x) <= 20000 or not np.isfinite(x).all():
        raise ValueError("2–20000 finite observations required")
    if not 100 <= draws <= 5000 or not 0 < confidence < 1:
        raise ValueError("Invalid confidence or resample count")
    if paired is not None:
        y = np.asarray(paired, dtype=float)
        if y.shape != x.shape or not np.isfinite(y).all():
            raise ValueError("Paired observations must be aligned and finite")
        x = x-y
    blocks = [np.asarray([v]) for v in x]
    if groups is not None:
        if len(groups) != len(x):
            raise ValueError("Group identifiers must align with observations")
        indices = {}
        for i, group in enumerate(groups):
            indices.setdefault(group, []).append(i)
        if len(indices) < 2:
            raise ValueError("At least two independent groups required")
        blocks = [x[idx] for idx in indices.values()]
    sums = np.asarray([v.sum() for v in blocks]); sizes = np.asarray([len(v) for v in blocks])
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(draws):
        selected = rng.integers(0, len(blocks), len(blocks))
        estimates.append(float(sums[selected].sum()/sizes[selected].sum()))
    lo, hi = np.quantile(estimates, [(1-confidence)/2, (1+confidence)/2])
    return {"method": "group_percentile_bootstrap" if groups is not None else "item_percentile_bootstrap",
            "estimate": float(x.mean()), "low": float(lo), "high": float(hi), "confidence": confidence,
            "draws": draws, "seed": seed, "independent_units": len(blocks), "paired": paired is not None,
            "limitations": "Percentile interval; assumes exchangeable independent resampling units. Degenerate data can yield zero width."}


def power_law_scenarios(points, exponent_bounds, irreducible_bounds, floor, cap):
    """Fit a for fixed b,c on a 3×3 prior grid. Do NOT clip out-of-budget estimates."""
    pts = np.asarray(points, dtype=float)
    if pts.ndim != 2 or pts.shape[1] != 2 or len(pts) < 3 or not np.isfinite(pts).all():
        raise ValueError("At least three finite calibration points required")
    if len(set(pts[:, 0])) < 3 or (pts[:, 0] <= 0).any() or (pts[:, 1] < 0).any() or (pts[:, 1] > 1).any():
        raise ValueError("Distinct positive volumes and bounded proportion metric required")
    b0,b1 = exponent_bounds; c0,c1 = irreducible_bounds
    if not all(math.isfinite(v) for v in (b0,b1,c0,c1,floor,cap)) or not 0.001 <= b0 <= b1 <= 5 or not 0 <= c0 <= c1 < 1 or not 0 < floor < 1 or cap <= 0:
        raise ValueError("Invalid prior bounds, floor or cap")
    scenarios = []
    for b in np.linspace(b0,b1,3):
        basis = pts[:,0] ** -b
        for c in np.linspace(c0,c1,3):
            a = max(0., float(np.dot(basis, 1-pts[:,1]-c)/np.dot(basis,basis)))
            need = None
            if 1-floor > c:
                log_need = math.log(max(a/(1-floor-c),1e-300))/b
                need = max(1, math.ceil(math.exp(log_need))) if log_need < 700 else None
            scenarios.append({"b":float(b),"c":float(c),"a":a,"examples":need,
                              "within_cap":need is not None and need <= cap,
                              "rmse":float(np.sqrt(np.mean((a*basis+c-(1-pts[:,1]))**2)))})
    finite = [s["examples"] for s in scenarios if s["examples"] is not None]
    return {"method":"error=a*N^-b+c", "evidence_class":"prior_sensitivity_not_confidence_interval",
            "low":min(finite) if finite else None,"mid":scenarios[4]["examples"],
            "high":max(finite) if finite else None,"some_unreachable":len(finite)!=len(scenarios),
            "all_within_cap":all(s["within_cap"] for s in scenarios),"scenarios":scenarios,
            "limitations":"Fixed prior grid; exponent and irreducible error are not independently identified. Not for unbounded WER/RMSE."}


def monitoring_threshold(scores, *, false_alert_rate, calibration_ref):
    vals = np.asarray(scores,dtype=float)
    if vals.ndim != 1 or len(vals)<2 or not np.isfinite(vals).all() or not calibration_ref or not 0 < false_alert_rate < 0.5:
        raise ValueError("Calibration observations, reference and chosen false-alert rate required")
    return {"method":"empirical_lower_quantile", "threshold":float(np.quantile(vals,false_alert_rate)),
            "false_alert_rate_target":false_alert_rate,"calibration_ref":calibration_ref,"n":len(vals),
            "validated_false_alert_rate":None,"action":"review","authority":"advisory_only"}