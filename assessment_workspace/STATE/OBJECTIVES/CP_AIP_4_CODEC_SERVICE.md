---
card_id: CP_AIP_4_CODEC_SERVICE
title: AIP v1.0 §3 · Codec Service acceptance boundary · fail-closed · additive v0→v1 registry bump · commissioned-job pretraining contract seat · Item 5.4 CP-AIP-4
ratified_at_utc: 2026-02-23T06:55:00Z
ratified_by: Owner GO for CP-AIP-4 (2026-02-23 post-INTERIM REPORT verbatim 'Build the service seam + contract + pins against whichever codec path is cheapest to stand up honestly. If neither is viable in-pod, the fail-closed refusal path with stated reason IS the honest v1 behavior - do not mock a codec and call it real; mark any stub explicitly as honest-gap. Codec pretraining (§3.2) is a commissioned-job contract item - card it, do not run heavy pretraining in-pod without a measured cost receipt first.') + Item-4 checkpoint GO 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
card_sha256: 1d92cbfff9bb979b781487b06591c0833c77c82d19d7e51fd827cbf00ab7690b
milestone_status: OPEN (Item 5.4 CP-AIP-4 · in-flight for this seal)
---

# CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3 Codec Service Acceptance Boundary · fail-closed

## OBJECTIVE

Land the additive `perception/audio_codec/` acceptance boundary per AIP v1.0 §3 as pure §1.2 modality-extension of sealed CP-M6-4-1 `service.py` (`AUDIO_CODEC_SERVICE_PATH` + `AudioCodecServiceDescriptor` + `build_service_descriptor` + `assert_registered_like_perception_model`) and sealed CP-M6-4-2 `artefact.py` (`CodecArtefact` first-class `character_stream` field + `MissingCodecVersionError` + `require_codec_version` + `assert_downstream_carries_codec_version`). Zero sealed-carrier edit per SO §3.8.

Every §3.3 acceptance criterion is enforced by RED-first pytest invariants: (a) round-trip fidelity measured and recorded per codec version BEFORE serving any commission (§3.3 (a) verbatim), (b) downstream artifact lacking `codec_version` in provenance is REJECTED at the registry boundary (§3.3 (b) verbatim · reinforces sealed CP-M6-4-2 gate), (c) unsupported-condition input produces a refusal with STATED REASON and NO output artifact (§3.3 (c) verbatim). §3.1 P037 fail-closed posture is structural — no silent degradation. §3.2 P045 registration is additive v0→v1 bump preserving sealed v0 seed. §3.2 P049 commissioned-job pretraining contract requires measured cost receipt before heavy compute (owner directive verbatim).

`canon_ref: AIP v1.0 §3.1 P037 fail-closed + §3.2 P045 registration + §3.2 P047 output contract + §3.2 P048 codec_version mandatory + §3.2 P049 commissioned-job pretraining + §3.3 (a) (b) (c) acceptance criteria + §1.2 modality-extension + §1.4 measure-don't-assert + §1.5 unrepresentable-not-policed + §16.1 (a) CLEAN receipt + §16.2 codec-choice deferred.`

Owner content anchor verbatim (CP-AIP-4 GO 2026-02-23): "If neither is viable in-pod, the fail-closed refusal path with stated reason IS the honest v1 behavior - do not mock a codec and call it real."

## MUST DO

1. **§3.3 (a) round-trip fidelity measurement gate GREEN** — a codec version cannot serve any commission before a fidelity measurement has been recorded. `assert_codec_version_ready_to_serve(codec_version)` refuses with `MissingFidelityMeasurementError` when no `RoundTripFidelityMeasurement_v1` record exists for that version. Measurement record requires both `measurement_method` and `provenance_material_ref` fields structurally (§1.5). Enforced by `test_codec_version_without_fidelity_measurement_refuses_to_serve` + `test_fidelity_measurement_requires_measurement_method_and_provenance`. `canon_ref: AIP §3.3 (a) verbatim + §1.4 measure-don't-assert + §1.5.`

2. **§3.3 (b) downstream provenance gate composed via sealed carrier** — the NEW `assert_downstream_provenance_gate_v1(...)` composes sealed `assert_downstream_carries_codec_version` (CP-M6-4-2) via §1.2 modality-extension. Both missing-key and empty-string codec_version are rejected at the registry boundary with `RegistryBoundaryRejection`. Enforced by `test_registry_boundary_rejects_downstream_missing_codec_version` + `test_registry_boundary_rejects_downstream_empty_codec_version`. `canon_ref: AIP §3.3 (b) verbatim + §1.2 + §3.2 P048.`

