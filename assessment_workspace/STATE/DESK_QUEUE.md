# STATE/DESK_QUEUE.md

Batched fork queue per Standing Order §6.8.2. The desk answers at milestone seals; an item in this queue is **NOT** a hold — the run continues on everything the fork does not block.

Each entry carries: **fork id · surfaced-at seal · options · recommendation · what it blocks · what it does NOT block (i.e., what continues)**.

---

## DQ-01 · Auditor–Builder independence violation (§10.5 vs §6.8.2)

- **Surfaced at**: AUDIT-PREP-20260921 seal (state Commit-A `433748dc…`).
- **Fact**: Standards v2 §10.5 requires reviewer/auditor independence from the builder (10% re-performance by an independent reviewer). This E1 instance is both builder (Extraction-Akki backend) and auditor (Order A + Order B execution).
- **Options**:
  - **(a)** Owner assigns human reviewer for the 10% re-performance sample.
  - **(b)** Owner accepts single-agent audit annotated at every finding as `auditor=builder instance, independence waived pending desk`.
  - **(c)** Defer audit findings ratification until an independent reviewer is available; keep audit running to produce evidence for later re-performance.
- **Recommendation**: **(b)**. The owner directed §6.8 to open the audit self-running, so independence is knowingly waived; annotating every record is the cheapest reversible option and preserves optional (a) later.
- **Blocks**: audit ratification signature (per §6.8.5, that reaches the owner at completion).
- **Continues**: all audit passes (Order B Q-1..Q-11, Order A Part 0/I). Findings will land annotated per (b) throughout.

## DQ-02 · Deliverable count mismatch (five hashes vs owner-asked four)

- **Surfaced at**: AUDIT-PREP-20260921 seal.
- **Fact**: `programme/track-a` and `master` live in two different repos, so one `git bundle create` cannot cover both. Two bundles produced. Owner's Step 4 language ("owner asked for four hashes; with two bundles you will report five — flag the count and why") already anticipated this; flagging here for completeness.
- **Options**: **(a)** Accept as delivered · **(b)** Adjust protocol to require single-repo consolidation (breaks assessment_workspace / Extraction-Akki topology).
- **Recommendation**: **(a)**. The five hashes are recorded in DECISIONS.md and PINS.md inside the state bundle per §6.8.3.
- **Blocks**: nothing.
- **Continues**: everything.

## DQ-03 · S4 sub-slice blocked · MySQL `159.138.162.146` credentials  ~~CLEARED at CENSUS-2 seal (2026-09-21T~20:00Z)~~

- **Surfaced at**: CP-ESTATE-INGESTION wave-card AUTHOR (2026-09-21T13:15Z); confirmed still blocked at AUDIT-PREP seal.
- **Fact**: Fresh RMS creds sheet (2026-09-21) omitted this host. All other MySQL hosts in the ingestion scope authenticate.
- **Options**: **(a)** Owner supplies working creds for `159.138.162.146:3306` in next credential drop · **(b)** Owner explicitly de-scopes this host from S4 · **(c)** Owner supplies IP allowlist relaxation on the host so JUMP can reach a re-issued admin cred.
- **Recommendation**: **(a)** — the "MICROSERVICES-primary" DB is a named scope target; option (b) loses a scope target; (c) still needs a cred drop.
- **Blocks**: S4 sub-slice for host `159.138.162.146` only.
- **Continues**: all other MySQL sub-slices (8 of 9 hosts proven authable), NAS CIFS, Digicow AWS RDS/S3.
- **CLEARED**: fresh drop `RMS_CREDS.xlsx` sha256 `3311dae2…10cc545` (2026-09-21T~19:35Z) supplies `bramuel` / `[REDACTED-SECRET §HYGIENE-20260921]` for this host. WEEGO cluster now authed via JUMP (paramiko + `mysql --defaults-extra-file=<(...)`). 4 databases · 443 tables · 951 MB on `weego` DB alone · latest `update_time` = 2026-09-21T04:48Z. <!-- HYGIENE-20260921: raw pw redacted at HEAD; historical commit 816be899 still carries it. -->

