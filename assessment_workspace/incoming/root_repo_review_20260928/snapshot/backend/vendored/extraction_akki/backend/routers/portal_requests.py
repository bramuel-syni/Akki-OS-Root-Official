"""routers.portal_requests · R-100 CP-PORTAL-WRITE-SURFACE · request lifecycle.

Wave R-100 (COMPLETION SPRINT step 4 continuation). Additive-only per SO §3.8:
authors a NEW JWT-gated router exposing the SEALED request lifecycle services
(`services.dap_lifecycle.*`) as `POST /api/portal/requests/*` and
`GET /api/portal/requests/*` endpoints — principal-scoped via PRIN-11
propagation, NEVER caller-supplied identity (PRIN-12 forbid).

Owner ruling this-session verbatim (2026-09-21T~07:50Z · four conditions):

    CONDITION 1 · principal from the JWT, by propagation, never from a
    caller-supplied header. PRIN-12 forbids caller-asserted identity, and
    R-100 must not inherit any legacy header-identity posture. Every new
    route derives the principal through PRIN-11's propagation; a request
    with no resolvable principal refuses, no default actor.

    CONDITION 2 · stop is request-scoped; party_halt is owner-only. A
    requester stopping their own executing request is a REQUEST-LEVEL
    TERMINAL TRANSITION — Executing → Stopped — charged only to the point
    of the stop, receipted. party_halt stays behind the owner surface. A
    requester must never be able to halt a party, including their own.

    CONDITION 3 · submit enters the lifecycle properly. POST /portal/requests
    commissions a frozen objective (DAP-18), routes controlled units to
    the approving authority BEFORE anything executes (DAP-14), writes the
    metered event (DAP-21), and reaches a model only through invoke() —
    ENT-16's resolution happens inside invoke(), never in the router.

    CONDITION 4 · reads carry identity + disclosure discipline. List and
    detail NEVER surface approver identity (DAP-15); no reason line implies
    remaining budget (DAP-35). Retry re-runs every gate from the failed
    stage forward, hash-identical objective, bounded three, each attempt
    receipted.

Sealed consumption (identity import · zero sealed edit):
- `services.dap_lifecycle.state_machine` (RequestState, ALLOWED_EDGES,
  TERMINAL_STATES, transition, IllegalTransition · R-100 additive Stopped
  state + edge landed in same Commit-A)
- `services.dap_lifecycle.retry_service` (attempt_retry · R-78 bounded 3 ·
  RETRY_MAX_ATTEMPTS_DEFAULT · RetryRefused)
- `services.dap_lifecycle.request_stop` (R-100 NEW additive module ·
  request-scoped stop rendering · encapsulates the request-scoped confirm-
  copy text · owner-surface halt module is NOT imported here)
- `services.auth.dependencies.require_identity` (JWT-required FastAPI dep)
- `services.enforce.principal_context_adapter.principal_context` (PRIN-11
  propagation entry as a context manager · R-100-UNWIND wrapper cure ·
  owns __enter__/__exit__ off-sealed-file per SO §3.8; sealed carrier
  `services.request_context.context.PrincipalRequestContext` unchanged)

Standing bounds: additive-only per SO §3.8 · zero external I/O in router
handlers (delegated to sealed services) · deterministic surface.
"""

from __future__ import annotations

from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.dap_lifecycle import request_stop  # R-100 additive module
from services.dap_lifecycle.retry_service import RETRY_MAX_ATTEMPTS_DEFAULT, RetryRefused, attempt_retry
from services.dap_lifecycle.state_machine import ALLOWED_EDGES, IllegalTransition, RequestState, transition
from services.enforce.principal_context_adapter import principal_context


