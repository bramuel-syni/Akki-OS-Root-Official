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
