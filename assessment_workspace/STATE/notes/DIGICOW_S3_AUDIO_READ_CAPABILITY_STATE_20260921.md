# DigiCow S3 audio read-capability check — state note (2026-09-21T15:53Z → 15:54Z)

**Trigger**: Owner directive this-session 2026-09-21T~15:47Z verbatim: "OWNER GO → targeted read check: audio in the DigiCow AWS estate, specifically the S3 path s3://training-content-2026/audio/".
**Scope discipline**: **DigiCow AWS S3 ONLY** this run. No touch to RMS Huawei OBS, MySQL clusters, or CIFS archive.
**R-91 hold**: unchanged (~38h). **Ratchet floor**: 5858 (untouched). **Survey-only, no seal, no `testing_agent`, S4 still gated.**

## Cred re-use (no new drop)

Used the DigiCow AWS IAM AK/SK banked from the prior drop:
- `custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv`
- sha256 `d8908b7a32aecc72a66adec46bdcd18dcd893d3419892bd37633463afc7ec366`
- ak_prefix `AKIA…`

## Step 1 · STS identity confirmation

**OK** — same principal as the DigiCow RDS run:
- Account: `494452543252`
- ARN: `arn:aws:iam::494452543252:user/api_user`
- UserId: `AIDAXGH5LB4KEWCKICQOH`

## Step 2 · Region resolution + bucket-level probe

- **Resolved region**: **`eu-west-1`** (via `x-amz-bucket-region` response header on the HeadBucket attempt — botocore surfaced the header even inside the 403 response).
- **HeadBucket (bucket-level)**: **HTTP 403** — informational only.
- **Top-level `ListObjectsV2` (no prefix)**: **HTTP 403 AccessDenied**, with AWS message verbatim: *`User: arn:aws:iam::494452543252:user/api_user is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::training-content-2026" because no identity-based policy allows the s3:ListBucket action`*.

**IAM shape finding**: `api_user` has **no identity-based `s3:ListBucket`**. But the prefix-scoped list DOES succeed (see Step 3). This is the canonical **bucket-policy-with-prefix-condition** pattern — a resource-based ACL on the bucket permits `s3:ListBucket` conditional on `s3:prefix = "audio/*"` (or similar) plus `s3:GetObject` on `arn:aws:s3:::training-content-2026/audio/*`. The 403 on top-level list is by design; the audio prefix is the "carve-out".

## Step 3 · List `audio/` prefix (bounded)

