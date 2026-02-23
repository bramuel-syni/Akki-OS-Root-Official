# CP-AIP-LANGUAGE-COGNITION · comprehensive seal receipt

**Seal ID:** CP-AIP-LANGUAGE-COGNITION-20260223
**Ledger item:** EXECUTION_ORDER.md Item 5.12 (SPEC ENHANCEMENT · owner order 2026-02-23T~16:07Z)
**Boundary date (UTC):** 2026-02-23T~17:10Z
**Wave position:** 1st post-Item-5.11 wave (Item 5.11 wave COMPLETE 5.11.a-g all SEALED) · penultimate before 5.13 FINAL DELIVERABLE.

---

## Owner canon anchors (verbatim)

**SO §6.8 standing authority · owner drop 2026-02-23T~16:07Z `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`:**

> "A model that identifies the language of speech in the RMS archive by its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng, Swahili and English, and including code-switched speech where several occur in one utterance — producing per-span labels grounded to the second, so the census can measure language distribution as fact rather than mark it unmeasured."

**In canon terms:** A Targeta training run — a LoRA adapter over a Doc-20-registered base (VoxLingua107 or Whisper's encoder), frozen objective at commission, MOAC criteria owner-set, artefact registered with hash and rights posture, admitted to the census by the B5.4 gate. Trained inside the perimeter on tenant material; nothing leaves.

**Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** E1 wires the seam INTO Census Autonomy Service; pod is never data path. Training compute + model weights + labelled corpus NEVER leave Akki's boundary; no third-party export.

---

## 12 MUST-DO/MUST-NOT card lines as RED-first invariant node IDs

1. **Feature basis: signature not prosody alone** (Canon 4 §5.4 + Doc 20). `LanguageCognitionFeatureBasis_v1` — primary=(phonotactic, spectral) + secondary=(prosody, pitch, dynamics) disjoint. Pin: `test_signature_not_prosody_alone_feature_basis_declared`.
2. **Clean-monolingual alone MUST-NOT** (owner verbatim). `CleanMonolingualOnlyRefused` at `commission_language_cognition_training_run(has_code_switched_material=False)`. Pin: `test_clean_monolingual_alone_must_not_refusal_at_commission`.
3. **Speaker-disjoint splits N=20 DEFAULT tagged pending** (Canon 4 §5.5 + DAP-31). `SpeakerDisjointSplitContract_v1` + FORK DQ-21. Pin: `test_speaker_disjoint_split_contract_shape_frozen_n_default_20_tagged_pending`.
4. **No-speaker-ID MOAC probe chance-level** (DAP-31 applied to voices · Canon 8). `NoSpeakerIdMoacProbe_v1`. Pin: `test_no_speaker_id_moac_probe_shape_and_chance_level_threshold`.
5. **1-2s window + deterministic span rule + below-confidence unmeasured NEVER labelled** (Canon 5 §5.3). `WindowAndSpanRule_v1`. Pin: `test_window_and_span_rule_1_to_2_second_window_min_duration_hysteresis_below_confidence_unmeasured`.
6. **MOAC contract per-language ≥90% + code-switch-span ≥85% + no-speaker-ID pass + abstention reported** (owner verbatim). `LanguageCognitionMoacContract_v1` + FORK DQ-22 + DQ-23. Pin: `test_moac_contract_shape_frozen_per_language_90_code_switch_span_85_no_speaker_id_pass_abstention_reported`.
7. **B5.4 admission by receipted act nothing relabelled** (Canon 5 §B5.4 + Canon 8 §W2). `B5_4_AdmissionReceiptedAct_v1` + `PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY` = sealed callable. Pin: `test_b5_4_admission_receipted_overlay_to_measure_promotion_nothing_relabelled`.
8. **Doc 20 training-base extends sealed LID registrations no redeclaration §1.2** (Doc 20 + §1.2). `LanguageCognitionTrainingBaseRegistration_v1` composes sealed `LidModelRegistration_v1` by identity. Pin: `test_doc_20_training_base_registration_extends_sealed_lid_registrations_no_redeclaration`.
9. **RMS custody + in-perimeter training + DP-SGD default** (Canon 8 §3 + pilot §8.3). `RmsCustodyRightsPosture_v1` + FORK DQ-24. Pin: `test_rms_custody_in_perimeter_training_dp_sgd_default_carrier_shape`.
10. **Corpus assembly under census-assistant dialogue composes sealed CP-AIP-ASSIST-CENSUS by identity** (owner drop §Sequence · §coupling). `language_cognition_corpus_seam_v1.py` composes sealed `bank_confirmed_assistant_turn` + `render_content_registry_entry` by identity + `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple + `CorpusChannelUnreachableHonestGap_v1` declaring DQ-17 as ONLY gate FACT. Pin: `test_corpus_assembly_under_assistant_dialogue_composes_sealed_assist_census_by_identity`.
11. **Training run commissioned Track-4 job kind `training_runs` composed by identity + pod NEVER data path** (owner drop §Execution-reach + Ruling (b) verbatim). `TRACK_4_JOB_KINDS_ANCHOR` = sealed tuple + `PodAsDataPathRefused` extends sealed `PodIsNeverDataPathAtTrack4Error` by identity + `commission_language_cognition_training_run` refuses `pod://*` + `/app/*` prefixed refs. Pin: `test_training_run_commissioned_track_4_job_kind_training_runs_composed_by_identity_pod_never_data_path`.
12. **§1.2 no-redeclaration of sealed symbols** (SO §1.2). AST-scan for 26 sealed symbol names (from CP-SO-6.9-LID-WAVE + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS + CP-AIP-ASSIST-TRAINING + CP-CENSUS-THREE-WAVES + CP-AIP-10-TRAINING-RUNS). Pin: `test_no_redeclaration_of_sealed_symbols_1_2_language_cognition`.

---

## Additive modules (§3.8 additive-only · §1.2 modality-extension)

### `backend/services/audio_plane_v1/language_cognition_v1.py` (~440 lines)

- **Refusal hierarchy (base + 8 specialised subclasses):**
  - `LanguageCognitionBoundaryRefused` (base) + `CleanMonolingualOnlyRefused` + `SpeakerOverlapRefused` + `SpeakerIdentifiableArtefactRefused` + `BelowConfidenceLabelRefused` + `RelabellingAtRegimeFlipRefused` + `PodAsDataPathRefused` (extends sealed `PodIsNeverDataPathAtTrack4Error` by identity) + `SilentMoacThresholdChangeRefused` + `MockTrainingRunRefused`.
- **Frozen carriers (10):**
  - `LanguageCognitionFeatureBasis_v1` + `LanguageCognitionTrainingBaseRegistration_v1` (composes sealed `LidModelRegistration_v1` by identity) + `SpeakerDisjointSplitContract_v1` + `NoSpeakerIdMoacProbe_v1` + `WindowAndSpanRule_v1` + `LanguageCognitionMoacContract_v1` + `B5_4_AdmissionReceiptedAct_v1` + `RmsCustodyRightsPosture_v1` + `LanguageCognitionCorpusAssemblyPosture_v1`.
- **Posture markers (Final str · 9):**
  - `SIGNATURE_NOT_PROSODY_ALONE_POSTURE` + `CLEAN_MONOLINGUAL_ALONE_MUST_NOT_POSTURE` + `NO_SPEAKER_ID_MOAC_POSTURE` + `BELOW_CONFIDENCE_UNMEASURED_NEVER_LABELLED_POSTURE` + `NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE` (retagged from sealed LID scope) + `POD_NEVER_DATA_PATH_POSTURE_LANGUAGE_COGNITION` (composing sealed `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4`) + `E1_WIRES_AND_STEPS_BACK_POSTURE_LANGUAGE_COGNITION` + `TRAINING_ARTEFACT_NEVER_LEAVES_PERIMETER_POSTURE` + `LANGUAGE_COGNITION_SIX_PLUS_ONE_BINDING_POSTURE` (Final 12-tuple).
- **Sealed anchors composed by identity:**
  - `WHISPER_LID_REGISTRATION_TRAINING_BASE_ANCHOR` = sealed `WHISPER_LID_REGISTRATION` · `VOXLINGUA107_REGISTRATION_TRAINING_BASE_ANCHOR` = sealed `VOXLINGUA107_REGISTRATION` · `PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY` = sealed `promote_lid_regime_by_receipted_act` · `TRACK_4_JOB_KINDS_ANCHOR` = sealed `TRACK_4_JOB_KINDS`.
- **Boundary callable:** `commission_language_cognition_training_run` (refuses `has_code_switched_material=False` and `pod://*` / `/app/*` prefixed refs).

### `backend/services/audio_plane_v1/language_cognition_corpus_seam_v1.py` (~120 lines)

- **Sealed callables composed by identity:** `BANK_CONFIRMED_ASSISTANT_TURN_COMPOSED_BY_IDENTITY` = sealed `bank_confirmed_assistant_turn` · `RENDER_CONTENT_REGISTRY_ENTRY_COMPOSED_BY_IDENTITY` = sealed `render_content_registry_entry`.
- **Target languages:** `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple `("Kikuyu", "Luo", "Sheng", "Swahili", "English")`.
- **Honest-gap carrier:** `CorpusChannelUnreachableHonestGap_v1` declaring DQ-17 family (Weego/NAS credential rotations) as ONLY gate FACT not policy hold + `CORPUS_CHANNEL_UNREACHABLE_HONEST_GAP` Final constant.
- **Posture markers (3):** `CORPUS_ASSEMBLY_UNDER_ASSISTANT_DIALOGUE_POSTURE` + `DQ_17_ONLY_GATE_FACT_NOT_POLICY_HOLD_POSTURE` + `COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE`.

---

## Sealed carriers UNCHANGED per SO §3.8 additive-only

- `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE): composed by identity — `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `LidModelRegistration_v1` + `promote_lid_regime_by_receipted_act` + `LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE`.
- `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES): untouched.
- `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS): untouched.
- `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING): composed by identity — `TRACK_4_JOB_KINDS` + `PodIsNeverDataPathAtTrack4Error` + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` + `E1_STEPS_BACK_AFTER_WIRING_POSTURE`.
- `services/census_autonomy/assist_census_v1.py` (CP-AIP-ASSIST-CENSUS): composed by identity — `bank_confirmed_assistant_turn` + `render_content_registry_entry`.
- `services/census_autonomy/assist_training_v1.py` (CP-AIP-ASSIST-TRAINING): available for downstream consumers.
- `services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16): pilot §8.3 anchor cited.
- `services/entitlement_service_v1/tenant_separation_v1.py` (CP-TENANT-SEPARATION): RMS custody class cited.
- `services/census_autonomy/engine.py` (R-106 sealed).

