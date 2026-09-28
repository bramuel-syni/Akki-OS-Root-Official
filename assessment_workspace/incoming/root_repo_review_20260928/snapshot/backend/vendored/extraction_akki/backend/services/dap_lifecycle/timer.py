"""DAP Request Lifecycle · DAP-15 14-day timer.

Spec verbatim (extraction_request_approval_journey.md · L27):
    "A request that receives no decision within 14 calendar days of submission
    expires unexecuted — silence is never treated as approval (DAP-15). If the
    14th day falls on a day the data owner doesn't work, the deadline rolls
    forward to their next working day (never earlier). The deadline is computed
    and returned by the backend as window_ends_at; the front end never does the
    date arithmetic itself."

Owner correction verbatim (this-session): "DAP-15's 14-day expiry runs from
SUBMISSION to DECISION: the transition is In Approval → Expired when no
decision lands within 14 calendar days of submission. Ready → Expired is NOT
the DAP-15 rule."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Set

from services.dap_lifecycle.state_machine import RequestState


DAP_15_WINDOW_DAYS: int = 14


def compute_window_ends_at(
    *,
    submitted_at_utc: datetime,
    working_days: Optional[Set[int]] = None,
) -> datetime:
    """Compute window_ends_at = submitted_at_utc + 14 calendar days, rolled
    forward to the next working day if working_days is provided and the 14th
    day lands on a non-working weekday.

    working_days is a set of weekday ints per datetime.weekday() (Mon=0..Sun=6).
    None means no roll-forward.

    Roll-forward is monotonic upwards only (never earlier · journey L219
    verbatim: 'rolls forward (never earlier)').
    """
    base = submitted_at_utc + timedelta(days=DAP_15_WINDOW_DAYS)
    if working_days is None:
        return base

    candidate = base
    while candidate.weekday() not in working_days:
        candidate = candidate + timedelta(days=1)
    return candidate


def expire_if_window_elapsed(
    *,
    current_state: RequestState,
    decision_recorded: bool,
    window_ends_at: datetime,
    now_utc: datetime,
) -> RequestState:
    """DAP-15: In Approval + silence over the 14-day window → Expired.

    Silence is NEVER treated as approval (journey L27). If the caller invokes
    this for any state other than In Approval, or a decision was already
    recorded, the state is returned unchanged (fail-closed to no mutation).
    """
    if current_state is not RequestState.InApproval:
        return current_state
    if decision_recorded:
        return current_state
    if now_utc <= window_ends_at:
        return current_state
    return RequestState.Expired
