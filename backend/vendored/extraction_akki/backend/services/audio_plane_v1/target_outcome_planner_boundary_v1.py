"""CP-AIP-7-TARGET-OUTCOME-PLANNER · target_outcome_planner_boundary_v1 · additive §1.2.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-7-TARGET-OUTCOME-PLANNER and nothing else.

Spec anchors:
- AIP v1.0 §10.1 P161 verbatim (LOAD-BEARING): 'test_set_ref must
  exist before the Outcome is accepted.'
- §10.2 P162 verbatim: 'The test set precedes the training.'
- §10.2 verbatim: 'Population is register-defined, not label-defined.'
- §11.1 verbatim: 'The existing planner pattern is reused unchanged:
  a deterministic core computes eligibility; a learned layer may only
  reorder an already-eligible set it receives stripped of the values
  that decided eligibility; a gate compares learned output against
  the deterministic baseline; every plan is reproducible from its
  recorded inputs.'
- §11.4 P185 (V115) verbatim: 'Coverage report - per target stratum:
  hours available, quality distribution, gaps, cost of closing each gap.'
- §11.4 P188 (V118) verbatim: 'Cost quote with a stated confidence
  interval.'
- §16.2 owner working default 2026-02-23T04:15Z: 'platform default
  for gate_policy where Outcome does not set it is missed-stratum-
  gates-release (fail-closed per §1.5 doctrine).'

The compose-boundary binds sealed CP-AIP-6 `TargetOutcome_v0`
(contracts-layer) to sealed CP-M6-7-2/3 planner primitives + sealed
CP-M6-3 `CharacterRegister`. Five typed refusals surface the shape
violations at boundary:
  1. `TestSetUnresolvedAtPlannerEntry` (§10.2)
  2. `PopulationNotResolvableAgainstRegister` (§11.1 · re-raised from
     register_stratum_resolver_v1)
  3. `StratumSetSubtractedFromRegisterError` (§11.4 additive-only)
  4. `CostQuoteMissingCIAtBoundary` (§11.4 P188 · surfaces sealed
     `CostQuoteMissingCIError`)
  5. `MissedStratumReleaseAtBoundary` (§16.2 owner working default)

Sealed carriers composed (UNCHANGED per SO §3.8):
- backend/contracts/target_outcome_v0.py (CP-AIP-6): `TargetOutcome_v0`.
- backend/services/audio_plane_v1/training_planner.py (CP-M6-7-2/3):
  `run_eligibility_gate` · `CoverageReport` · `CostQuoteWithCI` ·
  `CostQuoteMissingCIError` · sealed planner primitives.
- backend/services/audio_plane_v1/character_register.py (CP-M6-3):
  `CharacterRegister`.
- backend/services/audio_plane_v1/register_stratum_resolver_v1.py
  (CP-AIP-7 sibling): `resolve_population_against_register`.

Additive-only per SO §3.8 · no edit to sealed carriers · §1.2 no-
redeclaration of sealed planner + register carriers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Optional, Protocol

from backend.contracts.target_outcome_v0 import TargetOutcome_v0
from backend.services.audio_plane_v1.character_register import CharacterRegister
from backend.services.audio_plane_v1.register_stratum_resolver_v1 import (
    PopulationNotResolvableAgainstRegister,
    resolve_population_against_register,
)
from backend.services.audio_plane_v1.training_planner import (
    CoverageReport,
    CostQuoteMissingCIError,
    CostQuoteWithCI,
    run_eligibility_gate,
)


HONEST_GAP_V1_POSTURE: Final[str] = (
    "CP-AIP-7-TARGET-OUTCOME-PLANNER · this compose boundary refuses "
    "malformed TargetOutcome_v0/planner-input pairs at entry; it does "
    "NOT itself compute eligibility or coverage - those are the sealed "
    "CP-M6-7-2/3 primitives, invoked unchanged per §11.1 verbatim."
)


# ---------------------------------------------------------------------------
# TestSetIndex_v1 Protocol seam · §10.1 P161 LOAD-BEARING resolver
# ---------------------------------------------------------------------------


class TestSetIndex_v1(Protocol):
    """§10.1 P161 verbatim (LOAD-BEARING): 'test_set_ref must exist
    before the Outcome is accepted.' Test-set resolver Protocol.
    """

    def resolve(self, test_set_ref: str) -> Optional[Any]:  # pragma: no cover
        ...


# ---------------------------------------------------------------------------
# Refusal hierarchy · all subclass PlannerBoundaryRefused
# ---------------------------------------------------------------------------


class PlannerBoundaryRefused(Exception):
    """Base class for every CP-AIP-7 compose-boundary refusal.

    Ledger check - CP-AIP-7-TARGET-OUTCOME-PLANNER refusal boundary.
    """


class TestSetUnresolvedAtPlannerEntry(PlannerBoundaryRefused):
    """§10.2 verbatim: 'The test set precedes the training.' Raised
    when `TestSetIndex_v1.resolve(target_outcome.test_set_ref)` is None.
    """


class StratumSetSubtractedFromRegisterError(PlannerBoundaryRefused):
    """§11.4 verbatim + §11.1 register-defined: emitted coverage
    report's stratum-set is a proper subset of the current register's
    stratum-set. Register never subtracts.
    """


class CostQuoteMissingCIAtBoundary(PlannerBoundaryRefused):
    """§11.4 P188 (V118) verbatim: 'Cost quote with a stated confidence
    interval.' Raised when sealed `CostQuoteWithCI` construction has
    raised `CostQuoteMissingCIError`.
    """


class MissedStratumReleaseAtBoundary(PlannerBoundaryRefused):
    """§16.2 owner working default 2026-02-23T04:15Z: 'missed-stratum-
    gates-release (fail-closed per §1.5 doctrine).' Raised when
    `TargetOutcome_v0.gate_policy == 'missed stratum gates release'`
    AND coverage report has a stratum whose `gap_hours_h > 0.0`.
    """


# ---------------------------------------------------------------------------
# Frozen boundary result carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PlannerBoundaryResult_v1:
    """CP-AIP-7 compose-boundary success carrier.

    Frozen 3-carrier:
      - `resolved_population`: register-resolved population string.
      - `test_set_ref`: verified-resolved test_set_ref.
      - `target_outcome`: the accepted `TargetOutcome_v0` instance.
    """

    resolved_population: str
    test_set_ref: str
    target_outcome: TargetOutcome_v0


# ---------------------------------------------------------------------------
# Compose-boundary entry · §10.2 + §11.1 refusals composed
# ---------------------------------------------------------------------------


def enter_planner_with_target_outcome(
    *,
    target_outcome: TargetOutcome_v0,
    character_register: CharacterRegister,
    test_set_index: TestSetIndex_v1,
) -> PlannerBoundaryResult_v1:
    """§10.2 + §11.1 compose-boundary entry.

    Refuses:
      - `TestSetUnresolvedAtPlannerEntry` if
        `test_set_index.resolve(target_outcome.test_set_ref)` is None
        (§10.2 verbatim 'The test set precedes the training').
      - `PopulationNotResolvableAgainstRegister` if
        `target_outcome.population` is not a register layer value
        (§11.1 verbatim 'population is register-defined').

    Returns:
      `PlannerBoundaryResult_v1` on success.
    """
    if test_set_index.resolve(target_outcome.test_set_ref) is None:
        raise TestSetUnresolvedAtPlannerEntry(
            f"CP-AIP-7 · §10.2 verbatim: 'The test set precedes the "
            f"training.' TargetOutcome_v0.test_set_ref="
            f"{target_outcome.test_set_ref!r} is not resolvable against "
            f"the TestSetIndex_v1 · refused at planner entry."
        )

    resolved_population = resolve_population_against_register(
        population=target_outcome.population,
        character_register=character_register,
    )

    return PlannerBoundaryResult_v1(
        resolved_population=resolved_population,
        test_set_ref=target_outcome.test_set_ref,
        target_outcome=target_outcome,
    )


# ---------------------------------------------------------------------------
# §11.4 additive-only stratum-set boundary
# ---------------------------------------------------------------------------


def assert_coverage_report_additive_over_register(
    *,
    coverage_report: CoverageReport,
    character_register: CharacterRegister,
) -> None:
    """§11.4 P185 verbatim + §11.1 register-defined: emitted
    `CoverageReport.entries[].stratum_ref` set MUST be a superset of
    the register's stratum-set (union of `CharacterEntry.layer`).
    Register never subtracts.

    Raises:
      StratumSetSubtractedFromRegisterError: coverage report's
      stratum-set is a proper subset of the register's stratum-set.
    """
    register_strata = frozenset(
        entry.layer for entry in character_register.entries
    )
    coverage_strata = frozenset(
        entry.stratum_ref for entry in coverage_report.entries
    )
    missing = register_strata - coverage_strata
    if missing:
        raise StratumSetSubtractedFromRegisterError(
            f"CP-AIP-7 · §11.4 verbatim + §11.1 verbatim: coverage "
            f"report is missing strata {sorted(missing)!r} present in "
            f"the current register (register strata: "
            f"{sorted(register_strata)!r} · coverage strata: "
            f"{sorted(coverage_strata)!r}). Register never subtracts."
        )


# ---------------------------------------------------------------------------
# §11.4 P188 · CostQuoteWithCI boundary
# ---------------------------------------------------------------------------


def build_cost_quote_with_ci_at_boundary(
    *,
    point_estimate: float,
    ci_low: Optional[float],
    ci_high: Optional[float],
) -> CostQuoteWithCI:
    """§11.4 P188 (V118) verbatim: 'Cost quote with a stated confidence
    interval.' Surfaces sealed `CostQuoteMissingCIError` at boundary
    as `CostQuoteMissingCIAtBoundary`.

    Raises:
      CostQuoteMissingCIAtBoundary: sealed `CostQuoteMissingCIError`
      was raised by sealed `CostQuoteWithCI` construction.
    """
    try:
        return CostQuoteWithCI(
            point_estimate=point_estimate,
            ci_low=ci_low,
            ci_high=ci_high,
        )
    except CostQuoteMissingCIError as exc:
        raise CostQuoteMissingCIAtBoundary(
            f"CP-AIP-7 · §11.4 P188 (V118) verbatim: 'Cost quote with "
            f"a stated confidence interval.' Sealed CostQuoteWithCI "
            f"refusal surfaced at compose boundary: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# §16.2 owner working default · missed-stratum-gates-release fail-closed
# ---------------------------------------------------------------------------


_MISSED_STRATUM_GATES_RELEASE: Final[str] = "missed stratum gates release"


def assert_missed_stratum_gates_release(
    *,
    target_outcome: TargetOutcome_v0,
    coverage_report: CoverageReport,
) -> None:
    """§16.2 owner working default 2026-02-23T04:15Z: 'missed-stratum-
    gates-release (fail-closed per §1.5 doctrine).'

    When `target_outcome.gate_policy == 'missed stratum gates release'`,
    the boundary refuses release if any stratum in the coverage report
    has `gap_hours_h > 0.0` (fail-closed).

    Raises:
      MissedStratumReleaseAtBoundary: gate_policy is the platform
      default AND coverage report has a stratum with a non-zero gap.
    """
    if target_outcome.gate_policy != _MISSED_STRATUM_GATES_RELEASE:
        return
    unmet = [
        entry.stratum_ref
        for entry in coverage_report.entries
        if entry.gap_hours_h > 0.0
    ]
    if unmet:
        raise MissedStratumReleaseAtBoundary(
            f"CP-AIP-7 · §16.2 owner working default 2026-02-23T04:15Z: "
            f"'missed-stratum-gates-release (fail-closed per §1.5 "
            f"doctrine).' TargetOutcome_v0.gate_policy is the platform "
            f"default AND coverage report has strata with unmet "
            f"acceptance: {sorted(unmet)!r} · release refused."
        )


# ---------------------------------------------------------------------------
# §11.1 sealed run_eligibility_gate composition · re-exported by name
# ---------------------------------------------------------------------------

# Re-export sealed CP-M6-7-2 run_eligibility_gate by name (composition,
# not redeclaration). §11.1 verbatim: 'The existing planner pattern is
# reused unchanged.'
__all__ = (
    "HONEST_GAP_V1_POSTURE",
    "TestSetIndex_v1",
    "PlannerBoundaryRefused",
    "TestSetUnresolvedAtPlannerEntry",
    "PopulationNotResolvableAgainstRegister",  # re-exported from resolver.
    "StratumSetSubtractedFromRegisterError",
    "CostQuoteMissingCIAtBoundary",
    "MissedStratumReleaseAtBoundary",
    "PlannerBoundaryResult_v1",
    "enter_planner_with_target_outcome",
    "assert_coverage_report_additive_over_register",
    "build_cost_quote_with_ci_at_boundary",
    "assert_missed_stratum_gates_release",
    "run_eligibility_gate",  # sealed CP-M6-7-2 composition.
)
