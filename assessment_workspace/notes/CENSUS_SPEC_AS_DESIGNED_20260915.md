READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CENSUS_SPEC_AS_DESIGNED_20260915.md

**Purpose.** Answer the owner's question — *"Do you remember the Census spec we designed?"* — by locating the census specification on disk exhaustively, quoting it verbatim, and mapping our planned census run against it.

**Discipline anchor:** DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline · every requirement citation carries verbatim quote + source file + section).

**Search receipts (this session).** Case-insensitive grep across `canon/`, `notes/`, `STATE/`, and `repos/*/` for `census`, `census-and-connection`, `Promise #12`, `first census activation`, `W-AUDIO-POC-3-STATIONS`, `media census`, `audio census`, `Canon-17-*`, `Canon-4`, `Documents 9–10`, and `estate_registry`.

---

## §A · Where the spec lives — the six load-bearing sources on disk

| # | Source | Location | What it carries |
|---|---|---|---|
| **S1** | Canon-4 · §4 The Census + §10 Mtafiti's Invariants | `canon/text/Akki_Canon_4_Operating_Engines.txt` lines 25–90 (§4 + §5 two-layer) and lines 57–66 (§10 invariants) | Canon-level census doctrine — the "walks-the-estate-exhaustively-and-objective-blind" definition + per-source/per-stratum output fields + unmeasured-is-first-class + every-figure-carries-method + 8 Mtafiti invariants. |
| **S2** | Master Requirements Registry · Doc-9 census rows | `canon/drops/20260910/extracted/text/Master_Requirements_Registry.md` lines 144–160 | 7 CANON invariants for THE CENSUS (`B5.1..B5.7`) + 4 CONNECTION invariants (`A5.1..A5.4`) + 6 PIPELINE invariants (`C5.1..C5.6`) — each carrying a `Doc 9` anchor + a specific line-ref into the source doc `09_Estate_Registry_Part_1_Connection_and_Census.md`. |
| **S3** | Canon-17-19 · §A17.10 + §A17.11 (parity: Canon-17-20-v3 §A17.10 + §A17.11 + §A20.11) | `canon/text/Akki_Canon_Documents_17_19.txt` lines 70–88 + `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt` lines 110–128 + line 369 | The "first census activation" clause that gates production model naming — CI fixture named; production selection deferred until census runs; audio's census-first rule is the general rule's origin, not an exception. |
| **S4** | Doc-0 · Promise #12 · "census-and-connection" | `canon/drops/20260910/extracted/text/Akki_Governance_Architecture_v1_from_15.txt` line 241 (parity: 20260909/20260907) | *"STATUS Partial — census and connection are specified (Promise #12); a published class list was not located."* — the anchor citation for Promise #12 in the Governance Architecture document. |
| **S5** | Governed Census + Harvest Platform Roadmap | `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md` (889 lines, banked 2026-09-12) | The DESIGN REFRAME: build census as a **generic scalable platform** (10 planes: Resource/Source/Capability/Objective/Outcome/Success/Commission/Supervision/HITL/Governance) with a `JobManifest` mounting each concrete case (audio, DB, image, video). Owner directive verbatim in the header (2026-09-12T~15:00Z). |
| **S6** | W-AUDIO-POC Scoping (16 Kenyan stations) | `notes/W_AUDIO_POC_SCOPING_20260912.md` (339 lines, banked 2026-09-12) | The audio-poc-specific census scoping: NAS reachability findings, audio capability location + LoC, model deps in `requirements.txt`, maturity assessment, per-surface pipeline stages. |

**Missing on disk (surfaced honestly, not silently):**

* `09_Estate_Registry_Part_1_Connection_and_Census.md` and `10_Estate_Registry_Part_2_Comprehensive_Registry.md` — the two documents the Master Requirements Registry cites with explicit line-refs — are NOT present on disk under any canon path. The 7 CANON census invariants + 4 connection + 6 pipeline invariants are cited by line into files that this workspace has never received. **`find canon -name "09_Estate_Registry*"` returns zero. `find canon -name "10_Estate_Registry*"` returns zero.** The invariant list in Master Requirements Registry is the strongest on-disk record we have of what those docs say.

**Implementation surfaces on disk (repos/Extraction-Akki/backend/):**

