READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-CENSUS-CANON-ALIGN · Wave Grounding Brief

**Wave ID:** W-CENSUS-CANON-ALIGN
**Charter class:** pre-census discipline-alignment wave (Option-α, ratified 2026-09-15T~02:05Z)
**Chartered from:** owner ruling 2026-09-15T~02:05Z (verbatim): *"go as recomended - a (run this on the GPUs). Build what needs to be built to run this."*
**Standing constraints:** tests-first · double-green byte-match · local two-commit (track-a code + master state) · never push · position-redaction hard-lock · egress window 08:00–02:00 UTC · verbatim-canon rule (DECISIONS.md 2026-09-15T~01:40Z) · terminal pytest only · testing_agent BANNED · HALT-rather-than-guess
**Precedent wave templates:** W-DATA-SUITE-V2-LIFT (M5 SW2) · W-SOLVA-V2-LIFT (parameterless boundary FIRST · engine skeletons HALT)
**Anchor ratchet floor at open:** 3979
**Target ratchet at close:** 3979 → 4015..4030 (+36..+51 across CP-C1..CP-C6)

---

## §A · Grounding · verbatim canon anchors

Every clause below carries a verbatim quote + source file + section. **No INFERRED requirements enter this brief.**

**A1 · Owner ruling this turn (verbatim, 2026-09-15T~02:05Z):**
> *"go as recomended - a (run this on the GPUs). Build what needs to be built to run this."*
> *"Option α is RATIFIED. Execute now, autonomously, under all standing discipline (tests-first, terminal pytest only, double-green byte-match, local two-commit, never push, position-redaction, egress window, verbatim-canon rule)"*
> *"D12 (CI-fixture transcription POC) stays OPEN — do not run it; owner will rule after census results."*

**A2 · Canon-4 §4 · verbatim, `canon/text/Akki_Canon_4_Operating_Engines.txt:26`:**
> *"The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity. One census serves every objective; no objective is consulted during the walk."*

**A3 · Canon-4 §4.1 · verbatim, `canon/text/Akki_Canon_4_Operating_Engines.txt:28..30`:**
> *"Per source and per stratum: volume, media types, languages, era distribution, quality strata, the share already verified, the share carrying personal data, the share licensed for external use — and, explicitly, what has not been measured."*
> *"Unmeasured is a first-class value."*
> *"Every figure carries its method."*

**A4 · Canon-4 §5.1 declaration baseline · verbatim, line 35:**
> *"A per-feed declaration, applied to every source under that feed — deterministic, low-cardinality, and always available. It is the certain floor the whole measure rests on … An undeclared feed resolves to unknown, which is the conservative value — absence of a declaration never resolves upward."*

**A5 · Canon-4 §8 · verbatim, line 52:**
> *"One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."*

**A6 · Master Requirements Registry · Doc-9 Requirement #13 B5.1..B5.7 · verbatim, `canon/drops/20260910/extracted/text/Master_Requirements_Registry.md:144..150`:**
> B5.1 *"The census is exhaustive and objective-blind; one measure serves all"*
> B5.2 *"Unmeasured is recorded as unmeasured"*
> B5.3 *"Every figure resolves to its method"*
> B5.4 *"The two-layer measure scales without per-item labelling"*
> B5.5 *"The defensibility verdict is a deterministic matrix lookup carrying its rule reference"*
> B5.6 *"Freshness is a mechanism, not a schedule"*
> B5.7 *"Sensitivity classification is the single entitlement attribute"*

**A7 · Master Requirements Registry · Doc-10 Requirement #14 A5.5 · verbatim, `Master_Requirements_Registry.md:155`:**
> *"The Registry is one record, read by many"*

**A8 · Canon-17-19 §A17.11 · verbatim, `canon/text/Akki_Canon_Documents_17_19.txt:84`:**
> *"named at first census activation … the census (Documents 9–10) runs first, and the specific model is named after, informed by what the census actually finds in the estate — not chosen speculatively ahead of it on the strength of a published benchmark."*

