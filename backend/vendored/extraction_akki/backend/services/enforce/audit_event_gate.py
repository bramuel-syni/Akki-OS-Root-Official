"""services/enforce/audit_event_gate.py · M11-W3 · Option C thin-adapter.

audit_event is append-only in the M11 data plane (no updates, no deletes);
Repository.insert_one is the sole allowed write.
"""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import audit_event as _m9_audit_event


COLLECTION_NAME: str = "audit_event"


async def append_audit_event(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    event_cls = getattr(_m9_audit_event, "AuditEvent", None)
    if event_cls is not None:
        _ = event_cls(**doc)
    return await repo.insert_one(dict(doc))
