"""Grey Mirror mirage contracts · Canon 8 §15-§16 + §32.4.

W10 CP2 · BUILD (not LIFT). Donor repos hold no mirage material
(DECISIONS.md 2026-08-19 L768 verdict).

Contracts:
  * Mirage_v0                — planting record (opaque · §32.4).
  * MirageTouch_v0           — touch record (governed vocabulary R2).
  * Severance_v0             — aftermath record on guilty_use touches.

Canon 8 §32.4 negative surface: NO surface renders mirage
construction. Every field this contract exposes MUST be
touch-safe (i.e., reading a mirage record cannot reconstruct the
planted material).

R2 (2026-08-26T04:20Z): touch_kind is a frozen Literal enum in the
contract · extension = snapshot-bump ceremony · no service-time
extensibility.

Freeze contracts: parity 52 → 55 (headline + 2 secondaries).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Mirage_v0(BaseModel):
    """A governed misdirection · planted credential, honeytoken, or
    decoy artefact (Canon 8 §15). This record IS the planting fact;
    it must NOT expose planting internals (§32.4)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    mirage_id: str = Field(
        ..., min_length=1, pattern=r"^mr_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'mr_<yyyy_mm_dd>_<n>'."
    )
    planted_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the mirage was planted."
    )
    expires_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the mirage expires. Canon 8 §17: "
                    "state without expiry IS a defect; auto-extension "
                    "is FORBIDDEN (§32.7)."
    )
    mirage_class: Literal[
        "planted_credential",
        "honeytoken",
        "decoy_artefact",
    ] = Field(
        ...,
        description="Canon 8 §15 mirage-class grammar · verbatim vocabulary."
    )
    planted_by: str = Field(
        ..., min_length=1,
        description="Which Mkono responder planted the mirage (e.g., "
                    "'mkono.mirage_planter'). Names the WRITER."
    )
    opaque_ref: str = Field(
        ..., min_length=1,
        description="A one-way reference to the planted material — a "
                    "hash prefix or opaque handle. Reads through this "
                    "field CANNOT reconstruct the planted material "
                    "(§32.4 mirage construction hidden)."
    )
    planting_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming WHY this mirage "
                    "was planted (e.g., 'honeytoken at boundary for "
                    "credential-touch detection'). Does NOT name WHERE."
    )


class MirageTouch_v0(BaseModel):
    """A recorded contact with a mirage (Canon 8 §15: 'contact with a
    mirage is a STRUCTURAL FINDING'). touch_kind grammar is
    CONTRACT-TIME per R2 · extension = snapshot-bump ceremony."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    touch_id: str = Field(
        ..., min_length=1, pattern=r"^mt_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'mt_<yyyy_mm_dd>_<n>'."
    )
    mirage_id: str = Field(
        ..., min_length=1,
        description="Mirage_v0.mirage_id that was touched. Service "
                    "enforces the mirage is on record (chokepoint · no "
                    "side doors)."
    )
    touched_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when the touch was recorded."
    )
    actor_ref: str = Field(
        ..., min_length=1,
        description="Reference to the actor who touched the mirage. "
                    "Same shape convention as WatchVerdictRow.subject_ref."
    )
    touch_kind: Literal["innocent_read", "guilty_use"] = Field(
        ...,
        description="Canon 8 §15 innocent/guilty split · CONTRACT-TIME "
                    "grammar per Orchestrator R2 (2026-08-26T04:20Z). "
                    "'innocent_read' = ordinary work; 'guilty_use' = "
                    "credential used against real endpoint / decoy "
                    "artefact exfiltrated."
    )
    evidence_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what evidence "
                    "supports the touch_kind classification. "
                    "'guilty_use' MUST cite specific evidence."
    )


class Severance_v0(BaseModel):
    """Aftermath record: severance executed on Mkono's own authority
    after a guilty_use touch (Canon 8 §15: 'the decision panel
    receives the AFTERMATH, not the request')."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    severance_id: str = Field(
        ..., min_length=1, pattern=r"^sv_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'sv_<yyyy_mm_dd>_<n>'."
    )
    touch_id: str = Field(
        ..., min_length=1,
        description="MirageTouch_v0.touch_id that motivated severance."
    )
    severed_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC when severance executed."
    )
    severed_by: str = Field(
        ..., min_length=1,
        description="Which Mkono responder executed the severance "
                    "(e.g., 'mkono.severance_manager'). Names the WRITER."
    )
    aftermath_note: str = Field(
        ..., min_length=1,
        description="Facts-not-claims sentence naming what was severed "
                    "and how the decision panel receives the aftermath "
                    "(not the request · §15)."
    )
