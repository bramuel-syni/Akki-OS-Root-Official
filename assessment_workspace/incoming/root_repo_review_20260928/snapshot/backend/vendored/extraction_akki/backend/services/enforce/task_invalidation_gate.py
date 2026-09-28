"""services/enforce/task_invalidation_gate.py · M11-W4/W5/W6/W7 · Option C thin-adapter.

Canon anchor: R-18 Tension (a) Option C · services.data.repository sole
Motor importer · M9 refuser composed first, then Repository op.
"""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import task_invalidation as _m9


COLLECTION_NAME: str = "task_invalidation"


async def append_task_invalidation(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    cls = getattr(_m9, 'TaskApprovalRefused', None)
    if cls is not None:
        _ = cls(**doc)
    return await repo.insert_one(dict(doc))
