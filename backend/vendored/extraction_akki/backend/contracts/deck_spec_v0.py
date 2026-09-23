"""Doc: Deck Rendering Engine v1.0 · DR-R4 shape-freeze OPENING · frozen contract shell.

DR-R4 verbatim (Master Requirements Registry line 269 · truncation preserved
verbatim as-received from canon extraction · flagged by registry itself as
RD-16 extraction-artefact against DR-R10 + DR-R13 · source deck_engine.md
UNRECOVERED at build-open):
    'DR-R4  DeckSpec_v0 — a frozen contract (it crosses the application
     boundary: the executive app and OS paths both submit it; freeze
     argued on D4b at Stage A, ...'
    (source: canon/drops/20260910/extracted/text/Master_Requirements_Registry.md)

DR-R2 companion (Master Requirements Registry line 267 · full text banked):
    'DR-R2  Determinism is a contract: identical (spec, token version,
     engine version) MUST produce byte-identical output'
    (source: same registry file · used here to justify deck_id as the
    stable-identity key that the byte-identical-output relation is defined
    against.)

Owner R-102 verbatim (banked at STATE/DESK_QUEUE.md DQ-15 · 2026-09-22T~06:50Z):
    'Q2/Q3/Q4 are RESOLVED by this directive — all three objective cards
     (CP-SKILLS-LAYER, CP-DECK-ENGINE, CP-STREAMING-EXTRACTION) are OPENED
     and BUILT in this run, not just drafted.'

This Slice 1 (P4-d-i) lands ONLY the minimum-viable shape-freeze for
DeckSpec_v0 per SO §3.10-α closed-schema discipline (frozen=True +
extra='forbid' from day one):

  * `deck_id` (str · min_length=1) — stable identifier for this deck
    specification. Required because DR-R2 byte-identical-output determinism
    is defined against the (spec, token version, engine version) tuple;
    deck_id is the operational handle for spec identity.

  * `spec_version` (Literal['v0']) — declarative version anchor. Frozen at
    'v0' by this contract; future DeckSpec_v1 lands as a NEW versioned
    contract per Doc-0 R-105 partial-retirement design (never mutation of
    V0).

Slice 2+ deferred behind this Slice 1 (SO §6.4 NOTHING-BEYOND):
  * Full field enumeration post deck_engine.md verbatim restore (currently
    STATEMENT UNRECOVERED · extraction artefact RD-16 · pending canon-source
    restore per DR-R10 + DR-R13 flags on the same registry row group).
  * DR-R1 rendering-service headline pins.
  * DR-R2 determinism-contract drift-detector pins.
  * DR-R5 validation-fail-closed enumerated-error pins.

The shape lands per SO §3.10-α closed-schema discipline:
  * `frozen=True` — every instance is immutable post-construction
    (Pydantic v2 raises ValidationError on attribute assignment).
  * `extra='forbid'` — additional properties are rejected at construction
    time; callers cannot silently widen the frozen contract.
"""
from __future__ import annotations

from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field


# R-102 productized-or-honest-gap Final constant · disk-verifiable posture
# for the missing deck_engine.md verbatim source. Slice 2 extends the
# DeckSpec_v0 field set once this gap is closed.
DR_R4_SOURCE_RESTORE_HONEST_GAP: Final[str] = (
    "DR-R4 source spec 'deck_engine.md' is UNRECOVERED at build-open. "
    "The Master Requirements Registry (Master_Requirements_Registry.md) "
    "carries the DR-R4 line with visible mid-sentence truncation and "
    "flags the same registry row group (DR-R10 and DR-R13) as "
    "'STATEMENT UNRECOVERED — extraction artefact (RD-16)'. Slice 1 "
    "lands the minimum-viable shape-freeze (deck_id + spec_version + "
    "frozen + extra='forbid') that is disk-verifiable against the "
    "truncated DR-R4 line as-received. Full field enumeration for "
    "DeckSpec_v0 awaits verbatim restore of deck_engine.md and is "
    "DEFERRED to CP-DECK-ENGINE Slice 2. This posture is R-102 "
    "productized-or-honest-gap discipline: no synthetic fields are "
    "invented; no canon claim is made beyond the truncated line."
)


class DeckSpec_v0(BaseModel):
    """DR-R4 frozen contract · Slice-1 minimum-viable shape.

    Two fields, both required. Field order matches the SO §2.5
    verbatim-declaration order in the module docstring. Additional
    properties are forbidden; the shape is a frozen tuple, not an
    extensible envelope. Post-construction assignment is refused.

    Slice 2 will extend this set once deck_engine.md is verbatim-restored;
    the extension itself will be an ADDITIVE Optional-field expansion so
    the Slice-1 snapshot remains a valid subset (SO §3.8 additive-only
    discipline). If the extension requires REQUIRED fields not present
    here, a NEW versioned contract DeckSpec_v1 will be provisioned per
    R-105 partial-retirement design.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    deck_id: str = Field(
        ...,
        min_length=1,
        description=(
            "Stable identifier for this deck specification. Required for "
            "DR-R2 byte-identical-output determinism identity (the "
            "(spec, token version, engine version) tuple) and DR-R12 "
            "metering cost-ledger keying by {deck_id}."
        ),
    )
    spec_version: Literal["v0"] = Field(
        ...,
        description=(
            "Declarative contract-version anchor. Frozen at 'v0' by this "
            "contract; future DeckSpec_v1 lands as a NEW versioned "
            "contract per Doc-0 R-105 partial-retirement design (never "
            "mutation of V0)."
        ),
    )
