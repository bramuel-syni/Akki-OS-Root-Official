## CENSUS-IDENTITY-RESTORE-20260925 — current execution dependency

**LATEST20:06Z:** updated portal workbook works; authenticated, bothVMs Running. Both Open console requests fail502 before terminal. Inspected akki-vm key field + expanded viewer readonly after readiness, no ordinary edit path established. No key/VM/policy/source changes. Need AISCA restore existing-console path or approved administrator enrollment, NOT more portal credentials or replacement approval. Provider brief prepared-not-sent `AISCA_PROVIDER_RECOVERY_REQUEST.md`; aggregate live receipt banked. Do not recreate/redeploy/stop/reboot or bypass disabled controls; root cause remains unverified. New key not yet generated; verify durable custody + working enrollment route before activation.

19:32Z owner says added portal credentials. Available assets show four new guide screenshots but no separate new portal-credential file. Both GPU workbook URLs remain unchanged, no email-shaped values; no portal-related env setting names. Ask for intended credential filename or missing attachment only. Do not claim the owner failed to provide it definitively; distinguish currently visible artifacts. No login attempted. Reconciliation receipt banked.

19:21Z URL resolved: owner supplied `https://console.cpt.aiscafrica.org`; browser HTTP200, AISCA email-first sign-in. Need authorized PORTAL account/sign-in access or owner-operated console. Do not request provider/URL/replacement approval again. No sign-in or compute change; VM console availability behind authentication still unverified. GPU workbook does not establish portal account credentials. Receipt `aisca_portal_public_entry_20260925T1921Z.json` banked.

19:19Z provider identified via owner guide: **AISCA / Rafay Console**. Unknown input narrowed to actual AISCA portal URL plus existing-VM console/admin availability. Guide shows SSH Public Key only during NEW VM creation; no existing-key update/serial procedure or portal credentials. Official Rafay VM serial support requires gateway, AISCA enablement unverified. `AISCA_ACCESS_GUIDE_FINDINGS.md` banks evidence. Do not ask provider name again or recreate VMs. New identity authorization stands; no key or host changed yet.

**SUPERSEDING OWNER CHOICE:** "Yes, entirely replace. Start a new" after explicit replacement/verify-before-revoke explanation. New Akki SSH identity is authorized; no need to ask again whether replacement is permitted. Need existing console/admin installation route (provider/access still unspecified), not old signing material as the sole option. Stage separately, preserve old/unrelated keys and pins, require successful new-key authentication on BOTH hosts before active switch/revocation, secure durable custody/backup. Nothing generated or changed remotely yet. Prior restore-only language below is historical.

18:57Z owner-workbook update: supplied GPU workbook privately inspected and matched to admitted host/user pairs. REAL pinned auth-none method queries on both hosts advertise **publickey only**, no authentication. No password/key sent or remote command executed. This freshly establishes that workbook passwords cannot recover the tested SSH channel, not which client key remains installed. Need original admitted private signing material from the authorized system/backup OR existing approved console/break-glass route. Restore permission already granted; no repeated permission request needed. Receipts under `execution_recovery/auth_none_owner_compute_workbook/`;23 diagnostic tests plus full103pass/2intentional-skip suite twice. T14 remains0/1. Do not run hardening/password retries or generate a key on the strength of this workbook.

18:40Z update: owner selected **Restore**, stating access remains linked to one system. Permission to restore existing identity is granted. Remaining question: which system retains its signing identity and how its authorized access/backup is available. Local second estate key does not match; available GPU key Git history and configured SSH agent yielded no original identity. Metadata lookup receipt banked. No repeated permission request, no replacement key, no remote attempt.

Owner continuation permits recovery, not speculative new keys/host weakening. Local actual private-key fingerprint differs from the admitted August28/September22 identity at the same custody path. Details and safe fingerprints: `notes/census_operational_v1/EXECUTION_RECOVERY.md`. Narrow custody directory search found no alternate private key; not an exhaustive backup search. No bootstrap password configured; historical password retirement intentional; generic hardening key paths are missing drill artifacts. Current remote authorized_keys contents and key-replacement causality remain unknown.

Protected objective: restore an authenticated, admitted Akki execution path so real tenant census can run without moving source reads into E1.

- Recommended: restore the already-admitted private key from approved backup/secure custody, or supply the authorized backup location for restoration.
- If unavailable: identify an already-authorized console/break-glass access route; explicit replacement admission and receipted installation required before changing the identity pin. Do not re-enable password login or infer a credential from historical custody filenames.
- Not acceptable: generate another key, change pins to match the current file merely to pass the guard, weaken known_hosts, repeat blind hardening, or query estate databases from E1.

Safeguard8/8 verified;82 scoped tests twice. Real refusal cr-809561ad5643 is banked; T14 remains0/1. Independent action mapping proceeds:888 original-markup event sites inventoried; component/Canon/writer/test joins remain open. DAP request-to-result, rights/metering and downstream work stay on unchanged plan.

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

## DQ-12 · CP-DOT-ENV-HYGIENE · **sequenced INTO R-101 ε-apply wave** (was: agent-side seal post-R-91)

