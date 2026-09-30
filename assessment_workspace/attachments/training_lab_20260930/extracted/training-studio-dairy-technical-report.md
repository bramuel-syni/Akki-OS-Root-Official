# Technical report: Form-type classifier for DigiCow field records

Run `RP-dairy-record-classifier-001` · objective `dairy-record-classifier@1` · direction T1 · backend **stub** · status **stub**

> STUB RUN. none — stub metrics are a deterministic function of the seed (see policy.stub.note)

## 1. Problem and objective

document-classification on document; population by spoken register in 4 strata. Acceptance is two-dimensional per stratum (accuracy × coverage); gate policy: **gates**.

| Stratum | Share | Baseline acc. | Floor acc. | Gap (pp) | Floor cov. | Available examples |
|---|---|---|---|---|---|---|
| ST1 Milk log | 52.0% | 91.0% | 95.0% | 4.0 | 99.0% | 900 |
| ST2 Vet visit | 21.0% | 82.0% | 90.0% | 8.0 | 97.0% | 900 |
| ST3 Feed purchase | 17.0% | 79.0% | 88.0% | 9.0 | 96.0% | 900 |
| ST4 Breeding record | 10.0% | 64.0% | 80.0% | 16.0 | 94.0% | 900 |

[measured] Receipt R01, R03: DigiCow estate census 2026-09-26, form-type strata counts, table 2; Baseline evaluation BL-0929 on TS-DOC-02 v1, per-form-type accuracy

## 2. Data statement

| Material | Stratum | Examples | Class | Lawful basis | Hash |
|---|---|---|---|---|---|
| M01 DigiCow field records 2025–2026, scanned | ST1 | 900 | measured | contract | `sha256:a1b2…10` |
| M02 DigiCow field records 2025–2026, scanned | ST2 | 900 | measured | contract | `sha256:c3d4…22` |
| M03 DigiCow field records 2025–2026, photographed | ST3 | 900 | measured | contract | `sha256:e5f6…3a` |
| M04 DigiCow field records 2025–2026, photographed | ST4 | 900 | measured | contract | `sha256:0718…4c` |

Training manifest `sha256:1f7e1fa30df68b713aaf15979bf47f53e423de6de0be544f078401389cff63aa`: 3,600 examples, 100.0% classed, lawful basis present: True, refused: 0. Per-example provenance in `training-manifest.jsonl` (A17.20). Selection: deterministic: examples ordered by sha256(example_id); first N per stratum; each volume is a superset of the previous.

| Stratum | Examples | By class | By lawful basis |
|---|---|---|---|
| ST1 | 900 | measured 900 | contract 900 |
| ST2 | 900 | measured 900 | contract 900 |
| ST3 | 900 | measured 900 | contract 900 |
| ST4 | 900 | measured 900 | contract 900 |

Collection schema (unit: document image): fields example_id, image_ref, form_type, farm_pseudonym, capture, content_hash, basis_ref; quality gates {"min_long_edge_px": 1200, "max_skew_deg": 15, "legible_by_annotator": true}; labelling: form type by one annotator with a second on a 10% audit sample; disagreements to the classification authority as human contribution events; the occupation-boolean field is never transcribed (R07); admission: an image enters the manifest only with class, lawful basis, basis_ref and content hash; otherwise refused and counted. [estimated] Receipt R06: Objective owner sign-off memo OO-DC-2026-10-01

[measured] Receipt R04: Data-processing agreement DPA-DIGICOW-2025-11 and rights declaration RD-DC-02, owner-signed 2026-09-24

## 3. Baseline record

Baseline run Baseline evaluation BL-0929 on TS-DOC-02 v1, per-form-type accuracy on the sealed test set (Stratified test set TS-DOC-02 v1, sealed 2026-09-28, 800 images, uncurated held-out). Base model: `models_registry.v0#document-ocr-candidates`, role: PROPOSED-class candidates; resolved deterministically at wizard compile time (A20.12–14); production selection calibration decides among eligible candidates on measured fit (A20.13).

## 3b. Objective critique (four lenses)

Full table in `critique.md`. Escalations to the objective owner are listed there; the adopted verdict records which objections were accepted and which overruled.

## 4. Method

Adopted direction T1 under the recorded verdict `TV-2026-10-04-002`. Recipe seat: **empty** (training_params@v0). Calibration at [250, 500, 1000] examples per stratum, 2 epochs each; two-arm optimizer comparison on the smallest valid stratum (ST3).

## 5. Setup and reproducibility

Execution mode: stub. Reproducibility contract: seed-fixed re-run within tolerance (accuracy ±0.002, coverage ±0.002); canon: C.8 standard training criteria; C.20.10 reproducibility test. Seed `dairy-record-classifier/calibration/2026-10-04`. Calibration cost: estimated £59.52 [estimated, R05], actual £59.52 (18.6 GPU h) [stub]; comparison cost £16.32 [estimated, R05].