* `services/mtafiti/census.py` — canon-4-shaped `SourceCandidate` dataclass + `census()` iterator + `classify_sensitivity()` + region/feed_id extractors.
* `services/mtafiti/composition_census.py` — SQL-side composition census with receipt-writing.
* `services/census_engine/engine.py` — multi-DB enumeration + `run_census()` + `enumerate_databases()` + `_next_census_id()`.
* `services/census_dimensions/dimensions_service.py` + `dimensions_loader.py` + `census_content_surfaces.v0.json` + `census_genres.v0.json` — dimensions layer.
* 7 pytest invariant tests: `test_census_dimensions.py`, `test_census_dimensions_ast_gate.py`, `test_census_dimensions_wire_shape.py`, `test_census_engine_contract.py`, `test_census_wire_shape.py`, `test_mtafiti_gpu_discovery_composition_census.py`, `test_ruling5_census_clarification_drawer_contract.py`.
* `services/audio_poc/{recording_inventory, transcript_inventory, pairing_registry, gap_set, classify_transcript_status}.py` — file-level, shape-only census machinery for NAS OFFAIRRECS + OBS google-transcripts (W-AUDIO-POC).
* `tools/mtafiti_composition_census.py` — CLI runner.

**Prior census run outputs on disk:** `notes/census_1_media_landscape.json` — a 13-column media-shaped-column census output from `digicow_live` + `ndume` MySQL databases (rows 42 to 2,286,019). Empirical proof the DB-side census machinery has been run.

---

## §B · Verbatim core clauses (the six sources, quoted)

### S1 · Canon-4 §4 The Census (verbatim, `canon/text/Akki_Canon_4_Operating_Engines.txt` lines 25–33)

> *"[Heading 1] 4  The Census"* (line 25)
>
> *"The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity. One census serves every objective; no objective is consulted during the walk."* (line 26)
>
> *"[Heading 2] 4.1  What the census produces at estate level"* (line 27)
>
> *"Per source and per stratum: volume, media types, languages, era distribution, quality strata, the share already verified, the share carrying personal data, the share licensed for external use — and, explicitly, what has not been measured."* (line 28)
>
> *"Unmeasured is a first-class value. A dimension not measured is recorded as unmeasured, never as zero, absent, or clean. A blank that reads as clean makes the whole instrument dishonest."* (line 29)
>
> *"Every figure carries its method. Any measurement a surface displays resolves to the census run that produced it, its date, the population measured, and whether the measurement was full or sampled — a sampled measurement is never presented as a full-population one."* (line 30)
>
> *"The sensitivity classification assigned here is the resource attribute Document 3 §22.1's entitlement rules match a requester's attributes against. No second classification exists for that purpose; entitlement reads this one."* (line 31)

### S1 · Canon-4 §10 Mtafiti's Invariants (verbatim, lines 57–66)

> *"[List Paragraph] The census is exhaustive and objective-blind; one measure serves every objective."*
>
> *"[List Paragraph] The declaration baseline is deterministic, feed-level, and always available. An undeclared feed resolves to the conservative value."*
>
> *"[List Paragraph] The inference overlay emits detections only. It never imports the verdict logic and never assigns a class."*
>
> *"[List Paragraph] The verdict is a deterministic matrix lookup carrying its rule reference. It contains no model."*
>
> *"[List Paragraph] The overlay influences the measure only after its admission gate passes; the baseline stands alone until then, and the Registry records which regime applied."*
>
> *"[List Paragraph] The measure never overstates standing and fails toward caution."*
>
> *"[List Paragraph] An unmeasured dimension is recorded as unmeasured, never as zero or clean."*
>
> *"[List Paragraph] A stale or un-censused region returns unknown rather than a fabricated distribution."*

### S1 · Canon-4 §5 The Two-Layer Measure — §5.1 declaration baseline + §5.2 inference overlay (verbatim, lines 33–37)

