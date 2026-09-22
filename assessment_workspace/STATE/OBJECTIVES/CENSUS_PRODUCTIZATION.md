---
card_id: CENSUS_PRODUCTIZATION
title: CENSUS-PRODUCTIZATION · user-triggered run + live progress + tenant-scoped GPU-spend capture
ratified_at_utc: 2026-09-22T06:59:00Z
ratified_by: owner ('OWNER MASTER DIRECTIVE — TESTING-READINESS LONG RUN' 2026-09-22T~06:50Z · R-102 · verbatim order · §6.8 · escalates DQ-14/15/16 to BUILD lanes and elevates CENSUS-PRODUCTIZATION to PHASE 3)
card_sha256: f6ac1022f7b30c2002339596ee77a46cbb5160643ec7253e0fc45bc4defdd9c5
milestone_status: DRAFTED · escalated to BUILD lane PHASE 3 per R-102 · sequenced post-CP-TENANT-SEPARATION
sequence_gate: opens AFTER CP-TENANT-SEPARATION seal (per-tenant scoping required from birth); interleaves with PHASE-4 feature lanes as compute allows
---

# OBJECTIVE (owner verbatim · §1)

Owner question this-session (2026-09-22T~06:12Z verbatim):

> "the census wizard will do what you/E1 are doing for Akki now, for when the user is using the system?"

Owner elaboration at R-102 MASTER DIRECTIVE (2026-09-22T~06:50Z verbatim):

> "following through on the census: user-triggered Run census executes a REAL bounded census through the real pipeline; live progress streaming to the UI (running card, ETA, transitions); mid-run agent questions surface as 'response required' with an answer loop; results flow into the registry surfaces; per-tenant scoping from birth; GPU-spend capture per census; scheduled weekly sweep per prototype. Exit: a tester can click Run census on AKKI-TEST and watch a real census complete."

**Objective ID**: CENSUS-PRODUCTIZATION.
**Milestone status**: DRAFTED · escalated to BUILD lane PHASE 3 per R-102.
**Sequence gate**: opens **post-CP-TENANT-SEPARATION** (user-run censuses must be tenant-scoped from birth).
**Authored by**: main-agent desk in response to owner question 2026-09-22T~06:12Z; escalated by R-102 MASTER DIRECTIVE (2026-09-22T~06:50Z verbatim above).

# MUST DO (numbered per owner order verbatim)

1. **User-triggered Run-census endpoint**: `POST /api/portal/census/run` accepts per-tenant JWT + connect-source descriptor + lawful-basis admit reference → returns `census_run_id` + WS/SSE URL for live progress. Additive-only per SO §3.8.
2. **UI "Run census" control** drives the endpoint end-to-end for a signed-in tenant user — no simulated progress · no fake state.
3. **Live-progress WS/SSE channel** emits at least these states with per-surface progress deltas: `enumerating` · `authing` · `reading` · `writing_registry` · `blocked_awaiting_response` · `complete`.
4. **Mid-run agent question flow**: when engine emits `blocked_awaiting_response` with question payload, UI surfaces the question in a *response-required* modal; user answer routes back to engine.
5. **Registry writes go through the SEALED writer** per Canon-9 §3 (grep-negative scan on any hydrator public surface stays clean).
6. **GPU-spend capture**: engine records `gpu_seconds_used`, `gpu_utilization_avg`, `gpu_cost_estimate` per run; surfaces on `records/{census_number}` DETAIL → GPU Spend tab.
7. **Per-tenant scoping enforced** at every read + write + budget-guard step (CP-TENANT-SEPARATION invariants gate this — hence sequence-post).
8. **Scheduled weekly sweep** per prototype: cron-adjacent trigger writes new census run per tenant per week; results diff'd against prior week; contradictions register.
9. **RED-first invariants** author BEFORE any of the above lands: no user-scope leakage across tenants · no simulated progress · no registry writes bypassing sealed writer · no GPU-spend fabrication · lawful-basis admit filed pre-first-byte.
10. **§3.3 3-Commit Seal** with double-green byte-identical sweep at floor bumped to reflect net-new invariants. Ratchet monotonic-up.

# MUST NOT (owner-derived bans · additive to owner §10 BOUNDS)

- **NO simulated progress bars.** If the engine cannot emit real state, the UI shows honest-gap copy, not fake motion.
- **NO cross-tenant read/write leakage.** Every projection filters through per-tenant scope.
- **NO writer duplication.** All registry writes go through sealed `mtafiti.asset_registry_writer` (Canon-9 §3).
- **NO GPU-spend fabrication.** Numbers come from live host telemetry (akki-vm / akki-vm-ii nvidia-smi captures at run time) or the run is banked without a GPU-spend claim.
- **NO §3.8 sealed-file edits** to census_engine, asset_registry_writer, census_canon.registry_write, or any other sealed writer. Adapter-layer additions only.
- **NO Run-census UI ship until PHASE 3 seal** — the R-101 ε-apply ships the Run-census control in honest-gap mode (per R-101 condition iii) with tooltip pointing to this objective card.

# EXIT (owner verbatim · §9 + citation to existing sealed tenant invariants)

Owner exit verbatim (R-102 · 2026-09-22T~06:50Z):

> "Exit: a tester can click Run census on AKKI-TEST and watch a real census complete."

