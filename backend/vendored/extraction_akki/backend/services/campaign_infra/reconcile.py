"""campaign_infra.reconcile — pod-side pull-and-bank of on-host journal.

When a pod session re-attaches to a host after any interval (10 min or
3 days), the reconciler enumerates the host's `AKKI_HOST_JOURNAL_ROOT`
runs and decides for each whether it is adoptable via restart-from-
checkpoint.

Adoptability verdict (extends r2 `adopt.can_adopt` to campaign scope):
    - still_running        — fresh on-host heartbeat + alive PID
    - restart_from_checkpoint — stale on-host heartbeat OR dead PID
                                 (recovery, not interference)
    - sealed              — ACTIVITY_SUMMARY.md present (run is DONE)
    - never_started       — no heartbeat AND no checkpoint marker

Zero-influence: this module NEVER modifies host files. It reads and
returns verdicts.
"""
from __future__ import annotations

import errno
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import on_host_logging as _hlog


log = logging.getLogger(__name__)


def _pid_is_alive(pid: int) -> bool:
    """POSIX signal-0 liveness check (mirrors watchdog.pid_is_alive)."""
    try:
        pid_int = int(pid)
    except (TypeError, ValueError):
        return False
    if pid_int <= 0:
        return False
    try:
        os.kill(pid_int, 0)
    except OSError as exc:
        if exc.errno == errno.EPERM:
            return True
        return False
    except Exception:
        return False
    return True


def _parse_iso(at_utc: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(at_utc.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _is_sealed(run_dir: Path) -> bool:
    """Real-seal check. Delegates to
    services.output_verified_seal.is_real_seal so the `Kind:` line is
    parsed and non-real kinds (stub/synthetic/unfinished/test_fixture)
    are refused. See STATE/STANDING_ORDERS.md §6 "ALIVE IS NOT DONE"
    (W0 close, 2026-09-13)."""
    from services.output_verified_seal import is_real_seal
    return is_real_seal(run_dir)


def list_host_runs() -> List[Dict[str, Any]]:
    """Enumerate all run dirs under the on-host journal root. Each entry
    carries `run_id` + `run_dir` (absolute path) + `heartbeat_present`
    (bool) + `sealed` (bool)."""
    root = _hlog.host_journal_root()
    if not root.exists():
        return []
    out: List[Dict[str, Any]] = []
    for entry in sorted(p for p in root.iterdir() if p.is_dir()):
        out.append({
            "run_id": entry.name,
            "run_dir": str(entry),
            "heartbeat_present": (entry / "heartbeat.json").exists(),
            "sealed": _is_sealed(entry),
        })
    return out


def adoptability_of_campaign_run(
    run_id: str,
    max_staleness_s: int = 600,
) -> Dict[str, Any]:
    """Return an adoptability verdict for the run with the given `run_id`.

    Verdict fields:
        run_id           — the run id
        adoptable        — bool (True iff restart_from_checkpoint applies)
        reason           — one of: still_running / restart_from_checkpoint
                                    / sealed / never_started
        heartbeat_utc    — the at_utc of the on-host heartbeat, or None
        training_pid     — the training pid recorded in the heartbeat,
                            or None
        pid_alive        — bool (checked only if heartbeat present)
    """
    run_dir = _hlog.host_journal_root() / run_id
    verdict: Dict[str, Any] = {
        "run_id": run_id,
        "adoptable": False,
        "reason": "",
        "heartbeat_utc": None,
        "training_pid": None,
        "pid_alive": False,
    }

    if _is_sealed(run_dir):
        verdict["reason"] = "sealed"
        return verdict

    hb_path = run_dir / "heartbeat.json"
    if not hb_path.exists():
        verdict["reason"] = "never_started"
        return verdict

    try:
        hb = json.loads(hb_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Corrupt heartbeat treated as never-started (safer default).
        verdict["reason"] = "never_started"
        return verdict

    verdict["heartbeat_utc"] = hb.get("at_utc")
    verdict["training_pid"] = hb.get("training_pid")

    pid_alive = _pid_is_alive(hb.get("training_pid"))
    verdict["pid_alive"] = pid_alive

    at = _parse_iso(hb.get("at_utc", ""))
    is_fresh = False
    if at is not None:
        age_s = (datetime.now(timezone.utc) - at).total_seconds()
        is_fresh = age_s <= max_staleness_s

    if is_fresh and pid_alive:
        verdict["reason"] = "still_running"
        verdict["adoptable"] = False
        return verdict

    # Either heartbeat stale OR pid dead (or both) — adoptable via
    # restart-from-checkpoint (recovery, not interference).
    verdict["reason"] = "restart_from_checkpoint"
    verdict["adoptable"] = True
    return verdict
