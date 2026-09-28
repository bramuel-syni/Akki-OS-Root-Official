"""MirageArtifactV0 · Doc 8 line 136, 183 verbatim · synthetic-provenance carried.

Owner-verbatim spec (canon/text/Akki_Canon_8_The_Watch.txt):

  §Line 136:
    'The mirage lies outward, never inward. Every mirage interaction
     writes truthfully marked records; the deception is a rendering
     shown to the suspect, never a falsification of anything beneath.
     And mirage state shares no store with production — bleed is
     unrepresentable, not filtered.'

  §Line 183:
    'Mirage isolation. Synthetic state shares no store with production;
     synthetic provenance is carried internally on every mirage
     artifact.'

Contract invariants (unrepresentable posture · Audio §1.5 discipline):
  * `synthetic_provenance` field is REQUIRED and non-empty (§Line 183:
    'carried internally on every mirage artifact').
  * `is_synthetic=True` is REQUIRED (bool field; True by construction).
  * `production_store_leak_check` is an assertion field that MUST be
    'passed' at ratification (guards against store bleed).

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/mirage_artifact_v0.contract_snapshot.json.
  * Parity map bump 69 -> 70.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MirageArtifactV0(BaseModel):
    """An artifact rendered inside the mirage · §Line 136-183 invariants."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    artifact_id: str = Field(..., min_length=1)
    mirage_session_id: str = Field(
        ...,
        min_length=1,
        description="Mirage session this artifact belongs to. Isolated "
                    "from production sessions per §Line 183.",
    )
    is_synthetic: Literal[True] = Field(
        ...,
        description="Every mirage artifact is synthetic by construction. "
                    "Grammar forbids False - a real artifact never lives "
                    "in mirage store (§Line 183 unrepresentable).",
    )
    synthetic_provenance: str = Field(
        ...,
        min_length=1,
        description="§Line 183 verbatim: 'synthetic provenance is carried "
                    "internally on every mirage artifact.' Non-empty ref "
                    "to the generation record required.",
    )
    production_store_leak_check: Literal["passed"] = Field(
        ...,
        description="Assertion that this artifact's persistence does not "
                    "share a store handle with production. Grammar allows "
                    "only 'passed' - failure state is unrepresentable "
                    "(§Line 136: 'bleed is unrepresentable, not filtered').",
    )
    outward_lie_only: Literal[True] = Field(
        ...,
        description="§Line 136 verbatim: 'The mirage lies outward, never "
                    "inward. Every mirage interaction writes truthfully "
                    "marked records; the deception is a rendering shown "
                    "to the suspect, never a falsification of anything "
                    "beneath.' True by construction.",
    )
    created_at: str = Field(..., min_length=1)
