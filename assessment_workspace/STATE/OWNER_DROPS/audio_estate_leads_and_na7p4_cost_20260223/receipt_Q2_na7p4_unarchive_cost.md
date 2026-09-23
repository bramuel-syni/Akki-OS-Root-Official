# OWNER-Q2 · na7p4* Huawei OBS unarchive cost estimate (fold-in receipt)

**Owner question verbatim (2026-02-23T08:06:00Z):** "Response to the blocked buckets — Those buckets (na7p4374) have the initial data sent to AWS, its backup of our video content. See attached. Could be data you already viewed. There is a cost to unarchive them — what the estimate."

**Owner correction verbatim (2026-02-23T08:09:00Z):** "na7p4* is huawei not AWS." Per correction: `na7p4*` lives on **Huawei OBS TR-Istanbul (`tr-west-1`)**; it holds the **initial video content**; a copy was sent to AWS as backup. Two estates may hold the same content. Label na7p4* as Huawei OBS everywhere. **Scenario C direction corrected: cross-check the readable AWS S3 estate for copies of `na7p4*` (Huawei) content · source from AWS if readable · pay Huawei nothing for unarchive.**

**Handling posture:** HONEST-GAP receipt · measured wherever possible · formulae banked with rate placeholders where pod cannot pin region-specific price · additive-only per SO §3.8.

**Ledger check** — this receipt is a fold-in to the CP-AIP-8-SAMPLING-REFLECTION state-repo touch; it banks measurements + a cost model, not new build. Item 5.8 of EXECUTION_ORDER.md is what is being sealed.

---

## 1 · Enumeration of the na7p4* set (measured)

Source: `phase0/connectivity_receipts/20260922T013648Z_CENSUS3_OBS_full_sweep.json` (full-estate sweep of the currently-authenticated Huawei account · sweep_wall 312 s · `max_list_pages_per_bucket=20`, `max_keys_per_page=1000`).

Filter: bucket-name starts with `na7p4`.

**Aggregate (measured):**

| Metric | Value | Notes |
|---|---|---|
| Bucket count | **38** | All in region `tr-west-1` (Istanbul), endpoint `obs.tr-west-1.myhuaweicloud.com`. |
| Objects (sampled) | **492,877** | Sum of `list.total_objects_scanned` across the 38 buckets. |
| Bytes (sampled) | **102,594,602,226,973 B** | Sum of `list.total_size_bytes` across the 38 buckets. |
| Bytes (decimal TB) | **102.59 TB** | 10^12 base — used for cloud pricing math. |
| Bytes (binary TiB) | **93.31 TiB** | 2^40 base — used for capacity math. |
| Buckets with `more_pages_pending=true` (list capped by the 20-page × 1,000-key sweep cap) | **13 of 38** | **This makes the 492,877 / 102.59 TB figures LOWER BOUNDS.** True totals require a raised page-cap sweep on the 13 specific buckets. |
| GetObject probes total | 190 | 5 per bucket × 38 buckets. |
| GetObject probes returning HTTP 200 | 0 | 100 % HTTP 403 `AccessDenied` at census time (2026-09-21T13:07 → 2026-09-22T01:36Z). |
| Buckets with `content_read_success=true` | **0 of 38** | Baseline: GetObject was blocked account-wide on na7p4* at census time. **Owner console screenshot 2026-02-23 states DIRECT READING FUNCTION IS ALREADY ENABLED on `na7p4374`** — the enablement post-dates the census. Per-bucket direct-read state for the other 37 na7p4* buckets is **unmeasured this seal**. |

**Extension histogram (aggregate, top 10):** `.mov: 242,396`, `.mp3: 119,137`, `.mp4: 37,093`, `.avi: 24,064`, `.jpg: 17,955`, `.txt: 10,426`, `(none): 5,984`, `.html: 4,026`, `.wav: 4,016`, `.docx: 3,053`.

**Content-class rollup (aggregate):** `video: 305,450` · `audio: 124,469` · `other: 21,029` · `image: 20,951` · `doc: 15,184` · `code: 5,713` · `archive: 81`.

**Size distribution (aggregate):** `10-100MB: 216,448` · `1-10MB: 101,373` · `100MB-1GB: 76,621` · `100KB-1MB: 40,945` · `1-100KB: 30,918` · `>=1GB: 14,306` · `<1KB: 8,237` · `0B: 4,029`.

**Per-bucket sample (`na7p4374` — the bucket in the owner screenshot):**

