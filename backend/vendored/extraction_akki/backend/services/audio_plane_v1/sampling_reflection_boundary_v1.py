"""CP-AIP-8-SAMPLING-REFLECTION · sampling_reflection_boundary_v1 · additive §1.2.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-8-SAMPLING-REFLECTION and nothing else.

Spec anchors:
- AIP v1.0 §11.2 V113 verbatim (LOAD-BEARING): 'The first job prices
  the real job.'
- §11.2 V113e verbatim: 'stated confidence interval - never a point
  estimate.'
- §11.2 V113f verbatim: 'A plan without a calibration stage is rejected.'
- §11.3 V114a verbatim: 'a proposed milestone list - the checklist of
  what must be done, in what order, for the commission to succeed.'
- §11.3 V114b verbatim: 'Each milestone carries a done-condition and
  an owner.'
- §11.3 V114c verbatim: 'Objective owner reviews and agrees the list
  at commission.'
- §11.3 V114d verbatim: 'from that point, all reporting is against it.'
- §16.2 codec-choice-measurement deferred to this seal per owner
  working default 2026-02-23T04:15Z.

The compose-boundary binds sealed CP-M6-8-1 `CalibrationOutput` +
`assert_plan_has_calibration_stage` + `assert_full_run_quote_has_ci` +
`PlanWithoutCalibrationStageRefused` + `PointEstimateOnlyQuoteRefused`
+ sealed §11.3 `Milestone` + `MilestoneList` + `construct_milestone_list`
+ `agree_milestone_list` + `assert_commission_open_only_after_agreement`
+ `MilestoneListEmptyError` + `CommissionOpenBeforeAgreementError` +
sealed CP-AIP-7 `PlannerBoundaryResult_v1` + sealed CP-M6-7-3
`CostQuoteWithCI`. Three typed refusals surface the shape violations
at boundary:
  1. `PlanWithoutCalibrationAtSRBoundary` (§11.2 V113f)
  2. `PointEstimateAtSRBoundary` (§11.2 V113e)
  3. `MilestoneListMissingAtSRBoundary` (§11.3 V114a)

Sealed carriers composed (UNCHANGED per SO §3.8):
- backend/services/audio_plane_v1/calibration.py (CP-M6-8-1).
- backend/services/audio_plane_v1/milestones.py (sealed §11.3).
- backend/services/audio_plane_v1/training_planner.py (CP-M6-7-2/3).
- backend/services/audio_plane_v1/target_outcome_planner_boundary_v1.py
  (CP-AIP-7).

Additive-only per SO §3.8 · no edit to sealed carriers · §1.2
no-redeclaration.
"""
from __future__ import annotations

from typing import Final, Tuple

from backend.services.audio_plane_v1.calibration import (
    PlanWithoutCalibrationStageRefused,
    PointEstimateOnlyQuoteRefused,
    assert_full_run_quote_has_ci,
    assert_plan_has_calibration_stage,
)
from backend.services.audio_plane_v1.milestones import (
    Milestone,
    MilestoneList,
    MilestoneListEmptyError,
    construct_milestone_list,
)


HONEST_GAP_V1_POSTURE: Final[str] = (
    "CP-AIP-8-SAMPLING-REFLECTION · §11.2 V113 verbatim: 'The first "
    "job prices the real job.' This compose-boundary refuses to price "
    "a real job without a preceding calibration stage output + refuses "
    "point-estimate quotes + refuses missing milestone lists. It does "
    "NOT itself perform calibration training or scaling-curve fitting "
    "- those are the sealed CP-M6-8-1 primitives, invoked unchanged."
)


# ---------------------------------------------------------------------------
# Refusal hierarchy · all subclass SamplingReflectionBoundaryRefused
# ---------------------------------------------------------------------------


class SamplingReflectionBoundaryRefused(Exception):
    """Base class for every CP-AIP-8 S&R compose-boundary refusal.

    Ledger check - CP-AIP-8-SAMPLING-REFLECTION refusal boundary.
    """


class PlanWithoutCalibrationAtSRBoundary(SamplingReflectionBoundaryRefused):
    """§11.2 V113f verbatim: 'A plan without a calibration stage is
    rejected.' Surfaces sealed `PlanWithoutCalibrationStageRefused`.
    """


class PointEstimateAtSRBoundary(SamplingReflectionBoundaryRefused):
    """§11.2 V113e verbatim: 'stated confidence interval - never a
    point estimate.' Surfaces sealed `PointEstimateOnlyQuoteRefused`.
    """


class MilestoneListMissingAtSRBoundary(SamplingReflectionBoundaryRefused):
    """§11.3 V114a verbatim: 'a proposed milestone list - the checklist
    of what must be done.' Surfaces sealed `MilestoneListEmptyError`.
    """


