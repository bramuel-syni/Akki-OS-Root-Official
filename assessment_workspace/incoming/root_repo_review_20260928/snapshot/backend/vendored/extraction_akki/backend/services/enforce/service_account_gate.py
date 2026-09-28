"""services/enforce/service_account_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane.service_account_entity import ServiceAccountEntity


COLLECTION_NAME: str = "service_account"


async def upsert_service_account(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    _ = ServiceAccountEntity(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
