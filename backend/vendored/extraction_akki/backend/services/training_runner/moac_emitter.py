"""MOAC emitter · Doc 17 line 90 · six-check card production.

Doc 17 line 90 verbatim (grounding brief line 61):
    'The surface displays "four of six checks passed" with all six
     criteria named and rejected models kept on record - real UI,
     real registry schema. But MOAC has a contract and no emitter:
     nothing in the current build actually runs a candidate through
     the six checks and writes the result. The surface is currently
     a faithful rendering of a process that has not yet executed.'

CP8 lands the emitter shell. The six checks (Canon 4 §26 · Doc 17
briefing) are:
  M-a  target-stratum improvement (>= baseline on target stratum)
  M-b  non-target regression       (<= baseline on non-target stratum)
  M-c  robustness                  (adversarial + noisy holdout)
  M-d  lineage                     (recipe_version + base_model + rights)
  M-e  calibration                 (measured against uncurated set)
  M-f  refusal-honesty             (refusal grammar under stress)

At CP8 landing (mock SSH seam), the emitter reports mocked=True on
every criterion output. Real values arrive when the SSH real path
lights up.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from services.training_runner.ssh_seam import SeamResult


CRITERION_NAMES: tuple = ("M-a", "M-b", "M-c", "M-d", "M-e", "M-f")


@dataclass(frozen=True)
class CriterionResult:
    name: str
    passed: bool
    measured_value: float
    threshold_note: str
    uncurated_flag: bool = True   # D-7 doctrine - MUST be True to accept.
    mocked: bool = True


def emit_six_check_card(
    run_id: str,
    seam_result: SeamResult,
    lineage_recipe_version: str,
    lineage_base_model_id: str,
) -> Dict[str, Any]:
    """Produce a six-check MOAC card from a seam_result + lineage.

    In mock mode: passes M-a, M-b (with parity), M-d (lineage cited),
    M-e (calibration input present) unconditionally; M-c and M-f are
    deferred as 'not yet measurable in mock' - card status accordingly
    reports 'four of six checks passed', matching Doc 17 line 90
    verbatim wording.
    """
    criteria: List[CriterionResult] = [
        CriterionResult(
            name="M-a",
            passed=seam_result.m_a_input >= 0.05,
            measured_value=seam_result.m_a_input,
            threshold_note="target-stratum improvement >= 0.05 (mock)",
            mocked=seam_result.mocked,
        ),
        CriterionResult(
            name="M-b",
            passed=seam_result.m_b_input <= 0.10,
            measured_value=seam_result.m_b_input,
            threshold_note="non-target regression <= 0.10 (mock)",
            mocked=seam_result.mocked,
        ),
        CriterionResult(
            name="M-c",
            passed=False,
            measured_value=0.0,
            threshold_note="robustness - not measurable in mock; awaits real "
                           "adversarial + noisy holdout probe (CP8 real flip)",
            mocked=seam_result.mocked,
        ),
        CriterionResult(
            name="M-d",
            passed=bool(lineage_recipe_version) and bool(lineage_base_model_id),
            measured_value=1.0 if (lineage_recipe_version and lineage_base_model_id) else 0.0,
            threshold_note=(
                "lineage cites recipe_version + base_model_id (A17.3 M-d "
                "extension). Rights lineage extends Doc14-016."
            ),
            mocked=seam_result.mocked,
        ),
        CriterionResult(
            name="M-e",
            passed=seam_result.m_e_input >= 0.70,
            measured_value=seam_result.m_e_input,
            threshold_note="calibration quality >= 0.70 on uncurated set (mock)",
            mocked=seam_result.mocked,
        ),
        CriterionResult(
            name="M-f",
            passed=False,
            measured_value=0.0,
            threshold_note="refusal-honesty - not measurable in mock; awaits "
                           "governed refusal-under-stress probe (CP8 real flip)",
            mocked=seam_result.mocked,
        ),
    ]
    passed_count = sum(1 for c in criteria if c.passed)
    return {
        "moac_card_id": f"moac/{run_id}",
        "run_id": run_id,
        "criteria": [asdict(c) for c in criteria],
        "passed_count": passed_count,
        "total_criteria": len(criteria),
        "verdict_summary": (
            f"{passed_count} of {len(criteria)} checks passed "
            f"({'mocked' if seam_result.mocked else 'live'})"
        ),
        "accept_for_service": (
            # Doc 17 line 101 verbatim: 'No model enters service without
            # clearing all six MOAC criteria on uncurated held-out material,
            # with no human in the acceptance path.'
            passed_count == len(criteria)
            and all(c.uncurated_flag for c in criteria)
            and all(not c.mocked for c in criteria)
        ),
        "reference_verbatim": (
            "Doc 17 line 101: 'No model enters service without clearing "
            "all six MOAC criteria on uncurated held-out material, with no "
            "human in the acceptance path.'"
        ),
    }
