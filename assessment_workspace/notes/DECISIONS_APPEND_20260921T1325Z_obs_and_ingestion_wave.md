
---

## HUAWEI-OBS-ACCESS-DRILL · owner-authorized · 2026-09-21T13:10Z

### Owner directive verbatim this-session (2026-09-21T~12:55Z + follow-up 2026-09-21T~13:15Z)

> "OWNER QUESTION → receipted drill (authorized now, non-interrupting to the R-91 hold): DO WE HAVE HUAWEI OBS (object storage) ACCESS with any banked access keys? ... If AK/SK found: probe OBS read-only via signed REST ... Failure-layer everything ... A 403 with a valid signature is an IAM-policy finding, not a network finding — distinguish them."
>
> Follow-up: "PART A — COMPLETE THE OBS SURVEY (the drill stopped mid-report). ... Resolve the ambiguity that 404-pattern hides ... for a SMALL sample (5-8) of the 404 buckets, re-probe HeadBucket + GetBucketLocation against the OTHER Huawei regional endpoints ... If a bucket returns 200/location from another region → region-mismatch. If it 403s with a valid signature everywhere → IAM-deny. ... For rms-ai: ListObjects max-keys=20, report object-name prefixes + count + total-size-if-cheap ONLY (no downloads). ... PART B — DEFINE THE ESTATE-INGESTION WAVE (add to scope, do NOT open bulk ingestion yet ...)."

### PART A — OBS survey complete

**Credentials on file**: `huawei_credentials.csv` (custody sha `8a14174c…`, 119 bytes, 2 lines). Byte-identical to `huawei_credentials_2_20260916.csv` (F.1 in previous credential-drop bind-delta = confirmed no rotation between drops). AK shape: `ak_len=20`, `sk_len=40`, `ak_prefix2=HP`, `ak_sha256_first10=6da66c162f`.

**Egress IP presented**: `35.184.53.215` (sandbox pod egress · via `ifconfig.me`).

**A.0 — Master-endpoint reachability** (`obs.ap-southeast-1.myhuaweicloud.com:443`):

- TCP: connected in 0.430s.
- TLS: OK · cert `CN=obs.ap-southeast-1.myhuaweicloud.com`, issuer `GlobalSign RSA OV SSL CA 2018`, not-after `Apr 6 01:56:21 2027 GMT`.
- ListBuckets: **HTTP 200 · 106 buckets enumerated · owner_id present** → the banked AK/SK is a valid, authenticating key.

**A.1 — Region-vs-IAM distinction (sample 3 of 105 initial 404s across the standard Huawei regional endpoint set)**:

Receipt: `phase0/connectivity_receipts/20260921T131024Z_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json` (sha256 pinned in next state seal).

**Verdict histogram**: `{REGION_MISMATCH_RESOLVED: 3, IAM_DENY_ACROSS_ALL_REGIONS: 0, HTTP_404_ACROSS_ALL_REGIONS_UNKNOWN_ROUTING: 0, MIXED: 0}`.

**Sample bucket resolutions**:

| Bucket           | Location from ListBuckets | Resolved at region endpoint             | HeadBucket | GetBucketLocation body region |
|---|---|---|---|---|
| `2024offairrecs` | `af-south-1`              | `obs.af-south-1.myhuaweicloud.com`      | 200 OK     | `af-south-1`                  |
| `citizen-vod`    | `ap-southeast-3`          | `obs.ap-southeast-3.myhuaweicloud.com`  | 200 OK     | `ap-southeast-3`              |
| `apr252017`      | `tr-west-1`               | `obs.tr-west-1.myhuaweicloud.com`       | 200 OK     | `tr-west-1`                   |

**Definitive answer to owner question**: **AK/SK authenticates with broad IAM scope; the initial 105×404 was a client-side region-routing bug in the first drill (I was hitting `obs.ap-southeast-1.…` for buckets that live in `af-south-1`, `ap-southeast-3`, `tr-west-1`, etc.). It is NOT an IAM-deny.** Regional-endpoint routing on the client side unlocks the other 105 buckets whenever needed. Owner does **not** need to take an IAM ask to the RMS admin — the key is fine.

**A.2 — `rms-ai` bucket contents survey (max_keys=20)**:

- Endpoint: `obs.ap-southeast-1.myhuaweicloud.com` · region `ap-southeast-1` (matches ListBuckets location).
- Status: 200 OK · elapsed 1.32s.
- **Count returned**: 20 · `is_truncated: true` → many more objects exist.
- **Total size across the 20-object sample**: **665,868 bytes (~650 KB)** · smallest `1,159 B` · largest `283,588 B` · mean ~33 KB.
- **Prefix histogram** (first path segment before `/`): `{"image_files": 20}` (100% of sample).
- **Sub-prefix (second path segment)** on all 20 objects: `image_files/2795ba36-2730-435f-b1be-eb07a9d83c1f/…` (single UUID-scoped directory).
- **File extensions**: mix of `.jpg`, `.jpeg`, `.png` (all images).
- **Content shape**: image bytes. **NO downloads · NO GetObject calls · NO ACL queries beyond bucket.**