| Field | Value |
|---|---|
| Region | `tr-west-1` (endpoint `obs.tr-west-1.myhuaweicloud.com`) |
| Created | 2024/04/15 02:33:58 |
| list.total_objects_scanned | 7,497 |
| list.total_size_bytes | 3,769,694,138,363 B (3.77 TB decimal) |
| more_pages_pending | **false** (full listing captured on 8 pages) |
| ext_top20 (first 5) | `.mov: 5,074` · `.mp4: 1,413` · `(none): 492` · `.avi: 388` · `.jpg: 51` |
| lm_min / lm_max | 2024/04/15 09:09:57 / 2024/04/15 15:23:40 |
| content_probes | 5 probes · **all HTTP 403 AccessDenied** · errorCode `AccessDenied` · reqIds banked |
| Sample keys (tail 20 chars) | `... 24th/Clip5963_01.mov` (1.55 GB) · `... au Kihara3308_01.mov` (46.4 MB) · `... au Kihara3215_01.mov` (41.1 MB) · `... HEFT/352_3130_01.mov` (348 MB) · `... rame 199680 - 200703` (34.9 KB) |

---

## 2 · Huawei OBS pricing (measured from published pages · rates for cost math)

Rates pinned from `https://support.huaweicloud.com/intl/en-us/price-obs/obs_42_0006.html` + `obs_42_0009.html` + `obs_42_0003.html` (HTTP 200 fetched from pod 2026-02-23T~08:14Z):

| Rate | Value (USD) | Source anchor | HONEST-GAP flag |
|---|---|---|---|
| Archive data restore (standard speed) | **$0.0100 / GB** | `obs_42_0006.html` billing example verbatim: "Archive data restore cost = $0.0100 USD/GB × 10 GB = $0.1 USD" | Generic international-tier example; **not TR-Istanbul-region-pinned** on this page. Region-specific rates in the Huawei console **`Detail Pricing` tab** were not reachable from pod (redirects to calculator SPA). |
| Archive restore request | **$0.0100 / 10,000 requests** | `obs_42_0006.html` verbatim: "Archive restore request cost = $0.0100 USD per 10,000 requests" | Same region caveat. |
| Archive storage | **$0.0045 / GB-month** | `obs_42_0006.html` + `obs_42_0009.html` verbatim | Same region caveat. |
| Temporary Standard-copy (during restore validity window) | **$0.0230 / GB-month** | `obs_42_0003.html` verbatim + `obs_42_0009.html` schedule | Same region caveat. |
| Outbound Internet (busy hours) | **$0.1180 / GB** | `obs_42_0006.html` verbatim: "Outbound Internet traffic cost = $0.1180 USD/GB × 10 GB = $1.180 USD (busy hours)" | Off-peak rate lower; not extracted at this pass. |
| Direct-reading traffic (Archive object read while direct-reading is enabled) | **UNMEASURED — placeholder `$X_dr / GB`** | `obs_42_0006.html` verbatim: "downloading or replicating Archive objects from a bucket with direct reading enabled generates data read traffic. The traffic is billed based on the amount of data retrieved" · no per-GB figure surfaced on this FAQ page | **HONEST GAP** — the direct-reading per-GB rate is quoted only on the region-detail pricing tab which is a JS-rendered calculator SPA not reachable via curl from pod. Formula banked with placeholder; owner or a rendered fetch is required to pin the number. |
| Data-listing / HeadBucket / HeadObject / ListObjects requests | **$0.0001 / 1,000 GET** (Standard-class rate; Archive lists billed the same as Standard per `obs_42_0004.html`) | verbatim | — |

Notes on the rate table:

- **Region-specific pinning HONEST GAP.** Huawei OBS publishes region-differentiated rates via the pricing calculator SPA (`https://www.huaweicloud.com/intl/en-us/pricing/calculator.html`), which returned HTTP 200 but requires client-side JS execution to reveal the TR-west-1 numbers. This pod cannot render JS. The billing examples above are generic international-tier and are used as UPPER-BOUND estimates for the math.
- **Direct-reading rate is the linchpin for Scenario A** and is the one number we could not pin from the FAQ page. Scenario A math therefore carries an explicit placeholder.
- **Range-billing rule for direct-reading:** Huawei OBS charges direct-reading traffic by the amount of data **retrieved** (i.e., the range actually returned) — so a ranged GET of an audio track inside an .mov container is billed by the audio range length, not the whole-object length. Cited from `obs_42_0006.html` CAUTION block: "the amount of data retrieved."

---

## 3 · Three cost scenarios (formula + measured math with explicit CIs / gaps)

### Notation

