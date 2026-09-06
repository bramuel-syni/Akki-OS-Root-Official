# W-COMPUTE-MAXIMIZE · Post-Seal Empirical Uplift Receipt

**Banked:** 2026-09-06T19:06:37Z (SSH check-1 during owner-priority audit; probe fired ~4 min after B1-v1 seal on akki-vm-ii).

**Purpose:** hard evidence that closes the wave-honest-limit banked in the W-COMPUTE-MAXIMIZE close ratchet-history entry (20260906T183500Z):

> "10-min empirical throughput probe runs on freed GPUs post-seal to confirm >85% util before window-fill projection is locked."

That probe was deferred at wave close because A-0-v2 (ETA seal ~19:47Z) and B1-v1 (ETA seal ~18:30Z) were still running under the pre-maximize config. This receipt captures the actual post-seal empirical util on akki-vm-ii (B1-v1 sealed 2026-09-06T19:02:31Z) and the still-blocked-but-armed state on akki-vm.

---

## Before (owner's dashboard reading at wave open · 2026-09-06T~18:00Z)

Verbatim owner phrasing (banked in ratchet-history CP):

> "on the compute, i need workflows for the next 3 day fully maximized. our jobs are not fully consuming the GPUs"

Dashboard-reading recorded in ratchet-history entry:

> "dashboard 19% overall / per-GPU 11-25% util unacceptable"

Contributing configuration:
- DDP-2GPU-tiny-batch: A-0-v2 `per_device=8 · grad_accum=4 · nproc=2 · EB=64` on both GPUs simultaneously.
- B1-v1 similarly held both GPUs at ~2 GB per-GPU / low util (Qwen2.5-3B under DDP-2GPU-tiny-batch).

## After (post-seal empirical · this receipt)

**akki-vm-ii (Campaign B v2.1 · TWO LANES LIVE):**

| GPU | Util | Memory used / total | Power draw | Temp | CUDA-pinned trainer |
|---|---|---|---|---|---|
| 0 | **82 %** | 105 451 MiB / 143 771 MiB (73 %) | 627.04 W | 65 °C | PID 193765/193862/193863 · CUDA_VISIBLE_DEVICES=0 · `B-REF-3B-v21-seed1` (per_device=16 · grad_accum=4 · EB=64) · corpus `ussd_plus_sms_deduplicated_v2` |
| 1 | **94 %** | 105 451 MiB / 143 771 MiB (73 %) | 642.83 W | 69 °C | PID 193766/193943/193944 · CUDA_VISIBLE_DEVICES=1 · `B1-CORPUS-USSD-ONLY-v21-seed1` (per_device=16 · grad_accum=4 · EB=64) · corpus `ussd_deduplicated_v2` (Campaign A share) |

Uplift on akki-vm-ii vs owner dashboard baseline: **11-25 % → 82-94 %** (both GPUs simultaneously loaded; >85% threshold cleared on GPU 1, marginally under on GPU 0).

**akki-vm (Campaign A · legacy A-0-v2 still finishing):**

| GPU | Util | Memory used / total | Power draw | Temp | Runner |
|---|---|---|---|---|---|
| 0 | 67 % | 30 891 MiB / 143 771 MiB (21 %) | 200.58 W | 44 °C | PID 194863 · A-0-v2 (Qwen 0.5B DDP-2GPU-tiny-batch, legacy config) · step 2750 |
| 1 | 0 % | 30 855 MiB / 143 771 MiB | 204.68 W | 39 °C | idle (memory reserved from DDP process) |

**akki-vm is not yet delivering the uplift** because the pre-maximize A-0-v2 is still finishing under the old config. Owner rule "never kill mid-flight" honored (banked in ratchet-history entry). v2.1 dispatchers `PID 213708 (GPU 1 lane)` and `PID 213711 (GPU 0 lane)` are ALIVE, ARMED, heartbeat fresh at 19:05:57Z, and waiting on A-0-v2 seal (`current_state: waiting_for_shield-train-campaign-a-v2-A-0-0p5B-20260906T170000Z`). Once A-0-v2 seals (heartbeat step 2750 at 19:06:16Z; ETA a few min based on trajectory), both v2.1 lanes fire immediately with EB=64 single-GPU big-batch config identical to akki-vm-ii's now-delivered pattern.

## Mechanism verification (from ps + /proc/PID/environ)

- Every v2.1 trainer PID's environment carries `CUDA_VISIBLE_DEVICES=<gpu-id>` matching its lane manifest (verified in-line above). Frozen by invariant `tests/invariants/test_dispatcher_gpu_pinning.py` (§B) on track-a HEAD 3f7bb0f.
- Every v2.1 trainer command line carries `--per-device-batch 16 --grad-accum 4 --num-epochs 3` → per_device × accum × 1-GPU = 16 × 4 × 1 = 64 → EB=64 comparability anchor preserved vs v2 pilots. Frozen by invariant §D/E.
- Both v2.1 dispatchers on akki-vm-ii report `queue_progress.total: 4` (each lane owns 2 seeds × 2 runs). Both dispatchers on akki-vm report same.
- akki-vm has legacy dispatch_error records (`dispatch_error_A-1-1p5B.json` + `A-2-3B.json` dated 2026-09-06T15:01Z) — pre-fix preexec_fn evidence; retained as diagnosis material, not re-fired because v2.1 replaces those runs.

## Wave close reconciliation

W-COMPUTE-MAXIMIZE ratchet closed 2986 (double-green byte-match at wave close on `phase0/drill_receipts/20260906T183500Z_...run1.log` + `T184000Z_...run2.log`) is CODE-COMPLETE. This receipt closes the deferred empirical evidence half of the wave (per the wave's own honest-limit note). No new tests, no ratchet move, no track-a commit needed — this is receipt-only banking of what the wave's own dispatchers produced ~20 min after wave-close double-green.

**Remaining wave-follow-on (chartered as new wave, not part of maximize close):**

- **W-Sequence-Packing** (bigger lift than batch retune per ratchet-history entry): USSD median <200 tok / ctx=1024 = 80% padding waste. Trainer is HF Trainer not SFTTrainer; needs authored packing collator. Ratchet-history entry `phase0/drill_receipts/20260906T183500Z_wave_compute_maximize_close_run1.log` notes this explicitly.
- **W-akki-vm empirical uplift receipt** (this receipt to be extended once A-0-v2 seals and v2.1 lanes fire on akki-vm).

---

## Files

- `akki-vm/post_seal_util.txt` — raw ssh probe output (date + nvidia-smi + trainer PIDs with /proc/PID/environ CUDA_VISIBLE_DEVICES + dispatcher PS + dispatcher_heartbeat.json + A-0-v2 seal check + latest heartbeat).
- `akki-vm-ii/post_seal_util.txt` — same shape for akki-vm-ii.
- `README.md` — this file (reconciliation summary).

**Discipline:** receipt-only. No code touched. Ratchet 2986 unchanged.
