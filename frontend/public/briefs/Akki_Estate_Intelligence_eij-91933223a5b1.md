# Akki Estate Intelligence — RMS MySQL estate

Job `eij-91933223a5b1` · status **partial** · measured 2026-09-29T18:49:55.453268Z · built 2026-10-03T01:10:25.048916Z

Census only: rows were measured on the jump host and discarded; this brief carries aggregates, sketches and hashes — no row, cell or identifier value.

## What the census found

19 databases and 703 tables (12.8 GiB, ≈25,599,098 rows) were measured; 0.3% of rows repeat exactly, 11.1% carry damage, 35.6% have empty required-looking fields and 61.1% of sampled rows carry personal-data markers. About 358.0 MiB (2.7%) looks reclaimable.

| Figure | Value |
|---|---|
| Connections / databases / tables | 5 / 19 / 703 |
| Rows (estimate) / rows measured | 25,599,098 / 2,565,679 |
| Bytes held (data + index) | 12.8 GiB |
| Exact duplicate rows | 0.3% (normalised 2.8%) |
| Degraded rows (placeholder, mojibake, truncation) | 11.1% |
| Rows with empty fields | 35.6% |
| Sampled rows with PII markers | 61.1% |
| Long-text near-duplicates (MinHash) | 75.4% |
| Bytes in tables not written for > 1 year | 50.6% |
| Reclaimable bytes (estimate) | 358.0 MiB (2.7%) |
| Same-schema duplicate table pairs with content overlap | 62 |
| Tables failed / empty | 44 / 300 |
| Table readiness grades | A: 117, B: 43, C: 87, D: 131, E: 21 |

## Databases — readiness grades and dimensional profile

| Connection / database | Tables | Rows est. | Bytes | Grade | Dimensions (tables carrying) |
|---|---|---|---|---|---|
| iebc_forms / viupay_agent_staging | 31 | 12,055,806 | 1.2 GiB | A (87.2) | identity 31, time 21, channel 21, money 20, measure 19, entity 16 |
| citizen_digital / db_visitors | 47 | 4,597,822 | 2.7 GiB | D (53.9) | identity 45, time 38, measure 21, content 17, entity 16, engagement 14 |
| viupay / viutickets | 57 | 2,131,949 | 421.2 MiB | B (77.4) | identity 54, time 50, measure 31, engagement 30, money 17, content 17 |
| iebc_forms / viutickets | 56 | 1,607,465 | 338.7 MiB | B (76.9) | identity 53, time 49, measure 31, engagement 30, money 17, product 16 |
| Razuna (Library Content) & Newsvault (Radio News content) / razuna | 82 | 1,341,823 | 4.5 GiB | D (53.3) | identity 79, content 40, measure 34, time 34, entity 27, product 15 |
| citizen_digital / local | 17 | 987,599 | 540.3 MiB | D (52.7) | identity 11, time 8, measure 7, engagement 3, entity 3, geo 2 |
| Razuna (Library Content) & Newsvault (Radio News content) / news_vault | 30 | 856,820 | 932.0 MiB | C (55.5) | identity 27, time 21, content 13, entity 7, measure 7, engagement 3 |
| viupay / kra_reports | 27 | 821,933 | 1.5 GiB | D (52.2) | identity 26, time 22, measure 14, entity 11, money 7, content 6 |
| citizen-pulse / saa | 28 | 423,473 | 153.0 MiB | D (52.0) | identity 26, time 20, entity 10, content 9, measure 8, engagement 6 |
| iebc_forms / viusasa_miniapps_prod | 21 | 272,232 | 216.8 MiB | D (51.6) | identity 21, time 17, measure 16, entity 8, content 6, product 6 |
| citizen-pulse / citizen-pulse | 39 | 157,828 | 70.4 MiB | unmeasured (None) |  |
| viupay / viupay | 39 | 138,966 | 105.0 MiB | C (55.7) | identity 36, time 35, entity 27, measure 24, money 11, engagement 10 |
| iebc_forms / iebc_forms | 3 | 135,432 | 53.6 MiB | C (60.8) | identity 3, time 3, content 2, measure 1 |
| iebc_forms / viupay | 38 | 67,080 | 61.3 MiB | D (47.3) | identity 35, time 34, entity 26, measure 23, money 10, engagement 9 |
| iebc_forms / ecommerce_tafaria | 130 | 981 | 6.0 MiB | B (84.3) | identity 128, time 121, measure 84, engagement 57, entity 48, money 39 |
| iebc_forms / viusasa_artists | 8 | 898 | 464.0 KiB | C (61.9) | identity 7, time 7, content 4, entity 3, measure 3, engagement 2 |
| iebc_forms / kra_reports | 19 | 768 | 864.0 KiB | D (54.0) | identity 18, time 17, measure 11, entity 10, money 4, content 4 |
| citizen-pulse / correspondents | 10 | 169 | 304.0 KiB | D (51.0) | identity 7, measure 6, time 6, entity 3, money 1, geo 1 |
| iebc_forms / miniapps | 21 | 54 | 944.0 KiB | D (42.9) | identity 21, time 17, measure 17, entity 8, content 6, product 6 |

