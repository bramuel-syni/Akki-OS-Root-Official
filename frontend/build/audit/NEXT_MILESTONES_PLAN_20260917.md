READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# NEXT MILESTONES PLAN · toward Akki OS v1.0 compliance · 2026-09-17

**Grounded in**: `AKKI_V1_GAP_ASSESSMENT_20260917.{md,json}` + `M9_SEAL_20260917.md` + `PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md`.
**Byte-identical downloadable copy** at `/app/frontend/public/audit/NEXT_MILESTONES_PLAN_20260917.md`.

**Sequencing principle**: TCB-first, dependency direction downward per v1.0 A.2 (Layer 1 → 2 → 3 → 4 → 5), cross-cutting standards (B.1-B.11) opened as each dependent component needs them. Frontends and real-infra bindings are surfaced as OWNER/INFRA input requests, not proposed as in-pod code.

**No sequencing dates promised.** The v1.0 doc's `D.1 Sequencing by dependency` + `D.4 Decision register` are OWNER territory; this plan proposes shape only and awaits ratification.

---

## MILESTONE M10 · The Ledger (hash-chained single-writer + independent verifier)

**Goal**: Build the B.4 Ledger — the record contract that A.3 governance rule 3 rests on. *"The record is a contract."*

**Closes v1.0 clauses**: **B.4** (hash-chained single-writer + Kafka-fronted durable log + independent verifier binary + nightly chain verification + head hash to per-tenant receipt endpoint) · **C.4** (component spec including break-glass row · row schema · verifier binary · SEV-1 chain-break alerting) · **B.3** (schema versioning for the Ledger row is frozen per major) · touches **B.5** (Ed25519 receipt signing).

**Why first**: A.3 rule 3 is the platform's honesty guarantee. Every downstream refuser + gate needs a real Ledger to emit intents into. Without it, every M9 refusal is preventive-charter-only forever. **This is the highest-leverage TCB build remaining.**

**Scope sketch (waves)**:
- **M10-W1 · Row schema freeze + intent emitter contract**. Freeze the B.4 row shape at schema_version v1: `{seq, prev_hash, hash, schema_version, tenant_id, run_id, task_id, actor_id, actor_type, event_type, resource_type, resource_id, decision, reason_code, payload_ref, at, break_glass_session_id}`. Author `contracts/ledger_v1.py` + JSON schema at `contracts/ledger_v1.schema.json`. Author `services/ledger_emitter/emit_intent.py` (the ONE way for any component to write an intent onto the durable log). AST negative-scan test refuses any other file to write directly to the Ledger collection.
- **M10-W2 · Single-writer service + hash chain**. Author `services/ledger_writer/main.py` — the sole consumer of the intent log. Computes `hash = SHA256(prev_hash || canonical(row))`, appends to a Mongo `ledger` collection (per-tenant DB per B.2 — which is a dependency; see M10 dependency notes below), maintains `ledger_heads` collection.
- **M10-W3 · Independent verifier binary**. Author `tools/ledger_verifier/verify.py` — a separate binary that reads only the durable log + the Ledger collection, recomputes the chain per tenant, and writes head hash + break events to a receipt file at `/app/frontend/public/audit/ledger_heads/<tenant_id>.json`.
- **M10-W4 · Break-glass ceremony rows + Northena convergence blocker**. Convergence in Northena BLOCKS on `ledger_writer` acknowledgement of the closing row per C.2. Break-glass rows carry `break_glass_session_id` non-null. Ceremony (proposal → countdown → countersign → atomic apply) per C.5.
- **M10-W5 · Migration path for existing partial writers**. Northena file-based ledger, memory ledger, audit_trail writer, platform_control_plane/audit_event refuser are retrofit as intent emitters (Commit-A only per §3.3) — no data loss, monotonic seq preserved. Owner-ratifiable back-compat plan per B.3.
- **M10-W6 · SEAL** — wave-close with inline OVERALL BUILD STATUS table.

