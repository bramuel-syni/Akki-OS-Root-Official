# CP-SO-6.9-LID-WAVE — comprehensive receipt · Item 5.11.a

**Seal boundary:** 2026-02-23T~12:30Z · **SO §6.9 LID RATIFICATION verbatim 2026-02-23 §1-§9** · **Audio-Plane v1.0 §4.1 N1 + B5.4 + Canon 8 §4 W2** · §1.2 modality-extension composing sealed CP-M6-1-1 `LanguageIDBackend` at `services/audio_plane_v1/language_identifier.py` · **RUN-TO-COMPLETION mandate ACTIVE**.

## §1 — What sealed

**SO §6.9 LID RATIFICATION** structurally landed at the audio-plane boundary. Whisper-LID (MIT) + VoxLingua107 (Apache-2.0) registered as canonical audio-native LID model registration acts (6-field verbatim shape). Overlay-detection record shape bound structurally (marker/label invariant + regime default `pre-admission` + do-not-flow-into-counted-measure). Admission gate DEFAULT threshold ≥ 0.90 tagged `pending`, scored against `google-transcripts/` 12-language labelled corpus. Regime promotion by receipted act (canon 8 §4 W2 · owner signature required). Anti-token HF pull wrapper (SO §6.9 clause 3). TENANT-LABELS-PENDING honest-gap covers English/Sheng/code-switched (12 languages RESOLVED via corpus).

## §2 — Ratchet

| Stage | passed | skipped | failed | delta |
|---|---:|---:|---:|---:|
| Pre-authorship (post-CP-AIP-10) | 6321 | 13 | 0 | — |
| Post-CP-SO-6.9-LID-WAVE RED-first authorship | 6332 | 13 | 0 | +11 canonical measured |
| Ratchet floor **post-seal** | **6332** | — | — | — |

- `baseline_failures.json` sha256 post-bump: `468340729cd16eb9f544453f4d18e33a6069cce79b1ec3aa638975daa20ce314`.
- `passed_floor` advanced 6321 → 6332 in `invariants_enforced_when_baseline_guard_1`.

## §3 — Modules added

**One new module under `backend/services/audio_plane_v1/`:**

- `lid_wave_overlay_and_admission_v1.py` (~325 lines):
  - `LidWaveBoundaryRefused` base + 4 subclasses (`LidLabelBelowConfidenceMustBeUnmeasuredError` · `LidOverlayMustNotFlowIntoCountedMeasureError` · `LidRegimePromotionRequiresOwnerReceiptedActError` · `TokenPresentedInPullError`).
  - `LidModelRegistration_v1` frozen dataclass (6-field verbatim: `model_entry` + `weight_sha256` + `licence_id` + `licence_file_path` + `pull_provenance_ref` + `execution_mode`).
  - `WHISPER_LID_REGISTRATION` (MIT · `whisper-lid-v1-mit`).
  - `VOXLINGUA107_REGISTRATION` (Apache-2.0 · `speechbrain-voxlingua107-apache-2-0`).
  - `OverlayLidDetection_v1` frozen dataclass with `__post_init__` enforcing marker/label + regime invariants.
  - `LidAdmissionGate_v1` frozen dataclass with `ClassVar DEFAULT_THRESHOLD_PENDING = 0.90`.
  - `LidRegimePromotionByReceiptedAct_v1` frozen dataclass.
  - `promote_lid_regime_by_receipted_act` boundary callable.
  - `TenantLabelsPendingHonestGap_v1` frozen dataclass + `TENANT_LABELS_PENDING_HONEST_GAP` for English/Sheng/code-switched.
  - `LID_TENANT_LABELS_RESOLVED_12_LANGUAGES` frozenset (kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas).
  - `HuggingFacePullWrapperAntiToken_v1` with `build_headers` + `scrub_env`.
  - `LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE` Final marker (B5.4).
  - `LID_HF_PULL_WRAPPER_ANTI_TOKEN_POSTURE` Final marker (SO §6.9 clause 3).
  - `LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE` Final marker.

## §4 — Test authorship (RED-first · GREEN post)

- **RED_pre:** 11/11 failed 0.73s (authentic `ImportError` right-reason — module absent).
- **GREEN_post:** 11/11 passed 0.75s.
- Test file: `backend/tests/invariants/test_cp_so_6_9_lid_wave_registration_and_admission_gate.py`.

## §5 — Double-green byte-identity (BASELINE_GUARD=1 PYTHONHASHSEED=0)

- **sweep_A**: 6341 passed / 13 skipped / 0 failed / 520 warnings / 198.68s.
- **sweep_B**: 6341 passed / 13 skipped / 0 failed / 520 warnings / 199.74s.
- **stripped_sha256:** `b71bead1574966208bf999b2f59477324c7f0c8c20381ce98d6ecccc2240650a` IDENTICAL both sweeps (12458 stripped bytes; 12469 raw bytes).

