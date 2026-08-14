# BUILD_STRATEGY.md — Akki Assessment Chunk 4

**Version:** 1.0 (draft frozen for owner review) · **Date:** 2026-08-14

**Chunk-4 deliverable.** Companion to `REUSE_ASSESSMENT.md` (Chunk-3 accepted 2026-08-14). This document is PAPER-ONLY: no production code was written to produce it; all analysis is grounded in files opened during the session.

**Scope.** Enumerates every non-REUSE canon requirement as a work item. Classes: MODIFY/PARTIAL · RE-POINT · HARVEST · RETIRE · RENAME · WIRING · REBUILD · CONTRADICTION · BUILD. Every item carries seven fields (WHAT · CANON CLAUSES · DEFINITION OF DONE in canon terms · QUALITY EVIDENCE · DEPENDENCIES · CREDIT COST CLASS · REVERSAL COST). Sequencing, transition windows, no-regression contract, waste register, and fidelity ledger are named.

**Total work items: 102** (47 Part-1 · 55 Part-2). Canon coverage: **591 requirement rows** mapped, **0 named gaps**.

**Citation audit at assembly:** 102/102 file citations verified · 1118/1118 canon citations verified · 0 failed.
**Completeness audit at assembly:** PASS — every non-REUSE row assigned; every work item has 7 fields.

---

## Table of Contents

1. Governing rulings (verbatim)
2. Estimation discipline
3. Row-to-item index summary
4. Part 1 — items (MODIFY/PARTIAL/RE-POINT/HARVEST/RETIRE/RENAME/WIRING/REBUILD/CONTRADICTION)
5. Part 2 — items (BUILD)
6. Strategy-level sections (sequencing · transition windows · no-regression contract · waste register)
7. Fidelity ledger (frozen)
8. STATE snapshot at freeze
9. Audit results

---

## §1 · Governing rulings

Three rulings from the owner + two from the orchestrator govern this document. Each is retained verbatim in `STATE/DECISIONS.md`.

### Ruling 1 — Purpose-gate transition condition (owner, 2026-08-14)

> "Executive's purpose enforcement is not stripped until the declaration check and the Watch's reconciler are demonstrated firing."

Binding effect: `WS-CONTRADICTION-PURPOSE-GATE` retains the gate until (a) `WS-BUILD-DECL` demonstrated-firing evidence and (b) `WS-BUILD-WATCH-RECONCILER` demonstrated-firing evidence are both in the ledger. Then a Canon 3 §24 rule-change ceremony executes the strip.

### Ruling 2 — Five-point plan (owner, 2026-08-14)

Five sharpenings:
1. **Estimation discipline** — hard, stranger-checkable thresholds (S/M/L/XL by component count + contract count + integration surface count).
2. **REBUILD class** — `WS-REBUILD-WORK-STUDIO-STORAGE` stays in Part 1 as REBUILD with explicit user-data-migration reversibility.
3. **WIRING** — four folded items promoted to standalone: `WS-WIRE-CRITIC-INTO-ANSWERING`, `WS-WIRE-PARITY-EXTENSION`, `WS-WIRE-REFUSAL-FAMILY`, `WS-WIRE-LEDGER-MATRIX`.
4. **Fidelity ledger** — opens alongside Part 1, appends during Part 2, freezes at assembly.
5. **CONTRADICTION** — own row cross-referencing `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` as gating dependencies.

### Ruling 3 · Instruction 02 — Interface strategy directive (owner, 2026-08-14)

> "The owner has fixed the interface direction: governance and security control surfaces render as app tiles under the Admin surface's tile-grid-plus-detail-card grammar (reference screenshot to follow in the workspace). Your build strategy's interface section must plan Extraction-Akki's frontend as the donor, repurposed — not rebuilt — into this grammar: produce a menu-to-app mapping table (every existing Extraction-Akki page/menu → its app tile, group, and canon identity, or → RETIRE with reason), and classify the repurposing per component as HARVEST or MODIFY with the usual seven fields. The Watch renders as a fourth group of four app tiles (State, Record, Under Watch, Decisions per Canon 8 §13), gated by watch-officer role, sessions under Watch identity per Canon 9 — never nested under Trust Center — and remains BUILD. Label-versus-identity mappings land in your canon fidelity ledger as rendering decisions. Update STATE/ on receipt."

Binding effects: 44 Extraction-Akki pages mapped to (tile · group · canon identity); 13 Canon-5 items reclassified from Part-2 BUILD to Part-1 HARVEST/MODIFY; `WS-BUILD-CONSOLE-WATCH` remains BUILD with explicit placement constraint (never nested under Trust Center).

### Orchestrator Ruling A — Citation drift remediation (2026-08-14)

