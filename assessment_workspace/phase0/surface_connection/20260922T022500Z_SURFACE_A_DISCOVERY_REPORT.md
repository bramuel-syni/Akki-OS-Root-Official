# CENSUS-SURFACE-A · Discovery Report

- **Surfaced at**: 2026-09-22T02:25:00Z
- **Wave**: CENSUS-SURFACE-A
- **Trigger**: Owner course-correction 2026-09-22T~02:20Z verbatim: *"you
  should [not] be adding new surface - you should be connecting the
  existing one to it, my assumption is there is an existing surface for
  this."*
- **Standing Order**: SO §6.8 (no GO required), §3.8 additive-only,
  §3 tests-first, §6.4 NOTHING-BEYOND scope frozen, §6.7 seal-report boundary.
- **Wave hold state**: R-91 horizon 2026-09-23T03:23:15Z UNCHANGED
  (~25h out). Owner explicit authorisation verbatim (2026-09-21T~11:45Z):
  *"This work is authorized NOW during the R-91 hold (the hold bars the
  ε-apply, not owner-ordered work). R-91 still applies only at the horizon."*
- **testing_agent**: STRICTLY BANNED per SO §6. Manual pytest + curl only.

## 1. Answer to owner Message 279 — what is currently on Akki surfaces

**Truthful verdict**: NOTHING from CENSUS-3 is currently on any Akki user
surface. Zero endpoints, zero UI. All CENSUS-3 findings live as receipts
under `phase0/census_v3/*.json` and `phase0/gpu_probes/*.json` only.

## 2. Existing surfaces inventoried per owner course-correction point 1

Canon 9 §13 authority table (line 23 verbatim from
`canon/text/Akki_Canon_9_Mkondo_Charter.txt`):

> Census and registry records | **Mtafiti** | Both authorities; every
> surface by proof link | Objective-blind measurement; the Watch reads
> sensitivity classes for tripwire coverage and never writes.

### 2.1 Existing canon-blessed writers (single-writer per Canon-9 §3)

| Location | Signature | Canon anchor |
|---|---|---|
| `services/mtafiti/asset_registry_writer.py::write_asset_record` | `(record: AssetRegistryRecord) -> WriteReceipt` | Canon-9 §3 single-writer; Canon-3 §9.3 append-only; Doc-0 G-3 Mtafiti extended asset-class registry |
| `services/census_canon/registry_write.py::register_source_candidate` | `(*, store, candidate, run_id, freshness_stamp, defensibility_measure, next_recheck_hint=None, supersedes_record_id=None, media_types=(), audio_bearing_share=None) -> record_id` | Canon-4 §8 one-record-per-source; Canon-4 §4.1 §4-carrier measurement (media_types + audio_bearing_share); Master Doc-10 A5.5 "The Registry is one record, read by many" |

### 2.2 Existing canon-blessed reader surface (Python-only, NO HTTP wrapper today)

`services/mtafiti/asset_inventory.py`:

- `list_all_assets() -> List[Dict]` — reader-only projection over `_REGISTRY`.
- `count_by_class() -> Dict[str, int]` — Doc-0 BR-4.1 coverage across five kinds.
- `enumerate_classes_always_five() -> Tuple[str, ...]` — Doc-0 TA-3.1 always-five.
- `cross_class_governance_query(*, custody_class, asset_class, owner_class)` — filter.
- `single_writer_still_holds() -> bool` — Canon-9 §3 negative-scan self-check.

### 2.3 Existing HTTP census surfaces

| Route | File | Auth | Reads |
|---|---|---|---|
| `GET /api/census/latest` | `services/census_engine/router.py:134` | none | `phase0/census/census_N/manifest.json` (newest N) |
| `GET /api/census/records` | `services/census_engine/router.py:157` | none | same directory, list summaries |
| `POST /api/census/run` | `services/census_engine/router.py:180` | none | triggers live RDS-Data walker |
| `GET /api/census/dimensions/{feed_id}` | `routers/census_dimensions.py:29` | none | Mongo |
| `GET /api/census/dimensions/registry/{kind}` | `routers/census_dimensions.py:43` | none | in-mem vocab |
| `POST /api/mtafiti/feasibility` | `routers/mtafiti.py:21` | none | feasibility (not asset inventory) |