- **Surfaced by**: DQ-11 hygiene probe at 2026-09-22T~06:15Z (receipt `phase0/hygiene_receipts/20260922T061500Z_dot_env_hygiene_probe.md`).
- **Re-sequenced at**: 2026-09-22T~06:15Z per owner ruling relayed to desk (banked at `DECISIONS.md:R-101 append` condition (iv) verbatim): *"same-boundary riders: DQ-12 CP-DOT-ENV-HYGIENE + 3-bundle Continuity regen"*. R-91 timer superseded (R-101); DQ-12 rides the same ε-apply boundary as the mirror + frontend rebuild, no longer a separate small seal.
- **Scope**: DQ-12 lands as the FIRST commit-A slice of the R-101 ε-apply wave (before the frontend rebuild slice) so any secret-hygiene finds from the broader sweep can also fold in cleanly.
- **Cure**:
  1. `git rm --cached /app/backend/.env` on `/app` main. File stays on disk; git stops tracking future changes.
  2. Introduce `/app/backend/.env.local` untracked-from-birth (already covered by `.env.*` gitignore rule at `/app/.gitignore:89`). Supervisor sources both files. New secrets land only in `.env.local`.
  3. Verify `git check-ignore -v backend/.env.local` returns the ignore rule; verify `git ls-files backend/.env` returns empty post-rm-cached.
  4. Update supervisor `frontend`/`backend` config to source both `.env` (public config · tracked) and `.env.local` (secrets · untracked) if not already.
- **RED-first test invariants** (author at wave open):
  - `test_backend_env_is_gitignored` — `git check-ignore -v backend/.env` returns success + rule.
  - `test_backend_env_local_untracked` — `.env.local` is untracked AND check-ignore returns success.
  - `test_no_secrets_pattern_in_tracked_env` — sweep of `backend/.env` (tracked at HEAD) for AK/SK/TOKEN/API_KEY/JWT_SECRET/EMERGENT_LLM_KEY-name → value-pair regex hits = zero (either key absent OR value shape ≠ high-entropy).
- **Blocks**: nothing operationally. `.env` continues to be sourced by supervisor throughout.
- **Continues**: everything.
- **Timing**: **inside R-101 ε-apply wave**, ratchet monotonic-up on the 3 hygiene invariants + the mirror-invariant retirements + net-new frontend tests.

## DQ-13 · CREDENTIAL ROTATION REQUIRED · owner-side · `EMERGENT_LLM_KEY` + `JWT_SECRET` + broad-sweep fold-ins

- **Surfaced by**: DQ-11 hygiene probe at 2026-09-22T~06:15Z + broad hygiene sweep at 2026-09-22T~06:30Z (receipts `phase0/hygiene_receipts/20260922T061500Z_dot_env_hygiene_probe.md` + `phase0/hygiene_receipts/20260922T063000Z_broad_sweep_receipt.md`).
- **Fact — LIVE (2)**: TWO live secrets currently in tracked `/app/backend/.env` AND in git history at `dc48d5313` + `e214236a8` (both commits carry the same value; committed 2026-09-19):
  - **`EMERGENT_LLM_KEY`** — 30-char high-entropy key. Used by backend for LLM inference (`emergentintegrations` library reads this). `/app/backend/.env:19`.
  - **`JWT_SECRET`** — 64-char high-entropy key. Used to sign session JWTs. **Past history holders can forge tokens.** `/app/backend/.env:59`.
- **Fact — SUSPECT (4 · owner eyeball required per broad sweep)**: high-entropy values embedded in Akki-Executive-{Core, Final} branched forks that classifier could not disambiguate live-vs-fabricated:
  - **JWT_SECRET fallback** — `backend_test.py:41` in both `Akki-Executive-Core` and `Akki-Executive-Final`. Hard-coded fallback used if env unset. Owner judgement needed: fabricated or real?
  - **AWS_ACCESS_KEY (AKIA)** ×2 — `memory/sprints/SHIELD_REIDENTIFIER_SKIP_LIST_STATE.md:107,114` in both `Akki-Executive-Core` and `Akki-Executive-Final`. AKIA-shape strings embedded in shield-test scenarios. Cannot tell from doc whether real AWS keys or fabricated. Owner judgement needed: fabricated or real (if real, revoke via AWS console)?
- **Rotation actions (owner-side)**:
  - **EMERGENT_LLM_KEY**: rotate at emergent management console (Profile → Manage Plan → Universal Key → rotate). Any holder of git history has the old key; assume compromised.
  - **JWT_SECRET**: rotate to a fresh 64-char random. Rotation invalidates all outstanding session tokens (users must re-login). This is the correct fail-safe posture after historical leak.
  - **backend_test.py JWT fallback** (2 forks): owner rules — fabricate a NEW test-fixture value AND remove the fallback path from `backend_test.py` (or leave in place if judged safe); the desk cannot judge from code alone.
  - **AKIA in shield-test docs** (2 forks × 2 lines): owner rules — if real, revoke via AWS console and add to shield-mask regex tests as `[REDACTED]` placeholders; if fabricated, keep in place and add a comment noting fixture-status to prevent future scanner alarms.
- **Follow-up (agent-side)**: after owner rotates:
  1. Update `/app/backend/.env` with new values (but this creates DQ-11 recurrence unless CP-DOT-ENV-HYGIENE has landed).
  2. Preferred sequencing: **DQ-12 CP-DOT-ENV-HYGIENE lands FIRST** at R-101 ε-apply (moves `.env`-source to `.env.local`), then owner rotation drops new values into `.env.local` (untracked). Zero-risk.
