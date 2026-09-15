READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# D12-03 · corpus-level finding · OFFAIRRECS is video-only-with-null-audio

**Sealed-at-utc:** 2026-09-15T~11:12Z.

## §1 · Owner directive · verbatim (2026-09-15T~11:05Z)

> "BLOCKER-D12-03 is NOT an owner-desk item; you have JUMP access and the working mount, so run the diagnosis yourself (bounded, in-window):
> 1. `ffprobe` (or `ffmpeg -i`) the already-fetched channel01 file on JUMP — confirm audio track presence/codec/duration.
> 2. Characterize the corpus: probe ONE file per channel across all 16 channels …
> 3. If any audio-bearing file exists: run ONE through the full pipe for a TRUE quality receipt …
> 4. Bank the channel characterization matrix + updated per-hour projection … Only if ffprobe shows NO audio anywhere does this go to the owner as a corpus-level finding."

## §2 · Corpus characterization matrix (Bramwel-account scope · OFFAIRRECS share)

Method: `mount.cifs //10.10.55.55/OFFAIRRECS vers=3.0,rsize=4M,cache=loose,ro` from JUMP · one file per channel · lex-first available across most-recent date-dir first · `ffprobe -show_entries stream=... -of json`.

**Nine of sixteen channels have media**. Channels 09-15 missing across any date-dir.

| Channel | file size | video | audio codec | audio duration | video duration |
|---|---|---|---|---|---|
| channel01 | 75.5 MB | h264 960×540 | aac 48 kHz stereo | **0.008 s** | 300.000 s |
| channel02 | 75.9 MB | h264 960×540 | aac 48 kHz stereo | **0.016 s** | 300.000 s |
| channel03 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.017 s** | 300.000 s |
| channel04 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.015 s** | 300.000 s |
| channel05 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.016 s** | 300.000 s |
| channel06 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.013 s** | 300.000 s |
| channel07 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.013 s** | 300.000 s |
| channel08 | 20.9 MB | h264 512×288 | aac 44.1 kHz stereo | **0.0015 s** | 300.000 s |
| channel09 | — | NO MEDIA across any date-dir | | | |
| channel10 | — | NO MEDIA across any date-dir | | | |
| channel11 | — | NO MEDIA across any date-dir | | | |
| channel12 | — | NO MEDIA across any date-dir | | | |
| channel13 | — | NO MEDIA across any date-dir | | | |
| channel14 | — | NO MEDIA across any date-dir | | | |
| channel15 | — | NO MEDIA across any date-dir | | | |
| channel16 | 75.9 MB | h264 960×540 | aac 48 kHz stereo | **0.005 s** | 300.000 s |

**Receipt banked at** `phase0/d12_poc_receipts/20260915T110724Z_d12_03_channel_corpus_characterization_v2.json` (14 623 bytes).

## §3 · Interpretation

**All 9 media-bearing channels carry an aac stereo audio stream in the mp4 container, but with audio duration between 1.5 milliseconds and 16.5 milliseconds — while video plays for the full 300 seconds.** This is uniform across two resolution tiers (960×540 for channel01/02/16, 512×288 for channel03-08).

