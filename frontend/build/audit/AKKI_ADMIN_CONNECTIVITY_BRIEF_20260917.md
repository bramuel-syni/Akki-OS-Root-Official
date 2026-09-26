# AKKI ADMIN CONNECTIVITY BRIEF — 2026-09-17

> **Audience.** Estate & network administrator (`BramwelMwalo`, Huawei domain `hid_mroq3ef3gos5pjp` / `3f9d29266af74046bfb637cabb995c39`) and anyone with owner-console rights on that account.
> **Purpose.** A concrete, actionable inventory of what credentials have been received, how they were used, what is currently reachable, what is not, and the exact administrative changes required to fully connect.
> **Ground rule.** Every fact carries a label — **[VERIFIED]** (checked on disk / git this session) or **[BANKED / UNVERIFIED]** (cited from a banked note without re-firing the probe this turn). Credentials are referenced by filename / location / purpose only. **No secret values appear in this brief.** SHA256 fingerprints and byte-lengths are shape metadata and are safe to publish.

Report generated: 2026-09-17 · Author: E1 (session assistant) · Anchor: `STATE/STANDING_ORDERS.md`.

---

## Table of contents

1. Credentials received
2. How each credential was used
3. What is connected and visible (working today)
4. What is not connected — blockers per source
5. **Clear ask — what the admin must do to fully connect**
6. Once-done verification plan

---

## 1 · Credentials received

All custody files are stored at `/app/backend/estate_keys/data_sources/` at mode `0600`, owner `root:root`, git-ignored on both repos. **No raw value is echoed anywhere.** SHA256 pins are content addresses of raw bytes and leak no field content by construction.

**Provenance:** `notes/CREDENTIAL_DROP_BIND_DELTA_20260916.md` §1 · **[VERIFIED]**. Manifest banked at `phase0/credential_drop_manifests/20260916T1910Z_drop_manifest.json` (177 lines).

| # | File name | Type | Purpose | Issued by | Received | Size (B) | Mode | Class | Label |
|--:|---|---|---|---|---|--:|---|---|---|
| 1 | `huawei_credentials.csv` | Huawei Cloud IAM AK/SK CSV | Huawei OBS / RDS discovery via SDK (`obs.af-south-1.myhuaweicloud.com`) | Owner (via admin console) | 2026-09-11T18:27:26Z | 119 | 0600 | Cloud AK/SK (AK len 20 · SK len 40) | VERIFIED |
| 2 | `admin_bind_20260915_bramuel_cd_visitors.json` | Shared DB credential (CD + Visitors) | MySQL read from JUMP for `citizen_digital` (`159.138.164.103:3306`) and `visitors` (`110.238.75.83:3306`) | Admin (`bramuel`) 2026-09-15T~04:25Z | 2026-09-15T07:03:22Z | 1 321 | 0600 | DB password (len 12 · alphanumeric mixed case) | VERIFIED |
| 3 | `db_credentials.csv` | VIUSASA-section DB credentials CSV | Cross-tenant MySQL logins (`bramuel@%`) — 3 hosts, same password fingerprint | Owner (initial drop, 2026-09-09 drill) | 2026-09-11T19:19:44Z | 539 | 0600 | DB password (len 16, shared across 3 hosts) | VERIFIED |
| 4 | `db_credentials_2.csv` | WEEGO-section host+db map (no creds) | Application-to-host mapping only (no user, no password) | Owner (3rd CSV drop, Part 7 of Huawei drill) | 2026-09-12T04:29:31Z | 321 | 0600 | Map file — 22 rows, 2 cols (dbname, host) | VERIFIED |
| 5 | `hf_token.csv` | HuggingFace token (pre-rotation) | Retained for forensic (`SEC-2026-09-12-01`); loader must refuse | Owner | 2026-09-13T05:21:52Z | 37 | 0600 | HF access token (`hf_`-prefix) | VERIFIED |
| 6 | `hf_token_rotated_20260914.csv` | HuggingFace token (rotated marker) | ACTIVE HF token for audio-poc gated-model pulls | Owner (rotation drop after `SEC-2026-09-12-01`) | 2026-09-14T12:24:25Z | 37 | 0600 | **Byte-identical to row 5** (see F.3 in `CREDENTIAL_DROP_BIND_DELTA_20260916.md`) | VERIFIED |
| 7 | `RMS_Connection_Creds.xlsx` | RMS network estate credentials (opaque xlsx) | Estate credentials bundle — treated as opaque bytes | Owner | 2026-09-14T11:27:24Z | 9 399 | 0600 | xlsx (opaque zip) — no prior sha pin | VERIFIED |
| 8 | `akki-aurora.json` | AWS RDS metadata | Legacy WPW campaign target (not on JUMP path) | Owner | 2026-08-18T20:12:48Z | 369 | 0600 | AWS RDS creds | VERIFIED |
| 9 | `aws_iam_user_AKIAXGH5.json` | AWS IAM user | Legacy WPW campaign | Owner | 2026-08-19T13:12:35Z | 300 | 0600 | AWS IAM user | VERIFIED |
| 10 | `db-restore-603-cluster.json` | AWS RDS Data API creds | WPW campaign restore | Owner | 2026-09-06T13:38:41Z | 418 | 0600 | AWS RDS Data API | VERIFIED |
| 11 | `synthetic-nonexistent.json` | Synthetic fixture | Fixture (invariant tests) | Session-authored | 2026-08-25T19:21:22Z | 359 | 0600 | Test fixture | VERIFIED |
| 12 | `x.json` | Legacy custody file | Legacy | Owner | 2026-08-18T20:04:39Z | 278 | 0600 | Legacy | VERIFIED |

