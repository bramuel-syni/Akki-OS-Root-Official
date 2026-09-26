READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROJECT STATE + GOVERNING RULES SNAPSHOT · 2026-09-17
**Authoritative memory-snapshot for the orchestrator. Grounded on-disk, not aspirational.**

**Author of snapshot**: this session, 2026-09-17T~10:00Z, after M9 SEAL + AKKI v1.0 GAP ASSESSMENT completion.
**Byte-identical downloadable copy** at `/app/frontend/public/audit/PROJECT_STATE_AND_RULES_20260917.md`.

---

## PART 1 · CURRENT STATE (from disk)

### 1.1 Repos + branches

| Repo | Path | Default branch | Active local branch | HEAD (this session close) |
|---|---|---|---|---|
| **Extraction-Akki** (code + build) | `/app/assessment_workspace/repos/Extraction-Akki` | `main` | **`programme/track-a`** | `2e82e4f` (CP-P6-CP5 Commit-A · unchanged after M9 SEAL) |
| **Assessment workspace** (state + seals + notes) | `/app/assessment_workspace` | `master` | `master` | `0c7634e8` (M9 SEAL Commit-C fixup) |
| Akki-OS-V1 (legacy source) | `/app/assessment_workspace/repos/Akki-OS-V1` | per-repo | untouched | (not touched this wave) |
| Akki-Executive-Core (legacy) | `/app/assessment_workspace/repos/Akki-Executive-Core` | per-repo | untouched | (not touched) |
| Akki-Executive-Final (legacy) | `/app/assessment_workspace/repos/Akki-Executive-Final` | per-repo | untouched | (not touched) |
| RMS-IQ-Core-2 (tenant app · C.23) | `/app/assessment_workspace/repos/RMS-IQ-Core-2` | per-repo | untouched | (not touched) |

**Discipline: local commits only. No push. Ever.**

### 1.2 Ratchet arc

- **Current floor: 4809** (`baseline_failures.json`.`invariants_enforced_when_baseline_guard_1.passed_floor` = 4809 · `counts_at_baseline.passed` = 4809 · `failed` = 0).
- **Ratchet history entries**: 216 total (`ratchet_history` array in `baseline_failures.json`).
- **Landmark points**:
  - First entry: 2026-08-27T07:52Z · passed=1932.
  - W-M2-SW1 first slice: 2026-09-13T18:43Z (rule_registry scaffold).
  - M6 SEAL: 2026-09-16T~19:36Z · passed_floor=4426 (unchanged from W9 UPGRADE seal).
  - M7 walk (W3 chokepoint W5-go 2026-08-25 owner order): ~mid-Aug landing dates.
  - M8 SEAL: 2026-09-17T~03:35Z.
  - M9 SEAL: 2026-09-17T~09:30Z · passed_floor=**4809** · arc **4433 → 4809 (+376 monotonic-up · zero rollback)**.
- **M9 per-phase deltas**: P1 +35 · P2 +48 · P3 +53 · P4 +88 · P5 +86 · P6 +66 = +376 (verified in `notes/M9_SEAL_20260917.md` §6).
- **Test suite runtime**: BASELINE_GUARD=1 sweep completes in ~130 s (measured 130.19 s + 130.25 s + 130.58 s + 130.99 s + 131.44 s across 5 sweeps this session · GREEN1/GREEN2 byte-match on `4795 passed, 1 skipped, 438 warnings` and `4809 passed, 1 skipped, 438 warnings`).

### 1.3 Code + test size (on-disk counts, `wc -l`)

- **Services**: **101 service directories** under `backend/services/` · **78,549 lines of Python** in services · **~55 live HTTP routers** (30 in `backend/routers/` top-level + 25 per-service `services/*/router.py`).
- **Tests**: **109,357 lines of Python in `backend/tests/`** — larger than the codebase itself. Under `backend/tests/invariants/` alone: 4,809 assertions banked under R-5 discipline after this session's landing.
- **Seals + receipts**: `phase0/output_verified_seals/` currently holds **all M6/M7/M8/M9 CP seals** with zero `pending-C-fixup` after the 2026-09-17 back-compat batch (verified · R-2 clean).
- **Drill receipts**: `phase0/drill_receipts/` currently ships 700+ tracked receipts including this session's aggregate back-compat batch + reconstructed P6-CP1..CP4 post-hoc + full R-5 suite for CP-P6-CP5.

