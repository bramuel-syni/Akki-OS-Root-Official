"""SkillFileProvenanceV0 · Doc 18 A18.7 · buyer-facing provenance chain.

Owner-verbatim from Doc 18 A18.7:
    'every skill's provenance chain traces back to the training run that
     produced its adapter (extends Doc14-016 rights-lineage + Doc14-017
     version-history).'

Same-commit DoD:
  * `ConfigDict(extra="forbid", frozen=True)` — buyer-facing shape drift
    protection + in-memory hardening (Owner ruling TF-E4 (b) β pattern).
  * `tests/invariants/skill_file_provenance_v0.contract_snapshot.json`
    is the frozen JSON Schema snapshot of THIS module's headline model
    at CP4 landing.
  * `test_frozen_contract_snapshot_parity.py` map bumps 59 → 60 with
    a new entry `skill_file_provenance_v0.py → skill_file_provenance_v0.contract_snapshot.json`.

Chain shape (verbatim from Doc 18 §7 illustrative):

    base_model ── training_run ── moac_admission ── skill_provision

Every ProvenanceStep row carries:
  * step_id       · UUID or ledger row identifier.
  * kind          · one of the four grammar values above.
  * label         · plain-language description for the /skill-files surface.
  * at            · ISO-8601 UTC timestamp of the step.
  * artifact_ref  · optional artifact-store key for the step artefact.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


PROVENANCE_STEP_KINDS: tuple = (
    "base_model",
    "training_run",
    "moac_admission",
    "skill_provision",
)


class ProvenanceStep(BaseModel):
    """A single step in the provenance chain from base model to skill provisioning."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    step_id: str = Field(..., min_length=1)
    kind: Literal["base_model", "training_run", "moac_admission", "skill_provision"]
    label: str = Field(
        ...,
        min_length=1,
        description="Plain-language description surfaced on /skill-files.",
    )
    at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of when this step happened.",
    )
    artifact_ref: Optional[str] = Field(
        default=None,
        description="Optional artifact-store key (`artifacts/{trace_id}/{...}.json`) "
                    "for the step's outward-facing artefact.",
    )


class SkillFileProvenanceV0(BaseModel):
    """Doc 18 A18.7 · buyer-facing provenance chain shape.

    Every skill's provenance chain runs base_model → training_run →
    moac_admission → skill_provision, ordered by ``at``. The chain
    integrity is validated at model construction; downstream services
    read this record via `services.skill_files.persistence`.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    skill_id: str = Field(..., min_length=1)
    adapter_id: str = Field(
        ...,
        min_length=1,
        description="Registry id of the adapter this skill exposes; extends "
                    "Doc14-006 (registry) + Doc14-017 (versioning).",
    )
    training_run_id: str = Field(
        ...,
        min_length=1,
        description="Ledger id of the training run that produced the adapter; "
                    "extends Doc17-008 (staged plans) + Doc14-016 (lineage).",
    )
    moac_card_id: str = Field(
        ...,
        min_length=1,
        description="Ledger id of the MOAC card that admitted the adapter "
                    "(Doc14-008 six-criterion card).",
    )
    recipe_version: str = Field(
        ...,
        min_length=1,
        description="`training_params@v0/<name>` sidecar reference (T-1.3); "
                    "the recipe seat entry that fired this adapter's run. "
                    "Empty seat is not admissible — CP5 fills the seat.",
    )
    provenance_chain: List[ProvenanceStep] = Field(
        default_factory=list,
        description="Ordered list of steps · runtime-validated to enforce "
                    "chain integrity.",
    )
    provisioned_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of skill provisioning.",
    )

    @model_validator(mode="after")
    def _validate_chain_shape(self):
        chain = list(self.provenance_chain)
        if chain and chain[0].kind != "base_model":
            raise ValueError(
                "Doc 18 A18.7 chain integrity: first step must be base_model, "
                f"got {chain[0].kind!r}"
            )
        return self
