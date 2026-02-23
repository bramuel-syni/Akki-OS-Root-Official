---
ratified_at_utc: 2026-02-23T16:07:00Z
card_id: CP-AIP-LANGUAGE-COGNITION
ledger_item: EXECUTION_ORDER.md · Item 5.12
authority: SO §6.8 standing authority (owner drop `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`)
status: PROMOTED — 2026-02-23T~17:20Z at Item 5.12 State Commit-B (post-Item-5.11.g seal · Item 5.11 wave COMPLETE)
---

# CP-AIP-LANGUAGE-COGNITION — a trained language-identification model for the RMS estate

**Owner authority:** SO §6.8 (2026-02-23) · owner drop `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`. Card drafted from owner text verbatim; builds under standing authority once its RED tests exist. **No GO needed.**

## OBJECTIVE

> "A model that identifies the language of speech in the RMS archive by its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng, Swahili and English, and including code-switched speech where several occur in one utterance — producing per-span labels grounded to the second, so the census can measure language distribution as fact rather than mark it unmeasured." (owner verbatim)

**In canon terms:** A Targeta training run — a LoRA adapter over a Doc-20-registered base (VoxLingua107 or Whisper's encoder), frozen objective at commission, MOAC criteria owner-set, artefact registered with hash and rights posture, admitted to the census by the B5.4 gate. Trained inside the perimeter on tenant material; nothing leaves.

## MUST DO

1. **Feature basis: signature not prosody alone** (Canon 4 §5.4 feature-basis declaration + Doc 20 training-base posture). The model MUST learn phonotactic and spectral structure as PRIMARY signal; prosody, pitch and dynamics are SECONDARY features. The card names the feature basis so the model is evaluated on what it should be learning. Owner verbatim: "The card names the feature basis so the model is evaluated on what it should be learning."

2. **Training material rule** (Canon 4 §5.1 + owner drop 2026-02-23 §Training-material). Baseline = clean, named presenter speech per language, naturally spoken. PLUS labelled code-switched material, per span, so transitions are in the training set. Owner verbatim: "Clean-monolingual alone is a MUST-NOT for the final model" — see MUST NOT §1 below.

3. **Speaker-disjoint splits with N ≥ 20 DEFAULT (tagged pending)** (Canon 4 §5.5 + DAP-31 logic). Minimum of N distinct presenters per language; train and test splits share NO speaker. This is the criterion that separates learning a language from learning a voice. Presenter minimum N is a FORK to `STATE/DESK_QUEUE.md` (DEFAULT = 20).

4. **No-speaker-identification MOAC probe** (DAP-31 logic applied to voices · Canon 8 §Personal-data biometric class). A speaker-identification probe against the artefact MUST fail to exceed chance on held-out presenters. A voice is biometric personal data; an artefact that could return "this is presenter X" does not leave the training run. This is a MOAC criterion — not a hope.

5. **Window and span rule** (Canon 5 §5.3 · owner drop §Window-and-span). Classification per one-to-two-second window; deterministic span rule (minimum span duration + hysteresis on label change) turns windows into language spans. Each span carries its start and end second (C5.3). A window below the confidence threshold is `unmeasured`, NEVER labelled.

6. **MOAC criteria set (every one met or the artefact is refused)** (owner drop §MOAC-criteria):
   - Per-language accuracy on speaker-disjoint real material — DEFAULT ≥ 90% (FORK to DESK_QUEUE).
   - Code-switch span accuracy — boundary within a ruled tolerance AND label correct — DEFAULT ≥ 85% (FORK to DESK_QUEUE).
   - No-speaker-identification probe passed (see §4 above).
   - Abstention rate REPORTED, not hidden.

7. **B5.4 admission by receipted act** (Canon 5 §B5.4 + Canon 8 §W2 receipted flip). On MOAC pass, the model's labels promote from OVERLAY to MEASURE by a receipted act; regime flag changes; NOTHING is relabelled. Until admission, the pre-trained overlay (sealed CP-SO-6.9-LID-WAVE `OverlayLidDetection_v1`) continues to label what it can and returns `unknown` for the rest.

8. **Doc 20 base registration first** (owner drop §Sequence · Doc 20 §training-base). Extend the sealed CP-SO-6.9-LID-WAVE `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` with the Doc 20 training-base posture: hash + licence pinned + LoRA-adapter declaration. Both bases already registered as OVERLAY act at CP-SO-6.9-LID-WAVE; this-card extends registration to TRAINING-BASE posture without redeclaration (§1.2 discipline).

9. **Rights and custody** (Canon 8 §3 + pilot licence §8.3 + DP-SGD default). Labelled corpus is tenant data — RMS custody class applies; training inside the perimeter (E1 pod NEVER data path per Ruling (b) AKKI-RUNS-IT verbatim); artefact belongs to RMS under pilot terms unless elected otherwise (§8.3); DP-SGD default applies unless the owner opts out for this internal run, recorded. DP opt-out is a FORK to DESK_QUEUE.

10. **Corpus assembly under the census assistant's dialogue** (owner drop §Sequence · §coupling). Corpus assembly runs UNDER THE CENSUS ASSISTANT'S DIALOGUE — this is Item 5.11.f (CP-AIP-ASSIST-CENSUS)'s first real objective. The assistant PROPOSES corpus slices; the owner/tenant CONFIRMS; gates DECIDE. Assistant primitives already sealed at 5.11.f (`assist_census_v1.bank_confirmed_assistant_turn` + `assist_census_v1.render_content_registry_entry`) — this-card composes them by identity, no redeclaration.

11. **Training run executes as commissioned Track-4 autonomy job** (owner drop §Execution-reach · Ruling (b) verbatim). Training run executes inside the Akki perimeter as a commissioned job per Track-4 wiring (sealed CP-TRACK-4-AUTONOMY-WIRING `training_runs` job kind). Akki runs it; E1 wires and STEPS BACK.

12. **Sequence** (owner drop §Sequence verbatim): register base → assemble and label the corpus under the census assistant's dialogue → commission with the frozen criteria → train → MOAC → admit → promote.

## MUST NOT DO

1. **Clean-monolingual training corpus alone** (owner verbatim: "Clean-monolingual alone is a MUST-NOT for the final model"). The final model refuses commission if the labelled training set carries NO code-switched material per span.

2. **Speaker overlap between train and test splits** (see MUST-DO §3). Splits sharing any presenter is refused.

3. **Artefact that identifies presenters above chance** (see MUST-DO §4). No-speaker-ID MOAC probe failure refuses MOAC and refuses admission — the artefact does NOT leave the training run.

4. **Labelling a below-confidence window** (see MUST-DO §5). Below-confidence windows are `unmeasured`, NEVER labelled with any language.

5. **Relabelling prior overlay labels at regime flip** (see MUST-DO §7). Overlay→measure promotion is a receipted act; regime flag changes; NOTHING is relabelled retrospectively.

6. **Pod as data path or training host** (Ruling (b) AKKI-RUNS-IT verbatim). E1's pod is NEVER the training host and NEVER a data path. Training compute + labelled corpus NEVER leave Akki's boundary. Registration of training-base MUST refuse `pod://*` and `/app/*` prefixed refs.

7. **Redeclaration of sealed CP-SO-6.9-LID-WAVE + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS symbols** (§1.2 discipline). Compose by identity; never redeclare.

8. **Silent MOAC threshold change** (owner verbatim: "MOAC criteria owner-set"). Threshold changes require a new owner-set frozen criteria contract; the artefact from a silently-changed threshold is refused admission.

9. **Mock training-run execution** (owner drop §Execution-reach verbatim: "commissioned-job contract with honest-gap on execution, never a mock"). If in-pod compute cannot honestly run even a small LoRA pass, the commissioned-job contract carries an honest-gap on execution — never a mock or a stub.

## NEW ADDITIVE MODULES

1. `backend/services/audio_plane_v1/language_cognition_v1.py` (~350 lines) — Targeta training-run boundary specific to language cognition:
   - `LanguageCognitionBoundaryRefused` (base) + specialised refusal subclasses:
     - `CleanMonolingualOnlyRefused` (MUST NOT §1).
     - `SpeakerOverlapRefused` (MUST NOT §2).
     - `SpeakerIdentifiableArtefactRefused` (MUST NOT §3).
     - `BelowConfidenceLabelRefused` (MUST NOT §4).
     - `RelabellingAtRegimeFlipRefused` (MUST NOT §5).
     - `PodAsDataPathRefused` (MUST NOT §6 · reuses sealed `PodIsNeverDataPathAtTrack4Error` posture).
     - `SilentMoacThresholdChangeRefused` (MUST NOT §8).
     - `MockTrainingRunRefused` (MUST NOT §9).
   - **Frozen carriers:**
     - `LanguageCognitionFeatureBasis_v1` — Final tuple declaring phonotactic + spectral structure as PRIMARY features; prosody/pitch/dynamics as SECONDARY.
     - `LanguageCognitionTrainingBaseRegistration_v1` — Doc 20 training-base extension carrier composing sealed `LidModelRegistration_v1` by identity + `lora_adapter_declaration` field.
     - `SpeakerDisjointSplitContract_v1` — presenter_minimum_n (DEFAULT 20 · tagged pending) + train/test share_no_speaker=True Final.
     - `NoSpeakerIdMoacProbe_v1` — held_out_presenter_set + chance_level_threshold + probe_passed carrier.
     - `WindowAndSpanRule_v1` — window_seconds_range (1.0, 2.0) + min_span_duration_seconds + hysteresis_frames + below_confidence_marker=`unmeasured`.
     - `LanguageCognitionMoacContract_v1` — per_language_accuracy_default=0.90 + code_switch_span_accuracy_default=0.85 + no_speaker_id_probe_passed=True + abstention_rate_reported=True.
     - `B5_4_AdmissionReceiptedAct_v1` — receipted act composing sealed `promote_lid_regime_by_receipted_act` by identity.
     - `RmsCustodyRightsPosture_v1` — custody_class=`RMS_TENANT` + in_perimeter_training=True + artefact_ownership_ref=pilot 8.3 + dp_sgd_default=True + dp_opt_out_ref (nullable).
     - `LanguageCognitionCorpusAssemblyPosture_v1` — assistant_module_ref points at sealed `assist_census_v1` (5.11.f) + workflow_kind=`propose_confirm_gate_decide`.
   - **Posture markers (Final str · owner verbatim):**
     - `SIGNATURE_NOT_PROSODY_ALONE_POSTURE` citing MUST-DO §1 verbatim.
     - `CLEAN_MONOLINGUAL_ALONE_MUST_NOT_POSTURE` citing MUST-NOT §1 verbatim.
     - `NO_SPEAKER_ID_MOAC_POSTURE` citing MUST-DO §4 verbatim + DAP-31-logic-applied-to-voices annotation.
     - `BELOW_CONFIDENCE_UNMEASURED_NEVER_LABELLED_POSTURE` citing MUST-DO §5 verbatim.
     - `NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE` (re-declares CP-SO-6.9-LID-WAVE's `LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE` scope for language cognition without symbol redeclaration).
     - `POD_NEVER_DATA_PATH_POSTURE_LANGUAGE_COGNITION` composing sealed CP-TRACK-4 `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4`.
     - `E1_WIRES_AND_STEPS_BACK_POSTURE_LANGUAGE_COGNITION` composing sealed CP-TRACK-4 `E1_STEPS_BACK_AFTER_WIRING_POSTURE`.
     - `TRAINING_ARTEFACT_NEVER_LEAVES_PERIMETER_POSTURE`.
     - `CORPUS_ASSEMBLY_UNDER_ASSISTANT_DIALOGUE_POSTURE`.

2. `backend/services/audio_plane_v1/language_cognition_corpus_seam_v1.py` (~150 lines · corpus-assembly seam under CP-AIP-ASSIST-CENSUS dialogue):
   - Boundary callables composing sealed 5.11.f `bank_confirmed_assistant_turn` + `render_content_registry_entry` by identity for corpus-slice proposals + owner-confirmation banking.
   - `CorpusChannelUnreachableHonestGap_v1` Final carrier declaring DQ-17 family (Weego/NAS credential rotations) as the ONLY gate on corpus assembly — recorded as a FACT, not a policy hold.
   - `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple: `("Kikuyu", "Luo", "Sheng", "Swahili", "English")`.

## SEALED CARRIERS TO NOT EDIT (§3.8 additive-only · §1.2 modality-extension composing by identity)

- `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE) — `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `LidAdmissionGate_v1` + `promote_lid_regime_by_receipted_act` all composed by identity; NO redeclaration.
- `services/audio_plane_v1/census_three_waves_v1.py` (CP-CENSUS-THREE-WAVES).
- `services/audio_plane_v1/training_run_boundary_v1.py` (CP-AIP-10-TRAINING-RUNS) — training-run boundary composed by identity.
- `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING) — `training_runs` job kind composed by identity for commissioned-job execution.
- `services/census_autonomy/assist_census_v1.py` (CP-AIP-ASSIST-CENSUS) — `bank_confirmed_assistant_turn` + `render_content_registry_entry` composed by identity for corpus-assembly under-dialogue seam.
- `services/entitlement_service_v1/pilot_licence_seeds_v1.py` (CP-ENT-16) — RMS pilot licence terms §8.3 composed by identity for artefact ownership.
- `services/entitlement_service_v1/tenant_separation_v1.py` (CP-TENANT-SEPARATION) — RMS custody class composed by identity.
- `services/census_autonomy/engine.py` (R-106 sealed).

