# Campaign v2 · Window-Fill Math + Corpus-Consistency + Runbook

**Authored:** 2026-09-06T~16:50Z  
**Wave:** W-SMS-Body-Emit (governance leg) → Campaign v2 relaunch (operational leg)  
**Authority:** owner corrections banked verbatim in the current session:

> CORRECTION 1 — Diagnose WHY akki-vm is idle BEFORE re-basing … [(a) drained vs (b) dispatcher died — bank as evidence for W-Queue-Watchdog]. Pull and bank any sealed runs' results (A-0 at minimum: held-out loss/PPL, adapter hash) while you're in there — that's reconciliation material.  
>
> CORRECTION 2 — CORPUS-CONSISTENT COMPARISONS … the re-based queues constitute CAMPAIGN v2 — ALL ladder runs (including re-runs of any sealed sizes, A-0 included) and ALL ablation runs execute on the NEW corpora, so every comparison is corpus-consistent. Already-sealed v1 runs stay banked untouched as labelled pilot records (nothing deleted — they're honest pilots that shaped v2, and wizard-testing material). B1 same treatment: if it seals on the old corpus, it banks as pilot and a corpus-consistent B1-v2 joins the queue.  
>
> CORRECTION 3 — A-3-7B placement: keep manifest ladder order in v2 (0.5B → 1.5B → 3B → 7B) rather than firing 7B first on the idle host — ladder order keeps early results flowing while the long 7B anchors the tail. If the window math shows the full v2 ladder + 7B doesn't fit at measured throughput, trim 7B to 1 seed (never trim the corpus-consistency rule).

---

## §A · Diagnosis verdict (CORRECTION 1 · complete)

**Answer: (b) DISPATCHER DIED.** Right-reason bug on both dispatchers; A-0-v1 sealed successfully, A-1-1p5B and A-2-3B never launched.

| Fact | Evidence |
|---|---|
| A-0-v1 sealed cleanly | `phase0/gpu_receipts/20260906T160900Z_diagnosis/akki-vm/ACTIVITY_SUMMARY.md` completed_at_utc 2026-09-06T15:00:56Z · started 2026-09-06T14:10:02Z (**50 min 54 s**) · train_loss 0.2799 · **held_out_loss 0.1232** · **held_out_ppl 1.1311** · n_held_out 5127 · **adapter_sha256 `49735d51ea7371eae6a7fe39ceed5f1160f969bf86a80b1a86d9eafaa046e55a`** |
| Dispatcher died 15:01:13Z | `phase0/gpu_receipts/20260906T160900Z_diagnosis/akki-vm/dispatcher.log` — 2 dispatch_error entries (A-1, A-2) with `err: "SubprocessError: Exception occurred in preexec_fn."` at 15:01:13.458–.461Z (0.003 s apart), then `dispatcher_completed` at 15:01:13.461Z |
| Root cause | `tools/on_host_queue_dispatcher.py::_dispatch_trainer` combined `start_new_session=True` AND `preexec_fn=os.setsid` on `subprocess.Popen`. start_new_session already invokes setsid before exec; adding preexec_fn=os.setsid causes second setsid, which raises PermissionError (child already session leader) → wrapped as SubprocessError |
| Fix banked in-wave | Removed `preexec_fn=os.setsid`; `start_new_session=True` alone provides nohup semantics. Test `tests/invariants/test_dispatcher_no_double_setsid.py` (2 invariants) freezes both fix and diagnosis-receipt path |
| Deployed | sha256 `9bd7f46f21e4ef09e366800659689ee3c28fbb1f67c7d7f44e6c19f80d0aba36` on **both** akki-vm and akki-vm-ii at `/home/ubuntu/akki_journal/on_host_queue_dispatcher.py` (2026-09-06T~16:45Z) |
| Broader scope banked | W-Queue-Watchdog wave remains chartered separately (heartbeat health check + auto-relaunch of dead dispatchers; the double-setsid was one root cause, not the whole watchdog story) |

---

## §B · A-0-v1 measured throughput (window-fill math anchor)

| Metric | A-0-v1 (Qwen2.5-0.5B, LoRA r=16, ctx=1024) |
|---|---|
| Corpus (train / held-out) | 20,510 train + 5,127 held-out rows (deduped) |
| Total steps | 963 (3 epochs × 321 steps/epoch) |
| Wall-clock train | 2,823 s ≈ **47 min** |
| Held-out eval | 224 s ≈ **3 min 44 s** |
| Total wall-clock | 3,054 s ≈ **50 min 54 s** |
| Steps/s | 0.341 |
| Samples/s | 21.796 |
| Per-row train time | 47 min ÷ 20,510 rows ≈ **8 s per 100 rows @ 0.5B** |

**Model-size scaling assumption (H200 · LoRA · 3 epochs):**
- 0.5B → baseline (1.0×)
- 1.5B → ≈ 3.0× (linear in parameter count for LoRA forward+backward)
- 3B → ≈ 6.0× (with per_device_batch dropped 8→2 and grad_accum raised 4→16 — offsets partial; empirical calibration required)
- 7B → ≈ 14× (batch dropped further to 1)

---

## §C · Window-fill math (target 85–90 %)

**Now:** 2026-09-06T~16:50Z · **Window end:** 2026-09-09T23:59Z · **Remaining:** ~79 hours
- akki-vm idle · budget: **~79 h**
- akki-vm-ii running B1-v1 · budget: **~79 h − (B1-v1 remaining ≈ 3 h) − (v2 rebank staging ≈ 1 h) = ~75 h** available for v2 B-queue

**Target fill (85–90 %):** akki-vm ~67-71 h · akki-vm-ii ~64-68 h

### Slice-size probe strategy (empirical, not fitted)
Start slice_size_per_table = **100 K rows** for the first extraction. This yields (based on v1 dedup ratios of ~80 %):
- `ussd_deduplicated` (A corpus, single table): ~80 K unique rows → ~64 K train + 16 K held-out
- `ussd_plus_sms_deduplicated` (B corpus, both tables): 200 K raw → ~160 K unique → ~128 K train + 32 K held-out
- `ussd_plus_sms_raw` (B2 corpus): 200 K raw → 200 K → ~160 K train + 40 K held-out

**If row_executor binds** before extraction completes, cap at whatever slice_size the extractor accepts and re-project. Bank W-Row-Stream-Extractor as the next wave (chartered in SPRINT_PLAN).

### Projected runtimes at 100 K/table (linear scaling from A-0-v1 anchor)

**Campaign A (v2 ladder on akki-vm, single-table ussd_deduplicated ~64 K train):**
| Run | Size | Est. train wall-clock | Note |
|---|---|---|---|
| A-0-v2 | 0.5B | ~2 h 30 m | 47 min × (64/20.5) |
| A-1-v2 | 1.5B | ~7 h 30 m | 3× base |
| A-2-v2 | 3B | ~15 h | 6× base |
| A-3-v2 | 7B | ~35 h | 14× base · **1 seed only** (window-fit) |
| **Ladder total** | | **~60 h** | ~76 % fill; leaves ~19 h margin |

**Campaign B (v2 ablations on akki-vm-ii, dedup + raw variants ~128–160 K train):**
| Run | Config | Est. wall-clock | Note |
|---|---|---|---|
| B-REF-v2 | 3B · dedup · r=16 · ctx=1024 | ~10 h | 6× base × (128/20.5) |
| B1-v2 | 3B · **ussd-only** · dedup · r=16 · ctx=1024 | ~5 h | ussd-only corpus ~64K rows |
| B2-v2 | 3B · **raw** · r=16 · ctx=1024 | ~13 h | 160K rows |
| B3-v2 | 3B · dedup · **r=8** · ctx=1024 | ~9 h | lower rank → faster |
| B4-v2 | 3B · dedup · **r=32** · ctx=1024 | ~11 h | higher rank → slower |
| B5-v2 | 3B · dedup · r=16 · **ctx=512** | ~7 h | half context |
| B6-v2 | 3B · dedup · r=16 · **ctx=2048** | ~15 h | double context |
| **B queue total** | | **~70 h** | ~88 % fill on akki-vm-ii ✓ |

**Total fill projection:** akki-vm 60/79 h ≈ 76 % · akki-vm-ii 70/75 h ≈ 93 % (over target on B — trim B6-v2 to 1 seed or drop B6 first if window compresses; NEVER trim corpus-consistency).

Empirical re-calibration required after A-0-v2 seals: measure actual scaling factor for 1.5B/3B/7B; adjust manifest before firing A-3-v2 (7B is the biggest window risk).

---

## §D · Pilot vs v2 boundary (CORRECTION 2 · complete)

| Cohort | Corpus | Status |
|---|---|---|
| A-0-v1 | ussd_deduplicated (v1 · 25.6 K rows) | **SEALED 2026-09-06T15:00:56Z** · banks as labelled pilot record · adapter_sha256 `49735d51ea…` |
| B1-v1 | ussd_deduplicated (v1 · 25.6 K rows) | **MID-TRAINING on akki-vm-ii** (step 400/963 as of 16:04Z; ETA ~18:30Z) · will seal as labelled pilot |
| A-{0,1,2,3}-v2 | ussd_deduplicated (v2 · 100 K slice → ~64 K train) | **TO EXTRACT + RUN** post-fix (this session bank + next-session ops) |
| B-{REF,1,2,3,4,5,6}-v2 | ussd_plus_sms_deduplicated (v2 dedup group) + ussd_plus_sms_raw (v2 raw group, B2 only) | **TO EXTRACT + RUN** |
| Cross-boundary comparisons | ❌ **BANNED** — v1 vs v2 comparisons confound the ablation variable with corpus drift |
| Intra-cohort comparisons | ✅ v1-pilots compare among themselves (only A-0-v1 pilot exists in Campaign A; B1-v1 sits alone as USSD-only pilot); v2 runs compare among themselves per the campaign design |

**Reconciliation record:** `phase0/campaign_drafts/campaign_b_corpus_swap_v2.json` (authored this session, invariant-frozen).

---

## §E · Runbook · v2 corpus extraction + queue relaunch (operational)

**Prerequisites (this session, all banked):**
- ✅ Dispatcher fix deployed to both hosts
- ✅ Ratchet at 2978 (double-green from 2956 → 2976 → 2978 · SMS-Body-Emit + dispatcher fix)
- ✅ v2 manifest design authored (§F below)
- ✅ Window-fill math projected

**Operational steps (deferred to next session · one-shot script):**

1. **Empirical row_executor probe.** From pod (or via ssh), run:
   ```bash
   cd /app/assessment_workspace/repos/Extraction-Akki/backend && \
     python -c "from services.shield_train.pipeline import execute_governed_lora_run; \
       ...  # dry_run=True with slice_size_per_table=100000"
   ```
   Confirm row_executor accepts 100 K/table without OOM. If it binds, cap slice_size and note W-Row-Stream-Extractor.

2. **Trigger v2 extractions.** Three extractions:
   - `ussd_deduplicated_v2` (single-table USSD, dedup on, slice=100 K) → new run_id `shield-train-campaign-a-v2-multi-table-20260906T171000Z` (name TBD by dispatcher timestamp)
   - `ussd_plus_sms_deduplicated_v2` (both tables, dedup on, slice=100 K each) → new run_id
   - `ussd_plus_sms_raw_v2` (both tables, dedup off, slice=100 K each) → new run_id
   
   Corpora auto-staged to both GPU hosts via `campaign_infra.production_trainer` default binding.

3. **Hash pre-flight.** Bank sha256s of `train_corpus.jsonl` + `held_out_corpus.jsonl` for each v2 corpus at `phase0/shield_train_receipts/held_out_slices/held_out_shield-train-*_v2_*.json` **BEFORE any v2 trainer starts** (per Ruling: banked_before_first_run_starts=True).

4. **Author v2 queue manifests.**
   - `phase0/campaign_drafts/campaign_a_v2_queue_manifest.json` — 4 runs in ladder order (A-0 → A-1 → A-2 → A-3, all seed=1)
   - `phase0/campaign_drafts/campaign_b_v2_queue_manifest.json` — 7 runs (B-REF, B1, B2, B3, B4, B5, B6 all seed=1). Queue behind B1-v1's ACTIVITY_SUMMARY.md so B1-v1 is not disturbed.

5. **Launch dispatchers.**
   - akki-vm: `setsid nohup python3 ~/akki_journal/on_host_queue_dispatcher.py --queue-file /home/ubuntu/akki_journal/queue/campaign_a_v2_queue.json --campaign-id campaign-a-v2-ladder-20260906 >> ~/akki_journal/queue/campaign_a_v2_dispatcher_stdout.log 2>&1 </dev/null &`
   - akki-vm-ii: same shape with campaign_b_v2. Set `wait_for_run_id` on the first v2 entry to B1-v1's run_id so v2 queue only fires after B1-v1 seals cleanly.

6. **Verify heartbeats fresh** (< 5 min old) then STAND DOWN per runbook.

---

## §F · Campaign v2 manifest design (banked, extraction+launch pending)

### Campaign A v2 · baseline ladder · akki-vm
```
A-0-v2  · Qwen2.5-0.5B · seed=1 · corpus=ussd_deduplicated_v2  · r=16 · ctx=1024 · batch=4·acc=8  · epochs=3 · ~2h30m
A-1-v2  · Qwen2.5-1.5B · seed=1 · corpus=ussd_deduplicated_v2  · r=16 · ctx=1024 · batch=4·acc=8  · epochs=3 · ~7h30m
A-2-v2  · Qwen2.5-3B   · seed=1 · corpus=ussd_deduplicated_v2  · r=16 · ctx=1024 · batch=2·acc=16 · epochs=3 · ~15h
A-3-v2  · Qwen2.5-7B   · seed=1 · corpus=ussd_deduplicated_v2  · r=16 · ctx=1024 · batch=1·acc=32 · epochs=3 · ~35h [tail anchor]
```

### Campaign B v2 · method ablations · akki-vm-ii (waits behind B1-v1)
```
B-REF-v2 · 3B · seed=1 · corpus=ussd_plus_sms_deduplicated_v2 · r=16 · ctx=1024 · batch=2·acc=16 · epochs=3 · ~10h [REFERENCE anchor]
B1-v2    · 3B · seed=1 · corpus=ussd_deduplicated_v2          · r=16 · ctx=1024 · batch=2·acc=16 · epochs=3 · ~5h  [corpus=USSD-only ablation]
B2-v2    · 3B · seed=1 · corpus=ussd_plus_sms_raw_v2          · r=16 · ctx=1024 · batch=2·acc=16 · epochs=3 · ~13h [dedup=off ablation]
B3-v2    · 3B · seed=1 · corpus=ussd_plus_sms_deduplicated_v2 · r=8  · ctx=1024 · batch=2·acc=16 · epochs=3 · ~9h  [rank=8 ablation]
B4-v2    · 3B · seed=1 · corpus=ussd_plus_sms_deduplicated_v2 · r=32 · ctx=1024 · batch=2·acc=16 · epochs=3 · ~11h [rank=32 ablation]
B5-v2    · 3B · seed=1 · corpus=ussd_plus_sms_deduplicated_v2 · r=16 · ctx=512  · batch=4·acc=8  · epochs=3 · ~7h  [ctx=512 ablation]
B6-v2    · 3B · seed=1 · corpus=ussd_plus_sms_deduplicated_v2 · r=16 · ctx=2048 · batch=1·acc=32 · epochs=3 · ~15h [ctx=2048 ablation]
```

**Ordering constraint (window-fit):**
- Campaign A v2 runs in strict ladder order (0.5B → 1.5B → 3B → 7B) per Correction 3.
- Campaign B v2 runs in author-fastest-first order so early results flow: B1-v2 (5h · USSD-only ablation reads cleanly against B-REF-v2 first) → B5-v2 (7h) → B3-v2 (9h) → B-REF-v2 (10h · reference lands after B1/B3/B5 for early paired comparisons) → B4-v2 (11h) → B2-v2 (13h) → B6-v2 (15h · tail anchor). If window compresses, DROP from the tail (B6 → B2 → B4) never from the head, and NEVER touch corpus-consistency.

---

## §G · Wave-honest-limits banked

1. **Extraction + queue launch NOT executed in this session.** Governance leg (SMS-Body-Emit) + dispatcher fix + ratchet + campaign v2 manifest DESIGN are banked at 2978 double-green. Actual v2 corpus extraction (calls RDS Data API for ~200 K rows across two tables) + queue launch is chartered as the immediate operational continuation.
2. **A-3-v2 (7B) is the highest window risk.** If A-2-v2 measured wall-clock exceeds projection by more than 25 %, drop A-3-v2 from Campaign A entirely per Correction 3 trim-last rule. Under no circumstances trim corpus-consistency to fit A-3.
3. **B6-v2 (ctx=2048) is the Campaign B tail-risk.** Same trim-last logic: drop from the queue tail if B-REF-v2 through B4-v2 aggregate exceeds 55 h.
4. **v1 pilots stay banked untouched.** A-0-v1 (sealed) and B1-v1 (mid-training, will seal as pilot) remain as labelled pilot records — nothing deleted per owner ruling. Cross-boundary v1↔v2 comparisons are BANNED.
5. **Row-stream extraction not yet built.** If empirical probe finds row_executor binds below 100 K/table, W-Row-Stream-Extractor (chartered in SPRINT_PLAN) becomes the required next wave before any larger slice can be attempted.

---

*Authored 2026-09-06T~16:50Z during W-SMS-Body-Emit close, banking the Campaign v2 design + window-fill math + Correction 1/2/3 execution plan. Operational v2 launch is a one-shot continuation from the runbook §E.*