## Degradation and trend

Row-weighted share of measured rows whose worst column shows the kind; a row can carry several kinds.

| Damage kind | Share of measured rows |
|---|---|
| mojibake | 0.0% |
| placeholder | 6.2% |
| truncation | 5.0% |
| invalid_format | 4.9% |
| whitespace | 3.5% |

Never-populated columns: 539 of 4,167 measured (12.9%). Columns never populated (null on ≥99.9 % of measured rows, primary key excluded): schema carried without data.

| Connection / database | Degraded rows | Dead columns | Stale tables | Writes span | Last write | Schema drift | Rows Δ |
|---|---|---|---|---|---|---|---|
| iebc_forms / miniapps | 71.4% | 16 / 52 | 4 | 1,409 days | 660 days ago | 0 | — |
| viupay / viupay | 69.4% | 20 / 264 | 11 | 2,088 days | 0 days ago | 0 | — |
| iebc_forms / viupay | 67.5% | 22 / 248 | 21 | 1,098 days | 628 days ago | 0 | — |
| citizen_digital / db_visitors | 37.6% | 55 / 418 | 8 | 21,947 days | 0 days ago | 0 | — |
| iebc_forms / viutickets | 25.4% | 38 / 479 | 38 | 1,041 days | 550 days ago | 0 | — |
| viupay / viutickets | 23.2% | 39 / 489 | 19 | 4,821 days | 0 days ago | 0 | — |
| Razuna (Library Content) & Newsvault (Radio News content) / razuna | 2.6% | 107 / 532 | 17 | 4,292 days | 16 days ago | 0 | — |
| citizen-pulse / saa | 1.7% | 16 / 159 | 7 | 1,368 days | 0 days ago | 0 | — |
| iebc_forms / kra_reports | 1.2% | 11 / 93 | 6 | 542 days | 994 days ago | 0 | — |
| iebc_forms / viusasa_artists | 0.4% | 14 / 70 | 6 | 214 days | 1,652 days ago | 0 | — |
| iebc_forms / ecommerce_tafaria | 0.2% | 93 / 390 | 33 | 11,593 days | 1,830 days ago | 0 | — |
| iebc_forms / viusasa_miniapps_prod | 0.0% | 31 / 134 | 6 | 2,066 days | 3 days ago | 0 | — |
| iebc_forms / iebc_forms | 0.0% | 2 / 31 | 0 | no timestamps | — | 0 | — |
| iebc_forms / viupay_agent_staging | 0.0% | 39 / 402 | 19 | 601 days | 1,537 days ago | 0 | — |
| viupay / kra_reports | 0.0% | 19 / 159 | 2 | 1,533 days | 3 days ago | 0 | — |
| citizen_digital / local | 0.0% | 4 / 73 | 5 | 488 days | 570 days ago | 0 | — |
| citizen-pulse / citizen-pulse | —% | 0 / 0 | 0 | no timestamps | — | 0 | — |
| citizen-pulse / correspondents | 0.0% | 3 / 19 | 0 | 273 days | 295 days ago | 0 | — |
| Razuna (Library Content) & Newsvault (Radio News content) / news_vault | 0.0% | 10 / 155 | 6 | 1,462 days | 16 days ago | 0 | — |

