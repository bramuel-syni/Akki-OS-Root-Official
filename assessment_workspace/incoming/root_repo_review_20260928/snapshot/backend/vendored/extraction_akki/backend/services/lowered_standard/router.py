"""services.lowered_standard.router — CA1-010 endpoints."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from services.lowered_standard import sessions as _s


router = APIRouter()


class OpenRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    actor: str = Field(..., min_length=1, max_length=200)
    reason: str = Field(..., min_length=1, max_length=800)
    purpose_scope: List[str] = Field(default_factory=list)
    expires_in_seconds: int = Field(default=1800, ge=1, le=86400)


class CloseRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    session_id: str = Field(..., min_length=1, max_length=64)
    actor: str = Field(..., min_length=1, max_length=200)


@router.post("/api/lowered_standard/open")
async def open_endpoint(body: OpenRequest) -> Dict[str, Any]:
    try:
        sess = _s.open_session(
            actor=body.actor,
            reason=body.reason,
            purpose_scope=body.purpose_scope,
            expires_in_seconds=body.expires_in_seconds,
        )
    except ValueError as exc:
        # Refusal grammar surfaced verbatim.
        raise HTTPException(status_code=422, detail=str(exc))
    return asdict(sess)


@router.post("/api/lowered_standard/close")
async def close_endpoint(body: CloseRequest) -> Dict[str, Any]:
    try:
        sess = _s.close_session(session_id=body.session_id, actor=body.actor)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return asdict(sess)


@router.get("/api/lowered_standard/active")
async def active_endpoint() -> Dict[str, Any]:
    return {"sessions": [asdict(s) for s in _s.active_sessions()]}


@router.get("/api/lowered_standard/history")
async def history_endpoint(limit: int = Query(50, ge=1, le=500)) -> Dict[str, Any]:
    return {"sessions": [asdict(s) for s in _s.all_sessions()[:limit]]}