**This is effectively "NO audio anywhere"** (owner's literal wording) — the audio track is a null placeholder written by the recording pipeline (`ActRecord.exe` per CP-A2 discovery), not real broadcast audio. faster-whisper on this corpus (CP-D12P1 first run · `channel01_2026_09_14_00_00_00.mp4` · 79.4 MB · CUDA + int8) returned `segment_count=0 · word_count_approx=0 · language_probability=0.29 · audio_duration=0.02 s` — matching ffprobe's audio-stream metadata.

**Per-hour projection update:** UNMEASURABLE for the CURRENT OFFAIRRECS corpus. faster-whisper on empty audio returns 0 segments in <1 s of GPU time · projection is meaningless. The NAS-leg throughput (D12-01 approach a-run-1 · 891.5 KB/s burst / 174 KB/s sustained mean) remains the pipeline-level constraint but is moot until real audio content is sourced.

## §4 · Auxiliary probe · other NAS shares (Bramwel-account scope)

Probed 5 candidate audio-bearing shares (per `smbclient -L //10.10.55.55` output · 12 disk shares visible + IPC$):

| Share | mount.cifs verdict |
|---|---|
| NEWSCLIPS | **Permission denied (errno 13)** |
| PROMOS | **Permission denied (errno 13)** |
| COMMERCIALS | **Permission denied (errno 13)** |
| ADS | **Permission denied (errno 13)** |
| video | **Permission denied (errno 13)** |

Other visible shares not probed (unlikely audio content): ATTENDANCE, BACKUP1, GRAPHICS, HRMIS, NetBackup, web, web_packages.

**Broadcast audio content likely resides in NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video shares but the Bramwel account has no permission on them.** OFFAIRRECS access via Bramwel is what the sealed CP-A2 contract targets; other-share access requires different credentials.

**Receipt banked at** `phase0/d12_poc_receipts/20260915T110930Z_d12_03_share_probe_matrix.json` (~2 KB).

## §5 · Impact on the ratified chain

Per owner directive (**ADDITION** 2026-09-15T~11:05Z verbatim):

> "when W-CENSUS-RUNTIME-ORCHESTRATION lands (M8 #5), fold the ffprobe characterization into the live NAS enumeration so media_types/audio-share become measured census fields, not POC one-offs."

Effects on downstream waves:

1. **M8 #5 W-CENSUS-RUNTIME-ORCHESTRATION (in-scope · addition binding)** — extend the live enumeration to run `ffprobe` on the first sample file per source/channel and populate two new `SourceRecord` fields via CP-C4 E.5 supersession:
   - `media_types` — set from `format_name` + stream `codec_type` roster (e.g. `["video/h264+aac-null"]`, `["audio/aac"]`, `["mixed"]`).
   - `audio_bearing_share` — the fraction of sampled files where `max_audio_duration >= 1.0 s` (or a canon-chosen threshold).
   These become measured census fields per Canon-4 §4.1 (the four SourceCandidate carriers are unchanged; `media_types` + `audio_bearing_share` belong on the SourceRecord as §8 defensibility_measure enrichments).

2. **M6 W-M6-INGEST-STAGE-1 · scope re-check needed** — the audio-plane ingestion charter targets OFFAIRRECS canonical path (per CP-A2 sealed regex `nas://OFFAIRRECS/Record/{channel_dir}`). If OFFAIRRECS is video-only-with-null-audio corpus-wide, the audio-plane ingestion has zero real content on this share. Two paths open:
   - **Path α (in-scope of M6):** re-scope the audio-plane source enumeration to include NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video shares. Requires different NAS credentials (owner-desk item).
   - **Path β (in-scope of M6):** re-scope the M6 charter to *video-plane* ingestion for OFFAIRRECS (h264 video, mostly empty audio track). This is a much larger scope change — video-plane is out-of-canon for M6 as ratified.

3. **W-AUDIO-PROD-MODEL-SELECT (M8 #6)** — production model selection per §A17.11 was gated on census activation of a real audio source. Corpus finding says OFFAIRRECS-under-Bramwel is not it. Model-select wave should defer until a real audio source is enumerated (Path α above).

## §6 · Owner-desk items updated

- **NEW ·** NAS credentials for NEWSCLIPS/PROMOS/COMMERCIALS/ADS/video shares — Bramwel account lacks permission. Broadcast audio content likely lives on these shares. Unlocks real audio corpus for D12 quality probe + M6 audio-plane ingestion + W-AUDIO-PROD-MODEL-SELECT.
- **NEW ·** OFFAIRRECS channels 09-15 are dark (no media in any date-dir). If this is expected (channels reserved / not yet activated), no action; if unexpected, upstream recording pipeline investigation.
- **NEW ·** OFFAIRRECS audio track is null across all 9 media-bearing channels. If this is expected (video-only-CCTV recording), no action; if unexpected, `ActRecord.exe` recording pipeline investigation.
- Existing D12-01 owner-desk item (NAS SMB throughput variance) still stands but not blocking — approach (a) mount.cifs closed the blocker at first-run 891.5 KB/s; variance to 174 KB/s observed and captured.

## §7 · D12-03 close condition

- **CLOSED via corpus-level finding** (owner directive close condition satisfied: "Only if ffprobe shows NO audio anywhere does this go to the owner as a corpus-level finding.").
- **NOT CLOSED via true-quality receipt** (no audio-bearing file in accessible corpus).

## §8 · Boundary probe #10 · CD+Visitors at D12-03 close

- citizen_digital (159.138.164.103:3306): FAIL · errno 110 · 6.006 s (unchanged from probes #1-9)
- visitors (110.238.75.83:3306): FAIL · errno 110 · 6.006 s (unchanged)
- Zero PASS to fold. Standing retry loop continues.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
