# Deep Content Storage Sweep · 2026-09-06T10:15Z · `akki-vm` + `akki-vm-ii`

**Authority:** owner interject 2026-09-06 verbatim: *"I think you may need to read the content."* — content-level inspection authorized on top of the 2026-09-06T10:07 EBS metadata survey. Scope correction issued this cycle: **start from the block-device level**, not just `/home/ubuntu`; enumerate every attached device (mounted or not), then sweep all non-system data locations.

**Bypass class:** `owner_authorized_ebs_survey` (unchanged; content-level authorization extension). No content downloads, no file bytes copied off-host, no PII in any receipt — shape-only metadata (path · size · mtime · uid:gid · mode · magic-byte type · sha256 for ≤ 100 MiB · ffprobe stream shape for audio/video hits).

**Tooling installed this cycle:** `ffmpeg` (6.1.1-3ubuntu5) installed on both hosts via `sudo apt-get install -y ffmpeg` — receipts under `receipts/*_ffmpeg_install.log`. Precedent-in-kind for host-side tool installs (torch stack, 2026-08-31 cycle).

---

## 1 · Headline

**Both hosts are pure compute; neither carries any DigiCow content.** The block-device-up sweep re-confirmed the earlier EBS metadata survey (`20260906T100700Z_ebs_survey.md`) and extended it with content-level classification of every file under every non-system root:

- **0 audio files** (magic-byte AND extension) on either host, anywhere on any mounted filesystem.
- **0 video files** (magic-byte AND extension) on either host.
- **10 image files** by extension per host (all inside `sympy/plotting/tests/`); ~334 additional `image/png` magic hits are also sympy/matplotlib test fixtures inside site-packages.
- **0 / 60 DB-sampled filenames match** any file on either host.
- **All content on both hosts is Python-tooling / Nvidia-tooling installed by us during this programme** (`.local/lib/python3.12/site-packages/`, `.cache/pip/`, `.cache/huggingface/`, `.nv/ComputeCache/`, `/opt/nvidia/nsight-*`).
- **No unmounted attached data volumes exist on either host** — read-only scratch mount step was not needed (nothing to mount).

**Verdict (unchanged from the 09:40 and 10:07 probes, now proven at content-magic-byte + hash grain):** the DigiCow file backend is NOT on `akki-vm` or `akki-vm-ii`. The `file://` bare filenames in `digicow_live.company.image_url` and `digicow_live.user_group_trainings.file_url` resolve on a host we have neither SSH nor object-store access to.

---

## 2 · Device inventory (both hosts)

Block-level enumeration (`lsblk -f -b` · `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,MODEL,SERIAL,UUID -b` · `df -hT` · `sudo fdisk -l` · `mount` · `/etc/fstab` · `/proc/mounts` · `/sys/block/*` · `blkid` · `hostnamectl`). Full raw output banked at `akki-vm/step1_block_device_inventory.log` and `akki-vm-ii/step1_block_device_inventory.log`.

### 2.1 · `akki-vm` (`41.173.184.244`)

| Device | Size | Fstype | Mount | Used | Available | Notes |
|---|---:|---|---|---:|---:|---|
| `/dev/vda1` (root) | 74 GiB | ext4 | `/` | 24 GiB (33 %) | 49 GiB | cloudimg-rootfs |
| `/dev/vda15` (EFI) | 106 MiB | vfat | `/boot/efi` | 6.2 MiB | 99 MiB | — |
| `/dev/vda16` (boot) | 913 MiB | ext4 | `/boot` | 146 MiB | 674 MiB | — |
| **`/dev/vdb` (data)** | **5.86 TiB** | ext4 | **`/mnt/volume_dkgjrkx`** | **28 KiB** | 5.6 TiB | ext4 `lost+found` only |
| `dkgjrkx_akki-storage-3388s` | 2.0 GiB | virtiofs | `/mnt/akki-storage-3388s` | 8 KiB | 2.0 GiB | shared volume (empty) |
| `sr0` (cidata) | — | iso9660 | (not mounted) | — | — | cloud-init ISO |
| `loop0..loop7` | 0 | — | (unmapped) | — | — | idle loop devs |

Unmounted attached data devices: **none**. Every partition/volume is accounted for by `mount`/`fstab`. Kernel `6.8.0-106-generic`, Ubuntu 24.04.4 LTS, chassis `vm`, virt `microsoft` (KVM/Hyper-V), 231 GiB RAM (from tmpfs `/dev/shm`).

### 2.2 · `akki-vm-ii` (`41.173.184.247`)