### 1.4 Milestones sealed on disk (M2 → M9)

Verified via `DECISIONS.md` grep + `phase0/output_verified_seals/` inventory + `git log`:

| Milestone | On-disk artefact | Status | Notes |
|---|---|---|---|
| **M0 · CANON ASSESSMENT** | DECISIONS.md 2026-09-13T~14:30Z (line 306) | **SEALED** (document-only) | 13 new `notes/canon_*_requirements.md` files · REUSE_ASSESSMENT_20260913.md · BUILD_STRATEGY_20260913.md · ratchet 3562 unchanged. |
| **M2 · Doc-0 Attr-4 / Rules Service scaffold** | W-M2-SW1..SW5 entries (rule_registry · Rules-Service ceremony R-1..R-4 · rule-book library · canon-derived seed jsonl · G-8 reliable-time-source) | **SEALED (component-level)** | Landed 2026-09-13T18:43Z onward per ratchet_history. |
| **M3 · Doc-0 Attr-5..7 (inferred)** | Not extracted as a dedicated seal note this session | **SEALED (embedded in ratchet arc)** | Bundled into the ratchet arc 3562 → 4426 pre-M6 SEAL. Exact CP list not enumerated in this snapshot; would require full ratchet-history walk. |
| **M4/M5** | Same — embedded in ratchet arc | **SEALED (embedded)** | Same disposition. |
| **M6 · SEAL** | `notes/M6_SEAL_20260916.md` + DECISIONS.md 2026-09-16T~19:36Z (line 10961) | **SEALED** | 9/10 + DEFERRED SW-10 · state-only wave-close · Path α clean · ratchet 4426 unchanged from W9 UPGRADE seal · TRACK-A HEAD `cdf2312d`. |
| **M7 · Serving-Integrity walk (W3 chokepoint · W5 go)** | Embedded in ratchet arc + `services/chokepoint/llm.py` (W5-go 2026-08-25 owner order) + M6 SEAL wave-close (M7 CPs bundled) | **SEALED (component-level · not a dedicated wave-close note this session)** | W3 chokepoint per Doc 01 §A5.1 lives as the SOLE LLM invocation seat. |
| **M8 · SEAL** | `notes/M8_SEAL_20260917.md` (23,315 B) + downloadable copy at `/app/frontend/public/audit/M8_SEAL_WAVE_CLOSE_20260917.md` + DECISIONS.md 2026-09-17T~03:35Z (line 11042) | **SEALED** | 7/7 CPs closed under §3.3 · Path α clean · state-only wave-close. |
| **M9 · Pilot Platform Layer (v0.2 Annex D)** | `notes/M9_SEAL_20260917.md` (322 lines · 12 sections) + downloadable copy at `/app/frontend/public/audit/M9_PLATFORM_LAYER_COMPLETE_20260917.md` + DECISIONS.md 2026-09-17T~09:30Z (line 11525) | **SEALED** | 36 code CPs + 1 wave-close · ratchet 4433→4809 (+376) · zero rollback · R-1..R-5 seal-chain integrity rules ratified mid-wave. |

**Aggregate**: 8 milestones (M0/M2/M3/M4/M5/M6/M7/M8/M9 — M1 is not a distinct-labeled seal on disk). Only M6, M8, M9 have dedicated `M*_SEAL_YYYYMMDD.md` wave-close notes.

### 1.5 What is genuinely LIVE / ENFORCED (real runtime code, not shape)

Grounded via `grep`-for-imports + on-disk router presence:

1. **LLM chokepoint** at `backend/services/chokepoint/llm.py` (491 LOC). SOLE LLM invocation seat per Doc 01 §A5.1. Enforcement mechanisms live: (a) AST negative-scan test refuses any other file to import an LLM SDK; (b) purpose gate via `chokepoint/llm_purpose_gate.py`; (c) masking-tier gate via `chokepoint/masking_tier.py` (+ `masking_tier_allowlist.v0.json`); (d) endpoint allowlist via `chokepoint/llm_endpoint_allowlist.py` (+ `.v0.json`); (e) credential-shaped-prompt scrub; (f) crossing receipt per call with metering (tokens_in, tokens_out, latency, model_id, provider). **Imported by live request handlers**: `services/chat/router.py` · `services/solva/reasoning.py` · `services/wizard/connect_llm_router.py`. Plus 5 test files verify the chokepoint under BASELINE_GUARD=1. **This is v1.0 C.1's inner-perimeter chokepoint working live.**