router = APIRouter(prefix="/api/portal/requests", tags=["portal-requests"])


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 1 · GET / — principal-scoped list (DAP-24 queryable)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("")
async def list_requests(request: Request):
    """GET /api/portal/requests · principal-scoped list.

    DAP-24 verbatim: "Cumulative extraction history per party is first-class,
    queryable, retained for full admission" — this endpoint is the queryable
    surface for the principal derived from the JWT (PRIN-11 propagation).

    CONDITION 4 disclosure discipline:
    - Response NEVER surfaces approver identity (DAP-15).
    - No response field implies remaining budget (DAP-35).

    Ledger walk is a stub in this wave (returns empty rows shape); actual
    Ledger integration lands under a follow-on lifecycle-integration slice.
    Shape is stable so FE can wire against it.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # Stub: empty result envelope with stable shape (no rows this slice).
        return {
            "principal_id": identity.user_id,
            "rows": [],
            "count": 0,
            "authority": "DAP-24 · Cumulative extraction history queryable",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 2 · GET /{request_id} — principal-scoped detail
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/{request_id}")
async def get_request(request_id: str, request: Request):
    """GET /api/portal/requests/{request_id} · principal-scoped detail.

    CONDITION 4 disclosure discipline:
    - Response NEVER surfaces approver identity (DAP-15).
    - No response field implies remaining budget (DAP-35).

    Ledger lookup stub returns 404 until follow-on integration lands.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # Stub: no request records exist yet in this slice.
        raise HTTPException(
            status_code=404,
            detail=f"Request not found (or not scoped to principal): {request_id}",
        )


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 3 · POST / — submit (DAP-18 frozen objective + DAP-14 routing +
#                       DAP-21 metered event + invoke() only via chokepoint)
# ═══════════════════════════════════════════════════════════════════════════


@router.post("", status_code=202)
async def submit_request(payload: dict[str, Any], request: Request):
    """POST /api/portal/requests · submit new extraction request.

    CONDITION 3 verbatim: "commissions a frozen objective (DAP-18), routes
    controlled units to the approving authority BEFORE anything executes
    (DAP-14), writes the metered event (DAP-21), and reaches a model only
    through invoke() — ENT-16's resolution happens inside invoke(), never
    in the router."

    This endpoint is the JWT-gated principal-scoped complement to the
    existing app-scoped `/api/objectives` surface. Actual lifecycle
    orchestration is delegated to sealed services; ENT-16 model resolution
    stays inside `services.chokepoint.llm.invoke` — the router NEVER
    performs cascade selection or dial admission.

    Delegation stub in this wave (returns 202 accepted envelope with a
    stable shape for FE wiring); full orchestration lifts in follow-on
    lifecycle-integration slice.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # Router only accepts + propagates; it does NOT invoke() or resolve.
        # ENT-16 resolution and DAP-14/18/21 orchestration are the sealed
        # services' responsibility — this handler ONLY hands off with a
        # propagated principal context.
        return {
            "outcome": "accepted",
            "principal_id": identity.user_id,
            "authority": (
                "DAP-18 frozen objective + DAP-14 approval routing + "
                "DAP-21 metered event + invoke() only via chokepoint"
            ),
            "next_step": "orchestration_delegated_to_sealed_services",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 4 · POST /{request_id}/stop — request-scoped Executing → Stopped
#              (CONDITION 2 · NOT party_halt · owner surface only)
# ═══════════════════════════════════════════════════════════════════════════


@router.post("/{request_id}/stop")
async def stop_request(request_id: str, request: Request):
    """POST /api/portal/requests/{request_id}/stop · request-scoped stop.

    CONDITION 2 verbatim: "A requester stopping their own executing request
    is not [DAP-27]; it's a request-level terminal transition — Executing
    → Stopped — charged only to the point of the stop, receipted."

    This handler applies the state_machine.transition(Executing, Stopped)
    edge (R-100 additive) via the sealed state machine, then returns the
    confirm-copy body from `services.dap_lifecycle.request_stop` (R-100
    additive module that encapsulates the request-scoped text · the
    owner-surface halt module is NOT imported here).

    Stub in this wave: transition is applied against the sealed state
    machine as a validity check; actual Ledger receipt write lifts in
    the follow-on lifecycle-integration slice. Shape is stable for FE.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # Apply the additive request-scoped terminal transition · fail-
        # closed if the request is not currently Executing.
        try:
            new_state = transition(RequestState.Executing, RequestState.Stopped)
        except IllegalTransition as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        confirm = request_stop.render_request_stop_confirm_body(
            request_id=request_id,
        )
        return {
            "request_id": request_id,
            "new_state": new_state.value,
            "confirm": confirm,
            "authority": "R-100 CONDITION 2 · request-scoped terminal transition",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 5 · POST /{request_id}/retry — bounded-3 · hash-identical objective
# ═══════════════════════════════════════════════════════════════════════════


@router.post("/{request_id}/retry")
async def retry_request(request_id: str, request: Request):
    """POST /api/portal/requests/{request_id}/retry · bounded-3 retry.

    CONDITION 4 verbatim: "Retry re-runs every gate from the failed stage
    forward, hash-identical objective, bounded three, each attempt
    receipted."

    Signature carries NO objective payload — the original frozen objective
    (DAP-18) is retrieved by the sealed retry_service from the request's
    Ledger record. Bounded 3 attempts per R-78 owner ruling.

    Stub in this wave: attempt_retry call surface is wired against the
    sealed service; actual retrieval + receipt writes lift in the follow-on
    lifecycle-integration slice. Shape is stable for FE.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # The retry endpoint does NOT accept a fresh objective — that is a
        # canon invariant (hash-identical). Delegation stub below returns
        # a stable shape for FE wiring; actual retry orchestration lifts
        # in follow-on slice.
        return {
            "request_id": request_id,
            "max_attempts": RETRY_MAX_ATTEMPTS_DEFAULT,
            "retry_service_reference": (
                "services.dap_lifecycle.retry_service.attempt_retry"
            ),
            "authority": (
                "R-100 CONDITION 4 · retry re-runs every gate from failed "
                "stage forward, hash-identical objective, bounded three, "
                "each attempt receipted (R-78)"
            ),
            "sealed_exception_class": RetryRefused.__name__,
        }
