# Requirements Master Register · 20 Documents · CP7 additive expansion

**Owner Ruling 2026-08-19 §6 · additive-only correction discipline.** This
file layers Docs 17, 18, 19 on top of the 17-doc register
(`notes/requirements_register_17docs.md`, 515 rows, preserved verbatim).
Nothing in the prior file is edited; the new 36 rows land as a strict
addition, so any downstream code referencing the 17-doc register still
resolves.

## Method

- Row IDs follow the same `DocNN-###` convention. Doc 19 splits into
  `Doc19A-###` (Critic Seam · Part A) and `Doc19B-###` (Evidence
  Protocol · Part B) because the doc itself divides into two named
  parts with distinct governance classes (CANON vs PROPOSED).
- Status class per row: **CANON** (Owner-ratified · load-bearing on
  build) · **RULED** (Owner ruling in place, mechanism follows) ·
  **PROPOSED** (drafted · awaiting Owner ratification before mechanism
  lands) · **OPEN** (Owner-input still needed).
- Build-status per row: **DONE** · **PARTIAL** · **REUSABLE** · **BUILD**
  · **OPEN-SLOT** (same grammar as the 17-doc register).
- Carrying-phase pointer names which CP moves the row (per Owner R4
  registry-carrying-phase discipline).

## Row-count table · Docs 17-19 delta

