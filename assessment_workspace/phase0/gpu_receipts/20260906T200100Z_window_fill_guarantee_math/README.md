# W-WINDOW-FILL-GUARANTEE · Math + Evidence

**Banked:** 2026-09-06T~20:01Z (bounded interject during owner Registry/Solva work order).

**Owner directive verbatim (via user proxy):**

> "Ensure the GPUs are fully consume next 3 days".

Standing obligation on the campaign window (through 2026-09-09T~19:40Z ≈ 72h from wave open). All four GPUs (2 hosts × 2 GPUs) held >85% busy through the window with ~10% margin, never idle lanes.

---

## §1 · Before (empirical, from SSH probe at wave open · 2026-09-06T19:40:53Z)

| Host | GPU | Util | Memory | Power | State |
|---|---|---|---|---|---|
| akki-vm | 0 | 12 % | 30.9 / 143.8 GB | 209.6 W | legacy A-0-v2 DDP still training · step 3425 · epoch 2.905 |
| akki-vm | 1 | **0 %** | 30.9 / 143.8 GB | 182.4 W | **legacy A-0-v2 DDP rank-1 exited · memory reservation held · 40 min idle already** |
| akki-vm-ii | 0 | 91 % | 105.4 / 143.8 GB | 606.9 W | v2.1 lane 0 B-REF-3B-v21 at step 900 |
| akki-vm-ii | 1 | 100 % | 105.4 / 143.8 GB | 654.6 W | v2.1 lane 1 B1-CORPUS-USSD-ONLY-v21 at step 900 |

Reconciliation: **akki-vm-ii already at spec (91/100%)**. **akki-vm is the problem** — 12/0% while waiting for A-0-v2 to seal.

---

## §2 · Root cause of the akki-vm idle window

A-0-v2 is a DDP-2GPU-tiny-batch run (`per_device=8 · grad_accum=4 · nproc=2 · EB=64`), started before W-COMPUTE-MAXIMIZE landed. At epoch 2.905 the training was in its final phase — rank-1 process exited before rank-0's held-out eval, leaving GPU 1's 31 GB memory reserved but unused. Two v2.1 lane dispatchers (PID 213708 + 213711) are alive and waiting per the never-kill-mid-flight rule, but cannot fire until A-0-v2's `ACTIVITY_SUMMARY.md` seal appears (the rank-1 memory reservation would OOM a fresh v2.1 lane anyway).

**Corrective action:** wait for A-0-v2 seal (~10 min from probe time based on ~20 steps/min trajectory). Owner directive: never kill mid-flight.

**Preventive action banked in this wave:** the v2.1 replacement of A-0-v2 (A-0-0p5B-v21-seed1 on the primary lane 0 queue) is a single-GPU big-batch run (`per_device=64 · grad_accum=1 · EB=64`), which cannot leak sibling-GPU reservations. Once the legacy A-0-v2 seals, the akki-vm idle window ends and both lanes fire at akki-vm-ii's utilization pattern.

---

## §3 · Queue-drain projections from measured v2.1 throughput

**Measured empirical step-rate** (from akki-vm-ii lane 0/1 first 51 min of B-REF-3B-v21 / B1-USSD-ONLY-v21):

- 3B single-GPU big-batch (per_device=16 · grad_accum=4 · EB=64 · seq=1024): ~17.6 steps/min. At 3 epochs × ~963 steps = 2 889 total → **~2.7 h per 3B run**.

**Extrapolated step-rate by rung** (bf16 LoRA-only, scaling by parameter count, single-GPU H200):

| Rung | Config (per_device × accum = EB=64) | Est. time per run |
|---|---|---|
| 0.5B | 64 × 1 | ~1.5 h |
| 1.5B | 32 × 2 | ~3 h |
| 3B | 16 × 4 | ~2.7 h (**measured**) |
| 7B | 8 × 8 | ~6.3 h (scaling) |
| 14B | 4 × 16 | ~12.6 h (scaling; probe first) |

### §3.1 · Primary queue drain (from 2026-09-06T~20:00Z)

