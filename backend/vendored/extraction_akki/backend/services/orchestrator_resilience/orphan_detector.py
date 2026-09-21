"""Orphan detector — reconcile-on-start for pod-side orchestrators.

An on-host job (burn / train) survives a pod-side orchestrator death
because it is launched with `setsid nohup` (detached process group).
When the orchestrator restarts (or is replaced by a watchdog respawn),
it MUST reconcile against on-disk run state: find any in-flight run
whose orchestrator appears dead (stale or missing heartbeat) and
surface it for pick-up.

Sealing convention: a run whose directory carries `ACTIVITY_SUMMARY.md`
is COMPLETED (already reconciled). It MUST NOT be flagged as an orphan.
Any other run with at least a launch record and one poll receipt is
in-flight from the filesystem's point of view."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from . import heartbeat as _hb

log = logging.getLogger(__name__)


SEALING_FILENAME = "ACTIVITY_SUMMARY.md"


def _has_sealing_marker(run_dir: Path) -> bool:
    """Real-seal check for orphan-detection. Delegates to
    services.output_verified_seal.is_real_seal so the `Kind:` line is
    parsed and non-real kinds are refused. See STATE/STANDING_ORDERS.md
    §6 "ALIVE IS NOT DONE" (W0 close, 2026-09-13).

    Historical note: the r3 case-insensitive filename normalization is
    preserved inside is_real_seal (see _find_seal_file). Writers still
    use the canonical SEALING_FILENAME.
    """
    from services.output_verified_seal import is_real_seal
    return is_real_seal(run_dir)


def _root() -> Path:
    return Path(os.environ.get(
        "GPU_BURN_ROOT", "/app/assessment_workspace/phase0/gpu_burn"
    ))


def _looks_in_flight(run_dir: Path) -> bool:
    """A run dir looks in-flight if it has at least one launch record
    (`*_launch_burn.json` OR `*_launch_train.json`) AND at least one
    poll receipt (`*_nvidia_smi_poll_*s.json`)."""
    launches = list(run_dir.glob("*_launch_burn.json")) + \
               list(run_dir.glob("*_launch_train.json"))
    if not launches:
        return False
    polls = list(run_dir.glob("*_nvidia_smi_poll_*s.json"))
    return len(polls) >= 1


def find_orphaned_runs(max_staleness_s: int = 600) -> List[Dict[str, Any]]:
    """Scan the gpu_burn root for orphaned runs.

    Returns a list of orphan records, each:
        {
          "run_id": str,
          "run_dir": str,           # absolute path
          "reason": "stale_heartbeat" | "no_heartbeat",
          "last_heartbeat_utc": str | None,
        }

    An empty list means every in-flight run has a live orchestrator (or
    there are no in-flight runs)."""
    root = _root()
    if not root.exists():
        return []
    out: List[Dict[str, Any]] = []
    for run_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        run_id = run_dir.name
        # Sealed → skip (case-insensitive check per W-Campaign-Infra r3).
        if _has_sealing_marker(run_dir):
            continue
        # Not-yet-in-flight (empty dir or launch-only, no polls) → skip
        # entirely for now; we only surface work that already has poll
        # receipts to pick up from.
        if not _looks_in_flight(run_dir):
            continue
        rec = _hb.read_heartbeat(run_id)
        if rec is None:
            out.append({
                "run_id": run_id,
                "run_dir": str(run_dir),
                "reason": "no_heartbeat",
                "last_heartbeat_utc": None,
            })
            continue
        if not _hb.orchestrator_is_live(run_id, max_staleness_s=max_staleness_s):
            out.append({
                "run_id": run_id,
                "run_dir": str(run_dir),
                "reason": "stale_heartbeat",
                "last_heartbeat_utc": rec.get("at_utc"),
            })
    return out