## 6. Results on held-out material

| Stratum | acc @250 | acc @500 | acc @1000 | cov @250 | cov @500 | cov @1000 | To acc. floor | To cov. floor | Binding | CI | Reachable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ST1 | 92.2% | 93.7% | 94.8% | 99.5% | 99.5% | 99.5% | 1083 | not on this curve | None | not reported (3 points) | no |
| ST2 | 83.8% | 85.8% | 87.2% | 97.7% | 98.4% | 98.7% | 3022 | 90 | accuracy | not reported (3 points) | no |
| ST3 | 81.8% | 85.3% | 88.4% | 96.8% | 97.2% | 97.7% | 914 | 75 | accuracy | not reported (3 points) | no |
| ST4 | 66.9% | 69.3% | 72.3% | 91.4% | 92.2% | 92.9% | 7456 | 2710 | accuracy | not reported (3 points) | no |

[stub] Evaluated on Stratified test set TS-DOC-02 v1, sealed 2026-09-28, 800 images, uncurated held-out. Failed strata are reported as plainly as passed ones.

### Diagnosis per stratum (professor names the cause; researcher picks the lever)

| Stratum | Cause | Test | Curve slope ratio | Train/held-out gap | Annotator agreement | First lever | Expected effect (class) |
|---|---|---|---|---|---|---|---|
| ST1 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 0.69 | 0.0098 | 0.96 | Geometric and photometric augmentation (rotation, skew, blur, exposure) | 0.02–0.06 accuracy (practice-anchored) |
| ST2 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 0.72 | 0.0101 | 0.9 | Geometric and photometric augmentation (rotation, skew, blur, exposure) | 0.02–0.06 accuracy (practice-anchored) |
| ST3 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 0.88 | 0.0101 | 0.88 | Geometric and photometric augmentation (rotation, skew, blur, exposure) | 0.02–0.06 accuracy (practice-anchored) |
| ST4 | **data-limited** | curve still rising at the last volume (slope > 0.5 × first-segment slope) and train/held-out gap small | 1.26 | 0.0095 | 0.83 | Geometric and photometric augmentation (rotation, skew, blur, exposure) | 0.02–0.06 accuracy (practice-anchored) |

Binding stratum: ST4. Comparison design: binding stratum ST4 diagnosed data-limited; highest-expected-effect admissible lever for that cause (cause map order).

### Two-arm comparison on ST3 at 1000 examples — lever: Geometric and photometric augmentation (rotation, skew, blur, exposure) (single-seed)

| Arm | Configuration | M-a target improvement | M-b non-target regression (max) | Coverage | Compute to convergence (GPU h) |
|---|---|---|---|---|---|
| A | without Geometric and photometric augmentation (rotation, skew, blur, exposure) | +0.0936 | 0.0000 | 97.7% | 2.55 |
| B | with Geometric and photometric augmentation (rotation, skew, blur, exposure) | +0.1213 | 0.0000 | 97.7% | 2.233 |

Delta B−A +0.0277 vs two-arm MDE 0.121: NOT detectable. Adoption evidence: **insufficient: delta +0.0277 below two-arm MDE 0.121 at test_n=140; the recipe seat stays empty until the comparison is repeated with more test items or seeds**.

Eligibility: M-a parity within 0.005: True; M-b within objective ceiling 0.01: arm A True, arm B True. Eligible for adoption: **False**. Compute is reported, not gating. **Verdict: pending Owner ruling on the measured results (A17.6); no threshold pre-exists the evidence.**

### Quote for the full run

Recommended examples: 2,700 (ST2: 900, ST3: 900, ST4: 900); 3 epochs; 10.32 GPU h. **Quote £37.98** (indicative band ±25% £28.48–£47.47 [estimated: statistical CI not available at this number of calibration points; band is a policy assumption, not a measurement]), spent so far £75.84, cap £600, within budget: True.


### Operational plan (industry lens)

Owner seat: census classification seat, DigiCow. Rollback: rule-based classifier v3. Retrain cadence: on new form version (census signal). [recalled] Receipt R06

| Stratum | Capture condition | Monitor | Coverage floor | Window | Trigger |
|---|---|---|---|---|---|
| ST1 | scan | recall on weekly audited sample | 99.0% | weekly | below floor two weeks running |
| ST2 | scan | same | 97.0% | weekly | below floor two weeks running |
| ST3 | photo | same, capture mix | 96.0% | weekly | below floor two weeks running |
| ST4 | photo | same, capture mix | 94.0% | weekly | below floor two weeks running |

### Value case (entrepreneur lens)

