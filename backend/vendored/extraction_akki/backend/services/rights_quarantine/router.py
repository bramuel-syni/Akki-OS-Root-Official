"""services.rights_quarantine.router — Doc14-020 quarantine surface.

Wave E · CP-E4 · four wire paths per owner ruling:
  GET  /api/rights_quarantine                           · list queue
  GET  /api/rights_quarantine/{admit_id}                · record detail
  POST /api/rights_quarantine/{admit_id}/release        · rights resolved OK
  POST /api/rights_quarantine/{admit_id}/refuse         · rights declined
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from services.rights_quarantine import (
    get_quarantine,
    list_quarantine,
    resolve_quarantine,
)
from services.response_sanitizer import sanitize  # Wave E CP-E7


router = APIRouter()


@router.get("/api/rights_quarantine")
def list_rights_quarantine() -> Dict[str, Any]:
    """Doc14-020 · list quarantined admits (rights-unclear material
    awaiting review)."""
    rows = [sanitize(r.model_dump()) for r in list_quarantine()]
    return {
        "rights_quarantine": rows,
        "count": len(rows),
        "pending_review_count": sum(1 for r in rows if r.get("resolution") is None),
    }


@router.get("/api/rights_quarantine/{admit_id}")
def get_rights_quarantine(admit_id: str) -> Dict[str, Any]:
    r = get_quarantine(admit_id)
    if r is None:
        raise HTTPException(
            status_code=404,
            detail={"plain": f"quarantine record {admit_id!r} not found",
                     "field": "admit_id",
                     "remedy": "list /api/rights_quarantine to see available records"},
        )
    return sanitize(r.model_dump())


class _ResolveInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resolution_summary: str = Field(..., min_length=1)


@router.post("/api/rights_quarantine/{admit_id}/release", status_code=200)
def release_rights_quarantine(admit_id: str, payload: _ResolveInput) -> Dict[str, Any]:
    """Terminal release — rights resolved OK. Caller may re-run
    admit_material() with rights_state='clear' after this."""
    try:
        r = resolve_quarantine(admit_id, "released", payload.resolution_summary)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        if "already resolved" in msg:
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    return sanitize(r.model_dump())


@router.post("/api/rights_quarantine/{admit_id}/refuse", status_code=200)
def refuse_rights_quarantine(admit_id: str, payload: _ResolveInput) -> Dict[str, Any]:
    """Terminal refuse — rights declined; no admit, ever."""
    try:
        r = resolve_quarantine(admit_id, "refused", payload.resolution_summary)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=404, detail=str(e))
        if "already resolved" in msg:
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    return sanitize(r.model_dump())
