"""services.model_recheck.router — W7 CP7 · HTTP surface.

Endpoints:
  GET /api/model_recheck/status/{model_id}    — one model's re-check state
  GET /api/model_recheck/all                  — every registered model's state
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from services.model_recheck.status import CA1_011_WATCH_SEAM, status_for
from services.model_registry.registry import load_registry


router = APIRouter()


@router.get("/api/model_recheck/status/{model_id}")
async def get_status(model_id: str) -> Dict[str, Any]:
    return status_for(model_id)


@router.get("/api/model_recheck/all")
async def list_all() -> Dict[str, Any]:
    payloads: List[Dict[str, Any]] = []
    for mid in load_registry().keys():
        payloads.append(status_for(mid))
    return {
        "count": len(payloads),
        "ca1_011_watch_seam": CA1_011_WATCH_SEAM,
        "statuses": payloads,
    }
