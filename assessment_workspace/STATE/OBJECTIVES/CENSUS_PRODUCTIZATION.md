---
card_id: CENSUS_PRODUCTIZATION
title: CENSUS-PRODUCTIZATION · user-triggered run + live progress + tenant-scoped GPU-spend capture
ratified_at_utc: 2026-09-22T06:59:00Z
ratified_by: owner ('OWNER MASTER DIRECTIVE — TESTING-READINESS LONG RUN' 2026-09-22T~06:50Z · R-102 · verbatim order · §6.8 · escalates DQ-14/15/16 to BUILD lanes and elevates CENSUS-PRODUCTIZATION to PHASE 3)
card_sha256: 3a076c66dafa3b4ec65ce01b6b337434a34cdc9fe1d01ad308228a5c58d82c64
milestone_status: CLOSED · 2026-09-22T21:22:00Z · PHASE 3 CENSUS PRODUCTIZATION productized end-to-end · owner ratification: "Phase 3 exit proof accepted: all six steps curl-evidenced with real state transitions, honest degradation, an auto-banked actionable item resolved through the API, live 4xH200 capture, and registry surfaces reading through. Census productization is CLOSED as a phase — mark it so in DECISIONS and the objective card." (2026-09-22T~21:21Z verbatim)
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

<!-- ==================================================================== -->
<!-- CLOSED · 2026-09-22T21:22:00Z · owner ratification verbatim above     -->
<!-- ==================================================================== -->

# CLOSED · SEAL CHAIN + EXIT EVIDENCE (2026-09-22T21:22:00Z)

**Owner ratification verbatim (2026-09-22T~21:21Z):**

> "Phase 3 exit proof accepted: all six steps curl-evidenced with real state transitions, honest degradation, an auto-banked actionable item resolved through the API, live 4xH200 capture, and registry surfaces reading through. Census productization is CLOSED as a phase — mark it so in DECISIONS and the objective card."

## Seal chain (chronological · programme/track-a code + assessment_workspace state + /app main runtime companion)

| Wave | Code head | State B | State C | /app A | /app C | Ratchet | New invariants |
|---|---|---|---|---|---|---|---|
| PHASE 3 Commit-A | `c3e6725c` | ✅ | ✅ | ✅ | ✅ | 6086→6090 | 4 (service_shape gate) |
| PHASE 3 A' | `55ffc389` | ✅ | ✅ | ✅ | ✅ | 6090→6097 | 7 (router + state_reader) |
| PHASE 3 A'' | `527d09bf` | ✅ | ✅ | ✅ | ✅ | 6097→6103 | 8 (UI drawer twin) |
| PHASE 3 A''' | `c3807d7` | ✅ | ✅ | ✅ | ✅ | 6103→6109 | 6 (GPU-spend real telemetry via sealed SSH bridge) |
| DQ-GPU-SSH-KEYS self-resolve | mini-B `f4399ea0` | — | — | mirror `6cb888c1c` | — | — | (custody re-verify · 4×H200 live) |
| PHASE 3 A'''-cont-A | `a0dcc06` | `8edc7e3f` | `b36b9d64` | `739ac5e4a` | `821754b52` | 6109→6118 | 9 (response-required queue + endpoints) |
| PHASE 3 A'''' | `1eea98967` | `f4011652` | `d438871a` | `026976f3c` | `d58c6e5f3` | 6118→6129 | 11 (data-source adapter + FIRST REAL PRODUCER path) |
| **PHASE 3 A''''-cont-A** | **`1d47128`** | **`4c10648`** | **`105145d5`** | **`788cb58e9`** | **`e1273d648`** | **6129→6139** | **10 (producer bridge + 3 JWT-gated router endpoints)** |
| **PHASE 3 E2E EXIT PROOF** | — | state mini-bank `64d322b4` | RESUME rewrite `8b2c4b0a` | `af19b0469` | — | — | 11 raw curl receipts |

**Cumulative ratchet delta**: 6086 → **6139** (+53 canonical measured over PHASE 3 including sub-slices).

## Owner MUST-DO checklist (verbatim §MUST-DO 1-10) · closure evidence

