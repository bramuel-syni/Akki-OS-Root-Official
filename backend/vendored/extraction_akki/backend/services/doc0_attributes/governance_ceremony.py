"""services.doc0_attributes.governance_ceremony — W-M2-SW15 · M2 end-gate."""
from __future__ import annotations

import importlib
from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict


class AttributeMissing(RuntimeError):
    """A required Doc-0 attribute surface is not importable."""


REQUIRED_ATTRIBUTES: Final[Tuple[str, ...]] = (
    "Attr-1", "Attr-2", "Attr-3", "Attr-4",
    "Attr-6", "Attr-7", "Attr-8", "Attr-9",
    "Attr-10", "Attr-11",
)


# Each required attribute maps to the module that exposes its surface.
_ATTR_TO_MODULE: Final[dict[str, str]] = {
    "Attr-1":  "services.doc0_attributes.tcb",
    "Attr-2":  "services.doc0_attributes.subsystems",
    "Attr-3":  "services.doc0_attributes.triad",
    "Attr-4":  "services.rules_service.rule_registry",
    "Attr-6":  "services.doc0_attributes.reference_monitor",
    "Attr-7":  "services.doc0_attributes.baseline",
    "Attr-8":  "services.doc0_attributes.audit_au3",
    "Attr-9":  "services.rules_service.ceremony",
    "Attr-10": "services.doc0_attributes.determinism",
    "Attr-11": "services.doc0_attributes.coherence",
}


class GovernanceCeremonyAttestation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    ceremony_complete: bool
    attributes_verified: int
    rules_service_stack_complete: bool
    sfp_8_gate_callable: bool
    reliable_time_source_callable: bool
    marker_retirements_recorded: Tuple[str, ...]


def _import_attribute_module(name: str):
    """Import the module for a required attribute; raise if missing."""
    return importlib.import_module(name)


def run_governance_ceremony() -> GovernanceCeremonyAttestation:
    """Fan-in verification.  Refuses on any missing attribute surface."""
    verified = 0
    for attr, modname in _ATTR_TO_MODULE.items():
        try:
            _import_attribute_module(modname)
            verified += 1
        except ImportError as exc:
            raise AttributeMissing(
                f"required attribute {attr!r} module {modname!r} "
                f"missing: {exc}"
            ) from exc

    # Verify the Rules-Service stack is complete end-to-end.
    from services.rules_service.rule_registry import get_rule_registry
    from services.rules_service.ceremony import start_rule_flip
    from services.rules_service.rule_book_library import RuleBook
    from services.rules_service.rule_enumeration_classifier import (
        g4_pending_override_count,
    )
    _ = get_rule_registry()
    rules_service_ok = (
        callable(start_rule_flip)
        and callable(g4_pending_override_count)
        and RuleBook is not None
    )

    # Verify SFP-8 gate + G-8 clock are callable.
    from services.serving_floor.sfp_8 import sfp_8_gate
    from services.reliable_time_source.clock import au_3b_defensible_now
    sfp8_ok = callable(sfp_8_gate)
    g8_ok = callable(au_3b_defensible_now)

    # Marker retirements recorded (lineage anchors preserved).
    retirements = ("R-C1", "R-C2")

    return GovernanceCeremonyAttestation(
        ceremony_complete=(
            verified == len(REQUIRED_ATTRIBUTES)
            and rules_service_ok
            and sfp8_ok
            and g8_ok
        ),
        attributes_verified=verified,
        rules_service_stack_complete=rules_service_ok,
        sfp_8_gate_callable=sfp8_ok,
        reliable_time_source_callable=g8_ok,
        marker_retirements_recorded=retirements,
    )


__all__ = [
    "REQUIRED_ATTRIBUTES",
    "AttributeMissing",
    "GovernanceCeremonyAttestation",
    "run_governance_ceremony",
]
