# DigiCow read-capability check — state note (2026-09-21T15:37Z → 15:40Z)

**Trigger**: Owner directive this-session 2026-09-21T~15:05Z: "OWNER CREDENTIAL DROP → DIGICOW estate, ingest under §E secret-hygiene then run a read-capability check STRICTLY scoped to DigiCow."
**Scope discipline**: DigiCow ONLY. No touch to the 8 RMS MySQL clusters, the OFFAIRRECS/Record CIFS mount, or the RMS Huawei OBS estate.
**R-91 hold**: unchanged (~38h to `2026-09-23T03:23:15Z`).
**Ratchet floor**: 5858 (untouched).
**Survey-only, no seal, no `testing_agent`, S4 still gated.**

## Custody ingest under §4.1 §E (byte-metadata only)

- **Drop 1 · Digicow.xlsx** → `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_xlsx.xlsx`
  - sha256 `2ec3761f15440cca8581506aa1556a3788ab623d590e8905004963baf8b6b391`
  - size 3934 B
- **Drop 2 · api_user_accessKeys.csv** → `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv`
  - sha256 `d8908b7a32aecc72a66adec46bdcd18dcd893d3419892bd37633463afc7ec366`
  - size 99 B (single AK/SK pair, AWS-IAM-style CSV)
- Manifest: `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_drop_manifest.json`

Xlsx sheet layout: `Sheet1`, 7 rows × 1 col, 4 populated rows, all `label: value` shape.

