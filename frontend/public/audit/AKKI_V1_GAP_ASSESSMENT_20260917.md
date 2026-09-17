# Akki OS v1.0 · DONE-vs-NOT-DONE Gap Assessment
**Generated 2026-09-17 · read-mostly assessment · no production code changes**

**Uncommitted · outside git tree · matches M8/M9 SEAL "downloadable copy" precedent.**

**Authoritative source**: *Akki OS — System Engineering Reference v1.0* (September 2026, Internal · Confidential). v1.0 supersedes v0.2; v0.2 is now Annex D of v1.0. Fetched into this session from `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/eo8oodof_Akki%20OS%20-%20System%20Engineering%20Reference%20v1.0%20%28Internal%2C%20Confidential%29.docx`.

**Grounding discipline**: every DONE/PARTIAL/NOT-STARTED verdict below is anchored to an on-disk path (module or seal or git log) I actually opened this session. Where I could not find on-disk evidence, the row says so — honesty over completeness.

**Classification legend**
- **DONE** = real runtime code that would enforce the mandate live (not just shape-frozen carriers). Module path + evidence.
- **PARTIAL** = shape-only carriers + invariants only; refusal classes exist; no runtime service actually enforces it OR only a fraction of the required behaviour exists.
- **NOT-STARTED** = no on-disk evidence for this component in this session's inventory.

---

## §1 · LAYER 1 · GOVERNANCE

| # | v1.0 clause | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 1.1 | C.1 | **SyniSense — boundary governor** (chokepoint + inner + outer perimeters + LLM proxy) | **PARTIAL** | `backend/services/synisense/` (config, exceptions, shield, startup_guard, webhook_registration) + `backend/services/chokepoint/llm.py` (491 LOC · SOLE LLM invocation seat with AST gate) + `backend/services/de_identify/tokenize_named_persons.py` + `backend/services/outer_gate/` (mint, receipt, transform) | Inner-perimeter chokepoint + LLM egress allowlist + crossing receipt + purpose gate + masking-tier gate REAL and enforced. Outer perimeter transform/receipt/verify endpoint present but not verified live-tenant. No `perimeter_crossings` Mongo collection per C.1.4 — persistence is file/receipt-based (see T1). |
| 1.2 | C.2 | **Northena — direction governor + run loop** | **PARTIAL** | `backend/services/northena/` (admit, converge, gate, ledger, router, trace_lens · 176 LOC ledger writer) | Admission + gate + convergence surfaces present; append-only writer real (Doc 05 §B5.4). Objective FREEZE (hash), gap re-tasking, and budget convergence per C.2.4 not verified as live enforced services against tenant runs. Ledger writer writes to filesystem JSON, not Mongo (see T1). |
| 1.3 | C.3 | **The Watch — Grey Mirror + Mkono** | **PARTIAL** | `backend/services/watch/` (containment, macho, mark, mirage, mirage_artifacts, mirage_provocation, fitness, certificate_library, capability_admission, continuity, continuity_policy.v0.json, persistence) | Rich present-tense scaffolding: Grey Mirror decoys/canaries (`mirage.py`), Mkono response half (`macho.py`), containment ceilings, fitness. But v1.0 A.4/C.3 places The Watch inside the TCB with certainty registry + verdict signatures — no cryptographic verdict signing found on disk. 62 of 82 security-monitoring requirements were declared unbuilt in D.5. |
| 1.4 | C.4 | **The Ledger** (hash-chained, single-writer, append-only, verifiable) | **PARTIAL** | `backend/services/northena/ledger.py` (append-only file writer · `led-<hex12>.json` per row) + `backend/services/audit_trail/{overview,router}.py` + `backend/services/platform_control_plane/audit_event.py` (frozen carrier · CP-P6-CP1) + `backend/services/memory/{ledger,ledger_reconstructor}.py` | Multiple "ledger-flavoured" writers exist but **no single-writer hash-chained (`hash = SHA256(prev_hash \|\| canonical(row))`) Ledger with independent verifier binary** as B.4 mandates. `platform_control_plane/audit_event.py` is a shape-only append-only refusal wrapper (frozen dataclass · P6-CP1) not a chained writer. **See T3.** |
| 1.5 | C.5 | **Rules Service — policy admin + ceremony** | **PARTIAL** | `backend/services/rules_service/{ceremony, rule_book_library, rule_book_seed.jsonl, rule_enumeration_classifier, rule_registry}.py` | Ceremony engine + registry + seed present. Countdown → countersign → atomic apply not verified end-to-end vs C.5's four-tier discipline (Fast/Standard/Slow/Watch). D.5 marks "Not built" for the Rules Service overall. |
| 1.6 | C.6 | **Model admission gate** | **PARTIAL** | `backend/services/model_admission/{ceremony,router}.py` | Router + ceremony present. Golden-input determinism suite + admission ledger + rerun-on-model-revoke not verified live. D.5 marks "Not built". |
| 1.7 | C.7 | **Output-content gate** | **NOT-STARTED (functionally)** | No dedicated `content_gate/` module. Edge verification exists inside chokepoint's egress allowlist. | D.5: "Edge verification present; internal-boundary placement not built." Confirmed on disk. |
| 1.8 | C.8 | **MOAC (acceptance evaluator)** | **PARTIAL** | `backend/services/targeta/{core,gate,plan,yield_layer}.py` (training-side MOAC) + `backend/services/g1_defensibility/` | Yield-wall / training evaluator present (Targeta side). Extraction/Solva-side acceptance criteria vs frozen criteria_sets not verified as an independent evaluator. D.5: "Training evaluator present; extraction acceptance not built." |
| 1.9 | C.9 | **Eligibility gate** | **PARTIAL** | `backend/services/whitepapers/` (WP wizard tier eligibility present per D.5) + `backend/services/checker/` + `backend/services/eligibility` (grep negative — not found as dedicated dir) | Document-tier eligibility present (per D.5 verbatim). General eligibility (per-recipient rights class vs tenant registry) not verified. |
| 1.10 | C.10 | **Critic Seam — RV-tier + QA-tier** | **PARTIAL** | `backend/services/critic_pass/{harness, manifest_gate, producer_seam, rubric, seeded_defect_corpus, calibration_ledger, archive}.py` + `backend/services/g1_defensibility/stamp_audit.py` | Harness + manifest gate + producer seam + rubric + seeded defect corpus + stamp audit REAL. Not verified whether factfulness verdicts feed the Ledger writer per C.10. D.5: "Verification capability present; record checks and stamp-audit not built." (Partial claim; stamp_audit.py exists so this is somewhat contradicted by disk.) |
| 1.11 | C.11 | **Agent + swarm containment** | **PARTIAL** | `backend/services/agent_containment/{ceilings,serving_freeze}.py` | Ceilings + serving freeze present as modules. Rung ladders + coalition-bound refusal + child-creation refusal + Watch-target refusal per C.11 §5 invariants not verified. D.5: "Not built" is too strong — carriers exist; runtime enforcement not verified. |