> *"The defensibility measure is produced in two layers, so it scales across a very large estate without labelling every item by hand."*
>
> *"[Heading 2] 5.1  The declaration baseline · A per-feed declaration, applied to every source under that feed — deterministic, low-cardinality, and always available. It is the certain floor the whole measure rests on, and it is never assigned per item: per-item declaration at estate scale is exactly the human bottleneck the two-layer design exists to avoid, and a per-item declaration that drifts over time is worse than a stable feed-level one. An undeclared feed resolves to unknown, which is the conservative value — absence of a declaration never resolves upward."*
>
> *"[Heading 2] 5.2  The inference overlay · The overlay detects defensibility signals in content itself — whether a report attributes and cites, whether its genre form is event-anchored or monologic, whether a claim corroborates across independent estate units — and emits detections with confidences attached. It emits detections and nothing else: an attachment-markedness value, a detected genre-form label, a corroboration value, and the confidence on each. A genre-form label is a detection, not a verdict."*

### S1 · Canon-4 §8 The Registry and Freshness (verbatim, lines 51–53)

> *"[Heading 1] 8  The Registry and Freshness"*
>
> *"One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."*
>
> *"Freshness is maintained by a logged date and a structural-delta check, driving scoped re-discovery of only the affected region and re-running the measure for that region alone. A retraction changes contested status, so a region's measure changes exactly when the estate's own record of a claim changes — which is why freshness is a mechanism rather than a fixed schedule."*
>
> *"A stale or un-censused region returns unknown to a feasibility query, never a fabricated distribution. No objective freezes against an estate the system has not measured."*

### S2 · Master Requirements Registry · Doc-9 CANON census invariants (verbatim, `canon/drops/20260910/extracted/text/Master_Requirements_Registry.md` lines 144–150)

**Requirement #13 · THE CENSUS · Doc 9 · owner: Mtafiti · anchor: `09_Estate_Registry_Part_1_Connection_and_Census.md`.**

| Row | Verbatim requirement | Line-ref | Class |
|---|---|---|---|
| **B5.1** | *"The census is exhaustive and objective-blind; one measure serves all"* | `:109` | CANON |
| **B5.2** | *"Unmeasured is recorded as unmeasured"* | `:111` | CANON |
| **B5.3** | *"Every figure resolves to its method"* | `:113` | CANON |
| **B5.4** | *"The two-layer measure scales without per-item labelling"* | `:115` | CANON |
| **B5.5** | *"The defensibility verdict is a deterministic matrix lookup carrying its rule reference"* | `:117` | CANON |
| **B5.6** | *"Freshness is a mechanism, not a schedule"* | `:119` | CANON |
| **B5.7** | *"Sensitivity classification is the single entitlement attribute"* | `:121` | CANON |

**Requirement #12 · CONNECTS TO ALL DATABASE TYPES · Doc 9 (paired with the census, connection is the pre-cursor).**

| Row | Verbatim requirement | Line-ref | Class |
|---|---|---|---|
| **A5.1** | *"One intake contract, no second path"* | `:55` | CANON |
| **A5.2** | *"Connection is inside the perimeter"* | `:57` | CANON |
| **A5.3** | *"Connection is a governed, recorded operation"* | `:59` | CANON |
| **A5.4** | *"The completeness claim is honest about connector gaps"* | `:61` | PROPOSED |

**Requirement #15 · READS ANY DATA TYPE, INCLUDING AUDIO · Doc 9 (the modality-uniform pipeline the census must read into).**

| Row | Verbatim requirement | Line-ref | Class |
|---|---|---|---|
| **C5.1** | *"The pipeline is modality-uniform"* | `:169` | CANON |
| **C5.2** | *"Perception crosses as a frozen job, returns as a frozen result"* | `:171` | CANON |
| **C5.3** | *"Grounding markers resolve to source position"* | `:173` | CANON |
| **C5.4** | *"Every perception model is registered with hash and licence"* | `:175` | CANON |
| **C5.5** | *"Perception calls route through the boundary governor"* | `:177` | CANON |
| **C5.6** | *"The execution seam keeps hardware invisible to consumers"* | `:179` | CANON |

**Requirement #14 · THE COMPREHENSIVE REGISTRY · Doc 10 (the storage side of the census output).**

| Row | Verbatim requirement | Line-ref | Class |
|---|---|---|---|
| **A5.1** | *"Every field resolves to its census method"* | `10_Estate_Registry_Part_2_Comprehensive_Registry.md:67` | CANON |
| **A5.2** | *"Opportunity Briefs are advisory and grounded"* | `:69` | CANON |
| **A5.3** | *"Cleanliness and duplication [CANON, assembled + RULED]"* | `:71` | — |
| **A5.4** | *"Linkage to other datasets [RULED — the one field with no canon home, now specified]"* | `:75` | — |
| **A5.5** | *"The Registry is one record, read by many"* | `:79` | CANON |

