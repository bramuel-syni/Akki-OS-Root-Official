---
card_id: CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY-20260223
ledger_item: Item 5.11.c of STATE/EXECUTION_ORDER.md
seal_family: SO §6.9 amendment §6 item 8 verbatim
opened_at_utc: 2026-02-23T13:55:00Z
milestone_status: OPEN-FOR-EXIT
card_sha256: ee0dad6f4e1f766b02e8a4a79df0e3272a5a2ee65399886f4b74405c64bbc7f9
---

# CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY — 3-wave census orchestration boundary

Owner canon anchor (SO §6.9 amendment §6 item 8 verbatim):

> "The census proceeds in its three waves — complete the walk with the
>  unmeasured register, the full B3 dimension set with the defensibility
>  matrix and sensitivity classification, then the perception pathway —
>  and language labels from item 4 enter it as overlay from the first run."

## Scope

Land the additive 3-wave orchestration boundary composing sealed
CP-SO-6.9-LID-WAVE overlay module. Ordered 3-tuple:
1. **Wave 1 — Unmeasured register** — `UnmeasuredRegisterWave_v1` (frozen · `dimensions_measured=False` per B5.4 shown-not-counted line).
2. **Wave 2 — B3 dimension set** — `B3DimensionSetWave_v1` carrying `b3_attachment_markedness` + `b3_genre_form` + `b3_corroboration` + `defensibility_matrix_rule_ref` (Canon 4 §5.1 qmatrix) + `sensitivity_class` (Canon 4 §5.1 + Canon 7 §3 conservative default).
3. **Wave 3 — Perception pathway** — `PerceptionPathwayWave_v1` carrying `lid_overlay_source_registration` (identity-check against sealed `WHISPER_LID_REGISTRATION` or `VOXLINGUA107_REGISTRATION`) + `lid_overlay_marker` Literal `INFERRED`/`unmeasured`.

Wave-out-of-order structurally refused. Unknown wave name refused. LID overlay
must trace to sealed registration (fabricated shapes refused). Ruling (b)
AKKI-RUNS-IT verbatim: `register_census_three_waves_as_census_autonomy_job`
refuses `pod://*` or `/app/*` prefixed refs.

## Sealed carriers composed (UNCHANGED per SO §3.8)

- `backend/services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE · `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `LidModelRegistration_v1`).

## New additive module

- `backend/services/audio_plane_v1/census_three_waves_v1.py` (~230 lines).

## Test module

- `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py` (10 RED-first invariant pins).

## EXIT — RED-first pytest node IDs (all 10 GREEN post-authorship)

```
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_census_three_waves_v1_three_waves_ordered_tuple_verbatim
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_unmeasured_register_wave_v1_frozen_dimensions_measured_false
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_b3_dimension_set_wave_v1_carries_defensibility_matrix_and_sensitivity
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_perception_pathway_wave_v1_carries_lid_overlay_from_first_run
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_wave_out_of_order_refused_at_boundary
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_unknown_wave_name_refused
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_lid_overlay_from_first_run_only_accepts_sealed_registration
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_register_census_three_waves_as_census_autonomy_job_refuses_pod_prefixed_refs
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_lid_overlay_from_first_run_posture_marker_present
tests/invariants/test_cp_census_three_waves_with_lid_overlay.py::test_no_redeclaration_of_sealed_lid_wave_symbols_1_2
```

## Ratchet

6340 → 6350 (+10 canonical measured). Double-green byte-identical stripped_sha256
`c10b70efc5ab8c6086e83f3fb2f862bdb61ece2977bfee3684d882239c35ca88` IDENTICAL both sweeps
(6359 passed / 13 skipped / 0 failed / 520 warnings / ~199s each).

## Ledger check

This seal implements Item 5.11.c of `STATE/EXECUTION_ORDER.md` and nothing else.
