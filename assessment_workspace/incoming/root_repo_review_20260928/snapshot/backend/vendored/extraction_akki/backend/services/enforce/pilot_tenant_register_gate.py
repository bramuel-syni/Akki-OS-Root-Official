"""services/enforce/pilot_tenant_register_gate.py · M11-W4/W5/W6/W7 · Option C thin-adapter.

Canon anchor: R-18 Tension (a) Option C · services.data.repository sole
Motor importer · M9 refuser composed first, then Repository op.
"""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane import pilot_tenant_register as _m9


COLLECTION_NAME: str = "pilot_tenant_register"


async def upsert_pilot_tenant_register(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    cls = getattr(_m9, 'PilotTenantRecord', None)
    if cls is not None:
        _ = cls(**doc)
    return await repo.update_one({"id": doc["id"]}, {"$set": dict(doc)}, upsert=True)
