"""services.canon_doc5_northena.northena_b5_ledger · Family B Part B · B5.1..B5.5.

Registers `Final[...]` load-bearing vocabulary for B5.1..B5.5 (Doc 5 · M10
Northena · Ledger append-only writer · Promise #18 direction half "Objective
Preservation (Direction Half)" · CANON) as authored in the v5 Master
Requirements Registry · System Rules Registry sheet · rows 75..79 (sha-pinned
custody workbook sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

The rule text is extracted verbatim from the source `.docx` at
`fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx`
(sha256 `f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc`).
The v5 SRR "Source (file:line)" column cites `.md:LINE-N` for each row; the
extension differs (`.docx` on disk vs `.md` cited) but the filename byte-matches
otherwise. Per Ruling 3 erratum extended at state commit `afd0f3c7`
(2026-09-21T03:42:00Z) the pointer shape is a HINT and the rule text governs.

For all 5 B5.1..B5.5 rows the SRR "Enforcement Class" column is EMPTY per
Ruling 3 erratum ("class column is a HINT · rule text governs"). Therefore
V7 rows are authored strictly from the rule text.

## Rules registered (Ruling 5 · SRR rows 75..79 verbatim)

- B5.1 · The freeze is atomic; the artifact is immutable for the run (row 75)
- B5.2 · Lawful basis is enforced at Admit, before any extraction (row 76)
- B5.3 · Two admission paths, both freezing the same way (row 77)
- B5.4 · The Ledger writer exposes append only (row 78)
- B5.5 · The stamp-audit side-channel is deliberately permissive (row 79)

## Grep-negative scanner anchors (where rule text states them)

- B5.1 · `scan_for_live_admission_edit` — rule says "A changed intent is
  a new admission, never an edit of a live one".
- B5.2 · `scan_for_downstream_lawful_basis_filter` — rule says "Purpose
  limitation is an admission property, not a downstream filter".
- B5.4 · `scan_for_ledger_update_or_delete` — rule says "No update path
  and no delete path exists within the retention window" and "Out-of-scope
  and refused items are recorded, never silently dropped".
- B5.5 · `scan_for_side_channel_typing_or_mutation` — rule says "Typing it
  would harden it into a mutation surface" and "Unit and audit stay in
  separate envelopes with separate lifecycles, joined by identity rather
  than embedded".

B5.3 asserts a shape invariant (two admission paths · both write Ledger
row · both freeze the same way) rather than negating a specific behavior;
no scanner is registered for it — property tests carry the rule.

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
# Registry-shape · closed vocabulary of Doc 5 Part B B5 CANON rule IDs
# ═══════════════════════════════════════════════════════════════════════════

DOC5_B5_RULE_IDS: Final[tuple[str, ...]] = (
    "B5.1",
    "B5.2",
    "B5.3",
    "B5.4",
    "B5.5",
)
DOC5_B5_RULE_COUNT: Final[int] = 5

DOC5_B5_ROW_SHARED_METADATA: Final[dict[str, str]] = {
    "objective": "O4 Direction, Scope & Focus",
    "promise": "#18 — OBJECTIVE PRESERVATION (Direction Half)",
    "doc": "Doc 5",
    "status": "CANON",
    "domain": "Northena",
    "relationship": "Base canon",
}


# ═══════════════════════════════════════════════════════════════════════════
# B5.1 · The freeze is atomic; the artifact is immutable for the run · SRR row 75
# Rule: "A changed intent is a new admission, never an edit of a live one.
#        The frozen artifact carries type and identity, version, scope set,
#        defensibility floor, done-condition, budget, and lawful basis."
# ═══════════════════════════════════════════════════════════════════════════

B5_1_STATEMENT: Final[str] = (
    "The freeze is atomic; the artifact is immutable for the run"
)
B5_1_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:123"
)
B5_1_FROZEN_ARTIFACT_FIELDS: Final[tuple[str, ...]] = (
    "type_and_identity",
    "version",
    "scope_set",
    "defensibility_floor",
    "done_condition",
    "budget",
    "lawful_basis",
)
B5_1_FROZEN_ARTIFACT_FIELD_COUNT: Final[int] = 7
B5_1_INVARIANT_FREEZE_IS_ATOMIC: Final[bool] = True
B5_1_INVARIANT_ARTIFACT_IS_IMMUTABLE_FOR_THE_RUN: Final[bool] = True
B5_1_INVARIANT_CHANGED_INTENT_IS_NEW_ADMISSION_NEVER_EDIT_OF_LIVE_ONE: Final[bool] = True

LIVE_ADMISSION_EDIT_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "edit_live_admission",
    "mutate_frozen_artifact",
    "update_admitted_artifact",
    "patch_active_admission",
    "modify_run_intent_in_place",
)


def scan_for_live_admission_edit(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors B5.1's grep-negative ban ("A changed intent is a new admission,
    never an edit of a live one").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in LIVE_ADMISSION_EDIT_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# B5.2 · Lawful basis is enforced at Admit, before any extraction · SRR row 76
# Rule: "Purpose limitation is an admission property, not a downstream filter
#        — a run with no lawful basis never starts, so no material is ever
#        touched under an unstated basis. Five deterministic validity checks
#        run in order at Admit, each with its own refusal reason; a failure
#        at any point refuses the admission and writes the reason, and no
#        downstream stage runs."
# ═══════════════════════════════════════════════════════════════════════════

B5_2_STATEMENT: Final[str] = (
    "Lawful basis is enforced at Admit, before any extraction"
)
B5_2_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:125"
)
B5_2_LAWFUL_BASIS_VALIDITY_CHECK_COUNT: Final[int] = 5
B5_2_INVARIANT_PURPOSE_LIMITATION_IS_ADMISSION_PROPERTY_NOT_DOWNSTREAM_FILTER: Final[bool] = True
B5_2_INVARIANT_RUN_WITH_NO_LAWFUL_BASIS_NEVER_STARTS: Final[bool] = True
B5_2_INVARIANT_NO_MATERIAL_TOUCHED_UNDER_UNSTATED_BASIS: Final[bool] = True
B5_2_INVARIANT_CHECKS_RUN_IN_ORDER_AT_ADMIT: Final[bool] = True
B5_2_INVARIANT_EACH_CHECK_HAS_ITS_OWN_REFUSAL_REASON: Final[bool] = True
B5_2_INVARIANT_FAILURE_AT_ANY_CHECK_REFUSES_ADMISSION_AND_WRITES_REASON: Final[bool] = True
B5_2_INVARIANT_NO_DOWNSTREAM_STAGE_RUNS_ON_FAILURE: Final[bool] = True

DOWNSTREAM_LAWFUL_BASIS_FILTER_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "lawful_basis_downstream_filter",
    "basis_check_after_extraction",
    "filter_after_admit_for_basis",
    "post_extraction_basis_gate",
    "basis_check_at_output_stage",
)


def scan_for_downstream_lawful_basis_filter(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors B5.2's grep-negative ban ("Purpose limitation is an admission
    property, not a downstream filter").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in DOWNSTREAM_LAWFUL_BASIS_FILTER_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# B5.3 · Two admission paths, both freezing the same way · SRR row 77
# Rule: "An external request is checked and frozen at Admit having arrived
#        complete; a work order cannot freeze until the shaping conversation
#        completes the objective envelope — the shaping dialogue is where
#        the envelope is filled, Admit is where it is checked and frozen.
#        Both paths write a Ledger row carrying the artifact reference and
#        the lawful-basis reference. (The shaping dialogue for commissioning
#        work — including training work — is specified in Document 12; its
#        output is an envelope Admit freezes.)"
# ═══════════════════════════════════════════════════════════════════════════

B5_3_STATEMENT: Final[str] = "Two admission paths, both freezing the same way"
B5_3_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:127"
)
B5_3_ADMISSION_PATHS: Final[tuple[str, ...]] = ("external_request", "work_order")
B5_3_ADMISSION_PATH_COUNT: Final[int] = 2
B5_3_INVARIANT_BOTH_PATHS_FREEZE_THE_SAME_WAY: Final[bool] = True
B5_3_INVARIANT_EXTERNAL_REQUEST_ARRIVES_COMPLETE: Final[bool] = True
B5_3_INVARIANT_WORK_ORDER_REQUIRES_SHAPING_CONVERSATION_COMPLETE: Final[bool] = True
B5_3_LEDGER_ROW_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "artifact_reference",
    "lawful_basis_reference",
)
B5_3_LEDGER_ROW_REQUIRED_FIELD_COUNT: Final[int] = 2
B5_3_INVARIANT_BOTH_PATHS_WRITE_LEDGER_ROW: Final[bool] = True
B5_3_SHAPING_DIALOGUE_SPEC_DOC: Final[str] = "Document 12"


# ═══════════════════════════════════════════════════════════════════════════
# B5.4 · The Ledger writer exposes append only · SRR row 78
# Rule: "No update path and no delete path exists within the retention
#        window. A correction is a new entry referencing what it corrects.
#        This is enforced as code: the ledger writer exposes append and
#        nothing else, checked by import assertion. Out-of-scope and refused
#        items are recorded, never silently dropped."
# ═══════════════════════════════════════════════════════════════════════════

B5_4_STATEMENT: Final[str] = "The Ledger writer exposes append only"
B5_4_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:129"
)
B5_4_LEDGER_ALLOWED_OPERATIONS: Final[tuple[str, ...]] = ("append",)
B5_4_LEDGER_ALLOWED_OPERATION_COUNT: Final[int] = 1
B5_4_LEDGER_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = ("update", "delete")
B5_4_LEDGER_FORBIDDEN_OPERATION_COUNT: Final[int] = 2
B5_4_INVARIANT_NO_UPDATE_PATH_WITHIN_RETENTION_WINDOW: Final[bool] = True
B5_4_INVARIANT_NO_DELETE_PATH_WITHIN_RETENTION_WINDOW: Final[bool] = True
B5_4_INVARIANT_CORRECTION_IS_NEW_ENTRY_REFERENCING_ORIGINAL: Final[bool] = True
B5_4_INVARIANT_ENFORCED_BY_IMPORT_ASSERTION_CHECK: Final[bool] = True
B5_4_INVARIANT_OUT_OF_SCOPE_AND_REFUSED_ITEMS_RECORDED_NEVER_DROPPED: Final[bool] = True

LEDGER_UPDATE_OR_DELETE_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "ledger_update",
    "ledger_delete",
    "ledger_patch",
    "ledger_remove_entry",
    "ledger_mutate_entry",
    "silently_dropped_refused_item",
)


def scan_for_ledger_update_or_delete(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors B5.4's grep-negative ban ("No update path and no delete path
    exists within the retention window" and "Out-of-scope and refused items
    are recorded, never silently dropped").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in LEDGER_UPDATE_OR_DELETE_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# B5.5 · The stamp-audit side-channel is deliberately permissive · SRR row 79
# Rule: "The Ledger absorbs untyped side-channel entries from other engines
#        — boundary emissions, measurement stamps, trace correlation, gate
#        receipts, refusal envelopes — without mutating the frozen row
#        contract. Typing it would harden it into a mutation surface; the
#        permissiveness is guarded by a snapshot test so the decision cannot
#        be quietly reversed. Unit and audit stay in separate envelopes with
#        separate lifecycles, joined by identity rather than embedded."
# ═══════════════════════════════════════════════════════════════════════════

B5_5_STATEMENT: Final[str] = (
    "The stamp-audit side-channel is deliberately permissive"
)
B5_5_SOURCE_FILE_LINE: Final[str] = (
    "05_Direction_Scope_and_Focus_Part_1_Northena.md:131"
)
B5_5_SIDE_CHANNEL_ENTRY_TYPES: Final[tuple[str, ...]] = (
    "boundary_emissions",
    "measurement_stamps",
    "trace_correlation",
    "gate_receipts",
    "refusal_envelopes",
)
B5_5_SIDE_CHANNEL_ENTRY_TYPE_COUNT: Final[int] = 5
B5_5_INVARIANT_SIDE_CHANNEL_ABSORBS_UNTYPED_WITHOUT_MUTATING_FROZEN_ROW: Final[bool] = True
B5_5_INVARIANT_TYPING_SIDE_CHANNEL_WOULD_HARDEN_INTO_MUTATION_SURFACE: Final[bool] = True
B5_5_INVARIANT_PERMISSIVENESS_GUARDED_BY_SNAPSHOT_TEST: Final[bool] = True
B5_5_INVARIANT_UNIT_AND_AUDIT_STAY_IN_SEPARATE_ENVELOPES_WITH_SEPARATE_LIFECYCLES: Final[bool] = True
B5_5_INVARIANT_UNIT_AND_AUDIT_JOINED_BY_IDENTITY_RATHER_THAN_EMBEDDED: Final[bool] = True

SIDE_CHANNEL_TYPING_OR_MUTATION_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "type_side_channel_entry",
    "typed_stamp_audit_row",
    "mutate_frozen_row_via_side_channel",
    "embedded_audit_in_unit_envelope",
    "merge_audit_into_unit_row",
)


def scan_for_side_channel_typing_or_mutation(
    text: str,
) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors B5.5's grep-negative ban ("Typing it would harden it into a
    mutation surface" and "Unit and audit stay in separate envelopes with
    separate lifecycles, joined by identity rather than embedded").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in SIDE_CHANNEL_TYPING_OR_MUTATION_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)
