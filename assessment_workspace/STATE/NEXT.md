# NEXT.md - Exact next actions

**Last updated:** 2026-08-25 · **W6 OPEN · openers done** · programme/track-a HEAD `f647051` (W6 opener #2 · FL-P4-W4-01 reconciled) · master HEAD has W6 opener #1 (re-baselined wave table + calibration factor 1.60×). W5 CLOSED at Extraction-Akki@`39386ac`.

## Cycle status (2026-08-25 · W6 openers CLOSED · W6 scope opening)

- **W1..W5 · CLOSED**. 195/195 gating tests green across the wave-open cohort (194 W5-close + 1 FL-P4-W4-01 reconciled).
- **W6 opener #1 · re-baseline · DONE**. Calibration factor 1.60× published in notes/status_and_wave_plan.md §7. W6 stop-and-report line: **2880 LOC**.
- **W6 opener #2 · FL-P4-W4-01 · DONE**. Root-cause named (W4 close missed the snapshot bump); reconciliation via snapshot bump ratified by this owner ruling; fidelity ledger row closed at phase0/fidelity_ledger/FL-P4-W4-01.json.
- **W6 SCOPE opening · IN PROGRESS**:
  - CP1 · rulings + brief (this update) — pending.
  - CP2 · rates register (owner-supplied or honestly absent) + Cost Ledger backend + tests — pending.
  - CP3 · retention enforcement + tests — pending.
  - CP4 · Grey Mirror groundwork + Solva stages 4-6 mechanism-side — pending.
  - CP5 · W5 deferrals folded in (LLM chip UI + Data Suite + CA1-010) — pending.
  - CP6 · wave close (dashboard + STATE + screenshots) — pending.

## W6 openers summary

### Opener #1 · Re-baseline (in notes/status_and_wave_plan.md §7)
- W1: 1006 LOC actual vs 800 est → 1.26×.
- W2: 1666 vs 150 → 11.11× — **class misclassification** (S→M-effective).
- W3: 2519 vs 2000 → 1.26×.
- W4: 2566 vs 600 → 4.28× — **class misclassification** (M→L-effective).
- W5: 4026 vs 2500 → 1.61×.
- **Calibration factor: 1.60× (median), 1.95× (weighted mean)** — using MEDIAN as the go-forward multiplier (owner ruling naming).
- W6-W9 re-baselined: **W6 ~2880 LOC · W7 ~3520 LOC · W8 ~5600 LOC · W9 ~6400 LOC · total ~18400 LOC**.
- Remaining build effort is 60% higher than pre-calibration; W1-W5 landed 95% higher than pre-calibration.
- Three ruling paths named for owner (accept re-baseline / narrow scope / add L-extended tier); default: accept.

### Opener #2 · FL-P4-W4-01 closed
- Root-cause: W4 extended `LedgerRow` (added `thinklab_objective`, `row_id`, description tweaks, `additionalProperties: True` on stamp_audit, dropped `at` from required) but skipped the snapshot bump — silently failing test at HEAD `a71ea67`.
- Reconciliation: bump `northena_ledger_row.contract_snapshot.json` to match current W4-ratified code shape. Owner Ruling W6 GO opener #2 IS the explicit ratification moment.
- Right-reason failure: phase0/drill_receipts/20260825T204000Z_w6_opener2_FL-P4-W4-01_right_reason.log.
- Green after fix: 195/195 in phase0/drill_receipts/20260825T205000Z_w6_opener2_FL-P4-W4-01_green.log.
- Fidelity ledger row banked at phase0/fidelity_ledger/FL-P4-W4-01.json — CLOSED.
- Process finding: W4 close cohort had a scoping gap (missed a contract snapshot test). Note in the ledger row; future wave-close cohorts assemble by grep for `test_*_frozen*.py` + `test_*_contract*.py`.

## W6 scope plan (post-openers)

Grounded in the register rows FIRST (owner ruling). Six checkpoints:

**CP2 · Cost Ledger (CA1-008 + Docs 11/12)**:
- Read the CA1-008 lever sequence from the addendum / Doc 11 / Doc 12 verbatim (BEFORE opening code — quote it in the CP2 brief).
- Rates register: `services/cost_ledger/rates.py` reads from `phase0/rates_register/*.json` — OWNER-SUPPLIED FACTS or honestly absent. If no rate on record for a model or GPU-hour, ledger shows quantities with the W2 honest-gap sentence.
- Ledger backend: `services/cost_ledger/ledger.py` consumes W5 metering receipts (all `solva_* / chat_* / thinklab_* / llm_*` kinds) + W2 reflection quotas + seam GPU usage into ledger entries.
- Surface: `pod_shell/frontend/src/components/CostLedger.jsx` per v7 oracle `COMPUTE_CHARTS` fabric.

**CP3 · Retention enforcement (CA1-N1)**:
- Quote the register's letter for retention on each record class we hold: receipts / ledger rows / chat turns / admits / seam runs.
- Append-only classes NEVER get delete verb — retention on those = marked-expired + excluded-from-render. If the register says otherwise, quote it and STOP.
- Enforcement mechanism per the letter (expiry marking / governed deletion path).
- Surface: retention state row on records + attestation record.

**CP4 · Grey Mirror groundwork + Solva stages 4-6**:
- Solva stages 4 (triangulation) · 5 (tension_detection) · 6 (probability_weighting) ADAPTED from Executive-Final donor · mechanism-side only.
- Grey Mirror overview surface only if oracle has parts that render honestly from what exists (else deferred to W9 with Watch).

**CP5 · W5 deferrals folded in**:
- ConnectDrawerChat LLM chip UI polish (backend live).
- Data Suite surface v7-exact (data facts from real connected sources · structure-only posture).
- CA1-010 session-scoped lowered-standard with logged expiry (state visible + refusal grammar).

**CP6 · wave close**: dashboard delta + screenshots + STATE + close report.

## Verification path for orchestrator (independent audit) — W6 openers close

```bash
cd /app/assessment_workspace/repos/Extraction-Akki
git log --oneline programme/track-a | head -3
# f647051 W6 opener #2 · FL-P4-W4-01 reconciled · frozen contract parity restored
# 39386ac W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension

python3 -m pytest backend/tests/invariants/test_northena_ledger_row_v0.py -v
# Expect: 1 passed.

cd /app/assessment_workspace
git log --oneline master | head -3
# (opener #1 re-baseline + STATE update committed at close)

cat notes/status_and_wave_plan.md | grep -A2 "Calibration factor"
# Expect the 1.60× naming.
```

## Blocked (awaiting from owner)

- None new. **W6 scope proceeds unless owner steers to option (b) narrow-scope or (c) L-extended-tier from opener #1's naming.**

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
