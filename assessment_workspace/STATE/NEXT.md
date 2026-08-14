# NEXT.md — Exact next actions

**Last updated:** 2026-08-14 · WS-BUILD-CONNECT-GPU built end-to-end · 52/52 gating tests green on `programme/track-a` HEAD `dad2faa` · surface live at pod preview URL behind bearer auth · mock-sshd drill green · awaiting real VM credentials via the surface.

## Cycle status (2026-08-14 · WS-BUILD-CONNECT-GPU build cycle)

- **DECISIONS.md** — verbatim owner ruling on console-access + credential-delivery + WS-BUILD-CONNECT-GPU appended.
- **Fidelity ledger** — FL-P2-03 SUPERSEDED-TO-ACCEPTANCE · FL-P2-04 CLOSED path (a) · FL-P2-06 opened + CLOSED (WS-BUILD-CONNECT-GPU code-complete).
- **`programme/track-a`** — 7 tests-first commits at HEAD `dad2faa`. Working tree clean. 52/52 gating tests pass.
- **Surface reachable at:** `https://akki-reuse-assess.preview.emergentagent.com/register/connect/gpu`
- **Owner access token:** stored in `/app/backend/.owner_credentials` (mode 0600). Pod operator reads the file, hands the value to the owner. See §"Owner access token handoff" below.
- **Assessment-repo `master`:** pending this cycle's follow-up commit.

## Blocked (awaiting from owner)

- **Real AISCA VM credentials entered via the WS-BUILD-CONNECT-GPU surface.** Owner action; no builder-side task.
- **Reference screenshot file** — transcription-grade holds.

## Owner access token handoff (pod-operator procedure)

The token is a 64-char hex string, generated once on backend startup at `/app/backend/.owner_credentials` (mode 0600, never in any git repo, never in logs). To hand it over:

```bash
cat /app/backend/.owner_credentials
```

That value is the owner's login for `/register/connect/gpu`. It is an APP login only — not a Rafay console credential, not a VM credential, not an SSH key. Standing policy on external-console credentials is not touched. Rotate at any time by deleting the file and restarting the backend (`sudo supervisorctl restart backend`).

## Cold-reader-executable next actions

### 1. Deliver cycle-close report to owner (this reply)

Gating tests inventory · drill receipts · owner access token · exact URL · scope-class confirmation.

### 2. On real VM credentials entered via the surface

The seven-stage pipeline fires automatically. Watch for:
- **Green path:** `state_class='green'`, four-questions render `One GPU machine connected · hardened · accepted` / [acceptance sentences] / `Ready for first data` / `The machine matches what was ordered`. PINS.md gains a CONNECT-GPU-PINS block with `checkpoint_14d_utc = deploy_date + 14d`.
- **Failed path (hardening failure):** `state_class='failed'`, copy `This is ours — retry the submit once the cause is corrected.` `data_movement_permitted=False`. Retry supported.
- **Held path (acceptance failure = §6 mismatch):** `state_class='held'`, evidence-as-sentences, copy `Held with evidence — escalated to the vendor.` `data_movement_permitted=False`. Escalate to owner; NEVER modify `phase0/acceptance.sh` to accommodate a smaller SKU.

### 3. On green Phase-0 completion

- Assemble commissioning record; ledger it fully (hardening + acceptance sections).
- Update `STATE/PINS.md` `+14d checkpoint` line with the exact UTC deadline pinned from Deploy Date.
- Update NEXT.md to Phase-2 slice actions.
- Close FL-P1-02 stub open point on the same event.

### 4. Verification path for orchestrator (independent audit)

```bash
# Repo audit
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -E "File citations|Canon citations|failed"
python3 tools/completeness_audit.py 2>&1 | tail -3

# Track-a audit
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
    backend/tests/invariants/test_connect_gpu_scope_S_or_M.py -v
# Expect: 52 passed at HEAD dad2faa.

# Surface audit
curl -o /dev/null -w "HTTP %{http_code}\n" -L https://akki-reuse-assess.preview.emergentagent.com/register/connect/gpu
curl -o /dev/null -w "HTTP %{http_code}\n" https://akki-reuse-assess.preview.emergentagent.com/api/deliverables
curl -o /dev/null -w "HTTP %{http_code}\n" -X POST https://akki-reuse-assess.preview.emergentagent.com/api/connect/gpu -H "Content-Type: application/json" -d '{}'
# Expect: 200 / 200 / 401.
```

### 5. No push, ever

Owner Clarification 1 unchanged. Local commits are the record.
