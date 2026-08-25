# W7 Grounding Brief · Targeta · Model Ecosystem · Model Admission Ceremony

**Status**: PREP — assembled while W7 GO is with the owner. CP1 does not start until explicit "W7 go" is banked in `STATE/DECISIONS.md`.
**Anchor**: `notes/status_and_wave_plan.md` §Wave 7 · `notes/requirements_register_17docs.md` Docs 13/14 · `notes/canon_addendum_1_requirements.md` CA1-004/CA1-005/CA1-011.
**Re-baselined budget**: **~3520 LOC** (owner ruling 2026-08-25 · 1.60× calibration).
**Assessment repo HEAD at brief-authoring**: master @ `1f9d21a`. Extraction-Akki HEAD: `programme/track-a` @ `7db5a00` (W6 close).
**Predecessor pins the owner steered**: pydantic 2.13.4 load-bearing (backend/requirements.txt L4-L18); canonical-projection remediation is a **W8 opener**, not W7.

---

## 1 · Register rows grounded (Docs 13/14 + CA1 amendments)

### 1.1 · Doc 13 · Autonomous Training (Targeta) · 23 rows

**Canonical anchor**: Canon 4 §§20–22 (Targeta + Critic Seam + Independence rule). Extracted rows from `notes/canon_4_requirements.md` — verbatim IDs:

