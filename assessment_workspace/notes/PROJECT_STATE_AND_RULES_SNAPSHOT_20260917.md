READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROJECT STATE + GOVERNING RULES SNAPSHOT · 2026-09-17 (revised 21:46Z)
**Authoritative memory-snapshot for the orchestrator. Grounded on-disk, not aspirational.**

**Revised 2026-09-17T~21:46Z** to bank CP-M13W1 landing (TCB.yaml + `akki.arch` global import assertions CI · SCOPED current-tree only per owner Option A) and ratchet bump 4810→4814. Prior 21:15Z revision banked CP-Anti-Forget-1 (R-6 anti-forget boot manifest). Prior 20:30Z revision banked owner directive: DEFINITION OF DONE, EVIDENCE BAR L1-L5, and levelled component table with test-ID citations. Assertion counts and LOC are **not** evidence of a guarantee — test IDs mapped to spec I-clauses are.

**Byte-identical downloadable copy** at `/app/frontend/public/audit/PROJECT_STATE_AND_RULES_20260917.md`.

---

## 0 · DEFINITION OF DONE (owner-authoritative · applies to every milestone from M10 onward)

A milestone seals **only** when all five gates are green:

1. **Every spec invariant it closes (C.n I-x) is mapped to a test ID and passing under `BASELINE_GUARD=1`.**
2. **The D.3 platform tests it enables (P-nn) pass.**
3. **Affected components are re-levelled on the evidence bar.**
4. **D.5 is regenerated from the levelled table.**
5. **The milestone's Ledger rows are visible end to end** (Ledger is a first-class evidence surface from M10 onward).

## 0.1 · EVIDENCE BAR (owner-authoritative · verbatim)

| Level | Definition |
|---|---|
| **L1** | Code exists |
| **L2** | Wired on HTTP |
| **L3** | Named invariants covered by test IDs |
| **L4** | Enforced fail-closed at runtime |
| **L5** | In the CI ratchet (`BASELINE_GUARD=1` byte-match + byte-identical determinism corpus per B.8) |

**Rule**: **NOTHING sits above L2 without L3 evidence.** L3+ (L3, L4, L5) all require a specific-invariant test ID that names the C.n I-x mandate.

Test IDs are the currency. Assertion count and LOC totals are context — not currency.

---

## 1 · CURRENT STATE (from disk · 2026-09-17T~21:46Z)

### 1.1 Repos + branches

| Repo | Path | Active branch | HEAD |
|---|---|---|---|
| **Extraction-Akki** (code) | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `71faac1` (CP-M13W1 Commit-A · advanced from `fd4432a` CP-Anti-Forget-1) |
| **Assessment workspace** (state) | `/app/assessment_workspace` | `master` | `5ebb875f` (CP-Anti-Forget-1 Commit-C fixup · to be advanced by CP-M13W1 Commit-B/C in this snapshot commit) |
| Akki-OS-V1 | `/app/assessment_workspace/repos/Akki-OS-V1` | untouched this wave | — |
| Akki-Executive-Core | `/app/assessment_workspace/repos/Akki-Executive-Core` | untouched this wave | — |
| Akki-Executive-Final | `/app/assessment_workspace/repos/Akki-Executive-Final` | untouched this wave | — |
| RMS-IQ-Core-2 (tenant app · C.23) | `/app/assessment_workspace/repos/RMS-IQ-Core-2` | untouched this wave | — |

**Local commits only. No push. Ever.**

### 1.2 Ratchet arc

- **Current floor: 4814** (`baseline_failures.json` · `passed_floor = 4814 · passed = 4814 · failed = 0`).
- Arc: **4433 → 4814 (+381)** across M9 (+376: P1 +35 · P2 +48 · P3 +53 · P4 +88 · P5 +86 · P6 +66) + CP-Anti-Forget-1 (+1: R-6 anti-forget boot manifest self-check) + CP-M13W1 (+4: TCB.yaml + akki.arch 4 invariants).
- **BASELINE_GUARD=1 sweep runtime**: ~132 s (byte-matched on `4814 passed, 1 skipped, 438 warnings` across GREEN1/GREEN2 at 2026-09-17T~13:43/13:45Z).

### 1.3 Code + test size (context only · not evidence of guarantee)