## DQ-04 · S4 sub-slice blocked · MySQL `HOST` placeholder (WEEGO)  ~~CLEARED at CENSUS-2 seal (2026-09-21T~20:00Z)~~

- **Surfaced at**: CP-ESTATE-INGESTION wave-card AUTHOR; confirmed still blocked at AUDIT-PREP seal.
- **Fact**: The fresh creds sheet has valid credentials for WEEGO but the host cell contains the literal string `HOST` (placeholder), not an IP.
- **Options**: **(a)** Owner supplies IP · **(b)** De-scope WEEGO.
- **Recommendation**: **(a)**.
- **Blocks**: WEEGO ingestion sub-slice only.
- **Continues**: everything else.
- **CLEARED**: WEEGO IS `159.138.162.146` — the section-header row carries the placeholder `HOST` label, and member rows (`analytics`, `sql_demo`, `sql_trial1`, `weego`) inherit from the section credentials. Section-inheritance parser landed in `tools/estate_census_v2.py:_load_fresh_creds`. Same clearance as DQ-03.

## DQ-05 · S4 sub-slice blocked · Huawei OBS `obs:object:GetObject` scope missing

- **Surfaced at**: HUAWEI-OBS-ACCESS-DRILL seal (part of `18b4d85…`).
- **Fact**: Current rotated AK/SK (`HPUA…`) authorises `ListBuckets` and `ListObjects` (verified 200 OK against multiple buckets across regions), but `GetObject` returns 403 across all tested buckets. Region-routing bug already ruled out.
- **Options**: **(a)** RMS admin extends IAM policy to include `obs:object:GetObject` on the audit-scope buckets · **(b)** Owner supplies a second AK/SK pair with wider scope for read ingestion · **(c)** De-scope object-body reads from S4 (keep bucket/object metadata only).
- **Recommendation**: **(a)**. GetObject is required to satisfy "read every byte through a ledgered ExternalRead event" — metadata-only is a scope regression per Doc 5 B5.4.
- **Blocks**: OBS object-body ingestion sub-slice (any surface that requires reading object bytes).
- **Continues**: OBS metadata-level manifest work (ListObjects → manifest → LawfulBasisAdmit rows can still be prepared and emitted).

## DQ-06 · HuggingFace ingestion credentials

- **Surfaced at**: HF-HOLD SEC-2026-09-12-01 (still standing).
- **Fact**: HF hold is still active per §4.1 §E; no HF token supplied.
- **Options**: **(a)** Owner drops HF read token · **(b)** HF hold remains in force → no HF ingestion this milestone.
- **Recommendation**: **(b)** unless a corpus is specifically needed by an in-flight card. HF-HOLD is standing; no card in flight requires it.
- **Blocks**: any HF-sourced ingestion sub-slice.
- **Continues**: everything else.


## DQ-07 · GPU visibility · owner said "GPUs are connected" but they are NOT visible from this preview container  ~~CLOSED at GPU-LANE-OPEN-20260922 seal (2026-09-22T~01:07Z)~~

