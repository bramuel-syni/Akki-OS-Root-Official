---
card_id: CP_SO_6_9_LID_WAVE_20260223
title: SO §6.9 LID wave · Whisper-LID (MIT) + VoxLingua107 (Apache-2.0) registration acts + OverlayLidDetection_v1 shape + admission gate DEFAULT ≥ 90% scored against google-transcripts labelled corpus + regime promotion by receipted act + anti-token HF pull wrapper · Item 5.11.a
ratified_at_utc: 2026-02-23T12:15:00Z
ratified_by: Owner drop verbatim 2026-02-23 (SO §6.9 LID RATIFICATION) — 'Register two audio-native models instead, both under licences that need no review — Whisper language detection (MIT) and SpeechBrain VoxLingua107 (Apache 2.0) — pinning the hash and recording the licence file as the registration act.' + RUN-TO-COMPLETION mandate 2026-02-23 + owner ruling verbatim 'Admission gate DEFAULT ≥ 90% scored against google-transcripts/datasets/{kik,ebu,swa,luo,kln,guz,mer,bxk,kam,mrg,lwg,mas}/{audio,transcript} labelled corpus as ground truth. TENANT-LABELS-PENDING RESOLVED for 12 languages listed; English/Sheng/code-switched retain honest-gap.'
card_sha256: <computed_at_promote>
milestone_status: QUEUED (Item 5.11.a · opens immediately post CP-AIP-10 seal · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-SO-6.9-LID-WAVE-20260223 · Whisper-LID + VoxLingua107 registration + OverlayLidDetection + admission gate + regime promotion by receipted act

## OBJECTIVE

Land the additive LID-wave compose-boundary as pure §1.2 modality-extension of sealed CP-M6-1-1 `LanguageIDBackend` protocol at `services/audio_plane_v1/language_identifier.py` (D10 pluggable-seam). Register **two audio-native LID models** as registration acts (weight-file sha256 + licence file + pull provenance under anti-token wrapper): (1) **Whisper LID (MIT)** and (2) **SpeechBrain VoxLingua107 (Apache-2.0)**. Bind the overlay-detection record shape structurally (`marker="INFERRED"` when labelled, `"unmeasured"` when below-confidence; `regime="pre-admission"` initially; do-not-flow-into-counted-measure guard). Bind the admission gate structurally (DEFAULT threshold ≥ 90% segment-level agreement, tagged `pending`; scored against the `google-transcripts/` 12-language labelled corpus per SO §6.9 LID RATIFICATION). Bind regime promotion structurally by receipted act (owner signature required per canon 8 §4 W2; nothing ever relabelled). Bank `TENANT-LABELS-PENDING` honest-gap for English/Sheng/code-switched (retained per SO §6.9 LID RATIFICATION). Zero sealed-carrier edit per SO §3.8.

`canon_ref: SO §6.9 LID RATIFICATION verbatim 2026-02-23 §1-9 + Audio-Plane v1.0 §4.1 N1 + B5.4 shown-not-counted line + Canon 8 §4 W2 receipted-act + §1.2 modality-extension + §6.9 clause 3 anti-token pull hazard scope.`

## MUST DO

1. **Whisper-LID registration act shape (MIT licence)** — `LidModelRegistration_v1` frozen dataclass carries `model_entry: str`, `weight_sha256: str`, `licence_id: Literal["MIT","Apache-2.0"]`, `licence_file_path: str`, `pull_provenance_ref: str`, `execution_mode: Literal["cpu","cuda"]`. Whisper registration must have `licence_id == "MIT"`. Enforced by `test_whisper_lid_registration_act_shape_MIT_licence_pinned_so_6_9_lid`.
2. **VoxLingua107 registration act shape (Apache-2.0 licence)** — same frozen dataclass; VoxLingua107 registration must have `licence_id == "Apache-2.0"`. Enforced by `test_voxlingua107_registration_act_shape_apache_2_0_licence_pinned_so_6_9_lid`.
3. **OverlayLidDetection marker structural invariant** — `marker == "INFERRED"` iff `label is not None`; `marker == "unmeasured"` iff `label is None`; frozen dataclass refuses construction when invariant violated (`LidLabelBelowConfidenceMustBeUnmeasuredError`). Enforced by `test_overlay_lid_detection_marker_INFERRED_when_label_set_unmeasured_when_none_b5_4`.
4. **OverlayLidDetection regime default `pre-admission`** — frozen dataclass default; construction with `regime="post-admission"` requires a companion `LidRegimePromotionByReceiptedAct_v1` reference; otherwise refused (`LidOverlayMustNotFlowIntoCountedMeasureError`). Enforced by `test_overlay_lid_detection_regime_starts_pre_admission_default_so_6_9`.
5. **Do-not-flow-into-counted-measure Final posture marker** — `LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE: Final[str]` verbatim of B5.4 line. Enforced by `test_lid_do_not_flow_into_counted_measure_posture_marker_present_b5_4`.
6. **Admission gate DEFAULT threshold ≥ 0.90 tagged pending** — `LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING: Final[float] = 0.90`; gate evaluation records `gate_status == "pending"` until owner retunes and receipts. Enforced by `test_admission_gate_default_threshold_is_0_90_pending_so_6_9_lid`.
7. **Regime promotion requires owner receipted act (canon 8 §4 W2)** — `promote_lid_regime_by_receipted_act(model_entry, owner_signature_ref, previous_regime, new_regime)` raises `LidRegimePromotionRequiresOwnerReceiptedActError` when `owner_signature_ref` is empty or `previous_regime == new_regime`. Enforced by `test_lid_regime_promotion_requires_owner_receipted_act_canon_8_4_W2`.
8. **Nothing-relabelled-at-regime-flip Final posture marker** — `LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE: Final[str]`; a historic overlay detection cannot be mutated when regime flips (frozen dataclass structural guarantee). Enforced by `test_lid_nothing_relabelled_at_regime_flip_posture_marker_present_so_6_9`.
9. **HF pull wrapper anti-token structural guarantee** — `HuggingFacePullWrapperAntiToken_v1.build_headers()` returns `dict[str,str]` with no bearer-like key (Authorization/Bearer/token in any case) and no `HF_TOKEN`/`HUGGINGFACEHUB_API_TOKEN` reference. Scrubs env of those keys before returning. Enforced by `test_hf_pull_wrapper_build_headers_has_no_bearer_like_key_so_6_9_clause_3`.
10. **TENANT-LABELS-PENDING honest-gap for English/Sheng/code-switched** — `TenantLabelsPendingHonestGap_v1(languages)` records exactly `frozenset({"English","Sheng","code-switched"})` per SO §6.9 LID RATIFICATION residual. The 12 languages (kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas) are marked RESOLVED (present in `google-transcripts/` corpus). Enforced by `test_tenant_labels_pending_honest_gap_english_sheng_code_switched_so_6_9_lid_ratification`.
11. **§1.2 no-redeclaration of sealed symbols** — no shadow of `LanguageIDBackend`, `UnratifiedInferredBackend`, `LanguageIDResult`, `AudioSegment` from `services/audio_plane_v1/language_identifier.py` in the additive module. Enforced by `test_no_redeclaration_of_sealed_symbols_1_2_so_6_9_lid`.

## MUST NOT DO

- No download of actual model weights at this seal (measure-don't-assert · schema-level registration acts only; hash pinning is a shape contract for the future download; the download itself is a Track-4 Census Autonomy Service job).
- No presentation of any HF token in any pull path (SO §6.9 clause 3 verbatim: "no `Authorization`/`token=` header ever attached").
- No relabelling of historic overlay detections when regime flips (frozen dataclass structural guarantee).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3.

## NEW ADDITIVE MODULES

`backend/services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (§1.2 modality-extension of CP-M6-1-1 `LanguageIDBackend`).

Test file: `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py` (11 RED-first pins).

## SEALED CARRIERS TO NOT EDIT

- CP-M6-1-1 `services/audio_plane_v1/language_identifier.py` (D10 pluggable-seam · `LanguageIDBackend` + `UnratifiedInferredBackend` + `LanguageIDResult` + `AudioSegment`).
- All CP-AIP-1..10 audio_plane_v1 boundary modules.

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_whisper_lid_registration_act_shape_MIT_licence_pinned_so_6_9_lid`
2. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_voxlingua107_registration_act_shape_apache_2_0_licence_pinned_so_6_9_lid`
3. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_overlay_lid_detection_marker_INFERRED_when_label_set_unmeasured_when_none_b5_4`
4. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_overlay_lid_detection_regime_starts_pre_admission_default_so_6_9`
5. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_lid_do_not_flow_into_counted_measure_posture_marker_present_b5_4`
6. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_admission_gate_default_threshold_is_0_90_pending_so_6_9_lid`
7. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_lid_regime_promotion_requires_owner_receipted_act_canon_8_4_W2`
8. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_lid_nothing_relabelled_at_regime_flip_posture_marker_present_so_6_9`
9. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_hf_pull_wrapper_build_headers_has_no_bearer_like_key_so_6_9_clause_3`
10. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_tenant_labels_pending_honest_gap_english_sheng_code_switched_so_6_9_lid_ratification`
11. `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py::test_no_redeclaration_of_sealed_symbols_1_2_so_6_9_lid`

## LEDGER CHECK

> **Ledger check — this seal implements EXECUTION_ORDER.md Item 5.11.a CP-SO-6.9-LID-WAVE and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal per SO §3.3 · terminal pytest only · BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256 · milestone-seal continuity bundles per SO §6.9(5) AMENDED · GAPS_FIXED_LEDGER append at seal boundary.**

## STOP

- STOP on any `SPEC-CONFLICT-<n>` discovered mid-slice.
- STOP on hard custody/gate violation.
- STOP if the `Ledger check` line cannot be written truthfully at Commit-A/B.
- STOP if any sealed carrier would need edit — additive-only per SO §3.8.
- STOP if RED_pre does not authentically fail with `ModuleNotFoundError`/`ImportError` right-reason on all 11 pins.
- STOP if double-green sweep stripped_sha256 differs between sweep_A and sweep_B.
- STOP if any HTTP pull wrapper header dict contains a bearer-like key at construction (anti-token discipline).

## ANCHORS

- **SO drop anchors:**
  - `STATE/OWNER_DROPS/so_6_9_lid_ratification_20260223/DROP.md` §1-9 verbatim.
  - `STATE/OWNER_DROPS/rms_creds_3_and_multilingual_corpus_20260223/DROP.md` — google-transcripts labelled corpus.
- **Spec anchors (verbatim):**
  - Audio-Plane v1.0 §4.1 N1: "A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."
  - B5.4 shown-not-counted line.
  - Canon 8 §4 W2 receipted-act promotion.
  - §1.2 modality-extension composes sealed symbols; no redeclaration.
  - §6.9 clause 3 anti-token pull hazard scope.
- **Sealed-carrier anchors (composed UNCHANGED per SO §3.8):**
  - `backend/services/audio_plane_v1/language_identifier.py` (CP-M6-1-1 · D10 pluggable-seam · `LanguageIDBackend` protocol + `UnratifiedInferredBackend` placeholder + `LanguageIDResult` + `AudioSegment`).
- **Owner anchors:**
  - RUN-TO-COMPLETION mandate 2026-02-23.
  - SO §6.9 LID RATIFICATION verbatim (both models + admission gate DEFAULT ≥ 90% + TENANT-LABELS-PENDING RESOLVED for 12 languages listed).