**Hard dependencies**:
1. **B.2 Mongo-per-tenant (M11) partial dependency**: the `ledger` collection needs to live in the tenant DB (`t_<tenant_id>.ledger`). Can be started with a stub `akki.data` layer that writes to `platform.ledger` for a single default tenant, but proper B.2 comes with M11.
2. **Kafka-compatible durable log (INFRA)**: v1.0 D-08 mandates Kafka-compatible log for ledger.intents.*. **NEEDS OWNER/INFRA INPUT.** Interim: Redis Streams (current per D-08) with acknowledged writes; upgrade path is a shape-preserving swap.
3. **B.5 Ed25519 receipt signing (touched not owned)**: interim HMAC-SHA256 receipts (current chokepoint pattern) + shape-frozen Ed25519 carrier; real KMS-backed Ed25519 lives in M13.

**Owner/infra inputs required BEFORE M10 execution**:
- ☐ Ratify Row schema v1 shape (B.4 lists 16 fields; verify no v1.0 revision drift).
- ☐ Ratify: interim durable log = Redis Streams with `xack` acknowledged writes, OR block M10 on Kafka? Recommend interim Redis with shape-frozen Kafka upgrade.
- ☐ Ratify: verifier binary output path. Proposed `/app/frontend/public/audit/ledger_heads/<tenant_id>.json`.
- ☐ Nightly verifier cadence: default 24h · SEV-1 on chain break.

**Risk / rework notes**:
- **Migration risk (M10-W5)**: existing filesystem ledger rows must map cleanly to the new schema. `northena/ledger.py` row shape (`LedgerRow` from `contracts/northena_ledger.py`) needs a compat mapper. If field semantics differ, this is B.3-major-migration territory — a decision-register entry + 90-day notice per B.3.
- **Kafka vs Redis Streams**: if owner rules on Kafka upfront, M10 delays by the infra-provisioning window. If owner rules Redis Streams interim, M10 unblocks now with a shape-preserving Kafka upgrade downstream.
- **Rework impact if v1.0 revises Row schema post-M10-W1**: full major-version migration + hash chain reset per B.3. High cost. Freezing the row shape at M10-W1 with owner ratification prevents this.

**Honors governing rules**:
- Tests-first RED → double-GREEN byte-match per every CP.
- AST negative-scan tests enforce single-writer + no-direct-Ledger-write outside emitter — matches CP-M7-W2-CP1 (chokepoint AST gate) precedent.
- Preventive-charter: the emitter refuses malformed intents; the writer refuses out-of-order sequences. Runtime hard-gate is the Kafka acknowledged-write itself.
- R-5 seal-chain integrity: per-CP RED/GREEN1/GREEN2 receipts banked at seal time.
- §3.3 3-commit protocol on every code CP; §3.3 2-COMMIT SHAPE on M10-W6 SEAL.
- Zero closed enums, zero data-plane imports, zero domain tokens, frozen dataclass carriers.

---

## MILESTONE M11 · Mongo-per-tenant persistence + `akki.data` repository layer

**Goal**: Bind every M9 shape-frozen carrier + M10 ledger + every runtime component to real MongoDB persistence per B.2 · D-01. Close the biggest T1-tension gap.

