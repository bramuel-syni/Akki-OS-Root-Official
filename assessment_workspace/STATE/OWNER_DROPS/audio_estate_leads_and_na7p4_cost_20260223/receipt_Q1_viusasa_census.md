# OWNER-Q1 · Viusasa `transcoded-content` census (fold-in receipt)

**Owner question verbatim (2026-02-23T08:06:00Z):** "More leads to where audio is — On **CAL Huawei account**, On viusasa — there is a bucket `transcoded-content`, folder `MUSIC` and `MUSIC-AUDIO`."

**Handling posture:** HONEST-GAP receipt · measured wherever possible · pod credentials/network limits recorded verbatim · additive-only per SO §3.8.

**Ledger check** — this receipt is a fold-in to the CP-AIP-8-SAMPLING-REFLECTION state-repo touch; it banks measurements, not new build. Item 5.8 of EXECUTION_ORDER.md is what is being sealed.

---

## 1 · Credential inventory (measured)

Pod-side estate keys inventoried at `/app/backend/estate_keys/data_sources/`:

| File | Size | Purpose (from filename) | Notes |
|---|---|---|---|
| `huawei_credentials.csv` | 119 B | Huawei OBS AK/SK · **AK prefix `HP` · length 20 · SK length 40** | Byte-identical to alt file (per prior receipt `20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json`). |
| `huawei_credentials_2_20260916.csv` | (same) | Alt Huawei OBS AK/SK | Byte-identical to above (banked sha256 `8a14174c6a5167cb7fb2f8877b4c3b3ed2d1eed7540aeab0fc4f654457698667`). |

**Ownership scoping (measured against the account those creds resolve to):** running `ListBuckets` returned **106 buckets** with owner_id present (HTTP 200 OK · endpoint `obs.ap-southeast-1.myhuaweicloud.com` acting as master). The bucket list contains RMS-domain buckets (`newlibrary-*`, `citizen-*`, `news-vault`, `music-bucket-rms`, all `na7p4*`, etc.) and test-viusasa variants. **No bucket named `transcoded-content` is present in the returned list.**

**HONEST GAP #1 · CAL Huawei account credentials NOT PRESENT in pod estate keys.** The owner statement specifies the **CAL Huawei account** for the `transcoded-content` bucket. The AK banked in `huawei_credentials.csv` resolves to a Huawei account whose ListBuckets output does NOT include `transcoded-content`, and the master endpoint used is `obs.ap-southeast-1.myhuaweicloud.com`. Direct probing of the CAL account cannot be performed from this pod at this seal boundary. Nothing named CAL is discoverable in credential filenames or in the currently-visible bucket list.

Requested: owner ledger action supplying an AK/SK for the CAL Huawei account (or a bucket policy grant on `transcoded-content` reachable from the RMS/AI account credentials already banked).

---

## 2 · Viusasa-labelled buckets observable on the currently-authenticated Huawei account (measured)

Extracted from banked full-estate sweep `phase0/connectivity_receipts/20260922T013648Z_CENSUS3_OBS_full_sweep.json` (sweep_id `CENSUS3-OBS-FULL-SWEEP-20260922T013000Z`; sweep_wall 312 s; ListObjects paged with `max_keys=1000`, `max_list_pages_per_bucket=20`).

| Bucket | Region | Created | list.total_objects | list.total_size_bytes | more_pages_pending | ext_top20 first 3 | content_read_success |
|---|---|---|---|---|---|---|---|
| `viusasanews` | `af-south-1` | 2024/03/21 13:28:58 | `null` | `null` | `null` | (not populated) | `null` |
| `test-viusasa-bucket` | `af-south-1` | 2024/10/03 09:16:07 | **648** | **1,091,514,572** (1.09 GB) | false | `.ts:582 .jpeg:24 .webp:16` | false (HTTP 403 on probes) |
| `test.test-viusasa-bucket` | `af-south-1` | 2024/10/16 15:28:38 | **0** | 0 | false | (empty) | n/a |
| `upload.test.test-viusasa-bucket` | `af-south-1` | 2024/10/17 14:47:48 | **0** | 0 | false | (empty) | n/a |
| `uploads.test-viusasa-bucket` | `af-south-1` | 2024/10/16 15:19:44 | **0** | 0 | false | (empty) | n/a |

**Findings observed:**

1. `viusasanews` returns `null` for `list.total_objects` / `list.total_size_bytes` in the census (i.e., ListObjects did not return a populated page for this bucket at census time — the census sweep classified it as `head_ok` yet listed no objects, or list failed silently; **exact failure_layer is not captured** for this bucket in the current sweep JSON).
2. `test-viusasa-bucket` holds 648 objects (1.09 GB), extension mix dominated by `.ts` (582) + `.jpeg` (24) + `.webp` (16) + `.jpg` (12) + `.m3u8` (7) — this is an **HLS-segment video test bucket**, not the `MUSIC` / `MUSIC-AUDIO` folder pattern the owner describes.
3. Three of the four viusasa buckets on this account are empty test buckets.
4. **The `transcoded-content` bucket named by the owner is not visible on this account.** It is on the CAL Huawei account per owner statement.

