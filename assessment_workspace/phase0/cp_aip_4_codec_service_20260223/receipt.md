# CP-AIP-4-CODEC-SERVICE · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T06:55:00Z
**Ledger anchor:** EXECUTION_ORDER.md Item 5.4 · CP-AIP-4 (Codec Service acceptance boundary · AIP v1.0 §3 · fail-closed)
**Owner authorization:** CP-AIP-4 GO (2026-02-23 post-INTERIM REPORT) verbatim: *"Build the service seam + contract + pins against whichever codec path is cheapest to stand up honestly. If neither is viable in-pod, the fail-closed refusal path with stated reason IS the honest v1 behavior - do not mock a codec and call it real; mark any stub explicitly as honest-gap. Codec pretraining (§3.2) is a commissioned-job contract item - card it, do not run heavy pretraining in-pod without a measured cost receipt first."* + Item-4 checkpoint GO 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals' + Cadence GO (2026-02-23) 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

---

## 1 · Scope

The codec-service acceptance boundary per AIP v1.0 §3. This seal lands FIVE additive modules composing sealed CP-M6-4-1 `service.py` (`AUDIO_CODEC_SERVICE_PATH` + `AudioCodecServiceDescriptor` + `build_service_descriptor` + `assert_registered_like_perception_model`) and sealed CP-M6-4-2 `artefact.py` (`CodecArtefact` first-class `character_stream` field + `MissingCodecVersionError` + `require_codec_version` + `assert_downstream_carries_codec_version`) via §1.2 modality-extension. Zero sealed-carrier edit per SO §3.8.

Every §3.3 acceptance criterion is enforced by RED-first pytest invariants:

- **§3.3 (a)** — round-trip fidelity measured and recorded per codec version BEFORE that version serves any commission. `MissingFidelityMeasurementError` refuses at `assert_codec_version_ready_to_serve`. Measurement record requires `measurement_method` + `provenance_material_ref` fields structurally (§1.5 unrepresentable-not-policed).
- **§3.3 (b)** — downstream artifact lacking `codec_version` REJECTED at registry boundary. `RegistryBoundaryRejection` composes sealed `assert_downstream_carries_codec_version` (CP-M6-4-2) via §1.2 modality-extension. Both missing-key and empty-string codec_version rejected.
- **§3.3 (c)** — unsupported-condition input produces refusal with STATED REASON and NO output artifact. `UnsupportedCodecConditionRefused` carries offending condition name + codec version in message; no `CodecArtefact` construction path exists on refusal branch.

§3.1 P037 fail-closed posture is STRUCTURAL — no silent degradation. §3.2 P045 registration is additive v0→v1 bump preserving sealed v0 seed. §3.2 P049 commissioned-job pretraining requires MEASURED cost receipt before heavy compute (owner directive verbatim). `HONEST_GAP_V1_POSTURE` Final marker documents owner directive on refusal-as-honest-v1-behavior.

### New additive modules under `backend/services/perception/audio_codec/` (5 files):

- **`round_trip_fidelity_v1.py`** (~188 lines · sha256 `6db53193e10187550b56d010df1ea336a3106e34926692122a040cabce39e043`):
  - `RoundTripFidelityMeasurement_v1` frozen dataclass (§3.3 (a) verbatim record shape · `codec_version` + `measurement_method` + `provenance_material_ref` + `measured_at_utc` + measurement values).
  - `MissingFidelityMeasurementError` + `FidelityMeasurementIncomplete` refusal sentinels.
  - `assert_codec_version_ready_to_serve(codec_version)` gate — refuses with `MissingFidelityMeasurementError` when no record exists.
  - `record_fidelity_measurement(measurement)` composer — JSONL append-only persistence at `phase0/audio_codec_fidelity/measurements.jsonl`.

