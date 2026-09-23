---
card_id: CP_AIP_6_OBJECTIVE_WIZARD
title: AIP v1.0 §8 Objective Wizard + §9 Collection Schema + §12.1 Registry Namespace · compile-time rejections + baseline-tier frozen v1.0 + sealed-not-deleted namespace · Item 5.6 CP-AIP-6
ratified_at_utc: 2026-02-23T07:50:00Z
ratified_by: Owner cadence directive (2026-02-23 CP-AIP-4 GO verbatim) 'run CP-AIP-5 → CP-AIP-10 sequentially · brief report-and-continue after CP-AIP-6 seals · HALT after CP-AIP-10 for full plane completion report · immediate HALT on any SPEC-CONFLICT-<n>' + Item-4 checkpoint GO + §16.1 (c) CLEAN receipt (2026-02-23T05:00:00Z) verbatim recommendation ('extend existing state machine with additive `objective` variant on WizardCommitState_v0.variant Literal · sibling machine explicitly rejected per §1.2').
card_sha256: 2147181fd6e598cc0619286eab63558802871298875aba93c0e7fc8a3b115fb9
milestone_status: OPEN (Item 5.6 CP-AIP-6 · in-flight for this seal · brief report-and-continue after seal per owner cadence)
---

# CP-AIP-6-OBJECTIVE-WIZARD · AIP v1.0 §8 + §9 + §12.1

## OBJECTIVE

Land the additive Objective Wizard compile boundary + Collection Schema two-tier contract + Registry Namespace sealed-not-deleted per AIP v1.0 §8 + §9 + §12.1 as pure §1.2 modality-extension of sealed CP-M11-wizard state machine (`operator_state_machine.py` + `WizardCommitState_v0` + `turn_ledger.py` + `session_persistence.py` + `admission_handoff.py` + `agent_interface.py`). Zero sealed-carrier edit per SO §3.8 · §16.1 (c) CLEAN receipt applied verbatim (sibling contract lands the objective variant; sealed `WizardCommitState_v0` is NOT edited).

Every §8.4 compile-time rejection is enforced by RED-first pytest invariants: (i) `TestSetRefMissing` on empty/whitespace `test_set_ref` (§8.4 + §10.2 verbatim 'The test set precedes the training'), (ii) `AcceptanceBarNotStratified` on empty/malformed acceptance (§8.4 + §10.2 verbatim 'Acceptance is per stratum'), (iii) `CustodyViolation` on Collection Schema columns whose names contain §6.2-custody-violating tokens (§8.4 verbatim). §9.2 baseline tier v1.0 contents are encoded as a frozen 5-tuple (`language_identification`, `code_switch_points`, `condition_profile`, `dedup_instance_condition_map`, `synthesis_relevant_group_level_acoustics`) per §9.2 verbatim. §12.1 registry namespace closure state is `sealed` (never `deleted`) — structurally enforced (`AudioModalityNamespace_v0` has NO `delete()` method; §1.5 unrepresentable-not-policed). §12.1 writes are namespace-scoped (every `ScopedWrite_v0` carries the `commission_id`); reads compose with the global registry. §8.5 `ObjectiveSession_v0` records `options_considered` AND `options_rejected` (the "why was the model built this way" ledger anchor).

`canon_ref: AIP v1.0 §8.1..§8.5 + §9.1..§9.3 + §10.1..§10.2 + §12.1 + §16.1 (c) CLEAN receipt verbatim + §16.2 baseline-tier PENDING-OWNER-CONFIRMATION + §1.2 modality-extension + §1.5 unrepresentable-not-policed + §6.2 custody conditions.`

Owner content anchor (Item-4 GO): the wizard MUST land BEFORE the planner (CP-AIP-7) — §15 P234 verbatim: 'The planner must never accept a hand-authored Outcome once the wizard exists; building the planner first invites the malformed-input class the compile stage makes impossible.'

## MUST DO