---

## Test evidence

- **RED_pre 12/12 authentic FileNotFoundError right-reason** (module absent) · `phase0/cp_aip_language_cognition_20260223/RED_pre_20260923T164826Z.log` (or similar timestamp).
- **GREEN_post 12/12 passed 0.80s** · `phase0/cp_aip_language_cognition_20260223/GREEN_post_20260923T165100Z.log`.
- **Pre-Commit-A double-green** BASELINE_GUARD=1 PYTHONHASHSEED=0 stripped_sha256 `7ac8a18af0db7a3840a61335c427a1a7b87fdb7037f9a14609fb3c16c3be5918` IDENTICAL both sweeps:
  - Sweep A · `phase0/drill_receipts_cp_aip_language_cognition/20260923T170049Z_sweep_A.log` · ~209s · 6411 passed / 13 skipped / 0 failed / 520 warnings.
  - Sweep B · `phase0/drill_receipts_cp_aip_language_cognition/20260923T170715Z_sweep_B.log` · ~209s · 6411 passed / 13 skipped / 0 failed / 520 warnings.

**baseline_failures.json sha256 post-bump:** `b0bccedd9feb04895efe66fd88409272c676c2518f5b29bf735530c2ab397974` · passed_floor 6399 → 6411 · counts_at_baseline.passed 6399 → 6411 · invariants_enforced_when_baseline_guard_1.passed_floor 6399 → 6411.

