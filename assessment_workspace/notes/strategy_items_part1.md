# strategy_items_part1.md — BUILD_STRATEGY Part 1

**Chunk 4, Part 1.** Every non-REUSE row that is NOT a BUILD (Part 2 will hold the 55 BUILD items covering 148 rows).

**Scope of this file:** 34 items, classes MODIFY / PARTIAL / RE-POINT / HARVEST / RETIRE / RENAME / WIRING / REBUILD / CONTRADICTION. Every item carries all seven fields exactly.

**Prohibitions active:** no production code, no harvesting-in-code, no re-pointing, no scaffolding, no canon edits. Paper only.

**Governing rulings:** Ruling 1 (transition condition for purpose-gate strip) and Ruling 2 (five-point plan responses). See `STATE/DECISIONS.md`.

---

## Estimation discipline (Ruling 2 §1)

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

## Field template (verbatim from Ruling 1 scope requirement)

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

# A. WIRING items (11)

WIRING covers new work that connects REUSE / HARVEST items into a request-path or matrix seat. WIRING items DO NOT invent new engines; they place existing pieces in canon-required seams.

---

## WS-WIRE-CUSTODY-DECL

1. **WHAT.** Wire the declaration-check verdict (from `WS-BUILD-DECL`, Part 2) into the fail-closed custody chain at `services/northena/admit.py:107-148 compile_and_freeze` (rows C1-014, C1-015 fail-closed; C1-038..C1-041 model-routing PARTIAL). Record class touched: `Ledger.Row` (Canon 9 §6 row 1, writer = Northena ledger, reader = Compliance Console + Watch). Task identity: `custody.admit.declaration_join`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §4.1 (unrepresentable-not-policed); Canon 1 §6 (fail-closed custody); Canon 3 §6.1 (declarations captured before operations); Canon 6 §3 L010 (declarations from setup morning forward).
3. **DEFINITION OF DONE.** Every `compile_and_freeze` invocation refuses admission when the actor declaration is absent, expired, or scope-mismatched (Canon 3 §6.1). Refusal writes a `LedgerRow(stage="admit", decision="refused", reason_family="declaration_missing"|"declaration_expired"|"declaration_scope_mismatch")` — same append-only path (Canon 1 §4.3 N-INV-4). N-INV-8 (append-only) and N-INV-9 (refusals recorded) hold on the new refusal path. Verification pack: Canon 3 §31 "prove-one-run" export for a refused admission shows declaration verdict as the refusal cause.
4. **QUALITY EVIDENCE.** Invariant test class extending `tests/invariants/test_northena_ledger_row_v0.py` and `tests/invariants/test_admission_refusal_v0_contract_frozen.py`. Uncurated sample: at least one drill run with a fixture where the declaration is expired mid-run; the refusal reason must appear in the sample. Calibration obligation (Canon 3 §31): the refusal reason exports intact through the prove-one-run pack.
5. **DEPENDENCIES.** Gated by `WS-BUILD-DECL` (declaration seat + admit-time check + supersession) — Part 2 item. Uses declaration record class from `WS-BUILD-RECORD-MATRIX` (Part 2). Interacts with `WS-WIRE-LEDGER-MATRIX` (this Part 1) — the ledger becomes matrix-governed by that item.
6. **CREDIT COST CLASS.** M. Justification: 1 component (`services/northena/admit.py`), 0 new contracts (extends the frozen `AdmissionRefusalV0` shape), 2 integration surfaces (declaration seat + ledger writer).
7. **REVERSAL COST.** Cheap. The ledger is append-only; a wiring rollback issues a canon-9 correction row (new entry, never a mutation — Canon 8 §21). No user-visible state migrates. Risk: refusal-corpus contamination if the new reason family is retired later — mitigated by keeping the family taxonomy in the refusal-family registry (`WS-WIRE-REFUSAL-FAMILY`).

---

## WS-WIRE-REGISTRY

1. **WHAT.** Wire Function & Promise Registry rows (C1-053, C1-054) to the harvested `services/registry_context/` prompt-context injection subsystem (`WS-HARVEST-REGISTRY-CONTEXT`). Record classes touched: `Registry.Function`, `Registry.Promise` (Canon 9 §6-§18, currently BUILD in Part 2 — this item wires the readers). Task identity: `registry.function_promise_context`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §8 (Function & Promise Registry as tooling artefact); Canon 5 §17 (Registry Administration surface); Canon 2 §14 (condition watchers via readable registry).
3. **DEFINITION OF DONE.** Every prompt built by `registry_context/` reads from the Function & Promise Registry writer (Canon 9 §6 row for Function/Promise classes) rather than from ad hoc lookups. Registry-Administration console read-back (Canon 5 §31-§36) shows every function and promise it will surface AT the same shape the prompt sees. Verification: a compliance-owner opening the Registry-Administration console and clicking any Function row sees the same content the runtime prompt would inject at that instant.
4. **QUALITY EVIDENCE.** Contract test at the `Registry` reader shape (freeze snapshot). Uncurated sample: prompt-injection log for one real workspace over one drill day is diffed against the console read-back. Calibration under Canon 4 §32 quality matrix: coverage = 100% of runtime-inject calls source from the registry writer.
5. **DEPENDENCIES.** Gated by `WS-HARVEST-REGISTRY-CONTEXT` (Part 1) + `WS-BUILD-RECORD-MATRIX` (Part 2 — assigns writer role). Couples with `WS-BUILD-CONSOLE-ADMINISTRATION` (Part 2, read-back surface).
6. **CREDIT COST CLASS.** M. Justification: 2 components (`registry_context/` + admin console read-back path), 1 changed contract (registry reader shape stabilised), ≤2 integration surfaces.
7. **REVERSAL COST.** Medium. If the wiring lands wrong, prompts revert to ad hoc lookups quickly; but a rule-on-paper flag (Canon 5 §26) may fire mid-transition and needs to be ledgered. Reversal requires a matching Registry-writer un-assignment in the record matrix — new entry only.

---

## WS-WIRE-LOOP-ORCH

1. **WHAT.** Operating-loop end-to-end orchestration (C1-062..C1-067, C4-049..C4-051): declare → measure → target → check → deliver → observe. Uses harvested `services/targeta/gap_candidate_filer.py` (`WS-HARVEST-GAP-FILER`). Contracts touched: mining-plan contract (`test_targeta_invariants.test_mining_plan_contract_frozen`), yield-layer permutation guard (`test_targeta_invariants.test_yield_output_is_permutation_raises_on_drop`). Record class touched: `Ledger.Row` (each stage emits). Task identity: `loop.orchestrate.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §6 (loop as first-class); Canon 4 §12-§14 (targeta plans; mtafiti measures); Canon 4 §21-§25 (Critic Seam); Canon 6 §5-§7 (Exploration → gap file → commissioning).
3. **DEFINITION OF DONE.** For a single admitted artefact, all six stages emit their canonical LedgerRow shapes in order; every stage's floor-carrier invariants (targeta yield-layer permutation guard; mtafiti verdict-is-matrix-lookup) hold. Canon 4 §32 "loop repeatability" parameter goes green on a byte-identical replay (`test_v0_paths_byte_identical_after_4a.py` style). Verification pack: Canon 3 §31 prove-one-run for one full loop cycle.
4. **QUALITY EVIDENCE.** Drill class (loop drill). Uncurated sample: one full workspace run replayed byte-identical; loop-completion parameter measured across 50 real runs. Calibration under Canon 4 §32 §10 repeatability + §21 quarantine.
5. **DEPENDENCIES.** `WS-HARVEST-GAP-FILER`, `WS-HARVEST-BATCH-QUARANTINE`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-CONSOLE-EXTRACTION-REGISTRY-DASHBOARD` (Part 2 — for the console-visible loop status).
6. **CREDIT COST CLASS.** L. Justification: 4 components (northena, targeta, mtafiti, service_1), 0 new contracts (uses existing frozen shapes), 3 integration surfaces (declaration, ledger writer, batch board).
7. **REVERSAL COST.** Low-medium. Loop composition is orchestration; the underlying engines are already frozen. Reversal = disabling the orchestrator hook and letting individual services run standalone (their existing tests still pass). No data shape changes.

---

## WS-WIRE-SOLVA-CIF

