# Technical report: ASR register adapter for the RMS contact-centre archive

Run `RP-asr-register-adapter-001` · objective `asr-register-adapter@1` · direction T1 · backend **stub** · status **stub**

> STUB RUN. none — stub metrics are a deterministic function of the seed (see policy.stub.note)

## 1. Problem and objective

speech-to-text on audio; population by spoken register in 4 strata. Acceptance is two-dimensional per stratum (accuracy × coverage); gate policy: **gates**.

| Stratum | Share | Baseline acc. | Floor acc. | Gap (pp) | Floor cov. | Available examples |
|---|---|---|---|---|---|---|
| ST1 Kenyan English | 46.0% | 86.0% | 90.0% | 4.0 | 97.0% | 1,200 |
| ST2 Kiswahili | 31.0% | 78.0% | 85.0% | 7.0 | 95.0% | 1,200 |
| ST3 Sheng | 14.0% | 61.0% | 75.0% | 14.0 | 90.0% | 1,200 |
| ST4 Code-switched | 9.0% | 66.0% | 78.0% | 12.0 | 92.0% | 1,200 |

[measured] Receipt R01, R03: Estate registry census 2026-09-22, register strata counts, table 4; Baseline evaluation run BL-0917 on TS-ASR-04 v2, per-stratum WER, 2026-09-17

## 2. Data statement

| Material | Stratum | Examples | Class | Lawful basis | Hash |
|---|---|---|---|---|---|
| M01 contact-centre recordings 2024–2026, consented | ST1 | 1,200 | measured | consent | `sha256:7c1e…a2` |
| M02 contact-centre recordings 2024–2026, consented | ST2 | 1,200 | measured | consent | `sha256:9b04…f1` |
| M03 community radio call-ins, licensed | ST3 | 1,200 | measured | licence | `sha256:3d7a…0c` |
| M04 contact-centre recordings 2024–2026, consented | ST4 | 1,200 | measured | consent | `sha256:e55b…77` |

Training manifest `sha256:e684ce16b4cd7feafaa895451c9d2ed3d44e386acf23e148679b38f4a27167cc`: 4,800 examples, 100.0% classed, lawful basis present: True, refused: 0. Per-example provenance in `training-manifest.jsonl` (A17.20). Selection: deterministic: examples ordered by sha256(example_id); first N per stratum; each volume is a superset of the previous.

| Stratum | Examples | By class | By lawful basis |
|---|---|---|---|
| ST1 | 1,200 | measured 1,200 | consent 1,200 |
| ST2 | 1,200 | measured 1,200 | consent 1,200 |
| ST3 | 1,200 | measured 1,200 | licence 1,200 |
| ST4 | 1,200 | measured 1,200 | consent 1,200 |

Collection schema (unit: utterance): fields example_id, audio_ref, transcript, register, speaker_pseudonym, duration_s, consent_ref, content_hash; quality gates {"duration_s": [1.0, 30.0], "sample_rate_hz": 16000, "transcript_non_empty": true}; labelling: register assigned by two annotators; disagreement resolved by the census classification authority, recorded as a human contribution event; admission: an example enters the manifest only with class, lawful basis and content hash; otherwise it is refused and the refusal counted. [estimated] Receipt R06: Objective owner sign-off memo OO-2026-09-29

[measured] Receipt R04: Rights declaration RD-RMS-07, owner-signed 2026-09-20, lawful basis per source

## 3. Baseline record

Baseline run Baseline evaluation run BL-0917 on TS-ASR-04 v2, per-stratum WER, 2026-09-17 on the sealed test set (Stratified test set TS-ASR-04 v2, sealed 2026-09-25, 1,200 utterances, uncurated held-out). Base model: `models_registry.v0#whisper-tiny`, role: ci-fixture-only; production selection deferred to first census activation (A17.11).

## 3b. Objective critique (four lenses)

Full table in `critique.md`. Escalations to the objective owner are listed there; the adopted verdict records which objections were accepted and which overruled.

## 4. Method

Adopted direction T1 under the recorded verdict `TV-2026-10-02-001`. Recipe seat: **empty** (training_params@v0). Calibration at [250, 500, 1000] examples per stratum, 2 epochs each; two-arm optimizer comparison on the smallest valid stratum (ST4).

## 5. Setup and reproducibility

Execution mode: stub. Reproducibility contract: seed-fixed re-run within tolerance (accuracy ±0.002, coverage ±0.002); canon: C.8 standard training criteria; C.20.10 reproducibility test. Seed `asr-register-adapter/calibration/2026-10-02`. Calibration cost: estimated £59.52 [estimated, R05], actual £59.52 (18.6 GPU h) [stub]; comparison cost £16.32 [estimated, R05].

## 6. Results on held-out material

