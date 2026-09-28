"""routers.portal_census_response_required — PHASE 3 continuation
A'''-cont-A · JWT-gated GET/POST surface for the response-required
queue backed by services.census_autonomy.response_required_queue.

Owner R-106 §4 verbatim (banked at services/census_autonomy/service_shape.py:70):
  "'response-required item to a queue surfaced ... in the portal UI'"

Owner directive 2026-09-22T~19:05Z (verbatim):
  "the drawer advertises response-required; the backing queue + endpoints
  must exist before anything else — an advertised control with no
  endpoint is a fake state by another name."

This router is ADDITIVE per SO §3.8. Zero edits to sealed carriers:
- `services.auth.dependencies.require_identity_or_deny` (READ-ONLY)
- `services.auth.identity.Identity` (READ-ONLY)
- `services.enforce.principal_context_adapter.principal_context` (READ-ONLY)
- `services.census_autonomy.response_required_queue` (this-slice A'''-cont-A ·
  own carrier · not sealed by any prior seal)

Wire-up: server.py includes `router` via `app.include_router(...)` in
BOTH the spine `server.py` and the runtime `/app/backend/server.py` per
the spine-bridge two-path resolution design.

Endpoints:
- `GET  /api/portal/census/response-required-items` — JWT-gated. Returns
  the list of PENDING items across all tenants (tenant-scoping under
  entitlement is a future desk-lane concern; this slice ships the queue
  infrastructure end-to-end).
- `POST /api/portal/census/response-required-items/{item_id}/resolve` —
  JWT-gated. Body carries resolver_id + resolution_text + resolved_state
  (must be RESOLVED_ACCEPTED or RESOLVED_REJECTED per closed vocab).
  Returns 404 when item_id unknown; 400 when resolved_state invalid;
  200 with the resolved payload on success.
"""

from __future__ import annotations

from typing import Any, Dict, Final

from fastapi import APIRouter, Body, HTTPException, Path, Request

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.census_autonomy.response_required_queue import (
    InvalidResolvedState,
    ItemNotFound,
    bank_response_required_item,  # noqa: F401 - re-export for future writers
    list_pending_response_required_items,
    resolve_response_required_item,
)
from services.enforce.principal_context_adapter import principal_context


# Final route paths — pinned so the invariant test can assert paired-equality.
LIST_ROUTE_PATH: Final[str] = "/api/portal/census/response-required-items"
RESOLVE_ROUTE_PATH_TEMPLATE: Final[str] = (
    "/api/portal/census/response-required-items/{item_id}/resolve"
)


router = APIRouter(prefix="", tags=["portal-census-response-required"])


@router.get(LIST_ROUTE_PATH)
async def get_response_required_items(request: Request) -> Dict[str, Any]:
    """List PENDING response-required items. JWT-gated."""
    result = await require_identity_or_deny(request)
    if not isinstance(result, Identity):
        # `require_identity_or_deny` returns an HTTPException-shaped Response
        # for the deny path per the sealed pattern; propagate as-is.
        return result  # type: ignore[return-value]

    identity: Identity = result
    with principal_context(identity.user_id):
        items = list_pending_response_required_items()
        return {"items": items, "count": len(items)}


@router.post(RESOLVE_ROUTE_PATH_TEMPLATE)
async def post_resolve_response_required_item(
    request: Request,
    item_id: str = Path(..., min_length=1),
    body: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    """Resolve a PENDING response-required item. JWT-gated."""
    result = await require_identity_or_deny(request)
    if not isinstance(result, Identity):
        return result  # type: ignore[return-value]

    identity: Identity = result

    resolution_text = str(body.get("resolution_text", "")).strip()
    resolved_state = str(body.get("resolved_state", "")).strip()
    if not resolution_text:
        raise HTTPException(
            status_code=400,
            detail="resolution_text is required",
        )
    if not resolved_state:
        raise HTTPException(
            status_code=400,
            detail="resolved_state is required",
        )

    with principal_context(identity.user_id):
        try:
            payload = resolve_response_required_item(
                item_id=item_id,
                resolver_id=identity.user_id,
                resolution_text=resolution_text,
                resolved_state=resolved_state,
            )
        except ItemNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except InvalidResolvedState as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"item": payload}
