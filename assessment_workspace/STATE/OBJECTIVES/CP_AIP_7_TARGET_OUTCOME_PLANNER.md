---
card_id: CP_AIP_7_TARGET_OUTCOME_PLANNER
title: AIP v1.0 §10 TargetOutcome-planner-boundary + §11.1 population-resolved-against-register + §11.4 additive-only-stratum-set + §16.2 gate_policy-platform-default · Item 5.7 CP-AIP-7
ratified_at_utc: 2026-02-23T07:56:00Z
ratified_by: Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO) 'run CP-AIP-5 → CP-AIP-10 sequentially · brief report-and-continue after CP-AIP-6 seals · HALT after CP-AIP-10 for full plane completion report · immediate HALT on any SPEC-CONFLICT-<n>' + Item-4 checkpoint GO 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals' + §16.2 owner working default 2026-02-23T04:15Z 'platform default for gate_policy where Outcome does not set it is missed-stratum-gates-release (fail-closed per §1.5 doctrine)' + owner content anchor CP-AIP-6 brief 2026-02-23T07:55Z 'confirm §8.4 compile-time rejections landed + confirm wizard mechanical guards prove against stub agent before any LLM per §8.3'.
card_sha256: 80f9757cd6fb7957e450e4cbdd16eadb9490d9d45c75dca679807c4c3cec32bd
milestone_status: OPEN (Item 5.7 CP-AIP-7 · in-flight for this seal · continues sequential cadence · brief report-and-continue NOT DUE at this seal · continues to CP-AIP-8 post-seal)
---

# CP-AIP-7-TARGET-OUTCOME-PLANNER · AIP v1.0 §10 + §11.1 + §11.4 + §16.2

## OBJECTIVE

Land the additive TargetOutcome-planner-compose-boundary as pure §1.2 modality-extension of sealed CP-AIP-6 `TargetOutcome_v0` (contracts/target_outcome_v0.py) + sealed CP-M6-7-2 planner architecture (`PlannerCore` Protocol · `LearnedReorderLayer` Protocol · `strip_eligibility_decision` · `run_eligibility_gate` · `PlanInputs` · `EligibilityDecision` · `EligibleStripped` · `PlanReproducibilityWitness`) + sealed CP-M6-7-3 planner outputs (`CoverageReport` · `PerStratumCoverageEntry` · `CurriculumOrdering` · `CostQuoteWithCI` · `MilestoneListRef` · `PlannerOutputs`) + sealed CP-M6-3 `CharacterRegister`/`CharacterEntry`.layer. Zero sealed-carrier edit per SO §3.8.

The compose-boundary binds: (i) `TargetOutcome_v0.test_set_ref` at planner entry — refused via `TestSetUnresolvedAtPlannerEntry` when the ref cannot be resolved against a `TestSetIndex_v1` Protocol (§10.2 verbatim 'The test set precedes the training'); (ii) `TargetOutcome_v0.population` refused via `PopulationNotResolvableAgainstRegister` when the population string does not correspond to a `CharacterRegister.entries[].layer` value (§11.1 verbatim 'population is register-defined'); (iii) coverage report refused via `StratumSetSubtractedFromRegisterError` when the coverage-report stratum-set is a proper subset of the current register's stratum-set (§11.4 additive-only stratum-set · register never subtracts); (iv) planner boundary output refused via `CostQuoteMissingCIAtBoundary` when the sealed `CostQuoteWithCI` construction has raised `CostQuoteMissingCIError` upstream — surfaces the sealed refusal at boundary shape verbatim (§11.4 P188 · V118); (v) planner-boundary output refused via `MissedStratumReleaseAtBoundary` when `TargetOutcome_v0.gate_policy == 'missed stratum gates release'` (owner working default) AND coverage report has a stratum whose acceptance is unmet (§16.2 fail-closed per §1.5 doctrine).

`canon_ref: AIP v1.0 §10.1..§10.2 verbatim + §11.1 verbatim planner architecture + §11.4 P185..P188 (V115..V118) verbatim planner outputs + §16.2 gate_policy platform default per owner working default 2026-02-23T04:15Z + §1.2 modality-extension + §1.5 unrepresentable-not-policed.`

