"""Real-scheduler-state reader for PHASE 3 CENSUS AUTONOMY SERVICE.

Owner directive verbatim (PHASE 3 continuation A''):

> "the UI must show REAL scheduler state only — the running card polls
> the service's own state, never synthesized progress."

This module is the SOLE authoritative reader for census-run state. It
returns exactly what lives on the filesystem cursor at
`$CENSUS_AUTONOMY_STATE_DIR/{pending,results,refusal_rows}/` — no
synthesis, no interpolation, no fake progress bars, no random values.

Wire path (A' router → A'' UI):
  GET /api/portal/census/runs/{census_run_id}/state
    → read_census_run_state(census_run_id) → {'status': …, …}
    → UI running-card renders exactly what the service knows

If the census_run_id has never existed, returns None (caller emits
404). If pending, returns {'status': 'PENDING', 'enqueued_at_utc': …}.
If complete, returns {'status': 'COMPLETE', 'completed_at_utc': …,
'payload': …}. If refused, returns {'status': 'REFUSED',
'refusal_code': …, 'detail': …}. That is the entire vocabulary.
"""

from __future__ import annotations

import json
import pathlib
from typing import Final, Optional, Tuple

from services.census_autonomy.engine import (
    CENSUS_STATE_DIR,
    PENDING_JOBS_SUBDIR,
    REFUSAL_ROWS_SUBDIR,
    RESULTS_SUBDIR,
)

# Closed-vocab state codes (SO §3.10-α Final tuple[str, ...]). Any
# unknown state → None (caller emits 404). The 3 codes below map
# directly to the 3 filesystem-cursor subdirs.
CENSUS_RUN_STATE_CODES: Final[Tuple[str, ...]] = (
    "PENDING",
    "COMPLETE",
    "REFUSED",
)


def _find_by_glob(subdir: str, census_run_id: str) -> Optional[pathlib.Path]:
    """Return the first filesystem receipt matching `*census_run_id*`."""
    d = CENSUS_STATE_DIR / subdir
    if not d.exists():
        return None
    matches = sorted(d.glob(f"*{census_run_id}*.json"))
    return matches[0] if matches else None


def read_census_run_state(census_run_id: str) -> Optional[dict]:
    """Return the real state for `census_run_id` from disk, or None.

    Order of lookup (most-recent authoritative state wins):
    1. results/  → COMPLETE  (terminal)
    2. refusal_rows/ → REFUSED  (terminal)
    3. pending/  → PENDING  (in-progress)
    4. none of the above → None (unknown id)

    NEVER synthesizes progress percentages, ETA, or fabricated status.
    """
    # 1. Completed?
    result_path = _find_by_glob(RESULTS_SUBDIR, census_run_id)
    if result_path is not None:
        doc = json.loads(result_path.read_text())
        return {
            "status": "COMPLETE",
            "census_run_id": doc.get("census_run_id"),
            "tenant_id": doc.get("tenant_id"),
            "completed_at_utc": doc.get("completed_at_utc"),
            "payload": doc.get("payload"),
        }

    # 2. Refused?
    refusal_path = _find_by_glob(REFUSAL_ROWS_SUBDIR, census_run_id)
    if refusal_path is not None:
        doc = json.loads(refusal_path.read_text())
        return {
            "status": "REFUSED",
            "census_run_id": doc.get("census_run_id"),
            "tenant_id": doc.get("tenant_id"),
            "refusal_code": doc.get("refusal_code"),
            "detail": doc.get("detail"),
            "banked_at_utc": doc.get("banked_at_utc"),
        }

    # 3. Pending?
    pending_path = _find_by_glob(PENDING_JOBS_SUBDIR, census_run_id)
    if pending_path is not None:
        doc = json.loads(pending_path.read_text())
        return {
            "status": "PENDING",
            "census_run_id": doc.get("census_run_id"),
            "tenant_id": doc.get("tenant_id"),
            "trigger": doc.get("trigger"),
            "enqueued_at_utc": doc.get("enqueued_at_utc"),
        }

    # 4. Unknown census_run_id — never synthesize.
    return None
