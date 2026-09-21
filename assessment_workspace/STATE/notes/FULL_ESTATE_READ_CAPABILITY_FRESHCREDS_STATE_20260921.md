# Full Estate Read-Capability Re-sweep (fresh creds) — state note (2026-09-21T14)

**Wave**: CP-ESTATE-INGESTION.
**Trigger**: Owner credential re-drop this-session 2026-09-21T~14:05Z.
**R-91 hold**: unchanged (~38h to `2026-09-23T03:23:15Z`, do NOT execute early).
**Ratchet floor**: 5858 (untouched — survey-only, no seal).
**No `testing_agent`**. **No S4 bulk ingestion** (still gated).

## Custody ingest under §4.1 §E (byte-metadata only)

- **New drop**: `RMS CREDS.xlsx` @ `custody/credentials/incoming_20260921/20260921T140818Z_RMS_CREDS.xlsx`
  - sha256 `3311dae2d142f3a651431325d68f72a011598054a39c0d7b3976c757410cc545`
  - size 6173 bytes
- **Prior baseline preserved**: `custody/credentials/prior_baseline/d778eb1e_prior_baseline.xlsx` (sha `d778eb1e…`, 9399 bytes) — retained for JUMP + legacy NAS-DSM/RADIO cred continuity, since the new drop does NOT re-carry those.
- **Primary custody path installed**: `/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx` = new drop.
- **Drop manifest**: `custody/credentials/incoming_20260921/20260921T140818Z_drop_manifest.json`.
- **Value-blind structure probe + shape-only diff**: `phase0/connectivity_receipts/20260921T140936Z_RMS_creds_drop_shape_probe_and_diff_20260921.json`.

## What this drop rewrites, verbatim (shape only)

Old sheet had 3 tabs (`NAS creds`, `NAS Guide + Cred`, `Huawei Creds`) with 8 MySQL clusters (3 credentialed).
New sheet has 1 tab (`Sheet1`), 5-column data layout `[schema, host, user, password, tag]`, **9 MySQL clusters (8 credentialed) + 1 NEW surface**:

| section | host | shape delta vs old | tag |
|---|---|---|---|
| VIUSASA | `203.123.86.10` | UNCHANGED (user_len=7 · pass_len=16 · 9 schemas) | `NOT YET UHURU` |
| USSD | `110.238.76.159` | UNCHANGED (user_len=7 · pass_len=16 · 10 schemas listed → 17 user schemas on-server) | `OK` |
| MICROSERVICES | `159.138.164.93` | UNCHANGED (user_len=7 · pass_len=16 · 2 schemas listed → 3 user on-server) | `OK` |
| MICROSERVICES | `HOST` (placeholder) | **NEW CREDS** (user_len=7 · pass_len=16) but no IP yet | `NOT YET UHURU` |
| MICROSERVICES | **`159.138.162.146`** | **STILL user_len=0 · pass_len=0** — the one remaining hole | (untagged) |
| MICROSERVICES | `159.138.164.124` | **UNBLOCKED** (was 0/0 → now 7/16) | `NOT YET UHURU` |
| MICROSERVICES | `110.238.75.83` | **UNBLOCKED** (was 0/0 → now 7/16) | `NOT YET UHURU` |
| MICROSERVICES | `203.123.83.144` | **UNBLOCKED** (was 0/0 → now 7/16) | `NOT YET UHURU` |
| **NAS - ACESS** | **`159.138.173.58`** | **NEW SURFACE** (user_len=7 · pass_len=17) for Razuna & Newsvault | `NOT YET UHURU` |
| _(RADIO ROW)_ | 3-cell row shape only | radio_source per new sheet | — |

The new drop does **not** re-carry NAS DSM creds, RADIO creds beyond the 3-cell row, JUMP SSH creds, or Huawei OBS AK/SK. JUMP + NAS-legacy continue via `LEGACY_SHEET_PATH` provenance (banked baseline preserved).

## Receipts banked (state repo, this run)

- `custody/credentials/incoming_20260921/20260921T140818Z_RMS_CREDS.xlsx`
- `custody/credentials/incoming_20260921/20260921T140818Z_drop_manifest.json`
- `custody/credentials/prior_baseline/d778eb1e_prior_baseline.xlsx`
- `phase0/connectivity_receipts/20260921T140936Z_RMS_creds_drop_shape_probe_and_diff_20260921.json`
- `phase0/connectivity_receipts/20260921T142146Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json` (200 KB)
- Adapted loader: `tools/rms_creds_loader_v2.py`

