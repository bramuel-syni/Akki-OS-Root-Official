"""ErasureRequest_v0 · CA1-N3 · Addendum §N-series.

Wave E · CP-E3 (2026-08-27T~13:45Z) resolves the three policy sentinels
to owner-ruled values via `services/n_series/erasure_policy.v0.json`
and lands the additive enforcement fields.

Additive fields (Wave E CP-E3, owner ruling verbatim: 'implement as
enforcement, not scaffolding'):
  * requestor_class          — {named_customer, named_employee}
                               (third-party requires separate
                               authorization per owner ruling)
  * platform_credential_ref  — reference to the existing platform
                               credential used to verify identity
                               (no new identity machinery)
  * model_flag_ids           — RightsLapseFlag_v0.flag_id list
                               emitted for models trained on the
                               subject's data
  * crossing_receipt_ref     — CrossingReceipt.receipt_id issued by
                               services.chokepoint when the erasure
                               operation crossed the custody line

The three open policy questions (each field's Literal type below):
  q1_erasure_reach          · "raw_source_only" | "raw_and_five_ring_units" |
                              "raw_and_units_and_model_weights" | OWNER_POLICY_PENDING
  q2_identity_verification  · "self_declared" | "independent_verifier" |
                              "existing_platform_credential" | OWNER_POLICY_PENDING
  q3_retention_conflict     · "erasure_wins_over_ca1_n1" |
                              "retention_wins_until_expiry" |
                              OWNER_POLICY_PENDING

Freeze contract: 44th post-W8 CP4 (ErasureRequest_v0 half).
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ErasureRequest_v0(BaseModel):
    """An access-and-erasure request record. Structural shape lands
    at W8; the three policy sentinels resolve on owner ruling
    (Wave E CP-E3 ratifies q1/q2/q3 via erasure_policy.v0.json)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    request_id: str = Field(
        ..., min_length=1, pattern=r"^er_[a-z0-9_-]+$",
    )
    requester_actor_id: str = Field(..., min_length=1)
    subject_summary: str = Field(
        ..., min_length=1,
        description="Which artefacts / records the request targets.",
    )
    requested_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")

    q1_erasure_reach: Literal[
        "raw_source_only",
        "raw_and_five_ring_units",
        "raw_and_units_and_model_weights",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N3 · POLICY QUESTION: how deep does erasure "
                    "reach? Owner ruled 'raw_and_five_ring_units' at "
                    "Wave E CP-E3 (models get FLAGGED separately, not "
                    "erased).",
    )
    q2_identity_verification: Literal[
        "self_declared",
        "independent_verifier",
        "existing_platform_credential",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N3 · POLICY QUESTION: identity verified via "
                    "requester's self-declaration, an independent "
                    "verifier, or the existing platform credential? "
                    "Owner ruled 'existing_platform_credential' at "
                    "Wave E CP-E3 (no new identity machinery).",
    )
    q3_retention_conflict: Literal[
        "erasure_wins_over_ca1_n1",
        "retention_wins_until_expiry",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N3 · POLICY QUESTION: when a record is under "
                    "an active CA1-N1 retention window, does an erasure "
                    "request override it? Owner ruled "
                    "'erasure_wins_over_ca1_n1' at Wave E CP-E3 "
                    "(REAL erasure).",
    )

    # ── Wave E CP-E3 additive fields (enforcement, not scaffolding) ──

    requestor_class: Literal[
        "named_customer",
        "named_employee",
    ] = Field(
        ...,
        description="Owner ruling: requestor = named customer or "
                    "employee only, no third-party without separate "
                    "authorization. Third-party requests are refused "
                    "at the service layer.",
    )
    platform_credential_ref: str = Field(
        ..., min_length=1,
        description="Reference to the existing platform credential "
                    "used for identity verification (no new identity "
                    "machinery per owner ruling).",
    )
    model_flag_ids: List[str] = Field(
        default_factory=list,
        description="RightsLapseFlag_v0.flag_id list emitted by the "
                    "service for each trained model whose corpus "
                    "included the subject's data (owner ruling: "
                    "already-trained models get FLAGGED then "
                    "scheduled for retraining OR documented as "
                    "residual exposure).",
    )
    crossing_receipt_ref: Optional[str] = Field(
        default=None,
        description="CrossingReceipt.receipt_id issued by the custody "
                    "chokepoint when the erasure operation crossed "
                    "the custody line (owner ruling: erasure "
                    "operations route through the custody chokepoint "
                    "with crossing receipts).",
    )

