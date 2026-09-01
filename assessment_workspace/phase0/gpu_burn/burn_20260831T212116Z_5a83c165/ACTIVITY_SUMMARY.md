# GPU 2h Dual-Host Burn — Activity Summary (owner-facing)

**RUN_ID:** `burn_20260831T212116Z_5a83c165`
**Authored (reconciliation):** 2026-09-01T02:50Z · main agent · **manually reconstructed** after the pod-side orchestrator process died mid-run. See §5 for the honest integrity finding.

---

## 1 · What happened

The owner authorized a longer GPU workload on 2026-08-31 at ~21:20 UTC verbatim: *"can you run a longer one like 2 hrs if not dependent on credits"*. The agent's answer, banked with the launch: credit-neutral (the workload runs on the owner's own EC2 GPU hosts — no platform credits burned; only agent babysitting time). Corpus preparation for the improved-training path (W-TxtTrain-v2) exceeded the owner's 30–40 min budget, so the agent picked the SIMPLE authorized fallback: **plain 2-hour dual-host governed matmul burn** across both hosts / all 4 H200s. Improved-training run banked as **W-TxtTrain-v2** — unblocked charter for a later slot.

## 2 · What actually ran

| Field | Value |
|---|---|
| Burn shape | governed fp16 matmul · 8192×8192 · continuous inner loop |
| Duration (planned) | 7200 s (2 h) |
| Duration (actual, per GPU) | **7200.01 s** — exact planned wall-clock (bit-precise) |
| Hosts | akki-vm · akki-vm-ii |
| GPUs | 4 × NVIDIA H200 (2/host · 143 771 MiB each) |
| Start | 2026-08-31T21:21:16Z (orchestrator launch) → per-host burn PIDs boot 21:21:45Z (akki-vm) / 21:21:31Z (akki-vm-ii) |
| End | 2026-08-31T23:21:46Z (akki-vm) / T23:21:32Z (akki-vm-ii) — both hosts landed `kind:"done"` events in their on-host burn.log |
| Torch / CUDA | torch 2.11.0+cu128 · CUDA 12.8 |

## 3 · Throughput & work

Per-GPU median throughput (from 239 30-second tick samples per GPU on each host, extracted from on-host `burn.log`):

| Host | GPU# | median tflops (fp16) | avg tflops (fp16) | iterations completed |
|---|---:|---:|---:|---:|
| akki-vm | 0 | **637.25** | 637.23 | 4,172,800 |
| akki-vm | 1 | **638.86** | 638.82 | 4,183,200 |
| akki-vm-ii | 0 | **643.44** | 643.30 | 4,212,544 |
| akki-vm-ii | 1 | **633.07** | 633.40 | 4,147,768 |
| **Fleet total** | 4 | **≈638 TFLOPS/GPU · 2.55 PFLOPS aggregate** | ≈638 avg | **16,716,312 iterations** |

Aggregate operations (2 × N³ per matmul with N=8192): **≈1.84 × 10¹⁹ fp16 ops = 18.4 exaFLOP** across the fleet over 2 hours.

## 4 · Power / temperature / cost

Sampled at 5-min polls (24 planned; **9 actually captured** — see §5 orchestrator integrity finding). From the last successful poll pair (2026-08-31T22:02Z, ~41 min into the run):

| Host | GPU# | util | mem | power draw | temp (°C) |
|---|---:|---:|---:|---:|---:|
| akki-vm | 0 | 100 % | 1 137 MiB | 694.22 W | 68 |
| akki-vm | 1 | 100 % | 1 137 MiB | 689.25 W | 68 |
| akki-vm-ii | 0 | 100 % | 1 137 MiB | 690.83 W | 66 |
| akki-vm-ii | 1 | 100 % | 1 137 MiB | 692.88 W | 74 |
| **Fleet** | 4 | 100 % | 4 548 MiB | **≈2 767 W** total (692 W/GPU avg) | 66–74 |

**Energy estimate (2h × 2 767 W):** ≈ **5.53 kWh**.

**Cost against estimate:**
- **Platform credits: $0.00.** Workload runs on the owner's EC2 GPU hosts, not on the pod's LLM key budget. Credit-neutral by design.
- Electricity delta on the owner's utility bill: 5.53 kWh × $0.10–0.15/kWh ≈ **$0.55 – $0.83** (or bundled inside the EC2 reserved-instance hourly rate; not itemized separately).
- Agent babysitting time: **< 5 min total** across two commit-boundary check-ins (launch confirm 21:21Z + post-close reconcile 02:50Z). Detached execution as the owner directed.

