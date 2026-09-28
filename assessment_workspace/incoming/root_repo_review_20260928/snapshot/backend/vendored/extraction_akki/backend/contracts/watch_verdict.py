"""WatchVerdictRow_v0 · Canon 8 §7 (Macho — the sensor) · Doc 9 §3.

Writer: Macho (sensor). Readers: Mkono + both consoles + auditors
(Canon 8 §33). Macho writes NOTHING ELSE (Canon 8 §7).

Constitutional negatives enforced by contract shape:
  * No 'profile' or 'raw_features' or 'threshold' keys (W13 · §32.1/32.2).
  * signal_class + severity carry a governed vocabulary; free-form
    fields ('evidence_note') carry a facts-not-claims sentence.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WatchVerdictRow_v0(BaseModel):
    """One row minted by Macho on the shared record."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    verdict_id: str = Field(
        ..., min_length=1, pattern=r"^vd_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'vd_<yyyy_mm_dd>_<n>'."
    )
    at_iso: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when Macho minted the verdict."
    )
    sensor: str = Field(
        ..., min_length=1,
        description="Which Macho sensor minted this verdict (e.g., "
                    "'macho.declaration_delta', 'macho.mirage_touch'). "
                    "Names the SENSOR (writer), not a threshold."
    )
    signal_class: str = Field(
        ..., min_length=1,
        description="Class of signal detected (e.g., "
                    "'declaration_behaviour_divergence', "
                    "'planted_credential_touched', 'refusal_bypass'). "
                    "Governed vocabulary owned by Macho."
    )
    severity: Literal["noted", "attention", "elevated", "severe"] = Field(
        ...,
        description="Canon 8 severity grammar · verbatim vocabulary. "
                    "'noted' = restraint record only (Canon 8 §22); "
                    "'severe' = mirage-touch or similar structural finding."
    )
    subject_kind: Literal["actor", "task", "artifact", "estate"] = Field(
        ...,
        description="What kind of subject the verdict targets."
    )
    subject_ref: str = Field(
        ..., min_length=1,
        description="Reference to the subject (e.g., 'actor:alice', "
                    "'task:t_1234'). Does NOT expose profile internals."
    )
    evidence_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming the observable "
                    "difference (Canon 1 §4.4). Never carries "
                    "'threshold' or 'raw features' language."
    )
