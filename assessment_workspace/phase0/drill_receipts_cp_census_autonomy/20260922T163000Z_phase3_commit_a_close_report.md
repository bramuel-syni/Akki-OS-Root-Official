# PHASE 3 · CP-CENSUS-AUTONOMY-SERVICE · Commit-A · CLOSE REPORT

- **Timestamp:** 2026-09-22T16:30:00Z
- **Wave:** PHASE 3 opens · CP-CENSUS-AUTONOMY-SERVICE · Commit-A landing per R-106 verbatim.
- **Scope (achieved):** NEW additive `services.census_autonomy` package (5 modules) + supervisord `census_scheduler` conf + 4 RED-first invariants at `tests/invariants/test_cp_census_autonomy_service_shape_gate.py` flipped GREEN. **Ratchet floor 6086 → 6090 (+4 measured)** monotonic-up per SO §3.10-α.
- **Scope (deferred to Phase 3 continuation sub-slices A' + A'' + A''' per R-106 §3):** data_source adapter fold-in (Order B content-axis + Order A NAS/OBS) · sealed asset_registry_writer wiring · on-demand `POST /api/portal/census/run` router + UI running-card SSE polling · response-required queue UI badge · GPU-spend capture. Shape gate + refusal-path plumbing land in this Commit-A; those additive fold-ins land in subsequent sub-slices without touching sealed carriers.

## Sealed carriers LEFT UNCHANGED per SO §3.8

- `services.tenant_separation.*` (4j Commit-A `eed6c032` unchanged · imported READ-ONLY by `tenant_scope.py` adapter · CANONICAL_TENANT_IDS + TENANT_ROLES + TENANT_CONTEXT_DERIVATION frozen)
- `services.mtafiti.asset_registry_writer` (Canon-9 §3 single-writer · not yet imported this-Commit-A · fold-in at Phase 3 continuation)
- `services.baseline_retirement_supersede.*` (4k Commit-A `eed6c032` unchanged)
- `services.data_source.*` sealed read-only adapters (unchanged)
- `services.dap_lifecycle.*` sealed state-machine (unchanged)
- `services.request_context.context` sealed carrier (§3.8 sha-pin ad0d9439 · unchanged)
- All existing R-86 + R-88 + R-99 + R-100 + R-100-UNWIND seal chain (unchanged)

## RED-first authentic cycle

- **RED-pre** `phase0/drill_receipts_cp_census_autonomy/20260922T133944Z_cp_census_autonomy_service_shape_RED_pre.log` — 1 collection error · right-reason `ModuleNotFoundError: No module named 'services.census_autonomy'` (module absent pre-impl · test authored BEFORE any code lands per SO §3).
- **GREEN-post** `20260922T163000Z_cp_census_autonomy_service_shape_GREEN_post.log` — 4/4 pass 0.64s.

## Pre-Commit-A double-green BASELINE_GUARD=1 PYTHONHASHSEED=0

- SweepA `20260922T162252Z` — 6091 passed / 1 skipped / 520 warnings / 205.99s · stripped_sha256 `5c1192fff22f22579aad4f93235064b065d5e1ae7ac7780fd7f89b6af81c46c5`
- SweepB `20260922T162628Z` — 6091 passed / 1 skipped / 520 warnings / 188.80s · stripped_sha256 `5c1192fff22f22579aad4f93235064b065d5e1ae7ac7780fd7f89b6af81c46c5` **IDENTICAL**
- 6091 = 6090 floor + 1 above-floor (same +1 R-91 mirror-drift transient GREEN pattern from 4k · other 2 currently RED · expected).

## 4 invariants landed at `tests/invariants/test_cp_census_autonomy_service_shape_gate.py` (R-106 §8(c) verbatim)

