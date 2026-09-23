---
card_id: CP_AIP_ASSIST_CENSUS_20260223
title: Census Assistant — six binding conditions verbatim (no path to any decision · confirmed turns only banked · read-only against Registry · MOAC owner-set only · anchored+gated content · no learning from dialogue) · Item 5.11.f
ratified_at_utc: 2026-02-23T15:30:00Z
ratified_by: Owner drop verbatim 2026-02-23 `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md` (Track-5 pre-build checkpoint REMOVED · CP-AIP-ASSIST cards PRE-APPROVED BY CONSTRUCTION under §6.8 standing authority) + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 (E1 wires the seam INTO Census Autonomy Service; pod NEVER data path).
card_sha256: 3a996943801ba1d8d5919baa2313ccb24feb330fc64c74bab0dc6384b3e8f79b
milestone_status: OPEN (Item 5.11.f · opens immediately post CP-TRACK-4-AUTONOMY-WIRING seal · 6th item of Item 5.11 wave · REPORT-AND-CONTINUE not idle-halt · RUN-TO-COMPLETION mandate ACTIVE)
---

# CP-AIP-ASSIST-CENSUS-20260223 · Census Assistant · six binding conditions verbatim as MUST-DO/MUST-NOT test IDs

## OBJECTIVE

Land the additive Census Assistant boundary as pure §1.2 modality-extension composing sealed CP-AIP-6 wizard `services/wizard/objective_compile.py` (compile_target_outcome + compile_collection_schema + ObjectiveSession_v0) + sealed Census Autonomy Service `services/census_autonomy/response_required_queue.py` (bank_response_required_item) + sealed CP-TRACK-4-AUTONOMY-WIRING `services/census_autonomy/track_4_autonomy_wiring_v1.py` (Track4LidPassRegistration_v1 + AutonomyEngineRunReceipt_v1 + register_all_three_track_4_jobs). Bind the six binding conditions verbatim as MUST-DO/MUST-NOT test IDs. Placement OUTSIDE the TCB. Every user-facing string is a Content Registry entry. Zero sealed-carrier edit per SO §3.8. Ruling (b) AKKI-RUNS-IT verbatim honored structurally: the assistant module has zero decision-boundary imports; pod is never a data path.

`canon_ref: SO §6.9 amendment 2026-02-23 + owner drop 2026-02-23 assist_cards_preapproved_and_run_to_completion_20260223 verbatim (six binding conditions as MUST-DO/MUST-NOT test IDs) + Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23 + §1.2 modality-extension + §1.5 unrepresentable-not-policed (refusal exceptions rather than silent bypass) + §6.9 markers-over-refusal.`

## MUST DO