| Stratum | acc @250 | acc @500 | acc @1000 | cov @250 | cov @500 | cov @1000 | To acc. floor | To cov. floor | Binding | CI | Reachable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ST1 | 86.9% | 88.5% | 89.4% | 97.4% | 98.4% | 98.9% | 1309 | 157 | accuracy | not reported (3 points) | no |
| ST2 | 80.1% | 81.9% | 83.4% | 95.4% | 96.1% | 96.7% | 1899 | 156 | accuracy | not reported (3 points) | no |
| ST3 | 64.3% | 67.4% | 70.3% | 88.5% | 89.3% | 89.6% | 2897 | 1435 | accuracy | not reported (3 points) | no |
| ST4 | 68.8% | 71.0% | 74.0% | 90.8% | 91.3% | 92.0% | 3007 | 1052 | accuracy | not reported (3 points) | no |

[stub] Evaluated on Stratified test set TS-ASR-04 v2, sealed 2026-09-25, 1,200 utterances, uncurated held-out. Failed strata are reported as plainly as passed ones.

### Diagnosis per stratum (professor names the cause; researcher picks the lever)

| Stratum | Cause | Test | Curve slope ratio | Train/held-out gap | Annotator agreement | First lever | Expected effect (class) |
|---|---|---|---|---|---|---|---|
| ST1 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 0.54 | 0.0104 | 0.94 | Speed perturbation (0.9/1.0/1.1) | -0.05–-0.1 relative WER (literature-anchored) |
| ST2 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 0.85 | 0.0095 | 0.91 | Speed perturbation (0.9/1.0/1.1) | -0.05–-0.1 relative WER (literature-anchored) |
| ST3 | **label-noise-limited** | annotator agreement < floor, or held-out plateaus below floor with train/held-out gap small and confident-learning flag rate > 3% | 0.94 | 0.0078 | 0.78 | Confident-learning pass and re-annotation of flagged labels | 0.02–0.08 task metric (literature-anchored) |
| ST4 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 1.32 | 0.0097 | 0.86 | Speed perturbation (0.9/1.0/1.1) | -0.05–-0.1 relative WER (literature-anchored) |

Binding stratum: ST4. Comparison design: binding stratum ST4 diagnosed data-limited; highest-expected-effect admissible lever for that cause (cause map order).

### Two-arm comparison on ST4 at 1000 examples — lever: Speed perturbation (0.9/1.0/1.1) (single-seed)

| Arm | Configuration | M-a target improvement | M-b non-target regression (max) | Coverage | Compute to convergence (GPU h) |
|---|---|---|---|---|---|
| A | without Speed perturbation (0.9/1.0/1.1) | +0.0799 | 0.0000 | 92.0% | 2.55 |
| B | with Speed perturbation (0.9/1.0/1.1) | +0.0918 | 0.0000 | 92.0% | 2.316 |

Delta B−A +0.0119 vs two-arm MDE 0.1461: NOT detectable. Adoption evidence: **insufficient: delta +0.0119 below two-arm MDE 0.1461 at test_n=130; the recipe seat stays empty until the comparison is repeated with more test items or seeds**.

Eligibility: M-a parity within 0.005: True; M-b within objective ceiling 0.01: arm A True, arm B True. Eligible for adoption: **False**. Compute is reported, not gating. **Verdict: pending Owner ruling on the measured results (A17.6); no threshold pre-exists the evidence.**

### Quote for the full run

Recommended examples: 4,800 (ST1: 1,200, ST2: 1,200, ST3: 1,200, ST4: 1,200); 3 epochs; 17.88 GPU h. **Quote £65.8** (indicative band ±25% £49.35–£82.25 [estimated: statistical CI not available at this number of calibration points; band is a policy assumption, not a measurement]), spent so far £75.84, cap £1800, within budget: True.


### Operational plan (industry lens)

Owner seat: answering-service seat, RMS pilot. Rollback: previous admitted adapter MA-0904. Retrain cadence: quarterly or on trigger. [recalled] Receipt R06

| Stratum | Capture condition | Monitor | Coverage floor | Window | Trigger |
|---|---|---|---|---|---|
| ST1 | phone line, contact-centre headset | coverage rate weekly; confidence distribution | 97.0% | weekly | below floor two weeks running |
| ST2 | phone line | same | 95.0% | weekly | below floor two weeks running |
| ST3 | phone line and community-radio call-in (calibration material is radio; production is phone) | same, plus register-classifier share | 90.0% | weekly | below floor two weeks running |
| ST4 | phone line | same | 92.0% | weekly | below floor two weeks running |

### Value case (entrepreneur lens)

