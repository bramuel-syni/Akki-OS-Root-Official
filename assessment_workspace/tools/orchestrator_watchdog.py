"""W-Orchestrator-Resilience-r1 · thin watchdog wrapper.

Wraps a pod-side orchestrator invocation in a respawn loop. If the
orchestrator process dies with a non-zero exit code (silent death,
OOM, unhandled exception, transient network blip in the seam), the
watchdog restarts it after a short back-off, up to MAX_RESPAWNS
attempts within RESPAWN_WINDOW_SECONDS. This is the "run under
supervisor" pattern the DECISIONS.md 2026-09-01T02:55Z reconcile
section called for — but as a userland respawner rather than a full
supervisor dependency, so it works in the pod without root.

Usage:
    python3 tools/orchestrator_watchdog.py \\
        -- \\
        env BURN_DURATION_SECONDS=7200 BURN_POLL_INTERVAL=300 \\
        python3 tools/gpu_burn_orchestrator.py

Exit codes:
    0  target exited cleanly on its own OR max respawns reached with
       last exit clean
    1  max respawns reached and the last attempt still failed
    2  watchdog itself received SIGTERM / SIGINT (owner asked stop)

The watchdog writes a heartbeat receipt per respawn under
`phase0/orchestrator_watchdog/<utc>_<pid>.jsonl` so an operator can
see when the target flapped."""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


MAX_RESPAWNS = int(os.environ.get("ORCH_WATCHDOG_MAX_RESPAWNS", "6"))
RESPAWN_WINDOW_SECONDS = int(os.environ.get("ORCH_WATCHDOG_WINDOW_S", "3600"))
INITIAL_BACKOFF_S = int(os.environ.get("ORCH_WATCHDOG_BACKOFF_S", "5"))
BACKOFF_CAP_S = int(os.environ.get("ORCH_WATCHDOG_BACKOFF_CAP_S", "60"))
LOG_ROOT = Path(os.environ.get(
    "ORCH_WATCHDOG_LOG_ROOT",
    "/app/assessment_workspace/phase0/orchestrator_watchdog",
))


def _iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_event(fp, obj):
    obj = dict(obj)
    obj.setdefault("at_utc", _iso())
    fp.write(json.dumps(obj, sort_keys=True) + "\n")
    fp.flush()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Respawning watchdog for pod-side orchestrators.")
    ap.add_argument("target", nargs=argparse.REMAINDER,
                    help="Target command (prefix with -- to separate args).")
    args = ap.parse_args()
    cmd = args.target
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("watchdog: no target command; usage: "
              "orchestrator_watchdog.py -- <command...>", file=sys.stderr)
        return 2

    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    log_path = LOG_ROOT / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{os.getpid()}.jsonl"
    stop_requested = {"v": False}

    def _stop(signum, _):
        stop_requested["v"] = True
        print(f"[watchdog] received signal {signum}, stopping cleanly",
              file=sys.stderr)
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    respawns = 0
    window_start = time.time()
    last_exit = None
    backoff = INITIAL_BACKOFF_S

    with log_path.open("w", encoding="utf-8") as fp:
        _write_event(fp, {"kind": "watchdog_start", "target_cmd": cmd,
                          "max_respawns": MAX_RESPAWNS,
                          "window_s": RESPAWN_WINDOW_SECONDS,
                          "watchdog_pid": os.getpid()})
        while respawns < MAX_RESPAWNS and not stop_requested["v"]:
            # Reset window counter if we've been running clean.
            if time.time() - window_start > RESPAWN_WINDOW_SECONDS:
                window_start = time.time()
                respawns = 0
                backoff = INITIAL_BACKOFF_S
            _write_event(fp, {"kind": "spawn", "attempt": respawns + 1})
            t0 = time.time()
            try:
                rc = subprocess.call(cmd)
            except FileNotFoundError as exc:
                _write_event(fp, {"kind": "spawn_error", "err": repr(exc)})
                return 1
            dt = time.time() - t0
            _write_event(fp, {"kind": "target_exit", "rc": rc,
                              "wall_s": round(dt, 2)})
            last_exit = rc
            if rc == 0 or stop_requested["v"]:
                _write_event(fp, {"kind": "watchdog_stop",
                                  "reason": "target_clean_exit"
                                             if rc == 0 else "signal_stop"})
                return 0 if rc == 0 else 2
            respawns += 1
            _write_event(fp, {"kind": "respawn_backoff", "s": backoff,
                              "respawns_used": respawns,
                              "respawns_budget": MAX_RESPAWNS})
            time.sleep(backoff)
            backoff = min(BACKOFF_CAP_S, backoff * 2)
        _write_event(fp, {"kind": "watchdog_stop",
                          "reason": "max_respawns_reached"
                                     if not stop_requested["v"]
                                     else "signal_stop",
                          "last_exit": last_exit})
    return 1 if not stop_requested["v"] else 2


if __name__ == "__main__":
    sys.exit(main())