| Stratum | Value £/yr | Basis | Quoted cost £ | Ratio | Reachable |
|---|---|---|---|---|---|
| ST1 | 5,200 | forms auto-classified: 52% of 24k forms/yr × £0.42 manual classification | — | — | no |
| ST2 | 2,100 | same basis, 21% | 14.13 | 148.6 | no |
| ST3 | 1,700 | same basis, 17% | 14.13 | 120.3 | no |
| ST4 | 1,000 | same basis, 10%; feeds breeding-record extraction downstream | 14.13 | 70.8 | no |

Phased path by value/cost: ST2 → ST3 → ST4. Kill criteria: binding stratum unreachable within available material and no lever with expected effect ≥ gap; quote exceeds cap after phasing; diagnosis = leakage. [estimated] Receipt R06

## 7. Ablations

None run. The record is silent on ablations.

## 8. Limitations (four lenses)

- **Statistical (professor):** all calibration numbers are single-seed; CIs not reported at this number of points; MDE vs floor per stratum: ST1 3.5pp, ST2 7.3pp, ST3 8.6pp, ST4 13.3pp. What would change the conclusion: a second seed disagreeing beyond the prior seed SD.
- **Methodological (researcher):** one comparison, one lever (Geometric and photometric augmentation (rotation, skew, blur, exposure)); no ablations; delta below two-arm MDE. What would change it: a repeat with ≥3 seeds or a larger sealed set on ST3.
- **Operational (industry):** calibration material may not match production capture on every stratum (see capture conditions); monitors are proposed, not yet live. What would change it: a production drift signal in the first month.
- **Economic (entrepreneur):** value figures are the owner's estimates [estimated]; costs are quotes at prior rates. What would change it: the binding stratum's curve projecting beyond available material.
- **Handwritten variants outside the four form types**: not in the census axis; closes with census re-run with an 'other' form type.
- **Production document model**: resolved at compile time among PROPOSED candidates; closes with calibration outcome recorded per A20.13.
- Strata not reachable within available material: ST1, ST2, ST3, ST4.

## 9. Negative results

None recorded in this run. A refused run's record is retained (WPW-7).

## Milestones

- MS1 [done] calibration evaluated on all four form types — owner: training manager
- MS2 [done] two-arm comparison laid side by side with eligibility test — owner: training manager
- MS3 [done] quote with range delivered and milestone list agreed — owner: objective owner
- MS4 [open] MOAC pack assembled for the full run — owner: training manager

## MOAC pack request

| Criterion | Source | Evidence | Status |
|---|---|---|---|
| M-a target-stratum improvement | A17.6 | comparison.arms[*].M_a_target_improvement | measured at calibration scale; full-run value pending |
| M-b non-target regression | A17.6 | comparison.arms[*].M_b_non_target_regression_max vs objective ceiling 0.01 | measured at calibration scale; full-run value pending |
| M-d lineage: recipe_version, base model, rights lineage | A17.3 | recipe_version pending Owner ruling; base_model models_registry.v0#document-ocr-candidates; rights lineage per manifest sha256:1f7e1fa30df68b713aaf15979bf47f53e423de6de0be544f078401389cff63aa | partial: recipe_version not yet assigned |
| C8-held-out held-out evaluation thresholds per task | C.8.4 | sealed test set Stratified test set TS-DOC-02 v1, sealed 2026-09-28, 800 images, uncurated held-out | evidence pending full run |
| C8-repro seed-fixed reproducibility within tolerance | C.8.4 | seed-fixed re-run within tolerance; tolerance ±0.002 | policy stated; second-run evidence pending |
| C8-provenance provenance completeness: 100% classed with lawful basis | C.8.4 | manifest sha256:1f7e1fa30df68b713aaf15979bf47f53e423de6de0be544f078401389cff63aa: 3600 examples, 100.0% classed, lawful basis present=True | met at manifest |
| C8-admission admission-test pre-check for the artefact | C.8.4 | admission pre-check runs on the artefact (C.6) | evidence pending artefact |

MOAC's full criteria set is versioned by ceremony (C.8 I-1); this pack supplies evidence per criterion and never a pass/fail Acceptance is MOAC's; no human in the path (#22).


## Completion certificate

not issued: full run not executed (policy.completion_certificate.issued_when). Template fields: run_id, objective_ref, recipe_version, compute_consumed_gpu_hours, data_touched_examples, manifest_hash, per_stratum_results, strata_failed, execution_mode, backend.


## Notebook

25 entries, hash-chained, head `sha256:8bfa82a1b2d67c2163828b2f22cc4c4760ce7c91dc6aa642dcccb29895d2bdce` (`notebook.jsonl`, WPW-3/4). Human contributions and CIF events are recorded by reference; correlation only.

---
*Instrument: training-studio (WPW-17). Authors are humans; this report names none until the objective owner signs.*
