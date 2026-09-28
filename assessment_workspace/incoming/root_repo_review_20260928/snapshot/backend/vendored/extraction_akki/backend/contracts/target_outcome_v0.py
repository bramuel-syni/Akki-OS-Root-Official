"""CP-AIP-6-OBJECTIVE-WIZARD · TargetOutcome_v0 contract · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

Spec anchor: AIP v1.0 §10 Target Outcome.

§10.1 verbatim seven-field schema:
    TargetOutcome {
      task          operational statement of what the model must do
      domain        context of use
      population    defined by reference to register strata, not labels
      acceptance    threshold per stratum; two-dimensional (accuracy, coverage)
      gate_policy   per Outcome: missed stratum gates release | ships documented
      test_set_ref  must exist before the Outcome is accepted
      constraints   latency, compute budget, deployment target
    }

§10.2 binding rules verbatim:
    - Population is register-defined.
    - Acceptance is per stratum.
    - The test set precedes the training.
    - The gate decision is recorded on the Outcome at definition.

Additive-only per SO §3.8. No edit to sealed wizard contracts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Final, Mapping, Tuple


GATE_POLICIES: Final[Tuple[str, ...]] = (
    "missed stratum gates release",
    "ships documented",
)


@dataclass(frozen=True)
class StratumAcceptance_v0:
    """§10.1 verbatim: 'threshold per stratum; two-dimensional (accuracy, coverage)'.
    Frozen carrier · §1.5 unrepresentable-not-policed: both dimensions
    are required for construction; missing either fails-fast.
    """

    accuracy: float
    coverage: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.accuracy <= 1.0:
            raise ValueError(
                f"StratumAcceptance_v0.accuracy={self.accuracy} outside "
                f"[0.0, 1.0] · §10.1 verbatim requires threshold values."
            )
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError(
                f"StratumAcceptance_v0.coverage={self.coverage} outside "
                f"[0.0, 1.0] · §10.1 verbatim requires threshold values."
            )


@dataclass(frozen=True)
class TargetOutcome_v0:
    """§10.1 verbatim seven-field TargetOutcome schema.

    Fields:
      - task · operational statement of what the model must do.
      - domain · context of use.
      - population · defined by reference to register strata (§10.2).
      - acceptance · threshold per stratum · two-dimensional.
      - gate_policy · per Outcome · closed-set (§10.2 verbatim).
      - test_set_ref · must exist before the Outcome is accepted (§10.2).
      - constraints · latency, compute budget, deployment target.
    """

    task: str
    domain: str
    population: str
    acceptance: Tuple[Tuple[str, StratumAcceptance_v0], ...]
    gate_policy: str
    test_set_ref: str
    constraints: Tuple[Tuple[str, Any], ...]

    def __post_init__(self) -> None:
        if self.gate_policy not in GATE_POLICIES:
            raise ValueError(
                f"TargetOutcome_v0.gate_policy={self.gate_policy!r} "
                f"outside closed-set {GATE_POLICIES!r} · §10.2 verbatim: "
                f"'The gate decision is recorded on the Outcome at "
                f"definition — not decided ad hoc at ship time.'"
            )