- **`unsupported_condition_refusal_v1.py`** (~101 lines · sha256 `73da3b0436ed8804a3cdd24432626743a4962c3b18756ad6d5c6340cd0667be8`):
  - `UnsupportedCodecConditionRefused` refusal class carrying offending `condition` + `codec_version` in structured message.
  - `refuse_unsupported_condition(condition, codec_version)` — fail-closed callable. §3.1 P037 verbatim structural: refusal branch returns NO artifact (no `CodecArtefact` construction path exists).

- **`downstream_provenance_gate_v1.py`** (~75 lines · sha256 `1cdbd2eeee94ae28dab9a52a74042f9ff62e2c3ac298b8f9127c2674314d6db8`):
  - `RegistryBoundaryRejection` refusal class.
  - `assert_downstream_provenance_gate_v1(provenance)` composes sealed `assert_downstream_carries_codec_version` (CP-M6-4-2) via §1.2 modality-extension. Both missing-key and empty-string codec_version rejected.

- **`models_registry_v1_bump_v1.py`** (~90 lines · sha256 `cae4a44f1c749be0e1b55a27bb27ea16a52c99c99c20804de22bbc9b329b9732`):
  - `build_v1_audio_codec_registration_entry()` builder citing sealed `AUDIO_CODEC_SERVICE_PATH` (CP-M6-4-1) verbatim.
  - Sets `census_visible=True` + `in_perimeter=True` per §3.2 P045 verbatim.
  - Zero edit to sealed `models_registry.v0.json` v0 seed (v1 bump lands new-shape carrier · NOT edited seed).

- **`pretraining_contract_v1.py`** (~115 lines · sha256 `1ea8b293bc003060b849e6b4a186a6dcf4e82f51c5b99d1675649a27eb1cec19`):
  - `PretrainingCostReceipt_v1` frozen dataclass (measurement anchors carried structurally).
  - `PretrainingCostReceiptMissing` refusal class.
  - `commission_codec_pretraining(*, cost_receipt)` gated callable — refuses without measured cost receipt (owner directive verbatim: 'do not run heavy pretraining in-pod without a measured cost receipt first').
  - `HONEST_GAP_V1_POSTURE` Final marker with owner directive verbatim ('the fail-closed refusal path with stated reason IS the honest v1 behavior · do not mock a codec and call it real').

### RED-first invariant pins (14 · `test_cp_aip_4_codec_service_aip_v1_0_section_3.py` · sha256 `7efb86f86e779f82fa1cf3f37b75d5a18d2854eb0d9f50be5ac62970029346ca` · 561 lines):

| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_codec_version_without_fidelity_measurement_refuses_to_serve` | §3.3 (a) verbatim · `MissingFidelityMeasurementError` |
| 2 | `test_fidelity_measurement_requires_measurement_method_and_provenance` | §3.3 (a) + §1.5 · `FidelityMeasurementIncomplete` structural gate |
| 3 | `test_new_modules_do_not_assert_throughput_figures` | §1.4 measure-don't-assert · no `50 tokens/second` etc. |
| 4 | `test_registry_boundary_rejects_downstream_missing_codec_version` | §3.3 (b) verbatim + §3.2 P048 + §1.2 composition |
| 5 | `test_registry_boundary_rejects_downstream_empty_codec_version` | §3.3 (b) verbatim + §1.5 unrepresentable |
| 6 | `test_unsupported_condition_refuses_with_stated_reason_and_no_artifact` | §3.3 (c) verbatim + §3.1 P037 fail-closed |
| 7 | `test_unsupported_condition_returns_no_artifact_on_refusal_path` | §3.3 (c) + §3.1 P039 structural |
| 8 | `test_codec_artefact_retains_character_stream_field` | §3.1 P039 + §3.2 P047 verbatim + §16.1 (a) CLEAN receipt · anti-regression on sealed CP-M6-4-2 |
| 9 | `test_registry_bump_entry_uses_sealed_service_path_verbatim` | §3.2 P045 verbatim + §1.2 |
| 10 | `test_pretraining_refuses_without_measured_cost_receipt` | §3.2 P049 verbatim + §1.4 |
| 11 | `test_pretraining_module_carries_explicit_honest_gap_marker` | Owner directive verbatim CP-AIP-4 GO |
| 12 | `test_new_modules_carry_no_audio_byte_or_waveform_carriers` | §3.1 P038 tokens-not-waveforms |
| 13 | `test_new_modules_do_not_redeclare_sealed_codec_carriers` | §1.2 modality-extension-not-parallel · 9 forbidden symbols |
| 14 | `test_new_modules_cite_section_3_and_ledger_check_anchor` | Anti-drift §3 + §5 + ledger-check anchor scan |

---

## 2 · RED-first evidence

Pre-modules test run (RED sweep · 2026-02-23T06:55:00Z · via `mv services/perception/audio_codec/{5 modules}.py /tmp/` isolation):

```
tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py
  FAILED test_codec_version_without_fidelity_measurement_refuses_to_serve             (ModuleNotFoundError right-reason)
  FAILED test_fidelity_measurement_requires_measurement_method_and_provenance         (ModuleNotFoundError right-reason)
  FAILED test_new_modules_do_not_assert_throughput_figures                            (AssertionError · modules missing right-reason)
  FAILED test_registry_boundary_rejects_downstream_missing_codec_version              (ModuleNotFoundError right-reason)
  FAILED test_registry_boundary_rejects_downstream_empty_codec_version                (ModuleNotFoundError right-reason)
  FAILED test_unsupported_condition_refuses_with_stated_reason_and_no_artifact        (ModuleNotFoundError right-reason)
  FAILED test_unsupported_condition_returns_no_artifact_on_refusal_path               (ModuleNotFoundError right-reason)
  PASSED test_codec_artefact_retains_character_stream_field                           (anti-regression · sealed CP-M6-4-2 already carries character_stream)
  FAILED test_registry_bump_entry_uses_sealed_service_path_verbatim                   (ModuleNotFoundError right-reason)
  FAILED test_pretraining_refuses_without_measured_cost_receipt                       (ModuleNotFoundError right-reason)
  FAILED test_pretraining_module_carries_explicit_honest_gap_marker                   (AssertionError · module missing right-reason)
  FAILED test_new_modules_carry_no_audio_byte_or_waveform_carriers                    (AssertionError · modules missing right-reason)
  FAILED test_new_modules_do_not_redeclare_sealed_codec_carriers                      (AssertionError · modules missing right-reason)
  FAILED test_new_modules_cite_section_3_and_ledger_check_anchor                      (AssertionError · modules missing right-reason)
