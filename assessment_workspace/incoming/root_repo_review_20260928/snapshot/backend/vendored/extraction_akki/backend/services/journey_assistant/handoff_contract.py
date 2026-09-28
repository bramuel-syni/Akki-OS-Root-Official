"""services.journey_assistant.handoff_contract — W-M4-SW5 · Promise #32.

Generalised registered-handoff-contract per crossing (Doc-0 §BR-6.1 · G-13).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


PROMISE_32_VERBATIM: str = (
    "Promise #32 · registered handoff contract per crossing "
    "(Doc-0): every crossing between components, planes, or gates "
    "records a handoff contract that names the checkpoint, the "
    "rights carry-forward basis, and the payload shape.  Fully "
    "discharged by M4 via the generalised handoff-contract "
    "mechanism (composed on M2 W-DOC0-ATTR3-TRIAD BA-3.3 op→"
    "checkpoint mapping)."
)

DOC0_BR6_1_STATUS_VERBATIM: str = (
    "Doc-0 BR-6.1 STATUS: Partial — Promise #32 is itself marked "
    "Partial in canon: 'one concrete instance … no generalised "
    "registered handoff contract per crossing.' See G-13."
)


class HandoffKind(str, Enum):
    FRONTIER = "frontier"
    IN_ESTATE = "in_estate"
    PLANE_TO_PLANE = "plane_to_plane"
    GATE_TO_GATE = "gate_to_gate"


class RightsCarryForwardMissing(RuntimeError):
    """Registered handoff contract missing the rights_carry_forward_basis."""


@dataclass(frozen=True)
class HandoffContract:
    kind: HandoffKind
    from_component: str
    to_component: str
    checkpoint_id: str
    at_utc: str
    payload_shape: str
    rights_carry_forward_basis: str


_ledger: List[HandoffContract] = []


def register_handoff(
    *,
    kind: HandoffKind,
    from_component: str,
    to_component: str,
    checkpoint_id: str,
    at_utc: str,
    payload_shape: str,
    rights_carry_forward_basis: str,
) -> HandoffContract:
    """Register a handoff contract for a crossing.

    Refuses on empty `rights_carry_forward_basis` — Promise #32
    generalisation binds rights carry-forward as a mandatory field of
    every recorded crossing.
    """
    if not rights_carry_forward_basis:
        raise RightsCarryForwardMissing(
            f"Promise #32: handoff at checkpoint {checkpoint_id!r} "
            f"requires a non-empty `rights_carry_forward_basis`"
        )
    c = HandoffContract(
        kind=kind,
        from_component=from_component,
        to_component=to_component,
        checkpoint_id=checkpoint_id,
        at_utc=at_utc,
        payload_shape=payload_shape,
        rights_carry_forward_basis=rights_carry_forward_basis,
    )
    _ledger.append(c)
    return c


def get_handoff_ledger() -> Tuple[HandoffContract, ...]:
    return tuple(_ledger)


def reset_handoff_ledger() -> None:
    """Test-only helper."""
    _ledger.clear()


__all__ = [
    "PROMISE_32_VERBATIM",
    "DOC0_BR6_1_STATUS_VERBATIM",
    "HandoffKind",
    "HandoffContract",
    "RightsCarryForwardMissing",
    "register_handoff",
    "get_handoff_ledger",
    "reset_handoff_ledger",
]
