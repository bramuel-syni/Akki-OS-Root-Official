"""Bounded operational executor composition. No sealed engine body is modified."""
import hashlib
import json
import logging
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


def _scope_job_id(current):
    """Stable id for one progressive-consumption scope across its bounded passes."""
    key = json.dumps([current["tenant_id"], sorted(current.get("source_ids") or []),
                      sorted(current.get("source_refs") or [])], sort_keys=True)
    return "census-" + hashlib.sha256(key.encode()).hexdigest()[:16]


def _progress_ring():
    from services.census_autonomy import engine
    return engine.CENSUS_STATE_DIR / "progress_ring"


def _supervise_pass(current):
    """Supervision Plane (L5, work_supervisor) — 'alive != done'. Record this pass's
    cumulative coverage as a ProgressSignal, then let the designed starvation watchdog
    decide whether the scope is still progressing. Returns (healthy, verdict)."""
    from datetime import datetime, timezone
    from services.work_supervisor.runtime_supervisor import (
        ProgressSignal, record_progress, output_verification_watchdog)
    files = objects = volume = 0
    for outcome in current.get("outcomes", []):
        for s in outcome.get("sources", []):
            files += s.get("file_count") or 0
            objects += s.get("object_count") or 0
            volume += s.get("volume_bytes") or 0
            # Full-content passes progress by objects read and bytes verified after the listing stands still.
            content = s.get("content") or {}
            objects += content.get("objects_read") or 0
            volume += content.get("bytes_read") or 0
    job_id = _scope_job_id(current)
    ring = _progress_ring()
    now = datetime.now(timezone.utc)
    record_progress(ProgressSignal(job_id=job_id, at_utc=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                   magnitude=float(files + objects), output_bytes=int(volume), output_path=job_id),
                    ring_root=ring)
    # A scope that produced ≥2 passes without growing coverage has starved (flatline),
    # even though the worker is 'alive'. SLA is generous: many passes may legitimately run.
    verdict = output_verification_watchdog(job_id, sla_seconds=int(os.environ["CENSUS_JOB_MAX_SECONDS"]) * 6,
                                           ring_root=ring, now_utc=now)
    return (verdict is None or verdict.reason != "starvation_output_flatline"), verdict


def _inherit_scope(current, successor):
    """A successor pass stays the same scoop of the same Targeta-ordered plan."""
    successor['continues_run_id'] = current['census_run_id']
    for key in ('scoop_plan_id', 'scoop_index', 'northena_run_id'):
        if current.get(key) is not None:
            successor[key] = current[key]


def continue_if_resumable(current):
    """Progressive consumption cadence, supervised by the designed L5 work_supervisor:
    a scope keeps scooping while it is genuinely progressing (alive AND done-growing);
    a starved (flatline) scope halts and escalates instead of looping forever."""
    resumable = [o['source_id'] for o in current.get('outcomes', [])
                 if o.get('status') == 'partial'
                 and any(s.get('resumable') and s.get('status') == 'partial'
                         and s.get('reason_code') == 'BUDGET_EXHAUSTED' for s in o.get('sources', []))]
    if not resumable:
        return None
    healthy, verdict = _supervise_pass(current)
    if not healthy:
        # NO RUN WITHOUT PROGRESS (SO §3.2): bank the starvation as owner-answerable, do not continue.
        current['scope_halt'] = {'reason': verdict.reason, 'message': verdict.message, 'at_utc': verdict.at_utc}
        store.save(current)
        return None
    successor, created = store.enqueue(current['tenant_id'], current['principal_id'], resumable,
                                       f"{current['census_run_id']}-continue",
                                       current['lawful_basis_admit_ref'], current.get('worker_id'), current.get('source_refs'), current.get('measurement'))
    if created:
        _inherit_scope(current, successor)
        # A source whose remaining work is confined to a read window (NAS off-peak) sleeps until the window opens.
        waits = [s.get('resume_not_before') for o in current.get('outcomes', []) for s in o.get('sources', [])
                 if s.get('status') == 'partial' and s.get('resumable') and s.get('reason_code') == 'BUDGET_EXHAUSTED']
        if waits and all(waits) and min(waits) > time.time():
            successor['not_before'] = min(waits)
        store.save(successor)
    current['continuation_run_id'] = successor['census_run_id']; store.save(current)
    return successor['census_run_id']