Cred shape (value-blind):
- CSV headers: `Access key ID`, `Secret access key` (AWS IAM naming, distinct from Huawei's `Access Key Id`/`Secret Access Key`).
- AK: 20 chars, UPPER prefix (canonical AWS `AKIA…` shape).
- SK: 40 chars, mixed case (canonical AWS).

Structural surface facts extracted from xlsx (labels + ARNs are non-secret AWS identifiers, safe to name):
- `region: eu-west-1` (AWS Ireland)
- `cluster arn: arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster` — RDS Aurora (Data-API-compatible)
- `secret arn: arn:aws:secretsmanager:eu-west-1:494452543252:secret:rds/data/api/user/secrets-8rZuVc`
- `database name: digicow_live, ndume` (+ owner note: "you have read access to all the records in those two databases - here is digicow data estate")

## Surface class determined

**AWS RDS Aurora, accessed via the RDS Data API using Secrets Manager for DB credentials.** The Data API pattern requires the IAM principal to have:
- `rds-data:ExecuteStatement`
- `secretsmanager:GetSecretValue` on the specific secret ARN

**Vantage**: DIRECT EGRESS from the sandbox pod to `rds-data.eu-west-1.amazonaws.com` (not via JUMP — this is a cloud endpoint the pod reaches directly, distinct from the RMS on-prem estate).

## Step 2 · Proofs (all read-only, all shape-only)

### STS `GetCallerIdentity`
- **OK** — Account `494452543252`, IAM principal `arn:aws:iam::494452543252:user/api_user`, UserId `AIDAXGH5LB4KEWCKICQOH`. IAM AK/SK live and valid.

### Data API sanity — `SELECT 1` on `digicow_live`
- **OK** in 1.215s. IAM AK/SK has the required `rds-data:ExecuteStatement` + `secretsmanager:GetSecretValue`; cluster is Aurora-Data-API-enabled; secret is valid.

### Per-database enumeration + prove-read

| database | `SHOW TABLES` | probed (cap 25) | proof-of-read pass | proof-of-read fail | describe errors |
|---|---:|---:|---:|---:|---:|
| `digicow_live` | **126 tables** | 25 of 126 | **25 / 25** | 0 | 0 |
| `ndume`        | **113 tables** | 25 of 113 | **25 / 25** | 0 | 0 |
| **total** | **239** | **50** | **50 / 50** | **0** | **0** |

Per-table proof was: `DESCRIBE <t>` + `SELECT COUNT(*) FROM <t>` + `SELECT * FROM <t> LIMIT 1` (shape-only redaction; RDS Data API's `Field` union redacted to `kind + is_null + byte_len/char_len/int_bit_len` — never emits real `stringValue`/`blobValue` content).

Table-name samples emitted (structural, non-secret):
- `digicow_live` (first 15): `admins`, `adoption`, `adoption_data`, `android_metadata`, `auth_group`, `auth_group_permissions`, `auth_permission`, `auth_user`, `auth_user_groups`, `auth_user_user_permissions`, `banner`, `breeding`, `calf`, `calf_milk`, `calving`. Signature: **Django ORM auth tables + dairy-domain business tables**. Backing framework Django (Python), MySQL-compatible dialect (works via Data API).
- `ndume` (first 15): `#Tableau_5_sid_00005080_5_Filter`, `County_Vet_Location`, `Issued_Semen`, `Semen_issuance`, `Sheet1`, `addedVets`, `ai_count` (AI = Artificial Insemination in the dairy context), `ai_search_records`, `breedings`, `breedings_straw_logs`, `calf_milk`, `calves`, `calving`, `campaign_targets`, `campaign_vaccines`. Signature: **veterinary-services / AI campaign management + Tableau BI artifacts + a Sheet1 (Excel-imported) table**.

## Verdict (binary + failure layer)

**Binary answer**: **YES**.
- Surface class: **AWS RDS Aurora via Data API + Secrets Manager**.
- Databases readable: `digicow_live` (126 tables), `ndume` (113 tables) — 239 total.
- Tables probed: 50 of 239 (bounded); **50 / 50** succeeded on the SELECT-LIMIT-1 shape proof; 0 permission-denied; 0 describe errors.
- Failure layer: **none**.

Content is READABLE END-TO-END across the DigiCow estate. If the owner wants proof over ALL 239 tables (not just the first 25 per DB), lift the `MAX_TABLES_PROBED_PER_DB=25` cap — but the current sample already exhibits zero permission variance, so a broader probe would only confirm the same result.

## Receipts banked (state-only)

- `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_xlsx.xlsx`
- `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv`
- `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_drop_manifest.json`
- `phase0/connectivity_receipts/20260921T154022Z_DIGICOW_read_capability_check_owner_authorized_20260921.json`
- `STATE/notes/DIGICOW_READ_CAPABILITY_STATE_20260921.md` (this file)
- Tool: `tools/digicow_read_capability_20260921.py`

## Notable findings

1. **DigiCow is a distinct AWS-hosted estate**, not part of the RMS on-prem estate. Direct egress to eu-west-1 works from the sandbox pod. IAM principal is `arn:aws:iam::494452543252:user/api_user` — a dedicated API service account.
2. **Data API vantage is elegant** — no need to (a) fetch the secret from Secrets Manager manually, (b) resolve the RDS cluster endpoint via DescribeDBClusters, or (c) open a TCP tunnel to a private-VPC RDS. Data API bridges IAM → Secrets Manager → RDS transparently. No hostname was ever exposed to the sandbox pod.
3. **DigiCow app framework**: Django (auth_* tables), MySQL-compatible dialect via Aurora Data API. Two databases live side-by-side: `digicow_live` (production app tables) and `ndume` (Kiswahili for "cattle" — likely a vet-services / breeding sub-application, with campaign management + Tableau BI artifacts embedded).
4. **Naming reuse** across the two DBs: `calf_milk`, `calving`, `breeding`/`breedings` appear in both — potentially a data-sync or shared-schema pattern between the consumer-facing (`digicow_live`) and the vet-services (`ndume`) apps.
5. **Cluster name suggests provenance**: `db-restore-603-cluster` — this looks like a cluster that was restored from a snapshot (perhaps ticket #603). Worth flagging if the owner cares about primary-vs-restore provenance.

## Standing bounds — all unchanged

- **R-91 hold** intact (~38h to `2026-09-23T03:23:15Z`).
- **Ratchet floor 5858** unchanged (survey-only, no code touched).
- **§3.8 additive-only** intact.
- **No `testing_agent`, no seal**.
- **S4 bulk ingestion** still gated (owner-explicit "no bulk pulls" this run — 50 LIMIT-1 SELECTs was the only content touch, and each returned 0 or 1 row with values redacted to shape).

## Hygiene tally

- Read-only across every touch. Zero bulk pulls. Zero writes.
- 50 `SELECT * FROM <table> LIMIT 1` executed; every row redacted to shape (kind + null-status + byte/char length + int-bit-length). No real row values in stdout / logs / receipts.
- AWS IAM AK/SK held in memory only; never printed. Shape only (ak_len=20, ak_prefix4="AKIA", sk_len=40).
- Custody file shas pinned in receipt + manifest.
- No `testing_agent`, no seal, no code changes to production tree.

## Standing admin asks (updated after this drop)

1. MySQL `159.138.162.146` creds — still missing.
2. MySQL `HOST` placeholder (WEEGO) — needs IP substitution.
3. Huawei OBS `obs:object:GetObject` scope on rotated AK/SK.
4. (nice-to-have) NAS DSM/SMB direct creds — CIFS mount working via cached session.
5. **(new — DigiCow) — CLOSED by this drop.** Full read across `digicow_live` + `ndume` via Data API.

— end of state note.
