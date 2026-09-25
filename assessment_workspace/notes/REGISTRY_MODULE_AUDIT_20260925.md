# Registry Module Audit · 2026-09-25T09:12Z

Owner ask verbatim: "Audit the registry module, i feel like you are jumpy and not going
deep into whats actually built. review then get back to me."

Method: read-only. Every claim below cites a file:line or a live endpoint response
captured from this pod at the timestamp above. Nothing was modified.

---

## 0. Headline findings (the five things that matter)

1. **There is no single "registry". There are FOUR disjoint registries** with different
   stores, different writers, and different readers. Only one of them is what the live
   frontend renders, and it is not the one the CENSUS-3 hydrator writes into.
2. **Both canon-blessed writers are in-memory dicts.** `asset_registry_writer._REGISTRY`
   and `census_canon.registry_write.RegistryStore` live in process RAM and are rebuilt on
   every backend restart by re-reading `phase0/` JSON. Nothing the hydrator "writes" is
   persisted. Mongo `mtafiti_registry_records` has **0 documents**.
3. **The Census Autonomy engine has no executor.** `engine.run_bounded_census` passes two
   gates and then writes a receipt whose payload is the literal note *"Commit-A shape gate
   landed; data_source adapter fold-in … in Phase 3 continuation"*. The `census_scheduler`
   (PID 275) is running and consuming jobs, but no job has ever read a byte. All 12 result
   receipts on disk carry that same note.
4. **The Registry landing read model mixes measured figures with hard-coded literals**
   while its header copy says *"Every figure here was measured, not estimated."*
   Enumerated in §4.3.
5. **Census #4 (RMS MySQL · 8 clusters · 41 DBs · 2,642 tables · ~428.8M rows) is on disk
   but invisible to the registry surfaces** — the hydrator hard-codes censuses 1/2/3 and a
   frozen 6-surface descriptor tuple. Its manifest also uses a compact timestamp format
   that breaks the legacy frontend date slice and would crash the hydrator's duration parser.

---

## 1. The four registries

| # | Store | Writer | Reader(s) | Live consumer | Rows now |
|---|-------|--------|-----------|---------------|----------|
| R1 | Mongo `mtafiti_registry_records` (`contracts/mtafiti_registry.py:26`) | `services/mtafiti/registry.py:122 upsert()` ← only caller `services/service_1/service.py:181-182` | `registry.read_all / read_by_source_ref` ← `routers/registry.py:129 what_you_hold` | none (frontend never calls `/api/registry/what_you_hold`) | **0** |
| R2 | in-memory `asset_registry_writer._REGISTRY` (`asset_registry_writer.py:57`) | `write_asset_record` (`:67`) ← callers: `census3_registry_hydrator.py:334`, `data_source_adapter.route_asset_registry_write` (`:334`, never invoked by engine) | `asset_inventory.list_all_assets / count_by_class` ← `routers/portal_census.py:114-116 GET /assets` | none | 6 after first request; 0 after restart until re-hydrated |
| R3 | in-memory `RegistryStore` singleton (`census3_registry_hydrator.py:134`) | `census_canon.registry_write.register_source_candidate` (`registry_write.py:217`) ← `hydrator:344`, `estate_enumerator.py:171`, `audio_inventory_supplement.py:166/175` | `_canon_registry_store()` — underscore-private, **no router reads it** | none | 6 (RAM only) |
| R4 | disk: `phase0/data_connection_records/*_FINAL.json` + `phase0/commissioning_records/*_ACCEPTED.json` | out-of-band scripts (connect wizard) | `services/registry_facts/facts.py:296 assemble_facts` → `GET /api/registry/facts` (unauthenticated, `router.py:15`) | **This is what the frontend consumed** (`App.js:1152`, `components/Registry.jsx:59`) — but that shell (`PortalIframe → v8_prototype.html`) is retired from routing (`App.js:1349-1355`) | 2 sources · 1 compute · 1 LLM |

Disjointness proof: R1 keys on `source_ref`, R2 on `asset_ref`, R3 on a sha256 `record_id`,
R4 on filename glob. No module joins them. `what_you_hold._read_holdings_axis`
(`routers/registry.py:127-131`) tries to join Connect `sources_store` → R1 and gets zero rows
because `sources_store` is empty and R1 is empty (live response: `holdings.rows=0,
connected.total=0`).

