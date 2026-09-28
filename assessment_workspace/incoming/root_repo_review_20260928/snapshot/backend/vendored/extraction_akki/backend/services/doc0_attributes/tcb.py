"""services.doc0_attributes.tcb — W-M2-SW7 · Doc-0 Attr-1.

TCB IN/OUT classification per `tcb_enumeration_v1` canon drop
2026-09-09 + Ratification_Record_v1 R-3 (Grey Mirror OUT, Mkono IN).
"""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field


TCB_VERSION: Final[str] = "tcb_enumeration_v1"


class TCBEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    component_id: str = Field(min_length=1)
    classification: str  # 'IN' or 'OUT'
    reason: str = Field(min_length=1)


# Seeded from tcb_enumeration_v1 + R-3 ratification.  Additive: any
# future ratification appends a new entry.
_TCB_ENTRIES: Tuple[TCBEntry, ...] = (
    TCBEntry(
        component_id="mkono",
        classification="IN",
        reason="R-3 RATIFIED 2026-09-09: Watch response half (Mkono) is TCB per BR-7.4 mechanical test.",
    ),
    TCBEntry(
        component_id="grey_mirror",
        classification="OUT",
        reason="R-3 RATIFIED 2026-09-09: Grey Mirror detection half is NOT TCB — learned pattern-matching per BR-7.4.",
    ),
    TCBEntry(
        component_id="ledger.writer",
        classification="IN",
        reason="Canon-3 §9.3 single-writer + BR-8.3.",
    ),
    TCBEntry(
        component_id="syn.chokepoint",
        classification="IN",
        reason="Canon-1 §4.1 fail-closed chokepoint (Doc-1 SyniSense A5.1).",
    ),
    TCBEntry(
        component_id="cif.acceptance_point",
        classification="IN",
        reason="BR-9.2 CIF single-experiment acceptance point (Doc-9).",
    ),
    TCBEntry(
        component_id="cif.detection",
        classification="OUT",
        reason="Learned per BR-9.4; detection may propose, only deterministic acceptance point acts.",
    ),
    TCBEntry(
        component_id="mem.retention_engine",
        classification="IN",
        reason=(
            "MEM-3 (Spec §4 Table 3): retention rule engine is a "
            "deterministic decision-maker · IN the TCB · owner "
            "MEMORY GO ruling + owner OPTION 1 ratification "
            "2026-09-19T~20:20Z verbatim · additive append per this "
            "module docstring line 24 amendment method."
        ),
    ),
    TCBEntry(
        component_id="mem.reload_verifier",
        classification="IN",
        reason=(
            "MEM-7 (Spec §4 Table 3): reload hash-verify is "
            "deterministic + fail-closed · IN the TCB · owner "
            "MEMORY GO ruling + owner OPTION 1 ratification "
            "2026-09-19T~20:20Z verbatim."
        ),
    ),
    TCBEntry(
        component_id="mem.drafting_component",
        classification="OUT",
        reason=(
            "MEM-2 (Spec §4 Table 3): drafting component is learned · "
            "MAY draft compacted text but MUST NOT decide retention "
            "(MEM-3 hard ban) · OUT of TCB · same wall-not-the-run "
            "split as Targeta and the Watch · owner MEMORY GO "
            "ruling + owner OPTION 1 ratification 2026-09-19T~20:20Z "
            "verbatim."
        ),
    ),
)


def get_tcb_current() -> Tuple[TCBEntry, ...]:
    """Return the current TCB classification set."""
    return _TCB_ENTRIES


def is_in_tcb(component_id: str) -> bool:
    """Return True iff the named component is classified IN.

    Unregistered components return False (fail-closed default).
    """
    for e in _TCB_ENTRIES:
        if e.component_id == component_id:
            return e.classification == "IN"
    return False


__all__ = ["TCB_VERSION", "TCBEntry", "get_tcb_current", "is_in_tcb"]