## EXIT (RED-first invariant node IDs)

Minimum 12 RED-first structural pins mapping to card lines:

1. `tests/invariants/test_cp_aip_language_cognition.py::test_signature_not_prosody_alone_feature_basis_declared`
2. `tests/invariants/test_cp_aip_language_cognition.py::test_clean_monolingual_alone_must_not_refusal_at_commission`
3. `tests/invariants/test_cp_aip_language_cognition.py::test_speaker_disjoint_split_contract_shape_frozen_n_default_20_tagged_pending`
4. `tests/invariants/test_cp_aip_language_cognition.py::test_no_speaker_id_moac_probe_shape_and_chance_level_threshold`
5. `tests/invariants/test_cp_aip_language_cognition.py::test_window_and_span_rule_1_to_2_second_window_min_duration_hysteresis_below_confidence_unmeasured`
6. `tests/invariants/test_cp_aip_language_cognition.py::test_moac_contract_shape_frozen_per_language_90_code_switch_span_85_no_speaker_id_pass_abstention_reported`
7. `tests/invariants/test_cp_aip_language_cognition.py::test_b5_4_admission_receipted_overlay_to_measure_promotion_nothing_relabelled`
8. `tests/invariants/test_cp_aip_language_cognition.py::test_doc_20_training_base_registration_extends_sealed_lid_registrations_no_redeclaration`
9. `tests/invariants/test_cp_aip_language_cognition.py::test_rms_custody_in_perimeter_training_dp_sgd_default_carrier_shape`
10. `tests/invariants/test_cp_aip_language_cognition.py::test_corpus_assembly_under_assistant_dialogue_composes_sealed_assist_census_by_identity`
11. `tests/invariants/test_cp_aip_language_cognition.py::test_training_run_commissioned_track_4_job_kind_training_runs_composed_by_identity_pod_never_data_path`
12. `tests/invariants/test_cp_aip_language_cognition.py::test_no_redeclaration_of_sealed_symbols_1_2_language_cognition`

