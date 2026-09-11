# Huawei Cloud Connectivity Drill — 2026-09-09

**Directive:** OWNER OPERATIONAL REQUEST — read-only recon of Huawei AK/SK credentials supplied by owner. Prove reach up to and including a database.
**Discipline:** No product-code changes. No commits. No push. No pytest. HOLD on build waves unbroken. SKs redacted throughout.
**Executor:** track-a agent, this session.
**Credential source:** owner-uploaded CSV, downloaded to `/app/backend/estate_keys/data_sources/huawei_credentials.csv` (0600, gitignored). CSV sha256 `8a14174c…698667`.

---

## Verdict line

**Huawei DB: REACHED — network + protocol + auth path all live on 2 of 9 known instances; blocked from data plane pending a valid DB password.**

Specifically, the container's egress IP `34.170.12.145` is:
- **Whitelisted** by the RDS security group on `RDS-INTERACTIONS` and `Weego_and_marketing-analytics` (af-south-1). Both accept a full TCP + MySQL handshake and answer authentication with MySQL error `1045 Access denied` — proof the DB engine is answering, not just the port.
- **Not whitelisted** on the other 6 public MySQL EIPs in af-south-1 (all TCP-time-out at 6s).
- **Not routable** to the 9th target (`rms-ai-pg`, PostgreSQL 16 in ap-southeast-1) — no public IP, VPC-internal only.

To move from "REACHED at auth layer" to "REACHED at data layer" on any of the two accessible instances, one thing is needed: a valid MySQL password for one of the DB users listed below.

---

## What was done, in order

**a. IAM identity** — key authenticates against `iam.ap-southeast-1.myhuaweicloud.com`. Returned:
- Domain (account) id: `3f9d29266af74046bfb637cabb995c39`
- User: `BramwelMwalo` (AK `HPUA…NS`, 20 chars; SK 40 chars, fingerprint `sha256_8=451a83c7`, never written to disk in cleartext beyond the source CSV)
- 18 enabled projects visible: `af-north-1, af-south-1, ap-southeast-1..4, cn-east-3, cn-north-1, cn-north-4, cn-south-1, cn-southwest-2, la-north-2, la-south-2, me-east-1, MOS, na-mexico-1, sa-brazil-1, tr-west-1`
- IAM policy scope inferred from downstream 403s: this key **has** RDS read, OBS read, IAM self-list. It **does not** have DWS list (403 `DWS.01010007 Policy doesn't allow dws:cluster:list`) nor DDS list (403 `DBS.280063 dds:instance:list`). Chinese-mainland regions (`cn-north-1`) return `APIGW.0802 The IAM user is forbidden in the currently selected region` — international-account restriction, not a permission gap per se.

**b. OBS storage** — `listBuckets` global call returned **106 buckets**, distributed:
- `af-south-1`: 70 buckets
- `tr-west-1`: 31 buckets
- `ap-southeast-3`: 4 buckets
- `ap-southeast-1`: 1 bucket

I did NOT list or read the contents of any bucket. Names of the first 15 (already known to owner as their own estate): `2024offairrecs, apr252017, cal-docs, caldocs, chamgei-backup, chris-test-b, citizen-classifieds, citizen-digital-cms-files, citizen-digital-cms-files-copy, citizen-vod, citizentv, database-backup-dlbms, datauploadroyalmedia.co.ke, drivesdata.royalmedia, edaily` (+91 more). Full JSON at `_scratch/probe_results.json`.

**c. RDS discovery** — 9 instances, all `ACTIVE`, across 2 regions:

| # | Name | Region | Engine | Port | Public IP | Private IP | Flavour | Created |
|---|------|--------|--------|------|-----------|------------|---------|---------|
| 1 | RDS-INTERACTIONS | af-south-1 | MySQL 8.0.28-231003 | 3306 | 159.138.162.220 | 10.10.150.3 | n1.large.2 | 2025-08-04 |
| 2 | Weego_and_marketing-analytics | af-south-1 | MySQL 8.0.28-231003 | 3306 | 159.138.162.146 | 10.10.150.54 | n1.xlarge.4 | 2024-02-12 |
| 3 | rds-shikisha | af-south-1 | MySQL 8.0 | 3306 | 203.123.83.144 | 10.10.150.82 | n1.large.2 | 2025-02-25 |
| 4 | weego-replica-d536 | af-south-1 | MySQL 8.0 | 3306 | — | 10.10.150.115 | n1.large.4.rr | 2025-05-19 |
| 5 | election-prod-db2 | af-south-1 | MySQL 5.7 | 3306 | 110.238.77.61 | 10.10.150.48 | — | — |
| 6 | visitors-database-cluster | af-south-1 | MySQL 5.7 | 3306 | 110.238.75.83 | 10.10.150.168 | — | — |
| 7 | dbms-trf-req-database-3 | af-south-1 | MySQL 5.7 | 3306 | 159.138.175.179 | 10.10.150.121 | — | — |
| 8 | citizen-digital-dev-db-cluster | af-south-1 | MySQL 5.7 | 3306 | 159.138.164.124 | 10.10.150.206 | — | — |
| 9 | rms-ai-pg | ap-southeast-1 | PostgreSQL 16 | 5432 | — | 192.168.1.30 | pg.n1.large.4.ha | 2026-07-13 |

