"""RightsLapseFlag_v0 · CA1-N3 · Wave E CP-E3.

Owner ruling (Wave E scope §2 verbatim, 2026-08-27T~12:10Z):
    "already-trained models get FLAGGED via the same provenance
     mechanism as A17.15 rights-lapse, then scheduled for retraining
     OR documented as residual exposure."

RightsLapseFlag_v0 is the record class for that flag. Each flag names
a trained model that carries training data whose subject has requested
erasure. Resolution is one of:
  * `scheduled_retrain` — the model is queued for retraining with the
    subject's data removed;
  * `documented_residual` — retraining is impractical; the residual
    exposure is documented on the model card.

Cross-reference: contracts/erasure_request.py::ErasureRequest_v0.
Cross-reference: services/n_series/erasure.py (writes flag on fire).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RightsLapseFlag_v0(BaseModel):
    """A rights-lapse flag on an already-trained model."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    flag_id: str = Field(
        ..., min_length=1, pattern=r"^rlf_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'rlf_<yyyy_mm_dd>_<n>'."
    )
    erasure_request_id: str = Field(
        ..., min_length=1, pattern=r"^er_[a-z0-9_-]+$",
        description="The ErasureRequest_v0.request_id this flag traces to."
    )
    model_id: str = Field(
        ..., min_length=1,
        description="Trained-model identifier whose training corpus "
                    "included the subject's data."
    )
    subject_ref: str = Field(
        ..., min_length=1,
        description="Reference to the erasure subject (opaque handle · "
                    "no raw PII in the flag record itself)."
    )
    flagged_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the flag was written."
    )
    resolution: Literal[
        "scheduled_retrain",
        "documented_residual",
    ] = Field(
        ...,
        description="Owner ruling verbatim: 'scheduled for retraining "
                    "OR documented as residual exposure.'"
    )
    resolution_summary: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what the flag "
                    "resolution promises (a queued retraining ceremony "
                    "OR the residual-exposure note landing point)."
    )