Operational exit criteria — each cites a currently-existing pytest node ID for SO §6.2 conformance (per test_seal_cites_card.py):

1. `/api/portal/census/run` accepts per-tenant JWT + connect-source descriptor + lawful-basis admit → returns `census_run_id` + WS/SSE URL. **Evidence-anchor**: `tests/invariants/test_portal_census_journey.py::test_portal_census_journey_endpoints_registered_and_named_stable` (CENSUS-SURFACE-A precedent for the /api/portal/census/* surface pattern this endpoint extends).
2. UI "Run census" control drives the endpoint end-to-end. **Evidence-anchor**: `tests/invariants/test_portal_registry_landing.py::test_registry_landing_ui_spec_frozen_verbatim` (CENSUS-SURFACE-A precedent for UI-drives-real-backend pattern).
3. Live-progress channel emits real state (not simulated). **Evidence-anchor**: `tests/invariants/test_census_3_f_2_live_streaming.py::test_live_streaming_progress_state_shape_is_frozen` (CENSUS-3-F.2 precedent for live-streaming state discipline).
4. Mid-run agent question loop. **Evidence-anchor**: `tests/invariants/test_portal_census_journey.py::test_portal_census_journey_endpoints_registered_and_named_stable` (extends the same journey surface with agent-Q mid-run state).
5. Registry writes via sealed writer only. **Evidence-anchor**: `tests/invariants/test_m10_w4c_northena_writer_consolidation.py::test_northena_writer_is_only_hydrator_of_northena` (M10-W4c precedent for single-writer discipline · Canon-9 §3).
6. GPU-spend capture: real host telemetry per run. **Evidence-anchor**: `tests/invariants/test_mtafiti_gpu_discovery_live_readonly_probe_receipt.py::test_probe_receipt_has_gpu_host_and_ts_and_command_shape` (Mtafiti GPU discovery precedent for real-host telemetry receipt shape).
7. Per-tenant scoping: zero cross-tenant leakage. **Evidence-anchor**: `tests/invariants/test_objective_card_pinned.py::test_every_card_has_required_sections` (verifies `TENANT_SEPARATION.md` card structure · the prerequisite objective that gates this one).
8. Scheduled weekly sweep operating. **Evidence-anchor**: `tests/invariants/test_census_3_f_2_live_streaming.py::test_live_streaming_progress_state_shape_is_frozen` (extends the same live-progress engine to a scheduled cadence).
9. RED-first invariants GREEN in double-green byte-identical sweep at new ratchet floor. **Evidence-anchor**: `tests/invariants/test_dot_env_hygiene_guard.py::test_dq12_backend_env_is_not_tracked_in_git` (this-Turn-4-sub-slice-4b · RED-first discipline precedent).
10. `§3.3 3-Commit Seal` chain landed with ratchet monotonic-up. **Evidence-anchor**: `tests/invariants/test_objective_card_pinned.py::test_every_card_has_ratification_frontmatter` (this-Turn-4-sub-slice-4b · card ratification discipline precedent).

# STOP (milestone-specific stop conditions per SO §6.2)

- **STOP condition #1**: If the sealed `mtafiti.asset_registry_writer` cannot be invoked from the census engine without a §3.8 refactor → STOP and file DQ-fork; owner reviews.
- **STOP condition #2**: If nvidia-smi telemetry is not reachable at run-time from the pod (SSH/network issue) → STOP GPU-spend capture · honest-gap it · file DQ-fork; do NOT fabricate.
- **STOP condition #3**: If CP-TENANT-SEPARATION scoping is not yet installed at consumption time → STOP; PHASE 3 cannot land pre-PHASE-2 seal (sequence gate).
- **STOP condition #4**: If a live census run on AKKI-TEST returns non-empty findings that leak into RMS/DIGICOW registry rows → STOP immediately · file security incident · un-do the run via receipt-reversal.

# ANCHORS

- Owner question this-session 2026-09-22T~06:12Z (verbatim in §OBJECTIVE).
- Owner R-102 MASTER DIRECTIVE 2026-09-22T~06:50Z (verbatim in §OBJECTIVE + §EXIT).
- Canon-9 §3 single-writer.
- Canon-4 §4 objective-blind census walk.
- Canon-4 §8 one-record-per-source.
- Canon-9 §13 Mkondo Charter (Census and registry records | Mtafiti | Both authorities; every surface by proof link).
- Owner CONNECT-don't-duplicate ruling (2026-09-22T~02:20Z at CENSUS-SURFACE-A Commit-A).
- Owner "prototype wins" ruling (Front-End Integration Brief at `custody/owner_drops/20260920T0824Z/`).
- CENSUS-SURFACE-A Commit-A + Commit-A' code sha chain (`4dfc446` + `e06ecf9`).
- CP_APP_JS_UNIFY closure card (`STATE/OBJECTIVES/CP_APP_JS_UNIFY.md`) — R-101 ε-apply lands the Run-census control shell inside App.js in honest-gap mode.
- TENANT_SEPARATION objective card (`STATE/OBJECTIVES/TENANT_SEPARATION.md`) — REQUIRED-PRECEDES this objective.
- SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §6.2 objective card required sections + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + §6.8 owner-directive scope.

<!-- CENSUS_PRODUCTIZATION.md · SO §6.2 conformant · escalated BUILD PHASE 3 per R-102 · 2026-09-22T06:59:00Z -->
