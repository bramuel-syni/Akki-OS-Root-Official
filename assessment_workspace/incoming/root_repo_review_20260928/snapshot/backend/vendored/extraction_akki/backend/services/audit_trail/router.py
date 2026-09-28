"""services.audit_trail.router — /api/audit_trail/overview (Wave F Cleanup).

Wire path for the audit-trail Overview surface — closes
CA1-001/002/003 per Wave F GO Scope C item (2) owner ruling verbatim
this session:
    "AUTHORIZED: build the audit-trail Overview surface
     (`services/audit_trail/` + wire + SPA per Ship-Manifest DoD)"

Body shape produced by services.audit_trail.overview.compute_overview();
see that module for canon anchors + verbatim quotes.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from services.audit_trail.overview import compute_overview


router = APIRouter()


@router.get("/api/audit_trail/overview")
async def get_audit_trail_overview() -> Dict[str, Any]:
    return compute_overview()
