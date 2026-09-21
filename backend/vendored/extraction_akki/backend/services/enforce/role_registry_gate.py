"""services/enforce/role_registry_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import role_registry as _m9_role_registry


COLLECTION_NAME: str = "role_registry"


async def upsert_role_registry_entry(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    """M9 role_registry module provides the entry schema; Repository upserts."""
    # M9 shape check delegated to module-level constructor if present
    entry_cls = getattr(_m9_role_registry, "RoleRegistryEntry", None)
    if entry_cls is not None:
        _ = entry_cls(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
