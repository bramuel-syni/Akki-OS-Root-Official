# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-09-22T18:50:00Z (PHASE 3 continuation A''' · CP-CENSUS-AUTONOMY-GPU-SPEND **Commit-A + /app companion Commit-A LANDED** · ratchet 6103 → 6109 · additive gpu_spend_capture module (thin adapter over sealed ssh_seam) with mock-mode HONEST_GAP + real-mode STOP-condition-2 HONEST_GAP semantics; NO fabricated GPU numbers per owner CENSUS_PRODUCTIZATION §44).

---

## 1 · POSITION

- **Phase:** PHASE 3 · **CENSUS AUTONOMY SERVICE** OPEN · Commit-A + A' + A'' + **A''' LANDED** · continuation **A'''-cont (response-required queue + routers + UI badge)** OR **A'''' (data_source adapter fold-in)** NEXT.
- **Turn queue:**
  - 4a-4j ✅ SEALED · 4k ✅ SEALED (ratchet 6080→6086).
  - PHASE 3 Commit-A ✅ SEALED · ratchet 6086→6090.
  - PHASE 3 A' ✅ SEALED · ratchet 6090→6097.
  - PHASE 3 A'' ✅ SEALED · code `527d09bf1948a6b32068769d5dcde6c9abcc192c` · /app `dd8ba7303` · state B `0e976251` · state C `6d654a66` · /app C `8dae79d6b` · ratchet 6097→6103.
  - **PHASE 3 A''' ✅ SEALED THIS-TURN** at code `c3807d7c72c9599db4e692ee88e44c8378ee1873` · /app companion `615ac44ac` · state B `<PENDING-P3-ATP-CB>` · state C `<PENDING-P3-ATP-CC>` · /app C `<PENDING-P3-ATP-CC-APP>` (CP-CENSUS-AUTONOMY-GPU-SPEND · Commit-A · 6 new RED-first invariants at `tests/invariants/test_cp_census_autonomy_gpu_spend_a_triple_prime.py` · NEW additive `services/census_autonomy/gpu_spend_capture.py` (thin adapter over sealed `services.training_runner.ssh_seam`) · GPU_SPEND_CAPTURE_STATE_CODES Final tuple ('CAPTURED','HONEST_GAP_UNREACHABLE','HONEST_GAP_MOCK_MODE') closed vocab · mock-mode returns HONEST_GAP_MOCK_MODE with no fabricated numeric fields · real-mode + unreachable returns HONEST_GAP_UNREACHABLE per STOP condition #2 · owner directive 'NO GPU-spend fabrication' enforced by 6-marker source-level ban · ratchet 6103→6109 +6 measured · double-green stripped-sha256 `bd2010df9cd70e7294cf92a04eaf2ae7a2a6ee08de9a2209ba813b7af2e4a8ac` IDENTICAL · 6112 passed / 1 skipped / 0 failed each · vendored twin same-seal sync file_count 1022→1023 structural_sha256 88dad1bd... · same-slice cure DECISIONS.md pointer restored to last-5-lines window).
  - **PHASE 3 A'''-cont NEXT** (RESPONSE-REQUIRED QUEUE + routers + UI response-required-badge): `services/census_autonomy/response_required_queue.py` filesystem-cursor-backed · `POST /api/portal/census/response-required-items/{item_id}/resolve` + `GET /api/portal/census/response-required-items` (JWT-gated) · NEW `ResponseRequiredBadge.jsx` React overlay component mounted alongside `CensusAutonomyDrawer.jsx`.
  - **A'''' after A'''-cont**: `data_source` adapter fold-in (Order B MySQL RDS · Order A NAS CIFS · OBS audio) + sealed `mtafiti.asset_registry_writer` wiring (Canon-9 §3 single-writer).
  - PHASE 4 (a-h) → Order B → Order A → BUILD_JOURNAL + OWNER_RETURN_REPORT.
  - R-101 preserved WHAT: mirror at 4h · v8-substitution retirement at 4k · 3 mirror-drift baselines transiently GREEN post-A'' but list retained; explicit retirement deferred to future CP-APP-JS-UNIFY.
  - R-102 MASTER DIRECTIVE: **productized-or-honest-gap SATISFIED** (system census + on-demand JWT + UI overlay drawer with REAL state polling + GPU-spend capture with mock-mode HONEST_GAP + real-mode STOP-condition-2 all productized).
  - R-103 amendment: no check-ins · autonomous forks with annotation.
  - R-104 approving authorities: named-but-unseated (RMS + DIGICOW · custody-material via §4.1 §F · excluded from `CENSUS_ADMITTED_TENANT_IDS`).
  - R-105 partial-retirement design: executed at 4k.
  - **R-106 CENSUS AUTONOMY SERVICE**: Commit-A + A' + A'' + A''' LANDED · A'''-cont/A'''' authored NEXT.
  - §6.8 report-and-continue.
