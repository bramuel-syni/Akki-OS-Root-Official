"""Resume — read prior poll receipts to compute where a restarted
poller should pick up.

Receipt naming convention (established Wave-G5b · fixed on disk in
`phase0/gpu_burn/<RUN_ID>/`): `<host>_nvidia_smi_poll_<elapsed_s>s.json`
carries the on-host elapsed-seconds in the filename. That elapsed_s is
measured against the ON-HOST burn/train start time, not the pod-side
orchestrator start — so it survives orchestrator crashes cleanly.

Idempotency guarantee: `should_poll_at_elapsed(run_id, host, elapsed_s)`
returns False for any window whose poll file is already on disk. A
restarted poller can therefore safely re-run its poll loop from
elapsed_s=0 without double-counting; the guard cheaply skips covered
windows."""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)


_POLL_FILENAME_RE = re.compile(
    r"^(?P<host>[A-Za-z0-9\-_]+)_nvidia_smi_poll_(?P<elapsed>\d+)s\.json$"
)


def _root() -> Path:
    return Path(os.environ.get(
        "GPU_BURN_ROOT", "/app/assessment_workspace/phase0/gpu_burn"
    ))


def _run_dir(run_id: str) -> Path:
    return _root() / run_id


def _iter_poll_elapsed(run_dir: Path, host: str):
    """Yield the elapsed_s values (as ints) for every poll receipt on
    disk that matches the (run_dir, host) tuple."""
    for p in run_dir.iterdir():
        m = _POLL_FILENAME_RE.match(p.name)
        if not m:
            continue
        if m.group("host") != host:
            continue
        try:
            yield int(m.group("elapsed"))
        except ValueError:
            continue


def resume_from_receipts(run_id: str, host: str,
                         poll_interval_s: int) -> Optional[Dict[str, Any]]:
    """Compute the resume state for `run_id`/`host`.

    Returns:
      * None if the run dir does not exist (nothing to resume; caller
        decides — usually treat as "not this poller's run").
      * A dict with:
          `cycles_completed`: number of poll receipts already on disk
                              for this host
          `last_elapsed_s`:   highest elapsed_s recorded, or None
          `next_elapsed_s`:   the next expected poll's elapsed_s
                              (last_elapsed_s + poll_interval_s, or
                              poll_interval_s if fresh)

    The next_elapsed_s value is a HINT for scheduling; the poller
    still guards with `should_poll_at_elapsed` before writing anything
    (idempotency belt-and-braces)."""
    if poll_interval_s <= 0:
        raise ValueError(f"poll_interval_s must be > 0, got {poll_interval_s}")
    d = _run_dir(run_id)
    if not d.exists() or not d.is_dir():
        return None
    elapsed = sorted(_iter_poll_elapsed(d, host))
    if not elapsed:
        return {
            "cycles_completed": 0,
            "last_elapsed_s": None,
            "next_elapsed_s": int(poll_interval_s),
        }
    last = elapsed[-1]
    return {
        "cycles_completed": len(elapsed),
        "last_elapsed_s": int(last),
        "next_elapsed_s": int(last) + int(poll_interval_s),
    }


def should_poll_at_elapsed(run_id: str, host: str, elapsed_s: int) -> bool:
    """Return True iff a poll receipt for `elapsed_s` is NOT yet on
    disk. Idempotency guard for restarted pollers."""
    d = _run_dir(run_id)
    if not d.exists():
        return True
    target = d / f"{host}_nvidia_smi_poll_{int(elapsed_s)}s.json"
    return not target.exists()
