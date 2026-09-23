# CP-TRACK-4-AUTONOMY-WIRING · comprehensive receipt · Item 5.11.e · 2026-02-23T14:50Z

## OWNER CANON ANCHOR (VERBATIM)

**SO §6.9 amendment §6 item 6 verbatim 2026-02-23:**

> "Register LID pass + corpus census + training seam as Census Autonomy
>  Service jobs. Verification of autonomy pickup (receipt from the
>  autonomy engine's run log showing the job ran) is the EXIT EVIDENCE
>  for each such wiring seal. E1 wires the seams INTO the Census
>  Autonomy Service so Akki runs them autonomously — then STEPS BACK.
>  E1's pod is NEVER the training host and NEVER a data path."

**Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:**

> "E1 wires the seam INTO the Census Autonomy Service. Pod is never a
>  data path."

## SEAL PROTOCOL SUMMARY

**Item 5.11.e of EXECUTION_ORDER.md — 5th item of Item 5.11 wave.**

- Ratchet 6369 → 6379 (+10 canonical measured own new pins).
- baseline_failures.json sha256 post-bump: `7130a31b2e22d2e326d215d8e9c9a9e6f3ddea53b0bfba7e24585603130bd8e2`.
- ORCH_BOOT.md notes+audit byte-identical sha256: `e44aab3bc76dd19ccf9ba320591b3d92d345b126b624d5f679989f2f8c50098a`.
- Objective card sha256 (line-removed convention): `21799936eafffe2548be7dc2236f3a19ab43b7850b34560f2c32f134f59dcca9`.
- Pre-Commit-A double-green BASELINE_GUARD=1 PYTHONHASHSEED=0 stripped_sha256: `b039979de0feb2e5de97600e52c65a82f76b351468f5fb6077166bfcb8981f06` IDENTICAL sweep_A (20260923T145644Z ~202s) + sweep_B (20260923T150017Z ~202s) both 6379 passed / 13 skipped / 0 failed / 520 warnings.
- Code Commit-A: `b49f7e9066b93ed3c89f370d68b0757400dfc241` on `programme/track-a`.
- /app main companion Commit-A: `313300d9f` on `main`.
- Code bundle emitted: `/app/assessment_workspace/continuity_bundles/code_20260923T150603Z_CP_TRACK_4_AUTONOMY_WIRING.bundle` sha256 `0b7b355f62e4f5e1632c10f0f6e1fcd5a1b724d682e54a1fc4dfc6ae95387273` (~18 MiB) per SO §6.9(5) AMENDED 7th application.
- Sealed carriers UNCHANGED per SO §3.8 additive-only:
  - `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE).
  - `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES).
  - `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS).
  - `services/census_autonomy/engine.py` (R-106 sealed).
- Ruling (b) AKKI-RUNS-IT verbatim honored — pod NEVER data path (Track-4 registration seats refuse `pod://*` + `/app/*` prefixed refs via `PodIsNeverDataPathAtTrack4Error`).

## THE 10 INVARIANT PINS

1. `test_track_4_wires_all_three_seams_registration_aggregate` — `register_all_three_track_4_jobs()` returns `Track4AllJobsRegistered_v1` with 3 registrations + `total_jobs_registered == 3`.
2. `test_lid_pass_registration_seat_via_track_4` — `register_lid_pass_as_census_autonomy_job()` returns `Track4LidPassRegistration_v1` composing sealed `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` by identity.
3. `test_pod_prefix_refused_at_lid_registration_seat` — `pod://queue` OR `/app/backend/adapter` at LID seat raises `PodIsNeverDataPathAtTrack4Error`.
4. `test_autonomy_engine_run_receipt_shape_frozen` — `AutonomyEngineRunReceipt_v1` frozen dataclass; cannot mutate `.status` after construction.
5. `test_autonomy_engine_run_receipt_status_literal_closed` — `status` in `{"completed","failed","refused"}` accepted; `"rogue_status"` raises `AutonomyEngineRunReceiptStatusRefused`.
6. `test_job_kind_literal_closed_three_kinds` — `TRACK_4_JOB_KINDS == ("lid_pass", "census_three_waves", "training_runs")`; `"rogue_job"` raises `Track4JobKindRefused`.
7. `test_track_4_autonomy_wiring_posture_marker_present` — `TRACK_4_AUTONOMY_WIRING_POSTURE` Final marker contains "census autonomy" + "e1 wires"/"wires" + "step".
8. `test_pod_is_never_data_path_posture_track_4_marker_present` — `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` Final marker contains "pod" + "never".
9. `test_no_redeclaration_of_sealed_symbols_1_2` — AST scan confirms zero redeclaration of any sealed CP-SO-6.9-LID-WAVE + CP-CENSUS-THREE-WAVES + CP-AIP-10-TRAINING-RUNS symbol.
10. `test_track_4_e1_steps_back_posture_marker_present` — `E1_STEPS_BACK_AFTER_WIRING_POSTURE` Final marker contains "steps back"/"step back" + "wires"/"wire".

