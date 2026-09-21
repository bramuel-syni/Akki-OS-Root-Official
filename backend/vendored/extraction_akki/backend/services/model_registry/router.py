"""services.model_registry.router — W7 CP7 · HTTP surface.

Endpoints:
  GET /api/model_registry/version         — current v(N), model count
  GET /api/model_registry/models          — full inventory (facts)
  GET /api/model_registry/models/{id}     — one entry (or 404 · honest gap)
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from services.model_registry.registry import (
    HONEST_REGISTRY_LOCATION,
    current_registry_version,
    load_registry,
)


router = APIRouter()


@router.get("/api/model_registry/version")
async def get_version() -> Dict[str, Any]:
    n, models = current_registry_version()
    return {
        "version_n": n,
        "version_str": f"v{n}",
        "model_count": len(models),
        "location_note": HONEST_REGISTRY_LOCATION,
    }


@router.get("/api/model_registry/models")
async def list_models() -> Dict[str, Any]:
    models = load_registry()
    # Partition by role for surface convenience.
    purchased = [
        m for m in models.values()
        if m.get("provider") == "emergent"
        or "purchased" in (m.get("role", "") or "")
    ]
    trained = [
        m for m in models.values()
        if m.get("role") == "trained_adapter"
    ]
    other = [
        m for m in models.values()
        if m not in purchased and m not in trained
    ]
    return {
        "total": len(models),
        "purchased_llms": purchased,
        "trained_adapters": trained,
        "other": other,
    }


@router.get("/api/model_registry/models/{model_id}")
async def get_model(model_id: str) -> Dict[str, Any]:
    entry = load_registry().get(model_id)
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"{model_id!r} not on record in services/model_registry. "
                f"Honest gap — no fabrication."
            ),
        )
    return entry
