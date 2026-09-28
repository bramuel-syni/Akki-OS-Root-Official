"""TrainingMaterialAdmitV0 · Doc 17 line 15 verbatim (training-material admit).

Doc 17 line 15 verbatim (grounding brief line 55):
    'Training material is drawn exclusively from de-duplicated,
     VAD-cleaned, qualified units — the same units the estate's
     extraction pipeline already produces, never raw source reached
     around that pipeline.'

Owner directive at Wave B open: 'trainer runner: LoRA/PEFT + Muon
two-arm + Critic Seam gating every output + MOAC emission + cost-ledger
metering + whitepaper on close.'

This contract is the mechanical gate that admits material to a run.
It fails hard if any of the three qualifications is missing.

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/training_material_admit_v0.contract_snapshot.json.
  * Parity map bump 64 -> 65.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TrainingMaterialAdmitV0(BaseModel):
    """Doc 17 line 15 · training-material admission gate.

    All three invariants MUST be True; a False on any bit is a hard
    refusal, not a warning. The `extraction_pipeline_ref` cites the
    exact estate pipeline (never raw source reached around it).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    admit_id: str = Field(..., min_length=1)
    training_run_id: str = Field(..., min_length=1)
    unit_manifest_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the manifest listing every unit admitted.",
    )
    unit_count: int = Field(..., ge=1)
    deduped: bool = Field(
        ...,
        description="Units are de-duplicated per Doc 17 line 15 verbatim.",
    )
    vad_cleaned: bool = Field(
        ...,
        description="Units are VAD-cleaned per Doc 17 line 15 verbatim.",
    )
    qualified: bool = Field(
        ...,
        description="Units are qualified per Doc 17 line 15 verbatim.",
    )
    extraction_pipeline_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the estate extraction pipeline that "
                    "produced these units. 'never raw source reached "
                    "around that pipeline' - the presence of a non-empty "
                    "ref is the mechanical admission that the pipeline "
                    "was the source.",
    )
    admitted_at: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def _all_three_qualifications_required(self):
        missing = []
        if not self.deduped:
            missing.append("deduped")
        if not self.vad_cleaned:
            missing.append("vad_cleaned")
        if not self.qualified:
            missing.append("qualified")
        if missing:
            raise ValueError(
                f"Doc 17 line 15 verbatim: 'Training material is drawn "
                f"exclusively from de-duplicated, VAD-cleaned, qualified "
                f"units'. Missing: {missing!r} - admission refused."
            )
        return self
