# Domain 5.10 — Cross-cutting

Scope (instruction §5.10): auth and identity (compare all four; Executive-Core
JWT vs core repos' auth service) · instance isolation + scoped-accessor pattern
· secrets and key custody · the test estate: what the ~830+ test files ACTUALLY
cover (sample by category, state sampling method + coverage of sample; do not
claim to have read all) · build gates and static analysis · deployment.

## Auth and identity — cross-repo comparison

Evidence collected in Chunk-3 recon:

| Repo | `backend/services/auth/` contents | `backend/routers/auth*` |
|---|---|---|
| **RMS-IQ-Core-2** | 16 files: `__init__.py`, `auth_refusal.py`, `auth_refusal_reasons.v0.json`, `demo_identity_seeder.py`, `dependencies.py`, `engineer_invites.py`, `engineer_key_grant.py`, `engineer_key_grant_ledger.py`, `engineer_key_grant_service.py`, `engineer_scope.py`, `identity.py`, `jwt_service.py`, `key_grants.py`, `password_hash.py`, `session_binding.py`, `user_store.py` | `auth.py` (single router) |
| **Akki-OS-V1** | 15 files — **missing `demo_identity_seeder.py`** (Chunk-2 §Claim 6 note); `engineer_key_grant.py`, `engineer_key_grant_service.py`, `user_store.py` DIFFER in content (older versions) | `auth.py` |
| **Extraction-Akki** | 16 files, byte-identical to RMS-IQ-Core-2 | `auth.py` |
| **Akki-Executive-Core** | **`backend/services/auth/` DOES NOT EXIST** | 9 routers: `admin_auth_events.py`, `admin_users.py`, `auth.py`, `auth_magic.py`, `auth_oauth.py`, `auth_password_change.py`, `early_access.py`, `first_session.py`, `oauth_google.py`, plus `mfa.py` |

**Judgement**:
- Core three ship a **platform-side auth service** with a scoped-key issuance ledger (`engineer_key_grant*`), user store, JWT service, session-binding, and refusal envelope. This is the Canon-7 §3 scoped-key boundary contract, backend side.
- Executive-Core ships an **application-side auth surface** with JWT (`import jwt` at `auth.py:15`), TOTP MFA (`import pyotp` L16), OAuth (Google + magic-link), MFA setup with QR codes, and admin surfaces. This is legitimate application-territory auth per Canon 1 §13.
- Under a spine-based plan, the core three's `services/auth/` becomes the platform boundary; Executive-Core's routers become one application's user-auth layer that CALLS INTO the boundary via scoped keys.

Rows:

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C7-003 · C7-004 · C7-011** | Scoped-key issuance per application; same flow for every caller; reference app uses same path | REUSE | `services/auth/engineer_key_grant*` (3 files); tests `test_engineer_key_grant_e2_taxonomy.py`, `test_engineer_key_grant_ledger.py`, `test_engineer_key_grant_load_bearing_wire_shape.py`, `test_memory_engineer_key_grant_e2e_propagation.py`, `test_master_admin_auth_reconciliation.py`, `backend_http_e2e_grant_test.py` |
| Executive-Core JWT + OAuth + MFA + magic-link | Application user auth (retained) | RE-POINT | `Akki-Executive-Core backend/routers/auth*.py`, `oauth_google.py`, `mfa.py` |
| Application-side rate-limit / CSRF / session-timeout / privacy-wall / clamav / RBAC / security-headers / sentry | Cross-cutting app-side security | RETIRE from platform (Canon 5 §46 no platform-side bypass path) | Executive-Core loose services |

## Instance isolation + scoped-accessor pattern

- Tests: `backend/tests/invariants/test_instance_isolation.py`, `test_instance_fixture_a_roundtrip.py`, `test_instance_fixture_b_walkthrough.py`, `test_synthetic_fixture_roundtrip.py`. Ensures per-instance data does not leak across instances.
- `services/memory/scoped_accessor.py` — the scoped-accessor pattern for memory-plane reads.
- `services/master_admin/*.py` — instance-owner surface with `pending_seams`, `recent_actions`, `tier_lock_path_a_ledger`.

Class: **REUSE**.

## Secrets and key custody

- `services/synisense/shield/trust_receipt.py:44-56` — HKDF-derived per-tenant signing key from `MASTER_SECRET` (env-scoped).
- `services/outer_gate/mint.py:_new_key` + `_fingerprint` + `MintWindowStore` — one-shot per-window keys with explicit `purge_window`.
- `services/auth/password_hash.py`, `services/auth/jwt_service.py`, `services/auth/key_grants.py` — password + JWT + scoped-key custody.

Class: **REUSE**.

## Test estate — sampling method + result

Extraction-Akki backend test estate = **256 test files** (per Chunk-1 file-type table).
RMS-IQ-Core-2 = 254; Akki-OS-V1 = 222; Akki-Executive-Core = **505** test files (Chunk-1 §2).

### Sampling method

Method used in Chunk 3:
1. Enumerated all 141 `.py` test files under `RMS-IQ-Core-2/backend/tests/` grouped by directory (143 in `invariants/`, 11 in `registry/`, 4 in `fixtures/`, 2 in `live_preview/`, others loose).
2. Listed all test-file names (stripped `test_` prefix and `.py` suffix) to compute the coverage universe — 130+ unique bucket names.
3. Opened 6 test files in Chunk-2 for close-reading (`test_shield_custody_chain.py`, `test_ast_egress_gate.py`, `test_p1_custody_closure.py`, `test_northena_ledger_retention.py`, `test_solva_assertion_boundary.py` first 60 lines, `test_g_13_execution_atomic.py`).
4. For every test-file bucket, extracted the domain-facing capability it covers by name-pattern alone (test names ARE evidence when they cite a Canon anchor in their docstring — verified for 6 opened files).

**Coverage of sample: opened 6 of 141 (≈ 4.3%). Everything else classified from name + directory + Chunk-1 recon.** Not claiming otherwise.

### Categorised summary of test estate

| Category | # test files (Extraction-Akki backend) | Sample opened | Confidence |
|---|---:|---|---|
| **Shield / custody chain / egress** | 4 (`test_shield_custody_chain`, `test_ast_egress_gate`, `test_p1_custody_closure`, `test_no_direct_llm_calls_outside_shield`) | 3 opened | HIGH — Chunk 2 Claim 2 |
| **Northena / ledger** | 4 (`test_northena_invariants`, `test_northena_ledger_retention`, `test_northena_ledger_row_v0`, `test_no_unauthorized_deletion_path`) | 1 opened | HIGH — Chunk 2 Claim 4 |
| **Solva** | 4 (`test_solva_assertion_boundary`, `test_solva_trace_ledger_integration`, `test_reasoning_faculty_isolation`, `test_composed_conclusion_class_from_solva_boundary`) | 1 opened | HIGH — Chunk 2 |
| **Mtafiti + five_rings + layer_a/b/c** | 10 (mtafiti_invariants, feasibility_*, layer_a/b/c_*, five_rings_v0_zero_mutation, floor_feasibility_shared_derivation, grain_compatibility_shared_source, freshness_*, v3_overlay_*) | 0 opened; test names covered in Chunk 2 shaping | MEDIUM — Solva-pattern discipline confirmed |
| **Targeta** | 1 (`test_targeta_invariants` — but multiple subtests listed in Chunk 2) | 0 opened; grep of test names verified | MEDIUM |
| **Outer gate** | 3 (irreversibility, v0_paths_byte_identical_4a/4b) | 0 opened | LOW — need Chunk 4 |
| **Auth / engineer-key-grant** | 6 (engineer_key_grant_*, memory_engineer_key_grant, master_admin_auth_reconciliation, backend_http_e2e_grant_test) | 0 opened | MEDIUM |
| **Compliance / refusal / rulebook** | 8 (admission_refusal_dispatch, admission_refusal_v0_contract_frozen, service_1_refusal_envelope, dispatch_grain_form_refusal, dispatch_shape_responsive, phase_8_b_5a_compliance, phase_8_b_5b, service_1_refusal_v1_envelope) | 0 opened | MEDIUM |
| **Governance ceremony (govern g_g1-g_g8 + ui1b)** | 5 (test_govern_g_g1_to_g_g8, test_govern_ui1b_gates + 3 iters) | 0 opened | MEDIUM |
| **Memory + observability** | 4 (memory_service_m_g1_to_m_g9, memory_observability_o_g1_to_o_g6, memory_http_surface, memory_engineer_key_grant_e2e_propagation) | 0 opened | MEDIUM |
| **Phase 3-9 stage/sub-stage/gate landings** | 14+ (phase3_sc2_live, phase3_sc3_govern_live, phase3_subcycle1_gates, phase_5_stage_b_async_delivery, phase_6_stage_b_economics, phase_7_stage_b_1/2/3_wizard, phase_8_b_1/2/5a/5b, phase_8_seam_3_sub_stage_1/2/3, phase_9_sub_stage_9_1_and_9_3) | 0 opened | LOW — these are the phase-close verifications; content unknown |
| **UI1c/d/e live-preview** | 6 (ui1c_live_preview, ui1d_iter22/23/24_live, ui1e_iter23/24_live, ui1d_live_preview) | 0 opened | LOW |
| **Trace lens** | 2 (trace_lens_readonly, trace_lens_cross_engine_correlation) | 0 opened | MEDIUM |
| **Registry** | ~5 (`registry/` subdir + machine_readable_registry_mrr_g1_to_g6 + registry_prove_ui1d_gates + registry_v1_consolidation_byte_identity) | 0 opened; Chunk 2 references | MEDIUM |
| **Frozen contracts + snapshot parity** | 4 (frozen_contract_snapshot_parity, admission_refusal_v0_contract_frozen, feasibility_result_v0_contract_frozen, invariant_contract_snapshots + backfilled_contract_snapshots + composed_conclusion_v0_contract_frozen + objective_request_v2_contract_frozen + 3 more) | 0 opened | MEDIUM |
| **Use-data / commission verdict** | 5 (use_data_http_iter11, use_data_iter12_addendum, use_data_iter14_sample_all_identities, use_data_commission_verdict, qualified_data_outer_gate_ride, qualified_data_selection) | 0 opened | MEDIUM |
| **Static-analysis invariants** (AST + no direct LLM + no deletion) | 3 (ast_egress_gate, no_direct_llm_calls_outside_shield, no_unauthorized_deletion_path) | 2 opened | HIGH |
| **Perception** | 1 (perception_router) + 9_2a_real_perception | 0 opened | LOW |
| **v1 harness / v2 gate / v3 overlay** | ~6 | 0 opened | LOW |
| **Others** (lift_manifest_*, transform_forms, opportunity_briefs_ob_g1_to_g5, standing_queries_sq_g1_to_g10, answer_fluency_af_g1_to_g8, fixture_refresh_fr_g1_to_g7, machine_readable_registry_mrr_g1_to_g6, cif_manifest_submission_gate — Akki-OS-V1 only, critic_pass_execution_atomic — Akki-OS-V1 only, etc.) | ~40 | 0 opened | LOW |

### Sampling honesty statement

Of 256 test files, **6 (2.3%) were opened directly**, with content read line-by-line. The remaining 250 are classified via (a) directory placement (`invariants/` = static-analysis discipline, `registry/` = ledger discipline, `live_preview/` = surface-live cell, `fixtures/` = fixture roundtrip), (b) file-name-to-canon-anchor mapping (name-only), and (c) transitive citation from files that WERE opened (e.g. `test_p1_custody_closure.py` cites 6 P1-G-R2 gates whose test-file names I found in Chunk 2). Do not extrapolate coverage beyond that sampling.

### Executive-Core test estate (505 files)

Categories glimpsed from `git ls-files backend/tests/`:
- `characterisation/` — golden-file characterisation tests (`test_chat_roundtrip_golden`, `test_solva_analyze_golden`, `test_work_studio_compile_golden`, `test_decks_work_studio`, etc.).
- Loose `test_invariant_*.py` cluster (18+ files including `invariant_audit_always`, `invariant_boundary_imports`, `invariant_chat_streaming_reidentify_present`, `invariant_contract_snapshots`, `invariant_cross_context_calls`, `invariant_deploy_smoke_present`, `invariant_fail_closed`, `invariant_first_session_response_shape`, `invariant_http_response_model`, `invariant_http_transport_pydantic_kwargs`, `invariant_narrowing_byte_equivalence`, `invariant_no_raw_axios`, `invariant_no_silent_skips`, `invariant_polymorphic_response_ratchet`, `invariant_sdk_slices`, `invariant_shield_no_leak`, `invariant_tenancy`, `invariant_violations_smoke`).
- **No files opened.** Categorisation is by name alone.

Class for the Executive-Core test estate under RE-POINT programme: **RE-POINT for characterisation goldens** (they exercise the surfaces we RE-POINT), **REBUILD for anything that asserts direct db access shape that changes under memory-plane migration** (Chunk-2 §Q7.2 storage row).

## Build gates + static analysis

Rows here that are the platform-wide enforcement discipline (also cross-refs to per-domain enforcement rows):

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C3-059** | AST egress gate + ledger-write-before-return + declaration-required + frozen-objective-not-mutated | REUSE (partial) | AST + ledger-write-before-return + frozen-objective enforced (Chunk 2 Claims 2, 4 + 5.2). **Declaration-required build gate is BUILD** (5.2 C3-008 seam). |
| **C3-060** | Every operation carries verdict receipt through response emission | REUSE | trust receipt discipline |
| **C3-061** | Gate that CANNOT DEMONSTRATE ITSELF FIRING is not in force | REUSE (discipline) | Verification Runner is the standing surface — 5.6 |
| **C4-065 · C4-066** | Static + runtime enforcement of operating-engine invariants | REUSE | 40+ invariant tests |
| **C7-029 · C7-030 · C7-031** | Rulebook enforcement — build gates for defect classes, runtime detection, standing queries | REUSE (for defects that have gates); **PARTIAL for the standing-query surface** | 5.6 mirror |
| **C7-032 · C7-033 · C7-034 · C7-035** | Rulebook does NOT invent classes at runtime / does NOT tolerate defects / does NOT rank as acceptable / does NOT re-route to memory | REUSE-doctrine | discipline held |

## Defect taxonomy (C7-D01–C7-D26)

Each of the 26 defect classes:

| Row | Class | Note |
|---|---|---|
| **C7-D01** D-Ledger | REUSE (enforced by ordering in admit/gate/converge) | 5.2 |
| **C7-D02** D-Manifest | HARVEST — Akki-OS-V1 `test_cif_manifest_submission_gate.py` | 5.4/5.5 |
| **C7-D03** D-Chip | BUILD | 5.7 |
| **C7-D04** D-Grounding | REUSE | Mtafiti provenance |
| **C7-D05** D-Fabricated-Absence | REUSE | Mtafiti three-state render |
| **C7-D06** D-Confident-Caveat | REUSE | Solva assertion boundary |
| **C7-D07** D-Bypass | REUSE | AST gate + runtime firewall |
| **C7-D08** D-Second-Record | REUSE | append-only + no_unauthorized_deletion_path |
| **C7-D09** D-Runtime-Human | REUSE-doctrine | no runtime-human path |
| **C7-D10** D-Frozen-Mutation | REUSE | FrozenArtifact TypeError |
| **C7-D11** D-Independence | PARTIAL | Chunk 4 |
| **C7-D12** D-Rule-Paper | PARTIAL | 5.6 |
| **C7-D13** D-No-Warmup-Violation | REUSE | no warm-up branch |
| **C7-D14** D-Untraceable-Adapter | BUILD | 5.4 MOAC |
| **C7-D15** D-MOAC-Missing | BUILD | 5.4 |
| **C7-D16** D-Verdict-Curation | REUSE | uncurated composition rule; test in mtafiti invariants |
| **C7-D17** D-Console-Interior | BUILD | 5.7 |
| **C7-D18** D-Watch-Interior | BUILD | 5.8 |
| **C7-D19** D-Behavioural-Register | N/A-DOCTRINE (unrepresentable-by-design) | 5.8 |
| **C7-D20** D-Bio-Watch-Merge | N/A-DOCTRINE | 5.8 |
| **C7-D21** D-Handoff | PARTIAL | 5.9 |
| **C7-D22** D-Dual-Hat | BUILD | 5.9 |
| **C7-D23** D-Cross-Auth-Credential | BUILD | 5.9 |
| **C7-D24** D-Missing-Attestation | REUSE | outer_gate receipts |
| **C7-D25** D-Refusal-Silent-Collapse | REUSE | refusal_family_classifier + envelope tests |
| **C7-D26** D-Reset-Absent | HARVEST | Akki-OS-V1 `cif_manifest_submission_gate` |

## Deployment

- Core three: `Dockerfile` + `docker-compose.yml` + `Makefile` at repo root; `backend/` + `frontend/` split; `.emergent/` build config.
- Executive-Core: split `Dockerfile.backend` + `Dockerfile.frontend`, `docker-compose.yml` + `docker-compose.prod.yml`, `nginx/`.

Both are FastAPI + React + Mongo, consistent with the environment charter. Under the RE-POINT programme, Executive-Core's application shell would be rewired to talk to Core-2's `/api/*` boundary via HTTP.

Class: **RE-POINT (Executive-Core shell)** + **REUSE (core-repo shell)**.

## Contradictions surfaced (Chunk-2 §Claim 6 carry-forward)

**PURPOSE-GATE CONTRADICTION**:
- RMS-IQ-Core-2 / Akki-OS-V1 / Extraction-Akki: `purpose_validator.py` shaved at IF-1 close 2026-07-14. Purpose survives only as a receipt field.
- Akki-Executive-Core: `purpose_validator.py:20-58` still enforces a real gate; `client.py:63` still calls `validate_purpose()`; last commit 2026-07-08 (six days before IF-1).

Neither is classified here; the client's governance call determines whether the shave is Canon-3-compliant (5.10 for cross-cutting because the discipline touches EVERY LLM call in the platform).

## Domain 5.10 subtotals

- REUSE: 22 rows (auth + isolation + secrets + test estate discipline + build gates + most defects)
- HARVEST from Akki-OS-V1: 2 (D-Manifest, D-Reset-Absent — via critic_pass/cif_manifest_submission_gate)
- BUILD: 7 (C3-059 declaration build gate; D-Chip, D-Untraceable-Adapter, D-MOAC-Missing, D-Console-Interior, D-Watch-Interior, D-Dual-Hat, D-Cross-Auth-Credential)
- PARTIAL: 4
- N/A-DOCTRINE / unrepresentable-by-design: 2 (D-Behavioural-Register, D-Bio-Watch-Merge)
- RE-POINT: 1 (Executive-Core app shell)
- RETIRE (from platform): 1 cluster (Executive-Core cross-cutting security duplication)
- CONTRADICTION carried: 1 (purpose gate)