3. **§3.3 (c) unsupported-condition fail-closed refusal** — `refuse_unsupported_condition(condition, codec_version)` raises `UnsupportedCodecConditionRefused` with stated reason (offending condition name + codec version in message) and returns NO output artifact (structural — no `CodecArtefact` construction path exists on the refusal branch). Enforced by `test_unsupported_condition_refuses_with_stated_reason_and_no_artifact` + `test_unsupported_condition_returns_no_artifact_on_refusal_path`. `canon_ref: AIP §3.3 (c) verbatim + §3.1 P037 fail-closed + §1.5.`

4. **§3.2 P045 additive v0→v1 registration entry-builder** — `build_v1_audio_codec_registration_entry()` returns a registration entry citing sealed `AUDIO_CODEC_SERVICE_PATH` verbatim, with `census_visible=True` and `in_perimeter=True` per §3.2 verbatim. Zero edit to sealed `services/perception/models_registry.v0.json` (v0 seed UNCHANGED); the entry is a new v1-shape carrier per its own append-only doctrine. Enforced by `test_registry_bump_entry_uses_sealed_service_path_verbatim`. `canon_ref: AIP §3.2 P045 verbatim + §1.2 modality-extension.`

5. **§3.2 P049 commissioned-job pretraining contract seat with cost-receipt gate** — `commission_codec_pretraining(*, cost_receipt)` refuses with `PretrainingCostReceiptMissing` when the cost receipt is absent, empty, or lacks measurement anchors. The module carries an explicit `HONEST_GAP_V1_POSTURE` Final marker documenting the owner directive verbatim (do not mock a codec; fail-closed refusal IS the honest v1 behavior). Enforced by `test_pretraining_refuses_without_measured_cost_receipt` + `test_pretraining_module_carries_explicit_honest_gap_marker`. `canon_ref: AIP §3.2 P049 verbatim + §1.4 measure-don't-assert + owner directive verbatim CP-AIP-4 GO.`

6. **§3.1 P039 character_stream anti-regression on sealed CP-M6-4-2** — a dedicated pin re-asserts that `CodecArtefact` retains `character_stream` as a first-class field per §3.2 P047 verbatim and §16.1 (a) CLEAN receipt. Enforced by `test_codec_artefact_retains_character_stream_field`. `canon_ref: AIP §3.1 P039 + §3.2 P047 verbatim + §16.1 (a) CLEAN receipt 2026-02-23T05:00:00Z.`

7. **§1.4 measure-don't-assert scan** — the NEW modules carry NO asserted throughput figures. AST/text scan bans string literals matching `50 tokens/second`, `100 tokens/second`, `50-100 tokens/second`, `50 tok/s`, `100 tok/s`, and any variant asserting an unmeasured target. Enforced by `test_new_modules_do_not_assert_throughput_figures`. `canon_ref: AIP §1.4 verbatim + owner directive verbatim (do not quote unmeasured figures).`

8. **§3.1 P038 tokens-not-waveforms schema scan** — the NEW modules carry NO audio-byte or waveform carriers. Forbidden names scanned across the five modules: `audio_bytes`, `waveform`, `samples`, `raw_audio`. Enforced by `test_new_modules_carry_no_audio_byte_or_waveform_carriers`. `canon_ref: AIP §3.1 P038 tokens-not-waveforms + §6.3 P100 unrepresentable-not-policed mirror.`

9. **§1.2 no-redeclaration scan of 9 sealed symbols** — the NEW modules do not redeclare any of the 9 sealed codec symbols (`CodecArtefact`, `MissingCodecVersionError`, `require_codec_version`, `assert_downstream_carries_codec_version`, `AUDIO_CODEC_SERVICE_PATH`, `AudioCodecServiceDescriptor`, `build_service_descriptor`, `assert_registered_like_perception_model`, and the sealed v0 registry seed constant name). Enforced by `test_new_modules_do_not_redeclare_sealed_codec_carriers`. `canon_ref: AIP §1.2 modality-extension-not-parallel + BL #4.`

10. **§3 anti-drift + ledger-check anchor scan** — the NEW modules cite AIP v1.0 §3 anchors verbatim in module docstrings AND carry the ledger-check anchor string. Enforced by `test_new_modules_cite_section_3_and_ledger_check_anchor`. `canon_ref: Anti-drift standing guard §3 + §5 + owner directive `every seal Commit-A carries "Ledger check - this seal implements <item n> and nothing else"'.`

11. **14 RED-first pytest invariants** — RED_pre 13/14 failed (1 anti-regression on sealed CP-M6-4-2 `CodecArtefact` schema) → GREEN_post 14/14 passed. Each pin cites the exact §3 or §1 or §16 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

