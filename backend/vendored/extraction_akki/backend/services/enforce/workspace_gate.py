"""services/enforce/workspace_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane.workspace_entity import WorkspaceEntity


COLLECTION_NAME: str = "workspace"


async def upsert_workspace(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    _ = WorkspaceEntity(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