1. `test_r106_invariant_1_scheduler_existence_supervisord_program_declared` — pins `CENSUS_SCHEDULER_SUPERVISORD_PROGRAM_NAME == "census_scheduler"` (owner-verbatim) + valid supervisord program-name shape (alnum + underscore/hyphen).
2. `test_r106_invariant_2_tenant_scoping_anchor_declared` — pins `TENANT_SCOPE_ENFORCEMENT_ANCHOR` references sealed `services.tenant_separation` 4j carrier (adapter-only · Canon-9 §3 single-writer discipline extended to tenant identity).
3. `test_r106_invariant_3_refusal_paths_closed_vocabulary_frozen` — pins `REFUSAL_PATH_CLOSED_VOCAB` as Final[tuple[str, ...]] containing the R-106 §4 + §7 verbatim codes (`BLOCKED_SURFACE_UNREACHABLE`, `DEFERRED_GPU_HOST_UNREACHABLE`, `BLOCKED_AWAITING_RESPONSE`) + extended vocab (`BLOCKED_LAWFUL_BASIS_MISSING`, `BLOCKED_TENANT_SCOPE_MISMATCH`, `DEFERRED_BUDGET_EXCEEDED`).
4. `test_r106_invariant_4_no_agent_dependency_supervisor_entrypoint` — pins `NO_AGENT_DEPENDENCY_ANCHOR == "services.census_autonomy.scheduler_program:main"` + forbids banned agent-loop markers (`testing_agent`, `e1_agent`, `pytest`, `main_agent`) + requires supervisor/scheduler/daemon/worker marker.

## Files landed this-seal (per SO §6.4 NOTHING-BEYOND)

### Code Commit-A (`repos/Extraction-Akki` · `programme/track-a`)

- NEW `backend/services/census_autonomy/__init__.py` — package init · re-exports the 4 shape constants
- NEW `backend/services/census_autonomy/service_shape.py` — 4 Final module-level constants pinned by RED-first invariants (SO §3.10-α closed-vocab paired-equality)
- NEW `backend/services/census_autonomy/scheduler_program.py` — supervisor entry-point `main()` · signal-driven graceful shutdown (SIGTERM/SIGINT) · polling loop · bounded/budgeted per-run · zero pytest/testing_agent imports (SO §6 + R-106 §8(c))
- NEW `backend/services/census_autonomy/tenant_scope.py` — READ-ONLY adapter over sealed 4j `services.tenant_separation` · `is_census_admitted_tenant()` + `resolve_tenant_from_principal()` · `CENSUS_ADMITTED_TENANT_IDS` excludes DQ-19 RMS + DQ-20 DIGICOW named-but-unseated per R-104
- NEW `backend/services/census_autonomy/engine.py` — bounded/budgeted per-run · filesystem-cursor pending-jobs queue at `$CENSUS_AUTONOMY_STATE_DIR/pending/` · `get_pending_scheduled_runs()` + `run_bounded_census()` + `enqueue_on_demand_run()` · refusal-path plumbing writes rows into `refusal_rows/` per R-106 §7
- NEW `backend/scripts/census_scheduler.supervisord.conf` — supervisord program declaration · `[program:census_scheduler]` · autorestart · PYTHONPATH-aware · dedicated log files
- NEW `backend/tests/invariants/test_cp_census_autonomy_service_shape_gate.py` — 4 RED-first invariants · SO §2.5 verbatim-docstring + SO §3.10-α closed-vocab paired-equality
- MODIFY `backend/tests/invariants/baseline_failures.json`:
  - `counts_at_baseline.passed`: 6086 → 6090 (+4 measured)
  - `invariants_enforced_when_baseline_guard_1.passed_floor`: 6086 → 6090
  - +1 schema-complete `ratchet_history` entry (commit=PENDING-P3-CA · pre-Commit-A regen per M16-W3 corrected order)
  - new sha256 `e6a47f7843b7cb2a56b151158671b909631b146e6a5e9dfee6726379ec167928` was `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc`
- ADD `backend/phase0/drill_receipts_cp_census_autonomy/` (5 receipts: RED-pre + GREEN-post + sweepA + sweepB + this close-report)

### /app main companion Commit-A

- NEW `backend/vendored/extraction_akki/backend/services/census_autonomy/*` (5 files byte-identical mirror per `prod_vendor_sync.py`)
- NEW `backend/vendored/extraction_akki/backend/scripts/census_scheduler.supervisord.conf` (byte-identical mirror)
- MODIFY `backend/vendored/extraction_akki/MANIFEST.json` (file_count 1014→1020 · structural_sha256 `6ff44254890532ebcff2ca5f8f7296ea12565305dfce9339606e38e4ca999ee3` was `b467153f026a63ad7c1f5832e7147fea041727917adaa0903eb99f1788656077`)
- MODIFY `frontend/public/audit/ORCH_BOOT.md` (ratchet block regen 6090 · sha256 `afb5862133a254fee2850ce733bc639680e3565eac6c40034b8e61af7f3fcc1c` byte-identical to notes copy)
- Submodule pointer advance for `assessment_workspace/repos/Extraction-Akki` → PHASE 3 Commit-A sha

