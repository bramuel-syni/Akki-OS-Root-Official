READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# NEXT MILESTONES PLAN · toward Akki OS v1.0 compliance · 2026-09-17 (revised 20:30Z)

**Revised 2026-09-17T~20:30Z** to bank owner corrections to sequence + expanded M10 scope + new M12b + D.3 acceptance suite as ratcheted deliverable.

**Grounded in**: `AKKI_V1_GAP_ASSESSMENT_20260917.{md,json}` · `M9_SEAL_20260917.md` · `PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md` (revised same day).

**Byte-identical downloadable copy** at `/app/frontend/public/audit/NEXT_MILESTONES_PLAN_20260917.md`.

**Sequencing principle**: TCB-first, but ordered by v1.0 D.1 dependency direction and B.3 forbidden-migration rule.

---

## 0 · DEFINITION OF DONE (repeated for every milestone below)

Every milestone from M10 seals **only** when:

1. Every spec invariant it closes (C.n I-x) is mapped to a test ID and passing under `BASELINE_GUARD=1`.
2. The D.3 platform tests it enables (P-nn) pass.
3. Affected components are re-levelled on the Evidence Bar L1-L5.
4. D.5 is regenerated from the levelled table.
5. The milestone's Ledger rows are visible end to end.

Evidence Bar: L1 code · L2 wired on HTTP · L3 named-invariant test IDs · L4 fail-closed runtime · L5 in CI ratchet. **Nothing above L2 without L3 evidence.**

---

## 1 · REVISED SEQUENCE (owner corrections banked verbatim)

**New order**: **M13-W1 → M11 → M10 → M12 → M12b → remaining M13 sub-waves → M14 ∥ M15 → M16 → M17.** Frontends out-of-band, gated at M12 completion. M16 CIF stays last and owner-scoped.

**Why this order** (per owner corrections 1-5):
1. **M13-W1 (TCB.yaml + `akki.arch`) is MANDATORY FIRST**, not optional. Ledger and repository layer are TCB builds → they land under B.8 review or they don't count.
2. **M11 precedes M10**. The Ledger lives in `t_<tenant_id>` databases with an insert-only writer role **per database** (C.4 + B.2). If M10 built on a shared DB first, migration to per-tenant DBs later would be a prohibited Ledger-collection migration (B.3 forbids Ledger row-schema migrations; B.7 forbids schema breaks in blue-green rollout).
3. **M10 scope MUST include**: rehoming `northena/ledger.py` to C.4 (Northena reduced to an intent emitter); the change-stream watcher; the insert-only role per tenant DB; the genesis hash per tenant; the verifier binary as a SEPARATE process. **Exit gate**: P-06, P-07, and C.4 I-1..I-6 at L5.
4. **M12b · "Governance invariants to L5"** inserted immediately after M12. Names C.3 · C.5 · C.6 · C.10 · C.11 · C.16 · C.19 · C.20. **Exit gate**: P-04, P-05, P-08, P-09, P-14, P-15.
5. **D.3 acceptance suite is a DELIVERABLE**, ratcheted from M10. P-01, P-02, P-03 land with M11/M10; the suite grows monotonically and runs **IN FULL before every seal**.

---

## 2 · MILESTONE M13-W1 · TCB.yaml + `akki.arch` global import assertions CI (MANDATORY FIRST)

**Goal**: Establish the B.8 TCB review regime before any TCB build (Ledger, Mongo repo). No milestone lands without `akki.arch` green.

**Closes v1.0 clauses**: **B.8** (TCB.yaml enumerates TCB packages; import assertions codified as a CI job; 2-reviewer branch protection on TCB paths).

