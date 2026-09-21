"""services.security_function_policies.sfp_vocabulary · G5-v5 SFP-1..7 first slice.

Registers `Final[...]` load-bearing vocabulary for SFP-1..SFP-7 (Security
Function Policies) as authored in the v5 Master Requirements Registry ·
System Rules Registry sheet · rows 597-603 (sha-pinned custody workbook
sha256 `00072c58…`).

For all 7 SFP rows the SRR "Enforcement Class" column is empty per Ruling 3
erratum ("class column is a HINT · rule text governs"). Therefore V7 rows
are authored strictly from the rule text.

## Rule-text-derived structure per SFP

Each SFP-N row in the SRR contains a pipe-delimited row of the form:

    | <Name> | Subjects: ... Objects: ... Operations: ...
    Rule: <rule text> (<citation>). |

The rule name, subject class, object class, operation tuple, rule text,
and citation are extracted into `Final[...]` constants; additional bool
Finals encode the specific invariants the rule text asserts; grep-negative
scanners are registered where the rule text explicitly negates a
behavior.

## Rules registered (Ruling 5 · SRR rows 597-603 verbatim)

- SFP-1 · Assertion Floor (row 597) · Doc 4 A2 · A5.5.
- SFP-2 · Certainty-to-Evidence Binding (row 598) · Doc 3 A5.2.
- SFP-3 · Acceptance Floor (row 599) · Promise #22 · MOAC.
- SFP-4 · Custody Floor (row 600) · Promise #1 · A5.1-A5.3.
- SFP-5 · Non-Conformance Ceiling (row 601) · Doc 3 A5.7.
- SFP-6 · Release Budget (row 602) · DAP-35.
- SFP-7 · Reproduction Ceiling (row 603) · DAP-31 · A5.15.

## Grep-negative scanner anchors (where rule text states them)

- SFP-1 · `scan_for_unanchorable_softening` — rule says "refused, not weakened"
  (an unanchorable sentence is refused, never softened / weakened to fit).
- SFP-2 · `scan_for_confidence_score_as_severance_input` — rule says "no
  confidence score, however high, is an eligible input".
- SFP-3 · `scan_for_partial_acceptance` — rule says "no partial acceptance".
- SFP-5 · `scan_for_conformance_as_conviction_ground` — rule says loss of
  conformance is "never, by itself, grounds for conviction".

Pure-data-in scanners (no I/O · no exception · no network): each takes a
text blob, returns a tuple of `(line_no, matched_pattern)` hits, empty
tuple when no watched pattern is present. Watch-pattern tuples are
themselves `Final[tuple[str, ...]]` closed-vocabs.

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""

from __future__ import annotations

from typing import Final

# ═══════════════════════════════════════════════════════════════════════════
# Registry-shape · closed vocabulary of SFP rule IDs
# ═══════════════════════════════════════════════════════════════════════════

SFP_RULE_IDS: Final[tuple[str, ...]] = (
    "SFP-1",
    "SFP-2",
    "SFP-3",
    "SFP-4",
    "SFP-5",
    "SFP-6",
    "SFP-7",
)
SFP_RULE_COUNT: Final[int] = 7


# ═══════════════════════════════════════════════════════════════════════════
# SFP-1 · Assertion Floor · SRR row 597
# Rule: "no sentence enters a composed answer without a per-sentence anchor
#        to material; an unanchorable sentence is refused, not weakened."
# ═══════════════════════════════════════════════════════════════════════════

SFP_1_NAME: Final[str] = "Assertion Floor"
SFP_1_SUBJECTS: Final[str] = "any principal requesting a composed answer"
SFP_1_OBJECTS: Final[str] = "the claim being composed"
SFP_1_OPERATIONS: Final[tuple[str, ...]] = ("assert", "compose", "refuse")
SFP_1_RULE: Final[str] = (
    "no sentence enters a composed answer without a per-sentence anchor "
    "to material; an unanchorable sentence is refused, not weakened"
)
SFP_1_CITATION: Final[tuple[str, ...]] = ("Doc 4 A2", "A5.5")

PER_SENTENCE_ANCHOR_REQUIRED_IN_COMPOSED_ANSWER: Final[bool] = True
UNANCHORABLE_SENTENCE_REFUSED_NOT_WEAKENED: Final[bool] = True
SOFTENING_UNANCHORABLE_FORBIDDEN: Final[bool] = True

UNANCHORABLE_SOFTENING_PATTERNS: Final[tuple[str, ...]] = (
    "weaken_when_unanchored",
    "soften_without_anchor",
    "default_when_anchor_missing",
    "hedge_when_no_material",
    "downgrade_confidence_when_unanchored",
)


def scan_for_unanchorable_softening(text: str) -> tuple[tuple[int, str], ...]:
    """Grep-negative pure-data-in scanner for SFP-1 ban.

    Returns tuple of (line_number, matched_pattern) hits when any pattern in
    `UNANCHORABLE_SOFTENING_PATTERNS` occurs as a substring in the text;
    empty tuple otherwise. Line numbers are 1-based.
    """
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in UNANCHORABLE_SOFTENING_PATTERNS:
            if pat in line:
                hits.append((i, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# SFP-2 · Certainty-to-Evidence Binding · SRR row 598
# Rule: "severance unlocks only from the closed six-signal registry; no
#        confidence score, however high, is an eligible input."
# ═══════════════════════════════════════════════════════════════════════════

SFP_2_NAME: Final[str] = "Certainty-to-Evidence Binding"
SFP_2_SUBJECTS: Final[str] = "the Watch's response function (Mkono)"
SFP_2_OBJECTS: Final[str] = "severance authority"
SFP_2_OPERATIONS: Final[tuple[str, ...]] = ("unlock", "withhold")
SFP_2_RULE: Final[str] = (
    "severance unlocks only from the closed six-signal registry; "
    "no confidence score, however high, is an eligible input"
)
SFP_2_CITATION: Final[tuple[str, ...]] = ("Doc 3 A5.2",)

SEVERANCE_REGISTRY_SIGNAL_COUNT: Final[int] = 6
SEVERANCE_UNLOCKS_ONLY_FROM_CLOSED_SIX_SIGNAL_REGISTRY: Final[bool] = True
CONFIDENCE_SCORE_NOT_ELIGIBLE_SEVERANCE_INPUT: Final[bool] = True

CONFIDENCE_SCORE_SEVERANCE_INPUT_PATTERNS: Final[tuple[str, ...]] = (
    "confidence_score_unlocks",
    "unlock_by_confidence",
    "severance_confidence_input",
    "high_confidence_severance",
)


def scan_for_confidence_score_as_severance_input(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Grep-negative pure-data-in scanner for SFP-2 ban.

    Returns tuple of (line_number, matched_pattern) hits when any pattern in
    `CONFIDENCE_SCORE_SEVERANCE_INPUT_PATTERNS` occurs; empty tuple
    otherwise.
    """
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in CONFIDENCE_SCORE_SEVERANCE_INPUT_PATTERNS:
            if pat in line:
                hits.append((i, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# SFP-3 · Acceptance Floor · SRR row 599
# Rule: "every stated criterion satisfied or the run is refused in full;
#        no partial acceptance."
# ═══════════════════════════════════════════════════════════════════════════

SFP_3_NAME: Final[str] = "Acceptance Floor"
SFP_3_SUBJECTS: Final[str] = "any training run"
SFP_3_OBJECTS: Final[str] = "model output"
SFP_3_OPERATIONS: Final[tuple[str, ...]] = ("accept", "refuse")
SFP_3_RULE: Final[str] = (
    "every stated criterion satisfied or the run is refused in full; "
    "no partial acceptance"
)
SFP_3_CITATION: Final[tuple[str, ...]] = ("Promise #22", "MOAC")

ACCEPTANCE_REQUIRES_EVERY_CRITERION_SATISFIED: Final[bool] = True
PARTIAL_ACCEPTANCE_FORBIDDEN: Final[bool] = True
TRAINING_RUN_REFUSED_IN_FULL_ON_ANY_UNSATISFIED_CRITERION: Final[bool] = True

PARTIAL_ACCEPTANCE_PATTERNS: Final[tuple[str, ...]] = (
    "partial_accept",
    "partially_accept",
    "partial_acceptance",
    "accept_some_criteria",
    "accept_with_deficit",
)


def scan_for_partial_acceptance(text: str) -> tuple[tuple[int, str], ...]:
    """Grep-negative pure-data-in scanner for SFP-3 ban.

    Returns tuple of (line_number, matched_pattern) hits when any pattern in
    `PARTIAL_ACCEPTANCE_PATTERNS` occurs; empty tuple otherwise.
    """
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in PARTIAL_ACCEPTANCE_PATTERNS:
            if pat in line:
                hits.append((i, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# SFP-4 · Custody Floor · SRR row 600
# Rule: "no asset crosses without de-identification appropriate to its
#        custody class."
# ═══════════════════════════════════════════════════════════════════════════

SFP_4_NAME: Final[str] = "Custody Floor"
SFP_4_SUBJECTS: Final[str] = "any data crossing the chokepoint"
SFP_4_OBJECTS: Final[str] = "the crossing itself"
SFP_4_OPERATIONS: Final[tuple[str, ...]] = ("cross", "de-identify", "re-identify")
SFP_4_RULE: Final[str] = (
    "no asset crosses without de-identification appropriate to its "
    "custody class"
)
SFP_4_CITATION: Final[tuple[str, ...]] = ("Promise #1", "A5.1-A5.3")

NO_ASSET_CROSSES_CHOKEPOINT_WITHOUT_DEIDENTIFICATION: Final[bool] = True
DEIDENTIFICATION_APPROPRIATE_TO_CUSTODY_CLASS: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# SFP-5 · Non-Conformance Ceiling · SRR row 601
# Rule: "loss of conformance alone returns an actor to baseline verification;
#        it is never, by itself, grounds for conviction."
# ═══════════════════════════════════════════════════════════════════════════

SFP_5_NAME: Final[str] = "Non-Conformance Ceiling"
SFP_5_SUBJECTS: Final[str] = (
    "any actor whose behavioural signature drifts from its declared conduct"
)
SFP_5_OBJECTS: Final[str] = "the actor's trust discount"
SFP_5_OPERATIONS: Final[tuple[str, ...]] = ("reduce", "revoke")
SFP_5_RULE: Final[str] = (
    "loss of conformance alone returns an actor to baseline verification; "
    "it is never, by itself, grounds for conviction"
)
SFP_5_CITATION: Final[tuple[str, ...]] = ("Doc 3 A5.7",)

NON_CONFORMANCE_RETURNS_ACTOR_TO_BASELINE_VERIFICATION: Final[bool] = True
NON_CONFORMANCE_ALONE_IS_NEVER_GROUNDS_FOR_CONVICTION: Final[bool] = True

CONFORMANCE_CONVICTION_PATTERNS: Final[tuple[str, ...]] = (
    "conformance_drift_convicts",
    "conviction_by_conformance_alone",
    "non_conformance_conviction",
    "drift_convicts_actor",
)


def scan_for_conformance_as_conviction_ground(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Grep-negative pure-data-in scanner for SFP-5 ban.

    Returns tuple of (line_number, matched_pattern) hits when any pattern in
    `CONFORMANCE_CONVICTION_PATTERNS` occurs; empty tuple otherwise.
    """
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in CONFORMANCE_CONVICTION_PATTERNS:
            if pat in line:
                hits.append((i, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# SFP-6 · Release Budget · SRR row 602
# Rule: "total release across all parties, operations, and time is bounded;
#        exceeding it is a floor violation, not a negotiable ceiling."
# ═══════════════════════════════════════════════════════════════════════════

SFP_6_NAME: Final[str] = "Release Budget"
SFP_6_SUBJECTS: Final[str] = "all external parties, jointly and severally"
SFP_6_OBJECTS: Final[str] = "the estate's total information release"
SFP_6_OPERATIONS: Final[tuple[str, ...]] = ("release", "refuse")
SFP_6_RULE: Final[str] = (
    "total release across all parties, operations, and time is bounded; "
    "exceeding it is a floor violation, not a negotiable ceiling"
)
SFP_6_CITATION: Final[tuple[str, ...]] = ("DAP-35",)

RELEASE_BUDGET_DIMENSIONS: Final[tuple[str, ...]] = ("parties", "operations", "time")
RELEASE_BUDGET_BOUNDED_ACROSS_PARTIES_OPERATIONS_TIME: Final[bool] = True
RELEASE_EXCESS_IS_FLOOR_VIOLATION_NOT_NEGOTIABLE_CEILING: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# SFP-7 · Reproduction Ceiling · SRR row 603
# Rule: "no artefact or output passes carrying reproduction of a controlled
#        unit above the ruled threshold."
# ═══════════════════════════════════════════════════════════════════════════

SFP_7_NAME: Final[str] = "Reproduction Ceiling"
SFP_7_SUBJECTS: Final[str] = "any artefact or output leaving a component boundary"
SFP_7_OBJECTS: Final[str] = "controlled-unit content"
SFP_7_OPERATIONS: Final[tuple[str, ...]] = ("egress", "refuse")
SFP_7_RULE: Final[str] = (
    "no artefact or output passes carrying reproduction of a controlled "
    "unit above the ruled threshold"
)
SFP_7_CITATION: Final[tuple[str, ...]] = ("DAP-31", "A5.15")

NO_EGRESS_ABOVE_RULED_REPRODUCTION_THRESHOLD: Final[bool] = True
REPRODUCTION_CEILING_IS_HARD_NOT_ADVISORY: Final[bool] = True