| Row ID | Canon anchor | Requirement (compressed) | Status per register |
|--------|--------------|--------------------------|---------------------|
| Doc13-001 | C4-014 (§11 Charter) | Targeta plans extraction — WHICH material, WHICH order, WHICH standards, WITHIN WHICH rights — against frozen objective | **REUSABLE** — RMS `services/targeta/` |
| Doc13-002 | C4-015 (§11 Objective-bound) | Targeta operates ONLY on frozen objectives (Doc 3 §5). Never plans against amending/drafting objective | **REUSABLE** — Northena's `FrozenArtifact` already refuses mutation (`a71ea67`) |
| Doc13-003 | C4-017 (§12 Reuse-first) | Targeta must identify reusable prior extractions before proposing new work. Non-reuse must state why | **REUSABLE** — plan.py yield-layer boundary |
| Doc13-004 | C4-021 (§16 S-A composition) | S-A composes: Northena + Mtafiti + Targeta + workers + SyniSense + Solva + rules | **REUSABLE** — northena + solva already live; Targeta service is next |
| Doc13-005 | C4-022 (§16 Terminus) | S-A ends in a FROZEN UNIT CONTRACT — deliverable contents, licence label, privacy attestation, quality card, proof trail bound + receipted | **BUILD** — the frozen-unit-contract shape is not in-tree |
| Doc13-006 | C4-026 (§18 Seam-1) | Frozen objective + declaration cross as whole artefact from Northena's admit row to Targeta's plan input. Registered handoff contract | **PARTIAL** — Northena admit exists; handoff contract to Targeta is BUILD |
| Doc13-007 | C4-029 (§20) | Workers execute extraction/annotation/verification/adapter-training under Targeta's plan and Northena's admit | **BUILD** — worker registry + F&P Registry (Doc 1 §8) |
| Doc13-008 | C4-030 (§20) | Worker output must carry manifest (Canon 2 §8) — every claim traces to source and states its evidence class | **BUILD** |
| Doc13-009 | C4-031 (§21 Critic Seam) | Critic Seam = standing quality layer on worker output; evaluates against registry-registered rubric | **BUILD** |
| Doc13-010 | C4-032 (§21) | Shipped output that has not passed Critic Seam is a defect; retroactive runs are re-verifications, not permission grants | **BUILD** |
| Doc13-011 | C4-033 (§22 Independence) | Critic Seam and target satisfy Solva-pattern independence (Doc 3 §18) — different base OR materially different context | **BUILD** — depends on Solva-pattern access which lives in W5 code |
| Doc13-012 | C4-034 (§23 Quarantine) | Worker output failing Critic Seam → QUARANTINE → Batch Board with status + resolution path; each resolution is a ledger event | **BUILD** — quarantine + Batch Board |
| Doc13-013 | C4-035 (§24) | Adapters train on labelled material; every trained adapter enters registry (Canon 5 §12.2) with base model, training lineage, inherited rights, scorecard, version history | **REUSABLE** — RMS `perception/model_registry.py` + `models_registry.v0.json` |
| Doc13-014 | C4-036 (§25) | Before any adapter exists for a given class, surface says so PLAINLY rather than empty error (Doc 6 §8) | **BUILD** — surface-side; honest-empty pattern already exists in Registry.jsx |
| Doc13-015 | C4-037 (§26 MOAC) | Every accepted adapter carries six-criterion Model Acceptance Card with real measured numbers | **BUILD** — six-criterion structure |
| Doc13-015a | C4-037a (§26.1) | MOAC.1 · Accuracy on tenant's uncurated measured composition (Doc 1 §4.10) | **BUILD** |
| Doc13-015b | C4-037b (§26.2) | MOAC.2 · Coverage across strata Mtafiti has measured | **BUILD** |
| Doc13-015c | C4-037c (§26.3) | MOAC.3 · Refusal behaviour under Solva-pattern (§17) — measured refuse-rate on out-of-scope prompts | **BUILD** |
| Doc13-015d | C4-037d (§26.4) | MOAC.4 · Provenance integrity of training data (Doc 1 §4.9) | **BUILD** |
| Doc13-015e | C4-037e (§26.5) | MOAC.5 · Cost per operation, measured on real load | **PARTIAL** — W6 CA1-008 Cost Ledger has cost quantities |
| Doc13-015f | C4-037f (§26.6) | MOAC.6 · Time to answer at 95th percentile, measured under platform load pattern | **BUILD** |
| Doc13-016 | C4-038 (§27) | MOAC evidence drawn from UNCURATED sample; curated benchmarks inadmissible | **BUILD** |
| Doc13-017 | C4-039 (§28 Rights lineage) | Every adapter carries full training lineage back to rights-held source. Unresolved lineage = defect, doesn't ship | **BUILD** |
| **Doc13-023 · CA1-011** | Addendum §2 CA1-011 | Standing re-check date per in-service model. Early failure → Watch (Doc 3) route | **SPLIT · Orchestrator ruling 2026-08-25T23:15Z** — W7 lands the re-check-date register + surfacing (Doc 13's letter). W9 lands the Watch-routed enforcement with a named seam. Enforcement half is NOT to be faked in W7; honest render on early failure ("Watch-route lands W9") |

### 1.2 · Doc 14 · Model Ecosystem · Baseline · Whitepaper · 28 rows

Canon 4 §§23–25 · Canon 6 §4. Selected representative rows (full register in `notes/requirements_register_17docs.md` §Doc 14):

| Row ID | Canon anchor | Requirement | Status |
|--------|--------------|-------------|--------|
| Doc14-001 | C4-075 (§32 Baseline curation) | Licence-verified baseline curation | **REUSABLE** — RMS `perception/models_registry.v0.json` seeded with `whisper-tiny` (SHA + license + origin URL) + `c1_candidates` for Qwen3/Llama/OCR/vision families |
| Doc14-023 · **CA1-004** | Addendum §1 CA1-004 (build-only closure) | Baseline line names licence-verified starting model per training run | **BUILD** — line surface + record class |
| Doc14-024 · **CA1-005** | Addendum §1 CA1-005 (build-only closure) | "Prepare white paper" action drafting from run artefacts (Promise #25 exceptional-run retention) | **BUILD** — Exec-Core `deck_generation_jobs.py` (208 LOC) / `deck_regenerate.py` (175) / `deck_lineage.py` (141) / `deck_retrieval.py` (129) are candidates but built for `Deck` (spreadsheet-analysis decks), NOT run-artefact whitepaper — reuse grade ADAPT-then-narrow, not LIFT |
| Doc14-026 | C4-090 (§39 One-license) | One-license reach across every LLM (Promise #30) | **REUSABLE** — LLM chokepoint (W5) already routes through Emergent universal key. Multi-LLM crossings under one licence surface is a naming layer, not a mechanism |

**Grounding gap flagged**: full 28-row expansion for Doc 14 needs a fresh pass through `notes/canon_4_requirements.md` §§23–25 during CP1 (roughly 15 more rows). Not front-loaded here to avoid speculation.

---

## 2 · Reuse pulls from the accessible repos

### 2.1 · RMS-IQ-Core-2 · `backend/services/targeta/` · LIFT candidate (425 LOC across 6 files)

Confirmed by direct file inspection:

| File | LOC | Role | Reuse grade |
|------|----:|------|-------------|
| `__init__.py` | 16 | package marker | LIFT |
| `core.py` | 78 | Deterministic eligibility + ranking. Hard-filter by floor; deterministic tie-break (relevance ↓, class_rank ↓, source_ref ↑). **Zero ML imports** (enforced by `test_core_has_no_ml_import`). | **LIFT** — matches Canon 4 §14 #1 "complete targeter by invariant" |
| `interface.py` | 97 | One-way set-preserving boundary. `EligibleCandidate` (carries floor + registry_defensibility internally) → `YieldCandidate` (excludes them by construction). `NonPermutationError` = TypeError, rejected not corrected (§10 verbatim). | **LIFT** — Canon-4 §10 boundary discipline is baked into the type |
| `plan.py` | 89 | Mining plan shape. Also lives in-tree at `Extraction-Akki/backend/contracts/targeta_plan.py` (68 LOC) with matching `targeta_mining_plan.contract_snapshot.json` under invariants — the plan CONTRACT is already lifted; the plan-generation SERVICE is next. | LIFT (contract already lifted) · **ADAPT** the service |
| `gate.py` | 109 | Two-arm gate: Arm 1 Helps + Arm 2 Coverage Veto. Veto overrides helps (§17 #6). Closed-seam pattern with `thresholds=None ⇒ closed`. | **LIFT** |
| `yield_layer.py` | 36 | Yield thresholds config. | **LIFT** |

**Reuse readiness**: HIGH. The `contracts/targeta_plan.py` port already happened in an earlier phase (68 LOC contract + snapshot on Extraction-Akki HEAD `7db5a00`). The service layer is a **direct LIFT** into `backend/services/targeta/` on `programme/track-a`, with minor import fix-ups (RMS uses `from contracts.five_rings import DefensibilityClass` — same import path as Extraction-Akki, so plausibly zero-friction).

**Companion test file**: RMS-IQ-Core-2 `backend/tests/invariants/test_targeta_invariants.py` (207 lines) — LIFT for the invariant baseline, then add W7-specific invariants (six-criterion MOAC shape, re-check date state).

### 2.2 · RMS-IQ-Core-2 · `backend/services/perception/model_registry.py` + `models_registry.v0.json` · LIFT candidate (114 LOC + 70-LOC JSON)

Verified by direct file inspection:

- **`model_registry.py`** (114 LOC): additive v(N)→v(N+1) registry versioning. Exposes `current_registry_version()`, `load_registry(kind)`, `attest_model(model_id)` (hard-fails if model not present), `register_model(model_id, entry)` (append-only). Owner ruling 9.2a-E1 α anchor is preserved in the module docstring.
- **`models_registry.v0.json`** (70 LOC): seeded with `whisper-tiny` CI fixture model (SHA-256, license, origin URL, HF snapshot revision) + `c1_candidates` for Qwen3, Llama, document-OCR, vision families. Each `c1_candidate` carries `class`, `family`, `modality`, `role`, `license`, `license_verification_url`, `checksum_policy`.

**Reuse readiness**: HIGH. This is the fabric for:
- **CA1-004 baseline line** (Doc14-023): the `models_registry.v0.json` schema already models `license` + `license_verification_url` + `origin_url` + `weights_sha256` — a baseline row IS a model registry entry with `role: baseline_at_run:<run_id>`. Additive v(N)→v(N+1) semantics let each training run bump the registry without mutating history.
- **CA1-011 standing re-check date** (Doc13-023): add a `re_check_due_at` field per in-service model + a scheduler that fires the six MOAC criteria on that cadence. Watch route (early-failure escalation) is DEFERRED to W9 per opener plan; without Watch, the re-check state is honestly rendered as "re-check due <date>" + "last re-check: <outcome>" with no auto-escalation path yet.

**Test companion**: none in-tree (RMS test file appears specific to whisper-tiny seed). Tests-first for the additive-versioning invariants + license-verification-required invariants + `attest_model` refusal grammar.

### 2.3 · Akki-Executive-Core · `backend/services/sandbox_generation.py` · 508 LOC · **REJECT for W7**

**Direct inspection verdict**: 508 LOC of Phase-J visitor-form-oriented Claude Sonnet 4.5 generation with 24h TTL persistence. Focused on generating 8 fictional working-session artefacts from a 7-question intake — **not on model acceptance ceremony**. Reuse map (§1 row `Model Admission ceremony`) tagged it ADAPT, but on inspection the shape is misaligned with the MOAC six-criterion structure. **Do NOT lift; build MOAC tests-first from Canon 4 §26 verbatim.**

### 2.4 · Akki-Executive-Core · `backend/services/analysis_lifecycle.py` · 443 LOC · **REJECT for W7**

**Direct inspection verdict**: Track-A Phase-1 analysis lifecycle for a spreadsheet `Analysis` entity — create/session-close/blob-purge. GridFS migration semantics. **Not baseline curation**; the reuse map §1 row was optimistic. Do not lift.

### 2.5 · Akki-Executive-Core · `backend/services/deck_*.py` · 653 LOC across 4 files · **ADAPT-then-narrow for CA1-005 (Whitepaper)**

Files verified by `wc -l`:
- `deck_generation_jobs.py` (208 LOC) — async deck generation job orchestration
- `deck_lineage.py` (141) — lineage tracking
- `deck_regenerate.py` (175) — regeneration path
- `deck_retrieval.py` (129) — retrieval / read-side

**Fit**: shape is "generate a `Deck` output artefact with lineage + regenerate + retrieve". CA1-005 says "Prepare white paper action drafting from run artefacts". Shape overlap is real but the Deck domain (spreadsheet-analysis decks) differs from run-artefact whitepapers. **Reuse grade: ADAPT-then-narrow** — pull the lineage + async-generation structure, narrow the output artefact to a whitepaper shape anchored on run receipts, drop the deck-specific templating.

**Do NOT front-load the LOC into the W7 budget**; if CP4 (CA1-005 whitepaper) can honestly ADAPT these files in <150 LOC, it lands in W7; otherwise defer the WP artefact generation surface to W8.

### 2.6 · Akki-Executive-Final · `backend/services/solva/` · **NOT for W7**

Reuse map §5 confirmed: cleaner Solver package than Core (`solva/reasoning/candidate_generation.py` 361 LOC + `frame_audit_engine.py` 253 + `probability_weighting.py` 233 + `refusal_logic.py` 229 + `situation_class_classifier.py` 160 + `tension_detection.py` 213 + `triangulation_engine.py` 174 = 1623 LOC in the reasoning/ subdir). **This is a W5-territory adaptation source; not the W7 focus.** Solva stages 4-6 mechanism-side already adapted in W6 CP4 (`d9ae4a5`).

---

## 3 · Provisional CP plan (subject to CP1 rulings + LOC accounting)

Not scheduling — grounding what each CP will lean on. Order is by dependency, not commitment.

| CP | Scope | Reuse source | Est. LOC (pre-cal.) |
|----|-------|--------------|--------------------:|
| CP1 | Rulings + brief close + rates register for training-run economics · **rate rows for adapter training + MOAC measurement passes** | Extends W6 rates_register with training-run rates | ~150 |
| CP2 | **Targeta service lift** (`services/targeta/{core,interface,plan,gate,yield_layer}.py`) with import fix-ups + tests-first for invariants | RMS `services/targeta/` (425 LOC · LIFT) + RMS `tests/invariants/test_targeta_invariants.py` (207 LOC · adapt) | ~500 |
| CP3 | **Model registry service lift** (`services/model_registry/`) + additive v(N)→v(N+1) versioning + `attest_model` hard-fail + `register_model` append-only + honest render on empty class | RMS `perception/model_registry.py` (114 LOC · LIFT) + `models_registry.v0.json` (70 LOC · LIFT · re-seed under W7 anchor) | ~350 |
| CP4 | **Model Admission ceremony backend** — six-criterion MOAC state machine · uncurated-sample evidence rule · rights-lineage-required-to-ship rule · quarantine + Batch Board records | BUILD, tests-first from Canon 4 §26 verbatim | ~700 |
| CP5 | **CA1-004 baseline line** + **CA1-011 re-check state** (Watch route DEFERRED to W9) + registry v(N)→v(N+1) bump path for baseline/re-check events | Extends CP3 registry | ~400 |
| CP6 | **CA1-005 whitepaper action** — ADAPT `deck_*.py` lineage + async-generation structure, narrow to whitepaper artefact; if >150 LOC of adaptation is needed, DEFER to W8 | Exec-Core `deck_*.py` (653 LOC across 4 files · ADAPT-then-narrow) | ~250 or DEFER |
| CP7 | **W6 deferrals folded in**: Data Suite surface (v7-exact) + LLM chip UI polish + fill W7 UI wiring (Model Ecosystem surface tabs: Baseline · Ecosystem · Admission) | Extends W6 Cost Ledger surface pattern + Registry.jsx `KV`/`FQ`/`StatGrid` primitives + honest-empty class 40 · Registry.jsx pattern | ~700 |
| CP8 | **Wave close** — cohort assembly per FL-P4-W4-01 discipline + STATE + screenshots + close report | — | ~50 |
| **Estimate total (pre-calibration)** |  |  | **~3100** |
| **Est. total × 1.60× calibration** |  |  | **~3520** (matches re-baseline) |

**Two guard checkpoints wired in**:
- **CP4 stop-and-report**: if MOAC state-machine LOC exceeds 700, halt CP4 and surface options (narrow to structural + defer measurement pass to W8) rather than eat the budget.
- **CP6 fork**: whitepaper ADAPT gets a hard 150-LOC lid; overrun → immediate defer to W8, no scope-shaving of CP4/CP5.

---

## 4 · Dependencies and cross-wave couplings

- **Watch mechanism (Doc 3)** is not landing until **W9**. **CA1-011 SPLIT** per Orchestrator ruling 2026-08-25T23:15Z: W7 lands the re-check-date register + surfacing (Doc 13's letter — per-model `re_check_due_at` visible on the MOAC six-criterion cadence). W9 lands the Watch-routed enforcement with a **named seam** so the connection point is on record from W7. **Do NOT fake the enforcement half in W7.** On early failure inside W7, surface renders honest state ("early failure · Watch-route lands W9") — same reference-not-copy posture as W6 CP4's Grey Mirror groundwork.
- **Solva-pattern independence check** (C4-033/Doc13-011) leans on Solva primitives already in-tree from W5/W6 CP4. No new W7 code needed for the independence primitive itself; W7 wires it into the Critic Seam.
- **Rights lineage** (C4-039/Doc13-017) leans on the northena ledger row shape (in-tree since W4) + registry attest_model semantics (CP3 above).
- **Frozen objective** (C4-015/Doc13-002) leans on the Northena `FrozenArtifact` class (in-tree since `a71ea67`).
- **Cost Ledger cost-per-op measurement** (MOAC.5 / C4-037e) leans on W6's `services/cost_ledger/` (in-tree since `d7ff88e`). Extends by adding an "adapter-training-run" ledger kind.
- **Pydantic 2.13.4 pin** (W6 opener finding): CP3 model registry + CP4 MOAC state machine will emit new frozen contracts. **Every new contract MUST land with (a) snapshot + (b) `CONTRACT_TO_SNAPSHOT` map entry + (c) `parity_at_N` count bump in the SAME commit** per the W6-ratified DoD.

---

## 5 · Load-bearing rulings from W6 close carried into W7

- **Pydantic 2.13.4 pin** logged as load-bearing in `Extraction-Akki/backend/requirements.txt` (comment L4–L18) — an environment rebuild that silently moves the version will fail the frozen cohort. Fidelity ledger rows FL-P4-W6-01/03/04/05/06/07 name the drift class.
- **Definition-of-done addition** effective W7 onward: any commit touching `contracts/*.py` emitting a pydantic BaseModel OR adding a `*.contract_snapshot.json` MUST touch snapshot AND `CONTRACT_TO_SNAPSHOT` AND `parity_at_N` count in the SAME commit (FL-P4-W6-02/08/09 process finding).
- **Canonical-projection remediation** is a **W8 opener**, not W7 — right before W8's governance ceremony wave, which mints the most new contracts.
- **Owner ruling on overrun** (2026-08-25): 15% W6 overrun accepted; **W7 is NOT narrowed to absorb**. Stop-and-report at 3520-LOC line is the control.

---

## 6 · Non-goals for W7 (explicit)

- **Watch mechanism** (Doc 3 · CA1-006 · CA1-012) — W9. CA1-011 Watch route lands in W9, not W7.
- **Governance ceremony wizard** (Doc 15 · CA1-009 generalised handoff) — W8.
- **N-series primitives** (CA1-N2 breach · CA1-N3 erasure · CA1-N5 continuity) — W8/W9.
- **Grey Mirror overview surface** — W9 (mechanism-side already in `d9ae4a5`; surface waits for Watch).
- **Canonical-projection pydantic remediation** — W8 opener.
- **CA1-005 whitepaper if ADAPT exceeds 150 LOC** — defer to W8 rather than eat budget.

---

## 7 · Open questions surfaced during grounding · ALL RESOLVED · CP1 rulings on record

**Q1 · CA1-011 route disposition** · **RESOLVED · Orchestrator ruling 2026-08-25T23:15Z**. SPLIT: W7 lands re-check-date register + surfacing (Doc 13's letter). W9 lands Watch-routed enforcement with a **named seam** on record from W7. Do NOT fake the enforcement half; honest render on early failure. Folded into §1.1 (Doc13-023) and §4 (dependencies).

**Q2 · MOAC uncurated-sample evidence source** · **RESOLVED · Owner ruling 2026-08-25T23:30Z (W7 GO)**. REUSE Registry census facts (the real connected estate — 235 tables' structural facts + crossing receipts) as uncurated sample where the register's letter permits. Fresh pass over actual records requires a **named purpose** + **structure-only posture** honored (chokepoint discipline). If Doc 13's letter genuinely requires record-contents sampling for which no purpose is on record, **NAME THE GAP** rather than sampling anyway. Applies to CP4 MOAC.1 (accuracy on uncurated composition) and MOAC.2 (coverage across strata Mtafiti measured).

**Q3 · Model registry namespace** · **RESOLVED · Owner ruling 2026-08-25T23:30Z (W7 GO)**. `services/model_registry/` as first-class top-level package. LIFT the RMS-IQ-Core-2 `services/perception/model_registry.py` + `models_registry.v0.json` fabric INTO this namespace; the perception mirror stays donor-side. Consistent with chokepoint/solva/northena landing pattern. **Seed policy**: registry seeds from FACTS only — the Emergent Universal LLM connection is real (already on record at W5). **whisper-tiny is NOT seeded** unless actually available on this estate; it stayed a donor-side CI fixture. Only real models on record.

**Q4 · CA1-005 whitepaper reuse grade** · **RESOLVED · Owner ruling 2026-08-25T23:30Z (W7 GO)**. 150-LOC hard lid stands. On overrun, W8-defer with a named gap in the W7 close report. Honest gate — no heroics. Applies to CP6 only.

---

## 8 · CP1 kickoff checklist (when owner "W7 go" lands)

1. Bank the "W7 go" ruling in `STATE/DECISIONS.md` (verbatim).
2. Open `notes/w7_brief.md` (CP1 checkpoint brief) with the full 23-row Doc 13 + 28-row Doc 14 register expansion grounded verbatim from `canon_4_requirements.md` — front-load the row IDs so CP2–CP8 target them explicitly.
3. Author the training-run rates register rows under `phase0/rates_register/training/` (owner-supplied or honestly absent).
4. Right-reason failure receipt for CP2 (targeta invariants + import path adaptation) BEFORE any lift.
5. Local-only commits on `programme/track-a`; no push.

Holding on owner steer.