---

## 3 · MUSIC-adjacent evidence on the currently-authenticated Huawei account (measured)

Only bucket carrying the string `music` in its name is `music-bucket-rms`:

| Bucket | Region | Created | list.total_objects (sampled) | list.total_size_bytes (sampled) | more_pages_pending | ext_top20 first 5 | content_read_success |
|---|---|---|---|---|---|---|---|
| `music-bucket-rms` | `af-south-1` | 2024/03/21 12:14:58 | **20,000** (sample cap) | **566,299,752,249** (~566.30 GB sampled · **LOWER BOUND**) | **true** (more pages beyond 20-page cap) | `.mp4:15677 .flx:1086 .rpt:610 .mp3:508 .frm:331` | **true** (GetObject succeeded on this bucket) |

Observations:

- 20,000 objects were sampled before the census hit the 20-page × 1,000-key cap; `more_pages_pending` is true, so **the true object count and byte total are unmeasured beyond the sampled 20,000 / 566.30 GB**.
- Extension mix reveals this bucket is a mixed-video-and-legacy-DB dump (`.flx .rpt .frm .fd .tag .dat .cab .xls` are legacy FoxPro-family / database formats), not a clean audio-library layout. Music-classed audio present: `.mp3 : 508` samples out of 20,000 (2.5 %) plus an `audio` content-class rollup of 510 samples.
- `content_read_success: true` — this bucket is readable with the currently-banked keys. GetObject works. (Contrast with the na7p4* group: 0/38 GetObject probes succeeded.)

**HONEST GAP #2 · `music-bucket-rms` is unmeasured beyond the census sample cap.** A full census (raising `max_list_pages_per_bucket` above 20 or removing the cap) would be needed to state the true object count and byte total. Not run at this seal boundary — that is a census-machinery invocation and is outside the Item 5.8 scope (SO §7 guard 5 · anti-drift).

---

## 4 · What answering OWNER-Q1 requires the owner to authorise

To perform the requested `transcoded-content` census (bucket on the CAL Huawei account, folders `MUSIC/` and `MUSIC-AUDIO/`), one of the following must happen additively (no code change · uses sealed census machinery in `services/audio_plane_v1/`):

1. **Owner supplies CAL Huawei account AK/SK** → banked at `/app/backend/estate_keys/data_sources/huawei_credentials_cal.csv` (name suggestion; owner chooses) with a manifest receipt at `phase0/owner_drop_manifests/`. Then rerun the sealed census sweep against the CAL account with prefix filter `MUSIC/` and `MUSIC-AUDIO/`.

2. **OR owner adds a bucket policy on `transcoded-content`** granting `ListObjects` (and optionally `GetObject`) to the RMS/AI AK banked here. Then rerun the sweep from this pod with prefix filters.

3. **OR owner supplies a signed URL / temporary IAM role** for the `transcoded-content` bucket. Sweep proceeds under that principal.

**Estimated additive work once authorised:** invoke sealed census sweep with prefix filter; produce a census receipt banked at `phase0/connectivity_receipts/`. Zero new services. Zero code edit. Sealed CP-CENSUS machinery composes with §1.2.

---

## 5 · What this receipt does NOT do

- **Does NOT extend scope.** OWNER-Q1 is a lead-follow; CP-AIP-8 is Sampling & Reflection compose-boundary. This receipt is banked at the state-repo touch of CP-AIP-8's Commit-B and lives under `STATE/OWNER_DROPS/`, not under `phase0/cp_aip_8_.../`. Item 5.8 of `EXECUTION_ORDER.md` is what the seal implements.
- **Does NOT assert CAL access.** Section 1 declares HONEST GAP #1 (no CAL creds). The follow-on census is contingent on owner ledger action.
- **Does NOT assert music-bucket-rms totals.** Section 3 flags HONEST GAP #2 (sample-cap lower bound).

---

## 6 · Standing bounds

- Cadence unchanged (CP-AIP-8 → CP-AIP-9 → CP-AIP-10 sequential · HALT after CP-AIP-10 for full plane completion report).
- Six Standing Bans in force.
- 17 guards in force.
- SPEC-CONFLICT log this receipt: **NONE.**

---

## 7 · Related banked artefacts

- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/DROP.md` (owner drop verbatim).
- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/DROP_CORRECTION.md` (owner correction — na7p4* is Huawei not AWS).
- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/receipt_Q2_na7p4_unarchive_cost.md` (sibling · OWNER-Q2).
- `phase0/connectivity_receipts/20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json` (RMS/AI account access proof).
- `phase0/connectivity_receipts/20260921T131024Z_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json` (region/IAM cross-map).
- `phase0/connectivity_receipts/20260922T013648Z_CENSUS3_OBS_full_sweep.json` (full-account census sweep of the RMS/AI Huawei account · source of Section 2 + 3 numbers).
