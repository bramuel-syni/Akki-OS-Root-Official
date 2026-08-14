# NEXT.md - Exact next actions

**Last updated:** 2026-08-14 · Owner course-correction cycle CLOSED · wizard rebuilt to the brief's 5-step grammar for ALL resource kinds · estate keypair + provisioning card live · non-compute Step 5 records honest intent · programme/track-a HEAD `f83b509` · 123/123 gating tests green · IP allowlist unchanged per owner's strict directive.

## Cycle status (2026-08-14 · owner course-correction response)

- **FL-P2-14 CLOSED-BY-OWNER.** The fixture set (5-page brief + Registry screenshots + AISCA guide figures) IS the fixture.
- **Standing posture correction recorded** at the top of `STATE/CONTEXT.md`.
- **Wizard is generic.** 5 steps for all kinds, per PDF §5. Per-type branches at Step 2. Provisioning card at compute Step 2. Handshake walk at compute Step 5. Honest intent record at non-compute Step 5.
- **Estate ed25519 keypair** in seam custody (private mode 0600, never in return values). Provisioning card rendered from `GET /api/connect/estate-facts`.
- **Non-compute intents** ledgered via `POST /api/connect/intent`; `kind='compute'` refused (directs to the seven-stage `/api/connect/gpu`).
- **123/123 gating tests green.** 90 backend python + 12 frontend allowlist + 21 frontend rehome/wizard.
- **Live provisioning-card content (rotates on pod restart):**
  - Public key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki`
  - Fingerprint: `SHA256:TpJcdNAQ4iSQKK5inwPueOM6Qak5NcsD5XhZpWorZ+c`
  - Pod egress IP: `104.198.214.223`
- **Fidelity ledger:** FL-P2-14 CLOSED-BY-OWNER; FL-P2-16 CLOSED (wizard grammar); FL-P2-17 CLOSED (provisioning card); FL-P2-18 CLOSED (posture correction).

## Two-sentence access-mechanism proposal (still awaiting owner ratification)

> Access to the estate is IP-pinned; the allowlist admits your client `/32` (initial value `34.16.56.64`) at position `xff[-3]` of the ingress-set X-Forwarded-For chain, refusing every other address with HTTP 403 and one plain sentence. Additions and removals travel through `SPINE_ALLOWED_IPS` in `/app/backend/.env` - every change is a ledger row and the surface renders the current allowlist state as plain sentences.

## Blocked (awaiting from owner)

- **Ratify the two-sentence access proposal** (still standing).
- **FL-P2-09 disposition** - pod egress-IP rotation. Rotated AGAIN this cycle: STATE was `34.170.12.145` last cycle, now `104.198.214.223` this cycle. `34.16.56.64` stays in `SPINE_ALLOWED_IPS` unchanged per owner directive.
- **Vendor-side VM provisioning using the provisioning card:**
  - Paste the estate public key `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGKlcjZE/04clh3FLddGn7Wx69pytk8KJA5j9M6rKVA7 estate@akki` into the VM's SSH Public Key field at creation (AISCA guide Fig 10).
  - Add TWO /32 rows to the VM's Security Group SSH rules (AISCA guide Fig 11): the owner's own operator /32 AND the pod egress /32 (currently `104.198.214.223/32`, subject to rotation).
- **Then enter credentials via Registry -> +Connect -> Compute chip -> Step 3.** The unchanged seven-stage pipeline fires; with the estate key already installed, hardening shortens to verify-key-only -> disable password auth -> probe dead.

## Cold-reader-executable next actions

### 1. Deliver course-correction cycle report to owner (this reply)

Gating-test delta + right-reason receipts + wizard journey demonstrated (screenshots of all 5 steps incl. non-compute honest Step 5) + provisioning card content + scope number + commit SHAs.

### 2. On owner ratification of allowlist entry / vendor-side provisioning

- Update `SPINE_ALLOWED_IPS` in `/app/backend/.env` (add owner's client `/32`). Record allowlist change as a ledger row.
- Owner enters credentials through the wizard's compute path; the seven-stage pipeline fires. Watch for green/failed/held per brief §5 paragraphs 6-7.

### 3. Post-Phase-0 (next cycle)

- **A4 increment (Registry honest-state instrumentation):** wire the COMPUTE CONNECTED tab's after-state to the real commissioning record on disk (present a "Just connected" pill + meta line + link to the record). Add DATA CONNECTED / LLMS & TRAINED MODELS state transitions when their waves land.
- **Wire-up non-compute Step 5 to per-wave connectors** as they land (data-source in Phase 2 admit-slice; LLM/trained-model in later waves).

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
    backend/tests/invariants/test_estate_keys_and_connect_estate.py -v
# Expect: 90 passed at HEAD f83b509.

cd /app/frontend && node --test plugins/ip-allowlist/__tests__/ip_allowlist.test.js
# Expect: 12 passed.

cd /app/assessment_workspace/repos/Extraction-Akki && node --test pod_shell/frontend/__tests__/rehome.test.js
# Expect: 21 passed.

# Provisioning card live probe (through local backend + crafted XFF)
curl -s -H "X-Forwarded-For: 34.16.56.64,172.71.255.34,136.110.244.150" \
     "http://127.0.0.1:8001/api/connect/estate-facts" | python3 -m json.tool
```

### 5. No push, ever
