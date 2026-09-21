"""Mtafiti Objective Carrier — frozen contract.

W-MTAFITI-GPU-DISCOVERY · CP1 kernel.

Owner ruling verbatim (STATE/DECISIONS.md 2026-09-09T~evening):
    "The registry building function goes beyond the reading file names.
    Its should be 'objective generation' blind but can carry multiple
    objectives which it facilitates but not create new objectives."

Canon binding:
  - C2-031 (Origination — constitutively load-bearing) extends by
    construction from CIF to mtafiti: mtafiti neither invents nor
    originates an objective. Origination remains the seat of the
    coach, ground reality, or a genuinely outside reviewer.
  - C4-014 / C4-015: objectives arrive at Targeta already FROZEN.
  - Mtafiti-Spec §1: mtafiti's registry serves EVERY objective — it
    carries multiple objectives supplied by Targeta / CIF and
    facilitates discovery under them.

This module is the sole entrypoint for admitting an objective carrier
into mtafiti. `admit_carrier(payload)` refuses any origin outside the
three canonical seats.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, List, Mapping

from pydantic import BaseModel, ConfigDict, Field


class ObjectiveOrigin(str, Enum):
    """The three canonical objective origins — C2-031 extended to mtafiti."""

    TARGETA = "targeta"
    CIF = "cif"
    COACH_ORIGINATION_PORT = "coach_origination_port"


class ObjectiveOriginationForbidden(Exception):
    """Raised when a payload tries to admit an objective with an origin
    outside the three canonical seats — including mtafiti-internal
    origins (banned by C2-031 extension) and unset / null origins.
    """


class MtafitiObjectiveCarrier(BaseModel):
    """Frozen carrier for an objective handed to mtafiti by Targeta / CIF.

    Multi-objective carry: `served_by` lists the mtafiti measures this
    carrier is asked to serve — Mtafiti-Spec §1 "one measure that serves
    every objective".
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    objective_id: str = Field(min_length=1)
    origin: ObjectiveOrigin
    frozen_at: datetime
    served_by: List[str] = Field(default_factory=list)


def admit_carrier(payload: Mapping[str, Any]) -> MtafitiObjectiveCarrier:
    """Admit a carrier from a raw payload, refusing any non-canonical origin.

    The whole point of routing through this function is that a call site
    which tries to fabricate an origin string ("mtafiti", "self", ...)
    hits `ObjectiveOriginationForbidden` at the door — Pydantic's
    enum-coercion would otherwise emit a generic ValidationError.
    """
    origin = payload.get("origin")
    allowed_values = {m.value for m in ObjectiveOrigin}
    if origin is None or origin not in allowed_values:
        raise ObjectiveOriginationForbidden(
            f"origin {origin!r} is not one of the three canonical seats "
            f"{sorted(allowed_values)!r} — C2-031 extension (mtafiti "
            f"cannot originate objectives)."
        )
    return MtafitiObjectiveCarrier(**dict(payload))
