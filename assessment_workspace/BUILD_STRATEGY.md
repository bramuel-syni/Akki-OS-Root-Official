# BUILD_STRATEGY.md — Akki Assessment Chunk 4

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
- **§10** — Canon fidelity ledger (27 rows CLOSED by Build Order 01, frozen)
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
- **Register/console surface** = adds a first-class named surface listed in Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED) or Canon 9 (task-identity register, record matrix, handoff registry).
- **Data migration** = any programme that moves user-visible state from one storage/plane shape to another; append-only history is not migration; storage-shape change is migration.

**XL item roster (7 items — Build Order 01 §1 correction; the count was mis-stated as nine):** WS-REPOINT-ANSWERING-SURFACES · WS-REBUILD-WORK-STUDIO-STORAGE (Part 1); WS-BUILD-OBJECT-STORAGE-PORT · WS-BUILD-WATCH-FOUNDATION · WS-BUILD-WATCH-ACTORS · WS-BUILD-RECORD-MATRIX · WS-BUILD-TASK-IDENTITY-REGISTER (Part 2). Each carries its defence in the item entry.

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

## §4 · Part 1 items — 47 items

Full drafts, seven fields each, inlined below verbatim from the working paper `notes/strategy_items_part1.md`. Headings demoted so this section's IDs remain unique.

**Chunk 4, Part 1.** Every non-REUSE row that is NOT a BUILD (Part 2 will hold the 55 BUILD items covering 148 rows).

**Scope of this file:** 34 items, classes MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE / RENAME / WIRING / REBUILD / CONTRADICTION. Every item carries all seven fields exactly.

**Prohibitions active:** no production code, no harvesting-in-code, no re-pointing, no scaffolding, no canon edits. Paper only.

**Governing rulings:** Ruling 1 (transition condition for purpose-gate strip) and Ruling 2 (five-point plan responses). See `STATE/DECISIONS.md`.

---

#### Estimation discipline (Ruling 2 §1)

Every item carries a credit cost class. Class is decided against these hard, stranger-checkable thresholds. No vibes.

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
- **Register/console surface** = adds a first-class named surface listed in Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED) or Canon 9 (task-identity register, record matrix, handoff registry).
- **Data migration** = any programme that moves user-visible state from one storage/plane shape to another; append-only history is not migration; storage-shape change is migration.

Every XL item carries a one-paragraph defence field explaining which of the two XL criteria applies and why.

Fields that cannot be filled honestly for a specific item become entries in `notes/fidelity_ledger.md`. No invented detail.

---

#### Field template (verbatim from Ruling 1 scope requirement)

Each item below has exactly these seven fields:

1. **WHAT** — component, contract(s), record classes (Canon-9 rows), task identity.
2. **CANON CLAUSES SATISFIED** — document + section citations. No clause, no item.
3. **DEFINITION OF DONE** — in canon terms; invariants that hold; operative parameters that go green; verification pack/drill that demonstrates firing. "Code complete" / "tests pass" are FORBIDDEN.
4. **QUALITY EVIDENCE** — test class (unit / contract / invariant / drill), uncurated sample or fixture, calibration/verification obligation under Canon 4 §32 + Canon 3 §31.
5. **DEPENDENCIES** — by item reference; which port / register gates it.
6. **CREDIT COST CLASS** — S/M/L/XL + reuse justification. XL carries one-paragraph defence.
7. **REVERSAL COST** — what undoing costs.

Cross-cutting doctrinal frame (applies to every item; not repeated inside items):
- Canon 9 §6-§18 record matrix (every writer↔readers row is a live contract) — every item names the record class it touches.
- Canon 9 §8-§35 task-identity register — every item names its task identity even though the register is a Part-2 BUILD.
- Canon 4 §32 quality matrix + Canon 3 §31 verification packs — every QUALITY EVIDENCE field references one or both.
- Ruling 1 four-test discipline — every DoD passes: named mechanism · quality-discipline exact · credit spend defended · nothing lands canon does not keep.

---

### A. WIRING items (11)

WIRING covers new work that connects REUSE / HARVEST items into a request-path or matrix seat. WIRING items DO NOT invent new engines; they place existing pieces in canon-required seams.

---

#### WS-WIRE-CUSTODY-DECL

1. **WHAT.** Wire the declaration-check verdict (from `WS-BUILD-DECL`, Part 2) into the fail-closed custody chain at `services/northena/admit.py:107-148 compile_and_freeze` (rows C1-014, C1-015 fail-closed; C1-038..C1-041 model-routing PARTIAL). Record class touched: `Ledger.Row` (Canon 9 §6 row 1, writer = Northena ledger, reader = Compliance Console + Watch). Task identity: `custody.admit.declaration_join`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §4.1 (unrepresentable-not-policed); Canon 1 §6 (fail-closed custody); Canon 3 §6.1 (declarations captured before operations); Canon 6 §3 L010 (declarations from setup morning forward).
3. **DEFINITION OF DONE.** Every `compile_and_freeze` invocation refuses admission when the actor declaration is absent, expired, or scope-mismatched (Canon 3 §6.1). Refusal writes a `LedgerRow(stage="admit", decision="refused", reason_family="declaration_missing"|"declaration_expired"|"declaration_scope_mismatch")` — same append-only path (Canon 1 §4.3 N-INV-4). N-INV-8 (append-only) and N-INV-9 (refusals recorded) hold on the new refusal path. Verification pack: Canon 3 §31 "prove-one-run" export for a refused admission shows declaration verdict as the refusal cause.
4. **QUALITY EVIDENCE.** Invariant test class extending `tests/invariants/test_northena_ledger_row_v0.py` and `tests/invariants/test_admission_refusal_v0_contract_frozen.py`. Uncurated sample: at least one drill run with a fixture where the declaration is expired mid-run; the refusal reason must appear in the sample. Calibration obligation (Canon 3 §31): the refusal reason exports intact through the prove-one-run pack.
5. **DEPENDENCIES.** Gated by `WS-BUILD-DECL` (declaration seat + admit-time check + supersession) — Part 2 item. Uses declaration record class from `WS-BUILD-RECORD-MATRIX` (Part 2). Interacts with `WS-WIRE-LEDGER-MATRIX` (this Part 1) — the ledger becomes matrix-governed by that item.
6. **CREDIT COST CLASS.** M. Justification: 1 component (`services/northena/admit.py`), 0 new contracts (extends the frozen `AdmissionRefusalV0` shape), 2 integration surfaces (declaration seat + ledger writer).
7. **REVERSAL COST.** Cheap. The ledger is append-only; a wiring rollback issues a canon-9 correction row (new entry, never a mutation — Canon 8 §21). No user-visible state migrates. Risk: refusal-corpus contamination if the new reason family is retired later — mitigated by keeping the family taxonomy in the refusal-family registry (`WS-WIRE-REFUSAL-FAMILY`).

---

#### WS-WIRE-REGISTRY

1. **WHAT.** Wire Function & Promise Registry rows (C1-053, C1-054) to the harvested `services/registry_context/` prompt-context injection subsystem (`WS-HARVEST-REGISTRY-CONTEXT`). Record classes touched: `Registry.Function`, `Registry.Promise` (Canon 9 §6-§18, currently BUILD in Part 2 — this item wires the readers). Task identity: `registry.function_promise_context`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §8 (Function & Promise Registry as tooling artefact); Canon 5 §17 (Registry Administration surface); Canon 2 §14 (condition watchers via readable registry).
3. **DEFINITION OF DONE.** Every prompt built by `registry_context/` reads from the Function & Promise Registry writer (Canon 9 §6 row for Function/Promise classes) rather than from ad hoc lookups. Registry-Administration console read-back (Canon 5 §31-§36) shows every function and promise it will surface AT the same shape the prompt sees. Verification: a compliance-owner opening the Registry-Administration console and clicking any Function row sees the same content the runtime prompt would inject at that instant.
4. **QUALITY EVIDENCE.** Contract test at the `Registry` reader shape (freeze snapshot). Uncurated sample: prompt-injection log for one real workspace over one drill day is diffed against the console read-back. Calibration under Canon 4 §32 quality matrix: coverage = 100% of runtime-inject calls source from the registry writer.
5. **DEPENDENCIES.** Gated by `WS-HARVEST-REGISTRY-CONTEXT` (Part 1) + `WS-BUILD-RECORD-MATRIX` (Part 2 — assigns writer role). Couples with `WS-BUILD-CONSOLE-ADMINISTRATION` (Part 2, read-back surface).
6. **CREDIT COST CLASS.** M. Justification: 2 components (`registry_context/` + admin console read-back path), 1 changed contract (registry reader shape stabilised), ≤2 integration surfaces.
7. **REVERSAL COST.** Medium. If the wiring lands wrong, prompts revert to ad hoc lookups quickly; but a rule-on-paper flag (Canon 5 §26) may fire mid-transition and needs to be ledgered. Reversal requires a matching Registry-writer un-assignment in the record matrix — new entry only.

---

#### WS-WIRE-LOOP-ORCH

1. **WHAT.** Operating-loop end-to-end orchestration (C1-062..C1-067, C4-049..C4-051): declare → measure → target → check → deliver → observe. Uses harvested `services/targeta/gap_candidate_filer.py` (`WS-HARVEST-GAP-FILER`). Contracts touched: mining-plan contract (`test_targeta_invariants.test_mining_plan_contract_frozen`), yield-layer permutation guard (`test_targeta_invariants.test_yield_output_is_permutation_raises_on_drop`). Record class touched: `Ledger.Row` (each stage emits). Task identity: `loop.orchestrate.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §6 (loop as first-class); Canon 4 §12-§14 (targeta plans; mtafiti measures); Canon 4 §21-§25 (Critic Seam); Canon 6 §5-§7 (Exploration → gap file → commissioning).
3. **DEFINITION OF DONE.** For a single admitted artefact, all six stages emit their canonical LedgerRow shapes in order; every stage's floor-carrier invariants (targeta yield-layer permutation guard; mtafiti verdict-is-matrix-lookup) hold. Canon 4 §32 "loop repeatability" parameter goes green on a byte-identical replay (`test_v0_paths_byte_identical_after_4a.py` style). Verification pack: Canon 3 §31 prove-one-run for one full loop cycle.
4. **QUALITY EVIDENCE.** Drill class (loop drill). Uncurated sample: one full workspace run replayed byte-identical; loop-completion parameter measured across 50 real runs. Calibration under Canon 4 §32 §10 repeatability + §21 quarantine.
5. **DEPENDENCIES.** `WS-HARVEST-GAP-FILER`, `WS-HARVEST-BATCH-QUARANTINE`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD` (Part 2 — for the console-visible loop status).
6. **CREDIT COST CLASS.** L. Justification: 4 components (northena, targeta, mtafiti, service_1), 0 new contracts (uses existing frozen shapes), 3 integration surfaces (declaration, ledger writer, batch board).
7. **REVERSAL COST.** Low-medium. Loop composition is orchestration; the underlying engines are already frozen. Reversal = disabling the orchestrator hook and letting individual services run standalone (their existing tests still pass). No data shape changes.

---

#### WS-WIRE-SOLVA-CIF