| Lane | Primary queue (runs) | Drain estimate | Combined h into window |
|---|---|---|---|
| akki-vm L0 (GPU 0) | A-0-0p5B-s1, A-2-3B-s1, A-3-7B-s1 (3 runs) | ~10.5 h | ~10.5 h |
| akki-vm L1 (GPU 1) | A-1-1p5B-s1, A-0-0p5B-s2, A-1-1p5B-s2, A-2-3B-s2 (4 runs) | ~10.2 h | ~10.2 h |
| akki-vm-ii L0 (GPU 0) | B-REF-3B-s1 (running, ~2h left), B3-RANK-8-s1, B5-CTX-512-s1, B-REF-3B-s2 (4 runs) | ~9 h | ~9 h |
| akki-vm-ii L1 (GPU 1) | B1-USSD-s1 (running, ~2h left), B2-DEDUP-OFF-s1, B4-RANK-32-s1, B6-CTX-2048-s1 (4 runs) | ~11 h | ~11 h |

**Idle gap without extension: ~60 h per lane through window end.** Extension mandatory.

### §3.2 · Ext1 queue drain (chained via queue_followon_launcher.py · queued 2026-09-06T~20:00Z)

| Lane | Ext1 runs (owner priority) | Drain estimate | Combined into window |
|---|---|---|---|
| akki-vm L0 | A-3-7B-s2 (b) · A-14B-s1-PROBE (c) · A-3-7B-s3 (d) · A-2-3B-s3 (d) · A-1-1p5B-s3 (d) | ~46 h | **~56.5 h** |
| akki-vm L1 | A-14B-s2 (c) · A-3-7B-s4 (d) · A-14B-s3 (d) · A-2-3B-s4 (d) · A-1-1p5B-s4 (d) · A-0-0p5B-s3 (d) | ~48 h | **~58 h** |
| akki-vm-ii L0 | B3-RANK-8-s2 (a) · B5-CTX-512-s2 (a) · B-REF-7B-s1 (b) · B-REF-14B-s1-PROBE (c) · B-REF-3B-s3 (d) · B-REF-7B-s2 (b) · B3-RANK-8-s3 (d) · B5-CTX-512-s3 (d) | ~37 h | **~46 h** |
| akki-vm-ii L1 | B1-USSD-s2 (a) · B2-DEDUP-OFF-s2 (a) · B4-RANK-32-s2 (a) · B6-CTX-2048-s2 (a) · B-REF-14B-s2 (c) · B-REF-7B-s3 (d) · B-REF-3B-s4 (d) · B-REF-3B-s5 (d) | ~43 h | **~54 h** |

**Ext1 drain (worst lane) ends at ~46 h.** Remaining window ~26 h. If we want a full 72 h without idle, an ext2 wave must be banked before ~T+40 h.

### §3.3 · Ext2 sketch (banked as follow-on plan, not yet written)

Ext2 will fill the tail 25 h/lane with owner priorities (d) + (e):
- Third seeds for remaining ablation dims (B1-s3, B2-s3, B4-s3, B6-s3 · A-3-s5, A-2-s5, A-1-s5, A-0-s4).
- W-Sequence-Packing lift IFF the packing collator lands (chartered as its own wave; if it lands, ~40 % throughput uplift on the USSD corpus, so ~15 h of packed 3B runs replace ~10 h wallclock).
- A-14B and B-REF-14B additional seeds (if PROBE seeds succeed at bf16 fit).

Ext2 authoring window: T+30 h (ext1 mid-drain, ~2026-09-08T02:00Z) so it's ready before ext1 completes.

---

## §4 · Chained-dispatch mechanism (deployed 2026-09-06T20:00Z)

### §4.1 · Post-fix dispatcher (track-a `HEAD post-3f7bb0f`)

