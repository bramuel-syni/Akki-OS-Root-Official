# Akki Estate Intelligence — RMS MySQL estate

Job `eij-1b359b3cbd2e` · status **partial** · measured 2026-09-29T19:12:15.151993Z · built 2026-09-29T22:55:38.885808Z

Census only: rows were measured on the jump host and discarded; this brief carries aggregates, sketches and hashes — no row, cell or identifier value.

## What the census found

20 databases and 1,006 tables (351.3 GiB, ≈259,273,874 rows) were measured; 1.5% of rows repeat exactly, 23.0% carry damage, 81.7% have empty required-looking fields and 71.8% of sampled rows carry personal-data markers. About 15.2 GiB (4.3%) looks reclaimable.

| Figure | Value |
|---|---|
| Connections / databases / tables | 5 / 20 / 1,006 |
| Rows (estimate) / rows measured | 259,273,874 / 5,881,277 |
| Bytes held (data + index) | 351.3 GiB |
| Exact duplicate rows | 1.5% (normalised 3.6%) |
| Degraded rows (placeholder, mojibake, truncation) | 23.0% |
| Rows with empty fields | 81.7% |
| Sampled rows with PII markers | 71.8% |
| Long-text near-duplicates (MinHash) | 85.3% |
| Bytes in tables not written for > 1 year | 15.4% |
| Reclaimable bytes (estimate) | 15.2 GiB (4.3%) |
| Same-schema duplicate table pairs with content overlap | 71 |
| Tables failed / empty | 44 / 368 |
| Table readiness grades | A: 171, B: 62, C: 191, D: 189, E: 25 |

## Databases — readiness grades and dimensional profile

| Connection / database | Tables | Rows est. | Bytes | Grade | Dimensions (tables carrying) |
|---|---|---|---|---|---|
| iebc_forms / viusasa_staging | 303 | 233,674,580 | 338.5 GiB | D (52.3) | identity 298, time 284, measure 211, engagement 162, entity 115, content 111 |
| iebc_forms / viupay_agent_staging | 31 | 12,055,806 | 1.2 GiB | A (87.2) | identity 31, time 21, channel 21, money 20, measure 19, entity 16 |
| citizen_digital / db_visitors | 47 | 4,597,869 | 2.7 GiB | D (54.0) | identity 45, time 38, measure 21, content 17, entity 16, engagement 14 |
| viupay / viutickets | 57 | 2,131,953 | 421.2 MiB | B (77.4) | identity 54, time 50, measure 31, engagement 30, money 17, content 17 |
| iebc_forms / viutickets | 56 | 1,607,465 | 338.7 MiB | B (77.0) | identity 53, time 49, measure 31, engagement 30, money 17, product 16 |
| Razuna (Library Content) & Newsvault (Radio News content) / razuna | 82 | 1,341,823 | 4.5 GiB | D (53.4) | identity 79, content 40, measure 34, time 34, entity 27, product 15 |
| citizen_digital / local | 17 | 987,599 | 540.3 MiB | D (52.7) | identity 11, time 8, measure 7, engagement 3, entity 3, geo 2 |
| Razuna (Library Content) & Newsvault (Radio News content) / news_vault | 30 | 856,820 | 932.0 MiB | C (56.9) | identity 27, time 21, content 13, entity 7, measure 7, engagement 3 |
| viupay / kra_reports | 27 | 822,072 | 1.5 GiB | D (52.2) | identity 26, time 22, measure 14, entity 11, money 7, content 6 |
| citizen-pulse / saa | 28 | 423,473 | 153.0 MiB | D (52.0) | identity 26, time 20, entity 10, content 9, measure 8, engagement 6 |
| iebc_forms / viusasa_miniapps_prod | 21 | 272,232 | 216.8 MiB | D (51.6) | identity 21, time 17, measure 16, entity 8, content 6, product 6 |
| citizen-pulse / citizen-pulse | 39 | 157,828 | 70.4 MiB | unmeasured (None) |  |
| viupay / viupay | 39 | 138,972 | 105.0 MiB | C (55.7) | identity 36, time 35, entity 27, measure 24, money 11, engagement 10 |
| iebc_forms / iebc_forms | 3 | 135,432 | 53.6 MiB | C (60.8) | identity 3, time 3, content 2, measure 1 |
| iebc_forms / viupay | 38 | 67,080 | 61.3 MiB | D (47.3) | identity 35, time 34, entity 26, measure 23, money 10, engagement 9 |
| iebc_forms / ecommerce_tafaria | 130 | 981 | 6.0 MiB | B (84.4) | identity 128, time 121, measure 84, engagement 57, entity 48, money 39 |
| iebc_forms / viusasa_artists | 8 | 898 | 464.0 KiB | C (62.1) | identity 7, time 7, content 4, entity 3, measure 3, engagement 2 |
| iebc_forms / kra_reports | 19 | 768 | 864.0 KiB | D (54.0) | identity 18, time 17, measure 11, entity 10, money 4, content 4 |
| citizen-pulse / correspondents | 10 | 169 | 304.0 KiB | D (51.0) | identity 7, measure 6, time 6, entity 3, money 1, geo 1 |
| iebc_forms / miniapps | 21 | 54 | 944.0 KiB | D (42.9) | identity 21, time 17, measure 17, entity 8, content 6, product 6 |