1. **§8.4 verbatim · Outcome without existing test_set_ref REJECTED at compile** — `compile_target_outcome(..., test_set_ref="")` refuses with `TestSetRefMissing`. §10.2 verbatim: 'The test set precedes the training.' Enforced by `test_compile_rejects_outcome_without_test_set_ref`. `canon_ref: AIP §8.4 + §10.2 verbatim.`

2. **§8.4 verbatim · Acceptance bar missing per-stratum dimension REJECTED at compile** — `compile_target_outcome(..., acceptance={})` refuses with `AcceptanceBarNotStratified`. §10.2 verbatim: 'Acceptance is per stratum.' Also refuses any stratum entry missing both `accuracy` + `coverage` dimensions per §10.1 verbatim two-dimensional shape. Enforced by `test_compile_rejects_acceptance_bar_without_per_stratum_dimension`. `canon_ref: AIP §8.4 + §10.1 + §10.2 verbatim.`

3. **§8.4 verbatim · CollectionSchema with §6.2-custody-violating column REJECTED at compile** — `compile_collection_schema(..., objective_tier=("per_utterance_embedding",))` refuses with `CustodyViolation`. Structural token scan on `voiceprint` / `per_utterance_embedding` / `speaker_id` / `speaker_embedding` / `raw_audio` / `utterance_bytes` / `audio_bytes` / `exemplar` (mirrors CP-AIP-3 write-boundary discipline). Enforced by `test_compile_rejects_collection_schema_with_custody_violating_column`. `canon_ref: AIP §8.4 + §6.2 verbatim.`

4. **§9.2 baseline tier v1.0 verbatim frozen 5-tuple** — `BASELINE_TIER_V1_0_CONTENTS = ("language_identification", "code_switch_points", "condition_profile", "dedup_instance_condition_map", "synthesis_relevant_group_level_acoustics")` per §9.2 verbatim; PENDING-OWNER-CONFIRMATION per §16.2 owner working default 2026-02-23T04:15Z; ceremony-governed for any additive change per §9.2 last sentence. Enforced by `test_baseline_tier_contents_match_v1_0_exact_verbatim`. `canon_ref: AIP §9.2 verbatim + §16.2.`

5. **§12.1 namespace closure state · sealed never deleted** — `AudioModalityNamespace_v0.close()` transitions `namespace_state` from `'open'` to `'sealed'`; there is NO `delete()` method on the class (§1.5 unrepresentable-not-policed). Enforced by `test_registry_namespace_closes_to_sealed_never_deleted`. `canon_ref: AIP §12.1 verbatim + §1.5.`

6. **§12.1 reads-compose-global · writes-namespace-scoped** — every `ScopedWrite_v0` record carries the `commission_id`; writes on a sealed namespace refuse; write path returns a new frozen namespace (append-only). Enforced by `test_registry_namespace_writes_are_scoped_reads_compose_global`. `canon_ref: AIP §12.1 verbatim.`

7. **§8.5 objective_session data class carries options_considered + options_rejected + refs** — `ObjectiveSession_v0` frozen dataclass with 6 carriers (`session_id` + `variant` + `options_considered` + `options_rejected` + `target_outcome_ref` + `collection_schema_ref`). §8.5 verbatim. Enforced by `test_wizard_objective_commit_state_has_objective_session_data_class`. `canon_ref: AIP §8.5 verbatim.`

8. **§8.5 options_rejected structurally a subset of options_considered** — `ObjectiveSession_v0.__post_init__` refuses construction if `options_rejected` is not a subset of `options_considered` (§8.5 verbatim answerability discipline). Enforced by `test_objective_session_records_options_considered_and_rejected`. `canon_ref: AIP §8.5 verbatim.`

9. **§1.2 no-redeclaration scan of 4 sealed wizard state carriers** — NEW modules do NOT redeclare `WizardCommitState_v0` / `OperatorTurn_v0` / `CommittedValue_v0` / `AgentAssumption_v0` (structural class-declaration scan on all 5 NEW modules). Enforced by `test_new_modules_do_not_redeclare_sealed_wizard_carriers`. `canon_ref: AIP §1.2 verbatim + §16.1 (c) CLEAN receipt.`