---

## 2. What each writer actually guarantees vs. what its docstring claims

### 2.1 `asset_registry_writer.write_asset_record` (R2)
- Docstring (`:1-17`): "Canon-3 §9.3 append-only … no update or delete path".
- Code (`:73`): `_REGISTRY[record.asset_ref] = record` — **an overwrite keyed by asset_ref**.
  A second write with the same `asset_ref` and different content silently replaces the
  first. Not append-only.
- `:53-57` own comment: *"NOT a persistence layer … downstream persistence is a later
  wave's concern."* That later wave has not landed.
- `WriteReceipt.au_3b_defensible` is hard `False` (`:77`) — every receipt carries a
  non-defensible timestamp by design (R-C2 marker, Doc-0 G-8 open).

### 2.2 `census_canon.registry_write.register_source_candidate` (R3)
- Genuinely append-only and deterministic (`registry_write.py:135-153`): same tuple → same
  `record_id` → no-op; different content under same id → `RegistryDeterminismFailure`.
  This is the best-built writer in the module.
- But the hydrator calls it with `freshness_stamp=desc["freshness_stamp_max"] or now()`
  (`hydrator:348`). For `nas_dsm` (`freshness_stamp_max=None`, `:225`) this means a **new
  record_id on every process start** — the store grows one orphan per restart for that
  surface. Harmless in RAM, but it is a determinism leak the writer was designed to prevent.
- Sensitivity is hard-coded `unknown / is_undeclared=True` for all six surfaces
  (`hydrator:304-312`). The classifier (`census_canon/source_candidate_classifier.py`) exists
  but is never invoked on this path.

### 2.3 `mtafiti.registry.upsert` (R1)
- Real Mongo persistence, keyed on `source_ref`, `$set` upsert (`registry.py:122-128`).
- Only writer is Service-1's dispatch (`service_1/service.py:181`), which composes a record
  from a `NormalizedUnit` fixture — i.e. this registry is fed by the **objective/extraction
  pipeline**, not by any census. It has never been written in this pod (0 docs).
- `detect_stale_records` (`:142`) implements the §17 #8 freshness invariant correctly
  (returns only stale refs), but no caller exists outside tests.

---

## 3. The hydrator (`census3_registry_hydrator.py`, 1,644 lines)

### 3.1 What it is
An **adapter that re-derives six registry rows from a compile-time tuple**
(`_SURFACE_DESCRIPTORS`, `:174-241`) on first HTTP hit (`portal_census.py:83-93
_ensure_hydrated`). It then serves ~1,300 lines of projection functions that shape
`phase0/census_v3/*.json` receipts into the owner-design read model.

### 3.2 What it reads from disk (real)
- `20260922T014400Z_CENSUS3_OBS_chapter.json` (`:148`) — bucket counts, 161.76 TB rollup.
- `duplication_v2/…CHAPTER_V2.json` (`:155`) — Tier-1/Tier-2 method, 87,684 clusters.
- `duplication_v2/…DIGICOW_LANGID_AGGREGATE.json` (`:162`) — LID language codes.
- `phase0/census/census_000{1,2,3}/manifest.json` (`:550`) — for list/detail rows.
- `phase0/gpu_probes/…LANGID_FULL_SWEEP_LAUNCH.json` (`:822`) — model name only.

### 3.3 What it does NOT read
- `phase0/census/census_0004/manifest.json` — exists (CENSUS-3-C, 2026-09-25T01:59Z),
  never loaded. `census_detail` map is `{1,2,3}` (`:946`); `census_list` is three literal
  calls (`:650-654`).
- `phase0/census_v3/nas/20260925T021101Z_CENSUS3E_NAS_content.json` — exists, never
  loaded; `nas_dsm` still shows `content_axis_pending_lane: CENSUS-3-E` (`:406`).
- `phase0/connectivity_receipts/*` — the JUMP/MySQL descriptor rows (`:209-229`) point at a
  receipt but never open it.

### 3.4 Surface descriptors are frozen constants, not derived
Every `freshness_stamp_min/max`, `audio_bearing_share` (0.18 / 0.927 / 1.0),
`media_types` tuple, `region` and `owner_id` (`:174-241`, `:324`) is typed in by hand.
`surface_breakdown_with_freshness` (`:374`) overlays a few live values from the OBS chapter
but the identity rows themselves cannot change without a code edit. A new census surface
(e.g. the 8 RMS MySQL clusters) therefore cannot appear in `/assets`, `/surfaces` or the
`sources_connected` stat card without editing this file.