def defer_if_scope_busy(current):
    """The admitted worker refused because this scope's enumeration is still running
    remotely (an orphaned pass after a control-plane restart; its checkpoint is durable).
    Alive is not done: re-enter the queue after a back-off instead of breaking the chain."""
    outcomes = current.get('outcomes', [])
    if not outcomes or not all(o.get('reason_code') == 'ENUMERATION_ALREADY_RUNNING' for o in outcomes):
        return None
    attempt = int(current.get('busy_retry_attempt') or 0) + 1
    if attempt > int(os.environ.get('CENSUS_BUSY_RETRY_MAX', '6')):
        return None
    successor, created = store.enqueue(current['tenant_id'], current['principal_id'], current['source_ids'],
                                       f"{current['census_run_id']}-busy{attempt}",
                                       current['lawful_basis_admit_ref'], current.get('worker_id'), current.get('source_refs'), current.get('measurement'))
    if created:
        _inherit_scope(current, successor)
        successor.update(busy_retry_attempt=attempt,
                         not_before=time.time() + int(os.environ.get('CENSUS_BUSY_RETRY_SECONDS', '900')))
        store.save(successor)
    current['continuation_run_id'] = successor['census_run_id']; store.save(current)
    return successor['census_run_id']


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
                from services.census_autonomy.census_router import execute_source
                execute = execute_source
            outcomes, registry = [], []
            for source in current["source_ids"]:
                if time.time() >= job_deadline:
                    outcome = {"source_id": source, "status": "blocked", "reason_code": "BUDGET_EXHAUSTED"}
                else:
                    try:
                        value = execute(run_id, tenant, source, admit_hash, job_deadline)
                        outcome = validate_output(value, run_id, tenant, source)
                        if outcome["status"] in {"complete", "partial"}:
                            registry.append(register_outcome(outcome))
                    except Exception as exc:
                        outcome = {"source_id": source, "status": "blocked", "reason_code": "EXECUTION_NOT_VERIFIED",
                                   "error_type": type(exc).__name__}
                outcomes.append(outcome)
                current = store.get(run_id, tenant) or current
                current["outcomes"] = outcomes
                store.save(current)
            from services.census_autonomy.deep_response import publish
            publish(current,admit_hash)
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
            from services.census_autonomy.registry_durability import preserve_result
            preserve_result(receipt)
            current.update(status="COMPLETE" if outcome_class == "COMPLETE" else "PARTIAL" if outcome_class == "PARTIAL" else "REFUSED",
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
        # Resumable enumeration continuation is additive and never fails the finished run.
        if current and current.get("status") == "PARTIAL":
            try:
                continue_if_resumable(current)
            except Exception:
                logging.getLogger(__name__).exception("Continuation enqueue failed for %s", run_id)
        # A scope still enumerating remotely re-enters after a back-off (alive != done).
        if current and current.get("status") == "REFUSED":
            try:
                defer_if_scope_busy(current)
            except Exception:
                logging.getLogger(__name__).exception("Deferred re-entry failed for %s", run_id)
        # Shovel cadence: a finished scoop (banked, refused or halted) that did not
        # self-continue advances its Targeta-ordered plan through Northena's ledger.
        if current and current.get("scoop_plan_id"):
            try:
                from services.census_autonomy.census_scoop_origination import advance_plan
                current = store.get(run_id, tenant) or current
                advance_plan(current)
            except Exception:
                logging.getLogger(__name__).exception("Shovel plan advance failed for %s; retained cursor is recoverable", run_id)
        engine._remove_pending_job(run_id)
        return current or {"census_run_id": run_id, "tenant_id": tenant, "status": "REFUSED"}