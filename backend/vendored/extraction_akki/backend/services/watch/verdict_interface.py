"""services.watch.verdict_interface — W-M3-SW2.

Verdict interface + four-rung action ladder.  BR-7.4 gate: verdicts
sourced from Learned components (per Doc-0 Attr-10 · determinism
inventory) cannot act directly; a Deterministic gate must sit
between them and the action ladder.
"""
from __future__ import annotations

from typing import Final, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from services.doc0_attributes.determinism import (
    classify, DeterminismClassMissing,
)


# Doc-0 §7 · verbatim ordered four-rung ladder.
ACTION_LADDER_RUNGS: Final[Tuple[str, ...]] = (
    "annotate", "shape", "contain", "sever",
)


class InvalidRung(ValueError):
    """Emitted rung is not in the fixed four-rung vocabulary."""


class LearnedFindingCannotAct(RuntimeError):
    """BR-7.4 refusal: a Learned-source verdict cannot act directly."""


class Verdict(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    rung: str
    rationale: str = Field(min_length=1)
    source_component: str = Field(min_length=1)

    @field_validator("rung")
    @classmethod
    def _rung(cls, v: str) -> str:
        if v not in ACTION_LADDER_RUNGS:
            raise InvalidRung(
                f"rung must be one of {ACTION_LADDER_RUNGS}; got {v!r}"
            )
        return v


def emit_verdict(*, rung: str, rationale: str, source_component: str) -> Verdict:
    """Construct + validate a Verdict at emission time.  Invalid
    rung refuses via InvalidRung (fail-closed)."""
    if rung not in ACTION_LADDER_RUNGS:
        raise InvalidRung(
            f"rung must be one of {ACTION_LADDER_RUNGS}; got {rung!r}"
        )
    return Verdict(
        rung=rung, rationale=rationale, source_component=source_component,
    )


def consume_verdict(v: Verdict) -> dict:
    """Admit or refuse the verdict for action per BR-7.4.

    Learned-source verdicts are refused directly; Deterministic-source
    verdicts are admitted.  Unclassified source components are treated
    as Learned (fail-closed default).
    """
    try:
        cls = classify(v.source_component)
    except DeterminismClassMissing:
        # Fail-closed: unclassified sources default to Learned.
        cls = "Learned"

    if cls == "Learned":
        raise LearnedFindingCannotAct(
            f"verdict from Learned source {v.source_component!r} cannot "
            f"act directly on rung {v.rung!r} (BR-7.4); route through a "
            f"Deterministic gate first"
        )

    return {
        "admitted": True,
        "rung": v.rung,
        "source_component": v.source_component,
        "source_class": cls,
    }


__all__ = [
    "ACTION_LADDER_RUNGS",
    "InvalidRung",
    "LearnedFindingCannotAct",
    "Verdict",
    "emit_verdict",
    "consume_verdict",
]
