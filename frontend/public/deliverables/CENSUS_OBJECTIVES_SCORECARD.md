# CENSUS-OBJECTIVES-SCORECARD · 2026-02-24T~03:50Z

**Owner directive verbatim 2026-02-24:** *"You are not reporting against the census objectives - also, there is no maori or arabic in the data you have so wrong findings."* → this document responds to Issue 1 (report against defined census objectives).

**Method:** each objective is pulled verbatim from the ratified card in `STATE/OBJECTIVES/` or the canon anchor in `canon/unpacked/`. If an objective is not defined in a card or a canon, this document says so — objectives are not invented. Status is one of `MET` / `PARTIAL` / `NOT-MET` / `BLOCKED`.

Companion documents: `OUTCOMES_TO_DATE.md` (team narrative · corrected) and, at `phase0/census_v3/duplication_v2/lid_reaggregate_20260224/`, the re-aggregated LID overlay after the new abstention + estate-filter (proof that the fix routes mi/ar → `unmeasured`).

**Ratchet floor at delivery:** 6411 → **6430** (+19 canonical measured) at BASELINE_GUARD=1 sweep completed 2026-02-24T~03:57Z from correct `backend/` cwd (per `backend/pytest.ini`) · **6430 passed / 13 skipped / 0 failed / 520 warnings in 187.11s** · same-slice cure `tools/prod_vendor_sync.py` executed 2026-02-24T~03:54Z (`file_count 1070` · `files_written 1` new module · `structural_sha256 e636bbbb…`). The additive fix module + 9 RED-first invariant pins land here.

---

## Objective A · Measure the language distribution of the RMS audio archive as FACT

**Source (verbatim):** `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` §OBJECTIVE line 16 · owner drop 2026-02-23T~16:07Z: *"A model that identifies the language of speech in the RMS archive by its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng, Swahili and English, and including code-switched speech where several occur in one utterance — producing per-span labels grounded to the second, so the census can measure language distribution as fact rather than mark it unmeasured."*

**Status:** `PARTIAL · overlay-visible · not-yet-fact`.

**Measured evidence:**
- INFERRED overlay live: sealed CP-SO-6.9-LID-WAVE registers Whisper-LID (MIT) + VoxLingua107 (Apache-2.0) as registration acts (`services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py`).
- Overlay records structurally binding: `OverlayLidDetection_v1.__post_init__` enforces `marker == "INFERRED" iff label is not None`. Regime pinned `"pre-admission"` at construction.
- Admission gate contract: `LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING = 0.90` scored against `google-transcripts/datasets/{kik,ebu,swa,luo,kln,guz,mer,bxk,kam,mrg,lwg,mas}/{audio,transcript}` — 12-language labelled corpus (SO §6.9 LID RATIFICATION amendment).
- **Overlay counts NEVER promoted to counted measure** (structural refusal `LidOverlayMustNotFlowIntoCountedMeasureError`; posture `LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE`).

**Honest gap (owner correction 2026-02-24 · P0 fidelity):** the 2026-09-22 DIGICOW_LANGID_AGGREGATE receipt reported raw language codes including `mi` (Maori · n=2), `ar` (Arabic · n=17), `la`, `nn`, `ro`, `ko`, `de`, `es`, `pt`, `cy`, `gu`, `el`, `nl` — **all false positives**, none of which are in the RMS estate. RCA + additive fix delivered under Objective K below; the false-positive labels were never fact, but the receipt-reader could be misled.

**Blocker to promotion to FACT:** CP-AIP-LANGUAGE-COGNITION training + MOAC ≥90% + B5.4 receipted-act promotion (per Canon 8 §4 W2). Current pod compute: **cannot execute the training** — see Objective L (functional-training order).

---

## Objective B · Complete the three census waves in verbatim order

**Source (verbatim):** `STATE/OBJECTIVES/CP_CENSUS_THREE_WAVES_20260223.md` §OBJECTIVE line 14 · owner drop verbatim: *"The census proceeds in its three waves — complete the walk with the unmeasured register, the full B3 dimension set with the defensibility matrix and sensitivity classification, then the perception pathway — and language labels from item 4 enter it as overlay from the first run."*

**Ordered 3-tuple:** `("unmeasured_register", "b3_dimension_set", "perception_pathway")` — enforced structurally by `CENSUS_THREE_WAVES` Final tuple + `test_census_three_waves_v1_three_waves_ordered_tuple_verbatim`.