All 9 sit in one shared VPC in af-south-1 (`de3ba6f7-d0e7-4228-8da2-19bd33a07ff2`, subnet `c7fef874-…`), except `rms-ai-pg` which is in its own VPC `35528a18-…` in ap-southeast-1.

**d. RDS API-level enumeration** — DB names and DB users pulled via `list_databases` / `list_db_users`:

| Instance | Databases | DB users |
|----------|-----------|----------|
| RDS-INTERACTIONS | `interactions` | *(none listed; root implicit)* |
| Weego_and_marketing-analytics | `analytics, sql_demo, sql_trial1, weego` | `readuser`, `weego` |
| rds-shikisha | `citizen-pulse, corporate, correspondents, saa` | `corporate`, `saa` |
| weego-replica-d536 | `analytics, sql_demo, sql_trial1, weego` | *(read-replica: 409 `DBS.280406 Operation not allowed by the DB instance type or status`)* |
| rms-ai-pg | *(PG endpoints not exposed via same SDK call; API-level enum limited)* | — |

Every MySQL instance advertises `db_user_name=root` as the default admin user. Backup policies are 7–30 day retention across the estate; audit-log endpoint (`ShowAuditlogPolicy`) was not permitted for this key.

**e. Live-connect probe (wire + protocol + auth path)** — TCP-connect + MySQL greeting parse + intentional bogus-password login attempt (to observe the auth-side response and prove the DB engine is answering, not just the port):

| Instance | Endpoint | TCP | Handshake | Auth response |
|----------|----------|-----|-----------|---------------|
| RDS-INTERACTIONS | 159.138.162.220:3306 | ✅ 251 ms | 85B, MySQL v10, banner `8.0.28-231003` | **`1045 Access denied for user 'rms_probe_readonly'@'34.170.12.145' (using password: YES)`** — engine live, auth-gated |
| Weego_and_marketing-analytics | 159.138.162.146:3306 | ✅ 266 ms | 85B, MySQL v10, banner `8.0.28-231003` | **`1045 Access denied`** — engine live, auth-gated |
| rds-shikisha | 203.123.83.144:3306 | ❌ 6s timeout | — | SG whitelist blocks 34.170.12.145 |
| election-prod-db2 | 110.238.77.61:3306 | ❌ 6s timeout | — | SG whitelist blocks 34.170.12.145 |
| visitors-database-cluster | 110.238.75.83:3306 | ❌ 6s timeout | — | SG whitelist blocks 34.170.12.145 |
| dbms-trf-req-database-3 | 159.138.175.179:3306 | ❌ 6s timeout | — | SG whitelist blocks 34.170.12.145 |
| citizen-digital-dev-db-cluster | 159.138.164.124:3306 | ❌ 6s timeout | — | SG whitelist blocks 34.170.12.145 |
| weego-replica-d536 | 10.10.150.115:3306 | ❌ 6s timeout | — | Private-only; requires VPC ingress |
| rms-ai-pg | 192.168.1.30:5432 | ❌ 6s timeout | — | Private-only; requires VPC ingress |

The bogus-user login was a deliberate honest-signal probe: the MySQL server's response of `1045` is only issued *after* it has parsed the client handshake, resolved the user, and evaluated the password — meaning the entire DB engine is answering, not merely a firewall or LB. The user string in the error (`'rms_probe_readonly'@'34.170.12.145'`) is the DB's own report of who tried, from what IP.

---

## Progress made

- Went from "AK/SK on paper" to "domain id + 18-project inventory + 106 OBS buckets + 9 RDS instances with engine, endpoint, DB names, DB users" in roughly 2.5 minutes of API calls.
- Proved two MySQL RDS instances answer at the DB engine layer to this container's egress IP.
- Mapped the exact security-group posture: 2 SGs open to our egress, 4 not. The two open ones share security-group `2cc0ad09-8d8f-464d-9d39-4fe1f3052b57`; the closed ones use different SGs.

## How much to go

- **Zero** additional discovery needed to answer "can this key reach a database?" — done.
- **One** owner input to move from "reach" to "data" — a working DB password for a real user.

## Decisions taken (silent, per doctrine)

- Did NOT attempt to modify any RDS security-group whitelist, even though the API scope may permit it — write ops are out of scope for a read-only drill.
- Did NOT list contents of any OBS bucket. The buckets appear to include names like `database-backup-*` and `chamgei-backup` which could plausibly contain a DB dump with credentials embedded — I deliberately did not open them.
- Did NOT retry Chinese-mainland regions after the first `APIGW.0802` (international-account-restriction is a hard signal, not a permission bug).
- Redacted the SK from every artefact. Only fingerprint (`sha256_8=451a83c7`) and length (`40`) are written anywhere.

## Discoveries worth naming

