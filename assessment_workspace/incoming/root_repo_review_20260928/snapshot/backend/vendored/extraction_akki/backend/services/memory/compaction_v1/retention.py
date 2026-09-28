"""services.memory.compaction_v1.retention · MEM-3 deterministic retention engine
+ MEM-2 learned drafting component (structurally separated on the same
module boundary per Canon 8 §W11).

Canon anchors verbatim:
  * MEM-3 (Attribute 10 · A5.5 · Doc 5 objective freeze) · Retention
    is deterministic + versioned + ratified.  Decided by a deterministic
    rule set.  A learned component MAY draft the compacted text; it MUST
    NOT decide what is retained.
  * MEM-R-003..MEM-R-009 · retention rule set v1 keep-rules:
      (a) every crossing/extraction receipt value by reference,
          never paraphrased. [MEM-R-004]
      (b) every fact-class claim by text hash pointer, never rewritten;
          fact MAY be dropped, NEVER altered. [MEM-R-005]
      (c) the frozen objective, floor, and frame reference verbatim.
          [MEM-R-006]
      (d) every refusal and its stated reason. [MEM-R-007]
      (e) every approval decision. [MEM-R-008]
      inference / utterance MAY be summarised under MEM-2.  All other
      classes are pointer-or-drop, never paraphrase. [MEM-R-009]
  * MEM-R-011 · new hash + lineage.
  * TCB (per Spec §4 Table 3): RetentionEngine IN · DraftingComponent OUT.

v1 default behaviour (MEMORY GO order · DEFAULT-class per R-20):
  ALL claims kept — no drops, no summarisation.  The DraftingComponent
  is present as an interface point for future rule sets but is NOT
  called from the v1 default path.  loss_statement counts all zero.
"""
from __future__ import annotations

from services.memory.compaction_v1.carriers import (
    _ALLOWED_CLASSES,
    Claim,
    ClassAnchor,
    RetentionRuleSetVersion,
    RunScopedContext,
)


class RetentionEngine:
    """MEM-3 · deterministic retention engine.

    Applies rule set version 'v1' per MEM-R-004..MEM-R-009 (recommended
    defaults DEFAULT-class per owner MEMORY GO ruling).  Returns a
    partition of the input claims into (retained, dropped) via the
    deterministic decide() call.

    TCB inclusion: IN (MEM-3 · Spec §4 Table 3).  This module MUST NOT
    import any learned/model-client surface (Canon 4 §22 rung-1
    determinism · MEM-R-048 grep-negative surface).
    """

    __slots__ = ("_rule_set_version",)

    def __init__(self, *, rule_set_version: RetentionRuleSetVersion) -> None:
        self._rule_set_version = rule_set_version

    @property
    def rule_set_version(self) -> RetentionRuleSetVersion:
        return self._rule_set_version

    def decide(
        self, *, ctx: RunScopedContext
    ) -> tuple[tuple[Claim, ...], tuple[Claim, ...]]:
        """Deterministic keep/drop partition.

        Rule set v1 default (per owner MEMORY GO DEFAULT-class):
          ALL classes kept · no drops · loss_statement all-zero.

        Future rule sets MAY drop inference/utterance under
        MEM-R-009 (pointer-or-drop, never paraphrase for other classes).
        """
        assert self._rule_set_version.version == "v1", (
            f"MEM-R-003 · unknown retention rule set version "
            f"{self._rule_set_version.version!r} (only 'v1' ratified this-cycle)."
        )
        retained = tuple(ctx.claims)
        dropped: tuple[Claim, ...] = ()
        return retained, dropped

    def build_class_anchors(
        self, *, claims: tuple[Claim, ...]
    ) -> tuple[ClassAnchor, ...]:
        """MEM-2 · MEM-R-005 · build pointer-by-hash anchors for retained claims.

        Deterministic: preserves input order.
        """
        return tuple(
            ClassAnchor(
                class_=c.class_,
                provenance_ref=c.provenance_ref,
                text_hash=c.text_hash,
            )
            for c in claims
        )

    def loss_statement_zero(self) -> dict[str, int]:
        """MEM-R-014 · loss statement class taxonomy verbatim · all-zero baseline."""
        return {cls: 0 for cls in _ALLOWED_CLASSES}


class DraftingComponent:
    """MEM-2 · learned drafting component.

    TCB inclusion: OUT (Spec §4 Table 3).  This component MAY be used
    to draft the compacted text for inference/utterance classes IF
    MEM-R-009 rule allows summarisation.  It MUST NOT decide what is
    retained (that is the RetentionEngine's role · MEM-3 hard ban).

    v1 default: this component is NOT called from the compact() path
    because rule set v1 keeps ALL classes (no summarisation).  It is
    exposed here as an interface point for future rule sets.

    Determinism inventory: Learned (per determinism_inventory_v1 ·
    Spec §4).  This is the ONLY Learned surface in the compaction
    v1 layer.  All other surfaces are Deterministic (retention
    decision · trigger · receipt · reload).
    """

    def draft_summary(
        self, *, claims: tuple[Claim, ...]
    ) -> str:
        """Draft a summary of inference/utterance claims.

        v1 default: NOT called.  Present as an interface point for
        future rule sets.  Deterministic stub returns a canonical
        empty summary (no learned component invoked in v1).
        """
        # v1 default: no drafting invoked · empty summary · no learned
        # component call · MEM-R-048 grep-negative surface satisfied.
        return ""


__all__: tuple[str, ...] = (
    "RetentionEngine",
    "DraftingComponent",
)
