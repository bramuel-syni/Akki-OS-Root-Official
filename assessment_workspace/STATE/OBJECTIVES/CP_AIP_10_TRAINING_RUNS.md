---
card_id: CP_AIP_10_TRAINING_RUNS
title: AIP v1.0 §11.6 Training-Runs commissioned-job compose-boundary (quote-before-start + metered-during + completion-certificate + failed-stratum-plain-reporting) + §11.5 per-example-provenance-through-training + Ruling (b) Census-Autonomy-Service registration seam · Item 5.10 CP-AIP-10 · LAST BY CONSTRUCTION
ratified_at_utc: 2026-02-23T11:10:00Z
ratified_by: Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO) 'run CP-AIP-5 → CP-AIP-10 sequentially · HALT after CP-AIP-10 for full plane completion report' AMENDED per §6.9 cadence amendment to REPORT-AND-CONTINUE + RUN-TO-COMPLETION mandate 2026-02-23 + Ruling (b) AKKI-RUNS-IT verbatim (2026-02-23) 'ALL Akki-based training + census EXECUTION runs INSIDE the live Akki OS system via the Census Autonomy Service / commissioned-job path within the tenant compute + custody boundary · Training compute + model weights + labelled corpus never leave Akki boundary · E1 role = build and WIRE the seams INTO the Census Autonomy Service so Akki runs them autonomously — then STEP BACK · E1 pod is never the training host and never a data path'
card_sha256: f1cd77d7c2cfae3bd68b4aa21dc7cfc764f076c1c5c962049771f8e8d8fb5246
milestone_status: OPEN (Item 5.10 CP-AIP-10 · CP-AIP-9 SEALED · this-CP LAST BY CONSTRUCTION · REPORT-AND-CONTINUE into SO-6.9 wave post-seal per §6.9 cadence amendment · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-AIP-10-TRAINING-RUNS · AIP v1.0 §11.6 + §11.5 + Ruling (b) Census-Autonomy-Service seam

## OBJECTIVE

Land the additive Training-Runs commissioned-job compose-boundary as pure §1.2 modality-extension of sealed CP-AIP-8 `SamplingReflectionBoundaryResult_v1` (S&R output carrying calibration + milestone list + confidence-interval cost quote) + sealed CP-AIP-7 `PlannerBoundaryResult_v1` (planner output carrying test-set-resolved + population + additive stratum set) + sealed CP-M6-7-3 `CostQuoteWithCI` (CI-bearing quote per §11.4 P188) + sealed CP-AIP-4 `pretraining_contract_v1` `HONEST_GAP_V1_POSTURE` marker (§3.2 P049 commissioned-job cost-receipt gate). Zero sealed-carrier edit per SO §3.8.

The compose-boundary binds eight structural rules (RED-first invariants listed in MUST DO).

`canon_ref: AIP v1.0 §11.6 P189a..P190e verbatim + §11.5 P185a..P187 verbatim + §1.2 modality-extension + §1.4 measure-don't-assert + §1.5 unrepresentable-not-policed + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23.`

## MUST DO

1. **§11.6 P189a verbatim · run-refused-without-passed-calibration** — enforced by `test_training_run_refused_without_passed_calibration_11_6`.
2. **§11.6 P190a..d verbatim · completion-certificate-4-field-shape** — 4 Final field names in this exact order: `compute_consumed`, `data_touched`, `manifest_hash`, `per_stratum_results`. Enforced by `test_completion_certificate_carries_exactly_four_verbatim_fields_11_6`.
3. **§11.6 P190e verbatim · failed-strata-plain-reporting** — `PerStratumResult_v1.status` is `Literal["passed", "failed"]`; render refuses if any stratum absent; failed rows identical in surface shape to passed rows. Enforced by `test_failed_strata_reported_as_plainly_as_passed_ones_11_6`.
4. **§11.5 P185a verbatim · per-example-provenance-required** — `TrainingManifestExampleRow_v1.provenance_ref` non-empty; `TrainingManifest_v1.append_row` refuses empty. Enforced by `test_training_manifest_refuses_row_without_provenance_ref_11_5`.
5. **§11.5 P187 verbatim · rights-lapse-enumerable-model-ids** — `RightsLapseDetector_v1.enumerate_affected_model_ids` returns `frozenset[str]`. Enforced by `test_rights_lapse_yields_enumerable_affected_model_ids_11_5`.
6. **Ruling (b) verbatim · Census-Autonomy-Service registration seam + pod-never-data-path** — refuses `pod://` or `/app/` prefixed refs. Enforced by `test_training_run_census_autonomy_registration_pod_never_data_path_ruling_b`.
7. **§1.2 no-redeclaration** of sealed symbols. Enforced by `test_no_redeclaration_of_sealed_symbols_1_2`.
8. **§1.4 + §11.6 heavy-fine-tune-deferred-posture** marker `HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE`. Enforced by `test_heavy_fine_tune_deferred_to_commissioned_job_posture_marker_present_11_6_1_4`.

## MUST NOT DO

- No edit to sealed CP-AIP-1..9 modules.
- No heavy fine-tune run executed in E1's pod at this seal (Ruling (b) verbatim: pod is never training host or data path).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3.

## NEW ADDITIVE MODULES

`backend/services/audio_plane_v1/training_run_boundary_v1.py` (§1.2 modality-extension).

Test file: `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py` (8 RED-first pins).

## SEALED CARRIERS TO NOT EDIT

- CP-AIP-7/8/9 audio_plane_v1 boundary modules · CP-M6-7-3 CostQuoteWithCI · CP-AIP-4 pretraining_contract_v1.

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_training_run_refused_without_passed_calibration_11_6`
2. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_completion_certificate_carries_exactly_four_verbatim_fields_11_6`
3. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_failed_strata_reported_as_plainly_as_passed_ones_11_6`
4. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_training_manifest_refuses_row_without_provenance_ref_11_5`
5. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_rights_lapse_yields_enumerable_affected_model_ids_11_5`
6. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_training_run_census_autonomy_registration_pod_never_data_path_ruling_b`
7. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_no_redeclaration_of_sealed_symbols_1_2`
8. `backend/tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_heavy_fine_tune_deferred_to_commissioned_job_posture_marker_present_11_6_1_4`

## LEDGER CHECK

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.10 CP-AIP-10-TRAINING-RUNS and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary.**

## STOP

- STOP on any `SPEC-CONFLICT-<n>` discovered mid-slice (log to `DECISIONS.md` verbatim, report, do not improvise).
- STOP on hard custody/gate violation.
- STOP if the `Ledger check — this seal implements Item 5.10 and nothing else` line cannot be written truthfully at Commit-A/B (per EXECUTION_ORDER anti-drift standing guard §5).
- STOP if any sealed carrier (CP-AIP-1..9 · CP-M6-7-3 · CP-AIP-4 pretraining_contract_v1 · sampling_reflection_boundary_v1 · target_outcome_planner_boundary_v1 · commission_view_boundary_v1) would need edit — additive-only per SO §3.8; refactor is BANNED.
- STOP if RED_pre does not authentically fail with `ModuleNotFoundError`/`ImportError`/`AttributeError` right-reason on all 8 pins.
- STOP if double-green sweep stripped_sha256 differs between sweep_A and sweep_B (byte-identity required).

## ANCHORS

- **Spec anchors (verbatim):**
  - AIP v1.0 §11.6 P189a: run refused without passed §11.2 calibration.
  - §11.6 P190a-d: completion certificate carries `compute_consumed` + `data_touched` + `manifest_hash` + `per_stratum_results`.
  - §11.6 P190e: failed strata reported "as plainly as passed ones".
  - §11.5 P185a: every training example carries its provenance into the training manifest.
  - §11.5 P187: rights lapse yields the enumerable set of affected models.
  - §1.2: modality-extension composes sealed symbols; no redeclaration.
  - §1.4: measure-don't-assert; measured-cost-receipt discipline.
  - §1.5: unrepresentable-not-policed (structural refusal patterns).
- **Owner anchors:**
  - Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 · `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md` · E1 wires seams into Census Autonomy Service · Akki executes · E1's pod NEVER training host or data path.
  - Cadence directive verbatim 2026-02-23 CP-AIP-4 GO · sequential CP-AIP-5 → CP-AIP-10 · AMENDED per §6.9 cadence amendment to REPORT-AND-CONTINUE.
  - RUN-TO-COMPLETION mandate verbatim 2026-02-23 · `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md`.
  - RMS CREDS 3 + `google-transcripts/` labelled multilingual ASR corpus verbatim 2026-02-23 · `STATE/OWNER_DROPS/rms_creds_3_and_multilingual_corpus_20260223/DROP.md` · feeds SO-6.9 LID wave + CP-AIP-10 training linkage.
- **Sealed-carrier anchors (composed UNCHANGED per SO §3.8):**
  - `backend/services/audio_plane_v1/sampling_reflection_boundary_v1.py` (CP-AIP-8 · S&R boundary · calibration gate + full-run-quote-CI gate + milestone-list composition).
  - `backend/services/audio_plane_v1/target_outcome_planner_boundary_v1.py` (CP-AIP-7 · planner boundary · upstream).
  - `backend/services/audio_plane_v1/training_planner.py` (CP-M6-7-2/3 · `CostQuoteWithCI` · CI-bearing cost type).
  - `backend/services/perception/audio_codec/pretraining_contract_v1.py` (CP-AIP-4 · commissioned-job contract seat · `HONEST_GAP_V1_POSTURE` pattern this-CP follows).
  - `backend/services/audio_plane_v1/commission_view_boundary_v1.py` (CP-AIP-9 · orthogonal · not consumed at this boundary).

