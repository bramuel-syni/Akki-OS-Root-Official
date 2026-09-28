"""services/enforce/user_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane.user_entity import UserEntity


COLLECTION_NAME: str = "user"


async def upsert_user(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    _ = UserEntity(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
