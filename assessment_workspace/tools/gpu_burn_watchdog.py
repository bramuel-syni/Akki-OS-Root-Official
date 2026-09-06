#!/usr/bin/env python3
"""gpu_burn_watchdog — supervisor tool for orphaned burns.

Scope: W-Orchestrator-Resilience-r2. INFORMATIONAL ONLY in this wave.
Auto-execute (subprocess.Popen of the respawn command) is chartered as
r3 and is deliberately absent here — invariant
`test_watchdog_script_no_subprocess_execute_in_r2_scope` freezes that
scope.

Usage:
    python3 tools/gpu_burn_watchdog.py [--max-staleness-s N] [--max-poll-age-s M]

Behaviour:
    * Scans `${GPU_BURN_ROOT}` (or the primitive default) for orphaned
      in-flight runs whose pod-side orchestrator is dead (missing / stale
      heartbeat, or heartbeat's PID no longer live).
    * For each orphan, prints the r2 adoptability verdict.
    * For each ADOPTABLE orphan, prints a copy-paste-ready shell command
      the operator can run to respawn the orchestrator adopting that
      orphan (`AKKI_ADOPT_RUN_ID=<run_id> python3 tools/gpu_burn_orchestrator.py`).

Zero-influence: the watchdog script writes nothing, signals nothing,
launches nothing. It just observes and prints. If the resilience layer
is missing, it prints an error and exits 0 (no cascade).
"""
from __future__ import annotations

import argparse
import os
import shlex
import sys
from pathlib import Path

# Ensure the Extraction-Akki backend is on sys.path so we can import the
# r1/r2 primitives (mirrors gpu_burn_orchestrator.py's own path insert).
_REPO_BACKEND = Path("/app/assessment_workspace/repos/Extraction-Akki/backend")
if str(_REPO_BACKEND) not in sys.path:
    sys.path.insert(0, str(_REPO_BACKEND))


ORCHESTRATOR_ENTRY_POINT = "/app/assessment_workspace/tools/gpu_burn_orchestrator.py"


def _fmt_respawn_command(run_id: str, run_dir: str) -> str:
    """Build the copy-paste shell command an operator would run to
    respawn the orchestrator adopting `run_id`. Uses `AKKI_ADOPT_RUN_ID`
    (frozen by invariant `test_watchdog_script_prints_respawn_command_with_env_var`)."""
    return (
        f"AKKI_ADOPT_RUN_ID={shlex.quote(run_id)} "
        f"python3 {shlex.quote(ORCHESTRATOR_ENTRY_POINT)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan for orphaned burns and recommend adopt-respawn "
                    "commands. r2 informational-only.",
    )
    parser.add_argument("--max-staleness-s", type=int, default=600,
                        help="heartbeat staleness threshold (s)")
    parser.add_argument("--max-poll-age-s", type=int, default=900,
                        help="poll-receipt age threshold for adoptability (s)")
    args = parser.parse_args()

    try:
        from services.orchestrator_resilience import watchdog
    except Exception as exc:
        print(f"[watchdog] resilience layer unavailable: {exc!r}", flush=True)
        return 0

    orphans = watchdog.select_adoptable_orphans(
        max_staleness_s=args.max_staleness_s,
        max_poll_age_s=args.max_poll_age_s,
    )
    if not orphans:
        print("[watchdog] no orphaned in-flight runs detected. Nothing to do.",
              flush=True)
        return 0

    adoptable = [o for o in orphans if o.get("adoptable")]
    non_adoptable = [o for o in orphans if not o.get("adoptable")]

    print(f"[watchdog] found {len(orphans)} orphaned run(s): "
          f"{len(adoptable)} adoptable, {len(non_adoptable)} not adoptable.",
          flush=True)
    for o in orphans:
        flag = "ADOPTABLE" if o.get("adoptable") else "NOT_ADOPTABLE"
        print(
            f"[watchdog]   {flag}: run_id={o['run_id']} · "
            f"reason={o['reason']} · "
            f"last_heartbeat={o.get('last_heartbeat_utc')} · "
            f"{o.get('adoptable_reason','')}",
            flush=True,
        )

    if adoptable:
        print("", flush=True)
        print("[watchdog] Recommended respawn commands (r2 informational-only; "
              "operator runs these manually — r3 will auto-execute):", flush=True)
        for o in adoptable:
            cmd = _fmt_respawn_command(o["run_id"], o.get("run_dir", ""))
            print(f"[watchdog]   $ {cmd}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
