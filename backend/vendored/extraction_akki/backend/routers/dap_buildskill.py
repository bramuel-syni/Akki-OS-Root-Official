"""routers.dap_buildskill · PHASE 4 (c-vi) · CP-SKILLS-LAYER-SERIES-CLOSE.

JWT-gated GET surface exposing the current provisioning state banked by the
sealed A18.2 persistence store. This is the backing surface for the DAP
buildskill page — the "advertised control with no endpoint is a fake state
by another name" doctrine is honoured: this router IS the endpoint, and
the page IS live against it.

Owner boundary directive verbatim (2026-02-23 · this-slice open):

    "§6.8 — continue. ... Proceed to CP-SKILLS-LAYER-SERIES-CLOSE (Slice 5):
     the buildskill surface must show real provisioning state or honest-gap,
     and the boundary report must include the tester walkthrough — the
     concrete steps a human takes and what they see."

Owner R-102 verbatim: "productized-or-honest-gap — the USER-visible bar."

## §3.8 additive-only posture

Sealed carriers consumed READ-ONLY:
- ``services.skill_provisioning_persistence.read_all`` (sealed at P4-c-ii
  Commit-A f7f08207 · A18.2 canon anchor). The router calls this public
  callable ONLY; zero imports of the underlying `_store_file`,
  `_active_dir`, `_default_dir`, or `_configure_for_tests` helpers.
- ``contracts.skill_provisioning_record_v0.SkillProvisioningRecordV0``
  (sealed at P4-c-i Commit-A 2f7d6b58 · A18.1 canon anchor · Pydantic
  8-field frozen tuple). The router serialises records via the sealed
  model's ``model_dump()`` discipline — no field additions, no shape
  mutation.
- ``services.auth.dependencies.require_identity_or_deny`` (sealed at
  earlier auth wave · READ-ONLY).

## Endpoint

``GET /api/dap/buildskill/provisioning-records`` — JWT-gated. Returns:

    {
      "records": [<SkillProvisioningRecordV0.model_dump()>, ...],
      "count":   <int · exact len(records)>
    }

ORIGIN-EMPTY at mount time (returns ``{records: [], count: 0}``) because
the sealed A18.2 store has zero writes on a fresh pod. Never fabricates;
never caches; reads sealed persistence on every call.

Standing bounds: additive-only per SO §3.8 · zero external I/O ·
deterministic · plain-product-language on the user-facing surface
(this router is a JSON API; product-language discipline applies to
frontend labels, not JSON field names).
"""

from __future__ import annotations

from typing import Any, Dict, Final, List

from fastapi import APIRouter, HTTPException, Request

from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.skill_provisioning_persistence import read_all


# Final route paths — pinned so the invariant test asserts paired-equality
# with the frontend hook's fetch URL construction (SO §3.10-α closed-set
# discipline extended to path constants).
PROVISIONING_RECORDS_ROUTE_PATH: Final[str] = (
    "/api/dap/buildskill/provisioning-records"
)


def _read_provisioning_records_body() -> Dict[str, Any]:
    """Business-logic helper · reads sealed A18.2 persistence via its
    public callable ONLY and returns the JSON body.

    Extracted so invariants can round-trip against the sealed store
    without going through HTTP transport (Pin 4 + Pin 5).
    """
    records: List[Dict[str, Any]] = [
        r.model_dump(mode="json") for r in read_all()
    ]
    return {"records": records, "count": len(records)}


router = APIRouter()


@router.get(PROVISIONING_RECORDS_ROUTE_PATH)
async def get_provisioning_records(request: Request) -> Dict[str, Any]:
    """List the current provisioning records for the DAP buildskill surface.

    JWT-gated via the sealed ``require_identity_or_deny`` dependency.
    On identity refusal, returns the auth gate's own HTTPException-shaped
    response (401/403); on success, returns the current sealed store
    state as JSON.
    """
    result = await require_identity_or_deny(request)
    if not isinstance(result, Identity):
        # `require_identity_or_deny` returns an HTTPException-shaped
        # Response on refusal; re-raise as 401 for FastAPI response body.
        raise HTTPException(status_code=401, detail="identity refused")

    return _read_provisioning_records_body()


__all__ = (
    "PROVISIONING_RECORDS_ROUTE_PATH",
    "_read_provisioning_records_body",
    "router",
)
