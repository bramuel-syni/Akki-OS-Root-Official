"""services.platform_control_plane.break_glass_session — CP-P2-CP5 · M9.

Break-glass session carrier + preventive-charter refusal wrapper per
Akki OS Pilot Platform Reference v0.2 §7.8 M-A-8 verbatim:

    Break-glass: stated reason · 2nd-operator approval · ≤4h · auto
    owner notification at open + close · flagged in both audit logs.

§10 verbatim: break_glass_session (id, tenant_id, operator_id,
approver_id, reason, opened_at, expires_at, closed_at).

Thin-kernel carrier + preventive-charter:
- `BreakGlassSession` frozen 8-carrier per §10.
- `assert_break_glass_valid(*, session, duration_hours,
  opened_notification_ref, close_notification_ref)` refuses on:
  1. reason empty.
  2. approver_id empty.
  3. approver_id == operator_id (self-approval refused).
  4. duration_hours > 4.
  5. opened_notification_ref empty.
  6. session.closed_at non-empty AND close_notification_ref empty.

CONTRACT-MODELED items enabled (from §8):
- Item 8 · Break-glass owner notification via email/webhook — the
  notification refs are ISO/audit-event refs; real webhook binding
  is downstream. This CP fixes the SHAPE that the two notification
  refs MUST be supplied at open and at close (audit-event id refs).

Duration computation: caller supplies `duration_hours` (they own the
datetime math between opened_at and expires_at). Constant
`BREAK_GLASS_MAX_DURATION_HOURS = 4` is the verbatim §7.8 ceiling.

Standing-line proof:
- No `bytes` field · all str · 8 exact-order fields.
- No enforcement hard-gate · caller invokes.
- Zero closed enums · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


BREAK_GLASS_SESSION_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.8 "
    "M-A-8 verbatim: Break-glass: stated reason · 2nd-operator "
    "approval · ≤4h · auto owner notification at open + close · "
    "flagged in both audit logs. §10 verbatim: break_glass_session "
    "(id, tenant_id, operator_id, approver_id, reason, opened_at, "
    "expires_at, closed_at)."
)


# §7.8 M-A-8 verbatim duration ceiling · hours as int.
BREAK_GLASS_MAX_DURATION_HOURS: int = 4


@dataclasses.dataclass(frozen=True)
class BreakGlassSession:
    """Frozen carrier for a control-plane break_glass_session per §10.

    Exact-order 8 str OPEN fields:
    - id · OPEN opaque assignment record id.
    - tenant_id · OPEN opaque · tenant the break-glass applies to.
    - operator_id · OPEN opaque · the operator invoking break-glass.
    - approver_id · OPEN opaque · the second operator authorising ·
      MUST be non-empty AND != operator_id.
    - reason · OPEN str · stated reason · MUST be non-empty.
    - opened_at · ISO-8601 UTC 'Z' str.
    - expires_at · ISO-8601 UTC 'Z' str.
    - closed_at · ISO-8601 UTC 'Z' str OR "" when not yet closed.
    """
    id: str
    tenant_id: str
    operator_id: str
    approver_id: str
    reason: str
    opened_at: str
    expires_at: str
    closed_at: str


BREAK_GLASS_SESSION_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "operator_id",
    "approver_id",
    "reason",
    "opened_at",
    "expires_at",
    "closed_at",
)


class BreakGlassSessionRefused(Exception):
    """Root refusal for break-glass invariants.

    Preventive-charter · caller-invoked only. COUNTS-only / positional
    -index-only refusal bodies (never id / tenant_id / operator_id /
    approver_id / reason values)."""


class MissingReasonRefused(BreakGlassSessionRefused):
    """Refused: reason empty (§7.8 stated reason)."""


class SecondApproverRefused(BreakGlassSessionRefused):
    """Refused: approver_id empty OR approver_id == operator_id
    (§7.8 2nd-operator approval · self-approval forbidden)."""


class ExceedsFourHoursRefused(BreakGlassSessionRefused):
    """Refused: duration_hours > BREAK_GLASS_MAX_DURATION_HOURS
    (§7.8 ≤4h ceiling)."""


class MissingOwnerNotificationRefused(BreakGlassSessionRefused):
    """Refused: opened_notification_ref empty OR (closed_at present
    AND close_notification_ref empty) (§7.8 auto owner notification
    at open + close)."""


def assert_break_glass_valid(
    *,
    session: BreakGlassSession,
    duration_hours: int,
    opened_notification_ref: str,
    close_notification_ref: str,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast on the more fundamental violation):
    1. reason empty → MissingReasonRefused.
    2. approver_id empty OR approver_id == operator_id →
       SecondApproverRefused.
    3. duration_hours > BREAK_GLASS_MAX_DURATION_HOURS →
       ExceedsFourHoursRefused.
    4. opened_notification_ref empty → MissingOwnerNotificationRefused
       (open).
    5. session.closed_at non-empty AND close_notification_ref empty →
       MissingOwnerNotificationRefused (close).

    Returns None on admit."""
    if session.reason == "":
        raise MissingReasonRefused(
            f"missing-reason refused: reason empty at positional "
            f"index {BREAK_GLASS_SESSION_FIELDS.index('reason')}."
        )
    if session.approver_id == "" or session.approver_id == session.operator_id:
        raise SecondApproverRefused(
            f"second-approver refused: approver_id at positional "
            f"index {BREAK_GLASS_SESSION_FIELDS.index('approver_id')} "
            f"empty or equals operator_id at index "
            f"{BREAK_GLASS_SESSION_FIELDS.index('operator_id')} · "
            f"§7.8 2nd-operator approval."
        )
    if duration_hours > BREAK_GLASS_MAX_DURATION_HOURS:
        raise ExceedsFourHoursRefused(
            f"exceeds-four-hours refused: duration_hours > "
            f"{BREAK_GLASS_MAX_DURATION_HOURS} · §7.8 ≤4h ceiling."
        )
    if opened_notification_ref == "":
        raise MissingOwnerNotificationRefused(
            f"missing-owner-notification refused: "
            f"opened_notification_ref empty · §7.8 auto owner "
            f"notification at open."
        )
    if session.closed_at != "" and close_notification_ref == "":
        raise MissingOwnerNotificationRefused(
            f"missing-owner-notification refused: "
            f"close_notification_ref empty while closed_at at "
            f"positional index "
            f"{BREAK_GLASS_SESSION_FIELDS.index('closed_at')} is "
            f"non-empty · §7.8 auto owner notification at close."
        )
    return None


__all__ = [
    "BREAK_GLASS_SESSION_ANCHOR",
    "BREAK_GLASS_MAX_DURATION_HOURS",
    "BREAK_GLASS_SESSION_FIELDS",
    "BreakGlassSession",
    "BreakGlassSessionRefused",
    "MissingReasonRefused",
    "SecondApproverRefused",
    "ExceedsFourHoursRefused",
    "MissingOwnerNotificationRefused",
    "assert_break_glass_valid",
]
