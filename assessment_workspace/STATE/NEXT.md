# NEXT.md - Exact next actions

**Last updated:** 2026-08-14 · Owner fixture-drop cycle CLOSED · Registry surface + Connect wizard live at root '/' per Screen mockups v7 (5-page written spec + owner's inline description of 4 screenshots) · GPU credential entry front door re-shaped from tile-grid detail card to conversational wizard's Compute path (submit machinery unchanged) · 105/105 gating tests green on `programme/track-a` HEAD `aeb2be0` · IP allowlist unchanged (`SPINE_ALLOWED_IPS=34.16.56.64` per owner's strict directive).

## Cycle status (2026-08-14 · owner fixture drop response)

- **Fixture pinned.** `fixtures/screen_mockups_v7.pdf` (sha256 `418ad0e3c087c613be7d7d885a18a3c895b7d51ed253119aff9ba042ee81da8a`, 195,644 bytes, 5 pages) written into PINS.md as file-cleared; full page-by-page inventory at `fixtures/screen_mockups_inventory.md`.
- **Discrepancy on record (FL-P2-14 OPEN).** Owner said "19 pages plus 4 inline screenshots" - PDF is 5 pages of pure text (Registry Feature & Component Brief), zero embedded images; the 4 inline screenshots were not accessible as job assets. Owner's inline textual description of the screenshots stands as the binding visual reference. Awaiting owner disposition on whether to re-upload the visual deck.
- **Registry surface live.** Root `/` renders `<Registry />` with three-tab shell (DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS), '+ Connect' button pushed right, role switcher (Compliance Owner · Watch Officer · Operator) in the header as STATIC presentation per FL-P2-15.
- **Connect wizard live.** '+ Connect' opens a right-hand drawer: "Connect something new" + "A conversation, not a form" deck; 4 suggestion chips (A data source · An LLM · A trained model · Compute) + free-text input + Send. Compute chip branches into the SAME 7 ordered GPU fields (Host Name · Username · Password [masked] · Public IP · Private IP · OS · Deploy date) that POST to the UNCHANGED `/api/connect/gpu` endpoint.
- **Empty state honors Content Rule 3.** Every tab renders honest current state ("No data connected yet." / "One machine pending connection." / "No models connected yet." / "drawn, never left blank"). Zero fabricated Acme demo numbers anywhere in code (`FL-P2-13 CLOSED`).
- **AdminSurface retired.** `/app/frontend/src/components/AdminSurface.jsx` deleted; its `admin-pill` and `tile-connect` testids gone.
- **`programme/track-a` HEAD `aeb2be0`** - 2 new sequential tests-first + implementation commits atop `acc25a8`.
- **105/105 total gating tests green** (78 backend python + 27 frontend node --test).
- **Fidelity ledger updated:** FL-P2-11 CLOSED (fixture upgrade), FL-P2-12 CLOSED (wizard-not-form rendering), FL-P2-13 CLOSED (demo-data-vs-honest-state), FL-P2-14 OPEN (PDF page-count discrepancy), FL-P2-15 CLOSED (role switcher deferred to Track-B).
- **Playwright render-tree proof:** 4 screenshots under `phase0/drill_receipts/screenshots/`; all 20 required data-testids verified present in the rendered tree.
- **IP allowlist unchanged.** `SPINE_ALLOWED_IPS=34.16.56.64` remains per owner's strict directive; deployment stays effectively private until owner's `/32` arrives.

## Two-sentence access-mechanism proposal (still awaiting owner ratification)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` - every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ratify the two-sentence access proposal** and/or **direct disposition of FL-P2-09** (pod egress-IP rotation: `34.16.56.64` in STATE vs `34.170.12.145` live).
- **FL-P2-14 disposition** - is the current PDF (5 pages) + inline description the intended fixture, or should the visual deck be re-uploaded?
- **Real AISCA VM credentials via the Registry → Connect wizard → Compute path** - blocked on owner's client-IP being on the allowlist.
- **Owner sign-off on (a) delivered** - Registry three-tab shell + wizard Compute path is live per fixture; (b) A4 honest-state instrumentation (real commissioning-record wiring into COMPUTE CONNECTED tab post-Phase-0) is the next-cycle increment, sized separately.

## Cold-reader-executable next actions

### 1. Deliver fixture-drop cycle report to owner (this reply)

PDF page inventory summary + scope class for (a) = M + test migration plan + built (a) + gating tests + evidence + FL-P2-14 discrepancy flag.

### 2. On owner ratification of allowlist entry / FL-P2-09 disposition

Update `SPINE_ALLOWED_IPS` in `/app/backend/.env`. Restart both services. Live-prove allow-branch from owner side. Record allowlist change as a ledger row.

### 3. On real VM credentials arriving through the wizard's Compute path

The unchanged seven-stage pipeline fires: intake → declaration → hardening → acceptance (via real `acceptance.sh` seam) → commissioning record → four-questions after-state → PINS `checkpoint_14d_utc` pin. Watch for `green` / `failed` / `held` grammar per PDF §5 paragraphs 6-7.

### 4. Phase A4 (Registry honest-state instrumentation) - next cycle

- Wire the COMPUTE CONNECTED tab's after-state to the real commissioning record on disk (present a "Just connected" pill + meta line + link to the record).
- DATA CONNECTED tab stays empty until admit-slice lands (Phase 2).
- LLMS & TRAINED MODELS tab stays empty until model registration lands (later phase).
- Tests-first for the state-transition invariants; do NOT fabricate any numbers.

### 5. Verification path for orchestrator (independent audit)

```bash
# Track-a audit (105/105 total gating)
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
    backend/tests/invariants/test_ip_allowlist_middleware.py -v
# Expect: 78 passed at HEAD aeb2be0.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 15 passed.
```

### 6. No push, ever

Owner Clarification 1 unchanged. Local commits on both `programme/track-a` (code, tests, pod-shell mirror) AND assessment-repo `master` (STATE, fidelity ledger, phase0 receipts, DECISIONS appendix, fixture inventory) are the record.
