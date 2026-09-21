"""M6 · Audio-Plane v1.0 · CP-M6-7-1 · Full §10 TargetOutcome carrier.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §10.1 P154..P164 (V98..V104 · TargetOutcome block):
      "task — operational statement of what the model must do"
      "domain — context of use"
      "population — defined by reference to register strata, not labels"
      "acceptance — threshold per stratum; two-dimensional (accuracy, coverage)"
      "gate_policy — per Outcome: missed stratum gates release | ships documented"
      "test_set_ref — must exist before the Outcome is accepted"
      "constraints — latency, compute budget, deployment target"

- Audio-Plane §10.2 P165..P169 (V105..V108 · binding rules):
      P166 (V105): "Population is register-defined. 'Language L, accent clusters 1–4, telephone band and studio, adult' — never 'speakers of L.' This is what makes coverage computable."
      P167 (V106): "Acceptance is per stratum. A single global threshold hides the failure that matters: 94% on the majority variant and 61% on the rest passes one test and fails the one that decides whether the work reaches the people it was built for."
      P168 (V107 · LOAD-BEARING): "The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time."
      P169 (V108): "The gate decision is recorded on the Outcome at definition — not decided ad hoc at ship time."

Wave-honest limits (per M6 SW7 grounding brief §D):
  - Population shape only: enforces "population references register
    strata (non-empty stratum_refs)"; does NOT verify that referenced
    stratum_refs exist in the CP-M6-3-1 CharacterRegister (downstream
    composition, out of scope this CP).
  - No LLM / HTTP / filesystem / network.
  - Case-agnostic; no coupling to any specific stratum class.
  - §3.1 P038 tokens-not-waveforms discipline preserved.
  - Composes with existing AcceptanceBar from objective_wizard.py
    (imported and re-exported); does NOT modify objective_wizard.py.

Contract:

    GATE_POLICY_VALUES = frozenset({
        "missed_stratum_gates_release",  # V102 · closed-set value 1
        "ships_documented",              # V102 · closed-set value 2
    }).

    PopulationSpec — frozen 1-carrier:
        stratum_refs: Tuple[str, ...]  (V100 · register-defined; V105
                                        refuses empty at __post_init__)

    Constraints — frozen 3-carrier (V104 verbatim triple):
        latency · compute_budget · deployment_target

    TargetOutcome — frozen 7-carrier (V98..V104):
        task · domain · population: PopulationSpec ·
        acceptance: AcceptanceBar (V106 per-stratum enforced at
                                   factory-level) ·
        gate_policy: str (V102 · closed-set enforced at __post_init__;
                          V108 gate-at-definition enforced by frozen
                          discipline) ·
        test_set_ref: str (V107 · LOAD-BEARING · mandatory · not Optional) ·
        constraints: Constraints.

    construct_target_outcome(...) -> TargetOutcome
        Factory that additionally enforces cross-field:
          - V107: test_set_ref != "" → TestSetRefMissingError otherwise.
          - V106: acceptance.has_per_stratum_dimension is True →
                  AcceptancePerStratumMissingError otherwise.

Refusals (4):
    - GatePolicyInvalidError            (V102 · closed-set)
    - PopulationEmptyStrataRefsError    (V105 · register-defined)
    - TestSetRefMissingError            (V107 · load-bearing)
    - AcceptancePerStratumMissingError  (V106 · per-stratum acceptance)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

# Compose with sub-wave 6: import + re-export AcceptanceBar so callers
# of target_outcome only need one import to construct TargetOutcome.
# (No modification to objective_wizard.py; import-only composition.)
from services.audio_plane_v1.objective_wizard import AcceptanceBar


GATE_POLICY_VALUES = frozenset({
    "missed_stratum_gates_release",
    "ships_documented",
})


class GatePolicyInvalidError(ValueError):
    """`gate_policy` not in the closed set GATE_POLICY_VALUES.
    §10.1 P160 (V102) verbatim: 'gate_policy — per Outcome: missed
    stratum gates release | ships documented'."""


class PopulationEmptyStrataRefsError(ValueError):
    """`PopulationSpec.stratum_refs` is empty.  §10.2 P166 (V105):
    'Population is register-defined ... never speakers of L.  This
    is what makes coverage computable.'  An empty stratum_refs is a
    label-only population, refused by construction."""


