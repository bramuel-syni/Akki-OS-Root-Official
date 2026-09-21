"""services.watch.capability_admission — W-M3-SW6 · Watch Learning L-5."""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field


CAPABILITY_REGISTER_R17_GRANULARITY_PENDING_OVERRIDE: Final[str] = "PENDING-OVERRIDE"


AC1_CEILINGS_NOT_ADMISSIBLE: Final[Tuple[str, ...]] = (
    "ac1.self_replication",
    "ac1.resource_acquisition",
    "ac1.credential_escalation",
    "ac1.oversight_tampering",
)


class AC1CeilingCannotAdmit(RuntimeError):
    """AC-18: AC-1 ceilings are not admissible under any ceremony."""


class LearnerCannotRatify(RuntimeError):
    """AC-18: a learner may propose but MUST NOT ratify a capability."""


class FirstExerciseFoundationFloor(RuntimeError):
    """AC-17: action citing no admitted class handled at reversible-
    only foundation floor; observation feeds research queue."""


class CapabilityClass(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    class_name: str = Field(min_length=1)
    admitted_conditions: Tuple[str, ...] = Field(min_length=1)
    proposer_role: str  # 'human' | 'learner'
    ratifier_role: str  # must be 'human' at ratification time


class CapabilityRegister(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    artefact_id: str = Field(min_length=1)
    classes: Tuple[CapabilityClass, ...] = ()


def propose_capability(
    *,
    proposer_id: str,
    proposer_role: str,
    class_name: str,
    admitted_conditions: Tuple[str, ...],
) -> CapabilityClass:
    if class_name in AC1_CEILINGS_NOT_ADMISSIBLE:
        raise AC1CeilingCannotAdmit(
            f"class_name {class_name!r} is an AC-1 ceiling; not "
            f"admissible under any ceremony (AC-18)"
        )
    return CapabilityClass(
        class_name=class_name,
        admitted_conditions=admitted_conditions,
        proposer_role=proposer_role,
        ratifier_role="pending",  # not yet ratified
    )


def ratify_capability(
    cls: CapabilityClass, *, ratifier_role: str
) -> dict:
    if ratifier_role != "human":
        raise LearnerCannotRatify(
            f"ratifier_role {ratifier_role!r} cannot ratify; only "
            f"'human' may ratify a capability class (AC-18)"
        )
    if cls.class_name in AC1_CEILINGS_NOT_ADMISSIBLE:
        raise AC1CeilingCannotAdmit(
            f"class_name {cls.class_name!r} is an AC-1 ceiling"
        )
    return {"ratified": True, "class_name": cls.class_name}


def cite_action_capability(
    *,
    register: CapabilityRegister,
    action_class: str,
) -> dict:
    for admitted in register.classes:
        if admitted.class_name == action_class:
            return {
                "exercised_admitted_class": True,
                "class_name": action_class,
                "artefact_id": register.artefact_id,
            }
    raise FirstExerciseFoundationFloor(
        f"action {action_class!r} cites no admitted class on artefact "
        f"{register.artefact_id!r}; falls to reversible-only "
        f"foundation floor (AC-17); observation record queues"
    )


__all__ = [
    "CAPABILITY_REGISTER_R17_GRANULARITY_PENDING_OVERRIDE",
    "AC1_CEILINGS_NOT_ADMISSIBLE",
    "AC1CeilingCannotAdmit",
    "LearnerCannotRatify",
    "FirstExerciseFoundationFloor",
    "CapabilityClass",
    "CapabilityRegister",
    "propose_capability",
    "ratify_capability",
    "cite_action_capability",
]