- **Surfaced at**: HYGIENE-20260921 seal (2026-09-22T~00:38Z), immediately after owner directive "GPUs are connected. Re-inventory compute NOW."
- **Fact**: Twelve read-only probes ran this seal — `nvidia-smi` (127 not-found), `lspci` (binary absent), `ls /dev/nvidia*` (2 no-such-file), `ls /dev/dri` (2 no-such-file), `/proc/driver/nvidia` (absent), `nvcc` (absent), `/usr/local/cuda*` (absent), `lsmod|grep nvidia` (empty), `dmesg|grep -iE 'nvidia|nouveau'` (empty), `env|grep -iE 'cuda|nvidia|gpu'` (no env vars), `python3 -c 'import torch'` (ModuleNotFoundError). Full receipt: `phase0/gpu_probes/20260922T003800Z_GPU_INVENTORY_PROBE.json`. Container was not started with `--gpus`, no `nvidia.com/gpu` allocated, no device passthrough.
- **Options**: **(a)** Owner supplies a remote GPU host (SSH endpoint + creds) reachable via existing JUMP `159.138.173.250` or directly · **(b)** This preview container is redeployed with GPU device passthrough (k8s `nvidia.com/gpu` resource + NVIDIA device plugin, or Docker `--gpus all`) — this is an owner/platform action, not an agent action · **(c)** Owner names the specific in-estate GPU host (e.g., `digicow-vm-gpu-01` or equivalent) and provides address + creds; agent tunnels via JUMP.
- **Recommendation**: **(a)** or **(c)** — either provides a fast unblock without a redeploy. **(b)** works but is slower.
- **Blocks**: GPU-quality language-ID on the Digicow S3 speech corpus · GPU re-classification of `*_probable` and `music_or_noise` segments from CENSUS-2 · pipeline extension over NAS/OBS audio once those walks land · any faster-whisper / silero / torch inference lane.
- **Continues**: S4a-DIGICOW-RDS adapter scaffolding (CPU-only) · Order B / Q-1 full audit run (CPU-only) · deep NAS via JUMP `smbclient` (network I/O, no GPU) · OBS ListObjectsV2 sweep across 106 buckets (network I/O, no GPU) · CPU-heuristic audio classification already banked at CENSUS-2 (16.59 h speech / 1.11 h music / balance ambient).
- **Disk pre-flight for when GPU unblocks**: `/app` is at 88 % (1.3 G free) — do NOT install model weights there. `/` overlay has 75 G free — install faster-whisper/silero and model caches there; use int8 quantized variants; clear cache after one-shot pass if disk pressure returns.
- **CLOSED**: owner drop `GPU CREDs.xlsx` sha256 `483b8f697dde5117d03bbc7b2cddc322fe49788f65d0d99b0516ff3c9fcdc29b` (2026-09-22T~00:45Z) named two hosts direct-reachable on public IPs: `akki-vm` (41.173.184.244) and `akki-vm-ii` (41.173.184.247). New pw drop failed (matches 2026-08-28 hardening posture), pubkey auth via banked `id_ed25519_akki_gpu` succeeded on both. Verified via ssh + `nvidia-smi`: **4 × NVIDIA H200 · 572 GB HBM3e VRAM · driver 570.211.01 · Ubuntu 24.04.4**. Full sweep for language-ID launched, ETA ~35 min. On-disk record cited (as owner referenced): `phase0/gpu_receipts/`, `phase0/keypair_hardening_receipts/`, `STATE/DECISIONS.md:521,1601,4525,4621`. Path taken: **(c)** direct on public IPs — no JUMP needed for this lane.

## DQ-08 · Historical commit 816be899 still carries the raw MySQL passwords · policy tradeoff, disclosed

