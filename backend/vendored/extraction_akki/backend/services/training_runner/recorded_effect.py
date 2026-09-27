"""Legacy result custody only; never admission, a new job authority or LIVE proof.

Write-once local sidecars reuse the runner's configured custody directory. A
durable claim precedes the external effect. Unknown outcomes never auto-resubmit;
the governed execution spine remains the live recovery/admission authority.
"""
import json
import os
import math
from dataclasses import asdict
from hashlib import sha256
from services.training_runner import persistence
from services.training_runner.ssh_seam import SeamResult


def identity(run):
    return {k: getattr(run, k) for k in ("run_id", "recipe_version", "base_model_id", "material_admit_ref", "adapter_kind")}


def _digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _path(run, stage):
    root = persistence._active_runs_dir() / "recorded_effects"
    root.mkdir(parents=True, exist_ok=True)
    return root / (_digest({"run_id": run.run_id}) + "." + stage + ".json")


def write_once(run, stage, value):
    target = _path(run, stage)
    body = {"identity": identity(run), "value": value}
    raw = json.dumps({**body, "sha256": _digest(body)}, sort_keys=True, allow_nan=False).encode()
    # The exclusive name is the claim. A truncated write is held, never re-run.
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        directory = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        # Keep the claim even if persistence fails: the external outcome is uncertain.
        raise


def read(run, stage):
    target = _path(run, stage)
    if not target.exists():
        return None
    try:
        saved = json.loads(target.read_text())
        if saved["identity"] != identity(run) or saved["sha256"] != _digest({
                "identity": saved["identity"], "value": saved["value"]}):
            raise ValueError("Stored effect identity/integrity mismatch.")
        return saved["value"]
    except (ValueError, KeyError, TypeError):
        raise RuntimeError("TRAINING_RESULT_CUSTODY_INVALID") from None


def result(run):
    value = read(run, "result")
    if value is None:
        raise RuntimeError("TRAINING_RESULT_NOT_RECORDED")
    try:
        parsed = SeamResult(**value)
        if type(parsed.mocked) is not bool or type(parsed.exit_code) is not int:
            raise ValueError("Invalid result types")
        if parsed.exit_code != 0:
            raise RuntimeError("TRAINING_EFFECT_FAILED")
        for name in ("wallclock_seconds", "gpu_hours", "m_a_input", "m_b_input", "m_e_input"):
            quantity = getattr(parsed, name)
            if type(quantity) not in (int, float) or not math.isfinite(quantity) or quantity < 0:
                raise ValueError("Invalid measured quantity")
        return parsed
    except (TypeError, ValueError):
        raise RuntimeError("TRAINING_RESULT_INVALID") from None


def execute_once(run, execute):
    if read(run, "result") is not None:
        return result(run)
    if run.status != "admitted":
        raise RuntimeError("HISTORICAL_TRAINING_RESULT_REQUIRES_RECOVERY")
    try:
        write_once(run, "claim", {"status": "effect_claimed"})
    except FileExistsError:
        raise RuntimeError("TRAINING_EFFECT_OUTCOME_UNCERTAIN") from None
    observed = execute(run.recipe_version, run.base_model_id, run.material_admit_ref)
    if not isinstance(observed, SeamResult):
        raise RuntimeError("TRAINING_RESULT_INVALID")
    write_once(run, "result", asdict(observed))
    return result(run)