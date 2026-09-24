READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M8 catch-all lane · from-disk findings · 2026-09-16T~07:20Z

**Authority:** Owner directive 2026-09-16T~07:15Z verbatim:

> "1. Quarantine-restoration pilot (M8 catch-all, banked long ago): the 165-quarantined D1a-1 legacy tests (per waveD close: 19 files / 88-89 tests). Run the banked pilot: pick 3–5 quarantined files, attempt restoration under current pytest-asyncio (fix async fixture teardown leaks where the fix is test-side only — NO mechanism refactor), measure: restored-green vs still-leaking. If the pilot restores cleanly, continue file-by-file with ratchet bumps per batch. If the leaks require mechanism changes, HALT that lane and bank the finding — no refactor.
> 2. W-TaskEval-v1 and the remaining small M8 watchdog/consistency items — for each: check from-disk whether it already exists (POST-2 lesson), verify-or-build accordingly, case-agnostic, tests-first.
> 3. If both lanes exhaust or block: produce the M8 status rollup (same shape as the M7 rollup) and hold with utilization interleave only.
> Standing: utilization check-ins every boundary to 72h completion · probes NOTE-SKIPPED pending JUMP rotation · all P1/P2 owner items parked and carried · all permanent guardrails. Report at quarantine-pilot outcome (it's the most informative next signal) with utilization snapshot."

**Method.** Applied POST-2 discipline (from-disk read is authoritative · absence is a finding) across both lanes.

---

## §1 · LANE 1 · Quarantine-restoration pilot

### From-disk read

- `baseline_failures.json` `counts_at_baseline.quarantined_d1a1 = 0` (zero quarantined D1a-1 tests remain).
- `baseline_failures.json` `quarantined_d1a1_files = []` (zero chartered files remain quarantined).
- `baseline_failures.json` `invariants_enforced_when_baseline_guard_1.quarantined_d1a1_files_exclusive = []` (zero full-skip files remain).
- `baseline_failures.json` `invariants_enforced_when_baseline_guard_1.quarantined_d1a1_max = 0` (ceiling is zero).
- `quarantine_reason_source` (verbatim): *"D1a-1 residue class RETIRED at Wave F Scope A (2026-08-27T~20:20Z) via Path 2 robust walker fix (removed sys.modules prefix filter that missed `backend.tests.*` module names arising from backend/__init__.py) + coupled requirements.txt reality-catches-up bumps (pytest 8.3.3→8.4.2, pytest-asyncio 1.2.0→1.4.0) + Rider-1 pin-vs-installed invariant guard. All 21 chartered files (19 partial-skip Q2 · 2 full-skip Q1) un-quarantined; 159 tests recovered (88 Q2 + 26 Q1a test_phase_8_b_5b.py + 45 Q1b test_phase_8_seam_3_sub_stage_3.py). See notes/waveF_retirement_charter.md and STATE/DECISIONS.md §Wave F · Scope A."*
- Tree-wide skip-decorator sweep: **only 1 skip decorator** remains in `tests/invariants/` — `test_wsolvalift_cp_s8_donor_lift_case_agnostic.py::test_cp_s8_engines_expose_run_callable` (legacy conditional · counted in `counts_at_baseline.legacy_conditional_skips: 1`, NOT D1a-1).

### Finding

**Lane 1 is EXHAUSTED.** The 165-quarantined D1a-1 class the owner directive referenced was **fully retired 19 days ago at Wave F Scope A** via a framework upgrade + robust walker fix (Path 2 from the waveF retirement charter, options 1+2). All 21 chartered files un-quarantined. 159 tests recovered. Zero residual D1a-1 quarantined tests exist to pilot on.

**Owner directive references appear to be from a pre-Wave-F snapshot.** No pilot-actionable work remains in this lane.

**No mechanism change proposed.** POST-2 lesson honoured: from-disk is authoritative; do not re-execute what was already discharged.

---

## §2 · LANE 2 · W-TaskEval-v1 + M8 watchdog/consistency items

Per SPRINT_PLAN.md (2026-09-06) and MILESTONE_STRUCTURE_REHOMED_20260915.md, the M8 catch-all P1..P6 charters are:

| # | Wave | Charter | From-disk status this shift |
|---|---|---|---|
| P1 | W-TaskEval-v1 | Task-shaped held-out eval (accuracy on option-picking · distributional shift · per-value-chain slicing · paired eval vs baseline_record) | **NOT BUILT · prerequisite unmet** |
| P2 | W-Gradient-Step-Checkpoint | Mid-epoch resume via `save_strategy='steps'` | out-of-directive-scope this shift |
| P3 | W-Row-Stream-Extractor | Bounded-memory row extraction | out-of-directive-scope this shift |
| P4 | W-Adapter-Tensor-Persist | .pt tensor persistence + adapter registry | depends-on P1 · not addressable |
| P5 | W-Queue-Watchdog | Dispatcher-level restart + queue-state symlink atomicity | **PARTIAL · orchestrator-level exists** |
| P6 | W-Cross-Table-Consistency-Check | Static + runtime check that no combination of emitted columns across tables can reconstruct an identifier | **NOT BUILT · buildable now (case-agnostic · preventive charter)** |

Owner directive scope this shift is P1 + P5 + P6 ("W-TaskEval-v1 and the remaining small M8 watchdog/consistency items"). Details on each:

### §2.1 · W-TaskEval-v1 (P1)

**Module search:** zero results under `backend/services/` for `task_eval` · `taskeval` · `held_out_eval` (module names). Only references are in `tests/invariants/test_multi_table_extract.py` (charter-source citation) and `baseline_failures.json` (ratchet-history free text).

**Prerequisite check (charter verbatim `SPRINT_PLAN.md:19`):** *"Prerequisites: Campaigns A + B have settled (both have adapter.tar.gz + held_out_eval.json banked)."*

Reality check:
- `phase0/text_train_pipeline/txttrain_20260831T193455Z_9594859a/adapter.tar.gz` exists (Campaign A · 2026-08-31).
- `phase0/gpu_receipts/20260906T160900Z_diagnosis/akki-vm/held_out_eval.json` exists (single held-out eval · 2026-09-06 diagnosis run).
- **No paired Campaign-B `adapter.tar.gz` + `held_out_eval.json` set found on disk.**

**Verdict: BLOCKED-ON-PREREQUISITE.** Campaign B settlement is an owner-side / campaign-execution scope item, not a build-lane action. Under owner discipline "do not sequence · owner picks", cannot advance without Campaign B landing an adapter + eval.

### §2.2 · W-Queue-Watchdog (P5)

**Module search:** `backend/services/orchestrator_resilience/watchdog.py` EXISTS (from `W-Orchestrator-Resilience-r2-close` · commit `5be5d36` · 2026-09-06).
- Covers: orchestrator-level (pod-side) liveness via `pid_is_alive` (POSIX signal-0 zero-influence · never terminates), `is_orchestrator_dead` composing r1 primitives (heartbeat + orphan_detector + adopt), `select_adoptable_orphans` surfacing adoptable orphans with reasons.
- Zero-influence discipline explicit in the module docstring: "The watchdog is an observer. No `terminate_*` / `kill_*` / `stop_*` / `signal_*` names on the public surface."

**Tools:** `tools/gpu_burn_watchdog.py` + `tools/orchestrator_watchdog.py` (both informational-only in r2 scope · auto-execute deferred).

**Chartered scope for P5 (verbatim `SPRINT_PLAN.md:52-56`):** *"on-host systemd-style watchdog for the dispatcher process; symlink-atomic queue-state advance; heartbeat monitored by lightweight sidecar (`on_host_dispatcher_watchdog.sh`)"*

**Delta:** existing surface covers pod-side orchestrator-level; chartered surface adds on-host dispatcher-level (queue-state symlink atomicity + systemd/bash sidecar).

**Verdict: PARTIAL · owner-input-scoped.** The on-host portion involves systemd/bash installation on GPU hosts during the LIVE 72h utilization campaign — a live-perturbation class the campaign discipline explicitly prohibits ("Never kill a training run mid-flight" · SO §5). The chartered follow-on operator action (`on_host_dispatcher_watchdog.sh` installation) is safer post-campaign. Under SO §4.2 rule-proliferation ban (POST-2 lesson) + campaign-discipline, do not author a parallel pod-side dispatcher-watchdog module during the live campaign.

### §2.3 · W-Cross-Table-Consistency-Check (P6)

**Module search:** zero results under `backend/services/` and `backend/contracts/` for `cross_emit` · `cross-emit` · `IdentifierReconstruct` · `identifier_reconstruction` · `correlation_check` · `column_combination` · `identifier_shaped` · `EMITTED_COLUMNS`. No pre-existing surface.

**Chartered scope (verbatim `SPRINT_PLAN.md:61-66`):** *"for waves emitting multiple identifier-shaped columns. static + runtime check that no combination of emitted columns across tables can reconstruct an identifier. Prerequisites: any wave emitting >1 identifier-shaped column from >1 table (preventive charter). Outcome: refuses-unclassified-by-construction extends per-emitted-set, closing a theoretical cross-table leak channel. Estimate: S (~250 LOC)."*

**Case-agnosticity check:** the contract is domain-agnostic (identifier-shaped columns exist across estate data, transcripts, extraction outputs — the check is a shape-frozen refusal contract not tied to any single kind).

**Verdict: BUILDABLE NOW.** Small scope (~250 LOC estimate) · case-agnostic · preventive-charter (does not require a triggering wave to land as a shape-frozen contract module) · zero owner-input dependency · zero live-campaign perturbation. Tests-first mechanical RED → double-green byte-match → ratchet bump → seal → §3.3 3-commit protocol matches all prior mechanism-build waves this session.

---

## §3 · Summary triage table

| Lane | Item | Status | Buildable this shift? |
|---|---|---|---|
| 1 | Quarantine-restoration pilot | EXHAUSTED (retired 19 days ago at Wave F Scope A) | No · nothing to pilot |
| 2 · P1 | W-TaskEval-v1 | BLOCKED-ON-PREREQUISITE (Campaign B unsettled) | No · owner-side scope |
| 2 · P5 | W-Queue-Watchdog | PARTIAL (orchestrator-level exists; on-host dispatcher-level chartered for post-campaign operator action) | No · live-campaign perturbation class |
| 2 · P6 | W-Cross-Table-Consistency-Check | NOT BUILT · buildable now (case-agnostic · preventive · ~250 LOC) | **Yes** · matches "case-agnostic, tests-first" directive |

---

## §4 · Recommendation

Under owner's directive step-3 verbatim ("If both lanes exhaust or block: produce the M8 status rollup ... and hold"), two of three lane-2 items are effectively blocked (P1 owner-prerequisite · P5 campaign-perturbation-class). The remaining path options are:

**A. Build W-Cross-Table-Consistency-Check (CP-M8-CTCC-1) now.** Small scope · case-agnostic · preventive-charter · zero owner-input dependency · zero live-campaign perturbation. Follows all prior mechanism-build waves' §3.3 3-commit protocol. This keeps the build lane moving in the way owner directive intended.

**B. Skip P6 and produce M8 status rollup immediately.** Same-shape as M7 VERIFICATION ROLLUP · covers the M8 catch-all state (both lanes' from-disk findings + P1..P6 status + GPU util snapshot) · then hold with utilization interleave only.

**Agent recommendation: A (build P6 now, then produce M8 status rollup).** Rationale: owner directive explicitly authorized "verify-or-build accordingly, case-agnostic, tests-first" for the lane-2 items; P6 uniquely matches "case-agnostic + buildable + no live-campaign perturbation"; discharging P6 removes one preventive-charter follow-on from the M8 backlog before rollup.

---

## §5 · Utilization snapshot at findings-report time

- Elapsed 2.73 h · Remaining 69.27 h.
- Both hosts sampler_alive+workload_alive throughout.
- akki-vm: 76 telemetry samples · 326 bench iters (ok=326) · peak 100% util per GPU · ~691 W · ~70°C.
- akki-vm-ii: 70 telemetry samples · 326 bench iters (ok=326) · peak 100% util per GPU · ~693 W · ~71°C.
- 652 total bench artefacts banked · zero synthetic burn · in-perimeter.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
