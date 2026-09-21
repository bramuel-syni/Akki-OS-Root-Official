"""services.cost_ledger.router — CA1-008 endpoints.

GET /api/cost_ledger/entries?since_iso=&limit=&kind=  · ledger rows.
GET /api/cost_ledger/rates                             · rates on record.
GET /api/cost_ledger/summary?since_iso=&kind=          · totals + levers.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Query

from services.cost_ledger import ledger as _ledger
from services.cost_ledger import rates as _rates


router = APIRouter()


@router.get("/api/cost_ledger/rates")
async def get_rates() -> Dict[str, Any]:
    """Owner-supplied rates on record. Empty lists mean honest absence."""
    data = _rates.load_rates()
    return {
        "models": data.get("models", []),
        "gpu_hours": data.get("gpu_hours", []),
        "honest_gap_note": _rates.HONEST_GAP_SENTENCE if not data.get("models") else "",
    }


@router.get("/api/cost_ledger/entries")
async def get_entries(
    since_iso: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    kind: Optional[str] = None,
) -> Dict[str, Any]:
    entries = _ledger.build_entries(since_iso=since_iso, limit=limit, kind=kind)
    return {
        "count": len(entries),
        "entries": [asdict(e) for e in entries],
        "lever_order": _ledger.LEVER_ORDER,
    }


@router.get("/api/cost_ledger/summary")
async def get_summary(
    since_iso: Optional[str] = None,
    kind: Optional[str] = None,
) -> Dict[str, Any]:
    entries = _ledger.build_entries(since_iso=since_iso, kind=kind)
    return _ledger.summarise(entries)
