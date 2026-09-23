---
card_id: CP_AIP_8_SAMPLING_REFLECTION
title: AIP v1.0 §11.2 sampling-reflection-calibration-boundary + §11.3 milestone-list-authoring + §16.2 codec-choice-measurement · Item 5.8 CP-AIP-8
ratified_at_utc: 2026-02-23T08:06:00Z
ratified_by: Owner cadence directive verbatim (2026-02-23 CP-AIP-4 GO) 'run CP-AIP-5 → CP-AIP-10 sequentially · brief report-and-continue after CP-AIP-6 seals · HALT after CP-AIP-10 for full plane completion report · immediate HALT on any SPEC-CONFLICT-<n>' + Item-4 checkpoint GO 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
card_sha256: d65ca42ea6cf188fcd59c2ea5dd566f02a09f6633c02e01212cbd50492224833
milestone_status: OPEN (Item 5.8 CP-AIP-8 · in-flight for this seal · continues sequential cadence · continues to CP-AIP-9 post-seal)
---

# CP-AIP-8-SAMPLING-REFLECTION · AIP v1.0 §11.2 + §11.3 + §16.2

## OBJECTIVE

Land the additive Sampling-and-Reflection compose-boundary as pure §1.2 modality-extension of sealed CP-M6-8-1 calibration primitives (`CalibrationOutput` · `CalibrationVolume` · `PerStratumTestSetEval` · `ScalingCurveFit` · `assert_full_run_quote_has_ci` · `assert_plan_has_calibration_stage` · `PlanWithoutCalibrationStageRefused` · `PointEstimateOnlyQuoteRefused` · `CalibrationVolumeCountError`) + sealed §11.3 milestone primitives (`Milestone` · `MilestoneList` · `construct_milestone_list` · `agree_milestone_list` · `assert_commission_open_only_after_agreement` · `MilestoneMissingDoneConditionError` · `MilestoneMissingOwnerError` · `MilestoneListEmptyError` · `MilestoneListAlreadyAgreedError` · `CommissionOpenBeforeAgreementError`) + sealed CP-AIP-7 `PlannerBoundaryResult_v1` + CP-M6-7-3 `CostQuoteWithCI`. Zero sealed-carrier edit per SO §3.8.

The compose-boundary binds: (i) plan-without-calibration-stage refused at S&R entry (§11.2 verbatim 'A plan without a calibration stage is rejected · The first job prices the real job'); (ii) full-run quote refused as point-estimate at S&R output (§11.2 verbatim 'never a point estimate'); (iii) S&R output refused if it lacks a non-empty proposed milestone list (§11.3 V114a verbatim 'a proposed milestone list - the checklist of what must be done'); (iv) commission-open refused if S&R output has not been agreed by the objective owner (§11.3 V114c/V114d verbatim 'from that point, all reporting is against it'); (v) sealed §11.3 milestone construction refusals bubble up unchanged (each milestone MUST carry done_condition + owner).

`canon_ref: AIP v1.0 §11.2 verbatim + §11.3 V114a..V114d verbatim + §16.2 codec-choice-measurement (deferred to this seal per owner working default) + §1.2 modality-extension + §1.5 unrepresentable-not-policed.`

Owner content anchor (§11.2 P179 verbatim): 'The first job prices the real job.' The S&R compose-boundary refuses to price a real job without a preceding calibration stage output.

## MUST DO

1. **§11.2 verbatim · plan-without-calibration-stage refused at S&R boundary** — `enter_sr_with_planner_result(planner_result, plan_has_calibration_output, ...)` invokes sealed `assert_plan_has_calibration_stage(plan_has_calibration_output=False)` which raises sealed `PlanWithoutCalibrationStageRefused`; the boundary surfaces this refusal via `PlanWithoutCalibrationAtSRBoundary`. Enforced by `test_sr_boundary_refuses_plan_without_calibration_stage`. `canon_ref: AIP §11.2 verbatim V113f + §11.2 P179.`

2. **§11.2 verbatim · cost-quote-never-point-estimate at S&R output** — the S&R boundary invokes sealed `assert_full_run_quote_has_ci(quote=<bare-float>)` which raises sealed `PointEstimateOnlyQuoteRefused`; the boundary surfaces this refusal via `PointEstimateAtSRBoundary`. Enforced by `test_sr_boundary_refuses_cost_quote_as_point_estimate`. `canon_ref: AIP §11.2 V113e verbatim + §11.2 P179.`