- **101 service directories** · **78,549 lines of Python** in services · **~55 mounted HTTP routers** (confirmed via `grep include_router server.py`).
- **109,357 lines of Python in tests/** · **467 test files under `tests/invariants/`** · **3,726 raw `def test_*` occurrences**.
- **Seals**: all M6/M7/M8/M9 CP seals landed · **zero `pending-C-fixup` occurrences** (R-2 clean · re-verified this session).
- **Drill receipts**: 700+ tracked including this session's aggregate back-compat batch + 4 P6 reconstructed-post-hoc + CP-P6-CP5 full R-5 suite.

### 1.4 Milestones sealed (M0..M9)

| Milestone | Artefact | Status | Notes |
|---|---|---|---|
| M0 · CANON ASSESSMENT | DECISIONS.md 2026-09-13T~14:30Z | SEALED (document-only) | 13 `notes/canon_*_requirements.md` · REUSE_ASSESSMENT_20260913.md · BUILD_STRATEGY_20260913.md · ratchet 3562. |
| M2 · Doc-0 Attr-4 / Rules-Service scaffold | W-M2-SW1..SW5 ratchet_history entries | SEALED (component-level) | rule_registry · Rules-Service ceremony · rule-book library · seed jsonl · reliable-time-source. |
| M3/M4/M5 | Embedded in ratchet arc 3562→4426 pre-M6 SEAL | SEALED (embedded) | Not enumerated as dedicated wave-close notes this session. |
| M6 · SEAL | `notes/M6_SEAL_20260916.md` + DECISIONS.md 2026-09-16T~19:36Z | SEALED | 9/10 + DEFERRED SW-10 · state-only wave-close · ratchet 4426 unchanged. |
| M7 · Serving-Integrity walk (W3 chokepoint · W5 go 2026-08-25) | Embedded in ratchet arc + `services/chokepoint/llm.py` | SEALED (component-level) | Sole LLM invocation seat landed. |
| M8 · SEAL | `notes/M8_SEAL_20260917.md` (23,315 B) + downloadable | SEALED | 7/7 CPs closed under §3.3 · state-only wave-close. |
| M9 · Pilot Platform Layer (v1.0 Annex D) | `notes/M9_SEAL_20260917.md` (322 lines) + downloadable | SEALED | 36 code CPs + 1 wave-close · ratchet 4433→4809 (+376) · zero rollback · R-1..R-5 ratified mid-wave. |

### 1.5 GPU 72h campaign

- **Elapsed 29.11 h · Remaining 42.89 h** (per `/app/frontend/public/audit/GPU_UTILIZATION_72H.json` regenerated 2026-09-17T08:48:15Z).
- Hosts `akki-vm` + `akki-vm-ii` · both `sampler_alive+workload_alive` · in-perimeter · no anomalies · zero synthetic burn · on cadence to 72h completion.

### 1.6 Admin-blocked ops items (respected · not blocking on · surface every seal boundary)

- **SEC events**: SEC-2026-09-12-01 · SEC-2026-09-14-04 (HF) · SEC-2026-09-13-T4-01/03/04/05 · SEC-2026-09-14-01/02/03 (JUMP · RADIO · NAS · DB).
- **Infra binds pending**: Transcription-server host+creds MISSING BIND · RADIO routing to 10.10.19.0/24 MISSING BIND · 5 closed-SG MySQL hosts.
- **Ratifications open**: R-7 · R-13 · R-14 · R-15 · R-16 · R-17 · BC-3 · BC-4 · S-24.
- **165 quarantined D1a-1 legacy tests** — leave quarantined per owner.
- **Owner-desk items surface every milestone-boundary report** (verbatim §Δ6): BC tier · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 charters · D9 receipt-unify · Amendment 8 HOLD · admin binds · SEC rotations · R-17(a) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

---

## 2 · LEVELLED COMPONENT TABLE (regenerated D.5 · every claim anchored to test IDs on disk)

**Legend**: **L1** code · **L2** L1 + HTTP · **L3** L2 + named invariant tests · **L4** L3 + fail-closed runtime · **L5** L4 + CI ratchet + byte-identical determinism. **Above L2 requires L3.**

### 2.1 GOVERNORS (Layer 1)

| Component | Spec | Owner-provisional | On-disk verdict | Named-invariant test IDs (on disk · verified this session) | Notes |
|---|---|---|---|---|---|
| **LLM chokepoint** (C.1) | C.1 I-1..I-6 | L4 | **L4 confirmed** | `test_llm_chokepoint_sole_importer::test_only_chokepoint_llm_may_import_llm_sdks` · `test_llm_chokepoint_sole_importer::test_legacy_synisense_llm_router_no_longer_imports_sdk` · `test_llm_purpose_gate_refuses_unlisted` · `test_llm_egress_allowlist_provider_scoped` · `test_llm_masking_tier_enforced` · `test_llm_crossing_receipt_metering` · `test_chokepoint_registers_all_crossings` · `test_w5_cp4_backend_endpoints::test_chat_ask_answers_with_provenance_and_receipt` · `test_w5_cp4_backend_endpoints::test_shield_receipts_filter_by_reasoning_kinds` · `test_w5_cp4_backend_endpoints::test_connect_llm_verify_never_leaks_key_in_response` | AST negative-scan enforces sole-importer; runtime enforces purpose + allowlist + masking + receipt. **HTTP paths**: `chat/router.py`, `wizard/connect_llm_router.py`, `solva/reasoning.py` (transitive). **Not L5**: no byte-identical determinism corpus per B.8. |
| **Northena run loop + append-only ledger** (C.2 + C.4-partial) | C.2 + C.4 (partial · file-based) | L2 | **L3 corrected up** | `test_northena_ledger_row_v0` · `test_northena_ledger_retention` · `test_master_admin_tier_lock_path_a_ledger` · `test_trace_lens_cross_engine_correlation` · `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit` | `services/northena/router.py` mounted at `/api` ✅. **Not L4**: file-based append-only writer is NOT hash-chained per B.4 · not fail-closed on chain break · no independent verifier binary. This is Doc 05 §B5.4 structural discipline, not v1.0 B.4. **M10 rehomes to C.4 shape** (intent-emitter + separate writer + verifier binary). |
| **The Watch** (C.3) | C.3 I-1 signed verdict · I-2 registry-only action | Not yet levelled | **L3 for I-2 · L2 for I-1** | `test_w9_cp1_watch_seam` · `test_w10_cp2_mirage_machinery` · `test_watch_action_v0_contract_frozen::test_four_class_closed_grammar` · `test_mirage_contracts_frozen` · `test_watch_cp_c2_http_journey::test_http_action_for_unknown_verdict_returns_404` · `test_watch_cp_c2_http_journey::test_http_structural_verdict_without_signal_on_record_refused` · `test_watch_cp_c2_http_journey::test_http_post_sever_signal_then_structural_verdict_maps_to_sever` · `test_watch_cp_c2_http_journey::test_http_state_reflects_recorded_verdicts_and_actions` | C.3 I-2 (**registry-only action**) has clear L3-L4: HTTP tests refuse unknown-verdict actions + refuse structural verdict without signal. C.3 I-1 (**signed verdicts**) — grep-negative on cryptographic verdict signing; verdicts have a shape but no signature check. **L4 gap for I-1 — closes at M13-W2 (Ed25519) + M12b (verdict signing wire-up).** |
| **The Ledger** (C.4) | C.4 I-1..I-6 hash-chained + single-writer + verifier | Owner-marked "PARTIAL, multiple writers, no B.4" | **L1 for C.4 shape · L3 for file-based partial** | (No B.4-hash-chained test IDs on disk. Multiple partial writers tested: `test_northena_ledger_row_v0` covers Northena file-based row shape only.) | **C.4 I-1..I-6 NOT MET.** Northena file-based writer is `contracts.northena_ledger`, not the v1.0 B.4 `ledger` collection with `hash = SHA256(prev_hash \|\| canonical(row))`. **M10 is the C.4 build.** |
| **Rules Service** (C.5) | C.5 I-3 atomic apply · I-4 no single-principal Slow/Watch | Not yet levelled | **L3 for I-3 · L3 partial for I-4** | `test_wm2_sw2_rules_service_ceremony::test_sw2_complete_ceremony_applies_flip` (**I-3 atomic apply**) · `test_wm2_sw2_rules_service_ceremony::test_sw2_r_2_second_signatory_pending_override` · `test_wm2_sw2_rules_service_ceremony::test_sw2_r_3_witness_same_as_watch` · `test_wm2_sw2_rules_service_ceremony::test_sw2_r_4_business_type_finite` · `test_wm2_sw2_rules_service_ceremony::test_sw2_r_c1_retirement_backed_by_mechanism` · `test_w8_cp3_approvals_ceremony::test_decide_request_enforces_separation_of_duties` · `test_w8_cp3_approvals_ceremony::test_decide_request_refuses_double_decision` · `test_wm2_sw15_doc0_attr12_governance_ceremony::test_sw15_r_c1_retirement_backed_by_mechanism` | C.5 I-3 (atomic apply) L3 solid. C.5 I-4 (**no single-principal for Slow/Watch tier**) — "second signatory pending" + "separation of duties" cover the shape, but **no test names "Slow" or "Watch" tier explicitly**. L3 partial. **Rules Service `router.py` exists but not obviously mounted at server.py; L2 needs confirmation.** |
| **Model Admission Gate** (C.6) | C.6 I-1 proxy resolves only admitted models | Not yet levelled | **L3 confirmed** | `test_w7_cp4_model_admission_ceremony::test_run_admission_accepts_valid_card_and_bumps_registry` · `test_w7_cp4_model_admission_ceremony::test_run_admission_refuses_unresolved_lineage` (**I-1 covered**) · `test_w7_cp4_model_admission_ceremony::test_run_admission_refuses_when_floor_missed` · `test_w7_cp4_model_admission_ceremony::test_admission_record_never_carries_credentials` · `test_admission_refusal_dispatch` · `test_admission_refusal_v0_contract_frozen` · `test_emit_moac_chokepoint_admission` · `test_w7_cp3_model_registry` | `model_admission_router` mounted in `server.py` ✅. **L3 solid; L4 partial** — I-1 tested at ceremony level, but proxy-resolves-only-admitted enforcement at *every* LLM call is chokepoint-side (not model_admission-side); needs one more wire. |
| **Output-Content Gate** (C.7) | C.7 | Not-started | **NOT-STARTED** | (None) | Edge verification exists in chokepoint egress allowlist; **internal-boundary placement not built**. L0. |
| **MOAC** (C.8) | C.8 | Not yet levelled | **L3 partial** | `test_emit_moac_chokepoint_admission` · `test_w7_cp4_model_admission_ceremony::test_moac_contract_has_six_criteria_fields` · `test_w7_cp4_model_admission_ceremony::test_moac_evidence_source_kind_refuses_curated_benchmark` · Targeta side: `test_targeta_invariants` · `test_wregext_g3_cp_r2_typed_custody_class` · `test_wrg_cp_rg_hygiene_01_custody_cat_guard` | Training-side yield-wall (Targeta) L3. Extraction-side acceptance-criteria-vs-criteria_sets L2 (contract shape only). |
| **Eligibility Gate** (C.9) | C.9 | Not yet levelled | **L1-L2** | (Whitepapers wizard tier eligibility per D.5 fragmentary · no explicit C.9 I-x test-ID owned by an `eligibility/` module.) | Document-tier eligibility L1. General C.9 gate NOT-STARTED. |
| **Critic Seam** (C.10) | C.10 factfulness steps 1-5 | Not yet levelled | **L3 partial (seam wire) · L1 for step-1..5 pipeline** | `test_critic_pass_lift::test_tier_2_rubric_has_seven_items` · `test_critic_pass_lift::test_qa_3_no_self_review` · `test_r4_8_critic_seam_producer_wiring::test_producer_seam_module_exports_route_and_summary` · `test_r4_8_critic_seam_producer_wiring::test_chat_answer_path_fires_critic_seam` · `test_r4_8_critic_seam_producer_wiring::test_whitepaper_draft_fires_critic_seam` · `test_r4_8_critic_seam_producer_wiring::test_producer_seam_reachable_from_pod_shell_import_chain` · `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit` · `test_wsolvalift_cp_s7_critic_seam` | **Seam wiring** L3 (chat + whitepaper paths fire producer_seam). **Explicit step-1..5 factfulness pipeline** — no test names "step 1 fact identification" · "step 2 fact assessment" · "step 3 stamp assignment" · "step 4 calibration" · "step 5 ledger emission" individually. L3 partial for the pipeline; L4 gap. |
| **Agent + Swarm Containment** (C.11) | C.11 I-1 grants · I-2 ladder | Not yet levelled | **L3 confirmed** | `test_wm3_sw7_agent_containment::test_sw7_module_fabric` · `test_wm3_sw7_agent_containment::test_sw7_all_twelve_ceilings_enumerated` · `test_wm3_sw7_agent_containment::test_sw7_narrow_start_admits_minimum_only` (**I-1 grants floor**) · `test_wm3_sw7_agent_containment::test_sw7_ac3_no_scope_before_admission` (**I-2 no scope before admission**) · `test_agent_containment_spec_v1_ingest::test_all_twelve_ac_headings_present_in_requirements_file` · `test_wdap_2g_coalition_and_estate_wide_bound` | L3 solid; router mount not obvious in server.py — L2 partial. |

### 2.2 CONTEXT (Layer 2)

| Component | Spec | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **Mtafiti** (C.12) | | **L3** | `test_census_dimensions` · `test_census_dimensions_ast_gate` · `test_census_dimensions_wire_shape` · `test_census_engine_contract` · `test_census_wire_shape` + contract snapshots (`mtafiti_detection_signal.contract_snapshot.json`, `mtafiti_objective_carrier.contract_snapshot.json`, `mtafiti_registry_record.contract_snapshot.json`, `feasibility_result.contract_snapshot.json`). Router `mtafiti_router` mounted in `server.py` ✅. L4 partial (classification + lawful-basis capture per D.5 not yet enforced). |
| **Memory** (C.13) | | **L3** | `test_r4_3_memory_wired` · `test_memory_service_m_g1_to_m_g9` · `test_memory_engineer_key_grant_e2e_propagation` · `test_memory_observability_o_g1_to_o_g6` · contract snapshots (`memory_plane_v0.contract_snapshot.json`, `memory_write_back_v0.contract_snapshot.json`). `memory_router` mounted in `server.py` ✅. L4 partial (key-scoping per D.5 not enforced). |
| **Governed-value taxonomy** (C.14) | | **L1** | Fragments across `perception/` + `governance/`; no dedicated `taxonomy/` module; no C.14 I-x test-IDs owned by a taxonomy module. |

### 2.3 ORCHESTRATION (Layer 3)

| Component | Spec | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **Northena orchestration face** (C.2) | | **L3** | Same as §2.1 Northena above. `northena_router` mounted at `/api` ✅. |
| **Mkondo** (C.15) | | **L1** | Only `services/handoff/contracts.py` exists; no C.15 checkpoint runtime; no named C.15 I-x test-IDs. `handoff_router` mounted (contracts surface only). |

### 2.4 INTEGRATION (Layer 4)

| Component | Spec | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **Connectors + Connect wizard** (C.16 read/write mode enforcement) | | **L3 shape-only** | M9 P3-CP2/CP3/CP4/CP5 shape refusers: `test_p3_cp2_connector_entity` · `test_p3_cp3_connector_mode_lattice::test_assert_downgrade_only_refuses_upgrade` · `test_p3_cp3_connector_mode_lattice::test_assert_downgrade_only_permits_downgrade` · `test_p3_cp4_mode_change_approval` · `test_p3_cp5_connection_test` + connect_gpu tests. `connect_router` mounted ✅. **L4 gap**: connector-runtime read/write-mode enforcement is not wired at the connector layer — M9 refusers are shape-only. **M12b closes.** |
| **Answering Service + Seam + Async** (C.17) | | **L1-L2** | `services/handoff/contracts.py` + `services/journey_assistant/` + `services/contract_shells/` + `services/response_sanitizer/` fragments. Async as polling per D.5. No dedicated `asks`/`deliveries`/`webhook_endpoints` collections tested. |
| **DAP** (C.18) | | **L3 confirmed** (corrected from prior assessment) | `test_wdap_2a_external_party_principal_and_admission` · `test_wdap_2b_browse_pull_seam_and_api_keys` · `test_wdap_2c_approval_routing_and_controlled_ops` · `test_wdap_2e_metering_and_cumulative_disclosure` · `test_wdap_2g_coalition_and_estate_wide_bound` · `test_wexr_cp_exr1_render_export_and_release` · `test_wm3_sw8_pruning_unlearning` + contract snapshots (`api_key_issue_receipt`, `approval_decision`, `commissioned_job`, `standing_approval`, `suspension_act`, `terms_resolution`, `controlled_determination`). **Correction to prior assessment**: DAP DOES have L3 invariant coverage. L4 partial — server.py mount of a dedicated DAP router not visible in the includes list; DAP surfaces reach client via commission/checker/master_admin adjacents. |

### 2.5 APPS + EXECUTION (Layer 5)

| Component | Spec | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **Solva** (C.19 I-4 frame never touches fact hash) | | **L3 confirmed** | `test_reasoning_faculty_isolation::test_stage_does_not_import_defensibility_class` · `test_reasoning_faculty_isolation::test_stage_has_no_defensibility_class_return_annotation` · `test_reasoning_faculty_isolation::test_stage_does_not_construct_defensibility_class` · `test_reasoning_faculty_isolation::test_assertion_does_not_import_from_reasoning` · `test_compute_seam_artifact_hash_verified::test_verify_matches_returns_true` · `test_compute_seam_artifact_hash_verified::test_verify_mismatched_hash_raises` (**"artifact_hash_mismatch" refusal**) · `test_solva_assertion_boundary` · `test_solva_reasoning_stages` · `test_solva_trace_ledger_integration` · `test_wm4_sw1_solva_explain_surface` · `test_composed_conclusion_class_from_solva_boundary`. `solva_router` mounted at `/api` ✅. **L3 solid**; L4 partial (frame per D.5 not built). |
| **Targeta** (C.20 custody seam) | | **L3** | `test_targeta_invariants` · `test_p1_custody_closure` · `test_wregext_g3_cp_r2_typed_custody_class` · `test_wrg_cp_rg_hygiene_01_custody_cat_guard`. Custody seam + manifests per D.5 not fully built. |
| **CIF** (C.21) | | **L0** | Grep-negative on `services/cif/`. NOT-STARTED. |
| **Documents Suite + Wizards** (C.22) | | **L2** | `services/whitepapers/` + `services/wizard/` + `services/doc0_attributes/` + `services/transform_forms/` + `services/skill_files/` present with routers. Named C.22 I-x test-IDs fragmentary. |
| **Tenant Apps** (C.23) | | **L1** (external repo) | RMS-IQ-Core-2 separate repo. No application-contract enforcement wire in Extraction-Akki. |

### 2.6 M9 PLATFORM CONTROL PLANE (36 CPs) — corrected level

**Owner-provisional characterization**: "shape-only".
**On-disk verdict**: **L3 for structure-shape · L1 for runtime-enforcement · L0 for L2 wiring** — the 36 M9 modules have 373 named-invariant test IDs (all `test_p1_cp*.py` .. `test_p6_cp*.py`) but are NOT wired on HTTP. They are frozen-dataclass shape refusers imported nowhere in `routers/` or `server.py`. Confirmed on-disk: no `include_router` for `platform_control_plane`. **The rule "nothing above L2 without L3 evidence" caps them at "L3-shape-only" — an honest hybrid state**: invariant coverage is real, HTTP enforcement is absent. **M12 closes the L2+L4 gap.**

### 2.7 CROSS-CUTTING B.1..B.11 · authoritative levelling

| # | Standard | Verdict | Named-invariant test IDs |
|---|---|---|---|
| B.1 | Identity / AuthN / AuthZ | **L4 partial** for existing JWT/session path · **L0** for X-Akki-Context HMAC (δ-1) | `test_master_admin_auth_reconciliation` · `test_p2_cp4_session_binder` · `test_p2_cp5_break_glass_session` · `test_phase_8_b_1_auth_and_shims::*` · `test_wdslift_cp_d5_analysis_session` · `test_no_unauthorized_deletion_path`. `auth_router` mounted at `/api` ✅. Motor Mongo users collection live. **X-Akki-Context HMAC: NOT-STARTED (M11-W2).** |
| B.2 | Tenancy + Mongo isolation | **L0** for the platform · **L4** for auth users only | Only `services/auth/user_store.py` uses Motor Mongo. Grep-negative on `t_<tenant_id>` convention. **M11 owns.** |
| B.3 | Contracts / versioning / Idempotency-Key | **L2** | `contracts/` directory + `test_frozen_contract_snapshot_parity`. **Idempotency-Key: NOT-STARTED.** Path versioning `/v1/` exists via `routers/v1.py`. |
| B.4 | The Ledger hash-chained standard | **L0** | See §2.1 The Ledger. **M10 owns.** |
| B.5 | Secrets / keys / crypto / Ed25519 | **L0** | Grep-negative on Ed25519 / KMS integration. **M13-W2 owns.** |
| B.6 | OTel / SLOs / error budgets | **L0** | Grep-negative on `opentelemetry` imports. **M13-W3 owns.** |
| B.7 | Deployment / Terraform / Helm / RPO/RTO | **L0** | No `terraform/` or `helm/`. **M13-W4 owns.** |
| B.8 | TCB engineering rules (TCB.yaml + akki.arch + determinism corpus + 2-reviewer) | **L3 partial** | Chokepoint AST negative-scan test IS an import-assertion (real); `services/doc0_attributes/tcb.py` per-attribute marker; R-1..R-5 seal-chain integrity. **Repo-root `TCB.yaml` and global `akki.arch` CI job: NOT-STARTED (M13-W1 owns · MANDATORY FIRST per owner directive).** Byte-identical determinism corpus for TCB members: NOT-STARTED (M13-W5). |
| B.9 | Threat model | **L2 (implicit)** | Threat coverage distributed across Watch (adv 4) · chokepoint (adv 2) · break-glass P2-CP5 (adv 3) · cross-tenant P6-CP3 (adv 1). No single `threat_model.md` artefact banked. |
| B.10 | Ops / runbooks / SEV taxonomy | **L0** | Grep-negative on `akki-runbooks` or `SEV-1` taxonomy. **M13-W7 owns.** |
| B.11 | Human touchpoints (6 kinds) | **L3 partial** | Approval: `platform_control_plane/mode_change_approval.py` shape refuser. Ceremony: `rules_service/ceremony.py` (test_sw2_* IDs). Break-glass: `platform_control_plane/break_glass_session.py` + `test_p2_cp5_break_glass_session`. Refusal-surfaced: every M9 refuser uses COUNTS-only bodies (M9 invariants). Notification: NOT-STARTED. Confirmation: partial via `wizard/`. |

### 2.9 ANTI-FORGET / BOOT DISCIPLINE (new · CP-Anti-Forget-1 · owner ruling 2026-09-17T~20:45Z)

| Component | Anchor | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **R-6 anti-forget boot manifest** (STANDING_ORDERS §7 R-6) | `notes/ORCH_BOOT.md` (state · master) + byte-identical audit copy at `/app/frontend/public/audit/ORCH_BOOT.md` + always-on invariant `backend/tests/invariants/test_orch_boot.py` | **L5** | `test_orch_boot.py::test_orch_boot_anti_forget_manifest_matches_live_ratchet_and_sealed_heads` — hard-asserts (1) both copies exist + byte-identical, (2) `ratchet.passed_floor == baseline_failures.passed_floor`, (3) `ratchet.baseline_failures_sha256 == live sha256`, (4) `heads_last_sealed.*.head` are 40-hex + banked in DECISIONS/NEXT (full-40 or 7/8-hex short form) — NOT compared to live `git rev-parse HEAD` (races with §3.3 Commit-A/B/C ordering per owner refinement). Freshness enforced by R-6 boundary regeneration; not by always-on equality-to-live-HEAD test.  This is the drift-and-burn priority guard.  Included in CI ratchet (BASELINE_GUARD=1) since 2026-09-17T~13:17Z. |

### 2.10 TCB GOVERNANCE REGIME (new · CP-M13W1 · owner autopilot directive 2026-09-17T~13:30Z Option A · scoped current-tree only)

| Component | Anchor | Verdict | Named-invariant test IDs |
|---|---|---|---|
| **TCB.yaml manifest** (repo root · v1.0 A.4 TCB packages · `review_policy:` PENDING_OWNER_RATIFICATION) | `TCB.yaml` at code-repo root · 216 lines · enumerates 10 present-on-disk TCB packages + 3 PENDING_M10/M11/M12 rows + 3 protected_sdks + 4 rules + review_policy | **L5 for the CURRENT-tree scope** | Consumed by `tools/akki_arch/check_imports.py` + `test_akki_arch_import_assertions.py`. Owner review of the row list is an M11 gate item (additions/deletions land as follow-up CP). |
| **`akki.arch` global import assertions CI** (`tools/akki_arch/check_imports.py` · AST-based checker · 435 lines) | Reads TCB.yaml + walks tree. 4 rules: R-A-1 llm_sdk_sole_importer HARD (extends existing chokepoint AST negative-scan) · R-A-2 governor_cross_import_ban HARD with allowed_import_targets [`services.chokepoint` + `services.watch.capability_admission` shared-primitive submodule] · R-A-3 learned_decision_cross_import_ban HARD bidirectional · R-A-4 layer_up_import WARN advisory (may promote HARD after M11/M12 restructure). | **L5 (CI-ratcheted)** | `test_akki_arch_refuses_learned_to_decision` · `test_akki_arch_refuses_governor_cross_import` · `test_akki_arch_refuses_layer_up_import` · `test_akki_arch_current_tree_green` (walks entire code repo · asserts 0 HARD violations). All at BASELINE_GUARD=1 since 2026-09-17T~13:43Z. |
| **B.8 upgrade from L3-partial to L5** | v1.0 B.8 TCB engineering rules | **L5 for M13-W1 scope (C1+C2)** · **L0 for C3 (CI job wire) + C4 (branch protection)** · both admin-blocked per plan · surfaced at seal boundary | See row-2 test IDs above. Byte-identical determinism corpus for TCB members: NOT-STARTED (M13-W5 territory · separate CP). |
| **Rule-tension (a) partial resolution via shared-primitive exception mechanism** | TCB.yaml `allowed_import_targets:` list in R-A-2 | **Applied to `services.watch.capability_admission`** · signals the pattern future M12 restructuring can consume | Discovered during current_tree_green RED phase: `agent_containment/ceilings.py:8` imports `services.watch.capability_admission`. Resolved by allowlist rather than refactor (SO §3.8 held). Similar patterns future waves can catalog. |

### 2.8 FRONTENDS

Not levellable on this scale — no React/Expo code exists per v1.0 D-01. Standalone HTML mockups only. **L0.**

---

## 3 · GOVERNING RULES / DISCIPLINES (unchanged from prior snapshot · citation-anchored)

### 3.1 Tests-first RED → double-GREEN byte-match (`STANDING_ORDERS.md §3`)
### 3.2 BASELINE_GUARD=1 semantics (`baseline_failures.json` field `invariants_enforced_when_baseline_guard_1.passed_floor`)
### 3.3 Monotonic ratchet + no-silent-rebaselining (`STANDING_ORDERS.md §3` + `DECISIONS.md §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17`)
### 3.4 §3.3 3-commit protocol + state-only 2-COMMIT SHAPE (`STANDING_ORDERS.md §3.3` verbatim: *"NO SEAL WITHOUT BOTH SHAs — post-seal receipt rule (2026-09-15)"*)
### 3.5 Local-commits-only / no-push · code on programme/track-a · state on master (Owner directive every wave; recurring in DECISIONS.md verbatim log)
### 3.6 No-secrets-to-stdout + custody helpers (`STANDING_ORDERS.md §4` + chokepoint credential-shaped-prompt scrub)
### 3.7 NO `testing_agent` (owner ban · recurring; reconfirmed 2026-09-17)
### 3.8 Thin-kernel / no-refactor (`STANDING_ORDERS.md §3` + Owner Ruling 2026-09-16T~08:35Z "roll-straight")
### 3.9 Preventive-charter (not hard-gate) — M9 verbatim standing lines (**subject to M12/M12b upgrade to runtime enforcement**)
### 3.10 Zero closed enums · 21-token grep-negative · zero data-plane imports · frozen dataclasses (M9 invariant fabric · **tension flagged: see §5.2**)
### 3.11 POST-2 placement (`tenant_id` at field index 1 in every ownership-scoped M9 entity)
### 3.12 GPU check-in at every seal boundary + zero-perturbation (`STANDING_ORDERS.md §5 GPU OBLIGATIONS`)
### 3.13 R-1..R-6 seal-chain integrity + anti-forget rules (`STANDING_ORDERS.md §7` · owner-ratified 2026-09-17T~09:15Z + R-6 addition 2026-09-17T~20:45Z)
### 3.14 Boot ritual + anti-"Chunk-1-drift" (`STANDING_ORDERS.md §1`)

### 3.15 NEW · Evidence Bar L1-L5 + Definition of Done (owner-authoritative 2026-09-17T~20:00Z)

Applies to every milestone from M10 onward. Recorded verbatim at §0 + §0.1 above. Adds:
- **DoD gate 1**: every closed C.n I-x mapped to a test ID passing under `BASELINE_GUARD=1`.
- **DoD gate 2**: D.3 platform tests (P-nn) the milestone enables pass.
- **DoD gate 3**: affected components re-levelled.
- **DoD gate 4**: D.5 regenerated from levelled table.
- **DoD gate 5**: milestone's Ledger rows visible end-to-end (Ledger is a first-class evidence surface from M10 on).
- **Currency**: test IDs, not assertion counts or LOC.
- **Cap rule**: nothing above L2 without L3 evidence.

---

## 4 · AUTHORITATIVE STATE SUMMARY (one paragraph · revised)

The Akki OS build is a substantial live-running FastAPI application (`backend/server.py` + ~55 mounted HTTP routers · 78,549 LOC across 101 service dirs · 109,357 LOC of tests · 468 test files under `tests/invariants/` · 3,727 raw `def test_*` occurrences · 4,810 pytest invariants passing under `BASELINE_GUARD=1` byte-match). Under the owner-authoritative Evidence Bar L1-L5 (2026-09-17T~20:00Z): **at L4 or above** — the LLM chokepoint (C.1 · AST-enforced sole-importer + purpose/masking-tier/endpoint-allowlist gates + crossing receipts · 10+ named test IDs) and Auth for the existing JWT/session path (B.1 · test_p2_cp4_session_binder + test_phase_8_b_1_auth_and_shims); **at L5** — R-6 anti-forget boot manifest (STANDING_ORDERS §7 · `notes/ORCH_BOOT.md` + `test_orch_boot.py` · always-on ratchet + baseline-sha256 hard-dynamic guard); **at L3** — Northena append-only writer (C.2/C.4-file-partial · corrected up from L2) · Watch registry-only-action (C.3 I-2 · test_watch_cp_c2_http_journey suite) · Model Admission (C.6 I-1 · test_run_admission_refuses_unresolved_lineage) · Rules Service atomic-apply (C.5 I-3 · test_sw2_complete_ceremony_applies_flip) · Critic Seam wire (C.10 · test_r4_8_critic_seam_producer_wiring) · Agent Containment (C.11 I-1/I-2 · test_sw7_narrow_start_admits_minimum_only · test_sw7_ac3_no_scope_before_admission) · Solva frame-isolation (C.19 I-4 · test_reasoning_faculty_isolation + test_compute_seam_artifact_hash_verified) · Targeta custody (C.20) · Mtafiti (C.12) · Memory (C.13) · DAP (C.18 · corrected: 5+ wdap test IDs on disk) · M9 platform control plane (373 test IDs across 36 CPs, shape-only, NOT wired on HTTP · L3-shape-only hybrid); **at L0-L2** — C.4 hash-chained Ledger + verifier (M10 target) · B.2 Mongo-per-tenant (M11 target) · X-Akki-Context HMAC (M11-W2) · B.5 KMS/Ed25519 (M13-W2) · B.6 OTel/SLOs (M13-W3) · B.7 Terraform/Helm (M13-W4) · B.8 TCB.yaml + akki.arch global CI (M13-W1 · owner-declared MANDATORY FIRST) · B.10 runbooks (M13-W7) · C.7 output-content gate (not-started) · C.15 Mkondo runtime (not-started) · C.21 CIF (not-started · L0) · Frontends per C.18 DAP + C.23 RMS AI Prototype v2 (not-started as React/Expo). M9 sealed cleanly + CP-Anti-Forget-1 landed at ratchet 4810 · master HEAD advancing this snapshot commit · track-a HEAD `fd4432a` · R-1..R-6 seal-chain integrity + anti-forget rules ratified · 20-CP master-side back-compat gap reconciled. GPU 72h campaign on cadence.

---

## 5 · RULE-TENSION PROPOSALS (owner to rule · surface only)

Two rule tensions were flagged by owner to resolve BEFORE M11 opens. Both are proposals with an agent recommendation; owner rules.

### 5.1 · Tension (a) — "thin-kernel / no-refactor" vs B.2's mandatory repository layer

**Statement of tension**: SO §3.8 (thin-kernel / no-refactor · additive CPs only · no existing-file rewrites) forbids modifying sealed M9 modules. B.2 mandates that every state-changing surface use `akki.data` repository primitives (`repo.find/insert_one/update_one/delete_one/aggregate`) with auto-injected `{tenant_id: ctx.tenant_id}` filters and cross-tenant-write rejection. Wiring the 36 M9 shape refusers to real Mongo persistence therefore requires *either* (i) modifying M9 modules to import the repository (refactor · violates SO §3.8), or (ii) writing new wrapper modules that call M9 refusers + the repository (additive · does not touch M9 code but doubles the module count).

**Options**:

- **Option A · Additive wrapper (strict SO §3.8 preserved)**. Every M9 module gets a sibling `<module>_repo.py` wrapper that: (1) calls the M9 refuser first (`assert_X_valid(record=...)`), (2) then calls `repo.<op>(...)`. AST negative-scan test refuses any file except the wrapper to import both `<module>` and `repo`. Rework: 36 new modules; zero M9 changes.
  - **Pro**: SO §3.8 held verbatim. All 36 sealed M9 CPs remain byte-identical. R-4 session-handoff briefs stay honest.
  - **Con**: Doubles module count for M9 layer. Two-file discipline per entity may drift under pressure. Wrappers duplicate imports and typing.

- **Option B · Narrow refactor exception under owner rule (SO §3.8 amended)**. Owner rules a one-time, milestone-scoped, explicit exception for the M11 CPs: each M9 module gains ONE import line + one `Depends(repo_factory)` in a new `enforce_*` function. Existing frozen carriers + refuser wrappers untouched. Test IDs re-run; if any invariant breaks, the exception is revoked. Rework: 36 file edits of ~2-3 lines each.
  - **Pro**: Single-file-per-entity discipline preserved. Cleaner call sites. Less duplication.
  - **Con**: SO §3.8 loses its absolute status; future waves may cite this as precedent. Requires owner ruling recorded verbatim in DECISIONS.md.

- **Option C · Hybrid (recommend)**. M9 modules stay frozen (SO §3.8 held). A new **thin adapter layer** at `services/enforce/<entity>_gate.py` is authored — one adapter per M9 entity — that: (1) imports the M9 refuser (allowed since M9 modules export refusers), (2) imports `akki.data.repo`, (3) exposes a single `Depends()` factory that FastAPI routes bind to. AST negative-scan enforces: only `services/enforce/` may import both. Rework: 36 new tiny adapter modules (~15 LOC each) + zero M9 changes.
  - **Pro**: SO §3.8 held strictly. Adapters live in a dedicated layer (`services/enforce/`) with its own AST gate. No duplication of M9 shape; adapters only add the persistence + Depends wiring. Cleaner than Option A (single layer) without amending SO like Option B.
  - **Con**: Introduces a new architectural layer that needs its own discipline. Requires an M12-W1 preamble to define the adapter contract.

**Agent recommendation**: **Option C**. Preserves SO §3.8 verbatim; introduces one clean layer with its own AST gate (matching the chokepoint precedent); each adapter is ~15 LOC and testable independently.

### 5.2 · Tension (b) — "zero closed enums" vs fixed enumerations B.8 determinism tests depend on

**Statement of tension**: SO §3.10 (zero closed enum type in any M9 module · all values are OPEN `str` carriers) is verbatim in every M9 seal note. B.8 mandates byte-identical golden-input determinism tests for TCB components. Some TCB components genuinely have finite closed enumerations (e.g., Watch verdict actions: **destroy · sever · contain · monitor** per C.3; permission verbs: **read · write · admin · dangerous** per B.1; capability ceilings: 12 named per C.11). A determinism test requires the closed set to be enumerated somewhere authoritative so the harness can generate golden inputs across the full state space.

**Observation from disk**: **Some C.n components ALREADY carry closed enumerations in tests without using `enum.Enum`**:
- `test_watch_action_v0_contract_frozen::test_four_class_closed_grammar` — 4 action classes as a closed grammar tuple
- `test_wm3_sw7_agent_containment::test_sw7_all_twelve_ceilings_enumerated` — 12 ceilings enumerated
- `services/watch/contracts/watch_action_v0.py::ACTION_CLASSES` — likely a tuple, not an Enum
- M9's `PILOT_TENANT_KEYS = ("RMS", "DigiCow", "BDO", "Trinity")` — closed tuple, not Enum

So SO §3.10 as authored bans `enum.Enum` specifically, not fixed enumerations as `tuple[str]` literals. This may already be reconciled by convention. But the phrase "zero closed enums" is imprecise — it could mean either (i) no `enum.Enum` class (technical), or (ii) no fixed-vocabulary tuple at all (semantic).

**Options**:

- **Option α · Clarify SO §3.10 as technical (recommend)**. Owner ratifies: "zero closed enum type" means **zero use of `from enum import Enum` or subclassing `Enum` / `IntEnum` / `str, Enum`**. Fixed-vocabulary `tuple[str, ...]` module-level constants (e.g., `ACTION_CLASSES = ("destroy", "sever", "contain", "monitor")`) are ALLOWED and enable B.8 determinism harnesses.
  - **Pro**: Matches on-disk practice already in Watch, Agent Containment, and M9 pilot register. No M9 rework. B.8 determinism corpus can enumerate golden inputs.
  - **Con**: Requires SO §3.10 amendment note. Some CPs may need a lint pass to confirm no `Enum` subclass slipped in.

- **Option β · Ban tuples too; every closed set is a JSON config**. Every finite enumeration lives in a `.v0.json` file (like `masking_tier_allowlist.v0.json`, `continuity_policy.v0.json`, `feasibility_config.v0.json` already in the codebase). Modules read the JSON at import time; B.8 golden-input harness enumerates from the JSON.
  - **Pro**: Uniform enumeration source. Owner-versioned. Easier B.3 schema evolution.
  - **Con**: Module import-time file IO. Existing tuple constants in Watch + M9 need conversion. High rework impact.

- **Option γ · Closed enum ban is a design rule, not a correctness invariant**. Delete SO §3.10 entirely. Owner rules that "zero closed enum" was a defensive stance against premature type freezing during M9 shape-freeze work but is no longer binding.
  - **Pro**: Removes the tension outright.
  - **Con**: Loses the discipline benefit of forcing values into OPEN `str` carriers (which enables extension without a major schema bump per B.3). Not recommended.

**Agent recommendation**: **Option α**. Codifies existing on-disk practice; amends SO §3.10 to specify "no `enum.Enum` subclass" without touching tuple-literal enumerations. Preserves the discipline benefit while unblocking B.8 determinism harnesses.

**Owner ruling required on both (a) and (b) BEFORE M11 opens.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
