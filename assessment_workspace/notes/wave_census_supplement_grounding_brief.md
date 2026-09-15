READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT · grounding brief

**Wave scope.** Single CP. Mount the two audio-plane connectors (NAS 16ch + OBS google-transcripts) into the CP-C4 census `RegistryStore` as first-class `SourceRecord`s, discharging the *"no live-scan tool"* unmeasured-with-reason entries the Item-3 census run banked for these two connectors at `notes/ITEM_3_CENSUS_RUN_20260915.md` §D rows 3–4.

**Owner directive · verbatim (course-correction 2026-09-15T~08:37Z clause a).**

> "(a) census supplement for NAS+OBS via the sealed audio_poc inventories mounted into the census registry (do not defer to M8)"

The "(do not defer to M8)" phrase is the load-bearing clause: without this pull-forward the NAS+OBS registration would land inside M8 W-CENSUS-RUNTIME-ORCHESTRATION. The owner explicitly refused that framing — the supplement lands now, in-scope with the M5 CENSUS-RUN discharge, before the W-RELEASE-GATE-PILOT-LIFT wave-close END-OF-WAVE report.

**Egress posture at wave open.** OPEN (2026-09-15T~09:27Z real wallclock; window 08:00–02:00 UTC per DECISIONS 2026-09-15T~04:12Z Effect 2). No WIP-staging required.

---

## §A · Anchors verbatim (canon-text authority)

**Canon-4 §4** (canon/text/Akki_Canon_4_Operating_Engines.txt:26):
> "The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity."

**Canon-4 §5.1** (line 35, verbatim conservative-fallback clause):
> "An undeclared feed resolves to unknown, which is the conservative value — absence of a declaration never resolves upward."

**Canon-4 §8** (`canon/text/Akki_Canon_4_Operating_Engines.txt:51`):
> "One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."

**Canon-4 §4.1 P29** (first-class-unmeasured verbatim, from CP-C2 landing):
> "Unmeasured is a first-class value."

**W-AUDIO-POC seal** (`phase0/output_verified_seals/audio_poc_v1.seal.txt` · Sealed-at-utc 2026-09-14T13:58:45Z · Kind `audio_poc_wave_close` · CP-A2 13 invariants "recording_inventory contract" · CP-A3 13 invariants "transcript_inventory contract"). This is the "sealed audio_poc inventories" the owner names in directive clause (a). The seal covers the *inventory contracts + snapshot fingerprint machinery* (parse smbclient ls / OBS ListObjects → canonical key → snapshot sha256), not a specific live scan.

---

## §B · Design (one CP · six invariants target)

Single kernel module `backend/services/census_canon/audio_inventory_supplement.py` exposing:

* **Module-level canonical tokens** (byte-identical strings, tested):
  * `NAS_FEED_IDENTITY = "audio_nas_offairrecs_16ch"`
  * `OBS_FEED_IDENTITY = "obs_google_transcripts_bucket"`
  * `NAS_SOURCE_REFERENCE = "nas://OFFAIRRECS/Record/{channel_dir}"` — canonical reference shape per CP-A2 recording_inventory parse regex (`services/audio_poc/recording_inventory.py:26-28`).
  * `OBS_SOURCE_REFERENCE = "obs://google-transcripts/{channel}/{date}/{key}"` — canonical reference shape per CP-A3 transcript_inventory parse regex (`services/audio_poc/transcript_inventory.py:20-22`).
  * `NAS_REGION = "estate.audio_plane"`  ·  `OBS_REGION = "estate.audio_plane"` — audio plane region tag (Audio-Plane-v1 §1.2 no-parallel-machinery: NAS + OBS live inside one region).
  * `NAS_DEFENSIBILITY_MEASURE = "sealed_cp_a2_recording_inventory@audio_poc_v1.seal"` — first-run defensibility per E.1 (Canon-4 §8 field · pointer to the sealed CP-A2 contract that would produce a snapshot when live scan wires in).
  * `OBS_DEFENSIBILITY_MEASURE = "sealed_cp_a3_transcript_inventory@audio_poc_v1.seal"` — first-run defensibility per E.1.
  * `NEXT_RECHECK_HINT_M8 = "M8·W-CENSUS-RUNTIME-ORCHESTRATION"` — the follow-on wave that lands the live SMB/OBS enumeration tools (per DECISIONS 2026-09-15T~04:12Z §Δ5).

* **Function:** `mount_audio_inventory_into_census(*, store: RegistryStore, run_id: str, freshness_stamp: str) -> tuple[str, str]` returning `(nas_record_id, obs_record_id)`. Composes:
  * `classify_sensitivity(feed_identity=..., feed_declaration_registry={})` (CP-C1 · always returns the Canon-4 §5.1 fallback in an empty registry).
  * `register_source_candidate(store=..., candidate=..., run_id=..., freshness_stamp=..., defensibility_measure=..., next_recheck_hint=..., supersedes_record_id=None)` (CP-C4).
  * Two calls, one per connector.