## What the data can do — dimensional monetisation candidates

Ranked by rows × readiness × supporting dimensions. Every candidate is an aggregate or de-identified product; rights are declared at Connect, not measured here.

### 1. Reference and master-data licensing — grade C

Clean product / catalogue / form reference tables licensable as master data where rights permit.

- Dimensions required: product; supporting: content, identity
- 87 supporting tables, ≈123,394,159 rows across 11 databases
- Top tables: iebc_forms/viusasa_staging.mpesa_stk_requests (6,558,280 rows, B); iebc_forms/viusasa_staging.model_has_platforms (514,007 rows, A); iebc_forms/viusasa_staging.media (145,302 rows, A); iebc_forms/viusasa_staging.episodes_revenue_share (636,131 rows, B)
- Blockers: 62.0% of supporting tables carry PII markers: de-identify or aggregate before any release · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 2. Content catalogue, recommendation and licensing corpus — grade C

Catalogue metadata, engagement-weighted recommendation features and licensable archive indexes.

- Dimensions required: content; supporting: engagement, time
- 98 supporting tables, ≈157,855,990 rows across 14 databases
- Top tables: iebc_forms/viusasa_staging.mpesa_stk_requests (6,558,280 rows, B); viupay/viutickets.movie_seats (1,158,096 rows, A); iebc_forms/viutickets.movie_seats (834,440 rows, A); iebc_forms/viusasa_staging.continue_watchings (5,053,836 rows, C)
- Blockers: 74.0% of supporting tables carry PII markers: de-identify or aggregate before any release · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 3. Channel / telco engagement analytics (USSD, SMS, app) — grade C

Channel performance, shortcode and campaign attribution, response-rate benchmarks.

- Dimensions required: channel, time; supporting: engagement, entity
- 57 supporting tables, ≈116,781,903 rows across 10 databases
- Top tables: iebc_forms/viusasa_staging.subscriptions (6,163,376 rows, C); iebc_forms/viusasa_staging.continue_watchings (5,053,836 rows, C); iebc_forms/viusasa_staging.model_has_platforms (514,007 rows, A); iebc_forms/viupay_agent_staging.agent_api_logs (522,652 rows, B)
- Blockers: 79.0% of supporting tables carry PII markers: de-identify or aggregate before any release · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 4. Customer / subscriber 360 and segmentation — grade D

Segmentation, lifetime value and retention modelling across products; requires de-identification before any release.

- Dimensions required: engagement, entity; supporting: channel, geo
- 76 supporting tables, ≈158,914,844 rows across 13 databases
- Top tables: iebc_forms/viusasa_staging.episode_views (5,561,526 rows, B); iebc_forms/viusasa_staging.mpesa_stk_requests (6,558,280 rows, B); iebc_forms/viusasa_staging.subscriptions (6,163,376 rows, C); iebc_forms/viusasa_staging.playback_stagings (34,331,240 rows, D)
- Blockers: 80.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 5. Time-series forecasting datasets — grade C

Daily/weekly demand and revenue series for forecasting products and planning benchmarks.

- Dimensions required: money, time; supporting: geo, product
- 82 supporting tables, ≈80,750,307 rows across 9 databases
- Top tables: iebc_forms/viusasa_staging.mpesa_stk_requests (6,558,280 rows, B); iebc_forms/viusasa_staging.content_performance_metrics (68,843 rows, A); iebc_forms/viusasa_staging.subscriptions (6,163,376 rows, C); iebc_forms/viusasa_staging.users (6,113,578 rows, C)
- Blockers: 77.0% of supporting tables carry PII markers: de-identify or aggregate before any release · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 6. Transaction & revenue analytics — grade C

Revenue, fee and settlement analytics; cohort and churn views once the entity dimension is joined.

- Dimensions required: money, time; supporting: entity
- 82 supporting tables, ≈80,750,307 rows across 9 databases
- Top tables: iebc_forms/viusasa_staging.mpesa_stk_requests (6,558,280 rows, B); iebc_forms/viusasa_staging.content_performance_metrics (68,843 rows, A); iebc_forms/viusasa_staging.subscriptions (6,163,376 rows, C); viupay/viupay.mpesa_stk_requests (20,889 rows, A)
- Blockers: 77.0% of supporting tables carry PII markers: de-identify or aggregate before any release · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 7. Geospatial demand and coverage mapping — grade D