Additional pins as needed for the 5 target-language tuple + `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final anchor + `CorpusChannelUnreachableHonestGap_v1` DQ-17 gate FACT.

## STOP

- STOP if any of the MUST-NOT §§1-9 fires — the artefact is refused, the seal does not close.
- STOP if `pytest tests/invariants/test_cp_aip_language_cognition.py` does not reach GREEN post-authorship of the additive modules.
- STOP if the sealed CP-SO-6.9-LID-WAVE / CP-TRACK-4-AUTONOMY-WIRING / CP-AIP-ASSIST-CENSUS carriers are edited (SO §3.8 additive-only).
- STOP if double-green `BASELINE_GUARD=1 PYTHONHASHSEED=0` stripped_sha256 does not match byte-identically between sweep_A and sweep_B.
- STOP if corpus-channel-unreachable honest-gap is falsified — the DQ-17 family credential rotation status is a FACT, not a policy hold.

## ANCHORS (§6.3 rule 1 — underlying components this builds on)

- **CP-SO-6.9-LID-WAVE (Item 5.11.a · SEALED 2026-02-23T~12:55Z)** — `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` + `LidAdmissionGate_v1` + `OverlayLidDetection_v1` + `promote_lid_regime_by_receipted_act`. This card extends the OVERLAY-scope registration to TRAINING-BASE scope + composes the admission gate + composes the receipted overlay→measure promotion by identity.
- **CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY (Item 5.11.c · SEALED 2026-02-23T~14:15Z)** — `CENSUS_THREE_WAVES` overlay-from-first-run structural sequencing.
- **CP-ENT-16-PILOT-LICENCE-SEEDS (Item 5.11.b · SEALED 2026-02-23T~13:40Z)** — RMS pilot licence carrier for artefact ownership per §8.3.
- **CP-TENANT-SEPARATION (Item 5.11.d · SEALED 2026-02-23T~14:40Z)** — RMS tenant custody class.
- **CP-TRACK-4-AUTONOMY-WIRING (Item 5.11.e · SEALED 2026-02-23T~15:22Z)** — `training_runs` job kind for commissioned-training execution + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` + `E1_STEPS_BACK_AFTER_WIRING_POSTURE`.
- **CP-AIP-ASSIST-CENSUS (Item 5.11.f · SEALED 2026-02-23T~16:05Z THIS-TURN)** — `bank_confirmed_assistant_turn` + `render_content_registry_entry` + six binding conditions verbatim as the consumer path for corpus-slice proposals under owner/tenant confirmation.
- **CP-AIP-10-TRAINING-RUNS (Item 5.11 pre-wave · SEALED 2026-02-23T~12:10Z)** — training-run boundary carrier.
- **Doc 20 canon** — training-base registration posture (hash + licence + LoRA-adapter declaration).
- **Canon 4 §5.1 + §5.4 + §5.5** — feature basis + defensibility matrix + speaker-disjoint splits.
- **Canon 5 §5.3** — per-span start/end second grounding.
- **Canon 5 §B5.4** — admission gate.
- **Canon 8 §W2** — receipted act for regime flip.
- **Canon 8 §3 + pilot licence §8.3** — RMS custody + artefact ownership.
- **DAP-31** — biometric personal data · logic applied to voices for no-speaker-ID MOAC.

## RATIFICATION

Card drafted from owner order verbatim (banked at `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`). SO §6.8 standing authority — builds under standing authority once its RED tests exist. No GO needed.

**Forks to DESK_QUEUE (not holds · DEFAULTs stand meanwhile):**
- Presenter minimum N (DEFAULT 20).
- Per-language accuracy threshold (DEFAULT ≥90%).
- Code-switch span accuracy threshold (DEFAULT ≥85%).
- DP opt-out (DEFAULT DP-SGD applies).

**Card status:** QUEUED at `STATE/OBJECTIVES/queued/CP_AIP_LANGUAGE_COGNITION.md`. Promoted to `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` at Item 5.12 open post-Item-5.11.g seal, card_sha256 computed and pinned at that boundary.
