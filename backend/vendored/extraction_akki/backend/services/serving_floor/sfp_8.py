"""services.serving_floor.sfp_8 — SFP-8 conformance gate · W-M2-SW6.

Canon anchor (verbatim, Serving_Integrity_Amendment_v1 §B V-2):
    SFP-8 defines a conforming serving path.  Only claims made on an
    SFP-8-conforming path are admissible.

A conforming path composes three named checkpoints:
  1. `artefact_hash` — content-hashed loaded artefact.
  2. `signed` — the loaded artefact bears a valid ratified signature.
  3. `audit_recorded` — the load event has been written to the Ledger
     (Canon-3 §9.3 single-writer).
  4. `fail_closed_on_failure` — failure of any downstream gate does
     NOT fall through to a permissive serving state.
"""
from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field, field_validator


SFP_8_VERSION: Final[str] = "v1"


class SFP8ConformanceError(RuntimeError):
    """Non-conforming path presented to the SFP-8 gate."""


class ServingPathContext(BaseModel):
    """Composed properties a serving path exposes to the gate."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    artefact_hash: str = Field(min_length=64, max_length=64)
    signed: bool
    audit_recorded: bool
    fail_closed_on_failure: bool

    @field_validator("artefact_hash")
    @classmethod
    def _hexlike(cls, v: str) -> str:
        # accept only hex-shape strings
        try:
            int(v, 16)
        except ValueError as exc:
            raise ValueError(f"artefact_hash must be hex; got {v!r}") from exc
        return v


def is_sfp_8_conforming(ctx: ServingPathContext) -> bool:
    """Return True iff every named checkpoint holds.

    Fail-closed: any missing property yields False.  This is a pure
    predicate — never raises.
    """
    return bool(
        ctx.signed
        and ctx.audit_recorded
        and ctx.fail_closed_on_failure
        and len(ctx.artefact_hash) == 64
    )


def sfp_8_gate(ctx: ServingPathContext) -> None:
    """Raise on non-conforming path; return None on conforming.

    DAP-31+ / DAP-32+ callers invoke this gate BEFORE emitting a probe
    or battery result.  Fail-closed by contract.
    """
    if not is_sfp_8_conforming(ctx):
        raise SFP8ConformanceError(
            f"serving path is not SFP-8-conforming "
            f"(signed={ctx.signed}, audit_recorded={ctx.audit_recorded}, "
            f"fail_closed_on_failure={ctx.fail_closed_on_failure}) — "
            f"claims from this path are not admissible per Amendment §B V-2"
        )


__all__ = [
    "SFP_8_VERSION",
    "SFP8ConformanceError",
    "ServingPathContext",
    "is_sfp_8_conforming",
    "sfp_8_gate",
]
