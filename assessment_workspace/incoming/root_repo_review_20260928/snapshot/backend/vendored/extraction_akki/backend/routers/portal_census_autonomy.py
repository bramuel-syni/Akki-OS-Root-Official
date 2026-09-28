"""routers.portal_census_autonomy · PHASE 3 continuation A' — JWT-gated
on-demand census run trigger + real-scheduler-state polling endpoint.

Owner R-106 §2 verbatim: "On-demand runs from any approved caller
(JWT-gated)."
Owner confirmation anchor point b verbatim (2026-09-22T~02:20Z):
"GATE THE READS behind the existing portal JWT (same pattern as
/api/portal/*)."
Owner directive PHASE 3 continuation A'': "the UI must show REAL
scheduler state only — the running card polls the service's own
state, never synthesized progress."

This router is ADDITIVE per SO §3.8. Zero edits to sealed carriers:
- `services.auth.dependencies.require_identity_or_deny` (imported READ-ONLY)
- `services.auth.identity.Identity` (imported READ-ONLY)
- `services.enforce.principal_context_adapter.principal_context` (READ-ONLY)
- `services.census_autonomy.engine` (PHASE 3 Commit-A c3e6725c · READ-ONLY except public callable `enqueue_on_demand_run`)
- `services.census_autonomy.service_shape.REFUSAL_PATH_CLOSED_VOCAB` (PHASE 3 Commit-A · READ-ONLY closed-vocab)
- `services.census_autonomy.tenant_scope` (PHASE 3 Commit-A · READ-ONLY)
- `services.census_autonomy.state_reader.read_census_run_state` (this-slice A')

Wire-up: `server.py` includes `router` via `app.include_router(...)`
(same additive pattern as `portal_census` at server.py line 262-263).

Endpoints:
- `POST /api/portal/census/run` — enqueue on-demand run (JWT-gated,
  tenant-scoped, LawfulBasisAdmit-gated). Returns 202 with
  `census_run_id`. Refusals return 4xx with a `refusal_code` field
  from the sealed `REFUSAL_PATH_CLOSED_VOCAB`.
- `GET /api/portal/census/runs/{census_run_id}/state` — real-state
  polling for the running-card UI. Returns 404 when the id is
  unknown (never synthesizes state). All responses reflect ONLY what
  lives on the filesystem cursor.
"""

from __future__ import annotations

from typing import Any, Dict, Final

from fastapi import APIRouter, Body, HTTPException, Path, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.enforce.principal_context_adapter import principal_context
from services.census_autonomy.engine import enqueue_on_demand_run
from services.census_autonomy.service_shape import REFUSAL_PATH_CLOSED_VOCAB
from services.census_autonomy.state_reader import read_census_run_state
from services.census_autonomy.tenant_scope import is_census_admitted_tenant

# ---------------------------------------------------------------------------
# Final route path pins (SO §3.10-α closed-vocab paired-equality). The
# RED-first invariants at
# tests/invariants/test_cp_census_autonomy_router_a_prime.py pin these
# by verbatim value.
# ---------------------------------------------------------------------------
ON_DEMAND_RUN_ROUTE_PATH: Final[str] = "/api/portal/census/run"
RUN_STATE_ROUTE_PATH_TEMPLATE: Final[str] = (
    "/api/portal/census/runs/{census_run_id}/state"
)

router = APIRouter(prefix="", tags=["portal-census-autonomy"])


def _refusal(
    status_code: int, refusal_code: str, detail: str
) -> JSONResponse:
    """Build a refusal response body carrying a sealed-vocab code."""
    if refusal_code not in REFUSAL_PATH_CLOSED_VOCAB:
        # Fail-loud shape violation; never emit unknown code to the UI.
        raise RuntimeError(
            f"Router attempted to emit refusal_code {refusal_code!r} "
            f"not in sealed REFUSAL_PATH_CLOSED_VOCAB "
            f"{REFUSAL_PATH_CLOSED_VOCAB}"
        )
    return JSONResponse(
        status_code=status_code,
        content={"refusal_code": refusal_code, "detail": detail},
    )


@router.post(ON_DEMAND_RUN_ROUTE_PATH, status_code=202)
async def post_on_demand_run(
    request: Request,
    body: Dict[str, Any] = Body(...),
):
    """POST /api/portal/census/run · enqueue on-demand census run.

    Body shape (required fields):
      {
        "tenant_id": str,                       # must be admitted
        "connect_source_descriptor": dict,      # source descriptor
        "lawful_basis_admit_ref": str,          # Doc-5 B5.2 pre-first-byte
      }

    Response 202: {"census_run_id": str, "status": "enqueued", ...}
    Response 400 BLOCKED_LAWFUL_BASIS_MISSING: missing lawful_basis_admit_ref
    Response 400 (generic): malformed body
    Response 403 BLOCKED_TENANT_SCOPE_MISMATCH: tenant not admitted
    """
    # JWT gate (sealed dependency).
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    tenant_id = body.get("tenant_id")
    connect_source_descriptor = body.get("connect_source_descriptor")
    lawful_basis_admit_ref = body.get("lawful_basis_admit_ref")

    if not tenant_id or not isinstance(tenant_id, str):
        return _refusal(
            400,
            "BLOCKED_TENANT_SCOPE_MISMATCH",
            "tenant_id missing or not a str",
        )
    if not lawful_basis_admit_ref or not isinstance(
        lawful_basis_admit_ref, str
    ):
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            "lawful_basis_admit_ref missing or not a str · "
            "Doc-5 B5.2 pre-first-byte gate",
        )
    if not isinstance(connect_source_descriptor, dict):
        return _refusal(
            400,
            "BLOCKED_LAWFUL_BASIS_MISSING",
            "connect_source_descriptor missing or not an object",
        )

    # Tenant-scope gate (adapter over sealed 4j tenant_separation).
    if not is_census_admitted_tenant(tenant_id):
        return _refusal(
            403,
            "BLOCKED_TENANT_SCOPE_MISMATCH",
            f"tenant_id {tenant_id!r} not in CENSUS_ADMITTED_TENANT_IDS "
            f"(named-but-unseated per R-104 or unknown)",
        )

    # Enqueue through sealed engine callable (PHASE 3 Commit-A c3e6725c).
    with principal_context(identity.user_id):
        census_run_id = enqueue_on_demand_run(
            tenant_id=tenant_id,
            connect_source_descriptor=connect_source_descriptor,
            lawful_basis_admit_ref=lawful_basis_admit_ref,
        )

    return JSONResponse(
        status_code=202,
        content={
            "census_run_id": census_run_id,
            "tenant_id": tenant_id,
            "status": "enqueued",
            "principal_id": identity.user_id,
        },
    )


@router.get(RUN_STATE_ROUTE_PATH_TEMPLATE)
async def get_run_state(
    request: Request,
    census_run_id: str = Path(..., min_length=1, max_length=128),
):
    """GET /api/portal/census/runs/{census_run_id}/state · REAL state.

    Owner directive: 'REAL scheduler state only — never synthesized
    progress.' This endpoint reads directly from the filesystem
    cursor via `state_reader.read_census_run_state`. Returns 404
    when the id is unknown; never fabricates.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    with principal_context(identity.user_id):
        state = read_census_run_state(census_run_id)

    if state is None:
        raise HTTPException(
            status_code=404,
            detail=f"census_run_id {census_run_id!r} unknown to scheduler",
        )
    return state
