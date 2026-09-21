"""adopt — auto-adopt an orphaned in-flight run.

Owner charter (banked in DECISIONS.md § W-Orchestrator-Resilience-r2):
  "auto-adopt orphans + watchdog respawn ... zero-influence preserved
   (observer adopts and observes; never terminates on-host jobs)."

An orphan is a run whose pod-side orchestrator died (see `orphan_detector`).
Its on-host job is likely still running because it was launched with
`setsid nohup` (detached process group). Adoption means: a replacement
orchestrator (either respawned via `watchdog` or manually started with
`AKKI_ADOPT_RUN_ID=<orphan_run_id>`) resumes POLLING into the existing
run_dir, honours the prior sealing/poll receipts, and bank a small
`adoption_<utc>_<pid>.json` ledger entry so the audit trail names the
adopting orchestrator.

Adoption is NEVER a mutation of the on-host job. This module does not
ssh, does not signal any process, does not touch the burn payload on
disk on the remote host. It writes ONE small JSON file per adoption
event on the pod side.

Adoptability policy (`can_adopt`):
  * The run MUST NOT be sealed (no `ACTIVITY_SUMMARY.md`).
  * The run MUST have at least one launch record and one poll receipt
    (in-flight predicate from `orphan_detector._looks_in_flight`).
  * The most recent poll receipt's mtime MUST be within `max_poll_age_s`
    seconds of now (default 900 s = 15 min = ~5× typical poll interval).
    If stale beyond that, the on-host job is probably already gone;
    refuse and let the operator inspect.

Idempotency (`mark_adopted`):
  * If a fresh adoption record exists within `dedupe_window_s` seconds
    (default 30 s), return that record; do NOT write a second file.
    This protects against a supervisor firing twice in quick succession.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger(__name__)


SEALING_FILENAME = "ACTIVITY_SUMMARY.md"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _latest_poll_mtime(run_dir: Path) -> Optional[float]:
    polls = list(run_dir.glob("*_nvidia_smi_poll_*s.json"))
    if not polls:
        return None
    return max(p.stat().st_mtime for p in polls)


def _launches_present(run_dir: Path) -> bool:
    return bool(list(run_dir.glob("*_launch_burn.json")) +
                list(run_dir.glob("*_launch_train.json")))


def can_adopt(orphan: Dict[str, Any],
              max_poll_age_s: int = 900) -> Tuple[bool, str]:
    """Decide whether an orphan run is safely adoptable.

    Args:
        orphan: dict shaped like the entries returned by
            `orphan_detector.find_orphaned_runs`
            (`{run_id, run_dir, reason, last_heartbeat_utc}`).
        max_poll_age_s: reject if the most recent poll receipt on disk
            is older than this many seconds (on-host job probably done).

    Returns:
        (True, "recent_poll_within_<n>s") if adoptable
        (False, reason) otherwise
    """
    run_dir_s = orphan.get("run_dir") or ""
    run_dir = Path(run_dir_s)
    if not run_dir.exists() or not run_dir.is_dir():
        return False, "run_dir_missing"
    if not _launches_present(run_dir):
        return False, "no_launch_record"
    # Real-seal check (W0 close 2026-09-13 · STANDING_ORDERS §6):
    # only a seal file that carries `Kind:` for a real-work kind counts
    # as sealed. A bare `ACTIVITY_SUMMARY.md` without `Kind:` is the
    # silent-success defect and is treated as NOT sealed.
    from services.output_verified_seal import is_real_seal
    if is_real_seal(run_dir):
        return False, "sealed"
    mtime = _latest_poll_mtime(run_dir)
    if mtime is None:
        return False, "no_polls"
    age = int(max(0, __import__("time").time() - mtime))
    if age > max_poll_age_s:
        return False, f"polls_stale_{age}s_gt_{max_poll_age_s}s"
    return True, f"recent_poll_within_{age}s"


def _recent_adoption(run_dir: Path,
                     dedupe_window_s: int) -> Optional[Dict[str, Any]]:
    files = sorted(run_dir.glob("adoption_*.json"),
                   key=lambda p: p.stat().st_mtime,
                   reverse=True)
    if not files:
        return None
    latest = files[0]
    age = __import__("time").time() - latest.stat().st_mtime
    if age > dedupe_window_s:
        return None
    try:
        return json.loads(latest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def mark_adopted(orphan: Dict[str, Any],
                 adopting_pid: int,
                 dedupe_window_s: int = 30) -> Optional[Dict[str, Any]]:
    """Bank an adoption ledger entry in the orphan's run_dir.

    Zero-influence: any write failure returns None; does NOT raise.
    Idempotent within `dedupe_window_s`: a fresh existing record short-
    circuits the write and returns the existing record dict.
    """
    try:
        run_dir = Path(orphan.get("run_dir") or "")
        if not run_dir.exists():
            return None
        # Dedupe
        recent = _recent_adoption(run_dir, dedupe_window_s)
        if recent is not None:
            return recent
        record: Dict[str, Any] = {
            "run_id": orphan.get("run_id"),
            "run_dir": str(run_dir),
            "adopted_at_utc": _iso_now(),
            "adopting_pid": int(adopting_pid),
            "prior_last_heartbeat_utc": orphan.get("last_heartbeat_utc"),
            "orphan_reason": orphan.get("reason"),
        }
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = run_dir / f"adoption_{stamp}_{adopting_pid}.json"
        out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8")
        return record
    except Exception as exc:
        log.warning("mark_adopted failed for run_id=%r: %r",
                    orphan.get("run_id"), exc)
        return None


def read_adoption_records(run_dir: Path) -> List[Dict[str, Any]]:
    """Return every adoption record in the run_dir, sorted by mtime asc."""
    p = Path(run_dir)
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    for f in sorted(p.glob("adoption_*.json"), key=lambda x: x.stat().st_mtime):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return out
