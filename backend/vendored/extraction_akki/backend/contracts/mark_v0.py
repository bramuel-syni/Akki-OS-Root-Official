"""MarkV0 · Doc 8 §Line 127 verbatim · the dye pack.

Owner-verbatim spec (canon/text/Akki_Canon_8_The_Watch.txt §Line 127):
    'A mark — the dye pack — is minted on conviction and binds every
     dimension the system can observe: identity, credentials, session
     and device fingerprint, the behavioural signature, and the
     content hashes of everything touched in the mirage, so the loot
     itself is dyed and its resurfacing anywhere, ever, is a
     structural detection. The mark survives the attacker shedding
     any one dimension, because the others still resolve.'

Six binding dimensions enumerated in the sentence (canon-authoritative):
  1. identity
  2. credentials
  3. session (session_id)
  4. device fingerprint (device_fingerprint)
  5. behavioural signature (behavioural_signature)
  6. content hashes (list, non-empty)

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/mark_v0.contract_snapshot.json.
  * Parity map bump 70 -> 71 (verified via test_frozen_contract_snapshot_parity).
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class MarkV0(BaseModel):
    """One dye-pack mark minted on conviction (§Line 127 verbatim)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    mark_id: str = Field(..., min_length=1)
    verdict_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the MachoVerdict this mark rests on "
                    "(the structural-certainty verdict that convicted).",
    )
    action_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the sever WatchActionV0 (§Line 99 · "
                    "sever = conviction). A mark against annotate/shape/"
                    "contain is a category error - refused at mint time.",
    )
    # ---- the six binding dimensions of §Line 127 verbatim ---- #
    identity: str = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'identity'.",
    )
    credentials: str = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'credentials'.",
    )
    session_id: str = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'session ... fingerprint'.",
    )
    device_fingerprint: str = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'device fingerprint'.",
    )
    behavioural_signature: str = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'the behavioural signature'.",
    )
    content_hashes: List[str] = Field(
        ...,
        min_length=1,
        description="§Line 127 verbatim: 'the content hashes of "
                    "everything touched in the mirage.' Plural, "
                    "non-empty - 'the loot itself is dyed.'",
    )
    minted_at: str = Field(..., min_length=1)
