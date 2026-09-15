READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# BC_DYNAMIC_RECOVERY_PACKET_20260915.md

**Purpose.** Owner ruling 2026-09-15T~03:55Z (verbatim, banked in DECISIONS.md same UTC): *"BC-3/BC-4 → DO NOT SET A STATIC NUMBER · BUILD THE DYNAMIC-RECOVERY DECISION PACKET. Owner rejects the static framing: recovery must be dynamic, and expensive GPU runs must not lose work. Author notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md proposing a TIERED policy for owner ratification (research-grounded, cite the practice)."*

**Type.** Owner-ratification decision packet. Read-only, no mechanism change, no ratchet change. Ratification directive from owner: *"Owner ratifies the packet; only then charter the implementation wave."*

**Compiled during** closed egress window 2026-09-15T~03:22Z (wave seal) → 08:00 UTC re-open. Non-egress work.

**Position-redaction rule applied:** host aliases only (`akki-vm`, `akki-vm-ii`, `synology-nas`), no IPs / usernames / keys / PII.

---

## §A · Owner-mandated four-tier structure (verbatim, this packet honours it row-for-row)

Owner's own five-point structure (verbatim from `STATE/DECISIONS.md` 2026-09-15T~03:55Z):

> **"1. GPU training runs:** asynchronous distributed checkpointing (PyTorch DCP, process-based async save, pinned-memory staging), two-tier storage (frequent local NVMe checkpoints + periodic durable remote base checkpoints), checkpoint interval set DYNAMICALLY by the Young/Daly rule τ ≈ √(2·C·MTBF) — cadence scales with run cost/failure rate; a correct resume restores weights + optimizer + data-pipeline offset + RNG state. Practical target: never lose more than ~10–15 min of GPU compute.
>
> **2. Ledgers/registry (append-only truth):** continuous WAL/append archiving → near-zero RPO, point-in-time recovery to any transaction boundary.
>
> **3. Artifacts/receipts/seals:** versioned, immutable (WORM) object storage so corruption or deletion cannot propagate — replication alone faithfully replicates corruption, so snapshots+immutability are a separate layer.
>
> **4. Site loss (BC-4):** propose warm-standby as the pilot-appropriate option (scaled-down functional copy; hours-not-days recovery; far cheaper than active-active), with pilot-light and active-active as priced alternatives; quarterly restore DRILLS with integrity checks (row counts, checksums, invariant runs) — an untested plan is a hypothesis. Map each tier to a concrete RPO/RTO and to which estate assets it covers."*

This packet elaborates each row with (a) proposed concrete configuration, (b) seasoned-best-practice citation from established literature, (c) RPO / RTO / cost-tier / covered-assets mapping, and (d) invariants for owner ratification.

---

## §B · Tier 1 · GPU training runs · Asynchronous distributed checkpointing

### §B.1 · Proposed configuration

* **Checkpoint library.** **PyTorch DCP** (`torch.distributed.checkpoint`) — the modern successor to `torch.save`/`torch.load`. DCP supports:
    * *Distributed checkpoint format:* sharded per-rank shards, deterministic reassembly on any world-size (elasticity).
    * *Async save API:* `torch.distributed.checkpoint.async_save()` — the model / optimizer state is snapshotted into pinned CPU memory in the foreground (blocks for <1 s at H200 scale), then the durable write happens in a background process while training continues.
    * *Process-based async save:* forks a checkpoint-writer subprocess with a pinned-memory staging buffer; the trainer process is unblocked as soon as pinning completes.
* **Two-tier storage.**
    * *Tier 1a · Local NVMe (frequent).* `/mnt/nvme/checkpoints/<run_id>/<step>/` on `akki-vm` / `akki-vm-ii`. Rolling retention (keep last 3 · rotate). Sub-second recovery on the same host.
    * *Tier 1b · Durable remote base (periodic).* Every Nth local checkpoint (N tuned by the Young/Daly cadence below) is replicated to the durable object store (Tier 3 below). Remote replication is asynchronous and does not block training.