12. **Ratchet floor 6266 → 6280** — +14 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · `ratchet_history` entry appended schema-complete (`passed=6280`). `invariants_enforced_when_baseline_guard_1.passed_floor` advanced in lock-step with `counts_at_baseline.passed`. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

13. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1 + CP-AIP-2 + CP-AIP-3 seals. Terminal `pytest` only. `testing_agent` BANNED. `BASELINE_GUARD=1 PYTHONHASHSEED=0` double-green byte-identical `stripped_sha256`. `canon_ref: SO §3.3 5-Commit-Seal + SO §7 guard 6 + SO Six Standing Bans.`

## MUST NOT

- Edit any sealed §3 carrier (`services/perception/audio_codec/service.py` CP-M6-4-1 + `artefact.py` CP-M6-4-2 + `census_visibility.py` + `perimeter_boundary.py`), or `services/perception/model_registry.py`, or `services/perception/models_registry.v0.json`, or any prior CP-AIP-1/CP-AIP-2/CP-AIP-3 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only.`

- Redeclare any of the 9 sealed codec symbols (`CodecArtefact`, `MissingCodecVersionError`, `require_codec_version`, `assert_downstream_carries_codec_version`, `AUDIO_CODEC_SERVICE_PATH`, `AudioCodecServiceDescriptor`, `build_service_descriptor`, `assert_registered_like_perception_model`, sealed v0 registry seed constant). `canon_ref: AIP §1.2 verbatim + BL #4.`

- Quote unmeasured throughput figures (e.g., "50-100 tokens/second") in the NEW modules. `canon_ref: AIP §1.4 measure-don't-assert + owner directive verbatim.`

- Introduce ANY audio-byte or waveform carriers (`audio_bytes`, `waveform`, `samples`, `raw_audio`) in the NEW modules — the codec outputs tokens and character_stream, never waveforms downstream. `canon_ref: AIP §3.1 P038 tokens-not-waveforms.`

- Mock a codec and call it real. If neither an HF-hosted base nor a local codec is viable in-pod, the fail-closed refusal path with stated reason IS the honest v1 behavior — mark any stub explicitly as honest-gap. `canon_ref: Owner directive verbatim CP-AIP-4 GO 2026-02-23.`

- Run heavy codec pretraining in-pod without a measured cost receipt first. Pretraining is a commissioned-job contract item, not a session-time activity. `canon_ref: AIP §3.2 P049 + owner directive verbatim CP-AIP-4 GO.`