- New `--follow-on-queue-file` CLI arg. On queue drain, launches new dispatcher subprocess (`python3 __file__ --queue-file <follow-on> --gpu-id <same> ...`) via `subprocess.Popen(start_new_session=True)` so the follow-on outlives the current dispatcher.
- New `QUEUE_DRAINED_lane<gpu_id>.json` marker written after `queue_completed.md` and before the `completed` heartbeat. Marker carries: kind, at_utc, gpu_id, campaign_id, total_runs, dispatcher_pid, queue_file, follow_on_queue_file.
- Ordering test-frozen: `queue_completed.md` → `QUEUE_DRAINED_lane*` → `completed` heartbeat.
- Deployed to both hosts at `/home/ubuntu/akki_journal/on_host_queue_dispatcher.py`.

### §4.2 · queue_followon_launcher.py (host-side watchdog)

- Bridges the pre-fix→post-fix gap. The four v2.1 dispatchers running at wave-open time were launched with pre-fix code (no `--follow-on-queue-file` arg). Launcher polls the primary queue's LAST run's `ACTIVITY_SUMMARY.md` (which cannot be confused with the sibling lane's seal on a same-campaign-id host, unlike shared `queue_completed.md`). On seal appearance, launcher fires a NEW dispatcher (post-fix code) with the ext1 manifest, armed with `--follow-on-queue-file <ext2>` if ext2 is banked. Idempotent via `ext1_launched_lane<gpu_id>.marker` sentinel. Refuses launch if ext1 manifest declares a mismatched gpu_id (safety guard).
- Deployed and running under nohup on both hosts:
  - akki-vm PID **229 182** · daemon mode · poll 60 s
  - akki-vm-ii PID **195 771** · daemon mode · poll 60 s

### §4.3 · Not implemented (deferred rationale)

**Fallback GPU-burn on idle lane** — owner said "if trivial". Trivial-cost analysis: a burn on the idle lane has ~5-10 GB working set (small enough to coexist) but races with the next dispatched trainer's memory allocation and can trigger PyTorch's caching allocator to hold onto pages, biasing the next run's throughput. The safer honest filler is chained real training (ext1 + ext2), which is what this wave delivers. If the ext1 chain fails for any reason, a burn is trivial to launch manually. Banked here as owner-intent-aligned.

---

## §5 · Ratchet + discipline

- Wave ratchet: **2986 → 2991** (+5), double-green byte-match on receipts `phase0/drill_receipts/20260906T*_wave_window_fill_guarantee_close_run{1,2}.log`.
- Invariants added:
  - `test_dispatcher_writes_queue_drained_marker_on_completion` — marker file exists, ordered before completed heartbeat.
  - `test_dispatcher_queue_drained_marker_carries_required_fields` — payload has kind/at_utc/gpu_id/campaign_id/total_runs/dispatcher_pid.
  - `test_dispatcher_accepts_follow_on_queue_file_arg` — argparse.
  - `test_dispatcher_launches_follow_on_when_armed_after_drain` — subprocess.Popen with --gpu-id preserved.
  - `test_dispatcher_follow_on_is_optional` — conditional guard.
- Two-commit pattern: dispatcher.py + tests → Extraction-Akki `programme/track-a`; STATE, launcher, manifests, receipts → workspace `master`.
- No push either side.
- All EB=64 comparability preserved across 21 extension runs (validated by existing `test_v21_effective_batch_math_holds` + `test_v21_comparability_anchor_preserved`).

---

## §6 · Verification path

- SSH check-2 (audit-completion): scheduled for the FIRST QUEUE_DRAINED marker or ext1 launch, whichever fires first. Owner directive banked at "TWO SSH checks per audit" and this bounded interject is inside that budget.
- Reconciliation script (to be authored if ext1 ever misses launch): reads all four `QUEUE_DRAINED_lane*.json` markers + `ext1_launched_lane*.marker` sentinels + `dispatch_error_*.json` records to compute per-lane idle-minute total across the 72 h window. Idle-minute total is the honest metric — >85 % target = <10.8 h total idle across 4 lanes × 72 h = 288 h possible.

---

**Discipline note:** this wave is a bounded interject on the Registry/Solva work order. On return, the STEP-1 new-HTML ingest continues from where it paused (decoded_v{2,8}.text was extracted; nav-label diff not yet run).