**Status:**
- Wave 1 · unmeasured_register: `MET · structural` — carrier `UnmeasuredRegisterWave_v1` with `dimensions_measured: False` per B5.4 shown-not-counted.
- Wave 2 · b3_dimension_set: `PARTIAL` — see Objective D.
- Wave 3 · perception_pathway with LID overlay from first run: `PARTIAL` — LID overlay is live (Objective A) but currently emits false positives (fixed under Objective K).

**Measured evidence:** sealed CP-CENSUS-THREE-WAVES module registers as Census Autonomy job (Ruling (b) AKKI-RUNS-IT verbatim): `register_census_three_waves_as_census_autonomy_job`. Pod refused as data path (`pod://*` and `/app/*` refused at seat).

---

## Objective C · Map station → language coverage (RMS station-axis)

**Source (verbatim):** ratified per `services/rms_station_language_axis.py` (station-prior + owner HONESTY RULE) · CP-CENSUS-RMS-STATION-LANGUAGE-AXIS seal (Item 1 · 2026-02-23T~04:00Z DONE).

**Status:** `MET · structural`.

**Measured evidence:**
- Every station-axis feed carries `attribution_for_asset` HONESTY RULE. Owner-set 16 named channels (per NFS/CIFS receipt · 2026-09-24 T3:38Z sweep receipt `20260924T033806Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json` §E verdict `FULL_16_CHANNELS_PRESENT_ALL_SAMPLED_READABLE`).
- 16-channel expected list (verbatim from `EXPECTED` tuple in the sweep script): Citizen TV, Inooro TV, Radio Citizen, Inooro FM, Ramogi FM, Egesa FM, Musyi FM, Hot 96 FM, Chamgei FM, Mulembe FM, Sulwe FM, Vuuka FM, Bahari FM, Muuga FM, Wimwaro FM, Ramogi TV.

**Honest gap:** language-per-station-per-hours breakdown as MEASURED FACT is downstream of Objective A promotion — currently INFERRED overlay only.

---

## Objective D · Full B3 dimension set with defensibility matrix + sensitivity classification

**Source (verbatim):** `STATE/OBJECTIVES/CP_CENSUS_THREE_WAVES_20260223.md` §OBJECTIVE line 14: *"the full B3 dimension set with the defensibility matrix and sensitivity classification."*

**Status:** `NOT-DEFINED-IN-CARD-AS-CANONICAL-MODULE · PARTIAL`.

The CP-CENSUS-THREE-WAVES card names the wave as `b3_dimension_set` but does not name a canonical module that carries the full B3 attribute set. Canon 3 Governance Engines and Canon 4 Operating Engines both reference B3 dimensions structurally.

**Measured evidence available:**
- Sensitivity classification: sealed `pilot_licence_seeds_v1.py` (CP-ENT-16) + tenant-separation invariants (CP-TENANT-SEPARATION) enforce role-based access at boundary; 5 named approving authorities across 2 tenants (RMS: Fred Afune / Muthoni Kiarie / Samuel Kibacia; DigiCow: Vincent Kimani / Peninah Wanja); overlap_count = 0.
- Defensibility: partial via B5.4 shown-not-counted line at every overlay carrier.

**Honest gap:** the B3 dimension set (as an enumerated tuple with every dimension named) is not surfaced in any current `services/` module or ratified card. **Owner ratification needed** on whether the current partial coverage satisfies Wave 2 or whether a canonical `B3DimensionSet_v1` carrier is required.

---

## Objective E · Identify duplicate/redundant corpus (dedup / instance condition map)

**Source (verbatim):** `STATE/OBJECTIVES/CP_AIP_2_DEDUP_CONDITION_MAP.md` §OBJECTIVE · AIP v1.0 §4.5 + §4.6 (b): *"dedup as augmentation · one canonical extraction stored · variant set → robustness stratum at zero acquisition cost."*

**Status:** `MET · structural`.

**Measured evidence:**
- Sealed CP-AIP-2 module lands `InstanceConditionMap` composition per §4.5.
- Sealed CP-M6-2-1 `InstanceConditionMap` composed structurally; §4.6 (b) acceptance criterion enforced by test `a deduplicated item without its instance condition map fails the ingestion invariant test`.
- Dedup receipt at `phase0/census_v3/duplication_v2/` (walked 2026-09-22).

**Honest gap:** dedup rates by tenant/channel not surfaced as a fact-table yet; TB reclaimed via dedup is inferred not measured.

---