County / constituency level demand, penetration and service-coverage maps sold as aggregated indices.

- Dimensions required: geo, time; supporting: engagement, money
- 36 supporting tables, ≈107,686,180 rows across 9 databases
- Top tables: iebc_forms/viusasa_staging.users (6,113,578 rows, C); iebc_forms/viusasa_staging.users_staging (6,049,518 rows, D); iebc_forms/viusasa_staging.playback_stagings (34,331,240 rows, D); iebc_forms/viusasa_staging.playback_qualified_streams (15,794,152 rows, D)
- Blockers: 78.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 8. Civic and audience insight panels — grade D

Aggregated audience and civic-participation indices by geography; strictly aggregate, never row-level.

- Dimensions required: entity, geo; supporting: content, engagement
- 28 supporting tables, ≈107,484,230 rows across 9 databases
- Top tables: iebc_forms/viusasa_staging.playback_stagings (34,331,240 rows, D); iebc_forms/viusasa_staging.playback_qualified_streams (15,794,152 rows, D); iebc_forms/viusasa_staging.users (6,113,578 rows, C); iebc_forms/viusasa_staging.users_staging (6,049,518 rows, D)
- Blockers: 86.0% of supporting tables carry PII markers: de-identify or aggregate before any release · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

## Strategies to reduce cost

No storage tariff on record: savings are stated in bytes. Set ESTATE_STORAGE_COST_PER_GB_MONTH to price them.

| Strategy | Reclaimable | Share | Action |
|---|---|---|---|
| Move tables not written for over a year to cold storage | 54.1 GiB | 15.4% | Export to compressed object storage, keep a schema stub and a pointer; restore on demand. |
| Remove redundant (prefix-covered) indexes | 14.0 GiB | 4.0% | Drop each non-unique index whose columns are a leading prefix of another index on the same table. |
| De-duplicate exact repeated rows inside tables | 1.2 GiB | 0.4% | Add uniqueness constraints or a merge step at ingestion; archive the historical duplicates. |
| Consolidate duplicate and staging copies of the same tables | 54.0 MiB | 0.0% | Retire or snapshot-then-drop the smaller copy of each same-schema pair with measured content overlap; keep one system of record. |
| Drop or archive empty tables | 13.7 MiB | 0.0% | Remove empty tables and their indexes after a 30-day observation window. |
| Repair or purge orphaned references | not a storage saving | — | Reconcile foreign-key candidates whose sampled values are missing in the target table; purge rows that reference nothing. |
| Minimise PII-dense tables that no product needs | not a storage saving | — | Tokenise or drop personal columns in analytics copies; keep raw identifiers only in the system of record. |

### Evidence per strategy

**Move tables not written for over a year to cold storage** — risk: Staleness is read from the latest timestamp column; tables without timestamps are not counted as stale.

- viusasa_staging.audits · 666 days · 18.6 GiB
- viusasa_staging.master_payments · 438 days · 4.2 GiB
- razuna.raz1_videos · 1341 days · 3.0 GiB
- viusasa_staging.payment_requests · 664 days · 2.8 GiB
- viusasa_staging.sms · 583 days · 2.7 GiB
- viusasa_staging.mpesa_stk_requests · 724 days · 1.4 GiB

**Remove redundant (prefix-covered) indexes** — risk: Write amplification falls immediately; verify no query hints name the dropped index.

- ecommerce_tafaria.playbacks · playbacks_playable_type_index covered by playbacks_playable_type_playable_id_index
- viusasa_staging.clip_requests · clip_requests_castr_stream_id_index covered by clip_requests_castr_stream_id_castr_clip_id_index
- viusasa_staging.continue_watchings · continue_watchings_user_id_index covered by continue_watchings_user_history_updated_index
- viusasa_staging.duka_product_search_clicks · duka_product_search_clicks_normalized_term_index covered by duka_product_search_clicks_normalized_term_product_id_unique
- viusasa_staging.duka_search_synonyms · duka_search_synonyms_synonym_index covered by duka_search_synonyms_synonym_canonical_unique
- viusasa_staging.elimu_learner_badges · elimu_learner_badges_badge_id_index covered by elimu_learner_badges_badge_id_sub_user_id_unique

**De-duplicate exact repeated rows inside tables** — risk: Duplicates measured on complete passes or stratified samples; the primary key was excluded from the comparison.

- viusasa_staging.search_lookups · 5.9% repeated · 8.7 GiB
- viusasa_staging.playback_qualified_streams · 5.1% repeated · 4.6 GiB
- viusasa_staging.episode_views · 22.0% repeated · 764.0 MiB
- kra_reports.external_credit_notes · 25.0% repeated · 277.8 MiB
- viusasa_staging.new_episode_views · 66.1% repeated · 98.7 MiB
- viusasa_staging.ussd_hits · 8.5% repeated · 573.0 MiB

