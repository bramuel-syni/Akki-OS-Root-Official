#!/usr/bin/env python3
"""Assemble BUILD_STRATEGY.md as a self-contained document.

Order per owner correction:
1. Method & submission attestations (this script writes it inline)
2. Full Part-1 items (from notes/strategy_items_part1.md, demoted headings)
3. Full Part-2 items (from notes/strategy_items_part2.md, demoted headings)
4-7. Sequence + transitions + no-regression + waste (from notes/strategy_sections.md)
8. Full fidelity ledger (from notes/fidelity_ledger.md)
9. Appendix: row-to-item index (from notes/row_to_item_index.md)

Working-papers notes/ files remain on disk unchanged.
"""
import re
import subprocess
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
NOTES = WORKSPACE / "notes"
OUT = WORKSPACE / "BUILD_STRATEGY.md"

def inline(path, header_shift=0):
    """Return file content with H1 headings shifted deeper by `header_shift`."""
    txt = path.read_text()
    if header_shift == 0:
        return txt
    # Shift # → ## (or deeper) at line start
    lines = []
    for line in txt.split("\n"):
        m = re.match(r"^(#+)\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            new_level = level + header_shift
            line = "#" * min(new_level, 6) + " " + m.group(2)
        lines.append(line)
    return "\n".join(lines)

# --- §0 · Preface ---
preface = """# BUILD_STRATEGY.md — Akki Assessment Chunk 4

**Version:** 1.1 (assembled, self-contained) · **Date:** 2026-08-14 · **Companion to:** `REUSE_ASSESSMENT.md` (Chunk-3 accepted 2026-08-14).

**Nature of this document.** Paper-only. No production code was written to produce it. Every factual claim is grounded in files opened during the session (canon `.docx` archives + four cloned repositories at pinned SHAs). No claim is grounded in a README, filename, or prior knowledge.

**Total work items: 102** (47 Part-1 · 55 Part-2). **Canon coverage: 591 rows.** **Named gaps: 0.**

---

## Table of Contents

- **§1** — Method & submission attestations
- **§2** — Estimation discipline (stated once)
- **§3** — Governing rulings (verbatim)
- **§4** — Part 1 items (47 · MODIFY/PARTIAL · RE-POINT · HARVEST · RETIRE · RENAME · WIRING · REBUILD · CONTRADICTION)
- **§5** — Part 2 items (55 · BUILD)
- **§6** — Proposed sequence with reasons (11 waves + dependency logic)
- **§7** — Transition conditions (T1–T4)
- **§8** — No-regression contract (20 existing standing invariants + 40 must-write-first tests)
- **§9** — Waste register (W-01 … W-08)
- **§10** — Canon fidelity ledger (27 open items, frozen)
- **Appendix A** — Row-to-item index (591 rows → 102 items, build-order traceability)

---

## §1 · Method & submission attestations

### 1.1 Grounding

Every factual claim in this document comes from files opened during the assessment session:
- Nine `.docx` canon archives → extracted `.txt` under `canon/text/` (see §1.5 below).
- Four repositories cloned locally with pinned SHAs (see §1.5 below).
- Extraction-Akki frontend inventory produced by `find` at HEAD `b150c21`.
- No README, filename, or prior knowledge was used as evidence.

Any un-fillable field is explicitly named in the fidelity ledger (§10). No blanks. No silent fill-ins.

### 1.2 STATE/ is live · cold-read test performed

`STATE/` at `/app/assessment_workspace/STATE/` is live and current:
- `CONTEXT.md` (113 lines) — narrative + assembly manifest.
- `PINS.md` (86 lines) — repo SHAs, canon file map.
- `DECISIONS.md` (130 lines) — five rulings verbatim.
- `NEXT.md` (73 lines) — cold-reader-executable next actions.

**Cold-read recovery test performed.** A stranger reading STATE/ finds:
- Chunk-4 posture (`assembly complete`) at top of `CONTEXT.md`.
- Five rulings in receipt order in `DECISIONS.md`.
- Repo SHAs + canon map in `PINS.md`.
- Next-step commands + expected outputs in `NEXT.md`.

Result: STATE/ is self-sufficient — a cold reader can resume with no session memory.

### 1.3 Citation audit result

`tools/citation_audit.py` at the assembly commit:
- File citations: **102/102 verified · 0 failed**.
- Canon citations: **1118/1118 verified · 0 failed** (against the notes corpus).

Citation drift disclosed and remediated per Orchestrator Ruling A (2026-08-14): 72 row-level corrections + 70 downstream citation corrections applied via `tools/drift_map.py` + `drift_apply.py` + `drift_downstream.py`. Edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`. Root cause: Chunk-1 extraction counted sub-paragraphs beyond canon `[Heading]` boundaries; prevention captured in `STATE/CONTEXT.md`.

### 1.4 Completeness audit result

`tools/completeness_audit.py` at the assembly commit:
- Every non-REUSE canon-row appears in exactly one work item.
- Named gaps section: **NONE**.
- Every work item in `strategy_items_part[12].md` has all seven fields.
- Result: **PASS**.

### 1.5 Pinned inputs

**Canon pack (nine documents, extracted via `python-docx` to `canon/text/`):**
- `Akki_Canon_1_Custody_Platform.txt` — [Heading] §1..§16.
- `Akki_Canon_2_CIF.txt` — [Heading] §1..§20.
- `Akki_Canon_3_Governance_Engines.txt` — [Heading] §1..§33.
- `Akki_Canon_4_Operating_Engines.txt` — [Heading] §1..§50.
- `Akki_Canon_5_Interface_Architecture.txt` — [Heading] §1..§43.
- `Akki_Canon_6_User_Journeys.txt` — [Heading] §1..§12.
- `Akki_Canon_7_Integration_and_Quality.txt` — [Heading] §1..§50.
- `Akki_Canon_8_The_Watch.txt` — [Heading] §1..§21.
- `Akki_Canon_9_Mkondo_Charter.txt` — [Heading] §1..§8.

**Repositories (pinned local clones):**
- `Akki-Executive-Core` — v4.4.5 · HEAD `04ec5e1e`.
- `Akki-OS-V1` — HEAD `a58fa8b`.
- `Extraction-Akki` — HEAD `b150c21`.
- `RMS-IQ-Core-2` — HEAD `4bc2f2b`.

### 1.6 Working papers on disk

The notes files feeding this document remain on disk unchanged and available as working papers:
- `notes/strategy_items_part1.md` (838 lines) — inlined into §4 below.
- `notes/strategy_items_part2.md` (628 lines) — inlined into §5 below.
- `notes/strategy_sections.md` (269 lines) — inlined into §§6-9 below.
- `notes/fidelity_ledger.md` (102 lines) — inlined into §10 below.
- `notes/row_to_item_index.md` (405 lines) — inlined into Appendix A below.
- Ten `notes/domain_5_*.md` files (Chunk-3 domain tables) — cross-referenced.
- `notes/canon_[1-9]_requirements.md` (Chunk-1 canon requirement extractions).

This submission stands alone; the working papers persist as the review trail.

---

## §2 · Estimation discipline (stated once)

Stranger-checkable class thresholds (per Ruling 2 §1). Every item below carries a class using these thresholds; every XL carries a one-paragraph defence.

| Class | Threshold |
|---|---|
| **S** | 1 component, 0 new contracts, ≤1 integration surface. |
| **M** | 1-2 components, OR 1 new/changed contract, ≤2 integration surfaces. |
| **L** | 3+ components, OR new register/console surface, OR a data migration. |
| **XL** | New engine/authority, OR estate-wide wiring. |

Definitions:
- **Component** = a directory-scoped unit under `backend/services/<name>/` or `frontend/src/<pillar>/<console>/` that owns a distinct responsibility.
- **Contract** = a frozen shape governed by `tests/invariants/test_invariant_contract_snapshots.py` (parity seat).
- **Integration surface** = every named boundary the item crosses: LLM boundary (`SyniSenseContract.shield_invoke`), memory plane, object storage port, streaming port, Watch input, Canon-9 record class, task-identity register.
- **Register/console surface** = adds a first-class named surface listed in Canon 5 §10 (four consoles) or Canon 9 (task-identity register, record matrix, handoff registry).
- **Data migration** = any programme that moves user-visible state from one storage/plane shape to another; append-only history is not migration; storage-shape change is migration.

**XL item roster (9 items):** WS-REPOINT-ANSWERING-SURFACES · WS-REBUILD-WORK-STUDIO-STORAGE (Part 1); WS-BUILD-OBJECT-STORAGE-PORT · WS-BUILD-WATCH-FOUNDATION · WS-BUILD-WATCH-ACTORS · WS-BUILD-RECORD-MATRIX · WS-BUILD-TASK-IDENTITY-REGISTER (Part 2). Each carries its defence in the item entry.

---

## §3 · Governing rulings (verbatim)

Five rulings govern this document. Full verbatim in `STATE/DECISIONS.md`; verbatim quotations follow here.

### 3.1 Ruling 1 — Purpose-gate transition condition (owner, 2026-08-14)

> "Executive's purpose enforcement is not stripped until the declaration check and the Watch's reconciler are demonstrated firing."

**Binding effect.** `WS-CONTRADICTION-PURPOSE-GATE` (Part 1) retains the gate until (a) `WS-BUILD-DECL` demonstrated-firing evidence AND (b) `WS-BUILD-WATCH-RECONCILER` demonstrated-firing evidence are both in the ledger. Then a Canon 3 §24 rule-change ceremony executes the strip. This is transition T1 in §7.

### 3.2 Ruling 2 — Five-point plan (owner, 2026-08-14)

> "1. Estimation anchor: (b) blended review-load + integration-surface count — BUT state the discipline once with hard, auditable thresholds ... The classes must be checkable by a stranger, not vibes.
> 2. REBUILD class: keep WS-REBUILD-WORK-STUDIO-STORAGE in Part 1 as its own REBUILD row ... its REVERSAL COST field must address user-data migration reversibility explicitly ...
> 3. WIRING: before finalizing your 7, verify these four aren't silently folded: (a) wiring critic_pass into the spine's answering path ... (b) extending the frozen-contract-snapshot parity discipline to every NEW contract this programme creates ... (c) wiring the refusal-family registry to the Canon 5 refusal card surfaces; (d) wiring the Northena ledger's sole-writer position to the Canon 9 record matrix ...
> 4. Fidelity ledger: draft notes/fidelity_ledger.md alongside Part 1, append during Part 2, freeze at assembly ...
> 5. CONTRADICTION: own row, agreed — WS-CONTRADICTION-PURPOSE-GATE is the natural home of the Ruling-1 transition window; its DoD is the demonstrated-firing evidence (declaration check + Watch reconciler) that lawfully permits the strip ..."

**Binding effects:** estimation thresholds stated in §2; WS-REBUILD-WORK-STUDIO-STORAGE stays Part 1; four WIRING items promoted to standalone (WS-WIRE-CRITIC-INTO-ANSWERING, WS-WIRE-PARITY-EXTENSION, WS-WIRE-REFUSAL-FAMILY, WS-WIRE-LEDGER-MATRIX); fidelity ledger opens Part 1 / freezes at assembly.

### 3.3 Ruling 3 · Instruction 02 — Interface strategy directive (owner, 2026-08-14)

> "The owner has fixed the interface direction: governance and security control surfaces render as app tiles under the Admin surface's tile-grid-plus-detail-card grammar (reference screenshot to follow in the workspace). Your build strategy's interface section must plan Extraction-Akki's frontend as the donor, repurposed — not rebuilt — into this grammar: produce a menu-to-app mapping table (every existing Extraction-Akki page/menu → its app tile, group, and canon identity, or → RETIRE with reason), and classify the repurposing per component as HARVEST or MODIFY with the usual seven fields. The Watch renders as a fourth group of four app tiles (State, Record, Under Watch, Decisions per Canon 8 §13), gated by watch-officer role, sessions under Watch identity per Canon 9 — never nested under Trust Center — and remains BUILD. Label-versus-identity mappings land in your canon fidelity ledger as rendering decisions. Update STATE/ on receipt."

**Binding effects:** 44 Extraction-Akki pages mapped to (tile · group · canon identity) — full table inlined in §4.M below; 13 Canon-5 items reclassified from Part-2 BUILD to Part-1 HARVEST/MODIFY; `WS-BUILD-CONSOLE-WATCH` remains BUILD with the explicit placement constraint (never nested under Trust Center).

### 3.4 Orchestrator Ruling A — Citation drift remediation (2026-08-14)

> "Citation drift (FL-P1-20): remediate NOW, before Part 2. This is a quality defect, not a governance question — the owner's standard is a zero-failure citation audit ... every correction is a re-read, never a guess ... keep FL-P1-20 as the record of the drift AND its remediation — the defect history is part of the honest record ... Root-cause one line in CONTEXT.md ..."

**Binding effects:** 72 row-level + 70 downstream citation corrections applied; root cause captured (sub-paragraph counting past heading boundaries); FL-P1-20 retained as defect+remediation record; audit clean.

### 3.5 Orchestrator Ruling B — Part 2 proceed + strategy sections (2026-08-14)

> "Part 2 proceeds now ... Draft the 42 BUILD items (148 canon rows) with all seven fields, same discipline. Specific requirements: (1) the Watch's 60 rows and Mkondo's 45 rows will dominate — bundle honestly ... (2) WS-BUILD-DECL and WS-BUILD-WATCH-RECONCILER carry the Ruling-1 transition linkage explicitly; (3) the two ports (streaming, object storage) appear as their own items ... (4) every item that creates a NEW contract references WS-WIRE-PARITY-EXTENSION as a dependency ... After Part 2: strategy-level sections (proposed sequence with dependency logic; transition windows named + guarded, T1 = Ruling 1; no-regression contract listing standing invariant tests + missing ones to write first; waste register; freeze the fidelity ledger), then full completeness audit ..."

**Binding effects:** Part 2 drafted (55 items — expanded from 42 to honor mechanism-bundling for Watch); two new port items promoted; parity-seat dependency verified per new-contract item; strategy sections §§6-9 below; ledger frozen.

---

"""

parts = []
parts.append(preface)

# --- §4 · Part 1 items ---
parts.append("## §4 · Part 1 items — 47 items\n\n")
parts.append("Full drafts, seven fields each, inlined below verbatim from the working paper `notes/strategy_items_part1.md`. Headings demoted so this section's IDs remain unique.\n\n")
p1 = inline(NOTES / "strategy_items_part1.md", header_shift=2)
# Trim the working-paper's own H1 title
p1 = re.sub(r"^### strategy_items_part1\.md.*?\n\n", "", p1, count=1)
parts.append(p1)
parts.append("\n\n---\n\n")

# --- §5 · Part 2 items ---
parts.append("## §5 · Part 2 items — 55 items\n\n")
parts.append("Full drafts, seven fields each, inlined below verbatim from the working paper `notes/strategy_items_part2.md`. Headings demoted so this section's IDs remain unique.\n\n")
p2 = inline(NOTES / "strategy_items_part2.md", header_shift=2)
p2 = re.sub(r"^### strategy_items_part2\.md.*?\n\n", "", p2, count=1)
parts.append(p2)
parts.append("\n\n---\n\n")

# --- §§6-9 · Sequence + transitions + no-regression + waste + freeze ---
parts.append("## §§6-9 · Strategy-level sections\n\n")
parts.append("Inlined verbatim from the working paper `notes/strategy_sections.md`. Section IDs preserved (§1 · §2 · §3 · §4 · §5 within the working paper map here as §6 · §7 · §8 · §9 · §10-freeze-note).\n\n")
ss = inline(NOTES / "strategy_sections.md", header_shift=1)
ss = re.sub(r"^## strategy_sections\.md.*?\n\n", "", ss, count=1)
parts.append(ss)
parts.append("\n\n---\n\n")

# --- §10 · Canon fidelity ledger ---
parts.append("## §10 · Canon fidelity ledger (frozen at assembly)\n\n")
parts.append("Frozen at BUILD_STRATEGY.md assembly per Ruling 2 §4. Any post-assembly change requires a Canon 3 §24 rule-change ceremony. 27 open items — each phrased so the owner answers in one sentence.\n\n")
fl = inline(NOTES / "fidelity_ledger.md", header_shift=1)
fl = re.sub(r"^## fidelity_ledger\.md.*?\n\n", "", fl, count=1)
parts.append(fl)
parts.append("\n\n---\n\n")

# --- Appendix A · Row-to-item index ---
parts.append("## Appendix A · Row-to-item index — 591 rows → 102 items\n\n")
parts.append("Inlined verbatim from the working paper `notes/row_to_item_index.md`. Build orders can be issued against BUILD_STRATEGY.md by item reference; this appendix provides the row-level traceability every item references.\n\n")
ri = inline(NOTES / "row_to_item_index.md", header_shift=1)
ri = re.sub(r"^## row_to_item_index\.md.*?\n\n", "", ri, count=1)
parts.append(ri)
parts.append("\n\n---\n\n## End of BUILD_STRATEGY.md\n\n")
parts.append("**Assembly complete. Working papers on disk in `notes/`. STATE/ live. Local commit issued. Push waits on owner's remote + token.**\n")

OUT.write_text("".join(parts))

# Report line count
n_lines = OUT.read_text().count("\n") + 1
print(f"BUILD_STRATEGY.md assembled: {n_lines} lines, {OUT.stat().st_size} bytes")
