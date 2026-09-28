"""services.training.router · /api/training/state (W11 CP3).

Read-only rollup of the Training plane surface state — Demand Tables +
Capacity Ledger + Test-set Seals · every artifact read from disk on
each call (REFERENCE-NOT-COPY · Design Law A8). Never returns AWS
credentials, cluster secrets, or database passwords — those never
touch the underlying store modules.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from services.training import capacity_ledger, demand_table, state as training_state
from services.training import test_set_seal
from services.training import optimizer_harness, recipe_seat
from contracts.optimizer_comparison_v0 import ArmMeasurements as _ArmMeasurements
from contracts.training_params_v0 import BudgetCap as _BudgetCap, TrainingParamsV0 as _TrainingParamsV0
from fastapi import HTTPException


router = APIRouter()


# ---------------------------------------------------------------------------
# GET /api/training/state · rollup for the /training React surface.
# ---------------------------------------------------------------------------

@router.get("/api/training/state")
async def get_training_state() -> Dict[str, Any]:
    """Return the current on-disk state of the training plane."""
    body = training_state.rollup()
    body["reference_note"] = (
        "REFERENCE-NOT-COPY · Design Law A8 · every demand table, "
        "capacity ledger row, and test-set seal is a file on disk. "
        "This surface reads those files each call; it does not cache. "
        "AWS credentials, cluster secrets, and database passwords are "
        "never written by the underlying modules and never appear here."
    )
    return body


# ---------------------------------------------------------------------------
# POST /api/training/demand-table/compile · deterministic compile.
# ---------------------------------------------------------------------------

class SchemeIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    named_failure: str = Field(min_length=1)


class StratumIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stratum_id: str = Field(min_length=1)
    B: int
    I: int


class DemandTableCompileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objective_id: str = Field(min_length=1)
    schemes: List[SchemeIn]
    per_stratum: List[StratumIn]


@router.post("/api/training/demand-table/compile")
async def post_compile_demand_table(payload: DemandTableCompileRequest) -> Dict[str, Any]:
    """§4.1 admissibility + §3.5 derivation · stamps the table to disk."""
    try:
        table = demand_table.compile(
            objective_id=payload.objective_id,
            schemes=[demand_table.Scheme(id=s.id, named_failure=s.named_failure)
                     for s in payload.schemes],
            per_stratum=[demand_table.StratumDemand(stratum_id=r.stratum_id, B=r.B, I=r.I)
                         for r in payload.per_stratum],
        )
    except (demand_table.UnnamedFailureError, ValueError) as e:
        return {"ok": False, "refusal_reason": str(e)}
    demand_table.stamp(table)
    return {
        "ok": True,
        "objective_id": table.objective_id,
        "compiled_at": table.compiled_at,
        "schemes_count": len(table.schemes),
        "strata_count": len(table.per_stratum),
        "per_stratum": [
            {"stratum_id": r.stratum_id, "B": r.B, "I": r.I, "E": r.E}
            for r in table.per_stratum
        ],
    }


# ---------------------------------------------------------------------------
# POST /api/training/test-set-seal · live-verify-first · honest hold.
# ---------------------------------------------------------------------------

class TestSetSealRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objective_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    target_table: str = Field(min_length=1)
    strata: List[str]
    sample_size: int = Field(gt=0, le=100_000)


@router.post("/api/training/test-set-seal")
async def post_test_set_seal(payload: TestSetSealRequest) -> Dict[str, Any]:
    """A17.11 · test-set-precedes-training. Refuses honestly on stale /
    link-broken / no-record verification state."""
    try:
        seal = test_set_seal.seal(
            objective_id=payload.objective_id,
            source_id=payload.source_id,
            target_table=payload.target_table,
            strata=list(payload.strata),
            sample_size=payload.sample_size,
        )
    except test_set_seal.SealRefused as e:
        return {"ok": False, "refusal_reason": str(e)}
    return {
        "ok": True,
        "seal_id": seal.seal_id,
        "manifest_sha256": seal.manifest_sha256,
        "sealed_at": seal.sealed_at,
        "rds_link_verified_at": seal.rds_link_verified_at,
    }


# ---------------------------------------------------------------------------
# GET /api/training/capacity · read-only ledger view.
# ---------------------------------------------------------------------------

@router.get("/api/training/capacity")
async def get_capacity_ledger() -> Dict[str, Any]:
    """Empty at ship. Grows as calibration probes write rows."""
    rows = capacity_ledger.read_all()
    return {
        "count": len(rows),
        "rows": [
            {
                "scheme_id": r.scheme_id,
                "stratum": r.stratum,
                "level": r.level,
                "state": r.state,
                "provenance": r.provenance,
                "marginal_gain": r.marginal_gain,
                "written_at": r.written_at,
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# W11 B · CP5 · Doc 17 §A17.3-A17.6 · Recipe seat + optimizer harness.
# ---------------------------------------------------------------------------

@router.get("/api/training/recipes")
async def get_recipes() -> Dict[str, Any]:
    """A17.3 · list every ratified recipe (training_params@v0/*).

    Empty at ship — no default recipe exists until the first training
    run fills it through the §3 optimizer-selection protocol
    (A17.5-A17.6). Doc 17 verbatim: 'Nothing may pre-populate
    training_params@v0 by convention, template, or engineer judgement.'
    """
    rows = recipe_seat.read_all()
    return {
        "ship_state": "empty" if not rows else "populated",
        "count": len(rows),
        "recipes": [r.model_dump() for r in rows],
        "empty_seat_note": (
            "Doc 17 §A17.5-A17.6 · no default recipe exists until the "
            "first training run fills it. The first value ever written "
            "carries the measured comparison that produced it."
        ),
    }


@router.get("/api/training/recipes/{recipe_version:path}")
async def get_recipe_by_version(recipe_version: str) -> Dict[str, Any]:
    """A17.4 · 'Revision is DEFAULT-class, but never unevidenced.'
    404 with structured refusal envelope when the version is unknown."""
    r = recipe_seat.get_by_version(recipe_version)
    if r is None:
        raise HTTPException(
            status_code=404,
            detail={
                "reason": "recipe_not_found",
                "recipe_version": recipe_version,
                "empty_seat_note": (
                    "Doc 17 empty-seat: 'Nothing may pre-populate "
                    "training_params@v0 by convention, template, or "
                    "engineer judgement.'"
                ),
            },
        )
    return r.model_dump()


@router.get("/api/training/optimizer-comparisons")
async def get_optimizer_comparisons() -> Dict[str, Any]:
    """A17.5 · list every optimizer comparison shell on record.
    Empty at ship — the protocol executes at the first adapter
    training on real material."""
    rows = optimizer_harness.read_all()
    return {
        "ship_state": "empty" if not rows else "populated",
        "count": len(rows),
        "comparisons": [r.model_dump() for r in rows],
    }


class OptimizerComparisonOpenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    comparison_id: str = Field(min_length=1)
    base_model_id: str = Field(min_length=1)
    evaluation_sets: List[str] = Field(min_length=1)
    budget_cap_wallclock_seconds: int = Field(gt=0)
    budget_cap_gpu_hours: float = Field(ge=0.0)
    smallest_stratum: str = Field(min_length=1)
    opened_at: str = Field(min_length=1)


@router.post("/api/training/optimizer-comparisons", status_code=201)
async def post_open_comparison(payload: OptimizerComparisonOpenRequest) -> Dict[str, Any]:
    """A17.5 · open a comparison shell with identical conditions frozen."""
    try:
        c = optimizer_harness.open_comparison(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail={
                "plain": str(e),
                "field": "comparison_id",
                "remedy": (
                    "Mint a fresh comparison_id for the new probe and retry. "
                    "The identical protocol governs every future recipe-"
                    "component candidate (A17.6)."
                ),
            },
        )
    return c.model_dump()


class ArmMeasurementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    moac_m_a_improvement: float
    moac_m_b_regression: float
    wallclock_seconds_to_convergence: int = Field(ge=0)
    gpu_hours_to_convergence: float = Field(ge=0.0)
    moac_m_e_calibration: float
    evaluation_samples_uncurated: bool


@router.post(
    "/api/training/optimizer-comparisons/{comparison_id:path}/arms/{arm}/measurements"
)
async def post_record_arm_measurements(
    comparison_id: str, arm: str, payload: ArmMeasurementRequest,
) -> Dict[str, Any]:
    """A17.5 · record four measured outputs on one arm. Harness auto-
    flips 'ineligible' if M-a or M-b quality parity fails."""
    try:
        measurements = _ArmMeasurements.model_validate(payload.model_dump())
        updated = optimizer_harness.record_arm_measurements(
            comparison_id, arm, measurements,
        )
    except optimizer_harness.ComparisonNotFound:
        raise HTTPException(
            status_code=404,
            detail={"reason": "comparison_not_found", "comparison_id": comparison_id},
        )
    except optimizer_harness.UncuratedFlagMissing as e:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": str(e),
                "field": "evaluation_samples_uncurated",
                "remedy": (
                    "D-7 doctrine: 'evaluation inputs may be engineered; "
                    "evaluation samples may not.' Set the flag to true and "
                    "resubmit."
                ),
            },
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={"plain": str(e), "field": "arm",
                    "remedy": "Set arm to 'baseline' or 'muon'."},
        )
    return updated.model_dump()


class OwnerVerdictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict: str
    ratified_at: str = Field(min_length=1)
    verdict_note: str = ""


@router.post("/api/training/optimizer-comparisons/{comparison_id:path}/verdict")
async def post_rule_on_comparison(
    comparison_id: str, payload: OwnerVerdictRequest,
) -> Dict[str, Any]:
    """A17.5 · Owner ruling adopts or rejects. 'no adoption threshold
    fixed in advance of the evidence' — measurements decide the ruling,
    not the harness."""
    try:
        updated = optimizer_harness.rule_on_comparison(
            comparison_id=comparison_id,
            verdict=payload.verdict,
            ratified_at=payload.ratified_at,
            verdict_note=payload.verdict_note,
        )
    except optimizer_harness.ComparisonNotFound:
        raise HTTPException(
            status_code=404,
            detail={"reason": "comparison_not_found",
                    "comparison_id": comparison_id},
        )
    except optimizer_harness.VerdictRefused as e:
        raise HTTPException(
            status_code=409,
            detail={
                "plain": str(e),
                "field": "verdict",
                "remedy": (
                    "A17.5 quality-parity gate: 'compute-to-convergence is "
                    "reported, never gating — a faster optimizer that "
                    "regresses quality is not eligible regardless of its "
                    "speed.' Open a fresh comparison with a different "
                    "candidate."
                ),
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"plain": str(e)})
    return updated.model_dump()


# ---------------------------------------------------------------------------
# W11 B · CP8 · Doc 17 lines 15, 55, 88-101 · Trainer runner HTTP surface.
# ---------------------------------------------------------------------------

from services.training_runner import runner as _trainer_runner  # noqa: E402


@router.get("/api/training-runs/state")
async def get_training_runs_state() -> Dict[str, Any]:
    """Trainer runner rollup · empty at CP8 ship (mock seam · no
    governed run has fired yet)."""
    return _trainer_runner.state_rollup()


class TrainingMaterialAdmitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    admit_id: str = Field(min_length=1)
    training_run_id: str = Field(min_length=1)
    unit_manifest_ref: str = Field(min_length=1)
    unit_count: int = Field(ge=1)
    deduped: bool
    vad_cleaned: bool
    qualified: bool
    extraction_pipeline_ref: str = Field(min_length=1)


@router.post("/api/training-runs/admit", status_code=201)
async def post_admit_material(payload: TrainingMaterialAdmitRequest) -> Dict[str, Any]:
    """Doc 17 line 15 · admit training material through the three-gate
    contract (de-duped + VAD-cleaned + qualified · pipeline citation)."""
    try:
        admit = _trainer_runner.admit_material(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "plain": str(e),
                "field": "qualifications",
                "remedy": (
                    "Doc 17 line 15 verbatim requires all three bits True "
                    "(deduped, vad_cleaned, qualified) plus a non-empty "
                    "extraction_pipeline_ref."
                ),
            },
        )
    return admit.model_dump()


class TrainingRunOpenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str = Field(min_length=1)
    recipe_version: str = Field(min_length=1)
    base_model_id: str = Field(min_length=1)
    adapter_kind: str
    material_admit_ref: str = Field(min_length=1)


@router.post("/api/training-runs/open", status_code=201)
async def post_open_run(payload: TrainingRunOpenRequest) -> Dict[str, Any]:
    """Doc 17 line 15 · open a run. LoRA/PEFT grammar closed on adapter_kind."""
    try:
        run = _trainer_runner.open_run(**payload.model_dump())
    except _trainer_runner.RecipeSeatEmpty as e:
        raise HTTPException(status_code=409,
                            detail={"plain": str(e), "field": "recipe_version",
                                    "remedy": "Adopt a recipe via CP5 optimizer harness first."})
    except _trainer_runner.RecipeNotAdopted as e:
        raise HTTPException(status_code=409,
                            detail={"plain": str(e), "field": "recipe_version",
                                    "remedy": "Use a recipe_version that appears in /api/training/recipes."})
    except _trainer_runner.MaterialAdmitNotFound as e:
        raise HTTPException(status_code=404,
                            detail={"plain": str(e), "field": "material_admit_ref",
                                    "remedy": "Call POST /api/training-runs/admit first."})
    except ValueError as e:
        raise HTTPException(status_code=422,
                            detail={"plain": str(e), "field": "body"})
    return run.model_dump()


@router.post("/api/training-runs/{run_id:path}/execute")
async def post_execute_run(run_id: str) -> Dict[str, Any]:
    """Fire the trainer through the SSH seam (mock at CP8 landing)."""
    try:
        updated = _trainer_runner.execute_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail={"reason": "run_not_found", "run_id": run_id})
    return updated.model_dump()


@router.post("/api/training-runs/{run_id:path}/emit-moac")
async def post_emit_moac(run_id: str) -> Dict[str, Any]:
    """Doc 17 line 90 · six-check MOAC card emission · Critic Seam routing."""
    try:
        result = _trainer_runner.emit_moac_for_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail={"reason": "run_not_found", "run_id": run_id})
    return result


class CloseRunRequest(BaseModel):
    """W11 C · CP-C2 warn-followup · Doc 14 §33 citation invariant.

    A close request MUST carry the fully-formed moac_card so the
    whitepaper drafter cites real record content. A moac_card missing
    verdict_summary / moac_card_id / accept_for_service used to be
    silently absorbed and the whitepaper_ref surfaced a
    'whitepaper_draft_error' placeholder - refused at the boundary
    from CP-C5 onward."""

    model_config = ConfigDict(extra="forbid")

    moac_card_id: str = Field(min_length=1)
    verdict_summary: str = Field(min_length=1)
    accept_for_service: bool
    run_id: Optional[str] = None
    criteria: Optional[list] = None
    passed_count: Optional[int] = None
    total_criteria: Optional[int] = None
    reference_verbatim: Optional[str] = None


@router.post("/api/training-runs/{run_id:path}/close")
async def post_close_run(run_id: str, moac_card: CloseRunRequest) -> Dict[str, Any]:
    """Owner directive · cost-ledger metering + whitepaper on close.
    Verdict flips to closed_adopted iff accept_for_service else
    closed_rejected.

    Doc 14 §33 citation invariant: moac_card MUST carry the citation
    fields (moac_card_id, verdict_summary, accept_for_service) so the
    whitepaper drafted at close cites the record it rests on."""
    try:
        updated = _trainer_runner.close_run(run_id, moac_card.model_dump(exclude_none=True))
    except KeyError:
        raise HTTPException(status_code=404,
                            detail={"reason": "run_not_found", "run_id": run_id})
    return updated.model_dump()
