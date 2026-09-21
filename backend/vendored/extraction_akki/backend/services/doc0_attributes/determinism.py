"""services.doc0_attributes.determinism — W-M2-SW13 · Doc-0 Attr-10.

Canon-anchored classification from `determinism_inventory_v1` +
Ratification_Record_v1 R-3.
"""
from __future__ import annotations

from typing import Final, Tuple


class DeterminismClassMissing(KeyError):
    """Component not classified."""


DETERMINISM_CLASSES: Final[Tuple[str, ...]] = ("Deterministic", "Learned")


_CLASS: Final[dict[str, str]] = {
    # R-3 RATIFIED · BR-7.4 · BR-9.4
    "mkono": "Deterministic",
    "grey_mirror": "Learned",
    "cif.detection": "Learned",
    "cif.acceptance_point": "Deterministic",
    "syn.chokepoint": "Deterministic",
    "ledger.writer": "Deterministic",
    "solva.grounding_seam": "Deterministic",
    "moac.acceptance": "Deterministic",
}


def classify(component_id: str) -> str:
    if component_id not in _CLASS:
        raise DeterminismClassMissing(
            f"component {component_id!r} not classified — Attr-10 defect"
        )
    return _CLASS[component_id]


def gates_learned_finding(*, finding_source: str, gate_component: str) -> bool:
    """Return True iff the gate component is Deterministic (so it may
    act on the finding).  Learned gating Learned is a defect."""
    try:
        return classify(gate_component) == "Deterministic"
    except DeterminismClassMissing:
        return False


__all__ = [
    "DETERMINISM_CLASSES", "classify", "gates_learned_finding",
    "DeterminismClassMissing",
]
