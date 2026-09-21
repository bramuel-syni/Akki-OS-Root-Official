"""services/enforce/break_glass_session_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import break_glass_session as _m9_bgs


COLLECTION_NAME: str = "break_glass_session"


async def upsert_break_glass_session(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    session_cls = getattr(_m9_bgs, "BreakGlassSession", None)
    if session_cls is not None:
        _ = session_cls(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