1. **WHAT.** Apply the spine's Solva-pattern validation (`services/solva_depth/`) to the CIF's OWN claims (Canon 2 §12: coach seat's origination port claims and CIF-parameter measurements). Record class touched: `Solva.Trace` (Canon 9 §6 writer = Solva). Task identity: `cif.solva_reflexive_check`.
2. **CANON CLAUSES SATISFIED.** Canon 2 §12 (CIF makes claims and must submit them to the same validation as user claims); Canon 3 §14 (assertion boundary applies universally); Canon 1 §7 (engine walls — Solva does not extract, but validates all claims).
3. **DEFINITION OF DONE.** Every CIF claim (frame detection, adoption, metabolisation completion, parameter reading) passes through `services.solva_depth.assertion.conclusion_class` with the same floor-over-load-bearing discipline (`test_class_is_floor_over_load_bearing_all_fact`). CIF cannot self-certify (Canon 2 §17-§19 "permanent bound — self-certification closed"). Verification: prove-one-run for a frame-adoption event shows Solva verdict on the CIF's claim.
4. **QUALITY EVIDENCE.** Invariant test extending `test_solva_assertion_boundary.py`. Uncurated sample: 20 CIF frame detections drawn from Watch/CIF logs in the first month post-live; every one carries a Solva trace row. Calibration under Canon 3 §31: assertion boundary is parameterless — no CIF field may inject "confidence" or "caveat".
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT` (Part 2), `WS-CIF-DETECTION` (Part 2), `WS-CIF-METABOLISATION` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2 — Solva trace writer row).
6. **CREDIT COST CLASS.** S. Justification: 1 component (CIF calls Solva), 0 new contracts, 1 integration surface (Solva-depth boundary).
7. **REVERSAL COST.** Low. The Solva boundary is already frozen; adding a caller is additive. Reversal = removing the CIF call site; the CIF then re-enters self-certification (Canon-2 violation). Ledger the wire event as an append-only record.

---

#### WS-WIRE-INTENT-AUDIT-WATCH

1. **WHAT.** Intent-audit divergence-field (from admit) consumed by the Watch's Macho sensor. Row C3-026 PARTIAL. Record class touched: `Watch.Verdict` (Canon 9 §6 writer = Watch, reader = Compliance Console + Governance). Task identity: `watch.macho.intent_divergence_sense`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §26 (intent audit); Canon 8 §6 (three-actor seam Macho sensor); Canon 8 §14-§15 (marks + reconciliation); Canon 9 §6 handoff `governance→Watch verdict`.
3. **DEFINITION OF DONE.** Every intent-audit divergence row (declared purpose vs measured purpose) becomes an input to Macho; a divergence above the governed threshold produces a Watch mark of class `intent_divergence` (Canon 8 §14). The mark carries the source LedgerRow id (append-only chain). Verification: a drill with a deliberately-diverged actor produces one and only one intent-divergence mark within Canon 8 §5 machine-speed bounds (< the frozen response-time seat).
4. **QUALITY EVIDENCE.** Drill class (Watch drill C8-034). Uncurated sample: 5 divergence fixtures spanning the calibration band + 5 non-divergent controls; false-mark rate must stay under the Canon-8 §32 operative parameter. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS` (Part 2 — Macho sensor), `WS-BUILD-WATCH-MARK-REGISTER` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-LEDGER-MATRIX` (this Part 1).
6. **CREDIT COST CLASS.** M. Justification: 2 components (intent-audit surface, Watch Macho ingest), 1 new contract (intent-divergence mark class), 2 integration surfaces (ledger reader + Watch mark writer).
7. **REVERSAL COST.** Medium. Marks are append-only; a wrong wire generates spurious marks. Reversal = disable divergence ingest; marks written stay in the register with a Canon 8 §21 correction entry. No mark class deletion.

---

#### WS-WIRE-WATCH-PLANE-ACTIVITY

1. **WHAT.** Watch reads plane activity (not content) — row C7-019. Canon 8 §21 boundary constraint: Watch sees activity metadata (who wrote what class, when, verdict), never plane content. Record class touched: `Watch.Read` (Canon 9 §8 read-only reader; no writer). Task identity: `watch.plane_activity_read`.
2. **CANON CLAUSES SATISFIED.** Canon 7 §19 (plane activity — not content); Canon 8 §21 (Watch never reads content); Canon 9 §8 (matrix defines reader lists per class).
3. **DEFINITION OF DONE.** Watch's plane-activity reader passes a discipline test that no content field crosses the boundary. Canon 8 §21 operative parameter "watch surface bounded to activity" goes green. Verification: an AST-level ingress-firewall test (mirror of the existing `test_ast_egress_gate.py` in Extraction-Akki) blocks any content-typed field from reaching Watch code.
4. **QUALITY EVIDENCE.** Invariant test (AST-scoped gate). Uncurated sample: one week of real plane activity events on the drill fixture; boundary crossing count = 0. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-HARVEST-PARTITIONS` (Part 1 — session partitions carry the activity envelope).
6. **CREDIT COST CLASS.** M. Justification: 2 components (plane reader shim + Watch ingest), 1 changed contract (Watch's read shape), 2 integration surfaces.
7. **REVERSAL COST.** Low-medium. Reversal = disable the reader. But if any Watch verdict was written using content (violation), those verdicts are frozen (append-only). Remediation is by Canon 8 §21 correction entry — not deletion.

---

#### WS-WIRE-ADMISSION-HANDOFF

1. **WHAT.** Existing admission→extraction handoff at `services/wizard/admission_handoff.py` (per REUSE_ASSESSMENT.md file map) registered as a Canon-9 §6 contract (row C9-036). Record class touched: `Handoff.Contract` (Canon 9 §8-§42). Task identity: `handoff.admission_to_extraction`.
2. **CANON CLAUSES SATISFIED.** Canon 9 §6 (handoff contracts as first-class); Canon 9 §8-§42 (six handoff contract shapes).
3. **DEFINITION OF DONE.** The `admission_handoff` interface is registered as one of the six Canon-9 handoff contracts (WS-BUILD-HANDOFF-REGISTRY, Part 2), its wire shape frozen under `tests/invariants/test_invariant_contract_snapshots.py` (see `WS-WIRE-PARITY-EXTENSION`). Verification: contract-snapshot test emits a parity seat entry for this handoff.
4. **QUALITY EVIDENCE.** Contract test (snapshot). Uncurated sample: one week of live admission handoffs; every handoff carries the frozen contract shape. Calibration under Canon 3 §31 verification pack ("prove-one-run" for one handoff).
5. **DEPENDENCIES.** `WS-BUILD-HANDOFF-REGISTRY` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1).
6. **CREDIT COST CLASS.** S. Justification: 1 component (existing handoff), 0 new contracts (just registers an existing shape), 1 integration surface (registry).
7. **REVERSAL COST.** Very low. Registration is metadata; reversal = de-register in a new matrix entry (append-only). Handoff code untouched.

---

#### WS-WIRE-CRITIC-INTO-ANSWERING (PROMOTED by Ruling 2)

1. **WHAT.** Wire the harvested `services/critic_pass/` (from `WS-HARVEST-CRITIC-SEAM`) INTO the spine's answering-request path — the seam only counts when it's in the request flow. Components touched: `services/chat/protective_layer/` + `services/documents/` + `services/analyze_workspace/` + every RE-POINTed answering surface (see `WS-REPOINT-ANSWERING-SURFACES`). Contract: critic-seam manifest gate on outbound answers. Record class touched: `Critic.Verdict` (Canon 9 §6 writer = Critic Seam, reader = Compliance Console + Watch). Task identity: `answer.critic_gate.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §21-§23 (Critic Seam guards what workers produce; identical architecture guards what the pipeline produces); Canon 7 §31-§34 (Critic Seam as integration contract); Canon 2 §10.2 (pre-ship checklist).
3. **DEFINITION OF DONE.** Every answering surface's outbound envelope passes the Critic manifest gate (`test_cif_manifest_submission_gate.py`-shape). No answer leaves the platform without a Critic verdict recorded in the ledger. Canon 4 §32 "critic hit-rate" parameter goes green against the uncurated sample. Verification: drill (Canon 8 §21-§39 standing drills) fires a shaped-defect fixture and the Critic Seam catches it before the answer surfaces.
4. **QUALITY EVIDENCE.** Contract test (manifest gate). Uncurated sample: 100 real answer envelopes across the four answering surfaces over one drill day; Critic verdict rate = 100%, catch rate on seeded defect corpus ≥ Canon 4 §32 threshold. Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-CRITIC-SEAM` (this Part 1), `WS-REPOINT-ANSWERING-SURFACES` (this Part 1), `WS-WIRE-LEDGER-MATRIX` (this Part 1).
6. **CREDIT COST CLASS.** L. Justification: 4+ components (chat, documents, analyze_workspace, deck_*, inbox_routing, work_studio outputs — the request path fans across the answering surface set), 1 new contract (Critic verdict shape at the outbound envelope), 2 integration surfaces (Critic Seam ingest + ledger writer).
7. **REVERSAL COST.** Medium. Reversal = removing the gate re-opens ungoverned answers (a Canon-7 violation, ledgered as such). Critic verdicts written stay in the ledger; new entries only. Every un-gated answer surface must issue a Canon 8 §21 correction entry naming itself.

---

#### WS-WIRE-PARITY-EXTENSION (PROMOTED by Ruling 2)

1. **WHAT.** Extend the frozen-contract-snapshot parity discipline (`tests/invariants/test_invariant_contract_snapshots.py` + 10+ frozen-shape invariants in `Extraction-Akki/backend/tests/invariants/`) to every NEW contract this programme creates: all six Canon-9 handoff contracts, all thirteen Canon-9 record classes, every Watch verdict shape, and the task-identity register schema. Contract touched: parity-seat manifest. Record class touched: `ParitySeat.Contract`. Task identity: `parity_seat.contract_freeze.per_shape`.
2. **CANON CLAUSES SATISFIED.** Canon 9 §6-§18 (record matrix as live contracts); Canon 9 §8-§42 (handoff contracts); Canon 8 §21-§59 (Watch record classes); Canon 3 §31 (verification packs); Canon 4 §32 (quality matrix).
3. **DEFINITION OF DONE.** For every new contract this programme creates, a matching parity-seat entry lands in `tests/invariants/test_invariant_contract_snapshots.py` (or a companion). Every new contract has a frozen JSON snapshot alongside `memory_plane_v0.contract_snapshot.json` shape. Contract-drift test fires (invariant class) on any downstream field-name / type change without matrix-recorded migration. Verification pack: Canon 3 §31 prove-one-run confirms every new contract carries its snapshot.
4. **QUALITY EVIDENCE.** Invariant class (contract-drift). Uncurated sample: every new contract from Part 2 BUILD items. Calibration under Canon 3 §31 — no contract lands without its parity seat.
5. **DEPENDENCIES.** Gates every Part 2 BUILD that introduces a new contract: `WS-BUILD-HANDOFF-REGISTRY`, `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-WATCH-RECORD-CLASSES`, `WS-BUILD-DECL` (declaration record).
6. **CREDIT COST CLASS.** L. Justification: touches the parity-seat surface (1 component) but crosses ≥6 new contracts (Canon-9 handoffs + 13 record classes + Watch verdict shapes + task-identity register); qualifies as L on the "3+ components / new register" criterion via the register count.
7. **REVERSAL COST.** Cheap but consequential to remove: the parity seat is READ by every regression test; delete it and downstream contract drift becomes undetectable. If wrong, correction is a new entry to the parity manifest — new entry only, never mutation.

---

#### WS-WIRE-REFUSAL-FAMILY (PROMOTED by Ruling 2)

1. **WHAT.** Wire the existing refusal-family taxonomy (`services/memory/memory_refusal_reasons.v0.json` + `services/memory/refusal.py`) to the Canon 5 §9.2 refusal card surface (`WS-BUILD-REFUSAL-CARD-COPY`, Part 2). Contract touched: refusal-reason JSON snapshot (frozen; must be extended via parity seat per `WS-WIRE-PARITY-EXTENSION`). Record class touched: `Refusal.Reason`. Task identity: `refusal.family.render_at_surface`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §9.2 (verbatim refusal card copy); Canon 1 §16 (refusal recorded, never dropped — N-INV-9); Canon 3 §17 (refusal shapes catalogued).
3. **DEFINITION OF DONE.** Every refusal reason surfaced in the Canon 5 §9.2 refusal card component is sourced from the `memory_refusal_reasons.v0.json` taxonomy — no ad hoc copy. The card's frozen-copy invariant test asserts byte-identity of the rendered refusal text with the taxonomy entry. Canon 3 §31 prove-one-run for a refused request emits the taxonomy id + the card copy identically.
4. **QUALITY EVIDENCE.** Invariant class (frozen-copy). Uncurated sample: every distinct refusal reason encountered across a drill week must render verbatim from the taxonomy in every refusal-card impression. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-REFUSAL-CARD-COPY` (Part 2 — the surface being wired to), `WS-WIRE-PARITY-EXTENSION` (this Part 1 — extends the parity seat for the JSON taxonomy).
6. **CREDIT COST CLASS.** S. Justification: 1 component (refusal card render), 0 new contracts (uses existing JSON snapshot), 1 integration surface (memory/refusal reader).
7. **REVERSAL COST.** Very low. Reversal = drop the wire; card falls back to no-refusal render (Canon 5 violation, dormant-state anti-pattern). Refusal taxonomy itself is untouched.

---

#### WS-WIRE-LEDGER-MATRIX (PROMOTED by Ruling 2)

1. **WHAT.** Promote the Northena ledger's sole-writer position (`services/northena/ledger.py:63 record()`, `insert_one` at L65) to a Canon 9 §6-§18 matrix-governed writer — the ledger IS the writer for record class `Ledger.Row` in the matrix. Component touched: `services/northena/ledger.py`. Contract touched: `LedgerRow` frozen shape (`test_northena_ledger_row_v0.py`). Record class: `Ledger.Row` (Canon 9 §6 row 1). Task identity: `ledger.writer.matrix_governed`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §4.3 (append-only, N-INV-4); Canon 1 §7.1 (Northena as authoritative ledger); Canon 9 §6-§18 (record matrix — writers and readers defined); Canon 9 §8 (reads route through matrix reader-list).
3. **DEFINITION OF DONE.** The record matrix `WS-BUILD-RECORD-MATRIX` (Part 2) names Northena's `record()` as the sole writer for `Ledger.Row`. Every reader of `db.northena_ledger` is enumerated in the matrix reader-list; any code path reading the collection outside the reader-list fails an AST discipline check (mirror of `test_ast_egress_gate.py`). Verification: matrix reader-list snapshot has 100% coverage of the observed readers over a drill week.
4. **QUALITY EVIDENCE.** Invariant class (matrix-writer-sole; AST-scoped reader-list check). Uncurated sample: full week of ledger writes and reads; writer count outside `record()` = 0, reader count outside matrix reader-list = 0. Calibration under Canon 3 §31 + Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1 — for the matrix shape).
6. **CREDIT COST CLASS.** M. Justification: 1 component (ledger), 1 new/changed contract (matrix governance seat on this ledger), 2 integration surfaces (matrix writer role + matrix reader-list).
7. **REVERSAL COST.** High-on-drift. If the matrix seat is landed and later stripped, existing readers may still route through the seat and stop reading. Reversal = new matrix entry re-opening the reader-list; but the ledger is append-only — no ledger row can be un-written. Any migration error stays in the append-only chain forever. This is a case for careful review before wiring.

---

### B. HARVEST items (9)

HARVEST covers pulling existing code from a non-spine repo into the spine as source-of-truth. The harvest is paper-only here; the actual code motion is a Ruling-1-prohibited operation until an owner build order lifts the prohibition.

---

#### WS-HARVEST-CRITIC-SEAM

1. **WHAT.** Harvest `services/critic_pass/` (7 files, ~950 LOC) + `services/critic_pass/rubric.py` + `services/critic_pass/seeded_defect_corpus.py` from Akki-OS-V1 into Extraction-Akki spine. Rows: C2-011, C2-016..C2-018, C2-025..C2-028, C2-052..C2-059, C4-031, C7-024..C7-028, C7-D02, C7-D26. Record class: `Critic.Verdict`. Task identity: `critic_seam.execute.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §21-§23 (Critic Seam architecture); Canon 7 §31-§34 (Critic Seam as integration contract); Canon 2 §10.2 (pre-ship checklist); Canon 2 §16-§18 (manifest schema + submission gate).
3. **DEFINITION OF DONE.** All 7 `critic_pass/` files present at the spine at import path `services.critic_pass`. Companion tests `test_critic_pass_execution_atomic.py` + `test_cif_manifest_submission_gate.py` present and firing. Canon 4 §32 "critic seam operative" parameter goes green (uncurated sample: 100% of critic invocations return a rubric-scored verdict). Verification pack: Canon 3 §31 prove-one-run on the critic seam.
4. **QUALITY EVIDENCE.** Contract test (manifest gate) + drill class (seeded-defect corpus). Uncurated sample: the `seeded_defect_corpus` fixture drives the drill; catch-rate must meet Canon 4 §32 threshold. Calibration obligation: Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** No dependencies inward (critic_pass is self-contained per Chunk 2 shaping analysis). Feeds `WS-WIRE-CRITIC-INTO-ANSWERING`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (services/critic_pass — self-contained per Chunk-2 dependency analysis), 0 new contracts (critic-pass is already frozen-shape at Akki-OS-V1), 1 integration surface (import into spine).
7. **REVERSAL COST.** Low. Files harvested can be de-harvested; the spine reverts to no-critic-seam (which is a Canon-7 violation but not a data-loss). No user-visible state changes.

---

#### WS-HARVEST-BATCH-QUARANTINE

1. **WHAT.** Harvest `services/service_1/batch_quarantine.py` (227 LOC) from Akki-OS-V1. Row C4-047. Cited by `critic_pass/harness.py:26` as the "fail-closed per-batch quarantine". Record class: `Batch.QuarantineDecision`. Task identity: `batch.quarantine.per_batch`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §23 (Quarantine); Canon 4 §34.1 (Batch Board); Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` sanctions the landing.
3. **DEFINITION OF DONE.** File at spine path `services/service_1/batch_quarantine.py`. Quarantine verdict emitted per batch flows to `WS-BUILD-BATCH-BOARD-SURFACE` (Part 2) as the panel data. Canon 4 §32 "batch quarantine hit rate" parameter goes green. Verification: drill fires a shaped-batch fixture; quarantine reason recorded.
4. **QUALITY EVIDENCE.** Invariant class (frozen-shape quarantine decision). Uncurated sample: 20 real batches drawn from the drill week; every above-threshold batch quarantined with a reason. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-BUILD-BATCH-BOARD-SURFACE` (Part 2) and `WS-WIRE-LOOP-ORCH` (this Part 1).
6. **CREDIT COST CLASS.** S. Justification: 1 component (single file), 0 new contracts (existing frozen shape), 1 integration surface.
7. **REVERSAL COST.** Very low. Single-file de-harvest; loop reverts to no-quarantine (Canon-4 violation, ledgered).

---

#### WS-HARVEST-GAP-FILER

1. **WHAT.** Harvest `services/targeta/gap_candidate_filer.py` (132 LOC) from Akki-OS-V1. Task identity: `targeta.gap_filer.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §35 (Gap ranking); Canon 6 §5-§7 (Exploration → gap file → commissioning loop).
3. **DEFINITION OF DONE.** File at spine path `services/targeta/gap_candidate_filer.py`. Its output feeds the operating loop's "target" stage (`WS-WIRE-LOOP-ORCH`). Canon 4 §32 "gap ranking coverage" parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (frozen candidate shape). Uncurated sample: gap candidates drawn from one drill week. Calibration under Canon 4 §32 + Canon 6 §5-§7.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-LOOP-ORCH`.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

#### WS-HARVEST-REGISTRY-CONTEXT

1. **WHAT.** Harvest `services/registry_context/` (5 files) from Akki-OS-V1. Task identity: `prompt.context_injection.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §17 (Registry Administration); Canon 2 §14 (condition watchers via readable registry).
3. **DEFINITION OF DONE.** Five files at spine paths under `services/registry_context/`. `test_registry_context_block_golden_snapshot.py` + `test_g_13_execution_atomic.py` at spine test paths. Canon 5 §17 admin-console read-back parameter goes green (see `WS-WIRE-REGISTRY`).
4. **QUALITY EVIDENCE.** Contract test (golden snapshot). Uncurated sample: 20 real prompt-injection events, golden snapshot diff against the runtime context. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-REGISTRY`.
6. **CREDIT COST CLASS.** S. Justification: 5 files but 1 component (self-contained), 0 new contracts.
7. **REVERSAL COST.** Low.

---

#### WS-HARVEST-PARTITIONS

1. **WHAT.** Harvest `services/partitions/session_working_set.py` (Akki-OS-V1 unique, 2 files). Task identity: `session.partition.per_actor`.
2. **CANON CLAUSES SATISFIED.** Canon 6 §3.1 (setup declarations create session scope); Canon 7 §19 (plane activity envelope).
3. **DEFINITION OF DONE.** Files at spine paths. `test_partition_schema_v0_envelope.py` at spine test path. Canon 6 §3.1 setup parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (partition envelope). Uncurated sample: one drill week; every session's partition envelope carries the frozen shape. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-WATCH-PLANE-ACTIVITY` and `WS-BUILD-SETUP-CONSOLE` (Part 2). **Also part of Open Question #9 (Akki-OS-V1 non-canonical harvest items).**
6. **CREDIT COST CLASS.** S. Justification: 1 component (2 files, self-contained), 0 new contracts.
7. **REVERSAL COST.** Low.

---

#### WS-HARVEST-SEQUENCING-HARNESS

1. **WHAT.** Harvest `services/sequencing_harness/` (7 files) from Akki-OS-V1. Task identity: `sequencing.harness.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §6 (loop pipeline); specific clauses require deeper read (see fidelity-ledger OQ #9 — pending owner call).
3. **DEFINITION OF DONE.** _Un-fillable at this stage without deeper read_ → **fidelity_ledger.md** entry FL-P1-01: "Which specific Canon clauses does `sequencing_harness` satisfy that are not already covered by `services/targeta` and `services/mtafiti`? Confirm harvest scope."
4. **QUALITY EVIDENCE.** _Pending Canon clause identification._
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-LOOP-ORCH` if canon anchor confirmed.
6. **CREDIT COST CLASS.** S–M pending scope. Provisional S (7 files self-contained). Reclassify after fidelity-ledger resolution.
7. **REVERSAL COST.** Low.

---

#### WS-HARVEST-FAR-ENDPOINT

1. **WHAT.** Harvest `services/far_endpoint/` (4 files) + `services/generated_gates/` (16 files, regenerable outputs) from Akki-OS-V1. Task identity: `far_endpoint.gate_generation.per_mandate`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §8 (Function & Promise Registry tooling artifacts).
3. **DEFINITION OF DONE.** Files at spine paths. Regeneration test `test_generated_gates_regeneration_diff.py` at spine test path; regeneration produces byte-identical outputs. Canon 1 §8 registry-tooling parameter goes green.
4. **QUALITY EVIDENCE.** Invariant class (byte-identical regeneration). Uncurated sample: one mandate cycle; regeneration diff = 0 bytes. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-REGISTRY`. **Also part of Open Question #9.**
6. **CREDIT COST CLASS.** S. Justification: 1 component (self-contained tooling), 0 new contracts.
7. **REVERSAL COST.** Very low. Tooling artefacts are regenerable.

---

#### WS-HARVEST-STREAMING

1. **WHAT.** Harvest `services/synisense/shield/streaming.py` from Akki-Executive-Core (Core-2/Extraction-Akki currently lack this file). Task identity: `shield.streaming.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §7.1 (Shield boundary as first-class); Canon 3 §12 (input seat); Canon 7 §19 (plane activity envelope for streamed frames).
3. **DEFINITION OF DONE.** File at spine path `services/synisense/shield/streaming.py`. The 19-LOC shim at `services/llm_streaming.py` (currently in Executive-Core, will be RE-POINTed) points to this spine location. Canon 3 §12 streaming-port parameter goes green (frames pass through the shield's input_seat).
4. **QUALITY EVIDENCE.** Invariant class (frame-envelope shape) + contract test at streaming boundary. Uncurated sample: streamed answer sessions over one drill day; every frame carries the shield envelope. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. **Gates `WS-REPOINT-ANSWERING-SURFACES`** — streaming port must exist before RE-POINT completes.
6. **CREDIT COST CLASS.** M. Justification: 1 component, 1 new/changed contract (streaming frame shape at the spine), 2 integration surfaces (input_seat + downstream reader).
7. **REVERSAL COST.** Low-medium. De-harvest = streaming dies at spine; Executive-Core RE-POINT stalls. Reversal via new import path is trivial while nothing depends on it, expensive once RE-POINT completes.

---

#### WS-HARVEST-TWO-PASS-AMENDMENT

1. **WHAT.** Harvest verbatim refusal templates from Executive-Core's `services/two_pass.py` as an amendment to the spine's Solva-pattern refusal shapes (Canon 3 §17). Task identity: `refusal.two_pass_template.per_amendment`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §17 (refusal shapes catalogued); Canon 5 §9.2 (verbatim refusal card copy).
3. **DEFINITION OF DONE.** Two-pass refusal templates registered as additional entries in the refusal-family taxonomy (`memory_refusal_reasons.v0.json`). Every template's rendered text passes the Canon 5 §9.2 frozen-copy invariant (see `WS-WIRE-REFUSAL-FAMILY`).
4. **QUALITY EVIDENCE.** Invariant class (frozen copy). Uncurated sample: every two-pass refusal template appears in the taxonomy JSON with byte-identical text.
5. **DEPENDENCIES.** `WS-WIRE-REFUSAL-FAMILY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (taxonomy JSON extension), 0 new contracts (uses existing taxonomy shape).
7. **REVERSAL COST.** Low. Roll back the JSON entries (parity-seat new entry); render surfaces revert to no-template.

---

### C. RE-POINT items (3)

RE-POINT covers Executive-Core answering surfaces whose LLM boundary is trivially adapter-swappable (`SyniSenseContract` at `backend/contracts/synisense.py:25-28`). Paper-only.

---

#### WS-REPOINT-ANSWERING-SURFACES

1. **WHAT.** RE-POINT Executive-Core answering surfaces (chat/, documents/, analyze_workspace/, ideas_engine/, deck_*.py, inbox_routing/) onto the spine via a `SyniSenseContract` adapter swap. Component set: 8 top-level services + 36 loose service files (per Chunk-2 shaping analysis). Contract touched: `SyniSenseContract.shield_invoke` (frozen at Executive-Core `backend/contracts/synisense.py:25-28`). Record class: `Answer.Envelope` (Canon 9 §6 writer = answering surface). Task identity: `answer.compose.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §12 (six services boundary); Canon 5 §40 (Work pillar surfaces); Canon 7 §11-§12 (envelope class-chip render); Canon 4 §32 (quality matrix applies to answers).
3. **DEFINITION OF DONE.** The in-process `SyniSenseContract` adapter is replaced (paper-plan) by an HTTP adapter that calls the spine's shield endpoint. Every answer envelope carries the spine's class-chip (Canon 5 §2-§4). All four RE-POINTable surface classes (chat, documents, analyze_workspace, deck_*) surface the spine's Critic-Seam verdict (via `WS-WIRE-CRITIC-INTO-ANSWERING`). Canon 4 §32 "answer-envelope class-chip presence" parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill class (answering-day drill). Uncurated sample: 100 real answers across the 8 surfaces over one drill day; envelope shape frozen. Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-STREAMING` (Part 1 — streaming port must exist), `WS-WIRE-CRITIC-INTO-ANSWERING` (this Part 1), `WS-WIRE-LEDGER-MATRIX` (this Part 1), `WS-BUILD-CLASS-CHIP-LIBRARY` (Part 2), `WS-BUILD-ANSWER-CARD` (Part 2). Also depends on `WS-REBUILD-WORK-STUDIO-STORAGE` for the work_studio subset (partial RE-POINT until storage lands).
6. **CREDIT COST CLASS.** XL. Justification: 4+ components AND estate-wide wiring. **One-paragraph defence:** Every non-application-territory answer flow in Executive-Core routes through this adapter swap, and the swap crosses the Shield boundary, streaming port, memory plane, ledger matrix, class-chip render surface, and Critic Seam simultaneously. Sequencing missteps in any of the six integration surfaces produce answer-outage or spec violation. The estate-wide integration-surface count and the answer-path fan-out both meet the XL bar independently.
7. **REVERSAL COST.** Very high on ANY user-visible answer regression during the transition. The adapter swap is atomic per-surface but staged across surfaces; a half-swap produces two adapters live simultaneously. Reversal requires per-surface adapter restoration and a Canon-3 §24 rule-change ceremony to un-freeze the swap. Data (answers) landing during a bad-swap window are ledgered append-only; no un-write, remediation via Canon 8 §21 correction entries per bad-swap answer.

---

#### WS-REPOINT-SOLVA-V2

1. **WHAT.** RE-POINT the Executive-Core `services/solva_v2/` narration surface (30 files: analyze_narration, chair_notes, chat_v2_prompts, engines/, etc.) — surface preserved, reasoning boundary delegated to spine's `solva_depth`. Component: `services/solva_v2/`. Contract: `analyze_narration.shield_invoke` Phase-4.0 shim. Record class: `Solva.Trace` (Canon 9 §6 writer = Solva). Task identity: `solva.narration.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §14 (assertion boundary — spine owns it); Canon 5 §40 (narration as journalist-style surface); Canon 2 §6 (engine walls — narration is not extraction).
3. **DEFINITION OF DONE.** Solva-v2 narration surface remains at Executive-Core-turned-application. Every reasoning boundary call routes through spine's `solva_depth.assertion.conclusion_class`. Canon 3 §14.2 "parameterless assertion boundary" invariant holds — no narration field injects "confidence" or "caveat". Canon 4 §32 narration operative parameter goes green.
4. **QUALITY EVIDENCE.** Invariant test extending `test_conclusion_class_signature.py`. Uncurated sample: 20 solva-v2 sessions from a drill week; every reasoning delegation carries a spine Solva trace row. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-REPOINT-ANSWERING-SURFACES` (adapter path), `WS-WIRE-SOLVA-CIF` (parallel Solva-boundary hygiene), `WS-WIRE-LEDGER-MATRIX`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (analyze_narration, engines/, guardrails/, integrity_validators), 1 changed contract (adapter shim shape), 2 integration surfaces (Shield + Solva boundary).
7. **REVERSAL COST.** Medium. Reversal restores Executive-Core's private Solva narration path (a Canon-3 §14 violation, ledgered). Sessions landed under the wrong path are frozen in the ledger; new entries only.

---

#### WS-REPOINT-SOLVA-VOICE-AUDIT

1. **WHAT.** RE-POINT Executive-Core's `services/solva_voice_audit/` (24 files: voice/, orchestration/, guardrails/, reasoning/) coach-voice narration surface. Component: `services/solva_voice_audit/`. Contract: `orchestration/shield_invoker.py`. Record class: `Solva.Trace` + potentially `Input.Seat.Audio` (see fidelity ledger). Task identity: `solva.voice_audit.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §12 (input seat) — voice audit ingest touches audio material; Canon 3 §14 (assertion boundary); Canon 5 §40 (narration surface); Canon 1 §7.1 (Shield boundary).
3. **DEFINITION OF DONE.** _Partial DoD, pending resolution of fidelity-ledger entry_ **FL-P1-02:** "Does audio material transit the shield's input_seat or REBUILD is required under Canon 3 §13.1 custody sequence?" (per Chunk-2 shaping analysis). If input_seat covers audio → RE-POINT as `WS-REPOINT-SOLVA-V2`-shape. If not → this item split into REBUILD-VOICE-INPUT + RE-POINT-NARRATION. **Placeholder DoD (path A):** Voice-audit ingest routes through spine's input_seat; audio + speech-derived text carry a Solva trace and a de-identifier verdict.
4. **QUALITY EVIDENCE.** Contract test (input-seat envelope). Uncurated sample pending path resolution. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-REPOINT-ANSWERING-SURFACES`, `WS-WIRE-LEDGER-MATRIX`, and pending fidelity-ledger entry FL-P1-02.
6. **CREDIT COST CLASS.** L on path A (RE-POINT); XL on path B (REBUILD required). Reclassify after fidelity-ledger resolution.
7. **REVERSAL COST.** Medium (path A). High if audio material was ever ingested outside the input_seat during the transition (Canon 3 §12 violation; ledgered forever).

---

### D. REBUILD items (1)

REBUILD covers non-canon-conformant Executive-Core code whose storage shape can NOT be RE-POINTed cleanly — a real code migration of user-visible state.

---

#### WS-REBUILD-WORK-STUDIO-STORAGE

1. **WHAT.** Migrate `work_studio`'s 200+ real user exports (residing in `Akki-Executive-Core/uploads/work_studio_exports/`) + the deep mongo storage layer (`db.work_studio_*` across the surfaces named in `routers/studio.py` [915 L], `studio_blocks.py` [1226 L], `work_studio_export.py` [2974 L], `work_studio_from_source.py` [800 L], `work_studio_overlay.py` [828 L], `work_studio_render.py`) to Doc 7 §19-§23 per-application memory plane. Component set: work_studio backend + object-storage port + 20+ frontend components under `components/work_studio/`. Contract: `work_studio_export.v0` (currently ad hoc; to be frozen). Record class: `WorkStudio.Doc`, `WorkStudio.Version`, `WorkStudio.Lineage`. Task identity: `work_studio.storage.per_document`.
2. **CANON CLAUSES SATISFIED.** Canon 7 Part IV §19-§23 (per-application memory plane; plane-keyed storage); Canon 1 §12 (six services; storage is a service); Canon 9 §6 (record classes at the storage boundary).
3. **DEFINITION OF DONE.** All work_studio state lives behind the memory-plane reader/writer boundary. The 200+ existing exports are migrated to the plane with byte-identical fidelity (source-of-truth JSON snapshots frozen under parity seat via `WS-WIRE-PARITY-EXTENSION`). `test_memory_service_m_g1_to_m_g9.py`-shape tests exist and pass for work_studio. Canon 7 §19-§23 "plane-keyed storage" parameter goes green. Verification: Canon 3 §31 prove-one-run on one migrated document renders byte-identically pre-and-post migration.
4. **QUALITY EVIDENCE.** Invariant class (byte-identical migration replay) + drill class (migration drill). **Uncurated sample: every single one of the 200+ exports must be part of the migration corpus — no sampling.** Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** **Gates completion of `WS-REPOINT-ANSWERING-SURFACES` for work_studio subset.** Depends on **Object Storage Port (Doc 7)** — not yet a spine capability; treated as an implicit BUILD dependency captured in fidelity ledger FL-P1-03. Depends on `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1), `WS-REPOINT-WORK-STUDIO-LLM` (this Part 1).
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** The item introduces a new authority (object-storage boundary) into the spine AND is estate-wide (every work_studio subsurface touches storage) AND carries a data migration (200+ real user exports). Any of the three would qualify XL on the threshold; all three together make the review-load and reversibility risk categorically higher than any RE-POINT. This is the single most reversal-expensive Part-1 item.
7. **REVERSAL COST.** **VERY HIGH — canonical cheap-to-build/expensive-to-reverse case.** Per Ruling 2 §2 specifically: user-data migration reversibility is inherently one-way once the plane becomes source-of-truth. **Explicit user-data reversal statement:** (a) A migration that lands wrong produces two source-of-truth stores in parallel (mongo + plane) for the transition window; every document touched during the window becomes ambiguous. (b) Rollback requires either restoring mongo as source-of-truth (losing plane-only writes) OR keeping plane and losing pre-plane mongo-only edits — either choice loses user work. (c) Recommended discipline: shadow-write phase (both stores written, reader still on mongo) precedes the reader-cutover; the shadow-write phase can be reversed cheaply. Reader-cutover cannot. This item must not proceed to reader-cutover without owner sign-off on the migration certificate (Canon 6 §11-§13 commissioning certificate shape).

---

### E. RE-POINT (Work-Studio LLM boundary only)

Separated from `WS-REBUILD-WORK-STUDIO-STORAGE` because the LLM boundary is adapter-swappable independent of the storage migration.

---

#### WS-REPOINT-WORK-STUDIO-LLM

1. **WHAT.** Adapter-swap `work_studio`'s `shield_invoke` call sites onto the spine `SyniSenseContract`. Component: `work_studio/` LLM boundary only (not storage). Contract: `SyniSenseContract.shield_invoke`. Record class: `Answer.Envelope` (via `WS-REPOINT-ANSWERING-SURFACES`). Task identity: `work_studio.shield_call.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §7.1 (Shield boundary); Canon 5 §40 (Work pillar); Canon 4 §32 (envelope quality).
3. **DEFINITION OF DONE.** Every `work_studio` shield call routes through the spine adapter (part of `WS-REPOINT-ANSWERING-SURFACES`). Storage layer remains at Executive-Core mongo until `WS-REBUILD-WORK-STUDIO-STORAGE` completes. Canon 4 §32 "answer envelope class-chip presence" parameter goes green for work_studio surfaces.
4. **QUALITY EVIDENCE.** Contract test (envelope shape). Uncurated sample: 20 work_studio sessions. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** Subset of `WS-REPOINT-ANSWERING-SURFACES`; independent of `WS-REBUILD-WORK-STUDIO-STORAGE`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (LLM boundary only), 0 new contracts, 2 integration surfaces (Shield + Critic Seam).
7. **REVERSAL COST.** Low. LLM-boundary reversal is fully covered by adapter restore.

---

### F. CONTRADICTION items (1)

CONTRADICTION covers Executive-Core surfaces where the assessment found a canon-compliant surface that a strict Canon-1 §12 reading would strip. Ruling 1 governs the transition.

---

#### WS-CONTRADICTION-PURPOSE-GATE

1. **WHAT.** Executive-Core `services/synisense/shield/purpose_validator.validate_purpose()` (at `client.py:63`) purpose-enforcement gate. Component: `services/synisense/shield/purpose_validator.py`. Contract: purpose-enforcement input envelope. Record class: `Purpose.Verdict` (Canon 8 §21-§59 category). Task identity: `shield.purpose_gate.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §6.1 (actor-declaration must fire); Canon 8 §14-§15 (Watch reconciler must fire); Canon 9 §6 handoff `governance→Watch verdict`. Ruling 1 binds the transition condition.
3. **DEFINITION OF DONE.** **Under Ruling 1, DoD IS the demonstrated-firing evidence.** Specifically: (a) `WS-BUILD-DECL` (declaration seat + admit-time check + supersession — Part 2) demonstrates firing via drill; the declaration verdict is observable in the ledger for a real refusal event. (b) `WS-BUILD-WATCH-RECONCILER` (Part 2 — named by Ruling 1) demonstrates firing via drill; the Watch reconciler produces a verdict shape per Canon 8 §14-§15 for a shared-record reconciliation event. Both drill outputs are retained in the ledger and cross-cited. **Only after both demonstrations fire** may the gate strip proceed via a Canon 3 §24 rule-change ceremony (5 steps including re-verified — see `WS-BUILD-CEREMONY-REVERIFY`). Until then: gate STANDS as a canon-compliant surface at Executive-Core HEAD. The strip event itself is a distinct future item, ledgered separately.
4. **QUALITY EVIDENCE.** Two drill records (one per prerequisite) in the ledger; parity-seat entries for the two new contracts (declaration verdict, Watch reconciler verdict) via `WS-WIRE-PARITY-EXTENSION`. Uncurated sample: at minimum one drill day covering each prerequisite. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** **GATED BY `WS-BUILD-DECL` AND `WS-BUILD-WATCH-RECONCILER`** (both Part 2 BUILD items). Also depends on `WS-BUILD-CEREMONY-REVERIFY` (this Part 1) for the strip ceremony's re-verify step. Also `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (the gate itself), 0 new contracts on retain-phase (evidence is written to existing ledger + Watch mark register), 2 integration surfaces (declaration verdict input + Watch reconciler input). Reclassify to S when strip-phase-only.
7. **REVERSAL COST.** **Very low during retain phase** (gate is doing its stated work). **Very high if stripped prematurely** (before both demonstrations fire) — this is a Canon-1 §7.1 authority breach that ledgers append-only and cannot be un-written; every downstream Shield call taken with the gate down is a Canon-3 §6.1 violation. Ruling 1 IS the safeguard against premature strip.

---

### G. RETIRE items (4 concrete + 1 rename = 5)

Concrete RETIRE clusters cite Canon 1 §12/§13/§15 or Canon 5 §43 (no bypass path).

---

#### WS-RETIRE-APP-TERRITORY

1. **WHAT.** Retire application-territory duplicates from the platform layer: Executive-Core `services/cohort/` (8 files) + `stripe_webhook.py` + `owner_digest.py` + `news_aggregator.py` + `first_login_password_set.py` + `platform_kb.py` + `backfill_shield_v1.py`. Component set: 15+ loose Executive-Core services (per `notes/retire_inventory.md`). Contract: none touched (retirement removes calls, no new contract). Record class: N/A (retiring writes, not new records). Task identity: `retire.app_territory.per_service`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §12 (six services boundary); Canon 1 §13 (same boundary for every application); Canon 1 §15 (no commerce — verbatim: "will not know a buyer, a price, or an order").
3. **DEFINITION OF DONE.** Every named service either (a) moves to the application layer of Executive-Core-turned-application, OR (b) deletes on migration completion. Platform boundary contains none of the listed files. Canon 1 §12 "six-services boundary invariant" AST discipline holds (no application-territory import from platform code). Verification: prove-one-run for a platform request has zero call sites into the retired names.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped import discipline). Uncurated sample: full platform request log for a drill week; zero platform→app-territory imports. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** Executive-Core-as-application transition boundary — implicit; captured in fidelity ledger FL-P1-04 if not yet defined at the programme level.
6. **CREDIT COST CLASS.** M. Justification: 8+ components across the list, 0 new contracts (retirement, not creation), 1 integration surface (application-boundary discipline).
7. **REVERSAL COST.** Low for the platform (retirement is subtractive). For the application layer, un-retirement = restore the code from git; no data motion required (application state was never at the platform boundary).

---

#### WS-RETIRE-XCUT-SECURITY

1. **WHAT.** Retire cross-cutting security duplicates: `services/csrf.py`, `rate_limit.py`, `rbac.py`, `security_headers.py`, `session_timeout.py`, `sentry_setup.py`, `privacy_wall.py`, `clamav_service.py` (Executive-Core; 8 files). Task identity: `retire.xcut_security.per_service`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §11 (the Shell — no bypass path); Canon 1 §7.1 (peer authorities); Canon 3 §30 (Enforcement Class — Watch territory).
3. **DEFINITION OF DONE.** Cross-cutting security lives ONCE — either at platform (its canon home) or at application; not duplicated across the boundary. Platform's own security surface passes Canon 5 §11 no-bypass invariant. Verification: AST discipline confirms no application-side rate-limiter/csrf/rbac call intercepts a platform request.
4. **QUALITY EVIDENCE.** Invariant class (AST discipline). Uncurated sample: full platform request log for a drill week; zero application-security interceptions. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** As `WS-RETIRE-APP-TERRITORY`.
6. **CREDIT COST CLASS.** M. Justification: 8 components (loose files), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Low.

---

#### WS-RETIRE-FRONTEND-ARCHIVES

1. **WHAT.** Retire codebase-self-marked archives: `frontend/src/_archived/` (61 files), `frontend/src/_archived_legacy/`, `frontend/src/_archived_coverage_loss/`, and `frontend/src/website/` (34 files, marketing). Task identity: `retire.frontend_archives.per_directory`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §43 (no surface offers bypass/override); Canon 1 §12-§13 (marketing website is application/commercial territory).
3. **DEFINITION OF DONE.** Archived directories removed from platform frontend deployment. Marketing website continues at application-layer (or standalone). Canon 5 §43 no-bypass invariant confirmed by inventory: only Canon 5 §10 four-console surfaces + Canon 5 §40 five-pillar surfaces render.
4. **QUALITY EVIDENCE.** Inventory audit (surface-list) + invariant class (no-bypass at the router). Uncurated sample: full frontend surface list for the drill week; every rendered route maps to a Canon 5 anchor.
5. **DEPENDENCIES.** As `WS-RETIRE-APP-TERRITORY`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (frontend surface list), 0 new contracts.
7. **REVERSAL COST.** Very low (files are in git).

---

#### WS-RETIRE-PROTOTYPE-DIVERGENCE

1. **WHAT.** Retire prototype-only surfaces that lack a Canon-5 anchor: `hrstuff` (Collab > HR Stuff), `datashield/reasoningshield/accessshield` naming, `compute` (Registry > Compute), `tasks` (WorkStudio > Task Manager), `mentions/emails/projects` (Collab). Task identity: `retire.prototype_divergence.per_surface`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §40 (fixed five-pillar taxonomy); Canon 5 §43 (no bypass); Canon 1 §13 (application territory).
3. **DEFINITION OF DONE.** Every prototype nav item that lacks a Canon 5 anchor is removed from the platform surface OR moved to application territory. Verification: canon-5 conformance audit shows 100% of platform nav items map to Canon 5 §40 pillars or §10 consoles.
4. **QUALITY EVIDENCE.** Inventory audit (nav-list vs Canon 5 anchors). Uncurated sample: full prototype nav list vs Canon 5 §10/§40 anchor list; delta = 0.
5. **DEPENDENCIES.** None (prototype is documentation/design only).
6. **CREDIT COST CLASS.** S. Justification: 1 component (prototype file), 0 new contracts.
7. **REVERSAL COST.** Zero (prototype-only).

---

#### WS-RENAME-PROTOTYPE-TAXONOMY

1. **WHAT.** Rename prototype labels to Canon 5 §10/§40 taxonomy: `WorkStudio → Work`, `ThinkLab / Monitor → Lead pillar sub-applications`, `Trust Center → Compliance Console`, `Registry → Extraction Console child + Control Band`, `Build → Build pillar (add Studio + Learn)`, `3rd Party Apps → 3rd Party pillar with Integration Console + app catalogue`. Task identity: `rename.prototype_taxonomy.per_label`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §40 (five pillars); Canon 5 §41 (Control Band).
3. **DEFINITION OF DONE.** Every prototype label renamed per the table in `notes/retire_inventory.md`. Canon-5 conformance audit shows 100% label-canon alignment. Verification: inventory diff between prototype pre-rename and Canon 5 anchors returns zero mismatch.
4. **QUALITY EVIDENCE.** Inventory audit. Uncurated sample: prototype label list post-rename.
5. **DEPENDENCIES.** None.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts.
7. **REVERSAL COST.** Zero.

---

### H. MODIFY / PARTIAL items (4)

MODIFY / PARTIAL covers existing code that must be extended to close an operative-parameter gap the assessment classified PARTIAL.

---

#### WS-BUILD-INDEPENDENCE-GATE

1. **WHAT.** Machine-checked reviewer-independence gate. Rows C2-012, C3-028, C7-D11 PARTIAL. Component: reviewer-selector code path (existing at Extraction-Akki; specific file to be identified via a focused read — fidelity-ledger FL-P1-05). Contract: reviewer-selection input envelope. Record class: `Independence.Verdict`. Task identity: `governance.independence_gate.per_selection`.
2. **CANON CLAUSES SATISFIED.** Canon 2 §12 (independence-rule machine-checked); Canon 3 §28 (reviewer-selector independence gate); Canon 7 §D11 (defect: independence hard-check).
3. **DEFINITION OF DONE.** Every reviewer selection passes an independence rule (Canon 3 §28) applied at machine speed; failing selections refuse with a canon-cited reason recorded in the ledger. Verification: drill with a deliberately-conflicted selector fixture triggers the refusal.
4. **QUALITY EVIDENCE.** Invariant class (independence rule at selector). Uncurated sample: 20 real reviewer selections across a drill week; independence rule fires as expected.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX`, `WS-WIRE-CRITIC-INTO-ANSWERING` (independence applies to critic reviewers), `WS-BUILD-RECORD-MATRIX` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components (selector + rule table), 1 new/changed contract (independence-verdict envelope), 2 integration surfaces.
7. **REVERSAL COST.** Low-medium. Reversal restores non-machine-checked selection — a Canon 3 §28 violation, ledgered forever.

---

#### WS-BUILD-DELIVERABLE-ATTESTATIONS

1. **WHAT.** Contents / privacy / quality attestation surface uplift (rows C4-056..C4-060 PARTIAL). Component: delivery-attestation surface (needs specific file identification — fidelity-ledger FL-P1-06). Contract: `Deliverable.Attestation.v0`. Record class: `Deliverable.Attestation`. Task identity: `deliverable.attest.per_delivery`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §50-§60 (contents/privacy/quality attestations at delivery).
3. **DEFINITION OF DONE.** Every deliverable carries a three-field attestation (contents / privacy / quality) rendered on the answer surface AND recorded to the ledger. Missing attestations fail closed. Verification: prove-one-run of one delivered answer shows the three attestations verbatim.
4. **QUALITY EVIDENCE.** Contract test (attestation shape) + drill (delivery drill). Uncurated sample: 20 real deliveries across a drill week; every one carries all three attestations.
5. **DEPENDENCIES.** `WS-WIRE-CRITIC-INTO-ANSWERING`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-ANSWER-CARD` (Part 2), `WS-BUILD-CLASS-CHIP-LIBRARY` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract (attestation envelope).
7. **REVERSAL COST.** Low. Reversal removes attestations from surfaces (Canon 4 §50 violation, ledgered).

---

#### WS-BUILD-CEREMONY-REVERIFY

1. **WHAT.** Canon 3 §24 rule-change ceremony's 5th "re-verified" step (row C3-033 PARTIAL, added by Chunk-3 A.2). Component: `services/checker/rule_change_request.py` + `state_machine.py` (existing; add re-verify state). Contract: rule-change ceremony state-machine shape (frozen at `test_govern_g_g1_to_g_g8.py`). Record class: `Ceremony.RuleChange`. Task identity: `ceremony.rule_change.per_change`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §24 (five-step ceremony: proposed → counter-signed → waited → applied → re-verified).
3. **DEFINITION OF DONE.** Every rule-change ceremony completes only after the 5th "re-verified" state is entered — a re-verification pack (Canon 3 §31 shape) fires against the applied rule and its Verdict is written to the ledger. Verification: drill with one full rule-change ceremony end-to-end; state-machine trace shows all five states.
4. **QUALITY EVIDENCE.** Invariant class (state-machine trace). Uncurated sample: every rule-change ceremony over a drill week completes with re-verify state. Calibration under Canon 3 §31 verification pack shape.
5. **DEPENDENCIES.** `WS-BUILD-VERIFICATION-RUNNER` (Part 2 — the re-verify runner surface), `WS-WIRE-LEDGER-MATRIX`. **Also gates `WS-CONTRADICTION-PURPOSE-GATE` strip ceremony.**
6. **CREDIT COST CLASS.** M. Justification: 1 component (checker), 1 changed contract (state-machine adds a state), 2 integration surfaces (ceremony + verification runner).
7. **REVERSAL COST.** Medium. Reversal drops the re-verify state — every ceremony landing during the reversal window carries a Canon-3 §24 partial completion (ledgered). No rule-change is un-applied by a state-machine reversal.