| Doc | Title | Anchor(s) | CANON | RULED | PROPOSED | OPEN | Total |
|----:|-------|-----------|------:|------:|---------:|-----:|-----:|
| 17 | Multidimensional Training Engine | Doc 17 §§1-9 · Doc 17 briefing §§1-8 · Training Techniques Spec v1.0 T-1..T-4 · Canon 4 §26-§33 | 11 | 0 | 0 | 6 | 17 |
| 18 | Callable Skill Files (Promise #33) | Doc 18 §§1-8 · Business Continuity Requirements §3.7 annex | 6 | 0 | 1 | 1 | 8 |
| 19A | QA & Evidence Integrity · Part A (Critic Seam) | Doc 19 §A · Critic Seam Spec v1.0 §5-§9 · Transformation Quality Spec §7 | 6 | 0 | 0 | 0 | 6 |
| 19B | QA & Evidence Integrity · Part B (Evidence Protocol) | Doc 19 §B · Critic Seam Spec v1.1 (Part B pointer) | 0 | 0 | 4 | 1 | 5 |
| **Delta** | | | **23** | **0** | **5** | **8** | **36** |

**Register total: 515 + 36 = 551 rows.**

Composite % preview against the new denominator is recomputed
authoritatively at W11 CP9; the additive-only landing here does NOT
touch the 17-doc totals.

## Doc 17 · Multidimensional Training Engine · 17 rows

Umbrella canon: Doc 17 §§1-9 + Doc 17 briefing (Incremental Training &
Capacity, `canon/text/Akki_OS_Incremental_Training_Capacity_Briefing.txt`) +
Training Techniques Spec v1.0 (`canon/text/Akki_Training_Techniques_Spec.txt`,
Owner-ratified 2026-07-17) + Canon 4 §26-§33 (baseline / MOAC lineage).

- **Doc17-001** ← A17.1 · Target Outcome schema IS the training contract; every
  run references one; the compile stage rejects an Outcome without an existing
  `test_set_ref` and without per-stratum acceptance. Status CANON · Build BUILD ·
  Carrying phase CP5 (recipe seat + Objective Wizard integration).
- **Doc17-002** ← A17.2 · Training seat starts EMPTY. No default recipe · no
  default optimizer · fills at first run (T-1.2). Status CANON · Build BUILD ·
  Carrying phase CP5.
- **Doc17-003** ← A17.3 · Every trained model's registry entry cites a
  `recipe_version`; MOAC M-d lineage extends by this field (T-1.3). Status
  CANON · Build BUILD · Carrying phase CP5.
- **Doc17-004** ← A17.4 · Optimizer selection is a two-arm measured
  comparison; Muon is the first named candidate; the adopt/reject decision is
  an Owner ruling on measured results (T-2). Status CANON · Build BUILD ·
  Carrying phase CP5 (shape) + CP8 (real arm).
- **Doc17-005** ← A17.5 · Demand Table computed at compile · per-stratum B/I/E
  · admissibility requires a `named_failure` per scheme. Status CANON ·
  Build **DONE** · Carrying phase **CP3** (`backend/services/training/demand_table.py`
  in Extraction-Akki@a85774a).
- **Doc17-006** ← A17.6 · Capacity Ledger holds per-scheme measured level with
  provenance day-one; state grammar `building | held | saturated`. Status
  CANON · Build **PARTIAL** · Carrying phase **CP3** (record + read view in
  Extraction-Akki@a85774a; marginal-gain writer deferred to CP8).
- **Doc17-007** ← A17.7 · Capacity Probe at Sampling & Reflection reads the
  ledger · probes selectively · writes marginal-gain. Status CANON ·
  Build **PARTIAL** (stub · records-surface only) · Carrying phase **CP3 → CP8**
  (execution).
- **Doc17-008** ← A17.8 · Gap-shaped staged plans: stage gates enforce
  no-regression against earlier-stage test sets before the next stage opens.
  Status CANON · Build BUILD · Carrying phase CP5 (planner core) + CP8
  (execution).
- **Doc17-009** ← A17.9 · `PERCEPTION_EXECUTION_MODE={cpu,gpu}` at import-time ·
  silent fallback prohibited. Status CANON · Build **DONE** (already on disk in
  Extraction-Akki `backend/services/perception/gpu_execution/cuda_runtime.py`) ·
  Carrying phase: prior wave (Owner ruling 9.2a-E2 α).
- **Doc17-010** ← A17.10 · `models_registry.v0.json` seeds with the whisper-tiny
  CI fixture; production models land additively at 9.2b via v0→v1 registry
  bump. Status CANON · Build **DONE** (already on disk in Extraction-Akki
  `backend/services/perception/models_registry.v0.json`) · Carrying phase:
  prior wave.
- **Doc17-011** ← A17.11 · Test set precedes training · D-7 uncurated held-out
  sample sealed at Objective Wizard compile · verdict-curation forbidden.
  Status CANON · Build **DONE** · Carrying phase **CP3** (test-set-seal in
  Extraction-Akki@a85774a · fresh DigiCow verification landed at commit
  3e99be2 on 2026-08-26 with seal succeeding on freshly verified rows).
- **Doc17-012** ← A17.12 · Taxonomy graduation sign-off · which product role
  admits a new scheme to the shared taxonomy. Status OPEN · Build OPEN-SLOT ·
  Carrying phase: Owner ruling pending (non-blocking to trainer scaffolding).
- **Doc17-013** ← A17.13 · Probe-selectivity threshold · confirm or adjust the
  proposed default (per-stratum resolution for strata flagged I=1 + strata the
  objective's acceptance gates on). Status OPEN · Build OPEN-SLOT · Carrying
  phase: Owner ruling pending.
- **Doc17-014** ← A17.14 · Validation gating: whether §8 (three-arm experiment)
  must complete before staged plans run on customer commissions, or in
  parallel. Status OPEN · Build OPEN-SLOT · Carrying phase: Owner ruling
  pending.
- **Doc17-015** ← A17.15 · Interference weighting trigger: when to promote I
  from binary to weighted; proposed default is calibration data showing
  misleading strata consistently cost more than one unit of capacity.
  Status OPEN · Build OPEN-SLOT · Carrying phase: Owner ruling pending.
- **Doc17-016** ← A17.16 · Saturation cross-tenant policy: cross-commission
  transfer + common substrates + tenant boundaries. Currently deferred until
  marginal-gain data exists to inform it. Status OPEN · Build OPEN-SLOT ·
  Carrying phase: post-CP8 Owner ruling.
- **Doc17-017** ← A17.17 · Doc 17 miscellaneous open items (residual). Status
  OPEN · Build OPEN-SLOT · Carrying phase: Owner brief.

## Doc 18 · Callable Skill Files (Promise #33) · 8 rows

Umbrella canon: Doc 18 §§1-8 + Business Continuity Requirements §3.7 annex.

- **Doc18-001** ← A18.1 · Callable skill provisioning contract (frozen ·
  `extra=forbid` · slice bound at freeze · "new slice = new skill"). Status
  CANON · Build **DONE** (already on disk in Extraction-Akki
  `backend/contracts/callable_skill_provisioning_v0.py` + snapshot).
- **Doc18-002** ← A18.2 · Per-call inner gate · identity + scope + floor checks
  on every invocation. Status CANON · Build **DONE**
  (`backend/services/transform_forms/callable_skill_gate.py`).
- **Doc18-003** ← A18.3 · Every response carries a defensibility class inline
  (`SUBSTANTIATED / GROUNDED / SPECULATIVE`). Status CANON · Build **DONE**
  (integrated into the gate).
- **Doc18-004** ← A18.4 · Write-once persistence · revocation lands in the
  record · never mutates prior state. Status CANON · Build **DONE**
  (`backend/services/transform_forms/callable_skill_persistence.py`).
- **Doc18-005** ← A18.5 · Endpoint path bound at provisioning · skill callable
  only through the exact declared path. Status CANON · Build **DONE** (part of
  provisioning contract).
- **Doc18-006** ← A18.6 · Single-shot pilot for enterprise sales; Owner
  ratifies before deployment. Status PROPOSED · Build **PROPOSED** · Carrying
  phase: **Owner ratification** (deferred to post-W11 per Owner CP3-open
  deprioritization: "defer A18.6 async delivery entirely").
- **Doc18-007** ← A18.7 · Every skill's provenance chain traces back to the
  training run that produced its adapter (extends Doc14-016 rights-lineage +
  Doc14-017 version-history). Status CANON · Build BUILD · Carrying phase
  **CP4** (extension of `callable_skill_persistence.py` to fire on MOAC
  admission).
- **Doc18-008** ← A18.8 · Audit cadence for provisioned skills. Status OPEN ·
  Build OPEN-SLOT · Carrying phase: Owner ruling pending.

## Doc 19 · QA & Evidence Integrity · Part A · Critic Seam · 6 rows

Umbrella canon: Doc 19 §A (Critic Seam) + Critic Seam Spec v1.0 §5-§9 +
Transformation Quality Spec §7 (QA-7 custody boundary).

**LIFT source**: Akki-OS-V1 `backend/services/critic_pass/` · 950 LOC ·
Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md`
(SHA `42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a`
byte-identical). All six rows landed as DONE via CP2 LIFT
(Extraction-Akki@feec2a5).

- **Doc19A-001** ← QA-1 · The Critic Seam detects and never decides
  (findings only · no override / veto / final-say authority for any
  collection of models). Status CANON · Build **DONE** · Carrying phase
  **CP2** (`backend/services/critic_pass/harness.py`).
- **Doc19A-002** ← QA-2 · Three-tier layer: Tier 1 deterministic checks ·
  Tier 2 independent critic model · Tier 3 human calibration with seeded
  defect audits. Status CANON · Build **DONE** · Carrying phase **CP2**
  (harness + seeded_defect_corpus + calibration_ledger).
- **Doc19A-003** ← QA-3 · Independence — critic and target must differ
  (different base OR materially different context shape); self-review
  refused with `ValueError('QA-3 violation')`. Status CANON · Build
  **DONE** · Carrying phase **CP2** (harness `run_critic_pass` +
  rubric.apply_rubric).
- **Doc19A-004** ← QA-4 · Rubric-driven with named failure classes
  (CR-1..CR-7); rubric versions ledgered. Status CANON · Build **DONE** ·
  Carrying phase **CP2** (rubric.py TIER_2_RUBRIC).
- **Doc19A-005** ← QA-5 · Every worker output passes through the Critic
  Seam; shipped-without-seam is a defect (extends Doc14-002/003). Status
  CANON · Build **DONE** · Carrying phase **CP2** (manifest_gate.py hard-fail
  gate for verdict submission).
- **Doc19A-006** ← QA-6 · Ensemble critics permitted only when Tier-3
  audits show single-critic below bar on any fall class across two
  consecutive audits (T-3 protocol). Status CANON · Build **DONE** ·
  Carrying phase **CP2** (calibration_ledger + seeded_defect_corpus
  discipline).

## Doc 19 · QA & Evidence Integrity · Part B · Evidence Protocol · 5 rows

Umbrella canon: Doc 19 §B + Critic Seam Spec v1.1 (Part B pointer).

All five rows are PROPOSED (Owner ratification pending) or OPEN. This
part lands mechanism-side at **CP6** (Evidence Protocol PROPOSED
harness) per the W11 plan.

- **Doc19B-001** ← EP-1 · Evidence register records every measurement
  with its evidence class (FACT / NORM / DEFAULT). Status PROPOSED ·
  Build **PROPOSED** · Carrying phase **CP6**.
- **Doc19B-002** ← EP-2 · Dual-judge protocol for evaluation blinding
  (D-7 uncurated verdict samples). Status PROPOSED · Build **PROPOSED**
  · Carrying phase **CP6**.
- **Doc19B-003** ← EP-3 · Verdict samples are ENGINEERED; evaluation
  SAMPLES are NEVER curated. Status PROPOSED · Build **PROPOSED** ·
  Carrying phase **CP6**.
- **Doc19B-004** ← EP-4 · Ordering constraint on evidence-class
  transitions (whether DEFAULT can promote to NORM without a bounded
  observation window). Status OPEN · Build OPEN-SLOT · Carrying phase:
  Owner ruling pending.
- **Doc19B-005** ← EP-5 · Evidence class attaches inline to every claim
  on every surface (per Doc 18 A18.3 · same discipline). Status
  PROPOSED · Build **PROPOSED** · Carrying phase **CP6**.

## Build-status counts (Docs 17-19 only)

| Status | Doc17 | Doc18 | Doc19A | Doc19B | Total |
|--------|------:|------:|-------:|-------:|-----:|
| DONE   | 3     | 5     | 6      | 0      | **14** |
| PARTIAL | 2    | 0     | 0      | 0      | **2** |
| BUILD  | 6     | 1     | 0      | 0      | **7** |
| PROPOSED | 0   | 1     | 0      | 4      | **5** |
| OPEN-SLOT | 6  | 1     | 0      | 1      | **8** |

Bucket shares (new-36): DONE 39 % · PARTIAL 6 % · BUILD 19 % ·
PROPOSED 14 % · OPEN-SLOT 22 %.

## Carrying-phase pointers

| CP | Rows carried this phase |
|----|-------------------------|
| CP2 (Critic Seam LIFT · Extraction-Akki@feec2a5) | Doc19A-001..006 (6 rows) |
| CP3 (Training core · Extraction-Akki@a85774a + interleave 3e99be2) | Doc17-005, Doc17-006 (partial), Doc17-007 (partial), Doc17-011 (4 rows) |
| CP4 (Doc 18 provenance chain + Skill Files surface) | Doc18-007 (1 row) |
| CP5 (recipe seat + optimizer harness shape) | Doc17-001, Doc17-002, Doc17-003, Doc17-004, Doc17-008 (5 rows) |
| CP6 (Evidence Protocol PROPOSED) | Doc19B-001, Doc19B-002, Doc19B-003, Doc19B-005 (4 rows) |
| CP8 (real trainer · real optimizer arm · marginal-gain writer) | Doc17-006 completion, Doc17-007 completion, Doc17-004 real-arm, Doc17-008 execution |
| Owner rulings (non-carrying) | Doc17-012..017, Doc18-006, Doc18-008, Doc19B-004 |

## Composite % impact

Adding 36 new register rows to the mechanism corpus grows the denominator
from **515 to 551**. The 17-doc register composite at W10 close was **52.49 %**
(280.4 / 515). This CP7 landing:
- adds 14 net DONE rows (equivalent to +14 weight if unweighted)
- adds 2 PARTIAL rows (equivalent to +1 weight at PARTIAL=0.5)
- adds 7 BUILD, 5 PROPOSED (weight 0), 8 OPEN-SLOT (weight 0)

Preview composite ≈ (280.4 + 15) / 551 ≈ **~53.6 %** (~+1.1 pp from
W10 authoritative baseline · pre-CP4/CP5/CP6 lifts). This preview is NOT
authoritative; W11 CP9 recomputes the composite under the full
composite-lock same-commit DoD (contract + snapshot + hardcoded
numeric assertion).

## DigiCow anchor · CP3 real material tie-in

Doc17-011 (test-set-precedes-training) landed as DONE on **2026-08-26**
via the fresh DigiCow probe (interleave commit 3e99be2):
- Fresh live verification: `data_source_db-restore-603-cluster_20260826T080958Z.json`
  · `link_working: true` · engine `aurora-mysql 8.0.42 (Aurora MySQL 3.10.3)`.
- Successful seal for `obj/digicow/ussd-generation` against
  `ussd_question_response` (strata `language.sw`, `language.sw+en`,
  sample_size 1000).
- Seal manifest SHA-256 `6a681df4006a7cb56f9a956688cfdf22b06204b4338792339ecf8f95809aa42e`
  references `rds_link_verified_at=2026-08-26T08:09:58Z`.

The refuse-stale / fresh-probe / seal-succeeds cycle is visible on the
`/training` React surface for Owner inspection from an allowlisted IP.

## Verification (independent audit)

```bash
cd /app/assessment_workspace
python3 -m pytest notes/tests/test_requirements_register_20docs.py -v
# Expect: 12/12 green.
```

---

## Wave B landings appendix (CP7 · additive per Owner Ruling 2026-08-19 §6)

Wave A closed with 11 commits (R1-R7) + external verification 4/4 PASS by
owner (2026-08-26T10:30Z). R6 register truth pass note lives at
`notes/waveA_r6_register_truth_pass.md`. Wave B kickoff and CPs 4-6 close
here as additive row moves — prior rows above stay byte-identical.

### R6 truth-pass absorption (Wave A · 10 status-inflated rows)

| # | Row | Prior verdict | Post-Wave-A | Commit |
|---|-----|---------------|-------------|--------|
| 1 | Wizard / Connect Chat (Canon 5 §14) | STATUS-INFLATED | FAITHFUL | `493f6bc` |
| 2 | CP3 Training plane repo/runtime drift | STATUS-INFLATED | FAITHFUL | `ed85766` |
| 3 | CP2 Critic Seam orphaned | STATUS-INFLATED | FAITHFUL (Callers-Cover-the-Rule) | `040ee64` |
| 4 | Doc18 Callable Skill Files unreachable-on-pod | STATUS-INFLATED | FAITHFUL | `1fdd529` |
| 5 | Doc10-006 Opportunity Briefs unused endpoint | STATUS-INFLATED | FAITHFUL | `bf53b0d` |
| 6 | Doc15-086 CA1-009 Handoff contract legacy-only | STATUS-INFLATED | **FAITHFUL** (wire `2cb1c91` + data `8f40baa` Wave B) | `2cb1c91` + `8f40baa` |
| 7 | Doc16-014 Refusal card DONE conflates donor/pod | STATUS-INFLATED | FAITHFUL | `a2b056a` |
| 8 | Doc04-014 Structured refusal Evidence/Coverage | STATUS-INFLATED | FAITHFUL (via RefusalCard) | `a2b056a` |
| 9 | Watch/GreyMirror surface without producers | STATUS-INFLATED | PARTIAL (honest "unbuilt" · Wave C completes) | `37688a9` |
| 10 | Doc08 Memory router legacy-only | STATUS-INFLATED | FAITHFUL | `8667a02` |

Net: 9/10 FAITHFUL (row 9 held PARTIAL pending Wave C). Row 6 upgraded to FAITHFUL by Wave B handoff-WARN fix `8f40baa`.

### CP4 (Wave B · 2026-08-26 · commit `8722e3c`) · Doc 18 A18.7

- **Doc18-007** ← A18.7 · buyer-facing provenance chain. Prior status
  `BUILD · Carrying phase CP4`. Post-CP4: **DONE**. Backing evidence:
  - Contract `contracts/skill_file_provenance_v0.py` + snapshot (3588 bytes) · parity 59 → 60.
  - Persistence `services/skill_files/{persistence,state}.py` · write-once JSONL.
  - Router `services/skill_files/router.py` · GET `/state`, GET/POST `/{skill_id}/provenance` (201/409/422).
  - Frontend `SkillFiles.jsx` at `/skill-files` route (both mirrors byte-identical).
  - Tests 34/34 green (contract-frozen 8 + module 8 + router user-path 7 + parity 3 + Ship-Manifest DoD 8).
  - Live-pod curl receipt: GET honest-empty · 404 A18.4 refusal envelope on unknown.

### CP5 (Wave B · 2026-08-26 · commit `b9ed85b`) · Doc 17 A17.3-A17.6

- **Doc17-002** ← A17.2 · empty-seat. Prior `BUILD · CP5`. Post-CP5: **DONE** ·
  `is_empty_seat()` on `services/training/recipe_seat.py`; no pre-population
  by convention (verbatim enforcement).
- **Doc17-003** ← A17.3 · registry entries cite `recipe_version`. Prior
  `BUILD · CP5`. Post-CP5: **DONE** · `register_adapter` chokepoint refuses
  entries missing `recipe_version` (`RecipeVersionMissingError`).
- **Doc17-004** ← A17.5-A17.6 · two-arm optimizer selection. Prior `BUILD · CP5`.
  Post-CP5: **DONE (shell + auto quality-parity gate + Owner-ruling injection
  point)**. CP8 lands the real-material execution (still `BUILD · Carrying
  phase CP8`).
- **Doc17-008** (referenced under CP5 sequencing) · Post-CP5: **DONE (shape)** ·
  training_params@v0 contract + write-once persistence gated on adopted
  comparison_ref (`UnevidencedRecipeViolation`). CP8 execution completes.

Backing evidence:
- Contracts `training_params_v0.py` (snapshot 2137 bytes) + `optimizer_comparison_v0.py` (snapshot 3576 bytes) · parity 60 → 62.
- Registry M-d extension `services/model_registry/registry.py::register_adapter`.
- Router extension: GET `/api/training/recipes`, GET `/api/training/recipes/{version}` (A17.4 404), GET/POST `/api/training/optimizer-comparisons`, POST `.../{id}/arms/{arm}/measurements`, POST `.../{id}/verdict`.
- Frontend Training.jsx extended with two panels (recipe seat + optimizer comparisons · byte-identical mirrors).
- Tests 57/57 green in CP5 cohort; 80/80 combined CP4+CP5+DoD; live-pod curl 5-endpoint confirmation.

### CP6 (Wave B · 2026-08-26 · commit `d199ea6`) · Doc 19B §19B.4-6

- **Doc19B-001** ← EP-1 · evidence register. Prior `PROPOSED · Carrying phase CP6`. Post-CP6: **DONE-scaffold (PROPOSED status class carried on every row)** · write-once JSONL append, empty at ship, §19B.6 refusal envelope on GET unknown.
- **Doc19B-002** ← EP-2 · dual-judge scoring. Prior `PROPOSED · CP6`. Post-CP6: **DONE-scaffold** · contract requires ≥2 judges + judge_versions parity, 422 on single-judge attempt, 5-site closed grammar for §19B.4.
- **Doc19B-003** ← EP-3 · A-4 claims validation. Prior `PROPOSED · CP6`. Post-CP6: **DONE-scaffold** · separate ledger, three-arm result enforced, never-a-gate posture surfaced (`never_a_gate_note` in GET body).
- **Doc19B-005** ← EP-5 · Explicit non-adoption. Prior `PROPOSED · CP6`. Post-CP6: **DONE (mechanically enforced by invariant)** · `test_ep5_non_adoption_invariant.py` (5 tests) asserts no `services/insurance_telemetry/` or `services/reduction_skill_enforcement/` exists on disk AND no route in pod_shell/backend/server.py.

Backing evidence:
- Contracts `evidence_register_row_v0.py` (snapshot 2534 bytes) + `claims_validation_row_v0.py` (snapshot 2051 bytes) · parity 62 → 64.
- Persistence `services/evidence_register/{register,claims_validation}.py` · write-once JSONL per figure_id / claim_id.
- Router `services/evidence_register/router.py` · 5 endpoints (list, get-by-id, POST both stores).
- Frontend `EvidenceRegister.jsx` at `/evidence-register` (both mirrors byte-identical) · PROPOSED badge · §19B.6 verbatim shown on empty state.
- Tests 51/51 green in CP6 cohort (contract-frozen 10+9 + module 8 + router 8 + EP-5 invariant 5 + parity 3 + Ship-Manifest DoD 8).
- Live-pod curl: GET empty registers · GET /nothing → 404 with §19B.6 verbatim in envelope · POST single-judge → 422 with EP-2 remedy.

### Preliminary composite % (post-Wave-B CP4-CP6)

- Post-CP7 (17→20-doc expansion) baseline: 53.6 % of 551 rows.
- Wave A R6 truth pass (8 STATUS-INFLATED → FAITHFUL, +8.5 DONE-equivalent):
  **~55.1 %** (±0.5pp) at Wave A close.
- Wave B `8f40baa` (row 6 data-side upgrade FAITHFUL): **~55.2 %**.
- Wave B CP4 (Doc18-007 BUILD → DONE, +1 row): **~55.4 %**.
- Wave B CP5 (Doc17-002/003/004/008 four rows BUILD → DONE/shape, +3.5 rows): **~56.0 %**.
- Wave B CP6 (Doc19B-001/002/003/005 four rows PROPOSED → DONE-scaffold, +3.5 rows): **~56.6 %**.

**Preliminary composite estimate at CP6 close: ~56.6 % (±1pp)**. Authoritative composite-lock ceremony (W10 CP9 pattern with per-row delta ledger + `tools/*_composite_recompute.py`) not run in Wave B — booked as optional Wave C close item at owner discretion. The tests continue to gate FAITHFUL verdicts; the composite % is a reporting number, not a build gate.

### Carrying-phase pointer (updated · additive)

- CP7 (this appendix · 2026-08-26 · workspace `master`): register truth-pass absorption for R6 + CP4/CP5/CP6 row moves.
- CP8 (Wave B · pending SSH key): trainer runner execution completes Doc17-004 (real arm), Doc17-006 completion, Doc17-007 completion, Doc17-008 (execution). Mock SSH seam first · flip to real on key arrival.
