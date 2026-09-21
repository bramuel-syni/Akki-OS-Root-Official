"""services.compute_estate.router — GET /api/compute/estate.

Wave-G5c-COMPUTE-BACKEND. Read-only wire path. Never carries IPs, auth
vocab, or engineering vocab (owner ruling F, banked in DECISIONS.md).
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from services.compute_estate.estate import assemble_estate

router = APIRouter()


@router.get("/api/compute/estate")
async def get_compute_estate() -> Dict[str, Any]:
    """Return the compute-estate descriptor derived from banked Wave-H
    receipts. Product language only.
    """
    return assemble_estate()
