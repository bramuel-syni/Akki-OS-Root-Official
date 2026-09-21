"""OptimizerComparisonV0 · Doc 17 §A17.5-A17.6 · two-arm optimizer harness.

Owner-verbatim spec anchor (grounding brief lines 29-30):

    A17.5-A17.6 [CANON] The optimizer-selection protocol: two arms,
    identical conditions, parity mandatory.

    The protocol executes at the first adapter training on real
    material, inside the P4-instrumented run. Its shape is one
    two-arm comparison — the current baseline optimizer versus a
    candidate, Muon named as the first — with identical training
    data, identical base model, identical evaluation sets, and an
    identical compute-budget cap, run on the smallest stratum that
    still yields a valid MOAC evaluation. Four measured outputs
    are reported for both arms without exception: target-stratum
    improvement (MOAC's M-a), non-target regression (M-b),
    wall-clock and GPU-hours to convergence, and calibration
    quality (an M-e input). Quality parity on M-a and M-b is
    mandatory for the candidate to remain eligible at all;
    compute-to-convergence is reported, never gating — a faster
    optimizer that regresses quality is not eligible regardless of
    its speed. The adopt/reject decision is then an Owner ruling
    made on the measured results, with no adoption threshold fixed
    in advance of the evidence, and verdict samples are uncurated
    per the platform's standing D-7 doctrine (evaluation inputs
    may be engineered; evaluation samples may not). On adoption,
    the winning arm writes training_params@v0 v1 with the
    comparison attached; on rejection, the candidate is recorded
    as tested, with its numbers, permanently. The identical
    protocol governs every future recipe-component candidate —
    this is not a one-time bootstrap, it is how the recipe seat
    is filled from now on.

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True) on every model.
  * tests/invariants/optimizer_comparison_v0.contract_snapshot.json
    is the frozen JSON Schema snapshot at CP5 landing.
  * Parity map bump 61 -> 62 in test_frozen_contract_snapshot_parity.py.

Verdict grammar (closed Literal per Owner Ruling R3 CP4 §19 pattern):
  * 'awaiting_owner' — measurements recorded, ruling pending.
  * 'adopted'        — Owner adopted the candidate (writes v1 recipe).
  * 'rejected'       — Owner rejected the candidate (recorded, tested,
                       numbers permanent).
  * 'ineligible'     — quality parity on M-a/M-b failed; verdict
                       gated by the harness itself, not by Owner.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


VERDICT_KINDS: tuple = ("awaiting_owner", "adopted", "rejected", "ineligible")
ARM_KINDS: tuple = ("baseline", "muon")


class ArmMeasurements(BaseModel):
    """Four measured outputs · A17.5 'without exception'."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    moac_m_a_improvement: float = Field(
        ...,
        description="Target-stratum improvement (MOAC M-a).",
    )
    moac_m_b_regression: float = Field(
        ...,
        description="Non-target regression (MOAC M-b).",
    )
    wallclock_seconds_to_convergence: int = Field(
        ...,
        ge=0,
        description="Wall-clock seconds · REPORTED, NEVER GATING (A17.5).",
    )
    gpu_hours_to_convergence: float = Field(
        ...,
        ge=0.0,
        description="GPU-hours · REPORTED, NEVER GATING (A17.5).",
    )
    moac_m_e_calibration: float = Field(
        ...,
        description="Calibration quality · MOAC M-e input.",
    )
    evaluation_samples_uncurated: bool = Field(
        ...,
        description="D-7 doctrine · evaluation inputs may be engineered, "
                    "samples may not. This flag MUST be True to accept the "
                    "measurement (harness invariant enforces).",
    )


class OptimizerComparisonV0(BaseModel):
    """Doc 17 §A17.5 · one two-arm comparison shell.

    Identical conditions are recorded on shell open (base_model_id,
    evaluation_sets, budget_cap). Each arm's four measured outputs
    are recorded when the arm completes. Verdict is ratified by
    Owner ruling on the measured results; no adoption threshold
    fixed in advance of the evidence.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    comparison_id: str = Field(..., min_length=1)
    base_model_id: str = Field(..., min_length=1)
    evaluation_sets: List[str] = Field(..., min_length=1)
    budget_cap_wallclock_seconds: int = Field(..., ge=1)
    budget_cap_gpu_hours: float = Field(..., ge=0.0)
    smallest_stratum: str = Field(
        ...,
        min_length=1,
        description="'The smallest stratum that still yields a valid MOAC "
                    "evaluation' (A17.5 verbatim).",
    )
    baseline_measurements: Optional[ArmMeasurements] = Field(
        default=None,
        description="Filled when baseline arm completes.",
    )
    muon_measurements: Optional[ArmMeasurements] = Field(
        default=None,
        description="Filled when muon arm completes.",
    )
    verdict: Literal["awaiting_owner", "adopted", "rejected", "ineligible"] = Field(
        default="awaiting_owner",
    )
    verdict_note: str = Field(
        default="",
        description="Human-speak note captured with the verdict; empty at "
                    "shell open.",
    )
    ratified_at: Optional[str] = Field(
        default=None,
        description="ISO-8601 UTC timestamp of owner ruling; None until "
                    "verdict != 'awaiting_owner'.",
    )
    opened_at: str = Field(..., min_length=1)