* **Dynamic checkpoint interval · Young/Daly rule.** Set the checkpoint cadence to:
    * **τ_opt ≈ √(2 · C · MTBF)**
    * where **C** is the checkpoint write cost (wall-time seconds to serialize + persist), and **MTBF** is the mean time between failures for the run's compute substrate.
    * The formula is derived by Young (1974) and refined by Daly (2006) for the case of constant failure rate and constant checkpoint cost — the two are the seasoned baseline citations for "when to checkpoint" across HPC and ML.
    * Practical instantiation: measure `C` on-the-fly from the first three DCP writes (median wall-time), measure `MTBF` from the run-manager's failure history on the specific host cluster (bootstrap from a conservative estimate — 24 h — until enough runs have been observed).
    * **Refresh cadence:** τ_opt is recomputed at each checkpoint boundary; cadence is DYNAMIC across the run.
* **Resume completeness invariant.** A correct resume restores FIVE state carriers:
    1. Model weights (all shards).
    2. Optimizer state (moments · exponential averages · Adam betas' running estimates).
    3. LR-scheduler state (step counter · warmup phase).
    4. Data-pipeline offset (sample index into the sharded dataset · epoch counter · deterministic shuffle seed).
    5. RNG state (torch · numpy · python-random · cuda-per-rank).
    * Failure to restore any of the five is a **broken resume** and MUST be refused by the resume path (invariant).
* **Practical target (owner verbatim):** *"never lose more than ~10–15 min of GPU compute"*.

### §B.2 · Seasoned-best-practice citations

* **Young (1974):** Young, J. W. — "A first order approximation to the optimum checkpoint interval." *Comm. ACM 17(9)*. The original τ ≈ √(2·δ·T) formula (δ = checkpoint cost, T = MTBF).
* **Daly (2006):** Daly, J. T. — "A higher order estimate of the optimum checkpoint interval for restart dumps." *Future Generation Computer Systems 22*. Refined τ estimator when failures are Weibull-distributed rather than exponential.
* **PyTorch DCP** (PyTorch 2.6+): the reference implementation for distributed checkpointing at scale · async_save API landed in PyTorch 2.5 and hardened through 2.6+ (`torch.distributed.checkpoint.async_save`).
* **NVIDIA MegaTron / DeepSpeed** patterns: pinned-memory staging + process-based async save was popularised by DeepSpeed and MegaTron-LM for foundation-model training at hyperscaler cadence.
* **Microsoft's "Just-in-Time Checkpointing" paper (2024)**: extends the two-tier pattern with in-memory replica staging for sub-minute recovery even under host loss.

### §B.3 · RPO / RTO / cost / coverage

| Field | Value | Notes |
|---|---|---|
| **RPO (data-loss window)** | **≤ 15 min of GPU compute** | Owner-mandated verbatim ("~10–15 min"). Tunable via Young/Daly τ_opt. |
| **RTO (recovery time)** | ≤ 5 min for same-host restart (Tier 1a NVMe); ≤ 30 min for lost-host restart (Tier 1b durable remote) | Resume from Tier 1a is a direct file read; Tier 1b involves a download to a fresh host. |
| **Cost tier** | **LOW-MED** | Local NVMe is free (comes with the host); durable remote adds object-store write cost proportional to checkpoint size × cadence. |
| **Covered estate assets** | LORA fine-tune runs · full-training runs · calibration-stage runs (Audio-Plane §11.2) · any GPU-bearing wave (post-D12) | Not audio-perception inference (short jobs, idempotent, checkpoint-not-needed). |

### §B.4 · Invariants for owner ratification

* **BC-1-GPU-INV-01:** No GPU training run may open without a `TrainingRunManifest.checkpoint_config` field set to a `PyTorchDCPCheckpointConfig` instance with all five resume-completeness carriers declared.
* **BC-1-GPU-INV-02:** A resume attempt that cannot restore all five carriers refuses to proceed and requires operator disposition.
* **BC-1-GPU-INV-03:** Young/Daly τ_opt is recomputed at each checkpoint boundary and receipted (`<run_id>/checkpoint_cadence_receipt.jsonl`).
* **BC-1-GPU-INV-04:** Durable-remote replication (Tier 1b) is monotonic — a checkpoint N is only replicated after checkpoint N-1's replication receipt lands.

---

## §C · Tier 2 · Ledgers / registry · Append-only continuous archiving

### §C.1 · Proposed configuration

* **Scope.** All append-only estate ledgers:
    * `STATE/DECISIONS.md` (ruling ledger).
    * `notes/RULING_LEDGER.md` (ratification transitions).
    * `phase0/northena_ledger/*` (six-carrier receipts).
    * `phase0/drill_receipts/*` (wave RED/GREEN receipts).
    * `phase0/output_verified_seals/*` (composite seal manifests).
    * `phase0/eyeball_proxies/*` (harness ground-truth receipts).
    * `phase0/gpu_receipts/*` + `phase0/gpu_inventory/*` (compute-plane evidence).
    * The append-only registry `services/census_canon/registry_write.py::RegistryStore` (once persisted).
    * The append-only WAL of any backing datastore (SQLite / Postgres / MongoDB / …).
* **Continuous WAL / append archiving.**
    * *Backing datastore case:* SQLite WAL-mode (`journal_mode=WAL`) OR Postgres pgBackRest / Continuous Archiving OR MongoDB oplog tailing — each supports the "point-in-time recovery to any transaction boundary" property.
    * *Filesystem case:* the current wave/close/drill-receipt corpus is a directory-of-append-only-markdown-and-JSON files. Continuous archiving = journalled filesystem (ext4 with data=journal or ZFS with snapshots) OR external replication via `rsync --append-verify` triggered on every close-note.
* **Point-in-time recovery.** Any transaction boundary — meaning any line-append in a `.md` ledger, any JSON record write, any WAL commit — is a recoverable checkpoint. Recovery replays the WAL / archive to the target timestamp.
* **Practical implementation for THIS estate (pilot-scale):**
    * git-commit-level PITR is ALREADY in force on `master` and `programme/track-a` (every close is a git commit).
    * Continuous archiving = periodic (every 15 min? every wave close?) push of `.git` bundles to Tier 3 WORM storage.
    * Restore is `git clone` of the bundle + `git reset --hard <commit>`.

### §C.2 · Seasoned-best-practice citations

* **Postgres WAL / pgBackRest / Barman**: canonical PITR implementations. Postgres docs · Chapter 26 (Backup and Restore).
* **MySQL binlog + xtrabackup**: MySQL PITR pattern.
* **MongoDB oplog tailing**: replica-set PITR.
* **SQLite WAL-mode**: single-file-database journal that supports PITR to any commit boundary.
* **git bundle**: portable append-only archive of a git repository, industry-standard for offline replication of git ledgers.
* **Kafka / Pulsar log-compaction**: streaming append-only patterns for high-throughput event ledgers (not needed at pilot scale).

### §C.3 · RPO / RTO / cost / coverage

| Field | Value | Notes |
|---|---|---|
| **RPO** | **~0** (transaction-boundary granularity) | Every ledger append is a recoverable point. |
| **RTO** | **≤ 5 min** for same-host restart · ≤ 15 min for lost-host WAL replay from Tier 3 | Restore is CPU-bound, not GPU-bound. |
| **Cost tier** | **LOW** | Archive size is small (markdown + JSON); replication bandwidth is tiny compared to GPU checkpoints. |
| **Covered estate assets** | DECISIONS · RULING_LEDGER · northena_ledger · drill_receipts · seals · eyeball_proxies · gpu_receipts + inventory · registry write path · any WAL-mode datastore | ALL append-only truth. |

### §C.4 · Invariants for owner ratification

* **BC-2-LEDGER-INV-01:** Every ledger write flushes to durable storage before returning (fsync-equivalent for the datastore).
* **BC-2-LEDGER-INV-02:** Continuous archiving pushes to Tier 3 WORM within a bounded window (proposed: 15 min).
* **BC-2-LEDGER-INV-03:** A PITR drill runs quarterly (per Tier 4 restore-drill invariant · §E.4).

---

## §D · Tier 3 · Artifacts / receipts / seals · Versioned + immutable (WORM) object storage

### §D.1 · Proposed configuration

* **Storage backend.** Object storage with **Object Lock in COMPLIANCE mode** (AWS S3 · Azure Blob immutable-storage · GCS Bucket Lock · MinIO with `s3-object-lock`).
* **Immutability semantics.**
    * *Compliance mode (proposed):* neither the estate operator nor the storage administrator can delete / modify a locked object before its retention period expires — NOT EVEN with root credentials.
    * *Governance mode (alternative):* the storage administrator with elevated privileges can lift the lock; useful for legal-hold flexibility but weaker for anti-tamper guarantees.
    * *Owner ratifies mode.*
* **Versioning.** Enabled — every write creates a new version; deletes are tombstones, not destructive.
* **What lives here (proposed):**
    * Deliverable audio-attribute bundles (from D12 POC onward).
    * Model checkpoints (durable Tier 1b tier from §B).
    * Seal files (`phase0/output_verified_seals/*`).
    * Owner-facing wave-close reports (`notes/W_*close*.md` snapshots).
    * Registry-write records (once persisted).
    * Continuous ledger archive bundles (from §C).
* **What does NOT live here:** transient training-scratch (Audio Plane §6.2 clause 2 · `regime=WORKER_SCRATCH_PURGED`); per-utterance embeddings (§6.2 clause 4 · destroy after cluster-assign).

### §D.2 · Seasoned-best-practice citations

* **SEC 17a-4** (financial-services regulation): the WORM regulatory baseline. NASDAQ / NYSE / OSC / SEBI equivalents all require WORM archival for trade records; the pattern is battle-tested at hyperscaler scale.
* **AWS S3 Object Lock (2018+)**: the reference cloud-object-lock implementation.
* **NIST SP 800-209** (Security Guidelines for Storage Infrastructure): §5.4 immutable storage recommendations.
* **"Replication alone faithfully replicates corruption"** — attributed to Peter Deutsch's "8 fallacies of distributed computing" corollary and reiterated in every serious DR review since; owner's verbatim quote in the ruling matches this seasoned principle.
* **Snapshot + immutability is a SEPARATE LAYER from replication** — the seasoned pattern is: primary → replica (for availability) → snapshot to WORM (for anti-tamper / anti-corruption).

### §D.3 · RPO / RTO / cost / coverage

| Field | Value | Notes |
|---|---|---|
| **RPO** | **~0** for objects that have completed their write | Once immutable, the object cannot be lost by any single-actor action. |
| **RTO** | ≤ 1 h (typical object-store rehydrate) | Depends on egress bandwidth. |
| **Cost tier** | **MED** | Object-store storage costs are cheap (~$0.023/GB/month S3-standard, cheaper in Glacier); immutable-storage add-on is a small premium. |
| **Covered estate assets** | Deliverables · checkpoints · seals · wave-close reports · registry records · ledger archives | The corpus of "must-not-be-corrupted-or-lost" material. |

### §D.4 · Invariants for owner ratification

* **BC-3-WORM-INV-01:** Every WORM-tier write receives a versioned object-key + immutability-lock receipt.
* **BC-3-WORM-INV-02:** No write path in the estate can delete or modify a WORM-tier object; deletion attempts refuse structurally.
* **BC-3-WORM-INV-03:** Retention period per artifact class is set at write time and honoured until expiry.
* **BC-3-WORM-INV-04:** Restore drill quarterly (§E.4).

---

## §E · Tier 4 · Site loss · Warm-standby (proposed) + priced alternatives

### §E.1 · Three site-loss regimes (owner picks · warm-standby is proposed)

| Regime | Description | RTO | RPO | Cost tier | Complexity |
|---|---|---|---|---|---|
| **Cold / Backup-Restore** | Backup exists at Tier 3 WORM; no standby infrastructure; rebuild from scratch on new site | **Days** | Depends on last backup (≤ 15 min per §B) | LOW | LOW |
| **Pilot-Light** | Minimal standby: critical stateful services (registry / ledger) replicating continuously to standby site; compute infrastructure NOT running (spun up on failover) | **Hours** (spin-up compute + restore state) | ≤ 15 min | LOW-MED | MED |
| **Warm-Standby (PROPOSED)** | Scaled-down functional copy: registry / ledger / a subset of compute running continuously at the standby site; full compute added on failover | **Hours-not-days** | ≤ 15 min | **MED** | MED |
| **Active-Active** | Full functional copy running continuously at the standby site; traffic can serve from either site immediately | Minutes | ≤ seconds | HIGH | HIGH |

Owner's verbatim proposal: *"propose warm-standby as the pilot-appropriate option (scaled-down functional copy; hours-not-days recovery; far cheaper than active-active), with pilot-light and active-active as priced alternatives."*

### §E.2 · Warm-standby concrete configuration (proposed)

* **Primary site:** current estate (JUMP + `akki-vm` + `akki-vm-ii` + `synology-nas` lease).
* **Standby site:** owner-provisioned second-region compute + object-storage account (owner input required · placeholder aliases `akki-vm-standby` + `synology-nas-standby`).
* **What runs continuously at standby:**
    * Registry replica (async replication from primary registry).
    * Ledger replica (continuous WAL archive replay per §C).
    * WORM object-storage replica (cross-region replication per §D).
* **What is spun-up on failover:**
    * GPU compute (H200 quota needed at standby region).
    * Trainer / worker processes.
    * Perception pipeline services.
* **Failover trigger:** operator declaration (this is a governance decision, not automation) OR primary-site liveness-probe absence over an SLA window (proposed: 30 min).
* **Failback:** manual, after primary site restoration; involves replaying standby-side ledger writes back to primary and re-verifying invariants.

### §E.3 · Seasoned-best-practice citations

* **AWS Well-Architected Framework · Reliability Pillar · Disaster Recovery patterns**: names the four regimes (Backup-Restore · Pilot-Light · Warm-Standby · Active-Active) and their cost/RTO trade-offs.
* **Microsoft Azure "Business continuity and disaster recovery" reference architecture**: same four-tier taxonomy.
* **Google Cloud "Disaster Recovery Planning Guide"**: same taxonomy · additional "Tier 0" cold-backup framing.
* **ISO 22301 "Business Continuity Management Systems"**: the international standard that formalises BCA · this packet's four-tier structure aligns with ISO 22301 §8.4.4 "Recovery strategies and solutions".

### §E.4 · Quarterly restore-drill invariants (owner verbatim: "an untested plan is a hypothesis")

* **BC-4-DRILL-INV-01 · Cadence:** Every quarter (max 90 days between drills).
* **BC-4-DRILL-INV-02 · Scope:** Random restore of 3 artifact classes drawn from the WORM tier (Tier 3) into an isolated recovery environment.
* **BC-4-DRILL-INV-03 · Integrity checks:**
    1. **Row counts** — sample a ledger; count rows before and after restore; must match exactly.
    2. **Checksums** — every restored object's SHA-256 must match the pinned checksum in the object's manifest.
    3. **Invariant runs** — restore triggers a full `BASELINE_GUARD=1 pytest tests/invariants/` run on the restored codebase; ratchet floor must hold (currently 4018).
* **BC-4-DRILL-INV-04 · Drill receipt:** Every drill produces a receipt at `phase0/bc_drill_receipts/<yyyymmddThhmmssZ>_bc_drill.json` with the three integrity-check outcomes.
* **BC-4-DRILL-INV-05 · Failure disposition:** A failed drill triggers an operator MARK write (`BC-DRILL-FAILURE-<uuid>`) — must be resolved before the next drill.

---

## §F · Aggregate RPO / RTO / cost matrix (single summary table for ratification)

| Tier | Asset class | RPO | RTO | Cost | Owner-verbatim justification |
|---|---|---|---|---|---|
| 1 | GPU training runs | ≤ 15 min compute | 5 min same-host · 30 min lost-host | LOW-MED | *"expensive GPU runs must not lose work"* + *"never lose more than ~10–15 min"* |
| 2 | Ledgers / registry / WAL | ~0 (transaction boundary) | ≤ 5 min same-host · ≤ 15 min lost-host | LOW | *"continuous WAL/append archiving → near-zero RPO"* |
| 3 | Artifacts / receipts / seals (WORM) | ~0 for committed objects | ≤ 1 h | MED | *"replication alone faithfully replicates corruption ... snapshots+immutability are a separate layer"* |
| 4 | Site-loss (warm-standby) | ≤ 15 min | hours-not-days | MED | *"warm-standby as the pilot-appropriate option ... far cheaper than active-active"* |

---

## §G · Invariants summary (18 total · to be landed inside the implementation wave · NOT this turn)

* **BC-1-GPU-INV-01..04** (4 invariants) · GPU checkpointing tier.
* **BC-2-LEDGER-INV-01..03** (3 invariants) · Append-only ledger tier.
* **BC-3-WORM-INV-01..04** (4 invariants) · WORM object-storage tier.
* **BC-4-DRILL-INV-01..05** (5 invariants) · Restore-drill tier.
* **BC-CROSS-INV-01** · Aggregate RPO / RTO / cost table pinned in a machine-readable `services/business_continuity/policy.py` module.
* **BC-CROSS-INV-02** · The four `BC_3_PENDING_OVERRIDE` / `BC_4_PENDING_OVERRIDE` sentinels remain in place as "static number refused"; the dynamic policy supersedes the static-number requirement via structured record, not silent-flip.

**Total: 18 invariants target for the implementation wave.**

---

## §H · Implementation-wave charter (proposed, NOT chartered until owner ratifies this packet)

* **Wave name (candidate):** `W-BC-DYNAMIC-RECOVERY-BUILD`.
* **Scope:** land the 18 invariants above under tests-first discipline; author `services/business_continuity/dynamic_recovery/*` (four sub-modules per tier); wire receipt-writes into every ledger write path; author the quarterly-drill harness.
* **Wave-honest limits (to declare on charter):**
    * *E.1 · No live cross-region replication in this wave — implementation lands the invariants + the config; actual second-site provisioning is a separate charter (owner input required for standby-region provisioning).*
    * *E.2 · No object-store immutability provisioning in this wave — the code path is authored, the config is pinned, but the actual bucket-with-object-lock is owner-provisioned when the estate commits to a specific cloud + region.*
    * *E.3 · The Young/Daly τ_opt is measured on-the-fly starting from a conservative bootstrap; no pre-computed cadence table.*
* **Ratchet target:** +18 (per invariant list); target ratchet 4018 → 4036.
* **Prerequisites:** owner ratifies THIS packet.
* **Sequencing:** owner's already-ratified sequencing pins put census → W-RELEASE-GATE-PILOT-LIFT → D12 POC ahead of this wave. This BC wave is a follow-on after those three land.

---

## §I · Position-redaction acknowledgement

Every row above:
- Uses aliases only (`akki-vm`, `akki-vm-ii`, `synology-nas`, `akki-vm-standby`, `synology-nas-standby`).
- Does not echo credentials, host IPs, SSH usernames, or PII.
- Cites disk-file paths and section numbers verbatim.

## §J · Owner ratification checklist

**Please confirm each row · a single "Y" / "N" per row is sufficient:**

- [ ] **Tier 1 · GPU:** PyTorch DCP async + Young/Daly dynamic cadence + five-carrier resume invariant + 10-15 min RPO target
- [ ] **Tier 2 · Ledgers:** Continuous append-archive with transaction-boundary PITR + git-bundle push-to-WORM (pilot-scale) or full WAL archiving (production-scale)
- [ ] **Tier 3 · WORM:** Object-lock in **COMPLIANCE** mode (proposed) vs **GOVERNANCE** mode (alternative) — owner picks mode
- [ ] **Tier 4 · Site-loss:** Warm-Standby (proposed) vs Pilot-Light (cheaper) vs Active-Active (pricier) — owner picks regime + provides standby-site region + provisioning path
- [ ] **Drill cadence:** Quarterly (proposed) vs monthly (heavier) vs biannual (lighter) — owner picks
- [ ] **RPO / RTO matrix (§F):** all four rows acceptable as pinned targets, or amend
- [ ] **Charter `W-BC-DYNAMIC-RECOVERY-BUILD`** with the 18 invariants above post-BC-packet-ratification

After ratification, the implementation wave charters and runs under tests-first discipline like every other wave in the programme.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
