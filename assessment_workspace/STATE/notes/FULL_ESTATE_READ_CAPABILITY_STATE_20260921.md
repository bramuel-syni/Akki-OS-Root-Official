# Full Estate Read-Capability Sweep — state note (2026-09-21)

**Wave**: CP-ESTATE-INGESTION.
**Slices released this run**: S1 (MySQL) + S2 (NAS, already answered) + S3 (OBS) — all as **read-capability surveys**, authenticated, read-only, single-touch proof-of-read per surface.
**Owner GO**: 2026-09-21T~13:40Z verbatim: "OWNER GO → FULL ESTATE READ-CAPABILITY SWEEP across ALL reachable surfaces … can we ACTUALLY READ THE CONTENT — not just reach the port."
**R-91 hold**: unchanged (~38h away — no touch). **Ratchet floor**: 5858 (untouched). **No seal** — survey only. **No `testing_agent`**.

## Receipts banked (state repo)

* `phase0/connectivity_receipts/20260921T133821Z_FULL_ESTATE_read_capability_sweep_owner_authorized_20260921.json` — main sweep (JUMP sizing + MySQL sweeps + NAS folded-in + OBS 1st pass + consolidated matrix + still-blocked set).
* `phase0/connectivity_receipts/20260921T134035Z_OBS_read_capability_delta_rerun_20260921.json` — OBS delta re-run after `max_keys=` SDK parameter fix (main sweep's OBS section had a `maxKeys=` typo). All 9 buckets listed successfully in this delta.

Prior receipts folded in unchanged:
* NAS S2 stack (4 receipts + state note listed in `STATE/notes/S2_NAS_SCHEMA_SURVEY_STATE_20260921.md`).
* OBS baselines: `20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json` (106-bucket inventory), `20260921T131024Z_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json`.

## JUMP box sizing (Section A · read-only)

| metric | value |
|---|---|
| `nproc` | **1 vCPU** |
| CPU model | `General Purpose Processor` (Huawei ECS-shape, kernel-reported) |
| AES-NI flag | **`aes` present** in `/proc/cpuinfo` |
| Memory (`free -m`) | `Mem: total 769 · used 401 · free 143 · shared 2 · buff/cache 353 · available 367` (MiB), Swap 0 |
| Uptime | `21:37:35 up 8 days, 6:13, 2 users, load avg 0.18 / 0.07 / 0.02` |

**Sizing verdict**: JUMP is a 1-vCPU / ~770 MiB RAM instance with AES-NI, idle load. Fine for tunnelling + light per-connection auth work; **NOT** sized for co-hosting heavy compute (any pull-to-JUMP ingestion path would immediately swap-thrash — Swap=0). Recommend ingestion topology puts JUMP as a tunnel only, not a stage.

## Section B · MySQL sweeps (via JUMP `direct-tcpip` forward)

### B1 · USSD @ `110.238.76.159:3306` — **CONTENT-READABLE: YES**

| field | value |
|---|---|
| auth | **OK** (server `5.7.44-241200-log`) |
| SHOW DATABASES | 20 total = 3 system + 17 user schemas |
| user schemas visible | `artists_app`, `citizen_digital`, `db_jipange`, `db_skiza`, `freddy_dev`, `miniapps`, `tafaria_ecommerce`, `tafaria_shop`, `viupay_dev`, `viupay_fare`, `viupay_fare_test`, `viusasa_dev`, `viusasa_staging`, `viusasa_staging_2`, `viusasa_staging_dev`, `viutickets`, `viutickets_dev` |
| proof-of-read (SELECT … LIMIT 1) | **16/17 succeed** (per-column shape captured; NO row values printed) |
| empty schemas | `artists_app` — 0 base tables in `information_schema.TABLES` (not a permission issue) |
| permission denied | **0** |
| sheet lists 10 schemas; server shows 17 | +7 delta (sheet under-lists); no schema-visibility loss vs sheet |

**Explicit answer**: We can **authenticate, list, describe, count, and read row-shape** on every user schema on USSD. The receipt captures column names + types + per-value byte-lengths + null-status for the LIMIT-1 row of one representative table per schema — with **zero real row values** in the transcript per hygiene.

### B2 · MICROSERVICES-primary (owner-named `159.138.162.146:3306`) — **CONTENT-READABLE: NO**

| field | value |
|---|---|
| auth | **N/A — no credentials in banked sheet** |
| sheet parses | `user_len=0, pass_len=0` for this host |
| structure probe confirms | No merged-cell C/D range covers row 32 (host `159.138.162.146`). Not a loader bug — the sheet truly lacks creds here. |
| schemas listed in sheet | `analytics`, `sql_demo`, `sql_trial1`, `weego`, `citizen-digital` |
| failure layer | `NO_CREDS_IN_BANKED_SHEET` — this is one of the five still-blocked MySQL clusters (see Section F). |

### B3 · MICROSERVICES credentialed sibling @ `159.138.164.93:3306` — **CONTENT-READABLE: YES** (surveyed as adjacent context; MICROSERVICES section is not empty)

| field | value |
|---|---|
| auth | **OK** (server `8.0.28-231003` — newer than USSD's 5.7) |
| SHOW DATABASES | 6 total = 3 system + 3 user schemas |
| user schemas | `kra_reports`, `viupay`, `viutickets` |
| proof-of-read | **3/3 succeed** |
| permission denied | 0 |
| sheet lists 2 schemas (`viupay`, `viutickets`); server shows 3 | +1 delta (`kra_reports` not in sheet — noteworthy: same schema also appears in `iebc_forms` cluster per the sheet; cross-cluster naming reuse) |

## Section C · NAS (S2 answer folded in verbatim)

**Explicit answer**: **CANNOT READ TODAY — banked NAS credentials are STALE.** Full detail in `STATE/notes/S2_NAS_SCHEMA_SURVEY_STATE_20260921.md`. Historical baseline from 2026-09-14 (pre-rotation): PARTIAL, service-account-scoped, **1 of 13 shares readable** (`OFFAIRRECS` only). Even under refreshed credentials the historical scope would need an admin scope-grant for "entire NAS" to become YES.

## Section D · OBS sweep (rotated AK/SK, prefix `HPUA`, sha `8a14174c…`)

**Buckets sampled**: 9 across 4 regions.
**HeadBucket 2xx**: **9 / 9**. **ListObjects 2xx**: **9 / 9**. **Regions with successful list**: **all 4** (`af-south-1`, `tr-west-1`, `ap-southeast-3`, `ap-southeast-1`).

### D1 · Per-bucket outcomes (delta receipt)

| bucket | region | HeadBucket | ListObjects | count returned | is_truncated |
|---|---|---|---|---|---|
| `2024offairrecs` | af-south-1 | **200** | **200** | 5 | true |
| `cal-docs` | af-south-1 | **200** | **200** | 5 | true |
| `chamgei-backup` | af-south-1 | **200** | **200** | 5 | true |
| `apr252017` | tr-west-1 | **200** | **200** | 1 | false |
| `feb272017` | tr-west-1 | **200** | **200** | 5 | true |
| `librarydirectupload2` | tr-west-1 | **200** | **200** | 5 | true |
| `citizen-vod` | ap-southeast-3 | **200** | **200** | 5 | true |
| `iso-rms-storage` | ap-southeast-3 | **200** | **200** | 1 | false |
| `rms-ai` | ap-southeast-1 | **200** | **200** | 5 | true |

Total objects visible in the bucket-sample listings: **37**. Every region-correct endpoint answered cleanly.

### D2 · Proof-of-read on `rms-ai` (single smallest object in first 20)

| field | value |
|---|---|
| list step (max_keys=20) | HTTP 200, 20 objects returned |
| chosen object | `image_files/2795ba36-2730-435f-b1be-eb07a9d83c1f/0140bbfa-61ee-4d16-878b-1c56f1b953ce.png` |
| chosen size | 1159 bytes |
| chosen etag | `41c7ca932138d32d17322f398619b8ad` |
| chosen lastModified | `2026/07/21 06:38:24` |
| **GetObject result** | **HTTP 403 · errorCode `AccessDenied`** (0.51s) |

**Explicit answer to OBS**: 
- **CAN LIST** — content is listable across every region we probed.
- **CANNOT GET** — the rotated AK/SK **lacks `obs:object:GetObject` scope** (or the equivalent policy verb) at least on `rms-ai`. The 2026-09-14 T7d receipt shows the **pre-rotation** AK/SK successfully GET-ed 26B and 39B objects from `google-transcripts` (af-south-1). Between then and now, the 2026-09-16 credential rotation delivered a **least-privilege AK/SK** that omits GetObject.
- **Scope-grant ask for the RMS admin**: add `obs:object:GetObject` to the rotated AK/SK's IAM policy (either bucket-wide or per-bucket as needed). Bounds on today's probe kept the test to a single object; a broader read-scope confirmation would need an updated policy first.

## Section E · Consolidated Estate Read-Capability Matrix (verbatim)

| # | surface | auth | enumerate | proof-of-read | **content-readable** | failure layer |
|---|---|---|---|---|---|---|
| 1 | JUMP `159.138.173.250:22` | OK (paramiko, host key un-drifted) | sizing captured (nproc/free/uptime) | shell rc=0 | **YES** | — |
| 2 | MySQL USSD `110.238.76.159:3306` | OK (`5.7.44-241200-log`) | SHOW DATABASES → 17 user schemas | 16/17 SELECT-LIMIT-1 succeed (shape only) | **YES** | — (1 empty schema, 0 denials) |
| 3 | MySQL MICROSERVICES-primary `159.138.162.146:3306` | **N/A — NO CREDS IN SHEET** | — | — | **NO** | `NO_CREDS_IN_BANKED_SHEET` |
| 4 | MySQL MICROSERVICES sibling `159.138.164.93:3306` | OK (`8.0.28-231003`) | SHOW DATABASES → 3 user schemas | 3/3 SELECT-LIMIT-1 succeed | **YES** | — |
| 5 | NAS DSM `10.10.55.55:5000` + SMB 445 | REJECTED (stale creds) | not enumerable today | — | **NO today** (historically PARTIAL 1/13) | `SHEET_CRED_STALENESS_ADMIN_ASK` |
| 6 | OBS region `af-south-1` (3 buckets sampled) | OK | HeadBucket 3/3, ListObjects 3/3, 15 objects visible | GetObject not attempted here (per owner: rms-ai only) | **YES for listing** | — for listing |
| 7 | OBS region `tr-west-1` (3 buckets sampled) | OK | HeadBucket 3/3, ListObjects 3/3, 11 objects visible | GetObject not attempted here | **YES for listing** | — for listing |
| 8 | OBS region `ap-southeast-3` (2 buckets sampled) | OK | HeadBucket 2/2, ListObjects 2/2, 6 objects visible | GetObject not attempted here | **YES for listing** | — for listing |
| 9 | OBS region `ap-southeast-1` (rms-ai) | OK | HeadBucket 1/1, ListObjects 1/1, 5 objects visible in sample | GetObject on smallest → **403 AccessDenied** | **PARTIAL: LIST-yes / GET-no** | `AK_SK_MISSING_GetObject_SCOPE` |

**Aggregate**: 4 surfaces YES (JUMP + 2 MySQL + OBS-list across 4 regions), 1 surface NO-today-with-history (NAS), 1 surface NO-no-creds (MySQL primary), 1 surface PARTIAL (OBS GetObject).

## Section F · Still-blocked MySQL clusters (owner's remaining admin ask, restated verbatim)

Five MySQL hosts have **no user/password credentials in the banked sheet**. Verified by (a) loader parse and (b) value-blind sheet structure probe (no merged C/D range covers these rows). These are the remaining scope-grant asks:

| section | host | schemas listed in sheet | status |
|---|---|---|---|
| MICROSERVICES | `HOST` (placeholder — no IP) | `WEEGO` | No host resolved; ask needs full record (host + creds) |
| MICROSERVICES | `159.138.162.146` (owner-named primary) | `analytics`, `sql_demo`, `sql_trial1`, `weego`, `citizen-digital` | Creds missing in sheet |
| MICROSERVICES | `159.138.164.124` | `citizen_digital`, `db_visitors`, `Visitors_database` | Creds missing |
| MICROSERVICES | `110.238.75.83` | `citizen_digital`, `db_visitors`, `db_visitors_old`, `db_visitors_v1`, `rembesha`, `Shikisha` | Creds missing |
| MICROSERVICES | `203.123.83.144` | `citizen-pulse`, `correspondents`, `saa` | Creds missing |

**Owner ask (single line)**: Ask the RMS admin to drop read-only credentials for these 5 MySQL hosts (or confirm they are decommissioned). Once dropped in-sheet with a matching sha256 pin (SO §4.1 §F), the same `full_estate_read_capability_sweep_20260921.py` runs unmodified against them.

## Aggregate scope-grant asks for the RMS admin (single consolidated list)

1. **NAS credentials** — re-confirm current DSM/SMB user + password (banked ones fail across every protocol variant).
2. **Huawei OBS IAM** — add `obs:object:GetObject` (or the equivalent policy verb) to the rotated AK/SK's IAM role for the buckets we need to actually READ from. LIST is already granted; GET is not.
3. **MySQL** — 5 blocked hosts as tabulated in Section F.
4. **(Optional, deferred)** — separate follow-up: is `HOST` (WEEGO row) a decommissioned host? If so, remove from sheet; if not, provide IP + creds.

## Hygiene tally

* Read-only across every touch. **Zero downloads** (except: 1 OBS object attempt returned 403 before any bytes moved) / **zero writes** everywhere.
* MySQL row values **never** entered stdout, log, or receipt — only column names + types + per-value byte lengths + null status.
* OBS credential material held in memory only; loaded from banked CSV with sha pin; never printed. GetObject returned 403 → no bytes to hash.
* SMB creds passed via tmpfs authentication file, `shred -uz` after use (per prior S2 receipts).
* JUMP host key un-drifted (`W45xvjhsARJOcFj9U/bcWC3KDte30T+Amu3eCx4UrwU` — matches T3 2026-09-14).
* No `testing_agent`, no seal, no code changes. Ratchet floor 5858 unchanged. R-91 hold intact (~38h to `2026-09-23T03:23:15Z`).

## Anomalies / surprises

1. **OBS GetObject-scope regression** — the 2026-09-16 credential rotation appears to have delivered a least-privilege AK/SK relative to the pre-rotation set. The pre-rotation set could GetObject on `google-transcripts`; the rotated set cannot GetObject on `rms-ai` (403). If least-privilege was the intent, the scope needs to include GetObject on at least the buckets we're expected to read from.
2. **`kra_reports` naming reuse** — appears as an expected schema on TWO different MySQL sections in the sheet: `iebc_forms` (row 1) and MICROSERVICES sibling `159.138.164.93` (verified live). Not necessarily a bug, but worth flagging in case of future cross-cluster confusion.
3. **USSD server delta** — sheet lists 10 schemas for USSD; server shows 17 user schemas. All 17 are readable. The sheet is under-descriptive by +7 (no permission or visibility loss — just documentation drift).
4. **JUMP is a 1-vCPU / 770-MiB / no-swap box.** Ingestion topology should treat it as a bidirectional tunnel only, not a landing pad.

## Standing bounds — all unchanged

* **R-91 hold** intact (~38h remaining to `2026-09-23T03:23:15Z`; DO NOT execute early).
* **Ratchet floor 5858** unchanged (no code changes; survey-only).
* **§3.8 additive-only** discipline intact (no code touched).
* **No `testing_agent`** invoked (per standing ban).
* **S4 data-ingest slices remain gated** on separate owner GO.

— end of state note.
