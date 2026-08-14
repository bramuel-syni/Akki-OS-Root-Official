# CONTEXT.md — Running narrative

**Last updated:** 2026-08-14, on receipt of Ruling 3 (Instruction 02, interface strategy directive).

## Where we are

- Assessment REUSE_ASSESSMENT.md ACCEPTED by owner (2026-08-14).
- Rulings issued: Ruling 1 (transition condition for purpose-gate), Ruling 2 (five-point plan responses), Ruling 3 / Instruction 02 (interface strategy directive — Extraction-Akki frontend as donor, tile-grid-plus-detail-card grammar). See `DECISIONS.md`.
- Next deliverable: `BUILD_STRATEGY.md` (paper, no code) — Part 1 in progress with interface section added.
- Prohibitions still in force: no production code, no harvesting-in-code, no re-pointing, no scaffolding, no canon edits. Throwaway audit scripts under `tools/` remain allowed.

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

- Building the BUILD_STRATEGY.md work-item universe. Every non-REUSE assessment row gets a stable work-item ID (WS-###). Every assessment row maps to EXACTLY ONE work item, mechanically audited via `notes/row_to_item_index.md`.
- Estimation discipline defined once in the document (S/M/L/XL credit cost class).
- Item tables split: Part 1 (MODIFY/PARTIAL, RE-POINT, HARVEST, RETIRE, WIRING) first; BUILD (148 rows) is the next chunk.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol):
- STATE/ present and intact: CONTEXT.md · PINS.md · DECISIONS.md · NEXT.md
- REUSE_ASSESSMENT.md intact: 450 lines
- notes/ intact: 31 files (28 canonical + 3 raw dumps)
- repos/ intact: 4 pinned clones (Akki-Executive-Core · Akki-OS-V1 · Extraction-Akki · RMS-IQ-Core-2)
- canon/ intact: 9 extracted `.txt` under `canon/text/`, source `canon_pack.zip`, `unpacked/`
- `notes/row_to_item_index.md` intact: 380 lines, 591 rows mapped, 85 items (30 Part-1 + 55 Part-2), named gaps = none.

Nothing missing. Resuming exactly at STEP 2 (estimation discipline) and STEP 3 (draft Part-1 item tables) per NEXT.md.

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

Latest audit: **102/102 file citations verified · 814/854 canon citations verified · 40 failed** — all inherited Chunk-1 drift where `Cn-0MM (§XX)` row IDs referenced §-numbers exceeding actual canon `[Heading]`-numbered spans (Canon 3 max §33, Canon 5 max §43, Canon 8 max §21, Canon 9 max §8). Disclosed in `fidelity_ledger.md` FL-P1-20; not silently corrected. Substance-grounding of every item's DEFINITION OF DONE remains sound (grounded in canon HEADING TITLES, not numeric anchors). Systematic re-mapping is a recommended scoped chunk.

## Doctrinal frame

- The four-test review discipline (Ruling 1 preamble) — every parameter of success is met by a named mechanism; quality discipline held exactly as canon; no build credit spent without survivable reason; nothing lands that canon does not keep. Every work item in Part 1 must satisfy all four tests.
- Canon 9 record matrix + task-identity register + handoff contract discipline — every item cites its record classes (as Canon-9 rows from `canon_9_requirements.md`) and its task identity, even though the register itself is BUILD.
- Canon 4 §32 quality matrix + Canon 3 §31 verification packs — every item states its QUALITY EVIDENCE against these.
- "Code complete" / "tests pass" are forbidden phrasings in Definition of Done (per owner instruction).

## Repos / SHAs / paths — see PINS.md