**Layer 1 verdict**: 0 DONE · 10 PARTIAL · 1 NOT-STARTED · **~28% DONE-equivalent** (weighted by TCB criticality).

---

## §2 · LAYER 2 · CONTEXT MANAGEMENT

| # | v1.0 clause | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 2.1 | C.12 | **Mtafiti — estate registry** | **PARTIAL** | `backend/services/mtafiti/{asset_inventory, asset_registry_writer, census, composition_census, cost_receipt, declaration, detectors/, executor/, feasibility, feasibility_config.v0.json, floor_feasibility, gpu_discovery_constants, inference}.py` (12+ modules) | Substantial: census, feasibility, detectors, executor, cost receipts, asset registry. Classification + lawful-basis capture not verified per D.5: "connector registration and census discovery present; classification and lawful basis not built." |
| 2.2 | C.13 | **Memory layer** | **PARTIAL** | `backend/services/memory/{constants, ledger, ledger_reconstructor, memory_refusal_reasons.v0.json, plane_registry, publication, refusal, revocation}.py` | Ledger + reconstructor + refusal-taxonomy + plane registry + publication + revocation. Key-scoping enforcement per C.13/D.5 not verified: "Context assembly present; key scoping not enforced." |
| 2.3 | C.14 | **Governed-value taxonomy** | **PARTIAL** | Fragments across `perception/`, `governance/` etc — no dedicated `taxonomy/` module found | D.5 verbatim: "Data classes present as configuration." Not verified as a governed vocabulary enforced at every crossing. |

**Layer 2 verdict**: 0 DONE · 3 PARTIAL · 0 NOT-STARTED · **~40% DONE-equivalent**.

---

## §3 · LAYER 3 · ORCHESTRATION

| # | v1.0 clause | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 3.1 | C.2 | **Northena (orchestration face)** | **PARTIAL** | Same modules as §1.2 above · plus `backend/services/orchestrator_resilience/` | Run-loop present. Full C.2.5 invariants (objective freeze immutability, gap disposition, budget convergence hard-close) not verified as enforced against tenant runs. |
| 3.2 | C.15 | **Mkondo — hand-off registry + platform orchestration** | **PARTIAL** | `backend/services/handoff/contracts.py` only (grep negative on `mkondo/` module directory) | Only `contracts.py` present in `handoff/`. C.15's checkpoint (no malformed or dual-hatted hand-off) not on disk as a runtime enforcer. D.5: "Pending build." |

**Layer 3 verdict**: 0 DONE · 2 PARTIAL · 0 NOT-STARTED · **~20% DONE-equivalent**.

---

## §4 · LAYER 4 · INTEGRATION

| # | v1.0 clause | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 4.1 | C.16 | **Connectors + Connect wizard** | **PARTIAL** | `backend/services/connect/{confirm_router, draft_store, gpu_pipeline_stub, gpu_submit, human_speak, rds_data_router, rds_data_submit, rulebook}.py` + `backend/services/perception/connectors/{archive_reader, cms_reader, social_reader}.py` + `backend/services/data_source/` + `backend/services/connect_estate/` + `platform_control_plane/{connector_entity,connector_mode_lattice,mode_change_approval,connection_test}.py` | Connect surface + connector runtime readers (archive/cms/social) present. Mode enforcement + task-scope enforcement live in M9 platform layer as **shape-only refusal wrappers** (P3-CP2, P3-CP3, P3-CP4, P3-CP5). D.5: "NAS and object store present; read/write mode enforcement and other types not built" — partially contradicted by mode_change_approval.py being a real refusal wrapper. |
| 4.2 | C.17 | **Answering service + seam contract + async delivery** | **PARTIAL** | `backend/services/contract_shells/` + `backend/services/response_sanitizer/` + `backend/services/journey_assistant/` + `backend/services/handoff/contracts.py` | Fragmented across multiple services. D.5: "Synchronous path present; contract partial; async as polling." Consistent with disk. No dedicated `asks/deliveries/webhook_endpoints` collections/services per C.17.4. |
| 4.3 | C.18 | **DAP — external acquisition portal** | **PARTIAL (backend shell only)** | `backend/services/dap/{admission, api_keys, approval, availability, boundary, browse, coalition, commission, disclosure_budget, gates, metering, pruning_unlearning, suspension, terms, trust_boundary, m3_block_completion, m3_remainder}.py` (17 modules) | Rich backend surface with admission/gates/metering/coalition/pruning-unlearning. Full external-party OIDC + party registry + entitlements per C.18 not verified. D.5 verbatim: "Not built." Contradicted by disk — 17 modules exist. Interpretation: modules exist but end-to-end DAP portal (backend + frontend) not verified. |