## Objective F · Classify data by sensitivity + defensibility (B3 dimensions applied per artefact)

**Source:** implicit in Objective D + `character_register_write_boundary_v1.py` write-boundary leakage-refusal (Canon 8 biometric class posture) + CP-TENANT-SEPARATION.

**Status:** `PARTIAL · sensitivity structural / defensibility partial`.

**Measured evidence:** character-register write-boundary refuses leakage paths (CP-AIP-3 + CP-M6-3-3 sealed). Voice biometric class refusal live (DAP-31 + CP-AIP-LANGUAGE-COGNITION `NoSpeakerIdMoacProbe_v1`).

**Honest gap:** per-artefact classifier that emits a sensitivity+defensibility tuple as fact is not yet a boundary callable; the classifications live implicitly across multiple write-boundary refusals.

---

## Objective G · Determine readability/accessibility per estate

**Source:** implicit in the estate-read-capability sweep pattern; ratified per `tools/full_estate_read_capability_sweep_20260921_freshcreds.py`.

**Status:** `MET · measured 2026-09-24T03:38Z`.

**Measured evidence (fresh receipt banked today · `phase0/connectivity_receipts/20260924T033806Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json`):**
- **JUMP** (159.138.173.250 · SSH 22): `OK`, opened in 1.885 s.
- **MySQL clusters** (via JUMP tunnel):
  - VIUSASA @ 203.123.86.10 · `AUTH-OK` · 10 user_dbs readable (viupay, viusasa_artists, viusasa_miniapps_prod, etc.).
  - USSD @ 110.238.76.159 · `AUTH-OK` · 17 user_dbs readable (artists_app, citizen_digital, db_jipange, db_skiza, etc.).
  - MICROSERVICES @ 159.138.164.93 · `AUTH-OK` · 3 user_dbs readable (kra_reports, viupay, viutickets).
  - MICROSERVICES @ 159.138.164.124 · `AUTH-OK` · 1 user_db (db_visitors).
  - MICROSERVICES @ 110.238.75.83 · `AUTH-OK` · 1 user_db (db_visitors).
  - MICROSERVICES @ 203.123.83.144 · `AUTH-OK` · 3 user_dbs (citizen-pulse, correspondents, saa).
  - **NAS - ACESS @ 159.138.173.58 · `AUTH-OK` · 2 user_dbs (`news_vault`, `razuna`) — Razuna + Newsvault UNBLOCKED** per owner's DQ-17 reclassification 2026-02-23T~19:xxZ.
  - MICROSERVICES @ `HOST` (placeholder) · `NO-CREDS-IN-SHEET · honest gap`.
  - MICROSERVICES @ 159.138.162.146 · `NO-CREDS-IN-SHEET · honest gap`.
- **NFS/CIFS** at `/mnt/nfs-share`: `FULL_16_CHANNELS_PRESENT_ALL_SAMPLED_READABLE` (kernel-mediated CIFS mount via cached `bramuel` session).
- **Huawei OBS** (carry-forward from 2026-09-22T01:36Z census-3 sweep): 106 buckets · **950,791 objects · 161,760,666,530,569 bytes ≈ 161.76 TB** listed; 32 of 106 confirmed getobject-success; 33 of 106 carry more pages beyond cap.

**Honest gap:** viusasa transcoded-content (MUSIC / MUSIC-AUDIO) on **CAL Huawei account** is **NOT** in this sweep — OWNER-Q1 pending (owner has not yet provided CAL Huawei account credentials). Also parked by owner explicit ruling: na7p4* Huawei OBS IAM `GetObject` grant (DQ-05) — owner said "skip this for now."

---

## Objective H · Assemble the labelled training corpus

**Source (verbatim):** `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` MUST-DO §10: *"Corpus assembly runs UNDER THE CENSUS ASSISTANT'S DIALOGUE — this is Item 5.11.f (CP-AIP-ASSIST-CENSUS)'s first real objective. The assistant PROPOSES corpus slices; the owner/tenant CONFIRMS; gates DECIDE."*

**Status:** `BLOCKED · honest gap surfaced by measured probe · owner ruling requested`.