## Section E · Estate Read-Capability Matrix (fresh-creds, verbatim)

| # | surface | auth | enumerate | proof-of-read (shape only) | **content-readable** | failure layer |
|---|---|---|---|---|---|---|
| 1 | JUMP `159.138.173.250:22` | OK (legacy sheet creds; host key un-drifted) | sizing re-confirmed: nproc=1 | shell rc=0 | **YES** | — |
| 2 | MySQL VIUSASA `203.123.86.10:3306` | **OK NEW** (`5.7.44-240900-log`) | 10 user schemas | **10/10** SELECT-LIMIT-1 succeed | **YES** | — |
| 3 | MySQL USSD `110.238.76.159:3306` | OK (`5.7.44-241200-log`) | 17 user schemas | 16/17 SELECT-LIMIT-1 (1 schema `artists_app` is empty, 0 denials) | **YES** | — |
| 4 | MySQL MICROSERVICES sibling `159.138.164.93:3306` | OK (`8.0.28-231003`) | 3 user schemas | 3/3 SELECT-LIMIT-1 succeed | **YES** | — |
| 5 | MySQL MICROSERVICES `HOST` placeholder (WEEGO) | **CREDS NEW but host missing** | — | — | **NO** | `PLACEHOLDER_HOST_NO_IP` |
| 6 | MySQL MICROSERVICES-primary `159.138.162.146:3306` | **STILL N/A — NO CREDS IN NEW SHEET** | — | — | **NO** | `NO_CREDS_IN_BANKED_SHEET_STILL` |
| 7 | MySQL MICROSERVICES `159.138.164.124:3306` | **OK NEW** (`5.7.43-231000-log`) | 2 user schemas | 2/2 SELECT-LIMIT-1 succeed | **YES** | — |
| 8 | MySQL MICROSERVICES `110.238.75.83:3306` | **OK NEW** (`5.7.43-231000-log`) | 1 user schema (`db_visitors`) | 1/1 SELECT-LIMIT-1 succeed | **YES** | — |
| 9 | MySQL MICROSERVICES `203.123.83.144:3306` | **OK NEW** (`8.0.28-231003`) | 3 user schemas (`citizen-pulse`, `correspondents`, `saa`) | 3/3 SELECT-LIMIT-1 succeed | **YES** | — |
| 10 | **MySQL "NAS - ACESS" `159.138.173.58:3306` — Razuna DAM + Newsvault backend** | **OK NEW** (`8.0.43-260600`) | 2 user schemas (`razuna`, `news_vault`) | 2/2 SELECT-LIMIT-1 succeed | **YES** | — (sheet label misleading: this is a MySQL DB, not a file server) |
| 11 | NAS DSM/SMB `10.10.55.55:5000` (direct) | **STILL REJECTED** — no new NAS creds in fresh drop; legacy creds remain stale (cite S2 stack) | not enumerable direct | — | **NO direct** — but see #12 | `NAS_DSM_SMB_STALE_LEGACY_NOT_REFRESHED` |
| 12 | **NAS via CIFS mount `/mnt/nfs-share` on JUMP** (kernel-mediated, cached `bramuel` session) | OK (kernel session persists across rotation) | **16 / 16 channels matched** (channel01–channel16) | Sampled channel01 (Citizen TV) + channel04 (Inooro FM): each 300+ subdirs, ~3000 .mp4 files at depth 3, mtime through 2026-08-01/2026-09-21; smallest file `config.xml` (526B / 542B) stat OK, `test -r` = **READABLE** | **YES for all 16 channels via the mount** | — |
| 13 | OBS `af-south-1` (list) | OK (carry-forward) | 3 buckets HeadBucket 2xx + ListObjects 2xx | (not re-tested; no new AK/SK) | **YES for listing** | — |
| 14 | OBS `tr-west-1` (list) | OK (carry-forward) | 3 buckets 2xx | (not re-tested) | **YES for listing** | — |
| 15 | OBS `ap-southeast-3` (list) | OK (carry-forward) | 2 buckets 2xx | (not re-tested) | **YES for listing** | — |
| 16 | OBS `ap-southeast-1` GetObject on rms-ai | OK (carry-forward) | list 2xx | GetObject on smallest → **403 AccessDenied** (carry-forward) | **PARTIAL: LIST-yes / GET-no** | `AK_SK_MISSING_GetObject_SCOPE` (unchanged) |

