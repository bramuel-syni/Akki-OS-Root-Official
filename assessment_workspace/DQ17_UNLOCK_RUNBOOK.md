# DQ-17 Unlock Runbook — end-to-end path for CP-AIP-LANGUAGE-COGNITION live execution

**Purpose:** the exact sequence from owner-side NAS/Weego credential rotation to a MEASURED-regime B5.4 admission of the trained language-identification model. This is a **docs-only runbook** — it does not authorise autonomous execution; the sealed refusals + posture markers still bind every step below.

**Ledger anchor:** Item 5.12 (`CP-AIP-LANGUAGE-COGNITION` SEALED at 2026-02-23T~17:28Z · State mini-bank `3158ca2d`). This runbook is the docs companion to Item 5.13 §6.1 (DQ-17 long-pole) — cross-referenced from `OWNER_RETURN_REPORT.md` §6.1.

**Authority:** SO §6.9 amendment + owner drop 2026-02-23T~16:07Z (`STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`) + Ruling (b) AKKI-RUNS-IT verbatim. Six-plus-one binding conditions per the sealed 12 MUST-DO/MUST-NOT card lines.

---

## Preconditions (all currently satisfied · listed for the record)

1. **Sealed boundary present.** `backend/services/audio_plane_v1/language_cognition_v1.py` (~440 lines · `commission_language_cognition_training_run` boundary + 10 frozen carriers + 9 posture markers + 4 sealed anchors composed by identity) is landed on `programme/track-a` @ `7e84cd98f37aea50f9d0ed55fbd8d654ffc582f7`.
2. **Corpus-assembly seam present.** `backend/services/audio_plane_v1/language_cognition_corpus_seam_v1.py` (~120 lines · composes sealed CP-AIP-ASSIST-CENSUS primitives by identity) is landed on the same head.
3. **Track-4 wiring live.** `training_runs` job kind is a sealed Census Autonomy job (CP-TRACK-4-AUTONOMY-WIRING · 5.11.e); engine has executed a contract-level receipt at 2026-09-23T14:48:03Z (`phase0/track_4_autonomy_engine_run_receipts/20260923T144803Z_training_runs_engine_run_receipt.json` · `engine_live_status=COMPLETE`).
4. **Baseline invariants held.** `passed_floor = 6411` · `baseline_failures.json` sha256 `b0bccedd9feb04895efe66fd88409272c676c2518f5b29bf735530c2ab397974` byte-verified.
5. **DP-SGD toolchain provisioning.** *Unmeasured on this pod.* Owner action separately if DQ-24 opts out of DP-SGD (see §3.4 below).

---

## Step 1 · Owner drops rotated NAS/Weego credentials (unblocks corpus channel)

### 1.1 · What the loader currently expects (per `tools/rms_creds_loader_v2.py`)

Credentials are loaded from an **xlsx-based drop path**, not `.env.local`. This is the shape the sealed code expects today.

**Primary drop path (current v2 sheet):**
```
/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx
```
Structure (verbatim from the loader module docstring):
- Single sheet: `Sheet1`
- 5-column data layout: `[schema, host, user, password, tag]`
- MySQL clusters only (7 clusters with creds + 1 without cred)

**Legacy drop path (JUMP + NAS + Radio + Huawei tabs — this v2 loader falls back here for NAS + Weego):**
```
/app/assessment_workspace/custody/credentials/prior_baseline/d778eb1e_prior_baseline.xlsx
```
Structure (verbatim from `rms_creds_loader_v2.py::NASSite` dataclass):
- Tab: `NAS Guide + Cred` (existing legacy tab name).
- Row shape per NAS site:
  - `dsm_url` — Synology DSM URL for the NAS.
  - `user` — service account user.
  - `password` — service account password.
  - `navigation_steps` — list of "click-through" strings the loader will replay to reach the audio channel root (typically 3-5 rows below the cred row).
  - `channel_registry` — list of dicts naming each Weego audio channel by path + folder-tree entry point.
- Loader discipline: values held **in memory only** · `describe()` emits only `<cred len=N>` shape · **NEVER prints raw values**.

### 1.2 · Rows the owner MUST refresh at rotation

For each RMS/Weego NAS site currently 403-refusing at reachability probe (see `phase0/connectivity_receipts/20260921T14*Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json`):

