"""contracts/solva_reasoning.py — W-SOLVA-V2-LIFT contracts.

Standalone reasoning component (owner directive 2026-09-13: NOT a
sub-component of Registry or DAP).  All contracts grounded first-hand
in canon opened this session; donor executive-domain content is
declared HALTED (DPO-S1 refusal categories, DPO-S2 LOCKED_QUESTIONS)
and not present as active code.

Canon anchors (first-hand):
  * Canon-4 §19  — Solva judges reasoning soundness and preservation.
  * Canon-4 §22  — 'Solva chooses the units; it does not choose what
                   those units imply.'  Load-bearing return is refs-only.
  * Canon-4 §23  — Three assertion classes: fact · utterance · non_factual.
  * Canon-4 §23.1 — Parameterless class-computation signature is the guard.
  * Canon-4 §24  — Three refusal actions: accept_as_stated · narrow_objective
                   · lower_standard.  Nothing else.
  * Canon-4 §26  — Trace exists from the first commit.
  * Canon-4 §21.1 — Intent audit: declared vs demonstrated situation class.
  * Canon-7 §44  — Critic Seam: findings classed, cited, never blocking,
                   never editing.
  * Canon-7 §44.1 — Critic reads artefact + canon + authorising + rubric,
                   NEVER the author's rationale (blind-spot rule).
  * Doc-0 §BR-2.1 — Two-faculty seam is enforced by IMPORT ASSERTION,
                   not coding convention.

R-C2 marker: SolvaTrace.au_3b_defensible defaults to False until
Doc-0 G-8 closes; test asserts silent flip is forbidden.

Extension discipline (Canon-1 §4.6): does NOT sibling
contracts/asset_registry.py or contracts/mtafiti_registry.py — this
file is a reasoning-plane peer, orthogonal to the registry plane.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator


# --- Canon-4 §23 · closed enum -------------------------------------
class AssertionClass(str, Enum):
    FACT = "fact"
    UTTERANCE = "utterance"
    NON_FACTUAL = "non_factual"


# --- Canon-4 §22 · unit reference (opaque handle, no class field) --
class UnitRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    unit_id: str = Field(..., description="Opaque handle to a governed unit.")


class LoadBearingSet(BaseModel):
    """Canon-4 §22: 'Solva chooses the units; it does not choose what
    those units imply.'  The set carries UnitRef objects — refs only,
    no class information."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    units: Tuple[UnitRef, ...] = Field(default_factory=tuple)


# --- Canon-4 §24 · three-action refusal envelope -------------------
class RefusalAction(str, Enum):
    ACCEPT_AS_STATED = "accept_as_stated"
    NARROW_OBJECTIVE = "narrow_objective"
    LOWER_STANDARD = "lower_standard"


class RefusalEnvelope(BaseModel):
    """Canon-4 §24 verbatim (paraphrase-anchored): 'Offering anything
    else would be offering something the system cannot actually deliver.'"""

    model_config = ConfigDict(extra="forbid")

    reason_class: AssertionClass = Field(..., description="The class the request landed at.")
    actions_offered: List[RefusalAction] = Field(
        ...,
        description="Exactly the three canon actions — no fourth is representable.",
    )

    @field_validator("actions_offered")
    @classmethod
    def _validate_actions(cls, v: List[RefusalAction]) -> List[RefusalAction]:
        # The list must be a subset of the three-action set (enforced
        # by the enum type) AND may not contain duplicates.
        seen = set()
        for a in v:
            if a in seen:
                raise ValueError(f"Duplicate refusal action offered: {a}")
            seen.add(a)
        return v


# --- Canon-4 §26 · trace from first commit -------------------------
class SolvaTrace(BaseModel):
    """Canon-4 §26 verbatim: 'It is the auditability that justifies
    letting a component reason at all, and it exists from the first
    commit.'"""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(...)
    reasoning_path: Tuple[str, ...] = Field(..., description="Engine steps traversed.")
    load_bearing_units: Tuple[UnitRef, ...] = Field(...)
    computed_class: AssertionClass = Field(...)
    conclusion: str = Field(..., description="The conclusion as it stands, class-annotated.")
    au_3b_defensible: bool = Field(
        default=False,
        description=(
            "R-C2 marker: timestamp not defensible under AU-3(b) until "
            "Doc-0 G-8 closes.  Silent flip forbidden by invariant."
        ),
    )


# --- Canon-4 §21.1 · intent audit --------------------------------
class IntentAuditRecord(BaseModel):
    """Canon-4 §21.1: opens with declared situation class; demonstrated
    observations appended as the session unfolds."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str = Field(...)
    declared_situation_class: str = Field(..., description="What the actor named at open.")
    demonstrated_observations: Tuple[str, ...] = Field(
        default_factory=tuple,
        description="Situation-class observations demonstrated by conduct as the session runs.",
    )


# --- Canon-7 §44 · Critic Seam ----------------------------------
class CriticInvocation(BaseModel):
    """Canon-7 §44.1: 'A critic reading the author's rationale inherits
    the author's frame.'  This shape carries ONLY {artefact, canon,
    authorising_instrument, rubric}.  No author_rationale field — its
    absence is the blind-spot-sharing prevention."""

    model_config = ConfigDict(extra="forbid")

    artefact: str = Field(..., description="The artefact under critique — the WHAT, not the WHY.")
    canon: str = Field(..., description="Canon reference(s) the critique reads against.")
    authorising_instrument: str = Field(..., description="Id of the run/authorising ceremony.")
    rubric: str = Field(..., description="The specific critique question.")


class CriticFindings(BaseModel):
    """Canon-7 §44: 'findings: classed, cited, never blocking, never
    editing.'  This shape carries findings and citations only."""

    model_config = ConfigDict(extra="forbid")

    findings: Tuple[str, ...] = Field(default_factory=tuple)
    citations: Tuple[str, ...] = Field(default_factory=tuple)
    # No 'blocks' / 'edits' / 'override' fields — their absence is the invariant.