- **Blocks**: nothing operationally today. Old secrets continue to function until rotation. **Historical leak is permanent** in git history (SO §3.8 no-history-rewrite); rotation is the only cure.
- **Continues**: everything.
- **Related**: DQ-11 (CP-VEND-HUAWEI-OBS cure module scheduled Turn-6 R-101 sequence) uses the same custody-xlsx-in-memory pattern that CP-DOT-ENV-HYGIENE + rotation enable at scale. Broad sweep verified `HUAWEI_OBS_AK/SK` have **zero hits in tracked disk** (correctly outside git; keys live at `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds`).

## DQ-14 · CP-SKILLS-LAYER · **BUILD lane · PHASE 4(c) per R-102 MASTER DIRECTIVE** (was: tier-4 draft-only)

- **Surfaced by**: Spec-coverage gap digest 2026-09-22T~06:20Z, digest §3.1 rank-3 finding — **5 of 8 A18.x rules NOT BUILT** (largest single not-built concentration in the 602-rule registry).
- **Escalated at 2026-09-22T~06:50Z** per owner R-102 verbatim: *"Q2/Q3/Q4 are RESOLVED by this directive — all three objective cards (CP-SKILLS-LAYER, CP-DECK-ENGINE, CP-STREAMING-EXTRACTION) are OPENED and BUILT in this run, not just drafted."*
- **NOT BUILT rules** (verbatim from Doc 18 · Objective O11 Skills & Rendering):
  - A18.1 *"The provisioning record, reused verbatim"* — NOT BUILT
  - A18.2 *"The slice freezes; it never edits"* — NOT BUILT
  - A18.3 *"Governance rides every response, not just the first one"* — NOT BUILT
  - A18.5 *"Scope is enforced server-side, not by client discipline"* — NOT BUILT
  - A18.8 *"Complete donor code exists; it is not in this build"* — NOT BUILT
- **BUILT in place** (A18.4, A18.6, A18.7): floor-refusal invariant · async-delivery-adoption · owner-confirmed-concept snapshot parity.
- **Build sequence**: opens PHASE 4(c) after CENSUS-PRODUCTIZATION seal in PHASE 3. Sequenced this way because skills-per-tenant scoping is a consumer of the CP-TENANT-SEPARATION scaffold.
- **Blocks**: nothing operationally. R-101 ε-apply ships prototype's skills-tab views live-wired-where-real, honest-gap where-not (per R-102 "functional or honest-gap" bar).
- **Continues**: everything.

## DQ-15 · CP-DECK-ENGINE · **BUILD lane · PHASE 4(d) per R-102 MASTER DIRECTIVE** (was: tier-4 draft-only)

- **Surfaced by**: Spec-coverage gap digest 2026-09-22T~06:20Z, digest §3.1 rank-4 finding — **14 of 14 DR-R1..R14 rules PARTIAL, 0 BUILT** (whole deck-rendering pipeline scaffolded only).
- **Escalated at 2026-09-22T~06:50Z** per owner R-102 same-verbatim.
- **PARTIAL rules** (14 · Deck Engine Spec · deck_engine.md):
  - DR-R1 *"One backend rendering service · input DeckSpec_v0, output a deck"* — PARTIAL
  - DR-R2 *"Determinism is a contract: identical (spec, token version, engine version) MUST produce byte-identical output"* — PARTIAL
  - DR-R3 *"Charts render as engine-generated SVG from plate law — no client-side charting runtime"* — PARTIAL
  - DR-R4 *"DeckSpec_v0 — a frozen contract (crosses executive app + OS boundaries)"* — PARTIAL
  - DR-R5..R14 · fail-closed validation + engine guarantees + mechanical lint + versioned token sets + HTML/PDF delivery + metering + backend-only parallel-safe pattern — all PARTIAL.
  - DR-R10, DR-R13 additionally flagged `STATEMENT UNRECOVERED — extraction artefact (RD-16)` — source `deck_engine.md` restore verbatim before build.
- **Build sequence**: opens PHASE 4(d) after PHASE 4(c). Independent of tenant-separation (deck rendering is a service · no per-tenant birth constraint).
- **Exit criteria**: user clicks Documents/Deck tab · asks for a deck (DeckSpec_v0 input) · engine renders HTML/PDF byte-deterministically · delivered per prototype.

## DQ-16 · CP-STREAMING-EXTRACTION · **BUILD lane · PHASE 4(e) per R-102 MASTER DIRECTIVE** (was: tier-4 draft-only fork)

- **Surfaced by**: Spec-coverage gap digest 2026-09-22T~06:20Z, digest §3.1 rank-6 finding — **4 of 4 SE-1..SE-4 rules PARTIAL** (real-time ASR streaming not implemented; batch-only ships).
- **Escalated at 2026-09-22T~06:50Z** per owner R-102 same-verbatim.
- **PARTIAL rules** (4 · SV extension · Streaming extraction):
  - SE-1 *"Streaming extraction is a named second mode of §17.4a, sharing its tokenized representation and Character Register outputs"* — PARTIAL
  - SE-2 *"Candidate: NVIDIA Nemotron ASR Streaming — cache-aware, 40 language-locales, language-ID conditioning built in"* — PARTIAL
  - SE-3 *(unrecovered in extraction · needs canon verbatim restore)* — PARTIAL
  - SE-4 *"Methodology, not a model: compact model tuned by register normalization against the Character Register"* — PARTIAL