| Row | Field | Current status | Owner action |
|---|---|---|---|
| A | `dsm_url` | pinned in legacy sheet | verify still points to live DSM (Synology URL) |
| B | `user` | rotated externally | drop rotated value at row B same cell |
| C | `password` | rotated externally | drop rotated value at row C same cell |
| D | `navigation_steps` | pinned | leave unless directory structure changed |
| E | `channel_registry` | pinned | leave unless Weego added/removed channels |

**Delivery mode:** direct xlsx replacement at `/app/assessment_workspace/custody/credentials/prior_baseline/d778eb1e_prior_baseline.xlsx` (encrypted transport per SO §3.4 secret-value-never-in-logs). Existing sealed loader picks up the new values on next process spawn — no code change needed.

### 1.3 · Optional alternative: `.env.local` shim (would require one small additive card)

If the owner prefers env-based rotation over xlsx replacement (e.g., for K8s Secret injection compatibility), it would require **one additive card** (not covered by this runbook; would be Item 6.x on a future ledger):

- **New env keys** (naming proposed here, subject to owner ratification):
  ```
  RMS_NAS_DSM_URL_<SITE_ID>       (e.g. RMS_NAS_DSM_URL_S1)
  RMS_NAS_USER_<SITE_ID>
  RMS_NAS_PASSWORD_<SITE_ID>
  RMS_WEEGO_CHANNEL_PATHS_<SITE_ID>   (JSON-encoded list of channel paths)
  ```
- **New loader shim:** `tools/rms_creds_loader_env_v3.py` — reads env-first, falls back to xlsx per current v2. Would compose the sealed loader dataclasses by identity (`NASSite` / `HostCred` / `MySQLCluster`) with no redeclaration.
- **RED-first pins:** `test_env_shim_composes_xlsx_loader_by_identity` + `test_env_shim_refuses_missing_required_keys` + `test_env_shim_never_logs_raw_values`.

**Owner decision required on this alternative** — until then, the xlsx path at §1.1/1.2 is the single sealed route.

### 1.4 · Verification of reachability post-rotation