**Layer 4 verdict**: 0 DONE · 3 PARTIAL · 0 NOT-STARTED · **~40% DONE-equivalent**.

---

## §5 · LAYER 5 · APPLICATIONS + EXECUTION

| # | v1.0 clause | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 5.1 | C.19 | **Solva — reasoning engine + assertion seam + frame** | **PARTIAL** | `backend/services/solva/reasoning.py` + `backend/services/solva_v2/intent_audit.py` + `backend/services/solva_depth/` + `backend/services/g1_defensibility/solva_depth/` + `backend/services/layer_a/ layer_b/ layer_c/` | Five-layer pipeline evidence: layer_a/b/c dirs exist. D.5: "Five-layer pipeline present; seam partial; frame not built; audit log not fed to Ledger." Consistent with disk. |
| 5.2 | C.20 | **Targeta — training + yield wall + custody seam** | **PARTIAL** | `backend/services/targeta/{core,gate,plan,yield_layer,interface}.py` (5 modules) + `backend/services/training_runner/` | Core evaluator + yield gate + plan + interface present. Custody seam + manifests + recipes not verified. D.5: "Evaluator present; custody seam and manifests not built." Consistent with disk. |
| 5.3 | C.21 | **CIF — Conditioned Ideation Faculty** | **NOT-STARTED** | Grep negative on `services/cif/` — no dedicated directory. `backend/services/campaign_infra/` is unrelated. | D.5: "Not built." Confirmed on disk. |
| 5.4 | C.22 | **Documents suite + wizards** | **PARTIAL** | `backend/services/whitepapers/` + `backend/services/wizard/` + `backend/services/doc0_attributes/{audit_au3,tcb}.py` + `backend/services/transform_forms/` + `backend/services/skill_files/` | Whitepaper Wizard present per D.5 verbatim. Shared model partial per D.5. Frontend surfaces for document creation not verified against C.22 §3-5. |
| 5.5 | C.23 | **Tenant applications** | **PARTIAL** | `backend/services/tenant_apps` (grep negative — not found as a dedicated dir). RMS-IQ-Core-2 repo has its own frontend/src/pages. Application contract enforcement missing. | D.5: "RMS-IQ and Farma IQ surfaces exist; application contract not enforced; personal client not built." Consistent with disk (RMS-IQ-Core-2 exists as a separate repo). |

**Layer 5 verdict**: 0 DONE · 4 PARTIAL · 1 NOT-STARTED · **~25% DONE-equivalent**.

---

## §6 · CROSS-CUTTING B.1–B.11

