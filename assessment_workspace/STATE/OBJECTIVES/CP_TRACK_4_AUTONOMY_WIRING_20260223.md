---
card_id: CP_TRACK_4_AUTONOMY_WIRING_20260223
title: Track-4 autonomy wiring — register LID pass + corpus census + training seam as Census Autonomy Service jobs; autonomy engine run-log receipt = EXIT EVIDENCE · Item 5.11.e
ratified_at_utc: 2026-02-23T14:50:00Z
ratified_by: Owner drop verbatim 2026-02-23 SO §6.9 amendment §6 item 6 — 'Register LID pass + corpus census + training seam as Census Autonomy Service jobs. Verification of autonomy pickup (receipt from the autonomy engine's run log showing the job ran) is the EXIT EVIDENCE for each such wiring seal. E1 wires the seams INTO the Census Autonomy Service so Akki runs them autonomously — then STEPS BACK.' + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (E1's pod is NEVER the training host and NEVER a data path).
card_sha256: 7f880346971520de65a6621041631c9bbe54df8862da2878ebd1b44c52dd26b7
milestone_status: OPEN (Item 5.11.e · opens immediately post CP-TENANT-SEPARATION seal · 5th item of Item 5.11 wave · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-TRACK-4-AUTONOMY-WIRING-20260223 · register LID pass + corpus census + training seam as Census Autonomy Service jobs; autonomy engine run-log receipt = EXIT EVIDENCE

## OBJECTIVE

Land the additive Track-4 boundary as pure §1.2 modality-extension composing three sealed carriers: CP-SO-6.9-LID-WAVE `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (`WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION`); CP-CENSUS-THREE-WAVES `services/audio_plane_v1/census_three_waves_v1.py` (`register_census_three_waves_as_census_autonomy_job`); CP-AIP-10-TRAINING-RUNS `services/audio_plane_v1/training_run_boundary_v1.py` (`TrainingRunCensusAutonomyRegistration_v1` + `register_training_run_as_census_autonomy_job`). Bind the three job kinds as a Literal-closed tuple. Bind the pod-is-never-data-path refusal structurally at every registration seat. Emit the autonomy-engine run-log receipt as the EXIT EVIDENCE — the LIVE `services/census_autonomy/engine.py` `enqueue_on_demand_run` + `run_bounded_census` chain must actually pick up and execute the three wired jobs. Zero sealed-carrier edit per SO §3.8. Ruling (b) AKKI-RUNS-IT verbatim honored structurally: E1 wires the seams INTO Census Autonomy Service; pod is never a training host or data path.

`canon_ref: SO §6.9 amendment 2026-02-23 §6 item 6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 + §1.2 modality-extension + §1.5 unrepresentable-not-policed (refusal exceptions rather than silent bypass).`

## MUST DO

1. **`TRACK_4_JOB_KINDS` Final Literal-closed 3-tuple** — `("lid_pass", "census_three_waves", "training_runs")`. Enforced by `test_job_kind_literal_closed_three_kinds`.
2. **`Track4LidPassRegistration_v1` frozen carrier composing sealed WHISPER_LID_REGISTRATION + VOXLINGUA107_REGISTRATION by identity** — Enforced by `test_lid_pass_registration_seat_via_track_4`.
3. **`Track4AllJobsRegistered_v1` frozen aggregate carrier composing 3 sealed registration seats** — `total_jobs_registered=3`. Enforced by `test_track_4_wires_all_three_seams_registration_aggregate`.
4. **`AutonomyEngineRunReceipt_v1` frozen EXIT-EVIDENCE carrier** — fields job_kind + run_id + started_at_utc + finished_at_utc + status + provenance_ref. Enforced by `test_autonomy_engine_run_receipt_shape_frozen`.
5. **`PodIsNeverDataPathAtTrack4Error` refusal on `pod://*` + `/app/*` prefixes at every registration seat** (Ruling (b) verbatim). Enforced by `test_pod_prefix_refused_at_lid_registration_seat`.
6. **`Track4JobKindRefused` refusal on job_kind not in TRACK_4_JOB_KINDS** — Enforced by `test_job_kind_literal_closed_three_kinds`.
7. **`AutonomyEngineRunReceiptStatusRefused` refusal on status not in Literal `completed`/`failed`/`refused`** — Enforced by `test_autonomy_engine_run_receipt_status_literal_closed`.
8. **`TRACK_4_AUTONOMY_WIRING_POSTURE` Final marker** citing owner verbatim + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` Final marker citing Ruling (b) verbatim + `E1_STEPS_BACK_AFTER_WIRING_POSTURE` Final marker citing 'then STEPS BACK' verbatim. Enforced by `test_track_4_autonomy_wiring_posture_marker_present` + `test_pod_is_never_data_path_posture_track_4_marker_present` + `test_track_4_e1_steps_back_posture_marker_present`.
9. **§1.2 no-redeclaration** of sealed CP-SO-6.9-LID-WAVE + CP-CENSUS-THREE-WAVES + CP-AIP-10-TRAINING-RUNS symbols (LidModelRegistration_v1, OverlayLidDetection_v1, WHISPER_LID_REGISTRATION, VOXLINGUA107_REGISTRATION, LidAdmissionGate_v1, CENSUS_THREE_WAVES, UnmeasuredRegisterWave_v1, B3DimensionSetWave_v1, PerceptionPathwayWave_v1, CensusThreeWavesCensusAutonomyRegistration_v1, TrainingRunCensusAutonomyRegistration_v1, CompletionCertificate_v1, TrainingManifest_v1). Enforced by `test_no_redeclaration_of_sealed_symbols_1_2`.
10. **EXIT EVIDENCE — LIVE Census Autonomy engine executes all 3 wired jobs end-to-end**: `register_all_three_track_4_jobs` produces a Track4AllJobsRegistered_v1 aggregate; `enqueue_on_demand_run` (LIVE engine.py) writes each job to `phase0/census_autonomy_state/pending/<ts>_<id>.json`; `run_bounded_census` executes each and writes a persisted result at `phase0/census_autonomy_state/results/<ts>_<id>_result.json`; `emit_autonomy_engine_run_receipt` records an AutonomyEngineRunReceipt_v1 per job composing the live engine's status; 3 per-job machine-readable JSON receipts + 1 composite seal-level exit-evidence receipt land at `backend/phase0/track_4_autonomy_engine_run_receipts/*.json`.

## MUST NOT DO

- No edit to sealed `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE closed).
- No edit to sealed `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES closed).
- No edit to sealed `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS closed).
- No edit to sealed `services/census_autonomy/engine.py` (R-106 sealed engine).
- No permission of `pod://*` or `/app/*` prefixed `engine_response_queue_ref` or `data_source_adapter_ref` at any Track-4 registration seat.
- No permission of any `job_kind` outside `TRACK_4_JOB_KINDS`.
- No permission of any `status` outside `completed`/`failed`/`refused` Literal at `AutonomyEngineRunReceipt_v1`.
- No redeclaration of any sealed CP-* symbol (§1.2 no-redeclaration).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3 (bans).

## NEW ADDITIVE MODULES

`backend/services/census_autonomy/track_4_autonomy_wiring_v1.py` (§1.2 modality-extension · ~283 lines · `TRACK_4_JOB_KINDS` + `Track4LidPassRegistration_v1` + `Track4AllJobsRegistered_v1` + `AutonomyEngineRunReceipt_v1` + `Track4BoundaryRefused` base + `PodIsNeverDataPathAtTrack4Error` + `Track4JobKindRefused` + `AutonomyEngineRunReceiptStatusRefused` refusal subclasses + `TRACK_4_AUTONOMY_WIRING_POSTURE` + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` + `E1_STEPS_BACK_AFTER_WIRING_POSTURE` + `register_lid_pass_as_census_autonomy_job` + `register_all_three_track_4_jobs` + `emit_autonomy_engine_run_receipt` boundary callables).

Test file: `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py` (10 RED-first pins).

Exit-evidence generator: `/app/assessment_workspace/tools/generate_track_4_autonomy_run_receipts.py` (analysis/evidence script per SO §3.8 · runs LIVE Census Autonomy engine end-to-end on 3 wired jobs).

## SEALED CARRIERS TO NOT EDIT

- CP-SO-6.9-LID-WAVE `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (Item 5.11.a sealed 2026-02-23 · `LidModelRegistration_v1` + `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `OverlayLidDetection_v1` + `LidAdmissionGate_v1` + `LidRegimePromotionByReceiptedAct_v1` + `HuggingFacePullWrapperAntiToken_v1`).
- CP-CENSUS-THREE-WAVES `services/audio_plane_v1/census_three_waves_v1.py` (Item 5.11.c sealed 2026-02-23 · `CENSUS_THREE_WAVES` + `UnmeasuredRegisterWave_v1` + `B3DimensionSetWave_v1` + `PerceptionPathwayWave_v1` + `register_census_three_waves_as_census_autonomy_job`).
- CP-AIP-10-TRAINING-RUNS `services/audio_plane_v1/training_run_boundary_v1.py` (Item 5.10 sealed 2026-02-23 · `TrainingRunCensusAutonomyRegistration_v1` + `register_training_run_as_census_autonomy_job` + `CompletionCertificate_v1` + `TrainingManifest_v1`).
- CP-CENSUS-AUTONOMY `services/census_autonomy/engine.py` (R-106 sealed · `enqueue_on_demand_run` + `run_bounded_census` + `_write_result_receipt`).

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_track_4_wires_all_three_seams_registration_aggregate`
2. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_lid_pass_registration_seat_via_track_4`
3. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_pod_prefix_refused_at_lid_registration_seat`
4. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_autonomy_engine_run_receipt_shape_frozen`
5. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_autonomy_engine_run_receipt_status_literal_closed`
6. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_job_kind_literal_closed_three_kinds`
7. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_track_4_autonomy_wiring_posture_marker_present`
8. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_pod_is_never_data_path_posture_track_4_marker_present`
9. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_no_redeclaration_of_sealed_symbols_1_2`
10. `backend/tests/invariants/test_cp_track_4_autonomy_wiring.py::test_track_4_e1_steps_back_posture_marker_present`

## LIVE-ENGINE EXIT-EVIDENCE (owner verbatim exit clause)

- Machine-readable per-job JSON receipts at `backend/phase0/track_4_autonomy_engine_run_receipts/20260923T144803Z_{lid_pass,census_three_waves,training_runs}_engine_run_receipt.json` — each carries `engine_live_status=COMPLETE`, `wiring_receipt_status=completed`, `persisted_pending_job_path` + `persisted_result_or_refusal_path` pointing at LIVE engine on-disk state.
- Composite seal-level exit-evidence receipt at `backend/phase0/track_4_autonomy_engine_run_receipts/20260923T144803Z_seal_level_composite_exit_evidence.json` composing all 3 per-job receipts + the 3 posture markers + owner verbatim exit clause.

## STOP

Stop at owner ratification of this card. If Owner rules SPEC-CONFLICT-<n>, HALT and log it in DECISIONS.md as SPEC-CONFLICT with the conflict text verbatim + which sealed carrier / owner clause is violated + proposed resolution. Owner ruling required to unblock. Otherwise (no conflict), REPORT-AND-CONTINUE into Item 5.11.f (CP-AIP-ASSIST-CENSUS · six binding conditions verbatim) per RUN-TO-COMPLETION mandate 2026-02-23.

## ANCHORS

- **Owner canon (SO §6.9 amendment §6 item 6 verbatim 2026-02-23):** 'Register LID pass + corpus census + training seam as Census Autonomy Service jobs. Verification of autonomy pickup (receipt from the autonomy engine's run log showing the job ran) is the EXIT EVIDENCE for each such wiring seal. E1 wires the seams INTO the Census Autonomy Service so Akki runs them autonomously — then STEPS BACK. E1's pod is NEVER the training host and NEVER a data path.'
- **Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** 'E1 wires the seam INTO the Census Autonomy Service. Pod is never a data path.'
- **Sealed carriers extended (unchanged this seal per SO §3.8):** `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE Item 5.11.a) · `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES Item 5.11.c) · `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS Item 5.10) · `services/census_autonomy/engine.py` (R-106 sealed engine).
- **Standing Orders:** SO §3 RED-first · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §6.4 same-seal orthogonal fold-in gap-closure · SO §6.9 desk discipline (markers-over-refusal + one-sentence protected-objective on every refusal/hold/gate) · SO §6.9(5) AMENDED bundle-based continuity · SO §7 17-guard consolidated set.
- **Objective card hash-pin protocol:** `card_sha256` computed over card text with the `card_sha256:` frontmatter line removed (line-removed convention · pin protocol consistent with prior seals CP-TENANT-SEPARATION + CP-CENSUS-THREE-WAVES).
- **Ledger check:** this card ratifies `CP-TRACK-4-AUTONOMY-WIRING` and nothing else. Additive-only per SO §3.8.

## RATIFICATION

Owner drop 2026-02-23 SO §6.9 amendment §6 item 6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 authorised this seal by pre-ratified construction (RUN-TO-COMPLETION mandate). Card ratified at 2026-02-23T14:50:00Z. EXIT EVIDENCE landed same-seal via `generate_track_4_autonomy_run_receipts.py` executing LIVE engine end-to-end.