**A9 · Canon-4 §Class-activation · verbatim, `canon/text/Akki_Canon_4_Operating_Engines.txt:291`:**
> *"The census activates matrix rows. A class with no material in the estate stays dormant — registered, instrumented on paper, zero build. A class the census actually observes activates: its checkpoints join the estate's first-measurement sample and its thresholds bind before that class enters production mining."*

**A10 · Owner S5 reframe · verbatim, `notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:4,25`:**
> *"build as a GENERIC, SCALABLE SYSTEM (a platform), NOT structured to this specific case … there is 'what the system should be' and separately 'mounting THIS job onto the system.'"*
> *"the platform builds estate-agnostic + modality-agnostic primitives. A job (audio census on 16 Kenyan stations OR text training on Aurora DBs OR an image-taxonomy census on an S3 bucket) is a mounting artifact — a JobManifest that binds the platform's registered planes to a concrete instance. Nothing case-specific may live in the platform code path."*

**A11 · Pull Seam Principle 1 · verbatim, `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam.txt` P015.s5..s7:**
> *"An outside party who wants a model shaped by the estate's data sends the model in; the model trains next to the data and leaves as weights. There is no configuration in which estate data is transferred to compute outside the perimeter. This is a prohibition with no exception, not a default setting."*

**A12 · Audio Plane v1.0 §1.4 · verbatim, `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` P019:**
> *"No data-volume requirement, accuracy expectation, or cost figure is quoted without a measurement behind it. The calibration stage exists to convert assertions into measurements before commitment."*

---

## §B · CP scope · mechanism landings

Six CPs. Each CP = its own RED-then-mechanism cycle with double-green byte-match, ratchet manifest bump, and two-commit pattern (track-a code + master state).

| CP | Focus | Canon anchor | Landed module | Invariants target |
|---|---|---|---|--:|
| **CP-C1** | Frozen `SourceCandidate` with Canon-4 §4 carriers (`source_reference`, `region`, `feed_identity`, `sensitivity`) + deterministic sensitivity classifier carrying rule reference (B5.5) | A2, A6 B5.5, A6 B5.7 | `contracts/canon_census_source_candidate.py` + `services/census_canon/source_candidate_classifier.py` | 6 |
| **CP-C2** | `Unmeasured` first-class sentinel value (B5.2) + `Measurement` frozen carrier with `method` field (B5.3) + full-vs-sampled flag | A3, A6 B5.2, A6 B5.3 | `contracts/canon_census_measurement.py` | 6 |
| **CP-C3** | `CensusRun` + `CensusRunId` deterministic gen · records `run_date`, `population`, `full_vs_sampled` at the run level | A3, A6 B5.3 | `services/census_canon/census_run.py` | 6 |
| **CP-C4** | Append-only registry write path: `register_source_candidate(candidate, run_id) -> record_id` (Canon-4 §8 · Doc-10 A5.5) | A5, A7 | `services/census_canon/registry_write.py` | 6 |
| **CP-C5** | `JobManifest` frozen carrier per S5 reframe · binds a job (source connectors + registry + capabilities) onto the case-agnostic platform | A10 | `contracts/census_job_manifest.py` | 6 |
| **CP-C6** | Canon-4 §4.1 output-field carriers (`SourceStratumMeasurement` with 8 dimensions: volume/media_types/languages/era/quality/verified_share/pii_share/licence_share) + `activation_list` carrier per A9 | A3, A9 | `services/census_canon/stratum_measurement.py` + `services/census_canon/activation_list.py` | 6 |

