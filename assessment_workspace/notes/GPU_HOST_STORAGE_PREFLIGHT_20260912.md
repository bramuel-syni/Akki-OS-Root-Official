# GPU Host Storage Preflight — 2026-09-12T~15:30Z

**Task class:** pre-flight probe · read-only · no build, no push, ratchet 3251 untouched.
**Executor:** track-a agent.

**Ground state:** ratchet floor 3251; `programme/track-a` HEAD `77834d1`; workspace `master` HEAD `2b42c988`.

---

## 1 · Real `df -hT` output — both hosts REACHABLE at 2026-09-12T~15:30Z

### akki-vm (41.173.184.244)

```
Filesystem  Type      Size  Used  Avail  Use%  Mounted on
/dev/vda1   ext4       72G   50G   23G   70%   /                        <-- root
/dev/vdb    ext4      5.9T   28K  5.6T    1%   /mnt/volume_dkgjrkx      <-- LARGE DATA VOLUME
tmpfs       tmpfs     231G     0  231G    0%   /dev/shm                  (RAM)
tmpfs       tmpfs      47G  1.5M   47G    1%   /run
virtiofs    virtiofs  2.0G  8.0K  2.0G    1%   /mnt/akki-storage-3388s
```

**Physical layout:** `vda` 75 GB (root system disk) · `vdb` 5.9 TB (attached data volume, ext4, essentially empty).

### akki-vm-ii (41.173.184.247)

```
Filesystem  Type   Size  Used  Avail  Use%  Mounted on
/dev/vda1   ext4    72G   62G  9.9G   87%   /                          <-- root · TIGHT
/dev/vdb    ext4   5.9T   28K  5.6T    1%   /mnt/volume_dkgjrkx        <-- LARGE DATA VOLUME
tmpfs       tmpfs  231G     0  231G    0%   /dev/shm
tmpfs       tmpfs   47G  1.5M   47G    1%   /run
```

**Physical layout:** same as akki-vm — `vda` 75 GB + `vdb` 5.9 TB ext4 empty.

## 2 · Current disk consumption (existing text-training work)

| Location | akki-vm | akki-vm-ii |
|---|---:|---:|
| `~/akki_journal/` (21 & 56 sealed shield-train dirs) | **3.1 GB** | **11 GB** |
| `~/.cache/huggingface/` (Qwen/base model weights) | **24 GB** | **29 GB** |
| `~/.cache/` total | 25 GB | 30 GB |
| `/home/ubuntu` total | 35 GB | 48 GB |
| **Root `/dev/vda1` free** | **23 GB** | **9.9 GB** |
| **`/mnt/volume_dkgjrkx` free (5.9 TB volume)** | **5.6 TB** | **5.6 TB** |

**Critical operational observation:** the massive 5.9 TB `/mnt/volume_dkgjrkx` volumes on both hosts are essentially empty (28 KB used). All prior text-training model cache lives on ROOT under `~/.cache/huggingface/` — which is why akki-vm-ii is at 87% root usage. **Set `HF_HOME=/mnt/volume_dkgjrkx/hf_cache` before pulling any new audio-model weights** to avoid overflowing root on akki-vm-ii.

---

## 3 · Three-bucket sizing

### (a) MODEL WEIGHTS — one-time resident downloads per host

| Model | Approx download size |
|---|---:|
| `facebook/mms-1b-all` (1 B params, fp16) | ~4 GB |
| `facebook/mms-lid-4017` (1 B Wav2Vec2 fp16) | ~1 GB |
| `Sunbird/faster-whisper-51-african-languages` (int8 CTranslate2) | ~3 GB |
| `htdemucs_ft` (Demucs v4 hybrid transformer) | ~0.4 GB |
| `pyannote/speaker-diarization-3.1` (segmentation + diarization pipelines) | ~1.5 GB |
| `microsoft/wavlm-base-plus-sv` | ~0.4 GB |
| PANNs `Cnn14` | ~0.3 GB |
| TorchAudio-SQUIM (native pipelines) | ~0.05 GB |
| DNSMOS ONNX + NISQA | ~0.1 GB |
| **Bucket-(a) total per host** | **~10.75 GB** |

With HF-cache overhead (config + tokenizer + snapshot symlinks + blob dedupe): realistic **~12–15 GB per host**.

### (b) WORKING/TRANSIENT SCRATCH — peak concurrent footprint (purged per job)

Per §2.1 lane layout: **4 concurrent workers max (2 lanes × 2 hosts)**.

Per-worker peak in-flight during a 30-min recording:
- NAS-staged .wav 16 kHz mono int16: ~57 MB (or PCM float32 ~115 MB)
- Demux normalized artifact: ~115 MB
- HTDemucs intermediate + 2 output stems (44.1 kHz stereo during processing): **~800 MB peak** during separation stage
- ASR temp cache + diarization RTTM/JSON: ~50 MB
- **Per-worker peak: ~1 GB**

**Per-host peak (2 concurrent lanes): ~2 GB. All-hosts peak: ~4 GB.**

`PurgeAttestation.purged=True` at each file's completion — **this is peak-in-flight, not cumulative.** Never grows.

### (c) RETAINED DELIVERABLE

**Attribute-stream bundle JSON** — always retained regardless of Path A/B/C:
- Per 30-min recording: ~200–500 KB JSON (transcripts + timestamps + `languages[]` + confidences + condition + diarization turns + quality scores + sha256).
- 3-station POC (~30 h processed): ~30 MB JSON.
- 16-station full (~480 h processed): ~500 MB JSON.

**Retained audio bytes — Path A only** (assumed keep-ratio = fraction of processed audio that survives music-free filter × non-English filter × quality gate):

