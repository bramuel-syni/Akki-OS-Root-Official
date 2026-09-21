"""W-CENSUS-CANON-ALIGN · CP-C1 · Contracts · SourceCandidate + Sensitivity.

Canon anchors (verbatim quotes carried in this docstring per the
Verbatim-canon standing rule · DECISIONS.md 2026-09-15T~01:40Z):

Canon-4 §4 (canon/text/Akki_Canon_4_Operating_Engines.txt:26):
    "The census walks the estate exhaustively and objective-blind, producing
     one candidate source record per discovered source. It enumerates and
     classifies; measurement follows separately. Each candidate carries the
     source reference, its region, the feed identity that keys the
     declaration baseline, and a deterministically classified sensitivity."

Master Requirements Registry Doc-9 B5.5 (:148):
    "The defensibility verdict is a deterministic matrix lookup carrying its
     rule reference."

Master Requirements Registry Doc-9 B5.7 (:150):
    "Sensitivity classification is the single entitlement attribute."

Canon-4 §5.1 (line 35):
    "An undeclared feed resolves to unknown, which is the conservative value
     — absence of a declaration never resolves upward."
"""

from __future__ import annotations

from dataclasses import dataclass


# Canon-4 §5.1 verbatim token used when a feed is undeclared.
UNDECLARED_SENSITIVITY_CLASS_LABEL: str = "unknown"


@dataclass(frozen=True)
class Sensitivity:
    """A deterministic sensitivity classification carrying its rule reference.

    * ``class_label`` — the class name from the feed's declaration, or the
      canon-verbatim token ``"unknown"`` when the feed is undeclared.
    * ``is_undeclared`` — True when the class_label is the Canon-4 §5.1
      conservative fallback; False when the class_label comes from a feed
      declaration.
    * ``rule_reference`` — a string naming the rule / declaration source
      that produced this classification (B5.5 verbatim: 'The defensibility
      verdict is a deterministic matrix lookup carrying its rule reference').
    """
    class_label: str
    is_undeclared: bool
    rule_reference: str


@dataclass(frozen=True)
class SourceCandidate:
    """A single candidate source record produced by an objective-blind census
    walk (Canon-4 §4).

    * ``source_reference`` — canonical reference for the source (e.g.
      ``nas://OFFAIRRECS/kbc/2026-08-01/00-00.mp3`` or ``mysql://ussd/farmers``).
    * ``region`` — the region attribute the census walk resolved for this
      source (Canon-4 §4 verbatim).
    * ``feed_identity`` — the feed identity that keys the declaration baseline
      (Canon-4 §4 verbatim · §5.1 declaration-baseline lookup key).
    * ``sensitivity`` — the deterministic sensitivity classification
      (Canon-4 §4 · B5.7 entitlement attribute · B5.5 rule reference carrier).
    """
    source_reference: str
    region: str
    feed_identity: str
    sensitivity: Sensitivity
