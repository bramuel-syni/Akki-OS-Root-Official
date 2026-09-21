"""services.doc0_attributes.audit_au3 — W-M2-SW12 · Doc-0 Attr-8."""
from __future__ import annotations

from typing import Final, Tuple, Mapping


AU3_ELEMENTS: Final[Tuple[str, ...]] = (
    "event_type", "when", "where", "source", "outcome", "principal",
)


class AU3Missing(ValueError):
    """Audit record is missing one or more of the six AU-3 elements."""


def audit_record_meets_au3(record: Mapping[str, object]) -> None:
    """Raise AU3Missing if any AU-3 element is absent or empty."""
    missing = []
    for k in AU3_ELEMENTS:
        v = record.get(k)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(k)
    if missing:
        raise AU3Missing(
            f"audit record missing AU-3 elements: {missing!r}"
        )


__all__ = ["AU3_ELEMENTS", "AU3Missing", "audit_record_meets_au3"]
