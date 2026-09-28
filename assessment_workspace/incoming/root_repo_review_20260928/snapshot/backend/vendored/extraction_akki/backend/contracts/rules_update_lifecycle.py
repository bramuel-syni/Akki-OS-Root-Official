"""Rules Updates ceremony lifecycle · Doc 15 §17 remainder.

After counter-sign (approvals CP3), an APPROVED rules_update kind
enters a three-state lifecycle:

    COUNTDOWN → APPLY → RE-CHECK

Each state is a distinct on-disk record (append-only) keyed to its
predecessor by id. Service-time invariants enforce the flow (see
services/approvals/rules_update_lifecycle.py).

Freeze contracts:
  * CountdownStarted_v0        — parity 42→43 (but W8 CP4 landed 43+44
    for N-series; this CP lands 45/46/47 · see snapshot mapping).
  * RulesUpdateApplied_v0      — one apply per countdown.
  * RulesUpdateReChecked_v0    — one re-check per apply.

Doc 15 §17 anchor: "propose · counter-sign · countdown · apply ·
re-check. The five states are a governance discipline, not a
technical machine; every transition is a record on file."
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CountdownStarted_v0(BaseModel):
    """Countdown window begun after an APPROVED rules_update decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    countdown_id: str = Field(
        ..., min_length=1, pattern=r"^cds_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'cds_<decision_tail>'."
    )
    decision_id: str = Field(
        ..., min_length=1,
        description="ApprovalDecision_v0.decision_id (verdict must be "
                    "'approved'; service enforces)."
    )
    started_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the countdown was started."
    )
    countdown_ends_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the countdown ends and apply may "
                    "fire. Doc 15 does not dictate the duration; owner "
                    "policy names it per rules_update kind."
    )
    started_by: str = Field(
        ..., min_length=1,
        description="Actor id starting the countdown. Convention: the "
                    "approver may start their own countdown; service "
                    "does not require SoD here."
    )
    note: str = Field(
        ..., min_length=1,
        description="Human sentence naming the countdown window rationale "
                    "(e.g., 'Standard 24h window for masking clauses.')."
    )


class RulesUpdateApplied_v0(BaseModel):
    """Rules update takes effect after countdown_ends_at has elapsed."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    applied_id: str = Field(
        ..., min_length=1, pattern=r"^app_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'app_<countdown_tail>'."
    )
    countdown_id: str = Field(
        ..., min_length=1,
        description="CountdownStarted_v0.countdown_id being applied."
    )
    applied_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the rule was applied. MUST be "
                    "≥ countdown_ends_at (service enforces)."
    )
    applied_by: str = Field(
        ..., min_length=1,
        description="Actor id firing the apply."
    )
    apply_result_summary: str = Field(
        ..., min_length=1,
        description="One-sentence description of what the apply changed. "
                    "Facts-not-claims (Canon 1 §4.4)."
    )


class RulesUpdateReChecked_v0(BaseModel):
    """Re-check confirms the applied change did what the request stated.
    Doc 15 §17: re-check is the ceremony completion — not a comfort loop."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    recheck_id: str = Field(
        ..., min_length=1, pattern=r"^rec_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'rec_<applied_tail>'."
    )
    applied_id: str = Field(
        ..., min_length=1,
        description="RulesUpdateApplied_v0.applied_id being re-checked."
    )
    rechecked_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the re-check was performed."
    )
    rechecked_by: str = Field(
        ..., min_length=1,
        description="Actor id firing the re-check."
    )
    recheck_verdict: Literal["matches", "diverges", "inconclusive"] = Field(
        ...,
        description="Doc 15 §17 verdict grammar · verbatim vocabulary."
    )
    recheck_summary: str = Field(
        ..., min_length=1,
        description="Human sentence naming what evidence supports the "
                    "verdict (e.g., which crossings were sampled). "
                    "'matches' MUST cite specific evidence."
    )