**Row totals** (per manifest): 12 files · 1 UNCHANGED · 0 ROTATED · 11 NEW-ENTRY. **[VERIFIED — `CREDENTIAL_DROP_BIND_DELTA_20260916.md` §1 row-counts.]**

### 1.1 Credential-shape confirmations

- **Huawei AK/SK.** AK length `20`, SK length `40`, both computed via `hashlib` on raw bytes only. Domain: `hid_mroq3ef3gos5pjp` / `3f9d29266af74046bfb637cabb995c39`. User: `BramwelMwalo`. **[VERIFIED — `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json` `custody_shape` block; `HUAWEI_CONNECTIVITY_DRILL_20260909.md` §a].**
- **CD/Visitors shared password.** Length `12`, alphanumeric mixed case. **[VERIFIED — `ADMIN_BINDS_20260915.md` §A.]**
- **VIUSASA-section password.** Length `16`, shared across 3 hosts (VIUSASA/USSD/MICROSERVICES banners in `db_credentials.csv`). **[VERIFIED — `HUAWEI_CONNECTIVITY_DRILL_20260909.md` Part 2.]**
- **HF token.** 37 bytes, `hf_`-prefix; env-var only injection contract (`HUGGING_FACE_HUB_TOKEN` or `HF_TOKEN`). **[VERIFIED — `HF_TOKEN_ROTATION_LEDGER_20260914.md` §2.]**

---

## 2 · How each credential was used

### 2.1 Huawei AK/SK (`huawei_credentials.csv`)

