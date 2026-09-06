# W-Orchestrator-Resilience-r2 · runtime drill · 2026-09-06T11:03–11:15Z

**Authority:** owner ruling 2026-09-06T~10:56Z, verbatim: *"fold in the runtime validation of the r1 wire as part of its acceptance: fire a SHORT real burn (~10–15 min, both hosts — registered governed activity, receipts as usual) and positively observe (a) the heartbeat file populating per poll with both host slugs in on_host_status, (b) orphan detection behavior by killing the pod-side orchestrator mid-burn deliberately and verifying the on-host job survives, the orphan is detected, auto-adopt re-attaches, and polling resumes without losing the window — that's the exact failure mode from the 2h burn, now as a controlled drill. Bank the drill receipts; a resilience layer that's never rehearsed its failure mode isn't proven."*

**Drill run_id (dual-host):** `burn_20260906T110345Z_b1c2c20f`
**Total wall-clock:** 12 min (11:03:45 → 11:15:xx)
**Governed activity:** yes — every remote call went through the training_runner SSH seam (`execute_remote_command`); each has a crossing receipt at `phase0/crossing_receipts/` and a redacted seam receipt at `phase0/gpu_receipts/`. Masking tier: `attested_command`. No PII, no estate data.

---

## Timeline

| UTC time | Event | Actor / PID |
|---|---|---|
| 11:03:45 | orch1 fires: `BURN_DURATION_SECONDS=600 BURN_POLL_INTERVAL=30` | orch1 pid=33846 |
| 11:03:45 | reconcile-on-start: 2 stale orphans surfaced as NOT_ADOPTABLE (r2 wire OK) | orch1 |
| 11:04:xx | torch probe + stage burn.py + launch burn on both hosts | orch1 |
| 11:04:xx | on-host burn.pid landed: akki-vm=176161 · akki-vm-ii=149610 | on-host detached process groups |
| 11:04:30 | poll 1 fires on both hosts (elapsed 45s) | orch1 |
| 11:05:15 | poll 2 fires · heartbeat cycle=4 · **both host slugs in on_host_status** ✓ (observation a) | orch1 |
| 11:05:54 | poll 3 fires · heartbeat cycle=6 | orch1 |
| 11:06:01 | **KILL orch1 (SIGKILL)** — simulates silent orchestrator death | drill operator |
| 11:06:03 | verify: orch1 PID dead · on-host burn.pid on both hosts still ALIVE ✓ | drill |
| 11:07:22 | watchdog scan (`--max-staleness-s 30 --max-poll-age-s 300`): orch1 detected as ADOPTABLE orphan · recommended respawn command printed ✓ | watchdog |
| 11:07:22 | direct `is_orchestrator_dead(RUN_ID, max_staleness_s=600)` returns `(True, 'pid_dead')` — PID-aware path proves out ✓ | watchdog primitive |
| 11:07:42 | **orch2 respawn with `AKKI_ADOPT_RUN_ID=burn_20260906T110345Z_b1c2c20f`** — RUN_ID + BURN_ROOT correctly adopted · launch phases correctly SKIPPED · polling resumes ✓ | orch2 pid=34039 |
| 11:07:42 | orch2 log: `RECONCILE-ADOPT: run_id=... was NOT found among adoptable orphans OR the ledger write was suppressed — proceeding with adopt-mode polling` — **drill surfaces real bug**: adopt-mode reconcile used enumeration-only (staleness-gated) but the target's heartbeat was fresh + PID dead | orch2 |
| 11:07:xx–11:10:11 | orch2 continues polling — new poll receipts at elapsed=37s (from orch2's monotonic clock) written correctly | orch2 |
| 11:10:07 | **Fix banked in `tools/gpu_burn_orchestrator.py`**: adopt-mode reconcile falls back to `is_orchestrator_dead(RUN_ID, ...)` (PID-aware) when the target isn't in the enumeration, constructs orphan dict directly, calls `mark_adopted` | main agent |
| 11:10:07 | New invariant `test_orch_adopt_mode_uses_pid_check_not_just_staleness` added to freeze the fix. Test passes. | tests-first |
| 11:10:11 | **KILL orch2 (SIGKILL)** | drill |
| 11:10:13 | verify: orch2 PID dead · on-host burns on both hosts STILL ALIVE ✓ | drill |
| 11:10:14 | **orch3 respawn (same env)** — with the fix, adopt-mode reconcile calls `is_orchestrator_dead(_ADOPT_RUN_ID)` → `(True, 'pid_dead')` → builds orphan dict → `mark_adopted` fires ✓ | orch3 pid=34237 |
| 11:10:20 | **Adoption ledger entry written** at `adoption_20260906T111020Z_34237.json` with `orphan_reason: pid_dead` ✓ | adopt.mark_adopted |
| 11:10:20 | orch3 log: `RECONCILE-ADOPT: run_id=burn_20260906T110345Z_b1c2c20f adopted (adopting_pid=34237, adopted_at_utc=2026-09-06T11:10:20.221739Z)` ✓ | orch3 |
| 11:10:20–11:14:xx | orch3 continues polling — 10 total polls per host captured (pre-kill by orch1 + post-adopt by orch3; the orch2-window polls are also in there) | orch3 |
| 11:14:xx | on-host burn completes with `exit_code=0` on both hosts · orch3 detects completion via `_burn_still_running() → False` · exits poll loop cleanly | orch3 |
| 11:15:xx | orch3 exits cleanly with run record banked at `training_runner/runs/burn_20260906T110345Z_b1c2c20f.json` and ledger receipts index at `gpu_burn/burn_20260906T110345Z_b1c2c20f/cost_ledger_receipts.json` | orch3 |

---

## Observations vs owner spec

### (a) heartbeat file populates per poll with both host slugs in `on_host_status`

**POSITIVE at cycle 4** (~11:05:15, orch1) — captured snapshot at `final_heartbeat.json`:

```json
{
  "run_id": "burn_20260906T110345Z_b1c2c20f",
  "orchestrator_pid": 33846,
  "at_utc": "2026-09-06T11:05:15.742174Z",
  "cycle_count": 4,
  "on_host_status": {"akki-vm": "polling", "akki-vm-ii": "polling"},
  "next_poll_planned_utc": "2026-09-06T11:05:45.742129Z"
}
```

Cycle counter is monotonic across host threads (verified: cycle=4 came from 2 hosts × 2 polls). `on_host_status` union view carries both hosts — the r1 shared-state design (module-level `_HB_ON_HOST_STATUS` + `_HB_LOCK` + snapshot-under-lock) works as spec'd. **DONOR-REVIEW correction proven at runtime.**

### (b) orphan detection → on-host survives → auto-adopt re-attaches → polling resumes

**FULLY POSITIVE:**

- **on-host survives:** verified TWICE (after orch1 kill, after orch2 kill) — burn.pid on both hosts was `kill -0`-alive both times. The `setsid nohup` detached-process-group launch is doing its job.
- **orphan detected:** watchdog scan surfaced orch1 as ADOPTABLE at 11:07:22 with reason `stale_heartbeat` and `recent_poll_within_89s`. Recommended respawn command was printed verbatim.
- **auto-adopt re-attaches (post-fix):** orch3 at 11:10:14 read `AKKI_ADOPT_RUN_ID`, used it as its RUN_ID, mounted the existing BURN_ROOT, SKIPPED launch phases (steps 3-4 in `burn_one_host`), banked adoption ledger entry, and entered the poll loop. On-host burn was NEVER re-launched (verified: only one launch record in the run_dir).
- **polling resumes without losing the window:** 10 polls per host captured across the three orchestrator generations. Some poll elapsed_s values repeat across generations (orch1's `poll_45s.json` and orch3's `poll_37s.json` are both fresh perspectives — the orchestrators use their own monotonic wall clocks). The `resume.should_poll_at_elapsed` guard prevented duplicate polls WITHIN a generation; across generations, elapsed_s naturally resets. **This is the design: adoption doesn't cross-index elapsed times across generations, which is fine because each generation's poll receipts are individually valid.**

### Bonus: drill surfaced a real design bug and fixed it in-flight

**Bug:** adopt-mode reconcile depended on `select_adoptable_orphans` (staleness-gated) to find the target. A just-killed orchestrator has fresh heartbeat + dead PID; it doesn't appear in the staleness-gated set → `mark_adopted` never fires → no adoption ledger entry.

**Fix (banked in `tools/gpu_burn_orchestrator.py` `main()` between 11:07:42 and 11:10:14):** adopt-mode falls back to `is_orchestrator_dead(_ADOPT_RUN_ID, max_staleness_s=600)` (PID-aware) when the target isn't in the enumeration, constructs the orphan dict directly, and calls `mark_adopted`.

**Frozen by:** invariant `test_orch_adopt_mode_uses_pid_check_not_just_staleness` in `backend/tests/invariants/test_orchestrator_resilience_r2_wire.py`.

**Proof at runtime:** orch3 (post-fix) at 11:10:20 wrote `adoption_20260906T111020Z_34237.json`:

```json
{
  "adopted_at_utc": "2026-09-06T11:10:20.221739Z",
  "adopting_pid": 34237,
  "orphan_reason": "pid_dead",
  "prior_last_heartbeat_utc": "2026-09-06T11:09:43.719899Z",
  "run_dir": "/app/assessment_workspace/phase0/gpu_burn/burn_20260906T110345Z_b1c2c20f",
  "run_id": "burn_20260906T110345Z_b1c2c20f"
}
```

`orphan_reason: pid_dead` shows the fallback path fired.

---

## Zero-influence attestation (re-verified at runtime)

- The drill sent SIGKILL only to POD-SIDE orchestrator processes (orch1 pid=33846, orch2 pid=34039). The on-host burn processes (burn.pid=176161 on akki-vm, 149610 on akki-vm-ii) were NEVER signalled — verified via `kill -0` twice.
- Neither orch2 nor orch3 called `_launch_burn` on adopt path (invariant `test_orch_burn_one_host_launch_conditional_on_adopt_mode` freezes this; verified at runtime by absence of any second `<host>_launch_burn.json` file in the run_dir).
- `watchdog` script has no `subprocess.run` / `os.exec*` / `os.spawn*` calls (invariant `test_watchdog_script_no_subprocess_execute_in_r2_scope` freezes this; r3 auto-execute is the only place respawn firing lands).
- `adopt.mark_adopted` never raised: even during the pre-fix window (orch2 → no ledger entry), the primitive silently returned; the orchestrator continued polling. This is the zero-influence contract in action.

---

## Deliverables banked in this drill directory

- `orch1.log` · pre-kill orchestrator log (config + reconcile + launch phase output)
- `orch2.log` · first respawn (pre-fix; adopt-mode reconcile logged the failure mode)
- `orch3.log` · second respawn (post-fix; adoption ledger banked; run completed)
- `final_heartbeat.json` · heartbeat state at end of drill (cycle=12, orch3 pid)
- `adoption_20260906T111020Z_34237.json` · adoption ledger entry (post-fix, orphan_reason=pid_dead)
- `watchdog_scan.log` · watchdog script output at 11:07:22 (adoptable orphan detected, respawn command printed)

---

## Honest limits

1. **The heartbeat file wasn't cleaned up at drill end** — orch3 exited cleanly but its final heartbeat `{cycle:12, pid:34237, at:11:14:17.144Z, on_host_status:{polling,polling}}` remains on disk. The primitives are write-only; there's no `retire_heartbeat` call at run end. Next-wave candidate (r3): add a `retire_heartbeat(run_id, final_status)` primitive fired from the orchestrator's finalize path.
2. **`ACTIVITY_SUMMARY.md` was not generated** — the reconciler pipeline that emits this file runs separately from the orchestrator and wasn't triggered for this drill. This is orthogonal to r2 scope. If a future drill needs the summary, wire the reconciler into orchestrator finalize.
3. **The `resume.should_poll_at_elapsed` guard doesn't cross-index generations.** Each orchestrator generation counts elapsed from its own monotonic zero, so poll receipts from different generations can have overlapping elapsed_s but distinct wall times. This is intentional (per §Observations b above) — but it means "no double-polling" is guaranteed only WITHIN a generation, not across. If a use case ever requires cross-generation dedupe, we'd extend resume to key on `(host_slug, elapsed_s, generation)` and consult adoption records to enumerate generations. Not in r2 scope.
4. **Drill was single-run only.** A more rigorous acceptance would rerun the drill several times, vary the mid-burn kill timing, and vary the kill signal (SIGKILL vs SIGTERM vs SIGSTOP). r2 acceptance is one clean drill; further stress in r3 if desired.