10. **Anti-drift §3 + §5 anchor scan · §8 + §9 + §10 + §12.1 citations + ledger-check** — every NEW module cites its exact AIP section anchor + carries the ledger-check anchor. Enforced by `test_new_modules_cite_section_anchors_and_ledger_check`. `canon_ref: Anti-drift standing guard §3 + §5.`

11. **10 RED-first pytest invariants** — RED_pre 10/10 failed → GREEN_post 10/10 passed. Each pin cites the exact §8 / §9 / §10 / §12 / §1 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

12. **Frozen contract snapshot parity fold-in** — 3 new frozen-dataclass modules (`target_outcome_v0.py` + `collection_schema_v0.py` + `wizard_objective_commit_state_v0.py`) added to `NON_CONTRACT_UTILITY_MODULES` in `test_frozen_contract_snapshot_parity.py` per established pattern (like `canon_census_source_candidate.py`, `data_suite_workspace.py`). Append-only addition to a mapping — no test surface change. `canon_ref: SO §3.8 additive + FL-P4-W6-08 naming rationale.`

13. **Ratchet floor 6292 → 6302** — +10 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · `ratchet_history` entry appended schema-complete (`passed=6302`). `invariants_enforced_when_baseline_guard_1.passed_floor` advanced in lock-step. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

14. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1..5 seals. Terminal `pytest` only. `testing_agent` BANNED. `BASELINE_GUARD=1 PYTHONHASHSEED=0` double-green byte-identical `stripped_sha256`. `canon_ref: SO §3.3 5-Commit-Seal + Six Standing Bans.`

## MUST NOT

- Edit any sealed §8 / §9 / §12 carrier (`contracts/wizard_commit_state.py` + `services/wizard/operator_state_machine.py` + `turn_ledger.py` + `session_persistence.py` + `admission_handoff.py` + `agent_interface.py`), or any prior CP-AIP-1/2/3/4/5 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only + §16.1 (c) CLEAN receipt verbatim.`

- Redeclare any of the 4 sealed wizard state carriers (`WizardCommitState_v0` / `OperatorTurn_v0` / `CommittedValue_v0` / `AgentAssumption_v0`). `canon_ref: AIP §1.2 verbatim + BL #4.`

- Emit a TargetOutcome without an existing `test_set_ref`. §10.2 verbatim. `canon_ref: AIP §10.2.`

- Emit a TargetOutcome with an acceptance bar missing per-stratum dimension. §10.2 verbatim. `canon_ref: AIP §10.2.`

- Emit a CollectionSchema requiring a §6.2-custody-violating column. §8.4 verbatim. `canon_ref: AIP §8.4 + §6.2.`