**Scope sketch (single-wave · single-CP style)**:
- **CP-M13W1-C1 · TCB.yaml at repo root**. Enumerate every TCB package by name per v1.0 A.4 table: `services/chokepoint/*` · `services/ledger_writer/*` (future M10) · `services/watch/*` · `services/rules_service/*` · `services/model_admission/*` · `services/critic_pass/*` · `services/solva/reasoning*` (frame boundary only) · `services/agent_containment/*` · `services/data/*` (future M11) · `services/enforce/*` (future M12) · every M9 `platform_control_plane/*` module · `contracts/*`. Also enumerates the specific 2-reviewer path patterns + the security-group reviewer requirement.
- **CP-M13W1-C2 · `tools/akki_arch/check_imports.py`** — a script that reads `TCB.yaml` and walks every Python file. Refuses (exit non-zero) any: (i) learned/decision-package cross-import; (ii) governor cross-import; (iii) import from a layer above its own. Extends the chokepoint AST negative-scan (`test_llm_chokepoint_sole_importer`) to a global surface. Test IDs: `test_akki_arch_refuses_learned_to_decision`, `test_akki_arch_refuses_governor_cross_import`, `test_akki_arch_refuses_layer_up_import`, `test_akki_arch_current_tree_green`.
- **CP-M13W1-C3 · CI job wire** — the check runs on every commit-A on `programme/track-a`. Fail-closed at merge review.
- **CP-M13W1-C4 · Branch protection ratification pin** — an owner-ratifiable pin in DECISIONS.md specifying: TCB paths require 2 reviewers, 1 from security group. GitHub-side wiring is admin-blocked (surface, don't build).
- **CP-M13W1-SEAL**.

**Hard dependencies**: None. **This milestone unblocks M11 and M10.**

**Owner/infra inputs before starting**:
- ☐ Confirm TCB.yaml row list from v1.0 A.4 (nothing missing).
- ☐ Ratify 2-reviewer + security-group requirement (branch protection pin).
- ☐ Ratify rule-tensions (a) and (b) from `PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md §5` (they govern subsequent milestones).

**DoD**: `TCB.yaml` on disk; `akki.arch` script + test IDs at L3; CI job green against current tree at L5; D.5 regenerated with a new "TCB governance" row at L5.

**Risk / rework**: Low. Extends the chokepoint AST precedent. Test file additions only.

**Honors governing rules**: Tests-first · §3.3 3-commit · R-5 receipts · additive only.

---

## 3 · MILESTONE M11 · Mongo-per-tenant persistence + `akki.data` repository layer (PRECEDES M10)

**Goal**: Bind every state-changing surface to `t_<tenant_id>` MongoDB via a single repository primitive. Close B.2 / D-01. **Precede M10** so the Ledger lands directly in per-tenant DBs (no forbidden migration later).

**Closes v1.0 clauses**: **B.2** (one DB per tenant `t_<tenant_id>` + platform DB + `akki.data` repo with `tenant_id` auto-filter + write-mismatch rejection + index CI check + retention per Annex A) · **D-01** (MongoDB primary datastore) · **B.1 δ-1** (`X-Akki-Context` HMAC signed header · tenant_context enforcement).

**Scope sketch (waves)**:
- **M11-W1 · `akki.data` repository primitive**. Author `services/data/repository.py` — the ONE class every service uses for `find/find_one/insert_one/update_one/delete_one/aggregate/count`. Injects `{tenant_id: ctx.tenant_id}` into every filter; rejects writes with mismatched `tenant_id` with refusal code `AKKI-DATA-001`. AST negative-scan test refuses any file outside `services/data/` to import Motor's `AsyncIOMotorClient` directly. Test IDs: `test_repo_auto_filters_by_tenant_id`, `test_repo_refuses_cross_tenant_write`, `test_data_layer_ast_sole_motor_importer`.
- **M11-W2 · X-Akki-Context signed header (B.1 δ-1)**. HMAC-SHA256 over `(tenant_id, principal_id, request_id, issued_at, ttl)`. Gateway middleware signs; every service dependency verifies. Rejects with `AKKI-AUTH-003`. Closes v0.2→v1.0 δ-1 on M9's shape-only `tenant_context.py`. Test IDs: `test_x_akki_context_hmac_signed`, `test_x_akki_context_refuses_missing`, `test_x_akki_context_refuses_expired`, `test_x_akki_context_refuses_wrong_key`.
- **M11-W3 · Control-plane collections** (5-10 CPs): `tenant`, `workspace`, `user`, `role_assignment`, `service_account`, `role_registry`, `session`, `break_glass_session`, `audit_event`, `audit_event_types`. Each becomes an `akki.data`-backed collection with its `tenant_id` auto-filter and index declaration. Uses the Option-C thin adapter layer per rule-tension (a) recommendation (subject to owner ruling).
- **M11-W4 · Estate + connector + compute collections**: `estate`, `connector`, `compute_integration`, `allocation`, `task`, `job`, `mode_change_approval`, `connection_test`.
- **M11-W5 · App + wizard + provisioning + theme collections**: `app`, `app_enablement`, `wizard_session`, `provisioning_report`, `theme`.
- **M11-W6 · Perimeter + receipt collections**: `perimeter_crossings`, `pseudonym_maps`, `tenant_dictionaries`, `receipts`, `transform_policies`.
- **M11-W7 · Governance + observability collections**: `watch_signals`, `watch_verdicts`, `watch_actions`, `deception_artefacts`, `certainty_registry`, `rule_drafts`, `rule_proposals`, `rule_registry`, `tasks`, `model_candidates`, `admission_results`, `model_registry`, `content_gate_results`, `content_policies`, `criteria_sets`, `moac_evaluations`, `eligibility_conditions`, `eligibility_checks`, `factfulness_verdicts`, `stamp_audits`, `qa_findings`.
- **M11-W8 · Index-declaration CI + retention TTL job**. Every collection declares its indexes in code (per Annex A `Key indexes` column). CI query-plan check fails build on unindexed query >100k docs. Retention TTL job scheduled per collection's `Retention` column.
- **M11-W9 · Data-plane repository split (connected-tier vs hosted-tier)**. Placement bit on `tenant.tier`. **NEEDS OWNER/INFRA INPUT** for real replica-set + IAM.
- **M11-W10 · SEAL**.

**Hard dependencies**:
1. **M13-W1 (TCB.yaml + akki.arch)** — repository layer is TCB.
2. **MongoDB replica set + IAM (INFRA)**. **NEEDS OWNER/INFRA INPUT.** Interim: local Mongo container with all `t_<tenant_id>` DBs sharing one instance.
3. **Rule-tension (a) resolution** — thin-adapter Option C (recommended) vs additive-wrapper Option A vs narrow-refactor Option B.

**Owner/infra inputs before starting**:
- ☐ MongoDB cluster provisioning (platform + hosted tier).
- ☐ IAM policy for per-DB users (one per hosted-tier tenant).
- ☐ For pilot tenants (RMS · BDO): confirmed estate MongoDB or agent-side embedded DB choice.
- ☐ Retention values per collection — verify Annex A defaults against pilot-tenant contract terms.
- ☐ Vector store choice (Atlas Vector Search vs Pinecone) per D-07 · deferred to sub-wave.
- ☐ Ratify rule-tension (a) — thin-adapter Option C is agent recommendation.

**DoD**: All state-changing surfaces route through `akki.data`; `test_p1_cp1_tenant_context_enforcement` invariants pass with real HMAC context; cross-tenant write attempt on every collection refuses with AKKI-DATA-001; **P-01 (per-tenant isolation smoke test), P-02 (X-Akki-Context enforcement), P-03 (retention TTL respected) land as part of the D.3 acceptance suite ratcheted from M11**; D.5 regenerated with 25+ B.2-repository rows at L4.

**Risk / rework**: T1-tension closes here. Existing filesystem `northena_ledger` rows are NOT migrated in M11 (M10 handles them). No user data at risk because M9 shape carriers hold nothing yet.

**Honors governing rules**: Tests-first · §3.3 3-commit · R-5 receipts · TCB paths gated by akki.arch · Option C thin-adapter preserves SO §3.8.

---

## 4 · MILESTONE M10 · The Ledger (hash-chained single-writer + independent verifier) — EXPANDED SCOPE PER OWNER

**Goal**: Build the B.4 Ledger + C.4 mechanism. Northena is **reduced to an intent emitter**; a separate writer computes the chain; a separate verifier binary recomputes nightly.

**Closes v1.0 clauses**: **B.4** (hash-chained single-writer + Kafka-fronted durable log + independent verifier binary + nightly chain verification + head hash to per-tenant receipt endpoint) · **C.4** all of I-1..I-6 (single writer · monotonic seq · SHA256 chain · genesis per tenant · break-glass row · verifier binary as separate process) · **B.3** schema-version frozen per major.

### 4.1 Owner-mandated M10 expanded scope

1. **Rehome `northena/ledger.py` to C.4**: Northena is reduced to an **intent emitter** (Northena calls `ledger_emitter.emit_intent(...)` and does NOT write directly). File-based writer at `northena/ledger.py` becomes a compat mapper that emits intents from historical rows; then quiesces.
2. **Change-stream watcher**: `services/ledger_writer/change_stream_watcher.py` — subscribes to the durable log (Redis Streams interim per D-08, upgrade path to Kafka), applies each intent in seq order.
3. **Insert-only writer role per tenant DB**: the writer's Mongo user in `t_<tenant_id>` has `insert` on `ledger` only. No `update`, no `delete`, no `find` (verifier has `find`). Role-per-DB enforced per B.2's IAM design.
4. **Genesis hash per tenant**: the first Ledger row for a tenant has `seq=0, prev_hash="0"*64, hash=SHA256("0"*64 || canonical(row))`. Verifier binary walks from genesis.
5. **Verifier binary as SEPARATE process**: `tools/ledger_verifier/verify.py` runs OUT-OF-PROCESS from `services/ledger_writer/`. Reads only the durable log + the Ledger collection (per its own read-only role). Recomputes the chain per tenant; publishes head hash to `/app/frontend/public/audit/ledger_heads/<tenant_id>.json` nightly. **Sever SEV-1** on chain break.

### 4.2 Exit gate

- **P-06 (Ledger append and query per tenant)** passes at L5.
- **P-07 (Chain verification nightly)** passes at L5.
- **C.4 I-1..I-6 all at L5** in the levelled table.

### 4.3 Scope sketch (waves)

- **M10-W1 · Row schema v1 freeze + intent emitter contract**. Freeze row shape per B.4: `{seq, prev_hash, hash, schema_version, tenant_id, run_id, task_id, actor_id, actor_type, event_type, resource_type, resource_id, decision, reason_code, payload_ref, at, break_glass_session_id}`. Author `contracts/ledger_v1.py` + JSON schema. Author `services/ledger_emitter/emit_intent.py` — the ONE way for any component to write an intent. TCB.yaml + akki.arch AST refuses any other file to write to `t_*.ledger` collections. Test IDs: `test_ledger_row_shape_v1_frozen`, `test_ledger_emitter_ast_sole_writer`, `test_ledger_intent_carries_tenant_id`.
- **M10-W2 · Single-writer service + hash chain**. `services/ledger_writer/main.py` + `services/ledger_writer/change_stream_watcher.py` — consumes intents in seq order, computes `hash = SHA256(prev_hash || canonical(row))`, appends to `t_<tenant_id>.ledger`. Genesis per tenant. Maintains `t_<tenant_id>.ledger_heads` for verifier receipts. Test IDs: `test_ledger_writer_consumes_in_seq_order`, `test_ledger_chain_hash_correct`, `test_ledger_genesis_row_per_tenant`, `test_ledger_writer_refuses_out_of_order_seq`, `test_ledger_writer_insert_only_role_enforced`.
- **M10-W3 · Verifier binary (separate process)**. `tools/ledger_verifier/verify.py` — walks the chain per tenant, recomputes hashes, writes head hash to receipt file. Detects chain breaks and emits SEV-1. Test IDs: `test_verifier_binary_walks_from_genesis`, `test_verifier_binary_detects_hash_break`, `test_verifier_binary_publishes_head_hash_per_tenant`, `test_verifier_binary_runs_out_of_process`.
- **M10-W4 · Break-glass rows + Northena convergence blocker**. Convergence in Northena BLOCKS on `ledger_writer` acknowledgement of the closing row (C.2). Break-glass rows carry `break_glass_session_id` non-null. Ceremony (proposal → countdown → countersign → atomic apply) per C.5 emits intents. Test IDs: `test_northena_convergence_blocks_on_ledger_ack`, `test_break_glass_row_carries_session_id`, `test_ceremony_apply_emits_ledger_intent`.
- **M10-W5 · Migration path for existing partial writers**. Northena file-based ledger, memory ledger, audit_trail writer, platform_control_plane/audit_event refuser are retrofit as intent emitters. Existing filesystem `phase0/northena_ledger/led-<hex12>.json` rows migrate into `t_<default_tenant_id>.ledger` via a one-shot backfill script; monotonic seq preserved. Owner-ratifiable back-compat plan per B.3. Test IDs: `test_northena_retrofit_emits_intents`, `test_memory_retrofit_emits_intents`, `test_audit_event_retrofit_emits_intents`, `test_backfill_preserves_monotonic_seq`.
- **M10-W6 · SEAL**.

### 4.4 Hard dependencies

1. **M13-W1** (TCB.yaml + akki.arch) — Ledger writer is TCB.
2. **M11** (Mongo-per-tenant) — Ledger lives in `t_<tenant_id>.ledger`; without M11 there is no place to write. **This is the reason M11 precedes M10.**
3. **Kafka-compatible durable log (INFRA)** — v1.0 D-08 mandate. **NEEDS OWNER/INFRA INPUT**. Interim: Redis Streams with `xack` acknowledged writes (current per D-08 note). Shape-preserving upgrade to Kafka downstream.
4. **B.5 Ed25519 receipt signing (touches, not owns)** — interim HMAC-SHA256 receipts (current chokepoint pattern) + shape-frozen Ed25519 carrier; real KMS-backed Ed25519 in M13-W2.

### 4.5 Owner/infra inputs before starting

- ☐ Ratify Row schema v1 shape (16 fields per B.4).
- ☐ Ratify interim durable log: Redis Streams with `xack` — OR — block M10 on Kafka provisioning. Agent recommends **Redis Streams interim** with shape-preserving Kafka upgrade.
- ☐ Verifier binary receipt location: `/app/frontend/public/audit/ledger_heads/<tenant_id>.json` (proposed) · cadence 24h · SEV-1 on chain break.
- ☐ Backfill scope: which historical file-based Ledger rows migrate to which default tenant DB.

### 4.6 DoD

- `contracts/ledger_v1.py` schema-version frozen; `services/ledger_emitter/` sole intent emitter with AST gate; `services/ledger_writer/` writes with SHA256 chain; verifier binary out-of-process. All test IDs listed above pass at L5. **P-06 (Ledger append and query per tenant), P-07 (Chain verification nightly)** land in D.3 acceptance suite. **C.4 I-1..I-6 at L5** in D.5. Ledger rows visible end-to-end for every M12/M12b component that emits intents.

### 4.7 Risk / rework

- **Migration risk**: existing filesystem rows must map cleanly. Compat mapper at M10-W5 handles this; if field semantics differ, B.3 major-migration territory.
- **Rework impact if v1.0 revises Row schema post-M10-W1**: full major-version migration + hash chain reset per B.3. High cost. Freezing at M10-W1 with owner ratification prevents this.

### 4.8 Honors governing rules

- Tests-first RED → double-GREEN byte-match per every CP.
- AST negative-scan tests enforce single-writer + no-direct-Ledger-write outside emitter.
- Preventive-charter: emitter refuses malformed intents; writer refuses out-of-order sequences. Runtime hard-gate is the Redis Streams / Kafka acknowledged-write.
- R-5 per-CP receipts at seal time.
- §3.3 3-commit protocol; §3.3 2-COMMIT SHAPE on M10-W6 SEAL.

---

## 5 · MILESTONE M12 · Wire M9 refusers as unroutable runtime chokepoints (T2 close)

**Goal**: Every M9 shape refuser (36 CPs) becomes runtime-enforced via the thin adapter layer (rule-tension (a) Option C · owner-ratifiable).

**Closes v1.0 clauses**: A.3 rule 2 (*"Enforcement happens at chokepoints that cannot be routed around"*) · every M9 CP row in Annex D §12 acceptance criteria gets a live enforcement point.

### 5.1 Scope sketch (waves)

- **M12-W1 · `services/enforce/` adapter contract**. Author `services/enforce/__init__.py` + `services/enforce/adapter_base.py`. One thin adapter per M9 entity (~15 LOC each) that: (1) calls M9 refuser, (2) calls `akki.data` repository, (3) exposes a `Depends()` factory. AST negative-scan test refuses any file outside `services/enforce/` to import both `platform_control_plane.*` refuser AND `akki.data.repo` in the same file. Test IDs: `test_enforce_adapter_calls_refuser_before_repo`, `test_enforce_ast_sole_composer`, `test_enforce_returns_fastapi_depends_factory`.
- **M12-W2 · Gateway middleware**. ASGI middleware runs P1-CP1 (tenant_context) · P2-CP3 (permission_evaluation) · P4-CP4 (task_scope_enforcement) · P4-CP6 (scheduler_admission) at request time. AKKI-AUTH-* / AKKI-DIR-* refusal codes surface to client per B.11 refusal-surfaced.
- **M12-W3 · Connector mode + wizard + provisioning wiring**. P3-CP3 (connector_mode_lattice) · P3-CP4 (mode_change_approval) · P5-CP4 (wizard_state_machine) · P5-CP5 (provisioning_report) live gates on HTTP paths.
- **M12-W4 · Audit event emission**. P6-CP1 (audit_event) becomes a live intent emitter to M10 Ledger writer. Every state-changing API call produces a Ledger row.
- **M12-W5 · Cross-tenant access suite (P6-CP3) becomes CI job**. Runs on every deploy per §4.3 M-H-6. Blocks release on failure. CONTRACT-MODELED item 13 closes.
- **M12-W6 · SEAL**.

### 5.2 Hard dependencies

1. **M10** (Ledger writer) — audit_event needs it.
2. **M11** (Mongo + X-Akki-Context) — every refuser needs a real caller context.
3. **M13-W1** (akki.arch) — adapter layer's AST gate enforced by akki.arch.

### 5.3 Exit gate

- All 36 M9 refusers wired via `services/enforce/`; **P-11 (M9 refuser runtime enforcement) at L5**; every M9 shape CP moves from L3-shape-only to L4-enforced in D.5.

### 5.4 DoD

- Test IDs: `test_enforce_<entity>_refuses_at_http` for every M9 CP; the cross-tenant CI job green at every deploy; D.5 regenerated with 36 M9 rows at L4.

---

## 6 · MILESTONE M12b · Governance invariants to L5 (NEW · inserted per owner directive)

**Goal**: Bring the substantial existing governance code (C.3 · C.5 · C.6 · C.10 · C.11 · C.16 · C.19 · C.20) from L3 to L5 by wiring named invariants to runtime enforcement + into the CI ratchet + into the D.3 acceptance suite.

**Owner-declared L5 targets** (verbatim from directive):
- **C.3** — certainty registry, Mkono actions
- **C.5** — all seven rule classes and tiers
- **C.6** — registry-only resolution
- **C.10** — factfulness + stamp-audit
- **C.11** — grants + ladder
- **C.16** — read/write mode enforcement
- **C.19** — frame
- **C.20** — custody seam

### 6.1 Exit gate

- **P-04, P-05, P-08, P-09, P-14, P-15** all pass at L5.

### 6.2 Scope sketch (waves)

- **M12b-W1 · C.3 to L5**. Wire the certainty registry as an intent emitter to M10 Ledger. Cryptographically sign verdicts (Ed25519 from M13-W2) — this closes the L4 gap identified in `PROJECT_STATE_AND_RULES_SNAPSHOT_20260917.md §2.1` on C.3 I-1. Mkono action refuses without signed verdict. New test IDs: `test_watch_verdict_ed25519_signed`, `test_mkono_action_refuses_unsigned_verdict`, `test_certainty_registry_intent_emitter`.
- **M12b-W2 · C.5 to L5**. Enumerate all 7 rule classes (Fast, Standard, Slow, Watch, plus the 3 owner-designated remainders per canon delta) and enforce tier discipline. New test IDs: `test_rules_service_seven_classes_enumerated`, `test_rules_service_slow_tier_refuses_single_principal` (**explicitly names Slow/Watch tier**, closing the L3-partial gap on C.5 I-4), `test_rules_service_watch_tier_refuses_single_principal`, `test_rules_service_atomic_apply_all_tiers` (extending existing `test_sw2_complete_ceremony_applies_flip`).
- **M12b-W3 · C.6 to L5**. Wire the model proxy so every LLM call resolves against `model_registry` per C.6 I-1 · registry-only resolution. Extends existing `test_run_admission_refuses_unresolved_lineage`. New test IDs: `test_llm_proxy_resolves_only_admitted_models`, `test_llm_proxy_refuses_unregistered_model_id`, `test_model_registry_intent_emitter`.
- **M12b-W4 · C.10 to L5**. Factfulness pipeline steps 1-5 individually tested + stamp-audit emits Ledger intents. New test IDs: `test_factfulness_step_1_fact_identification`, `test_factfulness_step_2_fact_assessment`, `test_factfulness_step_3_stamp_assignment`, `test_factfulness_step_4_calibration`, `test_factfulness_step_5_ledger_emission`, `test_stamp_audit_intent_emitter`.
- **M12b-W5 · C.11 to L5**. Grants + ladder wired to real Mongo store (M11 dependency) + intent emitter. Test IDs: `test_capability_grants_persisted_per_tenant`, `test_capability_rung_ladder_enforced`, `test_agent_containment_intent_emitter`, `test_coalition_bound_refusal_at_http`.
- **M12b-W6 · C.16 to L5**. Real connector runtime enforcing read/write mode at connector layer (not just M9 shape refuser). Wires `services/connect/` runtime through `platform_control_plane/connector_mode_lattice.py` via the M12 adapter. Test IDs: `test_connector_runtime_refuses_write_on_read_only`, `test_connector_runtime_refuses_full_on_read_write`, `test_connector_mode_intent_emitter`.
- **M12b-W7 · C.19 to L5**. Solva frame separation runtime-enforced at the assertion boundary (extending existing `test_reasoning_faculty_isolation` to a runtime check on the assertion output). Test IDs: `test_solva_frame_never_writes_fact_hash_at_runtime`, `test_solva_assertion_boundary_intent_emitter`.
- **M12b-W8 · C.20 to L5**. Targeta custody seam + manifests bound to Mongo (M11) + intent emitter. Test IDs: `test_targeta_custody_manifest_persisted`, `test_targeta_custody_seam_intent_emitter`, `test_targeta_yield_wall_refuses_below_floor`.
- **M12b-W9 · SEAL**.

### 6.3 Hard dependencies

1. **M10** (Ledger writer) for intent emission from every governor.
2. **M11** (Mongo) for real persistence of certainty registry · rule_registry · admitted models · stamp_audits · capability_grants · connector_mode transitions · custody manifests.
3. **M12** (enforce layer) for runtime adapter wiring.
4. **M13-W2** (Ed25519) for C.3 signed verdicts. **Note**: this is the ONE reason M12b needs some M13 sub-waves to precede parts of it. Owner may choose to (a) run M12b in full after all M13 sub-waves, or (b) run M12b-W1 (which needs Ed25519) after M13-W2 lands, with the rest of M12b running earlier.

### 6.4 DoD

- Every named test ID above passes at L5.
- **P-04 (Watch certainty registry + Mkono actions), P-05 (Rules Service all 7 classes), P-08 (Critic Seam factfulness pipeline), P-09 (Agent containment grants+ladder), P-14 (Connector mode runtime enforcement), P-15 (Custody seam)** all pass in D.3 acceptance suite.
- D.5 regenerated: C.3, C.5, C.6, C.10, C.11, C.16, C.19, C.20 all at L5.

---

## 7 · REMAINING M13 SUB-WAVES (after M12/M12b · cross-cutting standards)

**Goal**: Close remaining B.5 / B.6 / B.7 / B.10.

- **M13-W2 · KMS + per-tenant master keys + Ed25519** (B.5). Real KMS (AWS KMS hosted / HashiCorp Vault connected per D-06). Per-tenant master + per-purpose data keys. Ed25519 receipt-signing keys + public-key publication endpoint. **NEEDS OWNER/INFRA INPUT** for KMS/HSM. **May pull-forward to unblock M12b-W1 (C.3 signed verdicts).**
- **M13-W3 · OpenTelemetry + per-tenant SLOs + error budgets** (B.6). OTel SDK in every service. Per-tenant metrics with `tenant_id · run_id · task_id · component`. Per-service SLO from Part C sections. Error-budget tracker halts non-urgent deploys at 50% consumption. Alerts mapped to runbooks.
- **M13-W4 · Terraform + Helm + signed images + progressive rollout** (B.7). All infra as Terraform. Helm per service. Signed container images with admission controller. Cohort-progressive rollout (internal → hosted → connected) with SLO-breach rollback. **NEEDS OWNER/INFRA INPUT** for cluster + signing keys.
- **M13-W5 · Determinism byte-identical golden-input corpus** (B.8 remainder). Every deterministic TCB component ships golden-input corpus. Byte-identical decision output across runs + across versions within a major. Extends BASELINE_GUARD=1 byte-match discipline. **Depends on rule-tension (b) resolution** for closed-enum handling.
- **M13-W6 · 2-reviewer + branch protection** (B.8 remainder). GitHub branch protection: TCB paths 2 reviewers, 1 security-group. Tooling-enforced. **NEEDS OWNER/INFRA INPUT** for GitHub org admin.
- **M13-W7 · SEV taxonomy + runbooks + post-incident review + capacity mgmt** (B.10). `akki-runbooks` repo. Every alert → runbook. Alerts without runbooks fail review. Capacity review at 80%.
- **M13-W8 · SEAL**.

**Parallelisable**: W2 · W3 · W4 · W7 are independent by dependency; can run in parallel walks once infra unblocks.

---

## 8 · MILESTONE M14 (parallel with M15) · Answering Service + Seam + Async + Mkondo

**Goal**: Close C.15 (Mkondo hand-off registry) + C.17 (answering service + async delivery).

**Waves**:
- **M14-W1 · Hand-off contract v1**. Consume `services/handoff/contracts.py`; shape-freeze.
- **M14-W2 · Mkondo registry + checkpoint runtime**. Refuses malformed / dual-hatted hand-offs at request time. Ledger-intent emitter for every hand-off.
- **M14-W3 · `asks` + `deliveries` + `webhook_endpoints` collections** on Mongo (M11).
- **M14-W4 · Real async webhook delivery** signed with per-tenant Ed25519 (M13-W2).
- **M14-W5 · SEAL**.

**Depends on**: M10 · M11 · M13-W2.
**Risk**: Low (most shape exists).

---

## 9 · MILESTONE M15 (parallel with M14) · Documents Suite + Wizards

**Goal**: Close C.22 remaining doc classes + shared model + frame precedence per D-12.

**Depends on**: M9 P5 shape · M11 (documents collection) · M12 (enforce layer).
**Risk**: Medium.

---

## 10 · MILESTONE M16 · CIF (Conditioned Ideation Faculty · C.21) — NEW BUILD · OWNER-SCOPED

**Goal**: Build CIF from scratch. Currently L0.

**Depends on**: M10 · M11 · M12 · Solva stability.
**Risk**: Medium-high. Recommend owner-scoping session before M16-W1.

---

## 11 · MILESTONE M17 · Tenant Apps + Personal Client (C.23)

**Goal**: Application-contract enforcement + personal client for tenant-of-one.

**Depends on**: M9 P5 · M11 · M12.
**Risk**: Low-medium.

---

## 12 · FRONTENDS (out-of-band · web/Expo specialists)

- **DAP portal (C.18)** — external acquisition portal · Marion prototype.
- **RMS AI Prototype v2** — M. Chen surfaces (WorkStudio · Chat · Data Suite · Documents · ThinkLab · Productivity 360 · Collab · Mentions · Emails · Projects/Tasks · HR Stuff · Performance Management · Exco 360 · Board 360 · Admin).
- **Admin Console** — platform_operator + tenant_owner + tenant_admin surfaces.

**Handoff**: this planning agent surfaces the backend contracts (API paths + response shapes per C.16 · C.17 · C.18 · C.23) as the interface for frontend specialist agents. Frontend specialist agents own React/Expo implementation.

**Gate**: recommend starting frontends AFTER **M12 completion** so backend contracts have stabilised.

---

## 13 · D.3 PLATFORM ACCEPTANCE SUITE — DELIVERABLE ratcheted from M10

The D.3 acceptance suite is not an assumption; it is a milestone deliverable that grows monotonically from M10.

- **P-01, P-02, P-03** — land with M11 (per-tenant isolation smoke test, X-Akki-Context enforcement, retention TTL respected).
- **P-06, P-07** — land with M10 (Ledger append + query per tenant, chain verification nightly).
- **P-04, P-05, P-08, P-09, P-14, P-15** — land with M12b.
- **P-10, P-11, P-12, P-13** — land with M12 (refuser runtime enforcement).
- The suite **runs in full before every seal from M11 onward**. Any P-nn regression is a right-reason RED that blocks the seal.

---

## 14 · RECOMMENDED SEQUENCE (final · owner-ratifiable)

**M13-W1 (MANDATORY FIRST) → M11 → M10 → M12 → M12b → M13-W2..W7 → M14 ∥ M15 → M16 → M17**

**Pull-forward candidates**:
- M13-W2 (KMS + Ed25519) may need to lead M12b-W1 (C.3 signed verdicts).
- M13-W5 (determinism corpus) depends on rule-tension (b) resolution.

**Frontends**: parallel track under web/Expo specialists once M12 completes.

---

## 15 · NEEDS-OWNER-DECISION / INPUT CHECKLIST

**Before M13-W1 (blocking)**:
- ☐ Ratify TCB.yaml row list from v1.0 A.4.
- ☐ Ratify 2-reviewer + security-group requirement.
- ☐ **Rule-tension (a)** — thin-adapter Option C recommended (see snapshot §5.1).
- ☐ **Rule-tension (b)** — clarify SO §3.10 as technical (Option α recommended · see snapshot §5.2).

**Before M11 (blocking)**:
- ☐ MongoDB cluster provisioning (platform + hosted-tier).
- ☐ IAM policy for per-DB users.
- ☐ Pilot-tenant persistence choice (RMS · BDO: estate MongoDB or agent-embedded).
- ☐ Retention values per collection audit.
- ☐ Vector store deferral confirmed (Atlas Vector Search vs Pinecone).

**Before M10 (blocking)**:
- ☐ Row schema v1 ratification (16 fields per B.4).
- ☐ Interim durable log: Redis Streams (recommended) vs Kafka block.
- ☐ Verifier binary receipt location + cadence + SEV-1 wiring.
- ☐ Backfill scope for existing filesystem Ledger rows.

**Before M12b-W1 (partial-blocking)**:
- ☐ M13-W2 pull-forward decision (Ed25519 for C.3 signed verdicts).

**Before M13-W2..W7**:
- ☐ KMS choice (AWS KMS · HashiCorp Vault · HSM per D-06).
- ☐ Observability backend vendor.
- ☐ Terraform state store location (S3 backend recommended).
- ☐ Ed25519 receipt-signing public-key publication endpoint.
- ☐ SLO values per service (Part C draft).
- ☐ `akki-runbooks` repo creation.
- ☐ GitHub org admin for branch protection.

**Before FRONTENDS**:
- ☐ Confirm handoff to web/Expo specialist agents.
- ☐ Backend-contract stability point (recommend: after M12).

**CONTRACT-MODELED items 1-15** (from M9 SEAL rollup §7):
- ☐ K8s cluster + MIG hardware (items 1, 2).
- ☐ NetworkPolicy CNI (item 3).
- ☐ Live OIDC/SAML SSO per tenant (item 5).
- ☐ Real PKI + CA for data-plane agent cert (item 6).
- ☐ Real 12h/1h session store (item 7).
- ☐ Break-glass notification transport (item 8).
- ☐ WCAG-AA contrast library (item 9).
- ☐ KMS envelope encryption per-tenant (item 10 · M13-W2).
- ☐ Append-only durable Ledger store (item 11 · M10).
- ☐ Real storage + wall-clock scheduler for 30-day offboarding (item 12).
- ☐ CI cross-tenant suite (item 13 · M12-W5).
- ☐ Real connector runtime enforcing mode (item 14 · M12b-W6).
- ☐ Storage namespaced by tenant_id (item 15 · M11).

**Prior-wave ratifications open**: R-7 · R-13 · R-14 · R-15 · R-16 · R-17 · BC-3 · BC-4 · S-24 · Amendment 8 HOLD · 165 quarantined D1a-1 legacy tests.

**Owner-desk items surface every milestone-boundary report** (verbatim §Δ6): BC tier · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 charters · D9 receipt-unify · admin binds · SEC rotations · R-17(a) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

---

## 16 · COMPLIANCE STATEMENT

Every milestone above honors:
- Tests-first RED → double-GREEN byte-match discipline.
- Monotonic ratchet + no-silent-rebaselining.
- §3.3 3-commit protocol (or 2-COMMIT SHAPE for state-only closes / SEALs).
- R-1..R-5 seal-chain integrity rules.
- **Definition of Done gates 1-5** (owner-authoritative 2026-09-17).
- **Evidence Bar L1-L5** with the "nothing above L2 without L3" cap.
- Preventive-charter (not enforcement hard-gate) — upgrade path preserved by M12/M12b adapter layer.
- Zero closed enums (**pending rule-tension (b) clarification**), 21-token grep-negative, zero data-plane imports, frozen dataclass carriers.
- POST-2 placement.
- GPU check-in at every seal boundary + zero-perturbation.
- Local-commits-only / no-push.
- NO `testing_agent`.
- Thin-kernel / no-refactor — **pending rule-tension (a) resolution** (Option C recommended).

No sequencing dates promised. No scope reordering without owner ratification. This plan awaits owner decisions on the checklist above.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
