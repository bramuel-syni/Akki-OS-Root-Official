"""CIFProposal_v0 · SO §6.4 pre-ruling · M16 CIF scope · MILESTONE 7.

Owner Standing Order §6.4 verbatim (banked in STATE/STANDING_ORDERS.md
· Pre-ruling for M16 CIF scope):

    "M16 CIF scope — ruled now, since it moves the number most. CIF is
     built as canon already defines it: a learned ideation faculty
     outside the TCB; every CIF-originated idea passes a deterministic
     acceptance point before affecting anything (BR-9.2, single-
     experiment principle); CIF proposes and never ratifies (AC-18);
     its outputs enter the research loop (A5.22, L-4) and the
     capability register (A20.16, L-5); it has its own halt
     independent of the Targeta run it feeds (DET-1 closed as a MUST-
     DO). Nothing beyond that in M16. If the card needs more, that's
     a fork."

Structural placement (per sealed `services/doc0_attributes/tcb.py`
R-3 ratification 2026-09-09 banking):
- `cif.detection` component_id is classified **OUT** TCB (BR-9.4:
  learned per pattern-matching; may propose only).
- `cif.acceptance_point` component_id is classified **IN** TCB
  (BR-9.2: deterministic single-experiment acceptance point).

Shape (canon-as-written · 6 required fields · closed 2-tuple Literal
on `kind` binding routing to L-5 capability register or L-4 research
loop):

- `proposal_id`     · `^cif_[a-z0-9_-]+$` (namespace-isolated from
                      whitepaper `wp_` and skill `sk_` and hand-off
                      `hnd_` prefixes).
- `proposed_at`     · ISO-8601 UTC timestamp of proposal authoring.
- `proposed_by`     · component_id of the OUT-TCB learned faculty
                      that authored the proposal (typically
                      `cif.detection`).
- `kind`            · Literal["capability","research_loop_item"]:
                      closed 2-tuple binding L-5 (capability register
                      · A20.16) or L-4 (research loop · A5.22).
- `payload`         · opaque JSON-serialised string content of the
                      proposal (data-in surface per DAP-7 Option-D
                      bytes-in structural pattern · the OUT-TCB
                      faculty holds NO signing capability; what
                      crosses is inert data).
- `citations`       · closed tuple of str evidence-cites backing the
                      proposal (canon anchors, ledger row ids, etc.).

Same-commit DoD:
  * `ConfigDict(extra="forbid", frozen=True)` — shape drift
    protection + immutability post-construction (AC-18: proposals are
    intent-in-record only; the decision surface lives at W3
    acceptance_point).
  * The shape-snapshot sha256 is pinned in
    `tests/invariants/test_m16_w1_cif_proposal_shape_freeze.py` and
    breaks on any refactor until a ceremony re-pins it.

Non-goals (SO §6.4 "NOTHING beyond" clause):
  * NO ratification-adjacent field (no `ratified_at`, no `decided_by`,
    no `accepted`, no `admitted`).  AC-18 is preserved at the shape
    level.
  * NO write surface in this module.  Persistence is a downstream W4
    concern; the acceptance decision is a W3 concern.
  * NO reference to Targeta or the DET-1 halt.  That is a W5 concern.

Canon anchors: SO §6.4 pre-ruling verbatim + BR-9.2 (Doc-9 single-
experiment acceptance point) + BR-9.4 (Doc-9 detection may propose;
only deterministic acceptance point acts) + AC-18 (proposes-never-
ratifies) + A5.22 (L-4 research loop) + A20.16 (L-5 capability
register) + SO §3.8 (thin-kernel additive-only) + SO §3.10-α
(closed-schema discipline).
"""
from __future__ import annotations

from typing import Literal, Tuple

from pydantic import BaseModel, ConfigDict, Field


CIF_PROPOSAL_KINDS: Tuple[str, str] = ("capability", "research_loop_item")


class CIFProposal_v0(BaseModel):
    """SO §6.4 canon-as-written proposal shape · closed 6-field tuple.

    Every CIF-originated idea authored by the OUT-TCB learned
    detection faculty (BR-9.4) is expressed as one of these records.
    The record itself does not act: it carries intent-in-record only.
    The deterministic acceptance point (BR-9.2 · IN TCB · authored at
    W3) is the single surface that decides whether an accepted
    proposal routes to L-5 (capability register) or L-4 (research
    loop) at W4.  AC-18 is preserved at the shape level: no
    ratification-adjacent field exists.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    proposal_id: str = Field(
        ...,
        pattern=r"^cif_[a-z0-9_-]+$",
        description="Namespace-isolated proposal identifier · `^cif_[a-z0-9_-]+$`.",
    )
    proposed_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of proposal authoring.",
    )
    proposed_by: str = Field(
        ...,
        min_length=1,
        description=(
            "component_id of the OUT-TCB learned faculty that "
            "authored this proposal (typically `cif.detection`)."
        ),
    )
    kind: Literal["capability", "research_loop_item"] = Field(
        ...,
        description=(
            "SO §6.4 routing binding · closed 2-tuple Literal · "
            "`capability` → L-5 A20.16 · `research_loop_item` → L-4 A5.22."
        ),
    )
    payload: str = Field(
        ...,
        min_length=1,
        description=(
            "Opaque JSON-serialised content of the proposal · data-in "
            "surface per DAP-7 Option-D structural bytes-in pattern."
        ),
    )
    citations: Tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Closed tuple of evidence-cite strings backing the "
            "proposal (canon anchors, ledger row ids, etc.)."
        ),
    )


__all__ = ["CIFProposal_v0", "CIF_PROPOSAL_KINDS"]