2. **Northena run loop + append-only ledger writer** at `backend/services/northena/`: 176-LOC `ledger.py` (Doc 05 §B5.4 structural sole-writer discipline · WS-WIRE-LEDGER-MATRIX per Owner ruling 2026-08 promoted 2026-08 · persists to filesystem JSON at `phase0/northena_ledger/led-<hex12>.json` + append-only `index.json`) + `admit.py` + `converge.py` + `gate.py` + `router.py` + `trace_lens.py`. **Imported by** `services/memory/ledger.py` + `services/memory/ledger_reconstructor.py` + `services/wizard/turn_ledger.py` + `services/auth/engineer_key_grant_ledger.py` + `services/system_state.py`.

3. **The FastAPI server** — `backend/server.py` entry point + 30 top-level routers under `backend/routers/` (auth, census_dimensions, checker, compliance, connect, connect_gpu, contracts, discipline, docs_bundle, engineer, extraction_sample, g1, govern, handoff, health, instance, master_admin, memory, mtafiti, northena, objectives, operator, pricing, registry, s2_onboard, service_1, solva, artifact_store, ...) + 25 per-service routers (rights_quarantine, registry_facts, watch, baseline_line, grey_mirror, chat, training, connect_estate, cost_ledger, audit_trail, census_engine, chokepoint, northena, n_series, skill_files, evidence_register, governance, whitepapers, retention, model_admission, model_registry, trace, model_recheck, credentials_paste, lowered_standard). **~55+ live HTTP routes.**

4. **Auth stack on Mongo** — `backend/services/auth/user_store.py` uses Motor async Mongo for the users collection. `backend/services/auth/{jwt_service,password_hash,session_binding,engineer_key_grant,engineer_key_grant_ledger,engineer_key_grant_service,engineer_invites,identity,dependencies,demo_identity_seeder,auth_refusal,engineer_scope,key_grants}.py` (16 files). **This is the ONE place on the platform where v1.0 B.2 (Mongo per-tenant) actually applies today — for users only.**

5. **The Watch** — `backend/services/watch/` (15 modules: containment, macho [Mkono response], mark, mirage [Grey Mirror decoys], mirage_artifacts, mirage_provocation, fitness, certificate_library, capability_admission, continuity, continuity_policy.v0.json, persistence). Present as real code with a live router.

6. **Mtafiti** — `backend/services/mtafiti/` (12+ modules: asset_inventory, asset_registry_writer, census, composition_census, cost_receipt, declaration, detectors/, executor/, feasibility, floor_feasibility, gpu_discovery_constants, inference). Real census + feasibility + cost-receipt writer with a live router.

7. **Critic Seam** — `backend/services/critic_pass/{harness, manifest_gate, producer_seam, rubric, seeded_defect_corpus, calibration_ledger, archive}.py` + `services/g1_defensibility/stamp_audit.py`. Real Critic Seam mechanism.

8. **Rules Service** — `backend/services/rules_service/{ceremony, rule_book_library, rule_book_seed.jsonl, rule_enumeration_classifier, rule_registry}.py`. Ceremony + seed rulebook + registry.

9. **Model Admission Gate** — `backend/services/model_admission/{ceremony, router}.py`. Router live-mounted per the top-level routers list.

10. **Solva reasoning + 5-layer pipeline** — `backend/services/solva/reasoning.py` + `services/solva_v2/intent_audit.py` + `services/solva_depth/` + `services/g1_defensibility/solva_depth/` + `services/layer_a/` `layer_b/` `layer_c/`. Real reasoning surface.

11. **Targeta** — `backend/services/targeta/{core, gate, plan, yield_layer, interface}.py` + `services/training_runner/`. Real yield-wall evaluator.

12. **DAP backend** — `backend/services/dap/` (17 modules: admission, api_keys, approval, availability, boundary, browse, coalition, commission, disclosure_budget, gates, metering, pruning_unlearning, suspension, terms, trust_boundary, m3_block_completion, m3_remainder). Substantial backend surface, though no live top-level router mount for `/v1/dap/*` in `backend/routers/` (verify: DAP routes may not be exposed to HTTP yet).