- `N_obj = 492,877` objects (sampled · **lower bound** — 13/38 buckets have `more_pages_pending=true`).
- `S_bytes = 102,594,602,226,973 B` → `S_GB = 102,594.60 GB` (decimal, per pricing convention).
- `S_TB = 102.59 TB` (decimal).
- `S_audio_only_GB` = audio-track-only bytes across the 38 buckets · **UNMEASURED this seal** (see gap below).
- Rates: `R_restore = $0.0100 / GB`, `R_temp_storage = $0.0230 / GB-mo`, `R_egress = $0.1180 / GB` (busy), `R_direct = $X_dr / GB` (**placeholder**), `R_restore_req = $0.0100 / 10,000 req`, `R_list_req = $0.0001 / 1,000 req`.

### Scenario A — Direct read only what we actually need (owner's console shows direct-reading enabled on `na7p4374`)

**Formula:**
`cost_A = bytes_audio_ranges_actually_read × R_direct  +  list_and_range_requests × R_list_req`

**Math with placeholders:**
- Upper-bound bytes-read = `S_audio_only_GB × R_direct = S_audio_only_GB × $X_dr`.
- Lower-bound bytes-read (audio-classed objects only, ignoring audio tracks inside video files) is unmeasured this seal — the census records the audio content-class count (124,469 objects across the 38 buckets · 25.3 % of `N_obj`) but not the audio-only byte total.

**Illustrative bracket (assuming `X_dr` ≈ `R_egress` ≈ $0.118 / GB — worst-case if direct-reading traffic is priced at Internet-egress parity):**
- If audio-only bytes are ~10 % of total (typical for HD .mov / .mp4 A-track slices at 128 kbps AAC): `S_audio_bytes ≈ 10,259.46 GB` → cost_A ≈ `10,259.46 × $0.118 = $1,210.62`.
- If audio-only bytes are ~5 % (higher-bitrate video with tighter A/V ratio): cost_A ≈ `5,129.73 × $0.118 = $605.31`.

**HONEST GAPS in Scenario A:**
1. `R_direct` is **unmeasured** (FAQ page does not surface a per-GB number; pricing SPA needs JS).
2. `S_audio_only_GB` is **unmeasured** (census recorded audio-object counts, not audio-track byte totals in mixed-video buckets).
3. Direct-reading status is confirmed only for `na7p4374`. The other 37 buckets' direct-reading state is **unmeasured**. If direct-reading is not enabled on all 38 buckets, a restore step is mandatory on those buckets (see Scenario B).
4. Range-billing granularity is stated in the FAQ but not quantified per-request; if Huawei bills a minimum range per request, small-A-track slices could inflate.

**Scenario A is the recommended path if direct-reading is enabled on all 38 buckets AND `R_direct` proves to be at or below `R_egress`.** Its cost scales linearly with bytes actually read — a decisive advantage over Scenarios B or C.

### Scenario B — Standard restore of the whole na7p4* corpus, then egress

**Formula:**
`cost_B = S_GB × R_restore  +  ceil(N_obj / 10,000) × R_restore_req  +  S_GB × R_temp_storage × validity_months  +  bytes_egressed × R_egress  +  list_requests × R_list_req`

**Math with the pinned rates and measured `S_GB = 102,594.60` + `N_obj = 492,877`:**

| Line | Math | USD (LOWER BOUND) |
|---|---|---|
| Archive restore | `102,594.60 GB × $0.0100 / GB` | **$1,025.95** |
| Restore requests | `ceil(492,877 / 10,000) × $0.0100 = 50 × $0.0100` | **$0.50** |
| Temp Standard copy (30-day validity) | `102,594.60 GB × $0.0230 / GB-mo × 1 mo` | **$2,359.68** |
| Restore + copy subtotal | (no egress yet) | **$3,386.13** |
| Full egress to Internet (busy) | `102,594.60 GB × $0.1180 / GB` | **$12,106.16** |
| Restore + copy + full egress | | **$15,492.29** |

**Adjust if egress-to-same-region peer (e.g., pod inside `tr-west-1`) is used:** intra-region traffic is $0 in typical Huawei OBS pricing → cost_B collapses to **$3,386.13** for restore + validity window with no egress fee. This assumes the extractor is co-located in `tr-west-1`, which is a deployment-side decision.