- **Build sequence**: opens PHASE 4(e) BEHIND CENSUS-3-F.2.1 live-OBS-bind slice (continuous ops lane · runs after CP-VEND-HUAWEI-OBS DQ-11 cure at Turn-6). SE-1..4 extends the F.2.1 streaming runtime to ASR modality.
- **Exit criteria**: audio-source registered · live streaming ASR via cache-aware Nemotron (or methodology-equivalent compact model) · Character Register writes preserve tokenized-representation · language-ID conditioning honoured · runtime GREEN per SE-1..4 invariant tests.

---

## R-101 supersede rider (2026-09-22T06:15:23Z · owner ruling relayed to desk)

R-91 clock-gate (horizon `2026-09-23T03:23:15Z` NO EXPEDITE) is SUPERSEDED per owner ruling banked at `DECISIONS.md:R-101 append`. The R-91 WHAT (byte-identical mirror + 5 baselines → 0 + 5 annotations retire · retain cp10-still-recent · milestone_status SEALED) is unchanged. R-91 ε-apply commences at NEXT boundary condition-gated on the 6 conditions installed at R-101 (see `DECISIONS.md` R-101 append §CONDITION SET and `PINS.md` `R-101 CONDITION-GATE` block).

**Effect on queue:**
- DQ-11 timing tag "R-91 horizon 2026-09-23T03:23:15Z unchanged" — SUPERSEDED. Queued to Turn-5 CP-VEND-HUAWEI-OBS after Turn-3 R-101 ε-apply + Turn-4 Order B.
- DQ-12 re-sequenced INTO R-101 ε-apply wave as first Commit-A slice (see DQ-12 above · edited this-append).
- DQ-13 owner-side rotation — unchanged; DQ-12 lands FIRST enabling zero-risk rotation into `.env.local`.
- CENSUS-PRODUCTIZATION objective card DRAFTED at `STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md` · sequenced post-CP-TENANT-SEPARATION per owner second-question response requirement.

## Standing rules for this file

- Additive-only. An entry is closed by an owner desk-answer at the next milestone seal; **closed entries are struck-through, not deleted**, so the queue keeps its history.
- Items are ordered by surface-at-seal timestamp, oldest first. New items append.
- Every entry cites the seal at which it was surfaced.
- Every entry states **what continues** — not just what blocks — so the run's non-blocked breadth is visible at a glance.


## DQ-17 · WEEGO MySQL password rotation required · owner-exclusive · 2026-09-22T09:45:00Z

Filed post-INCIDENT-2026-09-22-01 during RMS CREDS 2 ingest (custody fold-in sub-slice 4f post-seal). See STATE/incidents/20260922T094500Z_INCIDENT_RMS_CREDS_V2_INGEST_AND_SHAPE_LEAK.md for full detail.

**Summary**: shape-only discipline breach printed a shared MySQL password (~16 chars, shared across weego cluster + citizen_digital + likely other DBs) into agent conversation-observation log. SO §3.8 no-history-rewrite means the leak is permanent in the run session log. Regardless of DQ-08 status, this specific credential is now in agent-memory-adjacent artefact space and must be rotated at source.

**Owner action**: rotate weego MySQL cluster password at source · update RMS CREDS xlsx via custody path §4.1 §E when v3 lands · confirm rotation via connectivity-matrix probe at next census pass.

**Priority**: **P0** (supersedes DQ-08 which becomes a subset).

**Related**: DQ-08 (rotation-verification blocker · superseded by DQ-17), DQ-13 (EMERGENT_LLM_KEY + JWT_SECRET rotation · related credential-hygiene lane).

**Standing-lesson (RG-3)**: NEVER print [str(c) for c in row] or first_word_of_each or any cell-value list from credential sheets. Only int counts, position indices, type names, length integers. Enforcement: hygiene-sweep invariant to add at a future slice.


## DQ-18 · CP-R91-RETIRE-SUPERSEDE · agent-side · SCHEDULED at Turn 4 sub-slice 4i (or dedicated slice pre-PHASE-2) · 2026-09-22T10:14:00Z