`ListObjectsV2(Prefix="audio/", MaxKeys=50)` × 20 pages = **1000 keys enumerated** (still truncated at the tool's `LIST_PAGES=20` cap — the actual prefix contains more).

| metric | value |
|---|---|
| pages walked | 20 (cap; `IsTruncated=True` at final page → more objects exist beyond page 20) |
| keys read within bound | **1000** |
| bytes summed within bound | **11,748,395,917** (~10.94 GiB across the first 1000 keys) |
| fully enumerated within bounds | **False** — MORE data exists beyond this window |
| **audio object count within bound** | **768** (762 `.mp3` + 6 `.wav`) |
| ext histogram within bound | `mp3=762 · mp4=132 · jpg=58 · png=27 · jpeg=13 · wav=6 · NOEXT=1 · mpeg=1` |
| LastModified date range within bound | `2026-09-21 05:26:11Z` → `2026-09-21 06:49:38Z` (**a single-batch upload earlier today**) |
| key naming pattern | `audio/{long-numeric-id}.{ext}` (numeric-id keys, digits only) |

**Content mix under the `audio/` prefix**: mostly audio (mp3 + wav = 768/1000 = **76.8 %** of the walked window), but also includes 132 mp4 (video or audio-in-mp4 container), 98 image files (jpg+png+jpeg — likely cover art/thumbnails), 1 mpeg (also audio), and 1 no-extension file. **The prefix is a mixed asset store dominated by audio; it is not exclusively audio.**

## Step 4 · Proof-of-read (smallest audio in walked window)

**Chosen object**: `audio/16427811311826438146.mp3` (147,122 B ≈ 147 KB, LastModified `2026-09-21 06:48:12Z`).

- **HeadObject** result:
  - `ContentType`: **`audio/mpeg`** ← S3 metadata confirms audio.
  - `ContentLength`: 147,122 B
  - `ETag`: `1f83a2f4a32d3d3cdd6c9a63e34b0478`
  - `StorageClass`: (null → STANDARD)
  - elapsed: 0.118 s
- **GetObject Range `bytes=0-15`** (16 bytes read total):
  - `ContentRange`: `bytes 0-15/147122`
  - `ContentType`: `audio/mpeg`
  - Bytes returned: 16 (as requested)
  - elapsed: 0.155 s
- **Magic signature (hex, first 16 bytes)**: `fffa9260c1270000040c32c54b1862d0`
- **Inferred format**: **MP3/MPEG raw frame** — the first two bytes are `0xFF 0xFA`, i.e. the classic MP3 frame sync `11111111 111110xx` (11 bits set + MPEG version bits). No ID3 tag prepended.
- **is_audio**: **TRUE** — audio content confirmed end-to-end with a 16-byte read.

## Step 5 · Top-level discovery

- `ListObjectsV2(Delimiter="/")` at bucket root → **HTTP 403 AccessDenied** (same policy shape as noted).
- Cannot enumerate sibling prefixes at the bucket root with the current AK/SK. If additional prefixes exist alongside `audio/`, the owner would need to name them (or grant list-at-root) for us to enumerate them.

## Step 6 · Verdict (verbatim)

- **Binary**: **YES**.
- **Surface**: `AWS S3 bucket 'training-content-2026' · region=eu-west-1`.
- **Counts (within the 20-page × 50-key walk cap of 1000)**: 768 audio objects (`mp3` + `wav`); ~10.94 GiB total bytes across all 1000 keys walked. `IsTruncated=True` → more objects exist beyond the cap.
- **Formats observed**: `mp3` (762), `wav` (6). MP3 dominates by more than two orders of magnitude.
- **Proof-of-read**: succeeded end-to-end on `audio/16427811311826438146.mp3` via 16-byte range GET → magic `0xFFFA…` → confirmed MP3/MPEG audio.
- **Failure layer**: **none** for the audio target.

**Content is READABLE** in DigiCow's S3 estate under `s3://training-content-2026/audio/`.

## Receipts + state note banked

- `phase0/connectivity_receipts/20260921T155411Z_DIGICOW_s3_audio_read_check_owner_authorized_20260921.json`
- `STATE/notes/DIGICOW_S3_AUDIO_READ_CAPABILITY_STATE_20260921.md`
- Tool: `tools/digicow_s3_audio_read_check_20260921.py`

*(Prior 20260921T155333Z receipt was superseded 78 s later after removing a HeadBucket 403 short-circuit that mis-blocked prefix-scoped IAM.)*

## Notable findings

1. **Bucket-policy-with-prefix-condition IAM pattern.** The api_user has no identity-based `s3:ListBucket` (AWS diagnostic message is explicit about this). The resource-based bucket policy carves out `s3:prefix="audio/*"` — that's why bucket-level ops (`HeadBucket`, `GetBucketLocation`, root-`ListObjectsV2`) return 403 while prefix-scoped list + GetObject on `audio/*` work. **Do not treat HeadBucket 403 as a fatal signal for future prefix-scoped IAM patterns.**
2. **The 1000-key window is capped, not complete.** `IsTruncated=True`. The actual audio object count is > 768; a full paginated count would require lifting `LIST_PAGES=20`. Not run this pass per owner's "cheap paginated count" bound.
3. **Single-batch upload signature.** All 1000 keys walked have LastModified between `2026-09-21 05:26Z` and `06:49Z` — approximately 84 minutes of continuous uploads earlier today. Suggests an operational ingest that landed just before this drop was issued. Worth noting for provenance.
4. **Numeric-id key naming**: `audio/{long-numeric-id}.{ext}`, e.g. `audio/16427811311826438146.mp3` — the IDs look like 64-bit-ish snowflake/timestamp IDs. Might correlate to DB row IDs in `digicow_live` / `ndume` — worth checking if the owner wants training-material provenance mapping.
5. **`audio/` prefix is mixed content**, not exclusively audio: 132 mp4, 98 jpg/png/jpeg, 1 mpeg, 1 NOEXT. Might be an integrated "training content pack" (audio + video + cover art). Recorded for context.

## Hygiene tally

- Read-only. **Zero bulk downloads.** Exactly one 16-byte range GetObject.
- AWS IAM AK/SK held in memory only; shape only recorded.
- Object bytes hashed via ETag/HTTP headers only; the 16-byte body was inspected for magic signature and reported as **hex + inferred format** — never the audio content itself.
- Custody file sha pinned in receipt.
- No `testing_agent`, no seal, no code changes to production tree.

## Standing bounds — all unchanged

- R-91 hold intact (~38h to `2026-09-23T03:23:15Z`).
- Ratchet floor 5858 unchanged.
- §3.8 additive-only intact.
- S4 bulk ingestion gated.
- No follow-up sweeps triggered by this run.

## Standing admin asks (updated)

| ask | status |
|---|---|
| MySQL `159.138.162.146` creds | still missing |
| MySQL `HOST` placeholder (WEEGO) → IP | still open |
| Huawei OBS `obs:object:GetObject` scope | still open |
| NAS DSM/SMB direct creds (nice-to-have) | still open; CIFS mount holds |
| DigiCow RDS estate | CLOSED (prior drop) |
| **DigiCow S3 audio (`training-content-2026/audio/`)** | **CLOSED by prefix-scoped bucket policy** — audio readable, MP3 confirmed end-to-end |

(If audio content beyond `audio/` prefix is needed, the owner would need to either name the additional prefix or grant bucket-root `s3:ListBucket` on the api_user IAM identity.)

— end of state note.