**HONEST GAPS in Scenario B:**
1. Rates are **generic international-tier**; TR-Istanbul-region rates may differ (see §2 above).
2. `N_obj` is a **lower bound** (13/38 buckets have `more_pages_pending=true`). True object count may push restore-request cost up ~2–3× on those specific buckets — negligible at this scale ($0.50 → ~$1.50 worst case) but flagged.
3. `S_GB` is a **lower bound** for the same reason. True total may be ~15–25 % higher on the 13 partial buckets, inflating restore + temp-storage subtotal proportionally.
4. Validity window (`validity_months`) assumed 30 days. Longer validity → linear cost inflation on the temp-copy line.
5. Expedited-restore rate is higher and is NOT quoted here (only standard-speed).

### Scenario C — Zero-restore path via AWS S3 overlap (owner-corrected direction)

**Framing (per owner correction verbatim):** `na7p4*` (Huawei OBS `tr-west-1`) holds the initial video content; a copy was sent to AWS S3 as backup. Every byte already readable on the AWS estate is a byte we never pay Huawei to unarchive.

**Formula:**
`cost_C = (1 - overlap_fraction) × cost_B  +  aws_retrieval_cost(overlap_fraction × S_GB)  +  aws_egress(overlap_fraction × S_GB)`

Where:
- `overlap_fraction` = fraction of `S_bytes` that has a byte-equivalent (or filename+size-equivalent as a proxy) copy on the AWS estate.
- `aws_retrieval_cost` depends on AWS storage-class of the mirror: if AWS Standard/IA, `retrieval_cost = 0` (only egress); if AWS Glacier, standard retrieval is ~$0.01 / GB, Deep Archive standard is ~$0.02 / GB.
- `aws_egress` per AWS pricing ~$0.09 / GB to Internet (first tier), $0 same-region.

**Measured overlap fraction this seal: UNMEASURED — HONEST GAP.**

Building the overlap fraction requires the pod-side occurrence-index (filename + size + optional first-N-bytes hash) crossing the na7p4* census against an AWS S3 census. This session:

- **AWS S3 estate census: NOT executed this seal.** No banked census sweep of AWS S3 exists in `phase0/connectivity_receipts/` matching a name pattern `*S3*ESTATE*` or `*AWS_S3*` for the video-backup mirror. (Present-in-pod: `aws_iam_user_AKIAXGH5.json` credential-shape probe; no full ListObjects sweep of an S3 estate for the na7p4* content mirror.)
- **na7p4* filename manifest: NOT extracted for cross-matching this seal.** The census JSON holds top-20 ext histograms, size-distribution buckets, and 5 sample keys per bucket · not a full filename manifest per bucket. Building a full manifest is an additive census re-invocation (raised page cap · list-only · no reads). Estimated additive cost: same order as the original sweep (~5 minutes wall).

**Two owner-authorised additive follow-ons would pin overlap_fraction:**

1. **RE-INVOKE census on na7p4* with `list_only=true` and raised page cap** → emit full filename+size manifest at `phase0/connectivity_receipts/<ts>_na7p4_manifest_for_overlap.json`. Zero code change (uses sealed CP-CENSUS machinery).
2. **INVOKE census on the AWS S3 estate that holds the backup** → emit full filename+size manifest at `phase0/connectivity_receipts/<ts>_aws_s3_video_backup_manifest.json`. Zero code change. Requires the AWS bucket name(s) from the owner if not already inferable from the banked IAM user JSON.

Then a **local join** of the two manifests on `(basename, size_bytes)` yields overlap_fraction with a confidence interval computed as the Jaccard on the pair. This is a state-side computation, not a build.

**If AWS mirror storage-class is not Standard/IA (i.e., the mirror was lifecycle-transitioned to Glacier or Deep Archive at some point), Scenario C loses its advantage:**
- AWS Glacier Standard retrieval ~$0.01 / GB is **at parity** with Huawei Archive restore $0.0100 / GB.
- AWS Deep Archive Standard retrieval ~$0.02 / GB is **more expensive** than Huawei.
- AWS Glacier Instant Retrieval is $0.03 / GB (higher).
- In those cases, Scenario A (Huawei direct-reading of the ranges we need) becomes the cheapest again.

**Recommendation posture** (banked, not yet actionable):

- **Do not commit to a scenario until overlap_fraction is measured** and AWS mirror storage-class is confirmed.
- If overlap_fraction ≥ 0.90 AND AWS mirror is Standard/IA: **Scenario C** dominates, cost approaches AWS-only egress on 92 TB ≈ $0 same-region or ~$9,200 to Internet.
- If overlap_fraction < 0.50: **Scenario A** is cheapest **iff** `R_direct` ≤ `R_egress` AND direct-reading is enabled on all 38 buckets AND we only need audio ranges (~5–10 % of total bytes) → order-of-magnitude $500–$1,500.
- Fallback: **Scenario B** with intra-region extractor ≈ **$3,386** for restore + 30-day validity, no egress.

