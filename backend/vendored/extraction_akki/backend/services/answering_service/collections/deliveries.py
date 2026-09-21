"""services.answering_service.collections.deliveries · Delivery_v0 collection.

Canon 17 §4 · answering-service triangle · the `delivery` entity is the
response record row of the answering-service triangle. Every delivery
carries a signature (per-tenant Ed25519 from W4) that binds the
delivered payload to the tenant.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`.

Append-only writer discipline (Canon 3 §9.3 · M11 single-writer):
only `insert_delivery` is exposed. No `update_*`, `delete_*`,
`upsert_*` surface (AST-enforced).

SO §3.8 thin-kernel additive-only. SO §3.10-α closed-schema discipline:
`Delivery_v0` frozen + extra=forbid.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


COLLECTION_NAME: str = "deliveries"


class Delivery_v0(BaseModel):
    """Frozen delivery row · Canon 17 §4 response entity."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    delivery_id: str = Field(
        ..., min_length=1, pattern=r"^dv_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'dv_<tenant>_<yyyy_mm>_<seq>'."
    )
    tenant_id: str = Field(
        ..., min_length=1,
        description="Tenant that owns this delivery · M11 per-tenant scope."
    )
    ask_id: str = Field(
        ..., min_length=1, pattern=r"^ask_[a-z0-9_-]+$",
        description="Ask this delivery answers."
    )
    webhook_endpoint_id: str = Field(
        ..., min_length=1, pattern=r"^we_[a-z0-9_-]+$",
        description="Confirmed webhook endpoint used for delivery."
    )
    state: str = Field(
        ..., min_length=1,
        description=(
            "Delivery state · closed alphabet at M11: "
            "'pending' | 'sent' | 'confirmed' | 'refused'. "
            "State transitions live at W4 signing surface."
        ),
    )
    signature: str = Field(
        ..., min_length=1,
        description=(
            "Ed25519 signature bytes hex-encoded (per-tenant key · "
            "M12b-W1 primitive · M14-W4 attaches at delivery time)."
        ),
    )
    payload_ref: str = Field(
        ..., min_length=1,
        description="Reference to the delivered payload · hash-binding."
    )
    delivered_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC timestamp of delivery record insertion."
    )


def _tenant_db_name(tenant_id: str) -> str:
    """Return the per-tenant DB name for the deliveries collection.

    Canon 3 §B.7 · M11 discipline: `t_<tenant_id>`.
    """
    return f"t_{tenant_id}"


def insert_delivery(
    delivery: Delivery_v0,
    *,
    repository: Any,
) -> Delivery_v0:
    """Append-only insert of a delivery row into the `deliveries`
    collection under the delivery's tenant-scoped database.

    Callers must supply a `Repository` bound to the correct tenant
    context (AKKI-DATA-001 cross-tenant refusal enforced by
    Repository).
    """
    doc: Dict[str, Any] = delivery.model_dump()
    repository.insert_one(doc)
    return delivery


def get_delivery(
    delivery_id: str,
    *,
    repository: Any,
) -> Optional[Delivery_v0]:
    """Read-surface lookup: returns the delivery matching delivery_id
    under the current tenant context, or None if absent."""
    doc = repository.find_one({"delivery_id": delivery_id})
    if doc is None:
        return None
    doc = {k: v for k, v in doc.items() if k != "_id"}
    return Delivery_v0(**doc)


def list_deliveries_for_ask(
    ask_id: str,
    *,
    repository: Any,
) -> List[Delivery_v0]:
    """Read-surface: all deliveries under the current tenant context
    for a given ask_id."""
    cursor = repository.find({"ask_id": ask_id})
    out: List[Delivery_v0] = []
    for doc in cursor:
        doc = {k: v for k, v in doc.items() if k != "_id"}
        out.append(Delivery_v0(**doc))
    return out