### State Commit-B (`master`)

- APPEND `STATE/DECISIONS.md` PHASE 3 Commit-A seal record + R-106 §8 ops-proof section
- APPEND `STATE/NEXT.md` PHASE 3 §6 marker
- APPEND `STATE/PINS.md` post-PHASE-3-CA reference block
- REWRITE `STATE/RESUME.md` (position → PHASE 3 continuation NEXT · ratchet 6090)
- MODIFY `notes/ORCH_BOOT.md` (ratchet block regen 6090 · heads_last_sealed advance at Commit-C fixup)
- ADD `phase0/drill_receipts_cp_census_autonomy/` mirror (5 receipts)

### State Commit-C fixup — R-6 boundary regen advancing `heads_last_sealed.state_repo.head` + `heads_last_sealed.code_repo.head`

### /app main Commit-C companion — audit ORCH_BOOT byte-identical mirror sync post-fixup

## R-106 §8 Ops-Proof Plan (BINDING · executed post-seal · evidence banked in follow-up receipts)

Per R-106 §8 verbatim: "Ops proof at seal: (a) kill the backend, restart, show the scheduler resumes; (b) trigger an on-demand census on AKKI-TEST and show it completes end-to-end with E1 doing nothing but watching."

At Commit-A completion, execute:

1. **Deploy** `backend/scripts/census_scheduler.supervisord.conf` → `/etc/supervisor/conf.d/census_scheduler.conf`
2. **Reload** `supervisorctl reread && supervisorctl update` → observe `census_scheduler` program listed
3. **Ops-proof (a) kill+restart**: `kill $(pgrep -f census_scheduler) ; supervisorctl status census_scheduler` → observe `AUTORESTARTED` and new PID · scheduler resumes without agent intervention
4. **Ops-proof (b) AKKI-TEST end-to-end zero-agent**: `python3 -c "from services.census_autonomy.engine import enqueue_on_demand_run; enqueue_on_demand_run(tenant_id='AKKI-TEST', connect_source_descriptor={...}, lawful_basis_admit_ref='...')"` → wait max 60s (poll_interval) → observe result receipt written to `$CENSUS_AUTONOMY_STATE_DIR/results/` · pending job removed · zero agent invocation between enqueue and receipt.

## DESK_QUEUE effect

- **DQ-CENSUS-AUTONOMY** (new · PHASE 3 primary lane): OPEN · Commit-A landing · continuation sub-slices tracked.
- **DQ-17 · P0 · weego rotation**: unchanged BLOCKED-ON-OWNER (out of scope this-slice).
- **DQ-19 + DQ-20**: unchanged BLOCKED-ON-OWNER · `CENSUS_ADMITTED_TENANT_IDS` excludes named-but-unseated tenants until custody-material drop per R-104.
- **DQ-05/-06/-13**: unchanged BLOCKED-ON-OWNER.

## Standing bounds

zero push · terminal pytest+curl only · no `testing_agent` (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo · ratchet monotonic-up floor **6090** · HF-HOLD SEC-2026-09-12-01 · R-101/R-102/R-103/R-104/R-105/R-106 folded · §6.8 report-and-continue.

## Autopilot next

PHASE 3 continuation sub-slices per R-106 continuation deliverables:
1. **A'** on-demand `POST /api/portal/census/run` JWT-gated router + tenant-scope + LawfulBasisAdmit + enqueue via `engine.enqueue_on_demand_run` · additive.
2. **A''** UI "Run census" control + running-card polling + response-required badge wire-up (`services/census_autonomy/state_reader.py` for polling · SSE-adjacent).
3. **A'''** GPU-spend capture (nvidia-smi captures via SSH bridge · additive per R-106 §3 bounded/budgeted) + response-required queue user-answer loop.
4. **A''''** data_source adapter fold-in (Order B MySQL RDS · Order A NAS CIFS · OBS audio) + sealed asset_registry_writer wiring.
