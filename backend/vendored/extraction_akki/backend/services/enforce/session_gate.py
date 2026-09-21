"""services/enforce/session_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import session_binder as _m9_session


COLLECTION_NAME: str = "session"


async def upsert_session(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    binder_cls = getattr(_m9_session, "SessionBinder", None)
    if binder_cls is not None:
        _ = binder_cls(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