1. **The key is powerful.** It is not a scoped-down service key — it holds Domain-scope RDS read across 16 non-mainland regions and IAM self-inspection. Anyone with this AK/SK can inventory every RDS instance the account owns, read backup schedules, and list DB users. It cannot list DWS or DDS by policy.
2. **Two production databases are publicly exposed** with a permissive-enough security-group to accept traffic from an anonymous GCP-block egress IP (this container). Those are `RDS-INTERACTIONS` and `Weego_and_marketing-analytics`. That is a posture the owner may or may not intend — flagging it, not fixing it.
3. **VPC design is split**: 8 of 9 RDS instances live in a single af-south-1 VPC/subnet, and `rms-ai-pg` sits alone in ap-southeast-1. Any cross-DB tooling that touches both regions needs peering or a jumphost story.
4. **Read-replica flag surfaces cleanly**: `weego-replica-d536` returns `DBS.280406 Operation not allowed by the DB instance type or status` on user-list — Huawei is refusing user enumeration on the replica, which is the correct answer.
5. **106 OBS buckets** is a very large estate footprint for this key. Storage reach is not limited to a project — the AK/SK sees the account's global bucket list in one call.

## Recommendations, inline with mission

The mission was DB reach. The wire is proven. To close the last mile the owner needs to pick **one** path:

- **Path A (fastest, cleanest, no infra change): supply a DB password.** Provide a username + password for either `RDS-INTERACTIONS` (root or a purpose-built read-only user on the `interactions` schema) or `Weego_and_marketing-analytics` (existing users `readuser` or `weego` are the obvious candidates). Egress IP `34.170.12.145` is already whitelisted on both. Handoff form: a `.env` line — do not paste it inline; drop it in the same `/app/backend/estate_keys/data_sources/` folder that already holds the AK/SK.

- **Path B (opens up the other 6 MySQL instances): widen the security-group whitelist.** Any of the 6 currently-blocked instances (`rds-shikisha`, `election-prod-db2`, `visitors-database-cluster`, `dbms-trf-req-database-3`, `citizen-digital-dev-db-cluster`, and — if the intent is replica access — `weego-replica-d536`) can be reached by adding `34.170.12.145/32` to their security-group inbound-rule on port 3306. The security-group IDs are captured in the RDS deep-inventory JSON. Owner sign-off would be needed since this is a live-estate write op.

- **Path C (for `rms-ai-pg` and the two private-only IPs): VPC ingress.** Either a bastion in VPC `35528a18-…` (ap-southeast-1) or `de3ba6f7-…` (af-south-1), or a Huawei Cloud VPN. Not something to do in-band from a drill.

## Precise MISSING list (so nothing is fudged)

| Blocker | For which target | What is missing |
|---------|------------------|-----------------|
| DB password | `RDS-INTERACTIONS` (159.138.162.220:3306, MySQL 8.0, db `interactions`) | Any DB user + password (root or purpose-built). Network already open to us. |
| DB password | `Weego_and_marketing-analytics` (159.138.162.146:3306, MySQL 8.0, dbs `analytics/sql_demo/sql_trial1/weego`) | Password for `readuser` or `weego` (or root). Network already open to us. |
| Security-group inbound rule | 6 other MySQL EIPs listed above | Add `34.170.12.145/32` on TCP/3306 |
| VPC ingress path | `weego-replica-d536`, `rms-ai-pg` | Bastion/VPN into VPC `de3ba6f7…` (af-south-1) and `35528a18…` (ap-southeast-1) |
| IAM policy grant | DWS list, DDS list, IAM audit-log | These 403 today; not needed for DB reach but worth noting |
| Chinese-mainland region access | any `cn-*` regions | `APIGW.0802` international-account-restriction; a domestic account would be required |

---

## Artefacts (uncommitted, local only)

- `/app/assessment_workspace/tools/huawei_probe.py` — IAM/OBS/RDS/DWS/DDS discovery
- `/app/assessment_workspace/tools/huawei_db_reach.py` — TCP + protocol + auth-path probe
- `/app/assessment_workspace/tools/huawei_rds_deep.py` — per-instance DB name / user / backup enum
- `/app/assessment_workspace/tools/_scratch/probe_results.json` — full discovery JSON
- `/app/assessment_workspace/tools/_scratch/dbreach_results.json` — reach probe JSON
- `/app/assessment_workspace/tools/_scratch/rds_deep.json` — RDS deep-inventory JSON
- `/app/backend/estate_keys/data_sources/huawei_credentials.csv` — the source CSV, 0600, gitignored, sha256 `8a14174c…698667`

## Guardrail attestation

- No product code touched. `programme/track-a` branch untouched. `master` workspace branch untouched by this drill.
- Ratchet floor unchanged at **3098** — no pytest invoked.
- HOLD respected — no build wave started, no CP10 commit.
- No commits made in this session by the drill. No push executed. `.gitignore` updated to ensure the credential file cannot be added by future `git add .` in either repo.
- SK never echoed. Only sha256-fingerprint (`sha256_8=451a83c7`) and length (`40`) written.
- All discovery is read-only. No RDS/OBS/IAM write ops executed.

---

# PART 2 — Path A: Live SQL Reach (2026-09-09, +45min)

**Directive:** OWNER OPERATIONAL REQUEST — Path A chosen. Owner supplied DB credentials in a second CSV. Attempt real SQL and prove data-layer reach.
**Credential source:** owner-uploaded CSV, downloaded to `/app/backend/estate_keys/data_sources/db_credentials.csv` (0600, gitignored). CSV sha256 `d8a7f0e2…0cf22`. Not committed on either repo; verified absent from `git status` on both.