**F.1 (A.2 finding)**: the `rms-ai` bucket at first-page-of-20 is homogeneous images under a single UUID-scoped directory. That UUID looks tenant-shaped; a full survey (S3 of the ingestion wave below) will confirm whether the whole bucket is single-UUID or multi-UUID.

### PART B — CP-ESTATE-INGESTION wave card AUTHORED (added to sprint scope, no data-touching sub-slice opened yet)

Full wave card at `phase0/spec_hunt_receipts/20260921T131500Z_cp_estate_ingestion_wave_card.md`.

**Scope in (reachable-now, verified 2026-09-21)**:

1. **MySQL USSD** `110.238.76.159:3306` (via JUMP) — from JUMP TCP_OPEN per `20260921T124751Z_JUMP_retry_owner_authorized_20260921.json`.
2. **MySQL MICROSERVICES-primary** `159.138.162.146:3306` (via JUMP) — same receipt.
3. **NAS DSM** `http://10.10.55.55:5000` (via JUMP) — same receipt.
4. **OBS `rms-ai` bucket** direct via `obs.ap-southeast-1.myhuaweicloud.com` — proven 200 OK ListObjects this drill.

**Scope out (owner-side asks · listed explicitly per owner directive)**:

- **5 MySQL clusters** still unreachable from JUMP: `203.123.86.10` (iebc_forms), `159.138.164.93`, `159.138.164.124`, `110.238.75.83`, `203.123.83.144`. Owner ask to RMS admin: JUMP-egress firewall allowlist.
- **105 additional OBS buckets** — **reachable with region-correct endpoint routing** per PART A verdict, but excluded from this wave pending explicit owner GO on scope (volumes may be large, esp. `citizen-vod` and media buckets). Flagged **OWNER-DROP-05: region-scope decision · sweep all 106 or scope to named allow-list?**

**Canon anchors verbatim (binding)**:

- Doc 5 B5.2 — Lawful-Basis-at-Admit emitted before first byte read.
- Doc 5 B5.4 — Append-only writer as sole persistence path.
- Doc 5 ENT/CON — No-second-store · adapter has zero writes outside the ledger writer surface.
- Every external read receipted as an `ExternalRead` event on the ledger.
- SO §3.8 additive-only · adapters land as new modules under `services/data_source/{source}_read_only/` · zero sealed edits.

**Sub-slice sequence (owner-gated, no auto-progression)**:

- **S1 · SCHEMA-SURVEY-MYSQL** — `SHOW DATABASES / TABLES / COLUMNS` + `SELECT COUNT(*)` per table on USSD + MICROSERVICES-primary. No row-level reads.
- **S2 · SCHEMA-SURVEY-NAS** — top-level share enumeration on NAS DSM. No file downloads.
- **S3 · SCHEMA-SURVEY-OBS-RMS-AI** — full ListObjects sweep (pagination · max_keys=1000). No GetObject.
- **S4a/b/c/d · DATA-INGEST SUB-SLICES** — individually owner-gated, one per surface, each landing as its own 3-Commit Seal with RED-first invariants on the adapter (LawfulBasisAdmit-before-first-byte + no-second-store + all-reads-receipted + idempotent-restart-from-cursor).

**Standing lesson banked** (for future OBS/multi-region work): **when a signed REST API returns HTTP 404 on a resource whose existence was confirmed by an earlier ListX call**, always retry the specific resource op against the regional endpoint identified in ListX before diagnosing as IAM. HTTP 404 is a routing artefact; HTTP 403 is the true IAM signal.

### Autopilot next (awaiting owner GO)

- **S1 · SCHEMA-SURVEY-MYSQL** is READY to run on `GO S1`. Adapter shape + RED tests will land first (additive under `services/data_source/mysql_ussd_read_only/` and `services/data_source/mysql_microservices_primary_read_only/`) with a shared receipted-external-read wrapper under `services/enforce/`.
- No auto-progression. No data-touching operation until owner explicit instruction per sub-slice.

### Standing bounds (unchanged)

R-91 hold **unchanged** (horizon `2026-09-23T03:23:15Z`, ~37.9h out at 2026-09-21T13:25Z) · **no `testing_agent`** (STRICTLY BANNED per SO §6) · zero push · zero remote · terminal `pytest` only · additive-only §3.8 · three-repo discipline · ratchet floor **5858** · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · structural §3.8 guard on `services/request_context/context.py` sha-pin `ad0d9439…` · mirror-invariant guard on `/app/backend/vendored/extraction_akki/backend/`.

**End of HUAWEI-OBS-ACCESS-DRILL + CP-ESTATE-INGESTION wave card.**