- **Discovery pass** (2026-09-09, `HUAWEI_CONNECTIVITY_DRILL_20260909.md` Parts 1–6). Read-only Huawei SDK calls: `iam.list-projects`, `obs.listBuckets` (returned **106 buckets** across `af-south-1` = 70, `tr-west-1` = 31, `ap-southeast-3` = 4, `ap-southeast-1` = 1), `rds.list_instances` (returned **9 RDS instances** in owner's tenant), `rds.list_databases`, `rds.list_db_users`, `eip.list_publicips`, `eip.list_bandwidths`. **[BANKED / VERIFIED-inside-note]**
- **Bounded shape-only probe** (2026-09-16T19:13:57Z). `obs.listObjects(bucket="google-transcripts", max_keys=1)` via `esdk-obs-python` under §E discipline. Endpoint `obs.af-south-1.myhuaweicloud.com`. **Status `200 OK`**, `contents_count=1`, `is_truncated=true`, `at_least_one_object_present=true`. Zero raw AK/SK bytes crossed stdout; shape metadata only. **[VERIFIED — `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json`.]**

### 2.2 CD + Visitors shared DB creds (`admin_bind_20260915_bramuel_cd_visitors.json`)

- **Planned target hosts:** `citizen_digital` at `159.138.164.103:3306` and `visitors` at `110.238.75.83:3306`, both reached from JUMP `159.138.173.250` (JUMP-side SG allow-list is scoped to that JUMP source IP). **[BANKED — `ADMIN_BINDS_20260915.md` §A.]**
- **Actual usage this session:** none. Probe was scheduled for 2026-09-15 08:00 UTC egress window; **JUMP is currently SEC-halted** (`SEC-2026-09-15-06`), so the probe was NOT fired. **[VERIFIED — `PROBE_REFIRE_STATUS_20260916.md` §2.]**

### 2.3 VIUSASA-section DB creds (`db_credentials.csv`)

- Used in the 2026-09-09 Huawei live-SQL drill (`HUAWEI_CONNECTIVITY_DRILL_20260909.md` Part 2) against three CSV-listed hosts:
  - `203.123.86.10:3306` (VIUSASA / IEBC section) → **TCP timeout 8s** from pod egress at that time.
  - `110.238.76.159:3306` (USSD host) → **CONNECTED** as `bramuel@%`; enumerated **17 non-system databases / 1 213 tables** (schema-only + `information_schema.TABLES.TABLE_ROWS`; **no user-table row values** printed).
  - `159.138.164.93:3306` (MICROSERVICES section) → **TCP timeout 8s** from pod egress at that time.
- **Later credential-reuse discovery** (2026-09-09 Part 5): same `bramuel` password also authenticates against `159.138.162.146` (Weego_and_marketing-analytics) in the owner's own AK/SK tenant — 4 databases including `weego` (413 tables). **[BANKED / VERIFIED-inside-drill].**

### 2.4 WEEGO host/db map (`db_credentials_2.csv`)

- Carries no username or password columns — only application-to-host mapping (§7 of the drill · Part 7). Used solely for schema-to-host cross-referencing; no probe. **[VERIFIED — `HUAWEI_CONNECTIVITY_DRILL_20260909.md` Part 7.]**

### 2.5 HF token (`hf_token_rotated_20260914.csv`)

- **Configured** as the active HF access token for the audio-poc plane's transcription-gap fills against NAS `OFFAIRRECS` recordings, injected only via env var `HUGGING_FACE_HUB_TOKEN` / `HF_TOKEN`. **[VERIFIED — `HF_TOKEN_ROTATION_LEDGER_20260914.md` §2 (Injection contract).]**
- **Not actually used to pull models this session** — the audio-poc live pull is CI-fixture only pending admin drops (transcription server host + creds, NAS IP-set). **[BANKED — `ADMIN_BINDS_20260915.md` §C.]**

### 2.6 Legacy AWS files (rows 8–10 in §1)

- Referenced by legacy WPW campaign artefacts; not touched by any Huawei / on-prem probe this session. **[BANKED / VERIFIED-shape-only.]**

---

## 3 · What is connected and visible today

### 3.1 Huawei OBS — LIVE (bounded-shape-only) **[VERIFIED — receipt on disk]**

- **Endpoint:** `obs.af-south-1.myhuaweicloud.com`
- **Region:** `af-south-1` (Johannesburg)
- **Bucket exercised:** `google-transcripts`
- **Op:** `listObjects(max_keys=1)`
- **Result:** `status=200 OK · contents_count=1 · is_truncated=true · at_least_one_object_present=true`
- **Discipline:** env-injection of AK/SK; no `csv.reader`; no `cat`/`head`/`tail`; SDK plugin `esdk-obs-python`; `readonly_obs_guard` in place; `SO §4.1 §E` preserved.
- **Receipt:** `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json`.

Related discovery (from earlier drill, `HUAWEI_CONNECTIVITY_DRILL_20260909.md`): **[BANKED / VERIFIED-inside-note]**
- **106 OBS buckets** visible to this AK/SK across `af-south-1` (70), `tr-west-1` (31), `ap-southeast-3` (4), `ap-southeast-1` (1). No contents read.
- **9 RDS instances** across `af-south-1` (8) and `ap-southeast-1` (1) discoverable via `rds.list_instances`.
- Read-scope of the AK/SK: RDS read, OBS read, IAM self-list, 18 project inventory. **Does not have** DWS list (403 `DWS.01010007`) or DDS list (403 `DBS.280063`). Chinese-mainland regions blocked by `APIGW.0802 international-account-restriction` (structural, not fixable admin-side).

### 3.2 RDS instances at the network + auth layer

| # | Instance / Host | Public IP | TCP :3306 from prior pod egress | MySQL greet | Auth (`bramuel`) | Data-layer state | Label |
|--:|---|---|:---:|:---:|:---:|---|---|
| 1 | `Weego_and_marketing-analytics` (af-south-1) | `159.138.162.146` | ✅ | ✅ MySQL 8.0.28 | ✅ **CONNECTED** | 4 dbs: `analytics` (28 tables), `sql_demo` (1), `sql_trial1` (1), `weego` (413 tables) | BANKED / VERIFIED-inside-drill |
| 2 | USSD host (third-party tenant) | `110.238.76.159` | ✅ | ✅ MySQL 5.7.44 | ✅ **CONNECTED** | 17 non-system dbs / ~1 213 tables (schema-only proof; details in Part 2) | BANKED / VERIFIED-inside-drill |
| 3 | `RDS-INTERACTIONS` (af-south-1) | `159.138.162.220` | ✅ | ✅ MySQL 8.0.28 | ✗ (`1045` — needs different password) | TCP + engine live; auth-gated | BANKED / VERIFIED-inside-drill |

### 3.3 Aggregate posture at the last banked refire (`PROBE_REFIRE_STATUS_20260916.md`)

| Metric | Value |
|---|---|
| Sources PASS | **1** (Huawei OBS) |
| Sources BLOCKED | **5** (CD, Visitors, NAS, Radio, Transcription) |
| Sources FAIL (attempted-and-network-failed) | 0 |
| Sources RUNNING | GPU 72-h campaign in-perimeter |

**Zero PII / row values crossed stdout this session or during the drill** — the discipline banked by `SO §4.1 §E` and `notes/DB_CONNECT_DECISION_POINT_20260913.md` §5 was upheld.

---

## 4 · What is not connected — blockers per source

For each source: exact reason, governing note, and any recorded probe timeout counts / SEC incident IDs.

### 4.1 Huawei OBS · 2nd AK/SK CSV (F.1 finding)

- **Status:** URL succeeded but delivered a **byte-identical duplicate** of `huawei_credentials.csv`.
- **Evidence:** sha256 of the re-download = `8a14174c6a5167cb7fb2f8877b4c3b3ed2d1eed7540aeab0fc4f654457698667`, matching the first file byte-for-byte at 119 B / 1 line.
- **Governing note:** `notes/OWNER_RULING_A_BUNDLE_SHAPE_BETA_20260916.md` §B; `CREDENTIAL_DROP_BIND_DELTA_20260916.md` §F.1.
- **Owner-desk item:** `OWNER-DROP-01` — refined class: **DOWNLOADED-BUT-BYTE-IDENTICAL** (not URL-fail, not genuinely-second-pair). **[VERIFIED — sha256 match.]**

### 4.2 MySQL `citizen_digital` (`159.138.164.103:3306`)

- **Status:** **BLOCKED**.
- **Reason:** JUMP path is SEC-halted (`SEC-2026-09-15-06`) pending root-pw rotation. Direct-from-pod would fail because the SG allow-list is scoped to JUMP source IP `159.138.173.250`, not the pod's egress.
- **Bind material on disk:** UNCHANGED (`admin_bind_20260915_bramuel_cd_visitors.json` sha `a7a616be4577319d10387f15e2e6302e508f1cddc035d017dda8bd7d8717f70d` matches prior pin).
- **Wire-time:** 0 (no wire attempted this session; the halt precludes it).
- **Governing notes:** `ADMIN_BINDS_20260915.md` §A · `PROBE_REFIRE_STATUS_20260916.md` §1 row 2 + §2. **[VERIFIED.]**

### 4.3 MySQL `visitors` (`110.238.75.83:3306`)

- **Status:** **BLOCKED** — same JUMP SEC-halt as row 4.2. Bind UNCHANGED. Wire-time: 0. **[VERIFIED — `PROBE_REFIRE_STATUS_20260916.md` §1 row 3.]**

### 4.4 Synology NAS (10.10.55.x subnet)

- **Status:** **BLOCKED · INBOUND-BIND-PENDING.**
- **Reason:** Admin verbatim 2026-09-15T~04:25Z: *"We will provide you with 10.10.55.x based IPs for access to these services, this is being handled this morning."* IP-set never delivered as of 2026-09-16T19:15Z ingestion.
- **Prior approach (superseded):** `10.10.19.0/24` route (`BLOCKER-RADIO-ROUTING-01` in an earlier ledger, now supersedes to `10.10.55.x` per admin).
- **Governing notes:** `ADMIN_BINDS_20260915.md` §B · `PROBE_REFIRE_STATUS_20260916.md` §1 row 4. **[VERIFIED.]**

### 4.5 Radio subnet

- **Status:** **BLOCKED · same as NAS row** — admin has not delivered the `10.10.55.x` IP-set. Radio integration is downstream (post-M6 audio-plane work). **[VERIFIED — `ADMIN_BINDS_20260915.md` §B, §D row 4.]**

### 4.6 Transcription server

- **Status:** **BLOCKED · SEC-BIND-01.** Admin has NOT dropped transcription-server host + creds this turn. D12 POC currently uses the CI whisper-tiny fixture on GPU hosts `akki-vm` / `akki-vm-ii` per owner ruling 2026-09-15T~03:55Z.
- **Governing notes:** `ADMIN_BINDS_20260915.md` §C · `PROBE_REFIRE_STATUS_20260916.md` §1 row 6. **[VERIFIED.]**

### 4.7 HuggingFace token

- **Status:** **NOT-ROTATED.** The rotated replacement file (`hf_token_rotated_20260914.csv`) is byte-identical to the pre-rotation file (`hf_token.csv`) — same sha256 `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`, same 37 bytes.
- **SEC state:**
  - `SEC-2026-09-12-01` = `OWNER-ROTATED-PENDING-CONFIRMATION` (still awaiting HF-side de-authorisation confirmation from owner).
  - `SEC-2026-09-14-04` = `PENDING-SECOND-ROTATION` (the rotated replacement itself was re-leaked via `head -1` during registration inspection; second rotation genuinely required).
- **Governing notes:** `HF_TOKEN_ROTATION_LEDGER_20260914.md` §4 · `CREDENTIAL_DROP_BIND_DELTA_20260916.md` §F.3 · `OWNER_RULING_A_BUNDLE_SHAPE_BETA_20260916.md` §D. **[VERIFIED.]**

### 4.8 3 remaining MySQL hosts (Weego backup / Voter / unnamed third)

- **Status:** **BLOCKED — admin has not scoped SG openings to these hosts** (admin's 2026-09-15 turn scoped only to CD + Visitors).
- **Governing notes:** `ADMIN_BINDS_20260915.md` §A last paragraph + §D row 3. **[VERIFIED.]**

### 4.9 Viusasa GaussDB (revised admin ask per public research)

- **Status:** **ADMIN-BIND-PENDING.** External research reframe: Viusasa migrated to Huawei Cloud GaussDB(for MySQL); the current on-prem entry `viusasa 203.123.86.10` is likely legacy/stale. Preferred bind is now `Viusasa GaussDB(for MySQL) endpoint + read-only creds + SG opening for JUMP 159.138.173.250` — same pattern as the working weego / ussd Huawei RDS binds.
- **Fallback:** keep the on-prem IP `203.123.86.10` as a fallback probe target (still SG-blocked from pod egress).
- **Governing notes:** `ADMIN_BINDS_20260915.md` §G + §D rows 7–8. **[BANKED / UNVERIFIED (research is not canon).]**

### 4.10 Bastion / JUMP itself

- **Status:** **SEC-HALTED · `SEC-2026-09-15-06`.**
- **Reason:** JUMP root password was inadvertently leaked to agent-tool STDOUT via a bad `sed` redaction. All JUMP-path probes note-skipped pending owner rotation.
- **Additional legacy risk (banked):** `SEC-2026-09-13-T4-02` — public-internet root SSH with password auth on JUMP is a hardening risk (open ssh-with-password from the internet).
- **Governing notes:** `PROBE_REFIRE_STATUS_20260916.md` §2 · `DB_CONNECT_DECISION_POINT_20260913.md` §8 (SEC-2026-09-13-T4-01..04). **[VERIFIED.]**

### 4.11 Pod egress IP drift (context, not a blocker per se)

- Pod egress IP has drifted at least once during the drill: `34.170.12.145` → `34.16.56.64` inside ~2 hours (2026-09-09). Any `/32` SG whitelist against a pod IP is stale by the next redeploy. This is the fundamental reason for **all** direct-whitelist churn described in §5.
- **Governing note:** `HUAWEI_CONNECTIVITY_DRILL_20260909.md` Parts 4–5 (Discovery 1). **[BANKED / VERIFIED-inside-note.]**

---

## 5 · Clear ask — what the admin must do to fully connect

This section is written so each item can be actioned without follow-up. Concrete host, IP, port, source, credential type. Ordered by unblock-value (highest first).

### 5.1 · Rotate the JUMP root password and reopen the JUMP path

- **Incident to clear:** `SEC-2026-09-15-06` (JUMP root password leaked to agent-tool STDOUT via bad `sed` redaction).
- **Concurrent legacy hardening (recommended):** `SEC-2026-09-13-T4-02` — reduce public-internet exposure of JUMP's root-SSH-with-password. Move to keypair-only auth if possible.
- **Action:**
  1. Rotate the JUMP root password on host `159.138.173.250`.
  2. Deposit the new password into `/app/backend/estate_keys/data_sources/` via the same secure hand-off channel as the earlier admin drops. Suggested filename: `jump_root_rotated_20260917.txt`, mode `0600`, root:root. **Do not paste inline in chat.**
  3. Ping the delivery team so we can update the `SEC-2026-09-15-06` ledger row to `OWNER-ROTATED-PENDING-VERIFICATION`.
- **Verification (§6.1) will confirm the halt is lifted.**

### 5.2 · Deliver the `10.10.55.x` IP-set for NAS + Radio access

- **Reference:** Admin verbatim 2026-09-15T~04:25Z (in `ADMIN_BINDS_20260915.md` §B).
- **Action:**
  1. Provide the concrete IP list (or CIDR) for the NAS shares under subnet `10.10.55.0/24` (or whatever exact `/24` / `/28` fragment the admin intends). Include: hostname (or share name) · IPv4 address · service port (SMB `445` / NFS `2049` · specify) · read-only mount user + credential channel.
  2. Provide the analogous IP set for the Radio service (host + port + protocol).
  3. Deposit the IP set as `/app/backend/estate_keys/data_sources/nas_radio_ipset_20260917.json` (mode `0600`), listing each entry as `{name, ip, port, service, credential_pointer}`.
- **Result:** unblocks 2 sources at once (NAS + Radio) via the JUMP-to-internal-subnet route.

### 5.3 · Open MySQL security groups for the JUMP source IP

- **Source IP to whitelist on TCP/3306:** `159.138.173.250/32` (JUMP bastion).
- **Instances to whitelist (per `ADMIN_BINDS_20260915.md` §A and `HUAWEI_CONNECTIVITY_DRILL_20260909.md` §c/§e):**

  | # | Instance name | Public IP | Region | SG(s) to edit |
  |--:|---|---|---|---|
  | 1 | `citizen_digital` (a.k.a. `citizen-digital-dev-db-cluster` — bind IP `159.138.164.103` per §A) | `159.138.164.103` | af-south-1 | `92233ae5-f4d2-4ace-8685-023881e189f1` (sg-Mysql) + `a6456cfb-696e-45c7-8147-13028a53dcea` (sg-Citizen-Digital) |
  | 2 | `visitors-database-cluster` | `110.238.75.83` | af-south-1 | `92233ae5-…` (sg-Mysql) + `aed8d060-…` (RMS-IPS) |
  | 3 | `rds-shikisha` | `203.123.83.144` | af-south-1 | `803fb5f5-…` (sg-shikisha) + `aed8d060-…` (RMS-IPS) |
  | 4 | `election-prod-db2` | `110.238.77.61` | af-south-1 | `92233ae5-…` (sg-Mysql) + `aed8d060-…` (RMS-IPS) |
  | 5 | `dbms-trf-req-database-3` | `159.138.175.179` | af-south-1 | `92233ae5-…` (sg-Mysql) |
  | 6 | `RDS-INTERACTIONS` | `159.138.162.220` | af-south-1 | `aed8d060-…` (RMS-IPS) + `2cc0ad09-…` (default) — *already permissive to earlier pod IP · confirm still open post-drift* |

- **Action:** for each row, add one inbound rule to the listed SG(s):
  - **Protocol** = TCP · **Port** = 3306 · **Source CIDR** = `159.138.173.250/32` · **Description** = `akki-jump-mysql-readonly`.
- **Note:** the earlier drill had cadence to whitelist the pod's ephemeral egress; that approach is fragile and was proven so (Part 5 Discovery 1). Whitelisting **JUMP** is durable because JUMP's IP is fixed.

### 5.4 · Provide DB credentials for the 6 hosts we can't authenticate to

Even after §5.3 lands, we still need per-instance DB user + password for these hosts (documented in `HUAWEI_CONNECTIVITY_DRILL_20260909.md` §3.B, Path A/B). Do not paste inline — drop each as a `.env`-shaped file into `/app/backend/estate_keys/data_sources/` at mode `0600`.

| # | Instance | Need | Suggested filename |
|--:|---|---|---|
| 1 | `RDS-INTERACTIONS` (`159.138.162.220`) | DB user + password with `SELECT` on `interactions` schema (network already open) | `rds_interactions_20260917.json` |
| 2 | `rds-shikisha` (`203.123.83.144`) | Password for known users `corporate` / `saa` (or a purpose-built read-only user) | `rds_shikisha_20260917.json` |
| 3 | `election-prod-db2` (`110.238.77.61`) | Username + password | `election_prod_db2_20260917.json` |
| 4 | `visitors-database-cluster` (`110.238.75.83`) | Username + password (schemas `citizen_digital`, `db_visitors`, `db_visitors_old`, `db_visitors_v1`, `rembesha`) | `visitors_cluster_20260917.json` |
| 5 | `dbms-trf-req-database-3` (`159.138.175.179`) | Username + password | `dbms_trf_req_20260917.json` |
| 6 | `citizen-digital-dev-db-cluster` (`159.138.164.124`) | Username + password | `citizen_digital_dev_20260917.json` |
| 7 | `weego-replica-d536` (private `10.10.150.115`) | Inherits from WEEGO primary — supplying the WEEGO primary read-only password unlocks this too | (covered by row above if primary cred lands) |

### 5.5 · Rotate the shared `bramuel@%` DB credential + issue app-scoped users

- **Why:** the current `bramuel@%` grant is host-wildcard (authenticates from any internet client) and shares the same 16-char password across at least three Huawei tenants (`110.238.76.159`, `159.138.162.146`, and the two blocked hosts under the same section). This is a shared admin-scoped credential, not an app-scoped one. Also: this password appeared in an early session transcript before position-redaction hard-lock landed (`SEC-2026-09-13-T4-04`).
- **Action:**
  1. Rotate the current `bramuel@%` password on **every** instance where it is set.
  2. Issue **app-scoped, least-privilege, per-DB users** for the mtafiti / extraction workload: read-only on the specific schemas needed, `SOURCE = <bastion_private_ip>/32` (after §5.7 lands), rate-limited.
  3. Deposit new per-instance creds per §5.4 file-naming convention.
- **Reference:** `HUAWEI_CONNECTIVITY_DRILL_20260909.md` §3.D and Part 2 §"Discoveries worth naming".

### 5.6 · Re-drop the second Huawei AK/SK pair (OWNER-DROP-01 refinement)

- **Why:** the first re-drop of the "second" CSV delivered a byte-identical duplicate of the first (sha256 `8a14174c…698667`). If a genuinely-second AK/SK pair exists (per the original owner statement at compaction handoff: *"files 1+2 Huawei AK/SK"*), please re-issue.
- **Action:**
  1. Re-upload the genuinely-second Huawei AK/SK CSV to a fresh customer-assets URL.
  2. Deposit as `/app/backend/estate_keys/data_sources/huawei_credentials_2_20260917.csv` (mode `0600`).
  3. Confirm the two AK/SK pairs are for **different Huawei service / account scopes** (otherwise duplication persists at the value layer).
- **Or, if there is only one pair:** confirm that in-writing so we can close `OWNER-DROP-01` with the "consolidated-into-single-file" verdict.

### 5.7 · Provision the af-south-1 bastion (durable path)

Bastion spec is banked in full in `SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md` §Bastion Spec — the admin already has it. Recap of what must land:

- **Name:** `akki-mtafiti-bastion-af-south-1`
- **Region / project:** `af-south-1` / project `517a45cac3994683abcf0cc155b3c01b`
- **VPC / subnet:** `de3ba6f7-d0e7-4228-8da2-19bd33a07ff2` (vpc-media-web, CIDR `10.10.150.0/24`) / `c7fef874-8aef-4b91-9d3b-7e84ce53104d` (subnet-media-web)
- **Flavour:** `s6.xlarge.2` (4 vCPU / 8 GiB) — trim option `s6.large.2`
- **Image:** Ubuntu 22.04 / 24.04 LTS
- **System disk:** 100 GiB General-Purpose SSD
- **EIP:** 1 reserved, pay-per-use traffic-mode (or bandwidth-mode 10 Mbps if sustained mtafiti traffic is planned)
- **Bastion SG:** new `sg-akki-mtafiti-bastion`. Inbound: TCP/22 from the delivery-team-supplied source CIDR set. Outbound: default allow-all.
- **DB SGs to modify (add `<bastion_private_ip>/32` on TCP/3306):** `aed8d060-…` (RMS-IPS), `2cc0ad09-…` (default), `803fb5f5-…` (sg-shikisha), `92233ae5-…` (sg-Mysql), `a6456cfb-…` (sg-Citizen-Digital).
- **Keypair:** delivery team generates ed25519 locally; admin injects public key at ECS create-time.

**IAM policies** (attach to user `BramwelMwalo` scoped to project `517a45cac3994683abcf0cc155b3c01b`, and to `b2c3b9b1ef6346ab9e45818f8a6714ba` if the second bastion is authorised):
1. `ECS FullAccess`
2. `VPC FullAccess`
3. `EVS FullAccess`
4. `EIP FullAccess`

(Least-privilege alternative is in `SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md` §Appendix.)

### 5.8 · (Optional) Provision the ap-southeast-1 bastion for `rms-ai-pg` (PostgreSQL 16)

- Only needed if `rms-ai-pg` (private-only in `192.168.1.30`) is in scope.
- **Alternative:** VPC peering between `vpc-media-web` (`10.10.150.0/24`) and `rms-ai-vpc` (`192.168.0.0/16`) — CIDRs do not overlap.
- Spec in `SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md` §Bastion Spec "SECOND BASTION".

### 5.9 · Genuinely rotate the HuggingFace token

- **Incident:** `SEC-2026-09-14-04` (rotated replacement was byte-identical to pre-rotation).
- **Action:**
  1. Owner-side: revoke the current HF token from the HuggingFace account settings.
  2. Issue a **new** HF token (different value).
  3. Deposit at `/app/backend/estate_keys/data_sources/hf_token_rotated_20260917.csv` (mode `0600`, `hf_`-prefix, single line).
  4. Confirm `wc -c` reads a 37-byte file (or whatever the new HF token size is — HF token sizes are stable per token class) and `sha256sum` differs from `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`.
- **Injection contract (unchanged):** env-var only (`HUGGING_FACE_HUB_TOKEN` or `HF_TOKEN`); never printed; never on a `ps auxww`-visible command line.

### 5.10 · Third-party tenant coordination (hosts #11 and #12 in `SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md`)

- Hosts `203.123.86.10` and `159.138.164.93` sit in a Huawei tenant the owner does not administer.
- **Action:** owner-to-owner conversation with the third-party tenant's administrator, asking them for **one SG inbound rule per host**: source = bastion EIP `/32` (from §5.7 once landed), TCP/3306. Nothing on our side unblocks the third-party side.

### 5.11 · Confirm or replace the Viusasa on-prem IP

- **Action:** admin confirms whether Viusasa has fully migrated to a Huawei Cloud GaussDB(for MySQL) endpoint (public research suggests it has). If yes: supply the GaussDB endpoint hostname + read-only creds + SG opening for JUMP `159.138.173.250` — same pattern as the working weego / ussd binds. If no: retain the on-prem `203.123.86.10` and open its SG per §5.3.
- Same open question exists for **Shikisha** (`203.123.83.144`): confirm on-prem vs cloud.
- **Reference:** `ADMIN_BINDS_20260915.md` §G.

### 5.12 · (Later) Drop transcription-server host + creds

- **Incident:** `SEC-BIND-01`. Admin/Owner drop pending.
- **Action:** deposit `{host, port, protocol, user, password_pointer}` file at `/app/backend/estate_keys/data_sources/transcription_server_20260917.json` mode `0600`. Ping delivery team.
- **Reference:** `ADMIN_BINDS_20260915.md` §C.

---

## 6 · Once-done verification plan

For each admin action above, this is the bounded probe we will run to confirm the connection. Every probe below is metadata-only: **zero secret values leave stdout, zero PII / row values are read, only counts / status codes / handshakes emit.**

### 6.1 JUMP rotation clear (§5.1)

- **Probe:** SSH keypair-only connect from pod → JUMP `159.138.173.250` using the freshly rotated password (or, preferably, a delivery-team public key installed on the JUMP host). Command shape: `ssh -o BatchMode=yes -o ConnectTimeout=5 <user>@159.138.173.250 'echo ready'`. **Password never on command line** — either keypair or `sshpass` reading from an `askpass` script.
- **PASS look:** stdout = `ready` · exit 0.
- **Additional:** update `SEC-2026-09-15-06` ledger row to `OWNER-ROTATED-PENDING-VERIFICATION` → `VERIFIED`.

### 6.2 NAS + Radio IP-set landing (§5.2)

- **Probe (NAS):** `nc -zv -w 5 <nas_ip> <nas_port>` from JUMP (once §5.1 lands). One line per `{name, ip, port}` entry.
- **Probe (Radio):** analogous.
- **PASS look:** `Connection to <ip> <port> port [tcp/*] succeeded!` for every entry. Any timeout or refused emits a `BLOCKED · reason=network_timeout / port_closed` row into a probe receipt (no data-plane read attempted at this stage).

### 6.3 MySQL SG openings (§5.3)

- **Probe (per row):** `bash -c 'exec 3<>/dev/tcp/<host_ip>/3306; head -c 85 <&3 | xxd -c 16 | head -n 6; exec 3<&-'` executed from JUMP `159.138.173.250`. This reads only the MySQL server's handshake packet (85 bytes, protocol v10, banner string) and closes. **No SQL run.**
- **PASS look:** first 5 bytes are `<len><seq>` then `\x0a` (protocol 10); banner string `8.0.28-…` or `5.7.44-…` (MySQL version). Receipt records only: `{host, port, tcp_ok: true, handshake_len: 85, mysql_version: "<parsed banner>"}`.

### 6.4 DB credentials functional (§5.4)

- **Probe (per row, per host):** `pymysql.connect(host=<host>, port=3306, user=<user>, password=os.environ['DB_PW'], connect_timeout=8, autocommit=True, init_command='SET SESSION TRANSACTION READ ONLY')` → `SELECT 1`, `SELECT VERSION()`, `SHOW DATABASES` (metadata only).
- **PASS look:** receipt row `{host, tcp_ok: true, handshake_ok: true, auth_ok: true, version: "<mysql_version>", databases_visible: <count>}`. **No table row data read. No PII surfaced.** Password is env-injected; never on command line, never in stdout, never in receipt.

### 6.5 `bramuel` rotation + app-scoped users (§5.5)

- **Probe:** re-run §6.4 against every affected instance using the **new** per-app credentials. Confirm old `bramuel` fingerprint (`sha256_8=5b9ec5c0`) **fails** (`1045 Access denied`). Confirm new per-app fingerprints (recomputed fresh) succeed with `SELECT 1` at read-only session.
- **PASS look:** old fp fails at every instance · new fp passes at exactly the schema-scope granted · session `@@SESSION.transaction_read_only = 1`.

### 6.6 Second Huawei AK/SK (§5.6)

- **Probe:** §E-discipline metadata parse on the new CSV: `sha256sum` + `wc -l` + `stat -c %a` (mode `0600`) + read AK/SK lengths from raw bytes; then `obs.listBuckets` and `obs.listObjects(bucket, max_keys=1)` under `readonly_obs_guard`. Compare against the first pair's sha256 (`8a14174c…698667`) — must **differ** to be genuinely-second.
- **PASS look:** sha256 differs · AK length 20 · SK length 40 · `listBuckets` returns > 0 (potentially different scope) · `listObjects` returns `status=200` on at least one bucket. Zero AK/SK bytes crossed stdout.

### 6.7 Bastion (§5.7)

- **Probe:** SSH from pod → bastion EIP; then bastion → each in-VPC RDS EIP on TCP/3306 via `bash /dev/tcp`. Then bastion → private-only `weego-replica-d536` `10.10.150.115:3306`.
- **PASS look (network layer):** every RDS EIP handshake succeeds within 300 ms; `weego-replica-d536` reachable at its private IP; receipt records only handshakes and MySQL version banners.

### 6.8 Second bastion / VPC peering (§5.8, optional)

- **Probe:** from ap-southeast-1 bastion (or peered path) → `rms-ai-pg` `192.168.1.30:5432` TCP-only.
- **PASS look:** TCP handshake succeeds; PostgreSQL server sends its startup message; receipt records only that fact.

### 6.9 HF token rotation (§5.9)

- **Probe:** §E-discipline metadata parse on the new file (`sha256sum`, `wc -c`, `stat -c %a`); confirm sha256 differs from `3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5`; then a bounded `huggingface_hub.HfApi().whoami()` call using env-injected token.
- **PASS look:** sha differs · `whoami` returns `{name, type: "user"}` shape with **no token value in stdout** · receipt records only presence of the fields, not their values. Update `SEC-2026-09-14-04` to `OWNER-ROTATED-PENDING-VERIFICATION` → `VERIFIED`.

### 6.10 Third-party tenant SGs (§5.10)

- **Probe:** TCP + MySQL-greet from bastion EIP to `203.123.86.10:3306` and `159.138.164.93:3306`. Then auth using the existing `bramuel` credential (or its replacement per §5.5) if the third-party accepts.
- **PASS look:** TCP handshake succeeds; MySQL banner emitted; auth response = `USER() bramuel@<bastion_eip>` or a fresh `1045` denial (which is still a "engine live, auth-gated" PASS at the network layer).

### 6.11 Viusasa reframe (§5.11)

- **Probe (if migrated):** §E parse of GaussDB endpoint file; then `pymysql` connect over JUMP tunnel with read-only session; `SELECT VERSION()` should return a Huawei GaussDB build string.
- **Probe (if on-prem):** §6.3 + §6.4 pattern against the on-prem IP once SG opens.

### 6.12 Transcription server (§5.12)

- **Probe:** whatever the drop file specifies (typically HTTPS to a whisper-compatible endpoint). We will define a bounded shape-only probe on receipt — e.g. `HEAD /health` returning `200`, or a synthetic 1-second silent-WAV round-trip yielding an empty transcript.

---

## Appendix · SEC incident ledger — quick reference

| Incident ID | Description | Status (as of 2026-09-16 bank) | Governing note |
|---|---|---|---|
| `SEC-2026-09-12-01` | Original HF token leak (pre-rotation `hf_token.csv` echoed) | `OWNER-ROTATED-PENDING-CONFIRMATION` | `HF_TOKEN_ROTATION_LEDGER_20260914.md` §4 |
| `SEC-2026-09-14-04` | Rotated HF replacement itself was re-leaked via `head -1`; byte-identical to pre-rotation | `PENDING-SECOND-ROTATION` (rotation not genuine) | `HF_TOKEN_ROTATION_LEDGER_20260914.md` §4 · `CREDENTIAL_DROP_BIND_DELTA_20260916.md` §F.3 |
| `SEC-2026-09-13-T4-01` | JUMP password (12 chars) echoed in early CSV structure inspection | Rotation required | `DB_CONNECT_DECISION_POINT_20260913.md` §8 |
| `SEC-2026-09-13-T4-02` | Public-internet root SSH with password auth on JUMP is a hardening risk | Hardening pending | `DB_CONNECT_DECISION_POINT_20260913.md` §8 |
| `SEC-2026-09-13-T4-03` | v1 T4 driver buffer bug briefly showed RADIO cred in pty echo | Scrubbed in-memory · not persisted | `DB_CONNECT_DECISION_POINT_20260913.md` §8 |
| `SEC-2026-09-13-T4-04` | DB password (16 chars, `bramuel@%`) echoed to transcript during structural inspection | Rotation required (§5.5) | `DB_CONNECT_DECISION_POINT_20260913.md` §8 |
| `SEC-2026-09-15-05` | Post-connectivity-verification owner rotation cadence | `PENDING-OWNER-ROTATION-POST-VERIFICATION` | `ADMIN_BINDS_20260915.md` §D row 6 |
| `SEC-2026-09-15-06` | JUMP root pw leaked to agent-tool STDOUT via bad `sed` redaction | JUMP-halt in force · §5.1 clears | `PROBE_REFIRE_STATUS_20260916.md` §2 |
| `SEC-BIND-01` | Transcription-server host + creds not delivered | Pending admin drop-in (§5.12) | `ADMIN_BINDS_20260915.md` §C |

---

## Appendix · Discipline attestation for this brief

- No product code touched; no commits; no push; no re-clone; pending `CP-M8-CSD-1` Commit-C fixup **not** touched.
- No credential values printed. Every reference is by filename / location / purpose. SHA256 fingerprints and byte lengths are shape metadata (safe under `SO §4.1 §E`).
- Every host / IP / port / bucket / SG-id / VPC-id / subnet-id / project-id / domain-id cited above was extracted from a note or receipt already on disk. Nothing was invented.
- Where a fact could not be re-verified this session, the label reads `BANKED / UNVERIFIED` or `BANKED / VERIFIED-inside-note`; where it was checked on disk this session, `VERIFIED`.

*End of brief.*