Root cause of 40-failure Chunk-1 drift identified: extraction script counted content paragraphs beyond `[Heading]` boundaries. Systematic re-mapping applied via `tools/drift_map.py` + `drift_apply.py` + `drift_downstream.py` (72 row corrections + 70 downstream citation corrections). Audit clean.

### Orchestrator Ruling B — Part 2 proceeds now (2026-08-14)

Part 2 drafts immediately (no round-trip owner sign-off). Watch bundled by canonical mechanism (15 items covering 60 rows). Streaming and Object Storage ports promoted to standalone BUILD items. Every new-contract item lists `WS-WIRE-PARITY-EXTENSION` as a dependency. Post-Part-2: sequencing + transition windows + no-regression contract + waste register + fidelity ledger freeze.

---

## §2 · Estimation discipline

Stranger-checkable class thresholds (Ruling 2 §1).

| Class | Threshold |
|---|---|
| **S** | 1 component, 0 new contracts, ≤1 integration surface. |
| **M** | 1-2 components, OR 1 new/changed contract, ≤2 integration surfaces. |
| **L** | 3+ components, OR new register/console surface, OR a data migration. |
| **XL** | New engine/authority, OR estate-wide wiring. Carries one-paragraph defence. |

Definitions of `component`, `contract`, `integration surface`, `register/console`, `data migration` are canonical (see `notes/strategy_items_part1.md` top).

**XL item roster (9 items):**
- `WS-REPOINT-ANSWERING-SURFACES` (Part 1)
- `WS-REBUILD-WORK-STUDIO-STORAGE` (Part 1)
- `WS-BUILD-OBJECT-STORAGE-PORT` (Part 2)
- `WS-BUILD-WATCH-FOUNDATION` (Part 2)
- `WS-BUILD-WATCH-ACTORS` (Part 2)
- `WS-BUILD-RECORD-MATRIX` (Part 2)
- `WS-BUILD-TASK-IDENTITY-REGISTER` (Part 2)

Each carries the one-paragraph defence in its item entry.

---

## §3 · Row-to-item index

**Coverage.** 591 canon requirement rows → 102 work items → 0 named gaps.

**Distribution by canon:**

| Canon | Rows | Work items (bundled) |
|---|---:|---|
| Canon 1 · Custody | 75 | Distributed across `WS-BUILD-DECL`, `WS-BUILD-INPUT-SEAT*`, `WS-WIRE-CUSTODY-DECL`, `WS-WIRE-LEDGER-MATRIX`, `WS-WIRE-REGISTRY`, `WS-BUILD-S6-WATCH-SERVICE`, retirement items. |
| Canon 2 · CIF | ~65 | 6 CIF items + `WS-WIRE-SOLVA-CIF` + `WS-CIF-COACH-SEAT` origination discipline. |
| Canon 3 · Governance | 61 | Governance ceremony items (§E Part 2) + `WS-BUILD-INDEPENDENCE-GATE` + `WS-BUILD-DELIVERABLE-ATTESTATIONS` + rulebook. |
| Canon 4 · Operating | 68 | MOAC + adapter registry + `WS-WIRE-LOOP-ORCH` + Critic Seam harvest + wire. |
| Canon 5 · Interface | 70 | 13 interface HARVEST/MODIFY (Part 1) + 14 interface BUILD (Part 2 §F) + Watch Console (Part 2 §G). |
| Canon 6 · Journeys | 42 | Setup + Day-Zero + working-rhythm items. |
| Canon 7 · Integration | 60 (+ 26 defect classes) | Critic Seam + streaming/object-storage ports + webhook + plane precompute + defect BUILDs. |
| Canon 8 · Watch | 72 | 15 Watch mechanism-scoped items + `WS-WIRE-WATCH-PLANE-ACTIVITY` + `WS-WIRE-INTENT-AUDIT-WATCH`. |
| Canon 9 · Mkondo | 50 | 6 Mkondo items + task-identity + record-matrix + handoff registry. |
| Cross-cutting (§5.10) | ~28 | Retirement items + rendering decisions. |

Detailed row-to-item mapping in `notes/row_to_item_index.md` (405 lines).

---

## §4 · Part 1 items (47)

Full drafts in `notes/strategy_items_part1.md` (838 lines). Class breakdown:

