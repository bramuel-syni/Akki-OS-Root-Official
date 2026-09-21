"""services.platform_control_plane.audit_event — CP-P6-CP1 · M9.

Frozen audit-event carrier + preventive-charter append-only refusal
wrapper per Akki OS Pilot Platform Reference v0.2:

- §10 verbatim: audit_event (id, tenant_id, actor_id, actor_type,
  action, resource_type, resource_id, at, break_glass_session_id).
- §7.7 M-A-7 verbatim: Audit: append-only per tenant + one platform
  log. Retention = pilot + 12 months. Every event type in §7.7 must
  be emitted.

Row 206 anchor: Frozen carrier + append-only refusal on
mutate/delete.

Refusals (fail-fast order):
1. is_delete_request True → AuditEventDeletionRefused
2. event_before != event_after → AuditEventMutationRefused

Standing-line proof:
- 9 str · 9 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


AUDIT_EVENT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: audit_event (id, tenant_id, actor_id, actor_type, "
    "action, resource_type, resource_id, at, break_glass_session_id). "
    "§7.7 M-A-7 verbatim: Audit: append-only per tenant + one "
    "platform log. Retention = pilot + 12 months. Every event type "
    "in §7.7 must be emitted. Row 206: append-only refusal on "
    "mutate/delete."
)


@dataclasses.dataclass(frozen=True)
class AuditEvent:
    """Frozen carrier for the control-plane audit_event record.

    Exact-order 9 str OPEN fields:
    - id · event record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - actor_id · actor identity ref.
    - actor_type · actor kind (OPEN str · e.g., user, service).
    - action · action ref (OPEN str · e.g., login, connector.disable).
    - resource_type · resource kind (OPEN str).
    - resource_id · resource identity ref.
    - at · ISO-8601 UTC 'Z' str.
    - break_glass_session_id · break-glass session ref (empty when
      not applicable) · composes with CP-P2-CP5 BreakGlassSession.
    """
    id: str
    tenant_id: str
    actor_id: str
    actor_type: str
    action: str
    resource_type: str
    resource_id: str
    at: str
    break_glass_session_id: str


AUDIT_EVENT_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "actor_id",
    "actor_type",
    "action",
    "resource_type",
    "resource_id",
    "at",
    "break_glass_session_id",
)


class AuditEventRefused(Exception):
    """Root refusal for audit-event append-only invariants."""


class AuditEventMutationRefused(AuditEventRefused):
    """Refused: proposed audit_event differs from prior state
    (§7.7 M-A-7 verbatim: append-only)."""


class AuditEventDeletionRefused(AuditEventRefused):
    """Refused: deletion of an audit_event requested (§7.7 M-A-7
    verbatim: append-only · Row 206 mutate/delete refusal)."""


def assert_append_only(
    *,
    event_before: AuditEvent,
    event_after: AuditEvent,
    is_delete_request: bool,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. is_delete_request True → AuditEventDeletionRefused (§7.7).
    2. event_before != event_after → AuditEventMutationRefused (§7.7).

    Returns None on admit (event_before == event_after AND not
    delete-request)."""
    if is_delete_request:
        raise AuditEventDeletionRefused(
            f"audit-event-deletion refused: deletion of audit_event "
            f"forbidden · §7.7 M-A-7 append-only."
        )
    if event_before != event_after:
        raise AuditEventMutationRefused(
            f"audit-event-mutation refused: proposed event differs "
            f"from prior state · §7.7 M-A-7 append-only."
        )
    return None


__all__ = [
    "AUDIT_EVENT_ANCHOR",
    "AUDIT_EVENT_FIELDS",
    "AuditEvent",
    "AuditEventRefused",
    "AuditEventMutationRefused",
    "AuditEventDeletionRefused",
    "assert_append_only",
]
