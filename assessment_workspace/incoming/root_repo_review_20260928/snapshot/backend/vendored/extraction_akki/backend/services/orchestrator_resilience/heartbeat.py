"""Heartbeat — point-in-time liveness record for pod-side orchestrators.

A heartbeat is written by the orchestrator on each poll cycle. The file
carries enough state that a reader can decide (a) whether the
orchestrator is still alive, and (b) if it died, when and mid-what
cycle. Successive writes REPLACE the prior snapshot; the file at any
moment reflects the most-recent tick.

Zero-influence: writes swallow storage failures. A heartbeat is an
observer, never a run participant."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)


REQUIRED_FIELDS = (
    "run_id",
    "orchestrator_pid",
    "at_utc",
    "cycle_count",
    "on_host_status",
    "next_poll_planned_utc",
)


def _root() -> Path:
    return Path(os.environ.get(
        "ORCHESTRATOR_HEARTBEAT_DIR",
        "/app/assessment_workspace/phase0/orchestrator_heartbeat",
    ))


def _hb_path(run_id: str) -> Path:
    return _root() / f"{run_id}.json"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_heartbeat(
    run_id: str,
    orchestrator_pid: int,
    cycle_count: int,
    on_host_status: Dict[str, str],
    next_poll_planned_utc: str,
) -> bool:
    """Write (replace) the heartbeat snapshot for `run_id`.

    Returns True on success, False on any storage failure. Never
    raises (zero-influence discipline)."""
    try:
        d = _root()
        d.mkdir(parents=True, exist_ok=True)
        rec: Dict[str, Any] = {
            "run_id": run_id,
            "orchestrator_pid": int(orchestrator_pid),
            "at_utc": _iso_now(),
            "cycle_count": int(cycle_count),
            "on_host_status": dict(on_host_status),
            "next_poll_planned_utc": next_poll_planned_utc,
        }
        _hb_path(run_id).write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return True
    except Exception as exc:
        log.warning("heartbeat write failed for run_id=%r: %r", run_id, exc)
        return False


def read_heartbeat(run_id: str) -> Optional[Dict[str, Any]]:
    """Return the current heartbeat snapshot, or None if none exists."""
    p = _hb_path(run_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def orchestrator_is_live(run_id: str, max_staleness_s: int = 600) -> bool:
    """Freshness check: return True iff a heartbeat exists AND its
    `at_utc` is within `max_staleness_s` seconds of now.

    Default max_staleness_s = 600 s = 2× the typical 300 s poll
    interval. The DECISIONS.md 2026-09-01T02:55Z reconcile finding
    established that 5-min polls should never lapse more than one
    cycle; two missed cycles is the operational "presumed dead"
    threshold."""
    rec = read_heartbeat(run_id)
    if rec is None:
        return False
    try:
        at = rec.get("at_utc", "")
        t = datetime.fromisoformat(at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return False
    age_s = (datetime.now(timezone.utc) - t).total_seconds()
    return age_s <= max_staleness_s


def retire_heartbeat(run_id: str) -> bool:
    """Remove the heartbeat file for `run_id` on clean orchestrator exit.

    Introduced in W-Campaign-Infra (folding lean r3 items in). The r2
    close honest-limit banked: "No heartbeat retirement on clean exit
    (stays on disk)". This function is the retirement primitive — the
    orchestrator calls it in its clean-exit path so `find_orphaned_runs`
    doesn't surface a completed run as an orphan just because its
    heartbeat file was never cleaned up.

    Returns True if a file existed and was removed. Returns False if
    no file existed OR the removal failed (zero-influence: never
    raises)."""
    p = _hb_path(run_id)
    if not p.exists():
        return False
    try:
        p.unlink()
        return True
    except OSError as exc:
        log.warning("retire_heartbeat unlink failed for run_id=%r: %r",
                    run_id, exc)
        return False