Owner content anchor (§15 P234 verbatim · already observed at CP-AIP-6 seal): 'The planner must never accept a hand-authored Outcome once the wizard exists' — CP-AIP-6 has now landed the wizard compile boundary; CP-AIP-7 now lands the planner compose boundary that consumes the wizard's compiled `TargetOutcome_v0`.

## MUST DO

1. **§10.2 verbatim · test-set-precedes-training at planner entry** — `enter_planner_with_target_outcome(target_outcome, ...)` refuses with `TestSetUnresolvedAtPlannerEntry` when `TestSetIndex_v1.resolve(target_outcome.test_set_ref)` returns None. §10.2 verbatim 'The test set precedes the training'. Enforced by `test_planner_boundary_refuses_unresolvable_test_set_ref`. `canon_ref: AIP §10.2 verbatim + §10.1 P161 verbatim (test_set_ref must exist).`

2. **§11.1 verbatim · population-resolved-against-register** — `resolve_population_against_register(target_outcome.population, character_register)` refuses with `PopulationNotResolvableAgainstRegister` when the population string is not a `CharacterEntry.layer` value present in `character_register.entries`. §11.1 verbatim 'population is register-defined, not label-defined'. Enforced by `test_planner_boundary_refuses_population_not_in_register`. `canon_ref: AIP §11.1 verbatim + §10.2 verbatim (population is register-defined).`

3. **§11.4 verbatim · additive-only-stratum-set (register never subtracts)** — the compose boundary refuses with `StratumSetSubtractedFromRegisterError` when the emitted `CoverageReport.entries[].stratum_ref` set is a proper subset of the current register's stratum-set (union of `CharacterEntry.layer` across register entries). §11.4 P185 verbatim 'per target stratum' anchored + §11.1 verbatim 'population is register-defined' contract: register defines the stratum-set; planner may add strata not subtract. Enforced by `test_planner_boundary_refuses_register_subtracts_stratum`. `canon_ref: AIP §11.4 P185 verbatim + §11.1 verbatim.`

4. **§11.4 P188 (V118) verbatim · cost-quote-with-CI at boundary** — the compose boundary refuses with `CostQuoteMissingCIAtBoundary` when the emitted `PlannerOutputs.cost_quote` construction has raised the sealed `CostQuoteMissingCIError` (i.e. `ci_low is None` or `ci_high is None`). Sealed refusal surfaced at boundary verbatim; no new logic. Enforced by `test_planner_boundary_refuses_missing_confidence_interval`. `canon_ref: AIP §11.4 P188 verbatim + V118 verbatim.`

5. **§16.2 owner working default · missed-stratum-gates-release fail-closed** — when `TargetOutcome_v0.gate_policy == 'missed stratum gates release'` (platform default per owner working default 2026-02-23T04:15Z), the compose boundary refuses with `MissedStratumReleaseAtBoundary` if the emitted `CoverageReport` has any stratum whose `gap_hours_h > 0.0` (fail-closed per §1.5 doctrine). Enforced by `test_planner_boundary_enforces_missed_stratum_gates_release_default`. `canon_ref: AIP §16.2 owner working default 2026-02-23T04:15Z + §1.5 unrepresentable-not-policed.`

6. **§11.1 verbatim · sealed run_eligibility_gate composition** — the compose boundary invokes sealed CP-M6-7-2 `run_eligibility_gate(plan_inputs=..., planner_core=..., learned_reorder_layer=...)` unchanged; new wrapper module MUST NOT re-declare `PlannerCore` / `LearnedReorderLayer` / `strip_eligibility_decision` / `run_eligibility_gate` / `PlanInputs` / `EligibilityDecision` / `EligibleStripped` / `PlanReproducibilityWitness`. Enforced by `test_planner_boundary_composes_sealed_run_eligibility_gate`. `canon_ref: AIP §1.2 + §11.1 verbatim.`

