"""services.answering_service.collections.webhook_endpoints · WebhookEndpoint_v0 collection.

Canon 17 §4 · answering-service triangle · the `webhook_endpoint`
entity is the confirmed destination for delivery. Each endpoint is a
tenant-scoped confirmed URL that a delivery may target.

Per-tenant DB scope per Canon 3 §B.7 · M11: writes route to
`t_<tenant_id>` databases via `services.data.repository.Repository`.

Append-only writer discipline (Canon 3 §9.3 · M11 single-writer):
only `insert_webhook_endpoint` is exposed. No `update_*`, `delete_*`,
`upsert_*` surface (AST-enforced).

SO §3.8 thin-kernel additive-only. SO §3.10-α closed-schema discipline:
`WebhookEndpoint_v0` frozen + extra=forbid.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


COLLECTION_NAME: str = "webhook_endpoints"


class WebhookEndpoint_v0(BaseModel):
    """Frozen webhook-endpoint row · Canon 17 §4 confirmed destination."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    webhook_endpoint_id: str = Field(
        ..., min_length=1, pattern=r"^we_[a-z0-9_-]+$",
        description="Stable surrogate. Convention: 'we_<tenant>_<yyyy_mm>_<seq>'."
    )
    tenant_id: str = Field(
        ..., min_length=1,
        description="Tenant that owns this webhook endpoint · M11 per-tenant scope."
    )
    url: str = Field(
        ..., min_length=1,
        description="Confirmed target URL for delivery."
    )
    confirmed_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC timestamp of endpoint confirmation."
    )


def _tenant_db_name(tenant_id: str) -> str:
    """Return the per-tenant DB name for the webhook_endpoints collection.

    Canon 3 §B.7 · M11 discipline: `t_<tenant_id>`.
    """
    return f"t_{tenant_id}"


def insert_webhook_endpoint(
    endpoint: WebhookEndpoint_v0,
    *,
    repository: Any,
) -> WebhookEndpoint_v0:
    """Append-only insert of a webhook_endpoint row into the
    `webhook_endpoints` collection under the endpoint's tenant-scoped
    database.

    Callers must supply a `Repository` bound to the correct tenant
    context (AKKI-DATA-001 cross-tenant refusal enforced by
    Repository).
    """
    doc: Dict[str, Any] = endpoint.model_dump()
    repository.insert_one(doc)
    return endpoint


def get_webhook_endpoint(
    webhook_endpoint_id: str,
    *,
    repository: Any,
) -> Optional[WebhookEndpoint_v0]:
    """Read-surface lookup: returns the endpoint matching
    webhook_endpoint_id under the current tenant context, or None if
    absent."""
    doc = repository.find_one({"webhook_endpoint_id": webhook_endpoint_id})
    if doc is None:
        return None
    doc = {k: v for k, v in doc.items() if k != "_id"}
    return WebhookEndpoint_v0(**doc)


def list_webhook_endpoints_for_tenant(
    tenant_id: str,
    *,
    repository: Any,
) -> List[WebhookEndpoint_v0]:
    """Read-surface: all webhook endpoints under the current tenant
    context (filter by tenant_id enforced via Repository auto-injection
    · argument-only echo)."""
    cursor = repository.find({"tenant_id": tenant_id})
    out: List[WebhookEndpoint_v0] = []
    for doc in cursor:
        doc = {k: v for k, v in doc.items() if k != "_id"}
        out.append(WebhookEndpoint_v0(**doc))
    return out