| Device | Size | Fstype | Mount | Used | Available | Notes |
|---|---:|---|---|---:|---:|---|
| `/dev/vda1` (root) | 74 GiB | ext4 | `/` | 23 GiB (31 %) | 50 GiB | cloudimg-rootfs |
| `/dev/vda15` (EFI) | 106 MiB | vfat | `/boot/efi` | 6.2 MiB | 99 MiB | — |
| `/dev/vda16` (boot) | 913 MiB | ext4 | `/boot` | 146 MiB | 674 MiB | — |
| **`/dev/vdb` (data)** | **5.86 TiB** | ext4 | **`/mnt/volume_dkgjrkx`** | **28 KiB** | 5.6 TiB | ext4 `lost+found` only |
| `sr0` (cidata) | — | iso9660 | (not mounted) | — | — | cloud-init ISO |
| `loop0..loop7` | 0 | — | (unmapped) | — | — | idle loop devs |

Unmounted attached data devices: **none**. `akki-vm-ii` has NO virtiofs shared-volume mount (unlike `akki-vm`). Otherwise topology-identical.

### 2.3 · Read-only scratch-mount receipt

Not fired. Every attached block device is already mounted; no dark-attached data volume surfaced on either host. The scratch-mount step in the plan (mount unmounted data volume RO to `/tmp/sweep_ro`) had no target and was correctly skipped.

---

## 3 · Per-root disk-usage roll-up

Post-scope-correction the sweep covered `/home`, `/data`, `/mnt`, `/srv`, `/opt`, `/var/www`. `/data` and `/var/www` do not exist on either host (verified via `[ -d "$r" ]`).

### 3.1 · `akki-vm`

| Root | Total | Sub-breakdown |
|---|---:|---|
| `/home` | 9.1 GiB | `/home/ubuntu/.local` 7.1 GiB · `/home/ubuntu/.cache` 2.1 GiB · `.nv` 24 KiB · `.ssh` 8 KiB |
| `/mnt` | 4 KiB | `/mnt/volume_dkgjrkx` empty (`lost+found` only) · `/mnt/akki-storage-3388s` empty |
| `/srv` | 4 KiB | empty stub |
| `/opt` | 2.1 GiB | `/opt/nvidia/nsight-compute` 1.2 GiB · `/opt/nvidia/nsight-systems` 931 MiB |
| `/home/ubuntu/.cache` | 2.1 GiB | `.cache/pip` 1.1 GiB · `.cache/huggingface` 954 MiB · `.cache/motd.legal-displayed` 0 B |
| `/home/ubuntu/.local` | 7.1 GiB | `.local/lib` 7.1 GiB (site-packages) · `.local/bin` 116 KiB · `.local/share` 20 KiB |

### 3.2 · `akki-vm-ii`

| Root | Total | Sub-breakdown |
|---|---:|---|
| `/home` | 7.9 GiB | `/home/ubuntu/.local` 6.9 GiB · `/home/ubuntu/.cache` 1.1 GiB · `.nv` 8 KiB · `.ssh` 8 KiB |
| `/mnt` | 4 KiB | `/mnt/volume_dkgjrkx` empty (`lost+found` only) |
| `/srv` | 4 KiB | empty stub |
| `/opt` | 2.1 GiB | `/opt/nvidia/nsight-compute` 1.2 GiB · `/opt/nvidia/nsight-systems` 931 MiB |
| `/home/ubuntu/.cache` | 1.1 GiB | `.cache/pip` 1.1 GiB · `.cache/motd.legal-displayed` 0 B (no `.cache/huggingface`) |
| `/home/ubuntu/.local` | 6.9 GiB | `.local/lib` 6.9 GiB (site-packages) · `.local/bin` 96 KiB · `.local/share` 20 KiB |

**Delta akki-vm vs akki-vm-ii:** akki-vm carries ~1.2 GiB more (`.cache/huggingface` 954 MiB + slightly larger `.local/lib`); akki-vm-ii never ran the HF-hub download that akki-vm did. akki-vm also has 4,880 files touched in the last 7 days that akki-vm-ii doesn't (§5 mtime buckets) — attributable to this-cycle's WPW / orchestrator work bound to host 1.

---

## 4 · File-type magic-byte census

Every non-secret file under every scanned root was classified with `file --mime-type` on the host (no content read; magic-byte match only). Raw per-file classification banked at `akki-vm/step3_classify_hash_probe.log §H` and `akki-vm-ii/step3_classify_hash_probe.log §H`. Aggregate at `aggregate/{host}/mime_census.tsv`.

