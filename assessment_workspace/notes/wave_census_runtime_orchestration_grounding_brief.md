READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-CENSUS-RUNTIME-ORCHESTRATION · Grounding Brief (M8 quick-hardening #5 · scope EXPANDED)

**Wave charter trigger.** DECISIONS 2026-08-27T~02:35Z Owner M8 sequencing verbatim (line 8319):

> "Then M8 unblocked quick hardening (small waves, high value): W-TESTS-FIRST-GUARD-INVARIANT → W-EXPORT-ARTEFACT-RENDER → W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL (paired) → W-CENSUS-RUNTIME-ORCHESTRATION → W-AUDIO-PROD-MODEL-SELECT (gated on census activation list — use census results; this names the production model per §A17.11 and is the natural successor to D12)."

**Scope EXPANSION** (owner directive 2026-09-15T~11:05Z verbatim, banked at DECISIONS line 8640):

> "M8 #5 W-CENSUS-RUNTIME-ORCHESTRATION scope EXPANDS per owner ADDITION verbatim: fold ffprobe characterization into live NAS enumeration; new SourceRecord fields `media_types` + `audio_bearing_share` become measured census fields (Canon-4 §4.1 + §8 enrichments)."

Owner GO chain confirmation (2026-09-15T~16:20Z): the paired wave completed, and the ratified next-active-step is this wave *(expanded)*.

---

## §A · Verbatim discharge anchors

### A.1 · Canon-4 §4 (canon/text/Akki_Canon_4_Operating_Engines.txt line 26)

> "The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity."

Discharge in this wave: `enumerate_estate(*, run_id, freshness_stamp, targets, probe_fn=None, feed_declaration_registry=None) -> List[str]` walks a caller-provided target-list objective-blind, produces one `SourceCandidate` per target, classifies sensitivity via CP-C1, and registers each via `register_source_candidate`. Deterministic.

### A.2 · Canon-4 §8 (canon/text/Akki_Canon_4_Operating_Engines.txt line 51)

> "One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."

Discharge in this wave: `SourceRecord` extends from 10 carriers to **12 carriers** with two new §8-enrichment fields — `media_types` (Sequence[str] · default empty tuple) + `audio_bearing_share` (Optional[float] · default None). Both are Optional-default so writes without probe data still succeed; the wave-expansion additions fold measured probe data into the record when a `probe_fn` is provided.

### A.3 · Canon-4 §4.1 (P28, line 28)

> "Per source and per stratum: volume, media types, languages, era distribution, quality strata, the share already verified, the share carrying personal data, the share licensed for external use — and, explicitly, what has not been measured."

Discharge in this wave: `media_types` (from ffprobe `format_name` + `codec_type` roster) is a §4.1 media-types measurement carried on the `SourceRecord` per owner scope-expansion; `audio_bearing_share` (fraction of sampled files whose `max_audio_duration >= 1.0 s`) is a §4.1 quality-strata measurement folded onto the record. Unmeasured is a first-class value (`media_types=()`, `audio_bearing_share=None`).

### A.4 · Canon-4 §5.1 (line 35)

> "An undeclared feed resolves to unknown, which is the conservative value — absence of a declaration never resolves upward."

Discharge in this wave: when `feed_declaration_registry` is None or lacks a feed's entry, sensitivity resolves to `Sensitivity(class_label="unknown", is_undeclared=True, rule_reference="Canon-4 §5.1 conservative fallback")` via CP-C1's `classify_sensitivity`. Absence never resolves upward.

### A.5 · Wave-honest limit precedent (CP-CSAIM1)

CP-CSAIM1 composed CP-C1 + CP-C4 for the NAS+OBS supplement. This wave generalises that pattern into a case-agnostic `enumerate_estate` orchestrator that accepts a `targets` list + optional `probe_fn` injection, so any caller-provided target set can be walked without hard-coding per-source shapes.

---

## §B · CP breakdown (2-CP wave)

| CP | Deliverable | File(s) |
|----|-------------|---------|
| CP-CRO1 | Extend `SourceRecord` from 10 → 12 carriers with `media_types: Tuple[str, ...]` (default `()`) + `audio_bearing_share: Optional[float]` (default `None`). Extend `register_source_candidate(...)` to accept the two new optional kwargs. Extend `_compute_record_id` to fold the new fields into the deterministic hash (so records with different probe data get distinct ids). Update CP-C4 shape test `test_cp_c4_source_record_frozen_canon_4_section_8_carriers` in-place to reflect the 12-carrier expected set with an audit-trail docstring pointing at this wave. | `services/census_canon/registry_write.py` (+2 fields, extended fn) · `tests/invariants/test_wcensus_cp_c4_registry_write.py` (12-carrier expected set) · `tests/invariants/test_wcro_cp_cro1_source_record_extension.py` (new invariants) |
| CP-CRO2 | New `services/census_canon/estate_enumerator.py :: enumerate_estate(*, run_id, freshness_stamp, targets: Sequence[EstateTarget], probe_fn: Optional[Callable] = None, feed_declaration_registry=None, store: RegistryStore) -> List[str]` (record_ids). `EstateTarget` is a frozen dataclass with `(source_reference: str, region: str, feed_identity: str, sample_ref: Optional[str])`. `probe_fn(sample_ref) -> Tuple[Tuple[str, ...], Optional[float]]` returns the `(media_types, audio_bearing_share)` pair — dependency-injected so the wave does NOT invoke ffprobe directly (case-agnostic; test-safe). When `probe_fn` is None OR `sample_ref` is None, no probe runs and defaults apply. Refusals: `CensusTargetsEmptyError` (empty targets); `CensusTargetInvalidError` (non-EstateTarget element in targets). Deterministic. | `services/census_canon/estate_enumerator.py` (new) · `tests/invariants/test_wcro_cp_cro2_estate_enumerator.py` (new) |

**Estimated ratchet delta:** +12 invariants (6 per CP · target: **4093 → 4105**).

---

## §C · Invariants gated (right-reason ImportError REDs before mechanism)

### C.1 · CP-CRO1 (6 invariants)

1. **12-carrier shape.** `SourceRecord` fields exactly `{record_id, source_reference, region, feed_identity, sensitivity, defensibility_measure, freshness_stamp, next_recheck_hint, census_run_id, supersedes_record_id, media_types, audio_bearing_share}`.
2. **New-field defaults.** `SourceRecord(record_id=..., source_reference=..., ..., supersedes_record_id=None)` (without `media_types`/`audio_bearing_share`) constructs with `media_types == ()` and `audio_bearing_share is None`.
3. **New-field types.** `media_types` is `Tuple[str, ...]` (Sequence coerced to tuple); `audio_bearing_share` is `Optional[float]` (None or float in [0.0, 1.0]).
4. **register accepts new kwargs.** `register_source_candidate(..., media_types=("audio/aac",), audio_bearing_share=0.75)` writes a record carrying those values.
5. **record_id hashes new fields.** Two `register_source_candidate` calls identical except for `media_types` yield DIFFERENT record_ids. Two identical-in-every-field calls (including new fields) yield the SAME record_id (idempotent).
6. **CP-C4 shape update banked in-place.** The CP-C4 shape invariant `test_cp_c4_source_record_frozen_canon_4_section_8_carriers` is updated to expect the 12-carrier set with an audit-trail docstring pointing at CP-CRO1. Prior 10-carrier assertion is DISCHARGED (not deleted).

### C.2 · CP-CRO2 (6 invariants)

1. **Module fabric.** `services.census_canon.estate_enumerator` exports `enumerate_estate` + `EstateTarget` + `CensusTargetsEmptyError` + `CensusTargetInvalidError`.
2. **Empty targets refuses.** `targets=()` propagates `CensusTargetsEmptyError` mentioning `targets`.
3. **Non-EstateTarget element refuses.** `targets=(EstateTarget(...), "bad")` propagates `CensusTargetInvalidError`.
4. **Probe-off path.** `probe_fn=None` produces records with `media_types=()` + `audio_bearing_share=None` per CP-CRO1 defaults.
5. **Probe-on path.** `probe_fn=lambda ref: (("audio/aac",), 0.9)` folds those values into the produced record; the returned record_id list has length == len(targets).
6. **Deterministic.** Same inputs + same `probe_fn` returns produce the same list of record_ids (idempotent write path via existing CP-C4 RegistryStore).

---

## §D · Wave-honest limits (declared at open)

1. **E.1** No LLM invocation. No HTTP call. No filesystem write. No direct `ffprobe` invocation in the mechanism — `probe_fn` is dependency-injected so the orchestrator is case-agnostic + test-safe. The actual `ffprobe` shell-out is a caller responsibility (a follow-on ops-wave lands the shell-out under `readonly_nas_guard`).
2. **E.2** `SourceRecord` extension is minimal (2 optional fields with sensible defaults). No breaking rewrite of the CP-C4 register write path.
3. **E.3** Case-agnostic. Word-boundary case-insensitive executive-domain negative-scan across new modules + tests (14-token set from CP-S8/CP-D8/CP-DASWR1/CP-DDDR1 precedent).
4. **E.4** CP-CSAIM1 records (2 records written at CP-CSAIM1 seal · `nas_offairrecs_16ch` + `obs_google_transcripts_bucket`) are NOT rewritten by this wave. If probe data becomes available for those records, correction records land via CP-C4 E.5 append-only with `supersedes_record_id` set — a separate operator-driven follow-on.
5. **E.5** `EstateTarget` is a frozen dataclass carrying only the 4 fields the enumerator needs. Extending it is a scope-expansion event that requires owner ratification.
6. **E.6** No mutation of caller inputs. Both `SourceRecord` and `EstateTarget` are frozen dataclasses.

---

## §E · Commit protocol

- **CP-CRO1 (Commit A on track-a):** code + tests + `baseline_failures.json` bump 4093 → 4099.
- **CP-CRO2 (Commit B on track-a):** code + tests + `baseline_failures.json` bump 4099 → 4105.
- **Wave-close (Commit C on master):** state — DECISIONS entry + NEXT refresh + composite seal + drill receipts + riders + boundary probe #15.
- **Seal:** `phase0/output_verified_seals/w_census_runtime_orchestration.seal.txt` (`Kind: w_census_runtime_orchestration`).
- **NEVER push.**

---

## §F · Decision points / stop conditions

Wave HALTS with a decision-point note if:
- Word-boundary executive-domain negative-scan surfaces a donor token in either engine module or either test file.
- Baseline ratchet regression at CP-CRO1 or CP-CRO2 double-green.
- Any file entering the ratchet path leaks credential-shaped content.
- CP-CRO1 record_id hash change breaks existing CP-CSAIM1 idempotent writes (would surface as regression in existing CP-CSAIM1 invariant tests).

Otherwise wave proceeds per owner directive.

---

## §G · Boundary-hygiene probe cadence

Per DECISIONS 2026-09-15T~09:50Z Effect 4 verbatim: *"Keep the CD/Visitors re-probe loop running at boundaries while egress is open."* Probe #15 fires at wave-close. Standing retry loop continues.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