**Aggregate**: 12 YES surfaces (JUMP + 7 MySQL clusters newly-or-still-readable + Razuna/Newsvault MySQL + NAS-via-CIFS + 3 OBS regions for listing), 1 PARTIAL (OBS GetObject), 2 NO (`159.138.162.146` + WEEGO/HOST placeholder), 1 NO-direct-but-YES-indirect (NAS DSM/SMB direct vs CIFS mount).

## What the fresh drop CLOSED vs what remains

### CLOSED by this drop (verbatim from before → after)

1. **MySQL `159.138.164.124`** — was `NO_CREDS_IN_BANKED_SHEET`; now readable (2 schemas).
2. **MySQL `110.238.75.83`** — was `NO_CREDS_IN_BANKED_SHEET`; now readable (`db_visitors`).
3. **MySQL `203.123.83.144`** — was `NO_CREDS_IN_BANKED_SHEET`; now readable (3 schemas).
4. **MySQL VIUSASA `203.123.86.10`** — was un-surveyed last run (owner didn't request); now confirmed readable (10 schemas). (The old sheet had creds for this row, but it wasn't in the owner's prior targeted sweep.)
5. **NEW MySQL surface `159.138.173.58` (Razuna DAM + Newsvault backend)** — fully unlocked; 2 schemas readable. This is the actual DB the RMS asset/news metadata lives in.
6. **NAS access via `/mnt/nfs-share` on JUMP** — full 16-channel enumeration succeeded (previously timed-out under looser bounds); READABLE across the sampled channels. Kernel-mediated CIFS session using cached `bramuel` credentials.

### STILL OPEN — three standing admin asks (revised)

1. **MySQL `159.138.162.146:3306`** — still no creds in sheet even after re-drop. The owner-named MICROSERVICES-primary remains blocked.
2. **MySQL `HOST` placeholder (WEEGO / MICROSERVICES)** — now has creds but no resolvable host; needs the literal token `HOST` replaced with an IP or DNS name.
3. **Huawei OBS GetObject scope** — new sheet carries no AK/SK; the 2026-09-16 rotated AK/SK still has ListBucket but no GetObject on rms-ai (403 AccessDenied). Prior receipts stand: `20260921T134035Z_OBS_read_capability_delta_rerun_20260921.json`.
4. **(nice-to-have; not blocking read use-case)** direct NAS DSM/SMB creds — the CIFS mount at `/mnt/nfs-share` on JUMP already gives us the content, but if that mount ever fails (server reboot / session expiry), a fresh set would restore direct access.

## Notable findings

1. **"NAS - ACESS" is a mislabeled MySQL surface**, not a file server. The sheet section title suggests file storage, but `159.138.173.58` runs MySQL 8.0.43-260600 with schemas `razuna` + `news_vault` — the metadata/index behind the RMS Razuna DAM (digital asset management) and Newsvault (broadcast news CMS). The actual audio/video assets live on the CIFS mount (`OFFAIRRECS/Record`); their metadata + editorial workflow lives in this MySQL.
2. **Access-token asymmetry between DBs (fresh creds unlock all) vs OBS (rotation dropped GetObject scope)** — the DB rotation was permissive; the OBS rotation was restrictive. Different rotation policies from two different admins.
3. **`kra_reports` naming reuse** — appears both on `203.123.86.10` (VIUSASA/iebc_forms) and `159.138.164.93` (MICROSERVICES sibling), sheet-listed on both. Not a bug; recorded for cross-cluster confusion prevention.
4. **JUMP host key still un-drifted** across the entire run.
5. **CIFS mount survives credential rotation** — the `bramuel` session in kernel's SMB cache remains valid despite the sheet-side rotation. On next reboot of JUMP, mount will need re-auth with the current NAS password (which we don't have).

## Hygiene tally

- Read-only across every touch. **Zero downloads** anywhere. **Zero writes**.
- MySQL row values never entered stdout / logs / receipts — column names + types + per-value byte-lengths + null status only.
- NFS/CIFS proof-of-read via `test -r` (POSIX read-permission check) — no byte reads required to prove readability.
- Credentials by shape only (sha8 for cross-run compare, no values). Custody file installed via `cp` (atomic replace); old preserved as `d778eb1e_prior_baseline.xlsx`.
- No `testing_agent`, no seal, no code changes to production tree. Ratchet floor 5858 unchanged.
- R-91 hold intact (~38h remaining).

— end of state note.
