# NEXT.md - Exact next actions

**Last updated:** 2026-08-25 · **W5 CLOSED** on programme/track-a HEAD `39386ac` · LLM chokepoint live · Solva reasoning live · Chat live · Reasoning Shield live · Connect-LLM verify backend live · **194/194 gating tests green** · **zero regressions** · **live E2E receipts on record**: `rcp-17085737b228` (chat) + `run-5c9cdc19d3da` (thinklab three-stage). Close report at `notes/w5_close_report.md`. **HOLD for owner "W6 go"** per owner's standing instruction.

## Cycle status (2026-08-25 · W5 close)

- W1..W5 · **CLOSED**.
- W6 · Cost Ledger surface · retention enforcement · Grey Mirror groundwork — **NEXT** on owner "W6 go".
- W7..W9 · unchanged per notes/status_and_wave_plan.md.

## Deferred to owner ruling (all named in notes/w5_close_report.md §10)

1. W6 GO signal.
2. Sizing verdict on L-class overrun (~2870 LOC vs ≤2500). Options: reclassify · narrow next scope · new L-extended tier.
3. `FL-P4-W4-01` · reconcile `northena_ledger_row` vs `northena_ledger_v1` snapshot mismatch (predates W5).
4. CA1-010 session-scoped lowered-standard bypass surface (test hook exists).
5. ConnectDrawerChat LLM chip UI polish (backend live; surface deferred).
6. Solva stages 4/5/6 (triangulation / tension / probability_weighting) — Grey Mirror groundwork W6+.

## Verification path for orchestrator (independent audit) — W5 close

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a | head -6
# 39386ac W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension
# ba14077 W5 CP4 backend · Chat · Reasoning Shield filter · Connect-LLM verify + custody
# 22b323d W5 CP3 · Solva reasoning + ThinkLab wire-through · 173/173 green
# feeb786 W5 CP2b · boundary-side metering via tiktoken (emergentintegrations exposes no usage)
# a5be529 W5 CP2 · LLM chokepoint · purpose gate · Emergent-universal registration · AST tightening
# a71ea67 W4 CLOSED · ThinkLab surface live at /thinklab + full W4 cohort green (Doc 05 · M class)

python3 -m pytest backend/tests/invariants/test_llm_*.py \
    backend/tests/invariants/test_solva_*.py \
    backend/tests/invariants/test_thinklab_reasoning_wire.py \
    backend/tests/invariants/test_w5_cp4_backend_endpoints.py \
    backend/tests/invariants/test_registry_facts_emergent_universal_listed.py -v
# Expect: 42 W5 net-new tests green.

curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
    http://127.0.0.1:8001/api/chat/ask \
    -H "Content-Type: application/json" \
    -d '{"question":"In one sentence, what is a governed chokepoint?"}'