3. **§11.3 V114a verbatim · proposed-milestone-list-required at S&R output** — S&R boundary invokes sealed `construct_milestone_list(milestones=(), commission_id=...)` on empty milestones which raises sealed `MilestoneListEmptyError`; the boundary surfaces this refusal via `MilestoneListMissingAtSRBoundary`. Enforced by `test_sr_boundary_refuses_missing_milestone_list`. `canon_ref: AIP §11.3 V114a verbatim + §11.3 P181.`

4. **§11.3 V114b verbatim · each-milestone-carries-done-condition-and-owner** — sealed `Milestone.__post_init__` refuses empty done_condition (via sealed `MilestoneMissingDoneConditionError`); the S&R boundary composes milestones through the sealed factory so this refusal surfaces unchanged. Enforced by `test_sr_boundary_composes_sealed_milestone_done_condition_refusal`. `canon_ref: AIP §11.3 V114b verbatim + §11.3 P182.`

5. **§11.3 V114c/V114d verbatim · commission-open-only-after-agreement** — sealed `assert_commission_open_only_after_agreement(milestone_list=<unagreed>)` raises sealed `CommissionOpenBeforeAgreementError`; the S&R boundary invokes this gate before allowing commission-open. Enforced by `test_sr_boundary_refuses_commission_open_before_agreement`. `canon_ref: AIP §11.3 V114c + V114d verbatim + §11.3 P182..P184.`

6. **§1.2 no-redeclaration scan · sealed calibration + milestone + planner carriers** — the NEW module does NOT redeclare `CalibrationOutput` / `CalibrationVolume` / `PerStratumTestSetEval` / `ScalingCurveFit` / `CostQuoteWithCI` / `Milestone` / `MilestoneList` / `PlannerBoundaryResult_v1` / `assert_plan_has_calibration_stage` / `assert_full_run_quote_has_ci` / `construct_milestone_list` / `agree_milestone_list` / `assert_commission_open_only_after_agreement`. Structural class-declaration + def scan. Enforced by `test_new_module_does_not_redeclare_sealed_carriers`. `canon_ref: AIP §1.2 verbatim + BL #4.`

7. **Anti-drift §3 + §5 anchor scan · §11.2 + §11.3 citations + ledger-check** — the NEW module cites its exact AIP section anchors + carries the ledger-check anchor. Enforced by `test_new_module_cites_section_anchors_and_ledger_check`. `canon_ref: Anti-drift standing guard §3 + §5.`

8. **7 RED-first pytest invariants** — RED_pre 7/7 failed → GREEN_post 7/7 passed. `canon_ref: SO §3 RED-first.`

9. **Ratchet floor 6310 → 6317** — +7 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

10. **5-commit seal on dual branches + /app companion** — Terminal `pytest` only · BASELINE_GUARD double-green. `canon_ref: SO §3.3 5-Commit-Seal.`

## MUST NOT

- Edit any sealed §11.2 / §11.3 carrier (`audio_plane_v1/calibration.py` CP-M6-8-1 · `audio_plane_v1/milestones.py` sealed · `audio_plane_v1/training_planner.py` CP-M6-7-2/3 · CP-AIP-7 `audio_plane_v1/target_outcome_planner_boundary_v1.py` + `register_stratum_resolver_v1.py`), or any prior CP-AIP-1..7 or CP-CENSUS carrier. `canon_ref: SO §3.8 additive-only.`

- Redeclare any sealed calibration / milestone / planner carrier. `canon_ref: AIP §1.2 verbatim + BL #4.`

- Price a real job without a preceding calibration stage output. §11.2 verbatim. `canon_ref: AIP §11.2 P179.`

- Emit a full-run cost quote as a point estimate. §11.2 verbatim. `canon_ref: AIP §11.2 V113e.`

- Emit S&R output without a proposed milestone list. §11.3 V114a verbatim. `canon_ref: AIP §11.3 V114a.`