1. **Binding condition (1) — No path to any decision (negative-scan import isolation)** — the assistant module MUST NOT import any decision-making boundary of the TCB (approve_by_any_one_named_authority, TenantApprovalDecision_v1, create_tenant_with_pilot_licence_seed, admit_material, commit_baseline_line, lawful_basis_admit, chokepoint_resolver). Enforced by `test_assist_no_path_to_any_decision_negative_scan_import_isolation`.
2. **Binding condition (2) — Confirmed turns only banked (A5.16 receipted provenance)** — `bank_confirmed_assistant_turn()` refuses `confirmed_by_owner=False` or empty `a5_16_receipt_ref` via `UnconfirmedTurnBankRefused`. Enforced by `test_assist_confirmed_turn_only_banked_a5_16_receipted_provenance`.
3. **Binding condition (3) — Census assistant read-only against Registry (B5.1 byte-identical)** — `ASSIST_CENSUS_READONLY_POSTURE` Final marker + AST scan bans any Registry-write callable (asset_registry_writer / write_asset / route_asset_registry_write / bank_response_required_item) from being called inside the assistant module. Enforced by `test_assist_census_readonly_with_without_byte_identical_b5_1`.
4. **Binding condition (4) — Training proposals freeze at commission; MOAC owner-set only** — `MOAC_OWNER_SET_ONLY_POSTURE` Final marker + AST scan bans any MOAC/training-proposal declaration (MOAC / moac_criteria / propose_training_run / set_moac) from being declared inside the census assistant module (training surface belongs to CP-AIP-ASSIST-TRAINING Item 5.11.g). Enforced by `test_assist_training_proposals_freeze_at_commission_moac_owner_set_only`.
5. **Binding condition (5) — Content generated · chat surface · anchored · gated (R-32/A5.15/CON-6)** — `render_content_registry_entry()` returns `ContentRegistryEntry_v1(content_registry_ref, a5_15_anchor_ref, con_6_gate_ref, honest_marker)`. Refuses missing `a5_15_anchor_ref` (must start with `a5_15://`) or missing `con_6_gate_ref` (must start with `con_6://`) via `UngatedContentRefused`. `honest_marker` in Literal(unmeasured/INFERRED/honest-gap/fallback/None) for §6.9 markers-over-refusal. Enforced by `test_assist_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal`.
6. **Binding condition (6) — No learning from dialogue (L-4/L-5 only admission path)** — `NO_LEARNING_FROM_DIALOGUE_POSTURE` Final marker + AST scan bans any learning-write function (learn_from_dialogue / train_from_conversation / dialogue_to_training / feed_learner) from being defined inside the assistant module. Enforced by `test_assist_no_learning_from_dialogue_l4_l5_only_admission_path`.
7. **Frozen `CensusAssistantConfirmedTurn_v1` carrier shape** — session_id + tenant_id + role + content_registry_ref + confirmed_by_owner (always True for banked) + confirmed_at_utc + a5_16_receipt_ref. Frozen dataclass. Enforced by `test_assist_frozen_confirmed_turn_carrier_shape`.
8. **`PLACEMENT_OUTSIDE_TCB_POSTURE` Final marker** verbatim citing owner clause. Enforced by `test_assist_placement_outside_tcb_posture_marker_present`.
9. **§1.2 no-redeclaration** of sealed CP-AIP-6 wizard symbols (compile_target_outcome, compile_collection_schema, ObjectiveSession_v0) + Census Autonomy Service (bank_response_required_item, route_asset_registry_write, run_bounded_census, enqueue_on_demand_run) + Track-4 (Track4LidPassRegistration_v1, AutonomyEngineRunReceipt_v1, register_all_three_track_4_jobs). Enforced by `test_assist_no_redeclaration_of_sealed_symbols_1_2`.
10. **`SIX_BINDING_CONDITIONS_POSTURE` Final 6-tuple** citing each binding condition verbatim. Enforced by `test_assist_six_binding_conditions_posture_markers_all_present`.

## MUST NOT DO

