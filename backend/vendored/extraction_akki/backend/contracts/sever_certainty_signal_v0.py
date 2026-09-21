"""SeverCertaintySignalV0 · Doc 8 line 31 verbatim · closed six-member registry.

Owner-verbatim spec (canon/text/Akki_Canon_8_The_Watch.txt line 31):
    'The closed sever-certainty registry — canary touch, attestation
     failure, mark hit, witness-write attempt, floor violation, mirage
     incrimination — is the whole of what may unlock the Watch's
     maximum autonomous force. A content score or a behavioural
     pattern, however confident, is a signal an attacker can shape,
     and a system whose maximum power can be triggered from outside
     is a weapon handed to whoever learns to trigger it. The certainty
     computation is a function with no parameter through which a
     detector's confidence can enter — Solva's own assertion boundary,
     transplanted: the signature is the guard.'

§Line 221 verbatim (owner-only ceremonial values):
    'the sever-certainty registry's membership — a closed list whose
     every addition is a ceremony, because it is the boundary of
     maximum autonomous force. Until ruled, the conservative default
     holds ... the six-member registry as written in §4.2.'

Closed grammar guarantees: no seventh signal can be added without a
spec-side ceremony (contract-level refusal). The six member IDs
below are the SIX literal signals from line 31; any attempt to
express a signal outside this grammar is unrepresentable, not policed
(Audio plane §1.5 discipline transplanted).

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/sever_certainty_signal_v0.contract_snapshot.json.
  * Parity map bump 67 -> 68.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# The SIX members of the closed sever-certainty registry (line 31 verbatim).
SEVER_CERTAINTY_SIGNALS: tuple = (
    "canary_touch",
    "attestation_failure",
    "mark_hit",
    "witness_write_attempt",
    "floor_violation",
    "mirage_incrimination",
)


class SeverCertaintySignalV0(BaseModel):
    """One assertion from a sever-certainty signal source.

    §Line 30 verbatim: 'Structural certainty is assertable only from
    signals an outsider cannot fabricate. Everything externally
    steerable caps at reversible containment, whatever its score.'

    This model carries no confidence field by design — 'The certainty
    computation is a function with no parameter through which a
    detector's confidence can enter' (line 31 verbatim). A signal is
    or is not present; there is no shade.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str = Field(..., min_length=1)
    signal_kind: Literal[
        "canary_touch",
        "attestation_failure",
        "mark_hit",
        "witness_write_attempt",
        "floor_violation",
        "mirage_incrimination",
    ] = Field(
        ...,
        description="One of the six line-31 registry members. Closed "
                    "grammar - no seventh member possible without spec "
                    "ceremony (§Line 221).",
    )
    asserted_by: str = Field(
        ...,
        min_length=1,
        description="The unfabricatable source (Solva assertion boundary "
                    "signature). NOT an outsider-steerable identity.",
    )
    asserted_at: str = Field(..., min_length=1)
    evidence_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to the immutable evidence row (a canary "
                    "trip receipt, an attestation failure log, a mark "
                    "resurfacing event, a witness-write attempt tripwire, "
                    "a floor violation record, or a mirage incrimination "
                    "action). Never a content score.",
    )
