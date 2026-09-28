"""Bounded/budgeted per-run census engine for PHASE 3 CENSUS AUTONOMY SERVICE.

Owner R-106 §3 verbatim (banked in STATE/DECISIONS.md at 4k Commit-B
f775adf6):

> "The census engine productized: port the estate_census v3 logic into
> backend services (additive; adapters over the sealed data_source
> packages), tenant-scoped from birth, LawfulBasisAdmit + all-reads-
> receipted + no-second-store invariants enforced in the service path,
> bounded/budgeted per run."

Owner R-106 §4 verbatim: 'mid-run decisions bank a response-required
item to a queue surfaced via UI badge · service CONTINUES on non-blocked
lanes · NEVER stalls'.
Owner R-106 §7 verbatim: 'Degradation honesty: unreachable surface →
BLOCKED row · unreachable GPU host → deferred-not-failed · run always
completes and reports.'

Shape at PHASE 3 Commit-A: additive scaffold with public callables
required by `scheduler_program.py`. Full estate_census v3 port + adapter
wiring lands in PHASE 3 Commit-A' + Commit-A'' sub-slices (Order B
content-axis + Order A NAS/OBS fold-in per R-106 §7 job catalogue).
"""

from __future__ import annotations

import json
import os
import pathlib
import time
import uuid
from typing import Any, Dict, Final, Mapping, Tuple

from services.census_autonomy.service_shape import REFUSAL_PATH_CLOSED_VOCAB

# Queue directory for pending scheduled + on-demand jobs. Persistent
# across pod restarts per R-106 §1 (see /app/assessment_workspace/
# phase0/census_autonomy_state/ mirror at ops-proof time).
CENSUS_STATE_DIR: Final[pathlib.Path] = pathlib.Path(
    os.environ.get(
        "CENSUS_AUTONOMY_STATE_DIR",
        "/app/assessment_workspace/phase0/census_autonomy_state",
    )
)
PENDING_JOBS_SUBDIR: Final[str] = "pending"
RESULTS_SUBDIR: Final[str] = "results"
REFUSAL_ROWS_SUBDIR: Final[str] = "refusal_rows"


def _ensure_state_dirs() -> None:
    """Create state directories if absent (idempotent)."""
    for sub in (PENDING_JOBS_SUBDIR, RESULTS_SUBDIR, REFUSAL_ROWS_SUBDIR):
        (CENSUS_STATE_DIR / sub).mkdir(parents=True, exist_ok=True)


def get_pending_scheduled_runs() -> Tuple[Dict[str, Any], ...]:
    """Return the current pending census jobs cursor (oldest-first).

    Reads deterministic filesystem cursor at
    `<CENSUS_STATE_DIR>/pending/*.json`. Returns tuple (immutable) so
    the caller cannot mutate the cursor. Empty tuple when idle.

    R-106 §2: 'weekly default per prototype · configurable per tenant ·
    on-demand JWT-gated trigger'. The weekly scheduler + on-demand API
    both write into this cursor; this callable is the single reader.
    """
    _ensure_state_dirs()
    pending_dir = CENSUS_STATE_DIR / PENDING_JOBS_SUBDIR
    if not pending_dir.exists():
        return ()
    jobs = []
    for path in sorted(pending_dir.glob("*.json")):
        try:
            jobs.append(json.loads(path.read_text()))
        except Exception:  # noqa: BLE001  degradation-honesty
            # Malformed job files are skipped; scheduler continues.
            continue
    return tuple(jobs)


def _write_refusal_row(
    census_run_id: str,
    tenant_id: str,
    code: str,
    detail: str,
) -> pathlib.Path:
    """Bank a refusal row per R-106 §7 degradation-honesty.

    Raises ValueError if `code` is not in the frozen refusal vocab.
    """
    if code not in REFUSAL_PATH_CLOSED_VOCAB:
        raise ValueError(
            f"Refusal code {code!r} not in REFUSAL_PATH_CLOSED_VOCAB "
            f"{REFUSAL_PATH_CLOSED_VOCAB}"
        )
    _ensure_state_dirs()
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    receipt = {
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "refusal_code": code,
        "detail": detail,
        "banked_at_utc": ts,
    }
    path = (
        CENSUS_STATE_DIR
        / REFUSAL_ROWS_SUBDIR
        / f"{ts}_{census_run_id}_{code}.json"
    )
    path.write_text(json.dumps(receipt, indent=2))
    return path


def _write_result_receipt(
    census_run_id: str,
    tenant_id: str,
    payload: Mapping[str, Any],
) -> pathlib.Path:
    """Write a completed-run result receipt per R-106 §5."""
    _ensure_state_dirs()
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    receipt = {
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "completed_at_utc": ts,
        "payload": dict(payload),
    }
    path = (
        CENSUS_STATE_DIR
        / RESULTS_SUBDIR
        / f"{ts}_{census_run_id}_result.json"
    )
    path.write_text(json.dumps(receipt, indent=2))
    return path


def _remove_pending_job(census_run_id: str) -> None:
    """Remove a pending job cursor entry after the job completes."""
    _ensure_state_dirs()
    for path in (CENSUS_STATE_DIR / PENDING_JOBS_SUBDIR).glob(
        f"*{census_run_id}*.json"
    ):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def run_bounded_census(
    job: Mapping[str, Any],
    job_deadline: float,
) -> Dict[str, Any]:
    """Execute a bounded census run for a single job.

    R-106 §3: 'bounded/budgeted per run'.
    R-106 §4: 'CONTINUES on everything not blocked — it never stalls'.
    R-106 §7: 'unreachable surface → BLOCKED row · run always completes
    and reports'.

    Job payload minimum shape:
      {"census_run_id": str, "tenant_id": str, "trigger": str,
       "connect_source_descriptor": dict, "lawful_basis_admit_ref": str}

    Returns a summary dict banking the run outcome (also written to
    disk via _write_result_receipt so the loop is crash-resumable).
    """
    # Reuse the real scoped runner. Shape-only COMPLETE is no longer an engine
    # result, even for a caller outside the currently mounted HTTP routes.
    from services.census_autonomy.operational_runner import run_bounded_census as execute
    return execute(job,job_deadline)


def enqueue_on_demand_run(
    tenant_id: str,
    connect_source_descriptor: Mapping[str, Any],
    lawful_basis_admit_ref: str,
) -> str:
    """Enqueue an on-demand census run for the scheduler to pick up.

    Called by `POST /api/portal/census/run` (JWT-gated · Phase 3
    continuation router wire-up).
    """
    _ensure_state_dirs()
    census_run_id = f"cr-{uuid.uuid4().hex[:12]}"
    job = {
        "census_run_id": census_run_id,
        "tenant_id": tenant_id,
        "trigger": "on_demand_api",
        "connect_source_descriptor": dict(connect_source_descriptor),
        "lawful_basis_admit_ref": lawful_basis_admit_ref,
        "enqueued_at_utc": time.strftime(
            "%Y%m%dT%H%M%SZ", time.gmtime()
        ),
    }
    path = (
        CENSUS_STATE_DIR
        / PENDING_JOBS_SUBDIR
        / f"{job['enqueued_at_utc']}_{census_run_id}.json"
    )
    path.write_text(json.dumps(job, indent=2))
    return census_run_id
