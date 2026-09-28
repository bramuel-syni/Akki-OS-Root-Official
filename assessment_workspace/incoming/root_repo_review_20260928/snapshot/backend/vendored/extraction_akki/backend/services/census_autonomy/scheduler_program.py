"""Supervisor-managed persistent worker for PHASE 3 CENSUS AUTONOMY SERVICE.

Owner R-106 §1 verbatim (banked in STATE/DECISIONS.md at 4k Commit-B
f775adf6):

> "A supervisor-managed persistent worker/scheduler process (e.g., a
> census_scheduler service registered in supervisord alongside backend)
> that survives agent absence, app restarts, and pod restarts — census
> runs happen with NO agent in the loop."

This module is the entry-point invoked by supervisord's
`command=/root/.venv/bin/python -m services.census_autonomy.scheduler_program`
(see `backend/scripts/census_scheduler.supervisord.conf`).

The loop:
- Reads scheduled census jobs per tenant from
  `services.census_autonomy.engine.get_pending_scheduled_runs()`.
- Reads on-demand jobs from the JWT-gated queue populated by the
  `POST /api/portal/census/run` endpoint (wired in Phase 3 continuation).
- Executes one job at a time, bounded by `MAX_JOB_WALL_CLOCK_SECONDS`.
- Between jobs, sleeps `SLEEP_BETWEEN_POLLS_SECONDS`.
- Never blocks waiting on an agent or human; mid-run decisions bank a
  `BLOCKED_AWAITING_RESPONSE` refusal row and CONTINUE on non-blocked
  lanes (R-106 §4 verbatim).
- Survives pod restarts via supervisord `autorestart=true` (see .conf).

Zero pytest / testing_agent imports here per SO §6 (testing_agent
STRICTLY BANNED) + R-106 §8(c) no-agent-dependency.
"""

from __future__ import annotations

import logging
import os
import signal
import sys
import time
from typing import Final

# NOTE: These imports are additive over sealed modules. All are read-only
# except `services.mtafiti.asset_registry_writer` which is the sealed
# single-writer (Canon-9 §3) used through the engine's `run_bounded_census`.
from services.census_autonomy.engine import (
    get_pending_scheduled_runs,
    run_bounded_census,
)

# Loop configuration (env-overridable, additive-only defaults).
SLEEP_BETWEEN_POLLS_SECONDS: Final[int] = int(
    os.environ.get("CENSUS_SCHEDULER_POLL_INTERVAL_SEC", "60")
)
MAX_JOB_WALL_CLOCK_SECONDS: Final[int] = int(
    os.environ.get("CENSUS_SCHEDULER_JOB_MAX_SEC", "3600")
)

# ---------------------------------------------------------------------------
# Signal-driven graceful shutdown (supervisord sends SIGTERM at stop).
# ---------------------------------------------------------------------------

_shutdown_requested: bool = False


def _install_signal_handlers() -> None:
    """Install SIGTERM/SIGINT handlers so supervisord restarts complete."""

    def _handler(signum: int, _frame: object) -> None:
        global _shutdown_requested
        _shutdown_requested = True
        logging.getLogger(__name__).info(
            "census_scheduler received signal %d — shutdown requested "
            "after current job completes", signum,
        )

    signal.signal(signal.SIGTERM, _handler)
    signal.signal(signal.SIGINT, _handler)


def _configure_logging() -> logging.Logger:
    """Stdout-only logging so supervisord captures via stdout_logfile."""
    logger = logging.getLogger("census_scheduler")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [census_scheduler] %(levelname)s %(message)s"
            )
        )
        logger.addHandler(handler)
    return logger


def main() -> int:
    """Persistent-worker entry-point invoked by supervisord.

    Loop discipline per R-106 §1 + §4 + §7:
    - Never blocks on an agent or human.
    - Bounds every job by wall-clock.
    - Emits state to stdout for supervisord log capture.
    - Returns 0 only on clean SIGTERM/SIGINT (autorestart handles crashes).

    On-demand jobs from `POST /api/portal/census/run` are picked up
    through the same `get_pending_scheduled_runs()` cursor once wired
    in Phase 3 continuation.
    """
    _install_signal_handlers()
    log = _configure_logging()

    log.info(
        "census_scheduler starting · poll_interval=%ds · job_max=%ds · "
        "shutdown_requested=%s",
        SLEEP_BETWEEN_POLLS_SECONDS,
        MAX_JOB_WALL_CLOCK_SECONDS,
        _shutdown_requested,
    )

    while not _shutdown_requested:
        try:
            pending = get_pending_scheduled_runs()
        except Exception as exc:  # noqa: BLE001  ops-degradation-honesty
            log.exception("get_pending_scheduled_runs failed: %s", exc)
            pending = ()

        if pending:
            job = pending[0]
            log.info(
                "picking up census job census_run_id=%s tenant=%s "
                "trigger=%s",
                job.get("census_run_id"),
                job.get("tenant_id"),
                job.get("trigger"),
            )
            job_deadline = time.time() + MAX_JOB_WALL_CLOCK_SECONDS
            try:
                run_bounded_census(job, job_deadline=job_deadline)
            except Exception as exc:  # noqa: BLE001  degradation-honesty
                # Refusal path stays honest: engine records the refusal
                # row; the loop must not stall.
                log.exception(
                    "run_bounded_census failed for census_run_id=%s: %s",
                    job.get("census_run_id"),
                    exc,
                )
        else:
            time.sleep(SLEEP_BETWEEN_POLLS_SECONDS)

    log.info("census_scheduler shutting down cleanly on signal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
