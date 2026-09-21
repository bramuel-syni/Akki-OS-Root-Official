"""services/enforce/tenant_gate.py · M11-W3 · Option C thin-adapter.

Canon anchor: v1.0 B.2 (per-tenant data plane) + R-18 Tension (a) Option C.
Composes M9 TenantEntity dataclass shape-refuser with Repository primitive.
"""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Context, Repository
from services.platform_control_plane.tenant_entity import TenantEntity


COLLECTION_NAME: str = "tenant"


async def upsert_tenant(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    """Shape-refuser first (TenantEntity(**doc) raises on mismatch),
    then Repository upsert (auto-inject tenant_id · AKKI-DATA-001 refuse)."""
    _ = TenantEntity(**doc)
    return await repo.update_one(
        {"id": doc["id"]}, {"$set": dict(doc)}, upsert=True,
    )
