"""Trainer backends. The runner talks to this interface and nothing else.

StubBackend: metrics are a deterministic function of (seed, stratum, volume,
arm) from policy.stub. Carries no evidential weight; every artefact says so.

RealBackend: the adapter the trainer runner (A17.12) will implement. It is a
contract here, not an implementation: instantiating it raises with the
contract stated. A17.9 applies: execution_mode is read from AKKI_EXECUTION_MODE
at import; unset or invalid raises; no silent CPU fallback.
"""
import hashlib, math, os


class TrainerBackend:
    name = "abstract"
    evidential_weight = None

    def calibrate(self, stratum, volume, manifest_slice_ref, arm="A"):
        """→ {"accuracy": float, "coverage": float, "gpu_hours": float, "checkpoint_ref": str}"""
        raise NotImplementedError

    def compare(self, stratum, volume, arms, manifest_slice_ref):
        """→ {arm: calibrate-shaped result + "compute_to_convergence_gpu_hours"} for each arm; identical data/base/eval/cap."""
        raise NotImplementedError

    def full(self, per_stratum_examples, recipe_version, manifest_ref):
        """→ completion certificate fields (policy.completion_certificate.fields). Never called before the Owner verdict is recorded."""
        raise NotImplementedError


class StubBackend(TrainerBackend):
    name = "stub"
    evidential_weight = "none — stub metrics are a deterministic function of the seed (see policy.stub.note)"

    def __init__(self, plan):
        self.plan, self.sp, self.seed = plan, plan["stub_policy"], plan["seed"]
        self.v0 = plan["calibration"]["volumes"][0]

    def _noise(self, *keys, scale):
        h = hashlib.sha256(":".join([self.seed, *map(str, keys)]).encode()).hexdigest()
        return (int(h[:8], 16) / 0xFFFFFFFF - 0.5) * 2 * scale

    def calibrate(self, stratum, volume, manifest_slice_ref, arm="A"):
        s = self.plan["strata"][stratum]
        steps = math.log2(volume / self.v0) + 1
        shift = 0.0 if arm == "A" else self._noise("arm", stratum, scale=0.006)
        acc = min(0.99, s["baseline_accuracy"] + self.sp["gain_per_log2_volume"][stratum] * steps + self._noise(stratum, volume, "acc", scale=self.sp["noise"]) + shift)
        cov = min(0.995, s["baseline_coverage"] + self.sp["coverage_gain_per_log2_volume"] * steps + self._noise(stratum, volume, "cov", scale=self.sp["noise"] / 2))
        cal = self.plan["calibration"]
        hrs = volume / 1000 * cal["epochs"] * self.plan["rates"]["gpu_hours_per_1000_examples_epoch"] + self.plan["rates"]["eval_gpu_hours_per_stratum"]
        train_gap = self.sp.get("train_gap", 0.01) + self._noise(stratum, volume, "gap", scale=0.004)
        return {"accuracy": round(acc, 4), "train_accuracy": round(min(0.999, acc + train_gap), 4), "coverage": round(cov, 4), "gpu_hours": round(hrs, 3), "checkpoint_ref": f"stub-ckpt-{stratum}-{volume}-{arm}"}

    def compare(self, stratum, volume, arms, manifest_slice_ref):
        """arms: list of {"arm","config"}; B carries the lever. Stub: B gains a share of the lever's expected effect (from the policy prior), deterministic."""
        out = {}
        for spec in arms:
            arm = spec["arm"]
            r = self.calibrate(stratum, volume, manifest_slice_ref, arm=arm)
            if arm == "B" and spec.get("expected_effect") and spec["expected_effect"].get("low") is not None:
                eff = spec["expected_effect"]
                gain = -(eff["low"] + eff["high"]) / 2 * (1 - r["accuracy"]) if eff["metric"].startswith("relative") else (eff["low"] + eff["high"]) / 2
                r["accuracy"] = round(min(0.99, r["accuracy"] + gain * (0.8 + self._noise("lever", stratum, scale=0.2))), 4)
            r["config"] = spec["config"]
            r["compute_to_convergence_gpu_hours"] = round(r["gpu_hours"] * (1.0 if arm == "A" else 0.86 + self._noise("c2c", arm, scale=0.05)), 3)
            out[arm] = r
        return out

    def full(self, *a, **k):
        raise RuntimeError("stub backend never runs the full stage; the full run is conditional on the Owner verdict and is not simulated")


class RealBackend(TrainerBackend):
    name = "real"
    CONTRACT = ("RealBackend is the adapter for the trainer runner (A17.12, ~2–3k LOC, not built). Contract: calibrate/compare/full as above; "
                "reads AKKI_EXECUTION_MODE ∈ {cuda, cpu} at import and raises otherwise (A17.9); dispatches through the platform's custody seam "
                "(training reads are custody reads, Doc 1); writes checkpoints every N steps per recipe (C.20.6); returns per-stratum results "
                "against the sealed test set; never returns a verdict.")

    def __init__(self, plan):
        mode = os.environ.get("AKKI_EXECUTION_MODE")
        if mode not in ("cuda", "cpu"):
            raise ImportError("AKKI_EXECUTION_MODE unset or invalid; no silent fallback (A17.9)")
        raise NotImplementedError(self.CONTRACT)


def make(plan):
    return {"stub": StubBackend, "real": RealBackend}[plan["backend"]](plan)
