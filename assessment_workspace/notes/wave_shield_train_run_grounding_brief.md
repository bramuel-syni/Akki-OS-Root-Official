# W-Shield-Train-run · grounding brief

**Authored:** 2026-09-06T~13:XXZ (post-Phase-A reach-verification session)
**Discipline:** STRICT tests-first · mechanical RED before impl · double-green from floor 2894 · two-commit pattern · no push.

---

## §Authority · owner ruling verbatim (2026-09-06T~13:XXZ, via user proxy)

> "Blocker acknowledged — and it's not a surprise gap, it's the chartered W-Shield-Train-run wave arriving exactly on schedule: the build wave landed primitives + admission, the run wave wires the actual training call. The owner's campaign authorization covers it. AUTHORIZED: author W-Shield-Train-run NOW as the final leg of the launch.
>
> Scope, tests-first with mechanical RED:
> 1. ON-HOST TRAINER ARTIFACT (trainer.py or equivalent, deployed to ~/akki_journal/): consumes a masked corpus JSONL + run spec (model, LoRA params, seed, ctx len, held-out slice ref), runs the LoRA fine-tune with: checkpoint every ~30 min + deterministic resume-from-checkpoint (the watchdog contract), journal/heartbeat writes per the campaign_infra on_host_logging shape, held-out eval at end (loss/perplexity on the banked slice — the campaign's measurement core), final seal record with adapter sha256. DONOR MATERIAL: the first LoRA run (txttrain_20260831T193455Z) had a WORKING training payload authored through the seam — find it in the receipts/phase0/text_train_pipeline artifacts and reuse its proven parts (dataset load, LoRA config, bf16 setup for H200) rather than re-inventing. Review-then-adopt, same discipline as the orchestrator donor diff.
> 2. UNSTUB execute_governed_lora_run: replace the NotImplementedError with the real composition — governed extraction (already built) → masked corpus file + sha256 → stage_corpus_to_host → invoke trainer detached → return run handle. Tests against fixture backend as the pipeline module already supports.
> 3. WIRE trainer_fn into campaign_infra.run_queue for production: the campaign runner's injected trainer_fn becomes the real on-host invocation via the seam. Keep injection (testability) — production wiring is just the default binding.
> 4. HELD-OUT SLICE FIRST (STEP 2 order unchanged): bank the deterministic split + sha256 BEFORE any training byte moves.
> 5. Then LAUNCH per the banked sequence: extraction receipts → rsync (manifests + trainer + watchdog + on_host_logging) to both hosts → watchdog cron install → detached launch A (akki-vm) + B (akki-vm-ii) → first heartbeat + first checkpoint + GPU-util evidence → bank receipts → commit both trees (two-commit pattern) → STAND DOWN per runbook.
>
> Trim honestly if needed: if authoring + testing the trainer pushes launch past today, cut Campaign A's 7B run or B's ctx-2048 BEFORE cutting anything else — window integrity beats ladder completeness. Double-green from floor 2894 for the invariant changes. Credentials redacted everywhere. Report launch confirmation with first-heartbeat evidence. Go."

---

## §A · Donor material (review-then-adopt)

**Source**: `/app/assessment_workspace/tools/text_train_pipeline/train_payload.py` (305 lines, dated 2026-08-31) plus receipts at `/app/assessment_workspace/phase0/text_train_pipeline/txttrain_20260831T193455Z_9594859a/` (adapter.sha256 = `a3693049…8468`, corpus.sha256 = `484a174c…dcc8`, adapter.tar.gz landed).

**Adopted verbatim from donor**:
- HF loader shape: `AutoTokenizer.from_pretrained(base, trust_remote_code=True)` + `AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.bfloat16, trust_remote_code=True)`.
- Tokenizer pad→eos fallback.
- LoraConfig: `r=<rank>, lora_alpha=2*r, lora_dropout=0.05, bias='none', task_type=TaskType.CAUSAL_LM, target_modules=['q_proj','v_proj']`.
- `_CorpusDataset(torch.utils.data.Dataset)` returning `input_ids` + `attention_mask` at `max_seq_len`.
- `DataCollatorForLanguageModeling(mlm=False)` for causal-LM label shift.
- `TrainingArguments(bf16=True, save_strategy='epoch', logging_steps=25, dataloader_num_workers=2, report_to=[])`.
- `Trainer` with a `TrainerCallback` subclass (`_StepLogger`) emitting JSONL per `on_log` + `on_epoch_end`.
- `_sha256_dir(adapter_out)` walk-hash for adapter integrity.

**Extended (this wave)**:
- Callback ALSO writes `campaign_infra.on_host_logging.write_host_heartbeat` per step, `.write_host_poll_receipt` at every `logging_steps` boundary, `campaign_infra.checkpoint.write_checkpoint_marker` per epoch (matching `save_strategy='epoch'`).
- `--resume-from` CLI flag: if set, honored by passing `resume_from_checkpoint=<path>` to `trainer.train()`.
- Held-out slice loaded from banked JSONL; final held-out eval computes causal-LM loss + perplexity on the slice; result banked in `write_run_summary` (`final_loss` field carries held-out loss, not train loss).
- Trainer exits with `write_run_summary(...)` → this is the `ACTIVITY_SUMMARY.md` write that the run_queue sealer reads.

**NOT adopted from donor** (deliberate divergence):
- Donor bypassed the governed row_executor (`ruling6_bypass` masking_tier). This wave routes the row-bearing extraction THROUGH `services.shield_train.row_executor.execute_row_bearing_query` under `t1_full_mask` + `AKKI_ENV=development` (the admitted tier + env from the 2026-09-06T~12:XXZ admission).

---

## §B · Composition (execute_governed_lora_run unstub)

Replaces the `NotImplementedError` at `services/shield_train/pipeline.py:242`. New composition (in order):

1. **Admission gate** — unchanged. `chokepoint.masking_tier.validate_tier(tier, akki_env=env)`.
2. **Build governed SELECT** — from `masking_policy.v0.json` ledger entries for `table_context`, enumerate columns whose `action ∈ {include, mask_regex_scrub}`. Compose `SELECT c1, c2, c3 FROM {table_context} LIMIT :slice_size` (or unlimited if `slice_size=0`). ORDER BY primary key for determinism (`id` on `ussd_question_response`, excluded from SELECT but usable in ORDER BY).
3. **Governed extraction** — call `row_executor.execute_row_bearing_query(sql, params, database, table_context, principal, purpose, backend_execute)`. This fires the row-bearing chokepoint receipt at `phase0/shield_train_receipts/`.
4. **Compose training_text** — for each row, build `training_text = f"[value_chain: {value_chain}]\nQ: {question_string}\nA: {option_string}"` (matches donor's field name). Drop rows with empty Q or empty A.
5. **Deterministic held-out split** — `held_out.deterministic_20pct_tail_split(rows, seed=31337)` returns `(train_rows, held_out_rows, split_meta)` with `held_out_sha256` + `train_sha256` and monotonic tail selection (last 20% by row_index post-sort-by-primary-key).
6. **Bank held-out slice hash PREFLIGHT** — `held_out.bank_held_out_slice_hash(run_id, table_context, split_meta, out_dir=phase0/shield_train_receipts/held_out_slices/)`. Written BEFORE any bytes cross to host. Receipt carries `banked_before_first_run_starts=True` boolean.
7. **Build masked corpus files** — `pipeline.build_masked_corpus_file(train_rows, corpus_path)` + `pipeline.build_masked_corpus_file(held_out_rows, held_out_path)`. Belt-and-braces PII-shape leak-check refuses on either write.
8. **Stage both corpora to host** — `pipeline.stage_corpus_to_host(corpus_meta, host_slug, remote_dir, ssh_seam)` + same for held_out. sha256-verified transport.
9. **Return handle** — dict shape:
   ```python
   {
     "receipt_utc": "...",
     "run_id": "...",
     "tier": "t1_full_mask",
     "env": "development",
     "host_slug": "akki-vm",
     "row_extraction_receipt_path": ".../phase0/shield_train_receipts/...json",
     "held_out_slice_receipt_path": ".../phase0/shield_train_receipts/held_out_slices/...json",
     "train_corpus": {"path", "sha256", "row_count", "bytes"},
     "held_out_corpus": {"path", "sha256", "row_count", "bytes"},
     "stage_receipts": [{...}, {...}],
   }
   ```

Zero-influence: any failure raises typed exception (`MaskingTierNotAdmitted`, `UnclassifiedRefusal`, `PolicyRefusal`, `SqlShapeRefusal`, `CorpusIntegrityRefusal`, `TransportIntegrityRefusal`). No partial-success silent-return.

---

## §C · production_trainer default binding (campaign_infra.run_queue trainer_fn)

New module `services/campaign_infra/production_trainer.py` exports `default_trainer_fn(run_name, manifest_entry, host)` that wires:
- Real `backend_execute` = adapter over `services.connect.rds_data_submit.get_rds_data_client(region)` (production RDS Data API).
- Real `ssh_seam` = adapter over `services.training_runner.ssh_seam.execute_remote_command` (governed remote exec seam).
- Calls `execute_governed_lora_run(tier='t1_full_mask', recipe_version=<manifest.recipe_version>, base_model_id=<manifest.base_model_id>, ..., backend_execute=..., ssh_seam=...)`.
- Invokes on-host trainer detached via `ssh_seam.execute_remote_command(host_slug, "setsid nohup python3 ~/akki_journal/on_host_trainer.py --run-id ...", purpose="lora_train_detached")`.
- Returns run-handle for `run_queue` to observe.

Keep injectability: `default_trainer_fn` accepts an optional `_seam_override` kwarg for tests.

---

## §D · on_host_trainer.py contract

Deployed to `~/akki_journal/on_host_trainer.py` on each GPU host via rsync. Consumes CLI args:
- `--run-id` (required) · `--run-dir` (required, e.g. `~/akki_journal/<campaign_id>_<run_name>`)
- `--campaign-id` · `--run-name`
- `--corpus <path>` (train JSONL) · `--held-out <path>` (held-out JSONL)
- `--base-model` (e.g. `Qwen/Qwen2.5-0.5B`)
- `--seed` · `--lora-rank` (LoRA r) · `--ctx-len` (max_seq_len)
- `--per-device-batch` · `--grad-accum` · `--lr` · `--num-epochs`
- `--resume-from` (optional; checkpoint dir path if resuming after watchdog restart)

Writes (via `on_host_logging` + `checkpoint`):
- `~/akki_journal/<run_id>/heartbeat.json` — replaced every logging_step (each `on_log` callback).
- `~/akki_journal/<run_id>/polls/poll_step_<step>.json` — one per logging_step.
- `~/akki_journal/<run_id>/checkpoint_marker.json` — replaced per epoch (matches `save_strategy='epoch'`).
- `~/akki_journal/<run_id>/adapter/` — HF `save_pretrained` output.
- `~/akki_journal/<run_id>/adapter.sha256` — walk-hash of adapter dir.
- `~/akki_journal/<run_id>/held_out_eval.json` — `{loss: float, perplexity: float, n_examples: int}` from causal-LM eval on the held-out JSONL.
- `~/akki_journal/<run_id>/ACTIVITY_SUMMARY.md` — sealing marker via `on_host_logging.write_run_summary`. Final loss = held-out loss.
- `~/akki_journal/<run_id>/train.log` — donor-shape JSONL log.

Zero-influence: exceptions surface as JSONL `{"kind":"fatal", ...}` and non-zero exit; no partial ACTIVITY_SUMMARY.

---

## §E · Held-out slice discipline (owner-explicit)

Deterministic 20% tail selection:
- After row_executor emits N rows in primary-key order (deterministic), the LAST `floor(N * 0.20)` rows are the held-out slice.
- Seed=31337 (from manifest `held_out_slice_spec: "deterministic_20pct_tail_seed_31337"`) is a doc-string identity, not a shuffle key — the tail selection is fully deterministic on row order.
- `train_sha256` = sha256 of train JSONL; `held_out_sha256` = sha256 of held-out JSONL. Both banked BEFORE any bytes cross to host.
- Receipt file at `phase0/shield_train_receipts/held_out_slices/held_out_<run_id>_<utc>.json` names both hashes + row counts + seed + banked_before_first_run_starts=True.

---

## §F · Wave-honest-limits (banked pre-close)

1. **Held-out eval is loss/perplexity only this wave.** Task-shaped eval (e.g. exact-match accuracy on the option-picking task) is a follow-on charter. Loss/perplexity is enough to establish the Promise-#24 baseline_record shape's minimum viable form (the CIF-ideation "measured delta vs baseline" mechanism can work on loss deltas alone).
2. **No task-shaped eval means "measured" is loss-shaped only.** Objective 1 (baseline_record) is partly satisfied — the WPW Tier 2 report drafter must acknowledge this in its acceptance-criteria copy. Loss-alone is the honest cap this wave.
3. **The on-host trainer does not sandbox `pip install` failures.** If transformers/peft/bitsandbytes are not installed on a host, the trainer emits `{"kind":"fatal","err":"transformers/peft import failed"}` and exits non-zero. The watchdog will restart intent-record but cannot recover without operator install.
4. **Adapter files are HF `save_pretrained` output, not `.pt` tensor.** Matches donor. `.pt` persistence remains follow-on.
5. **Watchdog restart bumps the resume-from step marker by one epoch,** not one gradient step. Fine-grained mid-epoch resume needs gradient-step checkpointing (a future wave). Matches `TrainingArguments(save_strategy='epoch')` fidelity.
6. **Row-executor batch fetch:** the row_executor pulls the whole slice into memory before writing the corpus JSONL. For 30k rows × 3 columns this is ~5MB (matches donor). For a full-table extract (~903k rows) this would be ~150MB — still fits comfortably in memory on the pod. If a future wave needs >1M rows this must batch. Banked for future waves.

---

## §G · New facts banked in this wave (owner-approved)

- **AWS credentials custody path**: `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json` (mode 0600, git-ignored via `estate_keys/.gitignore`). Standing credentials written by `services.connect.rds_data_submit._write_standing_creds`. Future sessions look HERE FIRST before declaring credentials lost.
- **akki-vm rebuild finding**: 5.9T volume mount SURVIVED at `/mnt/volume_dkgjrkx` but was WIPED (28K used post-rebuild). `~/akki_journal/` is GONE. Torch stack (2.11.0+cu128, 2×H200) SURVIVED. New GPU UUIDs differ from pre-rebuild. Akki-vm-ii unaffected.
- **DigiCow reach fact**: read access covers BOTH `digicow_live` AND `ndume` databases entirely. `ndume` becomes corpus-eligible for FUTURE waves (chartered follow-on, not this campaign). Current campaign manifests unchanged.
- **SSH host-key change**: `41.173.184.244` ed25519 fingerprint `SHA256:bTjxxKDWKHhPUA4Zz/BIU3W4yK/quLUAfJrW6Vgy1Ec` (post-rebuild). Old ecdsa entry flushed from `/root/.ssh/known_hosts` with backup at `.old` per OpenSSH's own emitted command.

---

## §H · Commit protocol

- Code lands on `Extraction-Akki` branch `programme/track-a` (local commit; NEVER pushed).
- STATE + receipts + grounding brief land on workspace `master` (local commit; NEVER pushed).
- Double-green from floor 2894 → target floor after this wave (ratchet_history append + counts_at_baseline.passed + invariants_enforced_when_baseline_guard_1.passed_floor in tandem — the manifest self-check invariant fires right-reason if tandem missed).
- Receipts: mechanical RED · double-green run1 · double-green run2 · post-launch heartbeat evidence.
