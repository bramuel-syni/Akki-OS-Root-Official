"""services.trace.router — /api/trace endpoints (W8 CP5)."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Query

from services.trace.timeline import load_timeline


router = APIRouter()


@router.get("/api/trace")
async def get_trace(
    since: Optional[str] = Query(None, description="ISO-8601 UTC lower bound"),
    kind: Optional[str] = Query(None, description="Filter to one kind"),
) -> Dict[str, Any]:
    kinds = [kind] if kind else None
    entries = load_timeline(since_iso=since, kinds=kinds)
    return {
        "count": len(entries),
        "entries": [asdict(e) for e in entries],
        "reference_note": (
            "REFERENCE-NOT-COPY · this timeline references records on disk; "
            "the original governance records live under phase0/ where each "
            "producer wrote them. source_path per entry."
        ),
    }
