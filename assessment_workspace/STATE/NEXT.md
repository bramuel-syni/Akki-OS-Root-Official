# NEXT.md — Exact next actions

**Last updated:** 2026-08-14 · Owner stop-order cycle CLOSED · minted-credential pattern retired · source-IP allowlist live on both backend and frontend · Connect GPU form re-homed under Admin surface · 99/99 gating tests green on `programme/track-a` HEAD `acc25a8` · awaiting owner's ruling on FL-P2-09 (pod egress rotation) and confirmation of the two-sentence access-mechanism proposal.

## Cycle status (2026-08-14 · Owner stop-order response cycle)

- **Token revoked (dead across three checks).** `/app/backend/.owner_credentials` deleted; `spine_auth.py` deleted; `/app/memory/test_credentials.md` scrubbed. Compromised token → HTTP 403 (was HTTP 422 = accepted before). No leak sites in `/app`, spine repo, logs, STATE, notes, phase0.
- **Source-IP allowlist middleware live.** FastAPI middleware at `services/ip_allowlist/middleware.py` (16 gating tests green). CRA dev-server middleware at `plugins/ip-allowlist/{check.js, middleware.js}` (12 gating tests green). Config in `/app/backend/.env`: `SPINE_ALLOWED_IPS=34.16.56.64`, `SPINE_TRUSTED_PROXY_HOPS=2`. Refusal grammar: HTTP 403 `text/plain` `"This surface answers allowlisted addresses only."` on EVERY route family (proven live).
- **Connect GPU form re-homed under Admin.** `/register/connect/gpu` retired at edge (HTTP 404 `text/plain` `"This route has been retired."`). Root `/` → `<AdminSurface />` → tile grid (TRUST CENTER + REGISTRY) → Connect tile → GPU form. 9/9 re-home gating tests green.
- **programme/track-a HEAD `acc25a8`** — 4 new sequential tests-first + implementation commits atop `98fcd75`.
- **99/99 total gating tests green** (78 backend python + 21 frontend node --test).
- **Fidelity ledger updated:** FL-P2-08 CLOSED (minted-credential retirement); FL-P2-09 OPEN (pod egress-IP rotation surprise); FL-P2-10 CLOSED (empirical header-topology trust boundary).
- **Assessment-repo master:** pending this cycle's follow-up commit (STATE + fidelity ledger + phase0 receipts + DECISIONS appendix).

## Two-sentence access-mechanism proposal (for owner reply)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` — every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ruling on FL-P2-09 (pod egress-IP rotation).** Empirical: pod egress is `34.170.12.145` (verified across 4 services this cycle), not the `34.16.56.64` pinned in STATE. Owner's directive `SPINE_ALLOWED_IPS=34.16.56.64` implemented as ordered; pod is NOT self-allowlisted. Owner disposition needed: (a) confirm `34.16.56.64` is the intended owner client `/32` (not pod egress) and stands as is; OR (b) direct a different value.
- **Confirmation of the two-sentence access-mechanism proposal above.** Owner's directive was: propose exactly one mechanism, exactly two sentences, no alternatives. This proposal is drafted; awaits acceptance.
- **Real AISCA VM credentials entered via the WS-BUILD-CONNECT-GPU surface.** Owner action; blocked on owner's client-IP being on the allowlist (see above) since the surface will otherwise refuse the owner too.
- **Reference screenshot file** — transcription-grade holds.

## Cold-reader-executable next actions

### 1. Deliver stop-order completion report to owner (this reply)

Security confirmations (token dead ×3 checks + lockdown live) FIRST · re-home + middleware evidence (live-proven refuse branch + test-proven allow branch + unit-test spoof-resistance) · test roll-up (99/99) · commit SHAs · two-sentence access-mechanism proposal.

### 2. On owner-confirmed allowlist entry

Update `SPINE_ALLOWED_IPS` in `/app/backend/.env` to add owner's client `/32` (leaving `34.16.56.64` per current directive unless owner rules otherwise). Restart backend + frontend. Live-prove allowed-branch from owner side (owner curls `/` from their client IP → 200; verify from backend log). Record allowlist change as a ledger row.

### 3. On owner credential entry via the re-homed form

The seven-stage pipeline fires automatically. Watch for green/failed/held branches exactly as banked before this cycle (four-questions render, commissioning record write, PINS `checkpoint_14d_utc` pin).

### 4. Verification path for orchestrator (independent audit)

```bash
# Repo audit
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -E "File citations|Canon citations|failed"
python3 tools/completeness_audit.py 2>&1 | tail -3

# Track-a audit (99/99 total gating)
cd repos/Extraction-Akki
git log --oneline programme/track-a
python3 -m pytest \
    backend/tests/invariants/test_actor_declaration_v0_contract_frozen.py \
    backend/tests/invariants/test_record_matrix_thin_kernel.py \
    backend/tests/invariants/test_task_identity_thin_kernel.py \
    backend/tests/invariants/test_parity_seat_extends_thin_kernel.py \
    backend/tests/invariants/test_admit_refuses_undeclared_actor.py \
    backend/tests/invariants/test_compute_seam_no_unledgered_exec.py \
    backend/tests/invariants/test_compute_seam_artifact_hash_verified.py \
    backend/tests/invariants/test_hardening_orchestrator.py \
    backend/tests/invariants/test_connect_gpu_pipeline.py \
    backend/tests/invariants/test_connect_gpu_scope_S_or_M.py \
    backend/tests/invariants/test_connect_gpu_acceptance_wired.py \
    backend/tests/invariants/test_ip_allowlist_middleware.py -v
# Expect: 78 passed at HEAD acc25a8.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 9 passed.

# Surface audit (refuse branch from pod egress)
curl -o /dev/null -w "HTTP %{http_code}\n" https://akki-reuse-assess.preview.emergentagent.com/
curl -o /dev/null -w "HTTP %{http_code}\n" https://akki-reuse-assess.preview.emergentagent.com/api/deliverables
curl -o /dev/null -w "HTTP %{http_code}\n" https://akki-reuse-assess.preview.emergentagent.com/register/connect/gpu
# Expect: 403 / 403 / 403 with text/plain body "This surface answers allowlisted addresses only."
```

### 5. No push, ever

Owner Clarification 1 unchanged. Local commits on both `programme/track-a` (code, tests, pod-shell mirror) AND assessment-repo `master` (STATE, fidelity ledger, phase0 receipts, DECISIONS appendix) are the record.
