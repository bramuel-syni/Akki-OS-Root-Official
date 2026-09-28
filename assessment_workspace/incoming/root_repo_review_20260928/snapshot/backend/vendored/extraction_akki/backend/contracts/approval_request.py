"""ApprovalRequest_v0 · Doc 15 · governance ceremony · Approvals fabric.

A single contract covers three surface variants (kind discriminator):
  * "rules_update"   · updating a Rulebook rule row (Doc 15).
  * "spend_request"  · authorising a spend against Cost Ledger rates
                       (Doc 15 · CA1-008 anchor).
  * "generic"        · any other governed change requiring approval.

Approval decision carries: approver_actor_id + verdict (approved /
refused / needs_more_info) + note + at_iso. Every request/decision
pair is a governance ceremony record on file.

Freeze contract: 41st post-W8 CP3. Snapshot bijection enforced.

Doc 15 anchor: governance ceremony = "someone proposes a governed
change; someone else records the decision; the pair becomes the
ledgered record on which the change either lands or is refused."
This shape generalizes Rules Updates + Spend Requests + any other
approval surface without duplicating the fabric per kind.
"""
from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ApprovalRequest_v0(BaseModel):
    """Governance request awaiting decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    request_id: str = Field(
        ..., min_length=1, pattern=r"^ar_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ar_<kind>_<yyyy_mm>_<n>'."
    )
    kind: Literal["rules_update", "spend_request", "generic"] = Field(
        ...,
        description="Approval surface variant. Discriminates the payload's "
                    "expected shape (see subject_ref for the anchor).",
    )
    subject_summary: str = Field(
        ..., min_length=1,
        description="One-sentence description of the governed change. "
                    "Facts-not-claims (Canon 1 §4.4)."
    )
    subject_ref: str = Field(
        ..., min_length=1,
        description="Stable reference to the artifact being changed. For "
                    "'rules_update': rule_row_id. For 'spend_request': "
                    "cost_ledger_entry_id or rate_id. For 'generic': "
                    "free-text but must cite an on-record artifact."
    )
    proposed_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the request was authored."
    )
    proposed_by: str = Field(
        ..., min_length=1,
        description="Actor id proposing the change."
    )
    payload: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional kind-specific payload. Owner may extend "
                    "this dict per kind; the contract doesn't dictate "
                    "the inner shape. Never carries credentials "
                    "(Owner Order 2026-08-25 §4)."
    )
    reserved_decision_kind: Optional[
        Literal[
            "promote_containment",
            "extend_expiry",
            "sign_de_mark",
            "resolve_authority_disagreement",
            "cancel_ceremony_in_countdown",
        ]
    ] = Field(
        default=None,
        description="Canon 8 §19 reserved-decision discriminator (W10 CP4). "
                    "Set only when kind='generic' AND the request is a "
                    "reserved decision. Closed enum per Orchestrator R3 "
                    "(2026-08-26T04:20Z) · extensions ride the same "
                    "contract+snapshot+parity same-commit ceremony. "
                    "Canon 8 §32.6 negative: NO reserved-decision is "
                    "executed by machine · this field only classifies."
    )


class ApprovalDecision_v0(BaseModel):
    """Decision on an ApprovalRequest_v0."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decision_id: str = Field(
        ..., min_length=1, pattern=r"^ad_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ad_<request_id_tail>_<yyyy_mm_dd>'."
    )
    request_id: str = Field(
        ..., min_length=1,
        description="ApprovalRequest_v0.request_id being decided."
    )
    verdict: Literal["approved", "refused", "needs_more_info"] = Field(
        ...,
        description="Doc 15 verdict grammar · verbatim vocabulary."
    )
    approver_actor_id: str = Field(
        ..., min_length=1,
        description="Actor id issuing the decision. Must differ from the "
                    "proposer (Doc 15 · separation-of-duties · enforced "
                    "at service time, not by the contract shape)."
    )
    note: str = Field(
        ..., min_length=1,
        description="Human sentence naming the reason for the verdict. "
                    "Never carries the verdict grammar as its own answer; "
                    "must add fact beyond the verdict."
    )
    decided_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the decision was recorded."
    )
