"""Deck Rendering Engine v1.0 · DR-R4 — the content-only deck contract, full shape (M6.1 · 2026-09-30).

DR-R4 verbatim (AKKI_OS_Deck_Rendering_Engine_v1, recovered 2026-09-28):
    { register: R1|R2|R3|R4|R5,
      meta: { title, audience_line, date, rights_posture_ref, sample_deck: bool },
      selection_manifest: { register_why, overrides[] },
      slides: [ { type, kicker, title, plate?: P1..P17, data?, so_what?,
                  figures: [ { value, unit, class: measured|estimated|sample, receipt_refs[] } ],
                  receipt_refs[], notes? } ],
      coverage_and_limits: { covered_basis_ref, limits[]: {reason∈refusal-grammar, statement, closing_condition} },
      appendix: { exhibit_index_auto: true, extra_slides[] } }
    "Content only. No color, font, size, spacing, or position field exists in the spec."

Why `v1`: `contracts/deck_spec_v0.py` (Slice 1) froze a two-field v0 and rules that REQUIRED additions land as a NEW
versioned contract (R-105). DR-R4 names this shape "DeckSpec_v0"; the name drift is recorded for owner ratification in
`notes/m6_execution/M6_READINESS_20260930.md` §3.2. Every model is frozen with extra='forbid', so a style, colour, accent
or position field is unrepresentable (gate_style_unrepresentable is the schema, not a check).
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

Register = Literal["R1", "R2", "R3", "R4", "R5"]
FigureClass = Literal["measured", "estimated", "sample"]
Plate = Literal["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17"]
# Slide-type library: the akki-decks SKILL.md is not in the repository; this set is the DEFAULT (disclosed) until it is ratified.
SlideType = Literal["title", "assertion", "exhibit", "comparison", "big_number", "table", "section", "coverage", "appendix"]
# Refusal grammar for limits[].reason — DEFAULT until the skill's grammar is ratified; mirrors the hold-reason families in use.
LimitReason = Literal["unmeasured", "sampled_only", "coverage_incomplete", "rights_withheld", "blocked_source", "stale", "not_applicable"]


class _Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Figure(_Frozen):
    value: Union[int, float, str, None] = Field(..., description="null only with unmeasured=true on the owning plate data (DR-R6)")
    unit: Optional[str] = None
    class_: FigureClass = Field(..., alias="class", description="Renders as its chip at the figure; required (gate_missing_class_refuses)")
    receipt_refs: List[str] = Field(default_factory=list)
    label: Optional[str] = None
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class Limit(_Frozen):
    reason: LimitReason
    statement: str = Field(..., min_length=1)
    closing_condition: str = Field(..., min_length=1)


class CoverageAndLimits(_Frozen):
    covered_basis_ref: str = Field(..., min_length=1)
    limits: List[Limit] = Field(default_factory=list)


class Override(_Frozen):
    slide_index: Optional[int] = None
    field: Literal["register", "plate"]
    value: str
    why: str = Field(..., min_length=1)


class SelectionManifest(_Frozen):
    register_why: str = Field(..., min_length=1)
    overrides: List[Override] = Field(default_factory=list)


class Meta(_Frozen):
    title: str = Field(..., min_length=1)
    audience_line: str = Field(..., min_length=1)
    date: str = Field(..., min_length=4, description="ISO date of the content, part of the content not the render")
    rights_posture_ref: str = Field(..., min_length=1)
    sample_deck: bool = False


class Slide(_Frozen):
    type: SlideType
    kicker: Optional[str] = None
    title: str = Field(..., min_length=1, description="An assertion, ≤2 lines at register scale (lint, DR-R7)")
    plate: Optional[Plate] = None
    data: Optional[Dict[str, Any]] = Field(default=None, description="Plate-specific schema, validated by the plate registry")
    so_what: Optional[str] = None
    figures: List[Figure] = Field(default_factory=list)
    receipt_refs: List[str] = Field(default_factory=list, description="Exhibit-level receipts; an exhibit with none resolvable refuses")
    notes: Optional[str] = None


class Appendix(_Frozen):
    exhibit_index_auto: bool = True
    extra_slides: List[Slide] = Field(default_factory=list)


class DeckSpec_v1(_Frozen):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)
    deck_id: str = Field(..., min_length=1)
    spec_version: Literal["v1"]
    register_: Register = Field(..., alias="register", description="canon field `register`; attribute renamed only because pydantic's BaseModel owns `.register`")
    meta: Meta
    selection_manifest: SelectionManifest
    slides: List[Slide] = Field(..., min_length=1)
    coverage_and_limits: CoverageAndLimits
    appendix: Appendix = Field(default_factory=Appendix)