**Total target invariants:** ~36 (aligned with owner's ~+10–15 estimate stretched to fit six discrete concerns).

---

## §C · Wave-honest limits

**E.1 · First-run shape acceptable for B5.6 (freshness).** Full structural-delta freshness mechanism is out-of-scope this wave; a `freshness_stamp` field on the source record + a `next_recheck_hint` field are the first-run shape. Follow-on wave lands the structural-delta re-run trigger.

**E.2 · Two-layer measure (§5.1 declaration baseline + §5.2 inference overlay) is out-of-scope.** This wave lands the **shape** for measurement carriers (Unmeasured + Measurement.method) but not the two-layer measurement mechanism itself. The census run will produce declarations at the feed level and emit `Unmeasured` for every dimension the census doesn't have a method for. A follow-on wave lands the inference overlay.

**E.3 · Perception pipeline (Doc-9 Requirement #15 C5.1..C5.6) is out-of-scope.** The audio POC's per-file inventory does not invoke the perception pipeline; the census records aggregate composition at file-level and emits `Unmeasured` for per-segment properties (languages[]/condition_profile/switch_points). Follow-on wave chartered by v1.0 §15 build-item 1 (`W-AUDIO-INGEST-STAGE-1`).

**E.4 · JobManifest is a shape-and-binding contract, not a runtime orchestrator this wave.** CP-C5 lands the frozen carrier. Wiring existing audio-poc surfaces (`recording_inventory`, `transcript_inventory`, `pairing_registry`) as registered plane implementations behind the JobManifest is deliberate follow-on. This wave keeps the JobManifest as a data-only contract per Solva-V2 CP-S2 parameterless-boundary precedent.

**E.5 · Registry-write is append-only.** No update path this wave. A source-record correction lands as a new record with a link to the superseded record (Canon-3 §9.3 append-only ledger spirit precedent from CP-D5).

**E.6 · GPU-host bind is out-of-scope this wave.** Owner directive item 2: *"If NO GPU is reachable from here: do NOT stall — run the census (it is I/O-and-metadata dominated, CPU-fine), and bank a bind-gap note."* The wave builds the census machinery on-pod (CPU-viable · in-perimeter) and the actual live-census execution (Item 3 of the directive) is a separate step post-wave. GPU-host bind is a separate wave.

**E.7 · D12 (transcription POC) stays OPEN.** Owner ruling this turn: *"D12 (CI-fixture transcription POC) stays OPEN — do not run it; owner will rule after census results."*

---

## §D · Commit protocol

**Per CP** (Solva-V2 precedent · same as W-DATA-SUITE-V2-LIFT):
* Commit A on `programme/track-a`: code + tests + ratchet manifest bump.
* Commit B on `master`: DECISIONS entry + NEXT.md refresh + drill receipts.

**Wave close:**
* Composite seal at `phase0/output_verified_seals/census_canon_align.seal.txt` · `Kind: census_canon_align` · Green1/Green2 sha256 pinned · byte-match TRUE.
* Rider 1: `pip freeze` + `pytest --collect-only`.
* Owner-facing 5-section close report at `notes/W_CENSUS_CANON_ALIGN_close.md`.

**Guardrails held whole wave:** no push · no `testing_agent` · no refactor · no wipe · no re-clone · no head/cat/sed on custody · terminal pytest only · position-redaction hard-lock · verbatim-canon rule.

---

## §E · §G stop conditions (verbatim from prior waves · unchanged)

Halt-and-report on any of:

1. **Real RED that doesn't hold** — a receipt that shows anything other than the expected right-reason failure.
2. **Ratchet retreat** — any bump that would take the floor DOWN.
3. **§16.2-class ambiguity** — a canon clause I cannot locate verbatim on disk when authoring a docstring citation.
4. **Egress window straddle** — no live-egress work during 02:00–08:00 UTC; the census run (Item 3) will HALT at 02:00 UTC if straddled and resume at 08:00 UTC.
5. **Pull Seam Principle 1 violation** — any code path that transfers estate bytes to outside compute.
6. **Verbatim-canon rule violation** — a docstring, brief, or receipt that carries an INFERRED requirement without owner ratification.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
