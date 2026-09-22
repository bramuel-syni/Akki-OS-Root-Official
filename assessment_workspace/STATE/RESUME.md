# STATE/RESUME.md — anti-compaction re-anchor (rewritten at EVERY seal)

**Last rewrite:** 2026-09-22T19:15:00Z (PHASE 3 continuation A'''-cont-A · CP-CENSUS-AUTONOMY-RESPONSE-REQUIRED-QUEUE **Commit-A + /app companion Commit-A LANDED** · ratchet 6109 → 6118 · additive filesystem-cursor-backed queue module + 2 JWT-gated routers + Ship-Manifest DoD parity restored; owner directive HONORED verbatim "advertised control with no endpoint is a fake state by another name" — the backing queue + endpoints now exist end-to-end).

---

## 1 · POSITION

- **Phase:** PHASE 3 · **CENSUS AUTONOMY SERVICE** OPEN · Commit-A + A' + A'' + A''' + **A'''-cont-A LANDED** · continuation **A'''-cont-B (UI response-required-badge)** OR **A'''' (data_source adapter fold-in)** NEXT.
- **Turn queue:**
  - 4a-4j ✅ SEALED · 4k ✅ SEALED (ratchet 6080→6086).
  - PHASE 3 Commit-A ✅ SEALED · ratchet 6086→6090.
  - PHASE 3 A' ✅ SEALED · ratchet 6090→6097.
  - PHASE 3 A'' ✅ SEALED · code `527d09bf` · ratchet 6097→6103.
  - PHASE 3 A''' ✅ SEALED · code `c3807d7` · ratchet 6103→6109.
  - **DQ-GPU-SSH-KEYS SELF-RESOLVED** at state mini-Commit-B `f4399ea0` / /app mirror `6cb888c1c` (custody key reverified · both hosts pubkey-authed · 4× H200 live nvidia-smi captured · backend/.env flipped GPU_CONNECT_MODE=real · gpu_spend_capture returning `status=CAPTURED` end-to-end · probe receipt banked).
  - **PHASE 3 A'''-cont-A ✅ SEALED THIS-TURN** at code `a0dcc0626fa80ec357dd8a56adc7fc2a21104669` · /app companion `739ac5e4a` · state B `<PENDING-P3-CA-TPRIME-CONT-A-CB>` · state C `<PENDING-P3-CA-TPRIME-CONT-A-CC>` · /app C `<PENDING-P3-CA-TPRIME-CONT-A-CC-APP>` (CP-CENSUS-AUTONOMY-RESPONSE-REQUIRED-QUEUE · 9 new RED-first invariants at `tests/invariants/test_cp_census_autonomy_response_required_a_triple_prime_cont_a.py` · NEW additive `services/census_autonomy/response_required_queue.py` (filesystem-cursor-backed queue rooted at `CENSUS_STATE_DIR/response_required/` · 3 public callables bank/list/resolve · `RESPONSE_REQUIRED_ITEM_STATE_CODES` Final closed vocab `('PENDING','RESOLVED_ACCEPTED','RESOLVED_REJECTED')` · atomic write-then-rename FS pattern · ItemNotFound + InvalidResolvedState exception classes · queue is ORIGIN-EMPTY at mount time · never fabricates) + NEW additive `routers/portal_census_response_required.py` (2 JWT-gated routes at `LIST_ROUTE_PATH` and `RESOLVE_ROUTE_PATH_TEMPLATE` Final constants · `require_identity_or_deny` gate identical to A' pattern) + additive `server.py` mount in BOTH spine + pod_shell + runtime (byte-identical between pod_shell/backend/server.py and /app/backend/server.py per Ship-Manifest DoD) · ratchet 6109→6118 +9 measured · double-green stripped-sha256 `31ba5011dcff95542b4844c73b9aaa5662dba8579ae8bb7ac7a012b02f386805` IDENTICAL sweep_A/B both 6121 passed / 1 skipped / 0 failed · vendored twin same-seal sync +2 files file_count 1023→1025 structural_sha256 `458c224f9583dc1970d7933bb619e39c01e1461d0e15fcc1fba1c047cc5f113f` · same-slice cure Ship-Manifest DoD parity restored).
  - **PHASE 3 A'''-cont-B NEXT** (UI response-required-badge): `ResponseRequiredBadge.jsx` React overlay component + `useResponseRequiredList.js` polling hook mounted alongside A'' `CensusAutonomyDrawer.jsx` in App.js twin (byte-identical /app/frontend/src ↔ pod_shell/frontend/src).
  - **A'''' after A'''-cont-B**: `data_source` adapter fold-in (Order B MySQL RDS · Order A NAS CIFS · OBS audio) + sealed `mtafiti.asset_registry_writer` wiring (Canon-9 §3 single-writer).
  - PHASE 4 (a-h) → Order B → Order A → BUILD_JOURNAL + OWNER_RETURN_REPORT.
  - R-101 preserved WHAT · R-102 productized-or-honest-gap SATISFIED (system census + on-demand JWT + UI drawer + GPU-spend + response-required queue+endpoints).
  - R-103 amendment applied · R-104 approving authorities named-but-unseated · R-105 partial-retirement design · R-106 CENSUS AUTONOMY SERVICE Commit-A + A' + A'' + A''' + A'''-cont-A LANDED.
- **Ratchet floor: `6118`** (was 6109 pre-A'''-cont-A · +9 canonical measured) · sha256 `88ce4652d26e4adf5aaae225d0092d7bed55c3289dcea68a6e8138afbd7a58eb`.

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
