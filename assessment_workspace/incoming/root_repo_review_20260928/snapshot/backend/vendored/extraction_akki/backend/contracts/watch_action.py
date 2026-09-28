"""WatchActionRecord_v0 · Canon 8 §8 (Mkono — the responder) · Doc 9 §3.

Writer: Mkono (responder). Readers: both authorities + both consoles
(Canon 8 §33). Mkono writes NOTHING BUT action records.

Every Mkono action is atomic act-and-attest — the ledger row lands
with the action, not after (Canon 8 §8, §32.5).

action_class grammar is verbatim from Canon 8 §7-§18:
  * noted_no_action        — restraint record (§22)
  * mark_minted            — attention/elevated marks (§10)
  * containment_started    — bounded reversible state (§14)
  * containment_extended   — reserved-decision required (§19)
  * de_mark_signed         — two signatures required (§11)
  * mirage_engaged         — planted credential/decoy contact (§15)
  * severance_executed     — guilty-inside-mirage aftermath (§15)
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WatchActionRecord_v0(BaseModel):
    """One action record written by Mkono in response to a verdict row."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    action_id: str = Field(
        ..., min_length=1, pattern=r"^ax_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ax_<yyyy_mm_dd>_<n>'."
    )
    at_iso: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when Mkono acted. Atomic with the "
                    "action itself (Canon 8 §32.5)."
    )
    verdict_id: str = Field(
        ..., min_length=1,
        description="WatchVerdictRow_v0.verdict_id this action responds to. "
                    "Service enforces the verdict is on record (seam law)."
    )
    action_class: Literal[
        "noted_no_action",
        "mark_minted",
        "containment_started",
        "containment_extended",
        "de_mark_signed",
        "mirage_engaged",
        "severance_executed",
    ] = Field(
        ...,
        description="Canon 8 action-class grammar · verbatim vocabulary."
    )
    responder: str = Field(
        ..., min_length=1,
        description="Which Mkono responder fired this action (e.g., "
                    "'mkono.mark_writer', 'mkono.containment_manager'). "
                    "Names the WRITER."
    )
    acted_on_ref: str = Field(
        ..., min_length=1,
        description="Reference to the acted-on subject. Same shape as "
                    "WatchVerdictRow_v0.subject_ref. Does NOT reveal "
                    "where within the estate a mark was placed (§32.3)."
    )
    outcome_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what happened. "
                    "IS the attestation body (Canon 8 §32.5 atomic)."
    )
