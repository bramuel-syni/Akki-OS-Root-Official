"""services/data/repository.py · M11-W1 · Repository primitive.

The SOLE Motor importer for the data plane (v1.0 B.2).  Auto-injects
`{tenant_id: ctx.tenant_id}` into every outgoing filter; refuses any
write whose document or filter carries a `tenant_id` mismatching the
context, with refusal code AKKI-DATA-001.

Canon anchors (verbatim):
  v1.0 B.2 · "Primary datastore is Mongo, one database per tenant,
  all access via `services.data.repository` — the sole Motor
  importer."
  v1.0 D-01 · "Tenant isolation invariant AKKI-DATA-001: a data-plane
  call whose document `tenant_id` mismatches the injected context
  tenant_id is refused."
  R-18 Tension (a) Option C · owner ruling 2026-09-17T~15:45Z ·
  SO §3.8 amended in place · "M11-W1 lands
  `services/data/repository.py` as the sole Motor importer."

Discipline:
  - Preventive-charter refusal shape (M9 precedent):
    `RepositoryRefusalError` root + named subclass
    `CrossTenantAccessRefused` (code = 'AKKI-DATA-001').
  - COUNTS-only refusal messages · no leaked identifiers.
  - Frozen `Context` carrier (1-field OPEN str: `tenant_id`).
  - Zero closed enums (SO §3.10 Option α).
  - `AKKI_DATA_001` bare string constant · no `enum.Enum` subclass.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

# SOLE MOTOR IMPORTER · enforced by
# backend/tests/invariants/test_m11w1_data_layer_sole_motor_importer.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection  # noqa: F401


# --- Refusal code -----------------------------------------------------------

AKKI_DATA_001 = "AKKI-DATA-001"


# --- Refusal-class hierarchy (M9 preventive-charter shape) -----------------

class RepositoryRefusalError(Exception):
    """Root of the M11-W1 data-plane refusal hierarchy."""
    code: str = ""


class CrossTenantAccessRefused(RepositoryRefusalError):
    """AKKI-DATA-001 · document or filter carries a tenant_id that
    mismatches the context tenant_id."""
    code: str = AKKI_DATA_001


# --- Frozen carrier: request context ---------------------------------------

@dataclass(frozen=True)
class Context:
    """Frozen 1-carrier · OPEN str per SO §3.10 Option α."""
    tenant_id: str


# --- Repository -------------------------------------------------------------

class Repository:
    """Thin wrapper over an `AsyncIOMotorCollection`.

    - Read path (`find`, `find_one`, `count_documents`): merges
      `{tenant_id: ctx.tenant_id}` into the outgoing filter.
    - Write path (`insert_one`, `update_one`, `update_many`,
      `delete_one`, `delete_many`): refuses on any tenant_id in the
      filter or document body that mismatches `ctx.tenant_id`;
      otherwise merges the ctx tenant_id and forwards.

    Callers under `services/enforce/<entity>_gate.py` (W3+) compose
    this primitive with the paired M9 refuser (Branch C · thin
    adapter · R-18 Tension (a) Option C).
    """

    __slots__ = ("_ctx", "_collection")

    def __init__(self, *, ctx: Context, collection: Any) -> None:
        self._ctx = ctx
        self._collection = collection

    # --- helpers ------------------------------------------------------------

    def _refuse_filter_cross_tenant(self, f: Mapping[str, Any]) -> None:
        v = f.get("tenant_id")
        if v is not None and v != self._ctx.tenant_id:
            # COUNTS-only refusal message · no identifier leakage.
            raise CrossTenantAccessRefused(
                f"AKKI-DATA-001: cross-tenant filter refused "
                f"(counts mismatch: 1)"
            )

    def _refuse_doc_cross_tenant(self, doc: Mapping[str, Any]) -> None:
        v = doc.get("tenant_id")
        if v is not None and v != self._ctx.tenant_id:
            raise CrossTenantAccessRefused(
                f"AKKI-DATA-001: cross-tenant document refused "
                f"(counts mismatch: 1)"
            )

    def _refuse_set_cross_tenant(self, update: Mapping[str, Any]) -> None:
        set_blk = update.get("$set")
        if isinstance(set_blk, Mapping):
            v = set_blk.get("tenant_id")
            if v is not None and v != self._ctx.tenant_id:
                raise CrossTenantAccessRefused(
                    f"AKKI-DATA-001: cross-tenant $set refused "
                    f"(counts mismatch: 1)"
                )

    def _inject_tenant_id_into_filter(
        self, f: Optional[Mapping[str, Any]]
    ) -> dict:
        out = dict(f or {})
        out["tenant_id"] = self._ctx.tenant_id
        return out

    def _prepare_doc_for_write(self, doc: Mapping[str, Any]) -> dict:
        self._refuse_doc_cross_tenant(doc)
        out = dict(doc)
        out.setdefault("tenant_id", self._ctx.tenant_id)
        return out

    # --- read path ---------------------------------------------------------

    def find(
        self, filter: Optional[Mapping[str, Any]] = None, **kwargs: Any
    ):
        """Merges tenant_id into filter · returns Motor's cursor (not awaited)."""
        f = self._inject_tenant_id_into_filter(filter)
        return self._collection.find(f, **kwargs)

    async def find_one(
        self, filter: Optional[Mapping[str, Any]] = None, **kwargs: Any
    ):
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.find_one(f, **kwargs)

    async def count_documents(
        self, filter: Optional[Mapping[str, Any]] = None, **kwargs: Any
    ):
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.count_documents(f, **kwargs)

    # --- write path --------------------------------------------------------

    async def insert_one(
        self, document: Mapping[str, Any], **kwargs: Any
    ):
        doc = self._prepare_doc_for_write(document)
        return await self._collection.insert_one(doc, **kwargs)

    async def update_one(
        self,
        filter: Mapping[str, Any],
        update: Mapping[str, Any],
        **kwargs: Any,
    ):
        self._refuse_filter_cross_tenant(filter)
        self._refuse_set_cross_tenant(update)
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.update_one(f, update, **kwargs)

    async def update_many(
        self,
        filter: Mapping[str, Any],
        update: Mapping[str, Any],
        **kwargs: Any,
    ):
        self._refuse_filter_cross_tenant(filter)
        self._refuse_set_cross_tenant(update)
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.update_many(f, update, **kwargs)

    async def delete_one(
        self, filter: Mapping[str, Any], **kwargs: Any
    ):
        self._refuse_filter_cross_tenant(filter)
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.delete_one(f, **kwargs)

    async def delete_many(
        self, filter: Mapping[str, Any], **kwargs: Any
    ):
        self._refuse_filter_cross_tenant(filter)
        f = self._inject_tenant_id_into_filter(filter)
        return await self._collection.delete_many(f, **kwargs)