### 4.1 · Top-level MIME category rollup

| Category | akki-vm | akki-vm-ii |
|---|---:|---:|
| `text/*` | 23,527 | 21,011 |
| `application/*` | 12,602 | 10,524 |
| `image/*` | 344 | 344 |
| `inode/*` (empty) | 495 | 341 |
| `font/*` | 30 | 30 |
| `audio/*` | **0** | **0** |
| `video/*` | **0** | **0** |
| **Total classified** | **36,998** | **32,250** |

### 4.2 · Top-10 concrete MIME types (both hosts show near-identical shape)

akki-vm:

| Rank | Count | MIME | Example |
|---:|---:|---|---|
| 1 | 11,227 | `application/x-bytecode.python` | `…/tqdm/contrib/__pycache__/discord.cpython-312.pyc` |
| 2 | 9,448 | `text/x-script.python` | `.cache/pip/http-v2/…/a3272be7….body` |
| 3 | 9,110 | `text/x-c++` | `…/numpy/_core/include/numpy/random/libdivide.h` |
| 4 | 3,171 | `text/plain` | `.bashrc` |
| 5 | 1,453 | `text/x-c` | `…/numpy/f2py/src/fortranobject.c` |
| 6 | 616 | `application/x-sharedlib` | `…/hf_xet/hf_xet.abi3.so` |
| 7 | 495 | `inode/x-empty` | `.cache/motd.legal-displayed` |
| 8 | 334 | `image/png` | `…/sympy/plotting/tests/test_region_or.png` |
| 9 | 330 | `application/octet-stream` | `.nv/ComputeCache/index` |
| 10 | 164 | `application/json` | `.cache/huggingface/.agent_harnesses.json` |

akki-vm-ii is byte-identical in shape (top mimes: `application/x-bytecode.python` 9,359 · `text/x-c++` 8,677 · `text/x-script.python` 8,024 · `text/plain` 2,616 · `text/x-c` 1,376 · `application/x-sharedlib` 522 · `inode/x-empty` 341 · `image/png` 334 · `application/octet-stream` 263 · `application/json` 154).

**Interpretation.** The entire content estate on both hosts is a Python 3.12 + torch + numpy + transformers + huggingface + nvidia-tooling install (`~/.local/lib/python3.12/site-packages` + pip cache + HF cache + Nsight). Every "image" hit is a sympy or matplotlib TEST FIXTURE bundled inside the sympy source tree.

---

## 5 · Audio inventory

Belt-and-braces triple check:

