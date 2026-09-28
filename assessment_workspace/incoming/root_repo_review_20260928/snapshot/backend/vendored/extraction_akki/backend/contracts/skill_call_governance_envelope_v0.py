"""Doc 18 A18.3 · Per-Call Governance Envelope V0 · frozen contract shape.

Doc 18 §A18.3 verbatim (Wave B grounding brief · Canon-of-Record):
    'A18.3  [CANON] Governance rides every response, not just the first
     one. Every response carries its class inline through the inner
     gate's per-call governance — the platform's existing live-response
     contract, applied here to a standing service instead of a single
     crossing. Nothing about the mechanism is new; what changes is that
     it now runs once per query for the life of the skill, rather than
     once per delivery.'

Doc 18 §18.6 (Canon "What must be true" paired anchor):
    'No response leaves the inner gate without its governance class
     carried inline.'

This module lands the CONTRACT SHAPE for that inline governance class.
Runtime wiring into the inner-gate per-call carrier is deferred to a
later slice per SO §6.4 NOTHING-BEYOND. At this slice the envelope is
a structural drift-detector pin: any future runtime that carries a
per-call governance record MUST conform to this shape or the parity
snapshot fires right-reason RED.

DISTINCT FROM sealed A18.1 SkillProvisioningRecordV0:
  * A18.1 = per-skill anchor (long-lived, write-once, one per skill).
  * A18.3 = per-call carrier (short-lived, high-cardinality, one per
    response). The envelope references `skill_id` from the provisioning
    record but is otherwise a distinct contract (Banked Lesson #8
    both-direction non-collision).

Wire exposure (structural pin only at this slice):
  * The per-call governance envelope is what the sealed inner-gate
    would populate on every response; the pin here freezes its shape
    so any future runtime cannot silently drift from the frozen tuple.

The A18.3 canon has NO free-form or extensible fields — extra
properties are forbidden (`extra="forbid"`) per the frozen-tuple
discipline established at A18.1.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SkillCallGovernanceEnvelopeV0(BaseModel):
    """A18.3 frozen contract · per-call governance carrier.

    Seven fields, all required (no optional fields at this slice —
    every response carries its class inline, per canon). Field order
    matches the natural per-call flow: identify (call_id, skill_id),
    authorise (grant_id, policy_ref), decide (decision_ts,
    governance_class, floor_applied).

    Additional properties are forbidden — the shape is a frozen tuple,
    not an extensible envelope.
    """

    model_config = ConfigDict(extra="forbid")

    call_id: str = Field(
        ...,
        min_length=1,
        description="Stable identifier for this per-call governance "
                    "decision · high-cardinality one-per-response.",
    )
    skill_id: str = Field(
        ...,
        min_length=1,
        description="Reference to the A18.1 provisioning record this "
                    "call is served under · low-cardinality one-per-skill.",
    )
    grant_id: str = Field(
        ...,
        min_length=1,
        description="Engineer key-grant record identifier the call "
                    "authenticated under · A18.5 verbatim: 'Access "
                    "rides the engineer key-grant records.'",
    )
    policy_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the policy the per-call governance "
                    "decision was resolved against · frozen at the "
                    "moment of decision, not at delivery.",
    )
    decision_ts: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of the per-call governance "
                    "decision · every call carries its own timestamp, "
                    "never inherited from a prior call.",
    )
    governance_class: str = Field(
        ...,
        min_length=1,
        description="The class carried inline on this response · A18.3 "
                    "verbatim: 'Every response carries its class inline.'",
    )
    floor_applied: str = Field(
        ...,
        min_length=1,
        description="The provisioned floor the class was checked against "
                    "· A18.4 verbatim: 'A query that falls below the "
                    "skill's floor returns the refusal envelope.'",
    )

    @field_validator("decision_ts")
    @classmethod
    def _iso_timestamp(cls, v: str) -> str:
        try:
            parsed = datetime.fromisoformat(v)
        except ValueError as exc:
            raise ValueError(
                f"decision_ts {v!r} is not ISO-8601 · A18.3 requires "
                f"ISO-8601 UTC timestamps for the per-call decision moment"
            ) from exc
        if parsed.tzinfo is None:
            raise ValueError(
                f"decision_ts {v!r} is naive · A18.3 requires "
                f"timezone-aware UTC"
            )
        return v