- No edit to sealed `services/wizard/objective_compile.py` (CP-AIP-6 closed).
- No edit to sealed `services/census_autonomy/response_required_queue.py` (Phase 3 A''' closed).
- No edit to sealed `services/census_autonomy/data_source_adapter.py` (Phase 3 A'''' closed).
- No edit to sealed `services/census_autonomy/engine.py` (R-106 closed).
- No edit to sealed `services/census_autonomy/track_4_autonomy_wiring_v1.py` (CP-TRACK-4-AUTONOMY-WIRING closed at Item 5.11.e).
- No import of any decision-boundary callable (binding condition 1).
- No banking of unconfirmed turns (binding condition 2).
- No Registry-write callable invocation from the assistant module (binding condition 3).
- No MOAC / training-proposal surface in this module (binding condition 4 · belongs to Item 5.11.g).
- No user-facing string outside a Content Registry entry with A5.15 anchor + CON-6 gate (binding condition 5).
- No learning-from-dialogue callable (binding condition 6).
- No redeclaration of any sealed CP-* symbol (§1.2 no-redeclaration).
- No refactor per SO §3.8 additive-only.
- No `testing_agent` per SO §3 (bans).

## NEW ADDITIVE MODULES

`backend/services/census_autonomy/assist_census_v1.py` (§1.2 modality-extension · ~185 lines · `ASSIST_CENSUS_READONLY_POSTURE` + `MOAC_OWNER_SET_ONLY_POSTURE` + `NO_LEARNING_FROM_DIALOGUE_POSTURE` + `PLACEMENT_OUTSIDE_TCB_POSTURE` + `SIX_BINDING_CONDITIONS_POSTURE` Final 6-tuple + `AssistCensusBoundaryRefused` base + `UnconfirmedTurnBankRefused` + `UngatedContentRefused` refusal subclasses + `CensusAssistantConfirmedTurn_v1` + `ContentRegistryEntry_v1` frozen carriers + `bank_confirmed_assistant_turn` + `render_content_registry_entry` boundary callables).

Test file: `backend/tests/invariants/test_cp_aip_assist_census.py` (10 RED-first pins).

## SEALED CARRIERS TO NOT EDIT

- CP-AIP-6 `services/wizard/objective_compile.py` (Objective Wizard sealed · compile_target_outcome + compile_collection_schema + ObjectiveSession_v0).
- Census Autonomy Service `services/census_autonomy/response_required_queue.py` (Phase 3 A''' sealed · bank_response_required_item).
- Census Autonomy Service `services/census_autonomy/data_source_adapter.py` (Phase 3 A'''' sealed · route_asset_registry_write).
- Census Autonomy Service `services/census_autonomy/engine.py` (R-106 sealed · run_bounded_census + enqueue_on_demand_run).
- CP-TRACK-4-AUTONOMY-WIRING `services/census_autonomy/track_4_autonomy_wiring_v1.py` (Item 5.11.e sealed 2026-02-23 · Track4LidPassRegistration_v1 + AutonomyEngineRunReceipt_v1 + register_all_three_track_4_jobs).

## EXIT (RED-first invariant node IDs)

1. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_no_path_to_any_decision_negative_scan_import_isolation`
2. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_confirmed_turn_only_banked_a5_16_receipted_provenance`
3. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_census_readonly_with_without_byte_identical_b5_1`
4. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_training_proposals_freeze_at_commission_moac_owner_set_only`
5. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_content_r32_a515_con6_anchored_gated_honest_marker_over_refusal`
6. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_no_learning_from_dialogue_l4_l5_only_admission_path`
7. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_frozen_confirmed_turn_carrier_shape`
8. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_placement_outside_tcb_posture_marker_present`
9. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_no_redeclaration_of_sealed_symbols_1_2`
10. `backend/tests/invariants/test_cp_aip_assist_census.py::test_assist_six_binding_conditions_posture_markers_all_present`

## STOP

Stop at owner ratification of this card. If Owner rules SPEC-CONFLICT-<n>, HALT and log it in DECISIONS.md as SPEC-CONFLICT with the conflict text verbatim + which sealed carrier / owner clause is violated + proposed resolution. Owner ruling required to unblock. Otherwise (no conflict), REPORT-AND-CONTINUE into Item 5.11.g (CP-AIP-ASSIST-TRAINING · same six binding conditions applied to training-run dialogue) per RUN-TO-COMPLETION mandate 2026-02-23.

## ANCHORS

- **Owner canon (owner drop 2026-02-23 verbatim):** `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md` — Track-5 pre-build checkpoint REMOVED; CP-AIP-ASSIST cards PRE-APPROVED BY CONSTRUCTION under §6.8 standing authority; six binding conditions verbatim as MUST-DO/MUST-NOT test IDs.
- **Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:** 'E1 wires the seam INTO the Census Autonomy Service. Pod is never a data path.' Honored structurally: assistant module has zero decision-boundary imports (binding condition 1 negative-scan) + zero Registry-write callables (binding condition 3).
- **Sealed carriers extended (unchanged this seal per SO §3.8):** listed under `SEALED CARRIERS TO NOT EDIT` above.
- **Standing Orders:** SO §3 RED-first · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §6.4 same-seal orthogonal fold-in gap-closure · SO §6.8 pre-approval by construction · SO §6.9 desk discipline (markers-over-refusal + one-sentence protected-objective on every refusal/hold/gate) · SO §7 17-guard consolidated set.
- **Objective card hash-pin protocol:** `card_sha256` computed over card text with the `card_sha256:` frontmatter line removed (line-removed convention · pin protocol consistent with prior seals CP-TENANT-SEPARATION + CP-CENSUS-THREE-WAVES + CP-TRACK-4-AUTONOMY-WIRING).
- **Ledger check:** this card ratifies `CP-AIP-ASSIST-CENSUS` and nothing else. Additive-only per SO §3.8.

## RATIFICATION

Owner drop 2026-02-23 `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md` PRE-APPROVED BY CONSTRUCTION under §6.8 standing authority (Track-5 pre-build checkpoint REMOVED). Card ratified at 2026-02-23T15:30:00Z. Six binding conditions verbatim as MUST-DO/MUST-NOT test IDs.
