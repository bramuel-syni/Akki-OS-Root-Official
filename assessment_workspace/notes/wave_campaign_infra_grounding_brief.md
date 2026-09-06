# W-Campaign-Infra Grounding Brief · 2026-09-06

**Wave name:** `W-Campaign-Infra` · 3-day unattended GPU campaign machinery + lean r3 items folded in.

**Authority — owner ruling banked verbatim (2026-09-06T~12:17Z via the user):**

> "the owner just asked for a 3-DAY UNATTENDED GPU JOB consuming zero platform credits, and I have proposed (pending his one-line go) a queued LoRA experiment campaign — 2–3 model sizes (0.5B → 7B class), full deduplicated USSD+SMS corpus with proper held-out slices, seeds + ablations, both hosts busy 3 days, everything checkpointed and journaled ON-HOST so no pod-side polling is needed. His greenlight may land any moment and it would supersede the queue.
>
> So instead of plain r3, fire **W-Campaign-Infra** — build the 3-day unattended machinery NOW so launch is ~1 hour of work when the go lands, folding the lean r3 items in (they are the same fabric):
>
> - On-host watchdog (cron/systemd-timer): restarts training from last checkpoint if the process dies; never touches a healthy run (zero-influence: restart-from-checkpoint is recovery, not interference — bank the distinction).
> - Checkpoint/resume training loop: checkpoint every ~30 min, deterministic resume, journal entries per checkpoint (WPW Tier 1 notebook shape).
> - Sequential run-queue runner: executes a declared campaign manifest (list of runs: model, corpus variant, seed, hyperparams, held-out slice spec) one after another per host, sealing each run before the next.
> - On-host self-logging: heartbeat + poll receipts written locally on the host, plus per-run summaries — reconcile path pulls and banks them when a pod session re-attaches (extend the r2 adopt machinery to campaign scope).
> - Lean r3 items folded in: retire_heartbeat on clean exit, sealing-name normalization, PID-aware/include_pid_dead mode on select_adoptable_orphans.
> - Q2 → (a): one lean close, one RED drill receipt covering the primitives; full drill matrix only if free.
>
> HARD GATE unchanged: no estate data flows until the owner's admission ruling lands — build the campaign runner against fixture corpora; the governed extraction slot stays parked behind `MaskingTierNotAdmitted` honest refusal. If the owner's go + admission land mid-wave, bank verbatim, close at a clean boundary, then launch sequence: Shield-Train-run extraction → campaign manifest authored → 3-day launch → detach.
>
> Tests-first with mechanical RED, double-green from floor 2847, local commits only, no push. Go."

---

## Section A · Zero-influence distinction to bank (banked as invariant this wave)

The user's directive names a NEW zero-influence class that must be explicit in the codebase:

> **"restart-from-checkpoint is recovery, not interference"**

Prior zero-influence classes in the codebase (r1/r2/watchdog): observation-only, never signalling anything alive. This wave adds a THIRD class:

**Recovery-not-interference discipline (bind by construction, freeze by invariant):**

1. **Fires only against dead processes.** The on-host watchdog script MUST check process liveness BEFORE any restart action. Restart against a live PID = interference (banned).
2. **Resumes from last checkpoint.** Fresh-start after death = discarding on-host state = interference (banned). The watchdog re-invokes the training run with the last-checkpoint path pinned via env var.
3. **Never touches a live run.** No signals, no state edits, no file writes to the run_dir while the training process is alive.
4. **Journal-on-restart.** Every restart writes an explicit journal entry (WPW-shape record_event) naming the restart action + the checkpoint resumed from + PID of new invocation — restart is observable and attributed, not silent.

Rule freezes this as: `test_on_host_watchdog_refuses_to_restart_live_process` + `test_restart_from_checkpoint_never_deletes_checkpoint` + `test_restart_writes_journal_entry`.

---

## Section B · Module architecture

New package `services/campaign_infra/`:

1. **`manifest.py`** — Campaign manifest schema (list of run declarations), load + validate. One manifest describes an ordered list of runs; each run is `{run_name, model_size_class, corpus_variant, seed, hyperparams, held_out_slice_spec}`. Validation refuses duplicates, refuses missing fields, refuses non-deterministic seeds (must be int).

2. **`checkpoint.py`** — Checkpoint I/O + resume marker. `CheckpointHandle` writes checkpoint files with deterministic name (`checkpoint_step_<n>_<sha>.pt` shape but shape-only in this wave — actual .pt writing is training-loop wave). `resume_from_checkpoint(run_dir)` returns the latest checkpoint's metadata for the trainer to re-init from. `write_checkpoint_marker(run_dir, step, sha)` writes a JSON pointer for the on-host watchdog to read on restart.

3. **`on_host_logging.py`** — On-host heartbeat + poll receipts + per-run summaries. Mirrors the pod-side `orchestrator_resilience/heartbeat.py` but writes to a host-local path (`AKKI_HOST_JOURNAL_ROOT` env var, default `~/akki_journal/`). No pod-side dependency at runtime — the reconciler pulls when a pod session re-attaches.

