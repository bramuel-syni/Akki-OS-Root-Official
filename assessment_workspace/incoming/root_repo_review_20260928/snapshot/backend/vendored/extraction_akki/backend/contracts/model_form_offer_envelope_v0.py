"""contracts.model_form_offer_envelope_v0 · W11 D · CP-D0 · A17.16 ACCEPT.

Owner verbatim (2026-08-26T~12:40Z · Batch 2 · ruling 1):
    'A17.16 ingredient-manifest guarantee: ACCEPT. Owner reasoning
     verbatim: claiming provenance of assertions would be
     "overclaiming something training structurally cannot support —
     a direct violation of the platform's own \"measure, don't
     assert\" doctrine. Provenance of ingredients is the honest
     ceiling... the training manifest already tracks exactly this."
     Effective NOW.'

Owner step 3 verbatim: 'take the model-output form OFF the wizard's
refused list. It must now be offerable carrying the INGREDIENTS-ONLY
guarantee explicitly ("provenance of ingredients: what went in, its
standard, its licence — never provenance of assertions") and the
surface/contract must make any stronger claim unrepresentable.'

Doc 17 §17.3 principle 4 verbatim: 'Unrepresentable, not policed.
Safety boundaries are enforced by making the violating state
impossible to express in the contract, not by review after the fact.'

Discipline (frozen · extra=forbid) matches every Wave A/B/C envelope.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# --- Load-bearing verbatim strings · locked at import time --- #
INGREDIENTS_ONLY_GUARANTEE_VERBATIM: str = (
    "provenance of ingredients: what went in, its standard, its "
    "licence — never provenance of assertions"
)


class ModelFormOfferEnvelopeV0(BaseModel):
    """The admission-time offer envelope for output.form == 'model'
    under A17.16 ACCEPT · replaces the prior AdmissionRefusal_v0
    (reason=form_not_offerable) that Phase 2 v3 §6.5 emitted.

    The envelope is a POSITIVE surface — it announces the model form
    IS offered, carrying only the ingredients-only guarantee. The
    contract itself makes any stronger claim unrepresentable
    (§17.3 principle 4)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    trace_id: str = Field(..., min_length=1)
    output_form: Literal["model"] = Field(
        ...,
        description="Locked to 'model' · A17.16 handles ONE admission "
                    "flip. Reusing this envelope for other output "
                    "forms is unrepresentable by construction.",
    )
    offered_at: str = Field(..., min_length=1)
    ingredients_guarantee: str = Field(
        ...,
        description="A17.16 verbatim guarantee text. Must equal "
                    "INGREDIENTS_ONLY_GUARANTEE_VERBATIM exactly. "
                    "Weakening the guarantee is refused at construction.",
    )
    forbidden_stronger_claims: List[str] = Field(
        ...,
        min_length=1,
        description="§17.3 principle 4 · 'unrepresentable, not policed.' "
                    "The envelope enumerates what stronger claim it "
                    "explicitly refuses to make. Non-empty by contract.",
    )

    @field_validator("ingredients_guarantee")
    @classmethod
    def _guarantee_is_verbatim(cls, v: str) -> str:
        if v != INGREDIENTS_ONLY_GUARANTEE_VERBATIM:
            raise ValueError(
                "ingredients_guarantee must be the A17.16 verbatim "
                f"text: {INGREDIENTS_ONLY_GUARANTEE_VERBATIM!r}. "
                f"Got: {v!r}. Paraphrase / weakening refused."
            )
        return v
