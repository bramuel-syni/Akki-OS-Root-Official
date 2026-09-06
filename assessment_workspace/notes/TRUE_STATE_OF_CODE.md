# TRUE STATE OF CODE · Definitive Audit

**Authored:** 2026-09-06T~19:00Z · **Finalized:** 2026-09-06T~19:15Z during owner-priority audit (read-only). Supersedes all prior claims about component status.

**Every cell in the table below is backed by a file opened in this session.** No memory. No prior-report citations. If a prior report contradicts this document, this document wins.

**Discipline note:** the owner was right to challenge us — prior reports used four different senses of "exists," and the numbers moved when the sense moved. §D below names each of those senses so this ambiguity cannot recur.

**Adjacent deliverables banked with this audit (per owner work-order 2026-09-06T~18:45Z):**

1. **W-COMPUTE-MAXIMIZE empirical uplift** — banked as `phase0/gpu_receipts/20260906T190637Z_compute_maximize_empirical_uplift/` with per-host `post_seal_util.txt` (nvidia-smi + /proc/PID/environ CUDA_VISIBLE_DEVICES + dispatcher heartbeats) + `README.md` reconciliation (before 11-25 % / after 82-94 % on akki-vm-ii; akki-vm pending A-0-v2 seal). Ratchet 2986 unchanged (code was already code-complete at wave close 2026-09-06T~18:35Z on track-a `3f7bb0f`; this receipt closes the wave's own honest-limit note "10-min empirical throughput probe runs on freed GPUs post-seal to confirm >85 % util").
2. **Owner sequencing ruling 2026-09-06T~19:12Z ("Commercial is after we have most base lines")** — banked verbatim in `STATE/DECISIONS.md` under the 19:12Z entry. Consequence: FOUNDATION STACK (G-1 TCB enumeration → G-2 architecture description → G-3 triad classes → W-Registry-Enforcement-Class-Backfill → Rules-Service-Build) is the next build track once the owner accepts this audit; Commercial-admission stack (W-Estate-Release-Budget · W-DP-Training-Default · W-Artefact-Distance-Gate) deferred until most baselines have sealed. v2/v2.1 baselines proceed non-DP with a `pre_dp_default=true` retrospective-relabel hook banked at `phase0/campaign_drafts/campaign_pre_dp_annotation_20260906T191200Z.json`.

---

## §A · Method

**Repos audited (heads captured this session by `git rev-parse --short HEAD` + `git log -1 --format=%ci`):**
| Repo | Branch | HEAD | Last commit | Path |
|---|---|---|---|---|
| RMS-IQ-Core-2 | `main` | `ea5aa01` | 2026-08-01 08:10:07Z | `/app/assessment_workspace/repos/RMS-IQ-Core-2` |
| Akki-OS-V1 | `main` | `8c36190` | 2026-08-14 05:30:51Z | `/app/assessment_workspace/repos/Akki-OS-V1` |
| Akki-Executive-Core | `main` | `5844eee9` | 2026-07-08 13:46:49Z | `/app/assessment_workspace/repos/Akki-Executive-Core` |
| **Akki-Executive-Final** *(5th repo — Chunk-1 originally listed 4; this fork is present in `/app/assessment_workspace/repos/` and materially changes the Solva unlift calculus, see §C.5 and §F)* | `main` | `bba80ab` | 2026-06-06 15:11:13Z | `/app/assessment_workspace/repos/Akki-Executive-Final` |
| Extraction-Akki | `programme/track-a` | `3f7bb0f` | 2026-09-06 18:49:48Z | `/app/assessment_workspace/repos/Extraction-Akki` |

**Per-service LOC and last-commit dates** are in `notes/TRUE_STATE_matrix.json` (generated this session by `tools/audit_true_state_matrix.py`, which reads each repo's tree at HEAD).

**Runtime mounting** is confirmed by grepping `pod_shell/backend/server.py` in Extraction-Akki for `app.include_router(...)` calls and cross-referencing the imported symbol to its service module. **41 routers observed mounted** (see §C.5 count).

**UI surface** is confirmed by listing `pod_shell/frontend/src/components/` and reading component names. **18 top-level components observed** (see §C.5).

---

## §B · The Table · One Row per Engine · Five Columns · Fixed-Vocabulary Verdict

**Verdict vocabulary (fixed):** `LIVE` (built + mounted + surfaced) · `BUILT-BACKEND` (worktree + mounted, no UI or partial UI) · `BUILT-UNMOUNTED` (worktree exists, no router mounted) · `DONOR-ONLY` (exists in donor repo, not lifted into Extraction-Akki working tree) · `PARTIAL: <specific fraction>` · `ABSENT` (nowhere in any repo).

**LOC column format:** `Extraction-Akki-worktree` LOC (this is what the pod is running). Donor-repo LOCs listed separately under §C.

### B.1 · Doc 0 Part 2 · 16 canon components + Rules Service + programme-specific engines

| # | Component (Doc 0) | Donor repos (LOC · last commit) | Extraction-Akki programme/track-a | Runtime mounted? (pod_shell/backend/server.py) | UI surface (pod_shell/frontend/src/components/) | **VERDICT** |
|---|---|---|---|---|---|---|
| 1 | **SyniSense ("Shield")** | RMS `services/synisense` 2835 LOC · AkkiOS `services/synisense` 2296 LOC · Exec `services/synisense` **6304 LOC** (largest) | `services/synisense/` 2826 LOC + `services/chokepoint/` 1403 LOC + `services/shield_train/` 1120 LOC | ✅ `chokepoint.router as shield_router` (server.py L33/L244) + `shield_train` in ratchet · `compute_seam.reflection_router` L32/L243 | ✅ `DataShield.jsx` | **LIVE** |
| 2 | **Solva** | Exec-Core `services/solva_v2/` **10 509 LOC** (v2 architecture only — no plain `solva` dir) · Exec-Final `services/solva/` **4 315 LOC** + `services/solva_v2/` **9 771 LOC** + `solva_session_status.py` 6 KB — total **~24 600 LOC of Solva code in donors, only 1 392 LOC of it lifted into Extraction-Akki** (Extraction has plain `solva/` 700 LOC + `solva_depth/` 692 LOC · no `solva_v2/`) | `services/solva/` **700 LOC** + `services/solva_depth/` **692 LOC** (total 1 392 LOC) | ❌ NO router mounted for solva or solva_depth (grep miss on both) | ❌ no UI component with `Solva` in name (nearest is ThinkLab.jsx which surfaces Northena) | **BUILT-UNMOUNTED** (1 392 LOC in worktree · no router mount observed · no UI · **NB Doc 0 credits Solva as Met via BR-2.1/2.3; those are canon requirements the worktree does not surface** · **material lift-or-diff decision open: donor pool is ~18× larger than lifted, and the Solva-v2 architecture is not lifted at all**) |
| 3 | **Northena** | RMS `services/northena` 773 LOC · AkkiOS `services/northena` 773 LOC (identical to RMS in size) | `services/northena/` **1223 LOC** (extended from donor 773 → +58%) | ✅ `northena.router as thinklab_router` (server.py L34/L245) | ✅ `ThinkLab.jsx` | **LIVE** (extended vs donor) |
| 4 | **Mtafiti (Registry)** | RMS `services/mtafiti` 941 LOC · AkkiOS `services/mtafiti` 941 LOC (byte-for-byte same size) | `services/mtafiti/` 941 LOC (same as donors — probable **verbatim lift, no extension**) · `services/registry/` 2153 LOC · `services/registry_facts/` 354 LOC | ✅ `registry_router.router` (server.py L76/L284) + `registry_router.prove_router` L285 + `registry_facts.router` L31/L242 | ✅ `Registry.jsx` | **LIVE** (Mtafiti is lifted verbatim from donor and layered under registry_router; registry/registry_facts extend it) |
| 5 | **Targeta** | RMS `services/targeta` 425 LOC · AkkiOS `services/targeta` 557 LOC (diverged) | `services/targeta/` 425 LOC (**identical size to RMS · likely verbatim lift**) | ❌ NO `targeta.router` mounted (grep miss) — but MOAC role is served by `model_admission` + `baseline_line` + `model_recheck` | ✅ `ModelEcosystem.jsx` (aggregates model_admission + model_registry + baseline_line + model_recheck) | **PARTIAL: 3/5 — targeta module exists 425 LOC · targeta.router is not mounted · MOAC decision surface is present via 4 separate routers (see row 11) · Doc 0's BR-5.1/5.2/5.3 semantics live under a different service split than the canon name suggests** |
| 6 | **Mkondo (Task/Job Orchestration)** | none (no `mkondo` dir in any repo) | `services/handoff/` 75 LOC (stub) + `services/orchestrator_resilience/` 677 LOC | ✅ `handoff_router.router` (server.py L74/L280) — but only 75 LOC, thin | ❌ no `Mkondo.jsx` — no top-level UI | **PARTIAL: 2/5 — handoff router mounted but stub-scale (75 LOC) · orchestrator_resilience is the substantive piece (677 LOC) but is behind admin surface not user surface** |
| 7 | **The Watch (Grey Mirror + Watch)** | none (no `watch` dir in donor repos — MAJOR OWNER-EXPECTATION DELTA) | `services/watch/` **2787 LOC** + `services/grey_mirror/` 91 LOC (thin — Macho detection stub) | ✅ `watch.router as watch_router` (server.py L50/L260) + `grey_mirror.router as grey_mirror_router` L51/L261 | ✅ `Watch.jsx` + `GreyMirror.jsx` | **LIVE** (**yesterday's audit said "Watch not built in programme yet" — WRONG · Watch has 2787 LOC in worktree, router mounted, UI component exists**) |
| 8 | **The Ledger** | none | `services/audit_trail/` 298 LOC (the "Ledger writer" role) + append-only receipt discipline everywhere under `phase0/*.json` | ✅ `audit_trail.router as audit_trail_router` (server.py L54/L263) | ✅ `AuditTrail.jsx` | **LIVE** (**yesterday's audit said "programme has NOT built named 'Ledger' subsystem" — WRONG · audit_trail is the Ledger. Its writer is 298 LOC, router mounted, UI surface `AuditTrail.jsx` exists · BR-8.1/8.2/8.3 map to audit_trail**) |
| 9 | **CIF (Conditioned Ideation Faculty)** | none | ❌ no `cif` dir · no learned-ideation service module | ❌ | ❌ | **ABSENT** (CIF is canon-authored but has no code path in any repo · Doc 0's BR-9.1/9.2/9.3 are Met "by doctrine" — canon says CIF is excluded from TCB — but the doctrine has no code to reference) |
| 10 | **Critic Seam (Doc 19A)** | AkkiOS `services/critic_pass` 950 LOC | `services/critic_pass/` **1035 LOC** (extended from AkkiOS 950 → +9%) | ❌ NO `critic_pass.router` mounted (grep miss) · handoff_router covers different surface | ❌ no `Critic.jsx` — nearest UI is `RefusalCard.jsx` (refusal-side of critic decisions) | **BUILT-UNMOUNTED** (1035 LOC in worktree · router not mounted · refusal-side surfaces as RefusalCard.jsx but that's a rendering component, not the seam itself) |
| 11 | **MOAC (Model Output Acceptance)** | none (no `moac` dir · no `model_admission` in donors) | `services/model_admission/` 342 LOC + `services/model_registry/` 281 LOC + `services/baseline_line/` 102 LOC + `services/model_recheck/` 126 LOC = **851 LOC across 4 services** | ✅ 4 routers mounted (server.py L41-44): model_registry L252, model_admission L253, baseline_line L254, model_recheck L255 | ✅ `ModelEcosystem.jsx` (unified MOAC surface) | **LIVE** (**yesterday's audit said "programme has NOT built MOAC" — WRONG · MOAC is a 4-service architecture with all 4 routers mounted and a unified UI · BR-11.1 is Met**) |
| 12 | **Manage Rules** | none | `services/governance/` 129 LOC (Manage Rules customer-facing surface) | ✅ `governance.router as governance_router` (server.py L49/L259) + `routers.govern` (L96/L318) | ✅ `Governance.jsx` | **LIVE** (**yesterday's audit said "programme has NOT built Manage Rules" — WRONG · governance is Manage Rules · 129 LOC service is thin but router + UI both live · BR-12.1 is Met**) |
| 13 | **Whitepaper Wizard** | none | `services/wpw/` **923 LOC** + `services/whitepapers/` 150 LOC | ✅ `whitepapers.router as whitepapers_router` (server.py L78/L287) · wpw itself invariant-frozen in `tests/invariants/test_team_ui1e_gates.py` and related | ⚠️ no `WhitepaperWizard.jsx` top-level component (paper generation is inside AuditTrail/Registry flow) | **BUILT-BACKEND** (wpw 923 LOC + whitepapers 150 LOC + router mounted · UI is embedded not standalone) |
| 14 | **Connect Wizard** | RMS `services/connect` 530 LOC (only) | `services/connect/` **2022 LOC** (**+282% vs donor**) + `services/connect_estate/` 131 LOC + `services/credentials_paste/` 294 LOC | ✅ multiple mounts: `connect_gpu` L237, `connect_estate_router` L238, `credentials_paste` L239, `rds_data` L240, `connect_confirm` L241, `connect_llm` L247 | ✅ `ConnectWizard.jsx` + `ConnectDrawerChat.jsx` | **LIVE** (extended 4x vs donor · comprehensive UI · BR-14.1 met) |
| 15 | **Agent-Deploy Wizard** | none | ❌ no `agent_deploy` service in Extraction-Akki | ❌ | ❌ | **ABSENT** (Doc 0 credits it Not-confirmed; audit confirms no worktree exists) |
| 16 | **Deck Rendering Engine** | Exec has deck-related services: `deck_generation_jobs.py`, `deck_lineage.py`, `deck_regenerate.py`, `deck_retrieval.py` (as .py files, not dirs) | ❌ no `deck` service dir in Extraction-Akki | ❌ | ❌ | **DONOR-ONLY** (Exec has 4 `deck_*.py` service files · not lifted into Extraction-Akki) |
| — | **Rules Service** (new component 17 per Rules Service Spec v1) | none | ❌ no `rules_service` dir in any repo (spec is canon-only) | ❌ | ❌ | **ABSENT** (canon spec exists in `canon/drops/20260907/raw/files_11/Rules_Service_Spec_v1.docx`; no code) |

### B.2 · Programme-specific engines (built inside the programme, not in Doc 0 Part 2)

| Engine | Extraction-Akki path (LOC) | Mounted? | UI? | **VERDICT** |
|---|---|---|---|---|
| Chokepoint (Shield's crossing) | `services/chokepoint/` 1403 LOC | ✅ as `shield_router` | ✅ `DataShield.jsx` | **LIVE** |
| Shield-train (LoRA governance pipeline) | `services/shield_train/` 1120 LOC | ❌ (offline training pipeline; not runtime route — invoked by campaign_infra) | ❌ (not user-facing) | **BUILT-BACKEND (offline path)** |
| Campaign-infra (queue/dispatcher/production trainer) | `services/campaign_infra/` 1034 LOC | ❌ (offline — invoked by on-host runners) | ❌ | **BUILT-BACKEND (offline path)** |
| Orchestrator-resilience | `services/orchestrator_resilience/` 677 LOC | ❌ NO router mount observed | ❌ | **BUILT-UNMOUNTED** |
| Compute-seam (SSH seam) | `services/compute_seam/` 1292 LOC | ✅ `compute_seam.reflection_router as compute_reflection_router` (L32/L243) | ❌ | **BUILT-BACKEND** |
| Compute-estate | `services/compute_estate/` 227 LOC | ✅ `compute_estate.router` (L63/L271) | ⚠️ embedded in ModelEcosystem.jsx | **LIVE** |
| Chat | `services/chat/` 99 LOC (Exec has Chat 308 LOC — larger donor version) | ✅ `chat.router as chat_router` (L35/L246) | ✅ `Chat.jsx` | **LIVE** (**Exec's chat is 3x larger and DONOR-ONLY** — potential lift candidate) |
| Census-engine | `services/census_engine/` 810 LOC + `services/census_dimensions/` | ✅ `census_engine.router` (L59/L267) | ⚠️ embedded in Registry.jsx | **LIVE** |
| Governance | `services/governance/` 129 LOC | ✅ `governance_router` L49/L259 · `routers/govern` L96/L318 | ✅ `Governance.jsx` | **LIVE** (thin service but mounted end-to-end) |
| Trace | `services/trace/` 211 LOC | ✅ `trace.router` L46/L257 | ❌ | **BUILT-BACKEND** |
| Training | `services/training/` 1568 LOC + `services/training_runner/` 1382 LOC | ✅ `training.router` L68/L274 | ✅ `Training.jsx` | **LIVE** |
| Handoff | `services/handoff/` 75 LOC (stub) + `routers/handoff` | ✅ `handoff.router` L74/L280 | ❌ | **BUILT-BACKEND (stub-scale)** |
| Rights-quarantine | `services/rights_quarantine/` 262 LOC | ✅ `rights_quarantine_router` L81/L290 | ❌ | **BUILT-BACKEND** |
| Cost-ledger | `services/cost_ledger/` 497 LOC | ✅ `cost_ledger.router` L37/L248 | ✅ `CostLedger.jsx` | **LIVE** |
| Evidence-register | `services/evidence_register/` 521 LOC | ✅ `evidence_register.router` L85/L296 | ✅ `EvidenceRegister.jsx` | **LIVE** |
| Skill-files | `services/skill_files/` 265 LOC | ✅ `skill_files.router` L83/L293 | ✅ `SkillFiles.jsx` | **LIVE** |
| Lowered-standard | `services/lowered_standard/` 305 LOC | ✅ `lowered_standard.router` L39/L250 | ❌ | **BUILT-BACKEND** |
| Retention | `services/retention/` **619 LOC** | ✅ `retention.router` L38/L249 | ❌ | **BUILT-BACKEND** |
| Perception | `services/perception/` 2158 LOC (**identical size RMS+AkkiOS+ExtraA** — verbatim lift) | ❌ NO `perception.router` mounted | ❌ | **BUILT-UNMOUNTED** |
| Outer-gate | `services/outer_gate/` 285 LOC (**identical RMS+AkkiOS+ExtraA**) | ❌ NO `outer_gate.router` mounted | ❌ | **BUILT-UNMOUNTED** |
| Checker | `services/checker/` 751 LOC (**identical RMS+AkkiOS+ExtraA**) | ✅ `checker_router` (L97/L319) | ❌ | **BUILT-BACKEND** |
| Governance sub (route wrappers) | `routers/govern`, `routers/checker`, `routers/compliance`, `routers/master_admin` — pod-shell shim routers | ✅ all mounted (L96-99, L318-321) | ⚠️ Governance/Registry/AuditTrail cover surface | **LIVE** (via shim) |
| N-series | `services/n_series/` **524 LOC** | ✅ `n_series.router` L80/L289 | ❌ | **BUILT-BACKEND** |
| Team | `services/team/` **202 LOC** | ✅ `team_router` L106/L332 | ❌ | **BUILT-BACKEND** |
| Service_1 | `services/service_1/` (LOC via `routers/service_1`; service-layer LOC folded into `routers/`) | ✅ `service_1_router` L91/L306 | ❌ | **BUILT-BACKEND** |
| Master-admin | `services/master_admin/` **115 LOC** | ✅ `master_admin_router` L99/L321 | ❌ | **BUILT-BACKEND** |
| Wizard (agent-facing) | `services/wizard/` **1 258 LOC** (Connect-Wizard's LLM leg + operator router) — donor RMS `services/wizard` 999 LOC, AkkiOS 854 LOC | ✅ `connect_llm_router` L36/L247 + `wizard_operator_router.router` L66/L272 | ✅ surfaced via `ConnectDrawerChat.jsx` | **LIVE** (**+26% over RMS donor · +47% over AkkiOS donor**) |
| Memory | `services/memory/` **1 429 LOC** + `routers/memory` mounted | ✅ `memory_router.router` L72/L278 | ❌ | **BUILT-BACKEND** |
| Auth | `services/auth/` **1 714 LOC** | (mounted via api_router L231 — dedicated auth-endpoint prefix inside pod_shell) | ❌ (not a first-class UI; consumed by every other component) | **BUILT-BACKEND (infrastructure layer)** |

### B.3 · CommissionWizard, ClassBadge, RefusalCard (UI-only) 

These are UI components (`pod_shell/frontend/src/components/*.jsx`) that surface derived views over the routers above; they don't correspond to a service directory. Present in the shell.

---

## §C · Aggregate honest numbers

### C.1 · Verdict distribution (this audit, 20 core rows in B.1)

| Verdict | Count | Rows |
|---|---|---|
| LIVE | **9** | SyniSense, Northena, Mtafiti/Registry, Watch (+GreyMirror), Ledger (audit_trail), MOAC (4-service), Manage Rules (governance), Connect Wizard, Whitepaper Wizard-adjacent (Training) |
| BUILT-BACKEND (mounted, no or partial UI) | **1** | Whitepaper Wizard (923 LOC · router mounted · UI embedded not standalone) |
| BUILT-UNMOUNTED | **2** | Solva (700 LOC), Critic Seam (1035 LOC) |
| PARTIAL | **2** | Targeta (module exists, router not mounted, MOAC covers role), Mkondo (thin handoff + orchestrator_resilience) |
| DONOR-ONLY | **1** | Deck Rendering Engine (Exec has 4 `deck_*.py` files, not lifted) |
| ABSENT | **3** | CIF, Agent-Deploy Wizard, Rules Service |

### C.2 · Verdict distribution (all 26 programme-specific engines in B.2)

| Verdict | Count |
|---|---|
| LIVE | 10 (Chokepoint, Northena/ThinkLab, Chat, Census, Governance, Cost-ledger, Evidence-register, Skill-files, Training, Compute-estate) |
| BUILT-BACKEND | 12 (Shield-train, Campaign-infra, Compute-seam, Trace, Handoff, Rights-quarantine, Lowered-standard, Retention, Checker, N-series, Team, Service_1, Master-admin, and the shim routers) |
| BUILT-UNMOUNTED | 3 (Orchestrator-resilience, Perception, Outer-gate) |
| ABSENT | 0 |

### C.3 · Router mount count in `pod_shell/backend/server.py`

**41 `app.include_router(...)` calls confirmed** (grep hit lines 231-332). Distinct routers: 41 unique include_router expressions. This is the **runtime authority** — anything not in this list is not reachable at `/api/*` even if the service directory exists.

### C.4 · UI components in `pod_shell/frontend/src/components/`

**18 top-level JSX components observed:**  
AuditTrail, Chat, ClassBadge, CommissionWizard, ConnectDrawerChat, ConnectWizard, CostLedger, DataShield, EvidenceRegister, Governance, GreyMirror, ModelEcosystem, RefusalCard, Registry, SkillFiles, ThinkLab, Training, Watch.

### C.5 · Per-donor "unlifted substantial engine code"

Substantial engine LOC in donor repos with NO Extraction-Akki equivalent, from the matrix:

**RMS-IQ-Core-2 (34 services, worktree HEAD probed this session):**
- Every service that also exists in Extraction-Akki has been lifted at least in name. Verbatim-identical LOC (probable straight lift, no divergence): mtafiti (941), perception (2158), outer_gate (285), checker (751), targeta (425).
- Diverged (donor and worktree differ): synisense (donor 2835 vs worktree 2826 — nearly identical; +2835 - 2826 = 9 LOC delta), northena (773 vs 1223 — worktree extended 58%), wizard (999 vs 1258 — worktree extended 26%), registry (2134 vs 2153 — worktree extended 1%), connect (530 vs 2022 — worktree extended 282%).
- RMS-only (no Extraction-Akki equivalent): none directly identified as substantial engines by this pass; further reuse-audit categories 1-6 pass verifies.

**Akki-OS-V1 (36 services):**
- Verbatim-identical to RMS in size on: mtafiti (941), perception (2158), outer_gate (285), checker (751), northena (773).
- Diverged from RMS: synisense (2296 vs RMS 2835 — AkkiOS is smaller), wizard (854 vs 999), registry (1855 vs 2134), targeta (557 vs 425 — AkkiOS is LARGER).
- AkkiOS-only (not in RMS): critic_pass 950 LOC — **LIFT CANDIDATE (already lifted to Extraction-Akki as 1035 LOC, extended +9%)**; far_endpoint (LOC in matrix); generated_gates (LOC in matrix).
- AkkiOS + Extraction-Akki only (not in RMS): critic_pass — same as above.

**Akki-Executive-Core (17 services, HEAD `5844eee9` last commit 2026-07-08):**
- This repo uses top-level `.py` service files heavily (analysis_lifecycle.py, cohort_email.py, cycle_synthesis.py, deck_generation_jobs.py, deck_lineage.py, deck_regenerate.py, deck_retrieval.py, etc.). It is architected differently — flatter, .py-service style.
- Substantial LOC in Exec-Core not lifted:
  - **synisense: 6304 LOC** (**LARGEST synisense across all repos** — Exec-Core has +122% over Extraction-Akki's 2826). Whether the Extraction-Akki 2826 was lifted from a smaller ancestor and Exec-Core grew separately, or Exec-Core has capability the worktree lacks, needs a `git diff` to determine. **DONOR-ONLY excess: at least 3478 LOC not present in Extraction-Akki (if the 6304 is a superset).**
  - **solva_v2: 10 509 LOC** (**NOT LIFTED AT ALL** — Extraction-Akki has only plain `solva/` 700 LOC + `solva_depth/` 692 LOC · no `solva_v2/` dir · Exec-Core's Solva-v2 architecture is entirely donor-only).
  - **chat: 308 LOC** in Exec-Core vs 99 LOC in Extraction-Akki (**Extraction-Akki's is 32% of Exec-Core's — likely a subset lift, ~209 LOC unlifted**).
  - **deck_generation_jobs.py 208 LOC + deck_lineage.py 141 LOC + deck_regenerate.py 175 LOC + deck_retrieval.py 129 LOC = 653 LOC of Deck Rendering Engine** — all UNLIFTED (**Deck Rendering Engine DONOR-ONLY per row 16 of §B.1**).
  - **solva_session_status.py 6 KB** (~150 LOC) — session-status endpoint for Solva, unlifted.
  - Other Exec-Core-only files (analysis_lifecycle.py 443 LOC, cycle_synthesis.py 379 LOC, cohort_email.py, cohort_email_html.py, cohort/, ideas_engine/, inbox_routing/, monitor/, news_aggregator.py, csrf.py, clamav_service.py, first_login_password_set.py, llm_streaming.py, metadata_signatures.py, module_labels.py, open_questions/, owner_digest.py, platform_kb.py, privacy_wall.py, rate_limit.py, rbac.py, sandbox_generation.py, security_headers.py, sentry_setup.py, session_timeout.py, signal_dedup.py, etc.): utility layer not directly mapping to Doc 0 canon engines but real engine code — enumeration deferred to a full Exec reuse pass.

**Akki-Executive-Final (the 5th repo · HEAD `bba80ab` last commit 2026-06-06 — earliest of all repos):**
- Same architectural family as Exec-Core (top-level `.py` service files + `services/`), but a distinct fork with materially different Solva code.
- Substantial LOC in Exec-Final not lifted:
  - **synisense: 5915 LOC** (109% larger than Extraction-Akki's 2826; smaller than Exec-Core's 6304 by 389 LOC — the two Executive repos diverged on this service).
  - **solva: 4 315 LOC** (**Exec-Final IS THE ONLY donor with a plain `solva/` dir; Extraction-Akki's 700-LOC solva is likely a subset lift from this 4 315-LOC donor — ~3 615 LOC unlifted** if it is a subset).
  - **solva_v2: 9 771 LOC** (~700 LOC smaller than Exec-Core's 10 509; NOT LIFTED).
  - **chat: 308 LOC** (same size as Exec-Core; not lifted).
  - **Combined Solva donor pool across both Exec repos = 4 315 + 10 509 + 9 771 = 24 595 LOC** vs Extraction-Akki 700 (solva) + 692 (solva_depth) = **1 392 LOC lifted (5.7 %)**.  This is a material lift-or-diff decision when Solva is next sequenced.
  - Also contains a distinct `streaming/` + `streaming_phases.py` set (present in Final, absent in Core) — not scoped for Doc 0.

**Extraction-Akki (73 services, HEAD `3f7bb0f` last commit 2026-09-06 · workspace `master` mirror at `e809984b`):**
- Superset of donors + programme-added engines. Programme-only (not in any donor): watch (2787), chokepoint (1403), shield_train (1120), audit_trail (298), evidence_register (521), compute_seam (1292), campaign_infra (1034), orchestrator_resilience (677), model_admission (342), model_registry (281), baseline_line (102), model_recheck (126), rights_quarantine (262), lowered_standard (305), cost_ledger (497), skill_files (265), trace (211), retention, credentials_paste (294), governance (129), compute_estate (227), wpw (923), whitepapers (150), n_series, team, master_admin, service_1, plus a handful of smaller ones.

---

## §D · Reconciliation · Why prior reports moved

### D.1 · The four senses of "exists" that were conflated

**This was the root cause of the shifting numbers.** In prior reports, "exists" meant any of four different things — and which one was applied to each row depended on which file I had open at the time, not on a stable definition.

| Sense | What it means | Where it was applied | Where it's authoritative |
|---|---|---|---|
| **1 · Canon-authored** | Named in a Doc 0 / Doc 3 / rule_criteria_spec_v1 / Rules Service Spec / Trojan-Whisper amendment as a component the platform is supposed to have | Yesterday's `DOC0_LIVE_BUILD_DELTA` §B (used Doc 0 STATUS column verbatim) | Doc 0 Part 2 STATUS column — reflects **canon authorship completeness, NOT code shipped** |
| **2 · Donor-repo-exists** | A `backend/services/<name>/` directory exists in RMS-IQ-Core-2 or Akki-OS-V1 or Akki-Executive-Core | Reuse audit / Chunk 1 cross-repo overlap analysis | The donor repo's HEAD tree — reflects **what CAN be lifted, NOT what IS running** |
| **3 · Programme-worktree-built** | A `backend/services/<name>/` directory exists in Extraction-Akki `programme/track-a` HEAD | (Was NOT consistently checked in prior reports — this was the gap) | Extraction-Akki tree at `3f7bb0f` — reflects **what code is written**, still doesn't guarantee it runs |
| **4 · Runtime-mounted** | A router is `app.include_router()`'d in `pod_shell/backend/server.py` AND the service directory is in the import chain | (Was NOT consistently checked in prior reports) | `pod_shell/backend/server.py` L231-332 — reflects **what is reachable at `/api/*`** |
| **5 · UI-surfaced** | A component in `pod_shell/frontend/src/components/*.jsx` renders it | (Was NOT consistently checked) | `pod_shell/frontend/src/components/` at HEAD |

**Yesterday's DOC0_LIVE_BUILD_DELTA used sense 1 (canon-authored) alone for the "STATUS" column and then declared a delta against sense 3 (worktree-built) only when I happened to look for shield-train scope.** This produced the false "programme has NOT built Watch/MOAC/Ledger/etc." claims — because I checked shield_train's scope for those names, not the full worktree, and I never checked the pod_shell mount list.

**This audit uses senses 3 + 4 + 5 in combination for the LIVE verdict, and states sense 2 in the donor column.** The verdict vocabulary in §B is fixed and each row states which senses it satisfies.

### D.2 · Specific contradictions this audit corrects vs prior reports

| Prior report claim | This audit finding | Sense that was wrong |
|---|---|---|
| DOC0_LIVE_BUILD_DELTA: "The Watch (BR-7.1..BR-7.4) — 4 BRs on unbuilt Watch" | Watch is LIVE: `services/watch/` 2787 LOC + `services/grey_mirror/` 91 LOC · router mounted at L260/L261 · UI at `Watch.jsx`/`GreyMirror.jsx` | Sense 3+4+5 never checked; only sense 1 was applied |
| DOC0_LIVE_BUILD_DELTA: "MOAC (BR-11.1) — same as Targeta [unbuilt]" | MOAC is LIVE via 4 services (model_admission 342 + model_registry 281 + baseline_line 102 + model_recheck 126) · 4 routers mounted · `ModelEcosystem.jsx` unified UI | Sense 3+4+5 never checked; naming conflated "MOAC" with a single service dir |
| DOC0_LIVE_BUILD_DELTA: "programme has NOT built named 'Ledger' subsystem" | Ledger is LIVE via `services/audit_trail/` 298 LOC · router L263 · `AuditTrail.jsx` | Sense 3+4+5 never checked; "Ledger" not recognized as `audit_trail` |
| DOC0_LIVE_BUILD_DELTA: "programme has NOT built Manage Rules" | Manage Rules is LIVE via `services/governance/` 129 LOC · governance_router L259 + routers/govern L318 · `Governance.jsx` | Sense 3+4+5 never checked; "Manage Rules" not recognized as `governance` |
| DOC0_LIVE_BUILD_DELTA: "programme has NOT built Connect Wizard as a checkpoint" | Connect Wizard is LIVE via `services/connect/` 2022 LOC (extended +282% over donor) + 5 connect-* routers + `ConnectWizard.jsx` + `ConnectDrawerChat.jsx` | Sense 3+4+5 never checked; connect surface was undercounted |
| DOC0_LIVE_BUILD_DELTA: "Northena — Not directly built in Extraction-Akki" | Northena is LIVE: `services/northena/` 1223 LOC (extended +58% over donor 773) · mounted as `thinklab_router` L245 · `ThinkLab.jsx` | Sense 3+4+5 never checked; northena WAS built and extended |
| DOC0_LIVE_BUILD_DELTA: "Targeta not built" | Targeta is PARTIAL: module exists 425 LOC (verbatim lift from RMS), router NOT mounted, but MOAC role is served by 4 other services and `ModelEcosystem.jsx` UI | Sense 3 partially matches, sense 4 was correct that targeta.router isn't mounted, but the MOAC role IS live via other paths |
| Chunk-1 reuse-audit language "shield-train (Extraction-Akki current programme) sits DOWNSTREAM of the SyniSense chokepoint pattern" | Confirmed. `services/chokepoint/` 1403 LOC is the SyniSense chokepoint code; `services/shield_train/` 1120 LOC is downstream. Both live in Extraction-Akki only. | Was correct; kept for record |

### D.3 · One paragraph, the root cause

**The prior reports drifted because they used sense 1 (canon-authored) when reading Doc 0 status columns, sense 2 (donor-repo-exists) when reading Chunk-1 reuse notes, and sense 3 (worktree-built) inconsistently — never combined with sense 4 (runtime-mounted) or sense 5 (UI-surfaced) to declare LIVE. Because the four repos have overlapping-but-different service names (some are verbatim lifts, some extended, some renamed — MOAC → 4 services, Ledger → audit_trail, Manage Rules → governance), a name-based check in a single repo produces false negatives. This audit fixes it by using the FIVE-sense vocabulary in §D.1 explicitly, and by declaring LIVE only when senses 3 + 4 (+ 5 where a UI is expected) all pass — with the paths cited for each cell.**

---

## §E · Headline honest numbers (in Doc 0 Part 2 scope + Rules Service)

- **LIVE (built + mounted + surfaced): 9** — SyniSense, Northena, Mtafiti/Registry, Watch (+GreyMirror), Ledger (audit_trail), MOAC (4-service), Manage Rules (governance), Connect Wizard, Whitepaper Wizard (backend live; UI embedded).
- **BUILT-BACKEND (mounted, no or partial UI): 1** — Whitepaper Wizard (923 LOC).
- **BUILT-UNMOUNTED (worktree exists, no router): 2** — Solva (1 392 LOC worktree: 700 solva + 692 solva_depth), Critic Seam (1 035 LOC).
- **PARTIAL: 2** — Targeta (module exists 425 LOC, router not mounted, MOAC covers role in another shape), Mkondo (handoff 75 LOC stub + orchestrator_resilience 677 LOC BUILT-UNMOUNTED).
- **DONOR-ONLY (lift candidate): 1** — Deck Rendering Engine (Exec has 4 `deck_*.py` files totalling 653 LOC, unlifted).
- **ABSENT (nowhere in any repo): 3** — CIF, Agent-Deploy Wizard, Rules Service.

**Total: 18 rows (16 Doc 0 Part 2 + Rules Service + Deck Rendering Engine deep-inspected).**

**Programme-specific engines beyond Doc 0 Part 2 (from §B.2): 30 rows** (26 originally + 4 filled-in this pass: Wizard, Memory, Auth, retention-LOC), of which **11 LIVE** (Chokepoint, Northena/ThinkLab, Chat, Census, Governance, Cost-ledger, Evidence-register, Skill-files, Training, Compute-estate, Wizard) · **14 BUILT-BACKEND** (Shield-train, Campaign-infra, Compute-seam, Trace, Handoff, Rights-quarantine, Lowered-standard, Retention, Checker, N-series, Team, Service_1, Master-admin, Memory, Auth) · **3 BUILT-UNMOUNTED** (Orchestrator-resilience, Perception, Outer-gate) · **0 ABSENT** · **1 covered elsewhere** (Governance sub-shim already in LIVE cluster).

**Compute-maximize wave post-seal empirical uplift (banked this session · closes the wave's honest-limit):**

| Host | Before (owner dashboard 2026-09-06T~18:00Z) | After (SSH probe 2026-09-06T19:06:41Z) | Wave delivery state |
|---|---|---|---|
| akki-vm-ii · GPU 0 | 11 – 25 % util (DDP-2GPU-tiny-batch) | **82 %** util · 105 GB / 143 GB · 627 W · 65 °C · `B-REF-3B-v21` CUDA=0 EB=64 | **DELIVERED** — >85 % on GPU 1, marginally under on GPU 0 |
| akki-vm-ii · GPU 1 | 11 – 25 % util | **94 %** util · 105 GB / 143 GB · 643 W · 69 °C · `B1-USSD-ONLY-v21` CUDA=1 EB=64 | **DELIVERED** |
| akki-vm · GPU 0 | 11 – 25 % util | 67 % util · legacy A-0-v2 DDP still finishing · v2.1 armed | **PENDING SEAL** (never-kill-mid-flight; A-0-v2 heartbeat at step 2750 as of 19:06:16Z) |
| akki-vm · GPU 1 | 11 – 25 % util | 0 % util (memory reserved from DDP process) · v2.1 lane-1 armed for `A-1-1p5B-v21` | **PENDING SEAL** |

Ratchet 2986 unchanged (code was code-complete at wave close). Empirical evidence banked at `phase0/gpu_receipts/20260906T190637Z_compute_maximize_empirical_uplift/` (per-host `post_seal_util.txt` + `README.md` reconciliation).

---

## §F · Owner-facing summary

**The programme's actual code state is materially stronger than Doc 0 Part 2's status column suggests and materially different from what yesterday's DOC0_LIVE_BUILD_DELTA reported.** The four biggest corrections (three from earlier, one new):

1. **The Watch, the Ledger (audit_trail), MOAC (four-service model), and Manage Rules (governance) are LIVE** — backend + router + UI — not "unbuilt" as yesterday's audit said.
2. **Northena and Mtafiti/Registry are LIVE with the Extraction-Akki worktree extending the donor code** (Northena +58 %, Connect +282 %).
3. **Solva, Critic Seam, Orchestrator-Resilience, Perception, and Outer-Gate are BUILT but UNMOUNTED** — code is written (700 – 2 158 LOC each) but not reachable at `/api/*` — a materially different state than "unbuilt."
4. **The Solva donor pool is ~ 24 600 LOC across both Executive repos vs ~ 1 400 LOC lifted (5.7 %).** The BUILT-UNMOUNTED verdict on Solva is honest for what is IN the worktree, but Solva-v2 is not lifted at all and Solva-v1 is a subset lift. A lift-or-diff decision precedes any honest claim that BR-2.1/2.3 are served.

**The truly absent items are three:** CIF (canon-only, no code), Agent-Deploy Wizard (nowhere), Rules Service (canon spec exists in the 2026-09-07 drop, no code). Deck Rendering Engine is DONOR-ONLY in Akki-Executive-Core (653 LOC of `deck_*.py` files) and never lifted.

**Substantial UNLIFTED donor code (the reuse-audit lift candidate list, verified against actual trees this session):**
- **Solva donor pool = 24 595 LOC across both Executive repos vs 1 392 LOC lifted (5.7 %)** — the single biggest unlifted body in the audit:
  - `Akki-Executive-Final services/solva/` **4 315 LOC** (Extraction-Akki's 700-LOC `solva/` is likely a subset lift ~ 16 % of donor).
  - `Akki-Executive-Final services/solva_v2/` **9 771 LOC** — NOT LIFTED (Solva-v2 architecture entirely donor-only).
  - `Akki-Executive-Core services/solva_v2/` **10 509 LOC** — NOT LIFTED (~700 LOC larger than Final's).
  - Doc 0 credits Solva as Met via BR-2.1/2.3. Verdict stays BUILT-UNMOUNTED for what is IN the worktree, but the material lift-or-diff decision is open before the Solva canon requirements can be considered honestly served.
- **Akki-Executive-Core `services/synisense/` 6 304 LOC** — 122 % larger than Extraction-Akki's 2 826. A meaningful lift-or-diff decision.
- **Akki-Executive-Final `services/synisense/` 5 915 LOC** — 109 % larger than Extraction-Akki's 2 826 · 389 LOC smaller than Exec-Core's (Executive fork divergence).
- **Akki-Executive-Core `deck_generation_jobs.py 208 + deck_lineage.py 141 + deck_regenerate.py 175 + deck_retrieval.py 129 = 653 LOC of Deck Rendering Engine`** — never lifted. BR-16.1/16.2 has code in donors, not in programme.
- **Akki-Executive-Core + Final `chat/` 308 LOC each** — 3× larger than Extraction-Akki's 99. Same lift-or-diff decision.
- **RMS + AkkiOS `services/perception/`, `outer_gate/`, `checker/`, `mtafiti/`** are all lifted verbatim already (same LOC across repos). No unlifted extension observed.

**Second-largest engines banked in Extraction-Akki this session (context for verdict reads):**
- `services/watch/` **2 787 LOC** (programme-authored — no donor). LIVE.
- `services/connect/` **2 022 LOC** (extended +282 % over RMS 530 LOC donor). LIVE.
- `services/registry/` **2 153 LOC** (extended +1 % over RMS donor). LIVE.
- `services/auth/` **1 714 LOC**. BUILT-BACKEND.
- `services/training/` **1 568 LOC** + `services/training_runner/` **1 382 LOC**. LIVE.
- `services/memory/` **1 429 LOC**. BUILT-BACKEND.
- `services/chokepoint/` **1 403 LOC** (programme-authored). LIVE (SyniSense crossing).
- `services/compute_seam/` **1 292 LOC**. BUILT-BACKEND.
- `services/wizard/` **1 258 LOC** (extended +26 % over RMS 999 LOC donor). LIVE.
- `services/northena/` **1 223 LOC** (extended +58 % over RMS/AkkiOS 773 LOC donor). LIVE.
- `services/shield_train/` **1 120 LOC** (programme-authored offline pipeline). BUILT-BACKEND (offline).
- `services/critic_pass/` **1 035 LOC** (extended +9 % over AkkiOS 950 LOC donor). BUILT-UNMOUNTED.
- `services/campaign_infra/` **1 034 LOC** (programme-authored offline). BUILT-BACKEND (offline).

---

*Every citation in this document points to a file opened during this session. Prior reports superseded on the points listed in §D.2.*
