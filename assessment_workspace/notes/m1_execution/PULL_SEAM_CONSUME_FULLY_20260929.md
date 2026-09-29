# M1 P0 — pull-seam census made to consume fully · 29 Sep 2026

Owner directive: holistic census on akki-vm (entire deep census as designed),
consume fully. E1 is control plane only; akki-vm is worker of record; the estate
(NAS/MySQL) is reachable only from the jump host, so akki-vm runs the reviewed
bundle and hops to the jump via the pull seam. No estate bytes touch E1 or the GPU.

## Root causes found (live, not assumed)

1. NAS traversal timed out because CIFS directory listing on the jump host is
   RTT-bound (`ping` avg 57.4 ms to 10.10.55.55) and getdents/stat do NOT scale
   with threads on a single CIFS session (measured: 4→95 files/s ceiling, 1 vCPU,
   `nproc=1`). A whole multi-TB share cannot be walked inside one bounded job.
2. MySQL receipt truncated at exactly 3×64 KiB. paramiko `exit_status_ready()` can
   fire while stdout is still in flight; the old drain broke early → `JSONDecodeError`.

## Fixes (all files under services/census_autonomy)

- `deep_files.py` rewritten: enumeration is **resumable**. A durable frontier
  (directory paths for NAS; continuation tokens + compact 16-byte ETag+size
  fingerprints for OBS) is checkpointed on the admitted worker only, every 30 s and
  at end of pass. A shared work queue commits a directory only when fully scanned.
  Each pass reports cumulative totals + `directories_pending`/`progress_this_run` +
  `epoch`/`runs_in_epoch`. Completing a share starts a fresh epoch (re-census) and
  banks the previous epoch summary. An flock refuses concurrent runs of the same
  scope (`ENUMERATION_ALREADY_RUNNING`). Parallelism defaulted to 2 (throughput does
  not scale on one CIFS session). Checkpoint dir `CENSUS_REMOTE_STATE_DIR` on worker.
- `deep_dispatch.py` / `deep_pull.py`: drain until channel **EOF** (`eof_received`),
  not just exit-status → fixes the MySQL truncation. Added SSH `set_keepalive(30)`
  so hour-long silent jobs survive stateful middleboxes.
- `operational_runner.py`: `continue_if_resumable()` — a finished PARTIAL run whose
  sources report `resumable + BUDGET_EXHAUSTED + progress>0` auto-enqueues a
  successor for exactly those sources (idempotency `{run_id}-continue`), so the
  supervised scheduler carries "consume fully" across passes with NO agent in loop.
  Additive and guarded — never fails the primary run; a stalled (progress 0) or
  complete or non-resumable outcome does NOT continue.

## Live evidence (this session, real transport, sanitized receipts)

- MySQL `cr-3b6b013458de`, akki-vm→jump pull seam, wall 16.2 s, receipt 1.97 MB
  (no truncation): **6/7 scopes COMPLETE — 20 databases, 1013 tables, ~239.6M
  estimated rows**. Only `artists_app` blocked `AUTHENTICATION_FAILED` (needs a
  MySQL GRANT — owner/estate dependency; banked as a response-required item).
  Latest registry record now reflects these totals; PARTIAL (artists_app open).
- NAS pull seam actively consuming through the scheduler: epoch 1, run 2,
  84,616 files across 16 channels, 310 dirs done, 4,844 pending, checkpoint sha
  advancing. Bounded probes confirmed cumulative growth (run1 4,388 → run2 13,794
  files) and clean partial flush with `pull_seam.inner_wall_seconds`.
- OBS resumable listing proven by probe: 99+ buckets, per-bucket continuation
  resumes; NoSuchBucket/ClientError surfaced per bucket, not fatal.

## Honest boundary

- The deep census produces metadata + sampled media probes (ffprobe duration on
  ≤3 path-hash-pinned media per channel), NOT transcription or language labels.
- "Consume fully" for a multi-TB archive is inherently many bounded passes; it now
  runs autonomously and losslessly (worker checkpoint). Not a single-pass claim.
- Tests: pull-seam-hop + deep-dispatch-transport + Watch-M2 mocked suites pass;
  116 census_operational tests pass. Pre-existing `test_execution.py` t08/t09
  failures reproduce identically at git HEAD (legacy aggregate-protocol tests) —
  not introduced here.

## akki-vm-ii training readiness (ground truth, real SSH telemetry)

2× NVIDIA H200 143 GB, both idle (0 %, 0 MiB), no GPU compute processes. `nvcc`
not on PATH. torch/torchaudio/transformers/peft/speechbrain/datasets/accelerate
ALL MISSING in system python and the census venv. 5.9 TB `/mnt/volume_dkgjrkx`
empty (28 KB used). No base-model weights, no labelled corpus, no split on disk.
Language-cognition training cannot legitimately launch until the framework is
provisioned, a base model is registered, and a labelled code-switched
speaker-disjoint corpus is assembled — none may be mocked (MUST-NOT §9).