**Measured evidence:**
- Sealed corpus seam `services/audio_plane_v1/language_cognition_corpus_seam_v1.py` binds `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple: `("Kikuyu", "Luo", "Sheng", "Swahili", "English")`.
- Sealed Census-Assistant primitives (CP-AIP-ASSIST-CENSUS): `bank_confirmed_assistant_turn` + `render_content_registry_entry` compose corpus-slice propose/confirm/gate/decide workflow.
- Owner 2026-02-24 training-order verbatim: *"this owner order IS the confirmed turn"* → banked as A5.16-receipted confirmed assistant turn per B5 discipline (recorded in DECISIONS.md wave-card 2026-02-24).

**Blockers (facts, not policy holds — per owner DQ-17 reclassification):**
1. **12-language `google-transcripts/datasets` labelled corpus is NOT in the pod perimeter.** Per Ruling (b) AKKI-RUNS-IT verbatim, the labelled corpus MUST NEVER enter the pod as data path (sealed refusal on `pod://*` + `/app/*`). Owner action needed: point to a reachable corpus location + delivery mechanism that Akki (not the pod) can consume. **Fork filed: `FORK-COMPUTE-CORPUS-OUT-OF-PERIMETER`.**
2. `CorpusChannelUnreachableHonestGap_v1` structural marker present at seam; owner has RE-CLASSIFIED DQ-17 (2026-02-23) as no longer a policy hold — every NAS/Razuna/Newsvault channel connects (see Objective G). So the DQ-17 gate is CLEARED; the remaining gap is the 12-language corpus location + delivery mechanism, which is a distinct fact.

---

## Objective I · In-perimeter training + custody-safe character register + DP-SGD default

**Source (verbatim):** `STATE/OBJECTIVES/CP_AIP_LANGUAGE_COGNITION_20260223.md` MUST-DO §9: *"RMS custody + in-perimeter training + DP-SGD default."*

**Status:** `MET · structural / BLOCKED · execution`.

**Measured evidence (structural):**
- Sealed `commission_language_cognition_training_run` at `services/audio_plane_v1/language_cognition_v1.py::401` structurally refuses `pod://*` and `/app/*` prefixed refs → pod cannot host training material or compute.
- Character register (CP-AIP-3) with 4-leakage-path custody invariant harness enforces no voiceprint leaks from artefact.
- No-speaker-ID MOAC probe (`NoSpeakerIdMoacProbe_v1`) refuses artefact if speaker-identification exceeds chance on held-out presenters.
- `RmsCustodyRightsPosture_v1` binds Canon 8 §3 + pilot §8.3 custody-rights posture.

**BLOCKED · execution (measured, this pod, this session):**
- No GPU on pod (nvidia-smi absent).
- No `torch` / `transformers` / `peft` / `speechbrain` installed on pod.
- No `opacus` (DP-SGD library) on pod.
- Every `aisca-gpu-01` commissioning record at `phase0/commissioning_records/` carries `vm_host` of `127.0.0.1` (pytest drill fixture) or `203.0.113.42`/`203.0.113.5` (TEST-NET-3 documentation range · **NOT** routable public IPs). Owner's WS-BUILD-CONNECT-GPU ruling 2026-08-14 verbatim: *"I will key the VM credentials into the app myself: Connect tile → GPU"* — real GPU VM credentials have never been keyed in.
- **Fork filed: `FORK-COMPUTE-GPU-CREDS-PENDING-OWNER-KEY-IN`.**
- **Fork filed: `FORK-DP-SGD-TOOLING-NOT-INSTALLED · owner one-word ruling requested (opt-out for internal run vs stall pending toolchain).`**

---

## Objective J · Tenant separation + custody boundary structurally enforced

**Source (verbatim):** `STATE/OBJECTIVES/CP_TENANT_SEPARATION_20260223.md` §OBJECTIVE.

**Status:** `MET · sealed 2026-02-23`.

**Measured evidence:** `test_cp_tenant_separation.py` GREEN (per 6411 baseline sweep at Item 5.13). RMS + DigiCow authority sets disjoint (`overlap_count = 0`). AKKI-TEST empty-tuple honest-gap banked explicitly.

---

## Objective K · LID overlay abstention + estate-language allow-list (owner correction 2026-02-24)

**Source (verbatim):** owner correction 2026-02-24 *"there is no maori or arabic in the data you have so wrong findings … VERIFY the abstention rule is live … CONSTRAIN honestly: consider an estate-language allow-list prior."*

**Status:** `MET · additive-fix landed 2026-02-24T~03:47Z · RED→GREEN pin proof · re-aggregated receipt banked`.

**Measured evidence:**

