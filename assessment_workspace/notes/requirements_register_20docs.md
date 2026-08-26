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