1. **WHAT.** Apply the spine's Solva-pattern validation (`services/solva_depth/`) to the CIF's OWN claims (Canon 2 §12: coach seat's origination port claims and CIF-parameter measurements). Record class touched: `Solva.Trace` (Canon 9 §6 writer = Solva). Task identity: `cif.solva_reflexive_check`.
2. **CANON CLAUSES SATISFIED.** Canon 2 §12 (CIF makes claims and must submit them to the same validation as user claims); Canon 3 §14 (assertion boundary applies universally); Canon 1 §7 (engine walls — Solva does not extract, but validates all claims).
3. **DEFINITION OF DONE.** Every CIF claim (frame detection, adoption, metabolisation completion, parameter reading) passes through `services.solva_depth.assertion.conclusion_class` with the same floor-over-load-bearing discipline (`test_class_is_floor_over_load_bearing_all_fact`). CIF cannot self-certify (Canon 2 §17-§19 "permanent bound — self-certification closed"). Verification: prove-one-run for a frame-adoption event shows Solva verdict on the CIF's claim.
4. **QUALITY EVIDENCE.** Invariant test extending `test_solva_assertion_boundary.py`. Uncurated sample: 20 CIF frame detections drawn from Watch/CIF logs in the first month post-live; every one carries a Solva trace row. Calibration under Canon 3 §31: assertion boundary is parameterless — no CIF field may inject "confidence" or "caveat".
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT` (Part 2), `WS-CIF-DETECTION` (Part 2), `WS-CIF-METABOLISATION` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2 — Solva trace writer row).
6. **CREDIT COST CLASS.** S. Justification: 1 component (CIF calls Solva), 0 new contracts, 1 integration surface (Solva-depth boundary).
7. **REVERSAL COST.** Low. The Solva boundary is already frozen; adding a caller is additive. Reversal = removing the CIF call site; the CIF then re-enters self-certification (Canon-2 violation). Ledger the wire event as an append-only record.

---

## WS-WIRE-INTENT-AUDIT-WATCH

1. **WHAT.** Intent-audit divergence-field (from admit) consumed by the Watch's Macho sensor. Row C3-026 PARTIAL. Record class touched: `Watch.Verdict` (Canon 9 §6 writer = Watch, reader = Compliance Console + Governance). Task identity: `watch.macho.intent_divergence_sense`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §26 (intent audit); Canon 8 §6 (three-actor seam Macho sensor); Canon 8 §14-§15 (marks + reconciliation); Canon 9 §6 handoff `governance→Watch verdict`.
3. **DEFINITION OF DONE.** Every intent-audit divergence row (declared purpose vs measured purpose) becomes an input to Macho; a divergence above the governed threshold produces a Watch mark of class `intent_divergence` (Canon 8 §14). The mark carries the source LedgerRow id (append-only chain). Verification: a drill with a deliberately-diverged actor produces one and only one intent-divergence mark within Canon 8 §5 machine-speed bounds (< the frozen response-time seat).
4. **QUALITY EVIDENCE.** Drill class (Watch drill C8-034). Uncurated sample: 5 divergence fixtures spanning the calibration band + 5 non-divergent controls; false-mark rate must stay under the Canon-8 §32 operative parameter. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS` (Part 2 — Macho sensor), `WS-BUILD-WATCH-MARK-REGISTER` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-LEDGER-MATRIX` (this Part 1).
6. **CREDIT COST CLASS.** M. Justification: 2 components (intent-audit surface, Watch Macho ingest), 1 new contract (intent-divergence mark class), 2 integration surfaces (ledger reader + Watch mark writer).
7. **REVERSAL COST.** Medium. Marks are append-only; a wrong wire generates spurious marks. Reversal = disable divergence ingest; marks written stay in the register with a Canon 8 §21 correction entry. No mark class deletion.

---

## WS-WIRE-WATCH-PLANE-ACTIVITY

1. **WHAT.** Watch reads plane activity (not content) — row C7-019. Canon 8 §21 boundary constraint: Watch sees activity metadata (who wrote what class, when, verdict), never plane content. Record class touched: `Watch.Read` (Canon 9 §8 read-only reader; no writer). Task identity: `watch.plane_activity_read`.
2. **CANON CLAUSES SATISFIED.** Canon 7 §19 (plane activity — not content); Canon 8 §21 (Watch never reads content); Canon 9 §8 (matrix defines reader lists per class).
3. **DEFINITION OF DONE.** Watch's plane-activity reader passes a discipline test that no content field crosses the boundary. Canon 8 §21 operative parameter "watch surface bounded to activity" goes green. Verification: an AST-level ingress-firewall test (mirror of the existing `test_ast_egress_gate.py` in Extraction-Akki) blocks any content-typed field from reaching Watch code.
4. **QUALITY EVIDENCE.** Invariant test (AST-scoped gate). Uncurated sample: one week of real plane activity events on the drill fixture; boundary crossing count = 0. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION` (Part 2), `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-HARVEST-PARTITIONS` (Part 1 — session partitions carry the activity envelope).
6. **CREDIT COST CLASS.** M. Justification: 2 components (plane reader shim + Watch ingest), 1 changed contract (Watch's read shape), 2 integration surfaces.
7. **REVERSAL COST.** Low-medium. Reversal = disable the reader. But if any Watch verdict was written using content (violation), those verdicts are frozen (append-only). Remediation is by Canon 8 §21 correction entry — not deletion.

---

## WS-WIRE-ADMISSION-HANDOFF

1. **WHAT.** Existing admission→extraction handoff at `services/wizard/admission_handoff.py` (per REUSE_ASSESSMENT.md file map) registered as a Canon-9 §6 contract (row C9-036). Record class touched: `Handoff.Contract` (Canon 9 §8-§42). Task identity: `handoff.admission_to_extraction`.
2. **CANON CLAUSES SATISFIED.** Canon 9 §6 (handoff contracts as first-class); Canon 9 §8-§42 (six handoff contract shapes).
3. **DEFINITION OF DONE.** The `admission_handoff` interface is registered as one of the six Canon-9 handoff contracts (WS-BUILD-HANDOFF-REGISTRY, Part 2), its wire shape frozen under `tests/invariants/test_invariant_contract_snapshots.py` (see `WS-WIRE-PARITY-EXTENSION`). Verification: contract-snapshot test emits a parity seat entry for this handoff.
4. **QUALITY EVIDENCE.** Contract test (snapshot). Uncurated sample: one week of live admission handoffs; every handoff carries the frozen contract shape. Calibration under Canon 3 §31 verification pack ("prove-one-run" for one handoff).
5. **DEPENDENCIES.** `WS-BUILD-HANDOFF-REGISTRY` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1).
6. **CREDIT COST CLASS.** S. Justification: 1 component (existing handoff), 0 new contracts (just registers an existing shape), 1 integration surface (registry).
7. **REVERSAL COST.** Very low. Registration is metadata; reversal = de-register in a new matrix entry (append-only). Handoff code untouched.

---

## WS-WIRE-CRITIC-INTO-ANSWERING (PROMOTED by Ruling 2)

1. **WHAT.** Wire the harvested `services/critic_pass/` (from `WS-HARVEST-CRITIC-SEAM`) INTO the spine's answering-request path — the seam only counts when it's in the request flow. Components touched: `services/chat/protective_layer/` + `services/documents/` + `services/analyze_workspace/` + every RE-POINTed answering surface (see `WS-REPOINT-ANSWERING-SURFACES`). Contract: critic-seam manifest gate on outbound answers. Record class touched: `Critic.Verdict` (Canon 9 §6 writer = Critic Seam, reader = Compliance Console + Watch). Task identity: `answer.critic_gate.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §21-§23 (Critic Seam guards what workers produce; identical architecture guards what the pipeline produces); Canon 7 §31-§34 (Critic Seam as integration contract); Canon 2 §10.2 (pre-ship checklist).
3. **DEFINITION OF DONE.** Every answering surface's outbound envelope passes the Critic manifest gate (`test_cif_manifest_submission_gate.py`-shape). No answer leaves the platform without a Critic verdict recorded in the ledger. Canon 4 §32 "critic hit-rate" parameter goes green against the uncurated sample. Verification: drill (Canon 8 §21-§39 standing drills) fires a shaped-defect fixture and the Critic Seam catches it before the answer surfaces.
4. **QUALITY EVIDENCE.** Contract test (manifest gate). Uncurated sample: 100 real answer envelopes across the four answering surfaces over one drill day; Critic verdict rate = 100%, catch rate on seeded defect corpus ≥ Canon 4 §32 threshold. Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-CRITIC-SEAM` (this Part 1), `WS-REPOINT-ANSWERING-SURFACES` (this Part 1), `WS-WIRE-LEDGER-MATRIX` (this Part 1).
6. **CREDIT COST CLASS.** L. Justification: 4+ components (chat, documents, analyze_workspace, deck_*, inbox_routing, work_studio outputs — the request path fans across the answering surface set), 1 new contract (Critic verdict shape at the outbound envelope), 2 integration surfaces (Critic Seam ingest + ledger writer).
7. **REVERSAL COST.** Medium. Reversal = removing the gate re-opens ungoverned answers (a Canon-7 violation, ledgered as such). Critic verdicts written stay in the ledger; new entries only. Every un-gated answer surface must issue a Canon 8 §21 correction entry naming itself.

---

## WS-WIRE-PARITY-EXTENSION (PROMOTED by Ruling 2)

1. **WHAT.** Extend the frozen-contract-snapshot parity discipline (`tests/invariants/test_invariant_contract_snapshots.py` + 10+ frozen-shape invariants in `Extraction-Akki/backend/tests/invariants/`) to every NEW contract this programme creates: all six Canon-9 handoff contracts, all thirteen Canon-9 record classes, every Watch verdict shape, and the task-identity register schema. Contract touched: parity-seat manifest. Record class touched: `ParitySeat.Contract`. Task identity: `parity_seat.contract_freeze.per_shape`.
2. **CANON CLAUSES SATISFIED.** Canon 9 §6-§18 (record matrix as live contracts); Canon 9 §8-§42 (handoff contracts); Canon 8 §21-§59 (Watch record classes); Canon 3 §31 (verification packs); Canon 4 §32 (quality matrix).
3. **DEFINITION OF DONE.** For every new contract this programme creates, a matching parity-seat entry lands in `tests/invariants/test_invariant_contract_snapshots.py` (or a companion). Every new contract has a frozen JSON snapshot alongside `memory_plane_v0.contract_snapshot.json` shape. Contract-drift test fires (invariant class) on any downstream field-name / type change without matrix-recorded migration. Verification pack: Canon 3 §31 prove-one-run confirms every new contract carries its snapshot.
4. **QUALITY EVIDENCE.** Invariant class (contract-drift). Uncurated sample: every new contract from Part 2 BUILD items. Calibration under Canon 3 §31 — no contract lands without its parity seat.
5. **DEPENDENCIES.** Gates every Part 2 BUILD that introduces a new contract: `WS-BUILD-HANDOFF-REGISTRY`, `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-WATCH-RECORD-CLASSES`, `WS-BUILD-DECL` (declaration record).
6. **CREDIT COST CLASS.** L. Justification: touches the parity-seat surface (1 component) but crosses ≥6 new contracts (Canon-9 handoffs + 13 record classes + Watch verdict shapes + task-identity register); qualifies as L on the "3+ components / new register" criterion via the register count.
7. **REVERSAL COST.** Cheap but consequential to remove: the parity seat is READ by every regression test; delete it and downstream contract drift becomes undetectable. If wrong, correction is a new entry to the parity manifest — new entry only, never mutation.

---

## WS-WIRE-REFUSAL-FAMILY (PROMOTED by Ruling 2)

1. **WHAT.** Wire the existing refusal-family taxonomy (`services/memory/memory_refusal_reasons.v0.json` + `services/memory/refusal.py`) to the Canon 5 §9.2 refusal card surface (`WS-BUILD-REFUSAL-CARD-COPY`, Part 2). Contract touched: refusal-reason JSON snapshot (frozen; must be extended via parity seat per `WS-WIRE-PARITY-EXTENSION`). Record class touched: `Refusal.Reason`. Task identity: `refusal.family.render_at_surface`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §9.2 (verbatim refusal card copy); Canon 1 §16 (refusal recorded, never dropped — N-INV-9); Canon 3 §17 (refusal shapes catalogued).
3. **DEFINITION OF DONE.** Every refusal reason surfaced in the Canon 5 §9.2 refusal card component is sourced from the `memory_refusal_reasons.v0.json` taxonomy — no ad hoc copy. The card's frozen-copy invariant test asserts byte-identity of the rendered refusal text with the taxonomy entry. Canon 3 §31 prove-one-run for a refused request emits the taxonomy id + the card copy identically.
4. **QUALITY EVIDENCE.** Invariant class (frozen-copy). Uncurated sample: every distinct refusal reason encountered across a drill week must render verbatim from the taxonomy in every refusal-card impression. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-REFUSAL-CARD-COPY` (Part 2 — the surface being wired to), `WS-WIRE-PARITY-EXTENSION` (this Part 1 — extends the parity seat for the JSON taxonomy).
6. **CREDIT COST CLASS.** S. Justification: 1 component (refusal card render), 0 new contracts (uses existing JSON snapshot), 1 integration surface (memory/refusal reader).
7. **REVERSAL COST.** Very low. Reversal = drop the wire; card falls back to no-refusal render (Canon 5 violation, dormant-state anti-pattern). Refusal taxonomy itself is untouched.

---

## WS-WIRE-LEDGER-MATRIX (PROMOTED by Ruling 2)

1. **WHAT.** Promote the Northena ledger's sole-writer position (`services/northena/ledger.py:63 record()`, `insert_one` at L65) to a Canon 9 §6-§18 matrix-governed writer — the ledger IS the writer for record class `Ledger.Row` in the matrix. Component touched: `services/northena/ledger.py`. Contract touched: `LedgerRow` frozen shape (`test_northena_ledger_row_v0.py`). Record class: `Ledger.Row` (Canon 9 §6 row 1). Task identity: `ledger.writer.matrix_governed`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §4.3 (append-only, N-INV-4); Canon 1 §7.1 (Northena as authoritative ledger); Canon 9 §6-§18 (record matrix — writers and readers defined); Canon 9 §8 (reads route through matrix reader-list).
3. **DEFINITION OF DONE.** The record matrix `WS-BUILD-RECORD-MATRIX` (Part 2) names Northena's `record()` as the sole writer for `Ledger.Row`. Every reader of `db.northena_ledger` is enumerated in the matrix reader-list; any code path reading the collection outside the reader-list fails an AST discipline check (mirror of `test_ast_egress_gate.py`). Verification: matrix reader-list snapshot has 100% coverage of the observed readers over a drill week.
4. **QUALITY EVIDENCE.** Invariant class (matrix-writer-sole; AST-scoped reader-list check). Uncurated sample: full week of ledger writes and reads; writer count outside `record()` = 0, reader count outside matrix reader-list = 0. Calibration under Canon 3 §31 + Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1 — for the matrix shape).
6. **CREDIT COST CLASS.** M. Justification: 1 component (ledger), 1 new/changed contract (matrix governance seat on this ledger), 2 integration surfaces (matrix writer role + matrix reader-list).
7. **REVERSAL COST.** High-on-drift. If the matrix seat is landed and later stripped, existing readers may still route through the seat and stop reading. Reversal = new matrix entry re-opening the reader-list; but the ledger is append-only — no ledger row can be un-written. Any migration error stays in the append-only chain forever. This is a case for careful review before wiring.

---

# B. HARVEST items (9)

HARVEST covers pulling existing code from a non-spine repo into the spine as source-of-truth. The harvest is paper-only here; the actual code motion is a Ruling-1-prohibited operation until an owner build order lifts the prohibition.

---

## WS-HARVEST-CRITIC-SEAM

1. **WHAT.** Harvest `services/critic_pass/` (7 files, ~950 LOC) + `services/critic_pass/rubric.py` + `services/critic_pass/seeded_defect_corpus.py` from Akki-OS-V1 into Extraction-Akki spine. Rows: C2-011, C2-016..C2-018, C2-025..C2-028, C2-052..C2-059, C4-031, C7-024..C7-028, C7-D02, C7-D26. Record class: `Critic.Verdict`. Task identity: `critic_seam.execute.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §21-§23 (Critic Seam architecture); Canon 7 §31-§34 (Critic Seam as integration contract); Canon 2 §10.2 (pre-ship checklist); Canon 2 §16-§18 (manifest schema + submission gate).
3. **DEFINITION OF DONE.** All 7 `critic_pass/` files present at the spine at import path `services.critic_pass`. Companion tests `test_critic_pass_execution_atomic.py` + `test_cif_manifest_submission_gate.py` present and firing. Canon 4 §32 "critic seam operative" parameter goes green (uncurated sample: 100% of critic invocations return a rubric-scored verdict). Verification pack: Canon 3 §31 prove-one-run on the critic seam.
4. **QUALITY EVIDENCE.** Contract test (manifest gate) + drill class (seeded-defect corpus). Uncurated sample: the `seeded_defect_corpus` fixture drives the drill; catch-rate must meet Canon 4 §32 threshold. Calibration obligation: Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** No dependencies inward (critic_pass is self-contained per Chunk 2 shaping analysis). Feeds `WS-WIRE-CRITIC-INTO-ANSWERING`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (services/critic_pass — self-contained per Chunk-2 dependency analysis), 0 new contracts (critic-pass is already frozen-shape at Akki-OS-V1), 1 integration surface (import into spine).
7. **REVERSAL COST.** Low. Files harvested can be de-harvested; the spine reverts to no-critic-seam (which is a Canon-7 violation but not a data-loss). No user-visible state changes.

---

## WS-HARVEST-BATCH-QUARANTINE

1. **WHAT.** Harvest `services/service_1/batch_quarantine.py` (227 LOC) from Akki-OS-V1. Row C4-047. Cited by `critic_pass/harness.py:26` as the "fail-closed per-batch quarantine". Record class: `Batch.QuarantineDecision`. Task identity: `batch.quarantine.per_batch`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §23 (Quarantine); Canon 4 §34.1 (Batch Board); Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` sanctions the landing.
3. **DEFINITION OF DONE.** File at spine path `services/service_1/batch_quarantine.py`. Quarantine verdict emitted per batch flows to `WS-BUILD-BATCH-BOARD-SURFACE` (Part 2) as the panel data. Canon 4 §32 "batch quarantine hit rate" parameter goes green. Verification: drill fires a shaped-batch fixture; quarantine reason recorded.
4. **QUALITY EVIDENCE.** Invariant class (frozen-shape quarantine decision). Uncurated sample: 20 real batches drawn from the drill week; every above-threshold batch quarantined with a reason. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-BUILD-BATCH-BOARD-SURFACE` (Part 2) and `WS-WIRE-LOOP-ORCH` (this Part 1).
6. **CREDIT COST CLASS.** S. Justification: 1 component (single file), 0 new contracts (existing frozen shape), 1 integration surface.
7. **REVERSAL COST.** Very low. Single-file de-harvest; loop reverts to no-quarantine (Canon-4 violation, ledgered).

---

## WS-HARVEST-GAP-FILER

1. **WHAT.** Harvest `services/targeta/gap_candidate_filer.py` (132 LOC) from Akki-OS-V1. Task identity: `targeta.gap_filer.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §35 (Gap ranking); Canon 6 §5-§7 (Exploration → gap file → commissioning loop).
3. **DEFINITION OF DONE.** File at spine path `services/targeta/gap_candidate_filer.py`. Its output feeds the operating loop's "target" stage (`WS-WIRE-LOOP-ORCH`). Canon 4 §32 "gap ranking coverage" parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (frozen candidate shape). Uncurated sample: gap candidates drawn from one drill week. Calibration under Canon 4 §32 + Canon 6 §5-§7.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-LOOP-ORCH`.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

## WS-HARVEST-REGISTRY-CONTEXT

1. **WHAT.** Harvest `services/registry_context/` (5 files) from Akki-OS-V1. Task identity: `prompt.context_injection.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §17 (Registry Administration); Canon 2 §14 (condition watchers via readable registry).
3. **DEFINITION OF DONE.** Five files at spine paths under `services/registry_context/`. `test_registry_context_block_golden_snapshot.py` + `test_g_13_execution_atomic.py` at spine test paths. Canon 5 §17 admin-console read-back parameter goes green (see `WS-WIRE-REGISTRY`).
4. **QUALITY EVIDENCE.** Contract test (golden snapshot). Uncurated sample: 20 real prompt-injection events, golden snapshot diff against the runtime context. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-REGISTRY`.
6. **CREDIT COST CLASS.** S. Justification: 5 files but 1 component (self-contained), 0 new contracts.
7. **REVERSAL COST.** Low.

---

## WS-HARVEST-PARTITIONS

1. **WHAT.** Harvest `services/partitions/session_working_set.py` (Akki-OS-V1 unique, 2 files). Task identity: `session.partition.per_actor`.
2. **CANON CLAUSES SATISFIED.** Canon 6 §3.1 (setup declarations create session scope); Canon 7 §19 (plane activity envelope).
3. **DEFINITION OF DONE.** Files at spine paths. `test_partition_schema_v0_envelope.py` at spine test path. Canon 6 §3.1 setup parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (partition envelope). Uncurated sample: one drill week; every session's partition envelope carries the frozen shape. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-WATCH-PLANE-ACTIVITY` and `WS-BUILD-SETUP-CONSOLE` (Part 2). **Also part of Open Question #9 (Akki-OS-V1 non-canonical harvest items).**
6. **CREDIT COST CLASS.** S. Justification: 1 component (2 files, self-contained), 0 new contracts.
7. **REVERSAL COST.** Low.

---

## WS-HARVEST-SEQUENCING-HARNESS

1. **WHAT.** Harvest `services/sequencing_harness/` (7 files) from Akki-OS-V1. Task identity: `sequencing.harness.per_run`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §6 (loop pipeline); specific clauses require deeper read (see fidelity-ledger OQ #9 — pending owner call).
3. **DEFINITION OF DONE.** _Un-fillable at this stage without deeper read_ → **fidelity_ledger.md** entry FL-P1-01: "Which specific Canon clauses does `sequencing_harness` satisfy that are not already covered by `services/targeta` and `services/mtafiti`? Confirm harvest scope."
4. **QUALITY EVIDENCE.** _Pending Canon clause identification._
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-LOOP-ORCH` if canon anchor confirmed.
6. **CREDIT COST CLASS.** S–M pending scope. Provisional S (7 files self-contained). Reclassify after fidelity-ledger resolution.
7. **REVERSAL COST.** Low.

---

## WS-HARVEST-FAR-ENDPOINT

1. **WHAT.** Harvest `services/far_endpoint/` (4 files) + `services/generated_gates/` (16 files, regenerable outputs) from Akki-OS-V1. Task identity: `far_endpoint.gate_generation.per_mandate`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §8 (Function & Promise Registry tooling artifacts).
3. **DEFINITION OF DONE.** Files at spine paths. Regeneration test `test_generated_gates_regeneration_diff.py` at spine test path; regeneration produces byte-identical outputs. Canon 1 §8 registry-tooling parameter goes green.
4. **QUALITY EVIDENCE.** Invariant class (byte-identical regeneration). Uncurated sample: one mandate cycle; regeneration diff = 0 bytes. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. Feeds `WS-WIRE-REGISTRY`. **Also part of Open Question #9.**
6. **CREDIT COST CLASS.** S. Justification: 1 component (self-contained tooling), 0 new contracts.
7. **REVERSAL COST.** Very low. Tooling artefacts are regenerable.

---

## WS-HARVEST-STREAMING

1. **WHAT.** Harvest `services/synisense/shield/streaming.py` from Akki-Executive-Core (Core-2/Extraction-Akki currently lack this file). Task identity: `shield.streaming.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §7.1 (Shield boundary as first-class); Canon 3 §12 (input seat); Canon 7 §19 (plane activity envelope for streamed frames).
3. **DEFINITION OF DONE.** File at spine path `services/synisense/shield/streaming.py`. The 19-LOC shim at `services/llm_streaming.py` (currently in Executive-Core, will be RE-POINTed) points to this spine location. Canon 3 §12 streaming-port parameter goes green (frames pass through the shield's input_seat).
4. **QUALITY EVIDENCE.** Invariant class (frame-envelope shape) + contract test at streaming boundary. Uncurated sample: streamed answer sessions over one drill day; every frame carries the shield envelope. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** No inward dependencies. **Gates `WS-REPOINT-ANSWERING-SURFACES`** — streaming port must exist before RE-POINT completes.
6. **CREDIT COST CLASS.** M. Justification: 1 component, 1 new/changed contract (streaming frame shape at the spine), 2 integration surfaces (input_seat + downstream reader).
7. **REVERSAL COST.** Low-medium. De-harvest = streaming dies at spine; Executive-Core RE-POINT stalls. Reversal via new import path is trivial while nothing depends on it, expensive once RE-POINT completes.

---

## WS-HARVEST-TWO-PASS-AMENDMENT

1. **WHAT.** Harvest verbatim refusal templates from Executive-Core's `services/two_pass.py` as an amendment to the spine's Solva-pattern refusal shapes (Canon 3 §17). Task identity: `refusal.two_pass_template.per_amendment`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §17 (refusal shapes catalogued); Canon 5 §9.2 (verbatim refusal card copy).
3. **DEFINITION OF DONE.** Two-pass refusal templates registered as additional entries in the refusal-family taxonomy (`memory_refusal_reasons.v0.json`). Every template's rendered text passes the Canon 5 §9.2 frozen-copy invariant (see `WS-WIRE-REFUSAL-FAMILY`).
4. **QUALITY EVIDENCE.** Invariant class (frozen copy). Uncurated sample: every two-pass refusal template appears in the taxonomy JSON with byte-identical text.
5. **DEPENDENCIES.** `WS-WIRE-REFUSAL-FAMILY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (taxonomy JSON extension), 0 new contracts (uses existing taxonomy shape).
7. **REVERSAL COST.** Low. Roll back the JSON entries (parity-seat new entry); render surfaces revert to no-template.

---

# C. RE-POINT items (3)

RE-POINT covers Executive-Core answering surfaces whose LLM boundary is trivially adapter-swappable (`SyniSenseContract` at `backend/contracts/synisense.py:25-28`). Paper-only.

---

## WS-REPOINT-ANSWERING-SURFACES

1. **WHAT.** RE-POINT Executive-Core answering surfaces (chat/, documents/, analyze_workspace/, ideas_engine/, deck_*.py, inbox_routing/) onto the spine via a `SyniSenseContract` adapter swap. Component set: 8 top-level services + 36 loose service files (per Chunk-2 shaping analysis). Contract touched: `SyniSenseContract.shield_invoke` (frozen at Executive-Core `backend/contracts/synisense.py:25-28`). Record class: `Answer.Envelope` (Canon 9 §6 writer = answering surface). Task identity: `answer.compose.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §12 (six services boundary); Canon 5 §40 (Work pillar surfaces); Canon 7 §11-§12 (envelope class-chip render); Canon 4 §32 (quality matrix applies to answers).
3. **DEFINITION OF DONE.** The in-process `SyniSenseContract` adapter is replaced (paper-plan) by an HTTP adapter that calls the spine's shield endpoint. Every answer envelope carries the spine's class-chip (Canon 5 §2-§4). All four RE-POINTable surface classes (chat, documents, analyze_workspace, deck_*) surface the spine's Critic-Seam verdict (via `WS-WIRE-CRITIC-INTO-ANSWERING`). Canon 4 §32 "answer-envelope class-chip presence" parameter goes green.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill class (answering-day drill). Uncurated sample: 100 real answers across the 8 surfaces over one drill day; envelope shape frozen. Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-STREAMING` (Part 1 — streaming port must exist), `WS-WIRE-CRITIC-INTO-ANSWERING` (this Part 1), `WS-WIRE-LEDGER-MATRIX` (this Part 1), `WS-BUILD-CLASS-CHIP-LIBRARY` (Part 2), `WS-BUILD-ANSWER-CARD` (Part 2). Also depends on `WS-REBUILD-WORK-STUDIO-STORAGE` for the work_studio subset (partial RE-POINT until storage lands).
6. **CREDIT COST CLASS.** XL. Justification: 4+ components AND estate-wide wiring. **One-paragraph defence:** Every non-application-territory answer flow in Executive-Core routes through this adapter swap, and the swap crosses the Shield boundary, streaming port, memory plane, ledger matrix, class-chip render surface, and Critic Seam simultaneously. Sequencing missteps in any of the six integration surfaces produce answer-outage or spec violation. The estate-wide integration-surface count and the answer-path fan-out both meet the XL bar independently.
7. **REVERSAL COST.** Very high on ANY user-visible answer regression during the transition. The adapter swap is atomic per-surface but staged across surfaces; a half-swap produces two adapters live simultaneously. Reversal requires per-surface adapter restoration and a Canon-3 §24 rule-change ceremony to un-freeze the swap. Data (answers) landing during a bad-swap window are ledgered append-only; no un-write, remediation via Canon 8 §21 correction entries per bad-swap answer.

---

## WS-REPOINT-SOLVA-V2

1. **WHAT.** RE-POINT the Executive-Core `services/solva_v2/` narration surface (30 files: analyze_narration, chair_notes, chat_v2_prompts, engines/, etc.) — surface preserved, reasoning boundary delegated to spine's `solva_depth`. Component: `services/solva_v2/`. Contract: `analyze_narration.shield_invoke` Phase-4.0 shim. Record class: `Solva.Trace` (Canon 9 §6 writer = Solva). Task identity: `solva.narration.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §14 (assertion boundary — spine owns it); Canon 5 §40 (narration as journalist-style surface); Canon 2 §6 (engine walls — narration is not extraction).
3. **DEFINITION OF DONE.** Solva-v2 narration surface remains at Executive-Core-turned-application. Every reasoning boundary call routes through spine's `solva_depth.assertion.conclusion_class`. Canon 3 §14.2 "parameterless assertion boundary" invariant holds — no narration field injects "confidence" or "caveat". Canon 4 §32 narration operative parameter goes green.
4. **QUALITY EVIDENCE.** Invariant test extending `test_conclusion_class_signature.py`. Uncurated sample: 20 solva-v2 sessions from a drill week; every reasoning delegation carries a spine Solva trace row. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-REPOINT-ANSWERING-SURFACES` (adapter path), `WS-WIRE-SOLVA-CIF` (parallel Solva-boundary hygiene), `WS-WIRE-LEDGER-MATRIX`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (analyze_narration, engines/, guardrails/, integrity_validators), 1 changed contract (adapter shim shape), 2 integration surfaces (Shield + Solva boundary).
7. **REVERSAL COST.** Medium. Reversal restores Executive-Core's private Solva narration path (a Canon-3 §14 violation, ledgered). Sessions landed under the wrong path are frozen in the ledger; new entries only.

---

## WS-REPOINT-SOLVA-VOICE-AUDIT

1. **WHAT.** RE-POINT Executive-Core's `services/solva_voice_audit/` (24 files: voice/, orchestration/, guardrails/, reasoning/) coach-voice narration surface. Component: `services/solva_voice_audit/`. Contract: `orchestration/shield_invoker.py`. Record class: `Solva.Trace` + potentially `Input.Seat.Audio` (see fidelity ledger). Task identity: `solva.voice_audit.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §12 (input seat) — voice audit ingest touches audio material; Canon 3 §14 (assertion boundary); Canon 5 §40 (narration surface); Canon 1 §7.1 (Shield boundary).
3. **DEFINITION OF DONE.** _Partial DoD, pending resolution of fidelity-ledger entry_ **FL-P1-02:** "Does audio material transit the shield's input_seat or REBUILD is required under Canon 3 §13.1 custody sequence?" (per Chunk-2 shaping analysis). If input_seat covers audio → RE-POINT as `WS-REPOINT-SOLVA-V2`-shape. If not → this item split into REBUILD-VOICE-INPUT + RE-POINT-NARRATION. **Placeholder DoD (path A):** Voice-audit ingest routes through spine's input_seat; audio + speech-derived text carry a Solva trace and a de-identifier verdict.
4. **QUALITY EVIDENCE.** Contract test (input-seat envelope). Uncurated sample pending path resolution. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-REPOINT-ANSWERING-SURFACES`, `WS-WIRE-LEDGER-MATRIX`, and pending fidelity-ledger entry FL-P1-02.
6. **CREDIT COST CLASS.** L on path A (RE-POINT); XL on path B (REBUILD required). Reclassify after fidelity-ledger resolution.
7. **REVERSAL COST.** Medium (path A). High if audio material was ever ingested outside the input_seat during the transition (Canon 3 §12 violation; ledgered forever).

---

# D. REBUILD items (1)

REBUILD covers non-canon-conformant Executive-Core code whose storage shape can NOT be RE-POINTed cleanly — a real code migration of user-visible state.

---

## WS-REBUILD-WORK-STUDIO-STORAGE

1. **WHAT.** Migrate `work_studio`'s 200+ real user exports (residing in `Akki-Executive-Core/uploads/work_studio_exports/`) + the deep mongo storage layer (`db.work_studio_*` across the surfaces named in `routers/studio.py` [915 L], `studio_blocks.py` [1226 L], `work_studio_export.py` [2974 L], `work_studio_from_source.py` [800 L], `work_studio_overlay.py` [828 L], `work_studio_render.py`) to Doc 7 §19-§23 per-application memory plane. Component set: work_studio backend + object-storage port + 20+ frontend components under `components/work_studio/`. Contract: `work_studio_export.v0` (currently ad hoc; to be frozen). Record class: `WorkStudio.Doc`, `WorkStudio.Version`, `WorkStudio.Lineage`. Task identity: `work_studio.storage.per_document`.
2. **CANON CLAUSES SATISFIED.** Canon 7 Part IV §19-§23 (per-application memory plane; plane-keyed storage); Canon 1 §12 (six services; storage is a service); Canon 9 §6 (record classes at the storage boundary).
3. **DEFINITION OF DONE.** All work_studio state lives behind the memory-plane reader/writer boundary. The 200+ existing exports are migrated to the plane with byte-identical fidelity (source-of-truth JSON snapshots frozen under parity seat via `WS-WIRE-PARITY-EXTENSION`). `test_memory_service_m_g1_to_m_g9.py`-shape tests exist and pass for work_studio. Canon 7 §19-§23 "plane-keyed storage" parameter goes green. Verification: Canon 3 §31 prove-one-run on one migrated document renders byte-identically pre-and-post migration.
4. **QUALITY EVIDENCE.** Invariant class (byte-identical migration replay) + drill class (migration drill). **Uncurated sample: every single one of the 200+ exports must be part of the migration corpus — no sampling.** Calibration under Canon 3 §31 + Canon 4 §32.
5. **DEPENDENCIES.** **Gates completion of `WS-REPOINT-ANSWERING-SURFACES` for work_studio subset.** Depends on **Object Storage Port (Doc 7)** — not yet a spine capability; treated as an implicit BUILD dependency captured in fidelity ledger FL-P1-03. Depends on `WS-BUILD-RECORD-MATRIX` (Part 2), `WS-WIRE-PARITY-EXTENSION` (this Part 1), `WS-REPOINT-WORK-STUDIO-LLM` (this Part 1).
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** The item introduces a new authority (object-storage boundary) into the spine AND is estate-wide (every work_studio subsurface touches storage) AND carries a data migration (200+ real user exports). Any of the three would qualify XL on the threshold; all three together make the review-load and reversibility risk categorically higher than any RE-POINT. This is the single most reversal-expensive Part-1 item.
7. **REVERSAL COST.** **VERY HIGH — canonical cheap-to-build/expensive-to-reverse case.** Per Ruling 2 §2 specifically: user-data migration reversibility is inherently one-way once the plane becomes source-of-truth. **Explicit user-data reversal statement:** (a) A migration that lands wrong produces two source-of-truth stores in parallel (mongo + plane) for the transition window; every document touched during the window becomes ambiguous. (b) Rollback requires either restoring mongo as source-of-truth (losing plane-only writes) OR keeping plane and losing pre-plane mongo-only edits — either choice loses user work. (c) Recommended discipline: shadow-write phase (both stores written, reader still on mongo) precedes the reader-cutover; the shadow-write phase can be reversed cheaply. Reader-cutover cannot. This item must not proceed to reader-cutover without owner sign-off on the migration certificate (Canon 6 §11-§13 commissioning certificate shape).

---

# E. RE-POINT (Work-Studio LLM boundary only)

Separated from `WS-REBUILD-WORK-STUDIO-STORAGE` because the LLM boundary is adapter-swappable independent of the storage migration.

---

## WS-REPOINT-WORK-STUDIO-LLM

1. **WHAT.** Adapter-swap `work_studio`'s `shield_invoke` call sites onto the spine `SyniSenseContract`. Component: `work_studio/` LLM boundary only (not storage). Contract: `SyniSenseContract.shield_invoke`. Record class: `Answer.Envelope` (via `WS-REPOINT-ANSWERING-SURFACES`). Task identity: `work_studio.shield_call.per_session`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §7.1 (Shield boundary); Canon 5 §40 (Work pillar); Canon 4 §32 (envelope quality).
3. **DEFINITION OF DONE.** Every `work_studio` shield call routes through the spine adapter (part of `WS-REPOINT-ANSWERING-SURFACES`). Storage layer remains at Executive-Core mongo until `WS-REBUILD-WORK-STUDIO-STORAGE` completes. Canon 4 §32 "answer envelope class-chip presence" parameter goes green for work_studio surfaces.
4. **QUALITY EVIDENCE.** Contract test (envelope shape). Uncurated sample: 20 work_studio sessions. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** Subset of `WS-REPOINT-ANSWERING-SURFACES`; independent of `WS-REBUILD-WORK-STUDIO-STORAGE`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (LLM boundary only), 0 new contracts, 2 integration surfaces (Shield + Critic Seam).
7. **REVERSAL COST.** Low. LLM-boundary reversal is fully covered by adapter restore.

---

# F. CONTRADICTION items (1)

CONTRADICTION covers Executive-Core surfaces where the assessment found a canon-compliant surface that a strict Canon-1 §12 reading would strip. Ruling 1 governs the transition.

---

## WS-CONTRADICTION-PURPOSE-GATE

1. **WHAT.** Executive-Core `services/synisense/shield/purpose_validator.validate_purpose()` (at `client.py:63`) purpose-enforcement gate. Component: `services/synisense/shield/purpose_validator.py`. Contract: purpose-enforcement input envelope. Record class: `Purpose.Verdict` (Canon 8 §21-§59 category). Task identity: `shield.purpose_gate.per_call`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §6.1 (actor-declaration must fire); Canon 8 §14-§15 (Watch reconciler must fire); Canon 9 §6 handoff `governance→Watch verdict`. Ruling 1 binds the transition condition.
3. **DEFINITION OF DONE.** **Under Ruling 1, DoD IS the demonstrated-firing evidence.** Specifically: (a) `WS-BUILD-DECL` (declaration seat + admit-time check + supersession — Part 2) demonstrates firing via drill; the declaration verdict is observable in the ledger for a real refusal event. (b) `WS-BUILD-WATCH-RECONCILER` (Part 2 — named by Ruling 1) demonstrates firing via drill; the Watch reconciler produces a verdict shape per Canon 8 §14-§15 for a shared-record reconciliation event. Both drill outputs are retained in the ledger and cross-cited. **Only after both demonstrations fire** may the gate strip proceed via a Canon 3 §24 rule-change ceremony (5 steps including re-verified — see `WS-BUILD-CEREMONY-REVERIFY`). Until then: gate STANDS as a canon-compliant surface at Executive-Core HEAD. The strip event itself is a distinct future item, ledgered separately.
4. **QUALITY EVIDENCE.** Two drill records (one per prerequisite) in the ledger; parity-seat entries for the two new contracts (declaration verdict, Watch reconciler verdict) via `WS-WIRE-PARITY-EXTENSION`. Uncurated sample: at minimum one drill day covering each prerequisite. Calibration under Canon 3 §31 + Canon 8 §21.
5. **DEPENDENCIES.** **GATED BY `WS-BUILD-DECL` AND `WS-BUILD-WATCH-RECONCILER`** (both Part 2 BUILD items). Also depends on `WS-BUILD-CEREMONY-REVERIFY` (this Part 1) for the strip ceremony's re-verify step. Also `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (the gate itself), 0 new contracts on retain-phase (evidence is written to existing ledger + Watch mark register), 2 integration surfaces (declaration verdict input + Watch reconciler input). Reclassify to S when strip-phase-only.
7. **REVERSAL COST.** **Very low during retain phase** (gate is doing its stated work). **Very high if stripped prematurely** (before both demonstrations fire) — this is a Canon-1 §7.1 authority breach that ledgers append-only and cannot be un-written; every downstream Shield call taken with the gate down is a Canon-3 §6.1 violation. Ruling 1 IS the safeguard against premature strip.

---

# G. RETIRE items (4 concrete + 1 rename = 5)

Concrete RETIRE clusters cite Canon 1 §12/§13/§15 or Canon 5 §43 (no bypass path).

---

## WS-RETIRE-APP-TERRITORY

1. **WHAT.** Retire application-territory duplicates from the platform layer: Executive-Core `services/cohort/` (8 files) + `stripe_webhook.py` + `owner_digest.py` + `news_aggregator.py` + `first_login_password_set.py` + `platform_kb.py` + `backfill_shield_v1.py`. Component set: 15+ loose Executive-Core services (per `notes/retire_inventory.md`). Contract: none touched (retirement removes calls, no new contract). Record class: N/A (retiring writes, not new records). Task identity: `retire.app_territory.per_service`.
2. **CANON CLAUSES SATISFIED.** Canon 1 §12 (six services boundary); Canon 1 §13 (same boundary for every application); Canon 1 §15 (no commerce — verbatim: "will not know a buyer, a price, or an order").
3. **DEFINITION OF DONE.** Every named service either (a) moves to the application layer of Executive-Core-turned-application, OR (b) deletes on migration completion. Platform boundary contains none of the listed files. Canon 1 §12 "six-services boundary invariant" AST discipline holds (no application-territory import from platform code). Verification: prove-one-run for a platform request has zero call sites into the retired names.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped import discipline). Uncurated sample: full platform request log for a drill week; zero platform→app-territory imports. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** Executive-Core-as-application transition boundary — implicit; captured in fidelity ledger FL-P1-04 if not yet defined at the programme level.
6. **CREDIT COST CLASS.** M. Justification: 8+ components across the list, 0 new contracts (retirement, not creation), 1 integration surface (application-boundary discipline).
7. **REVERSAL COST.** Low for the platform (retirement is subtractive). For the application layer, un-retirement = restore the code from git; no data motion required (application state was never at the platform boundary).

---

## WS-RETIRE-XCUT-SECURITY

1. **WHAT.** Retire cross-cutting security duplicates: `services/csrf.py`, `rate_limit.py`, `rbac.py`, `security_headers.py`, `session_timeout.py`, `sentry_setup.py`, `privacy_wall.py`, `clamav_service.py` (Executive-Core; 8 files). Task identity: `retire.xcut_security.per_service`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §11 (the Shell — no bypass path); Canon 1 §7.1 (peer authorities); Canon 3 §30 (Enforcement Class — Watch territory).
3. **DEFINITION OF DONE.** Cross-cutting security lives ONCE — either at platform (its canon home) or at application; not duplicated across the boundary. Platform's own security surface passes Canon 5 §11 no-bypass invariant. Verification: AST discipline confirms no application-side rate-limiter/csrf/rbac call intercepts a platform request.
4. **QUALITY EVIDENCE.** Invariant class (AST discipline). Uncurated sample: full platform request log for a drill week; zero application-security interceptions. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** As `WS-RETIRE-APP-TERRITORY`.
6. **CREDIT COST CLASS.** M. Justification: 8 components (loose files), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Low.

---

## WS-RETIRE-FRONTEND-ARCHIVES

1. **WHAT.** Retire codebase-self-marked archives: `frontend/src/_archived/` (61 files), `frontend/src/_archived_legacy/`, `frontend/src/_archived_coverage_loss/`, and `frontend/src/website/` (34 files, marketing). Task identity: `retire.frontend_archives.per_directory`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §43 (no surface offers bypass/override); Canon 1 §12-§13 (marketing website is application/commercial territory).
3. **DEFINITION OF DONE.** Archived directories removed from platform frontend deployment. Marketing website continues at application-layer (or standalone). Canon 5 §43 no-bypass invariant confirmed by inventory: only Canon 5 §10 four-console surfaces + Canon 5 §40 five-pillar surfaces render.
4. **QUALITY EVIDENCE.** Inventory audit (surface-list) + invariant class (no-bypass at the router). Uncurated sample: full frontend surface list for the drill week; every rendered route maps to a Canon 5 anchor.
5. **DEPENDENCIES.** As `WS-RETIRE-APP-TERRITORY`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (frontend surface list), 0 new contracts.
7. **REVERSAL COST.** Very low (files are in git).

---

## WS-RETIRE-PROTOTYPE-DIVERGENCE

1. **WHAT.** Retire prototype-only surfaces that lack a Canon-5 anchor: `hrstuff` (Collab > HR Stuff), `datashield/reasoningshield/accessshield` naming, `compute` (Registry > Compute), `tasks` (WorkStudio > Task Manager), `mentions/emails/projects` (Collab). Task identity: `retire.prototype_divergence.per_surface`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §40 (fixed five-pillar taxonomy); Canon 5 §43 (no bypass); Canon 1 §13 (application territory).
3. **DEFINITION OF DONE.** Every prototype nav item that lacks a Canon 5 anchor is removed from the platform surface OR moved to application territory. Verification: canon-5 conformance audit shows 100% of platform nav items map to Canon 5 §40 pillars or §10 consoles.
4. **QUALITY EVIDENCE.** Inventory audit (nav-list vs Canon 5 anchors). Uncurated sample: full prototype nav list vs Canon 5 §10/§40 anchor list; delta = 0.
5. **DEPENDENCIES.** None (prototype is documentation/design only).
6. **CREDIT COST CLASS.** S. Justification: 1 component (prototype file), 0 new contracts.
7. **REVERSAL COST.** Zero (prototype-only).

---

## WS-RENAME-PROTOTYPE-TAXONOMY

1. **WHAT.** Rename prototype labels to Canon 5 §10/§40 taxonomy: `WorkStudio → Work`, `ThinkLab / Monitor → Lead pillar sub-applications`, `Trust Center → Compliance Console`, `Registry → Extraction Console child + Control Band`, `Build → Build pillar (add Studio + Learn)`, `3rd Party Apps → 3rd Party pillar with Integration Console + app catalogue`. Task identity: `rename.prototype_taxonomy.per_label`.
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §40 (five pillars); Canon 5 §41 (Control Band).
3. **DEFINITION OF DONE.** Every prototype label renamed per the table in `notes/retire_inventory.md`. Canon-5 conformance audit shows 100% label-canon alignment. Verification: inventory diff between prototype pre-rename and Canon 5 anchors returns zero mismatch.
4. **QUALITY EVIDENCE.** Inventory audit. Uncurated sample: prototype label list post-rename.
5. **DEPENDENCIES.** None.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts.
7. **REVERSAL COST.** Zero.

---

# H. MODIFY / PARTIAL items (4)

MODIFY / PARTIAL covers existing code that must be extended to close an operative-parameter gap the assessment classified PARTIAL.

---

## WS-BUILD-INDEPENDENCE-GATE

1. **WHAT.** Machine-checked reviewer-independence gate. Rows C2-012, C3-028, C7-D11 PARTIAL. Component: reviewer-selector code path (existing at Extraction-Akki; specific file to be identified via a focused read — fidelity-ledger FL-P1-05). Contract: reviewer-selection input envelope. Record class: `Independence.Verdict`. Task identity: `governance.independence_gate.per_selection`.
2. **CANON CLAUSES SATISFIED.** Canon 2 §12 (independence-rule machine-checked); Canon 3 §28 (reviewer-selector independence gate); Canon 7 §D11 (defect: independence hard-check).
3. **DEFINITION OF DONE.** Every reviewer selection passes an independence rule (Canon 3 §28) applied at machine speed; failing selections refuse with a canon-cited reason recorded in the ledger. Verification: drill with a deliberately-conflicted selector fixture triggers the refusal.
4. **QUALITY EVIDENCE.** Invariant class (independence rule at selector). Uncurated sample: 20 real reviewer selections across a drill week; independence rule fires as expected.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX`, `WS-WIRE-CRITIC-INTO-ANSWERING` (independence applies to critic reviewers), `WS-BUILD-RECORD-MATRIX` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components (selector + rule table), 1 new/changed contract (independence-verdict envelope), 2 integration surfaces.
7. **REVERSAL COST.** Low-medium. Reversal restores non-machine-checked selection — a Canon 3 §28 violation, ledgered forever.

---

## WS-BUILD-DELIVERABLE-ATTESTATIONS

1. **WHAT.** Contents / privacy / quality attestation surface uplift (rows C4-056..C4-060 PARTIAL). Component: delivery-attestation surface (needs specific file identification — fidelity-ledger FL-P1-06). Contract: `Deliverable.Attestation.v0`. Record class: `Deliverable.Attestation`. Task identity: `deliverable.attest.per_delivery`.
2. **CANON CLAUSES SATISFIED.** Canon 4 §50-§60 (contents/privacy/quality attestations at delivery).
3. **DEFINITION OF DONE.** Every deliverable carries a three-field attestation (contents / privacy / quality) rendered on the answer surface AND recorded to the ledger. Missing attestations fail closed. Verification: prove-one-run of one delivered answer shows the three attestations verbatim.
4. **QUALITY EVIDENCE.** Contract test (attestation shape) + drill (delivery drill). Uncurated sample: 20 real deliveries across a drill week; every one carries all three attestations.
5. **DEPENDENCIES.** `WS-WIRE-CRITIC-INTO-ANSWERING`, `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-ANSWER-CARD` (Part 2), `WS-BUILD-CLASS-CHIP-LIBRARY` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract (attestation envelope).
7. **REVERSAL COST.** Low. Reversal removes attestations from surfaces (Canon 4 §50 violation, ledgered).

---

## WS-BUILD-CEREMONY-REVERIFY

1. **WHAT.** Canon 3 §24 rule-change ceremony's 5th "re-verified" step (row C3-033 PARTIAL, added by Chunk-3 A.2). Component: `services/checker/rule_change_request.py` + `state_machine.py` (existing; add re-verify state). Contract: rule-change ceremony state-machine shape (frozen at `test_govern_g_g1_to_g_g8.py`). Record class: `Ceremony.RuleChange`. Task identity: `ceremony.rule_change.per_change`.
2. **CANON CLAUSES SATISFIED.** Canon 3 §24 (five-step ceremony: proposed → counter-signed → waited → applied → re-verified).
3. **DEFINITION OF DONE.** Every rule-change ceremony completes only after the 5th "re-verified" state is entered — a re-verification pack (Canon 3 §31 shape) fires against the applied rule and its Verdict is written to the ledger. Verification: drill with one full rule-change ceremony end-to-end; state-machine trace shows all five states.
4. **QUALITY EVIDENCE.** Invariant class (state-machine trace). Uncurated sample: every rule-change ceremony over a drill week completes with re-verify state. Calibration under Canon 3 §31 verification pack shape.
5. **DEPENDENCIES.** `WS-BUILD-VERIFICATION-RUNNER` (Part 2 — the re-verify runner surface), `WS-WIRE-LEDGER-MATRIX`. **Also gates `WS-CONTRADICTION-PURPOSE-GATE` strip ceremony.**
6. **CREDIT COST CLASS.** M. Justification: 1 component (checker), 1 changed contract (state-machine adds a state), 2 integration surfaces (ceremony + verification runner).
7. **REVERSAL COST.** Medium. Reversal drops the re-verify state — every ceremony landing during the reversal window carries a Canon-3 §24 partial completion (ledgered). No rule-change is un-applied by a state-machine reversal.

---

## WS-BUILD-STANDING-QUERY-SURFACE

1. **WHAT.** Standing queries surface for compliance-owner review (rows C7-029..C7-031 PARTIAL). Component: `services/checker/` or Compliance-Console standing-query path (specific file — fidelity-ledger FL-P1-07). Contract: `StandingQuery.Definition.v0`. Record class: `Compliance.StandingQuery`. Task identity: `compliance.standing_query.per_review`.
2. **CANON CLAUSES SATISFIED.** Canon 7 §29-§31 (standing queries for compliance owners).
3. **DEFINITION OF DONE.** Compliance owner can define, list, and execute standing queries against ledgered state; each execution records a `Compliance.StandingQuery` row. Verification: drill with a compliance owner running three standing queries over a drill week.
4. **QUALITY EVIDENCE.** Contract test (query shape). Uncurated sample: 20 standing-query executions across a drill week.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX`, `WS-BUILD-CONSOLE-COMPLIANCE` (Part 2).
6. **CREDIT COST CLASS.** M. Justification: 1-2 components (query definition + execution surface), 1 new contract (standing-query shape), 1 integration surface (ledger reader).
7. **REVERSAL COST.** Low. Reversal removes the surface; compliance owner reverts to ad hoc reads (Canon 7 §29 gap).

---

# Part-1 item count summary

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

# I. INTERFACE strategy (Ruling 3 / Instruction 02)

Per Instruction 02: Extraction-Akki's frontend is the DONOR. Every existing page/menu is either repurposed into the Admin surface's **tile-grid-plus-detail-card grammar** (as HARVEST or MODIFY) OR classified RETIRE with a reason. The Watch is the fourth tile-group of four tiles (`State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13), remains BUILD, watch-officer-role gated, sessions under Watch identity per Canon 9, **NEVER nested under Trust Center**.

Reference screenshot pending arrival in workspace — recorded on every interface item as **`FIXTURE CLEARED @ transcription grade — see `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13); `test_four_questions_topline_present` added to new-invariants list per Build Order 01 §3`**.

## I.1 Extraction-Akki frontend inventory (verified at HEAD b150c21)

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

## I.2 Menu-to-app mapping table (every existing page)

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

## I.3 Interface work items (Part 1, HARVEST/MODIFY)

Twelve items own the 44-page repurposing plus one shell-grammar item. All carry the `FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` cited; `test_four_questions_topline_present` on new-invariants list` field.

---

## WS-HARVEST-SHELL-GRAMMAR

1. **WHAT.** Repurpose Extraction-Akki's `CanonOSShellPage.jsx` + `design/AkkiShell.jsx` + `AkkiV4Shell.jsx` + `AkkiV4ShellLayout.jsx` + `MarkedOpenSlot.jsx` + `akkiv4_design_system.js` + `ratified_copy.js` as the tile-grid-plus-detail-card grammar host — the Admin-surface shell. Components: 7 shell primitives. Contract: shell layout contract (tile-grid + detail-card render pass). Record class: N/A (surface-only). Task identity: `interface.shell.tile_grid`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md`; `test_four_questions_topline_present` on new-invariants list.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §11 (The Shell — no bypass path); Canon 5 §10 (five consoles hosted per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §43 (no bypass path); Instruction 02 (tile-grid-plus-detail-card grammar).
3. **DEFINITION OF DONE.** Every page listed in §I.2 renders inside the shell as an app tile in one of four groups (Extraction / Compliance / Integration / Administration) OR the Watch fourth-group. No page bypasses the shell. Canon 5 §43 no-bypass invariant holds. Shell placement invariant test asserts each tile carries its group + canon identity metadata. Verification: nav audit — 100% of rendered routes carry `(tile, group, canon_identity)` triple.
4. **QUALITY EVIDENCE.** Invariant class (shell-placement gate) + inventory audit (nav-to-tile mapping). Uncurated sample: every route rendered during a drill day. Calibration under Canon 3 §31 + Canon 5 §43.
5. **DEPENDENCIES.** Reference screenshot (fixture pending — fidelity ledger FL-P1-14). No inward code dependencies (primitives are donor-ready).
6. **CREDIT COST CLASS.** L. Justification: 3+ components (7 shell primitives) AND a new register/console surface (the tile-grid grammar itself is the register).
7. **REVERSAL COST.** Medium. Reversal restores Extraction-Akki's V4Shell as-is (no grammar overlay); every tile falls back to standalone routing — a Canon-5 §11 partial-shell state (ledgered). Data untouched.

---

## WS-HARVEST-CONSOLE-EXTRACTION

1. **WHAT.** Repurpose Extraction-Akki `pages/registry/` (4 pages) + `pages/memory/MemoryHomePage.jsx`, `MemoryPlaneDetailPage.jsx` + `pages/use_data/UseDataWizardPage.jsx`, `UseDataVerdictPanel.jsx` into the Extraction Console tile-group. 8 pages harvested; each becomes an app tile in the Extraction Console tile-group. Contract: Extraction Console tile-list. Record class: `Console.Extraction.Registration`. Task identity: `interface.console.extraction`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §13-§14 (Extraction Registry Dashboard + Model Catalogue); Canon 5 §17 (Registry Administration — Estate Map); Canon 7 §19-§23 (Memory planes surface); Instruction 02 (tile grammar).
3. **DEFINITION OF DONE.** Extraction Console tile-group hosts 8 donor tiles with canon identity per §I.2 table. Model Catalogue tile appears as a BUILD-marked open slot per `WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE` (Part 2); Batch Board tile appears as BUILD-marked slot per `WS-BUILD-BATCH-BOARD-SURFACE`. Canon 5 §13-§17 operative parameters go green for the harvested tiles; open-slot tiles carry Canon 5 §9 dormant-state copy.
4. **QUALITY EVIDENCE.** Inventory audit (tile-list-to-canon-identity mapping) + invariant class (tile placement in group). Uncurated sample: every route under Extraction Console during a drill day. Calibration under Canon 5 §10 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending (FL-P1-14).
6. **CREDIT COST CLASS.** L. Justification: 8 pages (3+ components), new register/console surface (Extraction Console tile-group), 2 integration surfaces (shell + component library).
7. **REVERSAL COST.** Medium. Reversal restores standalone routes; group binding is metadata (reversible via matrix new-entry). No data changes.

---

## WS-HARVEST-CONSOLE-COMPLIANCE

1. **WHAT.** Repurpose `pages/prove/ProvePage.jsx`, `ProveWalkPage.jsx` + `pages/govern/GovernHomePage.jsx`, `GovernRetentionPage.jsx`, `GovernHoldsPage.jsx`, `GovernRefusalHealthPage.jsx`, `GovernEstateRulesPage.jsx` + `pages/commission_view/CommissionViewHomePage.jsx`, `CommissionRunDetailPage.jsx` into the Compliance Console tile-group. 9 pages. Also picks up `MemoryPlaneObservabilityPage.jsx` and `TraceReceiptPage.js` and `AuditTrailPage.js` via MODIFY (rehome — see FL-P1-08/09/12). Contract: Compliance Console tile-list. Record class: `Console.Compliance.Registration`. Task identity: `interface.console.compliance`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §22-§26 (Compliance Home, Prove-one-run, Retention & Rights, Rulebook, rule-on-paper flag); Canon 3 §33-§48 (prove-one-run export); Canon 6 §11-§13 (commissioning); Canon 3 §31 (verification packs).
3. **DEFINITION OF DONE.** Compliance Console tile-group hosts the 9 donor tiles + 3 rehomed MODIFY tiles (12 total). Rulebook read-back tile lives at Compliance Home (Canon 5 §25 says rulebook lives here, not Administration — hence `GovernEstateRulesPage.jsx` rehomes). `WS-BUILD-VERIFICATION-RUNNER`, `WS-BUILD-PROVE-ONE-RUN`, `WS-BUILD-RULEBOOK-SURFACE` (Part-2 BUILD items) surface here as BUILD-marked open slots per Canon 5 §9. Canon 5 §22-§26 operative parameters go green for harvested tiles.
4. **QUALITY EVIDENCE.** Inventory audit + invariant (tile placement). Uncurated sample: every Compliance-Console route during a drill day. Calibration under Canon 3 §31 + Canon 5 §22.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`, `WS-WIRE-REFUSAL-FAMILY` (for GovernRefusalHealthPage), `WS-BUILD-CEREMONY-REVERIFY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** L. Justification: 9-12 pages, new console tile-group, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

## WS-HARVEST-CONSOLE-INTEGRATION

1. **WHAT.** Repurpose `pages/connect/` (6 pages) + `pages/use_data/UseDataDeveloperSurfacePage.jsx` into the Integration Console tile-group. 7 pages. Contract: Integration Console tile-list. Record class: `Console.Integration.Registration`. Task identity: `interface.console.integration`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §26-§29 (Integration Console: Home + First-call + Administer + Dual-actor scoping); Canon 6 §3.1 (setup declarations).
3. **DEFINITION OF DONE.** Integration Console tile-group hosts 7 donor tiles. Every Canon 5 §26-§29 tile presents with its canon identity. `WS-BUILD-WEBHOOK` (Part-2 BUILD) surfaces here as BUILD-marked open slot. Canon 5 §26-§29 operative parameters go green.
4. **QUALITY EVIDENCE.** Inventory audit + invariant. Uncurated sample: every Integration-Console route. Calibration under Canon 3 §31 + Canon 5 §26.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** M. Justification: 7 pages but 1 component (integration tile-group) + 1 new integration surface (shell binding). Rounds to M rather than L because the group is smaller and its Canon-5 clause-set is compact.
7. **REVERSAL COST.** Low-medium.

---

## WS-HARVEST-CONSOLE-ADMINISTRATION

1. **WHAT.** Repurpose `pages/master_admin/` (4 pages) + `pages/team/` (4 pages) + `pages/govern/GovernPendingPage.jsx`, `GovernChangeRulePage.jsx`, `GovernRegistriesPage.jsx` into the Administration Console tile-group. 11 pages. Contract: Administration Console tile-list. Record class: `Console.Administration.Registration`. Task identity: `interface.console.administration`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §10 (five consoles per Build Order 01 §1 correction — FL-OQ-04 CLOSED); Canon 5 §31-§36 (Administration Home + Change-a-Rule + What-I've-Changed + Roles & Rights + Counter-Sign Duties + Verification-Runner surface); Canon 3 §24 (ceremony).
3. **DEFINITION OF DONE.** Administration Console tile-group hosts 11 donor tiles. GovernChangeRulePage and ChangeARulePage dedupe (FL-P1-13 rendering decision — one canonical tile). Canon 5 §31-§36 operative parameters go green. `WS-BUILD-VERIFICATION-RUNNER` (Part-2 BUILD) surfaces as BUILD-marked open slot.
4. **QUALITY EVIDENCE.** Inventory audit + invariant. Uncurated sample: every Administration-Console route. Calibration under Canon 3 §31 + Canon 5 §31.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`, `WS-HARVEST-COMPONENT-LIBRARY`, `WS-BUILD-CEREMONY-REVERIFY`, `WS-BUILD-INDEPENDENCE-GATE`. Reference screenshot pending.
6. **CREDIT COST CLASS.** L. Justification: 11 pages, new console tile-group, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

## WS-HARVEST-COMPONENT-LIBRARY

1. **WHAT.** Repurpose reusable atoms: `RetentionPostureBadge.jsx`, `CounterSignBanner.jsx`, `AuthDeniedNotice.js`, `EngineCard.js`, `LedgerTable.js`, `OuterGateReceiptInline.js`, `StatusBadge.js`, `TrustReceiptLink.js` (8 components). Task identity: `interface.component_library.share`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §43-§65 (shared component library — insufficient-measurement render + absence-as-state + shared visual system).
3. **DEFINITION OF DONE.** All 8 atoms available to every console tile-group as single-source-of-truth imports (`components/ui_spec_v1/index.js` shape). Canon 5 §43-§65 shared-visual-system parameter goes green. Verification: static test `test_shared_components_single_source.test.js` (existing) confirms no duplicated component definitions.
4. **QUALITY EVIDENCE.** Invariant class (shared-source gate — existing test extends). Uncurated sample: full component-import graph during drill day; import count of each atom outside the library = 0. Calibration under Canon 5 §43.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (library), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

## WS-HARVEST-CLASS-CHIP-LIBRARY

1. **WHAT.** Repurpose `ClassBadge.js` + `ResponseClassPanel.jsx` as the class-chip library. Rows C5-002, C5-003, C5-004 (previously BUILD; reclassified HARVEST). Task identity: `interface.class_chip.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §2-§4 (class chip inseparable from claim + grounding marker).
3. **DEFINITION OF DONE.** ClassBadge + ResponseClassPanel available as the sole render path for class chips across every answer surface. Canon 5 §2 "class chip inseparable from claim" invariant holds — existing test `gate1_class_inseparable.test.js` (present in `frontend/src/__tests__/ui_spec_v1/`) fires green.
4. **QUALITY EVIDENCE.** Invariant class (existing `gate1_class_inseparable.test.js`). Uncurated sample: every rendered answer surface during a drill day. Calibration under Canon 5 §2 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (2 files, single library), 0 new contracts.
7. **REVERSAL COST.** Very low.

---

## WS-HARVEST-REFUSAL-CARD

1. **WHAT.** Repurpose `RefusalCard.js` as the Canon 5 §9.2 refusal card render, wired to the refusal-family taxonomy via `WS-WIRE-REFUSAL-FAMILY`. Rows C5-005, C5-006, C5-007 (previously BUILD; reclassified HARVEST since the render component exists in Extraction-Akki). Task identity: `interface.refusal_card.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §9.2 (verbatim refusal card); Canon 1 §16 (refusal recorded, never dropped).
3. **DEFINITION OF DONE.** RefusalCard renders the verbatim card copy from the `memory_refusal_reasons.v0.json` taxonomy per `WS-WIRE-REFUSAL-FAMILY`. Canon 5 §9.2 verbatim-copy invariant holds — existing test `gate2_refusal_firstclass.test.js` (present at spine) fires green. `test_auth_denied_notice_not_refusal_card.test.js` (existing) ensures auth-denied stays out of the refusal card. Verification: prove-one-run for one refused request renders the taxonomy id + card copy identically.
4. **QUALITY EVIDENCE.** Invariant class (existing `gate2_refusal_firstclass.test.js`). Uncurated sample: every refusal impression during a drill day; card copy is byte-identical to taxonomy. Calibration under Canon 5 §9.2 + Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`, `WS-WIRE-REFUSAL-FAMILY`, `WS-HARVEST-TWO-PASS-AMENDMENT` (for the added Executive-Core refusal templates). Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component, 0 new contracts.
7. **REVERSAL COST.** Very low.

---

## WS-HARVEST-DORMANT-STATE

1. **WHAT.** Repurpose `ProveDormantPage.jsx` + `TeamDormantPage.jsx` as the Canon 5 §9 dormant-state render pattern. Row C5-009 (previously BUILD; reclassified HARVEST). Task identity: `interface.dormant_state.render`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 5 §9 (dormant state — "what would activate" statement per screen).
3. **DEFINITION OF DONE.** Every tile that has no activated state renders the dormant-state pattern from these two donor pages, with a Canon 5 §9 "what would activate" copy line. Verification: every BUILD-marked open slot on any console tile-group carries this pattern.
4. **QUALITY EVIDENCE.** Invariant class (dormant-state grammar test). Uncurated sample: every dormant tile impression during drill week. Calibration under Canon 5 §9.
5. **DEPENDENCIES.** `WS-HARVEST-COMPONENT-LIBRARY`, `WS-HARVEST-SHELL-GRAMMAR`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (dormant pattern), 0 new contracts.
7. **REVERSAL COST.** Very low.

---

## WS-MODIFY-PLANE-OBSERVABILITY

1. **WHAT.** MODIFY `MemoryPlaneObservabilityPage.jsx` to rehome from Extraction Console → Compliance Console (RENDERING DECISION FL-P1-08). Canon 7 §29-§31 standing queries + Canon 3 §31 prove-one-run belong at Compliance. Task identity: `interface.plane_observability.rehome`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 7 §29-§31 (standing queries for compliance owners); Canon 3 §31 (verification packs); Canon 5 §22 (Compliance Home).
3. **DEFINITION OF DONE.** Page appears under Compliance Console tile-group with its Canon-5 identity; not duplicated under Extraction Console. Standing-query wiring lands via `WS-BUILD-STANDING-QUERY-SURFACE`. Verification: nav audit confirms exactly one home for this tile.
4. **QUALITY EVIDENCE.** Inventory audit. Uncurated sample: nav-audit run. Calibration under Canon 5 §10.
5. **DEPENDENCIES.** `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-BUILD-STANDING-QUERY-SURFACE`. Reference screenshot pending.
6. **CREDIT COST CLASS.** S. Justification: 1 component (single page rehome), 0 new contracts, 1 integration surface.
7. **REVERSAL COST.** Very low.

---

## WS-MODIFY-PROVE-ONE-RUN-EXPORT

1. **WHAT.** MODIFY `TraceReceiptPage.js` to be the Canon 3 §33-§48 prove-one-run export tile under Compliance Console, wired to `WS-BUILD-PROVE-ONE-RUN` (Part-2 BUILD). Component: single page. Task identity: `interface.prove_one_run_export.per_pack`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 3 §33-§48 (export prove-one-run pack); Canon 5 §23 (Prove-one-run panel).
3. **DEFINITION OF DONE.** Trace-receipt page becomes the export surface for a prove-one-run pack; every export event ledgered under `Ceremony.ProveOneRun` record class (Part-2). Placement: Compliance Console. Verification: prove-one-run drill exports a pack via this page and the export event lands in ledger.
4. **QUALITY EVIDENCE.** Contract test (pack shape) + drill. Uncurated sample: drill exports over a drill week. Calibration under Canon 3 §31 + Canon 3 §33.
5. **DEPENDENCIES.** `WS-HARVEST-CONSOLE-COMPLIANCE`, `WS-BUILD-PROVE-ONE-RUN` (Part 2), `WS-WIRE-LEDGER-MATRIX`. Reference screenshot pending.
6. **CREDIT COST CLASS.** M. Justification: 1 component, 1 new contract (pack export event class), 1 integration surface.
7. **REVERSAL COST.** Low.

---

## WS-MODIFY-USE-DATA-PLACEMENT

1. **WHAT.** MODIFY `UseDataLandingPage.jsx` to resolve rendering decision FL-P1-10: Canon 5 §14 (Extraction Model Catalogue) OR Canon 5 §43 (Reference App — Ask). Component: single landing page. Task identity: `interface.use_data.placement_resolution`. **FIXTURE CLEARED @ transcription grade (BAC applied); rendering decision resolved per FL-P1-10 (Build Order 01 §2.C — Use-Data landing homes to the Ask reference application).**
2. **CANON CLAUSES SATISFIED.** Canon 5 §14 (Model Catalogue) OR Canon 5 §43-§44 (Reference App — Ask). Owner must rule.
3. **DEFINITION OF DONE.** UseDataLandingPage placed under Extraction Console (as Model Catalogue anchor) OR under Ask Reference App per owner ruling. Nav audit confirms exactly one home.
4. **QUALITY EVIDENCE.** Inventory audit + owner ruling ledgered in DECISIONS.md.
5. **DEPENDENCIES.** Owner ruling (fidelity ledger FL-P1-10). Reference screenshot pending.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Very low.

---

## WS-MODIFY-VERDICT-DEMO

1. **WHAT.** MODIFY `UseDataVerdictDemoPage.jsx` — determine whether it is a canon-required surface OR a demo-only artifact for retirement (RENDERING DECISION FL-P1-11). Component: single page. Task identity: `interface.verdict_demo.classification`. **FIXTURE CLEARED @ transcription grade — `fixtures/binding_acceptance_criteria.md` applied.**
2. **CANON CLAUSES SATISFIED.** Canon 4 §7 (verdict is matrix lookup) — question: does the demo satisfy any Canon-5 tile requirement? If yes, HARVEST as Extraction Console tile; if no, RETIRE.
3. **DEFINITION OF DONE.** Either placed under Extraction Console with Canon-5 identity OR RETIRE with reason ledgered in DECISIONS.md.
4. **QUALITY EVIDENCE.** Inventory audit; owner rendering-decision ledger entry.
5. **DEPENDENCIES.** Owner ruling (fidelity ledger FL-P1-11). Reference screenshot pending.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Zero (either path).

---

## WS-MODIFY-AUDIT-TRAIL-PLACEMENT

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