- **Surfaced by**: R-105 autonomous decision at Turn 4 sub-slice 4h Path R (mirror-closure-only defer). See DECISIONS.md §"R-105 · AUTONOMOUS 4H PATH-R DEFER" for full contradiction analysis.
- **Fact**: at Turn 4 sub-slice 4h the R-91 mirror-close boundary surfaced a discipline contradiction between R-101 preserved WHAT (retire 5 baselines + drain annotations + bump floor + milestone SEALED) and SO §3.8 additive-only (retirement path requires modifying sealed R-86 test carrier `test_baseline_drift_annotations_present.py` properties 2/3/5). Path R defer executed at 4h.
- **Scope**: land NEW additive superseding invariant module at `backend/tests/invariants/test_r91_wave_close_supersede_annotation_guard.py` (SO §3.8 additive · new file · new invariant class · new package path). Module carries closure-guard semantics: when `MIRROR_DRIFT_NODEIDS & baseline_failures = {}` (all mirror-drift retired) OR when `CP_APP_JS_UNIFY.md milestone_status` contains `SEALED`, the annotation set-equality + non-empty checks are vacuously satisfied. Explicitly guards R-86 properties 1-5 by supersession pattern (adds the wave-close branch that R-86 tests lack).
- **Then execute 4-leg retirement** (all in same Commit-A per §3.3 3-Commit Seal · same as originally scoped in CP_APP_JS_UNIFY.md MUST-DO 4):
  1. Retire 5 R-91 baseline entries from `baseline_failures.baseline_failures` (drain to `[]` or filter to non-R-91-mirror-drift-only): `test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell` + `test_v8_substitution_rules_bind_to_rendered_dom::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` + `test_v8_substitution_rules_bind_to_rendered_dom::test_slot1_registry_aside_marker_present` + `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js` + `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir`.
  2. Drain `known_runtime_drift_annotations` to `{}` (or move to `retired_runtime_drift_annotations_r91_close` historical field).
  3. Bump `counts_at_baseline.failed` from `5` → `0` AND `counts_at_baseline.passed` from `6072` → `6077`.
  4. Bump `invariants_enforced_when_baseline_guard_1.passed_floor` from `6072` → `6077` (+5 measured retirements).
  5. Advance `CP_APP_JS_UNIFY.md` frontmatter `milestone_status:` SCHEDULED → SEALED.
- **RED-first properly disciplined** per 4d/4e/4f standing-lesson: author RED test first proving new closure-guard invariant fails when baselines still listed WITHOUT the guard, then GREEN post-guard-landing.
- **Double-green byte-identical BASELINE_GUARD=1 sweep required** pre-Commit-A. Expected post-retirement: 0 failed / 6077 passed / 1 skipped both sweeps · stripped-sha256 IDENTICAL.
- **§3.3 3-Commit Seal** (with /app companion Commit-A + Commit-C at each side per pattern).
- **Blocks**: nothing operationally today. Mirror is byte-identical from 4h · all 5 R-91 tests pass in real bytes · retirement is a bookkeeping+ratchet-lock rather than a functional gate.
- **Continues**: everything. 4i can proceed with Continuity Bundle regen + PINS sha-pin + hygiene independently; DQ-18 supersede can fold-in at 4i, OR land as dedicated CP-R91-RETIRE-SUPERSEDE slice, OR queue behind 4i and land at 4j — whichever preserves SO §6.4 nothing-beyond scope discipline.
- **Priority**: **P1** (unblocks R-101 preserved WHAT retirement leg · sequenced pre-PHASE-2 so tenant-separation opens on a fully-closed R-91 wave).


## DQ-19 · APPROVING AUTHORITY · RMS tenant · Tier-4 fork · named-but-unseated at 4j · custody-material pending

- **Surfaced at**: Turn 4 sub-slice 4j Commit-A (PHASE 2 CP-TENANT-SEPARATION open · 2026-02-XX).
- **Fact**: Owner card `TENANT_SEPARATION.md` §4 verbatim: "The named approving authority is a tier-4 fork per tenant — bank both to STATE/DESK_QUEUE.md; until named, no controlled request executes (DAP-14 holds by construction; nothing is defaulted)." Owner refinement this-session verbatim: "No override on the PRIN-1 authorities — admit as named-but-unseated records (names + roles only; identity details arrive only via the custody path per R-104; controlled-request routing testable on AKKI-TEST synthetics meanwhile)."
- **State at 4j**: `services/tenant_separation/dap_activation.py::_ACTIVATIONS["RMS"]["dap_14_named_authority"]` carries the name-of-record ("RMS Data-Owner Authority (name-of-record pending custody)") and role ("principal_of_record_dap_14_approver") with `seat_state="named_but_unseated"`. Zero identity material (no public_key / no mfa_anchor / no contact_modality) — those arrive only through a §4.1 §F sha-pinned custody drop per R-104.
- **Options**:
  - **(a)** Owner supplies RMS Data-Owner Authority identity material via a custody drop at `custody/credentials/rms_approving_authority_<yyyymmdd>.xlsx` (sha-pinned per §4.1 §F).
  - **(b)** Owner names a different principal-of-record for RMS DAP-14 before controlled requests execute against RMS.
  - **(c)** Owner defers RMS DAP-14 seating until a specific downstream slice needs it (RMS live extractions block until then).
