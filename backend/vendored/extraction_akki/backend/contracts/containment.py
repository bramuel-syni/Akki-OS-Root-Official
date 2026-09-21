"""Containment_v0 + ContainmentReconciliation_v0 · Canon 8 §14-§18.

Canon 8 §14: "A containment is a BOUNDED, REVERSIBLE operational
state — the affected actor's actions execute in a scoped
environment."

Canon 8 §17: "Every containment and mirage state carries an expiry.
A state WITHOUT AN EXPIRY IS A DEFECT."

Canon 8 §18: "Every containment/mirage expiry reconciles honestly —
the period accounted for, the outcome recorded."

Freeze contracts: parity 50→52 (headline + secondary).

Reserved-decision (Canon 8 §19) side of "extend / promote" is NOT
covered by this contract — that requires human authorship and lands
as an ApprovalRequest_v0 kind='generic'. This CP delivers only the
Mkono-side bounded state records.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Containment_v0(BaseModel):
    """Mkono's bounded, reversible operational state for an actor."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    containment_id: str = Field(
        ..., min_length=1, pattern=r"^cn_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'cn_<yyyy_mm_dd>_<n>'."
    )
    started_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when Mkono started the containment. "
                    "Atomic with the corresponding action_record."
    )
    expires_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the containment expires. Canon 8 "
                    "§17: state without expiry IS a defect; auto-extension "
                    "is FORBIDDEN (§32.7)."
    )
    verdict_id: str = Field(
        ..., min_length=1,
        description="WatchVerdictRow_v0.verdict_id that motivated this "
                    "containment. Seam law (§6)."
    )
    responder: str = Field(
        ..., min_length=1,
        description="Which Mkono responder started the containment "
                    "(e.g., 'mkono.containment_manager')."
    )
    contained_actor_ref: str = Field(
        ..., min_length=1,
        description="Actor under containment (e.g., 'actor:carol'). "
                    "Does NOT expose behavioural-profile internals (§32.1)."
    )
    bound_scope: Literal[
        "read_only_scoped_env",
        "quarantine_copy",
        "no_estate_write",
        "no_egress",
    ] = Field(
        ...,
        description="Canon 8 §14 bounded scope grammar · governed vocabulary. "
                    "'quarantine_copy' = actor's actions execute in a "
                    "quarantine of the estate; 'read_only_scoped_env' = "
                    "actor keeps read but no write; etc."
    )
    bound_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming the bound + expected "
                    "release behaviour. IS the reversibility statement."
    )


class ContainmentReconciliation_v0(BaseModel):
    """Reconciliation record written at containment expiry."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    reconciliation_id: str = Field(
        ..., min_length=1, pattern=r"^cr_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'cr_<yyyy_mm_dd>_<n>'."
    )
    containment_id: str = Field(
        ..., min_length=1,
        description="Containment_v0.containment_id being reconciled."
    )
    expired_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the containment actually expired "
                    "(may equal expires_at for clean expiries)."
    )
    outcome: Literal[
        "expired_clean",
        "extended_by_reserved_decision",
        "escalated",
    ] = Field(
        ...,
        description="Canon 8 §18 outcome grammar · governed vocabulary. "
                    "'expired_clean' = ordinary release; "
                    "'extended_by_reserved_decision' = human-authored "
                    "reserved-decision extension (§19); "
                    "'escalated' = containment ended in a promotion."
    )
    reconciled_by: str = Field(
        ..., min_length=1,
        description="Which Mkono responder wrote the reconciliation."
    )
    period_summary: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what happened "
                    "during the containment period. Canon 8 §18: "
                    "'the period accounted for, the outcome recorded'."
    )
