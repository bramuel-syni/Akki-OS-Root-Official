"""Evaluation statistics and scaling fits. Arithmetic the professor lens relies on."""
import hashlib, math


def z_for(conf):
    return {0.80: 1.2816, 0.90: 1.6449, 0.95: 1.9600}[conf]


def mde(p0, n, conf=0.90, power=0.80):
    """Minimum detectable improvement of a measured proportion over a fixed floor/baseline p0 on n test items
    (one-sample, two-sided at conf, power 0.80; normal approximation)."""
    z_a, z_b = z_for(conf), 0.8416
    return (z_a + z_b) * math.sqrt(p0 * (1 - p0) / n)


def mde_two_arm(p0, n, conf=0.90):
    """Minimum detectable difference between two arms each evaluated on n items (two-sample)."""
    z_a, z_b = z_for(conf), 0.8416
    return (z_a + z_b) * math.sqrt(2 * p0 * (1 - p0) / n)


def bootstrap_prop_ci(successes, n, seed, conf=0.90, draws=500):
    """Bootstrap interval for a proportion from n binary items (item resampling)."""
    p = successes / n
    ests = []
    for i in range(draws):
        h = hashlib.sha256(f"{seed}:{i}".encode()).digest()
        # deterministic binomial via many uniform draws would be slow; use normal approx with hashed noise
        u = int.from_bytes(h[:8], "big") / 2**64
        v = int.from_bytes(h[8:16], "big") / 2**64
        zn = math.sqrt(-2 * math.log(max(u, 1e-12))) * math.cos(2 * math.pi * v)
        ests.append(min(1, max(0, p + zn * math.sqrt(p * (1 - p) / n))))
    ests.sort()
    return ests[int((1 - conf) / 2 * draws)], ests[int((1 + conf) / 2 * draws) - 1]


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
    # errors are 1 - accuracy; irreducible c as a floor error
    pts = [(v, 1 - a) for v, a in points]
    out = {}
    for tag, b, c in (("low", prior_b[1], prior_c[0]), ("mid", sum(prior_b) / 2, sum(prior_c) / 2), ("high", prior_b[0], prior_c[1])):
        # fit a with b, c fixed: a = mean over points of (e - c) * N^b
        a_est = sum(max(e - c, 1e-4) * (v ** b) for v, e in pts) / len(pts)
        target_err = 1 - floor
        if target_err <= c:
            out[tag] = None  # floor below irreducible error: not reachable on this prior
        else:
            out[tag] = int(min(cap, (a_est / (target_err - c)) ** (1 / b)))
    return out


def examples_to_floor_from_prior(baseline, floor, per_point_range, cap):
    gap_points = max(0.0, (floor - baseline) * 100)
    return [int(min(cap, gap_points * per_point_range[0])), int(min(cap, gap_points * per_point_range[1]))]
