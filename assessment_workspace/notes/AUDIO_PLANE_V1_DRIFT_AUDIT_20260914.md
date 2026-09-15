READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md

**Purpose.** Cross-check what is already BUILT on disk against the newly-registered `Audio Intelligence Plane Specification v1.0` (canon drop `20260914_audio_plane_v1`), the `Pull Seam` design-principles doc (canon drop `20260914_pull_seam`), and existing canon on disk. Output a drift table: **built behaviour · v1.0 verbatim quote · match/deviation/not-yet-in-scope**.

**Discipline:** every "v1.0 verbatim quote" column cites the paragraph anchor in the structured extract (`Audio_Plane_Spec_STRUCTURED.txt` · P###) so the finding can be re-verified against the source. Findings are **surfaced only, not silently fixed** — the owner rules on each per DECISIONS.md 2026-09-15T~01:40Z.

**Wave-honest limits acknowledged:** W-AUDIO-POC (M5 SW1) explicitly scoped itself to **file-level, shape-only census + release-gate contract**; it did NOT open a segment-level ingestion pipeline. Findings below distinguish between (a) actual **DRIFT** of already-sealed mechanism vs v1.0 spec and (b) **NOT-YET-IN-SCOPE** items that v1.0 requires but that no wave has yet chartered.

---

## Table 0 · Anchor drift check — "Audio-Plane §1.2" citations across the on-disk canon-anchor notes

The M5 promises anchored on `Audio-Plane §1.2` across four `notes/*` files. Verifying the anchor citations verbatim against v1.0 §1.2 (P015).

| On-disk citation (file + line) | On-disk quoted text | v1.0 verbatim (P015) | Verdict |
|---|---|---|---|
| `notes/SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md:47` | *"Each governs its own domain and explicitly disclaims parallel machinery (Audio-Plane §1.2)."* | *"The audio plane introduces no sibling services. …Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."* (P015) | **MATCH** (paraphrase framing; underlying rule preserved) |
| `notes/SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md:92` | *"`Audio-Plane §1.2` ('The audio plane introduces no sibling services')."* | *"The audio plane introduces no sibling services."* (P015 s1) | **MATCH · verbatim** |
| `notes/SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md:369` | *"`Audio-Plane §1.2` 'Modality extension, not parallel machinery' ⇒ audio records fold into existing classes …"* | *"Modality extension, not parallel machinery"* (P014 heading) + *"The audio plane introduces no sibling services."* (P015 s1) | **MATCH · verbatim heading + first-sentence** |
| `notes/MILESTONE_PROMISE_BINDING_20260913.md:428` | *"Audio-Plane §1.2 no parallel machinery — enforced structurally by W-AUDIO-POC composing existing platform primitives."* | as above | **MATCH · shorthand OK** |
| `notes/MILESTONE_PROMISE_BINDING_20260913.md:503` | M5 anchor row lists "Audio-Plane §1.2" as one of four discharge targets | as above | **MATCH** |
| `notes/BUILD_STRATEGY_20260913.md:20` | *"Discharges DAP-A10 remainder; Promise #12 (fully); Audio-Plane §1.2."* | as above | **MATCH** |

**Verdict (anchor drift):** the on-disk §1.2 anchor citations across four canon-anchor notes all match the v1.0 verbatim text. The §1.2 clause was stable across the retired drafts (Audio Capability Spec v1.0 + Addendum v1.1.2) and v1.0. **No anchor drift.**

---

## Table 1 · W-AUDIO-POC machinery vs v1.0 requirements

### Recording-inventory pipeline

| # | Built (verbatim shape from `services/audio_poc/recording_inventory.py`) | v1.0 verbatim quote | v1.0 anchor | Verdict |
|---|---|---|---|---|
| D1 | `RecordingEntry` frozen 6-field: `station, date_utc, slot, filename_stem, size_bytes, mtime_utc`. **No** `languages[]`. **No** `condition_profile`. **No** `switch_points`. **No** `codec_version`. **No** `instance_condition_map`. | *"Recorded per segment: languages[], confidences, and code-switch points where multiple languages occur in one utterance."* | v1.0 §4.1 P061 | **NOT-YET-IN-SCOPE.** W-AUDIO-POC wave-honest limit E.2 declared this a **file-level, shape-only census, not a segment-level ingestion pipeline**. v1.0 §4.1's per-segment `languages[]`/`condition_profile`/`switch_points` capture is INGESTION-time, not census-time. The current pipeline produces the file-level inventory that a future ingestion pipeline will consume. **Follow-on wave chartered candidate: `W-AUDIO-INGEST-STAGE-1` (per-segment LID + condition-profile + switch-point capture).** |
| D2 | `RecordingEntry` file-level `size_bytes` + `mtime_utc` (no segment bounds) | *"Baseline-tier capture (§9.2) runs for all admitted material regardless of any active objective."* + *"Contents at v1.0: language identification, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group-level acoustics (§4)."* | v1.0 §4.6 P075 + §9.2 P150 | **NOT-YET-IN-SCOPE** (baseline tier is the follow-on wave's charter · same reason as D1) |
| D3 | `inventory_snapshot_sha256` produces a single digest over all entries | *"If a measured throughput ceiling ever demands relief, the relief is batched stamping (one row certifying N events with a digest), which remains a single record."* | v1.0 §1.3 P017 | **MATCH · shape-compliant.** The snapshot digest is exactly the batched-stamping shape §1.3 allows. Verdict conditional on the digest being stamped into the one Northena ledger (not a local one) — CURRENTLY: digests are produced as content-addresses but not yet routed into the one-ledger data class. **Sub-drift: sub-drift-D3a "digest-to-one-ledger routing missing" · not-yet-in-scope for the POC; follow-on wave.** |

### Transcript-inventory pipeline

| # | Built | v1.0 verbatim quote | v1.0 anchor | Verdict |
|---|---|---|---|---|
| D4 | `TranscriptEntry` frozen 7-field: `station, date_utc, slot, filename_stem, size_bytes, mtime_utc, transcript_status`. Same file-level shape; no `codec_version`, no `languages[]`. | *"A downstream artifact lacking codec_version in provenance is rejected at the registry boundary."* | v1.0 §3.3 P055 | **NOT-YET-IN-SCOPE for existing OBS transcripts** — those were produced by a legacy path predating v1.0's codec_version mandate; they cannot retroactively carry `codec_version` because no codec produced them. **However for FUTURE transcripts produced by the estate's own audio pipeline, v1.0 §3.3 P055 will bite.** Registered as **DRIFT-FUTURE** — the release-gate mechanism must extend to refuse artefacts lacking `codec_version` when the estate's own codec is admitted. |
| D5 | `classify_transcript_status` uses a closed set (FINISHED/PARTIAL/MISSING/MALFORMED) | *"No new machinery is built for display."* (P210) + one-record doctrine (P017) | v1.0 §13.4 P210 + §1.3 P017 | **MATCH · shape-compliant** |

### Pairing + gap-set

| # | Built | v1.0 verbatim quote | v1.0 anchor | Verdict |
|---|---|---|---|---|
| D6 | `AudioTranscriptPair` 5-field: `station, date_utc, slot, filename_stem, pair_state` + `compute_gap_set(pairs)` | v1.0 spec has no direct pairing requirement — pairing is a POC-scoped shape that maps NAS recordings to OBS transcripts. No v1.0 clause forbids it. §4.5 P071 dedup instance-condition-map is a related but distinct concern. | v1.0 §4.5 P071 (adjacent) | **NOT-A-DRIFT** — pairing/gap-set is a POC composition primitive; v1.0 has no requirement for or against it. Marked **INFERRED (owner-ratified 2026-09-13 at wave open · retained as POC scope).** |

### Release gate · `TranscriptArtefact`

| # | Built | v1.0 verbatim quote | v1.0 anchor | Verdict |
|---|---|---|---|---|
| D7 | `TranscriptArtefact` frozen 5-field: `tier, kdpa_verdict, named_persons_verdict, transfer_basis, licence_class`. **No `codec_version`.** | *"codec_version is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens."* | v1.0 §3.2 P048 | **DRIFT** on artefacts produced by the estate's own future codec. NOT-YET-IN-SCOPE for legacy OBS transcripts (no codec of ours produced them). **Recommended follow-on:** extend `TranscriptArtefact` with an optional `codec_version: Optional[str] = None` carrier that becomes MANDATORY when tier ∈ {estate-codec-produced}. **Owner rules on the extension.** |
| D8 | Refusal path: `admit_transcript_release` raises `TranscriptVerdictPending` on any PENDING verdict; refuses release wholesale. | *"if an approval cannot be reached, a terms lookup returns nothing, or a check errors, the crossing fails closed."* (Pull Seam P036.s4) + *"An unsupported-condition input produces a refusal with a stated reason and no output artifact."* (v1.0 §3.3 P056) | Pull Seam §2 P7 (fail-closed) + v1.0 §3.3 P056 | **MATCH.** The gate fails closed on PENDING with a stated reason. Aligned with both v1.0 and Pull Seam. |
| D9 | `admit_transcript_release` writes a receipt before returning? | *"Each operation writes a receipt … The receipt is written before the result is returned. If it cannot be written, the operation is refused."* | Pull Seam §2 P7 (P036) | **NOT-YET-IN-SCOPE.** `admit_transcript_release` returns None on success; there is no explicit receipt-write step wired into the surface today. The audio-poc `gap_fill_writer.py` writes a distinct kind of receipt, but the release-gate itself does not. Marked as **DRIFT-PULL-SEAM** (this ties into the Pull Seam Stage-2 recommendation about the unified `Receipt.v0` schema). |

### Model-choice drift (from CANON_MODEL_SPECS_VERBATIM_20260914.md)

| # | Built / staged | Canon verbatim quote | Anchor | Verdict |
|---|---|---|---|---|
| D10 | `services/perception/eab_1_pipeline/a1_vad.py` — **Silero VAD** wrapper; registry-pinned in `models_registry.v0.json` | Silero is not named in canon text. Canon-4 §50.1 M-11: *"Speaker overlap and call-in diarisation ⎢ Open diarisation stacks and overlap-aware recipes."* (starting-point clause · unnamed) | Canon-4 §50.1 · M-11 | **INFERRED · in-repo but not canon-named.** Silero fits the "open diarisation stacks" starting-point family but is not itself named. Requires owner ratification per Verbatim-canon standing rule. |
| D11 | `services/layer_b/diarization/pyannote_provider.py` — **pyannote/speaker-diarization-3.1** | Same as D10 — canon names starting points but not this specific model | Canon-4 §50.1 · M-11 | **INFERRED · in-repo but not canon-named.** Same disposition as D10. |
| D12 | Owner-suggested POC target: **whisper-tiny + faster-whisper (ctranslate2)** | Canon-17-19 §A17.10 (M-01, M-02): *"The registry seeds with whisper-tiny … backend: faster-whisper (ctranslate2) … CI CPU-mode ASR fixture model. NOT for production use."* | Canon-17-19 §A17.10 | **MATCH for CI/POC path.** The POC therefore proceeds against the canon-named CI-fixture. Straddles the CI-vs-production line at the moment we transcribe REAL NAS bytes (production data on a CI model). Marked **DEFAULT-PENDING-OVERRIDE** — owner rules whether the POC on real data may run against the CI fixture, or a wave must charter production-model selection first. |
| D13 | My earlier POC framing enumerated `whisper.cpp` as fall-back option (b) | Zero canon hits for `whisper.cpp` (search receipts in `notes/CANON_MODEL_SPECS_VERBATIM_20260914.md` Table 2) | — | **INFERRED · superseded.** whisper.cpp fall-back removed from the POC default per Verbatim-canon standing rule. |
| D14 | Cloud ASR (Groq / Deepgram / AssemblyAI / OpenAI) was correctly rejected on Pull-Seam grounds in my earlier framing | Pull Seam P015.s5..s7: *"There is no configuration in which estate data is transferred to compute outside the perimeter. This is a prohibition with no exception, not a default setting."* | Pull Seam §2 P1 | **MATCH.** Rejection stands. |

---

## Table 2 · Milestone Promise §12 (census-and-connection) vs v1.0 §1.4 "measure, do not assert"

Owner directive item E states: *"census run stays priority (it aligns with §1.4 measure-don't-assert — cite it)."* Verifying the alignment:

| Aspect | Built (W-AUDIO-POC census machinery) | v1.0 verbatim | v1.0 anchor | Verdict |
|---|---|---|---|---|
| Purpose | Enumerate 16 NAS channels × ~90 days of recordings + all google-transcripts on OBS; classify by transcript_status; produce gap-set | *"No data-volume requirement, accuracy expectation, or cost figure is quoted without a measurement behind it. The calibration stage exists to convert assertions into measurements before commitment."* | v1.0 §1.4 P019 | **MATCH.** The census IS the measurement that converts prior data-volume assertions into a measured inventory. |
| Read-only-ness | `readonly_nas_guard` (List/Read/Status only) + `readonly_obs_guard` (ListObjects/HeadObject/GetObject only) | Pull Seam P042 · *"The query runs inside the perimeter, on the estate's own compute, against data that never leaves the ESTATE side."* | Pull Seam §3 step 3 | **MATCH.** Census is Pull-Seam-conformant by construction (read-only on estate side · no bytes leave · aggregate-composition output only). |
| Governed-crossing status | Census output is aggregate composition (row counts, size buckets, date ranges) | Pull Seam P026 · Six-crossing table row `Browse`: *"Nothing ⎢ Aggregate composition only — never record contents"* | Pull Seam §2 P5 · P026 | **MATCH.** Census output is exactly the "Browse the estate" crossing shape (aggregate composition · never record contents). |
| Priority | Owner directive: run before production model selection | Canon-17-19 §A17.11 (M-03, M-04): *"Production selection is named after the census, not before it. Production base model selection lands additively at a later registry bump — 'named at first census activation' … the census (Documents 9–10) runs first, and the specific model is named after, informed by what the census actually finds in the estate — not chosen speculatively ahead of it on the strength of a published benchmark."* | Canon-17-19 §A17.11 | **MATCH.** Canon 17-19 §A17.11 explicitly sequences census-before-model-selection. Owner directive re-anchored. |

---

## Table 3 · Where v1.0 introduces NEW requirements not in scope of any existing wave

These are v1.0 requirements that no on-disk wave has chartered. They are enumerated so the owner can scope them into future waves.

| # | v1.0 verbatim requirement | v1.0 anchor | Existing surface (if any) | Status |
|---|---|---|---|---|
| N1 | *"A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."* | v1.0 §4.1 P060 | — | **NOT-YET-IN-SCOPE.** No LID module exists at segment level. `w11_stepA_base_models.md:148` mentions fastText LID.176 as a candidate — canon does not name it. Follow-on wave. |
| N2 | *"Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion."* | v1.0 §4.3 P067 | — | **NOT-YET-IN-SCOPE.** Follow-on wave. |
| N3 | *"[F]or each deduplicated item, the instance condition map … is retained."* | v1.0 §4.5 P071 | Occurrence index is referenced but not extended | **NOT-YET-IN-SCOPE.** Follow-on wave. |
| N4 | *"perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."* | v1.0 §3.2 P045 | — | **NOT-YET-IN-SCOPE.** No audio_codec service exists. Follow-on wave anchor: v1.0 §15 P232 sequences codec service as build-item 4 (after ingestion capture + dedup + Character Register schema). |
| N5 | *"An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."* | v1.0 §6.3 P100 | — | **NOT-YET-IN-SCOPE.** Character Register write path does not exist. Follow-on wave anchor: v1.0 §15 P231 sequences this as build-item 3. |
| N6 | *"Every constructed identity is scored against every speaker representation derivable from the corpus using standard speaker-verification methods. A minimum distance from all of them is required. Below threshold, the identity is rejected and resampled. There is no override."* | v1.0 §7.2 P109 | — | **NOT-YET-IN-SCOPE.** Voice identity invention plane is P2 (v1.0 §15 P239). |
| N7 | *"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned: An Outcome without an existing test_set_ref. An acceptance bar missing the per-stratum dimension. A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."* | v1.0 §8.4 P139..P142 | Objective Wizard exists at B-2/B-3 stage per `notes/*` — [VERIFY] item V94/V154 | **PARTIAL · needs [VERIFY].** v1.0 §16.1 P245 explicitly registers this as a [VERIFY] item. |
| N8 | *"The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time."* | v1.0 §10.2 P168 | — | **NOT-YET-IN-SCOPE.** Follow-on wave anchor: v1.0 §15 P235 build-item 7 (TargetOutcome type). |
| N9 | *"A plan without a calibration stage is rejected. The first job prices the real job."* | v1.0 §11.2 P181 | — | **NOT-YET-IN-SCOPE.** Follow-on wave anchor: v1.0 §15 P236 build-item 8 (Sampling & Reflection). |
| N10 | *"Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."* | v1.0 §13.4 P210 | — | **NOT-YET-IN-SCOPE.** Commission View is v1.0 §15 build-item 9 (P237). |

---

## §16.2 open decisions requiring owner ruling (surfaced clean · verbatim)

Per owner directive item E: *"§16.2 open decisions that need owner ruling: surface as a clean list."*

| Open decision (verbatim) | v1.0 anchor | Why it needs ruling now |
|---|---|---|
| **N for the shared-attribute condition (§6.2.2): inherit the platform minimum-group-size seam value, or set a register-specific one.** | P247 | Character Register build-item 3 in §15 cannot land without N. |
| **Platform default for gate_policy (§10.1) where an Outcome does not set it: missed stratum gates release, or ships documented. This default silently decides how minority-variant quality is treated under schedule pressure.** | P248 | TargetOutcome type build-item 7 in §15 cannot land without this default (or an explicit "no default · every Outcome must set it" ruling). |
| **Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3).** | P249 | Build-item 5 in §15 requires this. |
| **Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built (§3, §11.2).** | P250 | Deferrable — the doc itself defers to Sampling & Reflection to answer. But the census sequences before this: the codec choice is downstream of what the census finds (per Canon-17-19 §A17.11 M-03/M-04). |
| **Baseline tier contents (§9.2): the v1.0 set is the proposal; every addition is paid on every hour ingested, every omission is paid at re-ingestion.** | P251 | The v1.0 baseline set (5 items: language ID · code-switch points · condition profile · dedup instance condition map · synthesis-relevant group-level acoustics) is a proposal awaiting ratification. All follow-on ingestion waves depend on this ruling. |

---

## Summary

**Drift on already-sealed mechanism:** modest, and all of it is **NOT-YET-IN-SCOPE** rather than deviation. The two real forward-facing drift items are:

* **D7 (`TranscriptArtefact` lacks `codec_version` carrier)** — bites when the estate's own future codec produces transcripts (v1.0 §3.2 P048). Legacy OBS transcripts are exempt (no codec of ours produced them).
* **D9 (`admit_transcript_release` has no explicit receipt-write step)** — bites when Pull Seam Stage-2 lands the unified `Receipt.v0` schema.

**Anchor drift on §1.2 citations across the four M5 canon-anchor notes:** **zero.** The §1.2 clause was stable across the retired drafts and v1.0.

**Model-choice drift:** the POC's default (faster-whisper + whisper-tiny) is **canon-consistent as a CI fixture path**; production ASR selection is canon-deferred until first census activation. Silero (VAD) and pyannote (diarisation) are **INFERRED** — deployed in-repo but not canon-named; require owner ratification under the Verbatim-canon standing rule. My earlier "whisper.cpp fall-back" is **superseded** (zero canon support).

**Ten NOT-YET-IN-SCOPE items (N1..N10)** enumerate v1.0 clauses no wave has yet chartered. §15 build sequence gives the intended dependency order.

**Five §16.2 open decisions** need owner ruling before their downstream build items in §15 can land.

---

## Cross-links

* Verbatim requirements: `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md`.
* Model-spec table: `notes/CANON_MODEL_SPECS_VERBATIM_20260914.md`.
* Pull Seam requirements: `notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md`.
* Structured extract: `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt`.
* Standing rule: DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
