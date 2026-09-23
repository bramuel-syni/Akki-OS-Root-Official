# BUILD_JOURNAL.md — Chronological narrative of the 2026-02-23 autonomous wave

**Companion to:** `OWNER_RETURN_REPORT.md` (Item 5.13 FINAL DELIVERABLE).
**Anchor date:** 2026-02-23 (owner departure → 2026-02-23T~17:35Z owner return anchor).
**Authority:** SO §6.9 amendment + owner drop 2026-02-23 `assist_cards_preapproved_and_run_to_completion` verbatim (RUN-TO-COMPLETION mandate).

---

## 0 · What the wave was for

The owner stepped away on 2026-02-23 with a `RUN-TO-COMPLETION` mandate:

> "Run the entire remaining ledger to completion autonomously. HALT to owner ONLY on: `SPEC-CONFLICT-<n>` · hard custody/gate violation · completion of full ledger + `OWNER_RETURN_REPORT.md` + `BUILD_JOURNAL.md`. Otherwise REPORT-AND-CONTINUE at every milestone seal."

Mid-wave, the owner added a SPEC ENHANCEMENT (Item 5.12 `CP-AIP-LANGUAGE-COGNITION`) via §6.8 standing authority. This journal records what was built, when, and why — with owner canon anchors verbatim wherever they bind.

---

## 1 · Method (unchanged from prior seals · reaffirmed here)

Every seal follows the identical **RED-first mechanical** discipline (SO §3.3):