After the drop, the pod runs (autonomously if scheduled; or on the owner's on-demand trigger via `/api/portal/census/run`):
```
python3 tools/full_estate_read_capability_sweep_20260921_freshcreds.py
```
This writes a fresh receipt to `phase0/connectivity_receipts/<timestamp>_FULL_ESTATE_read_capability_sweep_freshcreds.json` showing each NAS site's status as `readable` (unlocks corpus-assembly) or still `blocked` (each blocked site is a distinct honest-gap; the DQ-17 CorpusChannelUnreachableHonestGap_v1 clears when at least one channel with the target languages goes readable).

---

## Step 2 · Corpus assembly under the Census Assistant dialogue

**Sealed anchor:** `services/audio_plane_v1/language_cognition_corpus_seam_v1.py` composes `services/census_autonomy/assist_census_v1.bank_confirmed_assistant_turn` + `.render_content_registry_entry` by identity (verified via `BANK_CONFIRMED_ASSISTANT_TURN_COMPOSED_BY_IDENTITY` + `RENDER_CONTENT_REGISTRY_ENTRY_COMPOSED_BY_IDENTITY` Final markers).

**What the owner sees at this stage (per the six binding conditions verbatim):**

Six binding conditions apply — every one must hold at every assistant turn:

1. **No path to any decision.** The Census Assistant module does NOT import any decision-boundary module (verified structurally by the sealed negative-scan import isolation test). The assistant can only **PROPOSE** corpus slices; the owner/tenant **CONFIRMS**; sealed gates **DECIDE**.
2. **Confirmed turns only banked.** Only turns carrying a valid A5.16 receipted-provenance ref (`a5_16_receipt_ref` field on `CensusAssistantConfirmedTurn_v1`) are banked; unconfirmed turns raise `UnconfirmedTurnBankRefused`.
3. **Census Assistant read-only against Registry.** B5.1 byte-identical guarantee (running the census with or without the assistant produces the same Registry state); no learning-write callables exposed.
4. **Training proposals freeze at commission — MOAC owner-set only.** The assistant may propose slices but cannot set MOAC criteria; MOAC is set by the owner's confirmation at commission time and then FROZEN (see §3).
5. **Content generated · chat surface · anchored · gated.** Every user-facing string is a `ContentRegistryEntry_v1` (fields: `content_registry_ref` + `a5_15_anchor_ref` + `con_6_gate_ref` + `honest_marker`). No ad-hoc strings. Ungated content raises `UngatedContentRefused`.
6. **No learning from dialogue.** L-4/L-5 is the ONLY admission path for any signal from the assistant into the model layer.

**Owner-facing flow:**

- Owner initiates a corpus-assembly session against a newly-readable NAS/Weego channel.
- Assistant proposes: *"Candidate slice for corpus: [channel] path=[X] · duration=[Y]s · prior-labels-from-LID-overlay=[Sw:12, En:3, code-switched:5] · presenters-detected=[N=4 unique]"* — every string is a Content Registry entry, anchored + gated.
- Owner **CONFIRMS** the slice (or rejects). Confirmation writes `CensusAssistantConfirmedTurn_v1` with A5.16 receipt to `services/census_autonomy/state/confirmed_turns/`.
- Repeat until per-language coverage passes the frozen presenter-N threshold (DEFAULT N=20 per DQ-21).

**What is NOT permitted (sealed refusals):**
- Any turn that would identify a presenter (biometric personal data) is refused.
- Any turn banking without receipt raises `UnconfirmedTurnBankRefused`.
- Any turn generating raw ad-hoc content strings raises `UngatedContentRefused`.

**Wall-time posture (UNMEASURED estimate for owner planning · this pod has never run it live):**
- **~30-90 min of owner-in-the-loop dialogue per language** for a first-quality corpus (5 languages × 60 min avg = ~5 h owner time · UNMEASURED · varies with presenter-uniqueness and code-switch density).
- Corpus target size: ~10-30 h of labelled audio per language after speaker-disjoint N=20 rule applies (UNMEASURED).

---

## Step 3 · Commission with frozen criteria

**Sealed boundary callable:** `services/audio_plane_v1/language_cognition_v1.commission_language_cognition_training_run(...)`.

Refuses `pod://*` + `/app/*` prefixed refs (Ruling (b) AKKI-RUNS-IT verbatim: pod NEVER data path).

### 3.1 · Frozen inputs at commission

- **Corpus manifest ref** — from Step 2 confirmed turns (must reference at least one code-switched span per `CleanMonolingualOnlyRefused` refusal · has_code_switched_material must be True).
- **Training base ref** — sealed `LanguageCognitionTrainingBaseRegistration_v1` composing sealed CP-SO-6.9-LID-WAVE `WHISPER_LID_REGISTRATION` or `VOXLINGUA107_REGISTRATION` by identity + `lora_adapter_declaration` + `training_base_posture_hash` + `licence_id_pinned`.
- **Speaker-disjoint split contract** — `SpeakerDisjointSplitContract_v1(presenter_minimum_n=..., train_test_speaker_intersection_empty=True)`.
- **MOAC contract** — `LanguageCognitionMoacContract_v1` (see §5).
- **RMS custody posture** — `RmsCustodyRightsPosture_v1(dp_sgd_applies=..., artefact_ownership_ref=pilot §8.3)`.

### 3.2 · DEFAULTS that apply (unless owner overrides at commission)

Per §6.3 of `OWNER_RETURN_REPORT.md`, all four 5.12 forks stand at DEFAULT meanwhile:

| DQ | Fork | DEFAULT applied | Override mechanism |
|---|---|---|---|
| DQ-21 | Presenter minimum N | **20** | Owner passes `presenter_minimum_n=<other>` at commission; recorded in the frozen `SpeakerDisjointSplitContract_v1` |
| DQ-22 | Per-language accuracy threshold | **≥ 0.90** | Owner passes `per_language_accuracy_min=<other>` at commission; recorded in the frozen `LanguageCognitionMoacContract_v1` |
| DQ-23 | Code-switch span accuracy threshold | **≥ 0.85** | Owner passes `code_switch_span_accuracy_min=<other>` at commission; recorded in the frozen `LanguageCognitionMoacContract_v1` |
| DQ-24 | DP-SGD opt-out | **DP-SGD applies** | Owner passes `dp_sgd_opt_out=True` + reason ref to `STATE/OWNER_DROPS/` at commission; recorded in the frozen `RmsCustodyRightsPosture_v1` |

### 3.3 · What "frozen" means (sealed refusal)

Once `commission_language_cognition_training_run(...)` returns a `TrainingCommissionProposal_v1` with `moac_frozen=True` (via sealed CP-AIP-ASSIST-TRAINING `freeze_training_commission_on_owner_confirm` composed by identity at 5.11.g), any subsequent attempt to edit MOAC criteria raises `SilentMoacThresholdChangeRefused` (from `language_cognition_v1.py`) → refusal at commission boundary. A silently-changed threshold artefact is refused admission at Step 6.

### 3.4 · Compute posture at commission (UNMEASURED estimate)

- **Owner-side wall-time:** ~5-15 min to review the frozen criteria + confirm (varies).
- **Pod-side wall-time:** <1 s (declares the boundary; no compute).

---

## Step 4 · Autonomous execution via Track-4 `training_runs` job

**Sealed anchor:** `services/census_autonomy/track_4_autonomy_wiring_v1.TRACK_4_JOB_KINDS` (Final 3-tuple) includes `training_runs` as a sealed Census Autonomy job kind.

**Ruling (b) AKKI-RUNS-IT verbatim:** *"E1 wires the seam INTO the Census Autonomy Service so Akki runs them autonomously — then STEPS BACK."*

### 4.1 · What happens at execution

1. Census Autonomy engine picks up the commissioned `training_runs` job (queued by Step 3).
2. Engine dispatches to the sealed training host (**never** the pod — `pod://*` + `/app/*` refused at commission per §3.1; `POD_NEVER_DATA_PATH_POSTURE_LANGUAGE_COGNITION` Final marker cites the discipline).
3. Training host runs the LoRA adapter pass over the Doc-20-registered base with the frozen corpus + MOAC criteria.
4. On completion, host writes a `CompletionCertificate_v1` (sealed at CP-AIP-10) with artefact hash + MOAC results.

### 4.2 · Receipt proving it ran (EXIT EVIDENCE)

**Autonomy engine receipt** (mandatory per sealed CP-TRACK-4-AUTONOMY-WIRING · same shape as the pre-DQ-17 contract-level receipt but with `wall_clock_seconds > 0` and real-artefact fields populated):

`phase0/track_4_autonomy_engine_run_receipts/<timestamp>_training_runs_engine_run_receipt.json`

Required fields (verified by sealed `test_track_4_all_jobs_registered_as_autonomy_jobs` invariant):
- `receipt_kind: track_4_autonomy_engine_run_receipt_v1`
- `job_kind: training_runs`
- `census_run_id: cr-<hex>`
- `started_at_utc / finished_at_utc / wall_clock_seconds: <real value>` — **wall_clock_seconds will be >>0** on live run (contrasts with 0.001 contract-only receipt at 2026-09-23T14:48:03Z).
- `engine_live_status: COMPLETE`
- `engine_result_body.completion_certificate_ref: /app/assessment_workspace/phase0/training_artefacts/<timestamp>_<lang>_lora_adapter_completion_certificate.json`
- `engine_result_body.artefact_hash_sha256: <hex>`
- `engine_result_body.moac_results: {per_language_accuracy: {sw: 0.xx, en: 0.xx, ...}, code_switch_span_accuracy: 0.xx, no_speaker_id_probe_result: chance_level_confirmed | REFUSED}`

### 4.3 · Compute posture at execution (UNMEASURED · training host is off-pod)

**Wall-time estimate for the training pass (owner-planning purposes · UNMEASURED · varies with training-host GPU class + corpus size):**

- On the 2× H200 (140 GiB × 2 = 280 GiB) `akki-vm` / `akki-vm-ii` GPU inventory (per `gpu_pipeline_status` in `/api/census/latest`): a LoRA-adapter pass over a 5-language × 20 h/lang corpus with Whisper-encoder or VoxLingua107 base is typically ~1-4 GPU-hours per language after data prep · **UNMEASURED on this pod**; owner should verify with training-host operator.
- Data-prep pipeline (already partially executed for Digicow S3 · see `phase0/census_v3/duplication_v2/20260922T020300Z_DIGICOW_LANGID_AGGREGATE.json`): ~1-3 h for 1500-object sweep on the current dual-host CT2 pipeline.

### 4.4 · What is NOT permitted (sealed refusals at execution)

- `PodAsDataPathRefused` (extends sealed `PodIsNeverDataPathAtTrack4Error` by identity) if the training host attempts to `POST` data back to the pod.
- `MockTrainingRunRefused` (per `COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE`) if the engine tries to short-circuit with a stub receipt (a `wall_clock_seconds < some_epsilon` receipt with no artefact_hash is refused at receipt-shape validation).

---

## Step 5 · MOAC evaluation

**Sealed anchor:** `LanguageCognitionMoacContract_v1` frozen at Step 3.

### 5.1 · Four MOAC criteria (all must pass or the artefact is refused)

1. **Per-language accuracy on speaker-disjoint held-out real material.**
   - Threshold: ≥ 0.90 (DQ-22 DEFAULT).
   - Test: run the LoRA adapter over held-out presenters (never seen at training) · compute per-language accuracy on the 5-tuple `(Kikuyu, Luo, Sheng, Swahili, English)` · every language ≥ threshold or refused.
2. **Code-switch span accuracy.**
   - Threshold: ≥ 0.85 (DQ-23 DEFAULT).
   - Test: for each code-switched utterance, the model's produced span boundaries must be within a ruled tolerance window AND the language label per span must be correct. Boundary tolerance is a fixed rule (currently pinned at ± 0.5 s per Canon 5 §5.3 window rule).
3. **No-speaker-identification probe at chance level.**
   - Sealed carrier: `NoSpeakerIdMoacProbe_v1(chance_level_epsilon=<default_0.05>, held_out_presenter_count=<>=20>)`.
   - Test: train a classifier probe against the LoRA adapter's features to distinguish held-out presenter identity. Probe's accuracy MUST fall within `1/N_presenters ± chance_level_epsilon` (i.e., chance level). Any probe result exceeding chance = biometric leakage = refused.
   - **This is the DAP-31-applied-to-voices criterion** — the voice-is-biometric-personal-data enforcement.
4. **Abstention reported.**
   - The model MUST report its below-confidence rate on the held-out set (windows where confidence < threshold = `unmeasured`, never labelled). Abstention rate is recorded in `moac_results` — not a pass/fail criterion in itself, but must be present for admission.

### 5.2 · Below-confidence rule (sealed at MUST-DO §5)

`WindowAndSpanRule_v1` — deterministic 1-2 s window + hysteresis + `below_confidence_threshold_action=unmeasured` (never labelled). `BelowConfidenceLabelRefused` fires at admission if any label carries `confidence < threshold`.

### 5.3 · Compute posture at MOAC (UNMEASURED estimate)

- MOAC run wall-time: ~5-30 min on the training host (varies with held-out set size · UNMEASURED).
- Owner review of `moac_results` before Step 6 admission: ~5-15 min.

---

## Step 6 · B5.4 admission + receipted overlay-to-measure promotion

**Sealed anchor:** `B5_4_AdmissionReceiptedAct_v1` composes sealed `promote_lid_regime_by_receipted_act` by identity (from CP-SO-6.9-LID-WAVE).

### 6.1 · Admission gate

- Owner reviews the `moac_results` from Step 5.
- If **all four MOAC criteria pass** AND `no_speaker_id_probe_result == chance_level_confirmed`: owner issues **B5.4 admission receipt** (`STATE/OWNER_DROPS/language_cognition_admission_<timestamp>.md` verbatim).
- Admission receipt carries: artefact hash sha256 (from Step 4 completion certificate) · MOAC results snapshot · owner signature block.

### 6.2 · Overlay→measure promotion

The receipted admission triggers `promote_lid_regime_by_receipted_act(receipt_ref=<>, from_regime=OVERLAY, to_regime=MEASURED)`. Sealed refusals apply:

- `RelabellingAtRegimeFlipRefused` — NOTHING is relabelled retrospectively at the flip. Prior overlay labels remain as overlay-annotated data; new labels from the admitted model carry `regime=MEASURED`.
- `NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE` Final marker enforces this structurally.

### 6.3 · What changes after admission

- `/api/census/latest` census_v3_extensions LID-overlay block flips its regime marker for future-tense classifications from `INFERRED` to `MEASURED`.
- Census Autonomy engine's `lid_pass` job kind (sealed at CP-SO-6.9-LID-WAVE) starts consuming the admitted artefact instead of the pre-trained overlay only.
- The DQ-17 `CorpusChannelUnreachableHonestGap_v1` closes (records `remediation_completed_at_utc = <admission_timestamp>`).

### 6.4 · Compute posture at admission (UNMEASURED)

- Wall-time: near-zero for the admission act itself (a receipt write + a regime flag flip in the LID overlay service).
- Owner review time to sign B5.4 receipt: ~15-30 min for careful review of MOAC results (UNMEASURED · varies).

---

## Honest-gap items that remain AFTER DQ-17 unlock

Even after this whole runbook completes, the following remain OPEN and require separate owner action or ledger progression:

1. **DQ-05 · Huawei OBS IAM GetObject grant.** Required to census the na7p4* audit-scope buckets (74 blocked buckets in the current CENSUS-3 access summary). Not on this runbook's path but blocks the na7p4* audio corpus from ever entering language-cognition training if speakers/languages live there. Owner-exclusive.

2. **Akki-OS-Root public exposure.** P0-security honest-gap · pod cannot flip visibility. Independent of DQ-17. Owner acts via GitHub UI → Settings → Danger Zone → Make private.

3. **DP-SGD toolchain provisioning on the training host.** If DQ-24 default (DP-SGD applies) is kept and the training host does not have DP-SGD-capable optimiser stack installed, execution at Step 4 will refuse via a compute-provisioning honest-gap. Owner action: verify with training-host operator that DP-SGD (Opacus or equivalent · Pytorch 2.x compatible) is installed and the training script accepts `--dp-sgd` flag before commission.

4. **§16.2 baseline-tier contents ratification.** Owner working default `gate_policy = 'missed stratum gates release'` fail-closed in force meanwhile. Independent of DQ-17 but touches the same MOAC pathway if the sealed gate policy changes.

5. **Auditor-independence advance (DQ-01).** All audit-close verdicts to date (including Item 5.14) carry the `auditor=builder instance` caveat per Standards v2 §10.5. If the owner wants an independent auditor at the next admission (Step 6), DQ-01 must be advanced separately — this runbook does NOT clear DQ-01.

6. **§6.9 clause-9 items.** None currently outstanding beyond items enumerated above, but any new owner ratifications post-DQ-17-unlock enter via §6.9 clause-9 channels.

7. **The four DQ-21..24 forks themselves.** DEFAULTs stand meanwhile; but if the owner ratifies each verbatim (accept or override) on return, the DEFAULT-tagged pending status clears in `STATE/DESK_QUEUE.md`. This runbook does not do that ratification.

---

## Cross-references

- **Sealed boundary:** `services/audio_plane_v1/language_cognition_v1.py` (Item 5.12 Code Commit-A `7e84cd98`).
- **Corpus seam:** `services/audio_plane_v1/language_cognition_corpus_seam_v1.py` (same commit).
- **Assist primitives composed by identity:** `services/census_autonomy/assist_census_v1.py` (Item 5.11.f Code Commit-A `424e2184`) + `services/census_autonomy/assist_training_v1.py` (Item 5.11.g Code Commit-A `fbb2f1f4`).
- **Track-4 wiring:** `services/census_autonomy/track_4_autonomy_wiring_v1.py` (Item 5.11.e).
- **LID base registrations:** `services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (Item 5.11.a).
- **Objective card:** `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` (card_sha256 `34338079d0340d2a0723aa765e6c611afb927056de05eb7700cf4b8053a4d91b`).
- **Owner drop:** `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md` (verbatim).
- **Ruling (b) verbatim:** `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md`.
- **Owner return report:** `OWNER_RETURN_REPORT.md` §6.1 (DQ-17) + §6.3 (DQ-21..24 defaults) + §11 (AUDIT-CLOSE ADDENDUM).
- **DESK_QUEUE:** `STATE/DESK_QUEUE.md` (DQ-17 · DQ-21..24 · DQ-01 · DQ-05 · DQ-13 rows).

---

**Ledger check:** this runbook implements Item 5.13-companion docs (DQ-17 unlock guidance) and nothing else. Additive-only per SO §3.8. No code delta. No autonomous execution authorised by this file — the sealed refusals + posture markers bind every step above regardless. Owner action required at Step 1, Step 2, Step 3, Step 6. Akki executes Step 4 autonomously per Ruling (b) AKKI-RUNS-IT verbatim once Step 3 completes.

**HALT.** No further autonomous action.
