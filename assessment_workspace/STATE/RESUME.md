# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-09-22T21:20:00Z (**PHASE 3 EXIT PROOF · E2E CURL CHAIN GREEN** · R-102/R-106 owner directive HONORED verbatim · A''''-cont-A CP-CENSUS-AUTONOMY-PRODUCER-BRIDGE 5-Commit-Seal LANDED + state-only mini-bank of E2E curl receipts · ratchet 6129 → 6139 · owner-answerable actionable unblock text now surfacing on the sealed queue from the sealed engine's honest-degradation refusal paths via the producer bridge · 4×H200 live nvidia-smi telemetry CAPTURED via sealed SSH bridge · registry read surface visible with 6 source assets + 7 provenance pointers).

---

## 1 · POSITION

- **Phase:** PHASE 3 · **CENSUS AUTONOMY SERVICE** OPEN · Commit-A + A' + A'' + A''' + A'''-cont-A + A'''' + **A''''-cont-A LANDED** + **E2E EXIT PROOF DELIVERED** · continuation **A'''-cont-B (UI response-required-badge · real producer data now available)** NEXT.
- **Turn queue:**
  - 4a-4j ✅ SEALED · 4k ✅ SEALED (ratchet 6080→6086).
  - PHASE 3 Commit-A ✅ SEALED · ratchet 6086→6090.
  - PHASE 3 A' ✅ SEALED · ratchet 6090→6097.
  - PHASE 3 A'' ✅ SEALED · code `527d09bf` · ratchet 6097→6103.
  - PHASE 3 A''' ✅ SEALED · code `c3807d7` · ratchet 6103→6109.
  - DQ-GPU-SSH-KEYS SELF-RESOLVED · 4× H200 live nvidia-smi active.
  - PHASE 3 A'''-cont-A ✅ SEALED · code `a0dcc06` · ratchet 6109→6118.
  - PHASE 3 A'''' ✅ SEALED · code `1eea98967` · state B `f4011652` · ratchet 6118→6129.
  - **PHASE 3 A''''-cont-A ✅ SEALED THIS-TURN** at code `1d47128` · /app companion `788cb58e9` · state B `4c10648550d945ab217622aeca4cf75bb7e6f89f` · state C `105145d5` · /app C `e1273d648` (CP-CENSUS-AUTONOMY-PRODUCER-BRIDGE · engine-integration LITE · NEW additive `services/census_autonomy/producer_bridge.py` [scans sealed engine's `<CENSUS_STATE_DIR>/refusal_rows/` cursor for a given census_run_id + maps each sealed `REFUSAL_PATH_CLOSED_VOCAB` code to owner-answerable unblock action via total `REFUSAL_TO_UNBLOCK_ACTION_MAP` + banks each row into the sealed A'''-cont-A queue via the sealed A'''' adapter's public `emit_data_source_producer_items` callable ONLY · zero engine internals imported] · NEW additive `routers/portal_census_autonomy_producer.py` [3 JWT-gated tenant-scoped endpoints: `POST /api/portal/census/runs/synchronous` + `POST /api/portal/census/runs/{id}/bank-refusals` + `GET /api/portal/census/gpu-spend`] · byte-identical server.py mirror pair `pod_shell↔/app/backend` both sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` · 10 new RED-first invariants · ratchet 6129→6139 +10 canonical measured · double-green stripped-sha256 `797c513e3fb586b038391158291553971dff8f7513fd9de484c87663fae86bee` IDENTICAL sweep_A/B both 6142 passed 1 skipped 0 failed 520 warnings · vendored twin same-seal sync file_count 1026→1028 structural_sha256 `3dbda87ece4b9c428f939484650ff300459859992efdbe34198b9a9477615b02`).
  - **E2E EXIT PROOF DELIVERED THIS-TURN** at state mini-bank `64d322b4` (state-only · post-A''''-cont-A seal · R-102/R-106 owner directive HONORED verbatim: 'close Phase 3 with an END-TO-END EXIT PROOF, curl-evidenced in the next report... Every step a raw curl receipt.'). All 6 steps GREEN. Raw curl receipts at `phase0/drill_receipts_cp_census_autonomy_a_quad_prime_cont_a/e2e_exit_proof/`:
    - Step 1 `POST /run` (JWT · AKKI-TEST) → 202 enqueued `cr-dae5dd7bb81f` · principal `demo.master_admin`.
    - Step 2 `GET /state` → real state-code progression `PENDING (t=+10..+70s) → COMPLETE (t=+80s)` scheduler pickup honoured.
    - Step 3 `POST /runs/synchronous {budget_seconds_offset:-1}` → sealed engine hits `DEFERRED_BUDGET_EXCEEDED` (R-106 §7 honest degradation) · producer_bridge auto-banks `rri-f92d0840500b48b3` via A'''' adapter.
    - Step 3b `GET /response-required-items` → 1 item with actionable unblock text `[UNBLOCK action_class=host_reachability] raise CENSUS_SCHEDULER_JOB_MAX_SEC or shard the run for tenant AKKI-TEST · census_run_id=cr-23a57600a13e · engine detail: wall-clock exhausted before first byte`.
    - Step 4 `POST /resolve {resolved_state:RESOLVED_ACCEPTED}` → state `PENDING → RESOLVED_ACCEPTED` · resolver + resolution_text + resolved_at_utc banked.
    - Step 5 `GET /gpu-spend` → `status=CAPTURED, mode=real, hosts=[akki-vm,akki-vm-ii]` · 4×H200 live nvidia-smi telemetry (akki-vm 76.94W/76.98W + akki-vm-ii 76.54W/83.31W) · zero fabrication.
    - Step 6 registry read surface visible: `/api/registry/what_you_hold` (Canon §5 four-axis) + `/api/portal/census/assets` (6 sources) + `/api/portal/census/latest` (CENSUS-3 + 7 provenance pointers).
  - **PHASE 3 A'''-cont-B NEXT** (UI response-required-badge · real producer data from A''''-cont-A now available): `ResponseRequiredBadge.jsx` + `useResponseRequiredList.js` polling hook mounted alongside A'' `CensusAutonomyDrawer.jsx` in App.js twin (byte-identical /app/frontend/src ↔ pod_shell/frontend/src).
  - **PHASE 4** (banked order): entitlements backend → Connect/Commission wizards live → CP-SKILLS-LAYER → CP-DECK-ENGINE → CP-STREAMING-EXTRACTION → MOAC refusal ceremony → Watch trail → Model Registry honest-scoped.
  - **Order B → Order A audits** (resolve `-2` collection-drift forensic first).
  - **Remaining ops lanes** → **BUILD_JOURNAL + OWNER_RETURN_REPORT**.
  - R-101 preserved WHAT · R-102/R-106 productized-or-honest-gap **EXIT-EVIDENCED via LIVE CURL CHAIN**.
  - R-103 amendment applied · R-104 approving authorities named-but-unseated · R-105 partial-retirement design · R-106 CENSUS AUTONOMY SERVICE Commit-A + A' + A'' + A''' + A'''-cont-A + A'''' + **A''''-cont-A LANDED with LIVE EXIT PROOF**.
- **Ratchet floor: `6139`** (was 6129 pre-A''''-cont-A · +10 canonical measured) · sha256 `a082bf82aa41a4c18758ccdf49a1db4c19e898ab185ed7c4f39714f6c95c0bb7`.

## 2 · STANDING (R-102 + R-103 + R-104 + R-105 + R-106 + §6.8)

- R-102/R-106: productized-or-honest-gap · **EXIT-EVIDENCED via LIVE CURL CHAIN**. Every phase-3 surface curl-tested end-to-end in this-turn.
- R-103: single continuous run · no check-ins · additive-reversible forks + annotate.
- R-104: named-but-unseated approving authorities RMS + DIGICOW · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CENSUS AUTONOMY SERVICE Commit-A + A' + A'' + A''' + A'''-cont-A + A'''' + A''''-cont-A LANDED + E2E EXIT PROOF · A'''-cont-B queued.
- §6.8: plan is authority · report-and-continue.

## 3 · SIX STANDING BANS (UNCHANGED)

zero push/fetch · testing_agent BANNED · no refactor · no secret values · honest-gap never fake · no history rewrite.

## 4 · BOOT-ARTIFACT WARNING

CHUNK-1 is STALE bootstrap. Never re-run/re-clone/wipe. Probe list §5 authoritative.

## 5 · 8 DISK PROBES

```bash
ls -la /app/assessment_workspace/ && ls -la /app/assessment_workspace/STATE/
cat /app/assessment_workspace/STATE/RESUME.md 2>/dev/null || echo "not created"
head -40 /app/assessment_workspace/STATE/STANDING_ORDERS.md
git -C /app/assessment_workspace log --oneline -12
git -C /app/assessment_workspace/repos/Extraction-Akki log --oneline -8 && git -C /app/assessment_workspace/repos/Extraction-Akki branch
git -C /app log --oneline -10
python3 -c "import json; d=json.load(open('/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json')); print(d['counts_at_baseline'])"
tail -80 /app/assessment_workspace/STATE/DECISIONS.md && cat /app/assessment_workspace/STATE/NEXT.md
```

Expected: probe-7 `{'failed': 3, 'passed': 6139, ...}` · 4 census autonomy shape invariants + 7 A' router/state-reader + 8 A'' UI drawer + 6 A''' GPU-spend + 9 A'''-cont-A response-required queue + 11 A'''' data-source-adapter + **10 A''''-cont-A producer-bridge invariants** · 3 mirror-drift baselines RETAINED per R-86 anchor.

## 6 · POINTERS

- 9 additive modules under `services/census_autonomy/` — `__init__ + service_shape + scheduler_program + tenant_scope + engine + state_reader + gpu_spend_capture + response_required_queue + data_source_adapter + producer_bridge`.
- 3 additive routers at `routers/portal_census_autonomy.py` (A') + `routers/portal_census_response_required.py` (A'''-cont-A) + `routers/portal_census_autonomy_producer.py` (A''''-cont-A).
- 1 supervisord conf at `scripts/census_scheduler.supervisord.conf`.
- 1 additive React overlay drawer at `pod_shell/frontend/src/components/portal/CensusAutonomyDrawer.jsx` + `/app/frontend/src/` twin (A'').
- 1 additive React polling hook at `pod_shell/frontend/src/hooks/useCensusRunState.js` + `/app/frontend/src/` twin (A'').
- App.js additive mount md5 `250dc6e55e02cdce1ad53a50c5b12f0e` byte-identical across twins.
- server.py mirror pair `/app/backend/server.py ↔ pod_shell/backend/server.py` sha256 `6840d542bfce588865633048edc16edc90c8d2be2b8f0a3341413d40c4a17728` (post-A''''-cont-A additive mount).
- Test files: `test_cp_tenant_separation.py` (8·4j) · `test_r91_v8_substitution_retirement_guard.py` (4·4k) · `test_cp_census_autonomy_service_shape_gate.py` (4·P3-A) · `test_cp_census_autonomy_router_a_prime.py` (7·A') · `test_cp_census_autonomy_ui_a_double_prime.py` (8·A'') · `test_cp_census_autonomy_gpu_spend_a_triple_prime.py` (6·A''') · `test_cp_census_autonomy_response_required_a_triple_prime_cont_a.py` (9·A'''-cont-A) · `test_cp_census_autonomy_data_source_adapter_a_quad_prime.py` (11·A'''') · **`test_cp_census_autonomy_producer_bridge_a_quad_prime_cont_a.py` (10·A''''-cont-A)**.
- Drill receipts: `_4j/` + `_4k/` + `_cp_census_autonomy/` + `_cp_census_autonomy_a_prime/` + `_cp_census_autonomy_a_double_prime/` + `_cp_census_autonomy_a_triple_prime/` + `_cp_census_autonomy_a_triple_prime_cont_a/` + `_cp_census_autonomy_a_quad_prime/` + **`_cp_census_autonomy_a_quad_prime_cont_a/`** (with `e2e_exit_proof/` subdir carrying 11 raw curl receipts).
- Custody: `custody/credentials/rms_connection_creds_v2.xlsx` + v1.

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · APPROVING AUTHORITY · RMS** · named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- **DQ-20** — **P1 · APPROVING AUTHORITY · DIGICOW** · named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- **DQ-GPU-SSH-KEYS** — SELF-RESOLVED 2026-09-22T19:00Z.
- **-2 collection-drift** — P1 forensic queued behind Order B audit.
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k; mirror-drift leg queued behind CP-APP-JS-UNIFY.

## 8 · FOUR BANKED LESSONS (from A''' + A'''-cont-A + A'''' + A''''-cont-A)

1. **YAML plain-scalar hazard**: ORCH_BOOT.md stanza entries must use dashes for `route - GET` patterns (never embedded colons in plain scalars).
2. **Server.py mirror-edit rule**: any additive mount in `server.py` must be mirrored byte-identically across the runtime mirror pair only. **CRITICAL CLARIFICATION (from A''''-cont-A)**: the mirror pair is `/app/backend/server.py ↔ pod_shell/backend/server.py` — **NOT** `spine ↔ pod_shell`. Spine `backend/server.py` has its own additive block for spine-side tests but is not part of the runtime byte-identity mirror; pod_shell is a thin bridge assembler by design (CP-PROD-DEPLOY-SELF-CONTAINMENT precedent).
3. **Canon-9 §3 negative-scan literal-substring hazard (from A'''')**: modules outside the sealed writer cannot carry the sealed attr-name as a literal substring anywhere in their file source. Cure: compose the attr name via string concatenation at import time.
4. **Producer-bridge additive discipline (from A''''-cont-A)**: to add a producer path over a sealed engine without §3.8 violation, use a NEW module that reads (never mutates) the sealed engine's public constants and banks via the sealed downstream carrier's public callable only. AST-level scan for banned internal imports enforced.
