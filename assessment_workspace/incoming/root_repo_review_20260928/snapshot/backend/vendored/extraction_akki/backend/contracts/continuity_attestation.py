"""ContinuityAttestation_v0 · CA1-N5 · Doc 8 §9 (witness) · Doc 9 §3.

Structural scaffolding for the governed-record continuity attestation.
The Witness (Canon 8 §9: 'holds NEITHER authority's credentials · attests
to standing drill outcomes · alarms outward on tamper · cannot act on
the estate') writes this record after a continuity drill.

Owner-policy fields carry `OWNER_POLICY_PENDING` sentinel string until
CA1-N5-q1 is ruled. Service-time invariant refuses to fire while any
such field remains pending.

Freeze contract: parity 49→50.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ContinuityAttestation_v0(BaseModel):
    """Witness-written record after a continuity drill."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    attestation_id: str = Field(
        ..., min_length=1, pattern=r"^ca_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ca_<yyyy_mm_dd>_<n>'."
    )
    attested_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the witness landed the attestation."
    )
    attested_by: str = Field(
        ..., min_length=1,
        description="Witness identifier (e.g., 'witness.independent'). "
                    "Canon 8 §9: the witness holds NEITHER authority's "
                    "credentials."
    )
    attested_scope: Literal[
        "all",
        "northena_ledger",
        "crossing_receipts",
        "chokepoint",
        "watch_verdicts",
        "watch_actions",
    ] = Field(
        ...,
        description="Which governed record class(es) the attestation "
                    "covers. Governed vocabulary."
    )
    rto_target_seconds: str = Field(
        ..., min_length=1,
        description="Stated Recovery-Time Objective for the attested "
                    "scope. String form (owner-facing). "
                    "CA1-N5 · CA1-N5-q1 owner policy: OWNER_POLICY_PENDING "
                    "until the owner rules. Service refuses to fire "
                    "while this equals OWNER_POLICY_PENDING."
    )
    verification_mechanism: str = Field(
        ..., min_length=1,
        description="How the attestation verifies continuity. "
                    "CA1-N5-q1 owner policy · options on record: "
                    "'replication_check' (same Ledger writer property) "
                    "OR 'independent_backup_check' (separate governed "
                    "layer). OWNER_POLICY_PENDING until ruled."
    )
    witness_signature: str = Field(
        ..., min_length=1,
        description="Witness-side signature or reference. Canon 8 §9. "
                    "Structural placeholder until Doc 8 witness fabric "
                    "lands its own signature scheme."
    )
    outcome: Literal["matches", "diverges", "inconclusive"] = Field(
        ...,
        description="Doc 15 §17 verdict grammar reuse · verbatim vocab."
    )
    summary: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what the drill "
                    "measured and what its outcome supports. "
                    "The 'matches' outcome MUST cite the drill scope + "
                    "measured recovery time."
    )
