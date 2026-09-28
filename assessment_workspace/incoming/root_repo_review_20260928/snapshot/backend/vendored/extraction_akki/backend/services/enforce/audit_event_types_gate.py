"""services/enforce/audit_event_types_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import audit_event_types as _m9_audit_event_types


COLLECTION_NAME: str = "audit_event_types"


async def upsert_audit_event_type(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    type_cls = getattr(_m9_audit_event_types, "AuditEventType", None)
    if type_cls is not None:
        _ = type_cls(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