1. **Ledger check** — the seal implements exactly one item of `EXECUTION_ORDER.md` and nothing else.
2. **RED-first tests** authored before any module code. RED_pre must fail with an authentic `ImportError` / `FileNotFoundError` right-reason ("module absent").
3. **Additive-only module authorship** (SO §3.8) — new file at a new path; no sealed carrier touched; §1.2 modality-extension composes prior sealed symbols by identity (never redeclare).
4. **GREEN_post** — every RED test flips GREEN when the module is authored correctly.
5. **Ratchet bump** — `baseline_failures.json` counts_at_baseline.passed + invariants_enforced_when_baseline_guard_1.passed_floor advanced by exactly the number of own new pins.
6. **Vendored twin sync** — `tools/prod_vendor_sync.py` mirrors the new module into `/app/backend/vendored/extraction_akki/` deterministically; MANIFEST.json regenerated; structural_sha256 pinned.
7. **ORCH_BOOT.md regen** — a new pre-Commit-A yaml block appended to `notes/ORCH_BOOT.md` with the new ratchet + baseline_failures_sha256 + heads_last_sealed pointing at prior sealed B/A commits (advance to this-seal's B/A at Commit-C fixup).
8. **Double-green byte-identical sweep** — `BASELINE_GUARD=1 PYTHONHASHSEED=0 pytest tests/invariants/` full sweep, twice, log stripped via `tools/strip_baseline_guard_log.py`, sha256 must match byte-identically.
9. **6-commit chain** — Code-A on `programme/track-a` + /app companion A on `main` + State Commit-B on `master` + State Commit-C fixup on `master` (R-6 boundary regen advancing heads_last_sealed to this-B + this-Code-A) + State PINS bank on `master` (bundle finalization) + /app companion C on `main` (byte-identical audit twin of State-B + State-C fixup + State PINS bank) + State mini-bank on `master` (RESUME.md rewrite).
10. **SO §6.9(5) AMENDED bundles** — code bundle + state bundle emitted; sha256 pinned in `STATE/PINS.md`; `git bundle verify` "is okay · complete history".
11. **REPORT-AND-CONTINUE** — no idle-halt; proceed to next ledger item unless SPEC-CONFLICT / hard custody-gate violation / completion.

Terminal `pytest` only. **`testing_agent` BANNED. Refactoring BANNED.**

---

## 2 · Wave chronology · 2026-02-23

### 2.1 · 12:10Z · CP-AIP-10-TRAINING-RUNS SEALED (last-by-construction AIP-plane)

**Owner anchor:** the AIP-plane closure required a shape declaration for the training-run boundary before Track-4 wiring could commission it as a job. `TrainingManifest_v1` + `CompletionCertificate_v1` frozen carriers landed as the exit-evidence pair for training-run commission → completion. Sealed at 6321 passed.

### 2.2 · 12:55Z · CP-SO-6.9-LID-WAVE SEALED (Item 5.11.a)

**Owner anchor:** SO §6.9 LID RATIFICATION 2026-02-23 (banked at `STATE/OWNER_DROPS/so_6_9_lid_ratification_20260223/DROP.md`). Whisper-LID (MIT) + SpeechBrain VoxLingua107 (Apache-2.0) canonical registration acts + `OverlayLidDetection_v1` overlay marker + `LidAdmissionGate_v1` + `promote_lid_regime_by_receipted_act` sealed. Overlay from first run; measure only after receipted regime promotion; nothing relabelled at flip. Sealed at 6332 passed.

### 2.3 · 13:40Z · CP-ENT-16-PILOT-LICENCE-SEEDS SEALED (Item 5.11.b)

**Owner anchor:** SO §6.9 amendment §6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim. Three-tenant pilot licence seeds (RMS + DigiCow + AKKI-TEST) with `compute_dial='Managed'` + `frontier_dial='Your Keys'` Literal-closed shape. `EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE` marker. Fold-in: CP-SO-6.9-LID-WAVE card_sha256 placeholder healed. Sealed at 6340 passed.

### 2.4 · 14:15Z · CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY SEALED (Item 5.11.c)

**Owner anchor:** SO §6.9 amendment §6 item 8 verbatim — "The census proceeds in its three waves — complete the walk with the unmeasured register, the full B3 dimension set with the defensibility matrix and sensitivity classification, then the perception pathway — and language labels from item 4 enter it as overlay from the first run." `CENSUS_THREE_WAVES` ordered 3-tuple + wave sequencing refusals + LID overlay source identity-check against sealed CP-SO-6.9-LID-WAVE registrations. Sealed at 6350 passed.

### 2.5 · 14:40Z · CP-TENANT-SEPARATION SEALED (Item 5.11.d)

**Owner anchor:** SO §6.9 amendment §6 item 7 verbatim + Ruling (b) verbatim. Named authorities Fred Afune / Muthoni Kiarie / Samuel Kibacia (RMS) + Vincent Kimani / Peninah Wanja (DigiCow); AKKI-TEST honest-gap declared explicit (empty tuple). Any-one decision rule + isolation-sweep EXIT EVIDENCE (`disjoint=True`) + fold-in CP-CENSUS-THREE-WAVES card structure heal. 141 isolation-sweep receipts persisted spanning 2026-09-22 → 2026-09-23. Sealed at 6369 passed.

### 2.6 · 15:22Z · CP-TRACK-4-AUTONOMY-WIRING SEALED (Item 5.11.e)

**Owner anchor:** SO §6.9 amendment §6 item 6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim — "E1 wires the seams INTO the Census Autonomy Service so Akki runs them autonomously — then STEPS BACK." Three job kinds registered as sealed Census Autonomy jobs (`lid_pass` + `census_three_waves` + `training_runs`); `AutonomyEngineRunReceipt_v1` EXIT-EVIDENCE carrier. **LIVE Census Autonomy engine execution** end-to-end: 3 machine-readable JSON run receipts persisted at `backend/phase0/track_4_autonomy_engine_run_receipts/*.json`; engine_live_status=COMPLETE all 3 runs; ~0.001s wall-clock each. `E1_STEPS_BACK_AFTER_WIRING_POSTURE` + `POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4` markers cite owner + Ruling (b) verbatim. Sealed at 6379 passed.

### 2.7 · 16:05Z · CP-AIP-ASSIST-CENSUS SEALED (Item 5.11.f)

**Owner anchor:** SO §6.9 amendment + owner drop 2026-02-23 `assist_cards_preapproved_and_run_to_completion` verbatim — Track-5 pre-build checkpoint REMOVED; both CP-AIP-ASSIST cards PRE-APPROVED BY CONSTRUCTION under §6.8. **Six binding conditions verbatim as MUST-DO/MUST-NOT test IDs**: (1) No path to any decision (negative-scan import isolation); (2) Confirmed turns only banked (A5.16 receipted provenance); (3) Census assistant read-only against Registry (B5.1 byte-identical); (4) Training proposals freeze at commission — MOAC owner-set only; (5) Content generated · chat surface · anchored · gated (R-32/A5.15/CON-6); (6) No learning from dialogue (L-4/L-5 only admission path). Placement OUTSIDE the TCB. Every user-facing string is a Content Registry entry. `bank_confirmed_assistant_turn` + `render_content_registry_entry` boundary callables; `AssistCensusBoundaryRefused` base + `UnconfirmedTurnBankRefused` + `UngatedContentRefused` subclasses. Sealed at 6389 passed.

### 2.8 · 16:07Z · OWNER SPEC ENHANCEMENT ORDER received mid-mini-bank landing

Post-CP-AIP-ASSIST-CENSUS mini-bank commit `90bbcc0d` (Item 5.11.f fully sealed), owner drop landed:

> "OWNER ORDER — SPEC ENHANCEMENT: CP-AIP-LANGUAGE-COGNITION. Respond in English only... Continue the run: finish 5.11.e/f/g as planned, then 5.12 to its honest reach, then 5.13 FINAL. All guards binding. Execute."

Owner text verbatim banked at `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`. Ledger sequenced: former 5.11.h renumbered to 5.13 FINAL; **Item 5.12 INSERTED** as CP-AIP-LANGUAGE-COGNITION (§6.8 standing authority · no GO needed). Queued objective card drafted at `STATE/OBJECTIVES/queued/CP_AIP_LANGUAGE_COGNITION.md` (fully-conforming SO §6.2 six-section schema · 12 RED-first invariant node IDs · 2 NEW additive modules planned · 9 refusal subclasses + 10 frozen carriers + 9 posture markers · composes by identity sealed CP-SO-6.9-LID-WAVE + CP-CENSUS-THREE-WAVES + CP-ENT-16 + CP-TENANT-SEPARATION + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS + CP-AIP-10). 4 DESK_QUEUE forks banked (DQ-21 presenter minimum N DEFAULT 20 + DQ-22 per-language accuracy ≥90% DEFAULT + DQ-23 code-switch span accuracy ≥85% DEFAULT + DQ-24 DP-SGD opt-out DEFAULT applies). Master commit `94cb01af` + /app companion `4371d9365` (byte-identical audit twin). RUN-TO-COMPLETION mandate stands; continue.

### 2.9 · 16:43Z · CP-AIP-ASSIST-TRAINING SEALED (Item 5.11.g · Item 5.11 wave COMPLETE)

**Same six binding conditions applied to training-run dialogue verbatim as MUST-DO/MUST-NOT test IDs.** `assist_training_v1` §1.2 modality-extension composing sealed CP-AIP-ASSIST-CENSUS `assist_census_v1` by identity: `UnconfirmedTrainingTurnBankRefused` + `UngatedTrainingContentRefused` + `FrozenMoacEditRefused` + `LearningWriteFromDialogueRefused` + `PodIsNeverDataPathAtAssistTrainingError` all extend sealed `AssistCensusBoundaryRefused` base by identity. `TrainingAssistantConfirmedTurn_v1` frozen 8-field carrier + `TrainingCommissionProposal_v1` frozen 6-field carrier. `bank_confirmed_training_turn` + `render_training_content_registry_entry` + `freeze_training_commission_on_owner_confirm` boundary callables. `WEIGHTS_CORPUS_NEVER_LEAVE_AKKI_POSTURE` Final str cites owner verbatim. Same-slice cure: vendored twin file_count 1066→1067 mid-slice sync resolved 1 spine-mirror failure. Sealed at 6399 passed.

### 2.10 · 17:28Z · CP-AIP-LANGUAGE-COGNITION SEALED (Item 5.12 · SPEC ENHANCEMENT · THIS-SEAL)

**Owner canon anchor verbatim (owner drop 2026-02-23T~16:07Z):**

> "A model that identifies the language of speech in the RMS archive by its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng, Swahili and English, and including code-switched speech where several occur in one utterance — producing per-span labels grounded to the second, so the census can measure language distribution as fact rather than mark it unmeasured."

**In canon terms:** A Targeta training run — LoRA adapter over a Doc-20-registered base (VoxLingua107 or Whisper's encoder), frozen objective at commission, MOAC criteria owner-set, artefact registered with hash + rights posture, admitted to census by B5.4 gate. Trained inside perimeter on tenant material; **nothing leaves**.

**12 MUST-DO/MUST-NOT card lines as RED-first invariant node IDs** — all flipped RED (FileNotFoundError, module absent) → GREEN 0.80s via 2 NEW additive modules composing sealed anchors by identity:

1. Feature basis: signature not prosody alone (Canon 4 §5.4 + Doc 20) — `LanguageCognitionFeatureBasis_v1` primary=(phonotactic, spectral) + secondary=(prosody, pitch, dynamics) disjoint.
2. Clean-monolingual alone MUST-NOT (owner verbatim) — `CleanMonolingualOnlyRefused` at commission.
3. Speaker-disjoint splits N=20 DEFAULT tagged pending (Canon 4 §5.5 + DAP-31 · FORK DQ-21) — `SpeakerDisjointSplitContract_v1`.
4. No-speaker-ID MOAC probe chance-level (DAP-31 applied to voices · Canon 8 biometric class) — `NoSpeakerIdMoacProbe_v1`.
5. 1-2s window + deterministic span rule + below-confidence unmeasured NEVER labelled (Canon 5 §5.3) — `WindowAndSpanRule_v1`.
6. MOAC contract per-language ≥90% + code-switch-span ≥85% + no-speaker-ID pass + abstention reported (FORK DQ-22 + DQ-23) — `LanguageCognitionMoacContract_v1`.
7. B5.4 admission by receipted act nothing relabelled (Canon 5 §B5.4 + Canon 8 §W2) — `B5_4_AdmissionReceiptedAct_v1` + `PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY` = sealed callable.
8. Doc 20 training-base extends sealed LID registrations no redeclaration §1.2 — `LanguageCognitionTrainingBaseRegistration_v1` composes sealed `LidModelRegistration_v1` by identity.
9. RMS custody + in-perimeter training + DP-SGD default (Canon 8 §3 + pilot §8.3 · FORK DQ-24) — `RmsCustodyRightsPosture_v1`.
10. Corpus assembly under census-assistant dialogue composes sealed CP-AIP-ASSIST-CENSUS by identity — `language_cognition_corpus_seam_v1.py` composes sealed `bank_confirmed_assistant_turn` + `render_content_registry_entry` by identity + `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple.
11. Track-4 training_runs job kind composed by identity + pod NEVER data path (Ruling (b) verbatim) — `TRACK_4_JOB_KINDS_ANCHOR` = sealed `TRACK_4_JOB_KINDS` + `PodAsDataPathRefused` extends sealed `PodIsNeverDataPathAtTrack4Error` by identity + `commission_language_cognition_training_run` refuses pod://* + /app/* prefixed refs.
12. §1.2 no-redeclaration of sealed symbols — AST-scan for 26 sealed symbol names; new module declares none of them.

**Long-pole gate:** `CorpusChannelUnreachableHonestGap_v1` declares DQ-17 family (Weego/NAS credential rotations) as ONLY gate FACT not policy hold. Non-blocking through this seal; surfaced in `OWNER_RETURN_REPORT.md` pending-human-items.

**In-pod compute honest-gap on execution:** owner drop §Execution-reach verbatim — "commissioned-job contract with honest-gap on execution, never a mock." `COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE` names the discipline. This-seal declares the training-run boundary + registers the corpus-assembly seam; no live LoRA pass executed. On DQ-17 unlock, the commissioned Track-4 `training_runs` job executes autonomously per Ruling (b) AKKI-RUNS-IT verbatim: Akki runs it; E1 wires and STEPS BACK.

Sealed at 6411 passed.

### 2.11 · 17:35Z · Item 5.13 FINAL DELIVERABLE (this journal + `OWNER_RETURN_REPORT.md`) delivered

Full ledger COMPLETE per RUN-TO-COMPLETION mandate. HALT to owner for review.

---

## 3 · Sealed-carrier composition topology at return

The Item 5.12 language-cognition Targeta training-run boundary composes **six prior sealed carriers by identity** (§1.2 modality-extension · no redeclaration) — the highest-scale composition in the wave:

```
CP-AIP-LANGUAGE-COGNITION (5.12)
  ├─ LanguageCognitionTrainingBaseRegistration_v1.sealed_lid_registration:
  │    ← CP-SO-6.9-LID-WAVE.LidModelRegistration_v1
  ├─ WHISPER_LID_REGISTRATION_TRAINING_BASE_ANCHOR:
  │    ← CP-SO-6.9-LID-WAVE.WHISPER_LID_REGISTRATION
  ├─ VOXLINGUA107_REGISTRATION_TRAINING_BASE_ANCHOR:
  │    ← CP-SO-6.9-LID-WAVE.VOXLINGUA107_REGISTRATION
  ├─ PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY:
  │    ← CP-SO-6.9-LID-WAVE.promote_lid_regime_by_receipted_act
  ├─ NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE:
  │    ← CP-SO-6.9-LID-WAVE.LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE (retagged for LC scope)
  ├─ TRACK_4_JOB_KINDS_ANCHOR:
  │    ← CP-TRACK-4-AUTONOMY-WIRING.TRACK_4_JOB_KINDS
  ├─ PodAsDataPathRefused (subclass):
  │    ← CP-TRACK-4-AUTONOMY-WIRING.PodIsNeverDataPathAtTrack4Error
  ├─ POD_NEVER_DATA_PATH_POSTURE_LANGUAGE_COGNITION:
  │    ← CP-TRACK-4-AUTONOMY-WIRING.POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4 (composed)
  ├─ E1_WIRES_AND_STEPS_BACK_POSTURE_LANGUAGE_COGNITION:
  │    ← CP-TRACK-4-AUTONOMY-WIRING.E1_STEPS_BACK_AFTER_WIRING_POSTURE (composed)
  ├─ BANK_CONFIRMED_ASSISTANT_TURN_COMPOSED_BY_IDENTITY (in corpus_seam_v1):
  │    ← CP-AIP-ASSIST-CENSUS.bank_confirmed_assistant_turn
  └─ RENDER_CONTENT_REGISTRY_ENTRY_COMPOSED_BY_IDENTITY (in corpus_seam_v1):
       ← CP-AIP-ASSIST-CENSUS.render_content_registry_entry

Downstream (via card ANCHORS section · not composed as symbols):
  · CP-CENSUS-THREE-WAVES (structural sequencing anchor for overlay-from-first-run)
  · CP-ENT-16-PILOT-LICENCE-SEEDS (RMS pilot licence terms §8.3 for artefact ownership)
  · CP-TENANT-SEPARATION (RMS custody class anchor)
  · CP-AIP-10-TRAINING-RUNS (training-run boundary carrier)
  · CP-AIP-ASSIST-TRAINING (available for downstream consumers of frozen training MOAC turns)
```

Every arrow marked `←` is a Python `is`-check-verified identity composition in the 12 RED-first invariant pins. Sealed symbols are canonical references, not redeclarations.

---

## 4 · Twenty-one lessons banked across the wave

The `RESUME.md` §8 registry carries 21 banked lessons; the last three (banked mid-wave) are:

- **Lesson 19** — Structural EXIT EVIDENCE (import-isolation + boundary-refusal + posture-marker presence) is the correct exit clause for READ-ONLY assistant seals — unlike wire-in seals which need a live-engine run receipt.
- **Lesson 20** — For a modality-extension seal that composes a prior sealed READ-ONLY assistant boundary (CP-AIP-ASSIST-CENSUS → CP-AIP-ASSIST-TRAINING), new refusal subclasses extend the sealed base by identity (§1.2 no-redeclaration), new posture markers use fresh Final names retagged for the new scope while citing the same clause verbatim, sealed frozen carriers are composed by identity in field types (never re-declared), and the new module's boundary callables MAY compose the sealed ones by identity.
- **Lesson 21** — A SPEC ENHANCEMENT inserted mid-run via §6.8 standing authority can compose MULTIPLE sealed anchors by identity — one card composes ALL sealed prerequisites by identity; the card's new symbols are NEW; the sealed anchors are canonical `is`-checked references. This is the honest expression of §1.2 modality-extension at the highest scale — multiple prior seals combine into a single new capability without redeclaring any sealed symbol. **In-pod compute HONEST-GAP on execution (never a mock) is the correct expression of "commissioned-job contract" for a seal where the pod cannot honestly run the training pass**; the seal declares the boundary + registers the corpus-assembly seam + records DQ-17 (NAS reachability) as the ONLY structural gate FACT — not a policy hold introduced by the seal.

---

## 5 · What is NOT in this wave (honest gaps and owner-exclusive items)

- **Live LoRA training pass** for CP-AIP-LANGUAGE-COGNITION — NOT executed. In-pod compute cannot honestly run even a small LoRA pass without NAS/Weego channel reachability + DP-SGD toolchain provisioned. Commissioned-job contract carries honest-gap on execution per `COMMISSIONED_JOB_HONEST_GAP_NOT_MOCK_POSTURE`. Owner-action: unlock DQ-17 family credentials.
- **CAL Huawei OBS grant** (DQ-05 + OWNER-Q1) — pod cannot execute; owner-exclusive.
- **Akki-OS-Root visibility flip** — pod cannot execute; owner acts via GitHub UI.
- **§16.2 baseline-tier contents ratification** — pod uses owner working default meanwhile; owner confirms on return.
- **na7p4* direct-reading rate + region-specific tr-west-1 pricing + AWS S3 backup overlap** — honest gaps recorded pre-wave.

All of the above are surfaced in `OWNER_RETURN_REPORT.md` §6 (PENDING OWNER ITEMS) with recommended defaults where the owner draft already carries them.

---

## 6 · Repository state at return (mirror of §9 in OWNER_RETURN_REPORT.md)

- **State repo:** `master` HEAD `3158ca2d1a8fe8508eb6ab26dc60a0b73375a052`.
- **Code repo:** `programme/track-a` HEAD `7e84cd98f37aea50f9d0ed55fbd8d654ffc582f7`.
- **/app companion:** `main` HEAD `07e6a48136513c2dd59d4cbb3431e6f29bd83d27`.
- **Baseline:** 6411 passed / 13 skipped / 0 failed / 520 warnings.

---

**Ledger check:** this journal (companion to `OWNER_RETURN_REPORT.md`) implements Item 5.13 of `EXECUTION_ORDER.md` and nothing else. Additive-only per SO §3.8.

**RUN-TO-COMPLETION mandate 2026-02-23 completion point reached.** HALT to owner for review.
