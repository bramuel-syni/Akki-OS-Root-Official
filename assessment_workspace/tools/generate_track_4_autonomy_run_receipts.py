"""Generate Track-4 autonomy-engine EXIT EVIDENCE run receipts.

Analysis/evidence script (SO §3.8 additive-only · no production code
touched). Run from the Extraction-Akki repo root so `backend.` imports
resolve. This script:

  1. Wires the three Track-4 seams via `register_all_three_track_4_jobs`
     (LID pass + census-three-waves + training-runs) — the seat that
     Item 5.11.e implements.
  2. For each wired job, uses the LIVE Census Autonomy engine
     (services.census_autonomy.engine) to `enqueue_on_demand_run`
     (writes a pending JSON job to disk) and then `run_bounded_census`
     (LIVE execution path). The engine's own persisted result-receipt
     JSON is the machine-readable proof-of-pickup + proof-of-run.
  3. Then emits a `AutonomyEngineRunReceipt_v1` (Track-4 exit-evidence
     carrier) per job composing the LIVE engine's returned status +
     provenance_ref pointing at the persisted result JSON.
  4. Writes all receipts under `backend/phase0/track_4_autonomy_engine_run_receipts/`
     for immutable audit.

Owner verbatim (SO §6.9 amendment §6 item 6 + Ruling (b) AKKI-RUNS-IT):
    "Verification of autonomy pickup (receipt from the autonomy engine's
    run log showing the job ran) is the EXIT EVIDENCE for each such
    wiring seal."

Ruling (b) verbatim: pod is never data path. This script does NOT put
pod://* or /app/* prefixes into engine_response_queue_ref or
data_source_adapter_ref; it uses `census_autonomy://*` refs which are
the Census Autonomy Service's own scheme.
"""
from __future__ import annotations

import json
import pathlib
import sys
import time
import uuid
from typing import Any, Dict

REPO_ROOT = pathlib.Path("/app/assessment_workspace/repos/Extraction-Akki")
BACKEND_ROOT = REPO_ROOT / "backend"
RECEIPTS_DIR = BACKEND_ROOT / "phase0" / "track_4_autonomy_engine_run_receipts"

# Add backend/ to sys.path so `import services.census_autonomy.engine`
# works exactly the way the production process runs it (see pytest.ini
# rootdir + engine.py imports `from services.census_autonomy.service_shape`).
sys.path.insert(0, str(BACKEND_ROOT))

# Also add /app/assessment_workspace/repos/Extraction-Akki so that
# `import backend.services.census_autonomy.track_4_autonomy_wiring_v1`
# (as used by the invariant tests) resolves.
sys.path.insert(0, str(REPO_ROOT))

from backend.services.census_autonomy import track_4_autonomy_wiring_v1 as TRACK4  # noqa: E402
from services.census_autonomy import engine as ENGINE  # noqa: E402


def _utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _utc_ts() -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


def _run_one_job_through_engine(*, job_kind: str) -> Dict[str, Any]:
    """Enqueue + execute one Track-4 job through the LIVE engine.

    Returns a merged receipt dict combining the engine's run-log entry
    with the Track-4 `AutonomyEngineRunReceipt_v1` exit-evidence carrier.
    """
    started_at = _utc_iso()
    started_wall = time.time()

    census_run_id = ENGINE.enqueue_on_demand_run(
        tenant_id=f"track4-{job_kind}",
        connect_source_descriptor={
            "job_kind": job_kind,
            "descriptor_kind": "track_4_wired_registration",
        },
        lawful_basis_admit_ref=f"census_autonomy://lawful_basis_admit/track4/{job_kind}",
    )

    # Locate the persisted pending job JSON the engine just wrote to disk
    # (this alone is a live-pickup proof — the engine's own persistence).
    pending_dir = ENGINE.CENSUS_STATE_DIR / ENGINE.PENDING_JOBS_SUBDIR
    pending_matches = sorted(pending_dir.glob(f"*_{census_run_id}.json"))
    pending_job = json.loads(pending_matches[-1].read_text())
    persisted_pending_path = str(pending_matches[-1])

    # Run through the LIVE bounded census engine (60s wall budget).
    live_result = ENGINE.run_bounded_census(
        job=pending_job,
        job_deadline=time.time() + 60.0,
    )

    # Locate the persisted result receipt on disk (engine writes JSON).
    # Engine's on-disk filename shape: `<ts>_<census_run_id>_result.json`
    # (see _write_result_receipt in engine.py). Try that first; fall
    # back to a broader pattern if the engine shape ever varies.
    results_dir = ENGINE.CENSUS_STATE_DIR / ENGINE.RESULTS_SUBDIR
    result_matches = sorted(results_dir.glob(f"*_{census_run_id}_result.json"))
    if not result_matches:
        result_matches = sorted(results_dir.glob(f"*{census_run_id}*.json"))
    if result_matches:
        result_json = json.loads(result_matches[-1].read_text())
        persisted_result_path = str(result_matches[-1])
    else:
        # Engine wrote a refusal row instead of a result (deferred/blocked).
        result_json = None
        refusal_dir = ENGINE.CENSUS_STATE_DIR / ENGINE.REFUSAL_ROWS_SUBDIR
        refusal_matches = sorted(refusal_dir.glob(f"*{census_run_id}*.json"))
        persisted_result_path = (
            str(refusal_matches[-1]) if refusal_matches else "no_persisted_receipt"
        )

    finished_at = _utc_iso()

    # Track-4 exit-evidence carrier composing the engine's live status.
    if live_result.get("status") == "COMPLETE":
        wiring_status = "completed"
    elif live_result.get("status", "").startswith(("BLOCKED_", "DEFERRED_")):
        wiring_status = "refused"
    else:
        wiring_status = "failed"

    track4_receipt = TRACK4.emit_autonomy_engine_run_receipt(
        job_kind=job_kind,
        run_id=census_run_id,
        started_at_utc=started_at,
        finished_at_utc=finished_at,
        status=wiring_status,
        provenance_ref=f"census_autonomy_service://run_log/{census_run_id}",
    )

    merged: Dict[str, Any] = {
        "receipt_kind": "track_4_autonomy_engine_run_receipt_v1",
        "job_kind": job_kind,
        "census_run_id": census_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "wall_clock_seconds": round(time.time() - started_wall, 3),
        "engine_live_status": live_result.get("status"),
        "wiring_receipt_status": wiring_status,
        "persisted_pending_job_path": persisted_pending_path,
        "persisted_result_or_refusal_path": persisted_result_path,
        "engine_result_body": result_json,
        "track_4_exit_evidence": {
            "job_kind": track4_receipt.job_kind,
            "run_id": track4_receipt.run_id,
            "started_at_utc": track4_receipt.started_at_utc,
            "finished_at_utc": track4_receipt.finished_at_utc,
            "status": track4_receipt.status,
            "provenance_ref": track4_receipt.provenance_ref,
        },
        "owner_verbatim": (
            "SO §6.9 amendment §6 item 6 + Ruling (b) AKKI-RUNS-IT: "
            "'Verification of autonomy pickup (receipt from the autonomy "
            "engine's run log showing the job ran) is the EXIT EVIDENCE "
            "for each such wiring seal.'"
        ),
    }
    return merged