Cost against estimate: **within budget on both axes** (credit=$0 as promised; agent-time well under the 30–40 min budget for even the simple path).

## 5 · Integrity finding (honest, banked)

**The pod-side orchestrator (`gpu_burn_orchestrator.py`, PID 66598) died silently at ~22:02Z**, ~41 minutes into the planned 2-hour polling window. Root cause not fully diagnosed at reconcile time; probable causes: pod host restart at ~13:53 UTC (`uptime = 12:53` observed at reconcile), OOM, or an unhandled exception in the polling loop that took the process down without writing to `orchestrator.log` (last write is at 21:21:16Z boot line only — no crash traceback).

Consequences:
- **~78 min of poll receipts (poll windows 2477s → 7200s) were NOT captured.** Only 9 of the planned 24 polls made it to disk.
- **Post-run "after" nvidia-smi snapshots + activity summary + cost-ledger crossing receipt were NOT auto-generated.** This document manually reconstructs them.
- **Post-run cleanup of `/tmp/akki_burn_burn_20260831T212116Z_5a83c165/` on both hosts was NOT auto-fired.** Reconcile step cleaned both hosts explicitly with receipts `gpurcp-032dc817a07f` (akki-vm) and `gpurcp-d59e7f2aba7c` (akki-vm-ii).

**Crucially, the on-host burn payload itself completed cleanly** — each host was launched with `setsid nohup python3 burn.py --duration 7200 &`, so the on-host processes were detached from the orchestrator's control tree. The on-host `burn.log` on both hosts landed the full sequence `boot → start ×2 → 478 tick → 2 summary → done` events, with `wallclock_s = 7200.01` and `kind:"done"` sealing entry, proving both hosts ran the FULL 2-hour burn as requested. The workload the owner authorized executed successfully; only the pod-side observer failed.

**Lesson banked (charter W-Orchestrator-Resilience-r1 for follow-on):**
1. Orchestrator should tee to persistent per-tick log so a crash timestamp is visible.
2. Orchestrator should run inside supervisor rather than raw nohup, so it auto-restarts on death.
3. Orchestrator polling should be resumable from the last-persisted poll on restart (idempotent state).
4. `list-runs` API should expose "orphan runs" (an on-host burn without an orchestrator process attached) so future reconciles are one command away.

## 6 · Receipts

- **On-host burn.log tails (banked locally):**
  - `phase0/gpu_burn/burn_20260831T212116Z_5a83c165/akki_vm_burn_log_reconcile.txt`
  - `phase0/gpu_burn/burn_20260831T212116Z_5a83c165/akki_vm_ii_burn_log_reconcile.txt`
- **All poll receipts (9 captured):** `phase0/gpu_receipts/2026083120*_akki_vm*_nvidia_smi_poll_*s_gpurcp-*.log`
- **Cleanup receipts:** `gpurcp-032dc817a07f`, `gpurcp-d59e7f2aba7c`
- **Pre-launch probe (idle-confirmed + stale-log cleanup):** `gpurcp-e62acdf9370c` (akki-vm), `gpurcp-3a726aec9ecc` (akki-vm-ii), `gpurcp-9d564a2fb271`, `gpurcp-d0442119b876`
- **Post-orch-death reconcile probe:** `gpurcp-08f7c21023d5` (akki-vm), `gpurcp-9e85ee0ae951` (akki-vm-ii)
- **Launch manifest:** `phase0/gpu_burn_2h_launcher/20260831T212116Z/launch_manifest.txt`

## 7 · Plain-language summary (owner-facing)

The 2-hour burn ran to completion on all 4 H200s across both hosts. Fleet-wide it delivered about 638 TFLOPS/GPU sustained fp16, pushing 2.55 PFLOPS aggregate for the full 2 hours — roughly 18.4 exaFLOP of governed matmul work registered on the owner's estate. Total power draw was about 2.77 kW; energy about 5.5 kWh. No platform credits were consumed. Agent babysitting stayed under 5 minutes. The pod-side observer process died at 41 minutes in, so the second half's live polls and the auto-generated activity summary were lost — reconstructed here from the on-host `burn.log` files which the on-host processes wrote independently of the observer. Both hosts are now cleaned and idle. Registered activity is banked in full.