- **New additive module:** `backend/services/audio_plane_v1/lid_overlay_abstention_and_estate_filter_v1.py` (~180 lines) composing sealed `OverlayLidDetection_v1` + `LidAdmissionGate_v1` + `LID_TENANT_LABELS_RESOLVED_12_LANGUAGES` by identity (§1.2 no-redeclaration).
  - `ESTATE_LANGUAGE_ALLOWLIST_v1: Final[frozenset[str]]` — verbatim 14-tuple `{kik, ebu, swa, luo, kln, guz, mer, bxk, kam, mrg, lwg, mas, en, sheng}`.
  - `LID_ABSTENTION_DEFAULT_THRESHOLD` binds sealed `LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING = 0.90`.
  - `LID_ABSTENTION_REASONS: Final[Tuple[str, str, str]]` = `("ok", "below_confidence", "out_of_estate_suspected_false_positive")`.
  - `LidOverlayFilteredSample_v1` frozen 4-field carrier `(overlay, raw_label, raw_confidence, abstention_reason)` — anti-loss discipline preserves raw model output alongside filtered result.
  - `apply_abstention_and_estate_filter(...)` boundary callable — single-writer path for LID overlay writes.
- **Nine RED-first invariant pins** at `backend/tests/invariants/test_lid_overlay_abstention_and_estate_filter.py`:
  1. `test_estate_language_allowlist_is_14_tuple_verbatim`
  2. `test_below_confidence_returns_unmeasured_abstention_below_confidence`
  3. `test_out_of_estate_label_returns_unmeasured_suspected_false_positive`
  4. `test_in_estate_high_confidence_returns_inferred_with_label`
  5. `test_raw_output_preserved_alongside_filtered_result_anti_loss`
  6. `test_admission_gate_default_threshold_0_90_used_by_filter`
  7. `test_abstention_reason_enum_is_three_tuple_verbatim`
  8. `test_no_redeclaration_of_sealed_symbols_1_2`
  9. `test_regression_20260922_mi_ar_false_positives_classified_out_of_estate` (regression proof for every out-of-estate code observed in the raw sweep: `mi, ar, la, nn, ro, ko, de, es, pt, cy, gu, el, nl`).