- Delete a registry namespace. §12.1 verbatim ('sealed, not deleted'). `canon_ref: AIP §12.1 + §1.5.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else. Wizard state machine + full elicitation flow are deferred to follow-on slices per scope-freeze SO §3.8. `canon_ref: SO §7 guard 5.`

## EXIT

**10 RED-first invariants (RED_pre 10/10 failed · GREEN_post 10/10 passed):**

- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_compile_rejects_outcome_without_test_set_ref
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_compile_rejects_acceptance_bar_without_per_stratum_dimension
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_compile_rejects_collection_schema_with_custody_violating_column
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_baseline_tier_contents_match_v1_0_exact_verbatim
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_registry_namespace_closes_to_sealed_never_deleted
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_registry_namespace_writes_are_scoped_reads_compose_global
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_wizard_objective_commit_state_has_objective_session_data_class
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_objective_session_records_options_considered_and_rejected
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_new_modules_do_not_redeclare_sealed_wizard_carriers
- tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py::test_new_modules_cite_section_anchors_and_ledger_check

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6292 → 6302 (+10 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical `stripped_sha256 8d8518c9dc0f75a545dfe3b0c7452dd9128eef0a6b7ecd1d492427d44b20e4a3` · 6311 passed / 1 skipped / 0 failed / 520 warnings both sweeps

## STOP

Stop at 5-commit seal landing. **Brief report-and-continue** (no halt · just a status update to owner) then IMMEDIATELY proceed to CP-AIP-7-TARGET-OUTCOME-PLANNER per owner cadence directive.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §8 / §9 / §10 / §12.1 / §16.1 (c) CLEAN receipt, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately. `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3 + owner cadence directive.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §8.1 role: 'The Objective Wizard elicits an objective in plain language and compiles two governed artifacts: TargetOutcome (§10) + Collection Schema (§9).'
- §8.2 elicitation sequence: question · population resolved against register strata · acceptance bar per stratum two-dimensional · collection consequences with cost visible.
- §8.3 propose-qualify-graduate discipline (deferred to follow-on slices per scope-freeze).
- §8.4 verbatim compile-time rejections (a) (b) (c) — all THREE enforced structurally this seal.
- §8.5 verbatim ledger stamping + options considered + options rejected.
- §9.1 definition · §9.2 baseline tier v1.0 verbatim contents · §9.3 objective tier declared per commission.
- §10.1 verbatim seven-field TargetOutcome schema + §10.2 verbatim binding rules.
- §12.1 verbatim namespace: per commission · scoped · reads compose global · writes namespace-scoped · closed-to-sealed-never-deleted.
- §15 P234 verbatim: 'The planner must never accept a hand-authored Outcome once the wizard exists.'
- §16.1 (c) CLEAN receipt verbatim (2026-02-23T05:00:00Z at `phase0/aip_spec_verification_20260223/receipt.md`): 'extend existing state machine with additive `objective` variant on WizardCommitState_v0.variant Literal · sibling machine explicitly rejected per §1.2.'
- §16.2 baseline-tier contents PENDING-OWNER-CONFIRMATION per owner working default 2026-02-23T04:15Z.
- §1.2 modality extension · §1.5 unrepresentable-not-policed.

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO + Cadence GO (2026-02-23 post-INTERIM REPORT): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/contracts/wizard_commit_state.py` (M11 wizard v0 · sealed · NOT edited · sibling contract lands objective variant).
- `backend/services/wizard/operator_state_machine.py` (sealed).
- `backend/services/wizard/turn_ledger.py` (sealed).
- `backend/services/wizard/session_persistence.py` (sealed).
- `backend/services/wizard/admission_handoff.py` (sealed).
- `backend/services/wizard/agent_interface.py` (sealed).
- All CP-AIP-1..5 modules — untouched this seal.

**New additive modules landed by this seal (5 files):**
- `backend/contracts/target_outcome_v0.py` (~85 lines · `TargetOutcome_v0` frozen dataclass seven-field schema + `StratumAcceptance_v0` two-dimensional + closed-set `GATE_POLICIES` constant).
- `backend/contracts/collection_schema_v0.py` (~65 lines · `CollectionSchema_v0` frozen two-tier + `BASELINE_TIER_V1_0_CONTENTS` Final 5-tuple + `CUSTODY_VIOLATING_TOKENS` 8-tuple).
- `backend/contracts/wizard_objective_commit_state_v0.py` (~80 lines · `ObjectiveSession_v0` frozen 6-carrier + `OBJECTIVE_VARIANT_NAME` Final constant · sibling contract not sealed carrier edit).
- `backend/services/wizard/objective_compile.py` (~135 lines · `compile_target_outcome` + `compile_collection_schema` compile-time gates + 3 refusal classes `TestSetRefMissing` + `AcceptanceBarNotStratified` + `CustodyViolation` all subclassing `ObjectiveCompileError`).
- `backend/services/registry/audio_modality_namespace.py` (~120 lines · `AudioModalityNamespace_v0` frozen dataclass with `open()` / `close()` / `write_data_point()` / `list_scoped_writes()` methods · `ScopedWrite_v0` frozen carrier · `NamespaceState = Literal['open', 'sealed']` closed-set · NO `delete` method structurally).

**Test file:**
- `backend/tests/invariants/test_cp_aip_6_objective_wizard_aip_v1_0_section_8_9_12.py` (~330 lines · 10 pins).

**Frozen-contract parity fold-in:**
- `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` — 3 new entries added to `NON_CONTRACT_UTILITY_MODULES` (append-only per FL-P4-W6-08 pattern).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.
