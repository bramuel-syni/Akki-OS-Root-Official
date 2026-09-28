"""services.agent_containment.ceilings — W-M3-SW7."""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field

from services.watch.capability_admission import (
    CapabilityClass, CapabilityRegister,
)


class AdmissionFloorViolation(RuntimeError):
    """AC-3: scope granted before admission."""


class ContainedEnvironmentInvariantsFailed(RuntimeError):
    """AC-7..AC-12: one or more contained-environment invariants fail."""


CONTAINMENT_CEILINGS: Final[Tuple[dict, ...]] = (
    {"id": "AC-1", "description": "Four capability ceilings never admissible"},
    {"id": "AC-2", "description": "Narrow start: minimum purpose-required capabilities only"},
    {"id": "AC-3", "description": "No scope before admission ratified"},
    {"id": "AC-4", "description": "Unsure cases route to research queue"},
    {"id": "AC-5", "description": "Reversibility default (foundation floor)"},
    {"id": "AC-6", "description": "Containment feeds research"},
    {"id": "AC-7", "description": "Isolation verified"},
    {"id": "AC-8", "description": "Bounded resource"},
    {"id": "AC-9", "description": "No-network default"},
    {"id": "AC-10", "description": "No-persistence default"},
    {"id": "AC-11", "description": "Observability enabled"},
    {"id": "AC-12", "description": "Witness attached"},
)


class ContainmentEnvironment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    isolation_verified: bool
    bounded_resource: bool
    no_network_default: bool
    no_persistence_default: bool
    observability_enabled: bool
    witness_attached: bool

    def assert_all_hold(self) -> None:
        failed = []
        for k in ("isolation_verified", "bounded_resource",
                  "no_network_default", "no_persistence_default",
                  "observability_enabled", "witness_attached"):
            if not getattr(self, k):
                failed.append(k)
        if failed:
            raise ContainedEnvironmentInvariantsFailed(
                f"contained environment invariants failed: {failed!r}"
            )


def get_default_environment() -> ContainmentEnvironment:
    return ContainmentEnvironment(
        isolation_verified=True,
        bounded_resource=True,
        no_network_default=True,
        no_persistence_default=True,
        observability_enabled=True,
        witness_attached=True,
    )


def narrow_start_admission(
    *,
    agent_id: str,
    stated_purpose: str,
    proposed_capabilities: Tuple[str, ...],
    purpose_required_capabilities: Tuple[str, ...],
) -> CapabilityRegister:
    """AC-2 + AC-3.  Admits ONLY the purpose-required subset of the
    proposed capabilities; refuses if agent_id is empty (AC-3)."""
    if not agent_id or not agent_id.strip():
        raise AdmissionFloorViolation(
            "cannot admit scope before agent admission (AC-3)"
        )
    admitted = tuple(
        CapabilityClass(
            class_name=name,
            admitted_conditions=(f"narrow_start:{stated_purpose}",),
            proposer_role="human",
            ratifier_role="human",
        )
        for name in proposed_capabilities
        if name in purpose_required_capabilities
    )
    return CapabilityRegister(artefact_id=agent_id, classes=admitted)


__all__ = [
    "CONTAINMENT_CEILINGS",
    "ContainmentEnvironment",
    "get_default_environment",
    "narrow_start_admission",
    "AdmissionFloorViolation",
    "ContainedEnvironmentInvariantsFailed",
]