**Closes v1.0 clauses**: **B.2** (one DB per tenant `t_<tenant_id>` + platform DB + repo layer with `tenant_id` auto-filter + rejection on cross-tenant write + index-declaration CI check + retention per Annex A) · **D-01** (MongoDB primary datastore) · **B.6** (per-tenant metrics query enforcement leverages B.2's `tenant_id` context) · touches **Annex A** (consolidated data model row-by-row).

**Why second**: Every downstream component's "storage collection" per Annex A stays fictitious without B.2. M10 writes to a single-tenant stub without B.2; every M9 refuser stays runtime-inert without a repository binding.

**Scope sketch (waves)**:
- **M11-W1 · `akki.data` repository primitive**. Author `services/data/repository.py` — the ONE class every service uses for `find/find_one/insert_one/update_one/delete_one/aggregate/count`. Injects `{tenant_id: ctx.tenant_id}` into every filter; rejects writes with mismatched `tenant_id` with `AKKI-DATA-001`. AST negative-scan test refuses any file outside `services/data/` to import Motor's `AsyncIOMotorClient` directly.
- **M11-W2 · Tenant-context signed header (`X-Akki-Context` HMAC)**. B.1 δ-1: HMAC-SHA256 over `(tenant_id, principal_id, request_id, issued_at, ttl)`. Gateway middleware signs; every service dependency verifies. Rejects with `AKKI-AUTH-003`. Closes the v0.2→v1.0 δ-1 gap on M9's shape-only `tenant_context.py`.
- **M11-W3..W7 · Per-collection repository bindings (waves ~5-10 CPs each)**:
  - **W3 · Control-plane collections**: tenant · workspace · user · role_assignment · service_account · role_registry · session · break_glass_session · audit_event · audit_event_types.
  - **W4 · Estate + connector + compute collections**: estate · connector · compute_integration · allocation · task · job · mode_change_approval · connection_test.
  - **W5 · App + wizard + provisioning + theme collections**: app · app_enablement · wizard_session · provisioning_report · theme.
  - **W6 · Perimeter + receipt collections**: perimeter_crossings · pseudonym_maps · tenant_dictionaries · receipts · transform_policies.
  - **W7 · Governance + observability collections**: watch_signals · watch_verdicts · watch_actions · deception_artefacts · certainty_registry · rule_drafts · rule_proposals · rule_registry · tasks · model_candidates · admission_results · model_registry · content_gate_results · content_policies · criteria_sets · moac_evaluations · eligibility_conditions · eligibility_checks · factfulness_verdicts · stamp_audits · qa_findings.
- **M11-W8 · Index-declaration CI + retention TTL job**. Every collection declares its indexes in code (per Annex A `Key indexes` column). CI query-plan check fails build on unindexed query > 100k docs. Retention TTL enforced by a scheduled job per collection's `Retention` column.
- **M11-W9 · Data-plane repository split (connected-tier vs hosted-tier)**. Connected-tier tenants: tenant's MongoDB replica set inside the estate. Hosted-tier: platform cluster with per-tenant DB users. Placement bit on `tenant.tier`. **NEEDS OWNER/INFRA INPUT** for real replica-set + IAM.
- **M11-W10 · SEAL**.

**Hard dependencies**:
1. **MongoDB replica set + IAM (INFRA)**: hosted-tier requires a platform cluster with per-DB users. Connected-tier requires estate MongoDB. **NEEDS OWNER/INFRA INPUT.** Interim: local Mongo container with all `t_<tenant_id>` DBs sharing one instance.
2. **v1.0 D-07 vector storage**: MongoDB Atlas Vector Search (where Atlas is in use) or Pinecone (where already deployed). **NEEDS OWNER/INFRA INPUT**: which per-tenant vector store per tier? Deferred to a sub-wave; M11 doesn't block on vector.

**Owner/infra inputs required BEFORE M11 execution**:
- ☐ Provisioning of MongoDB cluster for platform DB + hosted-tier tenants.
- ☐ IAM policy for per-DB users (one per hosted-tier tenant).
- ☐ For connected-tier pilot tenants (RMS · BDO): confirmed estate MongoDB or agent-side embedded DB choice.
- ☐ Retention values per collection: verify Annex A defaults against pilot-tenant contract terms.
- ☐ Vector store choice (Atlas vs Pinecone) per tier · deferred.

**Risk / rework notes**:
- **T1 tension closes here**. High leverage. Every M9 carrier + M10 ledger + every downstream refuser gets a real persistence layer.
- **Migration**: existing filesystem northena_ledger rows (`phase0/northena_ledger/led-<hex12>.json`) migrate into `t_<default_tenant_id>.ledger` at M10-W5. No user data at risk because M9 shape carriers hold nothing yet.
- **Cross-tenant risk**: the repository layer's `tenant_id` auto-filter + write-mismatch rejection is the primary control. AST + integration tests enforce it. This is the primary control per B.9 adversary 1.

**Honors governing rules**:
- Tests-first per every CP.
- Cross-tenant access suite (P6-CP3 shape-frozen) now becomes a live integration test suite hitting real DBs.
- R-5 receipts per CP.
- AST negative-scan for Motor client access outside repository layer.

---

## MILESTONE M12 · Wire M9 refusers as unroutable runtime chokepoints (T2 close)

**Goal**: Every M9 shape refuser (36 CPs) becomes runtime-enforced — no caller can bypass. Close the T2 tension.

**Closes v1.0 clauses**: **A.3 rule 2** (*"Enforcement happens at chokepoints that cannot be routed around"*) · every M9 CP row in Annex D §12 gets a live enforcement point.

**Why third**: Requires M11 (repository layer + `X-Akki-Context`) as caller context. Requires M10 (Ledger) to write refusal rows. Without those, wiring is premature.

**Scope sketch (waves)**:
- **M12-W1 · FastAPI dependency adapter primitive**. Author `services/enforce/` — one dependency-factory per M9 refuser. Example: `Depends(refuse_if_missing_tenant_context)` wraps `platform_control_plane/tenant_context.py`'s `assert_valid`. Every top-level router gains the dependency via a route decorator.
- **M12-W2 · Gateway middleware for tenant + session + role + task-scope**. ASGI middleware runs P1-CP1 (tenant_context) · P2-CP3 (permission_evaluation) · P4-CP4 (task_scope_enforcement) · P4-CP6 (scheduler_admission) at request time. AKKI-AUTH-* · AKKI-DIR-* refusal codes surface to client per B.11 refusal-surfaced pattern.
- **M12-W3 · Connector mode + wizard + provisioning wiring**. P3-CP3 (connector_mode_lattice) · P3-CP4 (mode_change_approval) · P5-CP4 (wizard_state_machine) · P5-CP5 (provisioning_report) become live gates on their respective HTTP paths.
- **M12-W4 · Audit event emission**. P6-CP1 (audit_event) becomes a live emitter to M10's Ledger writer. Every state-changing API call produces a Ledger row.
- **M12-W5 · Cross-tenant access suite (P6-CP3) becomes CI job**. Runs on every deploy per §4.3 M-H-6. Blocks release on failure. CONTRACT-MODELED item 13 closes.
- **M12-W6 · SEAL**.

**Hard dependencies**:
1. **M10 · Ledger writer** — audit_event emission needs it.
2. **M11 · Mongo persistence + X-Akki-Context** — every refuser needs a real caller context to refuse against.

**Owner/infra inputs required**:
- ☐ Confirm every M9 refuser has a runtime enforcement point mapped (mostly derivable from Annex D §12 acceptance criteria).
- ☐ Cross-tenant CI job placement in the release pipeline.

**Risk / rework notes**:
- **The 36 refusers are already correct in shape**. Wiring is additive per-CP; no rework of sealed M9 modules.
- **Preventive-charter → hard-gate upgrade path** preserved by construction per every M9 CP's seal note verbatim.
- **Test regression risk**: existing BASELINE_GUARD=1 4809-invariant sweep may need extension to cover the new middleware paths. Additive; not a rewrite.

**Honors governing rules**:
- Same tests-first + §3.3 + R-5 + zero-closed-enum + zero-data-plane-imports throughout.
- The 6 human-touchpoint kinds per B.11 (approval · ceremony · confirmation · notification · refusal-surfaced · break-glass) all have concrete adapters here.

---

## MILESTONE M13 · Cross-cutting standards binding (B.5 · B.6 · B.7 · B.8 · B.10)

**Goal**: Land the remaining cross-cutting standards that M10-M12 didn't already close. This is where the TCB.yaml regime lives.

**Closes v1.0 clauses**: **B.5** (KMS + per-tenant master keys + Ed25519 receipts + rotation policy) · **B.6** (OpenTelemetry + per-tenant metrics + error budgets + SLO alerts→runbooks) · **B.7** (Terraform + Helm + signed images + progressive rollout + RPO/RTO backups) · **B.8** (TCB.yaml + `akki.arch` global import assertions CI + determinism byte-identical golden-input corpus + 2-reviewer enforcement in tooling) · **B.10** (SEV taxonomy + runbooks in `akki-runbooks` + post-incident review + capacity mgmt).

**Why fourth**: These are cross-cutting standards. They don't gate M10/M11/M12 completely but they're the audit-readiness layer. Some pieces (B.8 TCB.yaml + `akki.arch`) can start early and land alongside M10/M11.

**Scope sketch (waves)**:
- **M13-W1 · TCB.yaml + `akki.arch` global import-assertions CI**. Author repo-root `TCB.yaml` listing every TCB member per v1.0 A.4 table. Author `tools/akki_arch/check_imports.py` — a CI job that fails the build on: (a) learned package importing decision package; (b) governor importing another governor's decision package; (c) any package importing a layer above it. Extends the chokepoint AST negative-scan pattern to a global check.
- **M13-W2 · KMS + per-tenant master keys + Ed25519**. Real KMS integration (AWS KMS in hosted tier · HashiCorp Vault in connected tier per D-06). Per-tenant master key wrapped by platform root; per-purpose data keys wrapped by tenant master. Ed25519 receipt-signing keys per tenant with public-key publication endpoint. **NEEDS OWNER/INFRA INPUT** for KMS/HSM.
- **M13-W3 · OpenTelemetry + per-tenant SLOs + error budgets**. OTel SDK in every service. Traces + metrics + logs with `tenant_id · run_id · task_id · component`. Per-service SLO from Part C sections. Error-budget tracker halts non-urgent deploys at 50% consumption. Alerts mapped to runbooks (`akki-runbooks` repo).
- **M13-W4 · Terraform + Helm + signed images + progressive rollout**. All infra as Terraform. Helm charts per service. Container images signed; admission controller rejects unsigned. Cohort-progressive rollout (internal → hosted → connected) with automatic SLO-breach rollback. **NEEDS OWNER/INFRA INPUT** for cluster + signing keys.
- **M13-W5 · Determinism byte-identical golden-input corpus for TCB members**. Every deterministic TCB component ships a golden-input corpus. Byte-identical decision output across runs + across versions within a major. Extends the current BASELINE_GUARD=1 byte-match discipline.
- **M13-W6 · 2-reviewer + branch protection**. GitHub branch protection: TCB packages require 2 reviewers, 1 from security group. Tooling-enforced.
- **M13-W7 · SEV taxonomy + runbooks + post-incident review + capacity mgmt**. Every alert mapped to a runbook in `akki-runbooks`. Alert without a runbook fails review. Central pool utilization > 80% for 7 days triggers capacity review.
- **M13-W8 · SEAL**.

**Hard dependencies**:
1. **KMS / HSM (INFRA)** — B.5. **NEEDS OWNER/INFRA INPUT.**
2. **CI infrastructure (GitHub Actions runners + Terraform state store + Vault)** — B.7 + B.8. **NEEDS OWNER/INFRA INPUT.**
3. **Observability backend (OTel collector + metrics/logs/traces store)** — B.6. **NEEDS OWNER/INFRA INPUT** (v1.0 says *"platform's observability backend"* without naming vendor).
4. **`akki-runbooks` repository** — needs creation with initial runbook per every extant SEV-1 alert.

**Owner/infra inputs required**:
- ☐ KMS choice (AWS KMS · HashiCorp Vault · HSM-backed per D-06).
- ☐ Observability backend vendor (OTel-native · e.g., Grafana Cloud · Honeycomb · Datadog).
- ☐ Sign-off on Terraform state store location (S3 backend recommended per D-06).
- ☐ Ed25519 receipt-signing public-key publication endpoint (per-tenant · unauthenticated read).
- ☐ SLO values per service (draft is in Part C sections; owner ratification needed).

**Risk / rework notes**:
- **B.8 R-5 already ratified** — R-5 seal-chain integrity carries some B.8 discipline forward.
- **TCB.yaml can land NOW** (no infra dependency). Consider pulling to run before M10 if owner wants earlier TCB-audit-readiness.
- **KMS migration**: interim per-tenant HMAC (current chokepoint pattern) → KMS wrap-and-store. Shape-preserving; no cryptographic downtime because keys are versioned + never reused.

**Honors governing rules**:
- Same. B.8 discipline codifies what R-1..R-5 + AST gates already do; B.8 makes it CI-mandatory.

---

## MILESTONE M14 · Answering service + Seam contract + Async delivery (C.17) + Mkondo (C.15)

**Goal**: Close the remaining orchestration + integration components. Layer 3 (Mkondo) + Layer 4 (Answering service) come together because they share the hand-off contract shape.

**Closes v1.0 clauses**: **C.15** (Mkondo hand-off registry + hand-off checkpoint · no malformed / dual-hatted hand-off) · **C.17** (answering service + seam contract + async delivery via `asks`/`deliveries`/`webhook_endpoints` collections + polling → real webhooks).

**Scope sketch (waves)**:
- **M14-W1 · Hand-off contract v1** at `contracts/handoff_v1.py`. Shape-freeze. Consume the existing `services/handoff/contracts.py`.
- **M14-W2 · Mkondo registry + checkpoint runtime**. `services/mkondo/registry.py` + `checkpoint.py`. Refuses malformed / dual-hatted hand-offs at request time.
- **M14-W3 · `asks` + `deliveries` + `webhook_endpoints` collections** on Mongo (per M11 repository).
- **M14-W4 · Real async webhook delivery** replaces current polling. Signed with per-tenant Ed25519 (M13).
- **M14-W5 · SEAL**.

**Hard dependencies**: M10 · M11 · M13-W2 (Ed25519).

**Risk**: Low. Most of the shape exists already in `services/handoff/contracts.py` + `services/journey_assistant/` + `services/contract_shells/`.

---

## MILESTONE M15 · Documents suite + wizards (C.22) close-out

**Goal**: Complete the documents suite + shared model + all remaining wizards. Whitepaper Wizard exists; the rest doesn't.

**Closes v1.0 clauses**: **C.22** (documents suite + wizards including brief · report · export · rights-checked · frame-audited).

**Scope**: shape carriers + refusers for each document class + wizard state machine + eligibility gate composition (C.9) + frame precedence per D-12 (org over individual within org scope; individual elsewhere).

**Hard dependencies**: M9 (wizard state machine shape) + M11 (documents collection) + M12 (runtime enforcement).

**Risk**: Medium. Wizard state machine composition against the app enablement + provisioning wizard (M9 P5) needs care.

---

## MILESTONE M16 · CIF (Conditioned Ideation Faculty, C.21) — NEW BUILD

**Goal**: Build CIF from scratch. Currently NOT-STARTED (grep-negative on `services/cif/`).

**Closes v1.0 clauses**: **C.21** (Conditioned Ideation Faculty · idea generation under governance · ideas collection · 12m retention).

**Scope**: cif entity carrier + idea generation contract + composition with Solva reasoning (C.19) + rights-class-aware retention.

**Hard dependencies**: M10 (Ledger) + M11 (Mongo) + M12 (runtime enforcement) + Solva stability (existing).

**Risk**: Medium-high. New surface with unclear scope. Recommend owner-scoping session before M16-W1.

---

## MILESTONE M17 · Tenant applications + personal client (C.23)

**Goal**: Real application-contract enforcement + personal-client-for-tenant-of-one build. Currently: RMS-IQ and Farma IQ surfaces exist as separate repos; contract not enforced.

**Closes v1.0 clauses**: **C.23** (tenant applications + personal client · application contract enforced).

**Scope**: application-contract shape carrier + refuser + composition with app_entity (M9 P5-CP1) + app_enablement (P5-CP2).

**Hard dependencies**: M9 P5 + M11 + M12.

**Risk**: Low-medium.

---

## FRONTENDS (routed to web/Expo specialists — NOT this planning agent)

**Not proposed as in-pod milestones.** v1.0 mandates React + TypeScript for the frontend (D-01 reference stack row). Frontends are:

1. **DAP portal (C.18)** — external acquisition portal · Marion / MER-1 / Meridian AI Research prototype. Owner directive routes this to a web-specialist agent, not this planning agent.
2. **RMS AI Prototype v2 · M. Chen · Compliance surfaces (C.23 tenant app + adjacent WorkStudio · Chat · Data Suite · Documents · ThinkLab · Productivity 360 · Collab · Mentions · Emails · Projects/Tasks · HR Stuff · Performance Management · Exco 360 · Board 360 · Admin).
3. **Admin console** for platform_operator + tenant_owner + tenant_admin roles (Annex D §4.1 · §8.4).

**Handoff shape**: this planning agent surfaces the backend contracts (API paths + response shapes per C.16 · C.17 · C.18 · C.23) as the interface for the frontend agents; frontend agents own the React/Expo implementation.

**Owner action required**: ☐ Confirm frontend routing (web/Expo specialist agents) is separate from this backend-build planning agent's scope.

---

## RECOMMENDED SEQUENCE

**TCB-first · dependency-direction-downward · one milestone open at a time**:

1. **M10 · The Ledger** (hash-chained single-writer + verifier binary) — closes B.4, unblocks every audit_event downstream. **Highest leverage TCB build.**
2. **M11 · Mongo-per-tenant + `akki.data` repository layer** — closes T1, closes B.2/D-01, unblocks every M9 refuser's persistence. **Highest leverage cross-cutting build.**
3. **M12 · Wire M9 refusers as runtime chokepoints** — closes T2, makes the 36 sealed M9 CPs live-enforced.
4. **M13 · Cross-cutting standards binding** (B.5 KMS + B.6 OTel + B.7 Terraform + B.8 TCB.yaml + B.10 runbooks) — closes audit-readiness.
5. **M14 · Answering + Seam + Mkondo** — closes Layer 3 + Layer 4 orchestration.
6. **M15 · Documents suite + wizards** — closes Layer 5 C.22.
7. **M16 · CIF** — closes Layer 5 C.21.
8. **M17 · Tenant applications** — closes Layer 5 C.23.
9. **Frontends** — parallel track under web/Expo specialists once backend contracts stabilise.

**Pull-forward candidate**: M13-W1 (TCB.yaml + `akki.arch`) can land BEFORE M10 to add audit rigor to the M10 build itself. Owner-ratifiable.

**Parallelisable pairs**:
- M14 + M15 (independent contracts).
- M13 sub-waves (B.5 / B.6 / B.7 / B.8 / B.10 land as separate walks once dependencies clear).

---

## NEEDS-OWNER-DECISION / INPUT CHECKLIST

**Owner decisions required before starting M10**:
- ☐ Ratify B.4 row schema v1 shape (16 fields; verify no v1.0 drift from what Annex A lists).
- ☐ Ratify interim durable log: Redis Streams (current per D-08) with `xack` semantics — OR — block M10 on Kafka provisioning.
- ☐ Verifier binary output location · nightly cadence · SEV-1 chain-break wiring.
- ☐ TCB.yaml pull-forward (recommend yes).

**Owner decisions required before starting M11**:
- ☐ MongoDB cluster provisioning (platform + hosted-tier). **INFRA.**
- ☐ IAM policy for per-DB users. **INFRA.**
- ☐ For pilot tenants (RMS · BDO): estate MongoDB confirmed OR agent-embedded DB choice. **INFRA.**
- ☐ Retention values per collection — audit Annex A defaults against pilot MOU terms.
- ☐ Vector store choice (Atlas Vector Search vs Pinecone) per D-07 · deferred to a sub-wave. **INFRA.**

**Owner decisions required before starting M12**:
- ☐ Every M9 refuser → runtime enforcement point mapping (mostly derivable · owner confirmation).
- ☐ Cross-tenant CI job placement in release pipeline.

**Owner decisions required before starting M13**:
- ☐ KMS choice (AWS KMS · HashiCorp Vault · HSM). **INFRA.**
- ☐ Observability backend vendor (OTel-native). **INFRA.**
- ☐ Terraform state store location (S3 backend recommended per D-06). **INFRA.**
- ☐ SLO values per service (Part C draft · owner ratification).
- ☐ `akki-runbooks` repo creation + initial runbook per extant SEV-1 alert.

**Owner decisions required for FRONTENDS**:
- ☐ Confirm handoff to web/Expo specialist agents.
- ☐ DAP + RMS AI Prototype v2 + Admin Console: which agent, which timeline.
- ☐ Backend-contract stability point (recommend: after M12) as gating for frontend start.

**Owner decisions required for CONTRACT-MODELED items 1-15**:
- ☐ K8s cluster + MIG hardware (hosted tier) — items 1, 2 in M9 rollup §7.
- ☐ NetworkPolicy CNI — item 3.
- ☐ Live OIDC/SAML SSO per tenant — item 5.
- ☐ Real PKI + CA for data-plane agent cert issuance — item 6.
- ☐ Real 12h/1h session store — item 7.
- ☐ Break-glass notification transport (email + webhook) — item 8.
- ☐ WCAG-AA contrast library — item 9.
- ☐ KMS envelope encryption per-tenant — item 10.
- ☐ Append-only durable Ledger store (M10 owns this) — item 11.
- ☐ Real storage + wall-clock scheduler for 30-day offboarding delete — item 12.
- ☐ CI cross-tenant suite (M12-W5 owns this) — item 13.
- ☐ Real connector runtime enforcing mode — item 14.
- ☐ Storage namespaced by tenant_id at bucket/prefix/schema (M11 owns bucket/schema; object store choice open) — item 15.

**Owner ratifications still open from prior waves**:
- ☐ R-7 · R-13 · R-14 · R-15 · R-16 · R-17 · BC-3 · BC-4 · S-24.
- ☐ 165 quarantined D1a-1 legacy tests (leave quarantined per owner · confirm continued disposition).
- ☐ Amendment 8 HOLD status.

**Owner-desk items surface every milestone-boundary report (verbatim §Δ6)**:
- BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · admin binds (5 MySQL SGs · RADIO route · transcription server) · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

---

## COMPLIANCE STATEMENT

Every milestone above:
- Honors tests-first RED → double-GREEN byte-match discipline.
- Honors monotonic ratchet + no-silent-rebaselining.
- Honors §3.3 3-commit protocol (or 2-COMMIT SHAPE for state-only closes / SEALs).
- Honors R-1..R-5 seal-chain integrity rules.
- Honors preventive-charter (not enforcement hard-gate) — every refuser is caller-invokable; runtime hard-gate via middleware adapter is additive.
- Honors zero closed enums, 21-token grep-negative, zero data-plane imports, frozen dataclass carriers.
- Honors POST-2 placement (`tenant_id` at field index 1 in every ownership-scoped entity).
- Honors GPU check-in at every seal boundary + zero-perturbation.
- Honors local-commits-only / no-push.
- Honors NO `testing_agent`.
- Honors thin-kernel / no-refactor (only additive CPs).

No sequencing dates promised. No scope reordering without owner ratification. This plan is a **shape-only proposal** awaiting owner decisions on the checklist above.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
