# PHASE 3 continuation A' · CP-CENSUS-AUTONOMY-ROUTER · Commit-A · CLOSE REPORT

- **Timestamp:** 2026-09-22T17:10:00Z
- **Wave:** PHASE 3 continuation A' opens · JWT-gated on-demand POST + real-scheduler-state GET · productizes the raw-Python enqueue path used in the R-106 §8(b) ops-proof (PHASE 3 Commit-A c3e6725c).
- **Scope (achieved):** NEW additive `routers.portal_census_autonomy` + NEW additive `services.census_autonomy.state_reader` + additive `server.py`/`pod_shell/backend/server.py`/runtime `server.py` 2-line insert · 7 new RED-first invariants at `tests/invariants/test_cp_census_autonomy_router_a_prime.py` · **ratchet floor 6090 → 6097 (+7 measured)**.
- **Scope (deferred to Phase 3 continuation A'' next):** UI "Run census" control + running-card polling that calls `GET /api/portal/census/runs/{id}/state` · owner directive "REAL scheduler state only" enforced by state_reader (6 markers of synthesis banned in-source per invariant 6).

## Sealed carriers LEFT UNCHANGED per SO §3.8

- `services.auth.dependencies.require_identity_or_deny` (imported READ-ONLY)
- `services.auth.identity.Identity` (imported READ-ONLY)
- `services.enforce.principal_context_adapter.principal_context` (imported READ-ONLY)
- `services.census_autonomy.engine.enqueue_on_demand_run` + `CENSUS_STATE_DIR` + subdir constants (PHASE 3 Commit-A c3e6725c · READ-ONLY)
- `services.census_autonomy.service_shape.REFUSAL_PATH_CLOSED_VOCAB` (PHASE 3 Commit-A · READ-ONLY closed-vocab · not redefined)
- `services.census_autonomy.tenant_scope.is_census_admitted_tenant` (PHASE 3 Commit-A · READ-ONLY)
- 4j `services.tenant_separation.*` (transitively READ-ONLY via tenant_scope adapter)
- Canon-9 §3 `services.mtafiti.asset_registry_writer` (unchanged · fold-in at A'''')
- Full R-86 + R-88 + R-99 + R-100 + R-100-UNWIND seal chain (unchanged)

## RED-first authentic cycle

- **RED-pre** `phase0/drill_receipts_cp_census_autonomy_a_prime/20260922T165224Z_a_prime_RED_pre.log` — 1 collection error · right-reason `ModuleNotFoundError: No module named 'routers.portal_census_autonomy'` (module absent pre-impl · test authored BEFORE any router lands per SO §3).
- **GREEN-post v1** `20260922T165332Z_a_prime_GREEN_post.log` — 6/7 pass · 1 failure at invariant 6 detected an over-broad synthesis-marker check that flagged the owner-verbatim docstring quote of "never synthesized progress". Corrected the invariant to check only actual synthesis code markers (`progress_percent`, `estimated_completion`, `fake_progress`, `mock_state`, `random.random`, `random.randint`) — docstring quoting the owner directive no longer triggers the guard.
- **GREEN-post v2** `20260922T165349Z_a_prime_GREEN_post_v2.log` — 7/7 pass 0.66s.

## Ship-Manifest DoD drift caught + cured

- Sweep A v1 caught the new `portal_census_autonomy` router mounted in `backend/server.py` but absent from `pod_shell/backend/server.py` → invariant `test_repo_server_routers_are_covered_by_pod_or_known_unwired` FAILED right-reason.
- Cured by adding identical 2-line additive mount to `pod_shell/backend/server.py`.
- Sweep A v2 caught the same drift between pod_shell and runtime `/app/backend/server.py` → invariant `test_runtime_server_matches_repo_pod_shell` FAILED right-reason.
- Cured by adding identical 2-line additive mount to `/app/backend/server.py` (runtime).
- **Time-window drift**: `test_cp10_harness_receipt_is_still_recent` at 12.22h age (0.22h past 12h threshold). Refreshed via `tools/wave_g5_realchrome_verification_harness.py --label a_prime_refresh` at 2026-09-22T17:00:08Z (GREEN · dummies absent · expected present · styled-element-anchor spans intact). Not caused by this-slice.

## Pre-Commit-A double-green BASELINE_GUARD=1 PYTHONHASHSEED=0

- SweepA `20260922T170423Z` — 6098 passed / 1 skipped / 520 warnings / 189.13s · stripped_sha256 `acf5963382c139d65d81e545a34d5a0c23830cf203e2c5867af5d486cad43d4f`
- SweepB `20260922T170741Z` — 6098 passed / 1 skipped / 520 warnings / 189.20s · stripped_sha256 `acf5963382c139d65d81e545a34d5a0c23830cf203e2c5867af5d486cad43d4f` **IDENTICAL**
- 6098 = 6097 floor + 1 above-floor (same R-91 mirror-drift transient GREEN pattern).

## 7 invariants landed at `tests/invariants/test_cp_census_autonomy_router_a_prime.py`

1. `test_a_prime_invariant_1_post_run_route_declared_verbatim` — pins `ON_DEMAND_RUN_ROUTE_PATH == "/api/portal/census/run"` (SO §3.10-α · paired equality) + route accepts POST.
2. `test_a_prime_invariant_2_get_run_state_route_declared_verbatim` — pins `RUN_STATE_ROUTE_PATH_TEMPLATE == "/api/portal/census/runs/{census_run_id}/state"` + route accepts GET.
3. `test_a_prime_invariant_3_post_run_requires_jwt` — POST without JWT returns 401 (Owner confirmation anchor point b · verbatim).
4. `test_a_prime_invariant_4_get_state_requires_jwt` — GET without JWT returns 401.
5. `test_a_prime_invariant_5_state_reader_returns_closed_vocab_status` — `CENSUS_RUN_STATE_CODES` Final tuple contains `PENDING`/`COMPLETE`/`REFUSED` · unknown id → None (never synthesizes).
6. `test_a_prime_invariant_6_state_reader_never_synthesizes_progress` — source-level guard bans `progress_percent`/`estimated_completion`/`fake_progress`/`mock_state`/`random.random`/`random.randint` from state_reader.py (Owner directive verbatim: "never synthesized progress").
7. `test_a_prime_invariant_7_refusal_codes_from_sealed_service_shape` — router imports sealed `REFUSAL_PATH_CLOSED_VOCAB` READ-ONLY · does not redefine (SO §3.8).

## Files landed this-seal (per SO §6.4 NOTHING-BEYOND)

### Code Commit-A (`repos/Extraction-Akki` · `programme/track-a`)

- NEW `backend/routers/portal_census_autonomy.py` — JWT-gated POST enqueue + GET real-state polling endpoints · Final route path constants pinned by invariants · refusal codes from sealed vocab
- NEW `backend/services/census_autonomy/state_reader.py` — real-state cursor reader · `CENSUS_RUN_STATE_CODES` Final tuple · `read_census_run_state()` returns None for unknown ids (never synthesizes)
- MODIFY `backend/server.py` — 2-line additive `include_router` insert
- MODIFY `pod_shell/backend/server.py` — 2-line additive mirror mount (Ship-Manifest DoD parity)
- NEW `backend/tests/invariants/test_cp_census_autonomy_router_a_prime.py` — 7 RED-first invariants
- MODIFY `backend/tests/invariants/baseline_failures.json`:
  - `counts_at_baseline.passed`: 6090 → 6097 (+7 measured)
  - `invariants_enforced_when_baseline_guard_1.passed_floor`: 6090 → 6097
  - +1 schema-complete `ratchet_history` entry
  - new sha256 `eb377b5c7627b5e06c12db68ba0a84a76003ac2a5503e6e3c233422aeca9ea3d`
- ADD `backend/phase0/drill_receipts_cp_census_autonomy_a_prime/` (RED-pre + GREEN-post v1 + GREEN-post v2 + SweepA v1 + SweepA v2 + SweepA v3 + SweepB + this close-report + 2 R-106 §8 ops-proof receipts folded in from prior seal boundary)

### /app main companion Commit-A

- NEW `backend/vendored/extraction_akki/backend/routers/portal_census_autonomy.py` (byte-identical mirror per `prod_vendor_sync.py`)
- NEW `backend/vendored/extraction_akki/backend/services/census_autonomy/state_reader.py` (byte-identical mirror)
- MODIFY `backend/vendored/extraction_akki/MANIFEST.json` (file_count 1020→1022 · structural_sha256 `082210b5bd609a7e0d23fc842c05f017d9778ad396215f900694d95101c2e56a`)
- MODIFY `backend/server.py` — 2-line additive mirror mount (runtime · matches pod_shell · Ship-Manifest DoD parity)
- MODIFY `frontend/public/audit/ORCH_BOOT.md` (ratchet block regen 6097 · byte-identical to notes copy)
- Submodule pointer advance for `assessment_workspace/repos/Extraction-Akki` → this-slice code Commit-A sha

### State Commit-B (`master`)

- APPEND `STATE/DECISIONS.md` A' seal record
- APPEND `STATE/NEXT.md` A' §6 marker
- APPEND `STATE/PINS.md` post-A' reference block
- REWRITE `STATE/RESUME.md` (position → A'' NEXT · ratchet 6097)
- MODIFY `notes/ORCH_BOOT.md` (ratchet block regen 6097 · heads_last_sealed advance at Commit-C fixup)
- ADD `phase0/drill_receipts_cp_census_autonomy_a_prime/` mirror

### State Commit-C fixup — R-6 boundary regen

### /app main Commit-C companion — audit ORCH_BOOT byte-identical mirror sync post-fixup

## DESK_QUEUE effect

- **DQ-CENSUS-AUTONOMY** (PHASE 3 primary lane): A' Commit-A LANDING · A'' UI running-card next.
- **DQ-17/-19/-20/-05/-06/-13**: unchanged BLOCKED-ON-OWNER.

## Standing bounds

zero push · terminal pytest+curl only · testing_agent BANNED per SO §6 · additive-only §3.8 · three-repo · ratchet monotonic-up floor **6097** · HF-HOLD SEC-2026-09-12-01 · R-101/R-102/R-103/R-104/R-105/R-106 folded · §6.8 report-and-continue.

## Autopilot next

A'' UI "Run census" control + running-card polling · reads `GET /api/portal/census/runs/{id}/state` · owner "REAL scheduler state only" directive enforced by state_reader source-level guard.
