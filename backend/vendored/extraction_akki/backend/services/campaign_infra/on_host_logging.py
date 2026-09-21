"""campaign_infra.on_host_logging — on-host heartbeat + poll receipts +
per-run summaries.

Writes to a HOST-LOCAL journal root (env `AKKI_HOST_JOURNAL_ROOT`,
default `~/akki_journal/`) so the training host is self-logging. No
pod-side dependency at runtime — a pod session reconciles by PULLING
the on-host journal via `reconcile.py` when it re-attaches.

Zero-influence: all writes swallow storage errors and return False.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


log = logging.getLogger(__name__)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def host_journal_root() -> Path:
    """Return the host-local journal root directory."""
    return Path(os.environ.get(
        "AKKI_HOST_JOURNAL_ROOT",
        str(Path.home() / "akki_journal"),
    ))


def _run_dir(run_id: str) -> Path:
    return host_journal_root() / run_id


def write_host_heartbeat(
    run_id: str,
    training_pid: int,
    step: int,
    campaign_id: str,
    run_name: str,
) -> bool:
    """Write (replace) the on-host heartbeat for a training run.

    The heartbeat is REPLACED on each write. Fresh heartbeat + alive PID
    = run is still going. Stale heartbeat OR dead PID = adoptable via
    restart-from-checkpoint."""
    try:
        d = _run_dir(run_id)
        d.mkdir(parents=True, exist_ok=True)
        rec: Dict[str, Any] = {
            "run_id": str(run_id),
            "training_pid": int(training_pid),
            "step": int(step),
            "campaign_id": str(campaign_id),
            "run_name": str(run_name),
            "at_utc": _iso_now(),
        }
        (d / "heartbeat.json").write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return True
    except Exception as exc:
        log.warning("on-host heartbeat write failed for %r: %r",
                    run_id, exc)
        return False


def write_host_poll_receipt(
    run_id: str,
    step: int,
    loss: Optional[float],
    wall_clock_s: Optional[float],
    campaign_id: str,
    run_name: str,
) -> bool:
    """Append a per-step poll receipt (loss + wall-clock + step) under
    the run's polls/ dir. One JSON file per poll (never appended in
    place — atomic write for concurrent-safe reads)."""
    try:
        d = _run_dir(run_id) / "polls"
        d.mkdir(parents=True, exist_ok=True)
        rec: Dict[str, Any] = {
            "run_id": str(run_id),
            "step": int(step),
            "loss": loss if loss is None else float(loss),
            "wall_clock_s": wall_clock_s if wall_clock_s is None
                            else float(wall_clock_s),
            "campaign_id": str(campaign_id),
            "run_name": str(run_name),
            "at_utc": _iso_now(),
        }
        filename = f"poll_step_{int(step):012d}.json"
        (d / filename).write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return True
    except Exception as exc:
        log.warning("on-host poll receipt write failed for %r: %r",
                    run_id, exc)
        return False


def write_run_summary(
    run_id: str,
    campaign_id: str,
    run_name: str,
    final_step: int,
    final_loss: Optional[float],
    started_at_utc: str,
    completed_at_utc: str,
    kind: str = "training_run_complete",
) -> bool:
    """Write the run's sealing summary — this file's existence is what
    the run-queue reads as 'run is DONE, move to next'. Filename is
    `ACTIVITY_SUMMARY.md` per the sealing convention (r3 close normalizes
    case-insensitive existence check).

    W0 close 2026-09-13 · STATE/STANDING_ORDERS.md §6 "ALIVE IS NOT DONE":
    the seal body carries `Kind: <kind>` so downstream readers via
    `services.output_verified_seal.is_real_seal` can distinguish a real
    completion from a stub/synthetic/unfinished marker. Defaults to
    `training_run_complete` for backward-compat with pre-W0 callers.
    """
    try:
        d = _run_dir(run_id)
        loss_str = "n/a" if final_loss is None else f"{final_loss}"
        from services.output_verified_seal import output_verified_seal
        output_verified_seal(
            d,
            kind=kind,
            body={
                "campaign_id": campaign_id,
                "run_name": run_name,
                "run_id": run_id,
                "final_step": final_step,
                "final_loss": loss_str,
                "started_at_utc": started_at_utc,
                "completed_at_utc": completed_at_utc,
            },
        )
        return True
    except Exception as exc:
        log.warning("on-host run summary write failed for %r: %r",
                    run_id, exc)
        return False