---

#### WS-BUILD-STANDING-QUERY-SURFACE

1. **WHAT.** Standing queries surface for compliance-owner review (rows C7-029..C7-031 PARTIAL). Component: `services/checker/` or Compliance-Console standing-query path (specific file — fidelity-ledger FL-P1-07). Contract: `StandingQuery.Definition.v0`. Record class: `Compliance.StandingQuery`. Task identity: `compliance.standing_query.per_review`.
2. **CANON CLAUSES SATISFIED.** Canon 7 §29-§31 (standing queries for compliance owners).
3. **DEFINITION OF DONE.** Compliance owner can define, list, and execute standing queries against ledgered state; each execution records a `Compliance.StandingQuery` row. Verification: drill with a compliance owner running three standing queries over a drill week.
4. **QUALITY EVIDENCE.** Contract test (query shape). Uncurated sample: 20 standing-query executions across a drill week.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-CONSOLE-COMPLIANCE` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components (query definition + execution surface), 1 new contract (standing-query shape), 1 integration surface (ledger reader).
7. **REVERSAL COST.** Low. Reversal removes the surface; compliance owner reverts to ad hoc reads (Canon 7 §29 gap).

---

### Part-1 item count summary

| Class | Count | Items |
|---|---:|---|
| WIRING | 11 | WS-WIRE-{CUSTODY-DECL, REGISTRY, LOOP-ORCH, SOLVA-CIF, INTENT-AUDIT-WATCH, WATCH-PLANE-ACTIVITY, ADMISSION-HANDOFF, CRITIC-INTO-ANSWERING (Ruling 2), PARITY-EXTENSION (Ruling 2), REFUSAL-FAMILY (Ruling 2), LEDGER-MATRIX (Ruling 2)} |
| HARVEST (non-interface) | 9 | WS-HARVEST-{CRITIC-SEAM, BATCH-QUARANTINE, GAP-FILER, REGISTRY-CONTEXT, PARTITIONS, SEQUENCING-HARNESS, FAR-ENDPOINT, STREAMING, TWO-PASS-AMENDMENT} |
| RE-POINT | 4 | WS-REPOINT-{ANSWERING-SURFACES, SOLVA-V2, SOLVA-VOICE-AUDIT, WORK-STUDIO-LLM} |
| REBUILD | 1 | WS-REBUILD-WORK-STUDIO-STORAGE |
| CONTRADICTION | 1 | WS-CONTRADICTION-PURPOSE-GATE |
| RETIRE (concrete + rename) | 5 | WS-RETIRE-{APP-TERRITORY, XCUT-SECURITY, FRONTEND-ARCHIVES, PROTOTYPE-DIVERGENCE} + WS-RENAME-PROTOTYPE-TAXONOMY |
| MODIFY/PARTIAL (non-interface) | 4 | WS-BUILD-{INDEPENDENCE-GATE, DELIVERABLE-ATTESTATIONS, CEREMONY-REVERIFY, STANDING-QUERY-SURFACE} |
| **INTERFACE HARVEST/MODIFY (Ruling 3)** | **13** | See §I below |
| **Part-1 Total** | **47** | (11 + 9 + 4 + 1 + 1 + 5 + 4 + 13). |

**Fidelity ledger entries opened in this file:** FL-P1-01 (sequencing_harness canon anchor), FL-P1-02 (audio input-seat), FL-P1-03 (Object Storage Port BUILD), FL-P1-04 (application-boundary transition), FL-P1-05 (independence-gate specific file), FL-P1-06 (attestation-surface specific file), FL-P1-07 (standing-query specific file), FL-P1-08 through FL-P1-19 (rendering decisions from §I).

---

### I. INTERFACE strategy (Ruling 3 / Instruction 02)

Per Instruction 02: Extraction-Akki's frontend is the DONOR. Every existing page/menu is either repurposed into the Admin surface's **tile-grid-plus-detail-card grammar** (as HARVEST or MODIFY) OR classified RETIRE with a reason. The Watch is the fourth tile-group of four tiles (`State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13), remains BUILD, watch-officer-role gated, sessions under Watch identity per Canon 9, **NEVER nested under Trust Center**.

Reference screenshot pending arrival in workspace — recorded on every interface item as **`FIXTURE CLEARED @ transcription grade — see `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13); `test_four_questions_topline_present` added to new-invariants list per Build Order 01 §3`**.

#### I.1 Extraction-Akki frontend inventory (verified at HEAD b150c21)

44 production pages across 12 menu groups + 10 shell/component files:

| Group (dir) | Pages | Type |
|---|---|---|
| Root shell | `CanonOSShellPage.jsx` | Root shell — tile-grid grammar donor |
| Design | `AkkiShell.jsx`, `AkkiV4Shell.jsx`, `AkkiV4ShellLayout.jsx`, `MarkedOpenSlot.jsx`, `ResponseClassPanel.jsx`, `akkiv4_design_system.js`, `ratified_copy.js` | Shell primitives |
| Components | `RetentionPostureBadge.jsx`, `CounterSignBanner.jsx`, `AuthDeniedNotice.js`, `ClassBadge.js`, `EngineCard.js`, `LedgerTable.js`, `OuterGateReceiptInline.js`, `RefusalCard.js`, `StatusBadge.js`, `TrustReceiptLink.js` | Reusable atoms |
| Connect | `ConnectHomePage`, `ConnectNewSourcePage`, `ConnectRulesPage`, `ConnectSetupPage`, `ConnectSourceProfilePage`, `ConnectV4Page` | 6 pages |
| Govern | `GovernChangeRulePage`, `GovernEstateRulesPage`, `GovernHoldsPage`, `GovernHomePage`, `GovernPendingPage`, `GovernRefusalHealthPage`, `GovernRegistriesPage`, `GovernRetentionPage` | 8 pages |
| Registry | `RegistryArtifactV4Page`, `RegistryEstateMapPage`, `RegistryV4Page`, `RegistryWhatYouHoldPage` | 4 pages |
| Memory | `MemoryHomePage`, `MemoryPlaneDetailPage`, `MemoryPlaneObservabilityPage` | 3 pages |
| Team | `TeamAccessRegisterPage`, `TeamApprovalSurfacePage`, `TeamConstitutionalSeatsPage`, `TeamLandingPage` | 4 pages |
| Trace | `TraceReceiptPage` | 1 page |
| Use Data | `UseDataDeveloperSurfacePage`, `UseDataLandingPage`, `UseDataVerdictDemoPage`, `UseDataVerdictPanel`, `UseDataWizardPage` | 5 pages |
| Prove | `ProvePage`, `ProveWalkPage`, `ProveDormantPage` | 3 pages |
| Commission View | `CommissionRunDetailPage`, `CommissionViewHomePage` | 2 pages |
| Master Admin | `AdminComplianceReadOnlyView`, `AuditTrailPage`, `ChangeARulePage`, `MasterAdminHomePage` | 4 pages |
| Team Dormant | `TeamDormantPage` | 1 page |
| Auth | `AuthLoginPage`, `AuthRegisterPage` | 2 pages |

Total: 44 pages + 10 shell/component files.

#### I.2 Menu-to-app mapping table (every existing page)

Column key: **Tile** = Admin-surface tile name (the "app" as user sees it) · **Group** = one of the four Canon-5 §10 consoles (Extraction / Compliance / Integration / Administration) OR Watch (Instruction 02 fourth group) OR RETIRE · **Canon Identity** = the Canon-5 or Canon-8 clause the tile satisfies · **Class** = HARVEST or MODIFY or RETIRE · **Item** = the Part-1 WS-item ID that owns the repurposing.

| Extraction-Akki page | Tile | Group | Canon Identity | Class | Item |
|---|---|---|---|---|---|
| `CanonOSShellPage.jsx` | (shell frame) | Root | Canon 5 §11 The Shell | HARVEST | WS-HARVEST-SHELL-GRAMMAR |
| `AkkiShell.jsx` | (shell primitive) | Root | Canon 5 §11 | HARVEST | WS-HARVEST-SHELL-GRAMMAR |
| `AkkiV4Shell.jsx` | (shell primitive) | Root | Canon 5 §11 | HARVEST | WS-HARVEST-SHELL-GRAMMAR |
| `AkkiV4ShellLayout.jsx` | (shell primitive) | Root | Canon 5 §11 | HARVEST | WS-HARVEST-SHELL-GRAMMAR |
| `MarkedOpenSlot.jsx` | (shell primitive) | Root | Canon 5 §11 | HARVEST | WS-HARVEST-SHELL-GRAMMAR |
| `ResponseClassPanel.jsx` | (component) | (reusable) | Canon 5 §2-§4 class chip | HARVEST | WS-HARVEST-CLASS-CHIP-LIBRARY |
| `ClassBadge.js` | (component) | (reusable) | Canon 5 §2 class chip | HARVEST | WS-HARVEST-CLASS-CHIP-LIBRARY |
| `RetentionPostureBadge.jsx` | (component) | (reusable) | Canon 5 §22-§23 retention posture | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `CounterSignBanner.jsx` | (component) | (reusable) | Canon 3 §24 ceremony banner | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `AuthDeniedNotice.js` | (component) | (reusable) | Canon 5 §43 (denied ≠ refusal card) | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `EngineCard.js` | (component) | (reusable) | Canon 1 §7 engine wall render | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `LedgerTable.js` | (component) | (reusable) | Canon 1 §4.3 ledger render | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `OuterGateReceiptInline.js` | (component) | (reusable) | Canon 4 §16 frozen unit receipt | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `RefusalCard.js` | (component) | (reusable) | Canon 5 §9.2 refusal card | HARVEST | WS-HARVEST-REFUSAL-CARD (couples with WS-WIRE-REFUSAL-FAMILY) |
| `StatusBadge.js` | (component) | (reusable) | Canon 5 §43-§65 sensor render | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `TrustReceiptLink.js` | (component) | (reusable) | Canon 4 §16 trust receipt | HARVEST | WS-HARVEST-COMPONENT-LIBRARY |
| `ConnectHomePage.jsx` | Connect | Integration Console | Canon 5 §24-§25 (Integration / Register first-call) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `ConnectNewSourcePage.jsx` | New Source | Integration Console | Canon 5 §27 (Register) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `ConnectRulesPage.jsx` | Rules | Integration Console | Canon 5 §29 (Dual-actor scoping) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `ConnectSetupPage.jsx` | Setup | Integration Console | Canon 6 §3.1 setup declarations | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `ConnectSourceProfilePage.jsx` | Source Profile | Integration Console | Canon 5 §28 (Administer connectors) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `ConnectV4Page.jsx` | Connect V4 | Integration Console | Canon 5 §26-§28 (Integration home) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `GovernHomePage.jsx` | Compliance Home | Compliance Console | Canon 5 §22 (Compliance Home) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `GovernRetentionPage.jsx` | Retention & Rights | Compliance Console | Canon 5 §24 (Retention & Rights) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `GovernHoldsPage.jsx` | Holds | Compliance Console | Canon 5 §24 (Holds panel — Retention & Rights) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `GovernRefusalHealthPage.jsx` | Refusal Health | Compliance Console | Canon 5 §22 + Canon 5 §9.2 refusal telemetry | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE (couples WS-WIRE-REFUSAL-FAMILY) |
| `GovernPendingPage.jsx` | Pending Ceremonies | Administration Console | Canon 3 §24 (pending countersign — Canon 5 §35 Counter-Sign Duties) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `GovernChangeRulePage.jsx` | Change a Rule | Administration Console | Canon 5 §32 (Change a Rule) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION (couples WS-BUILD-CEREMONY-REVERIFY) |
| `GovernEstateRulesPage.jsx` | Estate Rules | Administration Console | Canon 5 §25 (Compliance Rulebook) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE (rulebook belongs at Compliance Home) |
| `GovernRegistriesPage.jsx` | Registries | Administration Console | Canon 5 §17 (Registry Administration) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `RegistryV4Page.jsx` | Extraction Home | Extraction Console | Canon 5 §13 (Extraction Registry Dashboard) | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `RegistryEstateMapPage.jsx` | Estate Map | Extraction Console | Canon 5 §17 (Estate Map — Control Band) | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `RegistryArtifactV4Page.jsx` | Artifact Detail | Extraction Console | Canon 5 §13-§14 artefact card | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `RegistryWhatYouHoldPage.jsx` | What You Hold | Extraction Console | Canon 5 §17 (holdings inventory) | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `MemoryHomePage.jsx` | Memory Home | Extraction Console | Canon 5 §17 (Extraction Console — memory) | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `MemoryPlaneDetailPage.jsx` | Plane Detail | Extraction Console | Canon 7 §19-§23 memory plane | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `MemoryPlaneObservabilityPage.jsx` | Plane Observability | Compliance Console | Canon 7 §29-§31 standing queries + Canon 3 §31 prove-one-run | MODIFY | WS-MODIFY-PLANE-OBSERVABILITY (rehome to Compliance — RENDERING DECISION FL-P1-08) |
| `TeamLandingPage.jsx` | Team Home | Administration Console | Canon 5 §34 (Roles & Rights) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `TeamAccessRegisterPage.jsx` | Access Register | Administration Console | Canon 5 §34 (Roles & Rights — access register) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `TeamApprovalSurfacePage.jsx` | Approval Surface | Administration Console | Canon 5 §35 (Counter-Sign Duties) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `TeamConstitutionalSeatsPage.jsx` | Constitutional Seats | Administration Console | Canon 1 §7.1 peer authorities + Canon 3 §28 independence | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION (couples WS-BUILD-INDEPENDENCE-GATE) |
| `TraceReceiptPage.js` | Trace Receipt | Compliance Console | Canon 3 §33-§48 prove-one-run export | MODIFY | WS-MODIFY-PROVE-ONE-RUN-EXPORT (rehome — RENDERING DECISION FL-P1-09) |
| `ProvePage.jsx` | Prove | Compliance Console | Canon 5 §23 (Prove-one-run) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `ProveWalkPage.jsx` | Prove Walk | Compliance Console | Canon 5 §23 (Prove-one-run walk) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `ProveDormantPage.jsx` | Prove (Dormant) | Compliance Console | Canon 5 §9 (dormant state render) | HARVEST | WS-HARVEST-DORMANT-STATE (couples WS-BUILD-DORMANT-STATE-RENDER moved to Part 1) |
| `TeamDormantPage.jsx` | Team (Dormant) | Administration Console | Canon 5 §9 (dormant state render) | HARVEST | WS-HARVEST-DORMANT-STATE |
| `UseDataLandingPage.jsx` | Use Data | Extraction Console | Canon 5 §14 (Model Catalogue) OR Canon 5 §43 (Reference App — Ask) | MODIFY | WS-MODIFY-USE-DATA-PLACEMENT (see FL-P1-10 rendering decision — Ask app or Extraction Model Catalogue?) |
| `UseDataWizardPage.jsx` | Use Data Wizard | Extraction Console | Canon 5 §15-§17 shaping wizard | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `UseDataVerdictDemoPage.jsx` | Verdict Demo | Extraction Console | Canon 4 §7 (verdict is a matrix lookup — demo) | MODIFY | WS-MODIFY-VERDICT-DEMO (may retire as demo-only — FL-P1-11) |
| `UseDataVerdictPanel.jsx` | Verdict Panel | Extraction Console | Canon 4 §7 verdict panel | HARVEST | WS-HARVEST-CONSOLE-EXTRACTION |
| `UseDataDeveloperSurfacePage.jsx` | Developer Surface | Integration Console | Canon 5 §29 (Dual-actor scoping — developer surface) | HARVEST | WS-HARVEST-CONSOLE-INTEGRATION |
| `CommissionViewHomePage.jsx` | Commissioning | Compliance Console | Canon 6 §11-§13 (commissioning certificates) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `CommissionRunDetailPage.jsx` | Commissioning Run | Compliance Console | Canon 6 §11-§13 (commissioning run detail) | HARVEST | WS-HARVEST-CONSOLE-COMPLIANCE |
| `MasterAdminHomePage.js` | Admin Home | Administration Console | Canon 5 §31 (Administration Home) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `AdminComplianceReadOnlyView.jsx` | Admin Compliance | Administration Console | Canon 5 §31 (read-only compliance view for admin) | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION |
| `AuditTrailPage.js` | Audit Trail | Compliance Console | Canon 3 §33 (audit-trail export) | MODIFY | WS-MODIFY-AUDIT-TRAIL-PLACEMENT (rehome to Compliance — FL-P1-12) |
| `ChangeARulePage.js` | Change a Rule (Admin) | Administration Console | Canon 5 §32 | HARVEST | WS-HARVEST-CONSOLE-ADMINISTRATION (dedupe with GovernChangeRulePage — FL-P1-13) |
| `AuthLoginPage.js` | (auth surface) | RETIRE | Canon 1 §13 application-territory auth | RETIRE | WS-RETIRE-APP-TERRITORY (existing item; add these pages) |
| `AuthRegisterPage.js` | (auth surface) | RETIRE | Canon 1 §13 application-territory auth | RETIRE | WS-RETIRE-APP-TERRITORY |

**Coverage:** 44/44 production pages mapped. 42 HARVEST, 5 MODIFY (rendering decisions FL-P1-08 through FL-P1-13), 2 RETIRE (auth). No unmapped page.

**Missing donor pages (Extraction-Akki has no page for these Canon-5 requirements; remain Part-2 BUILD):**
- Watch Console (`WS-BUILD-CONSOLE-WATCH`) — REMAINS BUILD per Instruction 02 (with new placement constraint).
- Extraction Console `Model Catalogue` (`WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE`) — no Extraction-Akki donor; stays BUILD.
- Batch Board (`WS-BUILD-BATCH-BOARD-SURFACE`) — stays BUILD.
- Quality Observation (`WS-BUILD-QUALITY-OBSERVATION`) — stays BUILD.
- Setup / Day-Zero consoles (`WS-BUILD-SETUP-CONSOLE`, `WS-BUILD-DAY-ZERO`) — stay BUILD (Canon 6 §3.1 setup surface).
- Answering surface set: Three Lenses (`WS-BUILD-THREE-LENSES`), Answer Card (`WS-BUILD-ANSWER-CARD`), Agent Assumed Chip (`WS-BUILD-AGENT-ASSUMED-CHIP`), Refusal Card Copy verbatim (`WS-BUILD-REFUSAL-CARD-COPY` — the copy itself is a BUILD; harvest is only of the shell component) — stay BUILD.
- Five Pillars router (`WS-BUILD-FIVE-PILLARS`), Pulse News (`WS-BUILD-PULSE-NEWS`), Studio (`WS-BUILD-STUDIO`), Learn Pillar (`WS-BUILD-LEARN-PILLAR`), Reference App (`WS-BUILD-REFERENCE-APP`), Control Band (`WS-BUILD-CONTROL-BAND`) — stay BUILD (no donor).
- Verification Runner (`WS-BUILD-VERIFICATION-RUNNER`), Prove-one-run generator (`WS-BUILD-PROVE-ONE-RUN`), Rulebook read-back (`WS-BUILD-RULEBOOK-SURFACE`) — stay BUILD.

#### I.3 Interface work items (Part 1, HARVEST/MODIFY)

Twelve items own the 44-page repurposing plus one shell-grammar item. All carry the `FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` cited; `test_four_questions_topline_present` on new-invariants list` field.

---

#### WS-HARVEST-SHELL-GRAMMAR

1. **WHAT.** Repurpose Extraction-Akki's `CanonOSShellPage.jsx` + `design/AkkiShell.jsx` + `AkkiV4Shell.jsx` + `AkkiV4ShellLayout.jsx` + `MarkedOpenSlot.jsx` + `akkiv4_design_system.js` + `ratified_copy.js` as the tile-grid-plus-detail-card grammar host — the Admin-surface shell. Components: 7 shell primitives. Contract: shell layout contract (tile-grid + detail-card render pass). Record class: N/A (surface-only). Task identity: `interface.shell.tile_grid`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md`; `test_four_questions_topline_present` on new-invariants list.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §11 (The Shell — no bypass path); Canon 5 §10 (five consoles hosted per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §43 (no bypass path); Instruction 02 (tile-grid-plus-detail-card grammar).
3. **DEFINITION OF DONE.** Every page listed in §I.2 renders inside the shell as an app tile in one of four groups (Extraction / Compliance / Integration / Administration) OR the Watch fourth-group. No page bypasses the shell. Canon 5 §43 no-bypass invariant holds. Shell placement invariant test asserts each tile carries its group + canon identity metadata. Verification: nav audit — 100% of rendered routes carry `(tile, group, canon_identity)` triple.
4. **QUALITY EVIDENCE.** Invariant class (shell-placement gate) + inventory audit (nav-to-tile mapping). Uncurated sample: every route rendered during a drill day. Calibration under Canon 3 §31 + Canon 5 §43.
5. **DEPENDENCIES.** Reference screenshot (fixture pending — fidelity ledger FL-P1-14). No inward code dependencies (primitives are donor-ready).
6. **CREDIT COST CLASS.** L. Justification: 3+ components (7 shell primitives) AND a new register/console surface (the tile-grid grammar itself is the register).
7. **REVERSAL COST.** Medium. Reversal restores Extraction-Akki's V4Shell as-is (no grammar overlay); every tile falls back to standalone routing — a Canon-5 §11 partial-shell state (ledgered). Data untouched.

---

#### WS-HARVEST-CONSOLE-EXTRACTION

1. **WHAT.** Repurpose Extraction-Akki `pages/registry/` (4 pages) + `pages/memory/MemoryHomePage.jsx`, `MemoryPlaneDetailPage.jsx` + `pages/use_data/UseDataWizardPage.jsx`, `UseDataVerdictPanel.jsx` into the Extraction Console tile-group. 8 pages harvested; each becomes an app tile in the Extraction Console tile-group. Contract: Extraction Console tile-list. Record class: `Console.Extraction.Registration`. Task identity: `interface.console.extraction`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §13-§14 (Extraction Registry Dashboard + Model Catalogue); Canon 5 §17 (Registry Administration — Estate Map); Canon 7 §19-§23 (Memory planes surface); Instruction 02 (tile grammar).
3. **DEFINITION OF DONE.** Extraction Console tile-group hosts 8 donor tiles with canon identity per §I.2 table. Model Catalogue tile appears as a BUILD-marked open slot per `WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE` (Part 2); Batch Board tile appears as BUILD-marked slot per `WS-BUILD-BATCH-BOARD-SURFACE`. Canon 5 §13-§17 operative parameters go green for the harvested tiles; open-slot tiles carry Canon 5 §9 dormant-state copy.
4. **QUALITY EVIDENCE.** Inventory audit (tile-list-to-canon-identity mapping) + invariant class (tile placement in group). Uncurated sample: every route under Extraction Console during a drill day. Calibration under Canon 5 §10 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending (FL-P1-14).
6. **CREDIT COST CLASS.** L. Justification: 8 pages (3+ components), new register/console surface (Extraction Console tile-group), 2 integration surfaces (shell + component library).
7. **REVERSAL COST.** Medium. Reversal restores standalone routes; group binding is metadata (reversible via matrix new-entry). No data changes.

---

#### WS-HARVEST-CONSOLE-COMPLIANCE

1. **WHAT.** Repurpose `pages/prove/ProvePage.jsx`, `ProveWalkPage.jsx` + `pages/govern/GovernHomePage.jsx`, `GovernRetentionPage.jsx`, `GovernHoldsPage.jsx`, `GovernRefusalHealthPage.jsx`, `GovernEstateRulesPage.jsx` + `pages/commission_view/CommissionViewHomePage.jsx`, `CommissionRunDetailPage.jsx` into the Compliance Console tile-group. 9 pages. Also picks up `MemoryPlaneObservabilityPage.jsx` and `TraceReceiptPage.js` and `AuditTrailPage.js` via MODIFY (rehome — see FL-P1-08/09/12). Contract: Compliance Console tile-list. Record class: `Console.Compliance.Registration`. Task identity: `interface.console.compliance`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §22-§26 (Compliance Home, Prove-one-run, Retention & Rights, Rulebook, rule-on-paper flag); Canon 3 §33-§48 (prove-one-run export); Canon 6 §11-§13 (commissioning); Canon 3 §31 (verification packs).
3. **DEFINITION OF DONE.** Compliance Console tile-group hosts the 9 donor tiles + 3 rehomed MODIFY tiles (12 total). Rulebook read-back tile lives at Compliance Home (Canon 5 §25 says rulebook lives here, not Administration — hence `GovernEstateRulesPage.jsx` rehomes). `WS-BUILD-VERIFICATION-RUNNER`, `WS-BUILD-PROVE-ONE-RUN`, `WS-BUILD-RULEBOOK-SURFACE` (Part-2 BUILD items) surface here as BUILD-marked open slots per Canon 5 §9. Canon 5 §22-§26 operative parameters go green for harvested tiles.
4. **QUALITY EVIDENCE.** Inventory audit + invariant (tile placement). Uncurated sample: every Compliance-Console route during a drill day. Calibration under Canon 3 §31 + Canon 5 §22.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`, `WS-WIRE-REFUSAL-FAMILY` (for GovernRefusalHealthPage), `WS-BUILD-CEREMONY-REVERIFY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** L. Justification: 9-12 pages, new console tile-group, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

#### WS-HARVEST-CONSOLE-INTEGRATION

1. **WHAT.** Repurpose `pages/connect/` (6 pages) + `pages/use_data/UseDataDeveloperSurfacePage.jsx` into the Integration Console tile-group. 7 pages. Contract: Integration Console tile-list. Record class: `Console.Integration.Registration`. Task identity: `interface.console.integration`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §26-§29 (Integration Console: Home + First-call + Administer + Dual-actor scoping); Canon 6 §3.1 (setup declarations).
3. **DEFINITION OF DONE.** Integration Console tile-group hosts 7 donor tiles. Every Canon 5 §26-§29 tile presents with its canon identity. `WS-BUILD-WEBHOOK` (Part-2 BUILD) surfaces here as BUILD-marked open slot. Canon 5 §26-§29 operative parameters go green.
4. **QUALITY EVIDENCE.** Inventory audit + invariant. Uncurated sample: every Integration-Console route. Calibration under Canon 3 §31 + Canon 5 §26.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** M. Justification: 7 pages but 1 component (integration tile-group) + 1 new integration surface (shell binding). Rounds to M rather than L because the group is smaller and its Canon-5 clause-set is compact.
7. **REVERSAL COST.** Low-medium.

---

#### WS-HARVEST-CONSOLE-ADMINISTRATION