## LIVE-ENGINE EXIT EVIDENCE

Owner verbatim exit clause: *"Verification of autonomy pickup (receipt from the autonomy engine's run log showing the job ran) is the EXIT EVIDENCE for each such wiring seal."*

Exit-evidence generator `/app/assessment_workspace/tools/generate_track_4_autonomy_run_receipts.py` (analysis/evidence script per SO §3.8) executed the following LIVE end-to-end chain on all 3 wired jobs:

```
register_all_three_track_4_jobs(...)  # Track-4 boundary composes 3 sealed seats
    → enqueue_on_demand_run(tenant_id, connect_source_descriptor, lawful_basis_admit_ref)   # LIVE engine.py writes pending JSON
        → run_bounded_census(job=pending_json, job_deadline=+60s)                            # LIVE engine.py picks up + executes
            → _write_result_receipt(...)                                                    # LIVE engine.py persists result JSON
                → emit_autonomy_engine_run_receipt(job_kind, run_id, status, provenance_ref)  # Track-4 exit-evidence carrier
```

**Per-job receipts (3 machine-readable JSON files):**

| job_kind | census_run_id | engine_live_status | wiring_receipt_status | persisted_result_path |
|---|---|---|---|---|
| lid_pass | cr-f639cb8dbc7d | COMPLETE | completed | `phase0/census_autonomy_state/results/20260923T144803Z_cr-f639cb8dbc7d_result.json` |
| census_three_waves | cr-b104d3303bda | COMPLETE | completed | `phase0/census_autonomy_state/results/20260923T144803Z_cr-b104d3303bda_result.json` |
| training_runs | cr-5f7e857492e7 | COMPLETE | completed | `phase0/census_autonomy_state/results/20260923T144803Z_cr-5f7e857492e7_result.json` |

**Composite seal-level exit-evidence receipt** at `backend/phase0/track_4_autonomy_engine_run_receipts/20260923T144803Z_seal_level_composite_exit_evidence.json` composes:
- The 3 per-job receipts above.
- The 3 posture markers verbatim (`TRACK_4_AUTONOMY_WIRING_POSTURE` + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` + `E1_STEPS_BACK_AFTER_WIRING_POSTURE`).
- Owner verbatim exit clause (SO §6.9 amendment §6 item 6 + Ruling (b) verbatim).
- Aggregate `total_jobs_registered = 3` + `job_kinds_registered = ["lid_pass", "census_three_waves", "training_runs"]`.

## RATCHET + DELTA ATTRIBUTION

- Ratchet 6369 → 6379 (+10 canonical measured own new pins).
- baseline_failures.json ratchet_history entry appended with `seal_id: "CP-TRACK-4-AUTONOMY-WIRING-20260223"` + `passed_pre: 6369` + `passed: 6379` + `delta: 10` + full note verbatim.
- baseline_failures.json sha256 post-bump: `7130a31b2e22d2e326d215d8e9c9a9e6f3ddea53b0bfba7e24585603130bd8e2` (was `0a2ddca10e7623aa523f7bfdf1b5ccfef8447d420968c178f358750d45d322cf` pre-bump).

## RUN-TO-COMPLETION CADENCE

REPORT-AND-CONTINUE not idle-halt per SO §6.9 cadence amendment. Item 5.11.e CLOSED at this-mini-bank. Item 5.11.f (CP-AIP-ASSIST-CENSUS · six binding conditions verbatim) opens next.

## LEDGER CHECK

**Ledger check - this seal implements Item 5.11.e of EXECUTION_ORDER.md and nothing else.**