* **Idempotency:** since CP-C4 `_compute_record_id` is deterministic over the full input tuple, calling `mount_audio_inventory_into_census` twice with identical `run_id + freshness_stamp` produces the same 2 record_ids and `store.count()` stays at 2 (Canon-4 §8 "one record per source" + E.5 append-only).

* **Determinism failure surface:** covered by CP-C4 `RegistryDeterminismFailure` — mounting with a different `defensibility_measure` under the same `feed_identity + run_id + freshness_stamp` would raise (unreachable in this supplement because the module constants are literals).

## §C · Invariants (target ratchet 4056 → 4062, +6)

1. **module_fabric_present** — imports; exports: `mount_audio_inventory_into_census`, `NAS_FEED_IDENTITY`, `OBS_FEED_IDENTITY`, `NAS_DEFENSIBILITY_MEASURE`, `OBS_DEFENSIBILITY_MEASURE`, `NEXT_RECHECK_HINT_M8`.
2. **feed_identity_constants_are_canonical_tokens** — byte-identical string values as banked in §B; asserts the concrete tokens so a silent rename would fire.
3. **defensibility_measure_references_sealed_cp_a2_a3_contracts** — `NAS_DEFENSIBILITY_MEASURE` contains `cp_a2` + `recording_inventory` + `audio_poc_v1.seal`; `OBS_DEFENSIBILITY_MEASURE` contains `cp_a3` + `transcript_inventory` + `audio_poc_v1.seal`.
4. **mount_writes_two_records_under_same_run_id** — returned `(nas_id, obs_id)` both start with `"rec_"`; both are keys in `store`; both `SourceRecord.census_run_id` equal the passed `run_id`; `store.count() == 2`.
5. **mount_uses_canon_4_5_1_conservative_sensitivity_fallback** — both records carry `Sensitivity(class_label="unknown", is_undeclared=True, rule_reference="Canon-4 §5.1 conservative fallback")`.
6. **mount_is_idempotent_on_identical_inputs** — calling `mount_audio_inventory_into_census` a second time with the same args returns the same `(nas_id, obs_id)` and `store.count()` remains 2.

## §D · Cross-benefit expectation

None expected. The module lives under `services/census_canon/` (not `contracts/`); `test_frozen_contract_snapshot_parity.py` scope is unchanged. If a cross-benefit surfaces during GREEN it will be banked in the seal.

## §E · Wave-honest limits

* **E.1 · First-run shape.** `defensibility_measure` is a string pointer to the sealed CP-A2/A3 contracts. Full defensibility engine (matrix lookup with runtime data) is a later wave.
* **E.2 · No live scan.** This wave writes *placeholder* SourceRecords marking the two audio-plane connectors as *registered-but-unenumerated*. The next_recheck_hint field points to M8 W-CENSUS-RUNTIME-ORCHESTRATION where live SMB/OBS enumeration wires in. Post-M8, correction records with `supersedes_record_id` set will land per E.5 discipline.
* **E.3 · No new contracts.** The supplement composes existing frozen contracts (CP-C1 `SourceCandidate` + `Sensitivity`, CP-C4 `SourceRecord`). No `contracts/` module changes; `NON_CONTRACT_UTILITY_MODULES` exemption unchanged.
* **E.4 · Data-only.** The kernel is a pure composer — no execute/run/dispatch/start/stop/step/iterate/process/commission/trigger method exposed (CP-C5 DATA-ONLY carryover).
* **E.5 · Item-3 run_id supplied at call time.** Callers pass a CP-C3 `generate_census_run_id(...)` value; the supplement does not itself compute or persist the Item-3 run_id (that is a separate follow-on task once M5 CENSUS-RUN registry-writer walk lands).

## §F · Commit protocol

* **Commit A (code, `programme/track-a` in `repos/Extraction-Akki`):** the new test file + the new services module + the ratchet bump in `backend/tests/invariants/baseline_failures.json`. Message per SO §3 two-commit pattern.
* **Commit B (state, `master` in `/app/assessment_workspace`):** grounding brief + seal file + NEXT.md sequencing-pin refresh + DECISIONS.md entry. Message: `state: W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT · CP-CSAIM1 SEALED · <ratchet delta> · ...`.

## §G · Boundary hygiene retries

Per owner directive (b) — retry CD+Visitors probe at every CP boundary. This wave has one CP boundary (CP-CSAIM1 seal). One probe fires there; PASS-verdicts fold into the Item-3 registry-writer follow-on; FAIL-verdicts continue the standing retry loop.

## §H · Reporting

No mid-wave owner-facing report (CP-level updates stay inside sprint plan per SO §2). The wave-close outcome + Item-3 registry state fold into the W-RELEASE-GATE-PILOT-LIFT END-OF-WAVE report per owner cadence "*at RG wave seal + census completion*".

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
