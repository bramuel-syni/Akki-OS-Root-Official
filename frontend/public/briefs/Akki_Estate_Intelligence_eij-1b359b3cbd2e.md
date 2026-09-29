# Akki Estate Intelligence — RMS MySQL estate

Job `eij-1b359b3cbd2e` · status **partial** · measured 2026-09-29T19:12:15.151993Z · built 2026-09-29T19:31:12.533733Z

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
