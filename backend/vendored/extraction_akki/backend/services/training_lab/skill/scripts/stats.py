"""Evaluation statistics and scaling fits. Arithmetic the professor lens relies on."""
import math
from statistics import NormalDist

from services.training_lab.statistics import power_law_scenarios, wilson_interval


def z_for(conf):
    return {0.80: 1.2816, 0.90: 1.6449, 0.95: 1.9600}[conf]


def mde(p0, n, conf=0.90, power=0.80):
    """Minimum detectable improvement of a measured proportion over a fixed floor/baseline p0 on n test items
    (one-sample, two-sided at conf, power 0.80; normal approximation)."""
    z_a, z_b = z_for(conf), NormalDist().inv_cdf(power)
    return (z_a + z_b) * math.sqrt(p0 * (1 - p0) / n)


def mde_two_arm(p0, n, conf=0.90):
    """Minimum detectable difference between two arms each evaluated on n items (two-sample)."""
    z_a, z_b = z_for(conf), 0.8416
    return (z_a + z_b) * math.sqrt(2 * p0 * (1 - p0) / n)


def proportion_score_ci(successes, n, conf=0.90):
    """Wilson score interval from counts; NOT a bootstrap."""
    result = wilson_interval(successes, n, conf)
    return result['low'], result['high']


def fit_log_linear(points):
    xs = [math.log2(v) for v, _ in points]
    ys = [a for _, a in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    return slope, my - slope * mx


def power_law_fit(points, prior_b, prior_c, baseline, floor, cap):
    """error(N) = a·N^-b + c with c fixed from the prior (irreducible error above 0) when points < 5.
    Returns examples-to-floor as a range over the prior's b and c bounds, plus a point estimate at the prior midpoints."""
    return power_law_scenarios(points, prior_b, prior_c, floor, cap)


def examples_to_floor_from_prior(baseline, floor, per_point_range, cap):
    gap_points = max(0.0, (floor - baseline) * 100)
    return [int(min(cap, gap_points * per_point_range[0])), int(min(cap, gap_points * per_point_range[1]))]
