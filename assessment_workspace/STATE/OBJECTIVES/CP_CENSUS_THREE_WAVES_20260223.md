---
card_id: CP_CENSUS_THREE_WAVES_20260223
title: 3-wave census orchestration boundary with LID overlay from first run · Item 5.11.c
ratified_at_utc: 2026-02-23T14:00:00Z
ratified_by: Owner drop verbatim SO §6.9 amendment §6 item 8 (2026-02-23) — 'The census proceeds in its three waves — complete the walk with the unmeasured register, the full B3 dimension set with the defensibility matrix and sensitivity classification, then the perception pathway — and language labels from item 4 enter it as overlay from the first run.' + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (pod is never data path).
card_sha256: d857f2278902ac4d86e1bf4096330056b50bca3a1962810aa4432d2d46cfa133
milestone_status: SEALED (Item 5.11.c · 3rd item of Item 5.11 wave · CLOSED 2026-02-23T~14:15Z · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY-20260223 · 3-wave census orchestration boundary

## OBJECTIVE

Land the additive 3-wave census orchestration boundary as pure §1.2 modality-extension composing sealed CP-SO-6.9-LID-WAVE `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py`. Enforce the owner-verbatim ordered 3-tuple `(unmeasured_register, b3_dimension_set, perception_pathway)` with structural wave-out-of-order refusal at boundary. LID overlay labels from CP-SO-6.9-LID-WAVE sealed registrations enter Wave 3 as overlay from first run; fabricated shape-equivalent registrations are refused (identity-check). Ruling (b) AKKI-RUNS-IT verbatim honored structurally: `register_census_three_waves_as_census_autonomy_job` refuses `pod://*` and `/app/*` prefixed refs. Zero sealed-carrier edit per SO §3.8.

`canon_ref: SO §6.9 amendment 2026-02-23 §6 item 8 verbatim + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 + Canon 4 §5.1 detection layer + verdict layer + Canon 7 §3 sensitivity conservative default + B5.4 shown-not-counted line + §1.2 modality-extension.`

## MUST DO

1. **`CENSUS_THREE_WAVES` Final ordered 3-tuple** verbatim `("unmeasured_register", "b3_dimension_set", "perception_pathway")`. Enforced by `test_census_three_waves_v1_three_waves_ordered_tuple_verbatim`.
2. **`UnmeasuredRegisterWave_v1` frozen dataclass** with `register_entries_count: int`, `dimensions_measured: bool` (False at Wave 1 exit per B5.4 shown-not-counted line), `completed_at_utc: str`. Enforced by `test_unmeasured_register_wave_v1_frozen_dimensions_measured_false`.
3. **`B3DimensionSetWave_v1` frozen dataclass** carrying `b3_attachment_markedness`, `b3_genre_form`, `b3_corroboration`, `defensibility_matrix_rule_ref` (Canon 4 §5.1 qmatrix), `sensitivity_class` (Canon 4 §5.1 + Canon 7 §3). Enforced by `test_b3_dimension_set_wave_v1_carries_defensibility_matrix_and_sensitivity`.
4. **`PerceptionPathwayWave_v1` frozen dataclass** carrying `lid_overlay_source_registration: LidModelRegistration_v1` and `lid_overlay_marker: Literal["INFERRED","unmeasured"]`. Enforced by `test_perception_pathway_wave_v1_carries_lid_overlay_from_first_run`.
5. **Wave-out-of-order refused at boundary** — `open_wave(name, prior_wave_completed)` raises `CensusWaveOutOfOrderError`. Enforced by `test_wave_out_of_order_refused_at_boundary`.
6. **Unknown wave name refused** — `CensusWaveNameRefused`. Enforced by `test_unknown_wave_name_refused`.
7. **LID overlay identity-check against sealed registrations** — `lid_overlay_source_is_sealed_registration` refuses fabricated shape-equivalent objects. Enforced by `test_lid_overlay_from_first_run_only_accepts_sealed_registration`.
8. **Ruling (b) `pod://*` / `/app/*` refusal at registration seam** — `register_census_three_waves_as_census_autonomy_job` raises `PodIsNeverDataPathError`. Enforced by `test_register_census_three_waves_as_census_autonomy_job_refuses_pod_prefixed_refs`.
9. **`LID_OVERLAY_ENTERS_FROM_FIRST_RUN_POSTURE` Final marker** verbatim of SO §6.9 amendment §6 item 8. Enforced by `test_lid_overlay_from_first_run_posture_marker_present`.
10. **§1.2 no-redeclaration** of sealed CP-SO-6.9-LID-WAVE symbols (`LidModelRegistration_v1`, `OverlayLidDetection_v1`, `WHISPER_LID_REGISTRATION`, `VOXLINGUA107_REGISTRATION`) + sealed CP-M6-3-1 (`CharacterRegister`, `CharacterEntry`). Enforced by `test_no_redeclaration_of_sealed_lid_wave_symbols_1_2`.

## MUST NOT DO

- No edit to sealed `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE closed).
- No edit to sealed `services/audio_plane_v1/character_register.py` (CP-M6-3-1 closed).
- No permission of a wave name outside `CENSUS_THREE_WAVES`.
- No permission of a `lid_overlay_source_registration` that is not identity-equal to `WHISPER_LID_REGISTRATION` or `VOXLINGUA107_REGISTRATION`.
- No permission of a `pod://*` or `/app/*` prefixed engine_response_queue_ref or data_source_adapter_ref (Ruling (b) pod-never-data-path).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3.

## EXIT

RED-first invariant node IDs (all 10 GREEN post-authorship · 0.73s):

1. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_census_three_waves_v1_three_waves_ordered_tuple_verbatim`
2. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_unmeasured_register_wave_v1_frozen_dimensions_measured_false`
3. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_b3_dimension_set_wave_v1_carries_defensibility_matrix_and_sensitivity`
4. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_perception_pathway_wave_v1_carries_lid_overlay_from_first_run`
5. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_wave_out_of_order_refused_at_boundary`
6. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_unknown_wave_name_refused`
7. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_lid_overlay_from_first_run_only_accepts_sealed_registration`
8. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_register_census_three_waves_as_census_autonomy_job_refuses_pod_prefixed_refs`
9. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_lid_overlay_from_first_run_posture_marker_present`
10. `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_no_redeclaration_of_sealed_lid_wave_symbols_1_2`

Ratchet: 6340 → 6350 (+10 canonical measured). Double-green byte-identical stripped_sha256 `c10b70efc5ab8c6086e83f3fb2f862bdb61ece2977bfee3684d882239c35ca88` IDENTICAL both sweeps (6359 passed / 13 skipped / 0 failed / 520 warnings / ~199s each).

## STOP

- STOP on any `SPEC-CONFLICT-<n>` discovered mid-slice.
- STOP on hard custody/gate violation.
- STOP if any sealed carrier would need edit.
- STOP if RED_pre does not authentically fail with `ModuleNotFoundError`/`ImportError` right-reason on all 10 pins.
- STOP if double-green sweep stripped_sha256 differs between sweeps.

## ANCHORS

- SO §6.9 amendment 2026-02-23 §6 item 8 verbatim.
- Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (banked `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md`).
- Sealed CP-SO-6.9-LID-WAVE `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (`LidModelRegistration_v1` + `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `OverlayLidDetection_v1`).
- Sealed CP-M6-3-1 `services/audio_plane_v1/character_register.py` (`CharacterEntry` + `CharacterRegister`).
- Canon 4 §5.1 detection + verdict layer (`qmatrix` rule ref).
- Canon 7 §3 sensitivity classification conservative default.
- B5.4 shown-not-counted line (overlay detections never flow into counted measures pre-regime-flip).
- SO §3.8 additive-only.
- SO §3.3 5-commit seal.
- SO §6.9(5) AMENDED bundle-based continuity.

## LEDGER CHECK

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.11.c CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary.**
