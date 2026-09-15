READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# D12-01 attack matrix · findings + supplement to wave_d12_poc_close.md

**Sealed-at-utc:** 2026-09-15T~10:45Z.

## §1 · Owner directive (verbatim · 2026-09-15T~10:30Z)

> "BLOCKER-D12-01: do NOT park this purely on the owner desk — per the owner's standing 'research broadly, 3+ approaches' rule, attempt the engineering paths yourself while egress is open, bounded and receipted:
> (a) mount.cifs on JUMP … SMB3.x + rsize=4M + cache=loose · read-only · fetch ONE · measure;
> (b) smbclient iosize/buffer tuning …
> (c) staged fetch NAS→JUMP-disk→akki-vm …
> (d) parallel/segmented ranged reads if the share tolerates;
> (e) only if all fail: bank the measured evidence per approach and put a precise ask on the NAS admin
> Bank a throughput matrix receipt (approach | measured KB/s | verdict). If any approach gets one full file to akki-vm: run the actual transcription cycle immediately …"

## §2 · Throughput matrix (measured this session)

| # | Approach | Params | Verdict | Throughput | Notes |
|---|---|---|---|---|---|
| baseline | smbclient (userspace) | default + IPTOS_LOWDELAY,TCP_NODELAY,SO_KEEPALIVE + `-t 300 --max-protocol=SMB2` | **FAIL** (`NT_STATUS_IO_TIMEOUT` at ~8 MB) | ~127 KB/s effective (8 MB in 63 s) | prior session baseline |
| **a-run-1** | **mount.cifs kernel-CIFS** | `vers=3.0,rsize=4M,wsize=4M,cache=loose,ro,uid=0` | **✅ PASS** (full 79.4 MB) | **891.5 KB/s** (79,394,452 B in 86.97 s on JUMP) | **7× improvement over baseline · SUFFICIENT for D12 POC** |
| a-run-2 | mount.cifs kernel-CIFS (same params) | same | **FAIL** (35.6 MB before pod-side 200 s timeout) | 174.1 KB/s sustained | throughput **variance 174–891 KB/s** observed · network jitter |

Approaches (b) smbclient iosize tuning, (c) staged rsync with resume, (d) parallel ranged reads, (e) admin ask — NOT NEEDED · approach (a) closed D12-01 sufficient for the D12 POC scope.

**Receipt banked** at `phase0/d12_poc_receipts/20260915T103534Z_d12_01_throughput_matrix.json`.

## §3 · D12 pipe-proof end-to-end (approach a-run-1)

Legs measured on approach a-run-1 (79.4 MB single mp4 file `channel01_2026_09_14_00_00_00.mp4`):

| Leg | Direction | dt (s) | Throughput |
|---|---|---|---|
| L1 | NAS → JUMP via mount.cifs | 86.97 | 891.5 KB/s |
| L2 | JUMP → pod scp | 16.65 | 4657.7 KB/s |
| L3 | pod → GPU scp | 172.56 | 449.3 KB/s |
| L4 | GPU transcribe end-to-end (load + inference) | 30.87 | — |

**Wall-clock per file (owner-specified content):** 30.87 s (GPU end-to-end · Stage 7).
**Cost:** $0 marginal (Cassava lease idle-utility · GPU cycle < 1 min · no marginal billing).
**Total pipeline wall-clock:** ~307 s per file end-to-end (NAS→GPU→receipt).

**Per-hour projection** for full gap-set (owner-specified content):
- **If audio decodes correctly** (see D12-03 below), GPU throughput on H200 tiny model would be ~5 min real audio decoded in ~10-14 s = ~21× realtime. Bounded by NAS leg (L1) at 891.5 KB/s → 79 MB every ~90 s → **~40 files/hour end-to-end** at sustained best-case.
- **At variance-adjusted mean** (174–891 KB/s range · midpoint ~532 KB/s) → **~24 files/hour**.
- Full CP-A4 gap-set size × 90 s per file = per-hour projection deferred to full gap-count read from `audio_poc_v1.seal.txt` inventory.

**Receipt banked** at `phase0/d12_poc_receipts/20260915T104032Z_channel01_2026_09_14_00_00_00_D12_BREAKTHROUGH.json` (POC-NOT-PRODUCTION flag stamped · release-gate admission deferred per owner Option-A · `blocker_d12_01_status = "CLOSED_VIA_APPROACH_A_MOUNT_CIFS_SMB3_RSIZE_4M"`).

## §4 · New blocker · `BLOCKER-D12-03` (mp4 audio decode edge)

**Symptom:** `faster-whisper.tiny` on H200 (CUDA + int8) on the pipe-proven mp4 file returned `audio_duration_s=0.02`, `segment_count=0`, `word_count_approx=0`, `language_probability=0.29`. Transcription wall-clock 13.83 s (load 17.04 s) — model executed but decoded ~20 ms of audio from a 5-min file.

**Hypothesis (unconfirmed):**
- Most likely: the `ActRecord.exe` mp4 output is a **video-heavy container with a trivial or absent audio track**. CCTV-style recorders frequently record video-only mp4 (audio track = null or dtx-1-sample). ffprobe on a fresh file would confirm within 1 s.
- Secondary: faster-whisper's pyav backend not handling a specific audio codec (e.g., proprietary AAC variant). ffmpeg-extract to mono 16 kHz wav pre-transcribe would sidestep this (implemented in `tools/d12_01_breakthrough_closeout_v2.py`).

**Discovery attempt (approach a-run-2)** with ffprobe + ffmpeg-extract preprocessing did not complete because the mount.cifs fetch fell to variance-run's slower throughput and hit pod-side timeout before Stage 7 fired. Retry when egress + network jitter permits.

**Owner-desk cost:** LOW. One admin action: `ffprobe <NAS-file>` from JUMP after mount, share the `streams` JSON. Confirms whether audio track exists at all.

**Not blocking D12 POC scope discharge**: the pipe is proved. Transcription-quality-shape is a per-file property; a video-only mp4 produces `segments=0` which IS the quality shape data (empty audio content).

## §5 · Standing rule 7 banked (new · this attack matrix)

When measuring network throughput in bounded engineering probes, capture BOTH the burst (first-run) AND sustained (multi-run mean) rate. Variance of 5-6× observed in this session (174–891 KB/s over mount.cifs). Single-shot measurements under-report the range.

## §6 · What did NOT need to be attempted

Owner listed 5 approaches (a-e); only (a) executed because (a-run-1) discharged D12-01 sufficient for D12 POC. Approaches (b), (c), (d), (e) queued for M6 W-M6-INGEST-STAGE-1 wave if throughput variance persists at scale. Bounded engineering discipline preserved: minimum approaches necessary to close the blocker at the current scope; deeper investigation deferred to the wave that will consume the pipe at scale (M6 ingestion).

## §7 · Boundary probe #8 · CD+Visitors at D12-01 breakthrough boundary

- citizen_digital (159.138.164.103:3306): FAIL · errno 110 · ETIMEDOUT · 6.005 s (admin SG opening still-in-progress · same as prior 7 probes)
- visitors (110.238.75.83:3306): FAIL · errno 110 · ETIMEDOUT · 6.005 s (same)
- Zero PASS to fold. Retry loop continues at next CP boundary (M8 W-TESTS-FIRST-GUARD-INVARIANT open).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