---

## 4. Endpoint-by-endpoint: measured vs. literal

### 4.1 `GET /api/portal/census/records` + `/records/{n}` (`hydrator:646`, `:942`)
Live: `#1 COMPLETE 0m56s 2/2 · #2 COMPLETE 1m26s 2/2 · #3 NEEDS_ATTENTION 28m12s 32/106`.
Derived from manifests (real). `sources_read/sources_total` for #1/#2 reuse `database_count`
for both numerator and denominator (`:585-586`) — always 100 %, not a coverage measure.

Detail-tab literals:
- `_condition_of_read_census_2` (`:697`): `92 / 3 / 1 / 4 / 0` and `total_bytes_held =
  5,908,255 × 500` — a nominal bytes-per-row constant, labelled as such in the note (good),
  but the percentages have no receipt behind them.
- `_condition_of_read_census_3` (`:718`): `15.5 / 2.0 / 0.5 / 2.0 / 80.0` — literals; note
  says "current-seal estimates".
- `_gpu_spend_census_3` (`:819`): `gpu_hours=1.2`, `utilization_pct=62.0` — literals; only
  `objects_processed` and `model` are read from receipts.
- `_conversation_census_{1,2,3}` (`:842-887`): hand-typed dialogue transcripts with
  timestamps, presented as "Owner ceremony directives verbatim as banked in
  STATE/DECISIONS.md". Not read from DECISIONS.md.

### 4.2 `GET /api/portal/census/assets` (`portal_census.py:101`)
Live: 6 rows, all `asset_class=source`, all `custody_class=sensitive`, all owner_class
`external_party`. The five-class taxonomy always enumerates (`asset_inventory.py:67`) —
correct per TA-3.1 — but four of five classes are 0 and there is no writer path for
model/artifact/receipt/rule assets anywhere in the codebase.

### 4.3 `GET /api/portal/census/registry-landing` (`hydrator:1610`)
Header copy (`:1044`): *"Every figure here was measured, not estimated."*
Body:
| Field | Source | Status |
|---|---|---|
| `held_in_total 161.76 TB` | OBS chapter `estate_rollup` | **measured** |
| `sources_connected 6` | `len(_SURFACE_DESCRIPTORS)` | literal tuple length |
| `data_types_present 5` | union of hand-typed `media_types` | literal |
| `languages_observed 15` | LID aggregate keys | **measured** (Digicow S3 audio only) |
| `condition_of_the_estate 3.0/12.7/3.0/81.3 %` (`:1144-1151`) | literals | **hard-coded** |
| `how_far_we_have_got_with_it` TB | 161.76 × the literals above | derived-from-literal |
| `in_which_language` | LID counts × `audio_pool_tb = 0.01525` (`:1194`) | count measured · TB weight literal |
| `what_it_is_made_of` video/image/app/text | `balance × 0.85/0.06/0.06` (`:1320-1322`) | **priors**, labelled "DIRECTIONAL" in code, rendered as `size_tb` |
| `how_far_it_has_been_read.body` (`:1439-1445`) | `32 / 106`, "50 clusters (36 + 10)" | literals |
| `right_rail.census_run_status.next_census_utc 2026-09-29T05:52:00Z`, `days_until_next 7` (`:1522-1523`) | literals | **not read from the scheduler** |
| `census_did_not_touch.read_but_not_verified 30`, `read_with_problems_found 2` (`:1541-1542`) | literals | hard-coded |
| `honest_accounting_law.verified_volume_tb 4.85` | 161.76 × 3.0 % literal | derived-from-literal |
| `what_needs_care.risk_buckets` (`:1456-1461`) | four hand-typed rows | literal |

So: two stat cards are measured, the THE-MIX body is predominantly literal. The honest-
accounting law is carried as a field (as directed) but its `verified_volume_tb` is computed
from a hard-coded 3.0 %.