1. **WHAT.** Repurpose `pages/master_admin/` (4 pages) + `pages/team/` (4 pages) + `pages/govern/GovernPendingPage.jsx`, `GovernChangeRulePage.jsx`, `GovernRegistriesPage.jsx` into the Administration Console tile-group. 11 pages. Contract: Administration Console tile-list. Record class: `Console.Administration.Registration`. Task identity: `interface.console.administration`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §31-§36 (Administration Home + Change-a-Rule + What-I've-Changed + Roles & Rights + Counter-Sign Duties + Verification-Runner surface); Canon 3 §24 (ceremony).
3. **DEFINITION OF DONE.** Administration Console tile-group hosts 11 donor tiles. GovernChangeRulePage and ChangeARulePage dedupe (FL-P1-13 rendering decision — one canonical tile). Canon 5 §31-§36 operative parameters go green. `WS-BUILD-VERIFICATION-RUNNER` (Part-2 BUILD) surfaces as BUILD-marked open slot.
4. **QUALITY EVIDENCE.** Inventory audit + invariant. Uncurated sample: every Administration-Console route. Calibration under Canon 3 §31 + Canon 5 §31.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`, `WS-BUILD-CEREMONY-REVERIFY`, `WS-BUILD-INDEPENDENCE-GATE`. Reference screenshot pending.
6. **CREDIT COST CLASS.** L. Justification: 11 pages, new console tile-group, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

#### WS-HARVEST-COMPONENT-LIBRARY

1. **WHAT.** Repurpose reusable atoms: `RetentionPostureBadge.jsx`, `CounterSignBanner.jsx`, `AuthDeniedNotice.js`, `EngineCard.js`, `LedgerTable.js`, `OuterGateReceiptInline.js`, `StatusBadge.js`, `TrustReceiptLink.js` (8 components). Task identity: `interface.component_library.share`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §43-§65 (shared component library — insufficient-measurement render + absence-as-state + shared visual system).
3. **DEFINITION OF DONE.** All 8 atoms available to every console tile-group as single-source-of-truth imports (`components/ui_spec_v1/index.js` shape). Canon 5 §43-§65 shared-visual-system parameter goes green. Verification: static test `test_shared_components_single_source.test.js` (existing) confirms no duplicated component definitions.
4. **QUALITY EVIDENCE.** Invariant class (shared-source gate — existing test extends). Uncurated sample: full component-import graph during drill day; import count of each atom outside the library = 0. Calibration under Canon 5 §43.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (library), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

#### WS-HARVEST-CLASS-CHIP-LIBRARY

1. **WHAT.** Repurpose `ClassBadge.js` + `ResponseClassPanel.jsx` as the class-chip library. Rows C5-002, C5-003, C5-004 (previously BUILD; reclassified HARVEST). Task identity: `interface.class_chip.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §2-§4 (class chip inseparable from claim + grounding marker).
3. **DEFINITION OF DONE.** ClassBadge + ResponseClassPanel available as the sole render path for class chips across every answer surface. Canon 5 §2 "class chip inseparable from claim" invariant holds — existing test `gate1_class_inseparable.test.js` (present in `frontend/src/__tests__/ui_spec_v1/`) fires green.
4. **QUALITY EVIDENCE.** Invariant class (existing `gate1_class_inseparable.test.js`). Uncurated sample: every rendered answer surface during a drill day. Calibration under Canon 5 §2 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (2 files, single library), 0 new contracts.
7. **REVERSAL COST.** Very low.

---

#### WS-HARVEST-REFUSAL-CARD

1. **WHAT.** Repurpose `RefusalCard.js` as the Canon 5 §9.2 refusal card render, wired to the refusal-family taxonomy via `WS-WIRE-REFUSAL-FAMILY`. Rows C5-005, C5-006, C5-007 (previously BUILD; reclassified HARVEST since the render component exists in Extraction-Akki). Task identity: `interface.refusal_card.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §9.2 (verbatim refusal card); Canon 1 §16 (refusal recorded, never dropped).
3. **DEFINITION OF DONE.** RefusalCard renders the verbatim card copy from the `memory_refusal_reasons.v0.json` taxonomy per `WS-WIRE-REFUSAL-FAMILY`. Canon 5 §9.2 verbatim-copy invariant holds — existing test `gate2_refusal_firstclass.test.js` (present at spine) fires green. `test_auth_denied_notice_not_refusal_card.test.js` (existing) ensures auth-denied stays out of the refusal card. Verification: prove-one-run for one refused request renders the taxonomy id + card copy identically.
4. **QUALITY EVIDENCE.** Invariant class (existing `gate2_refusal_firstclass.test.js`). Uncurated sample: every refusal impression during a drill day; card copy is byte-identical to taxonomy. Calibration under Canon 5 §9.2 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`, `WS-WIRE-REFUSAL-FAMILY`, `WS-HARVEST-TWO-PASS-AMENDMENT` (for the added Executive-Core refusal templates). Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts.
7. **REVERSAL COST.** Very low.

---

#### WS-HARVEST-DORMANT-STATE

1. **WHAT.** Repurpose `ProveDormantPage.jsx` + `TeamDormantPage.jsx` as the Canon 5 §9 dormant-state render pattern. Row C5-009 (previously BUILD; reclassified HARVEST). Task identity: `interface.dormant_state.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §9 (dormant state — "what would activate" statement per screen).
3. **DEFINITION OF DONE.** Every tile that has no activated state renders the dormant-state pattern from these two donor pages, with a Canon 5 §9 "what would activate" copy line. Verification: every BUILD-marked open slot on any console tile-group carries this pattern.
4. **QUALITY EVIDENCE.** Invariant class (dormant-state grammar test). Uncurated sample: every dormant tile impression during drill week. Calibration under Canon 5 §9.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`, `WS-HARVEST-SHELL-GRAMMAR`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (dormant pattern), 0 new contracts.
7. **REVERSAL COST.** Very low.

---

#### WS-MODIFY-PLANE-OBSERVABILITY

1. **WHAT.** MODIFY `MemoryPlaneObservabilityPage.jsx` to rehome from Extraction Console → Compliance Console (RENDERING DECISION FL-P1-08). Canon 7 §29-§31 standing queries + Canon 3 §31 prove-one-run belong at Compliance. Task identity: `interface.plane_observability.rehome`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 7 §29-§31 (standing queries for compliance owners); Canon 3 §31 (verification packs); Canon 5 §22 (Compliance Home).
3. **DEFINITION OF DONE.** Page appears under Compliance Console tile-group with its Canon-5 identity; not duplicated under Extraction Console. Standing-query wiring lands via `WS-BUILD-STANDING-QUERY-SURFACE`. Verification: nav audit confirms exactly one home for this tile.
4. **QUALITY EVIDENCE.** Inventory audit. Uncurated sample: nav-audit run. Calibration under Canon 5 §10.
5. **DEPENDENCIES.** `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-BUILD-STANDING-QUERY-SURFACE`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (single page rehome), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

#### WS-MODIFY-PROVE-ONE-RUN-EXPORT

1. **WHAT.** MODIFY `TraceReceiptPage.js` to be the Canon 3 §33-§48 prove-one-run export tile under Compliance Console, wired to `WS-BUILD-PROVE-ONE-RUN` (Part-2 BUILD). Component: single page. Task identity: `interface.prove_one_run_export.per_pack`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 3 §33-§48 (export prove-one-run pack); Canon 5 §23 (Prove-one-run panel).
3. **DEFINITION OF DONE.** Trace-receipt page becomes the export surface for a prove-one-run pack; every export event ledgered under `Ceremony.ProveOneRun` record class (Part-2). Placement: Compliance Console. Verification: prove-one-run drill exports a pack via this page and the export event lands in ledger.
4. **QUALITY EVIDENCE.** Contract test (pack shape) + drill. Uncurated sample: drill exports over a drill week. Calibration under Canon 3 §31 + Canon 3 §33.
5. **DEPENDENCIES.** `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-BUILD-PROVE-ONE-RUN` (Part 2), `WS-WIRE-LEDGER-MATRIX`. Reference screenshot pending.
6. **CREDIT COST CLASS.** M. Justification: 1 component, 1 new contract (pack export event class), 1 integration surface.
7. **REVERSAL COST.** Low.

---

#### WS-MODIFY-USE-DATA-PLACEMENT

1. **WHAT.** MODIFY `UseDataLandingPage.jsx` to resolve rendering decision FL-P1-10: Canon 5 §14 (Extraction Model Catalogue) OR Canon 5 §43 (Reference App — Ask). Component: single landing page. Task identity: `interface.use_data.placement_resolution`. **FIXTURE CLEARED @ transcription grade (BAC applied); rendering decision resolved per FL-P1-10 (Build Order 01 §2.C — Use-Data landing homes to the Ask reference application).**
2. **CANON CLAUSES SATISFIED.** Canon 5 §14 (Model Catalogue) OR Canon 5 §43-§44 (Reference App — Ask). Owner must rule.
3. **DEFINITION OF DONE.** UseDataLandingPage placed under Extraction Console (as Model Catalogue anchor) OR under Ask Reference App per owner ruling. Nav audit confirms exactly one home.
4. **QUALITY EVIDENCE.** Inventory audit + owner ruling ledgered in DECISIONS.md.
5. **DEPENDENCIES.** Owner ruling (fidelity ledger FL-P1-10). Reference screenshot pending.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Very low.

---

#### WS-MODIFY-VERDICT-DEMO

1. **WHAT.** MODIFY `UseDataVerdictDemoPage.jsx` — determine whether it is a canon-required surface OR a demo-only artifact for retirement (RENDERING DECISION FL-P1-11). Component: single page. Task identity: `interface.verdict_demo.classification`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 4 §7 (verdict is matrix lookup) — question: does the demo satisfy any Canon-5 tile requirement? If yes, HARVEST as Extraction Console tile; if no, RETIRE.
3. **DEFINITION OF DONE.** Either placed under Extraction Console with Canon-5 identity OR RETIRE with reason ledgered in DECISIONS.md.
4. **QUALITY EVIDENCE.** Inventory audit; owner rendering-decision ledger entry.
5. **DEPENDENCIES.** Owner ruling (fidelity ledger FL-P1-11). Reference screenshot pending.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Zero (either path).

---

#### WS-MODIFY-AUDIT-TRAIL-PLACEMENT

1. **WHAT.** MODIFY `AuditTrailPage.js` (currently under master_admin/) to rehome under Compliance Console with Canon 3 §33 audit-trail export identity. Component: single page. Task identity: `interface.audit_trail.rehome`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 3 §33 (audit-trail export); Canon 5 §22 (Compliance Home).
3. **DEFINITION OF DONE.** Placed under Compliance Console, not duplicated under Administration. Nav audit confirms single home.
4. **QUALITY EVIDENCE.** Inventory audit.
5. **DEPENDENCIES.** `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-WIRE-LEDGER-MATRIX`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Very low.

---

**Interface strategy total: 13 items** (2 HARVEST shell + component + class chip + refusal card + dormant + 4 console groups + 4 MODIFY placement/rehome).

**Interface reclassification effects on grand item count:**
- Part-1 total: 34 (pre-Ruling-3) → **47** (post-Ruling-3).
- Part-2 total: 55 → 42 (13 items moved into Part 1).
- Grand total: 89 (unchanged; items redistributed).

**BUILD Watch Console placement constraint (encoded here; item itself remains Part-2 BUILD):**

The Part-2 item `WS-BUILD-CONSOLE-WATCH` acquires the following constraint in its DoD from Instruction 02:
> Watch renders as a fourth group of four app tiles under the Admin surface's tile-grid-plus-detail-card grammar. Tile names, verbatim from Canon 8 §13: `State`, `Record`, `Under Watch`, `Decisions`. Gated by watch-officer role. Sessions run under Watch identity per Canon 9. **NEVER nested under Trust Center or any Compliance-Console tile.**

This constraint MUST propagate into the Part-2 draft of `WS-BUILD-CONSOLE-WATCH`.



---

## §5 · Part 2 items — 55 items

Full drafts, seven fields each, inlined below verbatim from the working paper `notes/strategy_items_part2.md`. Headings demoted so this section's IDs remain unique.

**Chunk 4, Part 2.** All BUILD items with no canon-compliant donor code (i.e., must be built from paper canon). Every item covers 1+ canon requirement rows; the union of coverage across Part-1 + Part-2 = every non-doctrine canon row (mechanical audit produces zero gaps).

**Scope of this file:** 50 items — bundled by canonical mechanism per Orchestrator Ruling B ("not one mega-item per canon"). The Watch's 60 rows fan out to 15 mechanism-scoped items; Canon 9's 45 rows to 6; Canon 2 CIF's 30+ rows to 6.

**Ruling-1 transition linkage:** `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` carry the demonstrated-firing precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip.

**Ruling-B new items:** `WS-BUILD-STREAMING-PORT` and `WS-BUILD-OBJECT-STORAGE-PORT` promoted from folded dependencies to standalone items (multiple items gate on them; FL-P1-03 stays open pending owner ratification).

**Parity-seat linkage:** Every item creating a NEW contract cites `WS-WIRE-PARITY-EXTENSION` (Part 1) as a dependency — no new contract lands without a parity-seat entry.

Estimation discipline and field template — see `strategy_items_part1.md` §top. Not repeated.

**Cross-cutting doctrinal frame** applies to every item (Canon 9 record matrix + task identity + Canon 4 §32 quality matrix + Canon 3 §31 verification packs + Ruling 1 four-test discipline). Fields that cannot be filled honestly → `notes/fidelity_ledger.md`.

---

### A. Custody & Boundary (Canon 1 §12, §6.1, §7.1)

#### WS-BUILD-DECL

1. **WHAT.** Actor-declaration seat + admit-time check + supersession. Rows C3-008, C3-009, C3-010, C3-059. Component: new `services/declaration/` (writer + surface). Contract: `Declaration.v0` (frozen). Record class: `Actor.Declaration` (Canon 9 §6 — writer = declaration seat; readers = admit + Watch + Compliance Console). Task identity: `declaration.capture` and `declaration.check.per_admit`.
2. **CANON CLAUSES.** Canon 3 §6 (Admit — declarations captured before operations); Canon 3 §33 (governance orchestration end-to-end); Canon 6 §3 (setup declarations); Ruling 1 (declaration check is a Watch-reconciler-paired precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip).
3. **DEFINITION OF DONE.** Every `northena/admit.compile_and_freeze` call requires an in-force declaration; declarations captured at setup morning (Canon 6 §3) and re-captured on scope change (supersession event). Admit-time check refuses on missing/expired/scope-mismatched declaration; refusal ledgered via `WS-WIRE-CUSTODY-DECL`. `WS-CONTRADICTION-PURPOSE-GATE` strip prerequisite (a) demonstrates firing via a drill: a declaration-scoped refusal is observable in the ledger and rendered by the refusal card.
4. **QUALITY EVIDENCE.** Contract test (Declaration.v0 shape) + drill (a full admit-refusal cycle with a scoped-mismatched actor). Uncurated sample: every admission in a drill week carries a declaration id or refusal reason. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-WIRE-CUSTODY-DECL` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION` (new contract). Ruling-1 pair with `WS-BUILD-WATCH-RECONCILER`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (declaration seat + admit hook + surface), new register/console surface (declaration seat is a first-class register), 3 integration surfaces (admit, ledger writer, Watch reader).
7. **REVERSAL COST.** High. Declaration records are append-only; a wrong shape freezes forever. Reversal = new supersession entry with revised shape; existing records stay. Ruling-1 gate to strip depends on this firing — a wrong build blocks the strip lawfully.

#### WS-BUILD-INPUT-SEAT

1. **WHAT.** Canonical input-seat surface distinct from de-identifier. Row C3-018. Component: new `services/input_seat/` (per Canon 3 §12 seat, not tenant_entities de-identification). Contract: `Input.Envelope.v0`. Record class: `Input.Seat.Verdict` (Canon 9 §6 — writer = input seat; readers = admit + Watch). Task identity: `input_seat.admit.per_call`.
2. **CANON CLAUSES.** Canon 3 §12 (input seat); Canon 3 §33 (governance orchestration); Canon 1 §6 (fail-closed custody).
3. **DEFINITION OF DONE.** Every incoming payload passes through the input seat before de-identification; seat writes a verdict row per call (admit/refuse/quarantine). Existing `tenant_entities.py` becomes a downstream stage, not the seat itself. Verification: drill with a shaped-input fixture produces a seat verdict + downstream ledger row.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill. Uncurated sample: one drill day of live traffic; seat verdict count = incoming call count. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new authority (input seat is a Canon-3 §12 authoritative surface).
7. **REVERSAL COST.** High. Input-seat verdicts are ledgered; reversal removes the seat and re-exposes payload to un-gated code paths (Canon 3 §12 violation). Ledger stays.

#### WS-BUILD-INPUT-SEAT-DUAL

1. **WHAT.** Dual identity at input seat: governance identity at admit; Watch identity when sensing. Row C3-020. Component: extension of `services/input_seat/` (per WS-BUILD-INPUT-SEAT) with dual identity resolver. Contract: `Input.Seat.Identity.v0`. Record class: uses task-identity register (Canon 9 §8-§35). Task identity: `input_seat.identity_resolve.per_call`.
2. **CANON CLAUSES.** Canon 3 §12 (input seat dual role); Canon 9 §8-§35 (task identity register); Canon 8 §4.11 W11 (one task, one identity).
3. **DEFINITION OF DONE.** Every input-seat verdict carries exactly one task identity (governance OR Watch, never both — Canon 8 §4.11 W11). Task-identity register (WS-BUILD-TASK-IDENTITY-REGISTER) contains the mapping. Verification: AST discipline check (mirror `test_ast_egress_gate.py`) fires on any dual-identity assignment.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped one-identity gate). Uncurated sample: full drill day; dual-identity assignments = 0. Calibration under Canon 8 §4.11.
5. **DEPENDENCIES.** `WS-BUILD-INPUT-SEAT`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (extension), 1 new/changed contract (identity shape), 2 integration surfaces.
7. **REVERSAL COST.** Medium. Dual-identity slip is a Canon 8 W11 violation; reversal disables the resolver, task-identity register keeps prior records.

---

### B. Extraction Quality (Canon 4 §26, §32)

#### WS-BUILD-MOAC-SCORECARD

1. **WHAT.** MOAC six-criteria scorecard + measurement pipeline + drift + latest-reading-in-circulation. Rows C4-037a..f, C4-038, C4-039, C4-040, C4-067, C4-068, C7-D14, C7-D15. Component: new `services/moac/` (scorecard + drift monitor). Contract: `MOAC.Scorecard.v0` (frozen). Record class: `MOAC.Scorecard` (Canon 9 §6 — writer = MOAC engine; readers = Extraction Console + Compliance Console). Task identity: `moac.score.per_adapter_version`.
2. **CANON CLAUSES.** Canon 4 §26 (MOAC anchor); Canon 4 §32 (quality matrix); Canon 5 §14 (Model Catalogue surface pair).
3. **DEFINITION OF DONE.** Every adapter version carries a MOAC scorecard (6 criteria + uncurated-sample provenance + rights lineage + version history). Drift measured continuously; the latest reading is the one shown in circulation (Canon 4 §50). Adapter without a scorecard fails admission (D-MOAC-Missing per C7-D15). Verification: drill with a shape-defect fixture on any of 6 criteria produces the correct card decoration.
4. **QUALITY EVIDENCE.** Contract test (scorecard shape) + drill class (6 defect fixtures, one per criterion). Uncurated sample: 20 adapter versions across a drill month; scorecard coverage = 100%. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** `WS-BUILD-ADAPTER-REGISTRY`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (scorecard + drift + surface hook), new register/console (Model Catalogue tile pair), 2 integration surfaces.
7. **REVERSAL COST.** High. Scorecards ledgered; reversal removes MOAC gate — Canon 4 §26 violation. Records stay.

#### WS-BUILD-ADAPTER-REGISTRY

1. **WHAT.** Adapter registry surface + no-model-for-class rendering. Rows C4-034, C4-035, C4-036. Component: `services/adapter_registry/` (registry writer + surface data). Contract: `Adapter.Registration.v0`. Record class: `Adapter.Registration` (Canon 9 §6). Task identity: `adapter.register.per_version`.
2. **CANON CLAUSES.** Canon 4 §34-§36 (adapter surface); Canon 5 §14 (Model Catalogue read-back).
3. **DEFINITION OF DONE.** Every adapter used in extraction is registered with version, MOAC scorecard reference, rights lineage. Missing model for a class renders as its own state (no silent fall-back). Verification: drill with an unregistered adapter fails admission.
4. **QUALITY EVIDENCE.** Contract test (registration shape). Uncurated sample: full adapter set over a drill week. Calibration under Canon 4 §35.
5. **DEPENDENCIES.** `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

### C. Ports (Ruling B new items)

#### WS-BUILD-STREAMING-PORT

1. **WHAT.** Streaming port at the spine — anchors harvested `synisense/shield/streaming.py` (`WS-HARVEST-STREAMING` in Part 1) as a first-class port that answering surfaces call. Component: `services/synisense/shield/streaming.py` (post-harvest) + port shim. Contract: `Streaming.Frame.v0` (frozen — mirror of memory_plane_v0.contract_snapshot.json shape). Record class: `Streaming.Frame.Envelope` (Canon 9 §6). Task identity: `streaming.frame.per_session`.
2. **CANON CLAUSES.** Canon 1 §7.1 (Shield boundary); Canon 3 §12 (input seat — frames transit); Canon 7 §19 (plane activity envelope).
3. **DEFINITION OF DONE.** Every streamed answer session passes frames through this port; the port's shape is frozen under parity seat. Every RE-POINTed surface (`WS-REPOINT-ANSWERING-SURFACES`, Part 1) that streams calls this port. Verification: streaming drill (100 frames across sessions) shows envelope shape byte-identical to snapshot.
4. **QUALITY EVIDENCE.** Invariant class (frame-envelope). Uncurated sample: one drill day of streamed responses. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-STREAMING` (Part 1), `WS-WIRE-PARITY-EXTENSION`, gates `WS-REPOINT-ANSWERING-SURFACES` completion.
6. **CREDIT COST CLASS.** L. Justification: new register/console surface (port as a first-class integration surface).
7. **REVERSAL COST.** Medium. Streaming disabled; RE-POINT surfaces fall back to non-streamed responses.

#### WS-BUILD-OBJECT-STORAGE-PORT

1. **WHAT.** Object-storage port at the spine — provides per-application object storage per Canon 7 §19-§23 memory-plane discipline. Component: `services/object_storage/` (port + plane-keyed writer + revocation). Contract: `ObjectStorage.Blob.v0` (frozen). Record class: `ObjectStorage.Blob.Reference` (Canon 9 §6). Task identity: `storage.blob.per_object`. **PROPOSAL (per Ruling B): this lands as an XL BUILD item; FL-P1-03 stays OPEN pending owner ratification.**
2. **CANON CLAUSES.** Canon 7 §19-§23 (per-application memory plane with plane-keyed storage); Canon 1 §12 (six-services boundary — storage as a service); Canon 9 §6 (record classes at storage boundary).
3. **DEFINITION OF DONE.** Every blob write/read is plane-keyed via task-identity + application-scope. Blob metadata (id, plane, application, uploaded-by, retention-class) lives in ledger. Revocation cascades per Canon 3 §26-§27. Verification: drill with per-application isolation fixture — cross-application read returns refusal.
4. **QUALITY EVIDENCE.** Invariant class (plane-key discipline test) + drill class (cross-application isolation). Uncurated sample: full drill week of blob operations; cross-application leak count = 0. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`. **Gates `WS-REBUILD-WORK-STUDIO-STORAGE`** (Part 1 — the 200+ export migration.)
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** New engine/authority (object-storage service does not exist at the spine today); estate-wide (every application will eventually store artefacts); its API shape is a new frozen contract that irreversibly defines how work_studio + future artefact-creating applications write. XL bar met on the new-engine axis alone; also meets estate-wide-wiring axis independently.
7. **REVERSAL COST.** VERY HIGH. Once blobs exist, they cannot be un-stored trivially; reversal = keep the blob store but stop writing new blobs; downstream applications lose the artefacts they wrote. Reader-migration reversibility is the canonical case (see `WS-REBUILD-WORK-STUDIO-STORAGE`).

---

### D. Integration (Canon 7)

#### WS-BUILD-WEBHOOK

1. **WHAT.** Per-application webhook infrastructure for compliance-record notifications. Rows C7-009, C6-042. Component: `services/webhook/` (subscription registry + delivery + signing). Contract: `Webhook.Envelope.v0`. Record class: `Webhook.Delivery` (Canon 9 §6). Task identity: `webhook.deliver.per_event`.
2. **CANON CLAUSES.** Canon 7 §9 (webhook infrastructure); Canon 6 §11 (commissioning notifications); Canon 3 §33 (governance orchestration).
3. **DEFINITION OF DONE.** Applications register webhook subscriptions per compliance-record class; every write to a subscribed class fans out via signed deliveries. Delivery retries follow Canon 7 §9 discipline; failed deliveries ledgered.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill. Uncurated sample: 100 webhook deliveries across a drill week; retry rate + delivery hash. Calibration under Canon 7 §9.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Low. Reversal disables webhook delivery; applications poll instead.

#### WS-BUILD-PLANE-PRECOMPUTE

1. **WHAT.** Per-application memory-plane precompute per Canon 7 §19-§23. Row C7-018. Component: `services/plane_precompute/` (background job runner over memory planes). Contract: `PlanePrecompute.Task.v0`. Record class: `Plane.Precompute` (Canon 9 §6). Task identity: `plane.precompute.per_job`.
2. **CANON CLAUSES.** Canon 7 §19-§23 (memory plane precompute); Canon 3 §33 (governance orchestration).
3. **DEFINITION OF DONE.** Precompute jobs run within per-application task identity; job metadata + result hash ledgered; Watch reads job activity envelope (via `WS-WIRE-WATCH-PLANE-ACTIVITY`, Part 1) without reading content.
4. **QUALITY EVIDENCE.** Contract test (task shape) + invariant (no content crosses the Watch reader boundary). Uncurated sample: full drill week of precompute jobs. Calibration under Canon 7 §19 + Canon 8 §4.13 W13.
5. **DEPENDENCIES.** `WS-BUILD-OBJECT-STORAGE-PORT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-WATCH-PLANE-ACTIVITY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (job runner + plane reader + Watch envelope), new register (job class), 3 integration surfaces.
7. **REVERSAL COST.** Medium.

---

### E. Governance Ceremony (Canon 3 §24, §31, §33; Canon 6)

#### WS-BUILD-VERIFICATION-RUNNER

1. **WHAT.** Compliance-Console-triggered live verification runner. Rows C3-039, C3-040, C3-041, C3-042. Component: `services/verification_runner/` (pack loader + executor + result writer). Contract: `Verification.Pack.v0` + `Verification.Result.v0`. Record class: `Verification.Run` (Canon 9 §6). Task identity: `verification.run.per_pack`.
2. **CANON CLAUSES.** Canon 3 §31 (verification packs); Canon 3 §33 (Compliance Console read-back); Canon 6 §11-§13 (commissioning verification).
3. **DEFINITION OF DONE.** Compliance owner triggers a verification pack from the Administration Console (`WS-HARVEST-CONSOLE-ADMINISTRATION`, Part 1); pack loads named tests from `tests/invariants/`; results write to ledger. Also invoked by `WS-BUILD-CEREMONY-REVERIFY` (Part 1) as the 5th step. Verification: drill runs one pack end-to-end.
4. **QUALITY EVIDENCE.** Contract test (pack + result shapes) + drill (compliance owner runs a pack). Uncurated sample: full pack catalogue across a drill week. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-CEREMONY-REVERIFY` (Part 1), `WS-HARVEST-CONSOLE-ADMINISTRATION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (runner + pack registry + result writer), new register/console (verification-runner surface), 3 integration surfaces.
7. **REVERSAL COST.** Medium.

#### WS-BUILD-PROVE-ONE-RUN

1. **WHAT.** Canon 3 §33 "prove one run" export pack as single action. Rows C3-046, C3-047, C3-048. Component: `services/prove_one_run/` (pack compiler over ledger). Contract: `ProveOneRun.Pack.v0` (frozen). Record class: `ProveOneRun.Pack` (Canon 9 §6). Task identity: `prove_one_run.compile.per_run`.
2. **CANON CLAUSES.** Canon 3 §33 (prove-one-run + regulator pack); Canon 5 §21 (Prove-one-run panel; also §22-§23 Compliance Home).
3. **DEFINITION OF DONE.** For any run id, a single compile call emits a pack containing: admit row, declaration in force, rule versions consulted, retrieved evidence with hashes, trust receipts of outbound calls, verdicts, refusal receipts. Pack verifies offline by receipt signatures. Surface: rendered via `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (Part 1) tile.
4. **QUALITY EVIDENCE.** Contract test (pack shape) + drill (offline verification of an exported pack). Uncurated sample: 20 exported packs across a drill week; offline-verify pass rate = 100%. Calibration under Canon 3 §33.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (compiler + hasher + surface), new register (pack class), 3 integration surfaces (ledger reader, hash writer, surface).
7. **REVERSAL COST.** Medium. Packs signed and delivered stay; reversal disables new compilation.

#### WS-BUILD-SETUP-CONSOLE

1. **WHAT.** Setup surface + signed setup record artefact. Rows C6-007..C6-012. Component: `services/setup_console/` (setup flow + record writer). Contract: `Setup.Record.v0`. Record class: `Setup.Record` (Canon 9 §6). Task identity: `setup.commit.per_actor`.
2. **CANON CLAUSES.** Canon 6 §3 (setup declarations); Canon 6 §7 (signed setup record).
3. **DEFINITION OF DONE.** Setup flow captures actor identity, declarations, initial connectors, initial policies; produces a signed setup record. Record ledgered; parity-seat frozen. Verification: drill runs a full setup end-to-end and produces a valid signed record.
4. **QUALITY EVIDENCE.** Contract test + drill. Uncurated sample: 5 setup runs across drills. Calibration under Canon 6 §3.
5. **DEPENDENCIES.** `WS-BUILD-DECL`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`, `WS-HARVEST-CONSOLE-INTEGRATION` (Part 1 — setup pages).
6. **CREDIT COST CLASS.** L. Justification: 3 components (flow + record + surface), new register, 3 integration surfaces.
7. **REVERSAL COST.** Medium.

#### WS-BUILD-DAY-ZERO

1. **WHAT.** Estate map + commissioning certificate + Verification-Runner packs + Watch drills — the Day-Zero bundle. Rows C6-013..C6-022. Component: `services/day_zero/` (orchestrator over setup + estate scan + verification + drills). Contract: `Commissioning.Certificate.v0`. Record class: `Commissioning.Certificate` (Canon 9 §6). Task identity: `day_zero.commission.per_instance`.
2. **CANON CLAUSES.** Canon 6 §11-§13 (commissioning certificate); Canon 8 §5 W-drills (Watch fitness on day zero).
3. **DEFINITION OF DONE.** Day-zero orchestration produces: estate map + commissioning certificate signed by all seat-holders + Watch drill fitness receipt + Verification-Runner packs for all standing invariants. Certificate ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (full day-zero simulation on a fixture instance). Uncurated sample: every day-zero produces the four artefacts. Calibration under Canon 6 §11.
5. **DEPENDENCIES.** `WS-BUILD-SETUP-CONSOLE`, `WS-BUILD-VERIFICATION-RUNNER`, `WS-BUILD-WATCH-DRILL-HARNESS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components, new register (commissioning certificate).
7. **REVERSAL COST.** Medium.

#### WS-BUILD-RULEBOOK-SURFACE

1. **WHAT.** Compliance Rulebook read-back surface. Rows C3-030..C3-032, C3-034, C3-035, C7-D12. Component: `services/rulebook/` (read-back writer + surface data). Contract: `Rulebook.Rule.v0`. Record class: `Rulebook.Rule` (Canon 9 §6). Task identity: `rulebook.read_back.per_rule`.
2. **CANON CLAUSES.** Canon 3 §25 (rulebook); Canon 5 §25 (rulebook read-back at Compliance Home); Canon 7 §D12 defect (rule-on-paper flag).
3. **DEFINITION OF DONE.** Every governance rule visible in the rulebook shows: current text, effective date, ceremony trail (proposed→countersigned→waited→applied→re-verified via `WS-BUILD-CEREMONY-REVERIFY`), rule-on-paper flag if not yet applied. Surface rendered by `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1).
4. **QUALITY EVIDENCE.** Contract test (rule shape) + inventory audit (every rule has ceremony trail). Uncurated sample: full rulebook over drill week. Calibration under Canon 3 §25.
5. **DEPENDENCIES.** `WS-BUILD-CEREMONY-REVERIFY` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (rule writer + ceremony reader + surface data), new register.
7. **REVERSAL COST.** Medium.

---

### F. Interface BUILD (Canon 5, no Extraction-Akki donor)

Each of these tiles either has no existing page in the Extraction-Akki frontend (`WS-BUILD-*`) OR carries copy that must be built verbatim from canon (`WS-BUILD-REFUSAL-CARD-COPY`). Every tile appears as a BUILD-marked open slot inside the harvested console tile-groups (Part 1). All carry `FIXTURE CLEARED @ transcription grade — see `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13); `test_four_questions_topline_present` added to new-invariants list per Build Order 01 §3`.

#### WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE

1. **WHAT.** Extraction Console Model Catalogue tile — MOAC scorecard render per adapter version. Row C5-014. Component: new frontend tile + backend data provider. Contract: `Model.Catalogue.Row.v0`. Record class: `MOAC.Scorecard` (reader). Task identity: `catalogue.render.per_adapter`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §14 (Model Catalogue); Canon 4 §26 (MOAC).
3. **DEFINITION OF DONE.** Tile renders every adapter version with its MOAC scorecard, drift indicator, uncurated-sample provenance, rights lineage. Row without a scorecard renders as its own state.
4. **QUALITY EVIDENCE.** Inventory audit (tile row-count = adapter-version-count). Calibration under Canon 5 §14.
5. **DEPENDENCIES.** `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-ADAPTER-REGISTRY`, `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1 — the parent tile-group), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract (row shape), 2 integration surfaces.
7. **REVERSAL COST.** Low.

#### WS-BUILD-BATCH-BOARD-SURFACE