## Verdict line

**Huawei DB live SQL: CONNECTED to `110.238.76.159` (MySQL 5.7.44) as `bramuel@%`; read access to 17 non-system databases proven with row counts and a live sample query.**

Failure honesty: 2 of the 3 hosts in the CSV are TCP-blocked from our egress IP (`203.123.86.10` and `159.138.164.93` both hard-timeout at 8s). Those three hosts do not appear in the previous 9-instance RDS inventory — they are different EIPs, so this credential set targets a different set of instances than the ones the AK/SK had listed. That is a data point, not a failure.

## Pre-flight disclosure to owner

- The password field in the CSV printed to my terminal transcript during parse (the header-row detection was mis-scoped in my first script — the "VIUSASA" section-banner was treated as the header, so the redaction key never matched). The persisted artefacts are cleanly redacted (only `pw_fp=sha256_8=<8chars>` and `len=16` are written). If the owner considers session-transcript visibility as leakage, this password should be rotated. Fingerprint: `sha256_8=5b9ec5c0` (computed below).

## Credentials structure (redacted)

CSV lists **3 host+user+password rows** across 3 section-banners; other rows in each banner name additional databases without host/user/password columns — those DB names are the extended list of schemas served by the same section's host.

| Section banner | DB name | Host (EIP) | User | Password |
|---|---|---|---|---|
| VIUSASA | iebc_forms | 203.123.86.10 | bramuel | `<REDACTED fp=sha256_8=5b9ec5c0 len=16>` |
| USSD | artists_app | 110.238.76.159 | bramuel | `<REDACTED fp=sha256_8=5b9ec5c0 len=16>` |
| MICROSERVICES | viupay | 159.138.164.93 | bramuel | `<REDACTED fp=sha256_8=5b9ec5c0 len=16>` |

All three share the same password (same fingerprint), differ only by host. Same DB user (`bramuel`).

## Reach results per host

| # | Host | Result | Notes |
|---|------|--------|-------|
| 1 | 203.123.86.10:3306 | **NOT CONNECTED** — `2003 Can't connect to MySQL server ... (timed out)` at 8s | TCP-block from `34.170.12.145`; not the same instance as `rds-shikisha` (203.123.83.144) |
| 2 | 110.238.76.159:3306 | **CONNECTED** — MySQL 5.7.44-241200-log | `bramuel@%` grants — connects from any IP |
| 3 | 159.138.164.93:3306 | **NOT CONNECTED** — `2003 Can't connect to MySQL server ... (timed out)` | TCP-block from `34.170.12.145` |

## Live SQL evidence on 110.238.76.159 (redacted)

Commands issued via `pymysql`, connect_timeout=8s, read-only. Server responses verbatim (password never sent to stdout):

```
mysql> SELECT 1;
+---+
| 1 |
+---+
| 1 |

mysql> SELECT VERSION();
+---------------------+
| VERSION()           |
+---------------------+
| 5.7.44-241200-log   |

mysql> SELECT CURRENT_USER(), USER(), @@hostname, @@version_comment;
+----------------+----------------------------+-----------------------+--------------------------------+
| CURRENT_USER() | USER()                     | @@hostname            | @@version_comment              |
+----------------+----------------------------+-----------------------+--------------------------------+
| bramuel@%      | bramuel@34.170.12.145      | localhost.localdomain | MySQL Community Server - (GPL) |
```

Two facts to name from that: (i) `bramuel@%` — the grant is host-wildcard, this DB user is authorised from any IP, not just Huawei internal or a specific bastion; (ii) `@@hostname localhost.localdomain` — the RDS runtime doesn't reveal the instance hostname; consistent with Huawei RDS's default masking.

## Schema summary (20 databases visible, 17 non-system)

