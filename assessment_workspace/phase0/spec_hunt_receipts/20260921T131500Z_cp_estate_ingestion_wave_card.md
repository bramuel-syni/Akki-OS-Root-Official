# Wave Card · CP-ESTATE-INGESTION · Sprint-Scope Add · 2026-09-21T13:15Z

**Status**: PROPOSED (no data-touching sub-slice opened yet).
**Owner authorization line (this-session, 2026-09-21T~13:15Z verbatim)**:

> "PART B — DEFINE THE ESTATE-INGESTION WAVE (add to scope, do NOT open bulk ingestion yet — author the wave shape + objective card + RED-first discipline, then report for my GO on the first data-touching sub-slice). Scope covers exactly what is REACHABLE now: MySQL: USSD `110.238.76.159:3306` + MICROSERVICES-primary `159.138.162.146:3306` (via JUMP, banked read-only creds). Wave discipline: connect read-only → schema survey (SHOW DATABASES / TABLES / column metadata + row counts) FIRST as its own sealed sub-slice → owner reviews the survey → only then any data pull, and pulls land in the append-only ledger/tenant-primitive shape with receipts, never a second store. NAS DSM `10.10.55.55:5000` (reachable): survey the shares/paths the service account can see, read-only. OBS `rms-ai` bucket (reachable): treat as a read-only object source; object-level ingestion is its own sub-slice after the survey. Everything still blocked (5 MySQL clusters, 105 OBS buckets if region/IAM-blocked) stays OUT of the wave as owner-side asks, listed explicitly in the card so the boundary is clear. Bind the wave to canon: lawful-basis-at-Admit (Doc 5 B5.2), append-only writer (B5.4), no second store (ENT/CON bans), every external read receipted. RED-first invariants on the ingestion adapters (additive modules, zero sealed edits), standard 3-Commit Seal + continuity bundles."

---

## Objective

Bring the **reachable-now** subset of the RMS estate into the sealed Akki ledger/tenant-primitive shape as **append-only, receipted, canon-bound reads**. No second store. Every external byte we read is bound to a receipted event on the append-only writer. Ingestion adapters are additive modules under `services/data_source/…` — zero sealed edits.

## In-scope surfaces (reachable-now, verified 2026-09-21)

| # | Kind    | Endpoint / bucket                        | Vantage                                | Access proof                                                                                    |
|---|---|---|---|---|
| 1 | MySQL   | `110.238.76.159:3306` (USSD)             | via JUMP `159.138.173.250`             | JUMP TCP_OPEN in `20260921T124751Z_JUMP_retry_owner_authorized_20260921.json` |
| 2 | MySQL   | `159.138.162.146:3306` (MICROSERVICES-primary) | via JUMP `159.138.173.250`         | JUMP TCP_OPEN in same receipt |
| 3 | NAS-DSM | `http://10.10.55.55:5000` (NAS home)     | via JUMP `159.138.173.250`             | JUMP TCP_OPEN in same receipt |
| 4 | OBS     | `rms-ai` bucket (region `ap-southeast-1`) | direct (egress `35.184.53.215` → `obs.ap-southeast-1.myhuaweicloud.com`) | 200 OK ListBuckets + ListObjects(max_keys=20) in `20260921T131024Z_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json` · 20 objects returned all under prefix `image_files/2795ba36-2730-435f-b1be-eb07a9d83c1f/` · truncated=true · avg ~33 KB/obj · mix of jpg/png |

## Out-of-scope surfaces (still blocked · owner-side asks)

- **5 MySQL clusters** still unreachable from JUMP (Huawei microservices region): `203.123.86.10:3306` (iebc_forms), `159.138.164.93:3306`, `159.138.164.124:3306`, `110.238.75.83:3306`, `203.123.83.144:3306`. **Owner ask to RMS admin**: JUMP-egress firewall allowlist for these.
- **105 additional OBS buckets** are actually **REACHABLE with region-correct endpoint routing** (verdict PART A: `REGION_MISMATCH_RESOLVED` on 3/3 sample buckets). They span at least `af-south-1`, `ap-southeast-3`, `tr-west-1`, `sa-argentina-1`, `cn-north-*`, `eu-west-101`, `cn-east-3`, `cn-south-1`. **Not in this wave** — their inclusion needs an explicit owner GO because the volumes (esp. `citizen-vod`, media buckets) may be large. Flagged as **OWNER-DROP-05: region-scope decision — do we sweep all 106 buckets or scope to a named allow-list?**
- **Data-plane MySQL protocol sessions**: STILL BANNED without a separate owner GO for the ingestion sub-slices below.

## Canon anchors (verbatim binding)

- **Doc 5 B5.2 — Lawful-Basis-at-Admit**: every ingestion adapter emits a `LawfulBasisAdmit` event at first-touch that names the source, the basis, and the receipt sha. No admit = no ingest.
- **Doc 5 B5.4 — Append-only writer**: all ingested records land through the ledger append-only writer (`services/ledger_actor_binding` sealed carrier). No mutation of prior events. No side-channel store.
- **Doc 5 ENT/CON — No-second-store**: ingestion adapters MAY NOT write to a database of their own. All persistence goes through the ledger. Adapters may keep a transient in-memory cursor for pagination; that cursor is never persisted to disk outside the ledger.
- **Every external read is receipted**: each network call from an ingestion adapter emits a `ExternalRead` event carrying `{source, endpoint, timestamp, req_bytes, resp_bytes_shape, response_status, receipt_sha}`. The response payload itself lands via the ledger append path.
- **SO §3.8 additive-only**: adapters are net-new modules under `services/data_source/` (or `services/ingestion/`). Zero sealed edits.