1. **WHAT.** Batch Board surface with quarantined batches. Row C5-018. Component: frontend tile + backend data feed from `WS-HARVEST-BATCH-QUARANTINE` (Part 1). Contract: `Batch.Board.Row.v0`. Record class: `Batch.QuarantineDecision` (reader). Task identity: `batch_board.render.per_batch`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 4 §34.1 Batch Board; Canon 5 §17 Extraction Console.
3. **DEFINITION OF DONE.** Tile renders every batch with quarantine verdict + reason; quarantined batches highlighted; un-quarantined batches show pass state. No content leaks (Canon 4 §34.1 discipline).
4. **QUALITY EVIDENCE.** Inventory audit + invariant (no content leak). Calibration under Canon 4 §34.1.
5. **DEPENDENCIES.** `WS-HARVEST-BATCH-QUARANTINE` (Part 1), `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Low.

#### WS-BUILD-QUALITY-OBSERVATION

1. **WHAT.** Quality Observation tile with Critic-Seam calibration stale surface. Row C5-020. Component: frontend tile + backend Critic-Seam calibration state reader. Contract: `Quality.Observation.Panel.v0`. Record class: `Critic.Verdict` (reader). Task identity: `quality_observation.render.per_check`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §18 (Quality Observation); Canon 7 §33 (Critic Seam calibration); Canon 4 §32 (quality matrix).
3. **DEFINITION OF DONE.** Tile renders Critic Seam calibration status per adapter class; stale-calibration surface highlighted; drift alarms per Canon 4 §32.
4. **QUALITY EVIDENCE.** Inventory audit + calibration-stale drill. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-CRITIC-SEAM` (Part 1), `WS-WIRE-CRITIC-INTO-ANSWERING` (Part 1), `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

#### WS-BUILD-AGENT-ASSUMED-CHIP

1. **WHAT.** Agent-assumed chip render (chip that flags claims produced by the agent's own inference vs quoted evidence). Row C5-008. Component: new frontend chip component. Contract: `Agent.Assumed.Chip.v0`. Record class: none (surface-only). Task identity: `agent_assumed.render.per_claim`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §2.5 (Agent-assumed marking); Canon 5 §9.3 (Agent-assumed chip component).
3. **DEFINITION OF DONE.** Every claim carrying agent-derived (not-quoted) inference renders with the agent-assumed chip. Existing test `gate1_class_inseparable.test.js` extends to require chip presence.
4. **QUALITY EVIDENCE.** Invariant test (chip-presence per agent-derived claim). Uncurated sample: 100 answer envelopes; agent-assumed classifier accuracy per calibration. Calibration under Canon 5 §2.5.
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-BUILD-ANSWER-CARD`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Very low.

#### WS-BUILD-REFUSAL-CARD-COPY

1. **WHAT.** Verbatim Canon 5 §9.2 refusal card COPY authored + registered in the refusal-family taxonomy (extends `services/memory/memory_refusal_reasons.v0.json`). Rows C5-005, C5-006, C5-007, C7-D03. Component: taxonomy JSON extension + copy authoring. Contract: refusal-reason JSON snapshot (extends existing frozen shape via `WS-WIRE-PARITY-EXTENSION`). Record class: `Refusal.Reason` (writer). Task identity: `refusal.copy.per_family`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §9.2 (verbatim refusal card copy); Canon 1 §7.1 (refusal recorded); Canon 3 §17 (refusal shapes catalogued).
3. **DEFINITION OF DONE.** Every canon-listed refusal family has a verbatim copy entry in the taxonomy JSON. `WS-HARVEST-REFUSAL-CARD` (Part 1 — the render) reads these entries. Copy is byte-identical to Canon 5 §9.2 text.
4. **QUALITY EVIDENCE.** Invariant test (byte-identical copy render) + inventory audit (every family has a copy entry). Calibration under Canon 5 §9.2.
5. **DEPENDENCIES.** `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-WIRE-REFUSAL-FAMILY` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (JSON extension), 0 new contracts (extends existing), 1 integration surface.
7. **REVERSAL COST.** Very low.

#### WS-BUILD-THREE-LENSES

1. **WHAT.** Three lenses (Answer / Reasoning / Raw trail) over one object. Rows C5-045..C5-048, C7-006 (envelope class-chip render). Component: new frontend tile with three panels + backend three-panel data provider. Contract: `Three.Lenses.Envelope.v0`. Record class: `Answer.Envelope` (Canon 9 §6). Task identity: `answer.three_lenses.render.per_object`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §37.1 (three lenses); Canon 5 §2 (class chip inseparable per lens).
3. **DEFINITION OF DONE.** Every answer surface renders three lenses over the same object; class chip present in every lens; refusal card can appear in any lens.
4. **QUALITY EVIDENCE.** Invariant test (three-panel + class-chip presence) + drill (10 answer sessions rendered across three lenses).
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-BUILD-ANSWER-CARD`, `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

#### WS-BUILD-ANSWER-CARD

1. **WHAT.** Answer card (evidence strip + honesty strip + actions). Rows C5-049, C5-050, C5-051. Component: new frontend card + backend data provider. Contract: `Answer.Card.v0`. Record class: `Answer.Envelope` (reader). Task identity: `answer_card.render.per_answer`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §37 (Ask surface); Canon 5 §37.4 (machine form / answer envelope).
3. **DEFINITION OF DONE.** Every answer renders as an answer card with evidence + honesty + actions strips. Card is source-of-truth for the answer envelope.
4. **QUALITY EVIDENCE.** Invariant test (card shape). Uncurated sample: 100 answers across drill week. Calibration under Canon 5 §37.
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

#### WS-BUILD-FIVE-PILLARS

1. **WHAT.** Five-pillar router (Canon 5 §40): Ask · Work · Lead · Learn · Build + 3rd Party. Row C5-052. Component: new frontend router + pillar-registry backend. Contract: `Pillar.Registration.v0`. Record class: none (surface + registration). Task identity: `pillar.router.per_navigation`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §40 (five pillars); FL-OQ-04 (four-vs-five console taxonomy — pillars are distinct from consoles).
3. **DEFINITION OF DONE.** Every user surfaces routes through one of the five pillars; Canon-5 conformance audit = 100%.
4. **QUALITY EVIDENCE.** Inventory audit (surface-list → pillar-list). Calibration under Canon 5 §40.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-CONTROL-BAND`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new register/console surface (five-pillar taxonomy).
7. **REVERSAL COST.** Medium (pillar taxonomy touches every surface's placement).

#### WS-BUILD-PULSE-NEWS

1. **WHAT.** Pulse + News apps for the Lead pillar. Row C5-053. Component: new Lead-pillar applications. Contract: `Pulse.Post.v0`, `News.Item.v0`. Record class: `Pulse.Post`, `News.Item` (Canon 9 §6). Task identity: `pulse.compose.per_post`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §40 (Lead pillar apps); Canon 5 §43 (Pulse + News).
3. **DEFINITION OF DONE.** Two Lead-pillar apps render as tiles inside the Lead pillar router; Pulse is workspace-internal, News aggregates canon-tagged updates.
4. **QUALITY EVIDENCE.** Contract test + inventory audit.
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

#### WS-BUILD-STUDIO

1. **WHAT.** Studio — application composer surface for the Build pillar. Rows C5-055, C5-060. Component: new Build-pillar application. Contract: `Studio.Composition.v0`. Record class: `Studio.Composition`. Task identity: `studio.compose.per_app`. **FIXTURE CLEARED @ transcription grade (BAC applied); Studio deferred per FL-OQ-05 (Build Order 01 §4 amendment — leaves Wave 8).**
2. **CANON CLAUSES.** Canon 5 §42 (designed, not sourced); Canon 5 §43 Studio (per row extraction; scope resolution pending FL-OQ-05).
3. **DEFINITION OF DONE.** _Partial pending FL-OQ-05_: Studio surfaces expose app composition primitives per Canon 5 §42; scope of "compose" — does it include storage-plane assignment? — governed by owner ruling.
4. **QUALITY EVIDENCE.** Contract test + drill (one Studio-composed app end-to-end).
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-BUILD-OBJECT-STORAGE-PORT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`. Scope-gated by FL-OQ-05.
6. **CREDIT COST CLASS.** L (baseline scope) → XL if scope expands to storage-plane composition. Reclassify on FL-OQ-05 ruling.
7. **REVERSAL COST.** Medium-high depending on scope.

#### WS-BUILD-LEARN-PILLAR

1. **WHAT.** Learn-pillar surfaces (Canon 5 §40 fifth pillar). Row C5-057. Component: new Learn-pillar applications. Contract: `Learn.Module.v0`. Record class: `Learn.Module.Interaction`. Task identity: `learn.module.per_interaction`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §40 (five pillars — Learn); Canon 5 §43 (Learn surfaces).
3. **DEFINITION OF DONE.** Learn tiles render under Learn pillar; interactions ledgered per Canon 9 §6 without content leaking.
4. **QUALITY EVIDENCE.** Contract test + inventory audit.
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

#### WS-BUILD-REFERENCE-APP

1. **WHAT.** Reference App (Ask) — the canonical Ask app surface. Rows C5-043, C5-044, C6-038..C6-043. Component: new Ask pillar-application. Contract: `Ask.Session.v0`. Record class: `Ask.Session`. Task identity: `ask.session.per_actor`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §37 (Ask); Canon 5 §43-§44 (Reference App); Canon 6 §5-§7 (working-rhythm).
3. **DEFINITION OF DONE.** Ask app renders three-lenses (`WS-BUILD-THREE-LENSES`) over answer envelope; agent-assumed chip present per Canon 5 §2.5; refusal card renders verbatim per Canon 5 §9.2.
4. **QUALITY EVIDENCE.** Drill (10 Ask sessions across various shapes). Calibration under Canon 5 §37.
5. **DEPENDENCIES.** `WS-BUILD-THREE-LENSES`, `WS-BUILD-ANSWER-CARD`, `WS-BUILD-AGENT-ASSUMED-CHIP`, `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components, new register (Ask session class).
7. **REVERSAL COST.** Medium.

#### WS-BUILD-CONTROL-BAND

1. **WHAT.** Control Band (Connect / Estate Map / Rulebook / Access / Watch). Rows C5-058, C5-059. Component: new frontend control-band component + wiring to five sub-tiles. Contract: `Control.Band.Row.v0`. Record class: none (surface). Task identity: `control_band.render.per_user`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES.** Canon 5 §41 (Control Band).
3. **DEFINITION OF DONE.** Every user surface renders the Control Band with five items; each item links to the corresponding Canon-5 console tile.
4. **QUALITY EVIDENCE.** Inventory audit (control-band item count = 5). Calibration under Canon 5 §41.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-FIVE-PILLARS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

---

### G. Watch (Canon 8, 60 rows → 15 mechanism-scoped items)

#### WS-BUILD-WATCH-FOUNDATION

1. **WHAT.** Watch foundational discipline: machine-speed + cannot-act-unobserved + proves-own-fitness + sensing→verdict→response→action seam. Rows C8-004..C8-008. Component: `services/watch/foundation.py` + shared discipline module. Contract: `Watch.Attestation.v0`. Record class: `Watch.Attestation` (Canon 9 §6). Task identity: `watch.attestation.per_cycle`.
2. **CANON CLAUSES.** Canon 8 §1-§4 (What the Watch Is); Canon 8 §4.14 W14 (Self-proving); Canon 8 §5 (Macho — Eyes).
3. **DEFINITION OF DONE.** Machine-speed operative parameter measured continuously (Canon 8 §18); no Watch action executes without a receipt landing atomically (Canon 8 §4); fitness attested per cycle by drill receipts.
4. **QUALITY EVIDENCE.** Invariant class (machine-speed bound, receipt-atomicity gate). Uncurated sample: full drill week; violations = 0. Calibration under Canon 8 §18.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** New authority — the Watch is a Canon-1 §7.1 peer authority to governance. Its foundational discipline (machine-speed, cannot-act-unobserved, proves-own-fitness) is estate-wide (crosses every request path). XL bar met on both new-authority AND estate-wide-wiring axes.
7. **REVERSAL COST.** Very high — Watch attestations append-only; a bad build ledgers unreliable attestations forever.

#### WS-BUILD-WATCH-ACTORS

1. **WHAT.** Macho (sensor) + Mkono (responder) + Witness — three Watch actors bundled per Canon 8 §6 seam. Rows C8-009..C8-013, C8-055..C8-057, C8-059. Component: `services/watch/macho/`, `services/watch/mkono/`, `services/watch/witness/`. Contracts: `Watch.Verdict.v0` (Macho), `Watch.Action.v0` (Mkono), `Watch.Attestation.v0` (Witness). Record classes: `Watch.Verdict`, `Watch.Action`, `Watch.Attestation` (Canon 9 §6). Task identities: `watch.macho.sense`, `watch.mkono.respond`, `watch.witness.attest`.
2. **CANON CLAUSES.** Canon 8 §5 (Macho); Canon 8 §7 (Mkono); Canon 8 §16 (Witness); Canon 8 §21 seam.
3. **DEFINITION OF DONE.** Each actor writes only its own record class (Macho writes verdicts; Mkono writes actions; Witness writes attestations); actors read shared record. Verification: drill fires three-actor cycle end-to-end.
4. **QUALITY EVIDENCE.** Invariant class (writer-role exclusivity per Canon 9 §6). Uncurated sample: full drill week. Calibration under Canon 8 §5-§7.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION`, `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Three new authorities in one item (Macho, Mkono, Witness — each a Canon-8 named actor with its own record class); estate-wide (every request path passes through Macho); qualifies XL on both axes.
7. **REVERSAL COST.** Very high — actor verdicts/actions append-only.

#### WS-BUILD-WATCH-RECONCILER

1. **WHAT.** Watch reconciler — Macho verdict × Mkono action × Governance record reconciliation loop per Canon 8 §14-§15. Component: `services/watch/reconciler.py`. Contract: `Watch.Reconciliation.v0`. Record class: `Watch.Reconciliation` (Canon 9 §6). Task identity: `watch.reconciler.per_cycle`. **Ruling-1 linkage: this item's DEMONSTRATED FIRING is the second precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip.**
2. **CANON CLAUSES.** Canon 8 §14-§15 (With the Governing Authority + Disagreement); Canon 9 §6 (record matrix — reconciliation handoff `governance→Watch verdict`); Ruling 1 (transition condition).
3. **DEFINITION OF DONE.** Reconciler runs on every cycle; produces a `Watch.Reconciliation` record with fields (governance-verdict-id, watch-verdict-id, agree|disagree, disagreement-reason-if-any). **Ruling-1 demonstrated-firing evidence:** one drill produces a shared-record reconciliation event with an observable reconciliation row, cross-cited to the ledger. This satisfies precondition (b) for the purpose-gate strip.
4. **QUALITY EVIDENCE.** Invariant class (reconciliation-per-cycle gate) + drill class (shared-record fixture producing reconciliation event). Uncurated sample: every cycle produces one reconciliation record. Calibration under Canon 8 §14-§15.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-DECL` (Ruling-1 paired precondition), `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`. **Gates:** `WS-CONTRADICTION-PURPOSE-GATE` strip lawfulness.
6. **CREDIT COST CLASS.** L. Justification: 2 components (reconciler + handoff), 1 new contract, 3 integration surfaces (Macho reader + governance reader + reconciliation writer).
7. **REVERSAL COST.** Very high — Ruling-1 strip cannot proceed lawfully without this firing. Reconciliation records append-only.

#### WS-BUILD-WATCH-MARK-REGISTRY

1. **WHAT.** Watch Mark Register — writer, dimensions, de-mark two-signature discipline. Rows C8-014..C8-018. Component: `services/watch/mark_registry/`. Contract: `Watch.Mark.v0`. Record class: `Watch.Mark` (Canon 9 §6). Task identity: `watch.mark.per_placement`.
2. **CANON CLAUSES.** Canon 8 §10 (The Mark); Canon 9 §6 (mark record class).
3. **DEFINITION OF DONE.** Every mark placement writes a `Watch.Mark` row with dimensions; de-mark requires two signatures (Canon 8 §10 discipline); marks never rendered on public surfaces (Canon 8 §4.13 W13).
4. **QUALITY EVIDENCE.** Invariant class (two-signature de-mark gate + no-render W13). Uncurated sample: full drill week of mark placements. Calibration under Canon 8 §10.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 2 components + new register.
7. **REVERSAL COST.** Very high — marks append-only.

#### WS-BUILD-WATCH-CONTAINMENT

1. **WHAT.** Containment machinery — bounded, reversible, witnessed acts per Canon 8 §4.3 W3; expiries + reconciliation on release. Rows C8-019..C8-026. Component: `services/watch/containment/`. Contract: `Watch.Containment.v0` + `Watch.Containment.Release.v0`. Record class: `Watch.Containment` (Canon 9 §6). Task identity: `watch.contain.per_target`.
2. **CANON CLAUSES.** Canon 8 §4.3 W3 (reversible + bounded + witnessed); Canon 8 §8 (Four Layers of Constraint); Canon 8 §17 (expiry discipline).
3. **DEFINITION OF DONE.** Every containment is bounded (has explicit scope + duration); reversible (release possible); witnessed (Witness attestation recorded). Expiries do NOT auto-extend (Canon 8 §21 W-negative). On release, reconciliation record (`WS-BUILD-WATCH-RECONCILER`) fires.
4. **QUALITY EVIDENCE.** Invariant class (bounded-scope + no-auto-extend gates) + drill (containment lifecycle end-to-end). Calibration under Canon 8 §17.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-WATCH-ATTESTATION-WITNESS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-WATCH-MIRAGE

1. **WHAT.** Sarabi — the misdirection arm. Rows C8-020..C8-021, C8-036 (drill: planted credential touched + severance executed). Component: `services/watch/sarabi/mirage.py`. Contract: `Watch.Mirage.v0`. Record class: `Watch.Mirage.Placement` (Canon 9 §6). Task identity: `watch.mirage.per_placement`.
2. **CANON CLAUSES.** Canon 8 §11 (Sarabi — Misdirection Arm); Canon 8 §12 (Duties Deception Carries).
3. **DEFINITION OF DONE.** Mirages placed as planted credentials/paths; touch triggers containment. Mirage placement + touch events ledgered. No surface renders mirage construction (Canon 8 §21 W-negative — enforced via AST discipline check).
4. **QUALITY EVIDENCE.** Invariant class (no-mirage-render AST gate) + drill (planted-credential-touched fixture). Calibration under Canon 8 §11.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

#### WS-BUILD-WATCH-SIGNATURE-STORE

1. **WHAT.** Behavioural profile / signature store — no-reader W13 discipline. Rows C8-018, C8-058, C8-064, C8-045 (constitutional negative). Component: `services/watch/signature_store/`. Contract: `Watch.Signature.v0`. Record class: `Watch.Signature` (Canon 9 §6 — writer = signature substrate, readers = NO surface, ever, per W13). Task identity: `watch.signature.per_actor`.
2. **CANON CLAUSES.** Canon 8 §4.13 W13 (profile is armory, not inventory); Canon 8 §9 (Signature).
3. **DEFINITION OF DONE.** Signatures written; NO surface reads (AST discipline check across all surfaces). Behavioural profile internals never rendered anywhere. Export blocked (Canon 8 §21 W-negative).
4. **QUALITY EVIDENCE.** Invariant class (AST no-reader gate). Uncurated sample: full codebase AST scan; reader count = 0. Calibration under Canon 8 §4.13.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high (any leak is a Canon 8 W13 violation; leaked signatures cannot be un-leaked).

#### WS-BUILD-WATCH-DECISIONS-PANEL

1. **WHAT.** Reserved decisions + panel discipline. Rows C8-027..C8-029, C8-050 (no reserved-decision executed by machine). Component: `services/watch/reserved_decisions/`. Contract: `Watch.Reserved.Decision.v0`. Record class: `Watch.Reserved.Decision` (Canon 9 §6). Task identity: `watch.reserved_decision.per_case`.
2. **CANON CLAUSES.** Canon 8 §13 (Watch Console); Canon 8 §19 (Quality Parameters).
3. **DEFINITION OF DONE.** Reserved decisions never executed by machine (Canon 8 §21 W-negative); require Watch-officer signature (Canon 8 §13). Panel renders inside Watch Console (`WS-BUILD-CONSOLE-WATCH`).
4. **QUALITY EVIDENCE.** Invariant class (no-machine-execution gate) + drill. Calibration under Canon 8 §19.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-CONSOLE-WATCH`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-WATCH-DAY

1. **WHAT.** Watch officer's day — what officer reads/does/NEVER does. Rows C8-030..C8-033. Component: Watch-officer-day flow inside Watch Console. Contract: `Watch.Officer.Session.v0`. Record class: `Watch.Officer.Session` (Canon 9 §6). Task identity: `watch.officer.session.per_shift`.
2. **CANON CLAUSES.** Canon 8 §21 (What This Canon Comes Down To — officer discipline).
3. **DEFINITION OF DONE.** Watch officer's session ledgered; officer reads state band + record + under-watch panel + decisions panel; officer NEVER tunes thresholds (Canon 8 §21 W-negative — no threshold visible for tuning).
4. **QUALITY EVIDENCE.** Invariant class (no-threshold-render AST gate) + drill (officer day walk-through). Calibration under Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-CONSOLE-WATCH`, `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Medium.

#### WS-BUILD-WATCH-DRILL-HARNESS

1. **WHAT.** Watch drill harness — standing drills + fitness in receipts. Rows C8-034..C8-039. Component: `services/watch/drills/` (drill runner + fitness computer). Contract: `Watch.Drill.Receipt.v0`. Record class: `Watch.Drill.Receipt` (Canon 9 §6). Task identity: `watch.drill.per_run`.
2. **CANON CLAUSES.** Canon 8 §5 W-drills; Canon 8 §19 Quality Parameters (fitness); Canon 8 §4.14 W14 (self-proving).
3. **DEFINITION OF DONE.** Drills run on fixed cadence; each produces a receipt (Canon 9 §3 attestation shape). Fitness stated only via receipts (Canon 8 §21 no self-attestation). Verification: drill week produces receipts for every scheduled drill class.
4. **QUALITY EVIDENCE.** Contract test (receipt shape) + drill week. Uncurated sample: every scheduled drill in a week. Calibration under Canon 8 §19.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-MIRAGE`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-WATCH-AUTHORITY-PEERAGE

1. **WHAT.** Watch × Governance peerage — disagreement + task identity + new-entry-only correction. Rows C8-040..C8-044. Component: `services/watch/peerage/`. Contract: `Watch.Disagreement.v0`. Record class: `Watch.Disagreement` (Canon 9 §6). Task identity: `watch.peerage.disagree.per_event`.
2. **CANON CLAUSES.** Canon 8 §14-§15 (peerage + disagreement); Canon 8 §4.12 W12 (peer, not subordinate); Canon 8 §4.11 W11 (one task, one identity).
3. **DEFINITION OF DONE.** Neither authority commands the other. Disagreements ledgered; correction is by new entry only (Canon 8 §21 no in-place amend). Task identity discipline enforced per W11.
4. **QUALITY EVIDENCE.** Invariant class (no-command AST gate + new-entry-only invariant). Calibration under Canon 8 §14-§15.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-WATCH-RECORD-CLASSES

1. **WHAT.** All Watch record classes writers — verdict/action/marks/behavioural-profiles/attestation writer discipline. Rows C8-055..C8-059. Component: matrix entries in `WS-BUILD-RECORD-MATRIX` for every Watch class. Contract: matrix rows for verdict, action, mark, signature, attestation. Task identity: `watch.record.per_write`.
2. **CANON CLAUSES.** Canon 9 §6-§18 (record matrix); Canon 8 §21-§59 (Watch record classes).
3. **DEFINITION OF DONE.** Every Watch record class has an exclusive writer entry in the Record Matrix; readers explicitly enumerated per class (including the empty reader-list for behavioural profiles per W13).
4. **QUALITY EVIDENCE.** Matrix inventory audit. Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-WATCH-TO-CIF

1. **WHAT.** Watch findings crossing to CIF as detection input; only ratified frames cross back. Rows C2-014, C8-066..C8-068. Component: `services/watch/to_cif/`. Contract: `Watch.CIF.Handoff.v0`. Record class: `Watch.CIF.Handoff` (Canon 9 §6). Task identity: `watch.to_cif.per_finding`.
2. **CANON CLAUSES.** Canon 2 §6 (engine walls — CIF origination port); Canon 8 §21 (Watch/CIF interface); Canon 9 §6 handoff `Watch findings→CIF`.
3. **DEFINITION OF DONE.** Watch findings arrive at CIF as detection input under CIF's origination port. Nothing crosses back except ratified frames through the coach seat. Watch drills operate under CIF's permanent bound (Watch may never certify CIF).
4. **QUALITY EVIDENCE.** Contract test (handoff shape) + drill (Watch finding → CIF detection). Calibration under Canon 2 §6.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-CIF-COACH-SEAT`, `WS-CIF-DETECTION`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

#### WS-BUILD-WATCH-ATTESTATION-WITNESS

1. **WHAT.** Witness attestation infrastructure — the third actor. Rows C8-016 (Witness), C8-059 (writer). Component: `services/watch/witness/`. Contract: `Watch.Witness.Attestation.v0`. Record class: `Watch.Witness.Attestation` (Canon 9 §6). Task identity: `watch.witness.attest.per_event`.
2. **CANON CLAUSES.** Canon 8 §16 (The Witness); Canon 8 §4.10 W10 (the watcher is watched from outside).
3. **DEFINITION OF DONE.** Every containment + reserved-decision + Watch-officer session carries a Witness attestation. Attestations are the only evidence Watch may cite for its own fitness (Canon 8 §21).
4. **QUALITY EVIDENCE.** Invariant class (attestation-per-Watch-act gate). Calibration under Canon 8 §16.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-S6-WATCH-SERVICE

1. **WHAT.** Canon 1 §12 S6 — continuous machine-speed detection/response Watch service sentence. Row C1-069. Component: `services/watch/service.py` (top-level Canon-1 six-services entry point wiring). Contract: `Watch.Service.Registration.v0`. Record class: N/A. Task identity: `watch.service.per_instance`.
2. **CANON CLAUSES.** Canon 1 §12 (six services); Canon 8 §1 (What the Watch Is).
3. **DEFINITION OF DONE.** Watch appears as the sixth service at the platform boundary; every application crossing the boundary passes Watch scrutiny (Canon 1 §7.1 peer authority). Verification: platform-boundary audit shows six services live.
4. **QUALITY EVIDENCE.** Inventory audit (six-services listing) + drill. Calibration under Canon 1 §12.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION`, `WS-BUILD-WATCH-ACTORS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-CONSOLE-WATCH

1. **WHAT.** Watch Console as the fourth tile-group under the Admin surface's tile-grid-plus-detail-card grammar per Instruction 02. Tiles (four, verbatim from Canon 8 §13): `State` · `Record` · `Under Watch` · `Decisions`. Component: new frontend Watch-Console + backend data feeds. Contract: `Watch.Console.Tile.v0`. Record class: consumes Watch record classes (reader only). Task identity: sessions run under Watch identity per Canon 9. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md`; `test_four_questions_topline_present` on new-invariants list.**
2. **CANON CLAUSES.** Canon 8 §13 (Watch Console — four panels); Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED; Watch as fifth, rendered as fourth Admin-surface tile group per Instruction 02); Ruling 3 (Instruction 02).
3. **DEFINITION OF DONE.** Watch Console renders as a fourth tile-group with EXACTLY four tiles named `State`, `Record`, `Under Watch`, `Decisions`. **Watch-officer role-gated** (only watch-officer role sees the group). **Sessions run under Watch identity per Canon 9 (Task Identity Register).** **NEVER nested under Trust Center or any Compliance-Console tile — placement invariant test asserts this.** Verification: role-audit + placement-audit.
4. **QUALITY EVIDENCE.** Inventory audit (four-tile invariant + placement invariant + role-gate) + drill (watch-officer session end-to-end). Calibration under Canon 8 §13 + Instruction 02.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`. Reference screenshot pending (FL-P1-14).
6. **CREDIT COST CLASS.** L. Justification: 3+ components (4 tiles), new register/console (Watch tile-group), 3 integration surfaces (shell + Watch record classes + role-gate).
7. **REVERSAL COST.** Very high — placement change post-launch would break Instruction 02 explicit constraint; Watch-officer credentials outside the group is a Canon 8 §21 W-negative violation.

---

### H. Mkondo Charter (Canon 9, 45 rows → 6 items)

#### WS-BUILD-MKONDO-CHARTER

1. **WHAT.** Structure-only orchestration service — Mkondo maintains three registers, answers-here-not-memory. Rows C9-001..C9-003, C9-043..C9-047 (change + precedence + silence-as-finding). Component: `services/mkondo/charter.py`. Contract: `Mkondo.Charter.v0`. Record class: N/A (Mkondo is the registrar for others). Task identity: `mkondo.charter.per_change`.
2. **CANON CLAUSES.** Canon 9 §1-§3 (Mkondo Charter); Canon 9 §4-§8 (precedence, silence-as-finding, change).
3. **DEFINITION OF DONE.** Mkondo owns three registers (record matrix, task-identity, handoffs); every register access goes through Mkondo. Structure-only — Mkondo answers questions ABOUT records but NEVER holds the records themselves.
4. **QUALITY EVIDENCE.** Invariant class (structure-only gate) + inventory audit. Calibration under Canon 9 §3.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (three registers coordinated), new engine/authority (Mkondo is a Canon-9 first-class authority), 3 integration surfaces.
7. **REVERSAL COST.** Very high — Mkondo is the register-of-registers; removing it means the three registers lose their shared discipline.

#### WS-BUILD-RECORD-MATRIX

1. **WHAT.** Record matrix — 13 writer→readers rows. Rows C9-006..C9-018. Component: `services/mkondo/record_matrix/` (matrix definition + enforcement). Contract: `Record.Matrix.Entry.v0`. Record class: `Record.Matrix.Entry` (writer = Mkondo). Task identity: `matrix.entry.per_class`.
2. **CANON CLAUSES.** Canon 9 §6-§18 (record matrix — 13 rows).
3. **DEFINITION OF DONE.** All 13 record classes have matrix entries: writer role, reader-list, contract shape. AST discipline check enforces writer-role exclusivity and reader-list scoping. Verification: every service in the spine that writes a matrix-tracked class is the sole writer per matrix; every reader is in the reader-list.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped writer + reader gates). Uncurated sample: full codebase AST scan. Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-LEDGER-MATRIX` (Part 1 — anchors ledger writer), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Estate-wide wiring — every writer / reader across the entire spine is subject to matrix discipline; introduces 13 new contracts simultaneously; matrix is the substrate for all Canon-9 governance. Meets XL bar on estate-wide axis alone; also meets multi-new-contract axis.
7. **REVERSAL COST.** Very high — matrix defines the entire records governance; removal reverts to ad-hoc ownership. Records written stay.

#### WS-BUILD-READING-DISCIPLINE

1. **WHAT.** Reading discipline — matrix reader-list enforcement across Compliance Console + Watch Console. Rows C9-019..C9-022. Component: `services/mkondo/reading_discipline/`. Contract: enforced via record-matrix reader-list. Record class: N/A. Task identity: `matrix.read.per_call`.
2. **CANON CLAUSES.** Canon 9 §7 (reading discipline); Canon 9 §8 (matrix reader-list scoping).
3. **DEFINITION OF DONE.** Every read of a matrix-tracked class goes through the matrix reader path; unauthorized reads refuse with a Canon 9 §7 refusal. Compliance Console reads only its scoped classes; Watch Console reads only its scoped classes.
4. **QUALITY EVIDENCE.** Invariant class (matrix-reader gate). Uncurated sample: one drill week of console reads. Calibration under Canon 9 §7.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1), `WS-BUILD-CONSOLE-WATCH`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-TASK-IDENTITY-REGISTER

