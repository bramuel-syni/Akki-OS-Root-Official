"""M6 · Audio-Plane v1.0 · CP-M6-7-2 · §11.1 Training Planner architecture.

Verbatim canon anchor (§11.1 P172 · V109 · single-line for gating-test docstring parity):

  "The existing planner pattern is reused unchanged: a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs."

Verbatim canon anchors added by CP-M6-7-3 Part-B extension (§11.4 P185..P188 · V115..V118):

  V115 · P185: "Coverage report — per target stratum: hours available, quality distribution, gaps, cost of closing each gap."

  V116 · P186: "Curriculum — ordering and weighting across strata derived from the register, not from the corpus's natural distribution, which is always skewed toward whatever occurred most. The dedup instance condition map enters as a designated robustness stratum."

  V117 · P187: "Proposed milestone list (§11.3)."

  V118 · P188: "Cost quote with a stated confidence interval."

Readable rendering of the same clause:

    The existing planner pattern is reused unchanged: a
    deterministic core computes eligibility; a learned layer may
    only reorder an already-eligible set it receives stripped of
    the values that decided eligibility; a gate compares learned
    output against the deterministic baseline; every plan is
    reproducible from its recorded inputs.

This module lands the four-clause seam:

    1. `PlannerCore` (Protocol · runtime-checkable) — the
       deterministic core.  Returns an `EligibilityDecision` carrier
       that binds `eligible_ids` to `values_that_decided`.

    2. `strip_eligibility_decision(decision) -> EligibleStripped` —
       the strip.  Refuses inputs that are not actual
       `EligibilityDecision` instances (subclasses and duck-typed
       lookalikes are refused with
       `LearnedReorderStrippingViolationError`).  The returned
       `EligibleStripped` carries ONLY the ids — no eligibility
       metadata may cross this seam.

    3. `LearnedReorderLayer` (Protocol · runtime-checkable) — the
       learned reorder.  Signature accepts ONLY `eligible_stripped`;
       no values-that-decided-eligibility can cross the signature.

    4. `run_eligibility_gate(*, plan_inputs, planner_core,
       learned_reorder_layer)` — composes the four clauses:
       (a) `planner_core.compute_eligibility(plan_inputs=...)`
           → `EligibilityDecision`.
       (b) `strip_eligibility_decision(decision)` → `EligibleStripped`.
       (c) `learned_reorder_layer.reorder(eligible_stripped=...)`
           → `Tuple[str, ...]`.
       (d) Gate: `frozenset(ordered) == decision.eligible_ids` or
           `EligibilityGateSlippageError`.
       (e) Reproducibility: returns `(ordered, PlanReproducibilityWitness)`
           binding `sha256(plan_inputs)` to `sha256(plan_output)`.

Wave-honest limits (per M6 SW7 grounding brief §D):

- §11 body scope-limited to §11.1 architecture ONLY this CP.
- V109's "learned layer" is Protocol-only; no live training.
- No LLM / HTTP / filesystem / network.
- Case-agnostic; no coupling to any specific eligibility scheme.
- §3.1 P038 tokens-not-waveforms preserved (opaque metadata only).
- Synthetic fixtures only in tests.
- Composes with CP-M6-7-1 `TargetOutcome` via import; does NOT
  modify `target_outcome.py`.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields, is_dataclass
from typing import (
    Any,
    FrozenSet,
    Mapping,
    Protocol,
    Tuple,
    runtime_checkable,
)

from services.audio_plane_v1.target_outcome import TargetOutcome

__all__ = (
    "PlanInputs",
    "EligibilityDecision",
    "EligibleStripped",
    "PlanReproducibilityWitness",
    "PlannerCore",
    "LearnedReorderLayer",
    "strip_eligibility_decision",
    "run_eligibility_gate",
    "LearnedReorderStrippingViolationError",
    "EligibilityGateSlippageError",
    # CP-M6-7-3 · Part-B · §11.4 P184..P188 planner outputs.
    "PerStratumCoverageEntry",
    "CoverageReport",
    "CurriculumOrdering",
    "CostQuoteWithCI",
    "MilestoneListRef",
    "PlannerOutputs",
    "CostQuoteMissingCIError",
    "CurriculumWeightNormalizationError",
)


# ASCII UNIT SEPARATOR — canonical intra-field delimiter (matches prior
# audio_plane_v1 modules' convention · Canon-4 §22 + Pull Seam P1).
_US = "\x1f"


# ---------------------------------------------------------------------------
# Refusals (V109 clause-anchored)
# ---------------------------------------------------------------------------


class LearnedReorderStrippingViolationError(Exception):
    """§11.1 P172 (V109 · second clause).

    Raised when `strip_eligibility_decision` receives an input that is
    not an actual `EligibilityDecision` instance.  Subclasses and duck-
    typed lookalikes are refused so that no path exists by which
    values-that-decided-eligibility can leak across the seam into the
    learned reorder layer's view.
    """


class EligibilityGateSlippageError(Exception):
    """§11.1 P172 (V109 · third clause).

    Raised when the learned reorder layer's output set-membership
    diverges from the deterministic baseline (either a member is
    dropped or an extraneous member is injected).  Ordering may
    differ; membership may not.
    """


# ---------------------------------------------------------------------------
# Carriers (V109 clause-anchored)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PlanInputs:
    """§11.1 P172 (V109 · fourth clause · reproducibility).

    Frozen 3-carrier: every input the planner reads MUST live here so
    that the reproducibility witness's `plan_inputs_sha256` binds to
    the exact input set.

    Fields:
      - `outcome`: the CP-M6-7-1 `TargetOutcome` this plan targets.
      - `register_strata_refs`: tuple of register-defined stratum refs.
      - `seed`: integer seed for any deterministic tie-breaking.
    """

    outcome: TargetOutcome
    register_strata_refs: Tuple[str, ...]
    seed: int


@dataclass(frozen=True)
class EligibilityDecision:
    """§11.1 P172 (V109 · first clause · deterministic-core output).

    Frozen 2-carrier binding `eligible_ids` to `values_that_decided`.
    The strip in the second clause removes the latter before the
    learned reorder layer sees anything.
    """

    eligible_ids: FrozenSet[str]
    values_that_decided: Mapping[str, Any]


@dataclass(frozen=True)
class EligibleStripped:
    """§11.1 P172 (V109 · second clause · strip carrier).

    Frozen 1-carrier: carries ONLY `ids`.  No eligibility-value
    attribute of any name may live on this carrier — that would be a
    V109-forbidden leak of values-that-decided-eligibility into the
    learned reorder layer's view.
    """

    ids: FrozenSet[str]


@dataclass(frozen=True)
class PlanReproducibilityWitness:
    """§11.1 P172 (V109 · fourth clause · reproducibility witness).

    Frozen 2-carrier binding the sha256 of the recorded inputs to the
    sha256 of the plan output.  Same inputs → byte-identical witness;
    distinct inputs → distinct `plan_inputs_sha256`.
    """

    plan_inputs_sha256: str
    plan_output_sha256: str


# ---------------------------------------------------------------------------
# Protocols (V109 clause-anchored · runtime-checkable)
# ---------------------------------------------------------------------------


@runtime_checkable
class PlannerCore(Protocol):
    """§11.1 P172 (V109 · first clause).

    A deterministic core.  Same `plan_inputs` MUST yield the same
    `EligibilityDecision` — that determinism is what the gate in the
    third clause compares against.  Case-agnostic seam; no coupling
    to any specific eligibility scheme.
    """

    def compute_eligibility(
        self, *, plan_inputs: PlanInputs,
    ) -> EligibilityDecision: ...


@runtime_checkable
class LearnedReorderLayer(Protocol):
    """§11.1 P172 (V109 · second clause).

    A learned reorder layer.  Signature accepts ONLY
    `eligible_stripped: EligibleStripped` — no values-that-decided-
    eligibility can cross this signature.  Case-agnostic seam; no
    coupling to any specific model.
    """

    def reorder(
        self, *, eligible_stripped: EligibleStripped,
    ) -> Tuple[str, ...]: ...


# ---------------------------------------------------------------------------
# Strip (V109 · second clause enforcement)
# ---------------------------------------------------------------------------


def strip_eligibility_decision(
    decision: EligibilityDecision,
) -> EligibleStripped:
    """§11.1 P172 (V109 · second clause · strip enforcement).

    Convert an `EligibilityDecision` to an `EligibleStripped` carrier
    that carries ONLY the ids.  Refuses inputs that are not actual
    `EligibilityDecision` instances (subclasses and duck-typed
    lookalikes are refused) so that no path exists by which
    values-that-decided-eligibility can leak across the seam.
    """
    # Strict identity check: refuses subclasses and duck-types.
    if type(decision) is not EligibilityDecision:  # noqa: E721
        raise LearnedReorderStrippingViolationError(
            "strip_eligibility_decision refuses non-EligibilityDecision "
            "inputs to keep values-that-decided-eligibility stripped from "
            "the learned reorder layer's view (V109 · P172 second clause)."
        )
    return EligibleStripped(ids=frozenset(decision.eligible_ids))


# ---------------------------------------------------------------------------
# Reproducibility witness (V109 · fourth clause enforcement)
# ---------------------------------------------------------------------------


def _canonical_plan_inputs_bytes(plan_inputs: PlanInputs) -> bytes:
    """Deterministic byte-canonicalisation of PlanInputs for sha256.

    We do NOT introduce a new pickle / JSON dependency for the
    TargetOutcome — instead we walk the frozen-dataclass structure
    and emit an ASCII-US-separated field digest.  Case-agnostic
    (works for any TargetOutcome shape).
    """
    to = plan_inputs.outcome
    parts = [
        f"task={to.task}",
        f"domain={to.domain}",
        (
            "population="
            + ",".join(sorted(to.population.stratum_refs))
        ),
        (
            "acceptance.has_per_stratum_dimension="
            f"{to.acceptance.has_per_stratum_dimension}"
        ),
        (
            "acceptance.per_stratum_thresholds="
            + "|".join(
                f"{ref}:{acc}:{cov}"
                for ref, acc, cov in sorted(to.acceptance.per_stratum_thresholds)
            )
        ),
        f"gate_policy={to.gate_policy}",
        f"test_set_ref={to.test_set_ref}",
        f"constraints.latency={to.constraints.latency}",
        f"constraints.compute_budget={to.constraints.compute_budget}",
        f"constraints.deployment_target={to.constraints.deployment_target}",
        (
            "register_strata_refs="
            + ",".join(sorted(plan_inputs.register_strata_refs))
        ),
        f"seed={plan_inputs.seed}",
    ]
    return _US.join(parts).encode("utf-8")


def _canonical_plan_output_bytes(ordered: Tuple[str, ...]) -> bytes:
    """Deterministic byte-canonicalisation of the ordered plan output."""
    return _US.join(ordered).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Compose the four V109 clauses
# ---------------------------------------------------------------------------


def run_eligibility_gate(
    *,
    plan_inputs: PlanInputs,
    planner_core: PlannerCore,
    learned_reorder_layer: LearnedReorderLayer,
) -> Tuple[Tuple[str, ...], PlanReproducibilityWitness]:
    """§11.1 P172 (V109) verbatim — compose the four clauses.

    Ordering:
      (a) deterministic core → EligibilityDecision;
      (b) strip → EligibleStripped;
      (c) learned reorder → Tuple[str, ...];
      (d) gate: frozenset(ordered) == decision.eligible_ids or
          EligibilityGateSlippageError;
      (e) reproducibility witness bound to (plan_inputs, plan_output).

    Returns `(ordered_tuple, PlanReproducibilityWitness)`.
    """
    decision = planner_core.compute_eligibility(plan_inputs=plan_inputs)
    stripped = strip_eligibility_decision(decision)
    ordered = learned_reorder_layer.reorder(eligible_stripped=stripped)
    if frozenset(ordered) != decision.eligible_ids:
        raise EligibilityGateSlippageError(
            "gate rejected learned reorder output: membership diverged "
            "from deterministic baseline (V109 · P172 third clause). "
            "Ordering may differ; membership may not."
        )
    witness = PlanReproducibilityWitness(
        plan_inputs_sha256=_sha256_hex(
            _canonical_plan_inputs_bytes(plan_inputs),
        ),
        plan_output_sha256=_sha256_hex(
            _canonical_plan_output_bytes(ordered),
        ),
    )
    return ordered, witness


# ===========================================================================
# CP-M6-7-3 · Part-B · §11.4 P184..P188 · Planner outputs (V115..V118)
# ===========================================================================
#
# Appended as a no-refactor Part-B extension of the CP-M6-7-2 module.  All
# CP-M6-7-2 symbols above remain unchanged.  Part-B lands the four planner-
# output carriers verbatim per §11.4, plus two construction-time refusals:
# `CostQuoteMissingCIError` (V118) and `CurriculumWeightNormalizationError`
# (V116).  V117 is a forward-reference stub: `MilestoneListRef` carries a
# ref string only; the §11.3 milestone-list content contract lands at
# sub-wave 8.  Case-agnostic; no LLM/HTTP/filesystem/network.  Synthetic-
# fixtures-only in tests.  §3.1 P038 tokens-not-waveforms preserved.
# ===========================================================================


# ---------------------------------------------------------------------------
# Refusals (Part-B · V116 + V118)
# ---------------------------------------------------------------------------


class CurriculumWeightNormalizationError(Exception):
    """§11.4 P186 (V116).

    Raised when `CurriculumOrdering.stratum_weight_pairs` weights do
    not sum to 1.0 under floating-point tolerance (1e-9).  The
    curriculum is register-derived weighting; unnormalized weights
    would silently distort the derivation.
    """


class CostQuoteMissingCIError(Exception):
    """§11.4 P188 (V118 · LOAD-BEARING).

    Raised when `CostQuoteWithCI` is constructed with `ci_low is None`
    or `ci_high is None`.  V118 verbatim requires the quote to carry
    "a stated confidence interval" — a point number alone is refused.
    """


# ---------------------------------------------------------------------------
# Coverage report (V115)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PerStratumCoverageEntry:
    """§11.4 P185 (V115) verbatim per-stratum row.

    Frozen 5-carrier:
      - `stratum_ref`: register-defined stratum this row measures.
      - `hours_available_h`: hours available for this stratum.
      - `quality_distribution_summary_ref`: opaque ref to the quality
        distribution summary artifact for this stratum.
      - `gap_hours_h`: hours needed to close the gap for this stratum.
      - `cost_of_closing_gap`: opaque cost carrier for closing this
        stratum's gap.
    """

    stratum_ref: str
    hours_available_h: float
    quality_distribution_summary_ref: str
    gap_hours_h: float
    cost_of_closing_gap: str


@dataclass(frozen=True)
class CoverageReport:
    """§11.4 P185 (V115) verbatim coverage-report carrier.

    Frozen 1-carrier binding a tuple of `PerStratumCoverageEntry`.
    """

    entries: Tuple[PerStratumCoverageEntry, ...]


# ---------------------------------------------------------------------------
# Curriculum ordering (V116)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CurriculumOrdering:
    """§11.4 P186 (V116) verbatim curriculum carrier.

    Frozen 2-carrier:
      - `stratum_weight_pairs`: register-derived (not corpus-derived)
        (stratum_ref, weight) pairs.  Weights MUST sum to 1.0 under
        floating-point tolerance (1e-9); otherwise construction
        refuses with `CurriculumWeightNormalizationError`.
      - `robustness_stratum_ref`: Optional ref to the dedup instance
        condition map entering "as a designated robustness stratum"
        per V116.  May be None when robustness stratum is not yet
        designated.
    """

    stratum_weight_pairs: Tuple[Tuple[str, float], ...]
    robustness_stratum_ref: "str | None"

    def __post_init__(self) -> None:
        total = sum(w for _, w in self.stratum_weight_pairs)
        if abs(total - 1.0) > 1e-9:
            raise CurriculumWeightNormalizationError(
                "CurriculumOrdering weights must sum (be normalized) to "
                f"1.0 under floating-point tolerance; got sum={total!r} "
                "(V116 · P186 register-not-corpus derivation)."
            )


# ---------------------------------------------------------------------------
# Cost quote with confidence interval (V118)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CostQuoteWithCI:
    """§11.4 P188 (V118 · LOAD-BEARING) verbatim cost-quote carrier.

    Frozen 3-carrier:
      - `point_estimate`: point cost estimate.
      - `ci_low`: lower bound of the stated confidence interval.
      - `ci_high`: upper bound of the stated confidence interval.

    Both `ci_low` and `ci_high` are MANDATORY.  V118 verbatim: "Cost
    quote with a stated confidence interval."  A point number alone
    is not a *stated* CI — refuses `CostQuoteMissingCIError` at
    construction when either bound is None.
    """

    point_estimate: float
    ci_low: "float | None"
    ci_high: "float | None"

    def __post_init__(self) -> None:
        if self.ci_low is None:
            raise CostQuoteMissingCIError(
                "CostQuoteWithCI requires a stated confidence interval; "
                "ci_low is None (V118 · P188 load-bearing)."
            )
        if self.ci_high is None:
            raise CostQuoteMissingCIError(
                "CostQuoteWithCI requires a stated confidence interval; "
                "ci_high is None (V118 · P188 load-bearing)."
            )


# ---------------------------------------------------------------------------
# Milestone-list forward-reference stub (V117 · §11.3 stub)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MilestoneListRef:
    """§11.4 P187 (V117) verbatim forward-reference stub.

    Frozen 1-carrier: `ref` — an opaque string pointing to the
    §11.3 milestone-list artifact.  The §11.3 milestone-list content
    contract (V114) lands at sub-wave 8; here we only carry the ref.
    """

    ref: str


# ---------------------------------------------------------------------------
# Planner outputs composition (V115 + V116 + V117 + V118)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PlannerOutputs:
    """§11.4 P185..P188 (V115..V118) composed planner-output carrier.

    Frozen 4-carrier:
      - `coverage_report`: V115.
      - `curriculum`: V116.
      - `milestone_list_ref`: V117 forward-reference stub.
      - `cost_quote`: V118 CI-bearing quote.
    """

    coverage_report: CoverageReport
    curriculum: CurriculumOrdering
    milestone_list_ref: MilestoneListRef
    cost_quote: CostQuoteWithCI