- Open a commission before the objective owner has agreed the milestone list. §11.3 V114c/V114d verbatim. `canon_ref: AIP §11.3 V114c + V114d.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-8-SAMPLING-REFLECTION and nothing else. Full calibration training pipeline / real scaling curve fitting / cost model deferred to CP-AIP-10 downstream. `canon_ref: SO §7 guard 5.`

## EXIT

**7 RED-first invariants (RED_pre 7/7 failed · GREEN_post 7/7 passed):**

- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_sr_boundary_refuses_plan_without_calibration_stage
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_sr_boundary_refuses_cost_quote_as_point_estimate
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_sr_boundary_refuses_missing_milestone_list
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_sr_boundary_composes_sealed_milestone_done_condition_refusal
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_sr_boundary_refuses_commission_open_before_agreement
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_new_module_does_not_redeclare_sealed_carriers
- tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py::test_new_module_cites_section_anchors_and_ledger_check

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6310 → 6317 (+7 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical `stripped_sha256` (banked in receipt post-seal)

## STOP

Stop at 5-commit seal landing. Continue immediately to CP-AIP-9-COMMISSION-VIEW.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §11.2 / §11.3 / sealed CP-M6-8-1 primitives / sealed §11.3 milestone primitives / sealed CP-AIP-7 planner-boundary, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report immediately.

## ANCHORS

**Spec anchors (AIP v1.0):**
- §11.2 V113 verbatim (LOAD-BEARING): 'The first job prices the real job.'
- §11.2 V113e verbatim: 'stated confidence interval — never a point estimate.'
- §11.2 V113f verbatim: 'A plan without a calibration stage is rejected.'
- §11.3 V114a verbatim: 'a proposed milestone list — the checklist of what must be done, in what order, for the commission to succeed.'
- §11.3 V114b verbatim: 'Each milestone carries a done-condition and an owner.'
- §11.3 V114c verbatim: 'Objective owner reviews and agrees the list at commission.'
- §11.3 V114d verbatim: 'from that point, all reporting is against it.'
- §16.2 codec-choice-measurement (deferred to this seal per owner working default 2026-02-23T04:15Z).

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- CP-AIP-4 GO + Cadence GO (2026-02-23 post-INTERIM REPORT): 'run CP-AIP-5 → CP-AIP-10 sequentially; brief report-and-continue after CP-AIP-6 seals; HALT after CP-AIP-10 for full plane completion report; immediate HALT on any SPEC-CONFLICT-<n>.'

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/calibration.py` (CP-M6-8-1 · §11.2 · sealed · NOT edited).
- `backend/services/audio_plane_v1/milestones.py` (sealed §11.3 · NOT edited).
- `backend/services/audio_plane_v1/training_planner.py` (CP-M6-7-2/3 · sealed · NOT edited).
- `backend/services/audio_plane_v1/target_outcome_planner_boundary_v1.py` (CP-AIP-7 · sealed · NOT edited).
- `backend/services/audio_plane_v1/register_stratum_resolver_v1.py` (CP-AIP-7 · sealed · NOT edited).
- All CP-AIP-1..7 modules — untouched this seal.

**New additive module landed by this seal (1 file):**
- `backend/services/audio_plane_v1/sampling_reflection_boundary_v1.py` (~180 lines · `SamplingReflectionBoundaryResult_v1` frozen 3-carrier + 3 refusal classes all subclassing `SamplingReflectionBoundaryRefused` (`PlanWithoutCalibrationAtSRBoundary` · `PointEstimateAtSRBoundary` · `MilestoneListMissingAtSRBoundary`) + 4 boundary callables `enter_sr_with_planner_result` + `assert_full_run_quote_at_boundary` + `build_milestone_list_at_boundary` + `assert_commission_open_at_boundary` · composes sealed CP-M6-8-1 calibration + sealed §11.3 milestone + sealed CP-AIP-7 `PlannerBoundaryResult_v1` + sealed CP-M6-7-3 `CostQuoteWithCI` · `HONEST_GAP_V1_POSTURE` Final marker citing §11.2 P179 verbatim).

**Test file:**
- `backend/tests/invariants/test_cp_aip_8_sampling_reflection_aip_v1_0_section_11_2_11_3.py` (~280 lines · 7 pins).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §6.2 objective-card + hash-pin · SO §7 17-guard consolidated set · Six Standing Bans.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-8-SAMPLING-REFLECTION and nothing else.