1. **WHAT.** Task-identity register — 13 entries. Rows C9-023..C9-035, C7-D22. Component: `services/mkondo/task_identity/`. Contract: `Task.Identity.Registration.v0`. Record class: `Task.Identity` (writer = Mkondo). Task identity: `task_identity.register.per_task`.
2. **CANON CLAUSES.** Canon 9 §5 (task identity); Canon 8 §4.11 W11 (one task, one identity); Canon 7 §D22 (D-Dual-Hat defect).
3. **DEFINITION OF DONE.** Every runtime task carries exactly one registered task identity. Dual-hat tasks refuse (D-Dual-Hat defect). Verification: AST scan confirms every service call site is task-identity-tagged.
4. **QUALITY EVIDENCE.** Invariant class (task-identity-per-call gate + no-dual-hat gate). Calibration under Canon 8 §4.11 + Canon 9 §5.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-BUILD-INPUT-SEAT-DUAL`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Estate-wide — every task-taking call site across the spine registers here; 13 new contract entries land simultaneously; task identity is the substrate for W11 discipline (one of the fourteen Canon-8 doctrines). Both estate-wide-wiring and multi-new-contract axes meet XL.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL

1. **WHAT.** Structural credential-scope discipline — no credential spans both authorities. Row C7-D23 (D-Cross-Auth-Credential defect). Component: `services/mkondo/credential_scope/`. Contract: `Credential.Scope.v0`. Record class: `Credential.Scope` (writer = Mkondo). Task identity: `credential.scope.per_grant`.
2. **CANON CLAUSES.** Canon 8 §21 W-negative (no credential scope spans both authorities); Canon 9 §5 (task identity); Canon 7 §D23.
3. **DEFINITION OF DONE.** Every credential grant carries a scope; cross-authority scope refuses (D-Cross-Auth-Credential). Verification: AST scan of grants + credential-inventory audit shows dual-scope count = 0.
4. **QUALITY EVIDENCE.** Invariant class (no-dual-scope gate). Calibration under Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

#### WS-BUILD-HANDOFF-REGISTRY

1. **WHAT.** Six handoff contracts (chokepoint→model, verdict→response, containment→decision, mirage-release→reconciliation, disagreement→resolution, Watch findings→CIF). Rows C9-037..C9-042, C7-D21. Component: `services/mkondo/handoff_registry/`. Contract: `Handoff.Contract.v0` (frozen shape with parameter subclasses per handoff type). Record class: `Handoff.Contract` (Canon 9 §6). Task identity: `handoff.per_type`.
2. **CANON CLAUSES.** Canon 9 §6 (handoff contracts); Canon 7 §D21 (D-Handoff-Missing).
3. **DEFINITION OF DONE.** All six handoffs registered; every call across a Canon-9 seam uses a registered handoff shape; unregistered handoffs refuse. Verification: seam-audit shows six live handoffs.
4. **QUALITY EVIDENCE.** Invariant class (handoff-shape gate at every seam). Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-ADMISSION-HANDOFF` (Part 1 — registers the existing admission handoff), `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-WATCH-TO-CIF`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 2 components + 6 new contracts (handoff shapes) — meets L on register axis.
7. **REVERSAL COST.** Very high.

---

### I. Conditioned Ideation Faculty (Canon 2, ~30 rows → 6 items)

#### WS-CIF-COACH-SEAT

1. **WHAT.** Coach seat + origination port — the ONLY seat that adopts frames. Rows C2-009, C2-031. Component: `services/cif/coach_seat/`. Contract: `Coach.Seat.Adoption.v0`. Record class: `Coach.Seat.Adoption` (writer = coach seat). Task identity: `coach.adopt.per_frame`.
2. **CANON CLAUSES.** Canon 2 §12 (coach seat + origination port constitutional load-bearing).
3. **DEFINITION OF DONE.** Only the coach seat adopts frames (no other origination surface); frame adoptions ledgered; frame origin evidenced.
4. **QUALITY EVIDENCE.** Invariant class (single-origination-port AST gate). Calibration under Canon 2 §12.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-SOLVA-CIF` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new authority (coach seat) + 1 new contract.
7. **REVERSAL COST.** Very high — Canon 2 §12 constitutional load-bearing.

#### WS-CIF-ARCHIVE

1. **WHAT.** CIF living archive — four-state discipline + silence-is-a-data-state + rejection-names-condition + rent + zero-inherited-credibility + paper-first. Rows C2-019..C2-023. Component: `services/cif/archive/`. Contract: `Archive.Entry.v0` (frozen 4-state). Record class: `Archive.Entry` (writer = archive). Task identity: `cif.archive.per_entry`.
2. **CANON CLAUSES.** Canon 2 §10-§13 (Living Archive discipline).
3. **DEFINITION OF DONE.** Archive entries in exactly one of four states {proposed, provisionally-adopted, adopted, rejected}; silence is data-state (Canon 2); rejection names condition; entries pay rent (Canon 2 §11); zero inherited credibility from parent artefacts; paper-first before compute (Canon 2 §13).
4. **QUALITY EVIDENCE.** Invariant class (4-state + rent gates). Calibration under Canon 2 §10.
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-CIF-DETECTION

1. **WHAT.** Frame-signature detection (cascade / absorption / misfit). Rows C2-029, C2-030. Component: `services/cif/detection/`. Contract: `Frame.Signature.Detection.v0`. Record class: `Frame.Signature.Detection`. Task identity: `cif.detect.per_signal`.
2. **CANON CLAUSES.** Canon 2 §15-§16 (detection modes).
3. **DEFINITION OF DONE.** Signals arriving at CIF are classified into one of the three detection modes; detection events ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (three-mode fixture). Calibration under Canon 2 §15.
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT`, `WS-BUILD-WATCH-TO-CIF` (Watch findings feed detection), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** High.

#### WS-CIF-METABOLISATION

1. **WHAT.** Four-step frame-adoption sweep + build check. Rows C2-032, C2-033. Component: `services/cif/metabolisation/`. Contract: `Metabolisation.Step.v0`. Record class: `Metabolisation.Step`. Task identity: `cif.metabolise.per_frame`.
2. **CANON CLAUSES.** Canon 2 §17 (metabolisation sweep).
3. **DEFINITION OF DONE.** Every frame adoption traverses all four metabolisation steps; build check fires at closure; incomplete metabolisation refuses.
4. **QUALITY EVIDENCE.** Invariant class (four-step gate) + drill. Calibration under Canon 2 §17.
5. **DEPENDENCIES.** `WS-CIF-ARCHIVE`, `WS-CIF-DETECTION`, `WS-WIRE-SOLVA-CIF` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

#### WS-CIF-MONITORING

1. **WHAT.** Condition watchers + cascade detection + adversarial elicitation. Rows C2-034..C2-036. Component: `services/cif/monitoring/`. Contract: `Cif.Condition.Watch.v0`. Record class: `Cif.Condition.Watch`. Task identity: `cif.monitor.per_condition`.
2. **CANON CLAUSES.** Canon 2 §18 (monitoring); Canon 8 §5 (Watch to CIF handoff).
3. **DEFINITION OF DONE.** Condition watchers active; cascades detected pre-emptively; adversarial elicitation runs on schedule; findings ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (adversarial elicitation fixture). Calibration under Canon 2 §18.
5. **DEPENDENCIES.** `WS-CIF-DETECTION`, `WS-BUILD-WATCH-TO-CIF`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

#### WS-CIF-PARAMETERS

1. **WHAT.** CIF operative + quality parameters. Rows C2-040..C2-051 (manifest coverage, archive completeness, escalation latency, metabolisation execution, rent collection, promise metric, manifest hit-rate, provisional honesty, metabolisation closure, overhead ceiling, false-escalation rate, defaults). Component: `services/cif/parameters/`. Contract: `Cif.Parameter.Reading.v0`. Record class: `Cif.Parameter.Reading`. Task identity: `cif.parameter.per_cycle`.
2. **CANON CLAUSES.** Canon 2 §19 (Operative Parameters); Canon 2 §20 (Quality Parameters).
3. **DEFINITION OF DONE.** Every parameter measured continuously; latest reading is the one shown; drift monitored. Verification: parameter dashboard shows all 12 parameters within Canon 2 §19 bounds during a drill week.
4. **QUALITY EVIDENCE.** Contract test + inventory audit (12 parameters live). Calibration under Canon 2 §19-§20.
5. **DEPENDENCIES.** `WS-CIF-*` (all preceding CIF items), `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (parameters + measurement + rendering), new register.
7. **REVERSAL COST.** High.

---

### Part-2 item count summary

| Group | Count | Items |
|---|---:|---|
| A. Custody & Boundary | 3 | WS-BUILD-DECL, WS-BUILD-INPUT-SEAT, WS-BUILD-INPUT-SEAT-DUAL |
| B. Extraction Quality | 2 | WS-BUILD-MOAC-SCORECARD, WS-BUILD-ADAPTER-REGISTRY |
| C. Ports (Ruling B new) | 2 | WS-BUILD-STREAMING-PORT, WS-BUILD-OBJECT-STORAGE-PORT |
| D. Integration | 2 | WS-BUILD-WEBHOOK, WS-BUILD-PLANE-PRECOMPUTE |
| E. Governance Ceremony | 5 | WS-BUILD-VERIFICATION-RUNNER, WS-BUILD-PROVE-ONE-RUN, WS-BUILD-SETUP-CONSOLE, WS-BUILD-DAY-ZERO, WS-BUILD-RULEBOOK-SURFACE |
| F. Interface BUILD (no donor) | 13 | Model-Catalogue, Batch-Board, Quality-Obs, Agent-Chip, Refusal-Card-Copy, Three-Lenses, Answer-Card, Five-Pillars, Pulse-News, Studio, Learn-Pillar, Reference-App, Control-Band |
| G. Watch | 16 | Foundation, Actors, Reconciler, Mark-Registry, Containment, Mirage, Signature-Store, Decisions-Panel, Watch-Day, Drill-Harness, Authority-Peerage, Record-Classes, To-CIF, Attestation-Witness, S6-Watch-Service, Console-Watch |
| H. Mkondo | 6 | Charter, Record-Matrix, Reading-Discipline, Task-Identity-Register, Credential-Scope-Structural, Handoff-Registry |
| I. CIF | 6 | Coach-Seat, Archive, Detection, Metabolisation, Monitoring, Parameters |
| **Total** | **55** | |

**Reconciliation with row_to_item_index.md counts.** The initial count of 42 Part-2 items (55 - 13 interface reclassifications) has expanded to 55 because Ruling B mandated bundling by canonical MECHANISM rather than one-mega-item-per-canon. Watch expanded from ~10 items to 16; Ports promoted from folded dependencies to 2 standalone items (Streaming, Object-Storage). Grand total now: 47 Part 1 + 55 Part 2 = **102 work items**.

**New contracts + Parity-seat linkage.** Every item in this file with a `Contract:` line lists `WS-WIRE-PARITY-EXTENSION` as a dependency — enforced during the completeness audit.

**Ruling-1 transition linkage verified in:** `WS-BUILD-DECL` (precondition a) and `WS-BUILD-WATCH-RECONCILER` (precondition b). Both name `WS-CONTRADICTION-PURPOSE-GATE` as the item they lawfully permit to strip once both fire.

**Fidelity ledger entries opened in this file:** FL-P1-03 (Object Storage Port placement — resolved with PROPOSAL, ledger stays OPEN pending owner ratification); FL-OQ-05 (Studio scope reclassification — L → XL if storage-plane composition).


---

## §§6-9 · Strategy-level sections

Inlined verbatim from the working paper `notes/strategy_sections.md`. Section IDs preserved (§1 · §2 · §3 · §4 · §5 within the working paper map here as §6 · §7 · §8 · §9 · §10-freeze-note).

Post-Part-2 sections per Orchestrator Ruling B: sequencing · transition windows (T1 = Ruling 1 gate) · no-regression contract · waste register · fidelity ledger freeze.

---

### §1 · Proposed sequence with dependency logic

**Not a schedule.** A dependency ordering — items whose predecessors are not landed cannot lawfully proceed. Sequencing is Owner territory; this is the logical earliest each item CAN start.

#### 1.1 Dependency ordering (topological, coarse)

**Wave 0 — Foundational registers, must land before any authority-consuming work.**
- `WS-BUILD-MKONDO-CHARTER` — Mkondo is the register-of-registers.
- `WS-BUILD-RECORD-MATRIX` — defines every writer-role.
- `WS-BUILD-TASK-IDENTITY-REGISTER` — Canon 8 W11 substrate.
- `WS-WIRE-PARITY-EXTENSION` — every new contract lands only through this.
- `WS-BUILD-HANDOFF-REGISTRY` — six handoff shapes.

Rationale: Every subsequent item names one or more of these as a dependency. Land them first; land them once.

**Wave 1 — Ports and boundary.**
- `WS-BUILD-STREAMING-PORT` — anchors `WS-HARVEST-STREAMING`.
- `WS-BUILD-OBJECT-STORAGE-PORT` (FL-P1-03 pending owner ratification) — anchors work-studio migration.
- `WS-BUILD-INPUT-SEAT`, `WS-BUILD-INPUT-SEAT-DUAL`.
- `WS-WIRE-LEDGER-MATRIX` — anchors Northena in the matrix.
- `WS-WIRE-ADMISSION-HANDOFF` — registers existing admission handoff.

**Wave 2 — Governance and declaration.**
- `WS-BUILD-DECL` — declaration seat + check + supersession (Ruling-1 precondition a).
- `WS-WIRE-CUSTODY-DECL` — wires DECL into admit fail-closed.
- `WS-BUILD-RULEBOOK-SURFACE`, `WS-BUILD-CEREMONY-REVERIFY`, `WS-BUILD-VERIFICATION-RUNNER`.

**Wave 3 — Watch foundation and three actors.**
- `WS-BUILD-WATCH-FOUNDATION`.
- `WS-BUILD-WATCH-ACTORS`.
- `WS-BUILD-WATCH-RECORD-CLASSES`.
- `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-WATCH-MIRAGE`, `WS-BUILD-WATCH-ATTESTATION-WITNESS`.
- `WS-BUILD-WATCH-AUTHORITY-PEERAGE`.
- `WS-BUILD-WATCH-RECONCILER` (Ruling-1 precondition b).
- `WS-BUILD-WATCH-DRILL-HARNESS`.
- `WS-BUILD-WATCH-TO-CIF`.
- `WS-BUILD-S6-WATCH-SERVICE`.

**Wave 4 — Extraction quality + CIF spine.**
- `WS-HARVEST-BATCH-QUARANTINE`, `WS-HARVEST-GAP-FILER`, `WS-HARVEST-REGISTRY-CONTEXT`, `WS-HARVEST-PARTITIONS`, `WS-HARVEST-SEQUENCING-HARNESS` (pending FL-P1-01), `WS-HARVEST-FAR-ENDPOINT`.
- `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-ADAPTER-REGISTRY`.
- `WS-CIF-COACH-SEAT`, `WS-CIF-ARCHIVE`, `WS-CIF-DETECTION`, `WS-CIF-METABOLISATION`, `WS-CIF-MONITORING`, `WS-CIF-PARAMETERS`.
- `WS-WIRE-SOLVA-CIF`.

**Wave 5 — Critic seam in-flight + Loop.**
- `WS-HARVEST-CRITIC-SEAM`.
- `WS-WIRE-CRITIC-INTO-ANSWERING`.
- `WS-WIRE-LOOP-ORCH`, `WS-WIRE-REGISTRY`, `WS-WIRE-INTENT-AUDIT-WATCH`, `WS-WIRE-WATCH-PLANE-ACTIVITY`.
- `WS-BUILD-INDEPENDENCE-GATE`, `WS-BUILD-STANDING-QUERY-SURFACE`.

**Wave 6 — RE-POINT + REBUILD.**
- `WS-HARVEST-STREAMING` (already Wave 1 — landing point for the port).
- `WS-HARVEST-TWO-PASS-AMENDMENT`.
- `WS-REPOINT-ANSWERING-SURFACES` (XL — the estate-wide adapter swap).
- `WS-REPOINT-SOLVA-V2`.
- `WS-REPOINT-SOLVA-VOICE-AUDIT` (path A or B pending FL-P1-02).
- `WS-REPOINT-WORK-STUDIO-LLM`.
- `WS-REBUILD-WORK-STUDIO-STORAGE` (XL — user-data migration; shadow-write phase then reader cutover; owner sign-off on the commissioning certificate).

**Wave 7 — Interface (harvest + tile-grid grammar).**
- `WS-HARVEST-SHELL-GRAMMAR` (donates the tile-grid).
- `WS-HARVEST-COMPONENT-LIBRARY`, `WS-HARVEST-CLASS-CHIP-LIBRARY`, `WS-HARVEST-REFUSAL-CARD`, `WS-HARVEST-DORMANT-STATE`.
- Console harvests: `WS-HARVEST-CONSOLE-EXTRACTION`, `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-HARVEST-CONSOLE-INTEGRATION`, `WS-HARVEST-CONSOLE-ADMINISTRATION`.
- Placement modifiers: `WS-MODIFY-PLANE-OBSERVABILITY`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT`, `WS-MODIFY-AUDIT-TRAIL-PLACEMENT`, `WS-MODIFY-USE-DATA-PLACEMENT` (pending FL-P1-10), `WS-MODIFY-VERDICT-DEMO` (pending FL-P1-11).

**Wave 8 — Interface BUILD (no donor) + Watch Console.**
- `WS-BUILD-FIVE-PILLARS`, `WS-BUILD-CONTROL-BAND`.
- `WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE`, `WS-BUILD-BATCH-BOARD-SURFACE`, `WS-BUILD-QUALITY-OBSERVATION`.
- `WS-BUILD-REFUSAL-CARD-COPY`, `WS-WIRE-REFUSAL-FAMILY`, `WS-BUILD-AGENT-ASSUMED-CHIP`.
- `WS-BUILD-THREE-LENSES`, `WS-BUILD-ANSWER-CARD`.
- `WS-BUILD-REFERENCE-APP`.
- `WS-BUILD-PULSE-NEWS`, `WS-BUILD-STUDIO` (pending FL-OQ-05), `WS-BUILD-LEARN-PILLAR`.
- `WS-BUILD-CONSOLE-WATCH` (Instruction 02 exception — fourth tile-group, watch-officer gated).
- `WS-BUILD-SETUP-CONSOLE`, `WS-BUILD-DAY-ZERO`.

**Wave 9 — Governance ceremony completion + retirements.**
- `WS-BUILD-PROVE-ONE-RUN`, `WS-BUILD-DELIVERABLE-ATTESTATIONS` (Part 1).
- `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL`, `WS-BUILD-READING-DISCIPLINE`.
- `WS-BUILD-WEBHOOK`, `WS-BUILD-PLANE-PRECOMPUTE`.
- `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-BUILD-WATCH-DAY` (Watch Console operational).
- `WS-RETIRE-APP-TERRITORY`, `WS-RETIRE-XCUT-SECURITY`, `WS-RETIRE-FRONTEND-ARCHIVES`, `WS-RETIRE-PROTOTYPE-DIVERGENCE`, `WS-RENAME-PROTOTYPE-TAXONOMY`.

**Wave 10 — Purpose-gate transition (T1 window).**
- Verify `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` both fire in drills (both attested in the ledger).
- On confirmation, `WS-CONTRADICTION-PURPOSE-GATE` strip proceeds via Canon 3 §24 rule-change ceremony (path FL-R1-01 pending owner ruling).

#### 1.2 Guardrails on the sequence

- **No Wave-N item lands with an unlanded Wave-(N-1) dependency.** Enforced by the completeness audit script pre-submission.
- **XL items require review pack + one-paragraph defence.** **Seven XL items** (Build-Order-01 correction, was mis-stated as nine): `WS-REPOINT-ANSWERING-SURFACES` (Part 1) · `WS-REBUILD-WORK-STUDIO-STORAGE` (Part 1) · `WS-BUILD-OBJECT-STORAGE-PORT` (Part 2) · `WS-BUILD-WATCH-FOUNDATION` (Part 2) · `WS-BUILD-WATCH-ACTORS` (Part 2) · `WS-BUILD-RECORD-MATRIX` (Part 2) · `WS-BUILD-TASK-IDENTITY-REGISTER` (Part 2). Each carries the defence in its item entry. Two additional items carry conditional XL classification (not counted): `WS-REPOINT-SOLVA-VOICE-AUDIT` (L on path A, XL on path B — closed to path A per FL-P1-02); `WS-BUILD-STUDIO` (L baseline, XL if storage-plane composition — deferred per FL-OQ-05, stays L).
- **Reversal-cost gates.** Every VERY HIGH item requires an owner sign-off on the commissioning certificate before completing the reader-cutover.

---

### §2 · Transition windows

Transitions between old-and-new operating states of the estate. Named windows have named guards.

#### 2.1 T1 — Purpose-gate transition (Ruling 1 gate)

**Window definition.** Between `WS-BUILD-DECL` demonstrated-firing AND `WS-CONTRADICTION-PURPOSE-GATE` strip ceremony completion.

**Guards (from Ruling 1 + `WS-CONTRADICTION-PURPOSE-GATE`):**
- G-T1-A: Executive-Core's `purpose_validator.validate_purpose()` gate STAYS in force. Refusals from it continue to write to the ledger.
- G-T1-B: `WS-BUILD-DECL` demonstrated-firing evidence is recorded in the ledger (a drill exports a declaration-refusal event).
- G-T1-C: `WS-BUILD-WATCH-RECONCILER` demonstrated-firing evidence is recorded in the ledger (a drill exports a governance×Watch reconciliation event).
- G-T1-D: A Canon 3 §24 rule-change ceremony executes the strip. Path (Canon-3 §24 ceremony OR Watch verdict) resolves per FL-R1-01 owner ruling.

**Prohibited during window:** any code deletion of the purpose gate. Any downstream service assuming the gate is stripped.

**Exit:** Strip event ledgered + parity-seat entries confirmed for both new contracts + Compliance Console read-back shows the gate stripped.

#### 2.2 T2 — Executive-Core to application transition

**Window definition.** Between `WS-REPOINT-ANSWERING-SURFACES` start AND `WS-RETIRE-APP-TERRITORY` completion.

**Guards.**
- G-T2-A: Application-territory services (`services/cohort/`, `stripe_webhook.py`, etc.) run in parallel until adapter swap completes per surface.
- G-T2-B: Every RE-POINTed surface's adapter is atomic — no partial adapter states.
- G-T2-C: FL-OQ-10 owner ruling defines whether Executive-Core becomes an application, is archived, or is maintained parallel. Window cannot close without ruling.

**Prohibited during window:** any answer surface running on two adapters simultaneously.

**Exit:** All application-territory services either archived or moved to application layer; platform boundary contains none of the retired names (Canon 1 §12 audit).

#### 2.3 T3 — Work-Studio storage migration

**Window definition.** Between `WS-BUILD-OBJECT-STORAGE-PORT` completion AND `WS-REBUILD-WORK-STUDIO-STORAGE` reader-cutover.

**Guards.**
- G-T3-A: Shadow-write phase — new writes go to BOTH mongo + plane; reads stay on mongo. Reversible.
- G-T3-B: Reader-cutover — reads move to plane. **Not reversible** for reads that landed during shadow-write against plane-only edits (see WS-REBUILD REVERSAL COST).
- G-T3-C: Owner sign-off on the commissioning certificate BEFORE reader-cutover. Certificate is the Canon 6 §11 shape.
- G-T3-D: Migration certificate lists every one of the 200+ exports with pre-and-post hash.

**Prohibited during window:** any user-visible loss of prior work.

**Exit:** Reader-cutover ledgered; commissioning certificate signed; all 200+ exports byte-identical pre-and-post.

#### 2.4 T4 — Interface tile-grid landing

**Window definition.** Between `WS-HARVEST-SHELL-GRAMMAR` start AND `WS-BUILD-CONSOLE-WATCH` complete.

**Guards.**
- G-T4-A: Reference screenshot MUST have arrived in the workspace before any interface item lands rendering code. Fixture-pending on every interface item (FL-P1-14).
- G-T4-B: Watch Console NEVER nests under Trust Center at any point in the transition — placement invariant enforced by inventory audit.
- G-T4-C: Every retired prototype label (`WorkStudio`, `Trust Center`, `*Shield` naming) removed only after its replacement is live.

**Exit:** Nav audit confirms 100% Canon-5 conformance + Watch Console fourth-group present.

---

### §3 · No-regression contract

Every item's DoD depends on existing standing invariant tests continuing to hold, AND on new invariant tests landing before the item's completion. This section names both sets.

#### 3.1 Existing standing invariant tests that MUST continue to hold (Extraction-Akki HEAD `b150c21`)

Cited from `Extraction-Akki/backend/tests/invariants/` (verified via direct `find`):

| Test file | Guards |
|---|---|
| `test_invariant_contract_snapshots.py` | Parity seat — freezes every listed contract shape. Extended by `WS-WIRE-PARITY-EXTENSION`. |
| `test_northena_ledger_row_v0.py` | Ledger row shape frozen. Guarded by `WS-WIRE-LEDGER-MATRIX`. |
| `test_admission_refusal_v0_contract_frozen.py` | Admission refusal shape frozen. Used by `WS-WIRE-CUSTODY-DECL`. |
| `test_ast_egress_gate.py` | Content-boundary AST gate. Model for new AST tests in `WS-WIRE-WATCH-PLANE-ACTIVITY`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL`. |
| `test_v0_paths_byte_identical_after_4a.py` | Loop replay byte-identical. Guards `WS-WIRE-LOOP-ORCH`. |
| `test_targeta_invariants.py` (mining_plan_contract, yield-layer permutation guard) | Loop invariants. Guards `WS-WIRE-LOOP-ORCH`. |
| `test_solva_assertion_boundary.py` (conclusion_class_signature, class_is_floor_over_load_bearing_all_fact) | Solva boundary. Guards `WS-WIRE-SOLVA-CIF`, `WS-REPOINT-SOLVA-V2`. |
| `test_govern_g_g1_to_g_g8.py` | Rule-change ceremony state-machine. Guards `WS-BUILD-CEREMONY-REVERIFY`. |
| `test_g_13_execution_atomic.py` | Governance-13 execution atomicity. Guards `WS-WIRE-REGISTRY`. |
| `test_partition_schema_v0_envelope.py` | Partition envelope shape. Guards `WS-HARVEST-PARTITIONS`. |
| `test_registry_context_block_golden_snapshot.py` | Registry context snapshot. Guards `WS-HARVEST-REGISTRY-CONTEXT`. |
| `test_generated_gates_regeneration_diff.py` | Gate regeneration byte-identical. Guards `WS-HARVEST-FAR-ENDPOINT`. |
| `test_critic_pass_execution_atomic.py` (in Akki-OS-V1) | Critic seam execution atomicity. Guards `WS-HARVEST-CRITIC-SEAM`. |
| `test_cif_manifest_submission_gate.py` (in Akki-OS-V1) | Manifest gate. Guards `WS-WIRE-CRITIC-INTO-ANSWERING`. |
| `test_memory_service_m_g1_to_m_g9.py` (spine) | Memory service invariants. Guards `WS-REBUILD-WORK-STUDIO-STORAGE`. |
| `gate1_class_inseparable.test.js` (frontend) | Class chip inseparable from claim. Guards `WS-HARVEST-CLASS-CHIP-LIBRARY`, `WS-BUILD-AGENT-ASSUMED-CHIP`. |
| `gate2_refusal_firstclass.test.js` | Refusal card first-class. Guards `WS-HARVEST-REFUSAL-CARD`, `WS-BUILD-REFUSAL-CARD-COPY`. |
| `test_auth_denied_notice_not_refusal_card.test.js` | Auth-denied ≠ refusal card. Guards `WS-HARVEST-REFUSAL-CARD`. |
| `test_shared_components_single_source.test.js` | Component library single-source. Guards `WS-HARVEST-COMPONENT-LIBRARY`. |

#### 3.2 New standing invariant tests to write FIRST (before the item they gate lands)

| New test | Gates item(s) |
|---|---|
| `test_declaration_v0_contract_frozen.py` | `WS-BUILD-DECL` |
| `test_input_seat_envelope_v0_contract_frozen.py` | `WS-BUILD-INPUT-SEAT` |
| `test_input_seat_identity_one_per_task.py` | `WS-BUILD-INPUT-SEAT-DUAL` |
| `test_moac_scorecard_v0_contract_frozen.py` | `WS-BUILD-MOAC-SCORECARD` |
| `test_adapter_registration_v0.py` | `WS-BUILD-ADAPTER-REGISTRY` |
| `test_streaming_frame_v0_contract_frozen.py` | `WS-BUILD-STREAMING-PORT` |
| `test_object_storage_blob_v0_contract_frozen.py` | `WS-BUILD-OBJECT-STORAGE-PORT` |
| `test_webhook_envelope_v0.py` | `WS-BUILD-WEBHOOK` |
| `test_verification_pack_v0_contract_frozen.py` | `WS-BUILD-VERIFICATION-RUNNER` |
| `test_prove_one_run_pack_v0.py` | `WS-BUILD-PROVE-ONE-RUN` |
| `test_setup_record_v0_contract_frozen.py` | `WS-BUILD-SETUP-CONSOLE` |
| `test_commissioning_certificate_v0.py` | `WS-BUILD-DAY-ZERO` |
| `test_rulebook_rule_v0_contract_frozen.py` | `WS-BUILD-RULEBOOK-SURFACE` |
| `test_watch_verdict_v0.py`, `test_watch_action_v0.py`, `test_watch_attestation_v0.py` | `WS-BUILD-WATCH-ACTORS` |
| `test_watch_reconciliation_v0.py` | `WS-BUILD-WATCH-RECONCILER` (Ruling-1 firing evidence lives here) |
| `test_watch_mark_v0_contract_frozen.py` | `WS-BUILD-WATCH-MARK-REGISTRY` |
| `test_watch_containment_v0.py` + `test_watch_no_auto_extend.py` | `WS-BUILD-WATCH-CONTAINMENT` |
| `test_watch_mirage_no_render.py` (AST) | `WS-BUILD-WATCH-MIRAGE` |
| `test_watch_signature_no_reader.py` (AST) | `WS-BUILD-WATCH-SIGNATURE-STORE` |
| `test_watch_reserved_no_machine_execute.py` | `WS-BUILD-WATCH-DECISIONS-PANEL` |
| `test_watch_day_no_threshold_render.py` | `WS-BUILD-WATCH-DAY` |
| `test_watch_drill_receipt_v0.py` | `WS-BUILD-WATCH-DRILL-HARNESS` |
| `test_watch_disagreement_v0.py` | `WS-BUILD-WATCH-AUTHORITY-PEERAGE` |
| `test_record_matrix_writer_sole.py` (AST) | `WS-BUILD-RECORD-MATRIX` |
| `test_task_identity_one_per_call.py` (AST) | `WS-BUILD-TASK-IDENTITY-REGISTER` |
| `test_credential_scope_no_dual.py` (AST) | `WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL` |
| `test_handoff_contract_v0.py` | `WS-BUILD-HANDOFF-REGISTRY` |
| `test_coach_seat_single_origination_port.py` (AST) | `WS-CIF-COACH-SEAT` |
| `test_cif_archive_four_state.py` | `WS-CIF-ARCHIVE` |
| `test_cif_metabolisation_four_step.py` | `WS-CIF-METABOLISATION` |
| `test_watch_console_placement_not_trust_center.py` | `WS-BUILD-CONSOLE-WATCH` (Instruction 02 constraint) |
| `test_watch_console_four_tiles.py` | `WS-BUILD-CONSOLE-WATCH` |
| `test_five_pillars_router.py` | `WS-BUILD-FIVE-PILLARS` |
| `test_three_lenses_class_chip_present.py` | `WS-BUILD-THREE-LENSES` |
| `test_answer_card_v0.py` | `WS-BUILD-ANSWER-CARD` |
| `test_agent_assumed_chip_present.test.js` | `WS-BUILD-AGENT-ASSUMED-CHIP` |
| `test_ceremony_re_verified_state.py` | `WS-BUILD-CEREMONY-REVERIFY` |
| `test_independence_gate_v0.py` | `WS-BUILD-INDEPENDENCE-GATE` |
| `test_deliverable_attestation_v0.py` | `WS-BUILD-DELIVERABLE-ATTESTATIONS` |
| `test_standing_query_v0.py` | `WS-BUILD-STANDING-QUERY-SURFACE` |
| `test_work_studio_migration_byte_identical.py` | `WS-REBUILD-WORK-STUDIO-STORAGE` |
| `test_console_placement_uniqueness.py` | `WS-MODIFY-PLANE-OBSERVABILITY`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT`, `WS-MODIFY-AUDIT-TRAIL-PLACEMENT` |