---

## 4 · Explicit HONEST-GAP register (this receipt)

| Gap | Effect on estimate | To close |
|---|---|---|
| CAL Huawei account credentials not present in pod | OWNER-Q1 blocked (transcoded-content census not runnable). Not this receipt's scope but noted for the sibling. | Owner supplies AK/SK or bucket policy or signed URL. |
| Direct-reading per-GB rate `R_direct` unmeasured | Scenario A cost carries placeholder | Owner reads region-detail pricing tab / provides current rate; or rendered fetch. |
| Region-specific pricing for `tr-west-1` unmeasured | All scenarios carry generic-tier upper-bound rates | Same as above. |
| Audio-only bytes across mixed-video na7p4* files | Scenario A audio-fraction assumed (5–10 %) | Sample ~50 objects with ffprobe for A-stream size / total size ratio (additive; zero code change; ~1 hour). |
| Direct-reading enabled per-bucket for the 37 na7p4* siblings | Assumed disabled by default; owner confirmed only `na7p4374` enabled | Owner console screenshot or head-bucket probe with new `x-obs-directread` metadata check. |
| `N_obj` / `S_bytes` lower-bound (13/38 buckets more_pages_pending) | All scenarios' cost floors are minimums | Re-invoke sealed census with raised page-cap on the 13 specific buckets. |
| AWS S3 estate census for the na7p4* mirror not banked this session | Scenario C overlap_fraction unmeasured | Additive census invocation as described in §3 Scenario C follow-ons. |
| AWS mirror storage-class per-object unmeasured | Scenario C cost tier unpinned | Same as above (Head or ListObjectsV2 with `--include-attributes StorageClass`). |
| Expedited-restore rate not extracted (only standard) | Scenario B upper bound is under-estimated for expedited flows | Extract from region-detail pricing tab. |

---

## 5 · One-line owner-actionable summary (banked)

- **If a fast, cheap answer is preferred right now:** Scenario B floor = **~$3,386 USD** to restore 102.59 TB of na7p4* on Huawei OBS TR-Istanbul for a 30-day window, no egress (extractor co-located intra-region). This is a LOWER-BOUND at generic-tier rates and does NOT include egress.
- **If minimising cost is preferred and we can wait:** run the two additive Scenario-C-enabling censuses (na7p4* manifest + AWS S3 manifest), compute overlap_fraction, then pick between C, A, B. Estimated additive-work runtime: ~10 minutes wall + owner delivery of AWS bucket name(s) if not inferable.
- **If we know direct-reading is enabled on all 38 na7p4* buckets AND we only need audio ranges:** Scenario A illustrative bracket **$605 – $1,211 USD** at generic-tier rates (contingent on `R_direct` being close to `R_egress`).

---

## 6 · What this receipt does NOT do

- **Does NOT unarchive anything.** Zero writes, zero restores initiated. All figures are estimates.
- **Does NOT extend scope of CP-AIP-8.** Item 5.8 Sampling-and-Reflection compose-boundary is unchanged. This receipt banks measurements at the state-repo touch.
- **Does NOT bind owner to any scenario.** Recommendations are conditional and gap-flagged.

---

## 7 · Standing bounds

- Cadence unchanged (CP-AIP-8 → CP-AIP-9 → CP-AIP-10 sequential · HALT after CP-AIP-10 for full plane completion report).
- Six Standing Bans in force.
- 17 guards in force.
- SPEC-CONFLICT log this receipt: **NONE.**

---

## 8 · Related banked artefacts

- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/DROP.md` (owner drop verbatim).
- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/DROP_CORRECTION.md` (owner correction — na7p4* is Huawei not AWS).
- `STATE/OWNER_DROPS/audio_estate_leads_and_na7p4_cost_20260223/receipt_Q1_viusasa_census.md` (sibling · OWNER-Q1).
- `phase0/connectivity_receipts/20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json` (RMS/AI account access proof).
- `phase0/connectivity_receipts/20260921T131024Z_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json` (region/IAM cross-map · pins na7p4* → `tr-west-1`).
- `phase0/connectivity_receipts/20260922T013648Z_CENSUS3_OBS_full_sweep.json` (source of Section 1 measurements).
- Huawei price-obs FAQ pages (fetched HTTP 200 from pod 2026-02-23T~08:14Z): `obs_42_0003.html` · `obs_42_0004.html` · `obs_42_0005.html` · `obs_42_0006.html` · `obs_42_0009.html` · `obs_42_0011.html`.