| # | v1.0 clause | Standard | Status | Evidence on disk | One-line note |
|---|---|---|---|---|---|
| 6.1 | B.1 | **Identity, authentication, authorisation** (5 principals · OIDC/SAML · MFA · mTLS agents · double-authz) | **PARTIAL** | `backend/services/auth/` (16 files · user_store · password_hash · jwt_service · session_binding · engineer_key_grant + ledger + service · demo_identity_seeder · auth_refusal · dependencies · identity · engineer_invites · engineer_scope · key_grants) + `platform_control_plane/{tenant_context, role_registry, role_assignment, permission_evaluation, session_binder, break_glass_session, user_entity, service_account_entity}.py` (M9 P1+P2) | JWT + password hashing + user store on Motor Mongo. `X-Akki-Context` HMAC signed context per B.1 not verified — M9 tenant_context.py is a shape refuser only. **Five principal types not aligned to M9's seven roles — see T7.** MFA + WebAuthn + IdP federation not verified live. |
| 6.2 | B.2 | **Tenancy + data isolation in MongoDB** (DB-per-tenant · repo layer · index CI · retention) | **NOT-STARTED (per spec)** | `backend/services/auth/user_store.py` uses Motor Mongo for USERS ONLY. Grep negative on `t_<tenant_id>` collection convention. M9 platform layer modules are frozen dataclasses (no persistence). Northena ledger writes to filesystem JSON. Memory layer's `ledger.py` also file-based. | **Directly contradicts D-01 "MongoDB, one DB per tenant".** Only the auth `users` collection is on Mongo. Everything M9 built is shape-only carriers with zero persistence layer. See T1. |
| 6.3 | B.3 | **Contracts, versioning, compatibility** (path versioning · schema_version · JSON Schema · Idempotency-Key) | **PARTIAL** | `backend/contracts/` directory exists at repo root. `contracts/northena_ledger.py` referenced by ledger.py. No `akki-contracts` repo/CI schema validation found. `Idempotency-Key` grep negative across services. | Schema-version discipline present in some places (ledger row). Path-versioning `/v1/` not verified. Idempotency-Key not implemented. |
| 6.4 | B.4 | **The Ledger standard** (single writer · SHA256 hash chain · verifier binary · nightly chain verification) | **NOT-STARTED (per spec)** | See §1.4 above. Multiple "ledger-flavoured" writers (northena, memory, audit_trail); none is a single-writer hash-chained + independent verifier per B.4. `platform_control_plane/audit_event.py` (P6-CP1) is shape-only append-only refusal wrapper. | **The Ledger as B.4 specifies it — hash-chained single-writer verifier — DOES NOT EXIST on disk.** See T3. |
| 6.5 | B.5 | **Secrets, keys, cryptography** (KMS · per-tenant master keys · TLS 1.3 · mTLS · Ed25519 receipts) | **NOT-STARTED** | Grep negative on Ed25519 · no KMS integration found · no per-tenant key-rotation code. `chokepoint/llm.py` fetches provider credentials from a secrets manager stub. `outer_gate/receipt.py` exists but signature scheme not verified as Ed25519. | Real KMS + per-tenant master key hierarchy + rotation policy per B.5 not built. |
| 6.6 | B.6 | **Observability + SLOs** (OpenTelemetry · per-tenant metrics · error budgets · alerts→runbooks) | **NOT-STARTED** | Grep negative on `opentelemetry` imports. No SLO definitions on disk. No error-budget tracker. No alert→runbook mapping. | Not built. |
| 6.7 | B.7 | **Deployment, environments, upgrade** (Terraform · Helm · signed images · progressive rollout · RPO/RTO) | **NOT-STARTED** | No `terraform/` or `helm/` charts in Extraction-Akki repo. No signed-image admission controller. Repo has GitHub workflows for CI, no Terraform state. | Not built. |
| 6.8 | B.8 | **TCB engineering rules** (TCB.yaml · import assertions · determinism byte-identical tests · 2-reviewer) | **PARTIAL** | `backend/services/doc0_attributes/tcb.py` (single-file TCB marker per attribute). **No repo-root `TCB.yaml`.** `services/chokepoint/llm.py` **HAS** an AST negative-scan test enforcing sole importer rule (M9 CP-M7 precedent). `backend/tests/invariants/` has 4809 invariants including many determinism / structure checks. | AST gate for chokepoint LLM: REAL. TCB.yaml + import-assertion CI job: NOT-STARTED. Determinism byte-identical golden-input corpus: NOT-STARTED. 2-reviewer TCB rule: not enforced in tooling. See T6. |
| 6.9 | B.9 | **Threat model** (4 adversaries · malicious tenant · compromised model · insider · compromised agent) | **PARTIAL** | Watch modules address adversary 4. `chokepoint/llm.py` + purpose gate + masking tier address adversary 2. Break-glass carrier (P2-CP5) + cross-tenant refusal suite (P6-CP3) address adversaries 1+3. | Threat model DOCUMENTED implicitly across modules; NOT written as a single artefact matching B.9. |
| 6.10 | B.10 | **Operations, runbooks, incident response** (SEV-1/2/3 · runbooks · post-incident review · capacity mgmt) | **NOT-STARTED** | Grep negative for `runbook` in `akki-runbooks` or repo. No SEV taxonomy on disk. | Not built. |
| 6.11 | B.11 | **Human touchpoint standard** (approval · ceremony · confirmation · notification · refusal-surfaced · break-glass) | **PARTIAL** | Approval: `platform_control_plane/mode_change_approval.py` (real shape refuser). Ceremony: `rules_service/ceremony.py` + `model_admission/ceremony.py`. Break-glass: `platform_control_plane/break_glass_session.py` (P2-CP5). Refusal-surfaced: every M9 module carries COUNTS-only refusal bodies. Notification: NOT-STARTED. Confirmation: partial via `wizard/`. | 5 of 6 touchpoint kinds have some shape; notification pipeline missing. |

**Cross-cutting verdict**: 0 DONE · 5 PARTIAL · 6 NOT-STARTED · **~18% DONE-equivalent**.

---

## §7 · ANNEX D · PILOT TENANCY (= M9 what was built)

Annex D of v1.0 is v0.2 verbatim. This section maps every M9 phase against the Annex D clause + notes any v1.0 normative CHANGE that would rework what M9 sealed.

**M9 sealed state (verified from `phase0/output_verified_seals/` + git log `programme/track-a` this session)**:
- 36 code CPs + 1 wave-close · ratchet arc 4433 → 4809 (+376) · zero rollback · master HEAD `0c7634e8`.