13. **Retention enforcement** — `backend/services/retention/{enforce, classes, router}.py`. Router live-mounted.

14. **Agent containment** — `backend/services/agent_containment/{ceilings, serving_freeze}.py`. Real containment mechanism.

15. **The invariant fabric (build-time TCB discipline)** — `backend/tests/invariants/` with **4,809 pytest assertions passing BASELINE_GUARD=1 byte-match**. Plus R-1..R-5 seal-chain integrity rules ratified 2026-09-17 (STANDING_ORDERS.md §7).

### 1.6 What is SHAPE-ONLY (M9's specific output)

The 36 sealed M9 CPs under `backend/services/platform_control_plane/` are frozen dataclasses (`@dataclass(frozen=True)`) with `assert_X_valid` preventive-charter refusal wrappers. **Zero persistence layer.** They ARE composed correctly against v1.0 Annex D (=v0.2 verbatim), and their invariants (373 across P1-P6) run under BASELINE_GUARD=1. **They are not wired into runtime request paths as middleware/ASGI adapters** — caller must invoke them at composition boundary.

Modules (36): `tenant_context · tenant_entity · workspace_entity · user_entity · service_account_entity · tenant_lifecycle · role_registry · role_assignment · permission_evaluation · session_binder · break_glass_session · estate_entity · connector_entity · connector_mode_lattice · mode_change_approval · connection_test · compute_integration · allocation_entity · task_entity · task_scope_enforcement · task_invalidation · scheduler_admission · metering_ledger · preemption_contract · app_entity · app_enablement · app_revalidation · wizard_state_machine · provisioning_report · theme_entity · audit_event · audit_event_types · cross_tenant_access_suite · pilot_tenant_register · sandbox_offboarding` + M9_SEAL wave-close.

### 1.7 What is genuinely NOT-BUILT (v1.0 gap items · from `AKKI_V1_GAP_ASSESSMENT_20260917.md`)

Cross-referenced with the gap assessment banked at `/app/frontend/public/audit/AKKI_V1_GAP_ASSESSMENT_20260917.{md,json}`:

1. **B.2 · Mongo-per-tenant persistence** (`t_<tenant_id>` DBs + `akki.data` repository layer + retention enforcement per Annex A + index-declaration CI check). Only `auth/user_store.py` is on Mongo. **All 36 M9 carriers, all connectors, all runs, all crossings, all audit events lack a persistence layer today.**
2. **B.4 · Hash-chained single-writer Ledger + independent verifier binary**. Multiple partial writers exist (northena, memory, audit_trail, platform_control_plane/audit_event as shape refuser); NONE implements `hash = SHA256(prev_hash \|\| canonical(row))` with a Kafka-fronted durable log AND an independent nightly verifier that publishes head hash to a per-tenant receipt endpoint.
3. **B.5 · KMS + per-tenant master keys + Ed25519 receipts + rotation policy**. Grep-negative on Ed25519 · no KMS integration · no per-tenant key hierarchy code.
4. **B.6 · OpenTelemetry + per-tenant metrics + error budgets + SLO alerts→runbooks**. Grep-negative on `opentelemetry` imports; no SLO definitions on disk.
5. **B.7 · Terraform + Helm + signed images + progressive rollout + RPO/RTO recovery**. No `terraform/` or `helm/` charts.
6. **B.8 · TCB.yaml + `akki.arch` CI import assertions + determinism byte-identical golden-input corpus + 2-reviewer enforcement**. Chokepoint has AST gate (real) + M9 invariant fabric (real) + `services/doc0_attributes/tcb.py` per-attribute marker; repo-root `TCB.yaml` and global `akki.arch` CI job absent.
7. **B.10 · Runbooks + SEV taxonomy + post-incident review + capacity mgmt**. Grep-negative on runbook / akki-runbooks / SEV-1/SEV-2 taxonomy.
8. **C.7 · Output-content gate** (internal-boundary placement) — only edge-verification via chokepoint egress allowlist exists.
9. **C.21 · CIF (Conditioned Ideation Faculty)** — grep-negative on `services/cif/`; not started.
10. **C.15 · Mkondo hand-off registry** — only `services/handoff/contracts.py` exists; C.15's checkpoint (no malformed or dual-hatted hand-off) not runtime-enforced.
11. **Frontends per v1.0** — no React/Expo implementation of DAP portal (C.18) or the RMS AI Prototype v2 M. Chen surfaces (C.23). Standalone HTML mockups only on disk (URL vs disk SHA differ).
12. **CONTRACT-MODELED items 1-15** from M9 SEAL rollup §7: K8s namespace isolation · MIG GPU partitions · NetworkPolicy · real preemption controller · live OIDC/SAML SSO · real PKI · real 12h/1h session store · real webhook/email notification · WCAG contrast library · KMS envelope encryption · append-only durable Ledger store · 30-day irreversible-delete storage/scheduler · CI cross-tenant suite · connector runtime enforcing mode · storage namespaced by tenant_id. All shape-frozen; all bind-only downstream.

