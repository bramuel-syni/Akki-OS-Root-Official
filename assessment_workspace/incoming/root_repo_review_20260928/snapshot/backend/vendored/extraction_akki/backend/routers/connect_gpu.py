"""connect_gpu.py — /api/connect/gpu FastAPI router (WS-BUILD-CONNECT-GPU).

Owner ruling 2026-08-14 (DECISIONS.md · WS-BUILD-CONNECT-GPU):
  This is the product surface for VM credential delivery. Behind spine auth
  (mounted by /app/backend/server.py). Rate-limit + CSRF applied at the
  spine-level middleware; this router just accepts the payload and delegates.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from services.connect import gpu_submit


router = APIRouter()


class GpuSubmitPayload(BaseModel):
    host_name: str = Field(..., min_length=1, max_length=128)
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=1, max_length=256)  # masked, never echoed.
    public_ip: str = Field(..., min_length=1, max_length=64)
    private_ip: Optional[str] = Field(None, max_length=64)
    os: Optional[str] = Field(None, max_length=64)
    deploy_date: Optional[str] = Field(None, max_length=32)


@router.post("/api/connect/gpu")
async def post_connect_gpu(payload: GpuSubmitPayload, request: Request) -> dict:
    """Submit VM credentials → declaration → hardening → acceptance → after-state.

    Payload is passed to services.connect.gpu_submit.submit() which orchestrates
    the seven ordered stages per the owner ruling. Password is env-grade only
    inside the submit call; never returned in the response, never logged, never
    persisted after this call.
    """
    body = payload.model_dump()
    # Never log body — password is inside it. Router does not print / log.
    try:
        result = gpu_submit.submit(body, actor=_actor(request), drill_mode_ok=False)
    except gpu_submit.SubmitError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        # Never surface the payload in error messages.
        raise HTTPException(status_code=500, detail=f"submit failed: {type(exc).__name__}")
    return {
        "at": datetime.now(timezone.utc).isoformat(),
        **result,
    }


def _actor(request: Request) -> str:
    """Actor id for ledger row — spine auth attaches an actor to request.state.

    In this router we accept 'owner' as the default when the spine has not
    populated an actor (drill only — spine auth gate rejects unauthed callers
    before we get here).
    """
    return getattr(request.state, "actor", "owner")
