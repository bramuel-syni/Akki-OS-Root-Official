READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M7 · W-M7-UTILIZATION-72H · Launch Recovery Note · 2026-09-16T~03:41Z

**Context.** The 72h GPU utilization job was launched last shift at 2026-09-16T03:30:31Z (akki-vm) and 2026-09-16T03:30:35Z (akki-vm-ii) per the owner ruling 2026-09-16T~03:08Z. Boot-ritual reconciliation this shift surfaced a partial-launch failure: samplers were running and writing telemetry, but the bench workload never fired on either host.

## Diagnosis (from-disk evidence · session 2026-09-16T~03:37Z)

Probe via `python3 tools/m7_util_72h_orchestrator.py status_only` returned:

- **Sampler PIDs (`sampler_status.json`) live · sampler PID files EMPTY** — the JSON status carried `pid:297868` (akki-vm) / `pid:271760` (akki-vm-ii), but `sampler_pid.txt` was reported "No such file or directory" and the `===pids===` block was blank.
- **Bench workload absent everywhere** — `workload_status.json` empty; `workload.log` did not exist; `ps -ef | grep bench_workload` returned zero matches on both hosts.
- **GPUs idle** — `nvidia-smi` returned 0% utilization, 0 MiB memory used, ~76-80W power (idle baseline).
- **Root cause visible in `ps -ef`:** the inner launch script recorded on the remote showed `echo  > sampler_pid.txt; ... echo  > workload_pid.txt;` — the `$!` had been consumed by the outer bash's parameter expansion before `bash -c` received the inner body.

The prior orchestrator wrapped the inner script via `json.dumps(inner)`, which produces a double-quoted shell string. Bash's outer `"..."` context expands `$!` at parse time; because nothing was backgrounded in the outer shell yet, `$!` expanded to the empty string. The two `echo > *.pid` calls therefore wrote empty files, and the launcher's dependency on those files (implicit — nothing else referenced them, but the missing content was a load-bearing symptom that the wrapping was structurally broken) proved the wrapping needed a redesign.

The bench workload's absence was a downstream failure: with the inner script's `$!` expansion broken, the launcher's timing/quoting was drift-prone; the outer paramiko channel closed before the second background (`python3 bench_workload.py`) settled, so it never took hold.

## Fix (this shift)

`tools/m7_util_72h_orchestrator.py :: launch_detached` refactored to stage the inner script to disk on the host as `~/akki_util_72h/launcher.sh` via base64 decode, then invoke `setsid nohup bash launcher.sh </dev/null >/dev/null 2>&1 & disown`. Now `$!` evaluates inside the `launcher.sh` process where sampler.sh and bench_workload.py are the actual last-backgrounded PIDs.

The fix is scoped to `launch_detached` only. `stage_payloads`, `probe_state`, `sync_jsonl`, `_rollup_host`, `regenerate_report`, and all three CLI modes are unchanged.

## Recovery (this shift)

1. Killed the three stale sampler.sh PIDs across both hosts (`kill -TERM`, then `kill -9` for the residual PID 297639 on akki-vm). Zero live processes remained matching `sampler|bench_workload`.
2. Re-ran `build_and_launch` mode. `stage_payloads` re-copied both `bench_workload.py` and `sampler.sh`. `launch_detached` fired the fixed path.
3. Post-launch verification:
   - akki-vm: `sampler_pid.txt=299351` (7 bytes), `workload_pid.txt=299352` (7 bytes), both PIDs `sampler_alive`+`workload_alive`.
   - akki-vm-ii: `sampler_pid.txt=272895` (7 bytes), `workload_pid.txt=272896` (7 bytes), both PIDs `sampler_alive`+`workload_alive`.
   - `workload_status.json` populated on both hosts with `"state":"running"` payload.
4. First bench iterations landed at ~03:41:30Z (akki-vm) / ~03:41:38Z (akki-vm-ii):
   - matmul bf16 8192 × batch 1: **~650 TFLOPS** sustained on each GPU, p50 latency ~1.66 ms, p99 ~1.73 ms.
5. `nvidia-smi` direct probe at 03:43:25Z confirmed **97-98% utilization** on both GPUs (akki-vm), ~689-691W power draw, ~1495 MiB memory used.
6. `check_in` run at 03:44:44Z synced telemetry.jsonl + workload.jsonl. Rollup: 4 bench iterations banked on each host, all `ok=true`.

## Job state at recovery close (2026-09-16T03:44:44Z)

- **Earliest launch:** 2026-09-16T03:41:28Z (akki-vm sampler).
- **Elapsed at recovery close:** 0.05 hours.
- **Remaining:** 71.95 hours of 72.
- **Report served:** `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md` — HTTP 200, 2362 bytes at recovery close.
- **Sampler cadence:** 5 min (nvidia-smi query per GPU per host).
- **Workload cadence:** 60 s per bench configuration; rotating matrix of matmul (bf16/fp16/fp32-tf32 × 8192/12288/16384) + attention (bf16 × 2k/4k/8k seq × batch 1/4). Every completed iteration = one banked JSONL row.
- **Discipline held:** in-perimeter (torch.randn on-device only) · env-injection creds only (§E) · shape-only receipts · position-redaction · SEC probe-halt reading amended per owner ruling.

## Ratchet impact

None. This is a state-repo tool fix + recovery. No code-repo change. Ratchet floor remains **4358** (unchanged since CP-M6-9-2 close).

## Owner-facing summary

The 72h GPU utilization job is now genuinely LIVE with real bench iterations flowing. Prior state (03:30:31Z launch) had samplers-only-no-workload due to a launcher `$!` escape bug, now fixed. Recovery launched cleanly at 03:41:28Z. Report URL: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

Next actions per owner sequence (verbatim DECISIONS 2026-09-16T~03:08Z step 4):
1. Author M7-open milestone-boundary note + W0 (platform integrity) grounding brief.
2. Walk W0 autonomously under standing guardrails.
3. Interleave GPU utilization check-ins at every CP boundary of the M7 walk.
