"""services.compute_seam.reflection_router — FastAPI router for Doc 12 W2.

Owner Order 2026-08-25 · "W2 go" · FL-P2-28.

Endpoints:
  POST /api/compute/reflection   → compute the projection envelope
  POST /api/compute/commit       → acknowledge + commit (server-side gate)

Access control: the pod-shell IP-allowlist middleware gates every route
at the outer boundary; this router adds no per-route auth.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from services.compute_seam.reflection import (
    ReflectionRefusal,
    acknowledge_and_commit,
    compute_projection,
)


router = APIRouter()


class BudgetCeiling(BaseModel):
    model_config = ConfigDict(extra="ignore")
    amount: float = Field(ge=0.0)
    currency: str = Field(default="USD", min_length=1, max_length=8)


class ScopeCeiling(BaseModel):
    model_config = ConfigDict(extra="ignore")
    rows_ceiling: Optional[int] = Field(default=None, ge=0)
    gpu_hours_ceiling: Optional[float] = Field(default=None, ge=0.0)
    duration_seconds_ceiling: Optional[float] = Field(default=None, ge=0.0)


class ProposedAction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    kind: str = Field(..., min_length=1, max_length=32)
    scope_ref: str = Field(..., min_length=1, max_length=512)
    scope_ceiling: Optional[ScopeCeiling] = None
    budget_ceiling: Optional[BudgetCeiling] = None
    commissioner: Optional[str] = None
    lawful_basis: Optional[str] = None


class ReflectionRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    proposed_action: ProposedAction


class CommitRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    reflection_id: Optional[str] = None
    actor: str = Field(..., min_length=1, max_length=128)
    proposed_action: ProposedAction


@router.post("/api/compute/reflection")
async def post_compute_reflection(body: ReflectionRequest) -> Dict[str, Any]:
    envelope = compute_projection(proposed_action=body.proposed_action.model_dump())
    return envelope


@router.post("/api/compute/commit")
async def post_compute_commit(body: CommitRequest) -> Dict[str, Any]:
    try:
        run_row = acknowledge_and_commit(
            reflection_id=body.reflection_id,
            actor=body.actor,
            proposed_action=body.proposed_action.model_dump(),
        )
    except ReflectionRefusal as exc:
        # 422 — the payload is well-formed but the gate refuses. Plain
        # sentence carries the refusal reason (Doc 16 refusal grammar).
        raise HTTPException(status_code=422, detail=str(exc))
    return run_row