7. **§1.2 no-redeclaration scan · sealed planner + register carriers** — the two NEW modules do NOT redeclare `PlannerCore` / `LearnedReorderLayer` / `PlanInputs` / `EligibilityDecision` / `EligibleStripped` / `PlanReproducibilityWitness` / `CoverageReport` / `PerStratumCoverageEntry` / `CurriculumOrdering` / `CostQuoteWithCI` / `MilestoneListRef` / `PlannerOutputs` / `CharacterRegister` / `CharacterEntry`. Structural class-declaration scan on both NEW modules. Enforced by `test_new_modules_do_not_redeclare_sealed_planner_carriers`. `canon_ref: AIP §1.2 verbatim + BL #4.`

8. **Anti-drift §3 + §5 anchor scan · §10 + §11.1 + §11.4 + §16.2 citations + ledger-check** — both NEW modules cite the exact AIP section anchor they enforce and carry the ledger-check anchor. Enforced by `test_new_modules_cite_section_anchors_and_ledger_check`. `canon_ref: Anti-drift standing guard §3 + §5.`

9. **8 RED-first pytest invariants** — RED_pre 8/8 failed → GREEN_post 8/8 passed. Each pin cites the exact §10 / §11 / §16 / §1 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

10. **Ratchet floor 6302 → 6310** — +8 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · `ratchet_history` entry appended schema-complete (`passed=6310`). `invariants_enforced_when_baseline_guard_1.passed_floor` advanced in lock-step. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

11. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1..6 seals. Terminal `pytest` only. `testing_agent` BANNED. `BASELINE_GUARD=1 PYTHONHASHSEED=0` double-green byte-identical `stripped_sha256`. `canon_ref: SO §3.3 5-Commit-Seal + Six Standing Bans.`

## MUST NOT

- Edit any sealed §10 / §11.1 / §11.4 carrier (`audio_plane_v1/target_outcome.py` CP-M6-7-1 · `audio_plane_v1/training_planner.py` CP-M6-7-2/CP-M6-7-3 · `audio_plane_v1/calibration.py` CP-M6-8-1 · CP-AIP-6 sibling contracts `contracts/target_outcome_v0.py` · `contracts/collection_schema_v0.py` · `contracts/wizard_objective_commit_state_v0.py` · `services/wizard/objective_compile.py` · `services/registry/audio_modality_namespace.py`), or any prior CP-AIP-1..6 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only.`

- Redeclare any sealed planner or register carrier (§1.2 no-redeclaration). `canon_ref: AIP §1.2 verbatim + BL #4.`

- Emit a plan without resolving `TargetOutcome_v0.test_set_ref` first. §10.2 verbatim. `canon_ref: AIP §10.2 P162.`

- Emit a plan whose `TargetOutcome_v0.population` is not present in the current register's layer set. §11.1 verbatim. `canon_ref: AIP §11.1.`

- Emit a coverage report whose stratum-set is a proper subset of the current register's layer set. §11.4 additive-only + §11.1 register-defined. `canon_ref: AIP §11.4 + §11.1.`

- Emit a plan output without a stated confidence interval. §11.4 P188 verbatim. `canon_ref: AIP §11.4 P188.`