# ---------------------------------------------------------------------------
# §11.2 compose-boundary · plan-has-calibration gate
# ---------------------------------------------------------------------------


def enter_sr_with_planner_result(
    *,
    plan_has_calibration_output: bool,
) -> None:
    """§11.2 V113f verbatim compose-boundary entry.

    Refuses `PlanWithoutCalibrationAtSRBoundary` when
    `plan_has_calibration_output is False` via sealed
    `assert_plan_has_calibration_stage`. §11.2 P179 verbatim: 'The
    first job prices the real job.'
    """
    try:
        assert_plan_has_calibration_stage(
            plan_has_calibration_output=plan_has_calibration_output,
        )
    except PlanWithoutCalibrationStageRefused as exc:
        raise PlanWithoutCalibrationAtSRBoundary(
            f"CP-AIP-8 · §11.2 V113f verbatim: 'A plan without a "
            f"calibration stage is rejected.' Sealed refusal surfaced "
            f"at S&R compose boundary: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# §11.2 compose-boundary · full-run-quote-has-CI gate
# ---------------------------------------------------------------------------


def assert_full_run_quote_at_boundary(*, quote) -> None:
    """§11.2 V113e verbatim compose-boundary output gate.

    Refuses `PointEstimateAtSRBoundary` when `quote` is not an actual
    sealed `CostQuoteWithCI` instance via sealed
    `assert_full_run_quote_has_ci`. §11.2 P179 verbatim: 'stated
    confidence interval - never a point estimate'.
    """
    try:
        assert_full_run_quote_has_ci(quote=quote)
    except PointEstimateOnlyQuoteRefused as exc:
        raise PointEstimateAtSRBoundary(
            f"CP-AIP-8 · §11.2 V113e verbatim: 'stated confidence "
            f"interval - never a point estimate.' Sealed refusal "
            f"surfaced at S&R compose boundary: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# §11.3 compose-boundary · milestone-list construction
# ---------------------------------------------------------------------------


def build_milestone_at_boundary(
    *,
    milestone_id: str,
    done_condition: str,
    owner: str,
) -> Milestone:
    """§11.3 V114b verbatim milestone construction seam.

    Composes sealed `Milestone` construction. Sealed refusals bubble
    up unchanged (`MilestoneMissingDoneConditionError` on empty
    done_condition · `MilestoneMissingOwnerError` on empty owner).
    """
    return Milestone(
        milestone_id=milestone_id,
        done_condition=done_condition,
        owner=owner,
    )


def build_milestone_list_at_boundary(
    *,
    milestones: Tuple[Milestone, ...],
    commission_id: str,
) -> MilestoneList:
    """§11.3 V114a verbatim milestone-list construction seam.

    Composes sealed `construct_milestone_list`. Surfaces sealed
    `MilestoneListEmptyError` as `MilestoneListMissingAtSRBoundary`.
    """
    try:
        return construct_milestone_list(
            milestones=milestones,
            commission_id=commission_id,
        )
    except MilestoneListEmptyError as exc:
        raise MilestoneListMissingAtSRBoundary(
            f"CP-AIP-8 · §11.3 V114a verbatim: 'a proposed milestone "
            f"list - the checklist of what must be done.' Sealed "
            f"refusal surfaced at S&R compose boundary: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# §11.3 compose-boundary · commission-open-only-after-agreement gate
# ---------------------------------------------------------------------------


def assert_commission_open_at_boundary(*, milestone_list: MilestoneList) -> None:
    """§11.3 V114c + V114d verbatim commission-open gate.

    Invokes sealed `assert_commission_open_only_after_agreement`
    which raises sealed `CommissionOpenBeforeAgreementError` when
    `milestone_list.commission_agreement_ref is None`. That refusal
    bubbles up unchanged from the sealed gate.
    """
    from backend.services.audio_plane_v1.milestones import (
        assert_commission_open_only_after_agreement,
    )

    # Sealed refusal bubbles up unchanged - CP-AIP-8 boundary is a
    # composition seam per §1.2 not a re-implementation.
    assert_commission_open_only_after_agreement(milestone_list=milestone_list)


__all__ = (
    "HONEST_GAP_V1_POSTURE",
    "SamplingReflectionBoundaryRefused",
    "PlanWithoutCalibrationAtSRBoundary",
    "PointEstimateAtSRBoundary",
    "MilestoneListMissingAtSRBoundary",
    "enter_sr_with_planner_result",
    "assert_full_run_quote_at_boundary",
    "build_milestone_at_boundary",
    "build_milestone_list_at_boundary",
    "assert_commission_open_at_boundary",
)