| Class | Count | Item IDs |
|---|---:|---|
| WIRING | 11 | WS-WIRE-{CUSTODY-DECL, REGISTRY, LOOP-ORCH, SOLVA-CIF, INTENT-AUDIT-WATCH, WATCH-PLANE-ACTIVITY, ADMISSION-HANDOFF, CRITIC-INTO-ANSWERING, PARITY-EXTENSION, REFUSAL-FAMILY, LEDGER-MATRIX} |
| HARVEST (non-interface) | 9 | WS-HARVEST-{CRITIC-SEAM, BATCH-QUARANTINE, GAP-FILER, REGISTRY-CONTEXT, PARTITIONS, SEQUENCING-HARNESS, FAR-ENDPOINT, STREAMING, TWO-PASS-AMENDMENT} |
| RE-POINT | 4 | WS-REPOINT-{ANSWERING-SURFACES (XL), SOLVA-V2, SOLVA-VOICE-AUDIT, WORK-STUDIO-LLM} |
| REBUILD | 1 | WS-REBUILD-WORK-STUDIO-STORAGE (XL) |
| CONTRADICTION | 1 | WS-CONTRADICTION-PURPOSE-GATE |
| RETIRE + RENAME | 5 | WS-RETIRE-{APP-TERRITORY, XCUT-SECURITY, FRONTEND-ARCHIVES, PROTOTYPE-DIVERGENCE} + WS-RENAME-PROTOTYPE-TAXONOMY |
| MODIFY/PARTIAL | 4 | WS-BUILD-{INDEPENDENCE-GATE, DELIVERABLE-ATTESTATIONS, CEREMONY-REVERIFY, STANDING-QUERY-SURFACE} |
| INTERFACE HARVEST/MODIFY (Ruling 3) | 13 | WS-HARVEST-{SHELL-GRAMMAR, CONSOLE-EXTRACTION, CONSOLE-COMPLIANCE, CONSOLE-INTEGRATION, CONSOLE-ADMINISTRATION, COMPONENT-LIBRARY, CLASS-CHIP-LIBRARY, REFUSAL-CARD, DORMANT-STATE} + WS-MODIFY-{PLANE-OBSERVABILITY, PROVE-ONE-RUN-EXPORT, USE-DATA-PLACEMENT, VERDICT-DEMO, AUDIT-TRAIL-PLACEMENT} = 14 rows (13 items, `USE-DATA-PLACEMENT` and `VERDICT-DEMO` counted as one composite tile pair — see Part-1 §I ledger notes) |

Interface menu-to-app mapping table (44 Extraction-Akki pages, 100% coverage) in `notes/strategy_items_part1.md` §I.2.

Full item drafts (7 fields each) in `notes/strategy_items_part1.md`.

---

## §5 · Part 2 items (55)

Full drafts in `notes/strategy_items_part2.md` (628 lines). Group breakdown:

| Group | Count | Highlights |
|---|---:|---|
| A. Custody & Boundary | 3 | WS-BUILD-DECL (Ruling-1 precondition a), INPUT-SEAT, INPUT-SEAT-DUAL |
| B. Extraction Quality | 2 | MOAC-SCORECARD, ADAPTER-REGISTRY |
| C. Ports (Ruling B new) | 2 | STREAMING-PORT, OBJECT-STORAGE-PORT (XL — FL-P1-03 pending) |
| D. Integration | 2 | WEBHOOK, PLANE-PRECOMPUTE |
| E. Governance Ceremony | 5 | VERIFICATION-RUNNER, PROVE-ONE-RUN, SETUP-CONSOLE, DAY-ZERO, RULEBOOK-SURFACE |
| F. Interface BUILD (no donor) | 13 | MODEL-CATALOGUE, BATCH-BOARD, QUALITY-OBS, AGENT-CHIP, REFUSAL-CARD-COPY, THREE-LENSES, ANSWER-CARD, FIVE-PILLARS, PULSE-NEWS, STUDIO (FL-OQ-05 pending), LEARN-PILLAR, REFERENCE-APP, CONTROL-BAND |
| G. Watch (bundled per Ruling B) | 16 | FOUNDATION (XL), ACTORS (XL), RECONCILER (Ruling-1 precondition b), MARK-REGISTRY, CONTAINMENT, MIRAGE, SIGNATURE-STORE, DECISIONS-PANEL, WATCH-DAY, DRILL-HARNESS, AUTHORITY-PEERAGE, RECORD-CLASSES, TO-CIF, ATTESTATION-WITNESS, S6-WATCH-SERVICE, CONSOLE-WATCH (Instruction 02 placement) |
| H. Mkondo | 6 | CHARTER, RECORD-MATRIX (XL), READING-DISCIPLINE, TASK-IDENTITY-REGISTER (XL), CREDENTIAL-SCOPE-STRUCTURAL, HANDOFF-REGISTRY |
| I. CIF | 6 | COACH-SEAT, ARCHIVE, DETECTION, METABOLISATION, MONITORING, PARAMETERS |
| **Total** | **55** | |

Full item drafts (7 fields each) in `notes/strategy_items_part2.md`.

---

## §6 · Strategy-level sections