### 2.4 Existing portal read family (JWT-gated · owner-directed pattern)

| Route family | File | Auth | Purpose |
|---|---|---|---|
| `/api/portal/entitlement/*` (4 endpoints) | `routers/portal_entitlement.py` | `require_identity_or_deny` + `principal_context` | ENT-22 derive_allowance_remaining, ENT-3+ENT-43 dial-admit, ENT-9 catalog |
| `/api/portal/requests/*` (5 endpoints) | `routers/portal_requests.py` | same | DAP-14/18/21/24 request lifecycle |
| `/api/canon/rules/*` (5 endpoints) | `routers/canon_rules_registry.py` | none (canon anchors) | DAP-1..38 · RBM-1..23 · ROC-1..11 · RBM-8 R-91 ceremony |

## 3. The gap

CENSUS-3 receipts live in `phase0/census_v3/*.json` — a **sibling** of
`phase0/census/`, which is what `services.census_engine.router:_records_dir`
reads. The receipt shape is also different (chapter-shaped, not
manifest-shaped). And `mtafiti.asset_inventory` has no HTTP wrapper.
Result: **NO existing endpoint returns CENSUS-3 findings today.**

## 4. Canon-conformant additive connection (this wave)

Per owner course-correction point 2 verbatim: *"CONNECT, don't duplicate:
write the census results INTO the existing registry through its own
sealed writer contract ... and expose them through the EXISTING read
surface family — extending existing routes additively (e.g., a
census/asset-inventory view on the portal read surface) rather than
inventing a standalone /api/census/* family."*

### 4.1 Write path — into the sealed registry via sealed writers

Boot-time hydrator at `services/mtafiti/census3_registry_hydrator.py`
reads `phase0/census_v3/*.json` and, per censused surface, calls:

- `mtafiti.asset_registry_writer.write_asset_record(AssetRegistryRecord(...))`
  with `asset_class=SOURCE`, `custody_class=SENSITIVE`,
  `freshness_stamp=FreshnessStamp(logged_date=..., structural_signature=...)`,
  `named_owner=NamedOwner(owner_id='rms', owner_class='external_party',
  mandate_source='Canon-9 §13 · Mtafiti authority')`.

- `census_canon.registry_write.register_source_candidate(store=<module-scoped
  singleton RegistryStore>, candidate=SourceCandidate(...), run_id='CENSUS-3',
  freshness_stamp=<ISO>, defensibility_measure='CENSUS-3-A/B chapter-receipt
  proof-linked', media_types=(...), audio_bearing_share=<float or None>)`.

Both writes are deterministic-idempotent (same content → same receipt_id
→ no-op). Canon-9 §3 single-writer preserved by construction: the
hydrator module defines NO write/append/update/delete/add/put/set verb
on its public surface (structural negative-scan test
`test_hydrator_defines_no_writer_verb_on_public_surface`).

### 4.2 Read path — additive extension of portal read family

New router `routers/portal_census.py` mounts at `/api/portal/census`
(matches R-100 pattern verbatim: `require_identity_or_deny` +
`principal_context(identity.user_id)`).

Endpoints:

- `GET /api/portal/census/assets` — proxies `mtafiti.asset_inventory.
  count_by_class() / list_all_assets() / enumerate_classes_always_five()`.
- `GET /api/portal/census/surfaces` — per-surface breakdown with
  `freshness_stamp_min` / `freshness_stamp_max` (owner point e verbatim).
- `GET /api/portal/census/access` — readable vs blocked buckets +
  `unlocks` mapping stating exactly what owner action opens each blocked
  slice (owner point e verbatim: `na7p4_series`, `cold_tier_restore`,
  `hf_token`).
- `GET /api/portal/census/latest` — current chapter refs + provenance
  pointers (proof-link per Canon-9 §13).
- `GET /api/portal/census/duplication` — Tier-1/Tier-2 duplication
  chapter with rejected hypotheses + confirmed real mirrors.

### 4.3 Also serve CENSUS-3 through pre-existing `/api/census/latest`

Additive receipt-only bank: `phase0/census/census_0003/manifest.json` in
the shape `census_engine.router:_load_manifest` expects, with additive
`census_v3_extensions` field carrying surface_breakdown +
provenance_pointers + access_summary + duplication_summary. Zero code
touch on `services.census_engine.router`.

## 5. What a user actually hits (post-seal)

**Unauthenticated (rollup only)**:

- `curl $BASE/api/census/latest` → returns `census_0003/manifest.json`
  (CENSUS-3 rollup + census_v3_extensions).
- `curl $BASE/api/census/records` → list including census_0003.

**JWT-gated (full detail)**:

- `curl -H "Authorization: Bearer $TOK" $BASE/api/portal/census/assets`
  → Mtafiti asset-inventory count_by_class + list.
- `curl -H "Authorization: Bearer $TOK" $BASE/api/portal/census/surfaces`
  → per-surface freshness min-max + breakdown.
- `curl -H "Authorization: Bearer $TOK" $BASE/api/portal/census/access`
  → readable/blocked/unlocks.
- `curl -H "Authorization: Bearer $TOK" $BASE/api/portal/census/latest`
  → provenance pointers.
- `curl -H "Authorization: Bearer $TOK" $BASE/api/portal/census/duplication`
  → duplication chapter.

Token via existing flow (unchanged): `POST /api/auth/login` with a demo
account from `/app/memory/test_credentials.md`.

## 6. What is NOT in this wave (SO §6.4 NOTHING-BEYOND)

- **No App.js edits.** R-91 horizon 2026-09-23T03:23:15Z UNCHANGED.
  Dashboard UI spec banked at
  `phase0/surface_connection/portal_census_ui_spec.md` for post-ε-apply
  implementation.
- **No sealed edit.** Zero touches to any file in `services/mtafiti/*`,
  `services/census_canon/*`, `services/census_engine/*`, `contracts/*`,
  `routers/portal_entitlement.py`, `routers/portal_requests.py`,
  `services/auth/*`, `services/enforce/principal_context_adapter.py`.
- **No new `/api/census/*` family.** Existing `/api/census/*` continues
  unchanged; new endpoints sit on `/api/portal/census/*` per owner
  course-correction.
- **No CENSUS-3-C/D/E/F content-axis measurements** — those are their
  own lanes and land as census_0004..census_00XX later. Owner lane order
  F→C→D→E per this-session confirmation point c.
- **No sensitivity re-classification.** All hydrated records land with
  `Sensitivity(class_label='unknown', is_undeclared=True,
  rule_reference='Canon-4 §5.1 conservative fallback · census_v3 receipts
  not sensitivity-classified this wave')`. Full classification is a
  later wave (source_candidate_classifier.py exists but is not run here).

## 7. RED-first drill receipts

- `phase0/drill_receipts/20260922T02XXXXZ_surface_a_RED_pre.log`
  (5 tests fail right-reason ImportError on `routers.portal_census` +
  `services.mtafiti.census3_registry_hydrator`).
- `phase0/drill_receipts/20260922T02XXXXZ_surface_a_GREEN_post.log`
  (all new tests pass).
- Double-green sweep pending: `BASELINE_GUARD=1 PYTHONHASHSEED=0`
  stripped-sha256 pinned in this file after Commit-A.

## 8. Interleaved lanes (this session, per owner confirmation point c)

- CENSUS-SURFACE-A (this wave) — landing NOW on CPU, no GPU cost.
- CENSUS-3-F (OBS audio GPU pipeline on 15 readable OBS audio buckets)
  — kicked off in background AFTER this wave's Commit-A seals · uses
  the remote dual-host H200 pipeline · no local disk footprint (stream +
  hash-and-discard).
- CENSUS-3-C/D/E — sequenced after F per owner order.
- Order B / S4a-DIGICOW-RDS ingest adapter — CPU lane, continues
  interleaved.
