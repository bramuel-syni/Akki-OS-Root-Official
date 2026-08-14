# NEXT.md — Exact next actions

**Last updated:** 2026-08-14 · Owner rulings on FL-P2-03 + FL-P2-04 received, ruling logged verbatim to `DECISIONS.md`; Phase-1 hardening orchestrator code-complete on `programme/track-a` HEAD `ad65211` (5 commits atop `b150c21`; 35/35 gating tests pass); FL-P2-03 console-check precondition gap surfaced — no Rafay console credentials in workspace.

## Cycle status (2026-08-14 · owner-ruling-execution cycle)

- **DECISIONS.md** — verbatim owner ruling on FL-P2-03 + FL-P2-04 appended (§ "Owner Ruling on FL-P2-03 + FL-P2-04").
- **`programme/track-a`** — 5 commits at HEAD `ad65211`: `2b08b39` (tests-first A0/A1/seam) → `4855b35` (impl thin-kernel contracts + declaration + compute seam) → `ae7a816` (seam tools) → `abf6328` (tests-first hardening orchestrator, 9 assertions) → `ad65211` (impl hardening orchestrator). Working tree clean.
- **Phase-1 gating tests:** 35/35 pass (26 A0/A1/seam + 9 hardening orchestrator).
- **Right-reason failure logs banked:** `phase0/drill_receipts/20260814T120336Z_pre_implementation_right_reason_failure.log` (7 Phase-1 test files fail at collection with ModuleNotFoundError) + `phase0/drill_receipts/20260814T130000Z_hardening_orchestrator_right_reason_failure.log` (9 hardening tests fail at collection with ImportError).
- **`phase0/` frozen at Order-§6 spec** — `acceptance.sh` continues to probe for 4×H200 NVLink / ~30 TB HSS / restart-survives / password-dead. Optional hardening front-end (`AKKI_HARDENING_MODE=perform` gate) already present from previous cycle; VM-side script `harden.sh` idempotent + fail-closed; seam-side orchestrator `services/compute_seam/hardening.py` implements the six ordered steps per owner ruling.
- **FL-P2-03 console check:** URL identified — `https://console.rafay.dev/` (tenant-agnostic React SPA). Auth methods: email+password OR "Login with SSO" (email domain auto-detects OIDC/SAML). AISCA has no separate subdomain. **PRECONDITION GAP:** no Rafay console credentials have ever been provided in this workspace; check cannot be attempted. Escalated for owner-side credential handover.

## Blocked (awaiting from owner)

- **FL-P2-03 console visibility check** — blocked on Rafay console credentials. Owner must hand over EITHER (i) email + password, OR (ii) IdP-federated credentials + which IdP, OR (iii) an API key. See `ORCHESTRATOR.md` §2.1.
- **Phase-0 acceptance execution** — blocked on FL-P2-03 green + VM provisioning day + SSH credentials + BOOTSTRAP_SSH_PASSWORD arrival.
- **Phase-2 slice** — blocks on Phase-0 green.

## Cold-reader-executable next actions

### 1. Deliver cycle-close report to owner (this reply)

Console-check precondition gap (URL + auth methods + credentials-absent); hardening-module status (code-complete, 9/9 gating tests green, structural discipline verified via mocked outcomes); track-a commit log (5 commits at `ad65211`); Phase-1 deliverable report in Build-Order-01 shape.

### 2. On Rafay console credentials arriving

Perform read-only FL-P2-03 visibility check:
- Navigate to `https://console.rafay.dev/`; log in via provided credentials.
- Capture screenshot-grade evidence of the Services menu → Developer Hub → **High Speed Storage** section: does the ~30 TB HSS volume appear?
- Capture screenshot-grade evidence of Services menu → Developer Hub → COMPUTE → **Virtual Machines Catalog**: does a 4× H200 SKU entry appear?
- Assemble go/no-go REPORT with evidence attached (HTML snapshots or Playwright screenshots). Do NOT click provision under any circumstance; owner explicitly reserved provisioning until they have reviewed the evidence.

### 3. On SSH credentials + BOOTSTRAP_SSH_PASSWORD arrival (post FL-P2-03 green + Phase-0 acceptance)

- Populate `/app/backend/.env` (NEVER any git-tracked file) with `VM_HOST`, `VM_USER`, `SSH_PRIVATE_KEY_PATH`, `SSH_PUBLIC_KEY_PATH`, `SSH_CONNECT_TIMEOUT`, `HARDEN_SH_PATH`, `HARDENING_RECEIPT_DIR`, `BOOTSTRAP_SSH_PASSWORD` (single-use).
- Run `python3 -c "from services.compute_seam import hardening; print(hardening.run())"` — six ordered steps execute; external probe from pod must return `password_refused`.
- Verify hardening receipt lands at `HARDENING_RECEIPT_DIR`; ledger rows visible.
- Run `python3 backend/tools/run_acceptance_via_seam.py` — Phase-0 acceptance ledgered end-to-end.
- Assemble commissioning record combining hardening + acceptance sections.

### 4. On +14d checkpoint pinning

When VM provisioning day is confirmed, update `STATE/PINS.md` "checkpoint-targets deadline" line with actual UTC deadline (`provisioning_utc + 14d`).

### 5. Verification path for orchestrator (independent audit)

```bash
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -E "File citations|Canon citations|failed"
python3 tools/completeness_audit.py 2>&1 | tail -3

cd repos/Extraction-Akki
git log --oneline programme/track-a
python3 -m pytest backend/tests/invariants/test_actor_declaration_v0_contract_frozen.py \
    backend/tests/invariants/test_record_matrix_thin_kernel.py \
    backend/tests/invariants/test_task_identity_thin_kernel.py \
    backend/tests/invariants/test_parity_seat_extends_thin_kernel.py \
    backend/tests/invariants/test_admit_refuses_undeclared_actor.py \
    backend/tests/invariants/test_compute_seam_no_unledgered_exec.py \
    backend/tests/invariants/test_compute_seam_artifact_hash_verified.py \
    backend/tests/invariants/test_hardening_orchestrator.py -v
```

Expected at HEAD `ad65211`: 35 passed. Assessment-repo audits: 104/104 file · 1772/1772 canon · 0 failed; completeness PASS.

### 6. No push, ever

Owner Clarification 1: local commits are the record. Do not solicit push credentials.