| Database | Tables | Notable row counts (first 5 tables per DB) |
|----------|-------:|--------------------------------------------|
| information_schema | 74 | *(system)* |
| mysql | *(not shown)* | *(not queried)* |
| performance_schema | 88 | *(system)* |
| sys | 102 | *(system)* |
| **artists_app** | 0 | *(schema exists but empty — the CSV's "target" for this section)* |
| **citizen_digital** | 39 | article_article_category=**6,973**, article_categories=7, articles=**6,824**, audits=**1,009**, bans=0 |
| **db_jipange** | 22 | age_range=6, ci_sessions=97, counties=47, documents=0, entry_count=1 |
| **db_skiza** | 24 | age_range=6, ci_sessions=**170,616**, counties=47, documents=1, entry_count=1 |
| **freddy_dev** | 38 | audits=9, categories=12, comments=802, failed_jobs=0, iveris=2 |
| **miniapps** | 21 | DATABASECHANGELOG=40, callback=15, category=2 |
| **tafaria_ecommerce** | 130 | access_types=5, active_users=1, addresses=0, airtel_c2bs=0 |
| **tafaria_shop** | 117 | admins=1, attribute_families=1, attribute_group_mappings=27 |
| **viupay_dev** | 37 | cache=21, failed_jobs=95, gateway_configs=22, gateways=100 |
| **viupay_fare** | 42 | agent_api_logs=**696,796**, tbl_channelmaster=16 |
| **viupay_fare_test** | 41 | agent_api_logs=**696,796**, tbl_channelmaster=16 |
| **viusasa_dev** | 132 | active_users=**24,028**, addresses=0, airtel_c2bs=0 |
| **viusasa_staging** | 162 | access_types=7, active_users=1, airtel_c2bs=28 |
| **viusasa_staging_2** | 138 | access_types=5, active_users=1, addresses=1, airtel_c2bs=28 |
| **viusasa_staging_dev** | 151 | all counts=0 |
| **viutickets** | 56 | affiliates=25, audits=**128,791**, book_events=15, booked_concessions=16 |
| **viutickets_dev** | 44 | affiliates=1, audits=328, book_events=2 |

## Representative row-level proof (redacted)

Chose a low-sensitivity join table so I could show real rows without exposing PII:

```
mysql> USE citizen_digital;
mysql> SELECT * FROM article_article_category LIMIT 3;
+----+------------+----------------------+
| id | article_id | article_category_id  |
+----+------------+----------------------+
| 1  | 1          | 1                    |
| 2  | 2          | 1                    |
| 3  | 2          | 2                    |
```

Real integer join rows from a 6,973-row table. Proves the connection is not just at handshake — it's returning real data from the production `citizen_digital` schema.

I deliberately did **not** open any of the obviously PII-bearing tables (`active_users`, `bookings`, `agent_api_logs`, `audits`, `airtel_c2bs`, `airtel_money_*`, etc.) — those are named for owner situational awareness only, and their row counts prove they contain data, without me having to touch the data itself.

## Discoveries worth naming

1. **The credential is broad, not scoped.** `bramuel@%` gives read to 17 databases spanning ~1,200 tables. Notable production-scale tables: `citizen_digital.articles` (6,824 rows), `viupay_fare.agent_api_logs` (696,796 rows), `db_skiza.ci_sessions` (170,616 rows), `viutickets.audits` (128,791 rows), `viusasa_dev.active_users` (24,028 rows). This is a shared DB-admin credential, not a narrow app-role credential.
2. **`viupay_fare` and `viupay_fare_test` are identical shape and row count** (both `agent_api_logs=696,796`, both `tbl_channelmaster=16`). Either the "_test" schema is a mirror snapshot or they've drifted from a shared source. Worth an internal check.
3. **The CSV's "target" DB per section (`artists_app`) is empty** on this host. The actual live data is in the other 16 non-system schemas the same user can see. The CSV's per-section grouping (VIUSASA / USSD / MICROSERVICES) doesn't cleanly map to the schemas visible on the one reachable host — this suggests each section-banner in the CSV corresponds to one host, and the schemas listed under it are meant to live on that host. Only the USSD host (110.238.76.159) was reachable, and its schema set includes everything the CSV lists under USSD (artists_app, citizen_digital, db_jipange, db_skiza, freddy_dev, miniapps, tafaria_ecommerce, tafaria_shop, viupay_dev, viupay_fare, viutickets_dev) plus more.
4. **`bramuel@%` = host wildcard.** Any client on the internet that possesses this credential can connect. The Huawei RDS security-group is what actually gates ingress here — and it's open to `34.170.12.145` on this instance. Two independent locks were both permissive on this host: the SG allows the IP and the DB user allows any host.
5. **Two hosts in the CSV are TCP-blocked from our egress** — same failure mode as 6 instances in the earlier drill. Consistent with the pattern that only a subset of the RDS estate has our egress in its SG whitelist.

## Precise MISSING list (this half)

| Blocker | For which target | What is missing |
|---------|------------------|-----------------|
| SG inbound rule | 203.123.86.10 (VIUSASA section, dbs iebc_forms, kra_reports, miniapps, viupay, viupay_agent_staging, viusasa_artists, viusasa_miniapps_prod, viusasa_staging, viutickets) | Add `34.170.12.145/32` on TCP/3306 to that instance's SG |
| SG inbound rule | 159.138.164.93 (MICROSERVICES section, db viupay) | Add `34.170.12.145/32` on TCP/3306 |
| Nothing | 110.238.76.159 | Already reachable; live |

## Guardrail attestation (Part 2)

- No product code touched. `programme/track-a` branch untouched. `master` workspace branch untouched.
- Ratchet floor unchanged at **3098** — no pytest invoked.
- HOLD respected — no build wave, no CP10 commit.
- No commits made. No push. Both credential CSVs remain outside `git status` on both repos (verified). `.gitignore` covers `backend/estate_keys/data_sources/`.
- Password never written to disk in cleartext beyond the source CSV. Only fingerprint (`sha256_8=5b9ec5c0`) and length (`16`) are in this report and in `_scratch/live_sql_*.json`.
- Only read-only SQL executed: `SELECT`, `SHOW`, `USE`. No `INSERT / UPDATE / DELETE / CREATE / DROP / ALTER / GRANT`. Verified in scripts.

## Artefacts (uncommitted, local only)

- `/app/assessment_workspace/tools/huawei_live_sql.py` — 3-host CSV probe
- `/app/assessment_workspace/tools/huawei_live_sql_enum.py` — 20-DB enumerator on the reachable host
- `/app/assessment_workspace/tools/_scratch/live_sql_results.json` — probe results
- `/app/assessment_workspace/tools/_scratch/live_sql_enum.json` — schema + row-count map
- `/app/backend/estate_keys/data_sources/db_credentials.csv` — source CSV, 0600, gitignored, sha256 `d8a7f0e2…0cf22`


---

# PART 3 — Cost of running mtafiti / extraction against the Huawei estate

**Directive:** OWNER OPERATIONAL REQUEST — "Are we going to be charged to run mtafiti on this estate?" Grounded answer from actual estate config, not generic pricing.

## Verdict line

**Running mtafiti/extraction costs: ~$2–$4 (rough band) for a full one-shot pull of the currently reachable host, driven entirely by outbound EIP traffic (traffic-billed at $/GB, not per-query), charged to the Huawei account that OWNS THE EIP — for the 7 EIPs we can see in `af-south-1`, that is domain `3f9d29266af74046bfb637cabb995c39` (BramwelMwalo). For the reachable host `110.238.76.159` itself, the EIP is NOT visible to this AK/SK — likely a different Huawei tenant, which means someone else's account bears the cost of that specific extraction.**

Nothing is charged to our pod/account. Queries themselves are free. What is metered is the return-path bytes leaving the RDS's EIP.

## Part A — "mtafiti" terminology (in-repo confirmation)

Yes, `mtafiti` is a first-class named engine in the codebase and canon. Findings (case-insensitive grep, both repos + canon):

**In `Extraction-Akki` (tracked source):**
- `backend/services/mtafiti/` — 9 modules: `census.py, declaration.py, feasibility.py, floor_feasibility.py, inference.py, measure.py, registry.py, source_standing.py, v3_overlay.py, verdict.py`
- `backend/contracts/mtafiti_registry.py` (Pydantic frozen contract)
- `backend/routers/mtafiti.py`
- `backend/tests/invariants/test_mtafiti_invariants.py` (16 tests exercised per `REUSE_ASSESSMENT.md:108`)
- `docs/mandates/RMS_Mtafiti_Specification.md` + `docs/mandates/source/RMS_Mtafiti_Specification.docx`
- `docs/audits/g4_mtafiti_conformance_v1.md` — "17 MATCH / 2 SPEC_EXPANSION / 0 MATERIAL_GAP" (`BUILD_JOURNAL.md:1128`)

**In canon (workspace):**
- `notes/canon_4_requirements.md` §5–§10 defines Mtafiti as **the Measurement engine**:
  - C4-003 §5 Charter: "Mtafiti measures WHAT THE ESTATE ACTUALLY CONTAINS, at whatever scale (whole org, department, archive, single file — Doc 1 §1.1)"
  - C4-004 §5 Objective-blind: "Measures the ESTATE, never the ANSWER"
  - C4-010 §8 Census records: "Mtafiti writes census/registry records"
  - C4-011 §9 Composition: "by language, era, source, condition, evidence class"
  - C4-013 §10 Repeatable
- Also called "The Registry" per `canon/drops/20260907/extracted/text/doc0_governance_architecture.txt:235` ("Mtafiti (the Registry)")
- 22 canon rules in `System_Rules_Registry.json` mapped to Mtafiti as the owning engine.

**In owner's language:** "running mtafiti on this estate" = executing our objective-blind census/measurement workload against the Huawei RDS databases — a bulk read for schema + row counts + data profiling to populate the registry. That is exactly the shape of what we just did in the connectivity drill, at greater volume.

## Part B — Actual billing config (from `list_instances`, `list_publicips`, `list_bandwidths`)

### B.1 RDS instance charging_mode (already-billed vs metered)

Per Huawei RDS API `charge_info.charge_mode`:

| Instance | Region | Engine | Flavour | `charge_mode` |
|----------|--------|--------|---------|:-------------:|
| RDS-INTERACTIONS | af-south-1 | MySQL 8.0 | rds.mysql.n1.large.2 | **postPaid** |
| weego-replica-d536 | af-south-1 | MySQL 8.0 | rds.mysql.n1.large.4.rr | **postPaid** |
| rds-shikisha | af-south-1 | MySQL 8.0 | rds.mysql.n1.large.2 | **postPaid** |
| Weego_and_marketing-analytics | af-south-1 | MySQL 8.0 | rds.mysql.n1.xlarge.4 | **postPaid** |
| election-prod-db2 | af-south-1 | MySQL 5.7 | rds.mysql.x1.large.2 | **postPaid** |
| visitors-database-cluster | af-south-1 | MySQL 5.7 | rds.mysql.n1.xlarge.2 | **postPaid** |
| dbms-trf-req-database-3 | af-south-1 | MySQL 5.7 | rds.mysql.x1.large.2 | **postPaid** |
| citizen-digital-dev-db-cluster | af-south-1 | MySQL 5.7 | rds.mysql.x1.large.2 | **postPaid** |
| rms-ai-pg | ap-southeast-1 | PostgreSQL 16 | rds.pg.n1.large.4.ha | **prePaid** |

Reading: `postPaid` = pay-per-use, billed hourly by CPU/RAM/storage class regardless of query load; `prePaid` = the monthly/yearly commitment has already been paid up-front, no metered charge at all until the term rolls over. **Query load itself does NOT change the RDS bill** on either mode — there is no per-query, per-CPU-second, or per-row-read charge line in the Huawei RDS pricing model. The instance-hour price bought you the compute; using it more is free.

### B.2 EIP bandwidth billing (this is the metered driver)

Per `list_publicips` + `list_bandwidths` in `af-south-1` (matched to our 7 visible RDS EIPs):

| Public IP | Bound to | `bandwidth_size` | `share_type` | **`charge_mode`** |
|-----------|----------|:----------------:|:------------:|:-----------------:|
| 159.138.162.220 | RDS-INTERACTIONS | 300 Mbps | PER (dedicated) | **traffic** |
| 159.138.162.146 | Weego_and_marketing-analytics | 300 Mbps | PER | **traffic** |
| 203.123.83.144 | rds-shikisha | 300 Mbps | PER | **traffic** |
| 110.238.75.83 | visitors-database-cluster | 300 Mbps | PER | **traffic** |
| 110.238.77.61 | election-prod-db2 | 20 Mbps | PER | **traffic** |
| 159.138.175.179 | dbms-trf-req-database-3 | 20 Mbps | PER | **traffic** |
| 159.138.164.124 | citizen-digital-dev-db-cluster | 20 Mbps | PER | **traffic** |

**All 7 visible EIPs are `charge_mode=traffic`** — pay-per-GB egress. The `bandwidth_size` field is a bandwidth cap (throttling ceiling), not a billing floor. In `traffic` mode, you are billed by the volume of outbound bytes leaving the EIP; the Mbps figure only limits peak rate, it does not commit you to a monthly bandwidth block.

Reading: on `charge_mode=traffic`, downloading 1 GB out costs `1 × rate_per_GB_af-south-1`. Huawei public rate card for `af-south-1` (Johannesburg) EIP outbound traffic is in the **$0.08–$0.13 / GB** band (I have not confirmed the exact tier at this exact moment; owner should sanity-check against the invoice). No fixed monthly bandwidth commitment shielding this — every GB is metered.

`ap-southeast-1` publicip count was 4 in that project — none matched our targets (the only ap-southeast-1 instance `rms-ai-pg` has no public IP anyway; internal-only).

### B.3 The reachable host is in a **different tenant** than the AK/SK owner

Important honesty flag: `list_publicips` in `af-south-1` returned 71 EIPs but the reachable-live host `110.238.76.159` **is not among them**. Same for `203.123.86.10` and `159.138.164.93` from the DB creds CSV — none appear in this AK/SK's EIP visibility. That means:

- The RDS instance behind `110.238.76.159` is not one of the 9 the AK/SK could list.
- Its EIP lives under a different Huawei domain / project that the AK/SK is not authorised to inspect.
- We can still read the DATA (the DB credential worked; SG accepts our egress; the DB grants `bramuel@%`), but we cannot confirm its `charge_mode` from this AK/SK.
- Reasonable inference (same operator estate, same egress-pricing region): `traffic`-billed with a `bandwidth_size` cap. Not a fact — an inference. Owner can confirm from the Huawei billing console.

### B.4 Cross-region egress? No, this is single-hop internet egress

Our pod (`34.170.12.145`, GCP block) reaches the RDS EIP over public internet directly. Huawei doesn't distinguish "cross-region" for EIP outbound traffic — the EIP bills its own traffic in its own region regardless of destination. No secondary hop bills stack up on top of it.

### B.5 Data volume — how many GB is a full mtafiti pull

From `information_schema.TABLES.data_length + index_length` on the reachable host (`110.238.76.159`):

| Database | Tables | data (MB) | index (MB) | total | GB |
|----------|-------:|----------:|-----------:|------:|---:|
| db_jipange | 22 | 5,555.7 | 7,019.3 | 12,575.0 MB | **12.28** |
| db_skiza | 24 | 5,252.3 | 2,786.9 | 8,039.2 MB | **7.85** |
| viupay_fare | 42 | 998.1 | 618.7 | 1,616.8 MB | **1.58** |
| viupay_fare_test | 41 | 925.3 | 611.3 | 1,536.6 MB | **1.50** |
| viusasa_staging | 162 | 405.0 | 80.8 | 485.8 MB | 0.47 |
| viutickets | 56 | 215.7 | 60.1 | 275.7 MB | 0.27 |
| citizen_digital | 39 | 47.2 | 2.9 | 50.1 MB | 0.05 |
| viusasa_dev | 132 | 13.0 | 9.5 | 22.6 MB | 0.02 |
| viusasa_staging_2 | 138 | 14.6 | 4.4 | 19.0 MB | 0.02 |
| viusasa_staging_dev | 151 | 2.3 | 4.6 | 7.0 MB | 0.007 |
| tafaria_ecommerce | 130 | 2.0 | 3.9 | 6.0 MB | 0.006 |
| tafaria_shop | 117 | 2.1 | 2.6 | 4.7 MB | 0.005 |
| viupay_dev | 37 | 2.8 | 0.9 | 3.7 MB | 0.004 |
| freddy_dev | 38 | 1.6 | 1.4 | 3.0 MB | 0.003 |
| viutickets_dev | 44 | 1.8 | 1.0 | 2.7 MB | 0.003 |
| miniapps | 21 | 1.8 | 0.6 | 2.4 MB | 0.002 |
| **TOTAL** | **1,193** | **13,441.4** | **11,208.9** | **24,650.3 MB** | **~24.07 GB** |

Approximate row count across the 16 non-system schemas: **~179 M rows** (from `information_schema.TABLES.table_rows`, which is an estimator, not authoritative — actual could be 10–30% off in either direction).

Mtafiti's real payload will be smaller than 24 GB because:
- Indexes (11 GB, 45% of the estate) do not transit — census reads scan tables, not index blocks over the wire.
- Mtafiti-Spec measures + composes but does not necessarily pull every row of every table — it can sample stratified rows and count via `COUNT(*)`, `MIN/MAX`, and metadata queries. That's the whole point of "objective-blind census, not full replication".
- A full replicate-everything worst-case is bounded by `~13.4 GB` of actual data pages (`data_length` only).

### B.6 Rough cost band

Using the Huawei af-south-1 EIP `charge_mode=traffic` public rate band of ~$0.08–$0.13/GB:

| Scenario | Egress bytes | Approx cost (owner's account) |
|----------|:------------:|:-----------------------------:|
| Mtafiti census-only (metadata + `COUNT(*)` + stratified samples, ≈ 1–3% of data) | 0.1–0.4 GB | **< $0.05** |
| Realistic mtafiti scan (sample rows, first N per table, key-column projections, ≈ 10–20%) | 1.3–2.7 GB | **~$0.10–$0.35** |
| Full one-shot pull of `data_length` (all rows all tables all columns, uncompressed wire) | ~13.4 GB | **~$1.07–$1.74** |
| Full pull of data + indexes | ~24 GB | **~$1.93–$3.13** |

Rough band therefore: **cents to a few dollars** for the currently reachable host, one-time. Multiply by however-often the census runs and by whichever hosts we open next.

If we later open the other 6 af-south-1 RDS instances (or the 2 blocked hosts from the DB creds CSV), you can scale by their `data_length` — but note that some of those (`election-prod-db2`, `visitors-database-cluster`, `dbms-trf-req-database-3`, `citizen-digital-dev-db-cluster`) have **20 Mbps EIP caps** which will act as a soft throttle on how fast a pull can complete (20 Mbps = ~2.4 MB/s = ~8.6 GB/hour max), not a cost multiplier.

## Answers to the four owner-questions, plainly

1. **Does running queries cost extra?** No. RDS `charge_mode` is `postPaid` on 8 of 9 instances (already billed hourly by the owner regardless of our SELECTs) and `prePaid` on `rms-ai-pg` (already paid for a term). Neither mode meters per-query. SQL execution against the instance is a zero-marginal-cost activity on the RDS side.
2. **What IS the metered driver?** Outbound EIP traffic. All 7 visible EIPs are `charge_mode=traffic`, meaning every byte that leaves the RDS's public IP toward our pod is billed on a $/GB basis. Not covered under a bandwidth-commit — every GB counts.
3. **Order-of-magnitude for full extraction?** The one reachable host holds ~13 GB of data (~24 GB with indexes) across 16 schemas / ~179 M rows. A full worst-case pull is roughly **$1–$3** in EIP egress on that host at Huawei af-south-1 rates. Mtafiti's actual pattern (objective-blind census with sampling, metadata, and stratified counts) will be an order of magnitude smaller — cents.
4. **Whose account bears it?** For the 7 EIPs bound to the RDS instances the AK/SK can see, all live in domain `3f9d29266af74046bfb637cabb995c39` (BramwelMwalo / owner). Huawei bills EIP traffic to the account that owns the EIP, not the receiver — so **the owner's Huawei account, not ours**. For `110.238.76.159` (the actual reachable-live host from Part 2), the EIP is invisible to this AK/SK, which strongly suggests a different Huawei tenant/domain — whoever owns THAT account bears the cost of pulling from THAT host. Owner should verify from the console which of their linked accounts covers it.

## Guardrail attestation (Part 3)

- No product code touched. `programme/track-a` untouched. `master` workspace untouched.
- Ratchet floor **3098** unchanged. No pytest invoked. No testing_agent invoked.
- HOLD respected — no build wave, no CP10 commit.
- No commits. No push. Credential CSVs remain outside `git status` on both repos (verified).
- Only read-only APIs called: `rds.list_instances`, `eip.list_publicips`, `eip.list_bandwidths`, `information_schema.TABLES` SELECT. No writes to any DB, no changes to any SG or EIP.
- Password never written cleartext beyond source CSV.

## Additional artefacts (uncommitted, local only)

- `/app/assessment_workspace/tools/huawei_billing_probe.py`
- `/app/assessment_workspace/tools/_scratch/billing_probe.json`
- `/app/assessment_workspace/tools/_scratch/billing_stdout.log`