- **Surfaced at**: HYGIENE-20260921 seal (2026-09-22T~00:38Z).
- **Fact**: The additive-supersede scrub landed at HEAD replaces the tokens at the tip, but state commit `816be899` (CENSUS-2-20260921) still carries the two raw MySQL passwords (`bramuel` and Razuna) in its own diff. Anyone doing `git show 816be899` or `git checkout 816be899` sees them. SO §3.8 forbids `git filter-branch` / `rebase -i` / force-push to erase them from history — the only correction path available under standing orders is additive supersede at HEAD, which is what landed.
- **Options**: **(a)** Accept the tradeoff (recommended) and rotate the two passwords out-of-band so the historical leak becomes moot · **(b)** Owner temporarily suspends SO §3.8 for a targeted history rewrite of the two committed values across just these four blobs (destructive, breaks bundle hashes, breaks external mirrors' sync) · **(c)** Take no action and treat the historical leak as acceptable residual risk.
- **Recommendation**: **(a)**. Rotating the credentials neutralises the historical leak without breaking additive-only. Any external mirror or bundle already shipped is a bounded blast radius (the state bundle `akki_audit_20260921_state.bundle` in `/app/audit/inbox/` still carries the leak inside it — flag).
- **Blocks**: nothing operationally (agent can continue on either resolution).
- **Continues**: everything.


## ~~DQ-09 · Ratchet-of-record drift on `programme/track-a` · file `passed_floor` stuck at 5858 through three subsequent Commits-A~~ CLOSED at CENSUS-SURFACE-A Commit-B seal (2026-09-22T~03:45Z)

- **Surfaced at**: CENSUS-SURFACE-A Commit-A" (this-Commit-B state seal · 2026-09-22T~03:32Z at sweep boundary).
- **Fact**: On `programme/track-a` HEAD `e06ecf9` and at `HEAD~1` `4dfc446`, `backend/tests/invariants/baseline_failures.json` shows `counts_at_baseline.passed: 5858` and `passed_floor: 5858`. The last commit to actually write the file was `283524d` (CP-PROD-DEPLOY, 5857 → 5858). The three subsequent code commits — `42a0d3a` R-100-UNWIND (claimed 5852→5857), `4dfc446` SURFACE-A Commit-A (claimed 5858→5874), `e06ecf9` SURFACE-A Commit-A' (claimed 5874→5892) — declared ratchet bumps in their commit messages but did NOT touch the file. §1 SESSION BOOT PROTOCOL verification rule requires `counts_at_baseline.passed == passed_floor` and both to match the sweep-observed count — the file-of-record was stale by 34 (later 56) counts against the sweep-measured truth. `test_baseline_no_new_breakage` was silently GREEN throughout because the guard is `sweep_passed >= file_floor`, not equality.
- **Options**: **(a)** Reconcile at the next Commit-A pre-Commit-A regen (bump file to sweep-measured value in an additive step; monotonic-up preserved; no history rewrite). **(b)** Retroactive amend of the three prior Commits-A (destructive · violates §4 zero-push and §3.8 additive-only · inadmissible). **(c)** Leave stale and defer (carries §1 verify miss forward · unlisted risk that a future compaction-restart refuses to boot).
- **Recommendation**: **(a)**. Executed this-Commit-B seal (baseline_failures.json 5858 → 5914 · new sha256 `db5a7989...` · ORCH_BOOT.md ratchet regenerated to match · byte-identical POD audit mirror synced).
- **Blocks**: nothing operationally.
- **Continues**: everything.
- **CLOSED**: this-Commit-B (2026-09-22T~03:45Z). BASELINE_GUARD=1 double-green stripped-sha256 `213996fe...` byte-identical run1 + run2 · 5914 passed · 4 pre-existing baseline fails · 1 skip. `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` GREEN. `test_orch_boot_anti_forget_manifest_matches_live_ratchet_and_sealed_heads` GREEN. Standing lesson banked in DECISIONS.md: future waves must verify `passed_floor` bump landed in the file (spot-check `git diff HEAD -- backend/tests/invariants/baseline_failures.json`) before Commit-A. <!-- carried forward per additive-only §3.8; entry preserves history. -->

## DQ-10 · `/app main` `3840c8f58 ---` hook auto-commit anomaly · monitoring-only

- **Surfaced at**: CENSUS-3-F Commit-B state seal (2026-09-22T~05:15Z) during re-anchor.
- **Fact**: `/app main` HEAD `3840c8f58f520137886e21c30abc8b0b084c0990` (committed 2026-09-22T04:15:43Z by `E1 Autopilot`) carries the literal subject `---` (three dashes) followed by a full-length body containing the CENSUS-SURFACE-A Commit-C fixup narrative. The prior commit `fc4e572ab` is the explicit Commit-C companion. `3840c8f58` appears to be an Emergent pre-commit-hook auto-commit that stripped the subject line — the body-first narrative structure is otherwise identical to a normal seal report.
- **Options**:
  - **(a)** Monitor-only: bank one-line note here and in this-Commit-B DECISIONS narrative; take no further action unless it recurs.
  - **(b)** Dedicated close-and-cure: identify the pre-commit hook, patch it to preserve subject on auto-commit, seal as CP-HOOK-AUTO-COMMIT-CURE.
- **Recommendation**: **(a)** per owner Ruling 3 verbatim (2026-09-22T~04:2XZ) — *"As you proposed: short DQ item + one-line note in the Commit-B DECISIONS entry. No dedicated close needed unless the anomaly recurs — if a second hook auto-commit with a `---` subject ever lands, promote it to its own DQ with the hook config as the suspect."*
- **Blocks**: nothing operationally. The commit body carries full seal-report content, so audit legibility is preserved.
- **Continues**: everything. R-91 ε-apply at horizon 2026-09-23T03:23:15Z unchanged. CENSUS-3-F sealing this-wave unchanged.
- **Promotion trigger**: if a second commit with `---` (or any structurally-anomalous) subject lands on `/app main` from `E1 Autopilot`, promote DQ-10 to its own dedicated close with the hook config as suspect (per owner Ruling 3).

## DQ-11 · `/app/backend/.env` tracked-instead-of-gitignored · blocks live OBS env-bind

- **Surfaced at**: CENSUS-3-F.2 Commit-A' pre-flight (2026-09-22T~05:35Z) during owner-ruled FORK-F.2-OBS-CUSTODY α precondition check ("verify it is gitignored before writing").
- **Fact**: `git -C /app ls-files backend/.env` returns the path. `/app/.gitignore` lines 88-90 (`.env` / `.env.*` / `*.env`) do NOT apply because git ignores rules for already-tracked files. History carries `.env` at commits `dc48d5313` (2026-09-19 · frontend feat) + `e214236a8` (2026-09-19 · W10 allowlist). Existing content is benign (`AKKI_VM_HOST`/`USERNAME`/`PORT`, `MONGO_URL`, `EMERGENT_LLM_KEY` etc.) but writing `HUAWEI_OBS_SK` to it would be a credential-in-log defect that survives forever in git history.
- **Blocks**: **CENSUS-3-F.2.1 live-OBS-bind slice** (queued behind this DQ). Keys ARE durable at `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds` (openpyxl sheet-name probe verified, values not read).
- **Does NOT block**: CENSUS-3-F.2 shape landed this-wave (`runtime.py` + 6 live invariants GREEN), HF-offline env guard, phase0 receipt writer, cursor persistence. `stream_object` SAFE-REFUSES cleanly via `refuse_live_obs_without_env` when any OBS env key is missing.
- **Owner cure options**:
  - **(a)** Dedicated `CP-DOT-ENV-HYGIENE` seal: `git rm --cached /app/backend/.env` on `/app` main, add explicit `.env` entry to `.gitignore`, keep file on disk for supervisor runtime. Historical tracked commits remain but future edits stay untracked. Preferred if you want the .env to be the sole env source.
  - **(b)** Introduce `/app/backend/.env.local` (untracked from birth; already covered by `.env.*` gitignore rule but git respects that for a new file). Supervisor sources both. New sensitive keys land only in `.env.local`. Non-invasive to existing tracked .env.
  - **(c)** `services.secret_hygiene.huawei_obs_vend` — NEW module that reads `HUAWEI_OBS_AK/SK/ENDPOINT` from `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds` at process start via `openpyxl`, applies existing custody-cat guard, and returns them as an in-memory tuple. Adapter binds via this vend surface instead of env. Sidesteps `.env` entirely. Custody-hygiene guards apply.
- **Recommendation**: **(a) or (b)**. **(b)** is smaller blast radius. **(c)** adds a new custody-vending API (state-of-record surface event; may need owner ratification).
- **Continues**: everything else. R-91 horizon 2026-09-23T03:23:15Z unchanged.

---

## Standing rules for this file

- Additive-only. An entry is closed by an owner desk-answer at the next milestone seal; **closed entries are struck-through, not deleted**, so the queue keeps its history.
- Items are ordered by surface-at-seal timestamp, oldest first. New items append.
- Every entry cites the seal at which it was surfaced.
- Every entry states **what continues** — not just what blocks — so the run's non-blocked breadth is visible at a glance.