### 4.4 `GET /api/registry/what_you_hold` (`routers/registry.py:50`)
Live: every axis is zero (`connected.total=0`, `holdings.rows=0`,
`declaration_baseline_count=0`, `planes_active=0`, `registries_effective=0`). Collections
`mtafiti_declarations`, `mtafiti_inference_overlays`, `memory_planes`, `D_registries` do
not exist in `test_database` (only `users` exists). Additionally
`rings[hash(src["source_id"]) % 5]` (`:137`) is commented "stable ring assignment" but
Python's `str.hash` is salted per process — ring assignment would change on every restart.

### 4.5 `GET /api/registry/facts` (R4, unauthenticated)
Live: 2 Digicow Aurora sources (125 + 110 tables, `last_verified 2026-08-19`), 1 compute
host (`akki-vm`, 2× H200), 1 LLM (Emergent Universal). This is the only registry surface
that reads durable records, and it is 37 days stale on its data side, knows nothing of the
RMS estate, and its consuming shell is retired from routing.

### 4.6 `GET /api/census/latest` (legacy `census_engine/router.py:134`)
Live: returns census **#4** (`wave_id CENSUS-3-C`, 8 clusters / 41 DBs / 2,642 tables /
428,786,937 rows est). This is the one surface where the RMS estate is visible — and its
`finished_at_utc` is `20260925T015942Z` (compact). Censuses 1-3 use `2026-09-22T01:36:48Z`
(ISO). `App.js:1184` does `.slice(0,10)` → would render `20260925T0`; `hydrator:557
_duration_iso_to_seconds` uses `%Y-%m-%dT%H:%M:%S` → `ValueError` if #4 is ever added.
Manifest also records `connection_path: "direct pymysql"` from this pod — the data-path
violation is banked into the record itself.

---

## 5. What the live frontend actually shows for "Registry"

- `/os/admin/estate` (`pages/os/AdminEstate.jsx:60-70`): explicit honest-gap card —
  *"Backend for Registry not yet wired."* No API call.
- `/dap` landing (`DAPLanding.jsx:11-21`) and `/dap/estates/:id` (`DataEstates.jsx:5-62`):
  render **hard-coded Digicow prose and figures** (41.2 TB audio, 287,800 calls, 61,400
  hours, 9,140 complaint files, 2.1M pages, 1.4M email threads, "62 % checked", …). No API
  call. None of these numbers exist in any receipt under `phase0/`. Not labelled as sample.
- `/dap/resources/compute` (`AvailableResources.jsx`): real, from `/api/compute/estate`
  (2 hosts · 4 GPUs · 559 GB).
- `components/Registry.jsx` (1,061 lines, three tabs matching the owner design) is
  **not imported by any route** — orphaned.
- **No frontend file calls** `/api/portal/census/{assets,surfaces,access,latest,
  duplication,records,registry-landing}` or `/api/registry/what_you_hold`. The entire
  Commit-A'/A'' read model has zero consumers. Only `CensusAutonomyDrawer`
  (`POST /run`, `GET /runs/{id}/state`) and `ResponseRequiredBadge` reach `/api/portal/census/*`.

---

## 6. Census Autonomy — what the running scheduler does

- `scheduler_program.main` (`:117-145`): polls `pending/*.json` every 60 s, calls
  `run_bounded_census`.
- `engine.run_bounded_census` (`:149-224`): gate 1 `lawful_basis_admit_ref` present; gate 2
  wall-clock; then **writes a result receipt containing the descriptor echo and the literal
  Phase-3-continuation note, removes the pending file, returns COMPLETE**. No driver, no
  adapter, no registry write. Tenant-scope gate is a comment (`:185-188`).
- `data_source_adapter` (`:1-96` header): shipped with three driver *codes*, a mode env
  (`CENSUS_DATA_SOURCE_MODE`, unset → `stub`), an unblock-marker grammar, and a producer
  into the response-required queue — and states in its own header (`:87-95`) that live
  driver rows and engine integration are *"deferred to future slices"*. The adapter is
  never imported by the engine.
- Disk evidence: 12 result receipts (2026-09-22 → 2026-09-25), all with the same note; 1
  refusal row (`DEFERRED_BUDGET_EXCEEDED`); 0 pending; 0 response-required items.
- Therefore "Akki is running the census" is currently true only in the sense that a loop is
  alive. Every real walk to date (census_0001-0004, CENSUS-3-A/B/E) was executed by an
  agent-authored script from this pod, then banked to `phase0/`.

---

## 7. GPU door — verified this session (owner said "GPU connections look fine")