- **RED-first proof (2026-02-24T~03:45Z):** authentic `ImportError: cannot import name 'lid_overlay_abstention_and_estate_filter_v1' …` when only the test file existed (module absent · right-reason failure).
- **GREEN-post (2026-02-24T~03:47Z):** 9/9 passed in 0.67 s.
- **Re-aggregation receipt (2026-02-24T~03:48Z):** `phase0/census_v3/duplication_v2/lid_reaggregate_20260224/20260924T034805Z_LID_REAGGREGATE_ABSTENTION_ESTATE_FILTER.json` · sha256 `4fb7d9e0b29eb9e15e988d3610bf14106892e54d14c7056ba049c35f3aed977a` · applied the new filter to the raw 2026-09-22 DIGICOW aggregate. Outcome: `mi` (n=2, raw_avg_conf=0.000) → `unmeasured` (`below_confidence`); `ar` (n=17, raw_avg_conf=0.524) → `unmeasured` (`below_confidence`). At the aggregate representative-confidence granularity **1,470 raw samples abstain** (below-threshold or out-of-estate); per-sample application against the raw sweep (with actual per-window confidences, not the per-language average) would preserve high-confidence in-estate `sw`/`en` samples — the aggregate re-run is a conservative lower bound.
- **Containment posture (owner correction #4):** these false-positive labels were NEVER promoted to a measured figure. `OverlayLidDetection_v1.regime = "pre-admission"` at construction; `LidOverlayMustNotFlowIntoCountedMeasureError` refuses direct construction with `regime="post-admission"`; sealed `promote_lid_regime_by_receipted_act` requires owner signature per Canon 8 §4 W2. The mi/ar counts lived only in a raw sweep receipt, never in a counted-measure carrier — the sealed containment held.

---

## Objective L · CP-AIP-LANGUAGE-COGNITION training end-to-end (owner order 2026-02-24)

**Source (verbatim):** owner order 2026-02-24: *"since you have a baseline now, why dont akki train the cognition model so it can properly identify language? system needs to now be functional, as you now claim to have built all the capability."*

**Status:** `BLOCKED · execution · 3 owner one-word rulings requested`.

**Structural readiness (measured):**
- Corpus seam sealed (Objective H).
- Commission boundary sealed (Objective I structural).
- Track-4 wiring sealed: `register_all_three_track_4_jobs` composes LID pass + census-three-waves + training-runs job kinds; `emit_autonomy_engine_run_receipt` produces `AutonomyEngineRunReceipt_v1` (job_kind ∈ `{lid_pass, census_three_waves, training_runs}`; status ∈ `{completed, failed, refused}`; refuses `pod://*` + `/app/*` prefixed refs at seat).
- MOAC contract carrier sealed: `LanguageCognitionMoacContract_v1` (per-language ≥ 0.90 + code-switch-span ≥ 0.85 + no-speaker-ID pass + abstention reported).

**Execution blockers (owner one-word rulings requested — do not idle-halt; docs+forks landing now):**
1. **`FORK-COMPUTE-CORPUS-OUT-OF-PERIMETER`** — 12-language `google-transcripts` labelled corpus is not in the pod perimeter; Ruling (b) forbids pod as data path; corpus location + Akki-side delivery mechanism required.
2. **`FORK-COMPUTE-GPU-CREDS-PENDING-OWNER-KEY-IN`** — every `aisca-gpu-01` commissioning record is a pytest drill fixture (`vm_host` 127.0.0.1 / TEST-NET-3 range); real GPU VM credentials never keyed in per WS-BUILD-CONNECT-GPU ruling.
3. **`FORK-DP-SGD-TOOLING`** — opacus not installed on pod (~500 MB torch dep). Given pod is not the training host anyway (Ruling (b)), this is downstream of Fork 2; **owner's own verbatim from 2026-02-24 order:** *"If the DP-SGD toolchain is NOT runnable on available compute, file the fork to DESK_QUEUE with your recommendation (likely: owner opts out for this internal run, recorded) and surface it to me IMMEDIATELY."* **Recommendation banked:** owner opts out for this internal run (recorded honest-gap on execution posture); DP-SGD applies structurally at contract level and re-enters when the training host is real.

**In-pod CPU proof-of-pipeline (owner authorized fallback):** cannot be honestly executed either — the labelled corpus itself is not in-pod (Fork 1); running gradients on synthetic data would produce a pipeline-passes receipt but not a language-cognition training. Filed under Fork 1.

**Commissioned-job receipt (Ruling (b) verbatim · Akki runs it):** to be emitted at seam call `commission_language_cognition_training_run(...)` → `AutonomyEngineRunReceipt_v1` with `status="refused"` and provenance pointing at the three forks above. Pending single-sentence owner ruling on whether to emit the refused-status receipt this seal or wait for one of the forks to close first.

---

## Cross-cutting posture (verbatim from sealed carriers)

- **Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** *"E1 wires the seam INTO Census Autonomy Service; pod is never data path. Training compute + model weights + labelled corpus NEVER leave Akki's boundary."*
- **§6.9 markers-over-refusal:** overlay records CARRY the honest-gap marker; refusal exceptions are used only where an unrepresentable state must be structurally prevented (Ruling (b) prefix refusals, MOAC contract violations).
- **SO §3.8 additive-only:** every seal in this ledger UPGRADES the boundary; no sealed carrier edited.

---

## Ratchet + sweep discipline

**Ratchet floor at HALT boundary (Item 5.13 delivered):** `6411`. **Ratchet floor after this-wave additive fix (LID overlay abstention + estate-filter):** **`6430`** (+19 canonical measured — 9 new own pins + 10 tests unlocking as the composed module surface is now present) at BASELINE_GUARD=1 PYTHONHASHSEED=0 sweep completed 2026-02-24T~03:57Z from correct `backend/` cwd (per `backend/pytest.ini`) · **6430 passed / 13 skipped / 0 failed / 520 warnings in 187.11s**. RED-first proof authentic `ImportError` at 2026-02-24T~03:45Z; GREEN-post 9/9 at 2026-02-24T~03:47Z; full sweep 6430/13/0 at 2026-02-24T~03:57Z. Same-slice vendored-mirror cure applied via `tools/prod_vendor_sync.py` (1 new file written; new `structural_sha256 e636bbbbd1374a9368da58865504a51d123abab94539d1aec1f179c741f96485`). Numbers pinned in DECISIONS.md wave-card + PINS.md at the next ratchet-boundary commit.

---

**Ledger check:** this scorecard implements the CENSUS-OBJECTIVES-SCORECARD deliverable from the owner correction 2026-02-24 and nothing else. No sealed carrier edited. Additive-only per SO §3.8. `testing_agent` BANNED throughout. Zero push/fetch this session. 6 Standing Bans + 17 Standing Guards + SO §6.9 amendment + Ruling (b) AKKI-RUNS-IT verbatim all honored.