No previous verified census to compare against; trend starts with the next census.

## What the data can do — dimensional monetisation candidates

Ranked by rows × readiness × supporting dimensions. Every candidate is an aggregate or de-identified product; rights are declared at Connect, not measured here.

### 1. Content catalogue, recommendation and licensing corpus — grade C

Catalogue metadata, engagement-weighted recommendation features and licensable archive indexes.

- Dimensions required: content; supporting: engagement, time
- 50 supporting tables, ≈8,069,529 rows across 13 databases
- Licensable grain: ≈268,263 distinct content values (viupay/kra_reports.viusasa_postings.tims_posted_at); history 1970-01-01 → 2030-02-02 (21,947 days; viupay/viutickets.movie_seats.created_at); ≈268,263 distinct engagement values (viupay/kra_reports.viusasa_postings.response); latest timestamp lies in the future: placeholder dates are present in the time dimension
- Top tables: viupay/viutickets.movie_seats (1,158,096 rows, A); iebc_forms/viutickets.movie_seats (834,440 rows, A); iebc_forms/viupay_agent_staging.tbl_lastsession (935,106 rows, B); viupay/viupay.mpesa_stk_requests (20,888 rows, A)
- Blockers: 80.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 2. Reference and master-data licensing — grade D

Clean product / catalogue / form reference tables licensable as master data where rights permit.

- Dimensions required: product; supporting: content, identity
- 32 supporting tables, ≈4,023,136 rows across 10 databases
- Licensable grain: ≈460,786 distinct content values (Razuna (Library Content) & Newsvault (Radio News content)/razuna.raz1_videos.VID_NAME_IMAGE); ≈478,938 distinct identity values (Razuna (Library Content) & Newsvault (Radio News content)/razuna.raz1_videos.VID_CUSTOM_ID); ≈12,498 distinct product values (viupay/viutickets.media.order_column); history 1970-01-01 → 2030-02-02 (21,947 days; iebc_forms/viupay_agent_staging.tbl_lastsession.entrydate); latest timestamp lies in the future: placeholder dates are present in the time dimension
- Top tables: iebc_forms/viupay_agent_staging.tbl_lastsession (935,106 rows, B); viupay/viutickets.media (471,627 rows, C); iebc_forms/viutickets.media (392,888 rows, C); Razuna (Library Content) & Newsvault (Radio News content)/news_vault.stories (233,527 rows, C)
- Blockers: 78.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 3. Channel / telco engagement analytics (USSD, SMS, app) — grade C

Channel performance, shortcode and campaign attribution, response-rate benchmarks.

- Dimensions required: channel, time; supporting: engagement, entity
- 22 supporting tables, ≈4,517,978 rows across 9 databases
- Licensable grain: ≈189,723 distinct channel values (iebc_forms/viupay_agent_staging.agent_api_logs.msisdn); ≈1,247,320 distinct engagement values (citizen_digital/db_visitors.event_logs.event_log_id); history 2014-12-16 → 2026-09-29 (4,305 days; iebc_forms/viupay_agent_staging.agent_api_logs.entrydate); ≈211,545 distinct entity values (citizen_digital/db_visitors.event_logs.staff_id)
- Top tables: iebc_forms/viupay_agent_staging.agent_api_logs (522,652 rows, B); iebc_forms/viupay_agent_staging.tbl_lastsession (935,106 rows, B); citizen_digital/db_visitors.event_logs (2,494,639 rows, D); Razuna (Library Content) & Newsvault (Radio News content)/razuna.raz1_log_users (45,494 rows, B)
- Blockers: 91.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 4. Customer / subscriber 360 and segmentation — grade D

Segmentation, lifetime value and retention modelling across products; requires de-identification before any release.