class TestSetRefMissingError(ValueError):
    """`test_set_ref` is empty.  §10.2 P168 (V107 · LOAD-BEARING):
    'The test set precedes the training.  An Outcome without an
    existing, stratified test set is rejected at definition time.'"""


class AcceptancePerStratumMissingError(ValueError):
    """`acceptance.has_per_stratum_dimension` is False.  §10.2 P167
    (V106): 'Acceptance is per stratum. A single global threshold
    hides the failure that matters ...'."""


@dataclass(frozen=True)
class PopulationSpec:
    """§10.1 P158 (V100) verbatim carrier: 'population — defined by
    reference to register strata, not labels'.  V105 register-defined
    rule enforced at construction: empty `stratum_refs` refuses."""

    stratum_refs: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.stratum_refs:
            raise PopulationEmptyStrataRefsError(
                "PopulationSpec.stratum_refs must be non-empty "
                "(§10.2 P166 · V105: population is register-defined; "
                "empty stratum_refs is a label-only population)"
            )


@dataclass(frozen=True)
class Constraints:
    """§10.1 P162 (V104) verbatim carrier: 'constraints — latency,
    compute budget, deployment target'.  Frozen 3-carrier."""

    latency: str
    compute_budget: str
    deployment_target: str


@dataclass(frozen=True)
class TargetOutcome:
    """§10.1 P154..P164 (V98..V104) verbatim 7-carrier TargetOutcome
    block.  Frozen dataclass — V108 gate-at-definition enforced
    (gate_policy immutable post-construction).

    Fields (verbatim canon order):
      - task            (V98 · P156)
      - domain          (V99 · P157)
      - population      (V100 · P158 · PopulationSpec)
      - acceptance      (V101 · P159 · AcceptanceBar)
      - gate_policy     (V102 · P160 · closed-set)
      - test_set_ref    (V103 · P161 · LOAD-BEARING · mandatory)
      - constraints     (V104 · P162 · Constraints)
    """

    task: str
    domain: str
    population: PopulationSpec
    acceptance: AcceptanceBar
    gate_policy: str
    test_set_ref: str
    constraints: Constraints

    def __post_init__(self) -> None:
        if self.gate_policy not in GATE_POLICY_VALUES:
            raise GatePolicyInvalidError(
                f"gate_policy={self.gate_policy!r} not in closed set "
                f"{sorted(GATE_POLICY_VALUES)!r} "
                f"(§10.1 P160 · V102)"
            )


def construct_target_outcome(
    *,
    task: str,
    domain: str,
    population: PopulationSpec,
    acceptance: AcceptanceBar,
    gate_policy: str,
    test_set_ref: str,
    constraints: Constraints,
) -> TargetOutcome:
    """Factory: enforces cross-field V106 + V107 before construction.

    Refusals (in P036 receipt-before-result order):
      1. TestSetRefMissingError            (V107 · load-bearing · fires first)
      2. AcceptancePerStratumMissingError  (V106 · per-stratum acceptance)

    Then delegates to TargetOutcome(...) which fires:
      3. GatePolicyInvalidError            (V102 · closed-set)
      (and pass-through PopulationEmptyStrataRefsError from PopulationSpec
       __post_init__ if the caller passed an already-empty PopulationSpec)
    """
    if not test_set_ref:
        raise TestSetRefMissingError(
            "test_set_ref must be non-empty "
            "(§10.2 P168 · V107 · LOAD-BEARING: the test set precedes "
            "the training; an Outcome without an existing test set is "
            "rejected at definition time)"
        )
    if not acceptance.has_per_stratum_dimension:
        raise AcceptancePerStratumMissingError(
            "acceptance.has_per_stratum_dimension must be True "
            "(§10.2 P167 · V106: acceptance is per stratum; a single "
            "global threshold hides the failure that matters)"
        )
    return TargetOutcome(
        task=task,
        domain=domain,
        population=population,
        acceptance=acceptance,
        gate_policy=gate_policy,
        test_set_ref=test_set_ref,
        constraints=constraints,
    )
