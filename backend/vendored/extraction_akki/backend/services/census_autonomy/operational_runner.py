"""Bounded operational executor composition. No sealed engine body is modified."""
import hashlib
import json
import os
import time
from pathlib import Path

from services.census_autonomy import engine, operational_store as store
from services.census_autonomy.operational_scope import SOURCE_TENANTS
from services.census_autonomy.operational_validation import PROTOCOL, validate_output, classify_payload
from services.mtafiti.census_result_adapter import register_outcome


def admission_path():
    path = Path(os.environ["CENSUS_LAWFUL_BASIS_PATH"])
    raw = path.read_bytes()
    doc = json.loads(raw)
    if not doc.get("receipt_id") or doc.get("invariants", {}).get("read_only") is not True:
        raise ValueError("Read-only census admission is absent or invalid.")
    if not doc.get("scope"):
        raise ValueError("Census admission has no scope.")
    return path, hashlib.sha256(raw).hexdigest()


def run_bounded_census(job, job_deadline, execute=None):
    run_id, tenant = job.get("census_run_id"), job.get("tenant_id")
    descriptor = job.get("connect_source_descriptor") or {}
    with store.lock(f"execute:{run_id}", blocking=False) as acquired:
        if not acquired:
            return {"status": "PENDING", "census_run_id": run_id}
        current = store.get(run_id, tenant)
        if current and current["status"] != "PENDING":
            engine._remove_pending_job(run_id)
            return current
        try:
            if descriptor.get("version") != "operational-v1" or not current:
                raise ValueError("Legacy descriptor has no validated operational binding; no source read performed.")
            if time.time() >= job_deadline:
                raise TimeoutError("Census budget expired before execution.")
            bound = int(os.environ["CENSUS_JOB_MAX_SECONDS"])
            if bound <= 0:
                raise TimeoutError("Census budget does not permit execution.")
            job_deadline = min(job_deadline, time.time() + bound)
            if current["source_ids"] != descriptor.get("source_ids") or any(
                    SOURCE_TENANTS.get(s) != tenant for s in current["source_ids"]):
                raise ValueError("Source scope does not match the admitted tenant.")
            path, admit_hash = admission_path()
            if str(path) != job.get("lawful_basis_admit_ref") or descriptor.get("lawful_basis_sha256") != admit_hash:
                raise ValueError("Unrecognized lawful-basis reference.")
            current.update(stage="executing", started_at=store.now(), deadline=job_deadline)
            store.save(current)
            if execute is None:
                _mode = os.environ.get("AKKI_CENSUS_EXECUTION_MODE")
                if _mode == "non_gpu_jump":
                    from services.census_autonomy.jump_dispatch import execute_source
                elif _mode == "non_gpu_worker":
                    from services.census_autonomy.non_gpu_dispatch import execute_source
                else:
                    from services.census_autonomy.remote_dispatch import execute_source
                execute = execute_source
            outcomes, registry = [], []
            for source in current["source_ids"]:
                if time.time() >= job_deadline:
                    outcome = {"source_id": source, "status": "blocked", "reason_code": "BUDGET_EXHAUSTED"}
                else:
                    try:
                        value = execute(run_id, tenant, source, admit_hash, job_deadline)
                        outcome = validate_output(value, run_id, tenant, source)
                        if outcome["status"] == "complete":
                            registry.append(register_outcome(outcome))
                    except Exception as exc:
                        outcome = {"source_id": source, "status": "blocked", "reason_code": "EXECUTION_NOT_VERIFIED",
                                   "error_type": type(exc).__name__}
                outcomes.append(outcome)
                current = store.get(run_id, tenant) or current
                current["outcomes"] = outcomes
                store.save(current)
            payload = {"protocol": PROTOCOL, "outcomes": outcomes, "registry_receipts": registry,
                       "lawful_basis_sha256": admit_hash, "principal_id": current["principal_id"]}
            # Live DQ producer: bank owner-answerable unblock actions for real per-host
            # census gaps. Additive, guarded — never fails the run.
            try:
                from services.census_autonomy.census_dq_producer import emit_from_run
                emit_from_run(run_id, tenant)
            except Exception:
                pass
            outcome_class = classify_payload(payload)
            # The same sealed census writer owns durable results; the cursor is not a second registry.
            receipt = engine._write_result_receipt(run_id, tenant, payload)
            with receipt.open("rb") as persisted:
                os.fsync(persisted.fileno())
            if json.loads(receipt.read_text())["payload"] != payload:
                raise ValueError("Result persistence could not be verified.")
            current.update(status="COMPLETE" if outcome_class == "COMPLETE" else "REFUSED",
                           stage=outcome_class.lower(), finished_at=store.now(),
                           proof_ref=f"census_autonomy_state/results/{receipt.name}",
                           proof_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest())
            store.save(current)
        except Exception as exc:
            code = "DEFERRED_BUDGET_EXCEEDED" if isinstance(exc, TimeoutError) else "BLOCKED_AWAITING_RESPONSE"
            engine._write_refusal_row(run_id, tenant, code, "Operational census refused; no verified completion. " + type(exc).__name__)
            if current:
                current.update(status="REFUSED", stage="blocked", reason_code=code, finished_at=store.now())
                store.save(current)
        engine._remove_pending_job(run_id)
        return current or {"census_run_id": run_id, "tenant_id": tenant, "status": "REFUSED"}