- Dimensions required: engagement, entity; supporting: channel, geo
- 38 supporting tables, ≈6,039,769 rows across 12 databases
- Licensable grain: ≈1,247,320 distinct engagement values (citizen_digital/db_visitors.event_logs.event_log_id); ≈211,545 distinct entity values (citizen_digital/db_visitors.event_logs.staff_id); history 1970-01-01 → 2030-02-02 (21,947 days; viupay/viupay.mpesa_stk_requests.created_at); ≈748 distinct channel values (citizen_digital/db_visitors.event_logs.device_name); ≈20,442 distinct geo values (citizen_digital/local.uploaded_files.file_location); latest timestamp lies in the future: placeholder dates are present in the time dimension
- Top tables: viupay/viupay.mpesa_stk_requests (20,888 rows, A); citizen_digital/db_visitors.event_logs (2,494,639 rows, D); citizen-pulse/saa.submissions (20,159 rows, C); Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits (481,349 rows, D)
- Blockers: 82.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 5. Transaction & revenue analytics — grade C

Revenue, fee and settlement analytics; cohort and churn views once the entity dimension is joined.

- Dimensions required: money, time; supporting: entity
- 34 supporting tables, ≈1,142,878 rows across 8 databases
- Licensable grain: ≈21,671 distinct entity values (viupay/viutickets.orders.customer_id); ≈268,317 distinct money values (viupay/kra_reports.viusasa_postings.cu_invoice_number); history 2022-01-10 → 2026-09-29 (1,723 days; viupay/viupay.mpesa_stk_requests.created_at)
- Top tables: viupay/viupay.mpesa_stk_requests (20,888 rows, A); iebc_forms/viupay.mpesa_stk_requests (9,789 rows, B); viupay/viupay.mm_pay_instruments (16,299 rows, B); viupay/viutickets.orders (32,326 rows, C)
- Blockers: 91.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 6. Geospatial demand and coverage mapping — grade D

County / constituency level demand, penetration and service-coverage maps sold as aggregated indices.

- Dimensions required: geo, time; supporting: engagement, money
- 20 supporting tables, ≈1,963,125 rows across 8 databases
- Licensable grain: ≈20,442 distinct geo values (citizen_digital/local.uploaded_files.file_location); ≈48 distinct engagement values (Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits.event); history 2022-09-15 → 2026-09-29 (1,475 days; Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits.created_at)
- Top tables: citizen_digital/db_visitors.ci_sessions (56,175 rows, B); Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits (481,349 rows, D); citizen_digital/db_visitors.audits (219,709 rows, D); citizen-pulse/saa.submissions (20,159 rows, C)
- Blockers: 75.0% of supporting tables carry PII markers: de-identify or aggregate before any release · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 7. Time-series forecasting datasets — grade C

Daily/weekly demand and revenue series for forecasting products and planning benchmarks.

- Dimensions required: money, time; supporting: geo, product
- 34 supporting tables, ≈1,142,878 rows across 8 databases
- Licensable grain: ≈268,317 distinct money values (viupay/kra_reports.viusasa_postings.cu_invoice_number); history 2022-01-10 → 2026-09-29 (1,723 days; viupay/viupay.mpesa_stk_requests.created_at); ≈19,719 distinct product values (viupay/viutickets.payment_processings.order_id)
- Top tables: viupay/viupay.mpesa_stk_requests (20,888 rows, A); iebc_forms/viupay.mpesa_stk_requests (9,789 rows, B); viupay/viupay.mm_pay_instruments (16,299 rows, B); viupay/kra_reports.viusasa_postings (536,526 rows, D)
- Blockers: 91.0% of supporting tables carry PII markers: de-identify or aggregate before any release · most supporting tables have not been written for over a year: value is historical, not live · use rights are declared at Connect, not measured: a release needs its own grant and purpose

### 8. Civic and audience insight panels — grade D

Aggregated audience and civic-participation indices by geography; strictly aggregate, never row-level.

- Dimensions required: entity, geo; supporting: content, engagement
- 16 supporting tables, ≈1,903,655 rows across 8 databases
- Licensable grain: ≈78,156 distinct content values (citizen_digital/local.uploaded_files.text_file_path); ≈48 distinct engagement values (Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits.event); ≈23,153 distinct entity values (Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits.user_id); ≈20,442 distinct geo values (citizen_digital/local.uploaded_files.file_location); history 2022-01-10 → 2026-09-29 (1,723 days; citizen_digital/local.uploaded_files.time_processed)
- Top tables: citizen_digital/local.uploaded_files (79,759 rows, C); Razuna (Library Content) & Newsvault (Radio News content)/news_vault.audits (481,349 rows, D); citizen_digital/db_visitors.audits (219,709 rows, D); citizen-pulse/saa.submissions (20,159 rows, C)
- Blockers: 88.0% of supporting tables carry PII markers: de-identify or aggregate before any release · supporting tables grade D/E on completeness, duplication or degradation: cleanse first · use rights are declared at Connect, not measured: a release needs its own grant and purpose

