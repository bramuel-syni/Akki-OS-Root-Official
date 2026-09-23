"""CP-AIP-6-OBJECTIVE-WIZARD · objective_compile · §8.4 compile-time rejections.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

Spec anchor: AIP v1.0 §8.4 Compile-time rejections.

§8.4 verbatim: 'The wizard cannot emit an artifact the downstream
contracts would refuse. Rejected at compile, not warned:
    - An Outcome without an existing test_set_ref.
    - An acceptance bar missing the per-stratum dimension.
    - A Collection Schema requiring a column whose capture violates
      the custody conditions of §6.2.'

Additive-only per SO §3.8.  Sealed wizard state machine
(operator_state_machine.py) is NOT edited.
"""
from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from backend.contracts.target_outcome_v0 import (
    GATE_POLICIES,
    StratumAcceptance_v0,
    TargetOutcome_v0,
)
from backend.contracts.collection_schema_v0 import (
    CUSTODY_VIOLATING_TOKENS,
    CollectionSchema_v0,
)


class ObjectiveCompileError(Exception):
    """Base class for §8.4 compile-time rejections."""


class TestSetRefMissing(ObjectiveCompileError):
    """§8.4 verbatim: 'An Outcome without an existing test_set_ref.'
    Rejected at compile time · not warned · not deferred to runtime."""


class AcceptanceBarNotStratified(ObjectiveCompileError):
    """§8.4 verbatim: 'An acceptance bar missing the per-stratum
    dimension.'  Rejected at compile time."""


class CustodyViolation(ObjectiveCompileError):
    """§8.4 verbatim: 'A Collection Schema requiring a column whose
    capture violates the custody conditions of §6.2.'  Rejected at
    compile time via structural token scan of column names."""


def compile_target_outcome(
    *,
    task: str,
    domain: str,
    population: str,
    acceptance: Mapping[str, Mapping[str, float]],
    gate_policy: str,
    test_set_ref: str,
    constraints: Mapping[str, Any],
) -> TargetOutcome_v0:
    """§8.4 compile-time rejection surface for TargetOutcome_v0.

    Refusals (order-independent · fails-fast at first tripped guard):
      - `TestSetRefMissing` when `test_set_ref` is empty / whitespace-
        only / falsy (§8.4 verbatim + §10.2 verbatim: 'The test set
        precedes the training.').
      - `AcceptanceBarNotStratified` when `acceptance` is empty or any
        stratum entry lacks both accuracy + coverage dimensions (§8.4 +
        §10.2 verbatim: 'Acceptance is per stratum.').

    Returns a frozen `TargetOutcome_v0` on pass (structural §1.5 gates
    fire inside sealed `TargetOutcome_v0.__post_init__` for gate_policy
    closed-set discipline).
    """
    if not test_set_ref or not test_set_ref.strip():
        raise TestSetRefMissing(
            f"§8.4 compile-time rejection: test_set_ref="
            f"{test_set_ref!r} is empty/whitespace-only. §10.2 verbatim: "
            f"'The test set precedes the training. An Outcome without an "
            f"existing, stratified test set is rejected at definition time.'"
        )
    if not acceptance:
        raise AcceptanceBarNotStratified(
            "§8.4 compile-time rejection: acceptance is empty. §10.2 "
            "verbatim: 'Acceptance is per stratum. A single global "
            "threshold hides the failure that matters.'"
        )
    stratum_acceptance_pairs = []
    for stratum_name, dims in acceptance.items():
        if not isinstance(dims, Mapping):
            raise AcceptanceBarNotStratified(
                f"§8.4: acceptance[{stratum_name!r}] must map to a "
                f"two-dimensional (accuracy, coverage) mapping."
            )
        if "accuracy" not in dims or "coverage" not in dims:
            raise AcceptanceBarNotStratified(
                f"§8.4: acceptance[{stratum_name!r}] missing per-stratum "
                f"two-dimensional shape · both 'accuracy' and 'coverage' "
                f"required per §10.1 verbatim."
            )
        stratum_acceptance_pairs.append((
            stratum_name,
            StratumAcceptance_v0(
                accuracy=float(dims["accuracy"]),
                coverage=float(dims["coverage"]),
            ),
        ))
    return TargetOutcome_v0(
        task=task,
        domain=domain,
        population=population,
        acceptance=tuple(stratum_acceptance_pairs),
        gate_policy=gate_policy,
        test_set_ref=test_set_ref,
        constraints=tuple(constraints.items()),
    )


def compile_collection_schema(
    *,
    baseline_tier: Tuple[str, ...],
    objective_tier: Tuple[str, ...],
) -> CollectionSchema_v0:
    """§8.4 compile-time rejection surface for CollectionSchema_v0.

    Refusal:
      - `CustodyViolation` when any column name in baseline_tier or
        objective_tier contains a §6.2-violating token (§8.4 verbatim).
    """
    for column in tuple(baseline_tier) + tuple(objective_tier):
        lowered = column.lower()
        for tok in CUSTODY_VIOLATING_TOKENS:
            if tok in lowered:
                raise CustodyViolation(
                    f"§8.4 compile-time rejection: CollectionSchema "
                    f"column {column!r} contains §6.2-custody-violating "
                    f"token {tok!r}. §8.4 verbatim: 'A Collection Schema "
                    f"requiring a column whose capture violates the "
                    f"custody conditions of §6.2' is REJECTED at compile."
                )
    return CollectionSchema_v0(
        baseline_tier=tuple(baseline_tier),
        objective_tier=tuple(objective_tier),
    )