4. **`run_queue.py`** — Sequential runner over a manifest. `execute_campaign(manifest, host)` iterates entries, sealing each with `ACTIVITY_SUMMARY.md` before starting the next. Refuses to start a run if the prior run isn't sealed. Refuses parallel campaign runs on the same host by construction (fcntl-lock on a per-host state file).

5. **`reconcile.py`** — Pod-side pull-and-bank of on-host journal when a session re-attaches. Extends r2 `adopt.can_adopt` semantics to campaign scope: an on-host campaign run with fresh on-host heartbeat + alive PID is not adoptable (still running); one with stale on-host heartbeat + dead PID is adoptable-with-restart.

6. **`__init__.py`** — package surface exports.

Extensions to existing services:

- **`orchestrator_resilience/heartbeat.py`** — add `retire_heartbeat(run_id) -> bool` (removes heartbeat file on clean exit · zero-influence · returns False on missing file rather than raising). Freeze: `test_retire_heartbeat_removes_file_on_clean_exit` + `test_retire_heartbeat_is_idempotent`.

- **`orchestrator_resilience/orphan_detector.py`** — sealing-name normalization: accept `ACTIVITY_SUMMARY.md` in ANY case variant (case-insensitive existence check). Preserve the canonical name for writers. Freeze: `test_orphan_detector_accepts_uppercase_sealing_filename` + `test_orphan_detector_accepts_lowercase_sealing_filename`.

- **`orchestrator_resilience/watchdog.py`** — `select_adoptable_orphans(include_pid_dead=False)` new keyword: when True, ALSO enumerate runs whose heartbeat is fresh but whose recorded orchestrator PID is dead (currently missed by staleness-gated enumeration). Freeze: `test_select_adoptable_orphans_include_pid_dead_surfaces_fresh_heartbeat_dead_pid` + backward-compat `test_select_adoptable_orphans_default_still_staleness_gated`.

On-host script:

- **`tools/on_host_watchdog.sh`** — bash script for cron/systemd-timer. Reads `AKKI_ON_HOST_WATCHDOG_TARGETS_DIR` env for run dirs to supervise. Per target: (a) read the checkpoint marker + campaign manifest, (b) check the training process PID's liveness via `ps -p <pid>`, (c) if alive, exit 0 (no interference), (d) if dead, invoke the trainer with `--resume-from <checkpoint>` and write a journal entry naming the restart.

---

## Section C · HARD GATE preservation

- Governed row-bearing extraction (`services/shield_train/pipeline.execute_governed_lora_run`) stays parked behind `MaskingTierNotAdmitted` until owner rules on `admissible_under_env`.
- Campaign infra MUST work against fixture corpora (test fixtures + local test JSONL) with no dependency on real estate reads.
- Regression invariant: `test_campaign_infra_does_not_bypass_masking_tier_admission` calls `execute_campaign` with a manifest that would need governed extraction, asserts `MaskingTierNotAdmitted` still raises before any training-loop entry.

---

## Section D · Definition of Done

1. All 6 new modules in `services/campaign_infra/` exist + tested.
2. All 3 r3 extensions land in existing files + tested.
3. On-host watchdog script exists + tested for surface + zero-influence.
4. Mechanical RED drill receipt banked (right-reason ImportError/AssertionError/FileNotFoundError before any impl).
5. Double-green from floor 2847 with byte-match pass/skip/warning tallies.
6. HARD GATE preserved: extraction slot still refuses via `MaskingTierNotAdmitted`.
7. Zero-influence recovery-not-interference distinction frozen by invariant.
8. STATE mirror commit on `master` (DoD-named) + auto-emitter lump commit if diff exists.

---

## Section E · Wave-honest-limits (banked in advance)

1. **Training loop itself is NOT this wave.** Checkpoint I/O writes SHAPE-only (JSON marker files with expected fields). Actual .pt tensor persistence lands in the training-loop wave (natural follow-on after admission).
2. **No cron installation this wave.** The on-host watchdog script is authored + tested-for-shape; installation on the actual GPU hosts is a separate operator action (banked as follow-on).
3. **Reconcile pulls journal artefacts, does not stream them.** Real-time journal streaming would need a pod↔host push channel. Pull-on-attach is enough for the 3-day-then-reconcile pattern.
4. **On-host self-logging path is fixed** (`AKKI_HOST_JOURNAL_ROOT` env, default `~/akki_journal/`). Per-host divergent paths are a future concern.
5. **Manifest schema is v0.** Hyperparams field is dict-typed but not schema-validated (any dict shape). Model-size-class is a string ("0.5B", "1.5B", "7B") not a rigorous enum.

---

## Section F · Commit protocol

- Track-a: single close commit "W-Campaign-Infra-close" — 6 modules + 3 r3 extensions + watchdog script + comprehensive test file + baseline_failures.json bump.
- Master: DoD-named mirror commit + auto-emitter lump if working-tree diff exists.
- No push.

*Grounding brief authored 2026-09-06T~12:20Z pre-RED. All requirements traced verbatim to the user's ruling.*