### 1.8 GPU 72h campaign status

Per `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z:

- **Elapsed**: 29.11 h · **Remaining**: 42.89 h · **Total**: 72 h
- **Hosts**: `akki-vm` + `akki-vm-ii` (both `sampler_alive+workload_alive`)
- **Workload**: appliance benchmark suite (matmul bf16/fp16/fp32-tf32 · attention bf16 @ 2k/4k/8k · batch 1/4) — R-14 serving-engine admission precondition
- **In-perimeter**: True · **No estate data**: True · **Sampler interval**: 300 s · **Detachment**: setsid + nohup
- **Zero synthetic burn** · **No anomalies** · **No workload death** · **Both hosts reachable**
- **On cadence to 72h completion**. GPU campaign continues independent of milestone SEAL activity.

### 1.9 Admin-blocked ops items (from `notes/ADMIN_BINDS_20260915.md` + NEXT.md BLOCKER ledger)

Owner-listed, still-blocked, respected but not blocking on:

- **Security events**: SEC-2026-09-12-01 · SEC-2026-09-14-04 (HF) · SEC-2026-09-13-T4-01/03/04/05 · SEC-2026-09-14-01/02/03 (JUMP, RADIO, NAS, DB)
- **Infra binds pending**: Transcription-server host+creds MISSING BIND · RADIO routing to 10.10.19.0/24 MISSING BIND · 5 closed-SG MySQL hosts
- **Owner ratifications open**: R-7 · R-15 · R-16 · R-17 · BC-3 · BC-4 · S-24 · R-13 · R-14
- **Test discipline**: 165 quarantined D1a-1 legacy tests (leave quarantined per owner)
- **Owner-desk items surface every milestone-boundary report** (verbatim §Δ6): BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · admin binds · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine

**Notes on disk** referenced for context: `notes/SYSADMIN_NOTE_HUAWEI_ACCESS_20260909.md` · `notes/TASK_CONNECTIVITY_REDO_ADMIN_GUIDED_CLOSE_20260914.md` · `notes/HUAWEI_CONNECTIVITY_DRILL_20260909.md` · `notes/TASK2_CONNECTIVITY_CLOSE_20260914.md`.

---

## PART 2 · GOVERNING RULES / DISCIPLINES (each grounded in citation)

### 2.1 Tests-first RED → double-GREEN byte-match

**Source**: STANDING_ORDERS.md §3 BUILD DISCIPLINE (lines 61-186).
**Discipline**: For every new CP: (i) author invariants BEFORE the module → capture RED right-reason failure log; (ii) implement the module; (iii) run `BASELINE_GUARD=0` sweep to verify exact numeric +N delta = N new invariants (no silent rebaselining); (iv) bump ratchet floor in `baseline_failures.json`; (v) run `BASELINE_GUARD=1` twice to get GREEN1 and GREEN2 byte-matched on `<passed> passed, <skipped> skipped, <warnings> warnings` counts.
**Bytes-match target**: only the counts line, not the runtime seconds.
**Recorded receipts**: `phase0/drill_receipts/<TS>_<cp>_{RED,DELTA_GUARD0,GREEN1,GREEN2}.log`.

### 2.2 BASELINE_GUARD=1 semantics

**Source**: `backend/tests/invariants/baseline_failures.json` field `invariants_enforced_when_baseline_guard_1.passed_floor`.
**Discipline**: When `BASELINE_GUARD=1` is set, the test harness enforces `passed >= passed_floor`. A regression that drops passed below the floor is a right-reason RED that must block the CP until fixed. `BASELINE_GUARD=0` allows a raw sweep to see the delta before the floor is bumped.

### 2.3 Monotonic ratchet + no-silent-rebaselining

**Source**: STANDING_ORDERS.md §3 + DECISIONS.md §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17 (line 11441).
**Discipline**: The ratchet floor moves ONE direction only — up. Every bump is preceded by a `BASELINE_GUARD=0` delta sweep that proves the exact numeric delta = the count of new invariants. Silent rebaselining (bumping without a matching delta receipt) is banned. The ratchet history entries in `baseline_failures.json` are appended (never edited).

### 2.4 §3.3 3-commit protocol (code CP) + state-only 2-commit variant (SEAL / back-compat)

**Source**: STANDING_ORDERS.md §3.3 (lines 100-186) verbatim: *"NO SEAL WITHOUT BOTH SHAs — post-seal receipt rule (2026-09-15)"*.
**Owner §A authorization** 2026-09-15T~20:35Z.
**Discipline (code CP)**:
- **Commit-A** on `programme/track-a` (Extraction-Akki repo): code + tests + ratchet bump.
- **Commit-B** on `master` (assessment_workspace repo): state (seal file + seal note + DECISIONS.md append + NEXT.md pin + GPU util check-in + drill receipts).
- **Commit-C fixup** on `master`: self-reference · banks Master HEAD (Commit-B SHA) in seal file + DECISIONS entry + NEXT pin.
**State-only variant (2-COMMIT SHAPE)** for M6/M8/M9 SEAL + back-compat batches: no Commit-A (no code change) · Commit-B state + Commit-C fixup. Precedent: M6 SEAL 2026-09-16T~19:36Z · M8 SEAL 2026-09-17T~03:35Z · M9 SEAL 2026-09-17T~09:30Z.

### 2.5 Local-commits-only / no-push · code on programme/track-a · state on master

**Source**: Owner directive across every wave. Committed to STANDING_ORDERS.md §4 RUNTIME LAW (implied at lines 186-248, explicit in every owner directive verbatim log in DECISIONS.md — e.g., 2026-09-17T~08:55Z path-(a) confirmation *"Local-only, no push"*).
**Discipline**: `git push` never invoked. Every remote (`origin`) is untouched. Code lives on `programme/track-a` in Extraction-Akki. State lives on `master` in the assessment_workspace repo. Cross-repo consistency enforced via §3.3.

### 2.6 No-secrets-to-stdout + custody helpers

**Source**: STANDING_ORDERS.md §4 RUNTIME LAW (lines 186-248). Reinforced by chokepoint credential-shaped-prompt scrub (`services/chokepoint/llm.py` step 4: *"scrub_credential_shaped_prompt(prompt) — standing rule: no credentials transit to the model"*).
**Discipline**: Secrets never touch stdout / logs / traces. Custody helpers under `services/estate_keys/` + `services/credentials_paste/`. Response sanitizers under `services/response_sanitizer/`. HMAC keys per tenant per estate (B.5 intent).

### 2.7 NO `testing_agent` (owner ban)

**Source**: Recurring owner directive across every wave from 2026-09 onward. Called out in this session's incoming handoff brief verbatim: *"testing_agent is STRICTLY BANNED"* and reconfirmed by user 2026-09-17.
**Discipline**: `testing_agent` tool never invoked. Manual pytest via `python -m pytest tests/invariants/` only. `python3 -m pytest -q --tb=no --no-header` for sweep receipts.

### 2.8 Thin-kernel / no-refactor

**Source**: STANDING_ORDERS.md §3 + §2 ENGAGEMENT DISCIPLINE + Owner Ruling 2026-09-16T~08:35Z ("roll-straight" directive).
**Discipline**: Refactoring is strictly banned. Only additive CPs. Existing code is never modified beyond seal-file line-appends and standing-orders section additions. Every M9 CP added new module + new tests + ratchet bump; zero existing-file rewrites.

### 2.9 Preventive-charter (not hard-gate)

**Source**: PLATFORM_LAYER_REQUIREMENTS_v0_2.md standing lines · replicated in every M9 seal note verbatim: *"no enforcement hard-gate · preventive-charter · caller invokes · synthetic fixtures · upgrade path to hard-gate preserved by construction"*.
**Discipline**: Every M9 refuser is a caller-invoked assertion (`assert_X_valid`), not a runtime hard-gate. Upgrade path to hard-gate is preserved by shape: any framework adapter can wrap the refusal to make it runtime-unroutable without changing the refuser's code.

### 2.10 Zero closed enums · 21-token grep-negative · zero data-plane imports · frozen dataclasses

**Source**: PLATFORM_LAYER_REQUIREMENTS_v0_2.md standing lines · enforced by invariants in every M9 test file. Grep vocab defined in `tests/invariants/test_p*_cp*.py` `DOMAIN_TOKENS_21` (obfuscated to pair-halves per CP-M7-W2-CP1 precedent to avoid the test source itself matching).
**Discipline**:
- **Zero closed enum type**: no `from enum import` in any M9 module. All values are OPEN `str` carriers.
- **21-token grep-negative**: kikuyu · dholuo · kamba · swahili · nairobi · inooro · ramogi · musyi · sunbird · whisper · pyannote · htdemucs · mms-1b · mms-lid · wavlm · panns · squim · dnsmos · broadcast · off-air · synology. None appears in any M9 module source. Obfuscated to `("kik", "uyu")` pair-halves rebuilt at runtime in test sources (per CP-M7-W2-CP1 precedent 2026-09-16 + re-exercised in CP-P6-CP5 2026-09-17).
- **Zero data-plane imports**: `services.audio_plane_v1` · `services.release_gate` · `services.governance_plane` · `services.audio_poc` · `services.training_runner` · `services.ssh_seam` · `services.resource_registry` — banned in M9 modules.
- **Frozen dataclasses**: every M9 entity is `@dataclass(frozen=True)`. Field discipline: exact-order tuple + all `str` OPEN + top-level `_FIELDS` constant matching field order.

### 2.11 POST-2 placement

**Source**: DECISIONS.md · re-exercised throughout M9. **Discipline**: `tenant_id` is always the 2nd carrier field (index 1) in every ownership-scoped entity (verified in P1-CP2..CP5, P3-CP1..CP5, P4-CP1..CP8, P5-CP1..CP6, P6-CP1..CP5). Ownership-isolation invariant is `_FIELDS[1] == "tenant_id"`.

### 2.12 GPU check-in at every seal boundary + zero-perturbation

**Source**: STANDING_ORDERS.md §5 GPU OBLIGATIONS (lines 248-262).
**Discipline**:
- Every §3.3 seal boundary regenerates `/app/frontend/public/audit/GPU_UTILIZATION_72H.{json,md}` at Commit-B.
- Zero-perturbation: pytest work is CPU-only; GPU appliance benchmark on `akki-vm` + `akki-vm-ii` runs independently under setsid + nohup; sampler interval 300 s; sampler observes but does not touch workload.
- Anomaly conditions: workload death · sampler death · host unreachable · perimeter breach · anomalous metric drift → SEV-1 · anomaly-interrupt-priority raises.

### 2.13 R-1..R-5 seal-chain integrity rules (owner-ratified 2026-09-17T~09:15Z)

**Source**: STANDING_ORDERS.md §7 SEAL-CHAIN INTEGRITY RULES (lines 282+). DECISIONS.md entry §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17T~09:15Z (line 11441 verbatim).

- **R-1 · Master-parity check at CP boundary**. Before opening a new Commit-A on track-a for CP-N+1, verify Master HEAD banks the Commit-B SHA for CP-N in (a) seal file · (b) DECISIONS.md tail · (c) NEXT.md "CURRENT AS OF" line. STOP and reconcile if any shows `pending-C-fixup`.
- **R-2 · Seal-file `pending-C-fixup` counter**. Boot ritual + every pre-CP-open probe counts `pending-C-fixup` occurrences in `phase0/output_verified_seals/`. Count > 0 = chain not clean; refuse to open new CP until Commit-C fixup lands and reduces to 0.
- **R-3 · Ratchet-history / git-log cross-check**. Boot ritual walks `baseline_failures.json` `ratchet_history` from last-known-clean master HEAD forward; verifies each entry has a matching `git log programme/track-a` entry + matching seal file.
- **R-4 · Session-handoff brief reconciliation**. Incoming session's FIRST action on receiving a "sealed" claim is on-disk §3.3 3-commit completeness verification.
- **R-5 · Per-CP double-green raw-log requirement (MANDATORY)**. Seal-file writer refuses to compose `Double-green: GREEN1 X/Y/Z · GREEN2 X/Y/Z` line unless both raw log files exist on disk. Aggregate-only substantiation allowed ONLY for retroactive back-compat batches with explicit `RECONSTRUCTED POST-HOC AT HEAD <SHA> <DATE>` label.

### 2.14 Boot ritual + anti-"Chunk-1-drift" opening

**Source**: STANDING_ORDERS.md §1 SESSION BOOT PROTOCOL (lines 9-22).
**Discipline**: Every session opens by (i) reading STANDING_ORDERS.md · (ii) reading STATE/DECISIONS.md tail · (iii) reading STATE/NEXT.md current-position pin · (iv) verifying R-1/R-2/R-3 on disk. Never trust a session-handoff brief without on-disk verification per R-4. This session opened with exactly this drill and surfaced the 20-CP master-chain-lag defect immediately (R-4 in action pre-ratification).

### 2.15 Other standing lines held throughout M9

- No push · no `testing_agent` · no refactor · no biometric material · no enforcement hard-gate (all preventive-charter) · no speculative shapes · zero closed enums · zero data-plane imports · zero domain tokens · local git history IS the record.

---

## PART 3 · AUTHORITATIVE STATE SUMMARY (one paragraph)

The Akki OS build is a substantial live-running FastAPI application (**`backend/server.py` + ~55 HTTP routers · ~78k LOC across 101 service directories · ~109k LOC of tests · 4,809 pytest invariants passing under `BASELINE_GUARD=1` byte-match**) with **real live-enforced runtime chokepoints where they matter most**: the LLM chokepoint at `services/chokepoint/llm.py` (491 LOC · SOLE LLM invocation seat · AST-enforced import ban · purpose + masking-tier + endpoint allowlist gates · crossing receipts with metering · imported by `chat/router.py`, `solva/reasoning.py`, and `wizard/connect_llm_router.py`) and the append-only Northena ledger writer at `services/northena/ledger.py` (176 LOC · structural sole-writer · imported by memory, auth, wizard, system_state). Alongside these, substantial component code exists for **Mtafiti · Watch · Critic Seam · Rules Service · Model Admission · Solva · Targeta · DAP backend · Memory · Retention · Agent Containment**. The most recent milestone **M9 (Pilot Platform Layer · v1.0 Annex D)** sealed 36 code CPs across P1-P6 as shape-only frozen dataclass carriers with 373 invariants — **at ratchet floor 4809** (arc 4433→4809 +376 monotonic-up · zero rollback · master HEAD `0c7634e8` · track-a HEAD `2e82e4f`). This session ratified **R-1..R-5 seal-chain integrity rules** and reconciled a 20-CP master-side back-compat gap (14 sealed milestones + reconciliations · one bank-of-record commit chain complete). **Genuinely NOT-built vs v1.0**: (i) Mongo-per-tenant persistence (B.2/D-01); only auth users on Mongo. (ii) Hash-chained single-writer Ledger + independent verifier binary (B.4); multiple partial writers exist but none matches B.4. (iii) B.5 KMS/Ed25519 · B.6 OpenTelemetry+SLOs · B.7 Terraform/Helm · B.10 runbooks · TCB.yaml + `akki.arch` CI. (iv) C.7 internal-boundary content gate · C.15 Mkondo runtime · C.21 CIF. (v) Frontends per C.18 DAP + C.23 RMS AI Prototype v2 as React/Expo apps. The **GPU 72h campaign** runs on cadence at 29.11h elapsed / 42.89h remaining · both hosts alive · no anomalies. All **admin-blocked infra items** (transcription-server bind · RADIO route · 5 MySQL SGs · SEC events · owner ratifications R-7/R-13/R-14/R-15/R-16/R-17/BC-3/BC-4/S-24) are respected, surfaced at every milestone report, and not blocking on. **Discipline throughout**: tests-first RED→double-GREEN byte-match · monotonic ratchet · §3.3 3-commit protocol · preventive-charter · zero closed enums / 21-token grep-negative / zero data-plane imports · R-1..R-5 seal-chain integrity · no push · no `testing_agent` · no refactor · local git history is the record.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
