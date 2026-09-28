"""TrainingRunV0 · Doc 17 lines 15, 55, 88-101 · trainer-run envelope.

Doc 17 line 15 verbatim (grounding brief line 55):
    'Every model the platform trains is a LoRA/PEFT adapter over a
     registered open base model - never a full fine-tune, never an
     unregistered model. This is FACT-class in the ratified spec,
     meaning it is not revisited per training job; it is a standing
     constraint on what training is allowed to mean on this platform.'

Doc 17 line 101 verbatim (grounding brief line 64):
    'No model enters service without clearing all six MOAC criteria on
     uncurated held-out material, with no human in the acceptance path.'

Doc 17 line 90 verbatim (grounding brief line 61):
    'The surface displays "four of six checks passed" with all six
     criteria named and rejected models kept on record - real UI, real
     registry schema. But MOAC has a contract and no emitter: nothing
     in the current build actually runs a candidate through the six
     checks and writes the result. The surface is currently a faithful
     rendering of a process that has not yet executed.'

Owner directive at Wave B open (grounding brief line 66):
    'trainer runner: LoRA/PEFT + Muon two-arm + Critic Seam gating
     every output + MOAC emission + cost-ledger metering + whitepaper
     on close.'

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/training_run_v0.contract_snapshot.json.
  * Parity map bump 65 -> 66.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


ADAPTER_KINDS: tuple = ("lora", "peft")
RUN_STATUS: tuple = (
    "admitted",         # material admitted, run not yet started.
    "running_mock",     # mock SSH seam - deterministic canned execution.
    "running_real",     # real SSH seam - live GPU execution.
    "moac_emitted",     # six-check MOAC card written.
    "closed_adopted",   # whitepaper written, adapter registered.
    "closed_rejected",  # MOAC failed at least one criterion.
    "aborted",          # run halted before MOAC (crash/refusal/preempt).
)


class TrainingRunV0(BaseModel):
    """Doc 17 line 15 · one trainer run against one recipe on one base.

    LoRA/PEFT invariant enforced at construction; full fine-tunes are
    refused as-of-fact-class. Base model must be a registered id.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    run_id: str = Field(..., min_length=1)
    recipe_version: str = Field(
        ...,
        min_length=1,
        description="training_params@v0/<name> - MUST reference an "
                    "adopted optimizer_comparison recipe (A17.4 · CP5).",
    )
    base_model_id: str = Field(
        ...,
        min_length=1,
        description="Registered base model id (never an unregistered model, "
                    "Doc 17 line 15 verbatim FACT-class).",
    )
    adapter_kind: Literal["lora", "peft"] = Field(
        ...,
        description="LoRA/PEFT only. Full fine-tunes refused by grammar.",
    )
    material_admit_ref: str = Field(
        ...,
        min_length=1,
        description="training_material_admit_id (Doc 17 line 15).",
    )
    ssh_mode: Literal["mock", "real"] = Field(
        ...,
        description="Mock at CP8 landing; flips to real on Owner SSH key arrival.",
    )
    status: Literal[
        "admitted", "running_mock", "running_real",
        "moac_emitted", "closed_adopted", "closed_rejected", "aborted",
    ] = Field(default="admitted")
    moac_card_ref: Optional[str] = Field(
        default=None,
        description="Reference to the six-check MOAC card (Doc 17 line 90). "
                    "Populated on 'moac_emitted' status.",
    )
    whitepaper_ref: Optional[str] = Field(
        default=None,
        description="Reference to the whitepaper drafted on close "
                    "(owner directive · line 66).",
    )
    cost_ledger_ref: Optional[str] = Field(
        default=None,
        description="Reference to the cost-ledger row for this run "
                    "(owner directive · line 66).",
    )
    critic_seam_verdict: Optional[str] = Field(
        default=None,
        description="Critic Seam producer-side verdict summary "
                    "(Doc19A-005 Callers-Cover-the-Rule).",
    )
    started_at: str = Field(..., min_length=1)
    finished_at: Optional[str] = Field(default=None)
    aborted_reason: str = Field(
        default="",
        description="Non-empty when status='aborted'.",
    )

    @model_validator(mode="after")
    def _aborted_carries_reason(self):
        if self.status == "aborted" and not self.aborted_reason:
            raise ValueError(
                "Aborted runs MUST carry an aborted_reason (honesty "
                "grammar Doc19A · QA-4 findings carry classification)."
            )
        return self
