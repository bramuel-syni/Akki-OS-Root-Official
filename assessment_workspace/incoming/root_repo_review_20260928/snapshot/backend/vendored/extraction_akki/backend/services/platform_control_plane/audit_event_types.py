"""services.platform_control_plane.audit_event_types — CP-P6-CP2 · M9.

Preventive-charter refusal wrapper for audit-event-type superset
per Akki OS Pilot Platform Reference v0.2 §7.7 M-A-7 verbatim:

    Audit: append-only per tenant + one platform log. Retention =
    pilot + 12 months. Every event type in §7.7 must be emitted.

Row 207 anchor: Refusal when the emitted-event-types set is not a
superset of the §7.7 required set.

Design note: the concrete enumeration of §7.7 event types is not
in-scope for this CP's shape freeze — the required set is passed
by the caller (CONTRACT-MODELED: caller loads §7.7 verbatim canon
at run time). This CP shape-freezes the superset invariant and
returns the sorted-tuple of missing event-type refs when refused.

Refusals:
- required_event_types NOT ⊆ emitted_event_types →
  MissingRequiredEventTypesRefused

Standing-line proof:
- Pure function · no side effects · caller composes.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple


AUDIT_EVENT_TYPES_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §7.7 "
    "M-A-7 verbatim: Every event type in §7.7 must be emitted. Row "
    "207: Refusal when the emitted-event-types set is not a "
    "superset of the §7.7 required set."
)


# CONTRACT-MODELED: the concrete §7.7 event-type enumeration is
# loaded by the caller at run time · the CP shape-freezes the
# superset invariant only.
AUDIT_EVENT_TYPES_REQUIRED_SOURCE: str = "§7.7"


class AuditEventTypesRefused(Exception):
    """Root refusal for audit-event-types invariants."""


class MissingRequiredEventTypesRefused(AuditEventTypesRefused):
    """Refused: required_event_types is not a subset of
    emitted_event_types (§7.7 M-A-7 verbatim: every event type in
    §7.7 must be emitted)."""


def find_missing_event_types(
    *,
    emitted_event_types: Tuple[str, ...],
    required_event_types: Tuple[str, ...],
) -> Tuple[str, ...]:
    """Return sorted tuple of required event-type refs that are not
    emitted. Empty tuple when required ⊆ emitted."""
    emitted = frozenset(emitted_event_types)
    missing = [t for t in required_event_types if t not in emitted]
    return tuple(sorted(missing))


def assert_emitted_event_types_superset(
    *,
    emitted_event_types: Tuple[str, ...],
    required_event_types: Tuple[str, ...],
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refuses MissingRequiredEventTypesRefused when required is not
    a subset of emitted (case-sensitive).

    Returns None on admit."""
    missing = find_missing_event_types(
        emitted_event_types=emitted_event_types,
        required_event_types=required_event_types,
    )
    if missing:
        raise MissingRequiredEventTypesRefused(
            f"missing-required-event-types refused: "
            f"{len(missing)} required event-type ref(s) not emitted "
            f"· §7.7 M-A-7."
        )
    return None


__all__ = [
    "AUDIT_EVENT_TYPES_ANCHOR",
    "AUDIT_EVENT_TYPES_REQUIRED_SOURCE",
    "AuditEventTypesRefused",
    "MissingRequiredEventTypesRefused",
    "find_missing_event_types",
    "assert_emitted_event_types_superset",
]
