"""Witness fabric contracts · Canon 8 §9 + §33 · W10 CP5.

Three frozen record classes for the Watch's witness (Canon 8 §9):

  * WitnessIdentity_v0    — independent identity carrying opaque
                            signing_material_ref · NO authority
                            credentials · attests + alarms only.
  * WitnessAttestation_v0 — attestation to a drill receipt, continuity
                            snapshot, or record class manifest ·
                            written by the witness after read-only
                            inspection of the subject.
  * TamperAlarm_v0        — alarm raised by the witness on tamper
                            evidence (§9: alarms outward on tamper).

Freeze contracts: parity 55 → 58 (headline + 2 secondaries).

Design law reminder: witness holds NEITHER authority's credentials
(§9 verbatim) · witness cannot act on the estate. This is enforced
at the contract layer (no credential fields · no writer refs) and
the service layer (no imports of estate writers).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WitnessIdentity_v0(BaseModel):
    """Independent witness identity · Canon 8 §9."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    witness_id: str = Field(
        ..., min_length=1, pattern=r"^wi_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'wi_<yyyy_mm_dd>_<n>'."
    )
    registered_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the witness identity was registered."
    )
    signing_material_ref: str = Field(
        ..., min_length=1,
        description="Opaque reference to the witness's signing material "
                    "(hash prefix or handle). The RAW signing material "
                    "NEVER lives in the record; only its reference. "
                    "Canon 8 §9 · Owner Order 2026-08-25 §4."
    )
    independent_of_authorities: Literal[True] = Field(
        ...,
        description="Canon 8 §9 verbatim invariant: witness holds "
                    "NEITHER authority's credentials. This field is "
                    "always True; a False value is a contract-shape "
                    "refusal (governance defect)."
    )
    registration_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what the witness "
                    "attests to (drill receipts + tamper alarms) and "
                    "confirming its independence from Watch + governance."
    )


class WitnessAttestation_v0(BaseModel):
    """A single witness attestation to a governed record class artefact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    attestation_id: str = Field(
        ..., min_length=1, pattern=r"^wa_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'wa_<yyyy_mm_dd>_<n>'."
    )
    witness_id: str = Field(
        ..., min_length=1,
        description="WitnessIdentity_v0.witness_id issuing the attestation."
    )
    attested_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the attestation was recorded."
    )
    subject_kind: Literal[
        "drill_receipt",
        "continuity_snapshot",
        "record_class_manifest",
        "watch_action",
    ] = Field(
        ...,
        description="Canon 8 §33 subject-kind grammar · what class of "
                    "artefact this attestation covers. Governed vocab. "
                    "W11 C CP-C4 extended with 'watch_action' per Doc "
                    "8 §Line 170 sentence 1: 'Watch workers attest "
                    "each other's action digests within their bound.'"
    )
    subject_ref: str = Field(
        ..., min_length=1,
        description="Stable reference to the attested artefact "
                    "(usually a phase0/... path or an id). Read-only "
                    "target · the witness inspects but never writes it."
    )
    attested_hash: str = Field(
        ..., min_length=1,
        description="sha256 hash of the attested content at the moment "
                    "of attestation. Convention: 'sha256:<hex>'. "
                    "Later re-reads compare against this hash · a "
                    "mismatch is a TamperAlarm_v0."
    )
    attestation_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what the witness "
                    "observed. Never carries the subject_kind as its "
                    "own answer; must add fact beyond the classification."
    )


class TamperAlarm_v0(BaseModel):
    """Witness alarm raised on tamper evidence (Canon 8 §9)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    alarm_id: str = Field(
        ..., min_length=1, pattern=r"^ta_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ta_<yyyy_mm_dd>_<n>'."
    )
    witness_id: str = Field(
        ..., min_length=1,
        description="WitnessIdentity_v0.witness_id raising the alarm."
    )
    detected_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the tamper was detected."
    )
    evidence_kind: Literal[
        "missing_receipt",
        "modified_receipt",
        "signature_mismatch",
    ] = Field(
        ...,
        description="Canon 8 §9 tamper-evidence grammar · governed vocabulary."
    )
    evidence_ref: str = Field(
        ..., min_length=1,
        description="Stable reference to the tampered artefact "
                    "(usually a phase0/... path or an id)."
    )
    alarm_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what the witness "
                    "found. Never carries the evidence_kind as its own "
                    "answer; must add specific observed detail."
    )
