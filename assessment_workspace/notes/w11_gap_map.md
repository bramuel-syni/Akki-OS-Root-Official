# W11 · Training-section gap map (owner deliverable · 2026-08-26T11:15Z)

Owner ruling R11 opened W11 partial scope: real GPU wiring + this gap map. Hardware probe at STEP 2 returned **auth-blocked** (sshd_config advertises `publickey` only for user `ubuntu` · owner-supplied password rejected at the protocol layer). Gap map below records the hardware column as **UNKNOWN pending owner action** rather than fabricated.

Sources for every EXISTS row: absolute file path + LOC on programme/track-a HEAD `f101bd0`. Sources for every MISSING row: canon anchor + who provides.

---

## EXISTS (on programme/track-a `f101bd0`)

| Component | Path | LOC | Anchor | Status |
|-----------|------|----:|--------|--------|
| **Targeta selector** (training-target eligibility / ranking / gate / yield) | `backend/services/targeta/` (5 files: `core.py`, `gate.py`, `interface.py`, `plan.py`, `yield_layer.py`) | ~425 | Canon 4 §14 · Doc13-006..010 (W7 CP2 · RMS lift) | REUSABLE (lifted · in-use) |
| **MOAC contract** (6-criterion model acceptance card) | `backend/contracts/model_acceptance_card.py` + snapshot | ~350 | Canon 4 §26 · Doc14-008..014 | DONE (W7 CP4 · frozen · parity 37→38) |
| **Baseline-line contract** (licence-verified starting model per training run) | `backend/contracts/baseline_line.py` + `backend/services/baseline_line/` | ~150 | Canon 4 §32 · Doc14-023 (CA1-004) | DONE (W7 CP5) |
| **Whitepaper drafter** (post-training summary · §33 CITATION invariant) | `backend/contracts/whitepaper_draft.py` + `backend/services/whitepapers/draft.py` | ~130 | Doc 14 §33 · Doc14-024 (CA1-005) | DONE (W10 CP6 · frozen · parity 58→59) |
| **Custody chokepoint** (extraction admit seam · training data will ride this) | `backend/services/chokepoint/`, `backend/services/northena/` (admit path) | ~500 | Canon 4 §31 · Canon 3 chokepoint | DONE (baseline · pre-W7) |
| **Cost ledger** (rates lane · training-run cost accounting) | `backend/services/cost_ledger/` + rates register | ~200 | Doc 11 · Canon 4 §26 | DONE (W6 CP2b · rates lane W7 CP1) |
| **Model registry** (adapter storage · versioning · attestation) | `backend/services/model_registry/` (registry + attest_model) | ~300 | Canon 5 §12.2 · Doc14-006, 017 | PARTIAL (W7 CP3 lift · FACTS-only seed of 7 Emergent Universal models · adapter-training entry wire is BUILD) |
| **Model admission ceremony** (MOAC-required gate before adapter ships) | `backend/services/model_admission/ceremony.py` | ~200 | Canon 4 §26 · Doc14-008 | DONE (W7 CP4) |
| **Frozen-objective invariant** (workers never modify a frozen objective mid-run) | `backend/tests/invariants/test_targeta_invariants.py` + Targeta plan seam | — | Canon 4 §43 · Doc14-025 | REUSABLE (enforced) |
| **Real GPU host** (network + auth path) | `/app/backend/.env` · `AKKI_GPU_HOST=41.173.184.244` (owner-supplied) | — | R11 waiver | **PARTIAL** — TCP reachable · SSH publickey required · **hardware specs UNKNOWN** |
| **Skill-file donor code** (LIFT candidate · not yet in build) | `repos/RMS-IQ-Core-2/backend/contracts/callable_skill_provisioning_v0.py` (101 LOC) + `services/transform_forms/callable_skill_gate.py` (144 LOC) + `services/transform_forms/callable_skill_persistence.py` (111 LOC) — same bytes also in `Akki-OS-V1` | 356 | RMS BCR §3.7 annex · TF-E2 α · TF-E4 (a) α · TF-E4 (b) β (2026-07-08) | REUSABLE (donor · uncommitted to programme/track-a) |
| **Training techniques spec** (recipe seat · optimizer selection protocol) | `repos/RMS-IQ-Core-2/docs/requirements/training_techniques_spec_v1.md` | 103 lines | RMS T-1 · T-2 (Muon protocol) · owner-ratified 2026-07-17 (RMS scope) | REUSABLE-doc (RMS-native · not re-ratified for Extraction-Akki) |