## Sub-slice sequence (owner-gated · no auto-progression)

**S1 · SCHEMA-SURVEY-MYSQL** (READ-ONLY · no row data)
- Connect read-only to USSD + MICROSERVICES-primary from within JUMP tunnel.
- Emit per-cluster: `SHOW DATABASES`, then per-DB `SHOW TABLES`, then per-table `SHOW COLUMNS`, then `SELECT COUNT(*)` (row count only, no `SELECT *`).
- Bank a schema-survey receipt at `phase0/ingestion_receipts/{TS}_S1_mysql_schema_survey.json` per cluster.
- **NO row-level SELECT · NO SELECT * · NO data pull**.
- Owner reviews the survey and issues GO for S2 (or narrows the scope to specific tables).

**S2 · SCHEMA-SURVEY-NAS** (READ-ONLY · listing only)
- SSH into JUMP, then SMB/DSM listing of top-level shares that the service account can see (per NAS creds banked in `RMS_Connection_Creds.xlsx`).
- For each visible share: enumerate top-level directory names + counts + total-size-if-cheap (via `du -sh` or DSM API `listShares`).
- Bank at `phase0/ingestion_receipts/{TS}_S2_nas_share_survey.json`.
- **NO file downloads · NO recursive listing beyond top-level** (owner GO required for deep listing).

**S3 · SCHEMA-SURVEY-OBS-RMS-AI** (READ-ONLY · object metadata only)
- Full ListObjects sweep on `rms-ai` (pagination via marker/max_keys=1000).
- Emit prefix histogram + count-by-prefix + size-histogram + earliest/latest LastModified.
- Bank at `phase0/ingestion_receipts/{TS}_S3_obs_rms_ai_survey.json`.
- **NO GetObject · NO ACL query beyond bucket · NO regional-buckets sweep** (owner GO required for the 105 other buckets).

**S4 · DATA-INGEST-SUB-SLICES** (INDIVIDUALLY owner-gated · one per surface)
- S4a — MySQL USSD data pull (specific tables named by owner post-S1 review).
- S4b — MySQL MICROSERVICES-primary data pull (specific tables named by owner).
- S4c — NAS file ingestion (specific shares/paths named by owner post-S2).
- S4d — OBS rms-ai object ingestion (specific prefixes named by owner post-S3).
- **Each S4x lands as its own 3-Commit Seal** with a dedicated adapter under `services/data_source/{source}/`. RED-first tests on adapter: (i) LawfulBasisAdmit emitted before first byte; (ii) all rows/objects flow through the ledger; (iii) no second store; (iv) idempotent restart from last banked cursor.

## RED-first invariants on the ingestion adapters

For each adapter authored under `services/data_source/{source}_read_only/`, land RED tests FIRST:

1. `test_{source}_adapter_lawful_basis_admit_emitted_before_first_byte` — adapter refuses to call `network.read()` before writing a `LawfulBasisAdmit` event to the ledger.
2. `test_{source}_adapter_no_second_store` — adapter has no `open(..., 'w')` / `open(..., 'a')` / `write_text` / `write_bytes` / `pymongo.insert` / any DB write outside the ledger writer surface. Enforced by AST scan + grep-invariant.
3. `test_{source}_adapter_all_reads_receipted` — every `network.read()` call is bracketed by `ledger.append(ExternalRead(...))` — enforced by decorator or context-manager wrapper (adapter pattern per SO §3.8, e.g., `services/enforce/receipted_external_read_wrapper.py`).
4. `test_{source}_adapter_idempotent_restart_from_cursor` — after N records ingested + adapter killed + restart, adapter resumes at N+1, no gaps, no dupes.

RED-first sequence per sub-slice: **write RED tests → adapter module empty stub → RED evidence banked → author adapter → GREEN evidence banked → BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep → 3-Commit Seal**.

## Seal & continuity bundle discipline

Standard 3-Commit protocol (code A + state B + state C fixup) per sub-slice, with continuity bundles regenerated + PINS updated at each seal. Wave-level DECISIONS entry banks the wave card + each sub-slice cure.

## Standing bounds (unchanged)

R-91 hold **unchanged** (horizon `2026-09-23T03:23:15Z`) · **no `testing_agent`** (STRICTLY BANNED per SO §6) · zero push · zero remote · terminal `pytest` only · additive-only §3.8 · three-repo discipline · ratchet floor **5858** · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · structural §3.8 guard on `services/request_context/context.py` sha-pin `ad0d9439…` · mirror-invariant guard on `/app/backend/vendored/extraction_akki/backend/`.

## What is READY on owner GO

**S1 · SCHEMA-SURVEY-MYSQL** is ready to run on `GO S1`. It:
- Opens SSH tunnel to JUMP with banked creds (in-memory only, hygiene per JUMP retry drill 20260921T124751Z).
- From JUMP, opens read-only MySQL connections to USSD + MICROSERVICES-primary with banked read-only creds (loader `rms_creds_loader.load()`; secrets never printed).
- Emits `SHOW DATABASES / TABLES / COLUMNS` + `SELECT COUNT(*)` per table.
- Banks the survey receipt.
- Halts.
- Total wall-time budget: ~10 minutes.

Report for owner GO required. No auto-progression to S2/S3/S4 without explicit owner instruction.
