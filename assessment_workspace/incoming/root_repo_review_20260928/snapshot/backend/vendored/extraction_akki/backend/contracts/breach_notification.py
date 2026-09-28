"""BreachNotification_v0 · CA1-N2 · Addendum §N-series.

Wave E · CP-E2 (2026-08-27T~13:35Z) resolves the four policy sentinels
to owner-ruled values via `services/n_series/breach_policy.v0.json`.
The Literal grammars below still admit `OWNER_POLICY_PENDING` for
callers who haven't picked the resolved values; the service refuses
to fire when any sentinel remains.

Additive fields landed at CP-E2 (owner ruling verbatim: 'implement
as enforcement, not scaffolding'):
  * trigger_event_class          — {containment_failure, actual_exfiltration, unreceipted_crossing}
  * notify_deadline_utc          — Optional; enforcement-computed as
                                   triggered_at + 72h if not supplied
  * recipient_dpo_id             — Required for fire
  * recipient_witness_id         — Required, MUST be a registered
                                   WitnessIdentity_v0
  * source_watch_action_class    — the Watch action_class that motivated
                                   the notification; enforcement refuses
                                   for {annotate, shape, contain} per
                                   owner invariant ('contained/shaped
                                   events are the Watch working and
                                   MUST NOT trigger notification').
  * alert_channel_receipts       — list of file-drop paths where
                                   real-time alerts were written
                                   (ledger row alone is insufficient
                                   per owner ruling).

The four open policy questions (each field's Literal type below):
  q1_trigger_scope         · "refusal_bypass_only" | "refusal_bypass_and_near_miss" | OWNER_POLICY_PENDING
  q2_notification_routing  · "watch_self_witness" | "independent_authority" | OWNER_POLICY_PENDING
  q3_actor_masking         · "actor_ids_visible" | "actor_ids_masked" | OWNER_POLICY_PENDING
  q4_cadence               · "one_per_breach" | "aggregated_windows" | OWNER_POLICY_PENDING

Freeze contract: 43rd post-W8 CP4 (BreachNotification_v0 half).
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


OWNER_POLICY_PENDING = "OWNER_POLICY_PENDING"


class BreachNotification_v0(BaseModel):
    """A breach-notification record. Structural shape lands at W8;
    the four policy sentinels resolve on owner ruling (Wave E CP-E2
    ratifies q1/q2/q3/q4 via breach_policy.v0.json)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    notification_id: str = Field(
        ..., min_length=1, pattern=r"^bn_[a-z0-9_-]+$",
    )
    breach_summary: str = Field(
        ..., min_length=1,
        description="One-sentence description of what triggered the notification.",
    )
    triggered_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")

    q1_trigger_scope: Literal[
        "refusal_bypass_only",
        "refusal_bypass_and_near_miss",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N2 · POLICY QUESTION: does the notification fire on "
                    "refusal-bypass only, or on near-miss too? Owner ruled "
                    "'refusal_bypass_only' at Wave E CP-E2 · see "
                    "breach_policy.v0.json.",
    )
    q2_notification_routing: Literal[
        "watch_self_witness",
        "independent_authority",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N2 · POLICY QUESTION: routes to Watch (self-witness) "
                    "or an independent authority? Owner ruled "
                    "'independent_authority' at Wave E CP-E2 (DPO + external "
                    "witness).",
    )
    q3_actor_masking: Literal[
        "actor_ids_visible",
        "actor_ids_masked",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N2 · POLICY QUESTION: notification body carries "
                    "actor ids in the clear, or masked? Owner ruled "
                    "'actor_ids_masked' at Wave E CP-E2 (Canon 8 default).",
    )
    q4_cadence: Literal[
        "one_per_breach",
        "aggregated_windows",
        "OWNER_POLICY_PENDING",
    ] = Field(
        default="OWNER_POLICY_PENDING",
        description="CA1-N2 · POLICY QUESTION: one notification per breach, "
                    "or aggregated windows? Owner ruled 'one_per_breach' at "
                    "Wave E CP-E2.",
    )

    # ── Wave E CP-E2 additive fields (enforcement, not scaffolding) ──

    trigger_event_class: Literal[
        "containment_failure",
        "actual_exfiltration",
        "unreceipted_crossing",
    ] = Field(
        ...,
        description="Owner mapping (Wave E §1 verbatim): 'hard line "
                    "ACTUALLY CROSSED' onto the existing Watch event "
                    "grammar. Contained/shaped events are the Watch "
                    "working and MUST NOT reach this field.",
    )
    recipient_dpo_id: str = Field(
        ..., min_length=1,
        description="DPO recipient · existing platform credential ref. "
                    "Owner ruling: DPO + Watch's existing external witness.",
    )
    recipient_witness_id: str = Field(
        ..., min_length=1, pattern=r"^wi_[a-z0-9_-]+$",
        description="External witness recipient · MUST be a registered "
                    "WitnessIdentity_v0.witness_id with "
                    "independent_of_authorities=True.",
    )
    source_watch_action_class: str = Field(
        ..., min_length=1,
        description="The Watch action_class (or 'unreceipted_crossing' "
                    "for chokepoint-bypass events) that motivated this "
                    "notification. Service refuses for "
                    "{annotate, shape, contain} — those are the Watch "
                    "working and MUST NOT trigger a notification per "
                    "owner invariant.",
    )
    notify_deadline_utc: Optional[str] = Field(
        default=None,
        description="Enforcement-computed as triggered_at + 72h if not "
                    "supplied. 72h window is canon-grounded (Kenya DPA/"
                    "GDPR per owner ruling).",
    )
    alert_channel_receipts: List[str] = Field(
        default_factory=list,
        description="File-drop paths where real-time alerts were "
                    "written (channel = ledger record PLUS real-time "
                    "alert per owner ruling; ledger row alone is "
                    "insufficient).",
    )

