# CONTEXT.md — Running narrative

**Last updated:** 2026-08-14, at BUILD_STRATEGY.md v1.1 self-contained assembly.

## Where we are

- Chunk 4 COMPLETE at v1.1 assembly. `BUILD_STRATEGY.md` is now SELF-CONTAINED (2442 lines, 244 KB) at `/app/assessment_workspace/BUILD_STRATEGY.md`. Working papers in `notes/` remain on disk as the review trail.
- Rulings issued: **Ruling 1** (purpose-gate transition), **Ruling 2** (five-point plan), **Ruling 3 / Instruction 02** (interface strategy directive), **Orchestrator Ruling A** (citation-drift remediation), **Orchestrator Ruling B** (Part 2 proceed + strategy sections), **Orchestrator Ruling C** (self-contained assembly). All verbatim in `DECISIONS.md`.
- Assessment REUSE_ASSESSMENT.md ACCEPTED by owner (2026-08-14).
- Prohibitions still in force: no production code, no harvesting-in-code, no re-pointing, no scaffolding, no canon edits. Throwaway audit + assembly scripts under `tools/` remain allowed.

## Deliverable manifest

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — Chunk-3 accepted.
- `/app/assessment_workspace/BUILD_STRATEGY.md` (2442 lines) — Chunk-4 v1.1 self-contained assembly.
- Working papers on disk (feeding the assembly):
  - `notes/strategy_items_part1.md` (838 lines, 47 items).
  - `notes/strategy_items_part2.md` (628 lines, 55 items).
  - `notes/strategy_sections.md` (269 lines).
  - `notes/fidelity_ledger.md` (102 lines, 27 open items, frozen).
  - `notes/row_to_item_index.md` (405 lines, 591 rows → 102 items, 0 named gaps).
- Assembly tool: `tools/assemble_build_strategy.py`.
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.

## Audit posture at v1.1 assembly

- Citation audit (now includes BUILD_STRATEGY.md): 104/104 file · **1778/1778 canon · 0 failed**.
- Completeness audit (now validates BUILD_STRATEGY.md self-contained): PASS — every non-REUSE row assigned; every work item has 7 fields; BUILD_STRATEGY.md self-contained confirmed.
- Cold-read recovery test: STATE/ is self-sufficient; verified.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## What Ruling 1 changes

- **Binding transition condition on the purpose-gate contradiction (Open Question #1)**: Executive-Core's `services/synisense/shield/purpose_validator.validate_purpose()` (at `client.py:63`) is NOT stripped until BOTH (a) the actor-declaration check (Canon 3 §6.1, Assessment C3-008/C3-009/C3-010) AND (b) the Watch's reconciler are DEMONSTRATED FIRING. This turns Open Question #1 from an open governance call into a conditional strip whose enabling conditions are named.
- **Implicit resolution of Open Question #2 (actor declaration seam)**: because Ruling 1 makes the declaration check a precondition for the purpose-gate strip, the declaration check is confirmed a BUILD item (not left open or absorbed elsewhere). Cite: DECISIONS.md Ruling 1.
- **Executive-Core purpose gate posture**: RETAINED as a canon-compliant surface at Executive-Core HEAD until the two demonstrations fire. Not classified RETIRE until the transition condition is met.

## Open Questions status (from REUSE_ASSESSMENT.md §8)

| OQ | Status after Ruling 1 |
|---|---|
| 1. Purpose-gate contradiction | **PARTIALLY ANSWERED** — retention is conditional, strip is enabled by two demonstrated-firings. Fidelity-ledger entry for the strip itself remains. |
| 2. Admit-declaration seam | **ANSWERED (implicit)** — declaration check WILL be built. |
| 3. Rule-change re-verify step | OPEN — remains in fidelity ledger. |
| 4. Canon 5 four vs five consoles | OPEN — remains in fidelity ledger. |
| 5. Studio canonical scope | OPEN — remains in fidelity ledger. |
| 6. Eight vs five global rules | OPEN — remains in fidelity ledger. |
| 7. Cohort surface's canonical home | OPEN — remains in fidelity ledger. |
| 8. Work_studio storage coupling | OPEN — remains in fidelity ledger. |
| 9. Akki-OS-V1 non-canonical harvest items (partitions, sequencing_harness, far_endpoint) | OPEN — remains in fidelity ledger. |
| 10. Executive-Core post-IF-1 catch-up | OPEN — remains in fidelity ledger. |

## Current activity

- BUILD_STRATEGY.md ASSEMBLED. Chunk 4 complete at freeze. Awaiting owner response on 27 open fidelity-ledger items.

## Historical: recovery event · 2026-08-14T09:24Z (superseded by assembly notes above)

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. All Chunk-4 work post-recovery is documented in the assembly manifest at the top of this file.

## Ruling-2 effects on the item universe

Four WIRING items promoted (were folded); Part-1 item count 30 → 34, grand total 85 → 89.
- `WS-WIRE-CRITIC-INTO-ANSWERING` — critic_pass in-flight on the answering path (harvest lands code, wiring puts it in the request path).
- `WS-WIRE-PARITY-EXTENSION` — frozen-contract-snapshot parity discipline extended to every NEW contract this programme creates.
- `WS-WIRE-REFUSAL-FAMILY` — existing refusal-family taxonomy (`memory/memory_refusal_reasons.v0.json` + `memory/refusal.py`) wired to Canon 5 §9.2 refusal card surface.
- `WS-WIRE-LEDGER-MATRIX` — Northena ledger's sole-writer position promoted to Canon 9 §6-§18 record-matrix-governed writer.

Estimation discipline is now stranger-checkable (see Ruling 2 §1 in DECISIONS.md).
`WS-REBUILD-WORK-STUDIO-STORAGE` remains in Part 1 as a REBUILD row; its REVERSAL COST explicitly addresses user-data migration reversibility.
`fidelity_ledger.md` opens alongside Part 1 at `/app/assessment_workspace/notes/fidelity_ledger.md`; append during Part 2; freeze at BUILD_STRATEGY.md assembly.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — most reclassify to HARVEST or MODIFY (Part 1) with the Extraction-Akki donor page identified; Watch-related rows stay BUILD.
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.
- **Interface reclassification impact on item counts:** 13 Canon-5 items reclassified from Part-2 BUILD to Part-1 HARVEST/MODIFY, WS-BUILD-CONSOLE-WATCH stays Part-2 BUILD with new placement constraint, 11 Canon-5 items retain Part-2 BUILD status (no Extraction-Akki donor found). Part-1 total: 34 → 47 items; Part-2 total: 55 → 42 items. Grand total remains 89.

## Citation audit result at Part-1 close

Latest audit (post Orchestrator-Ruling-A remediation): **102/102 file citations verified · 854/854 canon citations verified · 0 failed.**

**Root cause of the initial drift (recorded per Orchestrator Ruling A):** Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for Part 2: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Doctrinal frame

- The four-test review discipline (Ruling 1 preamble) — every parameter of success is met by a named mechanism; quality discipline held exactly as canon; no build credit spent without survivable reason; nothing lands that canon does not keep. Every work item in Part 1 must satisfy all four tests.
- Canon 9 record matrix + task-identity register + handoff contract discipline — every item cites its record classes (as Canon-9 rows from `canon_9_requirements.md`) and its task identity, even though the register itself is BUILD.
- Canon 4 §32 quality matrix + Canon 3 §31 verification packs — every item states its QUALITY EVIDENCE against these.
- "Code complete" / "tests pass" are forbidden phrasings in Definition of Done (per owner instruction).

## Repos / SHAs / paths — see PINS.md
