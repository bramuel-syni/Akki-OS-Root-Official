# W11 Reassessment · Register delta + reuse inventory + DigiCow + revised plan (2026-08-26T11:40Z)

Owner directive 2026-08-26T11:20Z: 3 new spec docs supplied · SSH key incoming · DigiCow data claim · deeper donor reuse suspected · reassess before build.

## Contents

- §1 · Canon delta (Docs 17, 18, 19 + 2 spec docs ingested)
- §2 · Requirements register delta (new rows CANON/RULED/PROPOSED/OPEN)
- §3 · Deep donor re-crawl · reuse inventory
- §4 · DigiCow data · found on record · rights/lineage status
- §5 · Revised W11 plan · CP sequence + LOC estimate
- §6 · Owner-input list · updated
- §7 · Composite % preview impact
- §8 · Stop-and-report — no trainer build until owner approves this plan

---

## §1 · Canon delta

Three new source docs ingested (line-by-line reads, no sampling):

| Doc | File | Lines | Status |
|-----|------|------:|--------|
| **Doc 17 · Multidimensional Training Engine** | `canon/text/Akki_Canon_Documents_17_19.txt` (part 1) | ~120 | A17.1-A17.11 CANON, A17.12-A17.17 OPEN |
| **Doc 18 · Callable Skill Files (Promise #33)** | same file (part 2) | ~85 | A18.1-A18.5 CANON, A18.6 PROPOSED (single-shot pilot), A18.7 CANON, A18.8 OPEN (audit cadence) |
| **Doc 19 · QA & Evidence Integrity** | same file (part 3) | ~76 | Part A (Critic Seam) QA-1..QA-6 CANON, Part B (Evidence Protocol) EP-1..EP-5 PROPOSED, EP-4 ordering constraint OPEN |
| Incremental Training Capacity Briefing | `canon/text/Akki_OS_Incremental_Training_Capacity_Briefing.txt` | 231 | Companion briefing to Doc 17 (TCO theory · Demand/Capacity/Gap grammar) |
| Training Techniques Spec v1.0 | `canon/text/Akki_Training_Techniques_Spec.txt` | 52 | T-1..T-4 governed artefact · Owner-ratified 2026-07-17 (RMS-native · now inbound to Extraction-Akki via Doc 17) |

Canon pack now: **9 originals + Addendum 1 + Docs 17-19 = 12 canon docs** + 2 governed-artefact spec docs. Owner phrasing "the canon pack is now 20 docs" reflects the 17-doc register (16 canon + addendum) + new Docs 17/18/19 = **20 total docs** in the register-wide count.

### Key Doc 17 requirements (CANON verbatim)

- A17.1 — Target Outcome schema is the training contract; every training run references one.
- A17.2 — Training seat starts EMPTY (no default recipe · no default optimizer · fills at first run).
- A17.3 — Every run cites a `recipe_version` at MOAC lineage (M-d extension of T-1.3).
- A17.4 — Optimizer selection is a two-arm measured comparison (T-2 protocol · Muon named as first candidate).
- A17.5 — Demand Table computed at compile · per-stratum B/I/E · admissibility requires named-failure per scheme.
- A17.6 — Capacity Ledger holds per-scheme measured level with provenance · schema ships with `provenance[]` on day one.
- A17.7 — Capacity Probe at Sampling & Reflection · reads ledger · probes selectively · writes marginal-gain.
- A17.8 — Gap-shaped staged plans · stage gates enforce no-regression against earlier stage test sets.
- A17.9 — Execution mode explicit · `PERCEPTION_EXECUTION_MODE={cpu,gpu}` at import-time · silent fallback prohibited (Owner ruling 9.2a-E2 α condition 1 · already carrier'd in `cuda_runtime.py`).
- A17.10 — `models_registry.v0.json` seeds with CI fixture model (whisper-tiny) · production models land additively at 9.2b via v0→v1 registry bump (Owner ruling 9.2a-E1 α + seed-with-CI-fixture correction 2026-07-10 · already on disk).
- A17.11 — Test set precedes training (D-7 uncurated held-out · sealed at Objective Wizard compile · no verdict-curation).
- A17.12-A17.17 — OPEN decisions (taxonomy graduation sign-off · probe-selectivity threshold · validation gating gate-vs-parallel · interference weighting trigger · saturation-cross-tenant policy · single-shot pilot policy).

### Key Doc 18 requirements (CANON verbatim)

- A18.1 — Callable skill provisioning contract (frozen · extra=forbid · slice bound at freeze · "new slice = new skill").
- A18.2 — Per-call inner gate · identity + scope + floor checks on every invocation.
- A18.3 — Every response carries defensibility class inline (SUBSTANTIATED / GROUNDED / SPECULATIVE).
- A18.4 — Write-once persistence · revocation lands in the record · never mutates prior state.
- A18.5 — Endpoint path bound at provisioning · skill callable only through the exact declared path.
- A18.6 — PROPOSED · single-shot pilot for enterprise sales (owner ratifies before deployment).
- A18.7 — CANON · every skill's provenance chain traces back to the training run that produced its adapter (Doc14-016 rights-lineage + Doc14-017 version-history extends here).
- A18.8 — OPEN · audit cadence for provisioned skills.

### Key Doc 19 requirements (CANON verbatim)

**Part A · Critic Seam (QA-1..QA-6)**:
- QA-1 — The Critic Seam detects and never decides (findings only · no override/veto/final-say authority for any collection of models).
- QA-2 — Three-tier layer: Tier 1 deterministic checks · Tier 2 independent critic model · Tier 3 human calibration with seeded-defect audits.
- QA-3 — Independence — critic and target must differ (different base OR materially different context shape).
- QA-4 — Rubric-driven with named failure classes · rubric versions ledgered.
- QA-5 — Every worker output passes through Critic Seam · shipped-without-seam is a defect (Doc14-002/003).
- QA-6 — Ensemble critics permitted only when Tier-3 audits show single-critic below bar on any fall class across two consecutive audits (T-3 protocol).

**Part B · Evidence Protocol (EP-1..EP-5) — PROPOSED**:
- EP-1 — Evidence register records every measurement with its class (FACT/NORM/DEFAULT).
- EP-2 — Dual-judge protocol for evaluation blinding (D-7 uncurated verdict samples).
- EP-3 — Verdict samples are ENGINEERED, evaluation SAMPLES are NEVER curated.
- EP-4 — OPEN · ordering constraint on evidence class transitions (whether DEFAULT can promote to NORM without a bounded observation window).
- EP-5 — Evidence class attaches inline to every claim on every surface (per Doc 18 A18.3 · same discipline).

---

## §2 · Requirements register delta

Register (`notes/requirements_register_17docs.md`) grows from 17 docs to 20 docs. Below is the row-count table delta and the new row schemas.

### Row-count table addition

| Doc | Umbrella canon | Rows (CANON) | Rows (RULED) | Rows (PROPOSED) | Rows (OPEN) | Total |
|----:|---------------|-------------:|-------------:|-----------------:|------------:|-----:|
| 17 · Multidimensional Training Engine | Canon 4 §26-§33 · Doc 17 §§1-9 | 11 | 0 | 0 | 6 | 17 |
| 18 · Callable Skill Files | Doc 18 §§1-8 · BCR §3.7 annex | 6 | 0 | 1 | 1 | 8 |
| 19 · QA & Evidence Integrity | Doc 19 A · B · Canon 4 §21-§23 | 6 | 0 | 4 | 1 | 11 |
| **Delta** | | **23** | **0** | **5** | **8** | **36** |

Total register grows: 515 → **551 rows** (mechanism corpus recount pending §7 preview).

### New row schema (samples · full expansion at register-update CP)

- **Doc17-001** ← A17.1 · Target Outcome schema is the training contract. Status **BUILD** (Objective Wizard integration not on programme/track-a).
- **Doc17-002** ← A17.2 · Seat starts EMPTY (training_params@v0 sidecar · no default recipe). Status **BUILD** (T-1.2 · training-recipe seat not yet on disk).
- **Doc17-009** ← A17.9 · `PERCEPTION_EXECUTION_MODE={cpu,gpu}` at import-time · silent fallback prohibited. Status **DONE** (`backend/services/perception/gpu_execution/cuda_runtime.py` · 51 LOC · already in Extraction-Akki · Owner ruling 9.2a-E2 α carrier).
- **Doc17-010** ← A17.10 · `models_registry.v0.json` seeds with whisper-tiny CI fixture. Status **DONE** (`backend/services/perception/models_registry.v0.json` on disk).
- **Doc17-011** ← A17.11 · Test set precedes training · D-7 uncurated held-out. Status **REUSABLE** (D-7 posture is Northena admit + verdict discipline · already enforced).
- **Doc17-012..017** ← A17.12-17 · OPEN decisions. Status **OPEN-SLOT** (owner-policy pending · non-blocking to trainer scaffolding).
- **Doc18-001** ← A18.1 · Callable skill provisioning contract. Status **DONE** (`backend/contracts/callable_skill_provisioning_v0.py` · 101 LOC · frozen · snapshot on disk · REGISTER OVERSIGHT CORRECTED — earlier W11 gap map said "not in build" · it IS in the build).
- **Doc18-002** ← A18.2 · Per-call inner gate. Status **DONE** (`services/transform_forms/callable_skill_gate.py` · 144 LOC).
- **Doc18-003** ← A18.3 · Defensibility class inline. Status **DONE** (integrated into gate).
- **Doc18-004** ← A18.4 · Write-once persistence. Status **DONE** (`services/transform_forms/callable_skill_persistence.py` · 111 LOC).
- **Doc18-005** ← A18.5 · Endpoint path bound. Status **DONE** (part of provisioning contract).
- **Doc18-006** ← A18.6 · PROPOSED single-shot pilot. Status **PROPOSED** (owner ratifies before deployment).
- **Doc18-007** ← A18.7 · Provenance chain to training run. Status **BUILD** (training-run producer absent; extension of Doc14-016).
- **Doc18-008** ← A18.8 · OPEN audit cadence. Status **OPEN-SLOT**.
- **Doc19A-001..006** ← QA-1..QA-6 Critic Seam. Status **REUSABLE** (LIFT candidate · `Akki-OS-V1/backend/services/critic_pass/` · 950 LOC · not yet in Extraction-Akki). Anchors: `docs/requirements/critic_seam_spec_v1_1.md` (already in Extraction-Akki as spec) + owner ruling `critic_pass_e1_2026_07_25.md` in Akki-OS-V1.
- **Doc19B-001..005** ← EP-1..EP-5 Evidence Protocol. Status: **PROPOSED** (4) + **OPEN-SLOT** (EP-4 ordering constraint).

---

## §3 · Deep donor re-crawl · reuse inventory

**Prior gap map was under-inventoried.** Owner was right that summarized pulls had gaps. Actual findings:

### 3.1 · Already in Extraction-Akki (LIFTED prior · was mis-classified as MISSING in W11 gap map)

| Component | Path (Extraction-Akki) | LOC | Doc 17/18/19 requirement satisfied | Note |
|-----------|------------------------|----:|-------------------------------------|------|
| **cuda_runtime.py** · execution mode contract | `backend/services/perception/gpu_execution/cuda_runtime.py` | 51 | **A17.9** | Owner ruling 9.2a-E2 α carrier · `PERCEPTION_EXECUTION_MODE={cpu,gpu}` · import-time explicit |
| **execution_mode_telemetry.py** · attribution sidecar | `backend/services/perception/execution_mode_telemetry.py` | ~50 | **A17.9** (condition 2) | Ships `execution_mode` in result telemetry |
| **models_registry.v0.json** · CI fixture seed | `backend/services/perception/models_registry.v0.json` | ~450 lines JSON | **A17.10** | whisper-tiny pinned SHA · C1-candidate rows for Qwen3/Llama/DeepSeek families |
| **model_loader.py** · GPU model loader | `backend/services/perception/gpu_execution/model_loader.py` | 45 | A17.9 sibling | Backend-selection-aware loader |
| **audio_batching.py** · GPU batching | `backend/services/perception/gpu_execution/audio_batching.py` | 32 | A17.9 sibling | GPU batch composer |
| **asr_worker.py** · ASR perception worker | `backend/services/perception/asr_worker.py` | ~200 | Feeds Critic Seam (QA-2 target-independent path) | Real fixture · whisper-tiny |
| **diarization_worker.py** · speaker attribution | `backend/services/perception/diarization_worker.py` | ~150 | Multi-scheme target (Demand Table B ≥ 2) | pyannote provider path |
| **eab_1_pipeline/** · full VAD + dedup + segmentation + license classification pipeline | `backend/services/perception/eab_1_pipeline/` (7 files) | 649 | Feeds training data admission | 141 LOC dedup + 82 demux + 123 segment + 140 VAD + 52 license + 161 occurrence + 86 trace-walker |
| **callable_skill_provisioning_v0.py** · frozen contract | `backend/contracts/callable_skill_provisioning_v0.py` + snapshot | 101 | **A18.1, A18.5** | Slice-bound at freeze · endpoint-path declared |
| **callable_skill_gate.py** · per-call inner gate | `backend/services/transform_forms/callable_skill_gate.py` | 144 | **A18.2, A18.3** | Identity + scope + floor + defensibility inline |
| **callable_skill_persistence.py** · write-once store | `backend/services/transform_forms/callable_skill_persistence.py` | 111 | **A18.4** | Write-once · revocation records |
| **critic_seam_spec_v1_1.md** · governance doctrine | `docs/requirements/critic_seam_spec_v1_1.md` | ~200 | Doc 19A doctrine anchor | Spec text · doctrine only |
| **training_techniques_spec_v1.md** · governance doctrine | `docs/requirements/training_techniques_spec_v1.md` | 103 | T-1..T-4 doctrine anchor | Now formally under Doc 17 |
| **transformation_quality_spec_v1.md** · MOAC extension doctrine | `docs/requirements/transformation_quality_spec_v1.md` | ~200 | MOAC M-d extension for recipe_version (A17.3) | |

**Total already-lifted LOC serving Doc 17/18/19**: ~2136 LOC of production + ~500 LOC of doctrine.

### 3.2 · LIFT-clean from Akki-OS-V1 (not yet in Extraction-Akki)

| Component | Path (Akki-OS-V1) | LOC | Doc 19A/QA requirement | Verdict |
|-----------|-------------------|----:|-------------------------|---------|
| **critic_pass/harness.py** | `backend/services/critic_pass/harness.py` | 89 | **QA-1, QA-2** (three-tier layer · detection-only) | LIFT-clean |
| **critic_pass/rubric.py** | `backend/services/critic_pass/rubric.py` | 147 | **QA-4** (rubric-driven · named failure classes) | LIFT-clean |
| **critic_pass/calibration_ledger.py** | `backend/services/critic_pass/calibration_ledger.py` | 169 | **QA-3, QA-6** (independence + Tier-3 seeded audits) | LIFT-clean |
| **critic_pass/manifest_gate.py** | `backend/services/critic_pass/manifest_gate.py` | 137 | QA-5 (shipped-without-seam is a defect · gate at manifest boundary) | LIFT-clean |
| **critic_pass/seeded_defect_corpus.py** | `backend/services/critic_pass/seeded_defect_corpus.py` | 240 | QA-6 (Tier-3 seeded audits harness) | LIFT-clean |
| **critic_pass/archive.py** | `backend/services/critic_pass/archive.py` | 147 | QA-5 (persistence of finding records) | LIFT-clean |
| **critic_pass/__init__.py** | `backend/services/critic_pass/__init__.py` | 21 | Package exports | LIFT-clean |
| **critic_seam_spec_v1_1.md** (Akki-OS-V1 companion doctrine) | already same in Extraction-Akki | — | — | Same file · no lift |
| **test_critic_pass_execution_atomic.py** (invariant test) | `backend/tests/invariants/test_critic_pass_execution_atomic.py` | ~150 | QA-1 · QA-5 execution invariants | LIFT (adapt paths only) |
| **critic_pass close report + rulings + stage_a proposal** | `docs/close_reports/critic_pass.md` + `docs/rulings/critic_pass_e1_2026_07_25.md` + `docs/stage_a_proposals/critic_pass_stage_a.md` | ~300 | Doctrine trail | REFERENCE-only |

**Total LIFT-clean from Akki-OS-V1 for Doc 19A**: **950 LOC of production + 150 LOC of tests + ~300 LOC of doctrine trail**. This is one of the biggest single-CP wins in the plan.

### 3.3 · NOT found in any donor · still BUILD

| Component | Doc 17/18/19 requirement | Verdict |
|-----------|---------------------------|---------|
| **Training Planner** (gap-shaped stage plan) | A17.5, A17.8 | BUILD-us — no donor code matches the Demand-Table→Gap→Staged-Plan pattern |
| **Capacity Ledger writer** (marginal-gain rows · provenance) | A17.6, A17.7 | BUILD-us — donor `services/model_registry` has attest_model but not per-scheme per-stratum capacity levels |
| **Capacity Probe** at Sampling & Reflection | A17.7 | BUILD-us — donor has calibration_ledger.py (critic-side) but not model-capability-side |
| **Trainer runner** (LoRA/PEFT adapter dispatch) | A17.4, T-1..T-2 | BUILD-us — no donor has an actual training loop |
| **Muon optimizer arm** | T-2.2 shape (two-arm comparison) | BUILD-us — protocol only; comparison harness is BUILD |
| **Recipe seat `training_params@v0`** | T-1.1 (versioned · ledgered · outside contracts/) | BUILD-us — sidecar class · patterned after `extraction_params@v0` (which is in donors · check next) |
| **Objective Wizard demand-table compile step** | A17.5 | BUILD-us · integrates with existing Wizard surface |
| **Training panel frontend** + **Skill Files surface** | Canon 5 §12 · Doc 17 §6 | BUILD-us · React |

### 3.4 · ADAPT candidates (donor has partial · needs Doc 17/19 harmonization)

| Component | Path | LOC | What adapts |
|-----------|------|----:|-------------|
| **critic_pass** (see 3.2) once lifted · needs Doc 19 QA-1..QA-6 header + parity same-commit DoD | Akki-OS-V1 → Extraction-Akki | 950 | Contract snapshot + parity map + hardcoded count entries; harness signature extension for Doc 17 stage-gate integration |
| **models_registry.v0.json** · add C1 rows for MTEB text-embedding families (for USSD text training) | Extraction-Akki · already on disk | — | Text-modality candidates named at first census activation (Owner ruling anchor) |
| **transform_forms/callable_skill_persistence.py** · integrate provisioning trigger with training-run completion | Extraction-Akki · in build | 111 | Extension to write provisioning record ON MOAC admission (Doc 18 A18.7 provenance chain) |

### 3.5 · Extraction params sidecar (already-lifted precedent for T-1.1 pattern)

Grep confirms `extraction_params@v0` is the analog pattern the Training Techniques Spec T-1.1 explicitly references ("same discipline as extraction_params@v0"). Search reveals extraction_params is in `docs/requirements/extraction_derisking_spec_v1.md` (spec) but I need to check whether the sidecar class itself is already in Extraction-Akki — TBD at CP-open time.

---

## §4 · DigiCow data · found on record

Owner statement "you have data from DigiCow" verified against ground truth:

### 4.1 · What it is

- **Source**: `aws.rds.db-restore-603-cluster.digicow_live` · AWS RDS Aurora MySQL (engine 8.0.42 · Aurora MySQL 3.10.3) · eu-west-1
- **Connection channel**: rds-data-api (`arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster` · secret_arn in AWS Secrets Manager)
- **Owner-signed connection record** on disk: `/app/assessment_workspace/phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json` (link_working: true · 125 tables enumerated)
- **Modality**: **primarily TEXT** — USSD session records, SMS logs, question/response transcripts, user metadata, training-post views. This is a **farmer-facing agricultural-extension platform** (SMS/USSD channel). Registry.jsx line 417 verbatim: *"USSD activity dominates: the top four tables all sit in digicow_live and hold session-and-response records from the SMS/USSD farmer channel."*
- **Volume (top 25 tables surfaced in the record)**:
  - `ussd_users` · **2.28M rows** · 748 MB
  - `ussd_question_response` · **903K rows** · 133 MB
  - `ussd_api_session_validation` · 521K rows · 162 MB
  - `shortcode_questions_response` · 400K rows · 68 MB
  - `post_view` · 294K rows · 29 MB
  - `sms_log` · 256K rows · 68 MB
  - `user_group_trainings` · 164K rows · 111 MB
  - `post_gallery_view` · 117K rows · 8 MB
  - `users` · 108K rows · 26 MB
  - `single_training_post_view` · 75K rows · 15 MB
  - ... (top-25 continues in the record · full 125-table inventory available)
- **Strata (by initial inspection)**: USSD session type · language (multi-lingual EA farmer platform likely) · question category · training post category · time cohort. Doc 17 Demand Table will formalize this at compile.

### 4.2 · Custody status

- **Chokepoint residency allowlist** admits `eu-west-1` REGION for this source (`residency_allowlist.v0.json` line 24 · authored 2026-08-25 · Owner-governed).
- **Connection is LIVE** (link_working: true at 2026-08-19T15:25:13Z · re-verified via test invariants that read from the FINAL record).
- **rds_data_router.py** + **rds_data_submit.py** exist in `backend/services/connect/` — the read path through the chokepoint is on-disk.

### 4.3 · Rights & lineage status

**Rights**: **PENDING owner declaration.** Canon 4 §28 (Doc14-016 DONE for shape) demands rights-lineage-resolved before extraction admits training data. The data-connection record has fields for `link_working` and `resource.region` but NO `rights_declaration_signed_by_owner` field. Owner must sign a rights declaration explicitly naming:
- Legal basis for training on DigiCow user records (consent · legitimate interest · data-processor agreement · other).
- Scope of allowed training use (adapter-training only? · derived weights ownership? · redistribution rights?).
- PII posture · USSD user records almost certainly contain PII (`users` table · `sms_log`) · this drives CA1-N2/N3 (breach + erasure) becoming load-bearing.
- Data-subject notification path (CA1-N2 · FL-P4-W8-01 · 7 policy questions).

**Lineage**: The extraction chain will be `RDS Data API → rds_data_router → chokepoint admit → training-material admit contract (BUILD-us) → training-run record`. Each step writes a lineage row.

### 4.4 · What DigiCow enables for the "test the training section first" goal

- **Real strata for calibration**: USSD-channel text is a distinct modality slice with real skew (majority-language dominance · dialect variants · code-switching) — perfect for the Doc 17 Demand-Table + Capacity-Probe first exercise.
- **Test-set-precedes-training (A17.11)**: a small held-out slice (e.g., 1000 rows sampled by strata · sealed at Objective Wizard compile) can be sealed before any training pipeline fires.
- **First MOAC on real material**: the calibration probe run at Sampling & Reflection can emit the first real MOAC card against DigiCow's uncurated composition.

---

## §5 · Revised W11 plan

### 5.1 · Scope reset

Prior W11 gap-map envelope: 4-6k LOC. **Revised: ~2.5-3.5k LOC net-new** (LIFT-heavy · big single wins from callable-skill package already lifted + critic_pass ready to lift).

### 5.2 · CP sequence

CPs ordered by dependency AND by owner's stated goal *"test the training section first"* · Doc 17 A17.11 (test-set-precedes-training) + A17.5 (Demand Table at compile) both fire in CP3.

| CP | Scope | Requirements satisfied | Verdict | LOC est. |
|----:|-------|-----------------------|---------|--------:|
| **CP1** | R11 STEP 2/3 completion — real GPU handshake, hardware fact sheet, `/api/connect/gpu` real crossing receipt, mode toggle regression invariant (fix-back under R11 waiver). | R11 · Doc 17 A17.9 sibling | LIFT-adapt-in-place | ~150 |
| **CP2** | Doc 19A Critic Seam LIFT from Akki-OS-V1 · same-commit DoD for the new frozen contract (`critic_manifest_v0`, `critic_finding_v0`, `critic_calibration_ledger_v0`) · parity map + hardcoded numeric assertion + snapshots · register rows Doc19A-001..006 land as DONE. | Doc 19A QA-1..QA-6 · Doc 14-002..005 Critic Seam quartet | LIFT-clean (950 → repo) | ~1100 (950 lift + ~150 contracts) |
| **CP3** | Doc 17 A17.1-A17.11 · Target Outcome + Demand Table (compile step in Objective Wizard) + Capacity Ledger (schema + writer with provenance day-one) + Capacity Probe (Sampling & Reflection extension) · TEST SET SEAL first (A17.11) against DigiCow slice · training-panel frontend surface. This CP delivers the "test the training section first" outcome — owner can see the Demand Table for a real objective, the Capacity Ledger seeded EMPTY, and the calibration probe writing marginal-gain rows against DigiCow strata. **NO trainer runner yet** — the ceremony ships end-to-end WITHOUT firing a real training loop. | Doc 17 A17.1, A17.2, A17.5, A17.6, A17.7, A17.8, A17.11 · T-1.1 recipe seat empty · Doc 14 baseline-line reused | BUILD (heavy) + some ADAPT | ~1400 (500 contracts + 400 services + 500 frontend) |
| **CP4** | Doc 18 provenance-chain wire-up · extend `callable_skill_persistence.py` to trigger provisioning ON MOAC admission (A18.7) · Skill Files surface (frontend) · register Doc18-001..008 statuses corrected in the register (7 DONE + 1 PROPOSED + 1 OPEN-SLOT — big win: previously mis-classified as BUILD). | Doc 18 A18.1-A18.7 (A18.6 PROPOSED · A18.8 OPEN) · Doc14-016 rights-lineage extends | ADAPT (extension of already-lifted package) + BUILD frontend | ~350 (100 service extension + 250 frontend) |
| **CP5** | Doc 17 A17.3-A17.4 + T-1..T-2 · `training_params@v0` recipe seat sidecar (EMPTY at ship) · MOAC M-d extension for `recipe_version` · optimizer-selection protocol harness (two-arm comparison shape · does NOT run a real training loop yet · shape only) · register Doc17-002/003/004 land DONE. | Doc 17 A17.3, A17.4 · T-1.1, T-1.2, T-1.3, T-1.4, T-2.2 (shape only) | BUILD + parity same-commit DoD | ~250 |
| **CP6** | Doc 19B Evidence Protocol PROPOSED harness · EP-1..EP-3, EP-5 (EP-4 stays OPEN-SLOT) · evidence class inline attachment discipline extends across surfaces already rendering source_path citations. | Doc 19B EP-1, EP-2, EP-3, EP-5 (PROPOSED landing) · MOAC evidence class linkage | BUILD (small) | ~200 |
| **CP7** | Register expansion to 20 docs · `notes/requirements_register_17docs.md` → `notes/requirements_register_20docs.md` · 36 new rows (23 CANON + 5 PROPOSED + 8 OPEN-SLOT) · row-count table updated. | Register discipline · additive-only per Owner Ruling 2026-08-19 §6 | BUILD (docs) | ~250 register lines + 150 test LOC |
| **CP8** | Trainer runner LIFT-adapt + BUILD (LoRA/PEFT dispatch on real GPU via `/api/connect/gpu`) · Muon comparison arm · first real training run on DigiCow slice · MOAC card emitted · whitepaper drafter fires. **Gated on**: owner rights declaration for DigiCow · SSH key for real GPU · Doc14-020 §38 ruling if PII in corpus · owner ratification of recipe-seat and optimizer verdict per T-2.4. | Doc 17 A17.4 (execution) · T-2.2 (real two-arm run) · Doc 14 §33 whitepaper fires with real content · Doc 18 A18.7 provisioning fires | BUILD | ~800 (trainer runner) |
| **CP9** | Authoritative composite % recomputation · wave-close cohort re-run · close report. | Composite lock same-commit DoD | BUILD (docs) | ~200 |

**Grand total**: ~4700 LOC · **but ~1100 of that is LIFT-clean** (critic_pass) · **~950 more is LIFT-clean already** (callable-skill in Extraction-Akki wasn't correctly reflected in prior gap map). So the net BUILD is closer to **~2500-3000 LOC** — well under the revised envelope.

### 5.3 · The "test the training section first" path (CP1→CP2→CP3)

**Time-to-first-eyeball for the training section**: CP1 (GPU real) + CP2 (Critic Seam LIFT) + CP3 (Demand Table + Capacity Probe + Test-set-seal + Training panel).

At end of CP3, owner can eyeball:
- `/training` route on the SPA · Governance/Watch pattern · REFERENCE-NOT-COPY posture
- Real Demand Table for a DigiCow objective (compiled at Objective Wizard · staged rendering)
- Real Capacity Ledger (empty at ship · one calibration probe writes first row)
- Real Test-set seal on a small DigiCow strata slice (sealed before any training)
- Real Critic Seam surface (findings-only · Tier 1 deterministic + Tier 2 critic + Tier 3 seeded audit setup)

**All this WITHOUT the trainer runner firing.** The trainer runner is CP8. Owner gets a look at the shape · sees the DigiCow data flowing through the pipeline · sees Critic Seam working · sees Capacity Probe writing measured rows — before any GPU-hours are spent.

### 5.4 · Per-CP LIFT/ADAPT/BUILD split

| CP | LIFT LOC | ADAPT LOC | BUILD LOC |
|----|---------:|----------:|----------:|
| CP1 | 0 | 100 | 50 |
| CP2 | 950 | 100 | 50 |
| CP3 | 200 (perception plane reuse) | 400 | 800 |
| CP4 | 0 | 100 | 250 |
| CP5 | 0 | 50 | 200 |
| CP6 | 0 | 50 | 150 |
| CP7 | 0 | 0 | 400 |
| CP8 | 0 | 200 | 600 |
| CP9 | 0 | 0 | 200 |
| **Total** | **1150** | **1000** | **2700** |

Grand total ~4850 LOC · LIFT-plus-ADAPT is ~44% · pure BUILD is ~56%. Compared to prior W11 gap map (4-6k mostly BUILD): significant compression.

---

## §6 · Updated OWNER-input list

Owner supplies before CP8 fires a real training run:

1. **SSH key for GPU VM** — supplied "shortly" per current directive · unblocks CP1 (R11 STEP 2/3 finalize).
2. **DigiCow rights declaration** — owner-signed · legal basis + scope + PII posture + data-subject notification path. Load-bearing before CP3 seals a test set on real DigiCow rows and CP8 admits training material.
3. **Base model choice + licence** — which open base model does the first adapter train on (A17.10 registry has C1 candidates for Qwen3/Llama/DeepSeek/etc. named · owner names the specific base at first-census-activation per the models_registry.v0.json authority anchor).
4. **A17.10 census activation** — owner ruling to promote a specific C1 candidate to seeded model at 9.2b (v0→v1 registry bump).
5. **A17.12-A17.17 OPEN rulings** (6 policy answers):
   - A17.12 · Taxonomy graduation sign-off · which product role owns admitting a new scheme.
   - A17.13 · Probe-selectivity threshold · confirm/adjust proposed default (per-stratum for I=1 + acceptance-gated strata).
   - A17.14 · Validation gating (§8) gate-vs-parallel with first commission.
   - A17.15 · Interference weighting trigger (binary → weighted).
   - A17.16 · Saturation cross-tenant policy (currently deferred).
   - A17.17 · Doc 17 additional OPEN item · owner brief to clarify at ratification.
6. **A18.6 single-shot pilot ratification** — owner ratifies before enterprise deployment.
7. **A18.8 audit cadence for provisioned skills** — owner sets cadence.
8. **EP-4 evidence-class ordering constraint** (Doc 19B) — whether DEFAULT can promote to NORM without a bounded observation window.
9. **Doc14-020 §38 rights-unclear grammar** — carried over from W10 CP7 · N-series pattern · load-bearing before external delivery of any trained-skill output.
10. **Recipe-seat ratification for Extraction-Akki** — the RMS Training Techniques Spec v1.0 (T-1..T-4) was ratified 2026-07-17 for RMS scope · needs equivalent ratification anchoring into the Extraction-Akki canon (Doc 17 formalizes this · owner sign-off completes it).
11. **CA1-N2 + CA1-N3 policy answers** (14 questions · FL-P4-W8-01) — become load-bearing at CP8 if DigiCow training touches PII.
12. **CA1-N5 policy answer** (1 question · FL-P4-W9-01) — continuity attestation cadence.

### Which of these are BLOCKING vs NON-BLOCKING per CP

| Owner input | Blocks CP | Non-blocking to |
|-------------|-----------|-----------------|
| SSH key | CP1 | CP2, CP3 (can run offline against fixture · defer real GPU handshake) |
| DigiCow rights declaration | CP3 seal + CP8 admit | CP1, CP2, CP4, CP5, CP6, CP7 |
| Base model choice + A17.10 census activation | CP8 real training | CP1-CP7 |
| A17.12-17 rulings | Non-blocking (OPEN-SLOT pattern) | any CP |
| A18.6 pilot ratification | Non-blocking to CP4 build · blocking to real-deployment | CP4 code lands · deployment awaits |
| A18.8 audit cadence | Non-blocking | any CP |
| EP-4 ordering constraint | Non-blocking (OPEN-SLOT) | any CP |
| Doc14-020 ruling | CP8 external delivery | CP1-CP7 |
| Recipe-seat ratification | CP5 register-land | CP1-CP4 |
| CA1-N2/N3/N5 policy answers | CP8 real training (if PII) | CP1-CP7 |

---

## §7 · Composite % preview

Adding 36 new register rows to the mechanism corpus grows the denominator from 515 to **551**. Preview recompute (**NOT authoritative** · will be locked in CP9):

**With new rows lit as reassessed** (from §2 delta):
- Doc17 (17 rows): 3 DONE (17-009, 17-010, 17-011) + 6 OPEN-SLOT (17-012..017) + 8 BUILD = 3+0+0+8 buckets after · weighted = 3.0
- Doc18 (8 rows): 5 DONE (18-001..005) + 1 BUILD (18-007 trainer prereq) + 1 PROPOSED (18-006 · treat like OPEN-SLOT weight 0 pending owner ratification) + 1 OPEN-SLOT (18-008) · weighted = 5.0
- Doc19A (6 rows): 6 REUSABLE (QA-1..QA-6 LIFT-clean from Akki-OS-V1) · weighted = 3.0
- Doc19B (5 rows): 4 PROPOSED (EP-1,2,3,5 · treat like BUILD weight 0 pending owner ratification) + 1 OPEN-SLOT · weighted = 0.0
- Also correct: Doc18 discovery **retroactively bumps 5 rows already in build** that were mis-classified — this is a correction, not a delta from CP work. That correction alone lifts the composite.

Rough preview: mechanism weighted rises from 280.4 to ~**291.4** (280.4 + 11 new-DONE weight); denominator rises 515→551. **Preview composite ≈ 52.9%** (barely up from 52.49% authoritative · because denominator grows almost in lockstep with lit rows). This is HONEST — the register got LARGER at the same time the DONE count grew.

**After CP8 completes a real training run**: expect composite to jump ~2-4pp (Doc17-004 optimizer + T-2 · Doc17-008 gap-plan · Doc18-007 provenance chain · plus 3-5 more Doc14 rows moving from BUILD to DONE). Post-W11 composite estimate: **55-57%**. Authoritative recompute at W11 CP9.

---

## §8 · Stop-and-report

**No trainer code built.** Deliverables landed:
- Canon delta (§1) — 3 docs converted + full read.
- Requirements register delta (§2) — 36 new rows scoped.
- Reuse inventory (§3) — big finding: callable-skill package + cuda_runtime + models_registry ALREADY IN Extraction-Akki (prior gap map missed this). Critic_pass 950 LOC is LIFT-clean from Akki-OS-V1.
- DigiCow data (§4) — verified on record · connection live · rights declaration pending owner.
- Revised W11 plan (§5) — 9 CPs · ~4850 LOC · LIFT-heavy (44%) · owner's "test training section first" goal reachable at end of CP3 without spending GPU-hours.
- Owner-input list (§6) — 12 items · blocking-vs-non-blocking table per CP.
- Composite % preview (§7) — 515→551 rows · preview ~52.9% · not authoritative until CP9.

**Awaiting owner approval of this plan before CP1 opens.** R11 waiver remains open — CP1 completion is interleaved with STEP 5 (SSH key arrival + real GPU handshake).