========================= 13 failed, 1 passed in 0.70s =========================
```

Post-modules test run (GREEN sweep · 2026-02-23T06:57:00Z):

```
============================== 14 passed in 0.71s ==============================
```

All 13 RED pins flipped GREEN post-module authorship. The 1 anti-regression pin (`test_codec_artefact_retains_character_stream_field`) stayed GREEN — it guards sealed CP-M6-4-2 CodecArtefact against any future removal of `character_stream` (§3.1 P039 verbatim per §16.1 (a) CLEAN receipt).

Drill receipts banked at `backend/phase0/drill_receipts_cp_aip_4_codec_service/` (RED_pre + GREEN_post + sweep_A + sweep_B).

---

## 3 · Pre-Commit-A double-green byte-identical sweep

Both sweeps ran under `BASELINE_GUARD=1 PYTHONHASHSEED=0`.

- **Sweep A:** `6286 passed / 1 skipped / 0 failed / 520 warnings in 184.32s` (real 3m14.178s / user 3m5.342s / sys 0m11.806s).
- **Sweep B:** `6286 passed / 1 skipped / 0 failed / 520 warnings in 185.25s` (real 3m14.774s / user 3m6.310s / sys 0m11.734s).
- **stripped_sha256 (both sweeps):** `e33f1cd0599f9349907759b306b046c4e5ef8bf958cbf9b7805edf4f25538806` — **IDENTICAL**.

Raw + stripped logs banked at `phase0/cp_aip_4_codec_service_20260223/sweep_A.log` + `sweep_A.stripped` + `sweep_B.log` + `sweep_B.stripped`.

The passed count 6286 exceeds the ratchet floor 6280 by 6 (comprises tests outside the ratchet baseline manifest — expected). The three baseline_failures.json listed failures were flagged as expected.

---

## 4 · Ratchet bump

- **Floor:** 6266 → 6280 (+14 canonical measured pins from CP-AIP-4).
- **baseline_failures.json sha256 pre-bump:** `42910fa760d7f3ba84644b10f1f2d6f36daacd35aecfd95d19946ecbce29ccc0` (post-CP-AIP-3).
- **baseline_failures.json sha256 post-bump:** `678982b96d12fe19d55a001ca0fbf33abbda2cd869bd6bc5579f95959c64cab0`.
- Written with `indent=2, ensure_ascii=False` per BL #7 + BL #11.
- `ratchet_history` entry appended with schema-complete fields (`at_utc` + `commit` (PENDING at authorship · filled post-Commit-A) + `cp` + `note` + `passed=6280`).
- `invariants_enforced_when_baseline_guard_1.passed_floor` advanced 6266 → 6280 in lock-step with `counts_at_baseline.passed` (per `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` invariant).

---

## 5 · Sealed carriers UNCHANGED (SO §3.8 additive-only)

- `backend/services/perception/audio_codec/service.py` (CP-M6-4-1 · sealed).
- `backend/services/perception/audio_codec/artefact.py` (CP-M6-4-2 · sealed).
- `backend/services/perception/audio_codec/census_visibility.py` (sealed).
- `backend/services/perception/audio_codec/perimeter_boundary.py` (sealed).
- `backend/services/perception/model_registry.py` (sealed core).
- `backend/services/perception/models_registry.v0.json` (v0 seed · UNCHANGED · v1 bump lands new-shape carrier NOT edited seed).
- All CP-AIP-1 + CP-AIP-2 + CP-AIP-3 modules (`ingestion_provenance_v1.py` + `ingestion_capture_v1.py` + `dedup_instance_provenance_v1.py` + `dedup_capture_v1.py` + `character_register_write_boundary_v1.py` + `character_register_clustering_v1.py`) — untouched this seal.
- `services/rms_station_language_axis.py` + `services/audio_plane_v1/instance_condition_map.py` + `services/audio_plane_v1/dedup_path.py` + `services/audio_plane_v1/character_register.py` + `services/audio_plane_v1/leakage_path_harness.py` + all prior sealed carriers — untouched.

---

## 6 · Owner content anchors banked

- **HONEST_GAP_V1_POSTURE** — owner directive verbatim: 'the fail-closed refusal path with stated reason IS the honest v1 behavior · do not mock a codec and call it real'. Enforced by PIN-11 (module-level `Final` marker scan).
- **Pretraining is commissioned-job contract, not session-time activity** — owner directive verbatim: 'do not run heavy pretraining in-pod without a measured cost receipt first'. Enforced by PIN-10 (`commission_codec_pretraining` refuses without cost receipt).
- **§16.1 (a) CLEAN receipt (2026-02-23T05:00:00Z)** — `character_stream` is a FIRST-CLASS FIELD on sealed CodecArtefact; no new artifact type. Enforced by PIN-8 anti-regression.

---

## 7 · SPEC-CONFLICT log this slice

**NONE.**

---

## 8 · Standing bounds

Unchanged. R-102 productized-or-honest-gap · R-103 continuous · R-104 CORRECTED · R-105 partial-retirement · R-106 P3-CLOSED + P4-(a-d-i) + CP-CENSUS + CP-AIP-1 + CP-AIP-2 + CP-AIP-3 SEALED-A · §6.8 plan-authority report-and-continue.

Additive-only §3.8 · monotonic-up ratchet floor 6280 · no sealed carrier touched · no refactoring · terminal `pytest` only · `testing_agent` BANNED · Six Standing Bans in force.