Every new test is a Canon-3 §31 verification-pack shape.

---

### §4 · Waste register

Things reversed, abandoned, or redundant in the strategy. Ledgered so the honest history persists.

| id | waste | reason | reversibility |
|---|---|---|---|
| W-01 | Chunk-1 §-anchor drift (72 rows) | Extraction script counted sub-paragraphs beyond heading boundaries. | REMEDIATED via Ruling A tools (`drift_map.py`, `drift_apply.py`, `drift_downstream.py`). Audit clean. |
| W-02 | 47 unassigned Canon-2 CIF rows in initial Chunk-3 domain tables | Domain-table drafting missed the CIF-specific rows. | REMEDIATED in `row_to_item_index.md` — CIF items WS-CIF-* opened. |
| W-03 | 4 folded WIRING items (critic-into-answering, parity-extension, refusal-family, ledger-matrix) | Folded silently under HARVEST/BUILD items. | REMEDIATED via Ruling 2 — promoted to standalone. |
| W-04 | 13 interface BUILD items folded before Instruction 02 | Chunk-3 defaulted interface to BUILD; Instruction 02 fixed Extraction-Akki as donor. | REMEDIATED via Ruling 3 — reclassified to HARVEST/MODIFY. |
| W-05 | Reference screenshot delay | Owner has not delivered the tile-grid-plus-detail-card grammar screenshot. | OPEN — interface items carry `FIXTURE CLEARED @ transcription grade (FL-P1-14 — transcription-cleared vs file-cleared distinction recorded). |
| W-06 | FL-P1-05, FL-P1-06, FL-P1-07 — specific-file identification for three MODIFY items deferred | Focused reads not done in Part-1 drafting. | Requires re-read pass; substance-anchored citations hold. |
| W-07 | `WS-CIF-METABOLISATION`-style adopting frames vs Solva's parameterless assertion boundary | Potential seam conflict: CIF metabolisation claims frames adopted; Solva assertion boundary refuses caveated claims. | RESOLVED by design — CIF submits ratified frames back to Solva via `WS-WIRE-SOLVA-CIF`, no self-certification permitted (Canon 2 permanent bound). |
| W-08 | `AuthLoginPage.js`, `AuthRegisterPage.js` — application territory but present in Extraction-Akki frontend | Auth is application-layer per Canon 1 §13; drift into Extraction-Akki is a Canon-1 §12 breach. | REMEDIATED via Ruling 3 → folded into `WS-RETIRE-APP-TERRITORY`. |

---

### §5 · Fidelity ledger freeze note

At `BUILD_STRATEGY.md` assembly, `notes/fidelity_ledger.md` is FROZEN in its current form. Any new open question found after assembly requires a re-open through the same discipline (owner ruling + new entry).

**Frozen state at assembly:**
- Section A (8 owner open questions inherited): FL-OQ-03 through FL-OQ-10.
- Section B (7 Part-1 field-level entries): FL-P1-01 through FL-P1-07.
- Section C (12 Instruction-02 rendering decisions): FL-P1-08 through FL-P1-19.
- Section D (1 Ruling-1 leftover): FL-R1-01.
- Section E (citation-drift disclosure with full remediation trail): FL-P1-20 — retained per Orchestrator Ruling A (defect history part of the honest record).
- Section F (Part-2 field-level entries — appended during Part 2 drafting): FL-P1-03 upgraded with PROPOSAL (new engine BUILD, XL); FL-OQ-05 additional note re Studio scope XL reclass.

Total open items at freeze: **27** (8 + 7 + 12 + 1 + 1 disclosure + 0 net new from Part 2 that weren't already in Section B).


---

## §10 · Canon fidelity ledger (frozen at assembly)

Frozen at BUILD_STRATEGY.md assembly per Ruling 2 §4. All 27 rows CLOSED by Build Order 01 (2026-08-14). Ledger retained as the honest history of the drafting process; any re-opening requires a Canon 3 §24 rule-change ceremony against this document.

**Status at Build Order 01 (2026-08-14):** All 27 rows CLOSED by owner ruling. Retained as the honest history of the drafting process. Any future re-opening requires a Canon 3 §24 rule-change ceremony against this document.

**Ruling source:** Build Order 01 (owner channel) — full verbatim in `STATE/DECISIONS.md`.

---

### A. Open Questions inherited from REUSE_ASSESSMENT.md §8 — ALL CLOSED

| id | question | Build Order 01 ruling |
|---|---|---|
| **FL-OQ-03** | Canon 3 §24 rule-change re-verify step — runtime state, artifact write, or both? | **CLOSED — Both**: re-verified is a runtime state in the ceremony state machine AND a compliance-artifact write, and the state transitions only on the artifact's successful write. |
| **FL-OQ-04** | Canon 5 four-vs-five consoles — canonical count? | **CLOSED — Five consoles**: the Watch Console is the fifth in canon and renders as the fourth tile group on the Admin surface; "four-plus-Watch" and "five" are the same fact. (Note: premise "§10 lists four consoles" was a paraphrase defect — Canon 5 §10 verbatim reads "The platform has exactly five consoles" with Watch in the console table.) |
| **FL-OQ-05** | Studio canonical scope for this cycle? | **CLOSED — Deferred**: Studio does not ship this cycle; `WS-BUILD-STUDIO` leaves Wave 8 for a later cycle and its nav presence renders in the dormant-state grammar, never a dead link. |
| **FL-OQ-06** | Eight-vs-five/four global rules — canonical count? | **CLOSED — Both counts stand**: they count different things — the Eight Global Rules are Canon 5's interface law; the Four Classes are Canon 3's governed-value taxonomy; the Rulebook surface's invariant counts rules in force per instance (seeded: four), never a canon constant. |
| **FL-OQ-07** | Cohort surface — application-layer or retire? | **CLOSED — Fully retire**: Cohort fully retires from the platform; if it returns, it returns as an application on the boundary like any third party, outside this programme. |
| **FL-OQ-08** | Work-Studio migration path? | **CLOSED — Shadow-write-then-cutover**: with guards G-T3-A…D exactly as written; owner signs the commissioning certificate BEFORE reader-cutover, and NOT before all 200+ export hashes are listed on it. |
| **FL-OQ-09** | Akki-OS-V1 harvests — into spine or stay? | **CLOSED — Harvest into the spine**: Akki-OS-V1 becomes read-only reference at Wave-4 completion. |
| **FL-OQ-10** | Executive-Core disposition? | **CLOSED — Application on the boundary**: Executive-Core becomes an application on the boundary; nothing is maintained parallel after T2's exit; only what RETIRE names is archived. |

---

### B. Part-1 field-level entries — ALL CLOSED

| id | question | Build Order 01 ruling |
|---|---|---|
| **FL-P1-01** | `sequencing_harness` canon anchor + harvest scope? | **CLOSED — Focused read at Wave-4 preparation**: harvest only what Targeta and Mtafiti don't already satisfy, and on full overlap reclassify to RETIRE and log the waste. |
| **FL-P1-02** | Voice-audit custody — path A RE-POINT or path B REBUILD? | **CLOSED — Default path A** (RE-POINT through the input seat); path B only if the focused read proves a second custody path that cannot transit the chokepoint; that read is now urgent (Build Order 01 §6). |
| **FL-P1-03** | Object Storage Port placement? | **CLOSED — Own BUILD item**: a port under the boundary governor's ownership, not a new engine and not absorbed into the record matrix; contract through parity-extension as planned. |
| **FL-P1-04** | Application-boundary transition — discrete milestone or continuous? | **CLOSED — Discrete milestone**: T2's exit is the single completion criterion, verified by the Canon 1 §12 boundary audit. |
| **FL-P1-05** | Specific reviewer-selector file for Independence Gate? | **CLOSED — Focused read as first task of item's wave**: WHAT-field updates in place; no build before the read lands. |
| **FL-P1-06** | Specific deliverable-attestation surface file? | **CLOSED — Same discipline**: focused read as first task of item's wave; WHAT-field updates in place; no build before the read lands. |
| **FL-P1-07** | Specific standing-query definition/execution file? | **CLOSED — Same discipline**: focused read as first task of item's wave; WHAT-field updates in place; no build before the read lands. |

---

### C. Instruction-02 rendering decisions — ALL CLOSED

**Governing principle** (Build Order 01 §2.C): _"The organisation's language renders on screen; the canon identity lives beneath; the mapping is recorded in this ledger. A label is never evidence of identity, and identity never forces a label."_

| id | rendering decision | Build Order 01 ruling |
|---|---|---|
| **FL-P1-08** | MemoryPlaneObservability home? | **CLOSED — Ratified**: memory-plane observability homes to the Compliance Console. |
| **FL-P1-09** | TraceReceipt home? | **CLOSED — Ratified**: trace receipt homes to the Compliance Console's prove-one-run export. |
| **FL-P1-10** | UseDataLanding home — Model Catalogue or Ask App? | **CLOSED — Ask reference application** (Canon 5 §37 Ask); the model catalogue is the Extraction Console's. |
| **FL-P1-11** | Verdict Demo — canon-required or retire? | **CLOSED — Retire**: the walk pattern in the attached brief supersedes it. |
| **FL-P1-12** | AuditTrail home? | **CLOSED — Ratified**: audit trail homes to the Compliance Console export. |
| **FL-P1-13** | Change-a-Rule dedupe? | **CLOSED — Ratified**: one canonical change-a-rule tile; the duplicate retires. |
| **FL-P1-14** | Reference screenshot for tile-grid grammar? | **CLOSED — Fixture is the attached screenshot plus the attached v7 brief**; every FIXTURE PENDING clears on their arrival in the workspace. **GRADE DISTINCTION (Q1(c) ruling · 2026-08-14):** two fixtures arrived as files and are `file-cleared` (`Akki_Prototype_v7_Design_Brief.md` sha256 `063f2b47…9717b4`; `AISCA_GPU_Access_Guide.pdf` sha256 `0f6b6e0f…157f3`). Reference screenshot arrived as an owner-inline transcription (owner acknowledged the image file was lost in a prior compaction; asked to re-send as file; not yet arrived) and is `transcription-cleared` (`reference_screenshot_transcription.md` sha256 `d3ae9a6c…02fc949`). Re-open if the image file arrives and pixel-level review contradicts the transcription. Binding acceptance criteria extracted at `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13); `test_four_questions_topline_present` added to every console item's new-invariants list per Build Order 01 §3. |
| **FL-P1-14a** | Fixture-arrival log — grade + hashes recorded. | **CLOSED — logged 2026-08-14**: v7 brief `file-cleared`; AISCA GPU Guide `file-cleared` (with SOP-conflict-escalation flag — see FL-P2-03 / FL-P2-04); reference screenshot `transcription-cleared` per Q1(c). PINS.md carries the same table with hashes; `fixtures/binding_acceptance_criteria.md` is the extracted-content deliverable. |
| **FL-P1-15** | Retire "Trust Center" label? | **CLOSED — OVERTURNED**: "Trust Center" is KEPT as the rendered group label, mapped to the Compliance Console identity — the reference screenshot fixes this label; mapping recorded here: label `Trust Center` → identity Canon 5 §22 Compliance Console. |
| **FL-P1-16** | Retire "*Shield" naming? | **CLOSED — OVERTURNED**: the shield names are KEPT as rendered tile labels mapped to their canon identities per the brief's §4 table. Mappings recorded here: label `Data Shield` → identity Canon 5 §22-§23 Compliance Console (Prove-one-run · Retention & Rights); label `Reasoning Shield` → identity Canon 5 §22 Compliance Home + Canon 5 §24-§25 Rulebook; label `Access Shield` → identity Canon 5 §29-§31 Administration Console (Roles & Rights · Counter-Sign Duties). |
| **FL-P1-17** | "WorkStudio" rename? | **CLOSED — Ratified**: "WorkStudio" renames to "Work." |
| **FL-P1-18** | ThinkLab/Monitor placement? | **CLOSED — Ratified**: ThinkLab and Monitor reparent under Lead. |
| **FL-P1-19** | "3rd Party Apps" placement + label? | **CLOSED — Ratified**: capability is the Integration Console plus catalogue; the on-screen tab may remain "3rd Party Apps" as org language, mapping recorded here: label `3rd Party Apps` → identity Canon 5 §26-§28 Integration Console + application catalogue. |

---

### D. Ruling-1 leftover — CLOSED

| id | question | Build Order 01 ruling |
|---|---|---|
| **FL-R1-01** | Purpose-gate strip — Canon 3 §24 ceremony or Watch verdict? | **CLOSED — Canon 3 §24 rule-change ceremony**: it is a rule change and the ceremony's visibility is the point; the Watch's role is witness; the two drill attestations attach to the proposal as its EVIDENCE, not its mechanism. |

---

### E. Citation-drift disclosure — CLOSED (retained on the record)

| id | disclosure | Build Order 01 ruling |
|---|---|---|
| **FL-P1-20** | Chunk-1 §-anchor drift (72 rows) + remediation trail. | **CLOSED — Remains on the record as handled**; reopen only if a title-match is refuted. Full remediation history in this section retained: `tools/drift_map.py` + `drift_apply.py` + `drift_downstream.py`; edit log `tools/drift_edits.log`; xref `tools/drift_xref.json`. |