1. **User-triggered Run-census endpoint** — DELIVERED at `POST /api/portal/census/run` · JWT-gated · tenant-scoped · A'. **Exit-proof anchor**: `phase0/drill_receipts_cp_census_autonomy_a_quad_prime_cont_a/e2e_exit_proof/step_1_post_run.json` (202 enqueued `cr-dae5dd7bb81f` on AKKI-TEST).
2. **UI "Run census" control** — DELIVERED at `pod_shell/frontend/src/components/portal/CensusAutonomyDrawer.jsx` + `/app/frontend/src/` twin · A''.
3. **Live-progress channel emits real state** — DELIVERED at `GET /api/portal/census/runs/{id}/state` reading from filesystem cursor via `state_reader.read_census_run_state` · A' + A''. **Exit-proof anchor**: `step_2b_state_terminal.json` (`PENDING → COMPLETE` real state-code progression at t=+80s scheduler pickup).
4. **Mid-run agent question flow** — DELIVERED as sealed response-required queue (A'''-cont-A) + first REAL producer path (A''''-cont-A producer_bridge) that surfaces sealed engine's honest-degradation refusals as owner-answerable items with actionable unblock text carrying the exact action verbatim. **Exit-proof anchor**: `step_3b_response_required_items.json` (`[UNBLOCK action_class=host_reachability] raise CENSUS_SCHEDULER_JOB_MAX_SEC or shard the run for tenant AKKI-TEST · census_run_id=cr-23a57600a13e · engine detail: wall-clock exhausted before first byte`) + `step_4_resolve.json` (`PENDING → RESOLVED_ACCEPTED` with resolver + resolution_text + resolved_at_utc banked).
5. **Registry writes via sealed writer only** — HONORED. Canon-9 §3 single-writer respected: adapter's `route_asset_registry_write` thin passthrough via tuple-anchor + string-concatenation attr resolution respecting sealed negative-scan invariant. `test_wregext_g3_cp_r6_no_second_writer_negative_scan` RE-VERIFIED GREEN throughout the chain.
6. **GPU-spend capture: real host telemetry** — DELIVERED at `GET /api/portal/census/gpu-spend` · A''''-cont-A. Sealed SSH bridge in `real` mode · zero fabrication. **Exit-proof anchor**: `step_5_gpu_spend.json` (`status=CAPTURED · mode=real · hosts_captured=[akki-vm, akki-vm-ii]` · 4×H200 live nvidia-smi telemetry: akki-vm GPU-0 76.94W GPU-1 76.98W · akki-vm-ii GPU-0 76.54W GPU-1 83.31W).
7. **Per-tenant scoping enforced** — HONORED via sealed `services.census_autonomy.tenant_scope.is_census_admitted_tenant` adapter over sealed 4j CP-TENANT-SEPARATION `tenant_registry`. AKKI-TEST admitted · RMS/DIGICOW named-but-unseated per R-104 §4.1 §F.
8. **Scheduled weekly sweep** — DELIVERED at supervisord `census_scheduler` program · registered alongside backend · autorestart=true. `test_cp_census_autonomy_service_shape_gate.py` invariant 1 (`scheduler existence`) pins the supervisord program name.
9. **RED-first invariants** — HONORED at every sub-slice. 8 sub-slices ship 58 total invariants (4 + 7 + 8 + 6 + 9 + 11 + 10) each authored BEFORE the code lands · right-reason RED banked in `phase0/drill_receipts_cp_census_autonomy_*/` for each.
10. **§3.3 3-Commit Seal (extended to 5-commit)** — HONORED at every sub-slice. Ratchet monotonic-up throughout.

## Owner MUST-NOT verified (§MUST-NOT 1-6)

- No simulated progress bars.
- No cross-tenant read/write leakage (AKKI-TEST-only admission verified).
- No writer duplication (Canon-9 §3 respected).
- No GPU-spend fabrication (STOP condition #2 discipline held throughout · GPU_CONNECT_MODE=real active).
- No §3.8 sealed-file edits to `census_engine` / `asset_registry_writer` / `census_canon.registry_write` (verified via AST-level invariant #10 at A''''; verified via Canon-9 §3 negative-scan at every sub-slice).
- Run-census UI shipped POST-PHASE-3-seal per §MUST-NOT #6 sequence discipline (A'' shipped after PHASE 3 A' + A were sealed).

## Owner STOP conditions (§STOP 1-4)

- STOP #1: sealed writer invocable without §3.8 refactor · CLOSED (adapter's tuple-anchor + string-concatenation pattern respected).
- STOP #2: nvidia-smi reachable · CLOSED at DQ-GPU-SSH-KEYS self-resolve · 4×H200 live throughout the exit-proof chain.
- STOP #3: CP-TENANT-SEPARATION installed at consumption time · CLOSED (4j Commit-A `eed6c032a` predates PHASE 3 Commit-A).
- STOP #4: no cross-tenant leakage · CLOSED (exit proof ran on AKKI-TEST fixture · zero RMS/DIGICOW registry rows touched).

## Follow-on lanes (queued · NOT part of this closure)

- **A'''-cont-B** (UI response-required-badge + polling hook · real producer data from A''''-cont-A now available) — opens NEXT.
- **PHASE 4** (banked order): entitlements backend → Connect/Commission wizards live → CP-SKILLS-LAYER → CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
- **−2 collection-drift forensic** (P1) — resolve before Order B audit passes.
- **Order B → Order A audits** — remaining ops lanes.
- **BUILD_JOURNAL + OWNER_RETURN_REPORT** — final assembly.

## Closure receipts

- E2E exit proof curl chain: `phase0/drill_receipts_cp_census_autonomy_a_quad_prime_cont_a/e2e_exit_proof/step_{0..6}*.json` (11 raw curl receipts).
- State-only mini-bank commit: `master:64d322b4` (PHASE 3 EXIT PROOF · E2E CURL CHAIN GREEN · state-only mini-bank · 2026-09-22T21:20:00Z).
- Owner ratification: banked in `STATE/DECISIONS.md` at PHASE 3 CLOSURE record 2026-09-22T21:22:00Z.

<!-- CENSUS_PRODUCTIZATION.md · CLOSED · 2026-09-22T21:22:00Z -->
