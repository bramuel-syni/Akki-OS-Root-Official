#!/usr/bin/env python3
"""Apply Build-Order-01 corrections + fixture-cleared rewrites to notes/*.

Scope:
1. Flip every FIXTURE PENDING variant to FIXTURE CLEARED @ transcription grade
   with a BAC citation and (where applicable) the test_four_questions_topline_present
   invariant marker.
2. Fix all "Canon 5 §10 (four consoles)" citations to "five consoles" per
   Build Order 01 §1.
3. Fix row_to_item_index.md WS-BUILD-CONSOLES row.
4. Fix strategy_items_part2.md Watch-Console line to "five consoles ... Watch as fifth".

Idempotent: re-running produces identical output.
Throwaway analysis tool under tools/ — no production code.
"""
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
NOTES = WORKSPACE / "notes"
TOOL = WORKSPACE / "tools" / "assemble_build_strategy.py"

# Fixture-cleared variants — order matters (longer patterns first).
FIXTURE_REWRITES = [
    (
        "FIXTURE PENDING: reference screenshot for tile-grid-plus-detail-card grammar",
        "FIXTURE CLEARED @ transcription grade — see `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13); `test_four_questions_topline_present` added to new-invariants list per Build Order 01 §3",
    ),
    (
        "FIXTURE PENDING: reference screenshot` field",
        "FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` cited; `test_four_questions_topline_present` on new-invariants list` field",
    ),
    (
        "FIXTURE PENDING: reference screenshot",
        "FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md`; `test_four_questions_topline_present` on new-invariants list",
    ),
    (
        "FIXTURE PENDING + rendering decision pending.",
        "FIXTURE CLEARED @ transcription grade (BAC applied); rendering decision resolved per FL-P1-10 (Build Order 01 §2.C — Use-Data landing homes to the Ask reference application).",
    ),
    (
        "FIXTURE PENDING + FL-OQ-05 pending.",
        "FIXTURE CLEARED @ transcription grade (BAC applied); Studio deferred per FL-OQ-05 (Build Order 01 §4 amendment — leaves Wave 8).",
    ),
    (
        "FIXTURE PENDING` (FL-P1-14).",
        "FIXTURE CLEARED @ transcription grade (FL-P1-14 — transcription-cleared vs file-cleared distinction recorded).",
    ),
    (
        "FIXTURE PENDING.",
        "FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.",
    ),
]

# Canon-5-count corrections.
CANON_5_REWRITES = [
    (
        "Canon 5 §10 (four consoles + Watch as fourth group per Instruction 02)",
        "Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED; Watch as fifth, rendered as fourth Admin-surface tile group per Instruction 02)",
    ),
    (
        "Canon 5 §10 (four consoles hosted)",
        "Canon 5 §10 (five consoles hosted per Build Order 01 §1 correction — FL-OQ-04 CLOSED)",
    ),
    (
        "Canon 5 §10 (four consoles)",
        "Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED)",
    ),
    (
        "WS-BUILD-CONSOLES — four consoles as named surfaces (Canon 5 §10; note: FOUR, not five — Ruling-1 verification carried in fidelity ledger OQ#4)",
        "WS-BUILD-CONSOLES — five consoles as named surfaces per Canon 5 §10 (FL-OQ-04 CLOSED by Build Order 01 §1: five, with Watch as the fifth rendered as fourth Admin-surface tile group per Instruction 02)",
    ),
]

# Assembly-tool preface fixes (XL count, stale ledger sentence, stale push sentence).
ASSEMBLY_REWRITES = [
    (
        "**XL item roster (9 items):**",
        "**XL item roster (7 items — Build Order 01 §1 correction; the count was mis-stated as nine):**",
    ),
    (
        "Frozen at BUILD_STRATEGY.md assembly per Ruling 2 §4. Any post-assembly change requires a Canon 3 §24 rule-change ceremony. 27 open items — each phrased so the owner answers in one sentence.",
        "Frozen at BUILD_STRATEGY.md assembly per Ruling 2 §4. All 27 rows CLOSED by Build Order 01 (2026-08-14). Ledger retained as the honest history of the drafting process; any re-opening requires a Canon 3 §24 rule-change ceremony against this document.",
    ),
    (
        "**Assembly complete. Working papers on disk in `notes/`. STATE/ live. Local commit issued. Push waits on owner's remote + token.**",
        "**Assembly complete. Working papers on disk in `notes/`. STATE/ live. Local commits are the record (Owner Clarification 1, 2026-08-14 — no push).**",
    ),
]

def apply(path, rewrites):
    txt = path.read_text()
    for old, new in rewrites:
        txt = txt.replace(old, new)
    path.write_text(txt)

# Apply to notes files.
for name in ("strategy_items_part1.md", "strategy_items_part2.md", "strategy_sections.md"):
    p = NOTES / name
    apply(p, FIXTURE_REWRITES + CANON_5_REWRITES)

# row_to_item_index.md gets Canon-5 fixes only.
apply(NOTES / "row_to_item_index.md", CANON_5_REWRITES)

# Assembly tool preface fixes.
apply(TOOL, CANON_5_REWRITES + ASSEMBLY_REWRITES)

print("Corrections applied. Verify with grep.")