From this pod at 09:12Z, both hosts `41.173.184.244` (akki-vm) and `41.173.184.247`
(akki-vm-ii), OpenSSH 9.6p1, user `ubuntu`:
- key `estate_keys/gpu_hosts/id_ed25519_akki_gpu` (SHA256:dtmtQPKdrqRioj5sas2RCucpKpP97F5c0/0tPHTux2o) → `Permission denied (publickey)`
- password from `GPU_Creds_2.csv` → `Permission denied (publickey)`; server advertises
  `Authentications that can continue: publickey` only.
Fact: the door may be fine from the owner's machine, but **this pod's key is not in
`~ubuntu/.ssh/authorized_keys` on either VM**. That remains the single unblock:
append `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFHX3Gprvz1HSej3d0GclxFnsLyATu67A4TO8G9ItcgZ akki-gpu-hosts-seam-key-20260924T193015Z`.

---

## 8. Defects list (ranked)

| # | Defect | Where | Severity |
|---|---|---|---|
| D1 | Autonomy engine has no executor; receipts assert COMPLETE without reading | `engine.py:205-224` | P0 — falsifies "Akki runs it" |
| D2 | Registry landing mixes literals with measured figures under a "measured, not estimated" header | `hydrator:1044` vs `:1144-1151, :1320-1322, :1439-1445, :1522-1523, :1541-1542` | P0 — honest-accounting law breached in the read model that carries it |
| D3 | Frontend `/dap` landing + estates render fictional Digicow figures with no receipt and no sample label | `DAPLanding.jsx:11-21`, `DataEstates.jsx:5-62` | P0 — owner-facing fabrication |
| D4 | Census #4 (RMS · 41 DBs · 2,642 tables) invisible to hydrator + `/assets`; NAS 3-E receipt unread | `hydrator:174-241, :646-654, :946` | P1 |
| D5 | census_0004 manifest timestamp format (compact) diverges from #1-3 (ISO); breaks date slice + duration parser | `census_0004/manifest.json`, `App.js:1184`, `hydrator:557` | P1 |
| D6 | R2 writer overwrites by `asset_ref` while claiming append-only | `asset_registry_writer.py:73` | P1 — canon claim false |
| D7 | R3 `nas_dsm` record gets a fresh `record_id` every process start (`freshness_stamp_max=None` → `now()`) | `hydrator:225, :348` | P2 |
| D8 | `what_you_hold` reads five collections that do not exist; ring assignment uses salted `hash()` | `routers/registry.py:137, :171-189` | P2 — surface is unused anyway |
| D9 | Commit-A'/A'' read model (8 endpoints, ~1,300 lines) has zero frontend consumers; `components/Registry.jsx` orphaned | grep of `frontend/src` | P2 — built, not wired |
| D10 | R4 `/api/registry/facts` is unauthenticated and its data side is 37 days stale | `registry_facts/router.py:15` | P2 |
| D11 | Sensitivity hard-coded `unknown/undeclared` for all surfaces; classifier never invoked | `hydrator:304-312` | P2 |

---

## 9. What is genuinely solid (credit where due)

- `census_canon.registry_write` — deterministic ids, refuse-on-collision, correction chain
  via `supersedes_record_id`, §4.1 carriers participate in identity. Well built.
- `mtafiti.registry.detect_stale_records` — §17 #8 "re-measure only the affected region"
  implemented correctly.
- `asset_inventory` — reader-only discipline with a self-check (`single_writer_still_holds`).
- `portal_census` router — JWT-gated, principal-scoped, zero I/O in handlers, import-safe.
- `response_required_queue` + `data_source_adapter` marker grammar — ready to receive a real
  producer; the `host_reachability` unblock class exists for exactly the GPU-door case.
- `/api/census/latest` — the one surface that already sees census #4 truthfully.

---

## 10. Receipt

- Live captures: `GET /api/portal/census/{assets,records,registry-landing}`,
  `GET /api/registry/{what_you_hold,facts}`, `GET /api/census/latest`,
  `GET /api/compute/estate` at 2026-09-25T09:0xZ, JWT `demo.master_admin`.
- SSH probes: 2 hosts × 2 auth methods, all `Permission denied (publickey)`.
- Mongo: `test_database` → collections `['users']` only.
- Supervisor: `census_scheduler RUNNING pid 275`.
