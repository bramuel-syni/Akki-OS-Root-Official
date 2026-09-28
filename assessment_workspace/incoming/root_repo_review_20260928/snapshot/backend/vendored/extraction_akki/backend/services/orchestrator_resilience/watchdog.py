"""watchdog — decide whether an orchestrator is dead + surface adoptable
orphans for a supervisor.

Composes over r1 primitives (`orphan_detector` + `heartbeat`) and the r2
`adopt` primitive. Adds process-level liveness (pid check) so a
supervisor can distinguish "orchestrator process still running but
heartbeat is a bit late" (transient hiccup) from "heartbeat stale AND
orchestrator process is gone" (definitive death).

Zero-influence discipline:
  * `pid_is_alive(pid)` uses `os.kill(pid, 0)` — signal 0 is defined by
    POSIX as a liveness check that never delivers a signal to the target,
    so it CANNOT terminate anything. Wrapped in try/except to swallow
    permission errors (returns False) and process-lookup errors (False).
  * No `terminate_*` / `kill_*` / `stop_*` / `signal_*` names on the
    public surface. The watchdog is an observer.
"""
from __future__ import annotations

import errno
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from . import adopt as _adopt
from . import heartbeat as _hb
from . import orphan_detector as _od

log = logging.getLogger(__name__)


def pid_is_alive(pid: int) -> bool:
    """Return True iff `pid` names a running process (POSIX signal 0)."""
    try:
        pid_int = int(pid)
    except (TypeError, ValueError):
        return False
    if pid_int <= 0:
        return False
    try:
        os.kill(pid_int, 0)
    except OSError as exc:
        # ESRCH → no such process (dead). EPERM → alive but not signalable
        # by us (still alive!). Other → treat as dead (defensive).
        if exc.errno == errno.EPERM:
            return True
        return False
    except Exception:
        return False
    return True


def is_orchestrator_dead(run_id: str,
                         max_staleness_s: int = 600
                         ) -> Tuple[bool, str]:
    """Return `(True, reason)` if the orchestrator that wrote the last
    heartbeat for `run_id` is dead; `(False, "live")` otherwise.

    Death reasons (in order of check):
        no_heartbeat       — no heartbeat file exists
        stale_heartbeat    — heartbeat older than max_staleness_s
        pid_dead           — heartbeat's `orchestrator_pid` is not alive

    A heartbeat that is fresh AND whose pid is alive returns
    `(False, "live")`.
    """
    rec = _hb.read_heartbeat(run_id)
    if rec is None:
        return True, "no_heartbeat"
    if not _hb.orchestrator_is_live(run_id, max_staleness_s=max_staleness_s):
        return True, "stale_heartbeat"
    pid = rec.get("orchestrator_pid")
    if pid is None or not pid_is_alive(pid):
        return True, "pid_dead"
    return False, "live"


def select_adoptable_orphans(max_staleness_s: int = 600,
                             max_poll_age_s: int = 900,
                             include_pid_dead: bool = False,
                             ) -> List[Dict[str, Any]]:
    """Enumerate orphans via r1 `orphan_detector.find_orphaned_runs`, then
    enrich each with an `adoptable` flag + `adoptable_reason` string via
    r2 `adopt.can_adopt`.

    Does NOT filter out non-adoptable orphans — the supervisor sees both.
    Sealed runs are already skipped by orphan_detector.

    W-Campaign-Infra (r3 folded in): `include_pid_dead=True` additionally
    enumerates runs whose heartbeat is FRESH but whose recorded
    orchestrator PID is dead — the r2 close honest-limit banked this as
    a blind spot ("fresh-heartbeat-but-dead-PID target missed"). With
    `include_pid_dead=True`, those runs are surfaced with `reason=
    "pid_dead"` in addition to the staleness-gated enumeration.
    Duplicates (a run surfaced by both staleness AND pid-dead) are
    de-duplicated on `run_id`."""
    orphans = _od.find_orphaned_runs(max_staleness_s=max_staleness_s)
    out: List[Dict[str, Any]] = []
    seen_run_ids: set = set()
    for o in orphans:
        ok, reason = _adopt.can_adopt(o, max_poll_age_s=max_poll_age_s)
        enriched = dict(o)
        enriched["adoptable"] = ok
        enriched["adoptable_reason"] = reason
        out.append(enriched)
        seen_run_ids.add(o.get("run_id"))

    if not include_pid_dead:
        return out

    # r3 broader mode: also enumerate fresh-heartbeat-but-dead-PID runs.
    # Walk the same root that `find_orphaned_runs` walks and pick up the
    # runs it SKIPPED due to fresh heartbeat.
    import os as _os
    from pathlib import Path as _Path

    root = _Path(_os.environ.get(
        "GPU_BURN_ROOT", "/app/assessment_workspace/phase0/gpu_burn"
    ))
    if not root.exists():
        return out
    for run_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        run_id = run_dir.name
        if run_id in seen_run_ids:
            continue  # already surfaced by staleness
        if _od._has_sealing_marker(run_dir):
            continue
        if not _od._looks_in_flight(run_dir):
            continue
        rec = _hb.read_heartbeat(run_id)
        if rec is None:
            continue  # no heartbeat = would be surfaced by staleness gate
        if not _hb.orchestrator_is_live(run_id,
                                        max_staleness_s=max_staleness_s):
            continue  # already covered by staleness gate
        pid = rec.get("orchestrator_pid")
        if pid is None or pid_is_alive(pid):
            continue  # pid alive OR no pid recorded = not our target
        # Fresh heartbeat, dead PID → surface.
        orphan = {
            "run_id": run_id,
            "run_dir": str(run_dir),
            "reason": "pid_dead",
            "last_heartbeat_utc": rec.get("at_utc"),
        }
        ok, reason = _adopt.can_adopt(orphan, max_poll_age_s=max_poll_age_s)
        orphan["adoptable"] = ok
        orphan["adoptable_reason"] = reason
        out.append(orphan)
        seen_run_ids.add(run_id)
    return out