| # | M9 phase / CP | v1.0 Annex D clause | Status | v1.0 normative changes vs v0.2? |
|---|---|---|---|---|
| 7.1 | P1-CP1 · TENANT-CONTEXT-ENFORCEMENT | §4.3 | **PARTIAL (shape-only)** | v1.0 B.1 mandates `X-Akki-Context` HMAC-SHA256 signed header — **NEW normative in v1.0**. M9's shape refuser at `platform_control_plane/tenant_context.py` does not sign/verify. Rework required. |
| 7.2 | P1-CP2..CP5 · TENANT / WORKSPACE / USER / SERVICE-ACCOUNT entities | §10 verbatim | **PARTIAL** | v1.0 Annex A + B.1 tighten field discipline (user MFA enrol · service_account cert fingerprint · certificate rotation 24h at 50% lifetime). M9 carriers align to §10 field lists; no rework of shape. mTLS + cert issuance is new work downstream. |
| 7.3 | P1-CP6 · TENANT-LIFECYCLE-FSM | §4.7 | **PARTIAL** | v1.0 §4.7 unchanged from v0.2. Terminal `offboarded` state + 30-day irreversible-delete refusal composes with P6-CP5. |
| 7.4 | P2-CP1..CP4 · ROLE-REGISTRY / ROLE-ASSIGNMENT / PERMISSION-EVAL / SESSION-BINDER | §7.3 · §7.4 · §7.2 | **PARTIAL (shape-only)** | v1.0 §7.3 unchanged. **v1.0 B.1 introduces 5-principal model** (platform_operator/user/service_account/data_plane_agent/external_party). **M9's 7 roles are TENANT-INTERNAL RBAC** — different axis. Not a rework; they layer together (see T7). |
| 7.5 | P2-CP5 · BREAK-GLASS-SESSION | §7.8 | **PARTIAL** | v1.0 §7.8 unchanged. M9 shape carrier + 4-refusal rules match. Real notification pipe (webhook/email) missing. |
| 7.6 | P3-CP1..CP5 · ESTATE / CONNECTOR / CONNECTOR-MODE-LATTICE / MODE-CHANGE-APPROVAL / CONNECTION-TEST | §5 | **PARTIAL (shape-only)** | v1.0 §5 unchanged. M9 shape refusals composed correctly. Real connector runtime enforcing mode = CONTRACT-MODELED item 14. |
| 7.7 | P4-CP1..CP8 · COMPUTE-INTEGRATION / ALLOCATION / TASK / TASK-SCOPE-ENFORCEMENT / TASK-INVALIDATION / SCHEDULER-ADMISSION / METERING-LEDGER / PREEMPTION-CONTRACT | §6 | **PARTIAL (shape-only)** | v1.0 §6.4 unchanged. K8s namespace + MIG partitions + NetworkPolicy = CONTRACT-MODELED items 1-3 · not real. |
| 7.8 | P5-CP1..CP6 · APP-ENTITY / APP-ENABLEMENT / APP-REVALIDATION / WIZARD-STATE-MACHINE / PROVISIONING-REPORT / THEME-ENTITY | §8 · §9 | **PARTIAL (shape-only)** | v1.0 §8-9 unchanged. Wizard FSM shape-frozen; real wizard-runner service not verified vs `wizard/` module. |
| 7.9 | P6-CP1 · AUDIT-EVENT-ENTITY | §10 + §7.7 (append-only) | **PARTIAL (shape-only)** | v1.0 B.4 elevates append-only audit to **hash-chained Ledger standard** — SEE T3. M9's P6-CP1 shape refuser does NOT satisfy B.4; would need to feed a real single-writer chain. **Not rework of P6-CP1 itself; downstream work.** |
| 7.10 | P6-CP2 · AUDIT-EVENT-TYPES | §7.7 event list | **PARTIAL (shape-only)** | v1.0 Annex B expands the event catalogue substantially (`perimeter.*`, `run.*`, `watch.*`, `ledger.*`, `rule.*`, `task.*`, `model.*`, `content.*`, `moac.*`, `eligibility.*`, `critic.*`, `agent.*`, `estate.*`, `job.*`, `solva.*`, `targeta.*`, `authn/z.*`). **v1.0 introduces MANY new event types beyond v0.2 §7.7's 12.** M9's frozen vocabulary of required audit event types is a SUBSET of v1.0. Would need widening. |
| 7.11 | P6-CP3 · CROSS-TENANT-ACCESS-SUITE | §4.3 + §12 acceptance criterion 2 | **PARTIAL (shape-only)** | v1.0 §12.2 unchanged. Refusal aggregator at 6 planes shape-frozen. Real cross-tenant runtime suite = CONTRACT-MODELED item 13. |
| 7.12 | P6-CP4 · PILOT-TENANT-REGISTER | §11 verbatim | **PARTIAL (shape-only)** | v1.0 §11 unchanged (4 tenants: RMS, DigiCow, BDO, Trinity). |
| 7.13 | P6-CP5 · SANDBOX-OFFBOARDING | §4.7 (30-day irreversible-delete) | **PARTIAL (shape-only)** | v1.0 §4.7 unchanged. Evidence carrier (cert-rev / alloc-return / artefact-delete) shape-frozen. Real storage/scheduler binding = CONTRACT-MODELED item 12. |
| 7.14 | P6-CP6 · M9-SEAL | Wave-close (not a code CP) | **DONE (as a wave-close)** | Not a code component; documentation artefact. |

**Annex D verdict**: 1 DONE (wave-close) · 13 PARTIAL (all shape-only carriers, zero runtime enforcement, zero Mongo persistence per D-01) · 0 NOT-STARTED.

