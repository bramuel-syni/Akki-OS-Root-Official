"""campaign_infra.checkpoint — checkpoint marker I/O.

A checkpoint MARKER is a small JSON file that names the latest checkpoint
step and its sha (the actual tensor blob is written by the training loop
in a separate wave). The on-host watchdog reads this marker to know
which step to resume from after a crash.

Zero-influence: writes swallow storage errors and return False. The
checkpoint marker is a recorder — its failure must never break the
training run.

Wave-honest-limits (v0):
    - Actual .pt tensor persistence is NOT in this wave (training-loop
      wave chartered separately).
    - The marker is REPLACED on each write (not appended). "Latest
      checkpoint step" means the step named in the current marker.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


log = logging.getLogger(__name__)

_MARKER_FILENAME = "checkpoint_marker.json"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_checkpoint_marker(
    run_dir: str,
    step: int,
    sha: str,
    campaign_id: str,
    run_name: str,
) -> bool:
    """Write (replace) the checkpoint marker for `run_dir`.

    Returns True on success, False on any storage failure. Never raises
    (zero-influence discipline)."""
    try:
        d = Path(run_dir)
        d.mkdir(parents=True, exist_ok=True)
        rec: Dict[str, Any] = {
            "step": int(step),
            "sha": str(sha),
            "campaign_id": str(campaign_id),
            "run_name": str(run_name),
            "written_at_utc": _iso_now(),
        }
        (d / _MARKER_FILENAME).write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return True
    except Exception as exc:
        log.warning("checkpoint marker write failed for %r: %r",
                    run_dir, exc)
        return False


def read_checkpoint_marker(run_dir: str) -> Optional[Dict[str, Any]]:
    """Return the current marker for `run_dir`, or None if missing."""
    p = Path(run_dir) / _MARKER_FILENAME
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def latest_checkpoint_step(run_dir: str) -> Optional[int]:
    """Return the step named in the current marker, or None if no marker.
    "Latest" means the step named in the most-recently-written marker
    (marker file is REPLACED per write, not appended)."""
    m = read_checkpoint_marker(run_dir)
    if m is None:
        return None
    try:
        return int(m.get("step"))
    except (TypeError, ValueError):
        return None