**Consolidate duplicate and staging copies of the same tables** — risk: Copies may be deliberate (staging, backups). Confirm ownership before retirement; the sketch overlap is an estimate, not a row-level diff.

- iebc_forms/viupay.failed_jobs ↔ viupay/viupay.failed_jobs · overlap 78.0% · 31.6 MiB
- iebc_forms/viutickets.movies ↔ viupay/viutickets.movies · overlap 84.0% · 6.5 MiB
- iebc_forms/viutickets.ussd_hits ↔ viupay/viutickets.ussd_hits · overlap 100.0% · 6.5 MiB
- iebc_forms/viutickets.payment_processings ↔ viupay/viutickets.payment_processings · overlap 65.0% · 4.5 MiB
- iebc_forms/viupay.payment_requests ↔ viupay/viupay.payment_requests · overlap 50.0% · 3.5 MiB
- iebc_forms/viutickets.movie_shows ↔ viupay/viutickets.movie_shows · overlap 80.0% · 3.5 MiB

**Drop or archive empty tables** — risk: Empty by TABLE_ROWS estimate; a freshly truncated live table looks the same.

- ecommerce_tafaria.airtel_c2bs
- ecommerce_tafaria.airtel_ussd_pushes
- ecommerce_tafaria.album_track
- ecommerce_tafaria.albums
- ecommerce_tafaria.api_providers
- ecommerce_tafaria.article_menu
- ecommerce_tafaria.article_sources
- ecommerce_tafaria.articles
- … 360 more

**Repair or purge orphaned references** — risk: Targets were inferred from column names (x_id → x/xs); a missing target may be a naming convention, not a break.

- ecommerce_tafaria.invoices.order_id → orders · 100.0% orphaned of 4 sampled
- ecommerce_tafaria.invoices.payment_id → payments · 100.0% orphaned of 1 sampled
- viusasa_staging.active_users.user_id → user · 100.0% orphaned of 400 sampled
- viusasa_staging.airtel_ussd_pushes.user_id → user · 100.0% orphaned of 400 sampled
- viusasa_staging.article_menu.article_id → articles · 100.0% orphaned of 400 sampled
- viusasa_staging.audits.user_id → user · 100.0% orphaned of 400 sampled

**Minimise PII-dense tables that no product needs** — risk: Detector is deterministic and sampled; absence of a marker is not absence of personal data.

- viusasa_staging.playback_stagings · 91.0% of sampled rows
- viusasa_staging.telescope_entries · 79.0% of sampled rows
- viusasa_staging.audits · 100.0% of sampled rows
- viusasa_staging.sms · 100.0% of sampled rows
- viusasa_staging.ussd_hits · 100.0% of sampled rows
- viusasa_staging.playback_qualified_streams · 58.0% of sampled rows

## Where it falls short

