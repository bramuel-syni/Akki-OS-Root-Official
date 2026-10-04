"""services.cost_ledger.router — CA1-008 endpoints.

GET  /api/cost_ledger/entries?since_iso=&limit=&kind=  · ledger rows.
GET  /api/cost_ledger/rates                             · rates on record (models · gpu_hours · training · caas).
GET  /api/cost_ledger/summary?since_iso=&kind=          · totals + levers.
POST /api/cost_ledger/rates/{lane}                      · owner/operator authors ONE governed rate row (Mα MA-30).
DELETE /api/cost_ledger/rates/{lane}/{ident}            · withdraws a rate row (honest absence returns).
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from services.cost_ledger import ledger as _ledger
from services.cost_ledger import rates as _rates
from services.enforce.census_identity import census_identity


router = APIRouter()


class RateRow(BaseModel):
    model_config = {"extra": "allow"}
    source: str = Field(min_length=3, max_length=400)
    currency: str = Field(default="USD", max_length=8)
    notes: Optional[str] = Field(default=None, max_length=600)


def _operator(actor):
    if not {"operator", "master_admin"}.intersection(actor["roles"]):
        raise HTTPException(403, "An admitted operator is required to author a rate")


@router.get("/api/cost_ledger/rates")
async def get_rates() -> Dict[str, Any]:
    """Owner-supplied rates on record. Empty lists mean honest absence."""
    data = _rates.load_rates()
    return {
        **data,
        "lanes": {lane: {"key": spec["key"], "rate_fields": list(spec["rate_fields"])} for lane, spec in _rates.LANES.items()},
        "honest_gap_note": _rates.HONEST_GAP_SENTENCE if not any(data.values()) else "",
    }


@router.post("/api/cost_ledger/rates/{lane}", status_code=201)
async def author_rate(lane: str, body: RateRow, actor=Depends(census_identity)) -> Dict[str, Any]:
    _operator(actor)
    try:
        row = _rates.author_rate(lane, body.model_dump(), actor["principal_id"])
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return {"tenant_id": actor["tenant_id"], "rate": row}


@router.delete("/api/cost_ledger/rates/{lane}/{ident:path}")
async def withdraw_rate(lane: str, ident: str, actor=Depends(census_identity)) -> Dict[str, Any]:
    _operator(actor)
    try:
        removed = _rates.remove_rate(lane, ident)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    if not removed:
        raise HTTPException(404, "No rate row with that identity")
    return {"tenant_id": actor["tenant_id"], "removed": ident, "lane": lane}


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