- **Recommendation**: **(a)**. This is the shape the wave was designed against; identity material lands via custody, seat_state flips from `named_but_unseated` → `seated_named` at that slice, and no code changes here.
- **Blocks**: any RMS controlled-request execution (DAP-14 holds by construction). AKKI-TEST synthetics + audit-fixture routing exercises continue unblocked.
- **Continues**: PHASE 2 seals with named-but-unseated record + AKKI-TEST-routable synthetics. PHASE 3 CENSUS PRODUCTIZATION opens on top.
- **Priority**: **P1** (unblocks RMS live controlled requests · doesn't block PHASE 2 seal).

## DQ-20 · APPROVING AUTHORITY · DIGICOW tenant · Tier-4 fork · named-but-unseated at 4j · custody-material pending

- **Surfaced at**: Turn 4 sub-slice 4j Commit-A (PHASE 2 CP-TENANT-SEPARATION open · 2026-02-XX).
- **Fact**: Owner card `TENANT_SEPARATION.md` §4 verbatim (same as DQ-19). Owner refinement this-session verbatim: "No override on the PRIN-1 authorities — admit as named-but-unseated records (names + roles only; identity details arrive only via the custody path per R-104 · controlled-request routing testable on AKKI-TEST synthetics meanwhile)."
- **State at 4j**: `services/tenant_separation/dap_activation.py::_ACTIVATIONS["DIGICOW"]["dap_14_named_authority"]` carries the name-of-record ("DigiCow Data-Owner Authority (name-of-record pending custody)") and role ("principal_of_record_dap_14_approver") with `seat_state="named_but_unseated"`. Zero identity material — arrives via §4.1 §F sha-pinned custody drop per R-104.
- **Options**:
  - **(a)** Owner supplies DIGICOW Data-Owner Authority identity material via a custody drop at `custody/credentials/digicow_approving_authority_<yyyymmdd>.xlsx` (sha-pinned per §4.1 §F).
  - **(b)** Owner names a different principal-of-record for DIGICOW DAP-14 before controlled requests execute against DIGICOW.
  - **(c)** Owner defers DIGICOW DAP-14 seating until a specific downstream slice needs it (DIGICOW live extractions block until then).
- **Recommendation**: **(a)**. Symmetric with DQ-19.
- **Blocks**: any DIGICOW controlled-request execution (DAP-14 holds by construction). AKKI-TEST + audit-fixture routing exercises continue unblocked.
- **Continues**: PHASE 2 seals with named-but-unseated record. PHASE 3 CENSUS PRODUCTIZATION opens on top.
- **Priority**: **P1**.

## DQ-21 · CP-AIP-LANGUAGE-COGNITION · presenter-minimum-N per language · DEFAULT 20 tagged pending

- **Surfaced at**: Owner order 2026-02-23T~16:07Z inserting Item 5.12 CP-AIP-LANGUAGE-COGNITION (banked at `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md` + `STATE/DECISIONS.md`).
- **Fact**: Owner card line verbatim: "A minimum of N distinct presenters per language (DEFAULT 20, tagged pending); train and test splits share no speaker. This is the criterion that separates learning a language from learning a voice."
- **State at fork**: `SpeakerDisjointSplitContract_v1.presenter_minimum_n = 20` (DEFAULT · tagged pending) per queued card `STATE/OBJECTIVES/queued/CP_AIP_LANGUAGE_COGNITION.md` MUST-DO §3.
- **Options**:
  - **(a)** Owner confirms N=20 as final threshold.
  - **(b)** Owner sets a different N (higher = stronger speaker-disjoint discipline; lower = risk of learning voices).
  - **(c)** Owner defers ratification; DEFAULT N=20 stands meanwhile per owner directive verbatim: "DEFAULT values stand meanwhile."
- **Recommendation**: **(a)** or **(c)**. DEFAULT proceeds meanwhile per owner's explicit "not a hold · fork" instruction.
- **Blocks**: nothing. Card + RED tests + additive modules build under standing authority with DEFAULT N=20 tagged pending.
- **Continues**: Item 5.12 card promotion + RED-first pin authoring + base registration extension + corpus-assembly seam.
- **Priority**: **P2** (fork not hold · DEFAULT stands).

## DQ-22 · CP-AIP-LANGUAGE-COGNITION · per-language MOAC accuracy threshold · DEFAULT ≥90% tagged pending

- **Surfaced at**: Owner order 2026-02-23T~16:07Z (same source as DQ-21).
- **Fact**: Owner card line verbatim: "per-language accuracy on speaker-disjoint real material (DEFAULT ≥90%)."
- **State at fork**: `LanguageCognitionMoacContract_v1.per_language_accuracy_default = 0.90` per queued card MUST-DO §6.
- **Options**:
  - **(a)** Owner confirms ≥90% as final MOAC threshold.
  - **(b)** Owner sets a different threshold.
  - **(c)** Owner defers ratification; DEFAULT ≥90% stands meanwhile.
- **Recommendation**: **(a)** or **(c)**. DEFAULT proceeds meanwhile per owner's explicit fork instruction.
- **Blocks**: nothing.
- **Continues**: Item 5.12 machinery.
- **Priority**: **P2** (fork not hold · DEFAULT stands).

## DQ-23 · CP-AIP-LANGUAGE-COGNITION · code-switch span-accuracy threshold · DEFAULT ≥85% tagged pending

- **Surfaced at**: Owner order 2026-02-23T~16:07Z (same source as DQ-21).
- **Fact**: Owner card line verbatim: "code-switch span accuracy — boundary within a ruled tolerance and label correct (DEFAULT ≥85%)."
- **State at fork**: `LanguageCognitionMoacContract_v1.code_switch_span_accuracy_default = 0.85` per queued card MUST-DO §6.
- **Options**:
  - **(a)** Owner confirms ≥85% as final MOAC threshold + ratifies boundary tolerance value (frames-of-tolerance for span boundary alignment).
  - **(b)** Owner sets a different threshold.
  - **(c)** Owner defers ratification; DEFAULT ≥85% stands meanwhile.
- **Recommendation**: **(a)** or **(c)**. DEFAULT proceeds meanwhile per owner's explicit fork instruction. Owner ratification of the boundary-tolerance frame-count is deferred alongside — DEFAULT to be pinned in card at 5.12 open.
- **Blocks**: nothing.
- **Continues**: Item 5.12 machinery.
- **Priority**: **P2** (fork not hold · DEFAULT stands).

## DQ-24 · CP-AIP-LANGUAGE-COGNITION · DP-SGD opt-out · DEFAULT applies tagged pending

- **Surfaced at**: Owner order 2026-02-23T~16:07Z (same source as DQ-21).
- **Fact**: Owner card line verbatim: "DP-SGD default applies unless the owner opts out for this internal run, recorded."
- **State at fork**: `RmsCustodyRightsPosture_v1.dp_sgd_default = True` + `dp_opt_out_ref = None` per queued card MUST-DO §9.
- **Options**:
  - **(a)** Owner confirms DP-SGD default applies (`dp_opt_out_ref = None` remains).
  - **(b)** Owner opts out for this internal run — records the opt-out at a specific ref path (e.g., `STATE/OWNER_DROPS/language_cognition_dp_opt_out_<yyyymmdd>/`) and `dp_opt_out_ref` gets pinned.
  - **(c)** Owner defers ratification; DEFAULT DP-SGD stands meanwhile.
- **Recommendation**: **(a)** or **(c)**. DEFAULT proceeds meanwhile per owner's explicit fork instruction. DP-SGD is the safer default (privacy-preserving); opt-out requires explicit recording per owner directive verbatim: "unless the owner opts out for this internal run, recorded."
- **Blocks**: nothing.
- **Continues**: Item 5.12 machinery.
- **Priority**: **P2** (fork not hold · DEFAULT stands).

## DQ-25 · FORK-COMPUTE-CORPUS-OUT-OF-PERIMETER · 12-language `google-transcripts` corpus location + Akki-side delivery mechanism

- **Surfaced at**: CP-AIP-LANGUAGE-COGNITION functional-training order 2026-02-24T~xxZ (owner verbatim: "since you have a baseline now, why dont akki train the cognition model … system needs to now be functional").
- **Fact**: The 12-language labelled corpus at `google-transcripts/datasets/{kik,ebu,swa,luo,kln,guz,mer,bxk,kam,mrg,lwg,mas}/{audio,transcript}` (per SO §6.9 LID RATIFICATION admission-gate spec) is NOT in the pod perimeter. Per Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 the labelled corpus MUST NEVER enter the pod as a data path; sealed `commission_language_cognition_training_run` at `services/audio_plane_v1/language_cognition_v1.py:401` structurally refuses `pod://*` and `/app/*` prefixed refs at every ref position. Sealed `PodAsDataPathRefused` inherits from sealed `PodIsNeverDataPathAtTrack4Error`.
- **State at fork**: sealed corpus seam `language_cognition_corpus_seam_v1.py` binds `LANGUAGE_COGNITION_TARGET_LANGUAGES` Final 5-tuple + `CorpusChannelUnreachableHonestGap_v1` marker; Census Assistant confirmed-turn banked as A5.16 receipt 2026-02-24 (owner verbatim: "this owner order IS the confirmed turn"). Reachable-channel receipt banked 2026-09-24 (`FULL_ESTATE_read_capability_sweep` · Razuna+Newsvault+NAS all connected).
- **Options**:
  - **(a)** Corpus lives Akki-side already — owner points to the exact path in Akki's boundary where `google-transcripts/datasets/{kik,ebu,...}` is mounted. Wire seam produces `corpus_assembly_ref = "akki://google-transcripts/datasets/…"` handle; sealed commission callable proceeds.
  - **(b)** Corpus lives at an external mirror (HuggingFace dataset repo / S3 bucket / other) — owner names the mirror ref. Akki (not the pod) pulls under the sealed `HuggingFacePullWrapperAntiToken_v1` (SO §6.9 clause 3 anti-token discipline) or the equivalent S3 pull, materializes inside Akki's boundary.
  - **(c)** Owner authorizes a synthetic proof-of-pipeline LoRA on a reduced non-tenant public corpus (e.g., a subset of VoxLingua107 own labelled audio if licensable for this purpose) as commissioned-job receipt. NOTE: this proves pipeline plumbing, NOT language-cognition on RMS estate.
- **Recommendation**: **(a)** if available (fastest), else **(b)** (via a specific mirror ref). **(c)** if neither (a) nor (b) is reachable within the completion window — with explicit surfacing that (c) yields a pipeline-passes receipt not a fact-level language distribution.
- **Blocks**: emission of a `completed`-status `AutonomyEngineRunReceipt_v1` for the `training_runs` job kind. Blocks promotion of overlay→measure per B5.4 (which requires a MOAC-cleared trained artefact). Does NOT block delivery of the corrected OUTCOMES doc, the scorecard, the LID false-positive fix (all landed under Ruling 2 of this 2026-02-24 wave).
- **Continues**: LID overlay abstention + estate-filter (Objective K MET at ratchet target 6420); Census Assistant confirmed-turn banking; every other sealed capability.
- **Priority**: **P0** (functional-training gate).

## DQ-26 · FORK-COMPUTE-GPU-CREDS-PENDING-OWNER-KEY-IN · resume WS-BUILD-CONNECT-GPU · aisca-gpu-01 real VM credentials

- **Surfaced at**: CP-AIP-LANGUAGE-COGNITION functional-training order 2026-02-24T~xxZ. Owner directive verbatim: "check the GPU channel first (the H200 mapping that was live earlier via SSH keys / aisca-gpu-01 commissioning records)."
- **Fact**: Every `commissioning_aisca-gpu-01_*.json` file at `phase0/commissioning_records/` carries `vm_host` of either `127.0.0.1` (pytest test-drill fixture; `receipt_path` under `/tmp/pytest-of-root/pytest-<n>/test_drill_host_produces_disti0/hardening_receipt.json`) or `203.0.113.42` / `203.0.113.5` — the latter two are in the TEST-NET-3 documentation range per RFC 5737 and are NOT routable public IPs. Pod-side probes confirm no reachable GPU (`nvidia-smi: command not found`; no torch/transformers/peft/speechbrain/opacus installed). Owner's own WS-BUILD-CONNECT-GPU ruling 2026-08-14 verbatim (DECISIONS.md line 384): "I will key the VM credentials into the app myself: Connect tile → GPU." Surface was built at Phase-0 gating (test_four_questions_topline_present green on the WS-BUILD-CONNECT-GPU tile); real credentials never keyed in.
- **State at fork**: Track-4 wiring at `services/census_autonomy/track_4_autonomy_wiring_v1.py` sealed with `AutonomyEngineRunReceipt_v1` shape ready to emit a `completed`-status receipt when a real Akki-side dispatch returns.
- **Options**:
  - **(a)** Owner resumes WS-BUILD-CONNECT-GPU: keys real `aisca-gpu-01` VM credentials into the Connect → GPU tile per the 2026-08-14 verbatim plan. Track-4 `training_runs` job then dispatches to real H200 hardware inside Akki's boundary; commissioned-job receipt returns with status `completed` / `failed` per actual run outcome.
  - **(b)** Owner points to a different GPU host by IP + SSH key path (recorded as an additive commissioning ref).
  - **(c)** Continue in CPU-only mode (Fork DQ-25 (c) path) — pipeline-proof only.
- **Recommendation**: **(a)** — resumes the pre-existing WS-BUILD-CONNECT-GPU ceremony verbatim; owner already committed to this in 2026-08-14 ruling; pod side is ready.
- **Blocks**: real (non-mock) LoRA training pass on 4× H200 with NVLink per the 30 TB HSS-mounted acceptance record shape. Blocks emission of an authentic `completed`-status commissioned-job receipt.
- **Continues**: everything DQ-25 continues; additionally, all Track-4 wiring registration paths continue to structurally refuse `pod://*` / `/app/*` refs.
- **Priority**: **P0** (functional-training gate · downstream of DQ-25 corpus location).

## DQ-27 · FORK-DP-SGD-TOOLING · opacus / DP toolchain runnability · owner opt-out recommendation banked

- **Surfaced at**: CP-AIP-LANGUAGE-COGNITION functional-training order 2026-02-24T~xxZ. Owner verbatim: "If the DP-SGD toolchain is NOT runnable on available compute, file the fork to DESK_QUEUE with your recommendation (likely: owner opts out for this internal run, recorded) and surface it to me IMMEDIATELY."
- **Fact**: `opacus` (DP-SGD Python library) not installed on pod. Torch/transformers/peft/speechbrain also absent (all >~500 MB combined). Pod is not the training host anyway (Ruling (b) verbatim); DP-SGD tooling lives at the training host, not in the pod.
- **State at fork**: sealed `RmsCustodyRightsPosture_v1` carrier at `services/audio_plane_v1/language_cognition_v1.py` binds `dp_sgd_default = True`; `dp_opt_out_ref = None`. Existing DQ-24 already covers the DEFAULT-vs-opt-out fork at contract level. This entry (DQ-27) specifically covers the TOOLING runnability question the owner surfaced 2026-02-24.
- **Options**:
  - **(a)** Owner opts out for this internal run (per owner's own hedge "likely: owner opts out for this internal run, recorded"). Recorded at `STATE/OWNER_DROPS/language_cognition_dp_opt_out_20260224/DROP.md` with owner signature; `dp_opt_out_ref` gets pinned to that path. DP-SGD applies again structurally when a real training host + opacus tooling become available.
  - **(b)** Wait for DQ-26 to close (real GPU host lands), then install opacus + tooling on that host and run DP-SGD default.
  - **(c)** Owner defers ratification; DEFAULT DP-SGD stands meanwhile per DQ-24 (with a factual honest-gap noting the tooling isn't currently runnable).
- **Recommendation**: **(a)** for this internal run (matches owner's own hedge verbatim). Re-enter DP-SGD structurally at the next training run against a real host.
- **Blocks**: nothing on its own — DP-SGD is a training-run posture, not a wiring gate. DP-SGD toolchain runnability is downstream of DQ-25 (corpus) + DQ-26 (GPU).
- **Continues**: everything DQ-25/DQ-26 continue.
- **Priority**: **P1** (structural default stands · owner one-word ruling requested per 2026-02-24 owner directive verbatim "surface it to me IMMEDIATELY").