# Expect: {answer:"…", receipt_id:"rcp-…", model_id:"gpt-5-mini", provider:"emergent",
#          tokens_in:>0, tokens_out:>0, latency_ms:>0, refused:false, refusal_reason:""}
```

## Blocked (awaiting from owner)

- None new.

## No push, ever

Owner Clarification 1 (2026-08-14). Local commits are the record.

## Honest LOC drift note

W4 was scoped M (~600 LOC estimated). Delivered at ~2020 LOC (donor Northena adaptation is inherently 500+ LOC; ThinkLab v7 fabric fidelity ~500 LOC; deep tests-first cohort 457 LOC). Above M-class ceiling. Reported to owner; hold for classification ruling or narrowing envelope guidance for future M waves.

## Post-W4 report to owner

Deliver: 20 register rows targeted; 6 fully DONE + 2 PARTIAL + 12 deferred to W5+ · SIX mechanism reuse pulls cited per file · three screenshots (landing / mode entry / admit walk) · LOC ~2020 · SHAs (`7e6bbc4` · `7bea87d` · `a71ea67`) · dashboard delta: Doc 05 5% → 30%; composite headline 43% → 44%.

## Cycle status (2026-08-14 · Owner Simplification response)

- **Simplification cycle CLOSED.** Connect UX collapses to ONE panel. Step grammar survives only as post-submit progress view (the handshake walk from the seven-stage pipeline, which itself is UNCHANGED).
- **Deterministic local parsing live.** `POST /api/connect/parse-paste` — pattern-only, no LLM/HTTP/subprocess. Password never returned in response body; `password_captured` boolean signal only.
- **Client-side password custody honoured.** Browser keeps the raw paste in its own textarea memory and submits the full credential set once to `/api/connect/gpu` (existing seven-stage pipeline unchanged). No server-side secret state between the parse and connect requests.
- **Fidelity ledger:** FL-P2-19 CLOSED (synisense-reading recorded); FL-P2-20 CLOSED (single-panel collapse); FL-P2-21 CLOSED (no-LLM-transit invariant added as gating).
- **LOC delta:** `ConnectWizard.jsx` 623 → 451 (−172 lines, −28%). New backend: 266 lines (parser + router + init). New backend tests: 321 lines. Frontend tests net +52 lines.
- **143/143 gating tests green.** 108 backend python + 12 frontend allowlist + 23 frontend rehome/single-panel. Zero regressions.
- **Commit SHAs on programme/track-a (4 new atop `f83b509`):**
  - `1f3d3bd` Phase 1 tests-first · deterministic paste parser + no-LLM-transit invariants
  - `ef9e185` Phase 1 implementation · deterministic paste parser + router mounted
  - `5ce8647` Phase 1 tests-first · single-panel Connect surface invariants
  - `c490ce9` Phase 1 implementation · single paste-and-connect panel

## Two-sentence access-mechanism proposal (still awaiting owner ratification)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` - every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ratify the two-sentence access proposal** (still standing).
- **FL-P2-09 disposition** - pod egress-IP rotation. Rotated AGAIN this cycle: STATE was `104.198.214.223` last cycle, now `35.225.230.28` this cycle. `34.16.56.64` stays in `SPINE_ALLOWED_IPS` unchanged per owner directive.
- **Vendor-side VM provisioning using the provisioning card** (unchanged):
  - Paste the estate public key `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki` into the VM's SSH Public Key field at creation (AISCA guide Fig 10).
  - Add TWO /32 rows to the VM's Security Group SSH rules (AISCA guide Fig 11): the owner's own operator /32 AND the pod egress /32 (currently `35.225.230.28/32`, subject to rotation).
- **Then paste the AISCA Output panel into the single Connect panel.** The parser reads it deterministically; the confirmation view masks the password as `•••• captured`; owner taps Connect; the unchanged seven-stage pipeline fires; with the estate key already installed, hardening shortens to verify-key-only → disable password auth → probe dead.

## Cold-reader-executable next actions

### 1. Deliver the Owner Simplification cycle report (this reply)

Test delta + right-reason receipts + green receipts + no-LLM-transit hard-rule proof + 4 Playwright screenshots (single panel / paste-parsed confirm / with provisioning card / handshake walk result) + LOC delta + commit SHAs.

### 2. On owner ratification of allowlist entry / vendor-side provisioning

- Update `SPINE_ALLOWED_IPS` in `/app/backend/.env` (add owner's client `/32`). Record allowlist change as a ledger row.
- Owner pastes AISCA Output panel into single Connect panel; deterministic parse; confirm; connect; seven-stage pipeline fires. Watch for green/failed/held per brief §5 paragraphs 6-7.

### 3. Post-Phase-0 (next cycle)

- **A4 increment (Registry honest-state instrumentation):** wire the COMPUTE CONNECTED tab's after-state to the real commissioning record on disk (present a "Just connected" pill + meta line + link to the record). Add DATA CONNECTED / LLMS & TRAINED MODELS state transitions when their waves land.
- **Wire-up non-compute path to per-wave connectors** as they land (data-source in Phase 2 admit-slice; LLM/trained-model in later waves). The single-panel + intent-record grammar becomes real routing when the wave connectors are ready.

### 4. Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
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
    backend/tests/invariants/test_ip_allowlist_middleware.py \
    backend/tests/invariants/test_estate_keys_and_connect_estate.py \
    backend/tests/invariants/test_credentials_paste_parser.py -v
# Expect: 108 passed at HEAD c490ce9.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 23 passed.

# Live probe: no-LLM-transit proof (sentinel absent from response)
PW="INDEPENDENT_AUDIT_SENTINEL_$$"
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     -H "Content-Type: application/json" \
     -d "{\"paste\":\"Host Name: h\\nPassword: ${PW}\\nUsername: u\\nPublic IP: 1.2.3.4\",\"hint_kind\":\"compute\"}" \
     http://127.0.0.1:8001/api/connect/parse-paste | grep -c "${PW}"
# Expect: 0 (password never in response body).

# Provisioning card live probe
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     "http://127.0.0.1:8001/api/connect/estate-facts" | python3 -m json.tool
```

### 5. No push, ever

Owner Clarification 1 (2026-08-14). Assessment repo and Extraction-Akki both stay local.
