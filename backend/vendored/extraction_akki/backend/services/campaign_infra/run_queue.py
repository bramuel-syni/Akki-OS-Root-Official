"""campaign_infra.run_queue — sequential campaign runner.

`execute_campaign` iterates a manifest run-by-run, sealing each with
ACTIVITY_SUMMARY.md before starting the next. Refuses parallel campaign
runs on the same host via fcntl-lock on a per-host state file (env
`AKKI_CAMPAIGN_HOST_LOCK`, default `~/akki_journal/host.lock`).

Design decision: `trainer_fn` is a callable INJECTED by the caller
(not a fixed dependency). This lets the invariant harness pass a fake
trainer without touching real training code. In production, the caller
wires a real trainer that respects checkpoint markers + on-host logging.
"""
from __future__ import annotations

import fcntl
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from . import manifest as _m
from . import on_host_logging as _hlog


log = logging.getLogger(__name__)


class CampaignRunAlreadyActive(RuntimeError):
    """Another campaign is already running on this host (fcntl-lock)."""


class CampaignPriorRunNotSealed(RuntimeError):
    """The prior run did not seal itself — cannot advance to the next
    run without operator review."""


def _host_lock_path() -> Path:
    return Path(os.environ.get(
        "AKKI_CAMPAIGN_HOST_LOCK",
        str(_hlog.host_journal_root() / "host.lock"),
    ))


def _seal_run_dir(campaign_id: str, run_name: str) -> Path:
    return _hlog.host_journal_root() / f"{campaign_id}_{run_name}"


def _is_run_sealed(campaign_id: str, run_name: str) -> bool:
    """Real-seal check for a campaign run directory. Delegates to
    services.output_verified_seal.is_real_seal so the `Kind:` line is
    parsed and non-real kinds are refused. See STATE/STANDING_ORDERS.md
    §6 "ALIVE IS NOT DONE" (W0 close, 2026-09-13)."""
    from services.output_verified_seal import is_real_seal
    return is_real_seal(_seal_run_dir(campaign_id, run_name))


def next_pending_run(manifest: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the first run whose per-run dir is NOT sealed. None if
    every run is already sealed."""
    campaign_id = manifest["campaign_id"]
    for run in _m.iter_runs(manifest):
        if not _is_run_sealed(campaign_id, run["run_name"]):
            return run
    return None


def execute_campaign(
    manifest: Dict[str, Any],
    host: str,
    trainer_fn: Callable[..., Any],
    dry_run: bool = False,
) -> List[str]:
    """Execute the campaign sequentially on `host`.

    - Acquires an fcntl exclusive lock on `AKKI_CAMPAIGN_HOST_LOCK`.
      Raises CampaignRunAlreadyActive if another process holds it.
    - Skips runs whose per-run dir is already sealed (idempotent restart
      after a partial campaign).
    - Invokes `trainer_fn(run_name=..., manifest_entry=..., host=...)`
      for each unsealed run. Trainer is expected to write its own
      ACTIVITY_SUMMARY.md via on_host_logging.write_run_summary. If it
      completes without writing a summary, run_queue writes a synthetic
      "unfinished" summary and raises CampaignPriorRunNotSealed (owner
      review required before proceeding).
    - dry_run=True: skip trainer invocation entirely and return the
      planned order (useful for invariant harness verification).
    """
    _m.validate_manifest(manifest)
    campaign_id = manifest["campaign_id"]

    lock_path = _host_lock_path()
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if not lock_path.exists():
        lock_path.write_text("")
    lock_fh = open(lock_path, "r+")
    try:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CampaignRunAlreadyActive(
                f"host lock at {lock_path} held by another process"
            ) from exc

        planned: List[str] = []
        for run in _m.iter_runs(manifest):
            if _is_run_sealed(campaign_id, run["run_name"]):
                continue
            planned.append(run["run_name"])

        if dry_run:
            return planned

        for run_name in planned:
            run = next(r for r in _m.iter_runs(manifest)
                       if r["run_name"] == run_name)
            trainer_fn(run_name=run_name, manifest_entry=run, host=host)
            if not _is_run_sealed(campaign_id, run_name):
                # Trainer completed but did not seal. Write synthetic
                # unfinished marker and refuse to advance.
                _hlog.write_run_summary(
                    run_id=f"{campaign_id}_{run_name}",
                    campaign_id=campaign_id,
                    run_name=run_name,
                    final_step=-1,
                    final_loss=None,
                    started_at_utc="unknown",
                    completed_at_utc="unfinished",
                )
                raise CampaignPriorRunNotSealed(
                    f"run {run_name!r} did not seal · synthetic unfinished "
                    "marker written · operator review required before "
                    "advancing to the next run"
                )
        return planned
    finally:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)
        except Exception:
            pass
        lock_fh.close()
