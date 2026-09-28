"""services.doc0_attributes.reference_monitor — W-M2-SW10 · Doc-0 Attr-6."""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict


class InterfaceBypass(RuntimeError):
    """Access attempted through an interface that does not traverse a
    Reference Monitor."""


class ReferenceMonitor(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instance_id: str
    always_invoked: bool
    tamper_proof: bool
    verifiable_size: bool


_RMS: Final[Tuple[ReferenceMonitor, ...]] = (
    ReferenceMonitor(
        instance_id="watch",
        always_invoked=True,
        tamper_proof=True,
        verifiable_size=True,
    ),
    ReferenceMonitor(
        instance_id="governance",
        always_invoked=True,
        tamper_proof=True,
        verifiable_size=True,
    ),
)

_VALID_INTERFACES: Final[frozenset[str]] = frozenset({"watch", "governance"})


def list_reference_monitors() -> Tuple[ReferenceMonitor, ...]:
    return _RMS


def check_traverses_reference_monitor(*, interface: str, target: str) -> None:
    if interface not in _VALID_INTERFACES:
        raise InterfaceBypass(
            f"interface {interface!r} does not traverse a Reference "
            f"Monitor; access to {target!r} refused (Attr-6)"
        )


__all__ = [
    "ReferenceMonitor",
    "InterfaceBypass",
    "list_reference_monitors",
    "check_traverses_reference_monitor",
]