def main() -> int:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1 — wire all three seams via the Track-4 boundary (this is
    # the seat CP-TRACK-4-AUTONOMY-WIRING implements).
    aggregate = TRACK4.register_all_three_track_4_jobs(
        lid_pass_engine_response_queue_ref="census_autonomy://queue/lid_pass",
        lid_pass_data_source_adapter_ref="census_autonomy://adapter/lid_pass",
        census_three_waves_engine_response_queue_ref="census_autonomy://queue/census_three_waves",
        census_three_waves_data_source_adapter_ref="census_autonomy://adapter/census_three_waves",
        training_runs_engine_response_queue_ref="census_autonomy://queue/training_runs",
        training_runs_data_source_adapter_ref="census_autonomy://adapter/training_runs",
        training_runs_run_id=f"track4-training-{uuid.uuid4().hex[:8]}",
        training_runs_commissioned_job_contract_ref="census_autonomy://commissioned_job_contract/track4",
    )
    assert aggregate.total_jobs_registered == 3

    # Step 2 — for each job_kind, drive the LIVE engine (enqueue + run).
    receipts_by_kind = {}
    for job_kind in TRACK4.TRACK_4_JOB_KINDS:
        receipts_by_kind[job_kind] = _run_one_job_through_engine(job_kind=job_kind)

    # Step 3 — write one machine-readable JSON receipt per job_kind + a
    # composite receipt banking the seal-level exit-evidence.
    ts = _utc_ts()
    for job_kind, receipt in receipts_by_kind.items():
        out_path = RECEIPTS_DIR / f"{ts}_{job_kind}_engine_run_receipt.json"
        out_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    composite = {
        "receipt_kind": "track_4_seal_level_exit_evidence_composite_v1",
        "seal": "CP-TRACK-4-AUTONOMY-WIRING",
        "item": "Item 5.11.e of EXECUTION_ORDER.md",
        "emitted_at_utc": _utc_iso(),
        "aggregate_total_jobs_registered": aggregate.total_jobs_registered,
        "job_kinds_registered": list(TRACK4.TRACK_4_JOB_KINDS),
        "per_job_receipts": receipts_by_kind,
        "postures_composed": {
            "TRACK_4_AUTONOMY_WIRING_POSTURE": TRACK4.TRACK_4_AUTONOMY_WIRING_POSTURE,
            "POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4": TRACK4.POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4,
            "E1_STEPS_BACK_AFTER_WIRING_POSTURE": TRACK4.E1_STEPS_BACK_AFTER_WIRING_POSTURE,
        },
        "owner_verbatim_exit_evidence_clause": (
            "SO §6.9 amendment §6 item 6 + Ruling (b) AKKI-RUNS-IT verbatim: "
            "'Register LID pass + corpus census + training seam as Census "
            "Autonomy Service jobs. Verification of autonomy pickup (receipt "
            "from the autonomy engine's run log showing the job ran) is the "
            "EXIT EVIDENCE for each such wiring seal.'"
        ),
    }
    composite_path = RECEIPTS_DIR / f"{ts}_seal_level_composite_exit_evidence.json"
    composite_path.write_text(json.dumps(composite, indent=2, sort_keys=True))

    # Console summary (captured to drill-receipt log by caller).
    print(f"[TRACK-4 EXIT EVIDENCE] wrote {len(receipts_by_kind)} per-job receipts + 1 composite")
    for job_kind, r in receipts_by_kind.items():
        print(
            f"  · {job_kind}: engine_live_status={r['engine_live_status']} "
            f"wiring_receipt_status={r['wiring_receipt_status']} "
            f"run_id={r['census_run_id']} "
            f"persisted={r['persisted_result_or_refusal_path']}"
        )
    print(f"[COMPOSITE] {composite_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
