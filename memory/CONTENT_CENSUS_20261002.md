# Content census — tiered design (owner ruling 2026-10-02 evening)

## Ruling
Owner answered 1-a, 2-a, 3-a, 4-a and added: "Try sample per folder, a bigger sample. Be surgical so we can have a high
probability of truth." Context disclosed before the ruling: OBS endpoint `obs.af-south-1` is public → every byte read is
internet egress billed to RMS (~$0.10/GB assumed); the NAS path runs through the RMS jump host (SFTP) and the estate uplink.
Full byte-for-byte read (`content_full`) stays available as tier 3; it is NOT running now.

## What runs (measurement `content_sample`, native `census_autonomy` engine)
- `deep_content.py` orchestrator: listing (35 % of run) → header probes (to 65 %) → planned reads on `readers_per_gpu` (6) processes per
  GPU → `deep_sample.summarize_label`. Lock `.content.lock` per source on the host state dir (`/mnt/volume_dkgjrkx/akki-census-content`).
- `deep_sample.py`: `stratify` (folder strata, cap 120/store, split >1500 files to depth 4, year split, kind×year for hash-named stores),
  seeded nested sample order `sha256('akki-content-census-sample-v1|ref')`, `probe_header` (head 96 KiB + tail 384 KiB sparse file →
  ffprobe; mp3 basis vbr_header/bitrate_extrapolated; moov escalation 8 MiB), `plan_scope` (small folders ≤60 read whole; others ∝ hours,
  floor 30, cap 600; top-up ×2 to 1500 when speech-share half-width > 5 pts), ratio estimators with FPC (Taylor SE), `combine` in quadrature.
- Budgets (backend/.env): OBS 40k + 20k top-up files, NAS 8k + 4k; header sample 300/folder for video, every audio file probed.
- NAS reads only in `CENSUS_NAS_READ_WINDOW_UTC=17-03` (20:00–06:00 EAT); listing/headers any hour, 4 threads. Successor run sleeps via
  `resume_not_before` → `not_before` (operational_runner.continue_if_resumable).
- Busy re-entry back-off 300 s (`CENSUS_BUSY_RETRY_SECONDS`).

## Runs dispatched 18:22 UTC
- `cr-bbf71c8d905a` OBS-A (29 buckets incl. skizaaudio) on akki-vm; `cr-68be8ecf670a` OBS-B (8 buckets) on akki-vm-ii;
  `cr-8640b1cbcbc6` NAS (16 shares) on akki-vm-ii. Chains continue via BUDGET_EXHAUSTED successors until `estimated`.
- Superseded content_full chain cancelled: cr-2d1e7c55e63e marked SUPERSEDED_BY_OWNER_RULING; remote passes killed (REMOTE_WORKER_FAILED).

## Lessons
- `pkill -f <pattern>` over SSH kills the invoking shell when the pattern matches the command line → use `patter[n]`.
- "HTTP 403 error code: 1010" on the preview URL = Cloudflare bot rule rejecting python-urllib's User-Agent, NOT an OBS permission
  problem. Use curl (or a browser UA). The OBS blocked buckets are NoSuchBucket (36) / ClientError (4).
- A census_scheduler restart orphans in-flight SSH passes (they keep writing durable rows but the receipt is lost and the lock stays
  held until their deadline). Stop remote passes first (`pkill -f "akki-census-cod[e]"`), then restart.
- Scale: OBS ≈1.06 M audio + ≈3.5 M video objects (2024offairrecs 3.13 M video / 86 TiB), NAS ≈1.5 M video + 15 k audio. Header pass
  measured ≈250 files/s per host.

## 3 Oct 2026 — first receipts, the access wall, and the owner's redirection
- **OBS object reads are refused on 15 buckets** (`2024offairrecs` 3.18 M media, every `na7p…` bucket, `elections-portal`): LIST works,
  HEAD/GET → 403 AccessDenied; verified from the pod with a one-byte probe (same account id owns the objects; get_bucket_acl/policy also
  denied → restricted IAM user). That is 4.17 M of 4.6 M listed OBS media files (90.7 %), 120.7 TiB. Fix is on the owner's Huawei account:
  `obs:object:GetObject` for the census key on those buckets. Two buckets (`test-viusasa-bucket`, `fast-channels`) are Archive class without
  direct read → InvalidObjectState (restore needed). Nearly every OBS object is storage class GLACIER (Huawei Archive); `music-bucket-rms`
  and the OBS-B buckets read directly (direct-read retrieval fee applies on top of egress — not priced).
- **Readable OBS measured (both chains ended 19:14 / 19:20 UTC 2 Oct):** 20 buckets, 427 k media files, 9.5 TB: 41,098 h header-measured
  (95 % 40,022–42,175), speech 22,465 h (21,878–23,052), music 19,834 h; rmsbroadcast 18,983 h / speech 13,929 h; music-bucket-rms
  12,393 h / speech 1,845 h; citizen-digital-cms-files 5,979 h; news-vault 1,551 h; chamgei-backup 1,476 h; google-transcripts 530 h.
  7,523 files read in full; egress so far ≈ $77 (770 GB, assumed $0.10/GB).
- **Owner (3 Oct, with the three reports attached):** "Note the part you cannot access, focus on the part you can access … get us closer to
  the truth and revise these reports." Applied: denied/archived stores take NO sample budget (`plan_scope` readable-only weights); denied
  verdicts are re-probed every run (6 one-byte GETs) so a grant auto-resumes; `summarize_label` reports `listing` before `no_media` (shares
  not yet listed were wrongly `no_media`/complete); census = every file read, else ratio estimate; no-audio videos are zero-window rows;
  storage classes counted per bucket (`storage_classes` in the entry); `CENSUS_SAMPLE_STRATA_CAP` 120 → 160 so music-bucket-rms (125 folders)
  stratifies by folder. Hours are stated only where ≥1 header was probed (report side too).
- Report: `estate_intelligence_report.REPORT_VERSION` 4; `content_rollup.access_blocked/readable/storage_classes`; cold-bucket strategy
  counts only Standard-class cold bytes once classes are known. Pack: `producer_estate_content.py` (R10, F100–F124, S020–S022, T040–T044,
  C050–C055, D11 grant / D12 restore, D1 corrected when classes show cold buckets already Archive). Re-authored as `com-1f3a3606e140`
  (new day → new commission id); `_evidence_newer_than` also fires when a content chain ends. UI: `EstateContentAccess.jsx`.
- Re-commission tool: `assessment_workspace/tools/content_census_recommission_20261003.sh` (waits for the in-flight NAS receipt, restarts the
  scheduler for the env change, commissions OBS-A/OBS-B `…-readable` chains). Projected egress for the readable re-plan: music-bucket-rms may
  take most of the 40 k OBS-A budget (≈1–1.4 TB ≈ $100–140 + Archive direct-read fee).
- NAS: 16 shares = `channel01…08` + `Channel09…16` (mixed case). Pod restarts (20:09, 23:44, 00:21 UTC) orphaned NAS passes → busy retries
  (`ENUMERATION_ALREADY_RUNNING`, max 6 per chain). Rows/headers are durable on the host; only the receipt is lost.
