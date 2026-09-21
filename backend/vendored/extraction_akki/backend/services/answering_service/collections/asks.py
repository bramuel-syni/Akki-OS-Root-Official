"""services.answering_service.collections.asks · Ask_v0 collection.

Canon 17 §4 · answering-service triangle · the `ask` entity is the
request row of the answering-service triangle. Canon 15 §33 mirror:
every ask is authored under a `HandoffContract_v0` handoff_id.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`
(sole Motor importer).

Append-only writer discipline (Canon 3 §9.3 · M11 single-writer):
only `insert_ask` is exposed. No `update_*`, `delete_*`, `upsert_*`
surface (AST-enforced).

SO §3.8 thin-kernel additive-only: consumes sealed pre-M14 Repository
primitive without editing it. SO §3.10-α closed-schema discipline:
`Ask_v0` frozen + extra=forbid.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# Collection name constant · used as the mongo collection under
# t_<tenant_id> database.
COLLECTION_NAME: str = "asks"


class Ask_v0(BaseModel):
    """Frozen ask row · Canon 17 §4 request entity."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    ask_id: str = Field(
        ..., min_length=1, pattern=r"^ask_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'ask_<tenant>_<yyyy_mm>_<seq>'."
    )
    tenant_id: str = Field(
        ..., min_length=1,
        description="Tenant that owns this ask · M11 per-tenant scope."
    )
    handoff_id: str = Field(
        ..., min_length=1, pattern=r"^ho_[a-z0-9_-]+$",
        description="Governing HandoffContract_v0 · Canon 15 §33 mirror."
    )
    payload_ref: str = Field(
        ..., min_length=1,
        description="Reference to the payload · hash-binding per B-M10-Q1."
    )
    created_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC timestamp of ask creation."
    )


def _tenant_db_name(tenant_id: str) -> str:
    """Return the per-tenant DB name for the ask collection.

    Canon 3 §B.7 · M11 discipline: `t_<tenant_id>`.
    """
    return f"t_{tenant_id}"


def insert_ask(
    ask: Ask_v0,
    *,
    repository: Any,  # services.data.repository.Repository instance
) -> Ask_v0:
    """Append-only insert of an ask row into the `asks` collection under
    the ask's tenant-scoped database.

    Callers must supply a `Repository` bound to the correct tenant
    context; cross-tenant refusal is enforced by the repository primitive
    (AKKI-DATA-001 · Canon 8 §W11 tenant isolation).
    """
    doc: Dict[str, Any] = ask.model_dump()
    return _insert_via_repository(doc, ask, repository=repository)


def _insert_via_repository(
    doc: Dict[str, Any],
    ask: Ask_v0,
    *,
    repository: Any,
) -> Ask_v0:
    """Delegate the write to the sole Motor importer.

    The repository primitive auto-injects `{tenant_id: ctx.tenant_id}`
    on the document and refuses mismatched-tenant writes with
    AKKI-DATA-001.
    """
    # Delegate to the Repository primitive · thin adapter · Repository
    # signs off on the write's tenant isolation.
    repository.insert_one(doc)
    return ask


def get_ask(
    ask_id: str,
    *,
    repository: Any,
) -> Optional[Ask_v0]:
    """Read-surface lookup: returns the ask matching ask_id under the
    current tenant context, or None if absent."""
    doc = repository.find_one({"ask_id": ask_id})
    if doc is None:
        return None
    # Strip mongo `_id` if present (not part of the frozen model surface).
    doc = {k: v for k, v in doc.items() if k != "_id"}
    return Ask_v0(**doc)


def list_asks_for_handoff(
    handoff_id: str,
    *,
    repository: Any,
) -> List[Ask_v0]:
    """Read-surface: all asks under the current tenant context for a
    given handoff_id."""
    cursor = repository.find({"handoff_id": handoff_id})
    out: List[Ask_v0] = []
    for doc in cursor:
        doc = {k: v for k, v in doc.items() if k != "_id"}
        out.append(Ask_v0(**doc))
    return out
