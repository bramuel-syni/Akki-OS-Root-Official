"""services/enforce/task_scope_enforcement_gate.py · M11-W4/W5/W6/W7 · Option C thin-adapter.

Canon anchor: R-18 Tension (a) Option C · services.data.repository sole
Motor importer · M9 refuser composed first, then Repository op.
"""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import task_scope_enforcement as _m9


COLLECTION_NAME: str = "task_scope_enforcement"


async def upsert_task_scope_enforcement(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    cls = getattr(_m9, 'TaskScopeRefused', None)
    if cls is not None:
        _ = cls(**doc)
    return await repo.update_one({"id": doc["id"]}, {"$set": dict(doc)}, upsert=True)