- Silently degrade on unsupported-condition input. The codec fails closed; the character stream is retained and routed, never discarded. `canon_ref: AIP §3.1 P037 + P039 verbatim.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else. `canon_ref: SO §7 guard 5 + Anti-drift standing guard §3 + §5.`

## EXIT

**14 RED-first invariants (RED_pre 13/14 failed · GREEN_post 14/14 passed · authored under this seal · continue verbatim GREEN post-Commit-A):**

- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_codec_version_without_fidelity_measurement_refuses_to_serve
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_fidelity_measurement_requires_measurement_method_and_provenance
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_new_modules_do_not_assert_throughput_figures
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_registry_boundary_rejects_downstream_missing_codec_version
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_registry_boundary_rejects_downstream_empty_codec_version
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_unsupported_condition_refuses_with_stated_reason_and_no_artifact
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_unsupported_condition_returns_no_artifact_on_refusal_path
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_codec_artefact_retains_character_stream_field
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_registry_bump_entry_uses_sealed_service_path_verbatim
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_pretraining_refuses_without_measured_cost_receipt
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_pretraining_module_carries_explicit_honest_gap_marker
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_new_modules_carry_no_audio_byte_or_waveform_carriers
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_new_modules_do_not_redeclare_sealed_codec_carriers
- tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py::test_new_modules_cite_section_3_and_ledger_check_anchor

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6266 → 6280 (+14 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical stripped_sha256 `e33f1cd0599f9349907759b306b046c4e5ef8bf958cbf9b7805edf4f25538806` · 6286 passed / 1 skipped / 0 failed / 520 warnings both sweeps

## STOP

Stop at 5-commit seal landing. Continue immediately into CP-AIP-5-CLUSTERING per owner cadence directive (2026-02-23 GO CP-AIP-4 through CP-AIP-10 sequential, brief report-and-continue after CP-AIP-6 seals, HALT after CP-AIP-10 seals for full plane completion report).

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §3 or §16.1 (a), HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately (no continue). `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3 + owner cadence directive.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §3.1 P037 fail-closed verbatim: 'The audio codec fails closed; it never silently degrades. The character stream is retained and routed, never discarded.'
- §3.1 P038 tokens-not-waveforms.
- §3.1 P039 character_stream retention.
- §3.2 P045 registration verbatim: 'perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute.'
- §3.2 P047 output contract verbatim: `{ content_tokens[], character_stream, codec_version }`.
- §3.2 P048 codec_version mandatory verbatim: 'codec_version is a mandatory field of every downstream artifact's provenance.'
- §3.2 P049 commissioned-job pretraining verbatim: 'The codec pretrains unsupervised on unlabelled estate audio, under the standard commissioned-job contract.'
- §3.3 (a) round-trip fidelity measured verbatim.
- §3.3 (b) downstream artifact rejected without codec_version verbatim.
- §3.3 (c) unsupported-condition refusal with stated reason and no output artifact verbatim.
- §15 P232 build sequence: 'Codec service (§3) — Unsupervised pretraining starts on unlabelled audio while labelled work proceeds elsewhere.'
- §1.2 modality extension, not parallel machinery.
- §1.4 measure-don't-assert.
- §1.5 unrepresentable, not policed.
- §16.1 (a) CLEAN receipt (2026-02-23T05:00:00Z): `character_stream` is a first-class field on sealed `CodecArtefact`; no new artifact type.
- §16.2 codec-choice DEFERRED per owner (Sampling & Reflection §11.2 answers it once built).

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO (2026-02-23 post-INTERIM REPORT): 'Build the service seam + contract + pins against whichever codec path is cheapest to stand up honestly. If neither is viable in-pod, the fail-closed refusal path with stated reason IS the honest v1 behavior - do not mock a codec and call it real; mark any stub explicitly as honest-gap. Codec pretraining (§3.2) is a commissioned-job contract item - card it, do not run heavy pretraining in-pod without a measured cost receipt first.'
- Cadence directive (2026-02-23 GO): sequential CP-AIP-4 → CP-AIP-10; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 seals for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.
- HF-HOLD SEC-2026-09-12-01 LIFTED (2026-02-23T03:15Z) — HF-hosted codec bases permitted; local/cached fallback via `local_files_only=True` remains offline path.

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/perception/audio_codec/service.py` (CP-M6-4-1 · `AUDIO_CODEC_SERVICE_PATH` + `AudioCodecServiceDescriptor` + `build_service_descriptor` + `assert_registered_like_perception_model`).
- `backend/services/perception/audio_codec/artefact.py` (CP-M6-4-2 · `CodecArtefact` first-class `character_stream` field + `MissingCodecVersionError` + `require_codec_version` + `assert_downstream_carries_codec_version`).
- `backend/services/perception/audio_codec/census_visibility.py` (sealed).
- `backend/services/perception/audio_codec/perimeter_boundary.py` (sealed).
- `backend/services/perception/model_registry.py` (sealed core · extended additively via its own append-only doctrine).
- `backend/services/perception/models_registry.v0.json` (v0 seed UNCHANGED · v1 bump lands new-shape carrier NOT edited seed).
- All CP-AIP-1 + CP-AIP-2 + CP-AIP-3 modules — untouched this seal.

**New additive modules landed by this seal (5 files · `backend/services/perception/audio_codec/`):**
- `round_trip_fidelity_v1.py` (~188 lines · `RoundTripFidelityMeasurement_v1` frozen dataclass + `MissingFidelityMeasurementError` + `FidelityMeasurementIncomplete` + `assert_codec_version_ready_to_serve` gate + `record_fidelity_measurement` composer + JSONL append-only persistence at `phase0/audio_codec_fidelity/measurements.jsonl`).
- `unsupported_condition_refusal_v1.py` (~101 lines · `UnsupportedCodecConditionRefused` refusal class carrying offending condition + codec version + `refuse_unsupported_condition` fail-closed callable + refusal path returns no artifact structurally).
- `downstream_provenance_gate_v1.py` (~75 lines · `RegistryBoundaryRejection` refusal class + `assert_downstream_provenance_gate_v1` composer using sealed `assert_downstream_carries_codec_version` + empty-string rejection).
- `models_registry_v1_bump_v1.py` (~90 lines · `build_v1_audio_codec_registration_entry` builder citing sealed `AUDIO_CODEC_SERVICE_PATH` verbatim · `census_visible=True` + `in_perimeter=True` per §3.2 verbatim).
- `pretraining_contract_v1.py` (~115 lines · `PretrainingCostReceipt_v1` + `PretrainingCostReceiptMissing` refusal + `commission_codec_pretraining` gated callable + `HONEST_GAP_V1_POSTURE` Final marker with owner directive verbatim).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans (zero push/fetch · `testing_agent` BANNED · no refactor · no secret values · honest-gap never fake · no history rewrite) · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.
