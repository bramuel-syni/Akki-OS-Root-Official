"""services.baseline_line.router — W7 CP7 · HTTP surface.

Endpoints:
  GET /api/baseline_line/records          — all lines on record
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from services.baseline_line.records import load_baseline_lines


router = APIRouter()


@router.get("/api/baseline_line/records")
async def list_baseline_lines() -> Dict[str, Any]:
    lines = load_baseline_lines()
    return {
        "count": len(lines),
        "lines": [bl.model_dump() for bl in lines],
        "ca1_anchor": "CA1-004 · Doc 14 §32 · baseline line names licence-verified starting model",
    }
