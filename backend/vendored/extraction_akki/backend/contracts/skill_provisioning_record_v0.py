"""Doc 18 A18.1 · Callable-Skill Provisioning Record V0 · frozen contract shape.

Doc 18 §A18.1 verbatim (Wave B grounding brief · Canon-of-Record):
    'A18.1  [CANON] The provisioning record, reused verbatim. This is the
     frozen contract every skill is created against — not a draft to
     redesign, a specification already anchored to owner rulings
     TF-E2/TF-E4 and reused as-is:

         Callable-skill provisioning record
         {
             skill_id, corpus_slice_ref: artifact-store key,
             key_grant_id, floor, scope, endpoint_path,
             provisioned_at, revoked_at?: str
         }

     §3.7 annex, RMS Intelligence spec, 2026-07'

Doc 18 §A18.2 verbatim (paired slice-freezes-never-edits guardrail):
    'A18.2  [CANON] The slice freezes; it never edits. Corpus slice binds
     at freeze, an endpoint is provisioned against it, and a key is scoped
     to that endpoint. The slice persists via the artifact store,
     write-once. If the underlying material needs to change, the platform
     provisions a new skill against a new slice — it does not mutate the
     old one.'

DISTINCT FROM A18.7 SkillFileProvenanceV0 (already sealed):
  * A18.7 is the buyer-facing PROVENANCE CHAIN (base_model → training_run
    → moac_admission → skill_provision).
  * A18.1 is the OWNER-FACING PROVISIONING RECORD — the single frozen
    tuple recorded once at slice-freeze time, immutable except for the
    optional revoked_at deferred-lifecycle field (per A18.2 write-once
    persistence + owner ruling on revocation being a separate lifecycle).

Both records may reference the same skill_id, but they are separate
first-class Pydantic contracts with independent frozen snapshots for
parity attestation per M15-W2 shape-freeze discipline.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SkillProvisioningRecordV0(BaseModel):
    """A18.1 frozen contract · reused verbatim from §3.7 annex of the
    2026-07 RMS Intelligence spec.

    Eight fields, seven required + one optional (revoked_at). Field order
    matches the canon declaration verbatim. Additional properties are
    forbidden — the shape is a frozen tuple, not an extensible envelope.
    """

    model_config = ConfigDict(extra="forbid")

    skill_id: str = Field(
        ...,
        min_length=1,
        description="Stable identifier for this callable skill · new material "
                    "always yields a new skill_id per A18.2 slice-freezes-never-edits.",
    )
    corpus_slice_ref: str = Field(
        ...,
        min_length=1,
        description="Artifact-store key of the frozen corpus slice bound at "
                    "provisioning time · write-once per A18.2.",
    )
    key_grant_id: str = Field(
        ...,
        min_length=1,
        description="Engineer key-grant record identifier scoped to this "
                    "endpoint per A18.5 server-side scope enforcement.",
    )
    floor: str = Field(
        ...,
        min_length=1,
        description="Governance floor applied per call · below-floor "
                    "returns the refusal envelope per A18.4.",
    )
    scope: str = Field(
        ...,
        min_length=1,
        description="Scope band the key is limited to · enforced at the "
                    "gate on every call per A18.5.",
    )
    endpoint_path: str = Field(
        ...,
        min_length=1,
        description="HTTP path the skill is served under · one endpoint "
                    "per provisioning record per A18.2 endpoint-per-slice.",
    )
    provisioned_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of the write-once provisioning "
                    "event · the moment the corpus slice freezes.",
    )
    revoked_at: Optional[str] = Field(
        default=None,
        description="Optional ISO-8601 UTC timestamp of revocation · "
                    "revocation is a separate lifecycle event and does "
                    "NOT edit the frozen record's other fields "
                    "(A18.2 slice-freezes-never-edits · owner ruling on "
                    "revocation as a distinct lifecycle · non-blocking to "
                    "the frozen tuple).",
    )

    @field_validator("provisioned_at", "revoked_at")
    @classmethod
    def _iso_timestamp_or_none(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            parsed = datetime.fromisoformat(v)
        except ValueError as exc:
            raise ValueError(
                f"timestamp {v!r} is not ISO-8601 · A18.1 requires "
                f"ISO-8601 UTC timestamps for provisioned_at + revoked_at"
            ) from exc
        if parsed.tzinfo is None:
            raise ValueError(
                f"timestamp {v!r} is naive · A18.1 requires timezone-aware UTC"
            )
        return v