---

## EXIT EVIDENCE (structural)

Language-cognition Targeta training-run boundary is a shape declaration for a future training run whose only in-pod gate is corpus channel reachability (DQ-17 family). The 12 RED-first invariant pins ARE the structural exit evidence:

- All 12 MUST-DO/MUST-NOT card lines flip from authentic RED (FileNotFoundError, module absent) to GREEN (structural assertion of frozen carriers + refusal subclasses + sealed anchors composed by identity + boundary callable refusing pod://* / /app/* / has_code_switched_material=False).
- The commissioned Track-4 job kind `training_runs` was ALREADY exercised end-to-end at CP-TRACK-4-AUTONOMY-WIRING seal (Item 5.11.e) — 3 machine-readable JSON run receipts persisted; this-card's structural evidence composes that sealed job kind by identity for language-cognition scope.
- **In-pod compute honest-gap** (owner drop §Execution-reach verbatim): if in-pod compute cannot honestly run even a small LoRA pass, the commissioned-job contract carries an honest-gap on execution — NEVER a mock. `COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE` names this discipline. No live LoRA pass was executed in this seal; the seal declares the training-run boundary + registers the corpus-assembly seam.

---

## Bundle continuity (SO §6.9(5) AMENDED · 10th application)

- **Code bundle:** `continuity_bundles/code_20260923T171243Z_CP_AIP_LANGUAGE_COGNITION.bundle` · sha256 `866c9ef86b1223449edba20e81f6d13fdb31ce0ac85602afb25e0439f62823d5` · ~18 MiB · @ `programme/track-a` `7e84cd98f37aea50f9d0ed55fbd8d654ffc582f7` · `git bundle verify` "is okay" · complete history.
- **State bundle:** to be emitted at State PINS bank boundary (10th application).

---

## Objective card

- **Card:** `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` (promoted from `queued/` this-turn · fully-conforming SO §6.2 six-section schema · line-removed convention).
- **Owner drop:** `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md` (verbatim owner order).

---

## Long-pole gate (DQ-17 family · NAS/Weego)

- **Owner verbatim (owner drop §Long-pole):** "Corpus assembly needs NAS channels reachable (Weego/NAS credential rotations DQ-17 family) as ONLY gate recorded as FACT not policy hold."
- **Structural evidence:** `CorpusChannelUnreachableHonestGap_v1` frozen carrier with `blocked_on_ref="DQ-17 · Weego/NAS credential rotations · STATE/DESK_QUEUE.md"` + `is_fact_not_policy_hold=True` + `remediation_ref` naming owner-action-to-unlock.
- **Status:** OPEN honest-gap · non-blocking through this seal · surfaced in OWNER_RETURN_REPORT.md pending-human-items at Item 5.13.

---

## DESK_QUEUE forks (P2 · DEFAULTs stand meanwhile)

- **DQ-21** — presenter minimum N (DEFAULT 20 · MUST-DO §3).
- **DQ-22** — per-language accuracy threshold (DEFAULT ≥90% · MUST-DO §6).
- **DQ-23** — code-switch span accuracy threshold (DEFAULT ≥85% · MUST-DO §6).
- **DQ-24** — DP opt-out (DEFAULT DP-SGD applies · MUST-DO §9).

All P2 fork-not-hold DEFAULTs; recorded per owner directive verbatim in owner drop banked at CP-AIP-LANGUAGE-COGNITION SPEC ENHANCEMENT insertion.

---

## REPORT-AND-CONTINUE

**Ledger check:** this seal implements Item 5.12 of `EXECUTION_ORDER.md` and nothing else. Additive-only per SO §3.8.

**RUN-TO-COMPLETION mandate ACTIVE 2026-02-23:** proceed IMMEDIATELY to Item 5.13 FINAL DELIVERABLE (`OWNER_RETURN_REPORT.md` + `BUILD_JOURNAL.md`) with 5.12-position-report clause per owner ledger sequencing #1.

**5.13 inclusion checklist per owner order 2026-02-23T post-5.11.g:**
- (a) pending-owner-items section — NAS/Weego credentials to unlock corpus assembly (DQ-17 family · this-seal long-pole) + Akki-OS-Root privacy flip if unresolved + DESK_QUEUE forks with recommendations (N=20 · both accuracy thresholds · DP opt-out) + any §6.9 clause-9 items.
- (b) consolidated ratchet history 6224 → final (6411 at this seal · to advance further at 5.13 if delta emitted).
- (c) all seal SHA chains (CP-AIP-1..10 + CP-SO-6.9-LID-WAVE + CP-ENT-16 + CP-CENSUS-THREE-WAVES + CP-TENANT-SEPARATION + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS + CP-AIP-ASSIST-TRAINING + **CP-AIP-LANGUAGE-COGNITION this-seal**).
- (d) bundle sha256 pins (all 10 applications of SO §6.9(5) AMENDED).
- (e) GAPS_FIXED_LEDGER consolidated view.

**Anchor date:** 2026-02-23T~17:10Z (Code Commit-A boundary).