---

## MISSING

| Component | Provider | Anchor | Rough scope |
|-----------|----------|--------|------------:|
| **Trainer runner** (modality-agnostic LoRA/PEFT dispatch · integrates Critic Seam pass gate · emits MOAC card post-training) | **BUILD-us** | Canon 4 §26 (MOAC-required output) · §31 (extraction admit for training material) · RMS T-1 · T-2 | ~2000-3000 LOC · one wave-half |
| **Training-run contract** (start / end / status / lineage · versioned recipe field) | **BUILD-us** | Canon 4 §26 · §29 (versioning) · RMS T-1.1, T-1.3 | ~150 LOC contract + snapshot + parity same-commit DoD |
| **Training-config sidecar** (recipe seat · optimizer + LR schedule + adapter rank + target modules) | **BUILD-us** | RMS T-1.1 (versioned · ledgered · outside contracts/) | ~200 LOC + ledger integration |
| **Training-material admit contract** (extension of extraction admit for training corpus) | **BUILD-us** | Canon 4 §31 · Doc14-016 rights-lineage | ~120 LOC contract + snapshot |
| **Callable-skill provisioning contract** (LIFT from RMS donor · frozen · extra=forbid) | **BUILD-us (lift)** | RMS BCR §3.7 · TF-E2 α · TF-E4 (a) α · TF-E4 (b) β | 101 LOC lift · parity +1 · new register row (proposed Doc14-029 or CA1-N6) |
| **Callable-skill runtime** (per-call inner gate + write-once persistence · lift from RMS) | **BUILD-us (lift)** | RMS TF-E4 (a) α | 255 LOC lift · gate + persistence |
| **Training panel frontend** (recipe selector + run monitor + MOAC preview) | **BUILD-us** | Canon 5 (Interface architecture) · same v7 palette as Governance/Watch/GreyMirror | ~300-500 LOC React |
| **Skill Files surface** (provisioned-skills registry + per-skill governance card) | **BUILD-us** | Canon 5 §12 (Models tab neighbor) | ~250-400 LOC React |
| **Register row for callable-skill** (currently absent · 28 Doc 14 rows do not name it) | **BUILD-us (docs)** | new addendum row · CA1-N6 pattern | ~10 register lines |
| **Training corpus** (real data to train on · admitted through Northena) | **OWNER** | Canon 4 §31 · owner rights declaration | — |
| **Rights declaration** (owner-signed rights on training corpus · rights-lineage-resolved before extraction admits) | **OWNER** | Canon 4 §28 · Doc14-016 (DONE for shape · owner content pending) | — |
| **Base model choice + licence** (which open base model to LoRA/PEFT-adapt · which licence covers derived weights) | **OWNER** | Canon 4 §31 · one-licence-reach Doc14-026 | — |
| **Doc14-020 §38 rights-unclear ruling** (currently OPEN-SLOT from W10 CP7 · load-bearing before any external delivery of a trained-skill output) | **OWNER** | Canon 4 §38 · Doc14-020 | policy answer |
| **Recipe-seat ratification for Extraction-Akki** (RMS ratified 2026-07-17 for RMS scope · equivalent ratification needed for this pack's canon posture) | **OWNER** | RMS T-1 owner-ratified · needs re-anchor into 9-doc canon or new addendum row | policy ratification |
| **CA1-N2 / CA1-N3 / CA1-N5 policy answers** (FL-P4-W8-01 · FL-P4-W9-01 · N-series scaffolding is PARTIAL until policy lands · load-bearing for training pipeline that touches PII) | **OWNER** | Addendum §3 | 15 policy questions total |
| **SSH auth path to real GPU** (sshd on 41.173.184.244 advertises publickey only · password rejected at protocol layer) | **OWNER** | R11 waiver | supply private key OR flip PasswordAuthentication yes on the VM |
| **Hardware fact sheet on 41.173.184.244** (GPU model / count / VRAM / driver / CUDA / pytorch / disk / RAM · all UNKNOWN pending auth unblock) | **OWNER-then-BUILD-us** | STEP 2 gap · deferred | first probe on auth unlock |
| **CUDA toolkit / pytorch on VM** (whether pre-installed or main agent installs) | **UNKNOWN pending hardware probe** | — | probe reveals · owner ratifies install if agent-side |
| **AISCA-card equivalent for real GPU** (allowlist + SPINE_ALLOWED_IPS entries for the GPU host if it must call back into the pod) | **OWNER + BUILD-us** | R8/R9 allowlist pattern · same-commit DoD | ~30 LOC config + probe receipt |

---

## Hardware column · UNKNOWN

Everything below the "real GPU host" row is unfilled because auth is blocked. Once owner supplies an SSH key (or enables password auth server-side), the hardware fact sheet at STEP 2 will populate:

- GPU model + count (`nvidia-smi -L`)
- VRAM per card (`nvidia-smi --query-gpu=memory.total --format=csv`)
- Driver version (`nvidia-smi`)
- CUDA toolkit presence (`nvcc --version`)
- Python version + pytorch presence (with `torch.cuda.is_available()`)
- Free disk (`df -h /`) + RAM (`free -h`) + CPU count (`nproc`)
- Any running GPU processes (`nvidia-smi pmon -c 1`)

These facts directly drive the W11 build plan:
- If pytorch + CUDA present → trainer runner can install as pip package + adapter recipe.
- If CUDA missing → owner ratifies installing CUDA toolkit + drivers (a real change to the VM).
- If disk/VRAM insufficient for target adapter rank → recipe seat constrained accordingly.
- If GPU count > 1 → dispatch layer needs multi-GPU strategy declaration up front.

---

## What blocks W11 build-out right now

**One critical block · one soft block**:

1. **CRITICAL · SSH auth path** — cannot exercise the real GPU handshake through `/api/connect/gpu` until auth unlocks. Owner action (key supply OR sshd_config flip) is the unblock.
2. **SOFT · policy answers** — 15 non-blocking N-series answers + Doc14-020 + recipe-seat ratification. W11 build can start without these; they become load-bearing before FIRST LIVE training run, not before the trainer runner code lands.

---

## Recommended sequencing (informational · not booked without owner GO)

**W11 CP1**: unblock SSH auth path (owner action + main agent lands the key in .env at `AKKI_GPU_SSH_PRIVATE_KEY_PATH` with chmod-600 · restart backend to pick up · re-run STEP 2 hardware probe · bank real fact sheet · exercise /api/connect/gpu for a real crossing receipt through the custody chokepoint).

**W11 CP2**: STEP 3 fix-back — regression invariant (asserts env var names exist · NOT values · GPU_CONNECT_MODE mode toggle test).

**W11 CP3**: skill-files lift (356 LOC from RMS · frozen contract + parity map + snapshot same-commit DoD · new register row).

**W11 CP4**: training-run + training-config contracts (BUILD · ~470 LOC · frozen · same-commit DoD).

**W11 CP5**: trainer runner (BUILD · ~2000-3000 LOC · modality-agnostic · integrates Critic Seam gate + MOAC emission).

**W11 CP6**: training panel + skill files surfaces (BUILD · ~600-900 LOC React · REFERENCE-NOT-COPY posture).

**W11 CP7**: composite % recomputation + wave close.

Roughly 7 CPs · comparable to W10.

---

## Standing rules that persist through W11

- REFERENCE-NOT-COPY (A8) — trainer status surfaces render source_path citations, never fabricated recipe rows.
- Sanitizer at every response boundary — SSH key material, sudo credentials, adapter checkpoints treated same as signing_material.
- Same-commit DoD (FL-P4-W8-02) — every new frozen contract moves snapshot + map + hardcoded numeric assertion in the same commit.
- Corrected allowlist-flip procedure — both supervisor services restart at any .env change.
- No push · local commits only.

---

## Waiver expiry note (R11)

R11 opened the waiver for "connect directly, ignore rules only at this integration." That waiver window is still open because the connection is not established. The waiver expires the moment STEP 3 fix-back lands (regression invariant + local commit). Everything past STEP 3 runs under standard tests-first discipline.

Awaiting owner action on the SSH auth path.