**Root cause and prevention** (from prior close): Chunk-1 extraction from `.docx` archives numbered content paragraphs consecutively BEYOND canon `[Heading]` boundaries; `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for all subsequent work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

**Actual `[Heading]` section spans** (measured 2026-08-14): Canon 3 §1..§33 · Canon 4 §1..§50 · Canon 5 §1..§43 · Canon 6 §1..§12 · Canon 7 §1..§50 · Canon 8 §1..§21 · Canon 9 §1..§8.

**Remediation stats:** 72 row-level corrections + 70 downstream citation corrections applied. Rows where title-match failed and closing-section snap was applied (11 rows): C3-051, C3-060, C8-034, C8-035, C8-036, C8-037, C8-046, C8-048, C8-050, C8-051, C8-054.

---

### F. Part-2 field-level entries — CLOSED

Opened during Part-2 drafting; all resolved by rulings above.

| id | note | Build Order 01 resolution |
|---|---|---|
| **FL-P2-01** | `WS-BUILD-OBJECT-STORAGE-PORT` placement PROPOSAL (from Ruling B). | CLOSED via FL-P1-03 ruling — own BUILD item, port under boundary-governor ownership. |
| **FL-P2-02** | `WS-BUILD-STUDIO` scope reclassification note (L → XL if storage-plane composition). | CLOSED via FL-OQ-05 ruling — deferred; stays L baseline in dormant-state render; scope resolution deferred to later cycle. |
| **FL-P2-03** | AISCA SOP ↔ Build Order 01 §6 SKU mismatch — SOP documents only `1× H200 · 20 vCPU · 240 GB RAM · 3 TB ephemeral · 75 GB root HSS`; Order §6 mandates `4× H200 NVLink · 84 vCPU · 948 GB RAM · 12 TB ephemeral · ~30 TB HSS`. | **ESCALATED-AND-STOPPED** per Q2(a) · 2026-08-14. SOP as-written cannot produce Order §6 environment. Owner ruling needed on the provisioning path for the Order §6 SKU (different Catalog entry not in this PDF? different channel? or Order §6 environment unavailable in this Catalog?). Frozen artifacts: `phase0/acceptance.sh` + `commissioning_checklist.md` (probes 4×H200 NVLink · ~30 TB HSS · restart survives · password-dead — DO NOT modify to accommodate the 1×H200 SKU until owner rules). See `fixtures/aisca_sop_extraction.md` §3 (Conflict A) + §4 (Q-SOP-1, Q-SOP-2). |
| **FL-P2-04** | AISCA SOP ↔ Build Order 01 §6 credential-handoff procedural gap — SOP step SOP-8 hands over Public IP + Username + **Password**; Order §6 mandates key-only SSH, password auth disabled + probed dead, bootstrap credentials retired. | **ESCALATED** per Q2(a) · 2026-08-14. Reconciliable via Order §6's own credential-hardening clause (owner may confirm the hardening steps are inserted between SOP-8 and any data movement), but SOP text itself does not cover the hardening step. Owner ruling needed on whether the compute-seam's `acceptance.sh` extends to cover the hardening (currently it does not) or whether owner-side hands run the hardening before the seam gains admission. See `fixtures/aisca_sop_extraction.md` §3 (Conflict B) + §4 (Q-SOP-3). |
| **FL-P2-05** | Reference-screenshot grade — transcription-cleared vs file-cleared distinction. | **CLOSED** by Q1(c) ruling · 2026-08-14. Owner in-channel transcription is AUTHORITATIVE-UNTIL-FILE-ARRIVES; interface DoDs cite `fixtures/binding_acceptance_criteria.md` at transcription grade. Re-open only if image file arrives and pixels contradict transcription. See FL-P1-14 for the label→identity mappings and BAC-1..BAC-13 for the extracted binding criteria. |

---

### Ledger closure summary

- **A** — 8/8 CLOSED (owner Open Questions).
- **B** — 7/7 CLOSED (Part-1 field-level).
- **C** — 12/12 CLOSED (Instruction-02 rendering decisions), of which FL-P1-15 and FL-P1-16 OVERTURNED with explicit label→identity mappings; FL-P1-14 substantive closure carries a `transcription-cleared` vs `file-cleared` grade distinction (Q1(c) ruling · 2026-08-14).
- **D** — 1/1 CLOSED (Ruling-1 leftover).
- **E** — 1/1 CLOSED (citation-drift disclosure retained on record).
- **F** — 5/5 rows logged (Part-2 field-level): FL-P2-01, FL-P2-02, FL-P2-05 CLOSED by rulings; **FL-P2-03 ESCALATED-AND-STOPPED** (AISCA SOP SKU mismatch) and **FL-P2-04 ESCALATED** (SOP credential-handoff procedural gap) per Q2(a) · 2026-08-14, awaiting owner rulings before Phase 0 executes on the affected artifacts. Fixture-cycle work continues on the unblocked streams (v7 brief + transcription-driven interface DoDs + BUILD_STRATEGY.md corrections + commit on master).

**Owner's original 27 CLOSED rows** (Build Order 01 §2): A/1..8 + B/1..7 + C/1..12 = 27 · CLOSED. Rows D/E/F/P2 are retained history + newly-opened rows during the fixture cycle.

**Total: 27+2 = 29 rows CLOSED. FL-P1-14 flagged with conditional-substantive-closure pending attachment delivery. Ledger frozen at Build Order 01; changes require Canon 3 §24 rule-change ceremony.**


---

## Appendix A · Row-to-item index — 591 rows → 102 items

Inlined verbatim from the working paper `notes/row_to_item_index.md`. Build orders can be issued against BUILD_STRATEGY.md by item reference; this appendix provides the row-level traceability every item references.

**Universe:** 591 canon requirement rows (Canon 1..9 + MOAC sub-rows C4-037a..f + defect taxonomy C7-D01..D26).
**Item ID scheme:** `WS-<CLASS>-<TOPIC>-<seq>` or thematic bundles `WS-<TOPIC>`. Bundles group rows that are genuinely one buildable unit per Ruling 1's four-test framing.
**Every non-REUSE row appears in exactly ONE work item.** REUSE rows either have no item (marked `—`) or a WIRING item where new work depends on them.
**Named gaps** section at the end lists rows that would otherwise be silent.

### Bundling rationale

- Bundling is by CANONICAL SEAM (Canon 9 handoff / Canon 8 authority / Canon 4 engine / Canon 3 rulebook stage / Canon 5 console panel) — not by convenience.
- The 6 MOAC criteria (C4-037a..f) bundle as ONE scorecard item because they ARE one scorecard (Canon 4 §26 anchor).
- The 3-actor Watch cluster (C8-009..C8-013 + related) bundles as ONE item because the seam between Macho / Mkono / Witness is explicitly the Canon 8 §6 seam.
- Interface console rows (C5-013..C5-042) bundle by console because each console is its own capability grouping (Canon 5 §10).

### Mapping table

Legend for class: `REUSE` / `MODIFY` / `PARTIAL` / `RE-POINT` / `HARVEST` / `BUILD` / `RETIRE` / `REBUILD` / `N/A-DOCTRINE` / `CONTRADICTION`. The `Item` column shows the work-item ID this row lands in; `—` = no item (REUSE with no wiring, or pure doctrine).

#### Canon 1 · The Custody Platform (75 rows)

| Row | Class | Item | Domain | Note |
|---|---|---|---|---|
| C1-001..C1-013 | REUSE / N/A-DOCTRINE | — | 5.1/doctrine | Doctrinal frame. Fail-closed custody (C1-014/015) covered in WIRING WS-WIRE-CUSTODY-DECL (declaration-check integration with existing fail-closed chain). |
| C1-014 · C1-015 | REUSE | WS-WIRE-CUSTODY-DECL | 5.1 | REUSE with new wiring — declaration failure must join fail-closed set. |
| C1-016..C1-019 | N/A-DOCTRINE | — | 5.1 | Unrepresentable-not-policed doctrine. |
| C1-020..C1-027 | REUSE | — | 5.2 | Ledger discipline; single-owner-per-value; twelve doctrines seat rows. |
| C1-028 | N/A-DOCTRINE | — | 5.6 | Runtime-human doctrine. |
| C1-029..C1-035 | REUSE | — | 5.1/5.2 | Inheritance, provenance, canon-before-ruling, single experiment level. |
| C1-036 · C1-037 | N/A-DOCTRINE | — | 5.6 | Precedence, peerage. |
| C1-038..C1-041 | REUSE / PARTIAL | WS-WIRE-CUSTODY-DECL | 5.1 | C1-041 in-perimeter model routing PARTIAL — flagged at 5.1 note. |
| C1-042..C1-054 | REUSE | — | 5.3 | Six-engines seat rows. |
| C1-053 · C1-054 | REUSE | WS-WIRE-REGISTRY | 5.3/5.5 | Function & Promise Registry wiring depends on WS-HARVEST-REGISTRY-CONTEXT to close new registry rows. |
| C1-055..C1-061 | REUSE | — | 5.3 | Estate + two-layer + verdict as lookup. |
| C1-062..C1-067 | PARTIAL | WS-WIRE-LOOP-ORCH | 5.2 | Operating-loop end-to-end orchestration. Depends on WS-HARVEST-GAP-FILER. |
| C1-068..C1-070 | REUSE | — | 5.5 | Six services doctrine. |
| C1-069 (S6) | BUILD | WS-BUILD-S6-WATCH-SERVICE | 5.5 | Watch service sentence — couples with Canon-8 cluster. Part-2 (BUILD) chunk. |
| C1-071 · C1-072 | REUSE | — | 5.5 | Boundary discipline for every application. |
| C1-073..C1-075 | N/A-DOCTRINE | — | 5.5 | Canonical terms + document map. |

#### Canon 2 · Conditioned Ideation Faculty (66 rows) — largest un-mapped cluster before this chunk

CIF is heavy on discipline. Every implementable CIF row lands here.

| Row | Class | Item | Note |
|---|---|---|---|
| C2-001..C2-005 | N/A-DOCTRINE | — | Promise + adoption doctrine. |
| C2-006..C2-008 | N/A-DOCTRINE | — | Single-experiment principle. |
| C2-009 | BUILD | WS-CIF-COACH-SEAT | Coach seat + origination port constitutional load-bearing (Canon 2 §12). |
| C2-010 | REUSE | WS-WIRE-SOLVA-CIF | Solva-pattern validation for CIF's own claims. |
| C2-011 | HARVEST | WS-HARVEST-CRITIC-SEAM | Critic Seam extends per CIF pre-ship checklist. |
| C2-012 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE | Independence rule machine-checked (also C3-028). |
| C2-013 | REUSE | — | Bind to run telemetry (existing fields). |
| C2-014 | BUILD | WS-BUILD-WATCH-TO-CIF | Watch findings → CIF detection input (Canon 9 §6 handoff). |
| C2-015 | N/A-DOCTRINE | — | Engine walls seat. |
| C2-016..C2-018 | BUILD-with-HARVEST | WS-HARVEST-CRITIC-SEAM | Manifest schema + submission gate (critic_pass's `manifest_gate.py`). |
| C2-019..C2-023 | BUILD | WS-CIF-ARCHIVE | Living archive four-state discipline + silence-is-data-state + rejection-names-condition + rent + zero-inherited-credibility + paper-first. |
| C2-024 | N/A-DOCTRINE | — | Paper-precedes-compute doctrine. |
| C2-025..C2-028 | HARVEST | WS-HARVEST-CRITIC-SEAM | Naivety pass + pre-ship checklist extend Critic Seam rubric. |
| C2-029 · C2-030 | BUILD | WS-CIF-DETECTION | Frame signature detection (cascade / absorption / misfit). |
| C2-031 | BUILD | WS-CIF-COACH-SEAT | Origination port — only the coach adopts frames. |
| C2-032 · C2-033 | BUILD | WS-CIF-METABOLISATION | Four-step frame-adoption sweep + build check. |
| C2-034..C2-036 | BUILD | WS-CIF-MONITORING | Condition watchers + cascade detection + adversarial elicitation. |
| C2-037..C2-039 | N/A-DOCTRINE | — | Permanent bound — self-certification closed. |
| C2-040..C2-044 | BUILD | WS-CIF-PARAMETERS | Operative parameters (FACT-class) — manifest coverage, archive completeness, escalation latency, metabolisation execution, rent collection. |
| C2-045..C2-051 | BUILD | WS-CIF-PARAMETERS | Quality parameters (measured) — promise metric, manifest hit-rate, provisional honesty, metabolisation closure, overhead ceiling, false-escalation rate, defaults. |
| C2-052..C2-059 | REUSE | WS-HARVEST-CRITIC-SEAM | Enforcement uses standing vehicles + critic-seam amendment. |
| C2-060..C2-066 | N/A-DOCTRINE | — | Governance + what CIF does not do. |

**Named-gap resolution**: Every one of the 47 previously-unassigned Canon-2 rows is now mapped.

#### Canon 3 · Governance Engines (61 rows)

| Row | Class | Item |
|---|---|---|
| C3-001..C3-003 | REUSE | — |
| C3-004..C3-007 | REUSE | — |
| **C3-008 · C3-009 · C3-010** | **BUILD (implicit-answered by Ruling 1)** | **WS-BUILD-DECL** — actor-declaration seat + admit-time check + supersession |
| C3-011..C3-017 | REUSE | — |
| C3-018 | BUILD | WS-BUILD-INPUT-SEAT — canonical input-seat surface distinct from deidentifier |
| C3-019 | REUSE | — |
| C3-020 | BUILD | WS-BUILD-INPUT-SEAT-DUAL — dual identity (governance/Watch), couples with Watch cluster |
| C3-021 | REUSE | — |
| C3-022..C3-025 | REUSE | — |
| C3-026 | PARTIAL | WS-WIRE-INTENT-AUDIT-WATCH — divergence-field consumer, couples with Watch |
| C3-027 | REUSE | — |
| C3-028 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE — machine-checked reviewer-selector gate |
| C3-029 | REUSE | — |
| C3-030..C3-032 | REUSE / PARTIAL | WS-BUILD-RULEBOOK-SURFACE — Compliance Rulebook read-back is 5.7 BUILD; rows anchored here |
| C3-033 | **PARTIAL (updated Chunk-3 A.2)** | WS-BUILD-CEREMONY-REVERIFY — 5th step "re-verified" missing |
| C3-034..C3-035 | REUSE / PARTIAL | WS-BUILD-RULEBOOK-SURFACE |
| C3-036..C3-038 | REUSE | — |
| C3-039..C3-042 | PARTIAL | WS-BUILD-VERIFICATION-RUNNER — Compliance-Console-triggered live surface |
| C3-043..C3-045 | REUSE | — |
| C3-046..C3-048 | PARTIAL | WS-BUILD-PROVE-ONE-RUN — Canon 3 §33 export as single action |
| C3-049..C3-051 | N/A-DOCTRINE | — |
| C3-052 · C3-053 | REUSE | — |
| C3-054..C3-058 | N/A-DOCTRINE | — |
| C3-059 | PARTIAL | WS-BUILD-DECL — declaration build gate part of declaration item |
| C3-060 · C3-061 | REUSE | — |

#### Canon 4 · Operating Engines (68 rows + 6 MOAC sub-rows)

| Row | Class | Item |
|---|---|---|
| C4-001 · C4-002 | REUSE-doctrine | — |
| C4-003..C4-013 | REUSE | — |
| C4-014..C4-020 | REUSE | — |
| C4-021..C4-025 | REUSE | — |
| C4-026..C4-028 | REUSE | — |
| C4-029..C4-030 | REUSE | — |
| C4-031 | HARVEST | WS-HARVEST-CRITIC-SEAM |
| C4-032 · C4-033 | REUSE | — |
| C4-034..C4-036 | PARTIAL | WS-BUILD-ADAPTER-REGISTRY — adapter surface + no-model-for-class rendering |
| **C4-037a..C4-037f** | **BUILD** | **WS-BUILD-MOAC-SCORECARD** (six criteria one scorecard) |
| C4-038..C4-040 | BUILD | WS-BUILD-MOAC-SCORECARD (uncurated sample + lineage + version history — same scorecard) |
| C4-041 · C4-042 | REUSE | — |
| C4-043..C4-046 | REUSE | — |
| C4-047 | PARTIAL | WS-HARVEST-BATCH-QUARANTINE + WS-BUILD-BATCH-BOARD-SURFACE (see 5.7) |
| C4-048 | REUSE | — |
| C4-049..C4-051 | PARTIAL | WS-WIRE-LOOP-ORCH |
| C4-052..C4-055 | REUSE | — |
| C4-056..C4-060 | PARTIAL | WS-BUILD-DELIVERABLE-ATTESTATIONS — contents / privacy / quality attestation surface |
| C4-061..C4-064 | N/A-DOCTRINE | — |
| C4-065..C4-066 | REUSE | — |
| C4-067..C4-068 | BUILD | WS-BUILD-MOAC-SCORECARD (drift + latest reading is the one in circulation) |

#### Canon 5 · Interface Architecture (70 rows) — every Part-2 BUILD row lands here

| Row | Class | Item |
|---|---|---|
| C5-001 | REUSE-doctrine | — |
| C5-002..C5-004 | BUILD | WS-BUILD-CLASS-CHIP-LIBRARY — class chip inseparable from claim + grounding marker |
| C5-005..C5-007 | BUILD | WS-BUILD-REFUSAL-CARD-COPY — verbatim Canon 5 §9.2 refusal card as component |
| C5-008 | BUILD | WS-BUILD-AGENT-ASSUMED-CHIP |
| C5-009 | PARTIAL | WS-BUILD-DORMANT-STATE-RENDER — "what would activate" statement per screen |
| C5-010..C5-012 | BUILD | WS-BUILD-CONSOLES — five consoles as named surfaces per Canon 5 §10 (FL-OQ-04 CLOSED by Build Order 01 §1: five, with Watch as the fifth rendered as fourth Admin-surface tile group per Instruction 02) |
| C5-013 | PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD |
| C5-014 | BUILD | WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE (couples with WS-BUILD-MOAC-SCORECARD) |
| C5-015..C5-017 | REUSE / PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-SHAPING-WIZARD (surface uplift for freeze + sampling) |
| C5-018 | BUILD | WS-BUILD-BATCH-BOARD-SURFACE (couples with WS-HARVEST-BATCH-QUARANTINE) |
| C5-019 | REUSE | — |
| C5-020 | BUILD | WS-BUILD-QUALITY-OBSERVATION (Critic-Seam calibration stale surface; couples with WS-HARVEST-CRITIC-SEAM) |
| C5-021 | REUSE | — |
| C5-022..C5-026 | BUILD | WS-BUILD-CONSOLE-COMPLIANCE (Home + Prove-one-run + Retention & Rights + Rulebook + rule-on-paper flag; couples with WS-BUILD-PROVE-ONE-RUN + WS-BUILD-VERIFICATION-RUNNER + WS-BUILD-RULEBOOK-SURFACE) |
| C5-027..C5-030 | BUILD | WS-BUILD-CONSOLE-INTEGRATION (Register / First-call / Administer / Dual-actor scoping) |
| C5-031..C5-036 | BUILD | WS-BUILD-CONSOLE-ADMINISTRATION (Home + Change-a-Rule + What-I've-Changed + Roles & Rights + Counter-Sign Duties + Verification-Runner surface) |
| C5-037..C5-042 | BUILD | WS-BUILD-CONSOLE-WATCH (four panels; couples with Canon-8 cluster) |
| C5-043 · C5-044 | REUSE / PARTIAL | WS-BUILD-REFERENCE-APP (Ask surface as designed application) |
| C5-045..C5-048 | BUILD | WS-BUILD-THREE-LENSES (Answer / Reasoning / Raw trail over one object) |
| C5-049..C5-051 | BUILD | WS-BUILD-ANSWER-CARD (evidence + honesty + actions) |
| C5-052 | BUILD | WS-BUILD-FIVE-PILLARS (adds Lead + Learn; four-vs-five console reconciliation in fidelity ledger OQ#4) |
| C5-053 | BUILD | WS-BUILD-PULSE-NEWS |
| C5-054 · C5-056 | REUSE | — |
| C5-055 · C5-060 | BUILD | WS-BUILD-STUDIO (application-composer; OQ #5 in fidelity ledger) |
| C5-057 | BUILD | WS-BUILD-LEARN-PILLAR |
| C5-058 · C5-059 | BUILD | WS-BUILD-CONTROL-BAND (five items: Connect / Estate Map / Rulebook / Access / Watch) |
| C5-061..C5-062 · C5-066..C5-070 | REUSE-doctrine | — |
| C5-063 · C5-064 · C5-065 | BUILD | WS-BUILD-COMPONENT-LIBRARY (insufficient-measurement render + absence-as-state + shared visual system) |

#### Canon 6 · User Journeys (62 rows)

| Row | Class | Item |
|---|---|---|
| C6-001..C6-006 | REUSE-doctrine | — |
| C6-007..C6-012 | PARTIAL | WS-BUILD-SETUP-CONSOLE (setup surface + signed setup record) |
| C6-013..C6-022 | PARTIAL | WS-BUILD-DAY-ZERO (estate map + commissioning certificate + Verification Runner packs + Watch drills — couples with Canon-8) |
| C6-023..C6-028 | REUSE / PARTIAL | WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD (Opportunity Briefs advisory rendering) |
| C6-029..C6-033 | REUSE | — |
| C6-034..C6-037 | REUSE | — |
| C6-038..C6-043 | PARTIAL | WS-BUILD-WEBHOOK + WS-BUILD-REFERENCE-APP |
| C6-044 · C6-045 | REUSE / PARTIAL | WS-BUILD-CONSOLE-COMPLIANCE |
| C6-046..C6-054 | BUILD | WS-BUILD-CONSOLE-WATCH + WS-BUILD-WATCH-DAY (Watch officer's journey — couples with Canon-8 cluster) |
| C6-055 · C6-056 | REUSE | — |
| C6-057..C6-060 | REUSE-doctrine | — |
| C6-061 · C6-062 | N/A-DOCTRINE | — |

#### Canon 7 · Integration and Quality (35 + 26 = 61 rows)

Main rows:

| Row | Class | Item |
|---|---|---|
| C7-001..C7-005 | REUSE | — |
| C7-006 | PARTIAL | WS-BUILD-THREE-LENSES (envelope class-chip render) |
| C7-007 | REUSE | — |
| C7-008 | REUSE | — |
| C7-009 | BUILD | WS-BUILD-WEBHOOK |
| C7-010..C7-012 | REUSE | — |
| C7-013..C7-017 | REUSE | — |
| C7-018 · C7-019 | PARTIAL | WS-BUILD-PLANE-PRECOMPUTE + WS-WIRE-WATCH-PLANE-ACTIVITY |
| C7-020..C7-023 | REUSE | — |
| C7-024..C7-028 | HARVEST | WS-HARVEST-CRITIC-SEAM (Critic Seam is the anchor) |
| C7-029..C7-031 | REUSE / PARTIAL | WS-BUILD-STANDING-QUERY-SURFACE |
| C7-032..C7-035 | REUSE-doctrine | — |

Defect taxonomy:

| Row | Class | Item |
|---|---|---|
| C7-D01 · C7-D04..D10 · C7-D13 · C7-D16 · C7-D24 · C7-D25 | REUSE | — |
| C7-D02 · C7-D26 | HARVEST | WS-HARVEST-CRITIC-SEAM (manifest-gate + no-reset-absent) |
| C7-D03 | BUILD | WS-BUILD-CLASS-CHIP-LIBRARY |
| C7-D11 | PARTIAL | WS-BUILD-INDEPENDENCE-GATE |
| C7-D12 | PARTIAL | WS-BUILD-RULEBOOK-SURFACE |
| C7-D14 · C7-D15 | BUILD | WS-BUILD-MOAC-SCORECARD |
| C7-D17 | BUILD | WS-BUILD-CONSOLES (interior-render forbiddance is a design constraint on consoles) |
| C7-D18 | BUILD | WS-BUILD-CONSOLE-WATCH (interior-render forbiddance on Watch console) |
| C7-D19 · C7-D20 | N/A-DOCTRINE | — (unrepresentable-by-design at any future biometric register) |
| C7-D21 | PARTIAL | WS-BUILD-HANDOFF-REGISTRY (Canon 9) |
| C7-D22 · C7-D23 | BUILD | WS-BUILD-TASK-IDENTITY-REGISTER + WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL (Canon 9) |

#### Canon 8 · The Watch (72 rows) — ALL BUILD or doctrine

Bundled into cohesive Watch items per Canon 8 §6 seam + §7-§11 authorities + §13-§18 register + §19-§20 drills + §22-§24 officer's day + peer-authority.

| Row | Class | Item |
|---|---|---|
| C8-001..C8-003 | REUSE-doctrine / N/A-DOCTRINE | — |
| C8-004..C8-008 | BUILD | WS-BUILD-WATCH-FOUNDATION (machine-speed + attestation + seam sensing→verdict→response→action) |
| C8-009..C8-013 | BUILD | WS-BUILD-WATCH-ACTORS (Macho sensor + Mkono responder + Witness) |
| C8-014..C8-018 | BUILD | WS-BUILD-WATCH-MARK-REGISTER |
| C8-019..C8-026 | BUILD | WS-BUILD-WATCH-CONTAINMENT (containment + mirage + expiries + reconciliation) |
| C8-027..C8-029 | BUILD | WS-BUILD-WATCH-DECISIONS-PANEL |
| C8-030..C8-033 | BUILD | WS-BUILD-WATCH-DAY (couples with WS-BUILD-CONSOLE-WATCH) |
| C8-034..C8-039 | BUILD | WS-BUILD-WATCH-DRILLS (standing drills + fitness in receipts) |
| C8-040..C8-044 | BUILD | WS-BUILD-WATCH-AUTHORITY-PEERAGE (disagreement + task identity + new-entry-only correction; couples with WS-BUILD-TASK-IDENTITY-REGISTER) |
| C8-045..C8-054 | N/A-DOCTRINE | — (constitutional negatives as design constraints on the other Watch items) |
| C8-055..C8-059 | BUILD | WS-BUILD-WATCH-RECORD-CLASSES (verdict/action/marks/behavioural-profiles/attestation writers — couples with WS-BUILD-RECORD-MATRIX) |
| C8-060..C8-065 | N/A-DOCTRINE | — |
| C8-066..C8-068 | BUILD | WS-BUILD-WATCH-TO-CIF (findings→CIF; only ratified frames cross back) |
| C8-069 · C8-070 | REUSE-doctrine | — (boundary with Doc 9 — sits under Canon 9 handoffs) |
| C8-071 · C8-072 | N/A-DOCTRINE | — |

#### Canon 9 · Mkondo Charter (50 rows) — ALL BUILD or doctrine

| Row | Class | Item |
|---|---|---|
| C9-001..C9-003 | BUILD | WS-BUILD-MKONDO-CHARTER (structure-only orchestration service) |
| C9-004 · C9-005 | REUSE-doctrine | — |
| C9-006..C9-018 | BUILD | WS-BUILD-RECORD-MATRIX (13 writer→readers rows) |
| C9-019..C9-022 | BUILD | WS-BUILD-READING-DISCIPLINE (couples with WS-BUILD-CONSOLE-WATCH + WS-BUILD-CONSOLE-COMPLIANCE) |
| C9-023..C9-035 | BUILD | WS-BUILD-TASK-IDENTITY-REGISTER |
| C9-036 | PARTIAL | WS-WIRE-ADMISSION-HANDOFF (already implemented at wizard/admission_handoff.py; wire to registered-contract shape) |
| C9-037..C9-042 | BUILD | WS-BUILD-HANDOFF-REGISTRY (six handoff contracts) |
| C9-043..C9-047 | BUILD | WS-BUILD-MKONDO-CHARTER (change + precedence + silence-as-finding) |
| C9-048..C9-050 | REUSE-doctrine | — |

### Summary — Every non-REUSE row is assigned

- **Total canon requirement rows**: 591
- **N/A-DOCTRINE / REUSE-doctrine rows** (no item): ~200
- **REUSE rows** with no wiring dependency (no item): ~155
- **REUSE rows** with wiring dependency (WIRING item): ~10
- **Non-REUSE rows mapped to a work item**: **~228** (Part-1 classes: MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE ≈ 80 rows; Part-2 BUILD ≈ 148 rows; contradiction ≈ 1 row)

### Work-item universe (deduped by ID)

Every ID that appeared above, once. Class abbreviations: **P** = Part 1 (this chunk), **B** = Part 2 (BUILD chunk, next).

#### Part 1 (MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE / WIRING / CONTRADICTION)

Work items assembled from the mapping above.

| Item ID | Class | Rows covered | Item title |
|---|---|---|---|
| **WS-WIRE-CUSTODY-DECL** | WIRING | C1-014, C1-015, C1-038–C1-041 | Fail-closed custody joins declaration verdict |
| **WS-WIRE-REGISTRY** | WIRING | C1-053, C1-054 | Function & Promise Registry ↔ registry_context integration |
| **WS-WIRE-LOOP-ORCH** | PARTIAL | C1-062–C1-067, C4-049–C4-051 | Operating-loop end-to-end orchestration |
| **WS-WIRE-SOLVA-CIF** | WIRING | C2-010 | Solva-pattern validation applied to CIF's own claims |
| **WS-WIRE-INTENT-AUDIT-WATCH** | PARTIAL | C3-026 | Intent-audit divergence-field consumer wiring to Watch |
| **WS-WIRE-WATCH-PLANE-ACTIVITY** | WIRING | C7-019 | Watch reads plane activity (not content) |
| **WS-WIRE-ADMISSION-HANDOFF** | PARTIAL | C9-036 | Existing admission→extraction handoff registered as Canon-9 contract |
| **WS-WIRE-CRITIC-INTO-ANSWERING** | WIRING (Ruling 2) | (couples HARVEST-CRITIC-SEAM into request path) | Critic Seam in-flight on the answering path (§7 of Canon 7, §21-§23 of Canon 4) — separate from the harvest |
| **WS-WIRE-PARITY-EXTENSION** | WIRING (Ruling 2) | (couples every new contract) | Frozen-contract-snapshot parity discipline extended to every new contract this programme creates (Canon-9 handoffs, Watch verdicts, task-identity register) |
| **WS-WIRE-REFUSAL-FAMILY** | WIRING (Ruling 2) | (C5-005..C5-007 UI × C1-020 refusal taxonomy) | Refusal-family taxonomy in `services/memory/refusal.py` + `memory_refusal_reasons.v0.json` wired to Canon 5 §9.2 refusal card surface |
| **WS-WIRE-LEDGER-MATRIX** | WIRING (Ruling 2) | (couples C1-024, C1-027, C9-006..C9-018) | Northena ledger's sole-writer position (services/northena/ledger.py:63 `record()`) promoted to Canon 9 §6-§18 matrix-governed writer |
| **WS-HARVEST-CRITIC-SEAM** | HARVEST | C2-011, C2-016–C2-018, C2-025–C2-028, C2-052–C2-059, C4-031, C7-024–C7-028, C7-D02, C7-D26 | Critic Seam + manifest + amendments + independence hard-check |
| **WS-HARVEST-BATCH-QUARANTINE** | HARVEST | C4-047 (partial) | `services/service_1/batch_quarantine.py` (Akki-OS-V1) |
| **WS-HARVEST-GAP-FILER** | HARVEST | (couples C1-062–C1-067) | `services/targeta/gap_candidate_filer.py` (Akki-OS-V1) |
| **WS-HARVEST-REGISTRY-CONTEXT** | HARVEST | (couples C1-053, C1-054) | `services/registry_context/` (Akki-OS-V1) |
| **WS-HARVEST-PARTITIONS** | HARVEST | (couples C7-013 wiring) | `services/partitions/session_working_set.py` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-SEQUENCING-HARNESS** | HARVEST | (couples with WS-WIRE-REGISTRY) | `services/sequencing_harness/` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-FAR-ENDPOINT** | HARVEST | (couples with WS-WIRE-REGISTRY) | `services/far_endpoint/` + `services/generated_gates/` (Akki-OS-V1) — pending OQ#9 |
| **WS-HARVEST-STREAMING** | HARVEST | (couples with RE-POINT cluster) | `services/synisense/shield/streaming.py` (Executive-Core) |
| **WS-HARVEST-TWO-PASS-AMENDMENT** | HARVEST | (couples with Solva-pattern) | `services/two_pass.py` verbatim refusal templates as Solva-pattern amendment (Executive-Core) |
| **WS-REPOINT-ANSWERING-SURFACES** | RE-POINT | (Executive-Core: chat, documents, analyze_workspace, ideas_engine, deck_*, inbox_routing) | RE-POINT answering surfaces onto spine via `SyniSenseContract` adapter swap |
| **WS-REPOINT-SOLVA-V2** | RE-POINT | (Executive-Core `services/solva_v2/`) | RE-POINT narration surface; delegate assertion boundary to spine's `solva_depth` |
| **WS-REPOINT-SOLVA-VOICE-AUDIT** | RE-POINT | (Executive-Core `services/solva_voice_audit/`) | RE-POINT coach-voice surface |
| **WS-REBUILD-WORK-STUDIO-STORAGE** | REBUILD | (Executive-Core `work_studio` storage layer) | Migrate 200+ real user exports to Doc-7 §19-§23 memory plane |
| **WS-REPOINT-WORK-STUDIO-LLM** | RE-POINT | (Executive-Core `work_studio` LLM boundary only) | Adapter swap for shield_invoke calls |
| **WS-CONTRADICTION-PURPOSE-GATE** | CONTRADICTION (conditional under Ruling 1) | (couples C7-011, C7-012) | Executive-Core `purpose_validator` gate RETAINED until WS-BUILD-DECL and WS-BUILD-WATCH-RECONCILER demonstrate firing |
| **WS-RETIRE-APP-TERRITORY** | RETIRE | (Executive-Core cohort/, stripe_webhook, owner_digest, news_aggregator, first_login_password_set, platform_kb, backfill_shield_v1) | Application-territory duplicates (Canon 1 §12/§13/§15) |
| **WS-RETIRE-XCUT-SECURITY** | RETIRE | (Executive-Core csrf, rate_limit, rbac, security_headers, session_timeout, sentry_setup, privacy_wall, clamav_service) | Cross-cutting security duplicates (Canon 5 §11 + Canon 1 §7.1 + Canon 3 §30) |
| **WS-RETIRE-FRONTEND-ARCHIVES** | RETIRE | (Executive-Core `_archived/`, `_archived_legacy/`, `_archived_coverage_loss/`, `website/`) | Codebase-marked archives + marketing website |
| **WS-RETIRE-PROTOTYPE-DIVERGENCE** | RETIRE | (prototype `hrstuff`, `datashield/reasoningshield/accessshield` labels, `compute`, `tasks`, `mentions/emails/projects`) | Prototype-only surfaces without Canon-5 anchor |
| **WS-RENAME-PROTOTYPE-TAXONOMY** | RETIRE (rename-only) | (prototype WorkStudio/ThinkLab/Monitor/Trust/Registry/Build/3rd Party labels) | Rename to Canon 5 §10 taxonomy — no code deletion |
| **WS-BUILD-INDEPENDENCE-GATE** | PARTIAL/BUILD | C2-012, C3-028, C7-D11 | Machine-checked reviewer-independence gate |
| **WS-BUILD-DELIVERABLE-ATTESTATIONS** | PARTIAL | C4-056–C4-060 | Contents / privacy / quality attestation surface uplift |
| **WS-BUILD-CEREMONY-REVERIFY** | PARTIAL (Chunk-3 A.2) | C3-033 | Rule-change ceremony's 5th "re-verified" step |
| **WS-BUILD-STANDING-QUERY-SURFACE** | PARTIAL | C7-029–C7-031 | Standing queries surface for compliance-owner review |

**Part-1 total work items: 47** (11 WIRING · 9 HARVEST (non-interface) · 4 RE-POINT · 1 REBUILD · 4 RETIRE + 1 RENAME · 1 CONTRADICTION · 4 MODIFY/PARTIAL · **13 INTERFACE HARVEST/MODIFY** (Ruling 3)). Ruling 2 promoted 4 WIRING items; Ruling 3 reclassified 13 interface items from Part-2 BUILD to Part-1 HARVEST/MODIFY.

#### Part 2 (BUILD) — enumerated here for row-mapping completeness; content deferred to next chunk

| Item ID | Rows covered | Domain |
|---|---|---|
| WS-BUILD-DECL | C3-008, C3-009, C3-010, C3-059 | 5.2 (declaration seat) |
| WS-BUILD-INPUT-SEAT | C3-018 | 5.1 |
| WS-BUILD-INPUT-SEAT-DUAL | C3-020 | 5.1 (couples with Watch) |
| WS-BUILD-MOAC-SCORECARD | C4-037a..f, C4-038, C4-039, C4-040, C4-067, C4-068, C7-D14, C7-D15 | 5.4 |
| WS-BUILD-ADAPTER-REGISTRY | C4-034, C4-035, C4-036 | 5.4 |
| WS-BUILD-CONSOLES | C5-010, C5-011, C5-012, C7-D17 | 5.7 |
| WS-BUILD-CLASS-CHIP-LIBRARY | C5-002, C5-003, C5-004, C7-D03 | 5.7 |
| WS-BUILD-REFUSAL-CARD-COPY | C5-005, C5-006, C5-007 | 5.7 |
| WS-BUILD-AGENT-ASSUMED-CHIP | C5-008 | 5.7 |
| WS-BUILD-DORMANT-STATE-RENDER | C5-009 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD | C5-013, C6-023..C6-028 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE | C5-014 | 5.7 |
| WS-BUILD-CONSOLE-EXTRACTION-SHAPING-WIZARD | C5-015, C5-016, C5-017 | 5.7 |
| WS-BUILD-BATCH-BOARD-SURFACE | C5-018 | 5.7 |
| WS-BUILD-QUALITY-OBSERVATION | C5-020 | 5.7 |
| WS-BUILD-CONSOLE-COMPLIANCE | C5-022..C5-026, C6-044, C6-045 | 5.7 |
| WS-BUILD-CONSOLE-INTEGRATION | C5-027..C5-030 | 5.7 |
| WS-BUILD-CONSOLE-ADMINISTRATION | C5-031..C5-036 | 5.7 |
| WS-BUILD-CONSOLE-WATCH | C5-037..C5-042, C6-046..C6-054, C7-D18 | 5.7 (couples with Canon 8) |
| WS-BUILD-REFERENCE-APP | C5-043, C5-044, C6-038..C6-043 | 5.7 |
| WS-BUILD-THREE-LENSES | C5-045..C5-048, C7-006 | 5.7 |
| WS-BUILD-ANSWER-CARD | C5-049, C5-050, C5-051 | 5.7 |
| WS-BUILD-FIVE-PILLARS | C5-052 | 5.7 |
| WS-BUILD-PULSE-NEWS | C5-053 | 5.7 |
| WS-BUILD-STUDIO | C5-055, C5-060 | 5.7 (OQ #5) |
| WS-BUILD-LEARN-PILLAR | C5-057 | 5.7 |
| WS-BUILD-CONTROL-BAND | C5-058, C5-059 | 5.7 |
| WS-BUILD-COMPONENT-LIBRARY | C5-063, C5-064, C5-065 | 5.7 |
| WS-BUILD-RULEBOOK-SURFACE | C3-030..C3-032, C3-034, C3-035, C7-D12 | 5.6/5.7 |
| WS-BUILD-VERIFICATION-RUNNER | C3-039..C3-042 | 5.6 |
| WS-BUILD-PROVE-ONE-RUN | C3-046, C3-047, C3-048 | 5.6 |
| WS-BUILD-SETUP-CONSOLE | C6-007..C6-012 | 5.6 |
| WS-BUILD-DAY-ZERO | C6-013..C6-022 | 5.6 |
| WS-BUILD-WEBHOOK | C7-009, C6-042 | 5.5 |
| WS-BUILD-PLANE-PRECOMPUTE | C7-018 | 5.5 |
| WS-BUILD-S6-WATCH-SERVICE | C1-069 (S6) | 5.5 (couples with Canon 8) |
| WS-BUILD-WATCH-FOUNDATION | C8-004..C8-008 | 5.8 |
| WS-BUILD-WATCH-ACTORS | C8-009..C8-013 | 5.8 |
| WS-BUILD-WATCH-MARK-REGISTER | C8-014..C8-018 | 5.8 |
| WS-BUILD-WATCH-CONTAINMENT | C8-019..C8-026 | 5.8 |
| WS-BUILD-WATCH-DECISIONS-PANEL | C8-027..C8-029 | 5.8 |
| WS-BUILD-WATCH-DAY | C8-030..C8-033 | 5.8 |
| WS-BUILD-WATCH-DRILLS | C8-034..C8-039 | 5.8 |
| WS-BUILD-WATCH-AUTHORITY-PEERAGE | C8-040..C8-044 | 5.8 |
| WS-BUILD-WATCH-RECORD-CLASSES | C8-055..C8-059 | 5.8 (couples with WS-BUILD-RECORD-MATRIX) |
| WS-BUILD-WATCH-TO-CIF | C2-014, C8-066..C8-068 | 5.8/5.5 |
| WS-BUILD-WATCH-RECONCILER | (couples with WS-BUILD-WATCH-ACTORS Macho) | 5.8 (named by Ruling 1) |
| WS-BUILD-MKONDO-CHARTER | C9-001..C9-003, C9-043..C9-047 | 5.9 |
| WS-BUILD-RECORD-MATRIX | C9-006..C9-018 | 5.9 |
| WS-BUILD-READING-DISCIPLINE | C9-019..C9-022 | 5.9 |
| WS-BUILD-TASK-IDENTITY-REGISTER | C9-023..C9-035, C7-D22 | 5.9 |
| WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL | C7-D23 | 5.9 |
| WS-BUILD-HANDOFF-REGISTRY | C9-037..C9-042, C7-D21 | 5.9 |
| WS-CIF-COACH-SEAT | C2-009, C2-031 | Canon 2 |
| WS-CIF-ARCHIVE | C2-019..C2-023 | Canon 2 |
| WS-CIF-DETECTION | C2-029, C2-030 | Canon 2 |
| WS-CIF-METABOLISATION | C2-032, C2-033 | Canon 2 |
| WS-CIF-MONITORING | C2-034..C2-036 | Canon 2 |
| WS-CIF-PARAMETERS | C2-040..C2-051 | Canon 2 |

**Part-2 total work items: 42** (Ruling 3 moved 13 items into Part 1).

**Grand total work items: 89** (47 Part-1 + 42 Part-2). After Ruling 2: 85 → 89 via four promoted WIRING items. After Ruling 3: grand total unchanged (redistribution 34/55 → 47/42).

#### Ruling 3 interface reclassification (Part 2 → Part 1)

The following items moved from Part 2 BUILD → Part 1 HARVEST or MODIFY (Extraction-Akki donor in every case):
- `WS-BUILD-CONSOLES` → `WS-HARVEST-SHELL-GRAMMAR` (HARVEST — donor: `AkkiShell.jsx`, `AkkiV4Shell.jsx`, `CanonOSShellPage.jsx`)
- `WS-BUILD-CLASS-CHIP-LIBRARY` → `WS-HARVEST-CLASS-CHIP-LIBRARY` (HARVEST — donor: `ClassBadge.js`, `ResponseClassPanel.jsx`)
- `WS-BUILD-DORMANT-STATE-RENDER` → `WS-HARVEST-DORMANT-STATE` (HARVEST — donor: `ProveDormantPage.jsx`, `TeamDormantPage.jsx`)
- `WS-BUILD-CONSOLE-EXTRACTION-*` (dashboard, shaping-wizard) → `WS-HARVEST-CONSOLE-EXTRACTION` (HARVEST — donor: `pages/registry/`, `pages/memory/`, `pages/use_data/`)
- `WS-BUILD-CONSOLE-COMPLIANCE` → `WS-HARVEST-CONSOLE-COMPLIANCE` (HARVEST — donor: `pages/prove/`, `pages/govern/` [Retention/Holds/RefusalHealth/Home/EstateRules], `pages/commission_view/`)
- `WS-BUILD-CONSOLE-INTEGRATION` → `WS-HARVEST-CONSOLE-INTEGRATION` (HARVEST — donor: `pages/connect/`, `UseDataDeveloperSurfacePage.jsx`)
- `WS-BUILD-CONSOLE-ADMINISTRATION` → `WS-HARVEST-CONSOLE-ADMINISTRATION` (HARVEST — donor: `pages/master_admin/`, `pages/team/`, `pages/govern/` [Pending/ChangeRule/Registries])
- `WS-BUILD-COMPONENT-LIBRARY` → `WS-HARVEST-COMPONENT-LIBRARY` (HARVEST — donor: 8 atom components)
- NEW: `WS-HARVEST-REFUSAL-CARD` (donor: `RefusalCard.js`; couples with `WS-WIRE-REFUSAL-FAMILY`; replaces the render-side of `WS-BUILD-REFUSAL-CARD-COPY` which stays Part 2 as copy-only)
- NEW: `WS-MODIFY-PLANE-OBSERVABILITY` (rehome from Extraction → Compliance)
- NEW: `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (`TraceReceiptPage.js` rehome)
- NEW: `WS-MODIFY-USE-DATA-PLACEMENT` (Model Catalogue vs Ask Reference App — rendering decision pending)
- NEW: `WS-MODIFY-VERDICT-DEMO` (canon-required or RETIRE — rendering decision pending)
- NEW: `WS-MODIFY-AUDIT-TRAIL-PLACEMENT` (`AuditTrailPage.js` rehome)

`WS-BUILD-CONSOLE-WATCH` REMAINS Part 2 BUILD (Instruction 02 exception; new placement constraint encoded in its DoD).

Auth pages (`AuthLoginPage.js`, `AuthRegisterPage.js`) fold into existing `WS-RETIRE-APP-TERRITORY`.

### Named gaps (rows with no work item that are not doctrine-only)

None. Every non-doctrine row is assigned to exactly one work item. The 47 previously-unassigned Canon-2 CIF rows are resolved (some to doctrine, most to new `WS-CIF-*` items).

The 8 remaining Open Questions (from Assessment §8, minus OQ#1 conditional-answered and OQ#2 implicit-answered) become fidelity-ledger entries inside BUILD_STRATEGY.md and do NOT gate item creation.

### Auditability

- Every canon row above cites its class and item.
- Every Part-1 item is drafted in `notes/strategy_items_part1.md`.
- Every Part-2 item is drafted in `notes/strategy_items_part2.md` (next chunk).
- Mechanical audit: `tools/citation_audit.py` verifies file + canon citations across all notes files + BUILD_STRATEGY.md.


---

## End of BUILD_STRATEGY.md

**Assembly complete. Working papers on disk in `notes/`. STATE/ live. Local commits are the record (Owner Clarification 1, 2026-08-14 — no push).**
