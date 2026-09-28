"""services.northena.router — ThinkLab HTTP surface (Doc 05 · W4).

Endpoints:
  POST /api/thinklab/admit         — Doc 05 §B5.3 admission path.
  POST /api/thinklab/gate          — Doc 05 §A5.4 strict set-membership.
  POST /api/thinklab/converge      — Doc 05 §A5.5 threshold check.
  GET  /api/thinklab/runs          — list open runs (identity summaries).
  GET  /api/thinklab/runs/{run_id} — ledger rows for a run (by identity).
  GET  /api/thinklab/config        — v7 fabric constants for the surface.

REFERENCE-NOT-COPY: reads return row identities + summary shape; ledger
row content resolves through the read path (list_rows_by_run).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from services.northena import admit as northena_admit
from services.northena import converge as northena_converge
from services.northena import gate as northena_gate
from services.northena import ledger as northena_ledger
from services.solva import reasoning as solva_reasoning


router = APIRouter()


# ---------------------------------------------------------------------------
# v7 fabric constants — extracted verbatim from prototype.html.
# ---------------------------------------------------------------------------

_TL_MODES = [
    {"key": "clarity", "num": "01", "title": "Seek clarity",
     "objective": "Untangle a messy situation into the two or three questions that actually matter.",
     "duration": "15–20 min"},
    {"key": "strategy", "num": "02", "title": "Develop strategy",
     "objective": "Build a defensible position — options, trade-offs, and the recommendation you would sign.",
     "duration": "25–40 min"},
    {"key": "hypothesis", "num": "03", "title": "Simulate a hypothesis",
     "objective": "Stress-test a claim before management presents it. What would have to be true?",
     "duration": "20–30 min"},
    {"key": "perspective", "num": "04", "title": "Get perspectives",
     "objective": "The same problem through the eyes of the audit chair, the CFO, and the sceptical investor.",
     "duration": "15–25 min"},
]

_TL_STAGE_LABELS = ["Frame", "Name", "Challenge", "Weigh", "Lock-in"]

_TL_OUTPUTS = [
    "A one-page Brief or PDF, exportable in one click.",
    "A decision trail you can table at the next meeting.",
    "Optional handoff to Task Manager as tracked work.",
]

_LANDING_TIPS = {
    "clarity":     ["Say what's unclear. Akki surfaces what's already known before you decide."],
    "strategy":    ["Name the decision ahead of you. Four stages carry it from surface to lock-in."],
    "hypothesis":  ["State the hypothesis plainly. Akki stress-tests it against the estate."],
    "perspective": ["Ask for a vantage point other than your own — grounded, not invented."],
}


class Budget(BaseModel):
    model_config = ConfigDict(extra="ignore")
    gpu_hours: Optional[float] = Field(default=None, ge=0.0)
    amount: Optional[float] = Field(default=0.0, ge=0.0)
    currency: Optional[str] = Field(default="USD", min_length=1, max_length=8)


class AdmitRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    mode: str = Field(..., min_length=1, max_length=32,
                      description="One of clarity | strategy | hypothesis | perspective.")
    artifact_id: str = Field(..., min_length=1, max_length=128,
                             description="Client-supplied identity for the objective.")
    artifact_version: str = Field(default="1", min_length=1, max_length=32)
    lawful_basis: str = Field(default="",
                              description="Declared lawful basis — empty refuses at Admit.")
    scope: List[str] = Field(default_factory=list)
    done_condition: Optional[str] = None
    budget: Optional[Budget] = None
    commissioner: Optional[str] = None
    # Direction capture — the operator's stated question / problem / hypothesis.
    direction_statement: str = Field(default="", max_length=4000)


class GateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    run_id: str
    trace_id: str
    sub_objective: str
    artifact_ref: Dict[str, Any]
    lawful_basis_ref: str
    scope: List[str]
    warm_index: Optional[List[str]] = None


class ConvergeRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    run_id: str
    trace_id: str
    artifact_ref: Dict[str, Any]
    lawful_basis_ref: str
    done_condition_met: bool
    budget_exhausted: bool


class ReasonRequest(BaseModel):
    """W5 CP3 · Solva reasoning entry.

    Runs frame_audit → candidate_generation → synthesis through the LLM
    chokepoint (purpose: solva.frame_audit / .candidate_generation /
    .synthesis). Refusals surface VERBATIM per A8-Q3.
    """
    model_config = ConfigDict(extra="ignore")
    direction_statement: str = Field(..., min_length=1, max_length=4000)
    actor: str = Field(default="operator@estate", max_length=200)
    situation_class: str = Field(default="unknown", max_length=64)
    model: str = Field(default="gpt-5-mini", max_length=64)
    provider: str = Field(default="emergent", max_length=32)


@router.post("/api/thinklab/admit")
async def post_thinklab_admit(body: AdmitRequest) -> Dict[str, Any]:
    """§B5.3 external admission path. Refusals return 200 with the
    Doc 16 refusal envelope; the ledger row is written either way."""
    raw_intent: Dict[str, Any] = {
        "artifact_type": "thinklab_objective",
        "artifact_id": body.artifact_id,
        "artifact_version": body.artifact_version,
        "lawful_basis": body.lawful_basis,
        "scope": body.scope,
        "mode": body.mode,
    }
    if body.done_condition:
        raw_intent["done_condition"] = body.done_condition
    if body.budget:
        raw_intent["budget"] = body.budget.model_dump()
    if body.commissioner:
        raw_intent["commissioner"] = body.commissioner
    if body.direction_statement:
        raw_intent["direction_statement"] = body.direction_statement
    return await northena_admit.compile_and_freeze(raw_intent=raw_intent)


@router.post("/api/thinklab/gate")
async def post_thinklab_gate(body: GateRequest) -> Dict[str, Any]:
    return await northena_gate.route(
        run_id=body.run_id, trace_id=body.trace_id,
        sub_objective=body.sub_objective,
        artifact_ref=body.artifact_ref,
        lawful_basis_ref=body.lawful_basis_ref,
        scope=body.scope, warm_index=body.warm_index,
    )


@router.post("/api/thinklab/converge")
async def post_thinklab_converge(body: ConvergeRequest) -> Dict[str, Any]:
    return await northena_converge.check(
        run_id=body.run_id, trace_id=body.trace_id,
        artifact_ref=body.artifact_ref,
        lawful_basis_ref=body.lawful_basis_ref,
        done_condition_met=body.done_condition_met,
        budget_exhausted=body.budget_exhausted,
    )


@router.get("/api/thinklab/runs")
async def get_thinklab_runs(limit: int = 50) -> Dict[str, Any]:
    summaries = await northena_ledger.list_open_runs(limit=limit)
    return {"count": len(summaries), "runs": summaries}


@router.get("/api/thinklab/runs/{run_id}")
async def get_thinklab_run(run_id: str) -> Dict[str, Any]:
    rows = await northena_ledger.list_rows_by_run(run_id)
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"no ledger rows on record for run_id {run_id!r}",
        )
    return {"run_id": run_id, "rows": rows}


@router.get("/api/thinklab/config")
async def get_thinklab_config() -> Dict[str, Any]:
    """v7 fabric constants — the surface reads these to render itself."""
    return {
        "modes": _TL_MODES,
        "stage_labels": _TL_STAGE_LABELS,
        "outputs": _TL_OUTPUTS,
        "landing_tips": _LANDING_TIPS,
        "reasoning_dormant_state": (
            "Solva reasoning is in force. Direction capture routes through "
            "frame_audit → candidate_generation → synthesis; every stage "
            "carries a receipt identity and the model that answered."
        ),
    }


@router.post("/api/thinklab/reason")
async def post_thinklab_reason(body: ReasonRequest) -> Dict[str, Any]:
    """W5 CP3 · Solva reasoning pipeline.

    Owner sharpening §4 · A8-Q3 honesty:
      - No smoothed reasoning: a stage's `refused=True` + verbatim
        `refusal_reason` render on the surface exactly as returned.
      - Model provenance: every stage carries `model_id` + `provider`
        drawn from its crossing receipt.
    """
    from dataclasses import asdict
    run = await solva_reasoning.run_full_pipeline(
        direction_statement=body.direction_statement,
        actor=body.actor,
        situation_class=body.situation_class,
        model=body.model,
        provider=body.provider,
    )
    return {
        "run_id": run.run_id,
        "at_iso": run.at_iso,
        "actor": run.actor,
        "direction_statement": run.direction_statement,
        "receipt_ids": run.receipt_ids,
        "frame_audit": asdict(run.frame_audit),
        "candidate_generation": asdict(run.candidate_generation),
        "synthesis": asdict(run.synthesis),
    }
