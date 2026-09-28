"""services/solva_v2/intent_audit.py — CP-S6.

Canon-4 §21.1: intent audit opens with declared situation class;
demonstrated observations are appended as the session unfolds.

Append-only in spirit (Canon-3 §9.3): update returns a NEW record; the
original is unchanged.  IntentAuditRecord is frozen at the pydantic
layer to make mutation explicit.
"""
from __future__ import annotations

from contracts.solva_reasoning import IntentAuditRecord


def open_intent_audit(*, session_id: str,
                       declared_situation_class: str) -> IntentAuditRecord:
    return IntentAuditRecord(
        session_id=session_id,
        declared_situation_class=declared_situation_class,
        demonstrated_observations=(),
    )


def update_intent_audit_demonstrated(
    record: IntentAuditRecord,
    demonstrated_observation: str,
) -> IntentAuditRecord:
    """Append-only: returns a new record; the input record stays
    unchanged (Canon-3 §9.3 spirit: no update path within the retention
    window)."""
    return IntentAuditRecord(
        session_id=record.session_id,
        declared_situation_class=record.declared_situation_class,
        demonstrated_observations=(
            *record.demonstrated_observations,
            demonstrated_observation,
        ),
    )