### S3 · Canon-17-19 §A17.11 (verbatim, `canon/text/Akki_Canon_Documents_17_19.txt` lines 83–85 · full clause)

> *"A17.11  [CANON] Production selection is named after the census, not before it."*
>
> *"Production base model selection lands additively at a later registry bump — 'named at first census activation' — following the identical license-verify → checksum-pin → Owner-ruling sequence already registered for the Qwen3 and Llama text-generation candidate rows in the same file. Those rows exist today as class-level registrations with zero download and zero compute: parameters known, license disclosed or flagged for acquisition-time verification, specific members deferred. The same discipline governs audio. The sequencing consequence is direct: the census (Documents 9–10) runs first, and the specific model is named after, informed by what the census actually finds in the estate — not chosen speculatively ahead of it on the strength of a published benchmark."*

### S3 · Canon-17-19 §A17.11 tail — rights-declaration prerequisite (verbatim, line 94)

> *"Admission is blocked without rights lineage — the same discipline that governs every other admitted object on the platform. The sequencing this implies is not incidental: the census and rights-position machinery (Documents 9–10) is precisely what produces this declaration from an estate. For any customer engagement, the order is census → rights declaration → corpus admission → trainer, not a parallel track that could start independently."*

### S3 · Canon-17-20-v3 §A20.11 (verbatim, `canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.txt` line 369)

> *"A20.11  [CANON] Audio's resolution rule is not this document's to set. Document 17 A17.10–A17.11 already rules it: whisper-tiny is CI-fixture-only; production selection lands additively at a later registry bump, named at first census activation, following the identical license-verify → checksum-pin → Owner-ruling sequence this document uses for every other dimension. That sequencing is inherited here unchanged — audio's census-first rule is the general rule's origin, not an exception to it."*

### S4 · Doc-0 Promise #12 anchor (verbatim, `canon/drops/20260910/extracted/text/Akki_Governance_Architecture_v1_from_15.txt` line 241)

> *"STATUS  Partial — census and connection are specified (Promise #12); a published class list was not located."*

**Note:** Doc-0 in this corpus does not carry the FULL text of Promise #12 verbatim; it carries the STATUS anchor pointing at Promise #12. The full Promise #12 text is intended to live in `09_Estate_Registry_Part_1_Connection_and_Census.md` (absent on disk) and its CANON invariants (B5.1..B5.7 + A5.1..A5.4 + C5.1..C5.6) are the verbatim record we have.

### S5 · Governed Census + Harvest Platform Roadmap · load-bearing clauses (verbatim, `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md`)