- **Ratchet floor: `6109`** (was 6103 pre-A''' · +6 canonical measured) · sha256 `b4237e36dc075e839ecad8d31e9c294692ce1a4fba549fcb4a6cc66d8f7e1da3`.

## 2 · STANDING (R-102 + R-103 + R-104 + R-105 + R-106 + §6.8)

- R-102: productized-or-honest-gap · **SATISFIED** for system census + on-demand JWT + UI drawer + GPU-spend capture (mock HONEST_GAP + real STOP#2 HONEST_GAP).
- R-103: single continuous run · no check-ins · additive-reversible forks + annotate.
- R-104: named-but-unseated approving authorities RMS + DIGICOW · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- R-105: partial-retirement design executed at 4k.
- R-106: PHASE 3 CENSUS AUTONOMY SERVICE Commit-A + A' + A'' + A''' LANDED · A'''-cont/A'''' queued.
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

Expected: probe-7 `{'failed': 3, 'passed': 6109, ...}` · 4 census autonomy shape invariants (P3-CA) + 7 A' router/state-reader invariants + 8 A'' UI drawer invariants + **6 A''' GPU-spend invariants** · 3 mirror-drift baselines RETAINED per R-86 anchor.

## 6 · POINTERS

- 37 React OS surfaces at `/app/frontend/src/pages/os/`.
- 6 backend modules under `repos/Extraction-Akki/backend/services/tenant_separation/` (4j).
- 2 modules under `services/baseline_retirement_supersede/` (4k).
- 6 modules under `services/census_autonomy/` (PHASE 3 Commit-A + A' · __init__ + service_shape + scheduler_program + tenant_scope + engine + state_reader).
- **7th module: `services/census_autonomy/gpu_spend_capture.py` (PHASE 3 A''' · thin adapter over sealed ssh_seam).**
- 1 supervisord conf at `scripts/census_scheduler.supervisord.conf`.
- 1 additive router at `routers/portal_census_autonomy.py` (A').
- 1 additive React overlay drawer at `pod_shell/frontend/src/components/portal/CensusAutonomyDrawer.jsx` + `/app/frontend/src/` twin (A'').
- 1 additive React polling hook at `pod_shell/frontend/src/hooks/useCensusRunState.js` + `/app/frontend/src/` twin (A'').
- App.js additive mount md5 `250dc6e55e02cdce1ad53a50c5b12f0e` byte-identical across twins.
- Test files: `test_cp_tenant_separation.py` (8·4j) · `test_r91_v8_substitution_retirement_guard.py` (4·4k) · `test_cp_census_autonomy_service_shape_gate.py` (4·P3-A) · `test_cp_census_autonomy_router_a_prime.py` (7·A') · `test_cp_census_autonomy_ui_a_double_prime.py` (8·A'') · **`test_cp_census_autonomy_gpu_spend_a_triple_prime.py` (6·A''')**.
- Drill receipts: `_4j/` + `_4k/` + `_cp_census_autonomy/` + `_cp_census_autonomy_a_prime/` + `_cp_census_autonomy_a_double_prime/` + **`_cp_census_autonomy_a_triple_prime/`**.
- Custody: `custody/credentials/rms_connection_creds_v2.xlsx` + v1.

## 7 · OWNER-EXCLUSIVE OPEN

- **DQ-05** — Huawei OBS IAM GetObject grant.
- **DQ-06** — HF-HOLD SEC-2026-09-12-01.
- **DQ-13** — EMERGENT_LLM_KEY + JWT_SECRET rotation.
- **DQ-17** — **P0 · weego MySQL password rotation** post-INCIDENT-2026-09-22-01.
- **DQ-19** — **P1 · APPROVING AUTHORITY · RMS** · named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- **DQ-20** — **P1 · APPROVING AUTHORITY · DIGICOW** · named-but-unseated · excluded from `CENSUS_ADMITTED_TENANT_IDS`.
- **DQ-GPU-SSH-KEYS** — **SELF-RESOLVED 2026-09-22T19:00Z** (was mis-classified as owner-ask in the A''' seal report; owner correction 2026-09-22T~18:55Z clarified custody key already banked at `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu` fingerprint `SHA256:M3Dre1A1I1ZQFo0FDsfzbWPwn5z+oxmZ02y1eZwFy1A` matching `phase0/keypair_hardening_receipts/20260828T162217Z_step1_keygen.json`; reverified this-turn: both hosts pubkey-authed + 4× H200 live nvidia-smi captured; backend/.env flipped `GPU_CONNECT_MODE=real` + slug env vars set additively; end-to-end `capture_gpu_spend()` returned `status=CAPTURED` for both hosts with live redacted stdout; sealed ssh_seam banked 2 `census_autonomy_gpu_spend_capture` receipts at `phase0/gpu_receipts/`; probe evidence banked at `phase0/gpu_probes/20260922T190000Z_GPU_LANE_REVERIFY_A_TRIPLE_PRIME.json`).
- DQ-18 · CP-R91-RETIRE-SUPERSEDE · partially CLOSED at 4k (v8-substitution leg); mirror-drift leg queued behind CP-APP-JS-UNIFY.