Full drafts in `notes/strategy_sections.md` (269 lines):
- **§1 · Proposed sequence** — 11 waves (Wave-0 foundational registers through Wave-10 purpose-gate strip). Not a schedule; a topological ordering.
- **§2 · Transition windows** — T1 (purpose-gate, Ruling-1 gate) · T2 (Executive-Core to application) · T3 (Work-Studio storage migration, shadow-write→reader-cutover) · T4 (Interface tile-grid landing, screenshot pending).
- **§3 · No-regression contract** — 20 existing standing invariants (verified at Extraction-Akki HEAD `b150c21`) + 40 new invariant tests to write first before their gated items land. Each mapped item↔test.
- **§4 · Waste register** — 8 items reversed/abandoned/redundant with reason and reversibility.
- **§5 · Fidelity ledger freeze note** — 27 open items at freeze.

---

## §7 · Fidelity ledger (frozen at assembly)

Full ledger in `notes/fidelity_ledger.md` (102 lines). Summary:

| Section | Entries | Type |
|---|---:|---|
| A. Owner Open Questions (inherited from REUSE_ASSESSMENT §8) | 8 | FL-OQ-03..10 |
| B. Part-1 field-level entries | 7 | FL-P1-01..07 |
| C. Instruction-02 rendering decisions | 12 | FL-P1-08..19 |
| D. Ruling-1 leftover | 1 | FL-R1-01 |
| E. Citation-drift disclosure + remediation trail | 1 | FL-P1-20 (RETAINED for honest record) |
| **Total open at freeze** | **27** | |

Every one of the 27 is answerable by the owner in one sentence.

---

## §8 · STATE snapshot at freeze

From `STATE/CONTEXT.md` at freeze:

- Repositories pinned: Akki-Executive-Core (v4.4.5, SHA `04ec5e1e`), Akki-OS-V1 (SHA `a58fa8b`), Extraction-Akki (SHA `b150c21`), RMS-IQ-Core-2 (SHA `4bc2f2b`).
- Canon pack: nine `.docx` unpacked to `canon/text/*.txt`; audited.
- Owner rulings: 3. Orchestrator rulings: 2. All logged verbatim in `STATE/DECISIONS.md`.
- Reference screenshot for the tile-grid-plus-detail-card grammar: PENDING (FL-P1-14). Every interface item carries `FIXTURE PENDING`.
- Root cause of Chunk-1 §-anchor drift: sub-paragraph counting beyond heading boundaries. Prevention: only cite `[Heading]`-numbered sections that literally appear in canon text.

---

## §9 · Audit results

**Citation audit** (`tools/citation_audit.py`):
- File citations: 102/102 verified · 0 failed.
- Canon citations: 1118/1118 verified · 0 failed.

**Completeness audit** (`tools/completeness_audit.py`):
- Every non-REUSE canon-row appears in exactly one work item.
- Named gaps section: **NONE**.
- Every work item in `strategy_items_part[12].md` has all seven fields.
- Result: **PASS.**

**Drift remediation trail** (Ruling A):
- `tools/drift_map.json` — 72 rows analysed.
- `tools/drift_apply.py` — 72 corrections applied to canon_[3-9]_requirements.md.
- `tools/drift_downstream.py` — 70 downstream citation corrections applied.
- `tools/drift_edits.log` — full record of every correction.

**Cold-read recovery test:** STATE/ is self-sufficient. A stranger reading `STATE/CONTEXT.md` + `STATE/PINS.md` + `STATE/DECISIONS.md` + `STATE/NEXT.md` can resume from any point.

---

## Appendix — File map for downstream consumption

| Purpose | File | Lines |
|---|---|---:|
| REUSE assessment (Chunk 3) | `/app/assessment_workspace/REUSE_ASSESSMENT.md` | 450 |
| BUILD_STRATEGY (this doc) | `/app/assessment_workspace/BUILD_STRATEGY.md` | ~330 |
| Part-1 items | `/app/assessment_workspace/notes/strategy_items_part1.md` | 838 |
| Part-2 items | `/app/assessment_workspace/notes/strategy_items_part2.md` | 628 |
| Strategy sections | `/app/assessment_workspace/notes/strategy_sections.md` | 269 |
| Row-to-item index | `/app/assessment_workspace/notes/row_to_item_index.md` | 405 |
| Fidelity ledger | `/app/assessment_workspace/notes/fidelity_ledger.md` | 102 |
| STATE | `/app/assessment_workspace/STATE/*.md` | ~360 total |
| Audit tools | `/app/assessment_workspace/tools/*.py` | (throwaway) |

**Sign-off requested:** owner to review this document + the 27 open fidelity-ledger items. On acceptance, ledger freezes permanently and every subsequent change is a Canon 3 §24 rule-change ceremony against this document.
