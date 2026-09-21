"""services.canon_doc5_northena.northena_a5_vocabulary · Family B Part A · A5.1..A5.6.

Registers `Final[...]` load-bearing vocabulary for A5.1..A5.6 (Doc 5 · M10
Northena · Direction Governor · Promise #16 "Focus maintained under massive
context" · CANON) as authored in the v5 Master Requirements Registry ·
System Rules Registry sheet · rows 64..69 (sha-pinned custody workbook
sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

The rule text is extracted verbatim from the source `.docx` at
`fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx`
(sha256 `f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc`).
The v5 SRR "Source (file:line)" column cites `.md:LINE-N` for each row; the
extension differs (`.docx` on disk vs `.md` cited) but the filename byte-matches
otherwise. Per Ruling 3 erratum extended at state commit `afd0f3c7`
(2026-09-21T03:42:00Z) the pointer shape is a HINT and the rule text governs.

For all 6 A5.1..A5.6 rows the SRR "Enforcement Class" column is EMPTY per
Ruling 3 erratum ("class column is a HINT · rule text governs"). Therefore
V7 rows are authored strictly from the rule text.

## Rules registered (Ruling 5 · SRR rows 64..69 verbatim)

- A5.1 · Deterministic by construction, enforced structurally (row 64)
- A5.2 · The accountability standard (row 65)
- A5.3 · Admit freezes; judgement is borrowed, never performed (row 66)
- A5.4 · Gate is strict set-membership, with no inferential path (row 67)
- A5.5 · Converge owns the halt on fixed conditions (row 68)
- A5.6 · The budget is a hard stop (row 69)

## Grep-negative scanner anchors (where rule text states them)

- A5.1 · `scan_for_northena_ml_import` — rule says "No Northena module
  imports a machine-learning library or a learned component, and an
  import assertion enforcing this runs in continuous integration".
- A5.2 · `scan_for_score_based_admission_rationale` — rule names
  "Admitted because the model scored it highly enough" as the
  unauditable outcome the standard exists to prevent.
- A5.3 · `scan_for_northena_governor_internals_or_inference` — rule
  says "Northena never reads that governor's internals and never
  performs inference itself".
- A5.4 · `scan_for_gate_inferential_path` — rule says "No inferential
  path exists in Gate" and "Ambiguous membership is a compilation
  defect resolved at Admit by the reasoner, never a Gate-time judgement".
- A5.5 · `scan_for_learned_stopping_or_extra_halt_owner` — rule says
  "There is no learned stopping" and "the stop decision and its record
  belong to Northena alone".
- A5.6 · `scan_for_executor_owned_budget_ceiling` — rule says
  "enforced by the governor rather than by the executor that could be
  tempted to keep going".

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
# Registry-shape · closed vocabulary of Doc 5 Part A A5 CANON rule IDs
# ═══════════════════════════════════════════════════════════════════════════

DOC5_A5_RULE_IDS: Final[tuple[str, ...]] = (
    "A5.1",
    "A5.2",
    "A5.3",
    "A5.4",
    "A5.5",
    "A5.6",
)
DOC5_A5_RULE_COUNT: Final[int] = 6

DOC5_A5_ROW_SHARED_METADATA: Final[dict[str, str]] = {
    "objective": "O4 Direction, Scope & Focus",
    "promise": "#16 — FOCUS MAINTAINED UNDER MASSIVE CONTEXT",
    "doc": "Doc 5",
    "status": "CANON",
    "domain": "Northena",
    "relationship": "Base canon",
}


# ═══════════════════════════════════════════════════════════════════════════
# A5.1 · Deterministic by construction, enforced structurally · SRR row 64
# Rule: "No Northena module imports a machine-learning library or a learned
#        component, and an import assertion enforcing this runs in continuous
#        integration. Determinism is checked structurally, not by review."
# ═══════════════════════════════════════════════════════════════════════════

A5_1_STATEMENT: Final[str] = "Deterministic by construction, enforced structurally"
A5_1_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:65"
)
A5_1_INVARIANT_NO_ML_LIBRARY_IMPORT_IN_NORTHENA: Final[bool] = True
A5_1_INVARIANT_IMPORT_ASSERTION_RUNS_IN_CI: Final[bool] = True
A5_1_INVARIANT_DETERMINISM_CHECKED_STRUCTURALLY_NOT_BY_REVIEW: Final[bool] = True

NORTHENA_ML_IMPORT_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "import_sklearn_in_northena",
    "import_torch_in_northena",
    "import_tensorflow_in_northena",
    "import_keras_in_northena",
    "import_xgboost_in_northena",
)


def scan_for_northena_ml_import(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.1's grep-negative ban ("No Northena module imports a
    machine-learning library or a learned component").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in NORTHENA_ML_IMPORT_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.2 · The accountability standard · SRR row 65
# Rule: "Every run must be answerable deterministically: admitted because
#        these fields were valid; gated in because scope membership held;
#        stopped because this condition was met; refused because this rule
#        fired. 'Admitted because the model scored it highly enough' is the
#        unauditable outcome this standard exists to prevent."
# ═══════════════════════════════════════════════════════════════════════════

A5_2_STATEMENT: Final[str] = "The accountability standard"
A5_2_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:67"
)
A5_2_ANSWERABILITY_MODES: Final[tuple[str, ...]] = (
    "admitted",
    "gated_in",
    "stopped",
    "refused",
)
A5_2_MODE_COUNT: Final[int] = 4
A5_2_INVARIANT_EVERY_RUN_ANSWERABLE_DETERMINISTICALLY: Final[bool] = True
A5_2_INVARIANT_SCORE_BASED_ADMISSION_FORBIDDEN: Final[bool] = True

SCORE_BASED_ADMISSION_RATIONALE_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "admitted_because_score",
    "admitted_because_confidence",
    "model_score_gates_admission",
    "score_based_admission",
    "confidence_admits_run",
)


def scan_for_score_based_admission_rationale(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.2's grep-negative ban ("'Admitted because the model scored
    it highly enough' is the unauditable outcome this standard exists to
    prevent").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in SCORE_BASED_ADMISSION_RATIONALE_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.3 · Admit freezes; judgement is borrowed, never performed · SRR row 66
# Rule: "Admit compiles, validates, and freezes. Where compilation genuinely
#        needs judgement — resolving an ambiguous scope, setting a preservation
#        depth or a floor — Admit invokes the depth governor (Solva, Document 4)
#        through an opaque handle and freezes the value it returns. The judgement
#        is the reasoner's; the freeze is Northena's alone. Northena never reads
#        that governor's internals and never performs inference itself."
# ═══════════════════════════════════════════════════════════════════════════

A5_3_STATEMENT: Final[str] = "Admit freezes; judgement is borrowed, never performed"
A5_3_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:69"
)
A5_3_ADMIT_STEPS: Final[tuple[str, ...]] = ("compile", "validate", "freeze")
A5_3_ADMIT_STEP_COUNT: Final[int] = 3
A5_3_JUDGEMENT_HANDLE_TARGET: Final[str] = "Solva (Document 4 · depth governor)"
A5_3_INVARIANT_JUDGEMENT_BORROWED_VIA_OPAQUE_HANDLE: Final[bool] = True
A5_3_INVARIANT_FREEZE_IS_NORTHENA_ALONE: Final[bool] = True
A5_3_INVARIANT_NORTHENA_NEVER_READS_GOVERNOR_INTERNALS: Final[bool] = True
A5_3_INVARIANT_NORTHENA_NEVER_PERFORMS_INFERENCE: Final[bool] = True

NORTHENA_GOVERNOR_INTERNALS_OR_INFERENCE_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "northena_reads_solva_internals",
    "northena_inspects_governor_state",
    "northena_infer",
    "northena_predict",
    "northena_internal_reasoning",
)


def scan_for_northena_governor_internals_or_inference(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.3's grep-negative ban ("Northena never reads that governor's
    internals and never performs inference itself").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in NORTHENA_GOVERNOR_INTERNALS_OR_INFERENCE_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.4 · Gate is strict set-membership, with no inferential path · SRR row 67
# Rule: "Gate tests whether a sub-objective falls within the scope the frozen
#        artifact declares — membership against a defined set, and nothing
#        else. Ambiguous membership is a compilation defect resolved at Admit
#        by the reasoner, never a Gate-time judgement. No inferential path
#        exists in Gate. This is the specific mechanism by which a massive
#        context cannot pull the run off-objective: scope is a frozen set,
#        and adjacency is not membership."
# ═══════════════════════════════════════════════════════════════════════════

A5_4_STATEMENT: Final[str] = "Gate is strict set-membership, with no inferential path"
A5_4_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:71"
)
A5_4_INVARIANT_GATE_IS_STRICT_SET_MEMBERSHIP: Final[bool] = True
A5_4_INVARIANT_NO_INFERENTIAL_PATH_IN_GATE: Final[bool] = True
A5_4_INVARIANT_AMBIGUOUS_MEMBERSHIP_IS_COMPILATION_DEFECT: Final[bool] = True
A5_4_INVARIANT_ADJACENCY_IS_NOT_MEMBERSHIP: Final[bool] = True

GATE_INFERENTIAL_PATH_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "gate_infers_membership",
    "gate_predict_scope",
    "gate_time_judgement",
    "gate_resolves_ambiguity",
    "gate_adjacency_membership",
)


def scan_for_gate_inferential_path(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.4's grep-negative ban ("No inferential path exists in Gate"
    and "Ambiguous membership is a compilation defect resolved at Admit by
    the reasoner, never a Gate-time judgement").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in GATE_INFERENTIAL_PATH_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.5 · Converge owns the halt on fixed conditions · SRR row 68
# Rule: "Converge decides termination on two conditions fixed in the frozen
#        artifact, both threshold checks: done-condition met terminates as
#        success; budget exhausted terminates on budget; neither continues.
#        There is no learned stopping. The depth governor may report it
#        cannot reason further soundly — that report is an input Converge
#        acts on, but the stop decision and its record belong to Northena
#        alone, because a component that could stop a run without Northena
#        recording why would put a termination outside the audit surface
#        entirely."
# ═══════════════════════════════════════════════════════════════════════════

A5_5_STATEMENT: Final[str] = "Converge owns the halt on fixed conditions"
A5_5_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:73"
)
A5_5_HALT_CONDITIONS: Final[tuple[str, ...]] = ("done_condition_met", "budget_exhausted")
A5_5_HALT_CONDITION_COUNT: Final[int] = 2
A5_5_INVARIANT_CONVERGE_OWNS_HALT_DECISION: Final[bool] = True
A5_5_INVARIANT_HALT_CONDITIONS_ARE_THRESHOLD_CHECKS: Final[bool] = True
A5_5_INVARIANT_NO_LEARNED_STOPPING: Final[bool] = True
A5_5_INVARIANT_STOP_RECORD_BELONGS_TO_NORTHENA_ALONE: Final[bool] = True

LEARNED_STOPPING_OR_EXTRA_HALT_OWNER_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "learned_stop",
    "predicted_halt",
    "executor_terminates",
    "worker_halt_without_northena",
    "halt_outside_northena_ledger",
)


def scan_for_learned_stopping_or_extra_halt_owner(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.5's grep-negative ban ("There is no learned stopping" and
    "the stop decision and its record belong to Northena alone").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in LEARNED_STOPPING_OR_EXTRA_HALT_OWNER_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.6 · The budget is a hard stop · SRR row 69
# Rule: "A run halts at its ceiling and nothing past it is billed. This is
#        what makes an open-ended run commissionable at all: exposure is
#        bounded at commit, by a number the commissioner set, enforced by
#        the governor rather than by the executor that could be tempted to
#        keep going."
# ═══════════════════════════════════════════════════════════════════════════

A5_6_STATEMENT: Final[str] = "The budget is a hard stop"
A5_6_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:75"
)
A5_6_INVARIANT_RUN_HALTS_AT_CEILING: Final[bool] = True
A5_6_INVARIANT_NOTHING_PAST_CEILING_IS_BILLED: Final[bool] = True
A5_6_INVARIANT_EXPOSURE_BOUNDED_AT_COMMIT_BY_COMMISSIONER_SET_NUMBER: Final[bool] = True
A5_6_INVARIANT_BUDGET_ENFORCED_BY_GOVERNOR_NOT_EXECUTOR: Final[bool] = True

EXECUTOR_OWNED_BUDGET_CEILING_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "executor_budget_check",
    "worker_budget_ceiling",
    "executor_enforces_budget",
    "executor_stops_at_budget",
    "worker_owned_budget_halt",
)


def scan_for_executor_owned_budget_ceiling(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.6's grep-negative ban ("enforced by the governor rather than
    by the executor that could be tempted to keep going").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in EXECUTOR_OWNED_BUDGET_CEILING_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)
