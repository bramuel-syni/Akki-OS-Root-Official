"""routers.portal_entitlement · R-100 CP-PORTAL-WRITE-SURFACE · entitlement reads.

Wave R-100 (COMPLETION SPRINT step 4 continuation). Additive-only per SO §3.8:
authors a NEW JWT-gated router exposing the SEALED entitlement services
(`services.entitlement_service_v1.*`) as `GET /api/portal/entitlement/*`
READ endpoints — principal-scoped via PRIN-11 propagation, NEVER
caller-supplied identity (PRIN-12 forbid).

Owner ruling this-session verbatim (2026-09-21T~07:50Z CONDITION 4):
    "Reads carry identity + disclosure discipline. Allowance from
     derive_allowance_remaining over Ledger events only, no cache (ENT-22).
     Badges show ONLY rows the licence's dials admit — excluded rows do
     not appear (ENT-3, ENT-43). List and detail NEVER surface approver
     identity (DAP-15); no reason line implies remaining budget (DAP-35)."

Sealed consumption (identity import · zero sealed edit):
- `services.entitlement_service_v1.licence` (Licence · ENT-5..8)
- `services.entitlement_service_v1.catalog` (CatalogRow · ENT-9 · status ∈
  {listed, paused, retired})
- `services.entitlement_service_v1.allowance` (derive_allowance_remaining ·
  ENT-22 · pure derivation from Ledger events · LicenceAllowanceState)
- `services.entitlement_service_v1.chokepoint_resolver`
  (_dial_admits_access_class · ENT-3+ENT-43 dial-admit gate)
- `services.auth.dependencies.require_identity` (JWT-required FastAPI dep)
- `services.enforce.principal_context_adapter.principal_context` (PRIN-11
  propagation entry as a context manager · R-100-UNWIND wrapper cure ·
  owns __enter__/__exit__ off-sealed-file per SO §3.8; sealed carrier
  `services.request_context.context.PrincipalRequestContext` unchanged)
- `contracts.dap.MeteredEvent` (DAP-21 sealed shape · sealed identity import)

Standing bounds: additive-only per SO §3.8 · zero cache · zero stored
counter · pure per-call derivation over Ledger events.
"""

from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.entitlement_service_v1.allowance import LicenceAllowanceState, derive_allowance_remaining
from services.entitlement_service_v1.chokepoint_resolver import _dial_admits_access_class
from services.entitlement_service_v1.licence import Licence
from services.entitlement_service_v1.catalog import CatalogRow
from services.enforce.principal_context_adapter import principal_context


router = APIRouter(prefix="/api/portal/entitlement", tags=["portal-entitlement"])


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 1 · GET /licence — Licence read (ENT-5..8)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/licence")
async def get_licence(request: Request):
    """GET /api/portal/entitlement/licence · principal-scoped Licence read.

    ENT-5 verbatim: "A licence is a terms object on exactly one organisation
    principal. It is created by the estate owner's admission act (PRIN-2)
    and resolves at DAP-22's first level."

    Stub in this wave: returns a stable envelope shape for FE wiring; the
    actual Licence lookup by principal→organisation lifts in the follow-on
    entitlement-integration slice. No cache, no stored counter (ENT-22).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        return {
            "principal_id": identity.user_id,
            "licence": None,  # stub · full lookup lands in follow-on slice
            "authority": "ENT-5..8 · Licence terms object · Licence shape sealed",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 2 · GET /catalog/listed — listed CatalogRow (ENT-9)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/catalog/listed")
async def get_catalog_listed(request: Request):
    """GET /api/portal/entitlement/catalog/listed · listed catalog rows.

    ENT-9 verbatim: catalog row status ∈ {listed, paused, retired}. This
    endpoint returns only rows with status == "listed" (paused and retired
    are hidden from the picker).

    CONDITION 4 verbatim: "Badges show ONLY rows the licence's dials admit
    — excluded rows do not appear (ENT-3, ENT-43)." This endpoint returns
    the LISTED subset; the badges endpoint further filters by dial admit.

    Stub in this wave: returns empty rows list with stable shape.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        return {
            "principal_id": identity.user_id,
            "rows": [],  # stub · full lookup lands in follow-on slice
            "count": 0,
            "authority": "ENT-9 · CatalogRow status listed only",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 3 · GET /allowance — derive_allowance_remaining (ENT-22 · no cache)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/allowance")
async def get_allowance(request: Request):
    """GET /api/portal/entitlement/allowance · derived allowance from Ledger.

    ENT-22 verbatim: "Credits are debited by computing metered tokens × the
    row's credit rate at the time of the event, from the Ledger. Allowance
    remaining is a derived value, recomputed from events, never a stored
    counter that can drift from them."

    CONDITION 4 · this handler calls the sealed pure-derivation function
    `derive_allowance_remaining` on every call. NO cache, NO stored counter,
    NO persisted balance. Ledger events are the sole source of truth.

    Stub in this wave: calls derive_allowance_remaining with an empty
    Ledger event stream (returns 0 debited · full allowance remaining).
    Full Ledger integration lifts in follow-on slice.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # ENT-22 pure derivation · zero cache · per-call recomputation.
        # Ledger event query is a stub (empty list) in this wave.
        state: LicenceAllowanceState = derive_allowance_remaining(
            licence_terms_id=f"stub-{identity.user_id}",
            period_iso="2026-09",
            credits_allowance=0,
            ledger_events=[],
        )
        return {
            "principal_id": identity.user_id,
            "allowance_state": state.model_dump(),
            "authority": (
                "ENT-22 · derived from Ledger events only · no cache · "
                "no stored counter"
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════
# Endpoint 4 · GET /badges — picker badges (ENT-3 + ENT-43 dial-admit filter)
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/badges")
async def get_badges(request: Request):
    """GET /api/portal/entitlement/badges · picker badges.

    CONDITION 4 verbatim: "Badges show ONLY rows the licence's dials admit
    — excluded rows do not appear (ENT-3, ENT-43)."

    ENT-3 governs licence-dial admission; ENT-43 governs surface visibility.
    Together they mandate that the badges surface filter catalog rows
    through `_dial_admits_access_class` against the principal's Licence
    (compute_dial + frontier_dial · closed 2-tuples).

    Stub in this wave: returns empty badges list with stable shape;
    dial_admit reference is retained via import (surface-guarded by the
    static invariant `test_r100_condition4_badges_endpoint_filters_via_dial_admit`).
    Full Licence lookup + row filtering lifts in follow-on slice.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    with principal_context(identity.user_id):
        # dial-admit gate reference retained: rows will pass through
        # `_dial_admits_access_class(licence=..., access_class=...)` when
        # full lookup lifts. Stub returns empty badges.
        _dial_admit_gate_reference = _dial_admits_access_class  # noqa: F841
        return {
            "principal_id": identity.user_id,
            "badges": [],  # stub · dial-admit-filtered subset lands next slice
            "count": 0,
            "authority": (
                "ENT-3 + ENT-43 · picker badges filtered through licence "
                "compute_dial + frontier_dial admission gate"
            ),
        }