- Release when `TargetOutcome_v0.gate_policy == 'missed stratum gates release'` AND coverage report has a stratum whose acceptance is unmet. §16.2 owner working default. `canon_ref: AIP §16.2 + §1.5.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-7-TARGET-OUTCOME-PLANNER and nothing else. Full planner elicitation / calibration wiring / milestone-list expansion (§11.3) deferred to follow-on slices per scope-freeze SO §3.8. `canon_ref: SO §7 guard 5.`

## EXIT

**8 RED-first invariants (RED_pre 8/8 failed · GREEN_post 8/8 passed):**

- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_refuses_unresolvable_test_set_ref
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_refuses_population_not_in_register
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_refuses_register_subtracts_stratum
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_refuses_missing_confidence_interval
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_enforces_missed_stratum_gates_release_default
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_planner_boundary_composes_sealed_run_eligibility_gate
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_new_modules_do_not_redeclare_sealed_planner_carriers
- tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py::test_new_modules_cite_section_anchors_and_ledger_check

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6302 → 6310 (+8 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical `stripped_sha256` (banked in receipt post-seal)

## STOP

Stop at 5-commit seal landing. No cadence checkpoint at this seal (owner cadence directive verbatim: 'brief report-and-continue after CP-AIP-6 seals' — that's already dispatched at CP-AIP-6). Continue immediately to CP-AIP-8-SAMPLING-REFLECTION.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §10 / §11 / §16.2 / sealed CP-M6-7 primitives / sealed CP-AIP-6 contracts, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately. `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3 + owner cadence directive.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §10.1 P161 verbatim: 'test_set_ref must exist before the Outcome is accepted' (LOAD-BEARING).
- §10.2 P162 verbatim: 'The test set precedes the training.'
- §10.2 verbatim: 'Population is register-defined, not label-defined.'
- §11.1 verbatim: 'The existing planner pattern is reused unchanged: a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs.'
- §11.4 P185 (V115) verbatim: 'Coverage report — per target stratum: hours available, quality distribution, gaps, cost of closing each gap.'
- §11.4 P186 (V116) verbatim: 'Curriculum — ordering and weighting across strata derived from the register, not from the corpus natural distribution.'
- §11.4 P188 (V118) verbatim: 'Cost quote with a stated confidence interval.'
- §16.2 owner working default 2026-02-23T04:15Z: 'platform default for gate_policy where Outcome does not set it is missed-stratum-gates-release (fail-closed per §1.5 doctrine).'
- §1.2 modality extension · §1.5 unrepresentable-not-policed.

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO + Cadence GO (2026-02-23 post-INTERIM REPORT): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'
- CP-AIP-6 brief GO (2026-02-23T07:55Z): §8.4 (a)(b)(c) landed as pins confirmed · §8.3 stub-agent-before-LLM DEFERRED to follow-on additive seal per Absence-is-a-finding rule · continue into CP-AIP-7 without waiting for reply.

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/training_planner.py` (CP-M6-7-2 + CP-M6-7-3 · §11.1 + §11.4 · sealed · NOT edited).
- `backend/services/audio_plane_v1/target_outcome.py` (CP-M6-7-1 · §10 · sealed · NOT edited).
- `backend/services/audio_plane_v1/character_register.py` (CP-M6-3 · sealed · NOT edited).
- `backend/services/audio_plane_v1/calibration.py` (CP-M6-8-1 · §11.2 · sealed · NOT edited).
- `backend/contracts/target_outcome_v0.py` (CP-AIP-6 · §10.1 seven-field schema · sealed · NOT edited).
- All CP-AIP-1..6 modules — untouched this seal.

**New additive modules landed by this seal (2 files):**
- `backend/services/audio_plane_v1/register_stratum_resolver_v1.py` (~70 lines · `resolve_population_against_register` callable + `PopulationNotResolvableAgainstRegister` refusal · imports sealed `CharacterRegister`).
- `backend/services/audio_plane_v1/target_outcome_planner_boundary_v1.py` (~180 lines · `enter_planner_with_target_outcome` boundary + `PlannerBoundaryResult_v1` frozen carrier + 5 refusal classes `TestSetUnresolvedAtPlannerEntry` + `PopulationNotResolvableAgainstRegister` (re-raised) + `StratumSetSubtractedFromRegisterError` + `CostQuoteMissingCIAtBoundary` + `MissedStratumReleaseAtBoundary` all subclassing `PlannerBoundaryRefused` · composes sealed CP-AIP-6 `TargetOutcome_v0` + sealed CP-M6-7-2/3 `PlannerCore` + `run_eligibility_gate` + `CoverageReport` + `CostQuoteWithCI` + sealed CP-M6-3 `CharacterRegister` · `HONEST_GAP_V1_POSTURE` Final marker · `TestSetIndex_v1` Protocol seam).

**Test file:**
- `backend/tests/invariants/test_cp_aip_7_target_outcome_planner_aip_v1_0_section_10_11.py` (~340 lines · 8 pins).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-7-TARGET-OUTCOME-PLANNER and nothing else.