- Connection `artists_app`: PULL_SEAM_WORKER_FAILED:pymysql.err.OperationalError: (1045, Access denied for user bramuel159.138.173.250 (using passwo
- Degraded: viusasa_staging.telescope_entries · 100.0% of 38,110,619 rows (stratified_keyset_sample)
- Degraded: viusasa_staging.telescope_entries_tags · 100.0% of 10,406,547 rows (head_sample_no_single_primary_key)
- Degraded: viusasa_staging.payments · 97.3% of 6,323,116 rows (stratified_keyset_sample)
- Degraded: db_visitors.event_logs · 60.8% of 2,494,684 rows (stratified_keyset_sample)
- Degraded: viusasa_staging.playback_stagings · 2.4% of 34,331,240 rows (stratified_keyset_sample)
- Degraded: viusasa_staging.payment_requests · 9.8% of 6,852,215 rows (stratified_keyset_sample)
- Degraded: viutickets.media · 100.0% of 471,627 rows (stratified_keyset_sample)
- Degraded: viutickets.media · 100.0% of 392,888 rows (stratified_keyset_sample)
- PII-dense: viusasa_staging.playback_stagings · 90.7% of sampled rows
- PII-dense: viusasa_staging.telescope_entries · 78.6% of sampled rows
- PII-dense: viusasa_staging.audits · 100.0% of sampled rows
- PII-dense: viusasa_staging.sms · 100.0% of sampled rows
- PII-dense: viusasa_staging.ussd_hits · 100.0% of sampled rows
- PII-dense: viusasa_staging.playback_qualified_streams · 58.3% of sampled rows
- PII-dense: viusasa_staging.payment_requests · 100.0% of sampled rows
- PII-dense: viusasa_staging.mpesa_stk_callbacks · 99.4% of sampled rows

## Method and limits

Ratios are measured on complete passes (tables ≤100k rows) or stratified keyset samples (8×5k rows) and disclosed per table; cross-table overlap is a bottom-256 sketch Jaccard estimate over same-schema tables; no row values were retained or returned.

RMS MySQL only (owner order 1-a). OBS object and NAS file duplication follow from the enumeration frontier; languages, rights and semantic (embedding) similarity were not measured. Text near-duplicates use MinHash on the jump host so row text never left the estate.

## Governed dossier (LLM-composed from these aggregates only)

Model gpt-5-mini via the single chokepoint · receipt `rcp-f3b244641843` · 2026-09-29T23:02:40.432175Z

# Estate-handling dossier — executive briefing

Prepared for the estate owner. Source: aggregated census measurements of the estate (supplied dataset).

## Executive summary
- Scope: 20 databases, 1,006 tables (measured tables: 638) across the estate (source: headline: databases = 20; tables = 1006; tables_measured = 638). Measured rows: 5,881,277 (headline.rows_measured = 5,881,277). Total bytes: unmeasured in the supplied summary (bytes_total is unmeasured).
- Quality and risk snapshot: 1.5% exact repeated rows, 3.6% normalised duplicate rate, 23.0% degraded rows, 81.7% of rows carry empty required-looking fields, and 71.8% of sampled rows carry personal-data markers (source: headline: exact_duplicate_pct = 1.5%; normalised_duplicate_pct = 3.6%; degraded_pct = 23.0; null_bearing_pct = 81.7%; pii_pct = 71.8; pii_rows_checked = 1,011,330).
- Storage / reclaimable: ~15.2 GiB labelled reclaimable (15.2 GiB; reclaimable_pct = 4.3%) and stale data accounts for 15.4% of bytes (headline: reclaimable_label = "15.2 GiB"; reclaimable_pct = 4.3; stale_pct_of_bytes = 15.4). Cost-reduction levers with measured savings are provided below.
- Readiness distribution: Grades A:171, B:62, C:191, D:189, E:25 (headline.grades). Many candidate data-products are mid-to-low readiness (typical readiness scores in the mid‑50s to low‑60s).
- Blockers to release: heavy PII presence and declared-but-unverified rights (multiple product blockers state "use rights are declared at Connect, not measured"). Several supporting tables require de‑identification or aggregation before any release (per-product blockers; see product sections).

---

## Condition of the estate
- Surface metrics:
  - Databases: 20 (headline.databases = 20).
  - Tables: 1,006 total; 638 measured; 44 failed tables; 368 empty tables (headline: tables = 1006; tables_measured = 638; failed_tables = 44; empty_tables = 368).
  - Measured rows: 5,881,277 (headline.rows_measured = 5,881,277). Global rows_estimate fields are unmeasured in many places (rows_estimate: some databases show estimates; others are placeholders or unmeasured).
  - Data-size label: “351.3 GiB” appears in the supplied summary as bytes_label; the canonical total bytes figure itself is not provided (bytes_total is unmeasured).
- Data quality:
  - Exact duplicates low (1.5%) but near-text duplicates are extremely common (near_duplicate_text_pct = 85.3%) — duplicate detection must include semantic/text similarity (headline: exact_duplicate_pct = 1.5; near_duplicate_text_pct = 85.3).
  - Degradation: 23.0% of rows are flagged as carrying damage (headline.degraded_pct = 23.0).
  - Null/required fields: 81.7% of sampled rows have empty required‑looking fields (headline.null_bearing_pct = 81.7) — this is a major analytics completeness problem.
  - PII surface: 71.8% of sampled rows carry personal‑data markers (headline.pii_pct = 71.8; pii_rows_checked = 1,011,330). Top PII tables are concentrated in iebc_forms / viusasa_staging (examples: playback_stagings, sms, payment_requests — see “top_pii”).
- Operational status:
  - Many tables are stale (stale_pct_of_bytes = 15.4). Several product blockers call out that “most supporting tables have not been written for over a year” (per-product blockers).
  - Some connections are blocked (artists_app listed in headline.blocked_connections).

Conclusion: The estate holds substantial, productisable information but the bulk is low‑to‑moderate readiness due to pervasive nulls, PII, staleness and semantic near‑duplicates. Targeted remediation will unlock most commercial value.

---

## Duplication and storage economics
Measured storage-saving opportunities (from supplied cost strategies and duplicate-pair sketches):
- Move to cold storage: 54.1 GiB identified as not written for over a year; action recommended: export to compressed object storage and keep schema stubs (cost_strategy[0]: bytes_label = 54.1 GiB; share_of_estate = 0.1541). Note: staleness detection used latest timestamp columns; tables without timestamps may not be counted as stale.
- Remove redundant prefix indexes: estimated saving 14.0 GiB (cost_strategy[1]: bytes_label = 14.0 GiB; share_of_estate = 0.0397).
- De‑duplicate exact repeated rows inside tables: estimated saving 1.2 GiB (cost_strategy[2]: bytes_label = 1.2 GiB; share_of_estate = 0.0035).
- Consolidate duplicate/staging copies: estimated saving 54.0 MiB (cost_strategy[3]: bytes_label = 54.0 MiB).
- Archive / remove empty tables: estimated saving 13.7 MiB (cost_strategy[4]: bytes_label = 13.7 MiB).
- Note on reclaimed bytes: headline lists reclaimable_label = "15.2 GiB" and reclaimable_pct = 4.3% (headline.reclaimable_label; headline.reclaimable_pct).

Duplication hotspots (examples):
- failed_jobs between iebc_forms and viupay: content overlap ≈ 78% (top_duplicate_pairs[0]: content_overlap_estimate = 0.7812).
- movies tables and others show overlap estimates 80–84% (see top_duplicate_pairs entries). These are candidates for consolidation after ownership confirmation.

Risks to savings:
- Some duplicates are deliberate (staging/backups). Over‑aggressive deletion risks data loss — confirm ownership/intent before retirement.
- Index removal reduces storage but might change query performance; verify no explicit index hints exist.

Bottom line: Measured tactical actions (cold storage + index rationalisation + dedupe) yield immediate, verifiable savings (54.1 GiB + 14.0 GiB + 1.2 GiB = 69.3 GiB measured potential reduction; sources: cost_strategy entries). Further savings may be available but were not measured.

---

## What the data can do (dimensional monetisation — aggregate or de‑identified only)
Each candidate below is presented as an aggregate/de‑identified product only (no row‑level release).

1. Reference and master-data licensing
   - Proposition: licence cleaned reference/master tables (product/catalogue/form reference) as master data feeds to partners (requires rights). Readiness: score 60.1, grade C (data_products.reference_data.readiness_score = 60.1; readiness_grade = "C"). PII exposure: 62.1% of tables supporting the product carry PII markers; 40.2% supporting tables are stale (product blockers). Top value tables include mpesa_stk_requests and media but many have high PII ratios (e.g. mpesa_stk_requests pii_ratio = 1.0). Before licensing, de‑identify or publish only canonical reference fields and secure an explicit rights grant (blockers: "62.0% of supporting tables carry PII markers" and "use rights are declared at Connect, not measured").

2. Content catalogue, recommendation and licensing corpus
   - Proposition: aggregate catalogue metadata, engagement‑weighted recommendation features, licensable archive indices. Readiness: score 56.8, grade C (data_products.content_corpus.readiness_score = 56.8). PII exposure: high — 74.5% of supporting tables carry PII markers (product pii_table_share = 0.745) and 42.9% of supporting tables are stale (stale_table_share = 0.429). Licensable units exist (e.g. 4,037,354 distinct content values from playback_stagings.content_length). Any external catalogue or recommendation product must strip or aggregate PII (product blocker: "74.0% of supporting tables carry PII markers") and obtain rights clearance.

3. Channel / telco engagement analytics
   - Proposition: aggregated channel performance and campaign benchmarks (shortcode, delivery and response rates) for telcos/advertisers. Readiness: score 59.7, grade C (data_products.channel_engagement.readiness_score = 59.7). PII exposure: 78.9% supporting tables carry PII markers (pii_table_share = 0.789). Grain supports channel/time aggregation (licenses: 6,698,441 distinct channel values). Publish as aggregated metrics per channel/time bucket (e.g. daily county‑level response rates) after de‑identification and rights clearance.

4. Customer / subscriber 360 and segmentation (de‑identified)
   - Proposition: de‑identified LTV, segmentation and churn cohorts sold to partners or used internally for marketing; must be de‑identified before release. Readiness: score 53.5, grade D (data_products.customer_360.readiness_score = 53.5). PII exposure: 80.3% of supporting tables carry PII markers (pii_table_share = 0.803); many supporting tables are stale (stale_table_share = 0.513). The product can be built internally after cleansing, but external sharing requires strict hashing/tokenisation and a formal rights/legal review.

5. Time-series forecasting datasets (money/time)
   - Proposition: aggregated daily/weekly demand and revenue series for forecasting and capacity planning. Readiness: score 57.6, grade C (data_products.forecasting.readiness_score = 57.6). PII exposure: 76.8% supporting tables carry PII markers. Key time-range units exist (e.g. mpesa_stk_requests spans many historical days). Publish aggregated series (sums, counts, rates) at product/time granularity after removing direct identifiers and ensuring no small‑count leakage.

6. Transaction analytics (settlement and fee reporting)
   - Proposition: aggregated revenue, fee and settlement analytics for financial reconciliation and partner dashboards. Readiness: score 57.6, grade C (data_products.transaction_analytics.readiness_score = 57.6). PII exposure: 76.8% of supporting tables are PII‑dense. Release only as aggregated reports (daily/partner-level), and do not export row‑level payment identifiers without explicit legal clearance. Note: several top tables (mpesa_stk_requests, users, orders) carry full PII and must be tokenised.

7. Geospatial demand and coverage mapping
   - Proposition: county/constituency demand, penetration and coverage maps delivered as aggregated indices. Readiness: score 52.7, grade D (data_products.geo_demand.readiness_score = 52.7). PII exposure: 77.8% supporting tables carry PII; many supporting tables are stale. Produce aggregated indices (e.g. popularity per county per month) but remove or bucket fine geolocation fields to avoid re‑identification (product blockers note supporting tables grade D/E and PII risk).

8. Civic and audience insight panels
   - Proposition: aggregated civic‑participation indices and aggregated audience panels by geography; strictly aggregate, never row‑level. Readiness: score 49.0, grade D (data_products.civic_insight.readiness_score = 49.0). PII exposure: 85.7% of supporting tables carry PII markers (pii_table_share = 0.857). This product is feasible but requires the most remediation — remove or aggregate PII, improve completeness and confirm rights.

For every candidate product: do not release row‑level data; apply aggregation, k‑anonymity / differential privacy (where practical), or tokenisation; obtain explicit rights grants (product blockers repeatedly flag rights unmeasured).

---

## Risks and obligations
1. Personal data and privacy
   - High PII footprint: 71.8% of sampled rows carry personal‑data markers (headline.pii_pct = 71.8; pii_rows_checked = 1,011,330). Top PII tables include playback_stagings, sms, payment_requests (top_pii list). Any external sharing must be preceded by legal review and technical de‑identification/tokenisation. The detector used is sampled/deterministic — absence of a marker ≠ absence of personal data.
2. Staleness and value decay
   - Stale bytes account for 15.4% of bytes (headline.stale_pct_of_bytes = 15.4); multiple products note that many supporting tables have not been written for over a year. This reduces commercial value for time‑sensitive products (forecasts, engagement).
3. Rights and licensing
   - Use rights are declared at Connect but were not measured in the census; the summary repeatedly flags: "use rights are declared at Connect, not measured: a release needs its own grant and purpose" (per-product blockers). Do not publish or license data without explicit, recorded contractual grants for the intended purpose.
4. Re‑identification risk from near‑duplicates and granular fields
   - Near‑duplicate text is very high (85.3%) and granular columns (e.g. latitude/longitude, session keys, wallet identifiers) are present at high cardinality. Aggregation must account for linkage risk; small‑count suppression and rigorous review are required.
5. Structural and referential integrity
   - The census found orphaned references (examples: invoices.payment_id → payments orphan_ratio = 1.0; viusasa_staging.active_users.user_id orphan_ratio = 1.0; full list in orphaned_references). These undermine joins used in products and must be reconciled or documented as known gaps.
6. Unmeasured items
   - Total bytes (canonical bytes_total) is unmeasured in the supplied summary. Use rights and licence terms are not fully measured. Where a figure is missing in the transcript, it remains unmeasured — proceed on the basis that those items require explicit measurement before financial projection or transfer.

---

## 90‑day plan (numbered, decisive)
Priority: secure & reduce cost, remediate PII exposure, prepare one pilot product (channel_engagement or forecasting) for internal use.

1. Governance & legal (Days 0–10)
   - Action: Convene a 2‑hour triage between Data Owner, Legal, and Data Engineering.
   - Deliverable: Inventory of required rights per intended product (confirm whether Connect grants cover the use cases). Status: rights were not measured — therefore obtain explicit grants before any external release (product blockers).

2. Immediate containment of exposed PII (Days 0–14)
   - Action: Apply read‑only access controls to high‑PII tables identified in top_pii (e.g., playback_stagings, sms, payment_requests) and log all accesses.
   - Deliverable: Access control list and audit log retention policy. Rationale: headline.pii_pct = 71.8 and pii_rows_checked = 1,011,330.

3. Cold‑storage and archival for stale tables (Days 0–30)
   - Action: Export tables not written for > 1 year to compressed object storage; keep schema stubs and a retrieval process.
   - Target: 54.1 GiB measured candidate (cost_strategy[0]: bytes_label = 54.1 GiB; share_of_estate = 0.1541).
   - Deliverable: Archive manifest, restore runbook, and cost estimate for object storage.

4. Quick index rationalisation (Days 7–30)
   - Action: Identify non‑unique indexes that are leading prefixes of others and drop after 7‑day query monitoring.
   - Target measured saving: 14.0 GiB (cost_strategy[1]: bytes_label = 14.0 GiB).
   - Deliverable: Index removal roll‑back plan and before/after performance dashboard.

5. Exact deduplication pilot (Days 7–45)
   - Action: For three large, high‑value tables (suggest: mpesa_stk_requests, orders, playback_stagings), run dedupe pass and validate joins.
   - Target measured saving: 1.2 GiB (cost_strategy[2]: bytes_label = 1.2 GiB).
   - Deliverable: De‑duplication scripts, preserved archive of removed rows, and updated ingestion constraints.

6. Empty & duplicate table cleanup (Days 14–40)
   - Action: Place empty tables (368) into a 30‑day observation window; retire or archive after confirmation. Consolidate high‑overlap duplicate pairs (see top_duplicate_pairs) by snapshotting the smaller copy and retaining one system of record after owner sign‑off.
   - Deliverables: Retire list, snapshots, and owner confirmations (cost_strategy[3] and [4]).

7. Repair or document orphaned references (Days 14–60)
   - Action: For the orphaned_references list, either (a) repair by reintroducing or reassigning targets where available, or (b) document and purge rows that reference nothing.
   - Deliverable: Referential integrity report and remediation tasks (note: repair does not save storage but improves product quality).

8. PII tokenisation and analytics copy creation (Days 21–60)
   - Action: Create de‑identified analytics copies (tokenise ids, drop direct identifiers) for development of internal products. For each copy, produce a privacy risk memo.
   - Deliverable: Tokenisation scripts, one de‑identified analytics schema per product domain (channel_engagement and forecasting prioritised).

9. Pilot product delivery (Days 30–75)
   - Action: Build an internal pilot for Channel Engagement (or Forecasting) using de‑identified analytics copy.
   - Metrics: deliver aggregated dashboards (daily/weekly channel response rates), run an internal privacy review, and collect stakeholder feedback.
   - Readiness rationale: channel_engagement readiness_score = 59.7; forecasting readiness_score = 57.6.

10. Rights & commercial readiness (Days 45–90)
    - Action: For any external pilot or licensing, obtain explicit written rights from Connect or other owners; produce a Data Release Agreement and a Pricing/Usage policy (note: pricing not measured and must be determined by business).
    - Deliverable: Signed rights, release checklist, and minimal product SLA.

11. Data quality remediation (Days 30–90)
    - Action: Remediate top quality issues: reduce null_bearing_pct (81.7%) by addressing ingest validation on key tables; fix highest‑impact degraded tables listed in top_degraded.
    - Deliverable: Data quality tickets, measurable targets (e.g. reduce null_bearing in target tables by 30% in 60 days).

12. Measurement & ongoing census (Days 60–90)
    - Action: Run a follow‑up census on measured tables (recompute exact/near duplicates, PII share, staleness).
    - Deliverable: Comparison report vs. baseline (this dossier). Use the report to set the next 90‑day OKRs.

---

If you approve, I will:
- Produce an access‑controlled remediation workbook (per step) with owners and deadlines.
- Prepare the de‑identification templates and a privacy risk checklist for the pilot product(s).

Notes and caveats
- Several values in the supplied inventory are placeholders or unmeasured (for example the canonical total bytes figure is unmeasured). Where figures were missing they are reported as unmeasured and must be measured before cost or revenue projections are final.
- Rights: the summary repeatedly states "use rights are declared at Connect, not measured" — do not proceed with any licensing or outward release until the legal grant is obtained and captured.
- All releases must be aggregate or de‑identified; the census explicitly flags many tables with PII markers and high PII ratios (per‑product blockers and top_pii entries).

Appendix: primary figures cited
- Overall: databases = 20; total tables = 1,006; tables_measured = 638 (headline).
- Measured rows = 5,881,277 (headline.rows_measured).
- Exact duplicates = 1.5%; normalised duplicates = 3.6% (headline).
- Degraded rows = 23.0% (headline.degraded_pct).
- Null-bearing rows = 81.7% (headline.null_bearing_pct).
- PII in sampled rows = 71.8% (headline.pii_pct; pii_rows_checked = 1,011,330).
- Reclaimable: 15.2 GiB (reclaimable_label) = 4.3% reclaimable_pct (headline).
- Stale bytes = 15.4% of bytes (headline.stale_pct_of_bytes).
- Cost strategies measured savings: cold storage 54.1 GiB; drop redundant indexes 14.0 GiB; dedupe 1.2 GiB; consolidate copies 54.0 MiB; archive empty tables 13.7 MiB (cost_strategies entries).
- Readiness distribution: A=171, B=62, C=191, D=189, E=25 (headline.grades).

--- 

Tell me which of the 90‑day steps you want prioritised and I will convert that into a weekly sprint plan with owners and minimal checklists.