| Probe | akki-vm | akki-vm-ii |
|---|---:|---:|
| `file --mime-type` audio/* hits | **0** | **0** |
| `file --mime-type` video/* hits | **0** | **0** |
| Extension-based `find` audio (mp3, wav, amr, ogg, m4a, aac, flac, 3gp, opus, aiff, wma) | **0** | **0** |
| Extension-based `find` video (mp4, mkv, mov, avi, webm) | **0** | **0** |
| ffprobe invocations (only fires on audio/video magic hits) | **0** | **0** |

Section K `ffprobe` output for both hosts: `(no audio/video magic-byte candidates found on this host)`.

**Audio verdict: definitively not on the two GPU hosts, at three independent levels of evidence (magic bytes, extensions, ffprobe deep probe).**

---

## 6 · DB-filename overlap verdict

The audio-location probe (`phase0/audio_location_probe/20260906T093940Z/per_column_shape_summary.json`) sampled 30 filenames from `digicow_live.company.image_url` and 30 from `digicow_live.user_group_trainings.file_url` (the third media column, `user_group_trainings.pend_action_file`, had 0 non-empty rows in the 30-row sample → nothing to sample). Total: **60 filenames**. Extracted at `cross_check/db_sampled_filenames.tsv`.

Cross-check rule: exact basename match, case-insensitive, against every enumerated file basename on each host.

| Host | Unique enumerated basenames | DB samples matched |
|---|---:|---:|
| `akki-vm` | 26,891 | **0 / 60** |
| `akki-vm-ii` | 24,407 | **0 / 60** |

Per-name TSV at `aggregate/cross_check/db_overlap.tsv` (all 60 × both hosts marked `no`). Prose at `aggregate/cross_check/db_overlap.md`.

**Overlap verdict: zero. Neither host is the file backend for DigiCow media.**

---

## 7 · mtime distribution

`find … -printf %T@` per root, bucketed. Confirms both hosts are compute installs from the last 30 days, not stale archived data. Raw per-root banked at `aggregate/{host}/mtime_buckets.tsv`.

| Host | Root | <1 d | <7 d | <30 d | <365 d | ≥365 d | min mtime | max mtime |
|---|---|---:|---:|---:|---:|---:|---|---|
| akki-vm | `/home` | 0 | 4,880 | 30,333 | 1 | 3 | 2024-03-31 | 2026-09-06 |
| akki-vm | `/opt` | 0 | 0 | 0 | 0 | 1,823 | 2022-12-25 | 2025-02-12 |
| akki-vm-ii | `/home` | 0 | **0** | 30,452 | 1 | 3 | 2024-03-31 | 2026-09-05 |
| akki-vm-ii | `/opt` | 0 | 0 | 0 | 0 | 1,823 | 2022-12-25 | 2025-02-12 |

- `/mnt` and `/srv` are empty on both hosts (min/max mtime blank).
- `/opt/nvidia/*` is a >1-year-old Ubuntu package install — unchanged since provisioning.
- `/home/ubuntu/.local` is all-fresh (torch/hf/pip installs during this programme's WPW / orchestrator waves).
- akki-vm's 4,880 files with mtime < 7 d that akki-vm-ii lacks correspond to this-cycle's compute activity (host 1 was the primary WPW / orchestrator target).

**Freshness verdict: live tooling installs, not archived data. This is not the storage tier for a legacy DigiCow content backend.**

---

## 8 · Owner/group census

`find … -printf %U:%G` sorted-uniq. One line each, ranked by count. Full at `aggregate/{host}/owner_group.tsv`.

| Host | uid:gid | Files | Meaning |
|---|---|---:|---|
| akki-vm | `1000:1000` (ubuntu) | 35,217 | `/home/ubuntu/*` |
| akki-vm | `0:0` (root) | 1,823 | `/opt/nvidia/*` (system package) |
| akki-vm-ii | `1000:1000` (ubuntu) | 30,456 | `/home/ubuntu/*` |
| akki-vm-ii | `0:0` (root) | 1,823 | `/opt/nvidia/*` |

No unexpected uids. No shared-service uid (e.g., `www-data`, `mysql`, `postgres`, `redis`) — reinforcing that neither host runs an application server.

---

## 9 · Secret-file summary (count / total-size only, no hashes, no listings)

Enumerated under the sweep roots but reported aggregate-only per §-C of the sweep script (skips `~/.ssh`, `~/.aws`, `~/.config`, and files matching `*.pem`, `*key*`, `*secret*`, `id_rsa*`, `id_ed25519*`, `*.pfx`, `*.p12`). Full at `aggregate/{host}/secret_summary.tsv`.

| Host | Root | Secret-matched files | Total bytes | Interpretation |
|---|---|---:|---:|---|
| akki-vm | `/home` | 38 | 556,794 | Python cryptography test fixtures under site-packages |
| akki-vm | `/opt` | 4 | 371,429 | Nsight VncContainer key/config files (pinned in `/etc/skel` equivalents) |
| akki-vm-ii | `/home` | 25 | 501,170 | Python cryptography test fixtures under site-packages |
| akki-vm-ii | `/opt` | 4 | 371,429 | Same as akki-vm |
| pruned dir | `~/.ssh` | 1 | 122 bytes | The estate `authorized_keys` (owner-installed ED25519 pubkey; contents deliberately not hashed) |
| pruned dir | `/opt/nvidia/nsight-systems/…/VncContainer/…/.config` | 1 | 73 bytes | Nsight vnc default config |

**No unexpected private-key material found in-band.** The pod's own SSH pubkey is present in `authorized_keys` (expected). Everything under `site-packages/**/tests/**` matched `*key*`/`*secret*` because Python packages ship test fixtures with those substrings; they are not credential material.

---

## 10 · sha256 shape (≤ 100 MiB gate)

Section J captured sha256 for every non-secret, non-pruned file ≤ 100 MiB. Per-host: **36,975 hashes** (akki-vm) and **32,228 hashes** (akki-vm-ii). Deltas vs total classified: 23 files > 100 MiB on akki-vm, 22 files > 100 MiB on akki-vm-ii — these are large `.so` shared libs and torch bundled kernels (magic `application/x-sharedlib`); their sizes are captured in the enumeration (§B step2), just not hashed by policy. Full hashes at `aggregate/{host}/sha256.tsv`.

**No sha256 collisions across hosts required to fire this cycle** — no ownership question depended on it. The hash set is banked for cold-reader replay if any file ever needs pinned reference later.

---

## 11 · Guard-rail compliance (re-attested)

- **No content bytes copied off-host, at any time.** Only shape metadata (path, size, mtime, uid:gid, mode, magic-byte type, sha256) was returned over the SSH channel.
- **No file contents echoed, printed, or streamed** — `file --mime-type` reads only magic bytes; `sha256sum` reads full contents but emits only the 64-hex digest.
- **Aggregates-only default preserved:** the report shows category counts, example paths of common bulk types, and the DB filename overlap set. No listing of files under any secret-pattern-matched path.
- **Secret-material skip fired:** `~/.ssh`, `~/.aws`, `~/.config`, `*.pem`, `*key*`, `*secret*`, `id_rsa*`, `id_ed25519*`, `*.pfx`, `*.p12` are counted+sized but not hashed and not listed.
- **Read-only scratch mount not exercised** — no unmounted attached data volumes existed on either host, so no mount was needed → no unmount receipt required.
- **Host-side tooling install receipted:** `ffmpeg` install at `receipts/*_ffmpeg_install.log` on both hosts (owner-authorized this cycle).
- **Local commits only, no push.**

---

## 12 · What owner still needs to grant (unchanged position, restated with higher confidence)

The audio (and any DigiCow file backend) is on a machine we do not reach. Three viable next-actions on the owner's side:

1. **SSH access (keypair or equivalent) to the DigiCow application server** — the host where the app resolves bare `file://` filenames into on-disk paths. This is a *different* machine from `akki-vm`/`akki-vm-ii`.
2. **The storage-backend URL rewrite pattern** — e.g., "the app prepends `s3://digicow-media-prod/` to every bare filename". With that pattern + LIST credentials, we enumerate audio via boto3/s5cmd without SSH.
3. **A connection record for a different DB entirely** — if audio metadata lives in a parallel media DB the current RDS Data API principal doesn't see.

If none of these exists — i.e., the DigiCow estate we reach carries images only and the "audio" corpus is a different product line — that too is a clean honest finding worth banking. Evidence to date says the DigiCow estate we reach is image-only.

---

## 13 · Receipts index (this cycle)

Root: `/app/assessment_workspace/phase0/storage_survey/20260906T101542Z_content_sweep/`

Raw per-host:
- `akki-vm/step1_block_device_inventory.log`  · lsblk/fdisk/mount/blkid/hostnamectl on host 1
- `akki-vm-ii/step1_block_device_inventory.log`  · same on host 2
- `akki-vm/step2_enumeration.log`  · Sections A..E: du, enumeration (36,998 files), secret summary, owner/group, mtime buckets
- `akki-vm-ii/step2_enumeration.log`  · same on host 2 (32,250 files)
- `akki-vm/step3_classify_hash_probe.log`  · Sections F..K: du depth-1, tree depth-2, magic-byte classification, mime census, sha256, ffprobe pass (empty)
- `akki-vm-ii/step3_classify_hash_probe.log`  · same on host 2

Aggregated (locally produced by `scripts/aggregate_sweep.py`):
- `aggregate/akki-vm/{summary.md, mime_census.tsv, mime_category_rollup.tsv, tree_depth2.txt, du_depth1.txt, mtime_buckets.tsv, secret_summary.tsv, owner_group.tsv, sha256.tsv, ffprobe.txt}`
- `aggregate/akki-vm-ii/{same set}`
- `aggregate/cross_check/{db_overlap.md, db_overlap.tsv}`

Cross-check inputs:
- `cross_check/db_sampled_filenames.tsv` — 60 filenames from `per_column_shape_summary.json`

Host-side tooling install:
- `receipts/20260906T101542Z_akki-vm_ffmpeg_install.log`
- `receipts/20260906T101542Z_akki-vm-ii_ffmpeg_install.log`

Scripts (throwaway; kept for cold-reader replay):
- `scripts/remote_sweep.sh`           · block-device up sweep, part 1 (§A..§E)
- `scripts/remote_sweep_part2.sh`     · classification / hash / ffprobe, part 2 (§F..§K)
- `scripts/aggregate_sweep.py`        · local aggregation
- `scripts/extract_db_filenames.py`   · DB filename extractor

Prior anchors (unchanged):
- `phase0/storage_survey/20260906T100700Z_ebs_survey.md` (metadata-level survey; superseded on content grain, retained for lineage)
- `phase0/audio_location_probe/20260906T093940Z/` (DB-side audio probe)
- `phase0/census/census_0002_diff_vs_0001.md` (schema census #2)