> **Owner directive header** — *"Directive received: 2026-09-12T~15:00Z (owner) — 'build as a GENERIC, SCALABLE SYSTEM (a platform), NOT structured to this specific case ... there is "what the system should be" and separately "mounting THIS job onto the system."'"* (line 4)
>
> **Reframe rationale** — *"The owner's reframe is not a departure from spec; it is a direct read of spec §1.2 anti-proliferation + §1.1 recursion + Canon 4 §5 estate-scale invariance."* (line 15)
>
> **Consequence** — *"the platform builds estate-agnostic + modality-agnostic primitives. A job (audio census on 16 Kenyan stations OR text training on Aurora DBs OR an image-taxonomy census on an S3 bucket) is a mounting artifact — a `JobManifest` that binds the platform's registered planes to a concrete instance. Nothing case-specific may live in the platform code path. This is the spec's own anti-proliferation discipline pushed one level up."* (line 25)
>
> **Ten planes** — Resource · Source · Capability Registry · Objective (L1) · Outcome + Quality (L2) · Success + QC (L3) · Commission + Worker (L4) · Supervision (L5) · HITL (L6) · Governance. (line 30–40)
>
> **Cross-plane invariants** (line 42–48): Determinism boundary · Detect-autonomously / decide-only-with-owner-ruling (Ruling #5 pattern) · Absence-is-a-finding (Canon 4 §41 C4-057) · One-record law (Canon 9 C9-005) · Alive-is-not-done (new standing order) · No-run-without-progress-signal (new standing order).

### S6 · W-AUDIO-POC Scoping · load-bearing clauses (verbatim, `notes/W_AUDIO_POC_SCOPING_20260912.md`)

> **Task class** — *"Scoping / Discovery ONLY. No product code. No pytest. No ratchet touch (floor 3251 held). No downloads. No commits of credentials. No push."* (line 3)
>
> **NAS reachability verdict** — *"Verdict: NAS `10.10.55.55:5000` is unreachable from this pod."* (line 12) — four-probe evidence line 14–20.
>
> **Read-only ceiling** — *"even if reach lands, the standing law's scoping-only clause holds — at most enumerate top-level folder names and confirm the API surface (Synology DSM `FileStation` API at `/webapi/entry.cgi?api=SYNO.FileStation.List`). No file downloads. No audio movement."* (line 28)
>
> **Audio-pipeline location + maturity** — *"the audio capability lives in `Extraction-Akki` and only in `Extraction-Akki`. It is a well-structured, contract-first, CI-fixture-tier pipeline with real ASR + diarization providers wired but not-yet-run-against-real-audio."* (line 33) — followed by ~2,000 LoC inventory in §II.1 (line 38–70) and dep-list in §II.2 (line 72–79).
>
> **Overall maturity read** — *"the AUDIO PIPELINE IS THERE. Contracts, atomics, providers, GPU framework — the shape is complete. What's missing is (a) the ffmpeg/Silero backend adapters under `backends/`, (b) pyannote.audio + HF token installed for local diarization, (c) a language-ID module, (d) a music/speech binary classifier (vs the VAD's label-only content-type index), (e) a speaker-embedding extractor. Zero of these are new engines; four of five are wave-scope adds inside the existing perception package. That's a MODIFY / EXTEND posture, not a BUILD-FROM-SCRATCH."* (line 96)

---

## §C · Gap table — designed spec clause × what our planned census run covers

Our earlier proposed default scope (from my previous turn): *"full NAS OFFAIRRECS inventory across all 16 channels/dates (bounded, read-only, shape-only), full OBS google-transcripts inventory, deterministic pairing, gap-set. Include the 2 reachable MySQLs (weego, ussd) in the census scope if the designed census covers DB sources."*

| Designed spec clause (verbatim, source) | Our planned census-run behaviour | Verdict |
|---|---|---|
| **§B S1 P26** *"walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source"* | Enumerates all files under NAS OFFAIRRECS + all OBS keys under google-transcripts; 16 channels × 90 days; 1 candidate per file (RecordingEntry) — objective-blind (no channel/date filter beyond scope) | **COVERED (audio surface only)** |
| **§B S1 P26** *"Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity"* | RecordingEntry carries: station, date_utc, slot, filename_stem, size_bytes, mtime_utc. **No** `region`, **no** `feed_id`, **no** `sensitivity` classification | **PARTIAL — 3 of 4 canon carriers missing** |
| **§B S1 P28** *"Per source and per stratum: volume, media types, languages, era distribution, quality strata, the share already verified, the share carrying personal data, the share licensed for external use — and, explicitly, what has not been measured"* | Planned: volume (file count + size) + date range. **Missing:** media types, languages[], era distribution, quality strata, verified share, PII share, licence share | **PARTIAL — 2 of 8 output fields** |
| **§B S1 P29** *"Unmeasured is a first-class value. A dimension not measured is recorded as unmeasured, never as zero, absent, or clean"* | Currently our census would report the covered fields; **not explicitly** emit `unmeasured` for the 6 missing fields | **DRIFT — must be corrected before run** |
| **§B S1 P30** *"Every figure carries its method. Any measurement a surface displays resolves to the census run that produced it, its date, the population measured, and whether the measurement was full or sampled — a sampled measurement is never presented as a full-population one"* | Our snapshot has `inventory_snapshot_sha256` (content address). **Missing:** explicit census-run-id, date-of-run, population-measured field, full-vs-sampled flag | **PARTIAL** |
| **§B S1 P31** *"The sensitivity classification assigned here is the resource attribute Document 3 §22.1's entitlement rules match a requester's attributes against"* | Not planned — audio POC has no sensitivity classifier | **NOT-YET-IN-SCOPE** |
| **§B S2 B5.1** *"The census is exhaustive and objective-blind; one measure serves all"* | Audio-only. Planned scope: 16 NAS channels + OBS transcripts + 2 MySQLs (weego + ussd). Does not enumerate all connected sources on the estate (Huawei RDS not reachable, transcription-server absent) | **PARTIAL — not exhaustive across estate** |
| **§B S2 B5.2** *"Unmeasured is recorded as unmeasured"* | See P29 above | **DRIFT** |
| **§B S2 B5.3** *"Every figure resolves to its method"* | See P30 above | **PARTIAL** |
| **§B S2 B5.4** *"The two-layer measure scales without per-item labelling"* | Audio POC does not produce a defensibility measure; only inventory shape | **NOT-YET-IN-SCOPE (measurement layer is separate wave)** |
| **§B S2 B5.5** *"The defensibility verdict is a deterministic matrix lookup carrying its rule reference"* | Same as B5.4 | **NOT-YET-IN-SCOPE** |
| **§B S2 B5.6** *"Freshness is a mechanism, not a schedule"* | Planned run is a single snapshot; no freshness stamp beyond `mtime_utc`; no structural-delta re-run trigger | **PARTIAL** |
| **§B S2 B5.7** *"Sensitivity classification is the single entitlement attribute"* | Not planned | **NOT-YET-IN-SCOPE** |
| **§B S2 A5.1** *"One intake contract, no second path"* | NAS uses `readonly_nas_guard`; OBS uses `readonly_obs_guard`; MySQL uses `readonly_sql_guard`. Three distinct read guards, each with its own contract | **PARTIAL — 3 intake contracts, not 1 unified** |
| **§B S2 A5.2** *"Connection is inside the perimeter"* | ✓ NAS + OBS + MySQL reads all happen on estate side of the perimeter | **COVERED** |
| **§B S2 A5.3** *"Connection is a governed, recorded operation"* | ✓ Read guards refuse non-whitelisted ops. Receipts are written for `live_readonly_probe` runs | **COVERED** |
| **§B S2 A5.4** *"The completeness claim is honest about connector gaps"* | Planned run will explicitly note: Huawei RDS unreachable, transcription-server absent, 5 MySQL hosts SG-closed. Consistent with A5.4 [PROPOSED] | **COVERED** (once report explicitly enumerates gaps) |
| **§B S2 C5.1..C5.6** perception pipeline invariants | Audio POC census produces file-level inventory only; does not invoke perception pipeline. `classify_transcript_status` on OBS transcripts is size-based, not perception-based | **NOT-YET-IN-SCOPE (perception pipeline is separate wave)** |
| **§B S3 A17.11** *"the census (Documents 9–10) runs first, and the specific model is named after"* | Yes — census is sequenced before production model selection. This is what the whole run enables | **COVERED (sequencing anchor)** |
| **§B S5 GOVERNED-CENSUS-ROADMAP** — census as case-agnostic 10-plane platform via `JobManifest` | Currently W-AUDIO-POC's census surfaces are audio-specific (recording_inventory, transcript_inventory, pairing_registry). No `JobManifest` layer above them | **DRIFT vs the reframe — audio census is a lookalike, not a JobManifest mounting of the generic platform** |
| **§B S6 W-AUDIO-POC-SCOPING §III surface map** — Connect · Data tile · Mtafiti Census · Northena Data · Northena Rulebook · Solva Audio-Tape trust-receipt · Model Admission | Currently the run would produce a `notes/CENSUS_RUN_20260914.md` markdown report only. **Does NOT write into a Mtafiti registry surface, does NOT write a Northena Data admission event, does NOT write a Model Admission receipt** | **DRIFT — no registry write-back planned** |
| **§B S6 §II speaker-embedding / language-ID / music-detect / ffmpeg-Silero-backend-adapters** gaps | Not resolvable during census; those are perception-plane build items | **OUT-OF-SCOPE for the census (correct)** |

---

## §D · Where the DESIGNED spec DIFFERS materially from our proposed default

Three material differences the owner-verifying question surfaces (my proposed default deviates from the designed spec on these):

1. **The census is designed as a GENERIC PLATFORM, not audio-only.** S5 (Governed Census + Harvest Platform Roadmap · 2026-09-12) reframes the census as a 10-plane case-agnostic platform mounted per-job via a `JobManifest`. Our proposed default (audio channels + OBS + 2 MySQLs) is the AUDIO MOUNTING of that platform — it should be described as such, not as "the census run".
2. **The census is designed to WRITE THE REGISTRY.** S1 §8 and S2 A5.5 both require *"One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."* Our proposed default writes a markdown report at `notes/CENSUS_RUN_20260914.md`. **The designed spec requires registry writes, not a notes report.** The current `services/mtafiti/census.py` produces `SourceCandidate` records but no persistent registry write path is wired into the audio POC pipeline.
3. **The census is designed with EXPLICIT `unmeasured`.** S1 P29 + S2 B5.2 both make unmeasured a first-class value. Our proposed default fields don't yet emit `unmeasured` explicitly for the 6 unmeasured dimensions (media type / languages / era / quality / verified share / PII share / licence share).

**§C also surfaces a downstream drift** (S2 A5.4 rule connection-side "completeness claim is honest about connector gaps"): we HAVE the gap-set machinery, but the current audio-POC gap-set is only recording↔transcript pairing gaps — not connector-completeness gaps (unreachable Huawei RDS, absent transcription-server, SG-closed MySQLs).

---

## §E · Census activation semantics — verbatim

The owner directive asked specifically about "census activation" as a governed event. Verbatim canon references:

* **Canon-17-19 §A17.11** (S3 above · verbatim): *"named at first census activation"* — production model selection lands at this event.
* **Canon-4 §Depth-builds-on-activation** (line 317, verbatim): *"Depth builds on activation. A dormant class carries its row definition and instrument only; full depth builds when a census actually activates it. Speculative depth for a format no estate holds is waste, not diligence."*
* **Canon-4 §Class-activation** (line 291, verbatim): *"The census activates matrix rows. A class with no material in the estate stays dormant — registered, instrumented on paper, zero build. A class the census actually observes activates: its checkpoints join the estate's first-measurement sample and its thresholds bind before that class enters production mining."*
* **Canon-4 §Weak-surface activation** (line 336, verbatim): *"a row populates when a census actually activates the class, never in advance of one."*
* **Canon-4 §Dormant-carries-no-claim** (line 359, verbatim): *"A dormant row carries no product claim. Until a census activates a class, collateral describing it states the method the platform will apply, never a number — the same discipline that governs speech before its own validation completed, applied here before any measurement has been taken at all."*

**Consequence:** "activation" is not a single ceremonial event — it is a **per-class binding trigger**. A census run activates a class *only* if the estate contains material of that class; if it doesn't, the class stays dormant. The output of one census run is therefore a **set of newly-activated classes**, each of which then licenses downstream production work (registry bumps · threshold-binding · model naming).

---

## §F · What our proposed run does NOT do that the designed spec requires

Consolidated from §C/§D/§E:

* **[MISS]** No `feed_id` on RecordingEntry (Canon-4 §4).
* **[MISS]** No `region` on RecordingEntry (Canon-4 §4).
* **[MISS]** No `sensitivity` classification (Canon-4 §4 + S2 B5.7).
* **[MISS]** No explicit `unmeasured` value for the 6 unmeasured dimensions (S1 P29 + S2 B5.2).
* **[MISS]** No `census_run_id · run_date · population_measured · full_vs_sampled` metadata on figures (S1 P30 + S2 B5.3).
* **[MISS]** No registry write-back — planned to write a notes report, not a Registry record (Canon-4 §8 + S2 A5.5).
* **[MISS]** No `JobManifest` above the audio-specific surfaces — audio census is a lookalike, not a case-agnostic platform mounting (S5 reframe).
* **[MISS]** No class-activation semantics recorded — the run would not enumerate which classes it activates (S1 §Depth + Canon-4 line 291).
* **[MISS]** No structural-delta freshness mechanism (S1 §8 + S2 B5.6).
* **[MISS]** No two-layer measure (declaration baseline + inference overlay) — S1 §5 requires this, our proposed run has neither layer.
* **[PARTIAL]** Connector-completeness reporting is planned but as a note, not a first-class field per source (S2 A5.4).

**Present in our proposed default that IS compliant:**

* Read-only-ness inside perimeter (S2 A5.2).
* Governed + recorded operation (S2 A5.3) via existing readonly guards.
* Exhaustive-and-objective-blind across the reachable subset (S2 B5.1 · subject to connector-gaps reporting).
* Sequenced before production model selection (S3 A17.11).

---

## §G · Recommendation (report only · do NOT run)

Two clean options for the owner to rule on:

**Option (α) — RUN AS-DESIGNED (align to canon before executing).** Before the census run, land the missing carriers on `RecordingEntry`/`TranscriptEntry` (feed_id, region, sensitivity), the explicit `unmeasured` first-class value, the census-run-id metadata carrier, and a Registry-write path (write `SourceCandidate` records via `services/mtafiti/census.py` into an actual registry surface, not a notes report). **Cost:** a small pre-census wave (~+10–15 invariants · one or two CPs · terminal pytest only · local commits) to close the drift items in §C/§F before the live run. **Benefit:** the run output is Canon-4-§4-shaped and can serve every objective, not just audio.

**Option (β) — RUN THE LOOKALIKE (as I originally proposed).** Execute the file-level inventory as planned, produce `notes/CENSUS_RUN_20260914.md`, and bank a drift-note that this is an audio-POC lookalike, not the designed generic-platform census. Follow-on wave lands the canonical shape. **Cost:** the run is fast; the deliverable is a note, not a Registry write. **Benefit:** faster feedback loop for the transcription POC; but it violates 4 CANON invariants (B5.2/B5.3/B5.6/A5.5) and the S5 reframe.

**Default I would apply (SO §2, marked `DEFAULT-PENDING-OVERRIDE`):** **Option (α).** Reason: the owner's question this turn is precisely a discipline check that we are running the census AS DESIGNED, not a lookalike. Running the lookalike after being explicitly asked whether we remember the design would compound the failure this turn's directive corrects. Option (α) is a small wave (~+10–15 invariants) that closes the drift and then the run produces a Registry-shaped output.

**HALT before proceeding.** Owner rules.

---

## §H · Search receipts (proof of exhaustive read)

```
grep count under canon/  · "census"                     : 340 hits across 47 files
grep count under notes/  · "census"                     : 1,152 hits across 68 files
grep count under STATE/  · "census"                     : 156 hits (mostly DECISIONS.md history)
grep count under repos/  · "census"                     : (broad; deferred to file-name index above)
find canon/ -name "*Estate_Registry*"                    : 0 files (Doc-9 + Doc-10 absent)
find canon/ -name "09_Estate_*" -o -name "10_Estate_*"   : 0 files
grep "first census activation" under canon/              : 3 files (Canon-17-19 · Canon-17-20-v3 · drops/20260909/doc20 v3-full)
grep "Promise #12" under canon/                          : 3 files (Doc-0 parity across drops/20260907/09/10)
grep "census-and-connection" under canon/                : 6 files (parity across drops)
grep "W-AUDIO-POC-3-STATIONS" under notes/               : 1 file (SCOPING doc)
grep "audio census" under canon/ + notes/                : 47 hits
grep "media census" under canon/ + notes/                : 24 hits (mostly `census_1_media_landscape.json`)
```

**Verdict on the search:** The census specification lives across **6 on-disk sources + 12 in-repo implementation surfaces + 7 pytest invariant tests**. No single dedicated `notes/CENSUS_SPEC_*.md` file exists. The census specification is authoritative in canon (Canon-4 §4 + Master Requirements Registry Doc-9 rows) but the two source docs the Master Registry cites by line (`09_Estate_Registry_Part_1_Connection_and_Census.md` + `10_Estate_Registry_Part_2_Comprehensive_Registry.md`) are NOT on disk. The strongest on-disk verbatim record of what those two Docs say is the 21-row CANON invariant list in `canon/drops/20260910/extracted/text/Master_Requirements_Registry.md` lines 140–160.

---

## Cross-links

* Owner-facing question answer: this document.
* Verbatim-canon standing rule: `STATE/DECISIONS.md` 2026-09-15T~01:40Z.
* Pull Seam requirements (for Pull-Seam conformance of the census): `notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md`.
* Audio Plane v1.0 requirements (for §1.4 measure-not-assert): `notes/AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md`.
* Model-spec ledger: `notes/CANON_MODEL_SPECS_VERBATIM_20260914.md`.
* Drift audit vs built work: `notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
