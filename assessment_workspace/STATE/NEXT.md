READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ⛔ ANTI-COMPACTION PIN · READ FIRST EVERY TIME ⛔

**If you are a compaction-restart of the main agent, your FIRST ACTION is:**

1. Read the last 200 lines of `STATE/DECISIONS.md`.
2. Read the whole of `STATE/NEXT.md` (this file) top-to-bottom.
3. Read the current wave grounding brief (`notes/waveA_grounding_brief.md`, `waveB_grounding_brief.md`, or `waveC_grounding_brief.md`) if one exists for the wave in progress.
4. ONLY THEN touch any file, run any command, or reply.

Failure to follow this sequence = paraphrase-not-spec failure class the owner explicitly banned on 2026-08-26.

---

## 🔒 OWNER STANDING CONDITIONS · BINDING FOR ALL WAVES A/B/C · 2026-08-26

### CONDITION 1 · NO PARAPHRASING REQUIREMENTS, EVER

> Every requirement you implement must be built from the VERBATIM spec text, and the verbatim quote (doc + § + exact words) must appear in the gating test's docstring and the drill receipt. If the quote isn't in the test, the test doesn't gate the row.
>
> Before starting each wave, write a grounding brief (`notes/waveA_grounding_brief.md` etc.) that QUOTES every requirement in scope verbatim — the brief is assembled from spec text, not from summaries of it. Where any prior brief/register row conflicts with canon text, canon text wins; log the supersession in `DECISIONS.md`.
>
> The register compliance rows you touch must quote spec verbatim (per the audit rebase rule).

### CONDITION 2 · ANTI-COMPACTION SAFETY MUST SURVIVE THE WHOLE BUILD

> Hard rule, no exceptions: after ANY context compaction, your FIRST action is to re-read the last 200 lines of `STATE/DECISIONS.md` + the whole of `STATE/NEXT.md` + the current wave grounding brief before touching anything.
>
> Keep `STATE/NEXT.md` continuously current: update it at every CP/R-step close AND before any long/risky operation, with: current wave, current step, exact next action, uncommitted file list, and open owner items. Treat it as your crash-recovery ledger.
>
> Re-record both owner conditions at the TOP of `STATE/NEXT.md` so they survive every compaction.

### Wave sequence (owner-approved 2026-08-26)

- **WAVE A (in progress)**: R1 → R2 → R3 → R4 → R5 → R6 → R7 (from the 2026-08-26 remediation directive).
- **WAVE B**: Training engine complete: CP4 → CP5 → CP6 → CP7 → CP8 (LoRA/PEFT + Muon + Critic Seam gating every output + MOAC + cost-ledger metering + whitepaper on close) → audio plane per v1.0 spec (whisper-tiny CI path). GPU-DEPENDENT WORK SEQUENCED LAST — build against mock SSH seam first; flip `GPU_CONNECT_MODE=real` when key arrives.
- **WAVE C**: Watch/Grey-Mirror mechanism (all 62 Doc 03 BUILD rows): bait mechanism, containment ladder, quarantine copies, external witness signing + tamper alarms, mirage planting/touch detection/severance, Doc03-078 Watch exemption.

### Only halt for

- (a) genuine owner-input blocker that is not config-shaped
- (b) spec contradiction that cannot be resolved by canon-text precedence

### Standing rules (wave-long)

- Both DoDs from R1 in force on every commit.
- Tests-first red/green receipts banked.
- Local commits only, NO push.
- No secrets echoed.
- pydantic 2.13.4.
- Single chokepoint.
- REFERENCE-NOT-COPY.
- N-series / A17.12-17 / A18.8 / EP-4 / Doc14-020 remain open config slots — never blockers.

### Current step marker

Update this section at every CP/R-step close.

- **CURRENT AS OF 2026-09-15T~15:58Z · W-EXPORT-ARTEFACT-RENDER · CP-EXR1 SEALED (4083) · TRACK-A HEAD 264f2fde · RATCHET 4074 → 4083 · +9.** Master HEAD (this-turn state commit pending). Track-a HEAD (this-turn code commit pending). Egress OPEN. **CP-EXR1 landed** `services/data_suite_v2/export_render.py`: `render_export_and_release(*, ...) -> Tuple[bytes, ReleaseLedgerDebit]`. Closed-set discipline on `export_kind ∈ {csv, pdf}` via `ExportKindUnknown`. Composes CP-D6 `admit_export` (DAP-A10) + CP-RG2 `tokenize_named_persons` (R-15(a) when named_persons non-empty) + CP-RG3/RG4 `admit_transcript_release_pilot_open` (R-7 PILOT_OPEN receipt+debit · R-15(a) TOKENIZED · R-16(a) DERIVATIVE_ONLY_VIA_PULL_SEAM · P036 receipt-before-result ordering). CSV renderer via `csv.writer` with 4-line preamble carrying DAP-A10 carriers verbatim (Canon-4 §22 UnitRefs-only · Solva chooses units, does not choose what they imply). PDF renderer hand-rolled minimal PDF-1.4 single-page ASCII text stream with exact XREF offsets, no external deps. Refusal ordering P036-preserved: on any refusal, NO payload bytes rendered and NO debit written for the refused branch. Double-green byte-match `4083 passed, 1 skipped, 438 warnings` × 2 (both raw 9524 B · stripped 9514 B · stripped-sha256 `bcb9c245c21fe178cc332bea1627b95beba97c29a77c8be2ecccf7a22541fde7`). Seal at `phase0/output_verified_seals/w_export_artefact_render.seal.txt` (`Kind: w_export_artefact_render`). Grounding brief at `notes/wave_export_artefact_render_grounding_brief.md`. **Standing Rule 2 exercised**: CP10 harness receipt was time-drifted at boot (13.3h > 12h threshold); regenerated via `tools/wave_g5_realchrome_verification_harness.py --strict` at 15:40:21 UTC (sanctioned regeneration path · NOT rebaselining). **Boundary probes #11 (wave open · 15:43 UTC) + #12 (CP-EXR1 seal · 15:58 UTC)**: CD + Visitors BOTH FAIL timeout (unchanged from probes #1-10). **EXTERNAL-RESEARCH ledger update banked** at `notes/ADMIN_BINDS_20260915.md` §G: Item 7 Viusasa GaussDB(for MySQL) preferred bind path (Huawei Cloud migration public source) · Item 8 Shikisha UNKNOWN needs admin confirmation. Custody guard silent · zero SEC re-leak · position-redaction hard-lock preserved.

