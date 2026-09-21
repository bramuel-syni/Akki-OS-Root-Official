"""DAP Request Lifecycle · Waited-N-days derived-time surfaces.

Owner ruling verbatim (FORK-CON-INGEST-1 · RESOLVED · Q6 scoped narrower ·
2026-09-20T post-R-83 seal):

    "Q6's OMITTED covers exactly one thing — a wait figure shown AFTER a
    decision was made, measuring how long the owner took to decide (the
    Sign-off block's 'Waited N days' on the Approved branch, and the
    never-added Refused equivalent). That stays omitted. The two
    journey-doc lines are NOT Q6 — BUILD THEM, TC-INA-06 and TC-EXP-02
    stand:
        - In Approval drawer: 'It's been waiting [N] days' — elapsed
          time on an undecided request, derived from the submission
          date already in the header. Says nothing about the owner.
        - Expired drawer: 'Waited [N] days, the full review window' —
          a constant equal to the window; the status already says nobody
          decided in time.
    Owner's test for the invariant, verbatim: 'gated only if a decision
    exists and the figure measures the owner's speed in making it.'
    Register that as the Q6 boundary invariant."

Q6 boundary rule:
    A "waited N days" surface is Q6-OMITTED (must not exist) if and only if
    BOTH conditions hold:
      (1) a decision has been made on the request (Approved or Refused), AND
      (2) the surface's figure measures the owner's speed in making that
          decision.
    If either condition is false (no decision yet · or figure measures
    something other than owner decision speed) the surface is NOT Q6-gated
    and MAY exist.

TC-INA-06 (In Approval drawer):
    Copy verbatim (extraction_test_cases.xlsx · row TC-INA-06):
        "If no one at Digicow decides by [date], the request expires.
         It's been waiting N days."
    Journey doc verbatim (extraction_request_approval_journey_v2.md §5):
        "'In Approval' ('waiting 4 days')" · relative-time under the
        Approval drawer header.
    Q6 boundary: undecided request → (1) FALSE → NOT gated.
    Figure derivation: (now - submitted_at) in whole days.

TC-EXP-02 (Expired drawer):
    Copy verbatim (extraction_test_cases.xlsx · row TC-EXP-02):
        "Expired [date]. No decision was made." + "Waited 14 days,
        the full review window."
    Owner ruling verbatim (R-78 · 2026-09-20T~13:00Z · already sealed
    at CP-Q-UNLOCK-SUB-WAVE): "14-day expiry with working-day roll-
    forward. Ratified, DEFAULT-class."
    Q6 boundary: no decision was made → (1) FALSE → NOT gated · AND
    the figure is a CONSTANT (the review window length), not the
    owner's decision speed → (2) FALSE → still NOT gated even if (1)
    ever became TRUE (it can't for Expired but the double-guard is
    structural).

CP-Q-UNLOCK-SUB-WAVE seal chain (predecessor context preserved):
    Commit-A `c0f5e6d5` · Commit-B `6fc1a99b` · Commit-C `d5b0522f`.

Additive-only per SO §3.8 · this-desk consumes zero sealed writer · zero
sealed contract edit · pure functions with explicit-parameter surface.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Final


# --- TC-EXP-02 · Expired review-window constant ------------------------------

REVIEW_WINDOW_DAYS_DEFAULT: Final[int] = 14
"""Owner-ratified DEFAULT-class 14-day expiry window (R-78 · CP-Q-UNLOCK-
SUB-WAVE seal chain c0f5e6d5/6fc1a99b/d5b0522f). TC-EXP-02's "Waited N
days, the full review window" surface renders this value when no
roll-forward applies."""


def waited_days_in_approval(
    *,
    submitted_at_iso: str,
    now_iso: str,
) -> int:
    """TC-INA-06 · Return the elapsed whole-days count on an undecided
    In-Approval request.

    Signature discipline (Q6 boundary invariant enforcement):
      - Accepts ONLY submission-side + now-side parameters.
      - Accepts NO approver_id / decision / signoff-timing input.
      - The figure measures the request's own elapsed wait, NEVER the
        owner's speed in deciding.

    Args:
      submitted_at_iso: ISO-8601 datetime string, UTC, when the request
                       entered `In Approval`.
      now_iso:         ISO-8601 datetime string, UTC, the moment the
                       surface is rendered (caller-provided, never
                       time.time()-read here — this module stays pure).

    Returns:
      Non-negative whole-days count of elapsed wait. Truncates fractional
      days downward (a request submitted 25 hours ago has waited 1 day,
      not 2).

    Journey-doc contract verbatim: "It's been waiting N days" — the
    caller uses this integer verbatim in the drawer sentence
    "If no one at Digicow decides by [date], the request expires.
    It's been waiting N days."
    """
    submitted_at = _parse_iso_utc(submitted_at_iso)
    now = _parse_iso_utc(now_iso)
    delta = now - submitted_at
    days = delta.days
    return max(days, 0)


def expired_window_days(
    *,
    review_window_days: int = REVIEW_WINDOW_DAYS_DEFAULT,
) -> int:
    """TC-EXP-02 · Return the review-window constant surfaced on Expired.

    Signature discipline (Q6 boundary invariant enforcement):
      - Accepts ONLY the window constant.
      - Accepts NO approver_id / decision / signoff-timing input.
      - The figure IS the window constant, not a measurement of owner
        decision speed.

    Args:
      review_window_days: The review window length in whole days.
                         Defaults to the R-78 owner-ratified 14 days
                         (CP-Q-UNLOCK-SUB-WAVE seal chain c0f5e6d5/
                         6fc1a99b/d5b0522f). Callers with a working-day
                         roll-forward (TC-EXP-03) pass the actual rolled-
                         forward value in via this parameter; that too
                         is a request-side derivation, not an owner-speed
                         measurement.

    Returns:
      The window length itself. Used verbatim in the Expired drawer
      sentence "Waited N days, the full review window."
    """
    return int(review_window_days)


# --- Q6 boundary invariant helper --------------------------------------------


def is_q6_omitted_surface(
    *,
    has_decision: bool,
    figure_measures_owner_decision_speed: bool,
) -> bool:
    """Q6 boundary invariant helper · returns True iff a "waited N days"
    surface is Q6-OMITTED and MUST NOT exist.

    Owner verbatim: "gated only if a decision exists and the figure
    measures the owner's speed in making it."

    Both conditions must hold together (logical AND) for a surface to be
    Q6-gated / omitted:
      1. has_decision: True iff the request has reached Approved or
         Refused (a decision exists).
      2. figure_measures_owner_decision_speed: True iff the figure
         measures how long the owner took to decide (Sign-off block
         "Waited N days" · omitted).

    If either is False the surface is NOT Q6-gated and MAY exist:
      - TC-INA-06 (In Approval elapsed): has_decision=False → NOT gated.
      - TC-EXP-02 (Expired window constant): has_decision=False → NOT
        gated (AND the figure isn't owner-speed anyway).

    Callers use this helper at surface-authoring time to guard against
    ever authoring an owner-decision-speed figure on a decided request.
    """
    return bool(has_decision) and bool(figure_measures_owner_decision_speed)


# --- Internal helpers --------------------------------------------------------


def _parse_iso_utc(iso: str) -> datetime:
    """Parse an ISO-8601 UTC datetime string; refuse ambiguous input.

    Accepted forms:
      "2026-09-20T13:00:00Z"      (canonical)
      "2026-09-20T13:00:00+00:00" (offset)

    Naive timestamps (no tz suffix) are refused — fail-closed per FP-2.
    """
    # datetime.fromisoformat accepts "+00:00" but not the "Z" suffix on
    # older Python; normalize.
    normalized = iso.replace("Z", "+00:00") if iso.endswith("Z") else iso
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        raise ValueError(
            f"TC-INA-06 / TC-EXP-02 refuse naive datetime input {iso!r} · "
            "supply UTC ISO-8601 with 'Z' or '+00:00' suffix per FP-2"
        )
    return dt.astimezone(timezone.utc)


__all__ = (
    "REVIEW_WINDOW_DAYS_DEFAULT",
    "waited_days_in_approval",
    "expired_window_days",
    "is_q6_omitted_surface",
)
