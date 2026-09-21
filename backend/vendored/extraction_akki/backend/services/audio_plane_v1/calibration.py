"""M6 · Audio-Plane v1.0 · CP-M6-8-1 · §11.2 Calibration procedure.

Verbatim canon anchor (§11.2 P179..P180 · V113 · LOAD-BEARING · single-line for gating-test docstring parity):

  "Data requirements for low-resource fine-tuning are empirical; no analytical answer exists. The first commissioned stage is therefore a calibration: train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold. Only then is the full run quoted, with a stated confidence interval — never a point estimate. A plan without a calibration stage is rejected. The first job prices the real job."

This module lands calibration-procedure carriers + three refusals + two composition-checks.  V113a "three to four" is enforced as a shape rule on `CalibrationOutput.volumes` tuple length.  V113e CI-mandatory composes with CP-M6-7-3 `CostQuoteWithCI` via `assert_full_run_quote_has_ci`.  V113f existence gate refuses `PlanWithoutCalibrationStageRefused`.

Wave-honest limits (per M6 SW8 grounding brief §D):

- Carriers + refusals + composition-checks only; training not executed.
- No LLM / HTTP / filesystem / network.  Case-agnostic.
- §3.1 P038 tokens-not-waveforms preserved (opaque metadata only).
- Synthetic-fixtures-only in tests.
- Composes with CP-M6-7-3 `CostQuoteWithCI` via import; does NOT
  modify `training_planner.py`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple

from services.audio_plane_v1.training_planner import CostQuoteWithCI

__all__ = (
    "CALIBRATION_MIN_VOLUMES",
    "CALIBRATION_MAX_VOLUMES",
    "CalibrationVolume",
    "PerStratumTestSetEval",
    "ScalingCurveFit",
    "CalibrationOutput",
    "assert_full_run_quote_has_ci",
    "assert_plan_has_calibration_stage",
    "CalibrationVolumeCountError",
    "PointEstimateOnlyQuoteRefused",
    "PlanWithoutCalibrationStageRefused",
)


# V113a closed-range: "train at three to four data volumes".
CALIBRATION_MIN_VOLUMES: int = 3
CALIBRATION_MAX_VOLUMES: int = 4


# ---------------------------------------------------------------------------
# Refusals (V113a + V113e + V113f)
# ---------------------------------------------------------------------------


class CalibrationVolumeCountError(Exception):
    """§11.2 V113a: 'train at three to four data volumes'.

    Raised at `CalibrationOutput.__post_init__` when volumes count is
    below 3 or above 4.
    """


class PointEstimateOnlyQuoteRefused(Exception):
    """§11.2 V113e: 'Only then is the full run quoted, with a stated
    confidence interval — never a point estimate.'

    Raised by `assert_full_run_quote_has_ci` when the passed quote is
    not a `CostQuoteWithCI` instance (bare numbers and duck-typed
    lookalikes are refused).
    """


class PlanWithoutCalibrationStageRefused(Exception):
    """§11.2 V113f: 'A plan without a calibration stage is rejected.'

    Raised by `assert_plan_has_calibration_stage` when the plan has
    no calibration output attached.
    """


# ---------------------------------------------------------------------------
# Carriers (V113a..V113d)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CalibrationVolume:
    """§11.2 V113a: one of the three-to-four data volumes."""

    volume_id: str
    hours: float


@dataclass(frozen=True)
class PerStratumTestSetEval:
    """§11.2 V113b: 'evaluate per stratum against the test set'."""

    stratum_ref: str
    volume_id: str
    accuracy_at_volume: float


@dataclass(frozen=True)
class ScalingCurveFit:
    """§11.2 V113c: 'fit the scaling curve'."""

    fit_type: str
    fit_params: Mapping[str, float]


@dataclass(frozen=True)
class CalibrationOutput:
    """§11.2 V113 verbatim (LOAD-BEARING) composed calibration output.

    Frozen 4-carrier:
      - `volumes`: 3..4 `CalibrationVolume` (V113a · closed-range at __post_init__).
      - `per_stratum_evals`: tuple of `PerStratumTestSetEval` (V113b).
      - `curve_fit`: `ScalingCurveFit` (V113c).
      - `extrapolated_hours_to_threshold`: mapping stratum_ref → hours
        (V113d · 'extrapolate to the acceptance threshold').
    """

    volumes: Tuple[CalibrationVolume, ...]
    per_stratum_evals: Tuple[PerStratumTestSetEval, ...]
    curve_fit: ScalingCurveFit
    extrapolated_hours_to_threshold: Mapping[str, float]

    def __post_init__(self) -> None:
        n = len(self.volumes)
        if not (CALIBRATION_MIN_VOLUMES <= n <= CALIBRATION_MAX_VOLUMES):
            raise CalibrationVolumeCountError(
                f"CalibrationOutput requires 'three to four data volumes' "
                f"(V113a · P179 verbatim); got {n} (min={CALIBRATION_MIN_VOLUMES}, "
                f"max={CALIBRATION_MAX_VOLUMES})."
            )


# ---------------------------------------------------------------------------
# Composition-checks (V113e + V113f)
# ---------------------------------------------------------------------------


def assert_full_run_quote_has_ci(*, quote: CostQuoteWithCI) -> None:
    """§11.2 V113e verbatim enforcement.

    Refuses `PointEstimateOnlyQuoteRefused` when `quote` is not an
    actual `CostQuoteWithCI` instance.  CP-M6-7-3's
    `CostQuoteWithCI.__post_init__` already refuses None CI bounds;
    this gate closes the surface where a caller might pass a bare
    number or duck-typed lookalike instead of the CI-bearing carrier.
    """
    if type(quote) is not CostQuoteWithCI:  # noqa: E721
        raise PointEstimateOnlyQuoteRefused(
            "full run quote must be a CostQuoteWithCI (V113e · P179 "
            "'stated confidence interval — never a point estimate')."
        )


def assert_plan_has_calibration_stage(
    *, plan_has_calibration_output: bool,
) -> None:
    """§11.2 V113f verbatim enforcement.

    Refuses `PlanWithoutCalibrationStageRefused` when the flag is
    False.  V113f verbatim: 'A plan without a calibration stage is
    rejected.'
    """
    if not plan_has_calibration_output:
        raise PlanWithoutCalibrationStageRefused(
            "plan is missing calibration stage output "
            "(V113f · P179 'A plan without a calibration stage is rejected')."
        )