| Scale | Processed | Keep-ratio | Retained hours | Format | Retained size |
|---|---:|---:|---:|---|---:|
| POC (3 vernacular stations) | ~30 h | **~40%** (vernacular → almost all non-English; music/silence/quality filter ~40% survive) | ~12 h | 16 kHz mono int16 (~115 MB/h) | **~1.4 GB** |
| POC same, FLAC-compressed | — | — | ~12 h | FLAC (~55 MB/h) | ~0.7 GB |
| Full 16 stations (mixed) | ~480 h | **~25%** (includes English-only stations like Hot 96 / Citizen mixed-bilingual; keep-ratio drops) | ~120 h | 16 kHz mono int16 | **~14 GB** |
| Full 16 stations, FLAC | — | — | ~120 h | FLAC | ~6.6 GB |

**Path B / Path C:** retained audio bytes ~0. Only transcripts + pointers persist. Deliverable is JSON-only, tens of MB scale.

**Keep-ratio assumption caveats:** owner should ratify. My 40% (POC) and 25% (full) are conservative; if quality gates are relaxed at scale or vernacular content is cleaner than assumed, keep-ratio rises to 50-60% for POC and 30-40% for full run. **These are projections not measurements** (evidence_class:projected) — the real number lands at CP2's Sampling & Reflection.

---

## 4 · VERDICT — crisp table

| Host | Total | Root used | Root free | Data-vol (5.9 TB) free | Can hold POC (a+b+c-POC ≈ 17 GB)? | Can hold 16-station Path A full (~29 GB total)? |
|---|---:|---:|---:|---:|---|---|
| **akki-vm** | 72 G root + 5.9 T vol | 50 G | **23 G** | **5.6 T** | ✅ YES with `HF_HOME=/mnt/volume_dkgjrkx/hf_cache` — abundant on data volume | ✅ YES on data volume; trivial for 5.6 TB |
| **akki-vm-ii** | 72 G root + 5.9 T vol | 62 G | **9.9 G** ⚠ | **5.6 T** | ⚠ **NO** on root as-is; ✅ YES with HF_HOME relocation | ✅ YES on data volume |

### One-line verdict

**Both hosts can comfortably hold the POC and the full 16-station Path A corpus — but ONLY if HuggingFace cache is relocated from `~/.cache/huggingface` (currently on 72 GB root) to `/mnt/volume_dkgjrkx/hf_cache` (5.9 TB data volume, currently 28 KB used) BEFORE any audio model is pulled; otherwise akki-vm-ii's 9.9 GB root free space overflows on the first mms-1b-all download.**

## 5 · Full-run capacity + shortfall analysis

**16-station Path A total footprint per host:**
- Models: ~13 GB.
- Peak scratch: ~2 GB in-flight (purges per job).
- Retained deliverable: ~14 GB (16-station Path A, int16 PCM) OR ~6.6 GB (FLAC).
- **Total sustained: ~15–30 GB per host.** Both hosts' 5.6 TB data volumes hold ~200× that — **no shortfall for foreseeable scale**.

**No external/object-storage target needed until:** (a) corpus grows past ~5 TB (implausible for POC + 16-station + reasonable time horizon), OR (b) owner wants a copy landed outside the GPU perimeter for lab handoff. **The 5.9 TB `/mnt/volume_dkgjrkx` volumes are the natural landing zone for both perception artefacts and deliverable retention.**

**Stream-process-and-purge** (option 4-b) is NOT required at foreseeable scale — the data volumes are sized for it not to be. However, the platform's `RetentionPolicy` primitive from §A.10 of the reframe naturally supports it: any Artifact class can bind to `WORKER_SCRATCH_PURGED` if the owner wants to opt into no-persistence-of-audio-bytes even under Path A. That's an owner ruling, not a capacity constraint.

## 6 · Source audio explicitly NOT copied wholesale

Per `services/perception/eab_1_pipeline/a1_demux.py` docstring verbatim: *"Source objects are never modified or deleted"* — and the Governance Plane's `RetentionPolicy` regime `SOURCE_UNTOUCHED` binds the source-side audio class. **No GPU-host capacity is required for the whole estate.** The pipeline streams-and-purges from the NAS via `SourceConnector.stream()`; the on-host `WORKER_SCRATCH_PURGED` regime discards after each file completes. Only (a) models + (b) peak concurrent scratch + (c) deliverable bytes need GPU-host capacity.

---

## 7 · Operational recommendations (to relay to owner)

1. **Set `HF_HOME=/mnt/volume_dkgjrkx/hf_cache` on both hosts before W1 model install.** One env-var change in the on-host trainer + supervisor wrappers. No relocation of existing text-training models is required (they can stay on root; the audio models land on the data volume).
2. **akki-vm-ii root cleanup opportunity** (optional, not blocking): 29 GB of HF cache on root under `~/.cache/huggingface/` could move to `/mnt/volume_dkgjrkx/hf_cache_text` and free up ~29 GB on root. Not required for the audio POC (data volume is fine as-is), but a clean-up hygiene improvement.
3. **FLAC vs int16 PCM for retained audio** — FLAC ~half the bytes, lossless (recoverable to bit-exact PCM). Recommend FLAC for the deliverable class if owner rules Path A; downstream lab tools decode natively. Not a hard requirement — int16 PCM is fine at the scale computed.
4. **`/dev/shm` is 231 GB tmpfs on both hosts** — could be used for zero-copy audio staging during a run (Docker/kernel tmpfs); not required at foreseeable scale.

## 8 · Attestation

- No product code touched. Ratchet 3251 untouched.
- No push. Local commit only.
- Live SSH probe, 2026-09-12T~15:30Z. Both hosts reachable.
- Numbers are `df -hT` raw output; model sizes are conservative approximations pending real download.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