## Strategies to reduce cost

Priced with database storage at USD 0.1095/GB-month and object storage at USD 0.023/GB-month (reference list prices, not the owner's invoice: Huawei Cloud RDS for MySQL cloud SSD AF-Johannesburg 0.00015 USD/GB-hour x 730 h; OBS Standard 0.023 USD/GB-month); overlaps between strategies are possible, so the total is an upper bound.

| Strategy | Reclaimable | Share | Saving / month | Action |
|---|---|---|---|---|
| Move buckets not written for over a year to archive-class storage | 41.9 TiB | — | USD 986.49 | Apply a lifecycle rule (Standard → Archive/Cold) on buckets whose last object write is older than a year; keep listing metadata hot. |
| Reconcile duplicate objects across OBS buckets | 7.7 TiB | — | USD 180.33 | Confirm ETag+size candidates by object hash, keep one copy per bucket and replace the rest with references or lifecycle-delete them. |
| Move tables not written for over a year to cold storage | 6.5 GiB | 50.6% | USD 0.71 | Export to compressed object storage, keep a schema stub and a pointer; restore on demand. |
| Remove redundant (prefix-covered) indexes | 204.0 MiB | 1.6% | USD 0.02 | Drop each non-unique index whose columns are a leading prefix of another index on the same table. |
| De-duplicate exact repeated rows inside tables | 87.6 MiB | 0.7% | USD 0.01 | Add uniqueness constraints or a merge step at ingestion; archive the historical duplicates. |
| Consolidate duplicate and staging copies of the same tables | 55.5 MiB | 0.4% | USD 0.01 | Retire or snapshot-then-drop the smaller copy of each same-schema pair with measured content overlap; keep one system of record. |
| Drop or archive empty tables | 10.9 MiB | 0.1% | USD 0.00 | Remove empty tables and their indexes after a 30-day observation window. |
| Repair or purge orphaned references | not a storage saving | — | unpriced | Reconcile foreign-key candidates whose sampled values are missing in the target table; purge rows that reference nothing. |
| Minimise PII-dense tables that no product needs | not a storage saving | — | unpriced | Tokenise or drop personal columns in analytics copies; keep raw identifiers only in the system of record. |

Priced strategies total ≈ USD 1,167.57 per month (upper bound; overlaps possible).

### Evidence per strategy

**Move buckets not written for over a year to archive-class storage** — risk: Last write is the newest object timestamp in the listing; read frequency was not measured, and archive-class retrieval carries its own fee.

- music-bucket-rms · last write 920 days before the census · 4.9 TiB
- na7p43do · last write 911 days before the census · 4.1 TiB
- na7p43js · last write 913 days before the census · 3.6 TiB
- na7p434j · last write 911 days before the census · 3.5 TiB
- na7p41hj · last write 919 days before the census · 3.5 TiB
- na7p42xe · last write 911 days before the census · 3.4 TiB

**Reconcile duplicate objects across OBS buckets** — risk: Candidates share ETag and size, which for multipart uploads is not a content hash; bytes are candidates × mean object size, an estimate. Confirm before deleting.

- na7p43do · 197,528 candidates · ≈1.7 TiB
- na7p4oco · 166,328 candidates · ≈1.0 TiB
- na7p434j · 2,890 candidates · ≈674.1 GiB
- na7p42yg · 4,197 candidates · ≈501.9 GiB
- music-bucket-rms · 14,696 candidates · ≈485.3 GiB
- 2024offairrecs · 16,634 candidates · ≈462.4 GiB

**Move tables not written for over a year to cold storage** — risk: Staleness is read from the latest timestamp column; tables without timestamps are not counted as stale.

- razuna.raz1_videos · 1341 days · 3.0 GiB
- razuna.raz1_errors · 1340 days · 745.5 MiB
- local.audits · 733 days · 330.9 MiB
- kra_reports.external_credit_notes · 379 days · 277.8 MiB
- viupay_agent_staging.agent_api_logs · 1558 days · 166.7 MiB
- viutickets.media · 613 days · 152.7 MiB

**Remove redundant (prefix-covered) indexes** — risk: Write amplification falls immediately; verify no query hints name the dropped index.

- ecommerce_tafaria.playbacks · playbacks_playable_type_index covered by playbacks_playable_type_playable_id_index
- kra_reports.command_logs · command_logs_command_index covered by command_logs_command_started_at_index
- kra_reports.viusasa_postings · viusasa_postings_invoice_number_index covered by viusasa_postings_invoice_number_credited_at_index
- db_visitors.event_logs · event_logs_event_log_id_index covered by event_logs_event_log_id_unique
- saa.questionnaires · idx_avail_on_ussd covered by idx_ussd_menu
- saa.questions · idx_questionnaire_id covered by idx_questionnaire_order

**De-duplicate exact repeated rows inside tables** — risk: Duplicates measured on complete passes or stratified samples; the primary key was excluded from the comparison.

- kra_reports.external_credit_notes · 25.0% repeated · 277.8 MiB
- razuna.raz1_errors · 2.0% repeated · 745.5 MiB
- viutickets.movies · 7.5% repeated · 8.5 MiB
- viutickets.movies · 8.5% repeated · 6.5 MiB
- viutickets.movie_shows · 11.0% repeated · 4.5 MiB
- viutickets.movie_shows · 12.6% repeated · 3.5 MiB

**Consolidate duplicate and staging copies of the same tables** — risk: Copies may be deliberate (staging, backups). Confirm ownership before retirement; the sketch overlap is an estimate, not a row-level diff.

- iebc_forms/viupay.failed_jobs ↔ viupay/viupay.failed_jobs · overlap 83.0% · 31.6 MiB
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
- … 292 more

**Repair or purge orphaned references** — risk: Targets were inferred from column names (x_id → x/xs); a missing target may be a naming convention, not a break.

- ecommerce_tafaria.invoices.order_id → orders · 100.0% orphaned of 4 sampled
- ecommerce_tafaria.invoices.payment_id → payments · 100.0% orphaned of 1 sampled
- viutickets.booked_concessions.booking_id → bookings · 100.0% orphaned of 3 sampled
- viutickets.coupons.movie_show_id → movie_shows · 100.0% orphaned of 1 sampled
- viutickets.movie_bookings.booking_id → bookings · 100.0% orphaned of 3 sampled
- viutickets.booked_concessions.booking_id → bookings · 100.0% orphaned of 3 sampled

**Minimise PII-dense tables that no product needs** — risk: Detector is deterministic and sampled; absence of a marker is not absence of personal data.

- viupay_agent_staging.tbl_free_transid · 60.0% of sampled rows
- db_visitors.event_logs · 100.0% of sampled rows
- viupay_agent_staging.tbl_lastsession · 100.0% of sampled rows
- kra_reports.viusasa_postings · 100.0% of sampled rows
- viupay_agent_staging.agent_api_logs · 100.0% of sampled rows
- news_vault.audits · 100.0% of sampled rows

## Object and file estate (OBS buckets, NAS shares)

**OBS object store** — census `cr-f1415e395361` (partial, 2026-10-02T19:20:31.205815+00:00): 66 of 106 sources complete, 22,997,353 objects, 130.8 TiB; 1,158,906 duplicate candidates (5.0% of objects), ≈7.7 TiB estimated; 43 sources not written for over a year (41.9 TiB). Frontier complete: yes.

Duplicate candidates are objects whose ETag+size fingerprint was already seen in the same store; duplicate bytes = candidates × mean object size of the bucket (estimate). Not proven byte duplicates.

| Source | Status | Units | Bytes | Duplicate candidates | Last write | Formats |
|---|---|---|---|---|---|---|
| 2024offairrecs | complete | 3,194,745 | 86.7 TiB | 16634 | 2026-10-02T03:00:00.626000Z | .mp4 3,151,459, .mp3 27,002, no_extension 15,706, .mpt 408 |
| music-bucket-rms | complete | 152,801 | 4.9 TiB | 14696 | 2024-03-26T05:26:00.449000Z | .mp4 146,617, .txt 1,183, .flx 1,086, .rpt 610 |
| na7p43do | complete | 484,480 | 4.1 TiB | 197528 | 2024-04-04T02:11:50.597000Z | .mp3 326,105, .mts 39,439, .vis 39,437, .wav 12,472 |
| na7p43js | complete | 307,998 | 3.6 TiB | 27187 | 2024-04-02T06:06:20.407000Z | .ogg 118,600, .mp3 85,079, .adf 25,484, .vis 21,622 |
| na7p434j | complete | 15,377 | 3.5 TiB | 2890 | 2024-04-04T00:20:28.559000Z | .mov 5,427, .avi 4,258, .jpg 2,157, .txt 1,767 |
| na7p41hj | complete | 15,885 | 3.5 TiB | 1852 | 2024-03-27T08:11:46.711000Z | .mov 10,488, .mp4 2,347, .txt 1,519, .avi 1,198 |
| na7p42xe | complete | 13,965 | 3.4 TiB | 1120 | 2024-04-04T09:56:20.886000Z | .mp4 6,241, .mov 5,519, .txt 1,434, .avi 309 |
| na7p42xw | complete | 25,088 | 3.4 TiB | 2391 | 2024-03-31T09:49:02.340000Z | .mov 15,321, .txt 3,389, .avi 3,065, .mp4 1,289 |
| na7p42yg | complete | 28,059 | 3.3 TiB | 4197 | 2024-03-31T01:51:47.474000Z | .mov 21,920, .txt 3,169, .jpg 1,446, .avi 995 |
| na7p43d3 | complete | 16,396 | 2.9 TiB | 1395 | 2024-03-30T14:39:39.933000Z | .mov 10,623, .txt 2,032, .avi 1,270, .mp4 1,099 |
| na7p4oco | complete | 468,637 | 2.9 TiB | 166328 | 2024-04-03T20:50:57.931000Z | .mp3 218,902, .mts 36,886, .vis 36,878, .tmp 15,781 |
| rmsbroadcast | complete | 142,739 | 1.5 TiB | 5060 | 2024-03-24T09:25:18.604000Z | .mp3 127,221, .mp4 9,923, .mov 1,916, .m4v 1,550 |

Blocked sources (40): apr252017 (NoSuchBucket); citizen-vod (NoSuchBucket); elections (ClientError); feb272017 (NoSuchBucket); instore-radio-items (ClientError); iso-rms-storage (NoSuchBucket); librarydirectupload2 (NoSuchBucket); na7p4100 (NoSuchBucket); na7p410c (NoSuchBucket); na7p419y (NoSuchBucket); na7p41ab (NoSuchBucket); na7p41f4 (NoSuchBucket) …

**NAS file shares** — census `cr-cf4eef79995b` (complete, 2026-10-02T19:17:57.727454+00:00): 12 of 16 sources complete, 1,460,947 files, 43.7 TiB; duplication unmeasured (no fingerprints in this pass); 0 sources not written for over a year (0 B). Frontier complete: yes.

This enumeration recorded no content fingerprints (stat/listing only), so duplication is unmeasured; sizes and dates were read, bodies were not.

| Source | Status | Units | Bytes | Duplicate candidates | Last write | Formats |
|---|---|---|---|---|---|---|
| channel01 | complete | 95,122 | 6.9 TiB | — | 2026-09-29T03:25:01.311178Z | .mp4 95,108, .rmd 6, .mpt 3, .db 1 |
| channel02 | complete | 95,134 | 6.9 TiB | — | 2026-09-29T03:25:05.819412Z | .mp4 95,129, .db 1, .jpg 1, .rep 1 |
| channel16 | complete | 94,597 | 6.8 TiB | — | 2026-09-29T03:45:03.715768Z | .mp4 94,592, .db 1, .jpg 1, .rep 1 |
| Channel15 | partial · BUDGET_EXHAUSTED | 96,675 | 1.9 TiB | — | 2026-10-02T18:07:55Z | .mp4 96,667, .rmd 3, .db 1, .jpg 1 |
| Channel14 | partial · BUDGET_EXHAUSTED | 96,660 | 1.9 TiB | — | 2026-10-02T18:25:43Z | .mp4 96,654, .rmd 2, .db 1, .jpg 1 |
| Channel09 | partial · BUDGET_EXHAUSTED | 96,313 | 1.9 TiB | — | 2026-10-02T17:09:37Z | .mp4 96,309, .db 1, .jpg 1, .rep 1 |
| Channel11 | complete · BUDGET_EXHAUSTED | 95,602 | 1.9 TiB | — | 2026-09-29T03:12:09.048574Z | .mp4 95,592, .rmd 6, .db 1, .jpg 1 |
| Channel12 | complete | 95,600 | 1.9 TiB | — | 2026-09-29T03:15:28.913646Z | .mp4 95,590, .rmd 6, .db 1, .jpg 1 |
| channel07 | complete | 95,550 | 1.9 TiB | — | 2026-09-29T03:36:51.270784Z | .mp4 95,546, .db 1, .jpg 1, .rep 1 |
| channel06 | complete | 95,548 | 1.9 TiB | — | 2026-09-29T03:35:21.881683Z | .mp4 95,544, .db 1, .jpg 1, .rep 1 |
| channel05 | complete | 95,494 | 1.9 TiB | — | 2026-09-29T03:34:34.485438Z | .mp4 95,490, .db 1, .jpg 1, .rep 1 |
| channel04 | complete | 95,475 | 1.9 TiB | — | 2026-09-29T03:30:03.144274Z | .mp4 95,470, .db 1, .jpg 1, .rep 1 |

Blocked sources (4): Channel15 (BUDGET_EXHAUSTED); Channel14 (BUDGET_EXHAUSTED); Channel09 (BUDGET_EXHAUSTED); Channel13 (BUDGET_EXHAUSTED)

## Where it falls short

- Connection `iebc_forms` database `viusasa_staging`: PULL_SEAM_WORKER_FAILED:
- Connection `artists_app`: PULL_SEAM_WORKER_FAILED:pymysql.err.OperationalError: 1045 Access denied for user bramuel159.138.173.250 using password:
- Degraded: db_visitors.event_logs · 60.9% of 2,494,639 rows (stratified_keyset_sample)
- Degraded: viutickets.media · 100.0% of 471,627 rows (stratified_keyset_sample)
- Degraded: viutickets.media · 100.0% of 392,888 rows (stratified_keyset_sample)
- Degraded: db_visitors.telescope_entries · 100.0% of 164,127 rows (stratified_keyset_sample)
- Degraded: db_visitors.telescope_entries_tags · 100.0% of 42,165 rows (head_sample_no_single_primary_key)
- Degraded: razuna.raz1_folders_groups · 17.2% of 145,684 rows (stratified_keyset_sample)
- Degraded: viupay.payment_requests · 100.0% of 24,874 rows (complete)
- Degraded: viutickets.order_details · 100.0% of 22,010 rows (complete)
- PII-dense: viupay_agent_staging.tbl_free_transid · 60.3% of sampled rows
- PII-dense: db_visitors.event_logs · 100.0% of sampled rows
- PII-dense: viupay_agent_staging.tbl_lastsession · 100.0% of sampled rows
- PII-dense: kra_reports.viusasa_postings · 100.0% of sampled rows
- PII-dense: viupay_agent_staging.agent_api_logs · 100.0% of sampled rows
- PII-dense: news_vault.audits · 100.0% of sampled rows
- PII-dense: razuna.raz1_videos · 100.0% of sampled rows
- PII-dense: local.audits · 100.0% of sampled rows

## Method and limits

Ratios are measured on complete passes (tables ≤100k rows) or stratified keyset samples (8×5k rows) and disclosed per table; cross-table overlap is a bottom-256 sketch Jaccard estimate over same-schema tables; no row values were retained or returned.

RMS MySQL measured in depth (owner order 1-a). OBS object and NAS file estates are read from their retained enumeration receipts (listing and stat only: sizes, dates, ETag+size duplicate candidates; no object or file body); languages, rights and semantic (embedding) similarity were not measured. Text near-duplicates use MinHash on the jump host so row text never left the estate.