## §6 — Objective card

`STATE/OBJECTIVES/CP_SO_6_9_LID_WAVE_20260223.md` (fully-conforming SO §6.2 · promoted from `queued/` · card_sha256 `16fd5e40c5ac5ac9726ef07e5ee98faa453359f4e1e95ef826f1905f5a380f29` · 6 required sections: OBJECTIVE + MUST DO + MUST NOT + EXIT + STOP + ANCHORS · 11 RED-first EXIT node IDs).

## §7 — Milestone-seal continuity (SO §6.9(5) AMENDED · 3rd application)

- **Code bundle** (this-seal): `continuity_bundles/code_20260923T122933Z_CP_SO_6_9_LID_WAVE.bundle` · 19,235,396 bytes (18.3 MiB) · sha256 `c312d8cfcf611f59e8d3008df7be5cc27569d867931b1837dfe43ffb4def193f` @ `programme/track-a` `d4eae498`.
- **State bundle** (post-Commit-C fixup): PENDING — emitted after State Commit-C fixup lands.

## §8 — Owner SO §6.9 LID RATIFICATION posture (verbatim)

> "Neither offered option is the one to run: fastText LID.176 labels text, not audio, and needs a transcription model that isn't registered; Silero's language classifier carries a licence that must be verified as commercial before it can run (C5.4). Register two audio-native models instead, both under licences that need no review — Whisper language detection (MIT) and SpeechBrain VoxLingua107 (Apache 2.0) — pinning the hash and recording the licence file as the registration act."

**Applied at this seal:** two `LidModelRegistration_v1` frozen dataclasses with `licence_id` Literal['MIT','Apache-2.0']; weight_sha256 marked as `[weight-sha256-pinned-at-track-4-pull]` (weight pulls deferred to Track-4 Census Autonomy Service jobs per Ruling (b) AKKI-RUNS-IT verbatim — pod NEVER training host or data path). Anti-token pull wrapper structurally refuses any bearer-like header; env scrubbed of `HF_TOKEN` / `HUGGINGFACEHUB_API_TOKEN` / `HUGGING_FACE_HUB_TOKEN` before headers built.

## §9 — Rejected options bookkeeping (recorded per owner drop §7 verbatim)

- **fastText LID.176** → `WAITING-ON-TRANSCRIPTS` — parked, NOT registered. Reason: "fastText LID.176 labels text, not audio, and needs a transcription model that isn't registered."
- **Silero language classifier** → `LICENCE-REVIEW-REQUIRED C5.4` — parked, NOT registered. Reason: "Silero's language classifier carries a licence that must be verified as commercial before it can run (C5.4)."

## §10 — Honest-gaps at this boundary

- `TENANT-LABELS-PENDING` honest-gap RETAINED for **English + Sheng + code-switched** (3 languages) per SO §6.9 LID RATIFICATION §5-§6 verbatim. Corresponding `TenantLabelsPendingHonestGap_v1(languages=frozenset({"English","Sheng","code-switched"}))` banked structurally.
- `TENANT-LABELS-PENDING` RESOLVED for **12 languages** (kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas) via `google-transcripts/datasets/<lang>/{audio,transcript}` corpus. Corresponding `LID_TENANT_LABELS_RESOLVED_12_LANGUAGES` frozenset banked.

## §11 — 5-commit seal chain (in flight)

| # | Commit | SHA | Branch | Status |
|---|---|---|---|---|
| 1 | Code Commit-A | `d4eae498984abd7da16b1d36692178f513ad10b5` | `programme/track-a` | ✅ LANDED |
| 2 | /app companion A | `0e90b8c3dcef0bb5b2169cd2d6ce0eb492bf1059` | `main` | ✅ LANDED |
| 3 | State Commit-B | *(this bank)* | `master` | 🟡 PENDING |
| 4 | State Commit-C fixup | *(pending)* | `master` | 🟡 PENDING |
| 5 | /app companion C | *(pending)* | `main` | 🟡 PENDING |
| 6 | State mini-bank | *(pending)* | `master` | 🟡 PENDING |

## §12 — Ledger check

**This seal implements Item 5.11.a of `EXECUTION_ORDER.md` and nothing else.** Additive-only. No sealed carrier edit. RED-first · terminal pytest only · BASELINE_GUARD double-green byte-identical stripped_sha256 · SO §6.9(5) AMENDED continuity bundles. Ruling (b) AKKI-RUNS-IT verbatim honored — E1 wires seam then steps back; pod NEVER training host or data path (weight pulls deferred to Track-4 Census Autonomy Service jobs).