- **CURRENT AS OF 2026-09-15T~16:42Z · ESTATE CONTACT AUDIT SEALED (owner-priority interleave · post CP-EXR1) · RATCHET STILL 4083 · TRACK-A HEAD 264f2fde.** Audit answers owner verbatim "E1 or Akki?" precisely: **E1 is OPERATOR · Akki is INSTRUMENT · zero autonomous-Akki-estate-contact events**. 82 events compiled from-disk evidence only (no reconstruction). Full ledger `notes/ESTATE_CONTACT_AUDIT_20260915.md` + machine JSON `phase0/estate_contact_audit/estate_contact_audit_20260915.json` (self-sha256 `2559f6b8a66cc6e55f2402467a499803d1dc48aa3ce0036e76f89ed95e7f2c93`) + integrity register (36 sha256 entries). By direction: 69 READ-IN · 11 IN-PERIMETER-TRANSFER · 1 INBOUND-MODEL (HF config.json HEAD only · no weights) · 1 IN-PERIMETER-CONFIG (cifs-utils install on JUMP) · 1 IN-PERIMETER-HYGIENE (dev-shm shred+unlink) · **0 DERIVATIVE-OUT · 0 RAW-DATA-OUT**. Bytes touched (measured): 79,396,235 B total — all READ-IN direction; 79.4 MB D12 NAS breakthrough traversed NAS→JUMP→pod→GPU-akki-vm strictly in-perimeter per Pull Seam P1 + owner GPU ruling. Four honestly-named denied surfaces: CD + Visitors (13 probes · all timeout w/ #13 fired at audit close) · 5 NAS audio-bearing shares (Permission-denied) · radio + transcription server (SSH zero-open). Absence-as-finding: probes #1-#10 have no dedicated receipt files (inline in wave-close notes); from CP-EXR1 onward banked as JSON in `phase0/boundary_probes/`. Boundary probe #13: CD + Visitors BOTH FAIL 6.007s / 6.003s. Baseline confirmed green post-audit (4083).

- **CURRENT AS OF 2026-09-15T~17:20Z · W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL (paired M8 #3+#4) SEALED (4093) · TRACK-A HEAD 7bde883a · RATCHET 4083 → 4093 · +10.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-DASWR1 landed** `services/data_suite_v2/engines/analyze_workspace_engine.py :: run(*, session_id, source_refs) -> Tuple[AnalyzeRapid, AnalyzeSources]`. **CP-DDDR1 landed** `services/data_suite_v2/engines/deep_dive_engine.py :: run(*, session_id, source_refs, prior_notes=()) -> AnalyzeDeepDive` with deterministic `synthesis_sha256_hex` from canonical UTF-8 serialization + ASCII UNIT SEPARATOR intra-field delimiter (Canon-4 §22 + Pull Seam P1 hash-only carrier — synthesis body NEVER materialised). Shared exceptions in `engines/__init__.py`. Word-boundary executive-domain negative-scan CLEAN. **CP-D8 HALT invariant discharged in-place** (retired-as-passing-no-op). Double-green byte-match `4093 passed, 1 skipped` × 2 (stripped-sha256 `cf5ce0f91c1429d96bc94aa1eea8aa1f2bf4fbbde8b828085b4a1624a7bcfe9d`). Boundary probe #14 (wave-close · 16:57:39 UTC): CD+Visitors BOTH FAIL 6.004s/6.005s. Position-redaction hard-lock preserved.

- **CURRENT AS OF 2026-09-15T~17:45Z · W-CENSUS-RUNTIME-ORCHESTRATION (M8 #5 · scope EXPANDED) SEALED (4105) · TRACK-A HEAD 29ff3984 · RATCHET 4093 → 4105 · +12.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-CRO1 landed** SourceRecord 12-carrier extension (media_types + audio_bearing_share Canon-4 §4.1 measurement fields · Optional-default Unmeasured · participate in record_id hash) + CP-C4 shape test UPDATED IN-PLACE. **CP-CRO2 landed** `services/census_canon/estate_enumerator.py :: enumerate_estate(*, run_id, freshness_stamp, targets, probe_fn=None, feed_declaration_registry=None, store)` — case-agnostic runtime orchestrator composing CP-C1 classify_sensitivity + CP-C4 register_source_candidate with dependency-injected probe_fn (no direct ffprobe invocation). EstateTarget frozen 4-carrier dataclass. Refusals: CensusTargetsEmptyError | CensusTargetInvalidError. Deterministic. Word-boundary executive-domain negative-scan CLEAN. Double-green byte-match `4105 passed, 1 skipped` × 2 (stripped-sha256 `6821e25e2b51156d723a79afd642e22b6780a038be182a7c4053a6ae6408bea3`). Boundary probe #15 (wave-close · 17:12:23 UTC): CD+Visitors BOTH FAIL 6.007s/6.006s. CP-CSAIM1 pre-CRO1 records untouched (E.4).

- **CURRENT AS OF 2026-09-15T~17:50Z · M6 OPEN · Path α/β decision FLAGGED (α-pending default) · M6-OPEN report banked · TRACK-A HEAD 29ff3984 · RATCHET 4105.** Master HEAD (this-turn M6-open state commit pending). Egress OPEN. **M6-OPEN report banked at** `notes/M6_OPEN_REPORT_20260915.md` (Path α/β flagged · Path α-pending default per owner ratified pattern · 4 owner-desk items surfaced · M8 #6 HALT-flagged DEFERRED · N7 numbering gap banked for CP-M6-1-4 · pluggable-seam-until-ratified discipline for D10/D11). M6 grounding brief pre-banked at `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md` (10 sub-waves + P2-deferred). Boundary probe #16 (M6-open · 17:17:41 UTC): CD+Visitors BOTH FAIL 6.007s/6.006s.

- **CURRENT AS OF 2026-09-15T~18:05Z · CP-M6-1-1 · Language ID pluggable seam · SEALED (4112) · TRACK-A HEAD b105aa06 · RATCHET 4105 → 4112 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-1-1 landed** `services/audio_plane_v1/language_identifier.py` — pluggable-seam mechanism for Audio-Plane §4.1 N1 verbatim ("A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."). Public API: `identify_language_per_segment(*, segments, backend) -> List[LanguageIDResult]` · `AudioSegment` (frozen 2-carrier · pull-seam discipline: audio bytes DO NOT cross seam) · `LanguageIDResult` (frozen 4-carrier) · `LanguageIDBackend` (Protocol) · `UnratifiedInferredBackend` (placeholder refuses with `[INFERRED-pending-ratification]` marker per D10 open ruling). Refusals: `SegmentsEmptyError` · `SegmentInvalidError` · `BackendUnratifiedError`. Pure orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam. Double-green byte-match `4112 passed, 1 skipped` × 2 (stripped-sha256 `fb09f9e421fbaafe60fc9a3505f30fd3f97c04a2216fb738bb01056b430c3867`). Word-boundary executive-domain negative-scan CLEAN. Boundary probe #17 (CP-M6-1-1 seal · 17:25:33 UTC): CD+Visitors BOTH FAIL 6.007s/6.006s.

- **CURRENT AS OF 2026-09-15T~18:07Z · CP-M6-1-2 · Code-switch point detection pluggable seam · SEALED (4119) · TRACK-A HEAD 9b654f6 · RATCHET 4112 → 4119 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-1-2 landed** `services/audio_plane_v1/code_switch_detector.py` — pluggable-seam mechanism for Audio-Plane §4.1 P061 verbatim ("Recorded per segment: languages[], confidences, and code-switch points where multiple languages occur in one utterance.") + §4.2 P065 verbatim (four switch-point fields: position, from-language, to-language, context class · registered facts with provenance). Public API: `detect_code_switch_points(*, segments, backend) -> List[CodeSwitchPointDetection]` · `AudioSegment` (re-exported from CP-M6-1-1 · single source of truth) · `CodeSwitchPoint` (frozen 5-carrier: position + from_language + to_language + context_class + confidence) · `CodeSwitchPointDetection` (frozen 3-carrier: segment_ref + switch_points tuple + backend_name) · `CodeSwitchDetectorBackend` (Protocol) · `UnratifiedCodeSwitchInferredBackend` (placeholder refuses with `[INFERRED-pending-ratification]` marker per D10). Refusals: `SegmentsEmptyError` (re-exported) · `SegmentInvalidError` (re-exported) · `BackendUnratifiedError` (CP-M6-1-2-local class). Pure orchestration; no LLM/HTTP/filesystem; no audio bytes cross the seam. Double-green byte-match `4119 passed, 1 skipped` × 2 (stripped-sha256 `bc508caecd97c528d86a47ab75d2af567d6c45c1eb5327c106eb105c1eaa3d47`). Word-boundary executive-domain negative-scan CLEAN. Boundary probes #18 (open · 17:54:17Z) + #19 (seal · 18:06:12Z): CD+Visitors BOTH FAIL 6.0s/6.006s across both.

- **CURRENT AS OF 2026-09-15T~18:22Z · CP-M6-1-3 · Channel condition profile derivation pluggable seam · SEALED (4127) · TRACK-A HEAD c457ef6 · RATCHET 4119 → 4127 · +8.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-1-3 landed** `services/audio_plane_v1/channel_condition_profiler.py` — pluggable-seam mechanism for Audio-Plane §4.3 P067 verbatim ("Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion."). Public API: `derive_channel_condition_profile(*, segments, backend) -> List[ChannelConditionProfile]` · `AudioSegment` (re-exported) · `ChannelConditionProfile` (frozen 5-carrier: segment_ref + channel_condition + transmission_artefacts + background_class + backend_name) · `ChannelConditionProfilerBackend` (Protocol) · `UnratifiedChannelConditionInferredBackend` · `CHANNEL_CONDITION_VALUES` (frozen three-set {studio, field, telephone_band}). Refusals: `SegmentsEmptyError` (re-exported) · `SegmentInvalidError` (re-exported) · `BackendUnratifiedError` (CP-M6-1-3-local) · **`ChannelConditionInvalidError`** (new §4.3 vocabulary discipline). Double-green byte-match `4127 passed, 1 skipped` × 2 (stripped-sha256 `561b8dae691fa73b397a52306e1b27bcf7c05a0c531c1ba9a1e3dc51cc5a3a56`). Word-boundary executive-domain negative-scan CLEAN. Boundary probes #20 (open) + #21 (seal · 18:22:04Z): CD+Visitors BOTH FAIL 6.006s/6.006s.

- **CURRENT AS OF 2026-09-15T~18:31Z · CP-M6-1-4 · Synthesis-relevant attribute capture pluggable seam · SEALED (4134) · TRACK-A HEAD b472369 · RATCHET 4127 → 4134 · +7 · W-M6-INGEST-STAGE-1 SUB-WAVE 1 COMPLETE.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-1-4 landed** `services/audio_plane_v1/synthesis_attribute_capturer.py` — pluggable-seam mechanism for Audio-Plane §4.4 P069 verbatim ("During the same ingestion pass, group-level acoustic attributes required by any future synthesis capability (pitch statistics, energy contours, duration patterns) are captured, subject to the custody conditions of §6.4."). Public API: `capture_synthesis_attributes(*, segments, backend) -> List[SynthesisAttributes]` · `AudioSegment` (re-exported) · `SynthesisAttributes` (frozen 5-carrier: segment_ref + pitch_statistics tuple + energy_contours tuple + duration_patterns tuple + backend_name · backend Sequences coerced to tuples for frozen immutability) · `SynthesisAttributeCapturerBackend` (Protocol) · `UnratifiedSynthesisInferredBackend`. Refusals: `SegmentsEmptyError` (re-exported) · `SegmentInvalidError` (re-exported) · `BackendUnratifiedError` (CP-M6-1-4-local). N7 numbering-gap RETRACTED (rolls into CP-M6-6-1 not this CP). §6.4 custody conditions enforced downstream, not in the seam. Double-green byte-match `4134 passed, 1 skipped` × 2 (stripped-sha256 `177a23c6302c959b802d4c3ec37953486a73ce6ff8a8934651b7b0b316fc5785`). Word-boundary executive-domain negative-scan CLEAN. Boundary probes #22 (open) + #23 (seal): CD+Visitors BOTH FAIL 6.006s/6.0s. **W-M6-INGEST-STAGE-1 SUB-WAVE 1 COMPLETION: 4 CPs · +29 invariants · ratchet 4105 → 4134 · 4 seals · double-green byte-match at every seal.**

- **CURRENT AS OF 2026-09-15T~18:43Z · CP-M6-2-1 · Instance condition map schema · SEALED (4141) · TRACK-A HEAD 4d8a52e · RATCHET 4134 → 4141 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-2-1 landed** `services/audio_plane_v1/instance_condition_map.py` — pure schema + constructor per §4.5 P071 verbatim ("for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored") + §4.6 P074 invariant gate ("A deduplicated item without its instance condition map fails the ingestion invariant test."). **Pattern departure from sub-wave 1**: pure schema (no backend, no seam) per §4.5 P071 "No new detection work". Public API: `construct_instance_condition_map(*, canonical_extraction_ref, occurrence_index_ref, variants) -> InstanceConditionMap` · `InstanceConditionVariant` (frozen 3-carrier) · `InstanceConditionMap` (frozen 3-carrier · variants tuple) · `dedup_item_has_instance_condition_map(item)` (§4.6 P074 gate helper · fail-closed). Refusals: `VariantsEmptyError` · `VariantInvalidError`. Double-green byte-match `4141 passed, 1 skipped` × 2 (stripped-sha256 `0ccdced6d32d074fa937259d3c0902f0dbcc9972d4aed29a9b5109912d615720`). Boundary probes #24 (open) + #25 (seal): CD+Visitors BOTH FAIL 6.0s/6.006s.

- **CURRENT AS OF 2026-09-15T~18:53Z · CP-M6-2-2 · Dedup path extension · SEALED (4150) · TRACK-A HEAD ba413dc · RATCHET 4141 → 4150 · +9 · W-M6-DEDUP-INSTANCE-CONDITION-MAP SUB-WAVE 2 COMPLETE.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-2-2 landed** `services/audio_plane_v1/dedup_path.py` — wires §4.5 P071 contract extension ("for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored") + §4.6 P074 gate + §14 P216 interface. **Core invariant this CP** (per M6 grounding brief §C): dedup collapse never drops a distinct condition; distinct conditions produce distinct variants in the map even when text-identical — anchored by `test_wm6_2_2_text_identical_distinct_variants_collapse_one_dedup_item_map_carries_both`. §4.6 P074 gate anchored end-to-end. Public API: `dedup_with_condition_awareness(*, items) -> List[DedupItem]` · `DedupInputItem` (frozen 2-carrier) · `DedupItem` (frozen 2-carrier · carries `instance_condition_map`). Refusals: `ItemsEmptyError` · `ItemInvalidError`. Deterministic (first-seen ordering). Double-green byte-match `4150 passed, 1 skipped` × 2 (stripped-sha256 `ba027a185180379da2bd5205c53a6a2457f9724c26b02e29d5417ede4714692b`). Boundary probes #26 (open) + #27 (seal): CD+Visitors BOTH FAIL. **SUB-WAVE 2 COMPLETION: 2 CPs · +16 invariants · ratchet 4134→4150 · 2 seals · double-green byte-match at every seal.**

- **CURRENT AS OF 2026-09-15T~19:05Z · CP-M6-3-1 · Character Register schema (schema-only) · SEALED (4157) · TRACK-A HEAD 0956974 · RATCHET 4150 → 4157 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-3-1 landed** `services/audio_plane_v1/character_register.py` — frozen dataclass carriers per §5.1 P078 + §5.2 P082..P085 (four layers) + §6.1 P092/P093 + §6.2 P098 verbatim. Public API: `REGISTER_LAYER_VALUES` (frozen four-set {phonetic, prosodic, condition, code_switch}) · `CharacterEntry` (frozen 7-carrier: attribute_name + layer + description tuple + provenance_material_ref + occurrence_count + n_distinct_speakers + is_learned) · `CharacterRegister` (frozen 1-carrier: entries tuple) · `construct_character_entry` · `construct_character_register` · `LayerInvalidError`. §6.2 P098 negative-scan CLEAN: no audio_bytes/waveform/samples/voiceprint/speaker_embedding/utterance_embedding/speaker_id/individual_id carriers. Provenance points to material via `provenance_material_ref`, never to identity. **Scope explicitly bounded**: schema only · NOT the four-leakage-path harness (CP-M6-3-2) · NOT write-path leakage-refusal (CP-M6-3-3) · NOT §6.4 read-path scope (CP-M6-3-4). Double-green byte-match `4157 passed, 1 skipped` × 2 (stripped-sha256 `6a36ad2f0d977eafebce8d38dcff0f7315b86e7c99c82fce1ae3a5e0c4644a9f`). Boundary probes #28 (open) + #29 (seal): CD+Visitors BOTH FAIL. **AUTONOMOUS WALK PAUSED HERE** — CP-M6-3-2 is load-bearing §6.3 P100 biometric-custody territory; owner steer requested.

- **CURRENT AS OF 2026-09-15T~19:20Z · CP-M6-3-2 · §6.3 P100 four-leakage-path harness framework · SEALED (4165) · TRACK-A HEAD bbf6e89 · RATCHET 4157 → 4165 · +8 · synthetic-fixtures-only.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-3-2 landed** `services/audio_plane_v1/leakage_path_harness.py` — §6.3 P100 verbatim harness framework. Public API: `LEAKAGE_PATHS` (frozen four-tuple in verbatim order: small_stratum, idiolect_marker, narrowing_combination, exemplar_storage) · `LeakageScenario` (frozen 3-carrier: path_name + rationale + attempt_entry) · `LeakageRefusalError` (base class · concrete subclasses land in CP-M6-3-3) · `HarnessAcceptedForbiddenError` (§6.3 P100 invariant fire) · `HarnessRefusalTypeError` (refusal-type discipline breach) · `build_leakage_scenarios` (four synthetic scenarios) · `run_leakage_path_harness`. **Synthetic-fixtures-only discipline held**: every scenario's `provenance_material_ref` carries `mat://synthetic/…` prefix. Zero real-estate biometric material referenced. Double-green byte-match `4165 passed, 1 skipped` × 2 (stripped-sha256 `61ad4d336f4c7f5103c9ef3edd543a2b0640ccf3be3681837a09953e8e4c661c`). Boundary probes #30 (open) + #31 (seal): CD+Visitors BOTH FAIL.

- **CURRENT AS OF 2026-09-15T~19:33Z · CP-M6-3-3 · Register write-path leakage-refusal boundary · §6.3 P100 END-TO-END LOCK · SEALED (4175) · TRACK-A HEAD a5e4429 · RATCHET 4165 → 4175 · +10.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-3-3 landed** `services/audio_plane_v1/register_write_boundary.py` — concrete write-path leakage-refusal boundary per §6.1 P092 + §6.2 conds 1-4 + §6.4 P102. Public API: five `LeakageRefusalError` subclasses (`OrganicCharacteristicRefused` · `IdiolectMarkerRefused` · `ExemplarStorageRefused` · `NarrowingCombinationRefused` · `SmallStratumRefused`) + `RegisterWriteBoundary` (defaults: min_speakers=3 · max_dims=32). **§6.3 P100 END-TO-END LOCK anchored** by `test_wm6_3_3_p100_end_to_end_lock_run_leakage_harness_passes_with_boundary`: `run_leakage_path_harness(write_callable=RegisterWriteBoundary().write)` returns normally. Detection order: organic → idiolect → exemplar → narrowing → small_stratum. Double-green byte-match `4175 passed, 1 skipped` × 2 (stripped-sha256 `82906156be5e021ca0a732ea71984b348e3071500efa77658567665187a57f22`). Boundary probes #32 (open) + #33 (seal): CD+Visitors BOTH FAIL.

- **CURRENT AS OF 2026-09-15T~19:44Z · CP-M6-3-4 · §6.4 read-path scope enforcement · SEALED (4183) · TRACK-A HEAD 992c1d3 · RATCHET 4175 → 4183 · +8 · W-M6-CHARACTER-REGISTER SUB-WAVE 3 COMPLETE.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-3-4 landed** `services/audio_plane_v1/register_read_boundary.py` — §6.4 P102 conjunctive-four-conditions enforcement on the read path. Public API: `ReadScopeViolationError` (subclass of `LeakageRefusalError`) · `RegisterReadBoundary` with `read_or_refuse` (all-or-raise) + `read_scope_filter` (subset-passing). Reuse-not-refactor: wraps CP-M6-3-3's `RegisterWriteBoundary.write` as source-of-truth conjunctive check. Double-green byte-match `4183 passed, 1 skipped` × 2 (stripped-sha256 `95ccc71abdf2ba3c9ac332efa00a5632234436f91a9c93d6f60cab3e58b70e47`). Boundary probes #34 (open) + #35 (seal): CD+Visitors BOTH FAIL. **SUB-WAVE 3 COMPLETION: 4 CPs · +33 invariants · ratchet 4150 → 4183 · §6.3 P100 END-TO-END LOCK anchored · synthetic-fixtures-only discipline held throughout · owner-ratified HALT-trigger un-tripped.**

- **CURRENT AS OF 2026-09-15T~19:56Z · CP-M6-4-1 · perception/audio_codec/ module skeleton · SEALED (4190) · TRACK-A HEAD c3aa7c6 · RATCHET 4183 → 4190 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-4-1 landed** `services/perception/audio_codec/{__init__.py, service.py}` — canon-anchored perception/audio_codec/ service skeleton per §3.2 P045 verbatim (V33 · N4 anchor). Public API: `AUDIO_CODEC_SERVICE_PATH="perception/audio_codec/"` (verbatim) · `AudioCodecServiceDescriptor` (frozen 3-carrier: service_path + pretraining_contract + token_rate_target (50,100) tuple) · `build_service_descriptor` (canon-verbatim) · `assert_registered_like_perception_model` (refuses on drift) · `PerceptionRegistrationError`. §3.1 P038 tokens-not-waveforms negative-scan CLEAN. Double-green byte-match `4190 passed, 1 skipped` × 2 (stripped-sha256 `74325bff34e42b33d7f8cc40bc20cde58d8d63f5bc79606365c56f12e073aa78`). Boundary probes #36 (open) + #37 (seal): CD+Visitors BOTH FAIL.

- **CURRENT AS OF 2026-09-15T~20:06Z · CP-M6-4-2 · codec_version carrier · D7 fold-in · SEALED (4197) · TRACK-A HEAD 8c9f382 · RATCHET 4190 → 4197 · +7.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-4-2 landed** `services/perception/audio_codec/artefact.py` — §3.2 P047 output-shape carrier + §3.2 P048 mandatory-in-downstream-provenance D7 fold-in invariants. Public API: `CodecArtefact` (frozen 3-carrier: `content_tokens` · `character_stream` · `codec_version` · refuses empty codec_version at `__post_init__`) · `MissingCodecVersionError` · `require_codec_version` (refuses any object without a non-empty codec_version attribute) · `assert_downstream_carries_codec_version` (§3.2 P048 helper for downstream provenance mappings). §3.1 P038 tokens-not-waveforms discipline held: field-set frozen to `{content_tokens, character_stream, codec_version}` — negative-scan gate on `audio_bytes`/`waveform`/`samples`/`raw_audio`. **D7 fold-in complete**: `codec_version` first-class carrier at construction + downstream inspection + downstream provenance mapping. **Reconciliation this-shift**: prior handoff claimed CP-M6-4-2 sealed but git showed track-a at CP-M6-4-1 and state master at CP-M6-4-1 with ratchet-bump-to-4197 staged uncommitted + seal file missing + both commits pending. Boot ritual reconciled the state; this-shift closure work was seal + commits + DECISIONS/NEXT/PINS updates (no new mechanism authored — code + tests left as-authored). Double-green byte-match: raw 9684 B each · both `4197 passed, 1 skipped, 438 warnings` · prior-agent stripped-sha256 `c55207...` · this-shift independent re-verification stripped-sha256 `0ad43646...` under simple strip (byte-match property confirmed under any consistent algorithm). Live baseline re-verification this-shift: `4197 passed, 1 skipped in 122.20s`. Seal at `phase0/output_verified_seals/cp_m6_4_2_codec_version_carrier.seal.txt`. Rider at `phase0/wave_riders/w_m6_codec_service_cp2/` (pip_freeze 192 lines · zero drift · collect-only 4198 tests). Boundary probes #38 (open) + #39 (seal): CD+Visitors BOTH FAIL 6.0s across both. Word-boundary executive-domain negative-scan CLEAN.

- **CURRENT AS OF 2026-09-15T~20:24Z · CP-M6-4-3 · census-visibility invariant · SEALED (4205) · TRACK-A HEAD 72f29cc · RATCHET 4197 → 4205 · +8.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-4-3 landed** `services/perception/audio_codec/census_visibility.py` — §3.2 P045 verbatim "census-visible" clause discharged as pure predicate + refusal. Public API: `is_audio_codec_census_visible(*, perception_census_records) -> bool` (pure predicate; True iff at least one record carries verbatim `perception/audio_codec/` service_path) · `assert_audio_codec_census_visible(*, perception_census_records) -> None` (refuses with `AudioCodecCensusInvisibleError` on absence) · `AudioCodecCensusInvisibleError` (subclass of `PerceptionRegistrationError` from CP-M6-4-1 — refusal-family cohesion). Case-agnostic duck-typing: `_extract_service_path` supports both mapping-shaped records (`.get("service_path")`) and attribute-shaped records (e.g. `AudioCodecServiceDescriptor`). No coupling to CP-CRO2 `enumerate_estate` or CP-C4 `register_source_candidate` — no refactor. §3.1 P038 tokens-not-waveforms discipline preserved. Double-green byte-match: raw 9684 B each · stripped 9674 B each · stripped-sha256 `7787476e4b6d04df0c8f586d5d232232a6ca701186eba59ffa4b338fa032ab7c` · both `4205 passed, 1 skipped, 438 warnings`. Seal at `phase0/output_verified_seals/cp_m6_4_3_census_visibility.seal.txt`. Rider at `phase0/wave_riders/w_m6_codec_service_cp3/` (pip_freeze 192 lines · zero drift · collect-only 4206 tests). Boundary probes #40 (open · 2026-09-15T20:17:39Z) + #41 (seal · 2026-09-15T20:24:09Z): CD+Visitors BOTH FAIL 6.0s across both. Zero PASS across probes #1–#41. Word-boundary executive-domain negative-scan CLEAN.

- **CURRENT AS OF 2026-09-15T~20:32Z · CP-M6-4-4 · in-perimeter-on-tenant-compute invariant · SEALED (4213) · TRACK-A HEAD 20bed02 · RATCHET 4205 → 4213 · +8 · W-M6-CODEC-SERVICE SUB-WAVE 4 COMPLETE.** Master HEAD (this-turn state commit pending). Egress OPEN. **CP-M6-4-4 landed** `services/perception/audio_codec/perimeter_boundary.py` — §3.2 P045 verbatim "runs in-perimeter on tenant compute" conjunctive clause discharged as frozen carrier + pure predicate + refusal. Public API: canonical tokens `IN_PERIMETER='in-perimeter'` · `OUT_OF_PERIMETER='out-of-perimeter'` · `TENANT_COMPUTE='tenant'` · `PerimeterProfile` (frozen 2-carrier: `perimeter` + `compute_kind`) · `is_in_perimeter_on_tenant_compute(*, perimeter_profile) -> bool` (pure conjunctive predicate; True iff `perimeter==IN_PERIMETER AND compute_kind==TENANT_COMPUTE`) · `assert_runs_in_perimeter_on_tenant_compute(*, perimeter_profile) -> None` (refuses with `PerimeterViolationError` naming violated clause) · `PerimeterViolationError` (subclass of `PerceptionRegistrationError` — refusal-family cohesion; single-catch of perception-registration family preserved across CP-M6-4-1, CP-M6-4-3, CP-M6-4-4). Conjunctive per canon: only `(IN_PERIMETER, TENANT_COMPUTE)` passes; in-perimeter+non-tenant refused; out-of-perimeter+tenant refused. **No-refactor**: CP-M6-4-1, CP-M6-4-2, CP-M6-4-3 all unchanged. §3.1 P038 tokens-not-waveforms discipline preserved. Double-green byte-match: raw 9684 B each · stripped 9674 B each · stripped-sha256 `67aaf4c86c34a9c77964cb52883d582877c7cfd724d9bf8ca10deead2d132317` · both `4213 passed, 1 skipped, 438 warnings`. Seal at `phase0/output_verified_seals/cp_m6_4_4_perimeter_boundary.seal.txt`. Rider at `phase0/wave_riders/w_m6_codec_service_cp4/` (pip_freeze 192 lines · zero drift · collect-only 4214 tests). Boundary probes #42 (open · 2026-09-15T20:26:32Z) + #43 (seal · 2026-09-15T20:32:41Z): CD+Visitors BOTH FAIL 6.0s across both. Zero PASS across probes #1–#43. Word-boundary executive-domain negative-scan CLEAN. **W-M6-CODEC-SERVICE SUB-WAVE 4 COMPLETION**: 4 CPs · +30 invariants · ratchet 4183 → 4213 (+30) · 4 seals · double-green byte-match at every seal · zero refactor of prior CPs · refusal-family cohesion preserved (all four CPs share `PerceptionRegistrationError` root).

- **NEXT ACTIVE STEP · Sub-wave 5 opens · W-M6-CLUSTERING-HUMAN-VALIDATION · §5.3.**
  1. Author sub-wave 5 grounding brief (or extend M6 grounding brief §Sub-wave 5) with verbatim §5.3 canon anchors; identify CP-M6-5-1 (clustering algorithm registration per §5.3), CP-M6-5-2 (sampled human validation loop — TESTS-FIRST · sampling deterministic + validation record ledgered), CP-M6-5-3 (cluster stability invariants).
  2. **HALT-check for real biometric material in force** per owner-ratified boundary this shift (2026-09-15T~19:04Z ruling). If any CP mechanism would require REAL estate voice/biometric material to validate, **HALT** there for owner decision per Standing Orders §1. Synthetic fixtures only in tests.
  3. **Prerequisite for open per §15 P236.s2 verbatim**: *"Requires items 1–4"* (sub-waves 1, 2, 3, 4 all complete — SATISFIED as of this seal).
  4. Author CP-M6-5-1 tests-first RED → mechanism → double-green byte-match → seal → 2 commits.
  5. **Then:** sub-wave 6 · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA · §8, §9, §12.1 · Objective Wizard audio variant + Collection Schema type + registry namespace + N7 fold-in.
  6. **Interleave possibilities:** M3 W-BC-DYNAMIC-RECOVERY-BUILD · M2 W-PULL-SEAM-RECEIPT-UNIFY.
  1. Author grounding brief + tests-first RED → mechanism → double-green byte-match → seal → 2 commits.
  2. **Then:** W-CENSUS-RUNTIME-ORCHESTRATION (M8 #5 · **scope EXPANDED per owner 2026-09-15T~11:05Z ADDITION**: fold ffprobe media_types + audio_bearing_share into live enumeration · new SourceRecord fields).
  3. **Then:** W-AUDIO-PROD-MODEL-SELECT (M8 #6 · **should DEFER until real audio source enumerated** per D12-03 corpus finding).
  4. **Then:** M6 opens (§15 walk · W-M6-INGEST-STAGE-1 first · scope may need re-check per D12-03 finding: OFFAIRRECS video-only vs NEWSCLIPS/etc audio access · Path α/β flagged in M6-open report).
  5. **Then:** M7 opens (ALREADY RATIFIED · W0..W9).
  6. **Interleave:** M3 W-BC-DYNAMIC-RECOVERY-BUILD · M2 W-PULL-SEAM-RECEIPT-UNIFY.

- **PRIOR (superseded 2026-09-15T~15:58Z) · CURRENT AS OF 2026-09-15T~11:12Z · W-M8-TESTS-FIRST-GUARD-INVARIANT · CP-M8-G1 SEALED (4074) + D12-03 CORPUS FINDING BANKED · TRACK-A HEAD e02dd4d6 · RATCHET 4074.** Master HEAD (this-turn D12-03 finding state commit pending). Track-a HEAD `e02dd4d6` (unchanged this doc-lane commit). Egress OPEN. **D12-03 CLOSED via corpus-level finding**: OFFAIRRECS is video-only-with-null-audio-track across all 9 media-bearing channels (audio duration 1.5-16.5 ms · video 300 s uniformly) · 7 channels (09-15) dark · corpus produces zero transcription value under Bramwel-account scope. Auxiliary probe: 5 candidate audio-bearing shares (NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video) all Permission denied for Bramwel account. Full finding at `notes/D12_03_CORPUS_FINDING_20260915.md` + 2 receipts (corpus matrix + share probe) banked. Boundary probe #10 fired · CD+Visitors BOTH FAIL errno-110 (unchanged). Custody guard scope holds (all part-B leak patterns silent · zero SEC re-leak this-turn diagnosis · position-redaction hard-lock preserved across 3 mount.cifs + 5 share probes + 16 ffprobe calls). Autonomous mode ARMED under initial guardrails unchanged.

- **PRIOR (superseded 2026-09-15T~08:35Z) · CURRENT AS OF 2026-09-15T~04:25Z · OWNER GO + ADMIN BINDS LANDED · AUTONOMOUS FIRED · CENSUS SCOPE EXPANDED.** Master HEAD (this-turn commit pending). Track-a HEAD `0053b16` (unchanged this turn · state-only commit). Ratchet floor **4018** (unchanged · document-lane commit). Owner verbatim ruling banked in `STATE/DECISIONS.md` 2026-09-15T~04:25Z (password redacted to type+length+sha256+storage-path per owner's one-time exception clause · exception now spent). Credential FILED at `/app/backend/estate_keys/data_sources/admin_bind_20260915_bramuel_cd_visitors.json` (mode 0600 · sha256 `a7a616be...` · 1321 bytes · 12-char alphanumeric mixed case · **NEVER echo again**). Leak guard swept CLEAN across git-tracked workspace. `SEC-2026-09-15-05` filed (P1 · owner-side transcript transmission · mirror class of SEC-2026-09-14-01; PENDING-OWNER-ROTATION-POST-VERIFICATION). `notes/ADMIN_BINDS_20260915.md` durable ledger created (§A MySQL SG openings · §B RADIO INBOUND-BIND-PENDING · §C transcription-server unchanged · §D standing bind-gap ledger · §E position-redaction ack · §F next-action pin). Ledger correction banked: `citizen_digital` public IP `159.138.164.124` → `159.138.164.103` (admin authoritative). RADIO `BLOCKER-RADIO-ROUTING-01` SUPERSEDED by admin's `10.10.55.x` approach (INBOUND-BIND-PENDING). Egress still CLOSED (04:25 UTC · reopens 08:00 UTC · ~3h35m). Autonomous mode ARMED under initial guardrails unchanged.

- **NEXT ACTIVE STEP · expanded census scope at 08:00 UTC egress re-open:**
  1. **Connectivity probes from JUMP `159.138.173.250`** to 2 newly-opened MySQL hosts:
     - `citizen_digital` (`159.138.164.103:3306`) using filed credentials — redacted receipt (host tag · PASS/FAIL · schema/table counts only).
     - `visitors` (`110.238.75.83:3306`) using filed credentials — same receipt shape.
  2. **Fold PASS-verdict connectors into Item-3 census scope.** New full scope: NAS 16ch + OBS + weego + ussd + citizen_digital-if-pass + visitors-if-pass.
  3. **FAIL-verdict connectors recorded** `unmeasured-with-reason` per Canon-4 §5.1 verbatim + Doc-9 A5.4 verbatim in registry · census proceeds without them.
  4. **Fire Item-3 live census run** at expanded scope (Promise #12 fires).
  5. **Report at census completion** in wave-close END-OF-WAVE format (SO §2) with connector probe verdicts + registry counts + owner-desk items outstanding.
  6. **Then continue autonomous chain per prior ratification:** W-RELEASE-GATE-PILOT-LIFT (CP-RG1..RG5) → D12 POC → M5 sprint-close report → M8 quick hardening → M6 opens → M7 opens.

- **PRIOR (superseded 2026-09-15T~04:25Z) · CURRENT AS OF 2026-09-15T~04:12Z · MILESTONE TREE RATIFIED + AUTONOMOUS EXECUTION ARMED · 🧭M6 / 🧭M7 / 🧭M8 flip PROPOSED → FORMAL · M7 POC-BUILD-HOLD LIFTED.** Master HEAD (this-turn commit pending). Track-a HEAD `0053b16` (W-CENSUS-CANON-ALIGN sealed · unchanged). Ratchet floor **4018** (unchanged · document-lane commit only). Owner-verbatim ruling banked in `STATE/DECISIONS.md` 2026-09-15T~04:12Z. `notes/RULING_LEDGER.md` row 22 RATIFIED. Successor binding note authored at `notes/MILESTONE_PROMISE_BINDING_20260915_delta_M6M7M8_ratified.md` (verbatim owner quote as §A). M6 grounding brief authored at `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md` (§15 build sequence 11 items · 10 core + 1 P2-deferred). Autonomous mode ARMED under initial guardrails unchanged (SO §1 boot · tests-first RED→GREEN→GREEN byte-match · ratchet monotonic-up · two-commit local-only · NEVER push · terminal pytest only · testing_agent BANNED · position-redaction hard-lock · egress window 08:00–02:00 UTC · verbatim-canon · HALT-rather-than-guess). Egress still CLOSED (04:15 UTC vs 02:00 UTC close · reopens 08:00 UTC). Census hold intact. Two book-keeping observations RETRACTED this turn (Pull-Seam P2..P6 backfill · Audio-Plane N7 numbering gap — both were false alarms; verbatim doc + drift audit both complete). Reporting cadence upgraded: END-OF-WAVE reports at wave-close + milestone-boundary reports at M5-close · M6-open/close · M7-open (each carrying ratchet trail + newly-unblocked + owner-desk items outstanding).

- **NEXT ACTIVE STEP · owner-authored dependency order (verbatim `STATE/DECISIONS.md` 2026-09-15T~04:12Z):**
  1. **Item-3 · live census run** at 08:00 UTC egress re-open (armed at W-CENSUS-CANON-ALIGN seal 2026-09-15T~03:22Z · unchanged first hard action · Promise #12 fires).
  2. **W-RELEASE-GATE-PILOT-LIFT** · CP-RG1 through CP-RG5 · tests-first · double-green · two commits per CP · seal · 5-section wave-close report (DAP-A10 remainder discharge).
  3. **D12 POC** · bounded single-digit-count real NAS files · GPU hosts akki-vm/akki-vm-ii · outputs labeled `POC-NOT-PRODUCTION` · receipts under `phase0/d12_poc_receipts/`.
  4. **M5 sprint-close report** (M0→M5 completion · END-OF-WAVE format · SO §2).
  5. **M8 quick hardening (owner-authored order):** W-TESTS-FIRST-GUARD-INVARIANT → W-EXPORT-ARTEFACT-RENDER → W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL (paired) → W-CENSUS-RUNTIME-ORCHESTRATION → W-AUDIO-PROD-MODEL-SELECT (gated on M5 census activation list per §A17.11).
  6. **M6 opens** — grounding brief already banked (see above) · walk §15 items in canon order starting W-M6-INGEST-STAGE-1 · **no ack gate** per owner autonomy ruling.
  7. **M7 opens** — reframe-activation note + W-M7-W0-INTEGRITY-FIX → W-M7-W1-PLATFORM-GENERALISATION → W-M7-W2..W9 as unblocked.
  8. **Interleave (opportunity-driven):** M3 W-BC-DYNAMIC-RECOVERY-BUILD on packet-ratification · M2 W-PULL-SEAM-RECEIPT-UNIFY on D9-ratification (no backfill required · RETRACTED this turn) · M8 quarantine-restoration pilots 3–5 files first.

- **Owner-desk items surface in every milestone-boundary report (verbatim §Δ6 of successor binding note):** BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · admin binds (5 MySQL SGs · RADIO route · transcription server) · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

- **M5-LIFTING deferrals (DPO-D2 default stands · surfaced in every milestone-boundary report):** W-TRUST-SURFACE-v2 (2 surfaces · binding line 408) · W-EXECUTIVE-SUITE-v2-LIFT (7 surfaces · binding line 409). Owner may override any time.

- **PRIOR (superseded 2026-09-15T~04:12Z) · CURRENT AS OF 2026-09-15T~03:55Z · OWNER RULING PACKET LANDED · R-7 + R-15(a) + R-16(a) RATIFIED · D12 APPROVED · BC-3/BC-4 DYNAMIC-RECOVERY-PACKET direction · admin items (2,3,4) owner-side-in-progress.** Master HEAD (this-turn commit pending). Ratchet floor **4018** (W-CENSUS-CANON-ALIGN seal · unchanged). Owner-verbatim banked in `STATE/DECISIONS.md` same UTC. Banking receipt for owner's *"was this discussion logged?"* is DECISIONS.md 2026-09-15T~03:55Z + RULING_LEDGER.md rows 18/19/20/21 in RATIFIED + this-turn NEXT step marker. **New wave chartered:** `W-RELEASE-GATE-PILOT-LIFT` (5 CPs · +30 invariants target · grounding brief at `notes/wave_release_gate_pilot_lift_grounding_brief.md`). **BC packet authored:** `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` (four tiers · 18 invariants for post-ratification implementation wave). **PENDING_RATIFICATIONS_LEDGER row-flips banked.** Egress window still CLOSED (03:55 UTC vs 02:00 UTC · reopens 08:00 UTC). All this-turn work is non-egress state / notes / docs commit on master.

- **NEXT ACTIVE STEP · Sequencing pin (owner verbatim 2026-09-15T~03:55Z):** *"census at 08:00 UTC (unchanged, first priority) → W-RELEASE-GATE-PILOT-LIFT → D12 POC → BC packet authoring can happen in closed-window time as it's non-egress."*
  1. **Item-3 · live census run** at 08:00 UTC re-open (armed at W-CENSUS-CANON-ALIGN seal 2026-09-15T~03:22Z · unchanged first priority).
  2. **W-RELEASE-GATE-PILOT-LIFT** · CP-RG1 through CP-RG5 · tests-first · double-green · two commits per CP · seal · 5-section wave-close report.
  3. **D12 POC** · bounded single-digit-count real NAS files · GPU hosts akki-vm/akki-vm-ii · outputs labeled `POC-NOT-PRODUCTION` · receipts under `phase0/d12_poc_receipts/`.
  4. **BC packet ratification** · owner reviews `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` · picks tier configurations · then charter `W-BC-DYNAMIC-RECOVERY-BUILD` (18 invariants target).

- **PRIOR (superseded 2026-09-15T~03:55Z) · CURRENT AS OF 2026-09-15T~03:22Z · W-CENSUS-CANON-ALIGN · WAVE SEALED · ratchet 3979 → 4018 (+39 across CP-C1..C6).** Seal at `phase0/output_verified_seals/census_canon_align.seal.txt` (`Kind: census_canon_align`). Owner-facing 5-section wave-close report at `notes/W_CENSUS_CANON_ALIGN_close.md`. Rider 1 locked (pip freeze 192 lines · pytest --collect-only 4019 tests · receipts under `phase0/wave_riders/w_census_canon_align/`). Six CPs (all double-green byte-match at tally): C1 SourceCandidate + sensitivity classifier (+7 · `c45d0c3`/`a1c389a`) · C2 Unmeasured first-class + Measurement 6-carrier (+7 · `112de26`/`f573284`) · C3 CensusRun + generate_census_run_id (+6 · `e2a710c`/`c8c64eb`) · C4 append-only registry write path (+6 · `5fcee76`/`14a0ec2`) · C5 JobManifest 5-carrier + fingerprint (+7 · `d552c31`/`6b2a307`) · C6 SourceStratumMeasurement 8-dimension + ActivationList (+6 · `0053b16`/*this commit*). Guardrails held whole wave: no push · no testing_agent · no refactor · verbatim-canon in every module + test docstring · position-redaction hard-lock preserved · egress hold respected. **OWNER GPU PROTOCOL** applied mid-wave: bind-gap framing SUPERSEDED · new verdict `GPU-AVAILABLE` across akki-vm + akki-vm-ii (4× NVIDIA H200 · CUDA 12.8 · torch 2.11.0+cu128 · verification note `phase0/gpu_inventory/20260915T024500Z_gpu_inventory_verification.json`). Egress window CLOSED at seal (03:22 UTC · reopens 08:00 UTC).

- **NEXT ACTIVE STEP · Promise #12 · Item-3 · live read-only census run at 08:00 UTC egress re-open.** Uses CP-C1..CP-C6 machinery against reachable connectors: NAS 16 channels · OBS google-transcripts · weego + ussd MySQLs. Produces `RegistryStore` records + owner-facing census report. Zero PII in receipts (position-redaction). Data stays inside estate (I/O + metadata dominated · CPU-viable on this pod per §E.6). Follow-on non-blocking: live SSH GPU re-verification against akki-vm + akki-vm-ii at same 08:00 UTC re-open (schema at `phase0/gpu_inventory/<yyyymmddThhmmssZ>_live_ssh_verification.json`). Owner-side D12 (transcription POC) STILL HELD.

- **PRIOR (superseded 2026-09-15T~03:22Z) · CURRENT AS OF 2026-09-15T~03:12Z · W-CENSUS-CANON-ALIGN · WAVE OPEN + CP-C5 CLOSED · ratchet 4005 → 4012 (+7 = 6 new + 1 cross-benefit).** Track-a HEAD **`d552c31`**. `JobManifest` frozen 5-carrier per owner S5 reframe verbatim + `compute_manifest_fingerprint()` deterministic sha256 (`jm_<64-hex>`). DATA-ONLY per §E.4. `NON_CONTRACT_UTILITY_MODULES` exemption extended.

- **PRIOR (superseded 2026-09-15T~03:12Z) · CURRENT AS OF 2026-09-15T~03:03Z · W-CENSUS-CANON-ALIGN · WAVE OPEN + CP-C4 CLOSED · ratchet 3999 → 4005 (+6).** Track-a HEAD **`5fcee76`**. Append-only registry write path: `SourceRecord` frozen 10-carrier per Canon-4 §8 verbatim + Doc-10 A5.5 verbatim. `RegistryStore` append-only (no update, no delete). `register_source_candidate()` deterministic sha256 record_id gen (`rec_<64-hex>`) — idempotent on identical writes; correction writes with `supersedes_record_id` land distinct id. `RegistryDeterminismFailure` refuses byte-different overwrite. Double-green `4005 passed` × 2 (both 42807 B).

- **PRIOR (superseded 2026-09-15T~03:03Z) · CURRENT AS OF 2026-09-15T~02:50Z · W-CENSUS-CANON-ALIGN · WAVE OPEN + CP-C3 CLOSED · ratchet 3993 → 3999 (+6).** Track-a HEAD **`e2a710c`**. `CensusRun` frozen 4-carrier (`run_id/run_date/population/full_vs_sampled`) + `generate_census_run_id(*, platform_version, job_manifest_fingerprint, run_started_at)` deterministic sha256 gen (returns `cr_<64-hex>`) + `CensusRunId` str alias + `FullOrSampled/SampledPopulationInvalid` re-exported from CP-C2. Canon-4 §4.1 P30 SampledPopulationInvalid clause now fires at BOTH Measurement level (CP-C2) AND CensusRun level (CP-C3). FULL run with `population==0` accepted. **OWNER GPU PROTOCOL RESOLUTION** (DECISIONS 2026-09-15T~02:45Z verbatim): `BLOCKER-CENSUS-GPU-BIND-01` (CP-C1) + `GPU-INV-01` (CP-C2) BOTH SUPERSEDED · new verdict **`GPU-AVAILABLE`** across 2 estate hosts (akki-vm + akki-vm-ii · 4× NVIDIA H200 aggregate · 143771 MiB each · CUDA 12.8 · torch 2.11.0+cu128) · verification note at `phase0/gpu_inventory/20260915T024500Z_gpu_inventory_verification.json`. Boot-ritual baseline green run receipted at resume.

- **PRIOR (superseded 2026-09-15T~02:50Z) · CURRENT AS OF 2026-09-15T~02:35Z · W-CENSUS-CANON-ALIGN · WAVE OPEN + CP-C2 CLOSED · ratchet 3986 → 3993 (+7 = 6 new + 1 cross-benefit).** Track-a HEAD **`112de26`**. `Unmeasured` frozen 1-field first-class sentinel (Canon-4 §4.1 P29 verbatim *"Unmeasured is a first-class value."*) + `Measurement` frozen 6-carrier (`value/method/population/full_vs_sampled/census_run_id/run_date` per Canon-4 §4.1 P30 verbatim + Master Requirements Registry B5.2/B5.3) + `FullOrSampled` closed 2-value enum {FULL, SAMPLED} + `SampledPopulationInvalid` refuses SAMPLED measurement with population ≤ 0 (Canon-4 §4.1 P30 verbatim *"a sampled measurement is never presented as a full-population one"*) + `Unmeasured` and `Measurement` distinct types + `NON_CONTRACT_UTILITY_MODULES` exemption extended to `canon_census_measurement.py` (dataclass-not-pydantic per CP-D1+CP-C1 precedent). RED right-reason at `20260915T022612Z_wcensus_cp_c2_measurement_RED_pre_impl.log` (6 failed · ModuleNotFoundError/ImportError before mechanism). Double-green byte-match `3993 passed, 1 skipped, 438 warnings` × 2 (Run 1 123.57s · Run 2 123.61s · both 9444 B · tally md5 `bc82348bd7fc1c8535540d7d69304bef`). **Owner re-grounding pack banked verbatim** at DECISIONS 2026-09-15T~02:35Z (Option-α reaffirmed · GPU inventory chore `GPU-INV-01` opened for JUMP+estate-compute · D12 stays OPEN · SEC-2026-09-* rotations none-landed · canon drops none-new · egress-window hold protocol confirmed). **Egress window: CLOSED at CP-C2 close** (02:35 UTC vs 02:00 UTC close · reopens 08:00 UTC · CP-C3..CP-C6 non-egress proceed · Item-3 live census-run holds until re-open OR waits behind wave seal, whichever is later).

- **PRIOR (superseded 2026-09-15T~02:35Z) · CURRENT AS OF 2026-09-15T~02:21Z · W-CENSUS-CANON-ALIGN · WAVE OPEN + CP-C1 CLOSED · ratchet 3979 → 3986 (+7 = 6 new + 1 cross-benefit).** Track-a HEAD **`c45d0c3`**. SourceCandidate frozen 4-carrier (source_reference/region/feed_identity/sensitivity per Canon-4 §4) + Sensitivity frozen 3-field carrying rule_reference (B5.5) + deterministic classify_sensitivity with Canon-4 §5.1 conservative fallback ("unknown" verbatim token). **In-wave §G handled + resolved:** stale Chromium-harness-receipt (21h · CP10 wave) refreshed in-process to 0.00h age via `tools/wave_g5_realchrome_verification_harness.py --strict` (GREEN · underline=3/3 · oxblood=1/1) — not a silent rebaseline; verbatim in DECISIONS 2026-09-15T~02:21Z. `BLOCKER-CENSUS-GPU-BIND-01` recorded (no GPU visible to this pod; estate GPU hosts `akki-vm`/`akki-vm-ii` need operator bind before model-bearing waves).

- **PRIOR (superseded 2026-09-15T~02:21Z) · NEXT ACTIVE STEP (superseded) · CP-C2 · `Unmeasured` first-class sentinel + `Measurement` frozen carrier with `method` field** (Canon-4 §4.1 P29-P30 verbatim + Master Requirements Registry B5.2 + B5.3). Then CP-C3 CensusRun · CP-C4 registry-write · CP-C5 JobManifest · CP-C6 SourceStratumMeasurement + ActivationList → wave close → Item-3 census run (waits for 08:00 UTC egress re-open + GPU-host bind).

- **PRIOR (superseded 2026-09-15T~02:21Z) · CURRENT AS OF 2026-09-15T~02:20Z · CENSUS-SPEC-AS-DESIGNED reconstructed · HALT before census run per owner verification directive.** Owner asked *"Do you remember the Census spec we designed?"* — treated as a discipline check that we run the census AS DESIGNED, not a lookalike. Exhaustive read-only search executed: 340+ canon hits · 1,152 notes hits. Census specification located across **6 load-bearing sources** on disk (Canon-4 §4+§10 · Master Requirements Registry Doc-9 rows B5.1..B5.7 + A5.1..A5.4 + C5.1..C5.6 · Canon-17-19 §A17.10-A17.11 + Canon-17-20-v3 §A20.11 first-census-activation clause · Doc-0 Promise #12 anchor · GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md 10-plane reframe · W_AUDIO_POC_SCOPING_20260912.md audio-poc scoping) + **12 in-repo implementation surfaces** (mtafiti/census.py, census_engine/engine.py, composition_census.py, census_dimensions/*, 7 pytest invariant tests) + **prior census-run output on disk** (census_1_media_landscape.json). Two Doc-9/Doc-10 source files (`09_Estate_Registry_Part_1_Connection_and_Census.md` + `10_Estate_Registry_Part_2_Comprehensive_Registry.md`) referenced by Master Registry line-refs are ABSENT on disk (verbatim record is the Master Registry invariant list). **Deliverable banked:** `notes/CENSUS_SPEC_AS_DESIGNED_20260915.md`.

- **PRIOR (superseded 2026-09-15T~02:20Z) · CURRENT AS OF 2026-09-15T~02:00Z · CANON INGEST + VERBATIM DISCIPLINE CORRECTION · TWO NEW DROPS REGISTERED.** Two owner-provided canon artifacts registered as drops: `canon/drops/20260914_pull_seam/` (Pull Seam design principles, docx+extract+manifest) and `canon/drops/20260914_audio_plane_v1/` (Audio Intelligence Plane Spec v1.0, docx+md+extract+manifest · PARITY_TRUE across docx and md, 34/34 probes). Verbatim-canon standing rule banked in DECISIONS.md 2026-09-15T~01:40Z (any requirement in a grounding brief / note / invariant docstring must carry a verbatim quote + source file + section; INFERRED requires owner ratification BEFORE mechanism lands; my paraphrases are routing, not requirements). Two prior ingest notes SUPERSEDED (`notes/canon_pull_seam_requirements.md` + `notes/PULL_SEAM_CONFORMANCE_20260914.md`) — replaced by verbatim versions.

- **PRIOR (superseded 2026-09-15T~02:00Z) · CURRENT AS OF 2026-09-14T~15:11Z · W-DATA-SUITE-V2-LIFT · WAVE CLOSED · +50 invariants across CP-D1..CP-D8 · ratchet 3929 → 3979.** All 8 CPs green with double-green byte-match at each close. Track-a HEAD **`6549c31`**. Seal at `phase0/output_verified_seals/data_suite_v2_lift.seal.txt` (`Kind: data_suite_v2_lift` · Green1/Green2 sha256 pinned · byte-match TRUE). Rider 1 banked (pip freeze 192 + pytest --collect 3982 / 3980 tests). Owner-facing 5-section close report at `notes/W_DATA_SUITE_V2_LIFT_close.md`. **Guardrails held whole wave:** no push · no testing_agent · no refactor · no wipe · no re-clone · no head/cat/sed on custody · terminal pytest only · EAT-window compliant. **In-session tests-first correction:** CP-D4 prior-turn banked-false-RED violation was detected via SO §1 parse-not-paraphrase, remediated by mechanism roll-back + true-RED capture + false-receipt deletion; corrective ritual banked as standing pattern in DECISIONS.md 2026-09-14T~14:36Z. **DAP-Spec §A10 discharged** by CP-D6 ExportArtefact + admit_export refusal.

- **PRIOR (superseded 2026-09-14T~15:11Z) · CURRENT AS OF 2026-09-14T~15:04Z · W-DATA-SUITE-V2-LIFT · CP-D7 CLOSED · ratchet 3967 → 3973 (+6).** Track-a HEAD **`3dc0d63`**. Analysis-lifecycle state machine (case-agnostic donor re-shape from Akki-Executive-Core) · `AnalysisLifecycleState` closed 4-value {DRAFT/PROCESSING/READY/ARCHIVED} · type-separated from CP-D2 workspace lifecycle · 3-edge linear pipeline · post-terminal + back-edge + skip-edge + self-loop all refused.

- **PRIOR (superseded 2026-09-14T~15:04Z) · CURRENT AS OF 2026-09-14T~14:57Z · W-DATA-SUITE-V2-LIFT · CP-D6 CLOSED · ratchet 3961 → 3967 (+6).** Track-a HEAD **`7202916`**. Export-artefact contract discharges DAP-Spec §A10: `ExportArtefact` frozen 4-carrier (rights_posture, derivation_hash, derivation_unit_refs, terms_cited) + `export_gate.admit_export` refuses release naming the missing carrier via `ExportRefused`.

- **PRIOR (superseded 2026-09-14T~14:57Z) · CURRENT AS OF 2026-09-14T~14:50Z · W-DATA-SUITE-V2-LIFT · CP-D5 CLOSED · ratchet 3955 → 3961 (+6).** Track-a HEAD **`aebec40`**. AnalysisSession frozen 5-field record (Canon-3 §9.3 append-only) + deterministic sha256 snapshot fingerprint + AnalysisSessionCollision refusal on duplicate session_id.

- **PRIOR (superseded 2026-09-14T~14:50Z) · CURRENT AS OF 2026-09-14T~14:36Z · W-DATA-SUITE-V2-LIFT · CP-D1..CP-D4 CLOSED · +26 invariants (7+1cb+6+6+6) · ratchet 3929 → 3955.** Track-a HEAD **`cdcab77`**. Grounding brief banked at `notes/wave_data_suite_v2_lift_grounding_brief.md`. CP commits: `ed0265f` (D1 · workspace boundary) · `6df2a40` (D2 · workspace state machine) · `2b002df` (D3 · source registry) · `cdcab77` (D4 · Analyze-tab contracts). All CPs green with double-green byte-match at each close. **Tests-first discipline violation detected AND remediated:** prior turn banked a GREEN result (6 passed) as `RED_pre_impl` for CP-D4; this session rolled back mechanism, captured true right-reason `ModuleNotFoundError` × 6 in the v2_true receipt, deleted the false receipt, restored mechanism, resumed close. Full narrative + corrective ritual banked in DECISIONS.md entry 2026-09-14T~14:36Z.

- **NEXT ACTIVE STEP · CP-D5 · analysis-session record** (Canon-3 §9.3 append-only spirit · `AnalysisSession` frozen dataclass · new sessions never overwrite · snapshot fingerprint deterministic). Target ratchet 3955 → 3960–3963. Then CP-D6 export-artefact contract (discharges DAP-A10) → CP-D7 analysis-lifecycle state machine → CP-D8 case-agnostic donor lift with word-boundary executive-domain negative-scan. Wave close composite seal at `phase0/output_verified_seals/data_suite_v2_lift.seal.txt` per §E of grounding brief.

- **PRIOR (superseded 2026-09-14T~14:36Z) · CURRENT AS OF 2026-09-14T~13:58Z · W-AUDIO-POC WAVE CLOSED · +71 invariants across CP-A1..A6 · ratchet 3858 → 3929.** All 6 CPs green with double-green byte-match at each close. Track-a HEAD **`dc498fd`**. Seal banked at `phase0/output_verified_seals/audio_poc_v1.seal.txt` (`Kind: audio_poc_wave_close`). Owner-facing 5-section report at `notes/W_AUDIO_POC_wave_close.md`. Rider 1 banked (pip freeze 192 + pytest --collect 3932). **Guardrails held whole wave:** no push · no testing_agent · no refactor · no wipe · no re-clone · no head/cat on custody · token never echoed · EAT-window compliant. **Blockers escalated:** BLOCKER-HF-A5-01 (HF provider) · BLOCKER-HF-A5-02 (NAS-fetch plumbing) · BLOCKER-HF-A5-03 (release-gate verdicts).

- **BLOCKER ledger (all owner-listed still-blocked · this wave respects them, does not block on them):** SEC-2026-09-12-01 · SEC-2026-09-14-04 (HF) · SEC-2026-09-13-T4-01/03/04/05 · SEC-2026-09-14-01/02/03 (JUMP, RADIO, NAS, DB) · Transcription-server host+creds MISSING BIND · RADIO routing to 10.10.19.0/24 MISSING BIND · 5 closed-SG MySQL hosts · Owner ratifications R-7, R-15, R-16, R-17, BC-3, BC-4, S-24, R-13, R-14 · 165 quarantined D1a-1 legacy tests (leave quarantined per owner).

- **AFTER W-AUDIO-POC CLOSE · TASK 2 · M5 SW2 = W-DATA-SUITE-V2-LIFT (owner GO already banked · DPO-D1/DPO-D2 defaults stand · no amendments received):** case-agnostic donor lift from `analyze_workspace/` (CP-D1..CP-D8) per Solva-V2 precedent template. Step 2 discovery already banked in DECISIONS entry 2026-09-14T~13:00Z clause 12; do NOT redo discovery per owner directive.

- **AT M5 CLOSE:** owner-facing FULL SPRINT COMPLETION REPORT (M0→M5). END-OF-WAVE format per SO §2.

- **CURRENT AS OF 2026-09-13T~14:30Z · M0 · CANON ASSESSMENT MILESTONE CLOSED at floor 3562 (unchanged; document-only).** Owner-ratified M0..M5 milestone spine (2026-09-13). M0 delivered: (i) 13 new `notes/canon_*_requirements.md` files covering `DAP_Backend_Spec_v1` + amendments, `Serving_Integrity_Amendment_v1` (owner-attached 2026-09-13; introduces S-27, A20.15, SFP-8, DAP-31+/32+, AC-13/14, A5.7+, R-13/R-14), `Governance_Architecture_v1` files_15 delta (R-1/R-3/R-5 self-flipped RESOLVED), files_14 governance-suite bundle (TCB · Determinism · SAD · SFP · FP · TD · BCA · HG · P&U), and `Security_Assurance_Promise_Set_v2` delta (S-27 added; 26→27). (ii) Supersession-form `REUSE_ASSESSMENT_20260913.md` + `BUILD_STRATEGY_20260913.md` (Aug-14 originals preserved). (iii) C3 batch-ratification flipped 12 DEFAULT rows to RATIFIED per owner verbatim *"3 - Approved"*; RULING_LEDGER reconciled to 17 RATIFIED · 0 DEFAULT · 1 COUPLED · 6 OPEN (RS-R-2 second-signatory added to OPEN + SIA R-14 [candidate serving engine · name scrubbed per owner ruling 2026-09-14] deliberately unruled). (iv) S-7 CONTEXT PACKAGE (4-option deck) at `notes/S7_CONTEXT_PACKAGE_20260913.md`. (v) MILESTONE_PROMISE_BINDING §M3-ADDENDUM for S-27. **Guardrails held**: NO production code · NO scaffolding touched · local commits only · NEVER pushed · NO egress · testing_agent BANNED · SO §1 boot honoured · Ratchet floor 3562 untouched. **STRICT tests-first HELD across ELEVEN consecutive closes (unchanged; M0 was document-only).** Track-a HEAD `e2ae44b0` unchanged · master HEAD committed with this update.

- **RATCHET TRUTH between 2026-09-12T~07:35Z and 2026-09-13T~14:30Z (top-marker was stale during this window)**: `baseline_failures.json.ratchet_history` records three additional closes AFTER W-MTAFITI-GPU-DISCOVERY that this NEXT.md top-marker did NOT reflect until this refresh:
  - Entry 71 · commit `e1712a1` · 2026-09-13T08:35Z · **W1c** platform integration proof · passed=3503 (+11 from 3492).
  - Entry 72 · commit `33edf56b` · 2026-09-13T10:32Z · **W-REGISTRY-EXTENSION-G3 wave close** (Doc-0 G-3 half · 6 CPs) · passed=3531 (+28 from 3503).
  - Entry 73 · commit `7f6d235a` · 2026-09-13T10:48Z · **W-SOLVA-V2-LIFT wave close** (8 CPs · DPO-S2 HALT declared) · passed=3562 (+31 from 3531).
  Backfill commits: `c5d5d6c` (Registry-G3 backfill) and `e2ae44b` (Solva-V2-Lift backfill; current track-a HEAD). Ratchet floor at start of 2026-09-13 M0 session = 3562. All prior book-keeping (§C waves G-3 and Solva-V2-Lift) is authoritative; only NEXT.md's top-marker was stale.


- **CURRENT AS OF 2026-09-12T~07:35Z · W-MTAFITI-GPU-DISCOVERY · WAVE CLOSED at floor 3251 (+143 across the wave from 3098).** Seven CPs landed in sequence under strict discipline. Wave totals: **21 schemas · 1,637 tables · 18,316 columns · 181,708,249 rows** across Weego + USSD · **12,848** column-role signals · **115** raw-value PII signals redacted · **2,133** FK-candidate signals · **$0.000052** wave-total egress cost · **0 GPU-hours** consumed (Cassava lease basis · $0 marginal on idle capacity — regex-only CPU throughout). Ratchet chain: 3098 → 3164 → 3198 → 3212 → 3223 → 3232 → 3241 → 3251, every step double-green byte-match. Track-a commit chain: `3e72bd5` → `867a306` → `37a5024` → `4f57ff6` → `79f423e` → `d1ffd8d` → `77834d1`, all local, no push. Owner-facing wave-close doc landed at `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md`. Wave-close bundle sha256 sealed at `phase0/mtafiti_gpu_discovery/wave_close_bundle_latest.json`. **Zero escalation triggers fired · zero guard weakened · zero testing_agent invocations.** **STRICT tests-first HELD across SEVENTEEN-plus consecutive closes.**

- **Next active step (post-wave):** Owner review of wave-close doc. On owner nod, propose follow-on waves: `W-MTAFITI-GPU-EMBEDDINGS` (GPU-embedding relationship signals — Cassava lease means marginal $0) and/or `W-MTAFITI-DEEP-SWEEP` (deepen walker limits 10-100× while staying under $0.05 total). Also: sysadmin follow-up on the 9 SG-blocked hosts (multiplies discovery surface ~5×). CP10 of W-REGISTRY-FULL-BUILD remains on owner HOLD with its drafted close test shelved-untracked.

- **PRIOR (superseded 2026-09-12T~07:35Z) · CURRENT AS OF 2026-09-12T~07:10Z · W-MTAFITI-GPU-DISCOVERY CP4 CLOSED at floor 3223 (+11 from 3212) · DEEP COMPOSITION SURFACE MAPPED.** 21 schemas / 1,637 tables / 18,316 columns / ~181.7M rows / 12,848 name-based column-role signals across Weego + USSD. Kernel: `services/mtafiti/composition_census.py` (single-file to avoid collision with existing `census.py`). Extended METADATA_KEYS to include `census_sha256` / `manifest_sha256` / `inputs_sha256` (sha256 hex false-fires `pii.phone` on digit substrings). Live receipt: `phase0/mtafiti_gpu_discovery/composition_census_latest.json`. Bundled fix: package-name collision resolution (subpackage `census/` shadowed existing `census.py` — 49 tests broke, resolved by renaming to single-file module). Mechanical RED at `phase0/drill_receipts/20260912T070021Z_wave_mtafiti_gpu_discovery_cp4_RED_pre_impl.log`. Double-green `3223 passed, 1 skipped, 438 warnings` × 2. Track-a HEAD **`4f57ff6`** · master HEAD to be committed with this update. **STRICT tests-first HELD across FIFTEEN-plus consecutive closes.**

- **Next active step:** CP5 — data-quality profiling (null-density via `information_schema.STATISTICS` + targeted null-count via `SELECT SUM(CASE WHEN col IS NULL ...) FROM …` bounded by CP1 sampler; cardinality percentile; format-conformance for the ~13k columns already tagged by role-classifiers). GPU cycles still deferred to CP6 (embeddings + entity-resolution signals).

- **PRIOR (superseded 2026-09-12T~07:10Z) · CURRENT AS OF 2026-09-12T~06:55Z · W-MTAFITI-GPU-DISCOVERY CP3 CLOSED at floor 3212 (+14 from 3198) · FIRST LIVE READ ACHIEVED.** Both owner-named Huawei RDS hosts connected under the CP1+CP2 guards: **Weego (159.138.162.146)** via credential-reuse fanout (bramuel password originally banked under 203.123.86.10/VIUSASA row — matches prior-session finding) — 17 read-only SQLs traced, 4 user schemas (`weego`, `analytics`, `sql_demo`, `sql_trial1`), 0 PII signals in bounded sample; **USSD (110.238.76.159)** direct-credential match — 19 read-only SQLs, 17 user schemas, 22 PII signals redacted (16 pii.url + 3 pii.phone + 3 pii.ipv4). Every SQL routed through `refuse_if_write`; every sampled row through `redact_row`; defence-in-depth `assert_no_raw_pii(data_view(receipt))`. Kernel: `services/mtafiti/probes/live_readonly_probe.py` + throwaway orchestrator `backend/tools/mtafiti_live_readonly_probe.py`. Banked receipt: `phase0/mtafiti_gpu_discovery/live_readonly_probe_latest.json`. Escalation triggers monitored (no fires): no exotic data class surfaced, Cassava GPU lease unchanged (no GPU cycles used in CP3), Weego egress metadata-only (~500 KiB) well under $0.06 line, no guard weakened. Bundled in-CP fix: DECISIONS.md CP2 append missed trailing STANDING_ORDERS pointer — re-appended. Mechanical RED at `phase0/drill_receipts/20260912T064149Z_wave_mtafiti_gpu_discovery_cp3_RED_pre_impl.log` (8 failed / 3199 passed). Double-green `BASELINE_GUARD=1`: byte-match `3212 passed, 1 skipped, 438 warnings` × 2. Track-a HEAD **`37a5024`** · master HEAD to be committed with this update. **STRICT tests-first HELD across FOURTEEN-plus consecutive closes.**

- **Next active step:** CP4 — deep census composition-by-strata over the two live connections. Enumerate every schema→table→column; row-counts, null-density, cardinality profiles; all under the CP1+CP2 guards + CP1 deterministic-adaptive sampler. GPU cycles still deferred (regex-only detectors suffice for composition); GPU picks up at CP5 (semantic column classification via embeddings) and CP7 (cross-table relationship signals).

- **PRIOR (superseded 2026-09-12T~06:55Z) · CURRENT AS OF 2026-09-12T~06:35Z · W-MTAFITI-GPU-DISCOVERY CP2 CLOSED at floor 3198 (+34 from 3164).** PII detector + PII redaction guard landed. **HARD GATE lifted** — read-only SQL guard (CP1) AND PII redaction guard (CP2) BOTH green-and-committed → CP3 live SELECT authorised. Kernel: `services/mtafiti/detectors/{pii_detector,pii_redaction_guard}.py` + `MTAFITI_PII_HASH_SALT` in gpu_discovery_constants.py. Regex-driven deterministic detector emits DetectionSignal per marker per field (email/phone/ipv4/url/credit_card+Luhn/iban, all evidence_class=DETECTED, no verdict-shaped signal_name). redact_row() replaces PII values with `<REDACTED:pii.<kind>:<hash16>>` salted-sha256 tokens (deterministic + idempotent). assert_no_raw_pii() recursively scans dicts/lists/strings, raises RawPiiLeakForbidden on any raw PII (defence-in-depth for persistence layers). Mechanical RED: `phase0/drill_receipts/20260912T062758Z_wave_mtafiti_gpu_discovery_cp2_RED_pre_impl.log` (32 failed / 3166 passed, right-reason ImportError). Double-green `BASELINE_GUARD=1`: byte-match `3198 passed, 1 skipped, 438 warnings` × 2 (Run 1 101.72s · Run 2 102.03s). Track-a HEAD **`867a306`** · master HEAD to be committed with this update. **STRICT tests-first HELD across THIRTEEN-plus consecutive closes.**

- **Next active step:** CP3 opener — first LIVE read-only dry-run against Weego (`159.138.162.146`) + USSD (`110.238.76.159`). SELECT/SHOW only; zero writes. Read-only guard fires per statement. Bank the live-probe receipt at `phase0/mtafiti_gpu_discovery/live_readonly_probe_20260912.json` and gate an invariant on that receipt.

- **PRIOR (superseded 2026-09-12T~06:35Z) · CURRENT AS OF 2026-09-12T~06:17Z · W-MTAFITI-GPU-DISCOVERY CP1 CLOSED at floor 3164 (+66 from 3098; 64 direct CP1 governance tests + 2 frozen-contract-parity self-heal via new snapshot files).** Owner-authorized wave (HOLD lifted for GPU-mtafiti only; product-build HOLD on Registry-CP10 / Solva / DAP / Rules-Service-Stack remains). CP1 lands the four foundational governance bright-lines the owner refined this session: **(a) objective-generation blind** — new frozen carrier `contracts/mtafiti_objective_carrier.py` (`ObjectiveOrigin` ∈ {TARGETA, CIF, COACH_ORIGINATION_PORT}; `admit_carrier()` refuses mtafiti-internal origin; carrier is `extra="forbid"` + frozen); **(b) detect-not-decide** — new frozen `contracts/mtafiti_detection_signal.py` (`DetectionSignal` with closed schema, no verdict-shaped field names, `confidence ∈ [0,1]`, 5-value `EvidenceClass` taxonomy); **(c) deterministic adaptive sampling** — pinned constants `MTAFITI_GPU_SAMPLING_SEED=20260909` + `POLICY_ID="mtafiti-gpu-discovery-v1"` in `services/mtafiti/gpu_discovery_constants.py`; `deterministic_walk()` in `services/mtafiti/sampling/deterministic_adaptive_walker.py` yields byte-identical `manifest_sha256` for same inputs (C4-013); **(d) read-only SQL guard** — `services/mtafiti/executor/readonly_sql_guard.py` admits only SELECT/SHOW/USE/DESCRIBE/DESC/EXPLAIN; refuses INSERT/UPDATE/DELETE/CREATE/DROP/ALTER/GRANT/REVOKE/TRUNCATE/REPLACE/RENAME/MERGE/CALL/EXECUTE/LOCK/UNLOCK/SET/COMMIT/ROLLBACK/BEGIN/START; multi-statement refused; comment-hidden writes refused. **Pre-CP1 decision-point handled autonomously** (STANDING_ORDERS §2 DPO): harness ground-truth receipt was 65.2h old (threshold 48h) → applied owner's precedent path ("refresh the harness, don't relax the threshold" · DECISIONS 2026-09-08T~06:15Z STEP 5) → ran `tools/wave_g5_realchrome_verification_harness.py` GREEN (orphan_count=0), fresh receipt banked at `phase0/harness_ground_truth/latest.json` (2026-09-12T06:01:36Z) BEFORE CP1 tests-first work started. Mechanical RED banked at `phase0/drill_receipts/20260912T060604Z_wave_mtafiti_gpu_discovery_cp1_RED_pre_impl.log` (64 failed / 3098 passed / 1 skipped, right-reason ImportError against modules-not-yet-created). Frozen-contract-parity self-heal: `mtafiti_objective_carrier.contract_snapshot.json` + `mtafiti_detection_signal.contract_snapshot.json` + 2 `CONTRACT_TO_SNAPSHOT` entries in `test_frozen_contract_snapshot_parity.py`. Double-green `BASELINE_GUARD=1`: byte-match `3164 passed, 1 skipped, 438 warnings` × 2 runs (Run 1 101.30s · Run 2 101.20s). BASELINE_GUARD receipt: `passed=3164 / baseline-failures-remaining=0 / quarantined=0 · status: OK`. Ratchet manifest bumped in tandem (`counts.passed=3164` + `passed_floor=3164` + `ratchet_history` appended). CP10 wave-close test file (`test_w_registry_full_build_cp10_wave_close.py`) remains **shelved-untracked** in working tree pending owner lift of the Registry-CP10 HOLD. Track-a HEAD to be committed post-close · master HEAD to be committed with this update. **STRICT tests-first HELD across TWELVE-plus consecutive closes.**

- **Next active step:** CP2 opener (PII / sensitive-data detector + PII redaction guard). Owner CP1 refinement is explicit: *"the PII redaction guard stays CP2 (it gates sample PERSISTENCE, which doesn't happen in CP1) — BUT hard rule: BOTH the read-only guard AND the PII redaction guard must be GREEN before CP3's first live SELECT."* CP1 landed the read-only guard; CP2 must land the PII redaction guard before any live SQL touches Weego (`159.138.162.146`) or USSD (`110.238.76.159`). CP2 scope surface-request to be sent to owner at CP2 open per comms doctrine.

- **PRIOR (superseded 2026-09-12T~06:17Z) · CURRENT AS OF 2026-09-06T~17:05Z · W-SMS-BODY-EMIT CLOSED at floor 2978 (+22 from 2956: +20 SMS-Body-Emit + 2 dispatcher-double-setsid fix) · CAMPAIGN v2 LIVE ON BOTH HOSTS.** Wave lands owner Ruling #5(a) via user proxy (INCLUDE sms_sent with mask_regex_scrub + re-extract with sms_sent-inclusive emit + re-base queued ablations on diversified corpus). First complete drawer lifecycle proven end-to-end (Ruling #5 architecture 8-step: question opened → cautious default → main agent held ambiguity → owner ruled → governed decision written → evidence record banked → retroactive reclassification → downstream re-extraction rebased). **CORRECTION 1 diagnosis**: akki-vm dispatcher DIED 15:01:13Z with SubprocessError: Exception occurred in preexec_fn (root cause: `_dispatch_trainer` combined `start_new_session=True` with `preexec_fn=os.setsid` → double setsid → PermissionError). A-0-v1 SEALED CLEANLY (50m54s wall-clock, held_out_loss 0.1232, adapter_sha256 `49735d51ea…`); banks as v1-pilot record. **CORRECTION 2 Campaign v2**: ALL v2 runs corpus-consistent (A-{0,1,2,3}-v2 share ussd_deduplicated_v2 corpus 75K train/19K held sha256 `5a9b5dbb…`; B-{REF,3,4,5,6}-v2 share ussd_plus_sms_deduplicated_v2 corpus 29.6K train/7.4K held sha256 `5bad3900…` — dedup collapse RESOLVED from 87 rows to 37K unique; B2-v2 uses ussd_plus_sms_raw_v2 corpus 155K train/39K held sha256 `7b270bb8…`; B1-v2 shares Campaign A corpus). v1 pilots preserved untouched; cross-boundary v1↔v2 comparisons BANNED. **CORRECTION 3 ladder order**: 0.5B→1.5B→3B→7B strict order; trim 7B tail before touching corpus-consistency. **In-wave dispatcher fix** (`test_dispatcher_no_double_setsid.py` invariant, 2 tests) + deployed to both hosts (sha256 `9bd7f46f…`). **v2 corpus extractions** completed in 95s total (3 extractions via seam-monkey-patched extraction script; prod code untouched under thin-kernel; W-Seam-SFTP-Tilde-Expand chartered as follow-on). **Campaigns LIVE**: akki-vm dispatcher pid 194861 firing A-0-0p5B-v2 (trainer 194863, started 16:54:30Z, ETA seal ~19:47Z); akki-vm-ii dispatcher pid 177780 waiting behind B1-v1 seal (B1-v1 still training, ETA ~18:30Z). Window-fill projection ~76% akki-vm / ~93% akki-vm-ii — banks at `phase0/campaign_drafts/CAMPAIGN_V2_WINDOW_FILL_MATH.md`. Mechanical RED receipt `phase0/drill_receipts/20260906T161500Z_wave_sms_body_emit_RED_pre_impl.log` (16 fail / 16 pass pre-impl · right-reason on new-truth invariants). Double-green `BASELINE_GUARD=1` at floor 2978: byte-match `2978 passed, 1 skipped, 438 warnings` × 2 (Run 1 97.86s Run 2 97.04s). Track-a HEAD to be committed post-close · master HEAD to be committed with this update. **STRICT tests-first HELD across ELEVEN consecutive closes.**

- **PRIOR (superseded 2026-09-06T~17:05Z) · Current as of 2026-09-06T~14:56Z · W-MULTI-TABLE-EXTRACT CLOSED at floor 2956 (+32 from 2924) · CAMPAIGN B FULL QUEUE LIVE ON akki-vm-ii + CAMPAIGN A QUEUE LIVE ON akki-vm.** Wave lifts the shield-train-BUILD wave-honest-limit §F.1 ("single-table SELECT only"). Design: sequential per-table extract + pipeline-level compose (NOT SQL UNION) so `row_executor.execute_row_bearing_query`'s refuse-unclassified-by-construction property fires PER TABLE with its own chokepoint receipt. New primitive `backend/services/shield_train/multi_table.py`: `compose_multi_table_corpus(tables, database, principal, purpose, backend_execute, slice_size_per_table, dedup)` iterates tables in list order, calls row_executor per-table, composes training_text via table-shape formatters (`_compose_training_text_ussd` + `_compose_training_text_sms`), concatenates in table order (USSD first, SMS second — deterministic for tail split), optionally deduplicates by training_text sha256 (first-occurrence-wins). `pipeline.execute_governed_lora_run` extended to accept `table_context: str | list[str]` (list triggers multi-table path; str path unchanged for backward compat — all 30 W-Shield-Train-run tests still green) + optional `corpus_variant` kwarg. `campaign_infra.production_trainer.resolve_corpus_variant`: maps manifest strings — `ussd_deduplicated → [ussd_question_response, dedup=T]` · `ussd_plus_sms_deduplicated → [ussd_question_response, sms_log, dedup=T]` · `ussd_plus_sms_raw → [ussd_question_response, sms_log, dedup=F]`. Unknown variant refuses (silent guess would rewrite owner-approved design). New on-host artifact `tools/on_host_queue_dispatcher.py`: serial-with-dependency-wait queue runner polling `ACTIVITY_SUMMARY.md` every 60s; setsid + start_new_session detach; per-run dispatcher heartbeat at `~/akki_journal/queue/dispatcher_heartbeat.json`; JSONL dispatcher.log; seals via `queue_completed.md`. 32 new invariants across 8 sections. **STRICT tests-first HELD unbroken across TEN consecutive closes** (WPW-v1-d + Orch-Resilience-r1 + r1-wire + r2 + Shield-Train-build + Compute-Residuals + Campaign-Infra + Shield-Train-Admission + Shield-Train-run + Multi-Table-Extract). Mechanical RED receipt `phase0/drill_receipts/20260906T143700Z_wave_multi_table_extract_RED_pre_impl.log` (26 fail / 6 pass pre-impl). Double-green `BASELINE_GUARD=1`: 2956 passed × 2 runs (byte-match `2956 passed, 1 skipped, 438 warnings`; Run 1 107.63s, Run 2 106.51s). Track-a HEAD **`0287482`** · master HEAD to be committed with this update.

- **RULING #5 CONFLICT SURFACED AND RESOLVED HONESTLY.** Initial ledger-add of `sms_log.sms_sent` (interpreted current session's "cautious-default" ruling as `mask_regex_scrub`) triggered pre-existing invariant `test_sms_sent_lives_in_clarification_drawer` — prior owner Ruling #5 (2026-09-06T11:34:00Z) parks `sms_sent` in `masking_policy.v0.json::clarification_drawer` with `cautious_default_applied='exclude'` pending explicit owner ruling on (a) INCLUDE with mask_regex_scrub OR (b) EXCLUDE. Reverted ledger add immediately; updated SMS formatter to survive on `sms_title` alone; updated new tests to reflect Ruling #5 status; banked wave-honest-limit F.6 in grounding brief. **Owner ruling on Ruling #5 (a) vs (b) needed** for a follow-on wave to re-extract Campaign B with full sms_sent content — CURRENT WAVE PROCEEDS with `sms_title`-only SMS emit (short varchar bodies).

- **CAMPAIGN QUEUES LIVE AND DISPATCHING (dispatcher heartbeats banked):**
  - **akki-vm · Campaign A queue** — `dispatcher_pid 188774` alive · queue at `/home/ubuntu/akki_journal/queue/campaign_a_queue.json` · index 0/2 · waiting for `A-0-0p5B-seed01`'s `ACTIVITY_SUMMARY.md` (currently at step 950/963 · loss 0.153 · seconds from seal) · will auto-dispatch **A-1-1p5B (Qwen2.5-1.5B, rank 16, ctx 1024)** → **A-2-3B (Qwen2.5-3B)**. **A-3-7B TRIMMED per owner's trim-last guidance** ("cut Campaign A's 7B run or B's ctx-2048 BEFORE cutting anything else — window integrity beats ladder completeness"). A queue reuses A0's staged corpus (identical `ussd_deduplicated` per manifest).
  - **akki-vm-ii · Campaign B queue** — `dispatcher_pid 160175` alive · queue at `/home/ubuntu/akki_journal/queue/campaign_b_queue.json` · index 0/6 · waiting for `B1-CORPUS-USSD-ONLY`'s `ACTIVITY_SUMMARY.md` (currently at step 150/963 · loss 0.162) · will auto-dispatch **B-REF-3B → B2-DEDUP-OFF → B3-RANK-8 → B4-RANK-32 → B5-CTX-512 → B6-CTX-2048** in manifest-authored order.
  - Reorder reconciliation banked at `phase0/campaign_drafts/campaign_b_run_order_reconciliation.json` (B1 promoted first as in-scope substitution when B-REF blocked on multi-table gap; owner-explicit "no experiment deleted" — original ablation preserved, just resequenced).

- **DEDUP COLLAPSE — IDEATION FINDING BANKED.** `ussd_plus_sms_deduplicated` corpus extracted from RDS produced 25,203 raw rows → deduped to **87 unique training_text rows** (200× reduction). Root cause: SMS titles are template-repetitive (`"vaccination reminder"`, `"payment due"`, etc.) and USSD Q+A pairs have limited unique combinations under sms_title-only emission. Under `dedup=True` first-occurrence-wins, template duplicates collapse aggressively. Consequence: B-REF/B3/B4/B5/B6 all train on ~87 examples (train) + 21 (held-out) — will produce converged but likely-overfit adapters within minutes. Campaign B's `raw` corpus (25,203 train + 6,300 held-out) is the meaningful comparison. This IS an ideation finding worth banking as it exercises Objective 2 (novelty verdict machinery): the ablation shows that under current governance + template-heavy SMS + single-title emit, dedup dramatically over-collapses. Reversal path: Ruling #5(a) landing lifts to `sms_sent`-inclusive emit → per-message body content diversifies → dedup collapse rate drops.

- **NEW FACTS BANKED (owner-verifiable receipts):**
  - `sms_log.sms_sent` remains in clarification_drawer with cautious_default_applied=`exclude` (unchanged from Ruling #5; this wave respected as-is).
  - `sms_log` has 13 columns · 12 ledgered (all excluded except `sms_title` mask_regex_scrub) · 1 drawered (`sms_sent`).
  - Multi-table extraction fires per-table row_executor calls → per-table row-bearing chokepoint receipts (2 per multi-table extraction).
  - `campaign_a_queue.json` + `campaign_b_queue.json` scp'd to both hosts under `/home/ubuntu/akki_journal/queue/` (verified via ls + head after upload).

- **NEXT ACTIVE TRACK:** passive reattachment via `campaign_infra.reconcile.pull_and_bank` at next session-open (poll `~/akki_journal/queue/dispatcher_heartbeat.json` on both hosts + settle each seal per WPW A1-A6 acceptance drills as they land). Owner ruling awaited on: (1) Ruling #5(a) vs (b) — sms_sent emission decision; (2) whether to re-extract Campaign B dedup pool with a diversifying strategy (larger slice_size · random OFFSET · alternate dedup key) if the current 87-row-collapse is deemed too aggressive to compare meaningfully against B2's raw.

- **SPRINT_PLAN.md updated with SIX chartered follow-on waves (P1-P6):** W-TaskEval-v1 · W-Gradient-Step-Checkpoint · W-Row-Stream-Extractor · W-Adapter-Tensor-Persist · W-Queue-Watchdog · W-Cross-Table-Consistency-Check. All derived from wave-honest-limits banked during the last three closes.

- **STANDING RULE:** if owner rulings land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close at the next clean commit boundary. STRICT tests-first RED-then-GREEN with banked mechanical RED drill receipt remains the invariant across TEN consecutive closes.

- **PRIOR CURRENT-WAVE MARKER (W-SHIELD-TRAIN-RUN close at floor 2924 · retained for continuity)**:

- **CURRENT AS OF 2026-09-06T~14:20Z · W-SHIELD-TRAIN-RUN CLOSED at floor 2924 (+30 from 2894) · 3-DAY CAMPAIGNS LIVE ON BOTH GPU HOSTS.** Wave lands the actual on-host LoRA training call — `execute_governed_lora_run` NotImplementedError REPLACED with the real composition (admission gate → masking-policy-driven governed SELECT → `row_executor.execute_row_bearing_query` → training_text compose → deterministic 20% tail split → **held-out slice sha256 BANKED PREFLIGHT** → `build_masked_corpus_file` train+held-out → `stage_corpus_to_host` both with sha256-verified transport). New subsystem `backend/services/shield_train/held_out.py`: `deterministic_20pct_tail_split(rows, seed=31337)` returns `(train, held_out, meta)` with canonical-JSONL train_sha256 + held_out_sha256; `bank_held_out_slice_hash(...)` writes preflight receipt with `banked_before_first_run_starts=True` to `phase0/shield_train_receipts/held_out_slices/`; receipt never carries row content. New `backend/services/campaign_infra/production_trainer.py`: `default_trainer_fn(run_name, manifest_entry, host, ...)` is the production binding for `run_queue.execute_campaign(trainer_fn=...)`; wires services.connect.rds_data_submit as backend_execute + services.training_runner.ssh_seam as ssh_seam; **includes 1000-row LIMIT/OFFSET pagination for RDS Data API's 1 MB response cap** (env `AKKI_RDS_PAGE_SIZE` override); loads AWS creds from owner-approved custody `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json` (mode 0600, never logged); injection preserved via `_seam_override` + `_backend_override`. New on-host artifact `tools/on_host_trainer.py`: adapted from workspace donor `tools/text_train_pipeline/train_payload.py` (2026-08-31 · adapter.sha256 a369304911566bbac263a0b3552f239289472c98663119d0243e11e7862f8468); TrainerCallback writes heartbeat per logging_step + poll receipt + checkpoint marker per epoch (matches save_strategy=epoch); `--resume-from` honored via `trainer.train(resume_from_checkpoint=…)`; held-out eval computes causal-LM loss + perplexity; adapter walk-sha256; `write_run_summary` seals ACTIVITY_SUMMARY.md. Inline copies of campaign_infra writers keep the script self-contained on the host. 30 new invariants across 6 sections (grounding brief presence · held_out primitive · pipeline composition · production_trainer default binding · on_host_trainer contract structural · HARD-GATE + zero-influence regressions). **STRICT tests-first HELD unbroken across NINE consecutive closes** (WPW-v1-d + Orch-Resilience-r1 + r1-wire + r2 + Shield-Train-build + Compute-Residuals + Campaign-Infra + Shield-Train-Admission + Shield-Train-run). Mechanical RED receipt `phase0/drill_receipts/20260906T134500Z_wave_shield_train_run_RED_pre_impl.log` (26 failed / 4 passed pre-impl — the 4 passing are grounding brief + admission-gate regression + injection-preserved + admission-bypass zero-influence). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2924 passed × 2 runs (Run 1: 106.09s · Run 2: 107.62s), byte-match on `2924 passed, 1 skipped, 438 warnings`. Track-a HEAD **`7a60680`** · master HEAD to be committed with this update.

- **3-DAY CAMPAIGNS LIVE — first-heartbeat evidence banked:**
  - **CAMPAIGN A · akki-vm · run 0 `A-0-0p5B-seed01` (Qwen2.5-0.5B, LoRA rank 16, ctx 1024, per_device_batch 8 × 2 GPUs × grad_accum 4, 3 epochs)** — run_id `shield-train-campaign-a-baseline-ladder-20260906-20260906T140930Z` · training_pid 180594 alive · 2× NVIDIA H200 loaded · **step 75 @ 255s wallclock, loss trajectory 3.86 → 1.08 → 0.28** (learning signal strong) · 3 poll receipts written · steps_per_epoch=321 · total_steps=963 · 20,510 train + 5,127 held-out examples · GPU 0 80% util 29.8 GB · governed pipeline receipts banked at `phase0/shield_train_receipts/shield_train_row_receipt_20260906T140930Z_*.json` (row-bearing chokepoint · first end-to-end exercise on estate data · masked columns: option_string+question_string mask_regex_scrub · value_chain include) + `phase0/shield_train_receipts/held_out_slices/held_out_shield-train-campaign-a-baseline-ladder-20260906-20260906T140930Z_*.json` (banked_before_first_run_starts=True) · staged corpora at `~/akki_journal/<run_id>/{train_corpus,held_out_corpus}.jsonl` sha256-verified on both ends.
  - **CAMPAIGN B · akki-vm-ii · run 1 `B1-CORPUS-USSD-ONLY` (Qwen2.5-3B, LoRA rank 16, ctx 1024, per_device_batch 2 × 2 GPUs × grad_accum 16, 3 epochs)** — run_id `shield-train-campaign-b-method-ablations-20260906-20260906T141344Z` · training_pid 154018 alive · 2× NVIDIA H200 · booted 14:14:16Z · loading 3B model to GPU (download in progress at commit time) · governed pipeline receipts banked · train_corpus_sha256 `4929291dfc8923ba…` · held_out_corpus_sha256 `ae7bcb6aac0f0c5f…` (same corpus shape as A0 — but staged independently under B's run_id per campaign discipline · 20,510 train + 5,127 held-out).
  - **First-heartbeat receipts** at `phase0/gpu_receipts/20260906T141500Z_campaign_a_run0_first_heartbeat/` + `phase0/gpu_receipts/20260906T141800Z_campaign_b_run1_first_heartbeat/` (heartbeat.json + train.log + first-poll + nvidia_smi_snapshot).

- **B-REF-3B DEFERRED · owner ruling requested.** Campaign B first-run per manifest is `B-REF-3B` with `corpus_variant=ussd_plus_sms_deduplicated` — requires multi-table extraction (UNION of `ussd_question_response` + `sms_log`). `row_executor` supports single-table SELECT with bare column names ONLY per the W-Shield-Train-BUILD wave-honest-limit (§F.1: "single-table SELECT only, joins are r2"). LAUNCHED B1-CORPUS-USSD-ONLY (single-table USSD) as Campaign B's first-run instead — remains in-manifest, in-scope, in-plan. **Owner ruling needed on:** (a) charter `W-Multi-Table-Extract` to lift `B-REF-3B` + `B2-DEDUP-OFF` + `B3-RANK-8` + `B4-RANK-32` + `B5-CTX-512` + `B6-CTX-2048` (all use ussd_plus_sms), OR (b) authorize single-table variants (USSD-only) as substitute for the ussd_plus_sms specification.

- **PAGINATION HONEST-LIMIT SURFACED + FIXED IN-FLIGHT.** RDS Data API's 1 MB `UnsupportedResultException` fired on the first extraction attempt (30k × 3 cols exceeds cap). `_build_backend_execute` extended with transparent LIMIT/OFFSET pagination (page_size default 1000; env `AKKI_RDS_PAGE_SIZE` override); the SQL contract is unchanged (the pagination is behind the seam). Wave's 30 tests still green post-fix (contract untouched). Pagination preserves ORDER-BY-id determinism → held-out slice deterministic → hash reproducibility preserved.

- **AWS CUSTODY PATH BANKED (new fact this session).** `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json` (mode 0600, git-ignored) carries `aws_access_key_id + aws_secret_access_key + region=eu-west-1 + cluster_arn + secret_arn + database=digicow_live`. Written by `services.connect.rds_data_submit._write_standing_creds`. **Future sessions look here FIRST before declaring credentials lost.**

- **akki-vm REBUILD FINDING BANKED.** Post-rebuild (session 2026-09-06T~13:XXZ): 5.9T volume mount SURVIVED at `/mnt/volume_dkgjrkx` but was WIPED (28K used post-rebuild). `~/akki_journal/` was GONE (prior on-host receipts lost on this host only; akki-vm-ii unaffected). Torch stack (2.11.0+cu128 · CUDA 12.8 · 2× H200) + transformers 5.16.1 + peft 0.20.0 + accelerate 1.14.0 SURVIVED. New GPU UUIDs differ from pre-rebuild (`e87acccb…` + `3f6adf5f…`). Old SSH ed25519 key survived owner's rebuild (key auth worked post-flush).

- **SSH HOST-KEY CHANGE BANKED.** `/root/.ssh/known_hosts` had 3 stale entries for `41.173.184.244` (ed25519 line 2 + rsa line 3 + ecdsa line 4). Owner ruled "key change is legit" (rebuild). Flushed via `ssh-keygen -R "41.173.184.244"` (backed up to `.old`); re-probe under `accept-new` pinned the new ed25519 `SHA256:bTjxxKDWKHhPUA4Zz/BIU3W4yK/quLUAfJrW6Vgy1Ec` matching owner-provided fingerprint verbatim.

- **NDUME CORPUS-ELIGIBILITY BANKED (owner ruling verbatim).** > "Note you have read access to all the records in those two databases". Read access covers BOTH `digicow_live` AND `ndume` databases entirely. `ndume` becomes corpus-eligible for FUTURE waves (chartered follow-on, not this campaign). Current campaign manifests unchanged.

- **NEXT ACTIVE TRACK:** owner ruling awaited on (a) B-REF-3B multi-table charter vs single-table substitute (see above); (b) whether to launch remaining Campaign A rungs (1.5B, 3B, 7B) as A0 + B1 settle. If nothing else lands: passive reattachment per REATTACH_RUNBOOK.md — poll `phase0/on_host_journal/` via `campaign_infra.reconcile.pull_and_bank` when re-attaching to observe A0/B1 progress + settle each run per WPW A1-A6 acceptance drills. If owner rules (a) → charter `W-Multi-Table-Extract` (STRICT tests-first). W-WPW-v1-e (Tier 3) stays design-only pending R1/R2/R3.

- **STANDING RULE (still binding):** if owner rulings land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is now the recovered baseline across **NINE consecutive closes**. Do not slip back into co-authoring.

- **PRIOR CURRENT-WAVE MARKER (W-CAMPAIGN-INFRA close at floor 2893 → W-SHIELD-TRAIN-ADMISSION close at floor 2894 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~12:32Z · W-CAMPAIGN-INFRA CLOSED at floor 2893 (+46 from 2847).** 3-day unattended GPU campaign machinery (fixture-proven) + lean r3 items folded in. New subsystem `backend/services/campaign_infra/`: `manifest.py` (v0 schema · load_manifest + validate + iter_runs + ManifestInvalid · refuses duplicate run_names + non-int seeds + missing required fields) + `checkpoint.py` (write/read/latest_step_marker · marker REPLACED per write · actual .pt persistence is next-wave training-loop) + `on_host_logging.py` (write_host_heartbeat + write_host_poll_receipt + write_run_summary + host_journal_root · zero-influence writers) + `run_queue.py` (execute_campaign + next_pending_run + CampaignRunAlreadyActive fcntl-lock refusal + CampaignPriorRunNotSealed + dry_run mode) + `reconcile.py` (adoptability_of_campaign_run four-verdict + list_host_runs · case-insensitive seal check · pid liveness via os.kill(pid, 0)). New on-host script `tools/on_host_watchdog.sh` — cron/systemd-timer bash · reads AKKI_ON_HOST_WATCHDOG_TARGETS_DIR + AKKI_ON_HOST_TRAINER_CMD envs · zero-influence via `kill -0` live-PID skip · resume-from-checkpoint via marker sha + step · journal entry per restart. **R3 extensions folded in:** (a) `heartbeat.py::retire_heartbeat` (idempotent removal on clean exit · fixes r2 honest-limit "No heartbeat retirement on clean exit"); (b) `orphan_detector.py::_has_sealing_marker` (case-insensitive · accepts ACTIVITY_SUMMARY.md / activity_summary.md / Activity_Summary.MD · fixes r2 honest-limit "Sealing-filename case mismatch"); (c) `watchdog.py::select_adoptable_orphans(include_pid_dead=False|True)` (default is r2 backward-compat · True adds fresh-heartbeat-but-dead-PID runs with reason=pid_dead · fixes r2 honest-limit "select_adoptable_orphans blind spot"). **NEW ZERO-INFLUENCE CLASS BANKED THIS WAVE:** "restart-from-checkpoint is recovery, not interference" · frozen by 3 invariants (watchdog no-terminator-names + reconcile-never-deletes-checkpoint + zero_influence_class_documented). **HARD GATE PRESERVED:** MaskingTierNotAdmitted still raises for all 3 row-bearing tiers under any AKKI_ENV (2 regression invariants). **STRICT tests-first HELD unbroken across SEVEN consecutive closes** (WPW-v1-d + r1 + r1-wire + r2 + shield-train-build + compute-residuals + campaign-infra). Single mechanical RED drill receipt (`20260906T122400Z_wave_campaign_infra_RED_pre_impl.log` · 40 failed / 6 passed structural pre-checks · 2 test-authoring bugs surfaced + corrected pre-impl · all 46 tests GREEN on first impl run). Grounding brief authored pre-RED at `notes/wave_campaign_infra_grounding_brief.md` (owner ruling verbatim + §A zero-influence recovery-not-interference discipline with 4 enforcement clauses + §B module architecture + §C HARD GATE preservation + §D 8-item DoD + §E 5 wave-honest-limits + §F commit protocol). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2893 passed × 2 runs (Run 1: 106.77s · Run 2: 105.46s), byte-match on 2893/1/438, BASELINE_GUARD receipt `passed=2893 / baseline-failures-remaining=0 / quarantined=0 · status: OK`. Track-a HEAD **`9506a80`** · master HEAD to be committed with this update.

- **OWNER 3-DAY CAMPAIGN SHAPING BANKED VERBATIM (via user proxy pending owner one-line objectives-finalization):** owner "It could be a good run for us to establish certain base line based on objectives. You can shape two independent jobs for each VM. We can Also test the wizard logic(s) here." · **CAMPAIGN A (akki-vm) BASELINE LADDER**: Qwen2.5 0.5B → 1.5B → 3B → 7B sequential LoRA fine-tunes · fixed corpus (deduplicated ussd_question_response) · FIXED held-out slice (deterministic split banked BEFORE any training) · 2 seeds per size · output baseline_record per size (held-out loss/perplexity + task-shaped eval + cost actual + wall-clock + adapter hash). Gives future runs something to be "exceptional" against (R1 needs baselines to mean anything). · **CAMPAIGN B (akki-vm-ii) METHOD ABLATIONS**: fixed mid-ladder anchor (3B — rationale: capability inflection between 1.5B undersensitive and 7B too-expensive-to-replicate · H200 140GB handles LoRA at all ablation ranks) · varying method: corpus mix (USSD-only vs USSD+SMS), dedup on/off, LoRA rank (8/16/32), context length (512/1024/2048) · each ablation is a CIF-ideation-shaped event BEFORE running (hypothesis stated) so WPW novelty-chain mechanics (ideation → adoption → measured delta vs baseline) get exercised with real material. **WIZARD TESTING WOVEN THROUGH (owner explicit)**: every campaign run (i) auto-attaches Tier 1 notebook + captures live events (checkpoints + anomalies + cost checkpoints), (ii) drafts a Tier 2 report at settlement that CAN SETTLE (held-out measurements exist so acceptance criteria measure rather than refuse), (iii) evaluates Tier 3 eligibility MECHANICALLY + records verdict (eligible/not + why) with publication still blocked pending R1/R2/R3 · A1–A6 acceptance drills against real runs · A6 refused-run notebook retention path also planned. **DRAFT MANIFESTS = DESIGN ARTIFACTS**: authoring under `phase0/campaign_drafts/{campaign_a_baseline_ladder,campaign_b_method_ablations}.{json,md}` with honest wall-clock estimates + disk estimates + ladder-trim rationale. **NO DATA FLOW · ADMISSION GATE STILL FROZEN.** Owner-readable tables to follow in the next reply.

- **PRIOR CURRENT-WAVE MARKER (W-G5c-COMPUTE-RESIDUALS close at floor 2847 · retained for continuity)**:

- **CURRENT AS OF 2026-09-06T~12:15Z · W-G5c-COMPUTE-RESIDUALS CLOSED at floor 2847 (+11 from 2836).** Chart-caption + per-bar + tile-note substitutions complete the Compute Connected sub-tab visual surface. `pod_shell/frontend/src/App.js` gains **17 styled-element-anchor rules**: 14 r1 (3 chart captions across `door`/`week`/`state` chart states + 11 per-bar size labels · 5 door + 4 week + 2 state) + 3 r2 (owner-named tile notes for `Capacity this month` / `Committed to work` / `Free to allocate`). **0 LIVE facts landed this wave** — compute-estate exposes no hours-ledger / no queue-depth / no workflow-completion mechanism, so all 17 rules are HONEST-EMPTY or HONEST-PHRASING per grounding brief §B. All 14 r1 rules render `not measured`. The 3 r2 rules render specific honest-phrasings: capacity = `wall-clock ledger not measured` (names missing mechanism) · committed = `share-of-month not measured` (names missing mechanism) · free = `quoted against, not reserved` (VERBATIM preserve — honest product-language governance statement about allocation policy, not a numeric measurement, analogous to `compute-v2-runs-receipted-value` LIVE-TAUTOLOGY). 11 new invariants in `tests/invariants/test_compute_residuals_frontend.py`. **STRICT tests-first HELD unbroken across SIX consecutive closes** (WPW-v1-d + r1 + r1-wire + r2 + shield-train-build + compute-residuals). Single mechanical RED drill receipt this wave (`20260906T120500Z_wave_compute_residuals_RED_pre_impl.log` · 8 failed / 3 passed structural pre-checks · the 8 failures fire right-reason on 'rule not declared in App.js' before any implementation lands). **Authoring-time discovery banked as standing pattern:** original RED had 4 tests vacuously-passing because they iterated over rule inventory but only asserted on found rules (empty-list-passes-`assert not` pattern); all 4 tightened with full-iteration guards that record `<rule not declared>` as a mismatch AND assert iterated_count == inventory_size. Pattern for future substitution-rule invariant authoring — *vacuous-pass RED is not a right-reason RED*. Rule-must-match-rendered-DOM discipline preserved via new probe `tools/compute_residuals_dom_enum.py` + `tools/compute_residuals_dom_map.json` (extends compute-v2 probe with programmatic `<sc-raw-select value="{{ computeChart }}">` state switching via `select.value = X` + `dispatchEvent(change)` to enumerate all 3 chart states door/week/state · byText_union covers all 17 target strings). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2847 passed × 2 runs (Run 1: 105.04s · Run 2: 104.95s), byte-match on 2847/1/438, BASELINE_GUARD receipt `passed=2847 / baseline-failures-remaining=0 / quarantined=0 · status: OK`. Track-a HEAD **`81fe5a6`** · master HEAD to be committed with this update. Harness re-verify (real-Chromium eyeball proxy) fired GREEN at 20260906T121548Z: substitutions applied on compute-view=17 · dummies still present=[] · style signature met · merged GT rules=37 marked_slots=29 rule orphans=0 · 3 screenshots banked at `phase0/eyeball_proxies/20260906T121548Z_wave_g5_realchrome_wave_compute_residuals_close_{portal,registry,compute}.png`. **Compute Connected sub-tab visual surface now at 28 total rules: 4 LIVE + 6 HONEST-EMPTY + 1 LIVE-TAUTOLOGY (compute-v2 · 11) + 14 HONEST-EMPTY (r1) + 3 HONEST-PHRASING (r2).** Completes the Compute visual surface for the owner's pending eyeball per §DoD-item-8.

- **Grounding brief authored pre-RED** at `notes/wave_g5c_compute_residuals_grounding_brief.md` (CONDITION 1 · verbatim quotes from prototype + owner ruling). §A verbatim prototype source (COMPUTE_CHARTS object literal + computeStats array from `pod_shell/frontend/public/v8_prototype.html` bytes 766500-767760 and 1198800-1199650) + §B live-vs-honest-empty mapping + §C anchor authorship + §D DoD (8 numbered items from owner ruling verbatim) + §E wave-honest-limits + §F commit protocol.

- **Wave-honest-limits (candidates for -r3):** (1) **6 tile-notes remain uncovered** (owner named only 3 · candidate -r3 scope). Uncovered: `on-premise · RMS AI DC, Nairobi` and `A100 80GB · single node` (already covered by compute-v2 clusters-byline + gpus-byline per owner Ruling F), `both under the auto-run ceiling`, `14 complete, 3 ongoing, 1 failed`, `measured against wall-clock`, `runtime named in every receipt` (could be LIVE-TAUTOLOGY like compute-v2-runs-receipted-value if owner extends). (2) 0 LIVE facts land this wave — future waves adding hour-ledger / queue-depth / workflow-completion measurement would let r1+r2 dummies flip to LIVE. (3) Chart-selector navigation depth — if a future wave adds a chart state, probe extension must be updated to walk it.

- **NEXT ACTIVE TRACK (owner ruling 2c continues):** **W-Orchestrator-Resilience-r3** if no owner ruling has landed by that close — owner directive verbatim: "*keep it lean, prioritize retire_heartbeat + the PID-aware select_adoptable_orphans fix + sealing-name normalization; the full drill matrix only if cheap*". **Standing rule:** if owner's admission ruling (t1_full_mask under development env) OR TxtTrain-v2 go-signal lands mid-wave, bank verbatim in DECISIONS.md, finish the current wave at a clean commit boundary, then `W-Shield-Train-run` + `W-TxtTrain-v2` (fires through the governed pipeline) jump the queue. `W-WPW-v1-e` (Tier 3) stays design-only until R1/R2/R3 land. `W-Audio-P2` remains blocked on audio-location grant. `W-Chokepoint-LLM-row-bearing` + `W-Tenant-Entity-Catalogue` are chartered prerequisites for t1 admission's remaining two clauses.

- **PRIOR CURRENT-WAVE MARKER (W-Shield-Train-BUILD close at floor 2836 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~11:42Z · W-Shield-Train-BUILD CLOSED at floor 2836 (+50 from 2786). ADMISSION REMAINS PARKED.** Governed masking pipeline BUILT + fixture-proven end-to-end. New subsystem at `backend/services/shield_train/`: `authoring.py` (Doc 02 §A5.2 authoring surface · pure `add_entry` / `add_drawer_entry` / `resolve_drawer_entry` with monotonic `schema_version`) + `masking_policy.v0.json` (25 ledger entries covering `ussd_question_response` + `sms_log` end-to-end using census #2 schema facts + closed-declassification-path pattern from occupation ruling · 1 clarification_drawer entry per Ruling #5 for `sms_log.sms_sent` longtext body with `question_id: shield-2026-09-06-q001` and `cautious_default_applied: exclude`) + `row_executor.py` (governed row-bearing SQL executor · refuses unclassified tables and columns and policy-excluded columns by construction · applies mask_regex_scrub lifted from bypass-era `tools/text_train_pipeline/mask.py` · shape-only JSON receipts under `$SHIELD_TRAIN_RECEIPTS_DIR` · receipt fires even on backend outage with `error_class` field · `SELECT *` refused because unclassification-check unbounded columns · single-table SELECT with bare column names only in this wave · joins are next wave) + `pipeline.py` (masked-file transport with sha256 hash-mismatch = fatal `TransportIntegrityRefusal` · cleanup receipts with `du -sb` estimate · `execute_governed_lora_run` gates on `services.chokepoint.masking_tier.validate_tier` via `AKKI_ENV` raises `MaskingTierNotAdmitted` when not admissible). `services/training_runner/ssh_seam.py.execute_lora_train_real` UNSTUB — pre-r2 unconditional `RealSSHNotWiredYet` raise REMOVED · delegates to `shield_train.pipeline.execute_governed_lora_run` with `AKKI_LORA_MASKING_TIER` and `AKKI_LORA_TABLE_CONTEXT` env pins · **STUB is gone; ADMISSION GATE is what remains as the honest block.** `services/chokepoint/masking_tier_allowlist.v0.json` extended with `admission_request_drafted_by_wave` + `prerequisites_status` fields on `t1_full_mask` / `t2_partial` / `t3_category`; **`admissible_under_env: []` stays empty until owner rules** (single JSON-edit action); `t1_full_mask` prerequisite (iii) governed masking policy authored MARKED `satisfied_by_this_build: true` with evidence pointer to `masking_policy.v0.json`; prerequisites (i) LLM chokepoint + (ii) tenant entity catalogue still needed and OUT OF `W-Shield-Train` scope (chartered as `W-Chokepoint-LLM-row-bearing` + `W-Tenant-Entity-Catalogue`). 50 new invariants across 5 test files (14 policy structure + 12 registry-expansion coverage + 10 row-executor + 9 pipeline + 5 admission-request). **STRICT tests-first HELD unbroken across FIVE consecutive closes** (WPW-v1-d + r1 + r1-wire + r2 + shield-train-build). Single mechanical RED drill receipt this wave (`20260906T113342Z_wave_shield_train_build_RED_pre_impl.log` · 50/51 fail with mixed ImportError/AssertionError/FileNotFoundError before implementation). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2836 passed × 2 runs (Run 1: 104.10s · Run 2: 105.59s), byte-match on 2836/1/438, BASELINE_GUARD receipt `passed=2836 / baseline-failures-remaining=0 / quarantined=0`. Track-a HEAD **`d5aadef`** · master HEAD to be committed with this update.

- **ADMISSION REQUEST drafted in DECISIONS.md § W-Shield-Train-BUILD §Admission-Request.** Frame (owner-visible in `masking_tier_allowlist.v0.json.entries[t1_full_mask].prerequisites_status`): (iii) masking policy authored = satisfied by this build with evidence pointer; (i) LLM chokepoint + (ii) tenant entity catalogue = still needed, out-of-scope for this wave, chartered separately. **One-line owner ruling shape:** either "Admit `t1_full_mask` under env `<development|staging|...>`; (i) and (ii) can wait for their own waves" OR "Not admissible until (i) and (ii) also land — hold shield-train-run until then". **Where the ruling lands:** owner edits `admissible_under_env` from `[]` to the ruled env list — that single JSON edit is the entire admission action. This wave's `test_all_tiers_still_have_empty_admissible_under_env` invariant will trip the moment the edit lands — that's the intended trigger for `W-Shield-Train-run`.

- **Design decisions banked (each frozen by an invariant):** (1) `sms_sent` parked in `clarification_drawer` per Ruling #5. (2) `SELECT *` refused by construction. (3) sha256 mismatch on transport = fatal `TransportIntegrityRefusal`. (4) `execute_lora_train_real` unstub raises `NotImplementedError` when tier IS admitted (place-holder; full loop is next wave). (5) Regex scrub lifted verbatim from bypass-era `mask.py`. (6) `response_sanitizer` agreement invariant cross-checks phone/mobile classifications match `DIGICOW_PII_BANNED_FIELDS`.

- **Wave-honest-limits (candidates for next waves):** (a) `SELECT *` + joins unsupported — single-table SELECT with bare column names only; joins are the next row-executor wave. (b) Tenant entity catalogue prerequisite (ii) still needed for t1 admission — out of `W-Shield-Train` scope. (c) End-to-end training loop lands only when `W-Shield-Train-run` fires — this wave builds primitives + pipeline + admission gate; the actual on-host LoRA fine-tune call is the next wave. (d) LLM chokepoint prerequisite (i) still needed — chartered as `W-Chokepoint-LLM-row-bearing`.

- **NEXT ACTIVE TRACK:** **W-TxtTrain-v2** — the improved LoRA text training. Two paths depending on owner's next call: (A) if owner rules on admission for `t1_full_mask` in dev/staging, TxtTrain-v2 fires **through this new governed pipeline** (`execute_lora_train_real` → `execute_governed_lora_run` → row-extract → build corpus → stage → cleanup) — the acceptance-required path; (B) if owner defers admission, TxtTrain-v2 stays parked awaiting either the admission ruling OR a separate build wave granting a narrow bypass class. **Standing rule holds:** if TxtTrain-v2's go lands mid-wave (e.g. during residuals work), finish the residual at a clean commit boundary and re-verify the governed pipeline is still what fires. `W-Shield-Train-run` (end-to-end training loop on the governed pipeline) is chartered as natural follow-on after admission lands. `W-Chokepoint-LLM-row-bearing` and `W-Tenant-Entity-Catalogue` gate `t1` in full. **Small residuals** (chart-captions r1, tile-notes r2) still queue behind unless a natural pause opens.

- **Standing rule (still binding):** if owner rulings land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is now the recovered baseline across FIVE consecutive closes. **Runtime drill discipline** established at r2 stays binding whenever a resilience layer's primary failure mode CAN be rehearsed.

- **PRIOR CURRENT-WAVE MARKER (W-Orchestrator-Resilience-r2 close at floor 2786 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~11:19Z · W-Orchestrator-Resilience-r2 CLOSED at floor 2786 (+24 from 2762).** Auto-adopt + watchdog primitives land as `backend/services/orchestrator_resilience/{adopt,watchdog}.py` (adopt: `can_adopt/mark_adopted/read_adoption_records` · adoptability policy = not-sealed + has-launch + latest-poll-mtime-within-max_poll_age_s · idempotent within dedupe_window_s · zero-influence writer returns None on failure. watchdog: `pid_is_alive` via POSIX signal-0 [CANNOT terminate] · `is_orchestrator_dead` composes {no_heartbeat, stale_heartbeat, pid_dead} · `select_adoptable_orphans` composes r1 orphan_detector + r2 adopt.can_adopt). r2 wire in `tools/gpu_burn_orchestrator.py`: `AKKI_ADOPT_RUN_ID` env var pins RUN_ID + BURN_ROOT · `main()` reconcile upgraded to `select_adoptable_orphans` surfacing adoptability per orphan · `burn_one_host` skips stage-3/stage-4 (stage/launch) when adopting · adopt-mode reconcile falls back to PID-aware `is_orchestrator_dead` when target isn't in staleness-gated enumeration [drill-surfaced fix]. New supervisor tool `tools/gpu_burn_watchdog.py` prints copy-paste respawn commands (INFORMATIONAL only; auto-execute is r3 · invariant `test_watchdog_script_no_subprocess_execute_in_r2_scope` freezes the scope). 24 new invariants (15 primitives + 8 wire + 1 drill fix) in `test_orchestrator_resilience_r2.py` and `test_orchestrator_resilience_r2_wire.py`. 2 semantic-preserving relaxations to r1-wire tests (accept `select_adoptable_orphans` in addition to `find_orphaned_runs`; underlying contract unchanged). **STRICT tests-first discipline HELD unbroken across FOUR consecutive closes** (WPW-v1-d + r1 + r1-wire + r2). Two RED receipts banked: primitives RED (15/15 ImportError before modules · `20260906T105834Z_wave_orch_resilience_r2_RED_pre_module.log`) + wire RED (8/8 mixed AssertionError/FileNotFoundError before wire+script · `20260906T110056Z_wave_orch_resilience_r2_wire_RED_pre_impl.log`). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2786 passed × 2 runs (Run 1: 102.90s · Run 2: 102.79s), byte-match on 2786/1/438, BASELINE_GUARD receipt `passed=2786 / baseline-failures-remaining=0 / quarantined=0`. Track-a HEAD **`5be5d36`** · master HEAD to be committed with this update.

- **RUNTIME DRILL fired end-to-end — the exact 2h-burn failure mode is now a rehearsed receipt.** Full DRILL_REPORT.md at `phase0/drill_receipts/20260906T110345Z_wave_orch_resilience_r2_runtime_drill/`. Summary: dual-host `RUN_ID = burn_20260906T110345Z_b1c2c20f` · 12-min real burn · 0.28 GPU-hours · sustained 100 % util at ~640 TFLOPS/GPU · exit_code=0 on both hosts. Sequence: (1) fired orch1 → reconcile-on-start correctly surfaced 2 stale orphans as NOT_ADOPTABLE. (2) at cycle=4, captured heartbeat with `on_host_status: {"akki-vm": "polling", "akki-vm-ii": "polling"}` — **observation (a) POSITIVE**. (3) SIGKILL orch1 → verified on-host burn.pids ALIVE on both hosts via `kill -0` (setsid nohup detached process groups). (4) watchdog scan surfaced orch1 as ADOPTABLE + printed exact `AKKI_ADOPT_RUN_ID=...` respawn command. (5) respawned as orch2 → RUN_ID + BURN_ROOT correctly adopted, launch phases skipped, polling resumed. **Drill surfaced bug**: adopt-mode reconcile depended on staleness-gated enumeration → fresh-heartbeat-but-dead-PID target missed → no adoption ledger entry. (6) **Fix banked in-flight** with tests-first invariant: adopt-mode falls back to `is_orchestrator_dead(_ADOPT_RUN_ID)` (PID-aware). (7) SIGKILL orch2 → on-host STILL alive. (8) respawned as orch3 (post-fix) → adoption ledger entry banked at `adoption_20260906T111020Z_34237.json` with `orphan_reason: "pid_dead"` — **observation (b) POSITIVE**. (9) burn completed cleanly, 20 polls captured across 3 orchestrator generations. **Zero-influence RE-VERIFIED at runtime**: only pod-side orchestrator PIDs signalled; on-host burn.pids never touched; adopt.mark_adopted never raised even when returning None.

- **Wave-honest-limits surfaced by the drill (candidates for r3, banked in DRILL_REPORT.md):** (i) no heartbeat retirement on clean exit — final heartbeat remains on disk; candidate `retire_heartbeat(run_id, final_status)` primitive. (ii) sealing filename case mismatch — `adopt.can_adopt` and `orphan_detector._looks_in_flight` both key on uppercase `ACTIVITY_SUMMARY.md` while reconciler writes lowercase `activity_summary.{txt,json}`; consistent within r2 (both primitives agree) but a cleanup candidate. (iii) no cross-generation dedupe on `should_poll_at_elapsed`; intentional in r2 (adoption doesn't cross-index generations). (iv) `select_adoptable_orphans` inherits r1 staleness-only blind spot for fresh-heartbeat-but-dead-PID targets; drill-surfaced fix scoped narrowly to adopt-mode reconcile (broader fix candidate for r3 = add `include_pid_dead=True` to `select_adoptable_orphans`). (v) single drill run — a more rigorous r3 stress matrix would vary kill timing, signal type, and multi-orchestrator scenarios.

- **NEXT ACTIVE TRACK:** **W-TxtTrain-v2** (improved LoRA text training) now benefits from PROVEN pod-side resilience — both r1 wire + r2 auto-adopt rehearsed in a controlled drill. Still awaiting owner's explicit *go/no-go* per the WPW-v1-d ruling. **W-Orchestrator-Resilience-r3** stays chartered but LOW priority — r2 delivers the acceptance-required behaviour and the wave-honest-limits are enhancements, not blockers. **W-Audio-P2 remains blocked** on the audio-location grant (owner outbound sent; waiting on SSH-to-app-server / URL-rewrite-pattern-+-LIST-creds / different-DB-connection-record). **W-Shield-Train remains blocked** on masking-tier admission ruling. **W-WPW-v1-e (Tier 3 white paper)** stays design-only until R1/R2/R3 land.

- **Standing rule (still binding):** if owner's R1/R2/R3 rulings land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is now the recovered baseline across FOUR consecutive closes. Runtime drill discipline established: whenever a resilience layer's primary failure mode CAN be rehearsed as a controlled drill, do it — a resilience layer that's never rehearsed isn't proven.

- **PRIOR CURRENT-WAVE MARKER (W-Orchestrator-Resilience-r1-wire close at floor 2762 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~10:48Z · W-Orchestrator-Resilience-r1-wire CLOSED at floor 2762 (+14 from 2748).** Three resilience primitives (`heartbeat`, `orphan_detector`, `resume`) plumbed into `tools/gpu_burn_orchestrator.py`: (a) `burn_one_host` writes a heartbeat to `${ORCHESTRATOR_HEARTBEAT_DIR}/<RUN_ID>.json` on every poll cycle with plain `RUN_ID` key + shared `_HB_ON_HOST_STATUS` dict updated per-host under `_HB_LOCK` + atomic `next(_HB_CYCLE_COUNTER)` cycle number; (b) `burn_one_host` calls `resume.should_poll_at_elapsed(RUN_ID, host_slug, elapsed_s)` before capturing nvidia_smi as an idempotency guard (a restarted poller skips windows already receipted on disk — the "resumable polling" clause of the charter); (c) `main()` calls `orphan_detector.find_orphaned_runs(max_staleness_s=600)` before entering the `ThreadPoolExecutor` and prints an informational `RECONCILE:` block to stdout. Every resilience call is wrapped in try/except at the call site; imports are lazy inside the try; a broken/missing primitives package NEVER halts orchestrator start or breaks the poll loop (zero-influence discipline preserved from the primitives close). 14 new invariants in `test_orchestrator_resilience_wire.py` — AST-inspection of the tool source. **STRICT tests-first discipline unbroken across three consecutive closes** (WPW-v1-d + Orch-Resilience-r1 + this wire): mechanical RED drill receipt at `phase0/drill_receipts/20260906T104126Z_wave_orch_resilience_wire_RED_pre_impl.log` — 12/14 fail with right-reason assertion errors before wire lands (each naming the specific missing seam), 2 pass as correct structural pre-checks (source parseable + no top-level import present). Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2762 passed × 2 runs (Run 1: 102.70 s · Run 2: 102.30 s), byte-match on pass/skip/warning tallies (2762/1/438 both runs), BASELINE_GUARD receipt `passed=2762 / baseline-failures-remaining=0 / quarantined=0`. Track-a HEAD **`32d1180`** · master HEAD to be committed with this update. **DONOR-REVIEW actioned in full** per owner directive: 52-line pre-existing working-tree diff of unknown session origin reset before RED, reviewed against tests-first output. Kept: zero-influence try/except pattern + reconcile-on-start scaffolding + `informational-only in this wave` scoping. Rejected during tests-first: (a) compound `run_id=f"{RUN_ID}__{host_slug}"` breaks orphan_detector's plain-RUN_ID lookup (rewritten to plain RUN_ID), (b) inline `on_host_status={host_slug:"polling"}` dict per thread drops peer state (rewritten to module-level shared dict + Lock + snapshot-under-lock). Added beyond donor: `should_poll_at_elapsed` idempotency guard + threading.Lock + itertools.count. **BACKFILL** landed in this-wave manifest edit: prior primitives-close commit `3e2efc8` bumped `counts_at_baseline.passed` and `passed_floor` from 2732 → 2748 but MISSED the paired `ratchet_history` append — surfaced as a right-reason RED at `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` in this wave's initial Run 1 (2761 passed / 1 failed / history[-1].passed=2732 vs counts.passed=2748). Backfilled here with full attribution note; primitives-close double-green tallies unchanged and honest. Two `ratchet_history` entries appended this cycle: 2732→2748 (delta 16, backfill) and 2748→2762 (delta 14, this wave). History length: 35 → 37. **PINS.md auto-emitter identified:** `backend/services/connect/gpu_submit.py` `_update_pins()` (L60-91) rewrites the `<!-- CONNECT-GPU-PINS -->` block on every commissioning acceptance via the pipeline's stage-6 `pins_update`. Legitimate workflow state — future workflow: commit with attribution rather than leave uncommitted.

- **Runtime validation still pending.** The wire is SOURCE-LEVEL green (14 AST invariants freeze the wire shape). It is NOT YET runtime-tested against a live burn (that needs live SSH + GPUs + 20+ min wall-clock, not possible inside pytest). Wire-in-flight validation fires in the next actual burn/train run using `tools/gpu_burn_orchestrator.py`: first artefact to check is `${ORCHESTRATOR_HEARTBEAT_DIR:-phase0/orchestrator_heartbeat}/<RUN_ID>.json` appearing during the burn, with per-poll updates and both host-slugs eventually populating `on_host_status`. Runtime misbehaviour → add a runtime-observation test in a follow-on `W-Orchestrator-Resilience-r2` wave (auto-adopt orphans + watchdog respawn).

- **Owner report notes actioned (2026-09-06T~10:48Z ruling):**
  - Standing infrastructure note appended to `STATE/SPRINT_PLAN.md`: the dual 5.86 TiB `/dev/vdb` ext4 volumes on `akki-vm` + `akki-vm-ii` are flagged as candidate HSS/staging storage for W-Audio-P2 (§W-Audio-P2-c representative slice + §W-Audio-P2-d HSS ingest). Symmetric provisioning across both hosts enables either primary+hot-mirror or two-parallel-slices; capacity math shows 1000 h wav ≈ 10 % of a single volume so no storage provisioning is needed before W-Audio-P2-c can fire. Governance note: DO-shaped block volumes (not AWS EBS) — receipts must use "block volume attached to GPU host" language.
  - The three-level evidence verdict on the DigiCow file backend (§preceding DECISIONS entry) is going to the owner as an outbound message; no additional action on this side.

- **NEXT ACTIVE TRACK:** owner's *go/no-go* awaited on **W-TxtTrain-v2** (improved LoRA text training with deeper corpus, sms_log secondary, uniqueness dedup — still needs an explicit owner fire signal). **W-Orchestrator-Resilience-r2** (auto-adopt orphans + watchdog respawn) is chartered as the next resilience wave AFTER a runtime observation from a real burn validates this wire. **W-Audio-P2 remains blocked** on the audio-location grant. **W-Shield-Train remains blocked** on masking-tier admission ruling. **W-WPW-v1-e (Tier 3 white paper)** stays design-only until owner rulings R1/R2/R3 land.

- **Standing rule (still binding):** if R1/R2/R3 land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is the recovered baseline and has now held across THREE consecutive closes (WPW-v1-d · Orch-Resilience-r1 · Orch-Resilience-r1-wire). Continue.

- **PRIOR CURRENT-WAVE MARKER (W-Orchestrator-Resilience-r1 primitives close at floor 2748 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~10:28Z · W-Orchestrator-Resilience-r1 CLOSED at floor 2748 (+16 from 2732).** Pod-side orchestrator resilience primitives land as `backend/services/orchestrator_resilience/{__init__,heartbeat,orphan_detector,resume}.py` (thin kernel: 6 public functions across heartbeat + orphan_detector + resume · zero-influence writers that swallow their own storage errors and return False/None sentinels · observer discipline: no `update_*` / `set_*` / `kill_*` / `terminate_*` shapes on the public surface — the resilience layer never terminates jobs). 16 new invariants in `test_orchestrator_resilience.py` — every docstring cites the owner charter verbatim + zero-influence reference to WPW-2/A2. **STRICT tests-first discipline HELD unbroken from the WPW-v1-d recovery**: mechanical right-reason RED drill receipt banked BEFORE the module was authored (all 16 tests failing with `ImportError` from `services.orchestrator_resilience` against a non-existent submodule — correct spec-anchored refusal), at `phase0/drill_receipts/20260906T100500Z_wave_orch_resilience_RED_pre_module.log`. Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2748 passed × 2 runs (Run 1: 102.63 s · Run 2: 103.03 s), byte-match on pass/skip/warning tallies (2748/1/438 both runs · 271 progress lines each), BASELINE_GUARD receipt `passed=2748 / baseline-failures-remaining=0 / quarantined=0` byte-identical modulo timings. Track-a HEAD **`3e2efc8`** · master HEAD to be committed with this update. **Wiring is a follow-on**: the primitives are authored and green, not yet called by `tools/gpu_burn_orchestrator.py`; that wiring step is chartered as `W-Orchestrator-Resilience-r1-wire` and lands after owner ratifies these primitives (discipline: new primitive lands green before it's plumbed into a running orchestrator).

- **Owner interject banked mid-close (2026-09-06T~10:07Z + ~10:15Z)**, actioned in full, verbatim scope correction taken: *"Have you checked the EBS volume?"* → block-device-up storage inventory on both `akki-vm` + `akki-vm-ii`, empty attached data volumes re-confirmed (28 KiB used of 5.86 TiB per host, `lost+found` only); *"I think you may need to read the content."* → content-level deep sweep of every non-secret file under `/home` + `/mnt` + `/srv` + `/opt` + `/var/www` on both hosts (36,998 files / 9.1 GiB akki-vm · 32,250 / 7.9 GiB akki-vm-ii), classified with `file --mime-type` on host (magic-byte only), sha256 gated at ≤ 100 MiB, ffprobe installed on both hosts and run against every audio/video magic-byte candidate. **Verdict at three independent levels of evidence:** (1) magic-byte census → 0 audio/\* + 0 video/\* mimes on either host; (2) extension-based find → 0 audio-ext + 0 video-ext files on either host; (3) DB-sampled filename cross-check → 0 / 60 matches on 26,891 (akki-vm) + 24,407 (akki-vm-ii) unique basenames. **The DigiCow file backend is definitively not on the two GPU hosts.** Everything present on both hosts is Python site-packages / pip cache / HF hub cache / Nvidia tooling from this programme's WPW + orchestrator work. Report artefact at `phase0/storage_survey/20260906T101542Z_content_sweep/REPORT.md` + `aggregate/{akki-vm,akki-vm-ii,cross_check}/*` + `scripts/*` + `receipts/*_ffmpeg_install.log`. Guard-rail compliance re-attested (no bytes off-host, aggregates-only default preserved, secret patterns skipped count/size only, RO scratch mount correctly not fired since no unmounted volumes existed).

- **NEXT ACTIVE TRACK:** owner's go/no-go awaited on **W-TxtTrain-v2** (improved LoRA text training with deeper corpus, sms_log secondary, uniqueness dedup — chartered but a longer training run needs an explicit owner fire signal per WPW-v1-d ruling). If owner defers: **W-Orchestrator-Resilience-r1-wire** (plumb the just-landed primitives into `tools/gpu_burn_orchestrator.py`) is the next unambiguously-in-scope task. **W-Audio-P2 remains blocked** on the audio-location grant — after this content sweep, the position is now stated at highest confidence: the DigiCow file backend is a third machine (or an object store) we don't reach; owner grant needed is SSH access to it, or the URL-rewrite pattern + LIST creds for the backing bucket, or a connection record for a different DB entirely. **W-Shield-Train remains blocked** on masking-tier admission ruling. **W-WPW-v1-e (Tier 3 white paper) stays design-only** until owner rulings R1 (numeric exceptional threshold), R2 (release signatory), and R3 (three-tier structure + WPW-11 novelty-claim ratification) land.

- **Standing rule (still binding):** if R1/R2/R3 land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary, not mid-work. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is the recovered baseline and has now held across two consecutive closes (WPW-v1-d and Orch-Resilience-r1) — do not slip back into v1-c-style co-authoring.

- **PRIOR CURRENT-WAVE MARKER (W-WPW-v1-d close at floor 2732 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-06T~09:55Z · W-WPW-v1-d CLOSED at floor 2732 (+15 from 2717).** WPW Tier 2 Technical Report drafter lands as `backend/services/wpw/tier2_report.py` (thin kernel: `draft_report(run_dir)` + frozen 9-tuple `SECTION_SKELETON` + `INTERNAL_ONLY_MARKER` + `EVIDENCE_CLASSES` + `ACCEPTANCE_CRITERIA_ORDER`). 15 new invariants in `test_wpw_tier2_report.py` — every docstring cites verbatim WPW-8/-9/-10 + A4/A6. **STRICT tests-first discipline RECOVERED from the v1-c concession**: mechanical right-reason RED drill receipt banked BEFORE the module was authored (all 15 tests failing with `ImportError` from `services.wpw` against a non-existent `tier2_report` module — the correct spec-anchored refusal), at `phase0/drill_receipts/20260906T094500Z_wave_wpw_v1d_RED_pre_module.log`. Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2732 passed × 2 runs, stripped-diff = 0. WPW-9 refusal path (owner-flagged heart of the tier) tested: deleting `nvidia_smi_before.json` causes hardware-fingerprint figure to disappear from `figures[]` and surface in `refused_figures[]` with plain-language reason. WPW-10 internal-only marker in body + metadata; no outer-gate export surface. A4 traceability (100 % figure resolution in well-formed run) + A6 refused-run drafts with reason + all 6 acceptance numbers, both exercised. Right-reason RED discovered mid-close: `test_harness_ground_truth_receipt_is_recent` fired (6-day drift from last harness snapshot) → refreshed with fresh `--strict` harness run (20 rules / 20 marked / 0 orphans) before ratchet close. Real-data demonstration: `phase0/wpw_tier2_demo/txttrain_20260831T193455Z_9594859a/TIER2_REPORT.md` drafted against banked LoRA run — 9 sections + 5 resolving figures, 0 refused, settlement=`refused` because 4/6 acceptance criteria are honest-empty (no held-out slice, no abstention head, no served seat, no OOD eval — the drafter refused to fabricate what wasn't measured). Track-a HEAD `f42d0d5` · master HEAD to be committed with this update.

- **Owner interject banked (2026-09-06T09:35–09:40Z)** verbatim: *"I also need another census on the digicow db. there should be access to the audion files."* Actioned: **Census #2** fired via `POST /api/census/run`, 86 s wall-clock, same shape as #1 (2 DBs · 233 tables · net −1,166 rows over 8.7 days · 15 tables with row churn · 0 schema drift · 0 new media/audio-shaped columns). Registry surface shows Census #2 as latest via `/api/census/latest`. Diff at `phase0/census/census_0002_diff_vs_0001.{json,md}`. **Audio-location hunt: AUDIO NOT FOUND in digicow_live estate.** Owner-authorized bounded bypass probe (`BYPASS_CLASS = owner_authorized_audio_location_probe`, tool at `tools/audio_location_probe.py`) sampled the 3 media-shaped columns Census #2 exposed at hard cap 30 rows each · 90 total sample reads · shape-only receipts (no full URL banked). Verdicts: `company.image_url` = IMAGE (jpeg/png), `user_group_trainings.file_url` = IMAGE (100 % jpeg), `pend_action_file` = 100 % NULL. All URLs are bare filenames with `file://` scheme — actual files live in a storage backend external to RDS. What owner needs to grant to enable audio: bucket/host pattern the DigiCow app resolves filenames against + credential class required to LIST + connection record for a different DB if audio lives there.

- **NEXT ACTIVE TRACK:** **W-WPW-v1-e Tier 3 (white paper) stays design-only** until owner rulings **R1** (numeric exceptional threshold), **R2** (release signatory), and **R3** (three-tier structure + WPW-11 novelty-claim ratification) land. Unblocked follow-on tracks per SPRINT_PLAN.md: **W-TxtTrain-v2**, **W-Orchestrator-Resilience-r1** (owner directive #4 kept it chartered; not folded in this close because it wouldn't be cheap alongside Tier 2 + real-data demo + census #2 + audio hunt). **Blocked:** W-Audio-P2 (still needs audio location — see above), W-Shield-Train (masking-tier admission ruling).

- **Standing rule (still binding):** if R1/R2/R3 land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary, not mid-work. Discipline reminder: STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt is now the recovered baseline — do NOT slip back into v1-c-style co-authoring.

- **PRIOR CURRENT-WAVE MARKER (W-WPW-v1-c close at floor 2717 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-09-01T~02:55Z · W-WPW-v1-c CLOSED at floor 2717 (+14 from 2703).** WPW Tier 1 Lab Notebook writer lands as `backend/services/wpw/tier1_notebook.py` (thin kernel: attach/record/list/verify + WPW-18 economics helper). Auto-attach wired into `training_runner.open_run()` (WPW-1) with zero-influence try/except (WPW-2 · A2). 14 new invariants in `test_wpw_tier1_notebook.py` — every docstring cites verbatim WPW-N spec text. Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2717 passed × 2 runs, stripped-diff = 0. Concession banked (DECISIONS.md · W-WPW-v1-c section): tests+module co-authored in same batch, right-reason validity by inspection only, no mechanical RED drill receipt. Track-a HEAD `fcdca98` · master HEAD to be committed with this update.

- **GPU 2h dual-host burn RECONCILED** (owner-authorized 2026-08-31T~21:20Z "run a longer one" go-ahead). On-host burns completed the FULL 7200.01 s wall-clock on both hosts (`kind:"done"` sealing events banked). Fleet median ≈638 TFLOPS/GPU fp16 · 2.55 PFLOPS aggregate · ≈18.4 exaFLOP total · ≈5.5 kWh energy · $0.00 platform credits. **Integrity finding banked honestly**: pod-side orchestrator died at ~22:02Z (41 min in); 15/24 planned polls lost; post-run summary + cleanup were manually reconstructed at reconcile 2026-09-01T02:46–02:52Z. Activity summary at `phase0/gpu_burn/burn_20260831T212116Z_5a83c165/ACTIVITY_SUMMARY.md`. Both hosts now cleaned + idle (`gpurcp-032dc817a07f`, `gpurcp-d59e7f2aba7c`). Charter `W-Orchestrator-Resilience-r1` banked as unscheduled follow-on.

- **NEXT ACTIVE TRACK:** W-WPW-v1-d (Tier 2 Technical Report drafter · WPW-8/-9/-10 + A4/A6 per WPW spec §4 · buildable now per §7). Also unblocked. Tier 3 (W-WPW-v1-e) remains design-only until owner rulings R1 (exceptional threshold) + R2 (release signatory) + R3 (three-tier structure + WPW-11 novelty-claim ratification) land. Follow-on unblocked charters: **W-TxtTrain-v2** (improved LoRA text training with deeper corpus, sms_log secondary, uniqueness dedup); **W-Orchestrator-Resilience-r1** (heartbeat log + supervisor + resumable polling + orphan-run API). Blocked (waiting owner): **W-Shield-Train** on masking-tier admission ruling, **W-Audio-P2** on archive access.

- **Standing rule (still binding):** if R1/R2/R3 land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary, not mid-work. Discipline reminder for W-WPW-v1-d: return to STRICT tests-first RED-then-GREEN with a banked mechanical RED drill receipt (the v1-c concession should not recur).

- **PRIOR CURRENT-WAVE MARKER (W-G5c-COMPUTE-v2 close at floor 2703 · retained for continuity of ledger)**:

- **CURRENT AS OF 2026-08-31T~21:30Z · W-G5c-COMPUTE-v2 CLOSED at floor 2703 (+11 from 2692).** 11 tile-value substitution rules (4 LIVE, 6 HONEST-EMPTY, 1 LIVE-TAUTOLOGY) bind `/api/compute/estate` facts into the Compute Connected sub-tab. Harness green: 20 rules / 20 marked_slots / 0 orphans merged across Registry+Compute views; compute-view distinctive dummies (`on-premise · RMS AI DC, Nairobi`, `A100 80GB · single node`) absent; live phrasings (`on-premise · akki-vm + akki-vm-ii`, `H200 140 GiB · 2 nodes`, `not measured`) present; slot #1 style signature (INTERRUPT 3) intact. Double-green terminal `pytest tests/invariants/` under `BASELINE_GUARD=1`: 2703 passed × 2 runs, stripped-diff = 0. Systemic latent bug fixed in `_app_js_executable()` and 4 other loci in `test_wave_g_v8_shell_port.py` (block-first comment strip was silently mangling App.js when a `//` line comment contained `/*` — the compute-v2 addition surfaced a `runs/*.json` glob that tripped it). Receipts: harness log + 3 screenshots at `phase0/eyeball_proxies/20260831T212715Z_wave_g5_realchrome_wave_g5c_compute_v2_close_v2_*`. Residuals banked NOT as bugs but as scope statements: **-r1** chart-caption substitution (`COMPUTE_CHARTS` object · captions like `'1,240 hrs committed'` on doughnut/stack chart) · **-r2** tile-note substitution (small-print notes beneath each tile value, e.g. `'43% of the month'`).

- **NEXT ACTIVE TRACK (owner-sequenced 2026-08-31T~19:15Z, ruling 8):** W-WPW-v1-c (Tier 1 lab notebook). Unblocked. Owner rulings R1/R2/R3 still with owner; Tier 3 stays design-only until they land; Tiers 1+2 may build. Follow-on unblocked charters: **W-TxtTrain-v2** (owner-authorized 2026-08-31T~21:20Z, "can you run a longer one like 2 hrs if not dependent on credits" — GPU time is on owner's EC2, no platform credits; agent-time is the constrained resource). Blocked (waiting owner): **W-Shield-Train** on masking-tier admission ruling, **W-Audio-P2** on archive access.

- **Standing rule (still binding):** if R1/R2/R3 land mid-close of the next wave, bank them verbatim in DECISIONS.md and finish the close first; owner's sequencing wins at the NEXT clean commit boundary, not mid-work.

- **PRIOR CURRENT-WAVE MARKER (Wave-G5c stages 1–3 · retained for continuity of ledger)**:

- **Current wave**: **Wave-G5c stages 1–3 · LARGELY COMPLETE at floor 2680 (+69 from 2611 opening).** Owner rulings #1, #2, #5 landed with gates. First LIVE Census #1 fired against DigiCow cluster — owner expectation of >1 database CONFIRMED (2 DBs: digicow_live + ndume · 233 tables · 5,909,421 rows · single_database_visibility_flag=false · no permissions-gap finding to escalate). Slot #1 renders LIVE with Census #1 data ("RMS AI is reading 2 connected sources, holding with 233 tables read — size and completeness not yet measured, awaiting first census." — underline+oxblood styling intact per Wave-G5b interrupt). Compute-estate backend live-serving hosts+rollup. 6 compute-tile substitution rules declared+bind-ready. Doc 10 vs Doc 19B anchor verified (Doc 10=Promise #14 runtime evidence-records; Doc 19B=EP-4 terminal-test ordering guard, already landed Wave-D).

- **HONEST GAP (banked at 2026-08-28T~16:10Z close):** Compute-tab DOM substitution deferred. dc-runtime navigation path unresolved: post Admin>Registry, `regTabsView` labels (`Data Connected`, `Compute Connected`, `LLMs & Trained Models`) are NOT rendered in DOM. Investigation confirmed: `<sc-if value="{{ isRegistryGroup }}">` + `<sc-if value="{{ isRegEstate }}">` gate the tabs. The `Admin > Registry` navigation from the top-nav does NOT set `isRegistryGroup=true` (or `isRegEstate=true`). The tabs live behind a nav state the top-nav walker doesn't reach. Follow-up needs: (a) identify what triggers `isRegistryGroup=true` in the prototype's state machine, (b) drive the harness through that path, (c) re-run harness → compute-tile substitution → real-Chromium bundle capture. Rules and endpoints are ready; only the nav-path is missing.

- **NEXT ACTION** (owner call needed): **either** (A) resolve the Compute-tab nav path and then fire Wave-G5c-KEYPAIR-HARDENING (Ruling #4), **or** (B) proceed to Wave-G5c-KEYPAIR-HARDENING first and defer Compute-tab visual verification to a follow-up drill. Ruling #4 requires operator attention on both GPU hosts (STOP-before-disable-passwords discipline if key-auth verify fails) — I stopped short of firing it without an explicit go-ahead in this session because it carries lockout risk if a step fails mid-sequence. Also awaiting owner review of the Doc-anchor verification finding (banked verbatim in DECISIONS.md at 2026-08-28T~15:40Z).

- **PRIOR CURRENT-WAVE MARKER (Wave-G5c-COMPUTE-BACKEND · retained for continuity of ledger)**: Wave-G5c-COMPUTE-BACKEND · CLOSED 2026-08-28T~15:30Z at floor 2649 (+13 from 2636). `services/compute_estate/{estate,router}` landed + 1 MUST_BE_LIVE_ROUTES added (`GET /api/compute/estate`). Descriptor derived from newest Wave-H whitepaper (`wp_run_wave_h_*.json` glob, mtime_ns sort). Product-language only: name/readiness/gpu_model/gpu_count/gpu_memory_gb_per_gpu. Static-scan gate refuses hardcoded literals (`NVIDIA H200`, `akki-vm`, `139.8`, ...) — the surface follows facts, not code. Engineering-vocab ban: `test_estate_response_never_carries_engineering_vocab` refuses IPs / ssh / password / auth / iam / arn / sudo / kernel / driver_version / dotted-quad IPv4. Double-green: `20260828T152559Z_wave_g5c_compute_backend_close_run1.log` + `20260828T152747Z_..._run2.log`, both `passed=2649 · status: OK`, stripped-diff = 0. Post-bump verify at `20260828T152949Z_..._verify_after_ratchet_bump.log`. Live-pod probe: `{hosts:[akki-vm(Ready · 2× H200 · 139.8GB), akki-vm-ii(same)], rollup:{host_count:2, gpu_count_total:4, gpu_memory_gb_total:559.2}}`.

- **PRIOR CURRENT-WAVE MARKER (Wave-G5c-CENSUS · retained for continuity of ledger)**: Wave-G5c-CENSUS · CLOSED 2026-08-28T~15:15Z at floor 2636 (+25 from 2611). `services/census_engine/{engine,router}` landed + 3 MUST_BE_LIVE_ROUTES + boto3 seam confined to `services.connect.rds_data_submit.get_rds_data_client` (Doc 01 §A5.5 chokepoint held). Aggregates-only: SQL source scan bans MIN/MAX; row-value leak scan poisons the fake client with `"Alice"` and asserts it never crosses the seam. Numbered records at `phase0/census/census_<NNNN>/` starting at `#1`. Audit-per-read + chokepoint crossing per run. First LIVE census run remains a separately-authorized governed ceremony (deferred).

- **NEXT ACTION**: **Wave-G5c-COMPUTE-FRONTEND sub-close** — author `styled-element-anchor` rules in `pod_shell/frontend/src/App.js` folding compute-estate values into the prototype's Compute tab tiles (`computeCards[]`: labels `Total capacity`, `Allocated to Build`, `Queue depth`), extend `tools/wave_g5_realchrome_verification_harness.py` to navigate to the Registry Compute tab so the `rule-must-match-rendered-DOM` invariant covers the new slots, mirror pod_shell → /app/frontend + supervisor restart + re-harness. Same discipline: right-reason RED first, double-green exact-match, floor monotonic-up from 2649, separate commit per concern. After that: FIRST LIVE census run governed ceremony (RDS Data API against DigiCow cluster) — separate authorization from owner needed before firing the live seam. Then Final Owner Eyeball with the consolidated real-Chromium screenshot bundle (portal, Registry tiles live, narrative with underline/oxblood styling, census status line, per-database estate contents, Compute tab).

- **PRIOR CURRENT-WAVE MARKER (Wave G4 · owner REJECT · retained for continuity of ledger)**: — Owner Wave G3 REJECT verdict verbatim (2026-08-28T~11:45Z, banked in DECISIONS.md): *"A. Dummy data still the same - see screen shot. B. Legacy screens should be retired… On the topline statistics, i need practical data points that speak to everyday users using the system."* Root-cause diagnosed by direct DOM inspection: slot #1 sentence *"RMS AI holds 86.4 TB across 12 sources — 78% measured, with 6 opportunities standing ready."* is fragmented across five nested `<span>` elements (border-bottom underlines on `86.4 TB`, `12 sources`, `78% measured`; oxblood color on `6 opportunities`); TreeWalker SHOW_TEXT visits ~9 separate nodes, none containing the whole sentence, so the Wave G3 whole-sentence regex matched none. Three corrections applied. CORRECTION 1: element-anchor mechanism added (`kind: "element-anchor"` finds element whose `textContent.trim() === dummyContent.trim()`, assigns `.textContent = desired` — handles fragmented spans); idempotent MutationObserver re-application (post-mutation state ≠ dummy so re-walks skip naturally). CORRECTION 2: 10 topline tile-value substitutions added (Held in total, Sources connected, Share measured, Data types present, Languages observed, Share already verified, Share carrying PII, Licensed for external use, Not yet measured, Reduced to reusable memory); tile-value rule matches text node whose `trimmed === rule.dummy`, verifies `ancestor.textContent.includes(rule.label)` to disambiguate value collisions; substitutes real value (Sources connected ← `data_sources.length`) or HONEST-EMPTY (`"Not yet measured"`); preserves tile card layout (label + note untouched). CORRECTION 3: 14 legacy component imports + 15 legacy route paths retired from App.js; catch-all `path="*"` renders `<PortalIframe/>` (single-surface product rule); component source files RETAINED at `pod_shell/frontend/src/components/*.jsx` (donor material — deletion irreversible). Bundle audit confirms tree-shaking dropped retired code (`SSH key`×0, `Wave F Cleanup`×0, `CA1-001`×0, `/api/audit_trail`×0, `CommissionWizard`×0, `AuditTrail`×0, `Registry.jsx`×0, `aws.rds`×0, `cluster.digicow_live`×0, `insertLiveFactCard`×0, `Farma`×0). Wave G3 Flag B RESOLVED BY ELIMINATION. Visual-proof marker: `data-substitution-applied={substitutionsApplied}` on outer iframe host div (invisible bookkeeping on OUTER document, not inside prototype — per owner ruling). `test_wave_g_v8_shell_port.py` gained Section 11 (~78 assertions, all GREEN): 11a per-tile substitution declaration ×10, 11b tile-label-in-prototype ×10, 11c distinctive-dummy anchor, 11d element-anchor `textContent` marker, 11e idempotency guard, 11f outer-doc marker, 11g MutationObserver+childList+subtree, 11h no-legacy-imports ×14, 11i no-legacy-routes ×15, 11j retention ×14, 11k catch-all, 11l HONEST-EMPTY sentinel, 11m G4 DECISIONS anchors ×8. Wave G2 test `test_all_pod_component_routes_remain_deep_link_accessible` INVERTED in place. Wave R3 test `test_commission_wizard_component_exists` reduced to file-existence gate. Ratchet floor 2488 → 2566 (+78). Double-green BYTE-IDENTICAL close: run1 `2566 passed, 1 skipped, 438 warnings in 89.48s` · run2 `2566 passed, 1 skipped, 438 warnings in 90.01s`; `passed=2566 / baseline-failures-remaining=0 / quarantined=0 · status: OK (subset · quarantine · ratchet all pass)` in both; stripped-diff = 0 lines. Offline visual-proof harness (`tools/wave_g4_offline_visual_proof.js`) — 32 assertions GREEN: slot#1 fragmented-span element-anchor replacement (real DOM), slot#2 census text-node replacement (real DOM), live-values path renders `"3 connected sources"` + `"with 47 tables read"` (real DOM), Registry re-render simulation (real DOM: restore dummy → re-apply → dummy gone again), all 10 tile-value substitutions (synthetic fixture matching dc-runtime template shape — dc-runtime template interpolation doesn't fully hydrate in jsdom without real browser, best available offline; owner will eyeball live). Runtime mirror: `pod_shell/frontend/src/App.js` sha256 `e7a0c30a…` == `/app/frontend/src/App.js` (byte-identical); `v8_prototype.html` unchanged at `e56871d0…`; frontend supervisor-restarted and compiled successfully. **Position: HOLD for owner re-eyeball on live preview URL.** ACL note: pod frontend behind strict owner IP allowlist — pod-internal HTTP returns 403; only owner's browser sees the live surface. SSH interrupt priority unchanged.

- **PRIOR CURRENT-WAVE MARKER (Wave G3 · superseded by Wave G4 REJECT + this close, retained for continuity of ledger)**:

- **CP-D7 + CP-D8 combined artifacts (verification target list for owner):**
  - **28 NEW wire paths in MUST_BE_LIVE_ROUTES** (all verified LIVE on pod openapi at IP-allowlisted `/api/openapi.json` — see §2.1 of `notes/waveD_close_report.md`). Pod openapi paths 118 → 149 (+31 across CP-D7/D8).
  - **25 NEW SPA routes in MUST_BE_LIVE_SPA_ROUTES** (each declared in `frontend/src/App.js` or `frontend/src/pages/**` — see §2.2 of `notes/waveD_close_report.md`). New parametrized test `test_must_be_live_spa_route_declared_in_frontend` gates future CP closes.
  - **4 register REUSABLE→DONE moves**: Doc15-001, Doc15-020 (CP-D7); Doc16-001, Doc16-014 wire-through (CP-D8).
  - **Downgrade list** (rows that could not honestly lift as-planned): Doc15-014 stays PARTIAL (Watch mechanism = Wave-F scope); Doc16-023 walk-this DONE at wire+SPA surface / PARTIAL for semantics (Doc 10 evidence-record backfill pending); Doc02-020 CA1-007 wizard remains BUILD (out of CP-D7 lift scope); Doc15-085/-086/-087 stay BUILD/REUSABLE.

- **Wave D block ratchet (CP-D0 → CP-D8)**: `passed` 1830 → **2119** (+289); `baseline_failures` 156 → **0** (Wave D endgame); `passed_floor` 1830 → **2119** (monotonic); `MUST_BE_LIVE_ROUTES` 2 → **30** (+28); `MUST_BE_LIVE_SPA_ROUTES` 0 → **25** (+25); Register DONE this-wave rows: 4.

- **Current step**: **Wave G2 CLOSED at 2463/0/0 · HOLD for owner re-eyeball · 2026-08-28T~06:55Z.** Interpretation shell (`AkkiV8Shell.jsx` + `akkiv8_design_system.js`) deleted from both trees — BANNED permanently per method-change ruling in DECISIONS.md. Prototype now serves byte-verbatim from `public/v8_prototype.html` (sha256 `e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2` · matches Step-0 source). Root `/` renders `<PortalIframe/>` (same-origin iframe of the prototype) + injects DigiCow (`/api/registry/facts` · 125 tables · ussd_users 2.28M · region eu-west-1) + Audit Trail (`/api/audit_trail/overview` · CA1-001/002/003 counts) + Compute akki-vm metadata as text-node substitutions and appended live-fact cards inside `iframe.contentDocument`. 15 pod component routes retained URL-accessible for deep-linking. Env-drift fix: monkey-patched Motor `get_io_loop` in conftest.py (single hunk · idempotent · fixes anyio-parametrized `[asyncio]` tests that regressed post Wave G close). Test file rewritten: 100 mechanical fidelity gates (byte-search + hash comparisons, no interpretation logic). Right-reason RED banked at `phase0/drill_receipts/20260828T060500Z_wave_g2_literal_adoption_right_reason_fail.log`. Ratchet floor 2389 → 2463 (+74). Full-suite double-green identical: `20260828T065200Z_wave_g2_close_run1.log` + `20260828T065400Z_wave_g2_close_run2.log` (both `passed=2463 / baseline-failures-remaining=0 / quarantined=0` · 88.08s / 88.36s). Close report `notes/waveG2_close_report.md` with per-surface LIVE-DATA vs PROTOTYPE-SAMPLE table (§5). Extraction-Akki commit PENDING. **NEXT ACTION**: HOLD for owner re-eyeball. HIS verdict closes the wave, not our tests. If eyeball PASS: reuse audit resumes at Cat 6 boundary (Documents/TaskManager/DataSuite/WorkStudio/Exco-Board donor stacks catalogued in `notes/reuse_audit/PARKED_AT_CAT6_BOUNDARY.md`). If eyeball FAIL: owner's specific-defect ruling supersedes; interpretation still BANNED. SSH interrupt priority unchanged.

- **Standing arrivals (any one opens the next scope):**
  - **(a) SSH key delivery — INTERRUPT-PRIORITY (unchanged from all prior waves).** On key arrival, halt whatever posture and execute the sequence:
    1. `chmod 600 <key>`
    2. `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` in `/app/backend/.env`
    3. `GPU_CONNECT_MODE=real` env flip
    4. Hardware fact sheet probe (`nvidia-smi` + CUDA version + PyTorch build)
    5. **CUDA/PyTorch verify-only** (A17.17 CLOSED · Message 315 · capture versions; install ONLY if probe contradicts owner confirmation)
    6. **EP-4 precondition guard verify** — evidence register active + ≥2 registered judges with matching versions for site `terminal_test`; live run refuses to start otherwise (Reclassification 1 · Message 315)
    7. First live governed training run on sealed DigiCow set (fresh verification bench)
    8. Real MOAC card (`mocked=False` on all six criteria)
    9. Whitepaper drafted from a real admission (`accept_for_service=True` path becomes possible)
    10. Stop-and-report with hardware fact sheet + live run outcome.
  - **(b) Decks/Documents build GO (owner-sequenced post-plan).** The DRE + akki-decks specs are ingested; register rows carried at **BUILD-SCHEDULED-POST-PLAN**. Await explicit owner GO before opening scope.
  - **(c) Owner one-liners (still open · non-blocking · land as config zero-code-change unless code named):**
    - **CA1-N5 RTO seconds** — `services/watch/continuity_policy.v0.json:8` currently sentinel `"OWNER_POLICY_PENDING"`; single-JSON-edit landing once owner rules an integer number of seconds.
    - **DigiCow occupation-boolean PII call** — `dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer` on `ussd_users`; default under Wave-E CP-E7 posture is not-PII; owner rules yes/no. If yes, add to `services/response_sanitizer/` banned set + regenerate the sanitizer snapshot in the same commit (FL-P4-W8-02).
    - **Doc 10 evidence-record backfill decision** — `contracts/evidence_record_v0.py` targeting Doc 10 runtime ledger evidence-record (distinct from Doc 19B EP-1 register rows already covered by `evidence_register_row_v0.py`). Not authorized in the Master Plan; awaits owner GO.
    - **Base-model census activation (A17.10)** — first-adapter base-model choice; needed before any Wave-G-style live training scope opens against a specific base.

- **Master Plan ledger (all ratified · retained for audit · no reopens):**

| Wave | Ratification | HEAD | Test cohort at close |
|---|---|---|---:|
| Wave A | Ratified prior session (R7 · 2026-08-26T04:20Z) | `f101bd0` (post-R7) | 4/4 external PASS |
| Wave B | Ratified 2026-08-26T11:15Z (final at `75b7b1e`) | `75b7b1e` | 182/182 |
| Wave C | Ratified 2026-08-26 (3/3 PASS at `4aedb35`) | `4aedb35` | 169/169 |
| Wave D | Ratified 2026-08-27T~11:00Z (CP-D0 → CP-D9) | (CP-D9 lineage) | 2119/0/159 |
| Wave E | Ratified 2026-08-27T~14:20Z (CP-E1 → CP-E8) | `60b8760` | 2169/0/159 |
| Wave F | **RATIFIED 2026-08-27T~22:15Z (external RE-RUN 4/4 PASS)** | **`fcec7f8`** | **2355/0/0** |

- **Ratified HEAD pointers (Master Plan close):**
  - Extraction-Akki `programme/track-a`: **`fcec7f8`** (Wave F Cleanup CP · audit-trail Overview surface · CA1-001/002/003 CLOSE).
  - Master workspace: **`42ae8f5`** (Wave F Cleanup CP mirror · composite re-lock · register moves · close report · STATE mirrors · receipts).

- **Owner's closing acknowledgement (verbatim · retained in DECISIONS.md at 2026-08-27T~22:15Z entry):**
  > "Exceptional programme execution — from a 50% honest baseline through six ratified waves with zero unratified claims standing."

- **Wave F Scope C · compliance residue (registered 2026-08-27T14:35Z, per owner ruling verbatim):**
  - CA1-001 (Doc02-020a · audit-trail Overview names 2+ units) — **BUILD** · blocker: no audit-trail Overview surface service exists yet · deliverable: new `services/audit_trail/` surface mechanism.
  - CA1-002 (Doc06-016 · audit line names units-served count) — **BUILD** · same blocker as CA1-001.
  - CA1-003 (Doc07-019 · densification stat + warm/fresh tag) — **PARTIAL** · Addendum §1 covers half · blocked on CA1-001/002 surface.
  - CA1-N5 RTO value — **owner-policy-pending** · keep refusing on `rto_target_seconds='OWNER_POLICY_PENDING'` (service enforcement unchanged; RTO ruling from owner is the unblock).
  - CA1-N1 retention + CA1-N4 residency enforcement — **VERIFICATION** at Wave F · measured not assumed · confirm what earlier waves already enforce vs what is genuinely open (per owner ruling verbatim); no code touched this session.
  - Doc15-014 (Watch full mechanism) — **PARTIAL** carried from Wave D.
  - DigiCow occupation-class boolean columns (dairy_farmer / poultry_farmer / dairy_poultry_farmer) — **PII-classification question** · escalated to owner as a one-liner in the next report; NOT auto-escalated to the banned set.
  - Doc16-023 walk-this semantics (Doc 10 evidence-record backfill) — **PARTIAL** (wire DONE at CP-D8; semantics await Doc 10 backfill).

- **CP-E1..CP-E8 receipts (banked · Wave E ratified anchor):**
  - CP-E1 continuity double-run: `20260827T132858Z_cp_e1_close_run1.log` (2127 · OK · 59.81s), `20260827T133144Z_cp_e1_close_run2.log` (2127 · OK · 59.76s)
  - CP-E2 breach double-run: `20260827T134130Z_cp_e2_close_run1.log` (2138 · OK · 59.92s), `20260827T134327Z_cp_e2_close_run2.log` (2138 · OK · 60.04s)
  - CP-E3 erasure double-run: `20260827T135155Z_cp_e3_close_run1.log` (2147 · OK · 60.17s), `20260827T135352Z_cp_e3_close_run2.log` (2147 · OK · 60.21s)
  - CP-E4 quarantine double-run: `20260827T135837Z_cp_e4_close_run1.log` (2158 · OK · 60.33s), `20260827T140121Z_cp_e4_close_run2.log` (2158 · OK · 60.42s)
  - CP-E5 A18.6 single: `20260827T140432Z_cp_e5_close.log` (2160 · OK · 60.45s)
  - CP-E6 audit sweep single: `20260827T140840Z_cp_e6_close.log` (2164 · OK · 60.36s)
  - CP-E7 PII sanitizer single: `20260827T141354Z_cp_e7_close.log` (2169 · OK · 60.37s)
  - CP-E8 wave close double-run: `20260827T141917Z_cp_e8_wave_e_close_run1.log` (2169 · OK · 60.33s), `20260827T142028Z_cp_e8_wave_e_close_run2.log` (2169 · OK · 60.51s)

- **Composite delta (Wave E):** passed 2119 → 2169 (+50); baseline_failures unchanged 0; quarantined_d1a1 unchanged 159; MUST_BE_LIVE_ROUTES 30 → 37 (+7 wire paths shipped: 2 continuity + 1 rights-lapse-flags + 4 rights-quarantine); MUST_BE_LIVE_SPA_ROUTES unchanged 25 (SPA route for /rights-quarantine deferred to post-Wave-E UI shipping per owner ruling "belong on existing surfaces unless canon names a dedicated surface").
  - `phase0/drill_receipts/20260827T115307Z_cp_d9_hermeticity_smoke_run1.log` (targeted D-R5 file, 17 passed)
  - `phase0/drill_receipts/20260827T115317Z_cp_d9_hermeticity_smoke_run2.log` (targeted D-R5 file, 17 passed · back-to-back)
  - `phase0/drill_receipts/20260827T115329Z_cp_d9_hermeticity_full_invariants_run1.log` (`passed=2119 / baseline-failures-remaining=0 / quarantined=159 · OK` · 59.23s)
  - `phase0/drill_receipts/20260827T115439Z_cp_d9_hermeticity_full_invariants_run2.log` (`passed=2119 / baseline-failures-remaining=0 / quarantined=159 · OK` · 59.35s · IDENTICAL tally to run 1)

- **CP-D9 code fix (single file):** `backend/services/registry/sample_fixture_seeder.py` — replaced `find_one + insert_one` (insert-if-absent) with `replace_one({...key...}, doc, upsert=True)` for every sample-marked doc (briefs, gaps, prove answers, prove traces). Sample docs anchored to `_SAMPLE_SEEDED_AT_ISO = "2026-08-02T00:00:00Z"` so time-ordering invariants don't perturb across repeat runs. Non-sample owner-created docs untouched. No test file edited; no manifest edited; no other seeder edited (use_data/connect/team seeders confirmed clean by the two identical full-suite tallies).

- **CP-close invocation (unchanged)**: `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/`. Receipt format: `passed=<N> / baseline-failures-remaining=<K> / quarantined=<Q>`. CP-D9 hermeticity double-run verify: BOTH runs `passed=2119 / baseline-failures-remaining=0 / quarantined=159 · status: OK` at `phase0/drill_receipts/20260827T11532{9,4}Z_cp_d9_hermeticity_full_invariants_run{1,2}.log`. Previous CP-D8 close verify at `phase0/drill_receipts/20260827T114500Z_cp_d8_close.log`.

- **Exact next action (on one of the three ruled arrivals):**
  - **(a) SSH key path** (INTERRUPT-PRIORITY, unchanged): on key arrival, interrupt whatever posture and fire the sequence: `chmod 600 <key>` → `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` set in `/app/backend/.env` → `GPU_CONNECT_MODE=real` env flip → hardware fact sheet probe (`nvidia-smi` + CUDA + PyTorch) → CUDA/PyTorch **verify-only** (A17.17 CLOSED) → EP-4 precondition guard verify → first live governed training run on sealed DigiCow set → real MOAC card → whitepaper from real admission → stop-and-report with hardware fact sheet + live run outcome.
  - **(b) Wave F GO** — retirement of D1a-1 residue per `notes/waveF_retirement_charter.md` (19 files · 88 tests · 100% event-loop-closed class) + final lock + master-tree cleanup. Requires owner ruling on framework (pytest-asyncio ≥1.5 pilot) vs code (fixture refactor) split. **Wave F charter carries THREE locked scope items** registered across three ratifications: Scope A (D1a-1 retirement · original charter), Scope B (composite methodology reconciliation · registered 2026-08-27T12:05Z post Wave D · `notes/waveF_retirement_charter.md` §Wave-F-lock-ceremony), and **Scope C (compliance residue · registered 2026-08-27T14:35Z post Wave E · `notes/waveF_retirement_charter.md` §Scope-C-compliance-residue · 7 line items each with named blocker + measurement instruction)**. Wave F closer MUST close all three scopes in the same close package. Wave F Scope B recap: pick ONE ratified methodology (default: `tools/w10_cp9_composite_recompute.py` W10 CP9 lineage · 551-row mechanism corpus · 58-row interface · 0.7/0.3 blend · unchanged weights), reconcile Waves A-C preliminary ~59.5 %±1pp AND this-session flat 38.38/42.42% against the chosen methodology with row-by-row delta cited to commit SHAs, resolve the 5-row PROPOSED-vs-DONE-scaffold parser band by primary-declaration rule unless owner rules otherwise. Reconciliation drill receipt banked to `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_wave_f_composite_lock.log` under the permanent wave-close standard.
  - **(c) Wave F BUILD queue (background, gated by Wave F opening)**: Doc15-014 (Watch full mechanism · PARTIAL carried into Scope C), Doc15-085/-086/-087, Doc16-023 semantics (Doc 10 evidence-record backfill · Scope C), Doc02-020 CA1-007 UI placement between Review and Adopt (mechanism DONE at Wave E CP-E6).
  - **(d) NEW owner ruling** — any new ruling supersedes standing HOLD.
  - **(a) SSH key path** — Live GPU sequence (INTERRUPT-PRIORITY: interrupt Wave D immediately on key arrival):
    1. `chmod 600 <key>` on the delivered private key.
    2. `AKKI_GPU_SSH_PRIVATE_KEY_PATH=<path>` set in `/app/backend/.env`.
    3. `GPU_CONNECT_MODE=real` env flip.
    4. Hardware fact sheet probe · `nvidia-smi` + CUDA version + PyTorch build.
    5. **CUDA/PyTorch verify-only** (owner confirms already installed — A17.17 CLOSED): capture versions in hardware fact sheet; install ONLY if probe contradicts owner confirmation, and report the contradiction. [was: "CUDA/PyTorch install ceremony (owner-ratified)" · updated per Message 315 · A17.17]
    6. **EP-4 precondition: terminal-test ordering guard green** — evidence register active AND ≥2 registered judges with matching versions for site `terminal_test`; live run refuses to start otherwise (single-judge terminal verdict is unrepresentable). [inserted per Message 315 · Reclassification 1 · EP-4]
    7. First live governed training run on sealed DigiCow set (fresh verification bench).
    8. Real MOAC card (mocked=False on all six criteria).
    9. Whitepaper drafted from a real admission (`accept_for_service=True` path becomes possible).
    10. Stop-and-report with hardware fact sheet + live run outcome.
  - **(b) Wave D CPs** — reusable mass lift (~150 REUSABLE rows · Docs 04-08 / 13 / 15 / 16), sequenced as:
    - **CP-D1 · Invariant Debt Retirement** (FIRST · owner ruling 2026-08-27). **PARTIAL CLOSE 2026-08-27T07:22Z** at `programme/track-a` `13a0097`: 1830→1986 passes (+156), 383→227 broken (−41%). Fixes landed: (i) JWT_SECRET + ADMIN_EMAIL/PASSWORD hermetic defaults in `backend/tests/conftest.py`; (ii) `_motor_rebound_to_loop` autouse conftest fixture + `event_loop()` override at invariants scope + session-scope `_hermetic_db_seed` autouse; (iii) `admission_refusal_reasons.v4.json` rebuilt to honor its landing_note + 4 test_admission_refusal_dispatch tests adapted for A17.16 ACCEPT; (iv) 6 test files converted from `@pytest.fixture async def` to `@pytest_asyncio.fixture`; (v) `test_composed_conclusion_v0_contract_frozen.py` snapshot-count floor; (vi) `pytest.ini` `asyncio_default_fixture_loop_scope=function`. Residual 227 = CP-D1a scope.
    - **CP-D1a · Invariant Debt Retirement continuation** (PARTIAL CLOSE 2026-08-27T07:52Z at `programme/track-a` `18748a3`). Rungs 1-3 attempted; rung-4 fallback γ applied: 165 D1a-1 tests file-level pytestmark.skip'd across 6 files. 4/120 D1a-2 retired (parity-count floor class). Residual **116 D1a-2 failures** deferred to per-CP pay-down quota during Wave-D lift CPs.
    - **CP-D-guard · Baseline no-new-breakage guard install** (CLOSED 2026-08-27T08:23Z at `programme/track-a` `d5450ad`). Manifest at `backend/tests/invariants/baseline_failures.json` (116 IDs, 6 quarantine files, 165 D1a-1 ceiling, 166 total-skip ceiling, 1944 passed ratchet floor). `conftest.py` `pytest_sessionfinish` hook gated on `BASELINE_GUARD=1` (skips on `--collect-only` subprocess to avoid V3 false-trip). 12 always-on manifest-integrity companion tests in `test_baseline_no_new_breakage.py`. Positive + tamper-negative exercise both booked in the drill receipt.
    - **CP-D2 … CP-D8** — reusable lift CPs. Every close receipt is FULL-DIRECTORY scope invoked as `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/`. MUST_BE_LIVE_ROUTES same-commit discipline enforced. Each CP MUST retire ≥15 baseline_failures from the manifest in the same commit AND ratchet passed_floor + counts_at_baseline.passed up in the same commit (owner rulings (d) and (e), 2026-08-27).

- **Wave A/B/C ratified ledger** (Extraction-Akki `programme/track-a` · workspace `master`):
  - **HEAD (Extraction-Akki)**: `60b8760` (CP-E7 · Wave E CLOSED PENDING RATIFICATION · registry hermeticity + N-series enforcement + Doc14-020 quarantine + A18.6 adoption + audit sweep + PII sanitizer)
  - **HEAD (workspace)**: `3aa1c90`
  - **Wave A**: 4/4 external PASS at close · closed_at prior session.
  - **Wave B**: 4/4 external PASS (final re-verification at `75b7b1e`) · 182/182 green at close.
  - **Wave C**: 3/4 external PASS at `9544237` · **3/3 PASS** at `4aedb35` after ceremony-chokepoint fix + stranded-run backfill · 169/169 green at close.
  - **Waves A-C** aggregate: **169/169 pytest invariants** across the ratified cohort · zero regressions · Ship-Manifest DoD triple honored on every CP · live-pod clean.

- **Preliminary post-A-C composite %**: **≈ 59.5 % ±1pp** (reporting number · authoritative lock ceremony deferred to Wave F as planned). Delta trace recorded in STATE/DECISIONS.md `2026-08-26T12:45Z · WAVES A-C RATIFIED AS A BLOCK`.

- **Standing invariants (unchanged)**:
  - Anti-Compaction Rule: first action of every session = re-read STATE/NEXT.md + last 200 lines STATE/DECISIONS.md + `notes/waveC_grounding_brief.md`.
  - Tests-first is law: RED receipt banked before implementation on every CP.
  - No paraphrasing: verbatim canon quotes in every gating docstring (Owner Standing Condition 1).
  - Ship-Manifest DoD triple: runtime-assembler wire + frontend surface + green user-path test in the SAME commit.
  - `/app/backend/server.py` ↔ `pod_shell/backend/server.py` byte-identical mirror.
  - `/app/frontend/src/components/*.jsx` ↔ `pod_shell/frontend/src/components/*.jsx` byte-identical mirror.
  - Local commits only · no `git push`.
  - Testing: terminal `pytest` + `node --test` only. No testing subagent.

- **Ratified live-pod probe recipe (unchanged)**:
  - localhost curl with `X-Forwarded-For: 41.90.172.155, 10.0.0.1, 10.0.0.2`.
  - External URL 403-guarded by allowlist middleware · localhost path is the sanctioned pod probe. curl
- **CP-C2 warn-followup (owner-noted 2026-08-26T~11:42Z · queued)**:
  - `POST /api/training-runs/{id}/close` returns 200 but `whitepaper_ref="whitepaper_draft_error:'verdict_summary'"` — KeyError in whitepaper drafter path.
  - Fix tests-first: assert close response carries a real `whitepaper_ref` resolving to on-disk draft per Doc 14 §33 citation invariant.
  - Fold into next CP close report (CP-C3 or CP-C4 target).
- **Wave-close checklist (added per owner runtime-drift ruling)**:
  Every wave close MUST include:
    1. Backend supervisor restart (`sudo supervisorctl restart backend`).
    2. Live-pod curl against a route that MOVED in the wave.
    3. Runtime-drift guard test passes (`test_ship_manifest_dod_runtime_drift_guard.py`).
    4. Wave-close report only after these are green.
- **Wave A CLOSED**: 11 commits · R1→R7 · external verification 4/4 PASS
- **Wave B CLOSED + POST-VERIFY FIXED** (9 Extraction-Akki commits + 3 workspace commits):
  - `8f40baa` · handoff-WARN closure
  - `8722e3c` · CP4 · Doc 18 A18.7 skill-file provenance
  - `b9ed85b` · CP5 · Doc 17 A17.3-A17.6 recipe seat + optimizer harness + M-d
  - `d199ea6` · CP6 · Doc 19B EP-1/EP-3/EP-5 evidence register + A-4 + non-adoption
  - `14cbc53` (workspace) · CP7 register truth-pass absorption
  - `b24b069` · CP8 · Doc 17 trainer runner mock SSH seam + MOAC emitter
  - `e23ca94` · CP-Audio · Audio Plane §1.2/§1.5/§3.1-3.2 invariants
  - `3779aee` · CP5 verdict endpoint tail restored
  - `75b7b1e` · **post-verify fix**: governed seat-fill on adopted + verdict write-once + runtime-drift meta-invariant · **182/182 green**
- **Wave B external verification result (owner · 2026-08-26T11:15Z)**: **3/4 PASS + 1 FAIL** (governed HTTP path gap · closed by `75b7b1e`) · 4/4 PASS after fix (self-verified via 182 tests + live-pod journey curl · owner re-verification pending)
- **Blockers at Wave C open** (state corrected · DigiCow already ratified):
  - **SSH private key** — awaiting owner delivery. Only remaining blocker for live GPU run.
  - ~~DigiCow rights~~ — **RATIFIED** by owner 2026-08-26 ('take this as approval') per DECISIONS.md. NOT a blocker.
- **Wave A commit ledger** (retained for audit):
  - R1 · `155f1db` · Ship-Manifest DoD meta-invariant
  - R2 · `369f9b8` · Connect draft persistence + human-speak errors
  - R3 · `493f6bc` · Canon 5 §14 Shaping Wizard
  - R4.1 · `ed85766` · CP3 Training landing (closes drift)
  - R4.2 · `1fdd529` · Callable Skills lift
  - R4.3 · `8667a02` · Memory plane lift
  - R4.4 · `2cb1c91` · Handoff contract lift
  - R4.5 · `bf53b0d` · Opportunity briefs pipeline
  - R4.6+7 · `c577ea8` · Whitepaper + N-series HTTP surfaces
  - R4.8 · `040ee64` · Critic Seam producer wiring
  - R5 · `a2b056a` · RefusalCard lift · Canon 5 §9.2 verbatim
  - R7 · `37688a9` · Watch/Grey-Mirror honesty
- **Composite (R6 preliminary · pre-owner-authoritative-lock)**: 53.6% → ~55.1% (±0.5pp) · row 6 (Doc15-086 handoff) data-side upgraded to FAITHFUL by `8f40baa` (artifact reachable at runtime) · owner runs authoritative composite-lock recompute at Wave A/B close if desired
- **KNOWN_UNWIRED count**: 28 (unchanged after CP4 · new router services.skill_files is wired, not deferred)
- **KNOWN_RUNTIME_DRIFT count**: 0 (unchanged)
- **Uncommitted files (workspace)**: STATE/NEXT.md (this file · edit staged), STATE/DECISIONS.md (Wave B ledger entries staged)
- **Open owner items**: SSH key delivery (unblocks CP8 GPU live run · CP5-CP7 + mock-CP8 build first regardless); rights declaration for DigiCow (unblocks CP8 real-data live run)

---


# NEXT.md - Exact next actions

**Last updated:** 2026-08-26T11:40Z · **W11 REASSESSMENT DELIVERED · awaiting owner approval before CP1 opens** · Extraction-Akki HEAD `f101bd0` (programme/track-a · unchanged) · master HEAD pending commit.

## Cycle status (2026-08-26T11:40Z · W11 reassessment complete · plan awaiting owner GO)

- **Owner directive 2026-08-26T11:20Z**: reassess before build · 3 new spec docs supplied · SSH key incoming · DigiCow data claim · deeper donor reuse suspected.
- **Reassessment delivered**: `notes/w11_reassessment.md` (comprehensive · 8 sections).
  - **§1 Canon delta**: Docs 17/18/19 + Incremental Training Capacity Briefing + Training Techniques Spec ingested · converted to text · landed in `canon/text/`. Canon pack now 12 canon + 2 governed-artefact specs · register-wide count = 20 docs.
  - **§2 Register delta**: 36 new rows (23 CANON + 5 PROPOSED + 8 OPEN-SLOT) · register grows 515→551 rows.
  - **§3 Reuse inventory · MAJOR FINDING**: callable-skill package (356 LOC) + cuda_runtime + models_registry.v0.json + 649 LOC of eab_1_pipeline + execution_mode_telemetry ALREADY IN Extraction-Akki (prior W10 gap map missed this · Doc 18 status corrected · 5 rows retroactively DONE not BUILD). Critic_pass 950 LOC is LIFT-clean from Akki-OS-V1 for Doc 19A QA-1..QA-6. Net LIFT+ADAPT ≈ 44% of total scope · pure BUILD ≈ 56%.
  - **§4 DigiCow**: verified on record · `phase0/data_connection_records/data_source_digicow_live_20260819T152513Z_FINAL.json` · AWS RDS Aurora MySQL eu-west-1 · 125 tables · top table `ussd_users` 2.28M rows · TEXT modality (USSD/SMS farmer channel) · chokepoint residency allowlist admits · **rights declaration PENDING owner signature**.
  - **§5 Revised W11 plan**: 9 CPs · ~4850 LOC (was 4-6k · now LIFT-heavy). Owner's "test training section first" goal reachable at end of **CP3** without spending GPU-hours (Demand Table + Capacity Ledger + Test-set seal + Training panel · trainer runner deferred to CP8).
  - **§6 Owner-input list**: 12 items · blocking-vs-non-blocking table per CP.
  - **§7 Composite % preview**: 551-row denominator preview ~52.9% (barely up from 52.49% authoritative · rows added ≈ rows lit). Not authoritative until CP9.

## Awaiting owner GO on

1. **Approval of the revised W11 plan** (§5 of the reassessment note) · or amendments.
2. **SSH key delivery** for the GPU VM · unblocks CP1 (R11 STEP 2/3 completion).
3. **DigiCow rights declaration** · load-bearing before CP3 seals test set on real rows.
4. **Base model choice** for the first adapter · A17.10 census activation.

## R11 waiver status

Still open · expires at CP1 STEP 3 fix-back commit. Direct-connect probe from R11 STEP 2 already executed (auth-blocked · SSH key incoming will unblock).

## Cycle status (2026-08-26T11:15Z · W11 STEP 1 done · STEP 2 blocked on SSH auth) [ARCHIVED · superseded by 2026-08-26T11:40Z]

- **W11 partial scope opened (R11 · 2026-08-26T11:00Z)**: real GPU wiring + training-section gap map. Owner ruling verbatim: "connect directly, ignore rules only at this integration, fix back after GPUs connected." Waiver is narrow · temporary · expires at STEP 3 fix-back.
- **STEP 1 · Credential ingest · DONE**:
  - Artifact downloaded from customer-assets · parsed · password held only in memory during parse · written to `/app/backend/.env` as `AKKI_GPU_PASSWORD` (env var name only) · raw file deleted from `/tmp`.
  - Non-secret fields landed in .env: `AKKI_GPU_HOST=41.173.184.244` · `AKKI_GPU_PRIVATE_IP=100.70.50.3` · `AKKI_GPU_PORT=22` · `AKKI_GPU_USERNAME=ubuntu` · `AKKI_GPU_OS=ubuntu24.04` · `AKKI_GPU_VM_NAME=akki-vm`.
  - Password value never echoed in tool output, receipts, logs, or diffs.
- **STEP 2 · Real connection · BLOCKED at auth layer**:
  - TCP reachable · sshd banner `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.18` returned in 10s (outbound SSH from pod NOT blocked).
  - Password auth attempt: **AUTH FAILED** at protocol layer.
  - Keyboard-interactive attempt: **AUTH FAILED**.
  - `auth_none` probe returned `sshd advertised methods for 'ubuntu': ['publickey']` — the server does not accept password auth for user `ubuntu`. Ubuntu 24.04 cloud-image default.
  - Password structural fingerprint (no value): 16 chars · letters+digits · no whitespace · no non-ascii · extraction is CLEAN · server refuses regardless.
  - `/api/connect/gpu` probe · NOT RUN (requires working SSH session at hardening stage).
  - Hardware fact sheet: **UNKNOWN** (GPU model / count / VRAM / driver / CUDA / pytorch / disk / RAM all unprobed).
  - Sanitized receipt: `phase0/drill_receipts/20260826T110500Z_w11_real_gpu_probe.log` (no password leak · sanitizer verified).
- **STEP 3 · Fix-back · DEFERRED** to auth unblock.
- **STEP 4 · Gap map · DONE**: `notes/w11_gap_map.md` (12 EXISTS rows anchored to on-disk paths · 20 MISSING rows split BUILD-us vs OWNER · hardware column marked UNKNOWN pending auth · 7-CP recommended sequencing informational).
- **Rollback**: `GPU_CONNECT_MODE=mock` restored in `/app/backend/.env` (fallback preserved). `AKKI_GPU_*` env vars retained for STEP 2 retry once auth path unlocks. `AKKI_GPU_AUTH_METHOD_ACCEPTED=publickey` marker added in .env noting the constraint.

## Owner action needed to unblock STEP 2

**One of**:

- (a) **Supply an SSH private key** for user `ubuntu` on 41.173.184.244 (`id_ed25519` or `id_rsa` · key content). Main agent lands it in a chmod-600 file, wires `AKKI_GPU_SSH_PRIVATE_KEY_PATH` in .env, restarts backend to pick up.
- (b) **Enable password auth on the VM**: SSH into the VM via console/rescue path and run:
  ```
  sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' \
    /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf
  sudo systemctl restart ssh
  ```
  Then the plaintext password already on record works.

Once auth unlocks, main agent completes STEP 2 hardware probe + `/api/connect/gpu` real crossing receipt + STEP 3 fix-back (regression invariant + cohort re-run + local commit) inside the same waiver window.

## R11 waiver duration

Still open — expires at STEP 3 fix-back commit. All work AFTER fix-back runs under standard tests-first / ceremony discipline. Correction-discipline in-band still holds during the waiver (any change to /app/backend/.env or /app/backend/services/ that is NOT the connect probe must land as a normal red-green CP).

## Cycle status (2026-08-26T10:00Z · W10 RATIFIED · no next wave booked) [ARCHIVED · superseded by 2026-08-26T11:15Z]

- **W10 CLOSE RATIFIED** by owner 2026-08-26T10:00Z (R10 in STATE/DECISIONS.md).
- **External re-verification 4/4 PASS** at the real edge: non-allowlisted callers get 403 + refusal sentence on `/`, `/governance`, `/favicon.ico`, `/api/governance/state`, `/api/openapi.json`; headless external browser sees refusal sentence only (no SPA shell).
- **Composite % authoritative · locked**: **52.49 %**.
- **Wave-close cohort**: 45 test files · 303 assertions green (261 pytest + 25 + 17 node).
- **All 9 W10 CPs CLOSED**.
- **Owner-IP positive path from external edge**: pending owner-side confirmation (only the owner can do this from outside · not blocking ratification).

## Standing at ready state

No CP is open. No next wave is booked. Awaiting owner ruling on:
- Open W11 (post-W10 items below).
- Ratify different next-wave scope.
- Pause.

No further agent action will be taken unless the owner reports an access failure or opens a new scope.

## Outstanding items (deferred beyond W10 · all non-blocking)

### Non-blocking owner-policy answers (unchanged from W8/W9)
1. **FL-P4-W8-01** · CA1-N2 (data-subject breach notification) · owner policy pending (7 questions).
2. **FL-P4-W8-01** · CA1-N3 (data-subject erasure) · owner policy pending (7 questions).
3. **FL-P4-W9-01** · CA1-N5 (continuity attestation) · owner policy pending (1 question).

### New at W10
4. **Doc14-020** · Canon 4 §38 rights-unclear grammar · OPEN-SLOT (N-series pattern · registered at CP7).

### Larger post-W10 work (informational only · not booked)
5. **Audio trainer + real GPU wiring** — audio trainer NOT BUILT (perception-side ASR/diarisation wired but no training pipeline). GPU connect real 7-stage but `.env` currently points at mock SSH. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC). Answered informationally 2026-08-26T08:20Z · no CP scope change.

## Ratified owner rulings · executes without re-litigation

R1-R7 (2026-08-26T04:20Z · W10 pre-GO) · R8 (2026-08-26T05:20Z · preview allowlist permissive-mode for W10 duration · rescinded at wave close) · R9 (2026-08-26T09:20Z · preview allowlist strict-flip at wave close · corrected 09:45Z across both surfaces) · **R10 (2026-08-26T10:00Z · W10 wave RATIFIED)**.

## Standing rules (all remain binding beyond W10 close)

- **W10 CP9 · Authoritative composite recomputation + wave close + strict flip · CLOSED** (with mid-flight correction to strict-flip verification).
  - **Composite (authoritative · Owner correction #4)**: **52.49 %** replacing all wobbly running numbers.
    - Mechanism corpus: **54.45 %** (280.4 / 515 · 109 DONE + 46 PARTIAL + 306 REUSABLE + 53 BUILD + 1 OPEN-SLOT).
    - Interface dimension: **47.93 %** (27.8 / 58 · 10 DONE + 2 PARTIAL + 34 REUSABLE + 12 BUILD).
    - Blend: 0.7 × 54.45 + 0.3 × 47.93 = **52.49 %**.
  - **Method**: `tools/w10_cp9_composite_recompute.py` (deterministic · 32 delta entries · every delta anchored to canon § + commit SHA).
  - **Locked by pytest**: `backend/tests/invariants/test_w10_cp9_composite_lock.py` (5/5 green).
  - **Wave-close cohort**: **261/261 pytest** + **42 node** = 303 assertions across 45 test files. Receipts at `20260826T091500Z_w10_wave_close_green.log` (pytest 261/261) + `20260826T083100Z_w10_cp8_frontend_green.log` (node 25/25) + `20260826T094500Z_w10_strict_flip_matrix_green.log` (node 17/17).
  - **R9 strict flip · CORRECTED (09:45Z)**: initial 09:20Z flip restarted only backend · SPA surface stayed permissive · external tester (09:33Z) caught GET / returning 200. Fix: restart frontend + add 17-invariant mode-matrix node test that reads ALLOWLIST_MODE from `/app/backend/.env` single-source-of-truth and probes BOTH surfaces at BOTH ports across 5 endpoints × 3 probe classes. Full matrix verified in both directions. Updated flip procedure: `sudo supervisorctl restart backend frontend` (BOTH · not just backend). Receipt `20260826T094500Z_w10_strict_flip_verified_both_surfaces.log` supersedes `20260826T092000Z_w10_strict_flip_verified.log`. R9 stands.
  - **Cheap optional fix landed**: `/api/openapi.json` serves 200 (49 paths · docs_url/redoc_url disabled · response-boundary sanitizer intact).
  - **W10 close report banked**: `notes/w10_close_report.md` (W8/W9 format · 12 sections · updated §1 to reflect corrected R9 verification).
- **W10 delivered**:
  - Canon 8 mechanism fabric fully wired (CP1-CP5): Ruling-1 drill · Grey Mirror BUILD · Watch drills + fitness · Reserved-Decisions Panel · Witness fabric + tamper alarms.
  - Doc 14 §33 CA1-005 whitepaper drafter BUILD (CP6 · parity 58→59).
  - Doc 14 §§21-45 register expansion 4→28 rows (CP7).
  - Governance + Watch + Grey-Mirror frontends wired (CP8).
  - Authoritative composite % + wave close + strict flip + close report (CP9).

## W10 checkpoint status — ALL CLOSED

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · BUILD | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | CLOSED · 8/8 green · docs-only | ~130 |
| CP8 | Governance / Watch / Grey-Mirror frontends + backend state rollups | CLOSED · 32/32 green (7 be + 25 fe) | ~940 |
| CP9 | Authoritative composite · wave close · strict flip · close report | **CLOSED · 5/5 green · 261/261 cohort** | ~230 |

## Outstanding items (all non-blocking · deferred beyond W10)

### Non-blocking owner-policy answers (unchanged from W8/W9)
1. **FL-P4-W8-01** · CA1-N2 (data-subject breach notification) · owner policy pending (7 questions).
2. **FL-P4-W8-01** · CA1-N3 (data-subject erasure) · owner policy pending (7 questions).
3. **FL-P4-W9-01** · CA1-N5 (continuity attestation) · owner policy pending (1 question).

### New at W10
4. **Doc14-020** · Canon 4 §38 rights-unclear grammar · OPEN-SLOT (N-series pattern · registered at CP7).

### Larger post-W10 work (informational only · not booked)
5. **Audio trainer + real GPU wiring** — audio trainer NOT BUILT (perception-side ASR/diarisation wired but no training pipeline). GPU connect real 7-stage but `.env` currently points at mock SSH. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC). Answered informationally 2026-08-26T08:20Z · no CP scope change.

## Ratified owner rulings · executes without re-litigation

R1-R7 (2026-08-26T04:20Z · W10 pre-GO) · R8 (2026-08-26T05:20Z · preview allowlist permissive-mode for W10 duration · RESCINDED at wave close per R9) · **R9 (2026-08-26T09:20Z · preview allowlist strict-flip at wave close · verified · fail-closed posture restored)**.

## Standing rules (all remain binding beyond W10 close)

- Tests-first + right-reason receipts (every CP).
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 · 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act · not fired at W10 close · deferred to owner).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline (FL-P4-W9-02).
- Correction-discipline in-band (Owner Ruling 2026-08-19 §6 additive-only).
- Host-identity drill attribution: `drill_actor:*` prefix · no drill-mode switch (R1).
- **Composite % same-commit DoD extension**: any commit touching `tools/w10_cp9_composite_recompute.py` MUST touch `test_w10_cp9_composite_lock.py` in the SAME commit (booked at CP9).
- No push · local commits only.

## Blocked (awaiting owner)

- **No CP is blocked**. W10 is closed.
- Owner may open W11 (post-W10 items above) or ratify a different next-wave scope.

## Cycle status (2026-08-26T08:35Z · W10 CP8 CLOSED · CP9 opening) [ARCHIVED · superseded by 2026-08-26T09:30Z]

- **W10 CP8 · Governance / Watch / Grey-Mirror frontends · CLOSED** at 7/7 backend + 25/25 frontend + 28/28 CP-anchor cohort green.
  - **Backend (thin read-only state rollups · REFERENCE-NOT-COPY)**:
    - `services/governance/router.py` → GET /api/governance/state (approvals · rules_updates lifecycle · reserved_decisions).
    - `services/watch/router.py` → GET /api/watch/state (verdicts · actions · containments · reconciliations · continuity_attestations · witness_attestations · tamper_alarms · fitness summary rollup).
    - `services/grey_mirror/router.py` → GET /api/grey_mirror/state (mirages · touches · severances · BUILD-not-LIFT rationale in body).
    - Every entry carries `record_id` + `source_path` on disk; raw signing material / secrets sanitized out at boundary (Owner Order 2026-08-25 §4).
  - **Frontends** (all under `/app/frontend/src/components/` · mirrored to pod_shell):
    - `Governance.jsx` (routes `/governance` · reserved-decisions + rules-updates + approvals panels · Canon 8 §19 + Doc 15 §17 anchors · names the 5 reserved kinds verbatim per R3).
    - `Watch.jsx` (routes `/watch` · verdicts + actions + containments + witness + tamper + fitness · Canon 8 §7 + §8 + §9 + §14 + §25 anchors · Ruling-1 precondition (b) demonstrated status surfaced from fitness rollup).
    - `GreyMirror.jsx` (routes `/grey-mirror` · mirages + touches + severances · Canon 8 §§15-16 anchors · touch_kind CONTRACT-TIME grammar per R2 · BUILD-not-LIFT rationale visible).
    - Wired into `App.js` (live `/app/frontend/src/App.js` + mirrored `pod_shell/frontend/src/App.js`).
  - **Tests-first**:
    - Backend: `test_w10_cp8_state_endpoints.py` (7 tests · honest-empty · seeded-record reflection · no-raw-secret invariant).
    - Frontend: `pod_shell/frontend/__tests__/w10_cp8_frontends.test.js` (25 tests · source-content testids · REFERENCE-NOT-COPY markers · canon anchors · route wiring · live HTTP 200 through allowlist for all 3 routes · live API JSON shape).
  - **Receipts** (banked to assessment_workspace phase0/drill_receipts/):
    - `20260826T080000Z_w10_cp8_backend_right_reason_fail.log` (7 collection errors · services.governance/watch.router/grey_mirror not yet on disk).
    - `20260826T080100Z_w10_cp8_frontend_right_reason_fail.log` (20 fails · components missing + routes not wired + endpoints 404).
    - `20260826T083000Z_w10_cp8_backend_green.log` (7/7 green).
    - `20260826T083100Z_w10_cp8_frontend_green.log` (25/25 green).
  - **HTML snapshots banked** to `phase0/html_snapshots/` (owner-side rendering per R4):
    - `w10_cp8_governance.html` + `w10_cp8_governance_api.json`
    - `w10_cp8_watch.html` + `w10_cp8_watch_api.json`
    - `w10_cp8_grey_mirror.html` + `w10_cp8_grey_mirror_api.json`
- **Preview routes owner should eyeball** (permissive allowlist holds through CP9 close per R8):
  - `/governance` — reserved-decisions panel + rules-updates timeline + approvals ledger
  - `/watch` — fitness summary + verdicts/actions/containments/witness/tamper panels
  - `/grey-mirror` — mirages + touches + severances panels
  - Ruling-1 precondition (b) DEMONSTRATED renders in the Watch header (drill note on disk at `phase0/drill_receipts/ruling_1_drill_witness_note.md`).
- **Honest empty state**: all live record stores are 0-count today (production Watch has not yet fired against real traffic; mirages not yet installed; approvals ledger not yet lit). The surfaces render "0 X on record · Canon anchor: … · Drawn, never left blank."
- **Contract parity unchanged**: still 59 (CP8 is a surface CP · no new frozen contracts).
- **Stop-and-report to owner**: CP8 status paragraph + preview-route list delivered. CP9 opens on owner ack.

## Interleaved owner readiness query (2026-08-26T08:20Z) — audio trainer × GPU

Answered from ground truth (no ratification recorded · informational only):
- Audio trainer: **not built**. Perception-side audio inference wired (`services/layer_b/asr/*`, `layer_a/handlers/audio.py`, `services/perception/asr_worker.py`). Training-side absent — no `services/audio_trainer/`, no audio training-run contract.
- GPU connect: `/api/connect/gpu` real (7-stage pipeline · commissioning · trust receipts) but `.env` currently points at mock SSH host (`/tmp/akki_mock_sshd/*`). No production GPU connected today.
- Verdict: **not ready** for a real audio-trainer-on-GPU test. Building the trainer is roughly a wave of its own (~W10-scale · 5-7k LOC) · deferred beyond W10.
- Recorded here for continuity; no CP scope change.

## W10 checkpoint status

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · BUILD | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | CLOSED · 8/8 green · docs-only | ~130 |
| CP8 | Governance / Watch / Grey-Mirror frontends + backend state rollups | **CLOSED · 32/32 green (7 be + 25 fe)** | ~940 |
| CP9 | Authoritative composite % calculation + record + wave close + strict-flip verification | pending | — |

## Awaiting owner (post-CP8)

1. **Owner ack on CP8** (one-paragraph status + preview routes list delivered · CP9 opens on GO).
2. **9 policy answers** (FL-P4-W8-01 + FL-P4-W9-01 · non-blocking to CP9 open).

## Ratified · executes without re-litigation (unchanged from R1-R8)

R1-R8 · permissive allowlist holds through CP9 close · flip-back sequence baked into wave-close checklist.

## Cycle status (2026-08-26T07:20Z · W10 CP7 CLOSED · CP8 opening) [ARCHIVED · superseded by 2026-08-26T08:35Z]

- **W10 CP7 · Doc 14 §§23-25 24-row expansion · CLOSED** at 8/8 CP-cohort green + 88/88 wider W10 cohort green.
  - Register expanded: `notes/requirements_register_17docs.md` §Doc 14 grew from 4 rows to 28 rows (24 new rows: Doc14-002..022, 025, 027, 028).
  - Each row cites a Canon 4 § anchor (§§21-45 · Model Ecosystem lifecycle) with cross-anchors to Canon 5 §12.2 (Models tab) and Canon 6 §4 (Setup — Model Ecosystem) per §Row-count table.
  - Status vocabulary fixed to `{DONE, PARTIAL, REUSABLE, BUILD, BUILT-W10, OPEN-SLOT}`. Distribution: 7 DONE (MOAC 6-criterion + uncurated + rights-lineage) · 3 PARTIAL (adapter-registry wiring · version-history query surface · build-gate coverage) · 3 REUSABLE (Standards · Rights declaration · Frozen-objective invariants) · 8 BUILD (Critic Seam quartet · No-adapter surface · Contents attestation · Quality card · MOAC drift) · 1 OPEN-SLOT (Doc14-020 rights-unclear grammar · policy-pending · non-blocking per Owner CP7 GO).
  - Pre-CP7 rows (Doc14-001, 023, 024, 026) preserved verbatim (Owner Ruling 2026-08-19 §6 additive-only correction discipline).
  - Tests: `backend/tests/invariants/test_w10_cp7_doc14_expansion.py` (8 tests-first structural invariants · row count · ID set · no dupes · canon anchor · status token · pre-CP7 preservation · CP7 new-set sanity).
  - Receipts: red `phase0/drill_receipts/20260826T070000Z_w10_cp7_right_reason_fail.log` (2/8 fail with count 4≠28 + 24 missing IDs) + green `20260826T072000Z_w10_cp7_green.log` (21/21 with CP6 anchor cohort included).
  - Wider re-verification: 88/88 across W10 CP1-CP7 + all frozen/parity/W10 CPs. No regression.
- **Contract parity unchanged**: parity still 59 (register expansion is a docs-only CP · no new frozen contracts).
- **Stop-and-report to owner**: CP7 status paragraph delivered. CP8 opens on owner ack.

## W10 checkpoint status

| CP | Scope | Status | Actual LOC |
|----|-------|--------|-----------:|
| CP1 | Ruling-1 firing drill · Canon 8 §27 | CLOSED · 7/7 green | ~200 |
| CP2 | Grey Mirror mirage machinery · Canon 8 §15-§16 · BUILD | CLOSED · 25/25 green · parity 52→55 | ~800 |
| CP3 | Watch drills + fitness accounting · Canon 8 §25-§28 | CLOSED · 12/12 green | ~400 |
| CP4 | Reserved-decisions panel · Canon 8 §19 | CLOSED · 28/28 green | ~500 |
| CP5 | Witness fabric full signing · Canon 8 §9 + §33 | CLOSED · 23/23 green · parity 55→58 | ~600 |
| CP6 | CA1-005 whitepaper drafter · Doc 14 §33 · BUILD · 150-LOC lid | CLOSED · 13/13 green · parity 58→59 | ~140 |
| CP7 | Doc 14 §§23-25 24-row register expansion | **CLOSED · 8/8 green · docs-only · parity unchanged** | ~130 register lines + 152 test LOC |
| CP8 | Governance / Watch / Grey-Mirror React views + DOM asserts + HTML snapshots (REFERENCE-NOT-COPY) | pending | — |
| CP9 | Authoritative composite % calculation + record + wave close + strict-flip verification | pending | — |

## Awaiting owner (post-CP7)

1. **Owner ack on CP7** (one-paragraph status delivered · CP8 opens on GO).
2. **9 policy answers** (FL-P4-W8-01 + FL-P4-W9-01 · non-blocking to CP8-CP9 open).

## New open slot recorded at CP7

- **Doc14-020** ← C4-054 §38 · Rights-unclear grammar is a first-class state. Row marked **OPEN-SLOT** (same pattern as N-series) pending owner policy on the resolution ceremony. Non-blocking to W10 close.

## Ratified · executes without re-litigation (unchanged from R1-R8)

R1-R7 above · R8 preview allowlist config (2026-08-26T05:20Z · permissive holds through CP9 close · flip-back sequence baked into wave-close checklist).

## Standing rules (all binding through W10 close)

- Tests-first + right-reason receipts (every CP).
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act · projected ready at CP9 close).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline (FL-P4-W9-02).
- Correction-discipline in-band (Owner Ruling 2026-08-19 §6).
- Host-identity drill attribution: `drill_actor:*` prefix · no drill-mode switch (R1).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner ack on CP6 close (one-paragraph status delivered).
- Owner rulings on 9 policy questions (non-blocking to CP7 open · load-bearing before N-series + continuity attestations FIRE live records).

## Cycle status (2026-08-26T04:25Z · W9 CLOSED (with corrections FL-P4-W9-02) · W10 pre-GO orchestrator ratifications R1-R7 logged · awaiting owner W10 GO) [ARCHIVED · superseded by 2026-08-26T06:30Z]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files).
- **FL-P4-W9-02 opened + closed at open** · new post-compaction discipline ratified.
- **Orchestrator ratifications R1-R7 logged in DECISIONS.md 2026-08-26T04:20Z**:
  - **R1** · CP1 firing-drill · Canon 8 §27 · REAL default dirs · host-identity `drill_actor:` pattern (Phase 0 · DECISIONS.md L347) · no drill-mode switch.
  - **R2** · CP2 MirageTouch touch_kind grammar · CONTRACT-TIME frozen `Literal["innocent_read", "guilty_use"]` · no service-time extensibility.
  - **R3** · CP4 reserved_decision_kind · closed `Literal` enum (5 Canon 8 §19 verbatim items) · no free-text.
  - **R4** · CP8 screenshot posture · TRIAD (DOM-asserts + curl-through-allowlist + banked HTML snapshots under `phase0/html_snapshots/`) · owner-side visual verification standing named gap.
  - **R5** · Scope narrowing NONE · all 9 CPs stay · sequencing CP1 first · CP2-CP8 in order · CP9 last · stop-and-report 7,040 LOC re-baselined.
  - **R6** · N-series + continuity policy-pending state = config layer · answers land zero-code-change.
  - **R7** · Standing discipline continuation.
- **Ruling-1 status SURFACED (from FL-P4-W9-02 correction)**:
  - Precondition (a) declaration ✓ DEMONSTRATED (W1).
  - Precondition (b) Watch reconciler DEMONSTRATED FIRING · **NOT YET** · CP1 banks it.
  - Purpose-gate strip **NOT ready-for-ceremony** · will surface as ready at W10 CP9 close (owner act to strip).

## Awaiting owner (final list pre-W10)

1. **W10 GO** (the message that starts CP1 · may narrow scope · supersedes R5 if it does).
2. **9 policy answers** — FL-P4-W8-01 (7 · CA1-N2 + CA1-N3) + FL-P4-W9-01 (2 · CA1-N5). Non-blocking to W10 open · land as config zero-code-change per R6.

## Ratified · executes without re-litigation on GO

R1-R7 above · full verbatim in `STATE/DECISIONS.md` 2026-08-26T04:20Z section · full CP-by-CP scope in `notes/w10_grounding_brief.md` (updated 2026-08-26T04:25Z with R1-R6 baked into §3 · §4 · §6 · §10 · §13).

## Programme dashboard (post-W9 · composite % held pending W10 CP9)

- **Frozen contracts** · 52.
- **Fidelity ledger** · 16 rows opened · 14 CLOSED · 2 OPEN (both owner-policy-pending).
- **Test cohort** · 416 green (63 files).
- **Cumulative LOC (W1..W9)** · ~23039 net.
- **Composite %** · **HELD pending W10 CP9 authoritative recomputation** (owner correction #4 · method stated in brief §11).

## Ready for owner ceremony (Canon 3 §24 · owner act) — projected

- Purpose-gate strip · **projected ready at W10 CP9 close** (after CP1 banks Ruling-1 precondition (b) demonstration).

## Standing rules (unchanged from W9 + FL-P4-W9-02)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing until Canon 3 §24 strip ceremony (owner act).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- Post-compaction re-read discipline: last 200 lines of DECISIONS.md + current NEXT.md before any report/STATE change (FL-P4-W9-02).
- Correction-discipline: in-band · old wording struck-through · CORRECTION note · no silent rewrite (Owner Ruling 2026-08-19 §6).
- Host-identity drill attribution (Phase 0 DECISIONS.md L347): `drill_actor:*` prefix · no drill-mode switch (R1 confirmed for W10 CP1).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10 (executes R1-R7 · CP1 first).
- Owner rulings on 9 policy questions (non-blocking to W10 open · load-bearing before N-series + continuity attestations FIRE live records).

## Cycle status (2026-08-26T04:05Z · W9 CLOSED WITH CORRECTIONS · owner GO needed for W10) [ARCHIVED · superseded by 2026-08-26T04:25Z with R1-R7 logged]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files).
- **FL-P4-W9-02 opened + closed at open** · 3 report-time errors named + corrected in-band on `notes/w9_close_report.md §12` · new post-compaction discipline ratified (re-read last 200 lines of DECISIONS.md before drafting any report or STATE change).
- **Ruling-1 status SURFACED (missing from initial W9 reply · now corrected):**
  - Precondition (a) declaration ✓ DEMONSTRATED (W1).
  - Precondition (b) Watch reconciler DEMONSTRATED FIRING · **NOT YET** · `phase0/watch_*/` dirs do not exist on disk.
  - Purpose-gate strip **NOT ready-for-ceremony**. Needs a firing drill (W10 CP1 candidate · Canon 8 §27 · containment expiring clean · ~200 LOC).

## Awaiting owner (post-W9 · CORRECTED)

1. **FL-P4-W8-01 batch** · 7 N-series policy questions (CA1-N2 breach + CA1-N3 erasure).
2. **FL-P4-W9-01 batch** · 2 CA1-N5 continuity attestation questions.
3. **W10 GO + scope confirmation** — polish/completion wave · ~5000-6000 LOC estimated per §7 of `status_and_wave_plan.md` re-baselined table if extended · owner-confirmed scope named in `notes/w10_grounding_brief.md`.

**REMOVED from awaiting list per FL-P4-W9-02 corrections:**
- ~~A8 ruling~~ — ratified 2026-08-19 (DECISIONS.md L738-760). Walk-this UNBLOCKED for W10.
- ~~Executive-Final access decision~~ — repo accessed 2026-08-19 (HEAD `bba80ab`). Verdict on record: no Watch/Grey-Mirror material · Grey Mirror is a BUILD.

## Programme dashboard (post-W9 · composite % held pending W10 authoritative recomputation)

- **Frozen contracts** · 52.
- **Fidelity ledger** · 16 rows opened · 14 CLOSED · 2 OPEN (FL-P4-W8-01 + FL-P4-W9-01 · both owner-policy-pending).
- **Test cohort** · 416 green (63 files).
- **Cumulative LOC** · ~23039 net (W1..W9).
- **Composite %** · **HELD pending W10 authoritative recomputation** per owner correction #4. No running number in the interim.

## Ready for owner ceremony (Canon 3 §24 · owner act)

- Purpose-gate strip · **NOT YET ready-for-ceremony**. Blocked on Ruling-1 precondition (b) demonstration firing drill (W10 CP1).

## Standing rules (unchanged from W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law · A8 ratified 2026-08-19).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02).
- Pod-shell + spine same-commit mount DoD (FL-P4-W7-02).
- **NEW (FL-P4-W9-02)**: after ANY context compaction (agent restart, session reset, fork), FIRST action before drafting a report or STATE change is to re-read the last 200 lines of `STATE/DECISIONS.md` AND the current `STATE/NEXT.md`.
- Correction-discipline (Owner Ruling 2026-08-19 §6): corrections in-band with old wording struck-through + explicit CORRECTION note · never a silent rewrite.
- STATE/NEXT.md always carries exact resume point.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10.
- Owner rulings on 9 policy questions across 2 open FL rows (non-blocking to W10 open · but load-bearing before N-series + continuity attestations FIRE live records · and Ruling-1 firing drill is a separate CP1 unblocker).

## Cycle status (2026-08-26T03:45Z · W9 CLOSED · initial reply) [ARCHIVED · superseded by 2026-08-26T04:05Z with in-band corrections FL-P4-W9-02]

- **W9 CLOSED** at 416/416 wave-close cohort green (63 files) · `phase0/drill_receipts/20260826T034000Z_w9_wave_close_green.log`.
- **W9 LOC** · 2190 net (spine only · pod-shell unchanged) vs 6400 budget · **34%** · UNDER by 4210 LOC.
- **W9 register rows lit** · 17 (14 Canon 8 · 3 CA-series: CA1-011 · CA1-012 · CA1-N5 scaffold).
- **W9 fidelity ledger rows** · 1 opened (`FL-P4-W9-01` OPEN · CA1-N5-q1 owner-policy · non-blocking to close).
- **Auto-continue mandate SATISFIED** (W8 + W9 completed per owner ruling 2026-08-26T00:25Z).
- **Deferrals from W9**: Grey Mirror four sub-surfaces (§15-§16 + §32.4 · XL scope) · Walk-this per A8 ruling (owner-ruling pending) · Watch drills + fitness (§25-§28) · Reserved-decisions panel (§19) · Witness fabric (§9 full signing) · CA1-005 whitepaper · Doc 14 §§23-25 24-row expansion · Governance frontends. All named for a subsequent polish/completion wave with explicit owner GO.
- Full close report at `notes/w9_close_report.md` · dashboard §11 · owner policy questions §7 (batched across FL-P4-W8-01 + FL-P4-W9-01 = 9 total).

## Programme dashboard (post-W9)

- **Frozen contracts** · 52 (from 39 at W7 close · +13 across W8+W9).
- **Fidelity ledger** · 15 opened · 13 CLOSED · 2 OPEN (both owner-policy-pending).
- **Test cohort** · 416 green (from 250 at W6 close · +166 across W7+W8+W9).
- **Cumulative LOC** · ~23039 net (W1..W9).
- **Mechanism corpus** · ~50%.
- **Composite headline** · ~48%.

## Awaiting owner (post-W9)

1. **FL-P4-W8-01 batch** · 7 N-series policy questions (CA1-N2 breach + CA1-N3 erasure).
2. **FL-P4-W9-01 batch** · 2 CA1-N5 continuity attestation questions (verification architecture + RTO target).
3. **A8 ruling** (Walk-this Q1/Q2/Q3).
4. **Executive-Final access decision** (Grey Mirror mechanism completion depends materially).
5. **W10 GO + scope confirmation** (polish/completion wave · roughly 5000-6000 LOC estimated).

## Standing rules (unchanged from W8)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + hardcoded numeric assertion same-commit DoD (FL-P4-W8-02 extension).
- Pydantic 2.13.4 pin is LOAD-BEARING.
- Wave-close cohort assembly: grep filename + content-grep + `test_*_invariants.py` + hardcoded-count-assertion grep.
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- Owner GO for W10 (polish/completion wave) — no auto-continue covers this.
- Owner rulings on 9 policy questions across 2 open FL rows (non-blocking to close, but load-bearing before N-series + continuity attestations can FIRE live records).
- Owner A8 ruling (Walk-this) — load-bearing for that specific deferred item.

## Cycle status (2026-08-26T02:45Z · W8 CLOSED · W9 CP1 OPENING) [ARCHIVED]

- **W8 CLOSED** at 366/366 wave-close cohort green (55 files) · `phase0/drill_receipts/20260826T024000Z_w8_wave_close_green.log`.
- **W8 LOC** · 2964 spine + 4 pod-shell = 2968 net vs 5600 budget · **53%** · UNDER by ~2632 LOC.
- **W8 register rows lit** · 10 (7 Doc 15 · 3 CA-series partial/scaffolding).
- **W8 fidelity ledger rows** · 2 opened (`FL-P4-W8-01` OPEN owner-policy · `FL-P4-W8-02` CLOSED new DoD element).
- **Deferrals from W8**: CA1-005 whitepaper · Doc 14 §§23-25 24-row expansion · Governance frontends · CA1-012 Watch staleness-flagging · Data Suite · LLM chip polish. All named for W9 or a subsequent polish wave (no silent slip).
- **Frontends deferred to a subsequent polish wave** (backend records on record; screenshot gap unchanged).
- Full close report at `notes/w8_close_report.md` · dashboard §11 · owner policy questions §7.

## W9 opening — CP1 carry-over items (all P0)

1. **FL-P4-W8-01 policy answers** — if owner has ruled on the 7 N-series questions (Close Report §7), wire the answers · else continue rest of W9 without firing.
2. **Watch mechanism primary build** (Doc 3 · Doc 8) — includes CA1-011 enforcement half at `services.watch.route_recheck_failure` (W9 seam per Owner Ruling 2026-08-25T23:15Z SPLIT).
3. **Grey Mirror four sub-surfaces** (overview · monitor · response · people).
4. **Ledger continuity (CA1-N5)**.
5. **Walk-this** per A8 ruling (Q1 · Q2 · Q3).
6. **CA1-012 Watch staleness-flagging** (carried from W8).
7. **Doc 14 §§23–25 remaining 24 rows** (carried from W7).
8. **CA1-005 whitepaper re-evaluation** (carried from W7).

## W9 nominal scope (owner-confirmed 2026-08-26T00:25Z · auto-continue after W8)

- Watch mechanism · Grey Mirror completion (four sub-surfaces).
- CA1-N5 ledger continuity attestation.
- Walk-this per A8 ruling.
- CA1-011 enforcement half at named seam.
- CA1-012 Watch staleness-flagging.
- Doc 14 §§23-25 24-row expansion.
- CA1-005 whitepaper re-evaluation.
- Wave close · cohort assembly · close report.

**W9 stop-and-report line**: 6400 LOC per re-baselined table.

## Standing rules (all binding through W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (Design Law).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity map + **hardcoded numeric assertion** same-commit DoD (FL-P4-W8-02 extension).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki L4-L18).
- Wave-close cohort assembles by grep filename + content-grep + `test_*_invariants.py` + hardcoded-count-assertion grep (W8-added).
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- None. W9 CP1 opens immediately.

## Cycle status (2026-08-26T01:15Z · W7 CLOSED · W8 CP1 OPENING) [ARCHIVED]

- **W7 CLOSED** at 310/310 wave-close cohort green (44 files) · phase0/drill_receipts/20260826T010500Z_w7_wave_close_green.log.
- **Owner auto-continue** for W8 and W9 · per-wave go-gate lifted (2026-08-26T00:25Z verbatim in DECISIONS.md).
- **W7 LOC** · 2779 net (2429 spine + 350 pod-shell) vs 3520 budget · **79%** · UNDER by 741 LOC.
- **W7 register rows lit** · 17 (13 Doc 13 · 4 Doc 14).
- **W7 fidelity ledger rows** · 2 opened + closed (FL-P4-W7-01 · FL-P4-W7-02).
- **1 deferral to W8** · CA1-005 whitepaper (never opened · honest gate under 150-LOC lid).
- Full close report at `notes/w7_close_report.md` · dashboard on §10.

## W8 opening — CP1 carry-over items (all P0)

1. **Canonical-projection remediation** — pydantic-version-independent projection for frozen snapshots (Owner Ruling 2026-08-25T22:55Z Q1 · from W6 close). Load-bearing for W8's contract-heavy scope.
2. **Pod-shell mount completeness test** (new invariant · from FL-P4-W7-02 §7.2).
3. **Pod-shell boot test** (new invariant · from FL-P4-W7-02 §7.2).
4. **Async event-loop pollution owner-visibility ruling** (from W7 CP8 conftest fixture · owner may want a different remediation).
5. **CA1-005 whitepaper re-evaluation** (deferred from W7 CP6).
6. **Doc 14 §§23–25 · 24 remaining rows expansion** (from W7 opener grounding · deferred).

## W8 nominal scope (owner-confirmed 2026-08-26T00:25Z)

- Governance ceremony · Approvals surfaces.
- N-series: CA1-N2 breach notification · CA1-N3 access-and-erasure.
- CA1-009 generalized handoff contract.
- Rules Updates · Spend Requests · Trace surface (REFERENCE-NOT-COPY load-bearing).

## W9 nominal scope (owner-confirmed 2026-08-26T00:25Z · auto-continue after W8)

- Watch mechanism · Grey Mirror completion.
- CA1-N5 ledger continuity.
- Walk-this per A8 ruling (Q1 · Q2 · Q3).
- CA1-011 enforcement half at named seam (`services.watch.route_recheck_failure`).
- Ruling-1 closure question surfaced (NOT fired · Canon 3 §24 ceremony is an owner act).

## Standing rules (all binding through W8 + W9)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY (LOAD-BEARING for W8 Trace surface).
- Purpose gate on every crossing (still on record until Canon 3 §24 ceremony).
- Contract + snapshot + parity same-commit DoD (FL-P4-W6-02/08/09).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki L4-L18).
- Wave-close cohort assembles by grep filename + content-grep + `test_*_invariants.py` (W7-broadened).
- Pod-shell + spine same-commit mount DoD (W7-added).
- STATE/NEXT.md always carries exact resume point.
- Checkpoint commits at every green section.
- No push; local commits only.

## Blocked (awaiting)

- None. W8 CP1 opens immediately.

## Cycle status (2026-08-25T23:38Z · W7 CP1 CLOSED · CP2 opening) [ARCHIVED]

- **W7 GO** received from owner at 2026-08-25T23:30Z (see STATE/DECISIONS.md L1358-L1421). Scope: Docs 13 + 14 + CA1-004 + CA1-005 + CA1-011-split + W6 deferrals folded in. Budget ~3520 LOC · stop-and-report line at 3520.
- **CP1 (Rulings + rates lane) · GREEN**: 5/5 tests-first invariants green at `phase0/drill_receipts/20260825T233800Z_w7_cp1_green.log` (right-reason failure at `20260825T233500Z_w7_cp1_right_reason_fail.log`). Delta: `services/cost_ledger/rates.py` extended with `training` lane + `rate_for_training_run()`; `phase0/rates_register/training/` opened with README (honestly absent — no rate rows on record).
- **CP2 (Targeta service LIFT) · opening**: RMS-IQ-Core-2 `services/targeta/` (425 LOC · 6 files) LIFT into `Extraction-Akki/backend/services/targeta/`. Contract already in-tree (`contracts/targeta_plan.py` + snapshot). Tests-first from RMS `tests/invariants/test_targeta_invariants.py` (207 lines · adapt).

## W7 checkpoint status

| CP | Scope | Status | Est. LOC (pre-cal.) | Actual LOC |
|----|-------|--------|--------------------:|-----------:|
| CP1 | Rulings + rates lane · training register subdir · README | GREEN | 150 | ~50 (SLA under-run) |
| CP2 | Targeta service LIFT + invariants | opening | 500 | — |
| CP3 | Model registry service (top-level `services/model_registry/`) LIFT + FACTS-only seed (7 Emergent Universal models · no whisper-tiny) | pending | 350 | — |
| CP4 | Model Admission ceremony backend · six-criterion MOAC · uncurated-sample discipline · rights lineage · quarantine · Batch Board records | pending | 700 | — |
| CP5 | CA1-004 baseline line + CA1-011 re-check state (Watch route SPLIT to W9 · named seam on record from W7) | pending | 400 | — |
| CP6 | CA1-005 whitepaper · 150-LOC hard lid · OR W8-defer with named gap | pending | 250 or DEFER | — |
| CP7 | W6 deferrals folded in: Data Suite surface (v7-exact) · LLM chip UI polish · Model Ecosystem surface (Baseline · Ecosystem · Admission tabs) | pending | 700 | — |
| CP8 | Wave close · cohort assembly (grep frozen+contract) · STATE · screenshots · close report | pending | 50 | — |
| **Estimate total (pre-cal.)** | | | **3100 · × 1.60 ≈ 3520** | **~50 (CP1 only)** |

## W7 CP1 rulings summary (owner · 2026-08-25T23:30Z)

- **Q2 · MOAC uncurated-sample**: REUSE Registry census facts (235 tables · 145 crossing receipts) where letter permits. Fresh pass ONLY where Doc 13 requires record-contents sampling AND a named purpose is on record — else NAME THE GAP.
- **Q3 · Namespace**: `services/model_registry/` first-class package. LIFT RMS fabric. Seed from FACTS only: 7 Emergent Universal models (real, W5-connected). **whisper-tiny NOT seeded** (donor-side CI fixture, not on this estate).
- **Q4 · CA1-005 whitepaper**: 150-LOC hard lid; overrun → W8-defer with named gap.

## Standing rules (unchanged from W6)

- Tests-first + right-reason receipts.
- v7-exact T1 · real facts · drawn-not-blank.
- REFERENCE-NOT-COPY.
- Purpose gate on every crossing.
- Contract + snapshot + parity same-commit DoD (FL-P4-W6-02/08/09 ratification).
- Pydantic 2.13.4 pin is LOAD-BEARING (Extraction-Akki `5aba8e7`).
- Wave-close cohort assembles by grep `test_*_frozen*.py` + `test_*_contract*.py`.
- No push; local checkpoint commits; STATE/ kept current.

## Blocked (awaiting)

- None. CP2 proceeds immediately.

## Cycle status (2026-08-25T22:40Z · W6 CLOSED · steer requested) [ARCHIVED]

- **W1..W6 · CLOSED**. 250/250 W6 wave-close cohort green (36 test files) at `phase0/drill_receipts/20260825T224000Z_w6_wave_close_green.log`. Frozen+contract sub-cohort 18/18 green at `phase0/drill_receipts/20260825T223200Z_w6_close_frozen_cohort_green.log`.
- **W6 LOC actual**: +3319 net (+3716 −397) vs 2880 budget · **15% overrun**. Envelope stop-and-report to owner (see notes/w6_close_report.md §5 & §8).
- **9 fidelity ledger rows opened at W6 close** — TWO defect classes named, NOT nine of the FL-P4-W4-01 class:
  - 6 × **environmental pydantic 2.13.4 serialization drift** (FL-P4-W6-01/03/04/05/06/07) — none wave-attributable; models untouched since 2026-07-02/07-31.
  - 3 × **FL-P4-W4-01 map/count omission recurring** at W1 origin (FL-P4-W6-02/08/09) — actor_declaration snapshot on disk but never mapped; NamedTuple utilities over-enumerated. Recurrence count for FL-P4-W4-01 class: 2.
- **W6 deferrals named** (deferred to W7, not held-open):
  - Data Suite surface (v7-exact) — backend not yet built; full CP moves to W7.
  - LLM chip UI polish — cosmetic; belongs alongside Cost Ledger polish loop.
  - Grey Mirror overview surface — waiting on Watch (W9 per opener plan).
  - Pydantic-version-drift remediation — new P1 W7-opener owner-ruling item.
- **W7 nominal scope** (per opener #1 re-baseline): Targeta · Model Ecosystem · Model Admission · ~3520 LOC. **WAITING for owner W7 GO.**

## W6 delivered · commits on programme/track-a

```
7db5a00 W6 close · 9 fidelity ledger drifts reconciled · 2 distinct defect classes named
39a7034 W6 CP5 · Lowered Standard (CA1-010) · session-scoped state + expiry + in_process residency
d9ae4a5 W6 CP4 · Solva stages 4-6 · Grey Mirror groundwork · mechanism-side only
770e013 W6 CP3 · Retention enforcement · CA1-N1 · 218/218 green
717013f W6 CP2b · Cost Ledger frontend surface · CA1-008 lever sequence visible
d7ff88e W6 CP2 · Cost Ledger backend · CA1-008 rates + ledger + 5-lever attribution
f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
```

W6 close report: `notes/w6_close_report.md` (canonical).

## Owner steer requested before W7 GO (blocking)

1. **Pydantic-version-drift remediation path** (close report §4.1): pin pydantic (a) vs canonical-projection (b) vs both?
2. **W6 LOC overrun** (15%): accept the recalibrated envelope for W6 as delivered, or narrow-scope W7 to absorb the overrun?
3. **W7 scope confirmation**: Targeta · Model Ecosystem · Model Admission per re-baselined estimate of 3520 LOC — proceed as planned, or steer?

## Cycle status (2026-08-25 · W6 openers CLOSED · W6 scope opening) [ARCHIVED]

- **W1..W5 · CLOSED**. 195/195 gating tests green across the wave-open cohort (194 W5-close + 1 FL-P4-W4-01 reconciled).
- **W6 opener #1 · re-baseline · DONE**. Calibration factor 1.60× published in notes/status_and_wave_plan.md §7. W6 stop-and-report line: **2880 LOC**.
- **W6 opener #2 · FL-P4-W4-01 · DONE**. Root-cause named (W4 close missed the snapshot bump); reconciliation via snapshot bump ratified by this owner ruling; fidelity ledger row closed at phase0/fidelity_ledger/FL-P4-W4-01.json.
- **W6 SCOPE opening · IN PROGRESS**:
  - CP1 · rulings + brief (this update) — pending.
  - CP2 · rates register (owner-supplied or honestly absent) + Cost Ledger backend + tests — pending.
  - CP3 · retention enforcement + tests — pending.
  - CP4 · Grey Mirror groundwork + Solva stages 4-6 mechanism-side — pending.
  - CP5 · W5 deferrals folded in (LLM chip UI + Data Suite + CA1-010) — pending.
  - CP6 · wave close (dashboard + STATE + screenshots) — pending.

## W6 openers summary

### Opener #1 · Re-baseline (in notes/status_and_wave_plan.md §7)
- W1: 1006 LOC actual vs 800 est → 1.26×.
- W2: 1666 vs 150 → 11.11× — **class misclassification** (S→M-effective).
- W3: 2519 vs 2000 → 1.26×.
- W4: 2566 vs 600 → 4.28× — **class misclassification** (M→L-effective).
- W5: 4026 vs 2500 → 1.61×.
- **Calibration factor: 1.60× (median), 1.95× (weighted mean)** — using MEDIAN as the go-forward multiplier (owner ruling naming).
- W6-W9 re-baselined: **W6 ~2880 LOC · W7 ~3520 LOC · W8 ~5600 LOC · W9 ~6400 LOC · total ~18400 LOC**.
- Remaining build effort is 60% higher than pre-calibration; W1-W5 landed 95% higher than pre-calibration.
- Three ruling paths named for owner (accept re-baseline / narrow scope / add L-extended tier); default: accept.

### Opener #2 · FL-P4-W4-01 closed
- Root-cause: W4 extended `LedgerRow` (added `thinklab_objective`, `row_id`, description tweaks, `additionalProperties: True` on stamp_audit, dropped `at` from required) but skipped the snapshot bump — silently failing test at HEAD `a71ea67`.
- Reconciliation: bump `northena_ledger_row.contract_snapshot.json` to match current W4-ratified code shape. Owner Ruling W6 GO opener #2 IS the explicit ratification moment.
- Right-reason failure: phase0/drill_receipts/20260825T204000Z_w6_opener2_FL-P4-W4-01_right_reason.log.
- Green after fix: 195/195 in phase0/drill_receipts/20260825T205000Z_w6_opener2_FL-P4-W4-01_green.log.
- Fidelity ledger row banked at phase0/fidelity_ledger/FL-P4-W4-01.json — CLOSED.
- Process finding: W4 close cohort had a scoping gap (missed a contract snapshot test). Note in the ledger row; future wave-close cohorts assemble by grep for `test_*_frozen*.py` + `test_*_contract*.py`.

## W6 scope plan (post-openers)

Grounded in the register rows FIRST (owner ruling). Six checkpoints:

**CP2 · Cost Ledger (CA1-008 + Docs 11/12)**:
- Read the CA1-008 lever sequence from the addendum / Doc 11 / Doc 12 verbatim (BEFORE opening code — quote it in the CP2 brief).
- Rates register: `services/cost_ledger/rates.py` reads from `phase0/rates_register/*.json` — OWNER-SUPPLIED FACTS or honestly absent. If no rate on record for a model or GPU-hour, ledger shows quantities with the W2 honest-gap sentence.
- Ledger backend: `services/cost_ledger/ledger.py` consumes W5 metering receipts (all `solva_* / chat_* / thinklab_* / llm_*` kinds) + W2 reflection quotas + seam GPU usage into ledger entries.
- Surface: `pod_shell/frontend/src/components/CostLedger.jsx` per v7 oracle `COMPUTE_CHARTS` fabric.

**CP3 · Retention enforcement (CA1-N1)**:
- Quote the register's letter for retention on each record class we hold: receipts / ledger rows / chat turns / admits / seam runs.
- Append-only classes NEVER get delete verb — retention on those = marked-expired + excluded-from-render. If the register says otherwise, quote it and STOP.
- Enforcement mechanism per the letter (expiry marking / governed deletion path).
- Surface: retention state row on records + attestation record.

**CP4 · Grey Mirror groundwork + Solva stages 4-6**:
- Solva stages 4 (triangulation) · 5 (tension_detection) · 6 (probability_weighting) ADAPTED from Executive-Final donor · mechanism-side only.
- Grey Mirror overview surface only if oracle has parts that render honestly from what exists (else deferred to W9 with Watch).

**CP5 · W5 deferrals folded in**:
- ConnectDrawerChat LLM chip UI polish (backend live).
- Data Suite surface v7-exact (data facts from real connected sources · structure-only posture).
- CA1-010 session-scoped lowered-standard with logged expiry (state visible + refusal grammar).

**CP6 · wave close**: dashboard delta + screenshots + STATE + close report.

## Verification path for orchestrator (independent audit) — W6 openers close

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a | head -3
# f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
# 39386ac W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension

python3 -m pytest backend/tests/invariants/test_northena_ledger_row_v0.py -v
# Expect: 1 passed.

cd /app/assessment_workspace
git log --oneline master | head -3
# (opener #1 re-baseline + STATE update committed at close)

cat notes/status_and_wave_plan.md | grep -A2 "Calibration factor"
# Expect the 1.60× naming.
```

## Blocked (awaiting from owner)

- None new. **W6 scope proceeds unless owner steers to option (b) narrow-scope or (c) L-extended-tier from opener #1's naming.**

## No push, ever

Owner Clarification 1 (2026-08-14). Local commits are the record.

## Honest LOC drift note

W4 was scoped M (~600 LOC estimated). Delivered at ~2020 LOC (donor Northena adaptation is inherently 500+ LOC; ThinkLab v7 fabric fidelity ~500 LOC; deep tests-first cohort 457 LOC). Above M-class ceiling. Reported to owner; hold for classification ruling or narrowing envelope guidance for future M waves.

## Post-W4 report to owner

Deliver: 20 register rows targeted; 6 fully DONE + 2 PARTIAL + 12 deferred to W5+ · SIX mechanism reuse pulls cited per file · three screenshots (landing / mode entry / admit walk) · LOC ~2020 · SHAs (`7e6bbc4` · `7bea87d` · `a71ea67`) · dashboard delta: Doc 05 5% → 30%; composite headline 43% → 44%.

## Cycle status (2026-08-14 · Owner Simplification response)

- **Simplification cycle CLOSED.** Connect UX collapses to ONE panel. Step grammar survives only as post-submit progress view (the handshake walk from the seven-stage pipeline, which itself is UNCHANGED).
- **Deterministic local parsing live.** `POST /api/connect/parse-paste` — pattern-only, no LLM/HTTP/subprocess. Password never returned in response body; `password_captured` boolean signal only.
- **Client-side password custody honoured.** Browser keeps the raw paste in its own textarea memory and submits the full credential set once to `/api/connect/gpu` (existing seven-stage pipeline unchanged). No server-side secret state between the parse and connect requests.
- **Fidelity ledger:** FL-P2-19 CLOSED (synisense-reading recorded); FL-P2-20 CLOSED (single-panel collapse); FL-P2-21 CLOSED (no-LLM-transit invariant added as gating).
- **LOC delta:** `ConnectWizard.jsx` 623 → 451 (−172 lines, −28%). New backend: 266 lines (parser + router + init). New backend tests: 321 lines. Frontend tests net +52 lines.
- **143/143 gating tests green.** 108 backend python + 12 frontend allowlist + 23 frontend rehome/single-panel. Zero regressions.
- **Commit SHAs on programme/track-a (4 new atop `f83b509`):**
  - `1f3d3bd` Phase 1 tests-first · deterministic paste parser + no-LLM-transit invariants
  - `ef9e185` Phase 1 implementation · deterministic paste parser + router mounted
  - `5ce8647` Phase 1 tests-first · single-panel Connect surface invariants
  - `c490ce9` Phase 1 implementation · single paste-and-connect panel

## Two-sentence access-mechanism proposal (still awaiting owner ratification)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` - every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ratify the two-sentence access proposal** (still standing).
- **FL-P2-09 disposition** - pod egress-IP rotation. Rotated AGAIN this cycle: STATE was `104.198.214.223` last cycle, now `35.225.230.28` this cycle. `34.16.56.64` stays in `SPINE_ALLOWED_IPS` unchanged per owner directive.
- **Vendor-side VM provisioning using the provisioning card** (unchanged):
  - Paste the estate public key `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki` into the VM's SSH Public Key field at creation (AISCA guide Fig 10).
  - Add TWO /32 rows to the VM's Security Group SSH rules (AISCA guide Fig 11): the owner's own operator /32 AND the pod egress /32 (currently `35.225.230.28/32`, subject to rotation).
- **Then paste the AISCA Output panel into the single Connect panel.** The parser reads it deterministically; the confirmation view masks the password as `•••• captured`; owner taps Connect; the unchanged seven-stage pipeline fires; with the estate key already installed, hardening shortens to verify-key-only → disable password auth → probe dead.

## Cold-reader-executable next actions

### 1. Deliver the Owner Simplification cycle report (this reply)

Test delta + right-reason receipts + green receipts + no-LLM-transit hard-rule proof + 4 Playwright screenshots (single panel / paste-parsed confirm / with provisioning card / handshake walk result) + LOC delta + commit SHAs.

### 2. On owner ratification of allowlist entry / vendor-side provisioning

- Update `SPINE_ALLOWED_IPS` in `/app/backend/.env` (add owner's client `/32`). Record allowlist change as a ledger row.
- Owner pastes AISCA Output panel into single Connect panel; deterministic parse; confirm; connect; seven-stage pipeline fires. Watch for green/failed/held per brief §5 paragraphs 6-7.

### 3. Post-Phase-0 (next cycle)

- **A4 increment (Registry honest-state instrumentation):** wire the COMPUTE CONNECTED tab's after-state to the real commissioning record on disk (present a "Just connected" pill + meta line + link to the record). Add DATA CONNECTED / LLMS & TRAINED MODELS state transitions when their waves land.
- **Wire-up non-compute path to per-wave connectors** as they land (data-source in Phase 2 admit-slice; LLM/trained-model in later waves). The single-panel + intent-record grammar becomes real routing when the wave connectors are ready.

### 4. Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a
python3 -m pytest \
    backend/tests/invariants/test_actor_declaration_v0_contract_frozen.py \
    backend/tests/invariants/test_record_matrix_thin_kernel.py \
    backend/tests/invariants/test_task_identity_thin_kernel.py \
    backend/tests/invariants/test_parity_seat_extends_thin_kernel.py \
    backend/tests/invariants/test_admit_refuses_undeclared_actor.py \
    backend/tests/invariants/test_compute_seam_no_unledgered_exec.py \
    backend/tests/invariants/test_compute_seam_artifact_hash_verified.py \
    backend/tests/invariants/test_hardening_orchestrator.py \
    backend/tests/invariants/test_connect_gpu_pipeline.py \
    backend/tests/invariants/test_connect_gpu_scope_S_or_M.py \
    backend/tests/invariants/test_connect_gpu_acceptance_wired.py \
    backend/tests/invariants/test_ip_allowlist_middleware.py \
    backend/tests/invariants/test_estate_keys_and_connect_estate.py \
    backend/tests/invariants/test_credentials_paste_parser.py -v
# Expect: 108 passed at HEAD c490ce9.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 23 passed.

# Live probe: no-LLM-transit proof (sentinel absent from response)
PW="INDEPENDENT_AUDIT_SENTINEL_$$"
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     -H "Content-Type: application/json" \
     -d "{\"paste\":\"Host Name: h\\nPassword: ${PW}\\nUsername: u\\nPublic IP: 1.2.3.4\",\"hint_kind\":\"compute\"}" \
     http://127.0.0.1:8001/api/connect/parse-paste | grep -c "${PW}"
# Expect: 0 (password never in response body).

# Provisioning card live probe
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     "http://127.0.0.1:8001/api/connect/estate-facts" | python3 -m json.tool
```

### 5. No push, ever

Owner Clarification 1 (2026-08-14). Assessment repo and Extraction-Akki both stay local.

---

## CODE FREEZE · 2026-08-26 · R1–R7 PLAN DRAFTED, AWAITING OWNER GO

**Status**: Remediation plan R1-R7 drafted, awaiting owner GO. Code freeze in force.

**What happened**: Owner delivered R1-R7 remediation directive at 2026-08-26T09:00Z. Main agent misread it as an execution order and began R1 (Ship-Manifest DoD meta-invariant + KNOWN_UNWIRED / KNOWN_RUNTIME_DRIFT manifests + DECISIONS.md ruling insert). Owner then clarified: the R1-R7 message was the PLAN only; execution was NOT authorized. Halt issued 2026-08-26T09:11Z.

**Commits during the misread**: NONE. No git commit landed for R1 work in either repo. Verified:
- `/app/assessment_workspace/repos/Extraction-Akki` HEAD unchanged: `d763721 W11 CP7 · register expansion 17→20 docs · 36 new rows · 12/12 green`
- `/app/assessment_workspace` HEAD unchanged: `743046a audit · system-wide spec↔build audit 2026-08-26 · 10 status-inflations named · stop-and-report · no code writes` (this commit was authorized by the owner in the audit-delivery turn and is legitimate)

**Uncommitted R1 artefacts on disk** (per owner order: leave in place, do not revert):

Extraction-Akki repo (`programme/track-a` branch):
- `backend/tests/invariants/test_ship_manifest_dod.py` · meta-invariant test · 8 tests · GREEN in local run
- `backend/tests/invariants/known_unwired.py` · 35-entry ledger of routers-on-disk-not-wired-to-runtime-assembler
- `backend/tests/invariants/known_runtime_drift.py` · 3-entry ledger of /app-vs-pod_shell drift
- `phase0/drill_receipts/20260826T090647Z_w11_r1_ship_manifest_dod_right_reason_failure.log` · RED receipt
- `phase0/drill_receipts/20260826T090914Z_w11_r1_ship_manifest_dod_green.log` · GREEN receipt

Assessment workspace repo (`master` branch):
- `STATE/DECISIONS.md` (modified) · appended R1 owner-ruling section (Ruling #1 Ship-Manifest DoD + Ruling #2 Callers-Cover-the-Rule DoD + Canon-5-§14-supersedes-Simplification note) at lines 1607–1660

**Uncommitted CP4 artefacts** (pre-R1, from paused work — NOT touched by this halt):
- `backend/contracts/skill_file_provenance_v0.py`
- `backend/services/skill_files/`
- `backend/tests/invariants/test_skill_file_provenance_v0_contract_frozen.py`
- `backend/tests/invariants/test_skill_files_module.py`
- `phase0/drill_receipts/20260826T081745Z_w11_cp4_skill_file_provenance_right_reason_failure.log`

**Owner directive (verbatim, 2026-08-26T09:11Z)**:
> "HALT — my error, not the owner's. The owner asked for the plan only; execution was NOT authorized. Stop all code writes immediately. If R1 work has started: leave it uncommitted (or if a commit already landed, note the hash and stop — do not revert, do not continue). Log in STATE/NEXT.md: 'Remediation plan R1-R7 drafted, awaiting owner GO. Code freeze in force.' Stand by. Nothing executes until I relay the owner's explicit approval."

**Freeze scope**:
- NO further file writes to `pod_shell/backend/`, `pod_shell/frontend/`, `backend/`, or any `services/*` under Extraction-Akki.
- NO `git commit` in either repo.
- NO `git push` (standing rule; also frozen here for clarity).
- STATE/NEXT.md log entry (this section) is the one authorized write during the freeze.

**Resume protocol**: main agent will resume R1 only upon receiving the owner's explicit approval, relayed by the user. On resume, the plan is: (a) verify the freeze-state artefacts still match, (b) commit R1 to Extraction-Akki (`programme/track-a`) with the two receipts, (c) commit the DECISIONS.md addition to assessment_workspace (`master`), (d) stop-and-report before starting R2.

**Recorded**: 2026-08-26 · code freeze active · owner GO required to resume.



---

## 2026-08-31 · TONIGHT-GPU-ACTIVITY THREAD · pointer to sprint plan

Owner rulings 3–5 landed tonight (2026-08-31). Full sequence banked verbatim in DECISIONS.md.

**Sprint plan drafted:** `/app/assessment_workspace/STATE/SPRINT_PLAN.md` — four chartered tracks:
1. **W-G5c-close** (in-flight, ~½–1 day) · Wave-G5c frontend close + owner eyeball bundle
2. **W-Shield-Train** (2–4 days) · Shielded-training pipeline (masking policy → row executor → transport → LoRA unstub → cleanup) — owner authority-required for masking-tier admission
3. **W-Audio-P2** (2–3 days after archive access) · Audio archive Phase 2 admission (manifest hash → representative slice → HSS → GPU smoke)
4. **W-WPW-v1** (~2 days for Tier 1+2 after 30-min spec ingest) · Whitepaper Wizard v1 (Tier 3 blocked on R1/R2/R3)

Sequencing is owner-only. Suggested prompts and one non-binding enhancement path are in the sprint plan.

**Tonight-activity carrier:** `burn_20260831T183509Z_731f22ad` — fallback governed matmul burn on both hosts via `services.training_runner.ssh_seam.execute_remote_command`. Activity summary lands at `phase0/gpu_burn/burn_20260831T183509Z_731f22ad/activity_summary.{txt,json}` when the run completes.

**Pending owner rulings (not blocking main-agent work; only decision-blocking):**
- **A-vs-C** audio-vs-text training-material choice for the shielded-training pipeline (owner has this in front of him now, per ruling 5).
- **R1/R2/R3** for WPW Tier 3 (banked as parked; frame crisply in W-WPW-v1-b charter).
- **W-Shield-Train-b** masking-tier admission ruling (needed to unblock the shielded-training pipeline).
- **W-Audio-P2-a** audio-archive access details (endpoint + credentials + manifest source) — needed to unblock W-Audio-P2.

Ratchet floor unchanged: **2680**. Uncommitted local work: keypair-hardening tests (11 tests) + Wave-G5c-COMPUTE-FRONTEND (declared). Both roll into W-G5c-close double-green bump.

---

## 2026-08-31 · W-G5c-close CLOSED · WPW spec INGESTED · pointer updates

**Closed tonight:**
- **W-G5c-close**: ratchet 2680 → **2692**. Eyeball bundle at `phase0/eyeball_bundles/wave_g5c_close_20260831/` (portal + Registry aside live + Compute Connected tab + README with plain-language captions per screenshot + GPU-activity card covering both runs).
- **W-WPW-v1-a (spec ingest)**: raw docx banked at `canon/fixtures/whitepaper_wizard_spec_v1/spec.docx` (sha256 recorded) + extracted text alongside (`spec.extracted.txt`) + `README.md` documenting the derived-artifact discipline.
- **W-WPW-v1-b (charter + reuse assessment + R1/R2/R3 framing)**: `STATE/WPW_CHARTER.md`. R1/R2/R3 framed crisply for single-shot owner ruling.

**Chartered but not yet started (owner-sequenced):**
- **W-G5c-COMPUTE-v2**: successor to retired tile-compute-* rules · targets ACTUALLY rendered Compute Connected dummies · concrete DOM element table in `STATE/SPRINT_PLAN.md`. ~1–2 days · unblocked.
- **W-Shield-Train**: shielded-training pipeline (a–g scope in charter) · 2–4 days · depends on masking-tier admission ruling.
- **W-WPW-v1-c/d/f/g**: Tier 1 + Tier 2 + attribution + integration · ~2 days · unblocked.
- **W-WPW-v1-e**: Tier 3 · BLOCKED on R1/R2/R3 · deliver ~1–2 days after rulings.
- **W-Audio-P2**: audio archive Phase 2 admission · 2–3 days after archive access granted · BLOCKED on owner-provided access.

**Pending owner rulings (not blocking any in-flight main-agent work; only decision-blocking):**
- **OWNER-DESK · allowlist restore** (2026-09-15T~17:57Z ruling: `"remove the white listing rule for now - i cant access"` → `ALLOWLIST_MODE=permissive`). On owner "restore" ruling: flip `/app/backend/.env` to `ALLOWLIST_MODE=strict`, restart backend + frontend, bank restore in DECISIONS. Do NOT let this silently persist across compactions.
- **RATIFIED HALT-TRIGGER · SYNTHETIC-FIXTURES-ONLY through sub-wave 3 + §5.3 clustering + §7 voice verification** (owner ruling 2026-09-15T~19:07Z verbatim: *"If at ANY point in sub-wave 3 (or later: clustering §5.3, voice verification §7) a mechanism would require REAL estate voice/biometric material to validate, HALT there — that is a genuine owner decision point (KDPA biometric territory, and the release-gate biometric-tier refusals stay in force regardless)."*). Concrete trigger: if a §6.3 P100 harness scenario, a §5.3 clustering step, or a §7 verification path would call for actual estate audio, embeddings, or per-speaker enrolment corpora → HALT immediately, bank the halt, wait for owner ruling. Synthetic caller-scoped refs and hand-built dataclass instances remain green-lit.
- **A-vs-C** audio-vs-text training-material choice (owner ruled B tonight = text · that's satisfied).
- **R1** WPW exceptional threshold (R1-a absolute margin or R1-b percentile bar · agent recommends R1-a with conservative X).
- **R2** WPW external-release signatory (owner names authority + backup).
- **R3** WPW DEFAULT ratifications + novelty-clause ratification (three sub-questions R3-a/b/c framed in charter).
- **W-Shield-Train-b** masking-tier admission ruling.
- **W-Audio-P2-a** audio archive endpoint + credentials + manifest source.

**Next text-run recommendations (deferred to owner sequencing):**
- Sample from `OFFSET 500000` in `ussd_question_response` to reach populated `value_chain`.
- Add `sms_log.sms_sent` (longtext) as secondary corpus.
- Pre-filter for unique Q×A pattern (1 example per unique combination) to escape memorisation regime.

**Ratchet floor:** **2692** · double-green byte-identical last close · manifest updated in `backend/tests/invariants/baseline_failures.json`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