| Stratum | Value £/yr | Basis | Quoted cost £ | Ratio | Reachable |
|---|---|---|---|---|---|
| ST1 | 9,000 | calls served: 46% of 61k monthly calls × £0.32 handling saved per auto-served call, annualised at the floor | 18.11 | 497.1 | no |
| ST2 | 6,100 | same basis, 31% share | 18.11 | 336.9 | no |
| ST3 | 4,200 | same basis, 14% share; the client's stated pain point | 18.11 | 232.0 | no |
| ST4 | 1,800 | same basis, 9% share | 18.11 | 99.4 | no |

Phased path by value/cost: ST1 → ST2 → ST3 → ST4. Kill criteria: binding stratum unreachable within available material and no lever with expected effect ≥ gap; quote exceeds cap after phasing; diagnosis = leakage. [estimated] Receipt R06

## 7. Ablations

None run. The record is silent on ablations.

## 8. Limitations (four lenses)

- **Statistical (professor):** all calibration numbers are single-seed; CIs not reported at this number of points; MDE vs floor per stratum: ST1 3.8pp, ST2 5.4pp, ST3 8.8pp, ST4 10.3pp. What would change the conclusion: a second seed disagreeing beyond the prior seed SD.
- **Methodological (researcher):** one comparison, one lever (Speed perturbation (0.9/1.0/1.1)); no ablations; delta below two-arm MDE. What would change it: a repeat with ≥3 seeds or a larger sealed set on ST4.
- **Operational (industry):** calibration material may not match production capture on every stratum (see capture conditions); monitors are proposed, not yet live. What would change it: a production drift signal in the first month.
- **Economic (entrepreneur):** value figures are the owner's estimates [estimated]; costs are quotes at prior rates. What would change it: the binding stratum's curve projecting beyond available material.
- **Production base model**: named only at first census activation (A17.11); closes with registry bump after census.
- **Generalisation to non-RMS archives**: test set is RMS-only; closes with a second sealed test set from another estate.
- Strata not reachable within available material: ST1, ST2, ST3, ST4.

## 9. Negative results

None recorded in this run. A refused run's record is retained (WPW-7).

## Milestones

- MS1 [done] calibration evaluated on all four strata — owner: training manager
- MS2 [done] two-arm comparison numbers laid side by side with parity test — owner: training manager
- MS3 [done] quote with CI delivered and milestone list agreed — owner: objective owner
- MS4 [open] MOAC pack assembled for the full run — owner: training manager

## MOAC pack request

| Criterion | Source | Evidence | Status |
|---|---|---|---|
| M-a target-stratum improvement | A17.6 | comparison.arms[*].M_a_target_improvement | measured at calibration scale; full-run value pending |
| M-b non-target regression | A17.6 | comparison.arms[*].M_b_non_target_regression_max vs objective ceiling 0.01 | measured at calibration scale; full-run value pending |
| M-d lineage: recipe_version, base model, rights lineage | A17.3 | recipe_version pending Owner ruling; base_model models_registry.v0#whisper-tiny; rights lineage per manifest sha256:e684ce16b4cd7feafaa895451c9d2ed3d44e386acf23e148679b38f4a27167cc | partial: recipe_version not yet assigned |
| C8-held-out held-out evaluation thresholds per task | C.8.4 | sealed test set Stratified test set TS-ASR-04 v2, sealed 2026-09-25, 1,200 utterances, uncurated held-out | evidence pending full run |
| C8-repro seed-fixed reproducibility within tolerance | C.8.4 | seed-fixed re-run within tolerance; tolerance ±0.002 | policy stated; second-run evidence pending |
| C8-provenance provenance completeness: 100% classed with lawful basis | C.8.4 | manifest sha256:e684ce16b4cd7feafaa895451c9d2ed3d44e386acf23e148679b38f4a27167cc: 4800 examples, 100.0% classed, lawful basis present=True | met at manifest |
| C8-admission admission-test pre-check for the artefact | C.8.4 | admission pre-check runs on the artefact (C.6) | evidence pending artefact |

MOAC's full criteria set is versioned by ceremony (C.8 I-1); this pack supplies evidence per criterion and never a pass/fail Acceptance is MOAC's; no human in the path (#22).


## Completion certificate

not issued: full run not executed (policy.completion_certificate.issued_when). Template fields: run_id, objective_ref, recipe_version, compute_consumed_gpu_hours, data_touched_examples, manifest_hash, per_stratum_results, strata_failed, execution_mode, backend.


## Notebook

24 entries, hash-chained, head `sha256:09d339758105d831436b521d54916da5eac9352b3e75fb40182331dc2eff647a` (`notebook.jsonl`, WPW-3/4). Human contributions and CIF events are recorded by reference; correlation only.

---
*Instrument: training-studio (WPW-17). Authors are humans; this report names none until the objective owner signs.*