**Annex D normative deltas vs v0.2 that touch sealed M9 work**:
- **Δ-1** · `X-Akki-Context` HMAC-SHA256 signed context header (B.1) — new obligation on tenant_context.
- **Δ-2** · Append-only audit → hash-chained Ledger (B.4) — audit_event downstream.
- **Δ-3** · Event catalogue widening (Annex B) — audit_event_types vocabulary is now a subset.
- **Δ-4** · 5-principal identity model (B.1) — new axis alongside 7-role RBAC.
- **Δ-5** · Contract schema-versioning + Idempotency-Key (B.3) — new obligation on every state-changing surface.
- **Δ-6** · Determinism byte-identical golden-input tests + TCB.yaml + import-assertions (B.8) — new tooling obligation.
- **Δ-7** · Retention rules per Annex A (some tightened vs v0.2 §7.7's 12-month blanket).

**None of these deltas invalidate any sealed M9 CP.** They add new work downstream. Sealed M9 CPs remain correct-in-shape.

---

## §8 · FRONTENDS

| # | Component | Status | Evidence on disk | One-line note |
|---|---|---|---|---|
| 8.1 | **DAP portal (Marion / MER-1 / Meridian AI Research)** — v1.0 C.18 | **NOT-STARTED (as a live React/Expo app)** | Prototypes on disk: `/app/assessment_workspace/canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html` (230577 bytes · sha256 `d0fc1b49...`). URL-provided version (240645 bytes · sha256 `466c9f84...`) **DIFFERS** from on-disk version (10 KB delta · different SHA). | Standalone HTML mockup only. No React/Expo app in Extraction-Akki `frontend/src/pages/` that implements DAP surfaces (Data Estates · Extract · Connect Resources · Data Governance). Backend `services/dap/` (17 modules) is unwired to any frontend. |
| 8.2 | **RMS AI Prototype v2 ACTIVE — M. Chen · Compliance** | **NOT-STARTED (as a live React/Expo app)** | Prototypes on disk: `/app/assessment_workspace/canon/prototypes/20260907_v2_standalone/RMS_AI_Prototype_v2_Standalone.html` (1954907 bytes · sha256 `4199c49f...`). URL-provided version (2281042 bytes · sha256 `71bf9355...`) **DIFFERS** from BOTH on-disk v2 AND on-disk `RMS_AI_Prototype_standalone_v3.html` (2032024 bytes · sha256 `ee6ebe77...`). | Standalone HTML mockup only. WorkStudio · Chat · Data Suite · Documents · ThinkLab · Productivity 360 · Collab · Mentions · Emails · Projects/Tasks · HR Stuff · Performance Management · Exco 360 · Board 360 · Admin — no matching React pages in `Extraction-Akki/frontend/src/pages/` (which has AuthLoginPage · AuthRegisterPage · CanonOSShellPage · ProveDormantPage · TeamDormantPage · audit_trail · commission_view · connect · govern · master_admin · memory · prove · registry · team · trace · use_data — all internal Akki tool surfaces, no M. Chen consumer surfaces). |

**"copy.dc" variants — AMBIGUITY**: Owner directive references "the two 'copy.dc' variants — diff them on disk vs the standalone". Grep across `/app` returns **no files matching `*copy*dc*`**. On-disk variants found are `_v2_Standalone.html`, `_v3.html`, `_v7_Standalone.html`, `_v7_v2_EMBEDDED_APP.html`, `_v7_Standalone_v2.html`, `_v8_Standalone.html`. None labelled "copy.dc". Interpreting "copy.dc" as a shorthand this session cannot resolve without owner clarification. Reporting **honest ambiguity**, not fabricating a match.

**Frontends verdict**: 0 DONE · 0 PARTIAL · 2 NOT-STARTED · **0% DONE**.

---

## §9 · TENSIONS / CONTRADICTIONS

### T1 · JSON-file persistence vs D-01 "MongoDB, one DB per tenant" (+ vector search)

**On-disk finding**: The M9 platform layer's 36 sealed modules under `backend/services/platform_control_plane/` are **frozen dataclasses with zero persistence layer** (verified: `pilot_tenant_register.py` uses `@dataclasses.dataclass(frozen=True)` and imports only `dataclasses` + `typing.Tuple`). **Nothing in M9 persists to Mongo.** The Northena ledger writes to filesystem JSON at `phase0/northena_ledger/led-<hex12>.json` (Doc 05 §B5.4 · `AKKI_NORTHENA_LEDGER_RETENTION_MODE=indefinite` default). Memory layer's `ledger.py` is also filesystem-based. Auth `user_store.py` is the ONE Motor Mongo user against the whole codebase.

**v1.0 D-01 mandate**: *"MongoDB is the primary datastore … one database per tenant for tenant-scoped data (t_<tenant_id>), plus one platform database for control-plane data."*

**Verdict**: **Direct contradiction.** M9 persists nothing to Mongo; Northena persists to files. Pilot storage layer would need to be built (per-collection repositories under a `akki.data` layer per B.2) to close the gap. **Rework impact: HIGH — every M9 carrier needs a repository binding downstream.**

### T2 · Preventive-charter shape-freezing + refusal classes vs v1.0's mandated UNROUTABLE runtime chokepoint ENFORCEMENT

**On-disk finding**: 
- **Real runtime enforcement DOES exist** for the LLM chokepoint: `chokepoint/llm.py` (491 LOC · SOLE LLM invocation seat · AST negative-scan test refuses any other file to import an LLM SDK · crossing receipt per call · purpose + masking-tier + endpoint allowlist gates · scrub of credential-shaped prompts). This is real "unroutable chokepoint" discipline that would enforce live.
- **M9 platform control-plane modules** are preventive-charter shape refusals (frozen dataclass + `assert_X_valid` wrapper that raises refusal classes). Caller invokes them at composition boundary — they are **NOT wired into a service that any request must traverse**. The refusal happens only if some caller invokes the assertion. There's no framework `Depends()`, no ASGI middleware, no import assertion binding all incoming API calls through the M9 refusers.

**v1.0 A.3/A.4 mandate**: *"Enforcement happens at chokepoints that cannot be routed around."*

**Verdict**: **Split.** LLM chokepoint per C.1: **DONE** as an unroutable chokepoint. M9 P1-P6 platform layer: **PARTIAL** — the shapes are frozen and the refusal classes exist, but no service actually enforces them at request time. **Rework impact: MEDIUM — every M9 refuser needs a service adapter (FastAPI dependency / ASGI middleware) to become runtime-unroutable.**

### T3 · The Ledger (hash-chained single-writer append-only verifiable) vs current "seals"/audit_event

**On-disk finding**:
- Multiple "ledger-flavoured" writers exist: `northena/ledger.py` (176 LOC file-based append-only) · `memory/ledger.py` · `memory/ledger_reconstructor.py` · `audit_trail/router.py` · `platform_control_plane/audit_event.py` (P6-CP1 shape refuser).
- **None of them implements B.4's mandate**: `hash = SHA256(prev_hash || canonical(row))` with a single-writer service consuming from a durable log AND an independent verifier binary that reads only the log and the Ledger collection AND publishes head hash nightly.
- The M9 "seals" under `phase0/output_verified_seals/` are TCB-audit artefacts for build-side proof (not the tenant-facing Ledger). They serve a different purpose.

**v1.0 B.4 + C.4 mandate**: *"A component never writes to the Ledger directly. It emits a **ledger intent** onto the durable log; the single Ledger writer consumes intents in order, assigns seq, computes hash = SHA256(prev_hash || canonical(row)), and appends. … Chain verification: an independent verifier … recomputes the chain nightly per tenant and on demand."*

**Verdict**: **Not built.** Multiple partial writers exist; none matches B.4. **Rework impact: HIGH — needs a dedicated Ledger writer service + independent verifier + Kafka-compatible durable log + migration path for existing `northena_ledger` file rows into the chained model.**

### T4 · Frontends absent vs two rich prototypes now provided

**On-disk finding**: 
- Both DAP portal and RMS AI Prototype v2 are provided as standalone HTML/JS blobs (URL and disk versions **DIFFER by SHA-256**). Neither has a React/Expo implementation in any of the four repos' `frontend/src/pages/`.
- Extraction-Akki `frontend/src/pages/` has **internal Akki tool surfaces** (AuthLogin · CanonOSShell · connect · govern · master_admin · memory · prove · registry · team · trace · use_data) — not consumer/analyst surfaces (WorkStudio · Chat · Data Suite · ThinkLab · DAP-facing).
- RMS-IQ-Core-2 repo has its own frontend but is scoped to RMS-IQ (tenant app · C.23) not DAP or the M. Chen prototype.

**Verdict**: **Both frontends NOT-STARTED.** Prototypes are design references, not shipped code. **Rework impact: HIGH — both are Layer-5 delivery surfaces per v1.0.**

### T5 · Contract-modeled infra (K8s/MIG/IdP/PKI/KMS/Kafka/S3/vector) still not real

**On-disk finding**: M9 SEAL rollup §7 lists 15 CONTRACT-MODELED items all shape-frozen at M9 close. Verified this session:
- No K8s manifests / Helm charts in Extraction-Akki repo.
- No MIG partitioning code.
- No IdP integration (SAML/OIDC federation).
- No PKI (Ed25519 signing key management · no per-tenant CA).
- No KMS integration.
- No Kafka-compatible durable log.
- No S3-compatible object storage abstraction.
- No vector storage (MongoDB Atlas Vector Search or Pinecone) integration.

**v1.0 D-04..D-10 mandates**: All above are FIXED decisions.

**Verdict**: **Confirmed as CONTRACT-MODELED only.** No rework of M9 shape; all downstream binding work. **Rework impact: HIGH but PLANNED — this is the post-M9 milestone scope, not a gap in M9 discipline.**

### T6 · TCB regime (TCB.yaml, import assertions, determinism byte-identical tests, 2-reviewer) vs current thin-kernel invariants — what overlaps, what's missing

**On-disk finding**:
- **Overlaps**: 
  - `services/chokepoint/llm.py` HAS an AST negative-scan test (`test_llm_chokepoint_sole_importer`) that refuses any other file to import an LLM SDK. This IS a working import-assertion.
  - M9 invariant fabric (4809 pytest invariants under `tests/invariants/`) enforces zero-closed-enum · zero-domain-tokens · zero-data-plane-imports · positional-index-refusal-body · COUNTS-only-messages · frozen-dataclass-shape. Substantial TCB-style structural discipline.
  - `backend/services/doc0_attributes/tcb.py` per-attribute TCB marker.
  - `phase0/output_verified_seals/` per-CP seal file discipline with §3.3 3-commit protocol.
- **Missing**:
  - **No repo-root `TCB.yaml`** listing all TCB packages by name (grep negative).
  - **No `akki.arch` CI job** running import assertions across all layer boundaries (found: chokepoint's local test; not a global CI job).
  - **No determinism byte-identical golden-input test corpus** — M9 uses `BASELINE_GUARD=1` ratchet floor byte-match on counts, not byte-identical decision output across versions.
  - **No 2-reviewer enforcement in tooling** — git config permits any single reviewer to merge.
  - **R-1..R-5 seal-chain integrity rules** (this session's addition, `STANDING_ORDERS.md §7`) address recurrence of the master-chain-lag class of defect but are not the same as TCB rules.

**v1.0 B.8 mandate**: TCB.yaml + import assertions + 100% branch coverage on decision functions + property-based tests + determinism corpus + 2-reviewer.

**Verdict**: **PARTIAL.** Substantial structural discipline in place (chokepoint AST gate + M9 invariants + seal chain); B.8's specific artefacts (`TCB.yaml`, global akki.arch CI, byte-identical determinism corpus, 2-reviewer) not built. **Rework impact: MEDIUM — B.8 tooling to be authored.**

### T7 · B.1 principals (5) vs M9's 7 roles — reconcile

**On-disk finding**:
- **v1.0 B.1 principals (5)** = `platform_operator · user · service_account · data_plane_agent · external_party`. These are the **identity axis** — "what kind of thing is authenticating."
- **M9 P2-CP1 roles (7)** per Annex D §7.3 = `platform_operator · tenant_owner · tenant_admin · data_steward · analyst · viewer · service`. These are the **authorization axis** — "what tenant-internal RBAC role does the principal hold."
- Overlap: `platform_operator` (both) · `service` ≈ `service_account` (roughly · both are non-interactive tenant-bound).
- New in v1.0: `data_plane_agent` (mTLS agent inside connected-tier estate) · `external_party` (DAP-only registered outsider).

**Verdict**: **Not a contradiction — different axes.** The B.1 principals answer "who is the caller"; the D §7.3 roles answer "what may this user do inside this tenant." They compose. `data_plane_agent` and `external_party` are new principal types M9 did not model. **Rework impact: LOW — new carriers for the two new principal types, no impact on the 7 existing roles.**

### T8 · Any Annex D v0.2 → v1.0 normative deltas that invalidate or require rework of sealed M9 work

**On-disk finding**: Cross-referenced M9's 36 sealed CPs against v1.0 Annex D (=v0.2 verbatim) and v1.0 Parts A + B changes:
- **Zero sealed M9 CP is invalidated** by any v1.0 delta.
- **Every M9 shape-only carrier remains correct-in-shape** at ratchet 4809.
- **New work outside M9 shape**: T1 (persistence) · T2 (runtime chokepoint bindings) · T3 (Ledger writer + verifier) · T5 (real infra) · T6 (B.8 TCB tooling) · T7 (2 new principal types) · Δ-1..Δ-7 above.

**Verdict**: **No rework of sealed M9 work.** All M9 SHAs remain trustable. Downstream milestone scope grows to close the tensions.

---

## §10 · SUMMARY

### Per-layer %DONE estimate (weighted by TCB criticality)

| Layer | %DONE estimate | Notes |
|---|---|---|
| **L1 Governance** | **~28%** | Chokepoint LLM is real; Ledger + Watch + Rules + Gates are shape-only-or-partial. |
| **L2 Context** | **~40%** | Mtafiti + Memory substantial; taxonomy is config-level. |
| **L3 Orchestration** | **~20%** | Northena has real writer; Mkondo is `contracts.py` only. |
| **L4 Integration** | **~40%** | Connectors + DAP backend modules exist; async delivery + DAP frontend absent. |
| **L5 Apps** | **~25%** | Solva/Targeta partial; CIF not started; Documents partial. |
| **Cross-cutting B.1–B.11** | **~18%** | Only B.11 (touchpoints) + B.8 (TCB partial) + B.9 (implicit) have meaningful shape. |
| **Annex D (M9)** | **~90% shape / ~10% runtime** | 36/36 sealed as shape carriers; 0/36 have persistence or runtime enforcement bindings. |
| **Frontends** | **0%** | Both prototypes design-only. |

**Overall estimate**: **~25% DONE-equivalent across the platform** if weighted evenly by component; **~40%** if weighted by TCB criticality (Ledger, Watch, SyniSense, Northena carry heavy TCB weight, and disk shows real code for most).

### Count of DONE / PARTIAL / NOT-STARTED

Cells counted per row above:

| Bucket | Count | Rows |
|---|---|---|
| **DONE** | **1** | Annex D §7.14 (M9 wave-close artefact) |
| **PARTIAL** | **27** | Layer 1: 10 · Layer 2: 3 · Layer 3: 2 · Layer 4: 3 · Layer 5: 4 · Cross-cut: 5 |
| **NOT-STARTED** | **10** | Layer 1: 1 (C.7) · Layer 5: 1 (C.21) · Cross-cut: 6 (B.2, B.4, B.5, B.6, B.7, B.10) · Frontends: 2 |
| **Annex D M9 rows** (not double-counted) | 13 PARTIAL + 1 DONE | All shape-only carriers with correct v0.2 alignment |

### Top 5 tensions ranked by rework impact

1. **T1 · JSON-file persistence vs D-01 Mongo per-tenant** — HIGH impact. Every M9 carrier needs a repository binding; audit/perimeter_crossings/receipts/etc all need Mongo collections. This is the largest post-M9 gap.
2. **T3 · The Ledger (hash-chained single-writer verifier) does not exist as B.4 specifies** — HIGH impact. Multiple partial writers must consolidate to one Kafka-fronted single-writer with an independent verifier. Central to A.3 governance guarantee 3 ("record is a contract").
3. **T2 · Preventive-charter shape refusals not wired as runtime unroutable chokepoints** — MEDIUM impact. Every M9 refuser needs an ASGI/FastAPI adapter to become live-enforced. Not a rewrite; an addition per module.
4. **T5 · CONTRACT-MODELED infra items (K8s/MIG/IdP/PKI/KMS/Kafka/S3/vector) not real** — HIGH but PLANNED. Post-M9 milestone scope. 15 bind-only downstream CPs.
5. **T4 · Both frontends absent** — HIGH impact for tenant delivery. DAP portal + RMS AI Prototype v2 are consumer-facing surfaces required for Layer 5. No React/Expo code exists.

### Honest limits of this assessment

- **URL vs disk prototype SHA mismatch** (T4): the URL-provided DAP and RMS AI Prototype v2 files SHA-differ from the on-disk canon versions. This assessment lists both.
- **"copy.dc" variants**: owner directive references two "copy.dc" variants that grep-negative on disk. Reporting as ambiguity, not fabricating.
- **D.5 build-status-on-record disagrees with disk in places** — D.5 (v1.0) says "DAP: not built" but 17 modules exist under `backend/services/dap/`. Where D.5 and disk diverge, this assessment believes disk and notes the D.5 claim.
- **PARTIAL is a broad bucket**. A component sealed as a shape-only M9 CP + a component with real-but-incomplete runtime code both land in PARTIAL. The evidence column distinguishes them.
- **This assessment did not run any code**. Every verdict is from module presence + module content grep + git log + M9 seal files. No live execution.

---

**End of assessment.** Uncommitted · outside git tree · no push · no code changes to production tree.
