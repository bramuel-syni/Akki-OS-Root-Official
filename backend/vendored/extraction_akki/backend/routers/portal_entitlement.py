"""Identity-scoped, read-only entitlement projection; absence is not a grant."""
from fastapi import APIRouter, Request
from core import db
from services.portal_operational.access import portal_scope
from services.portal_operational.entitlements import LicencePortalView, read_view

router = APIRouter(prefix="/api/portal/entitlement", tags=["portal-entitlement"])


@router.get("/licence", response_model=LicencePortalView)
@router.get("/catalog/listed", response_model=LicencePortalView)
@router.get("/allowance", response_model=LicencePortalView)
@router.get("/badges", response_model=LicencePortalView)
async def get_entitlement(request: Request):
    async with portal_scope(request) as scope:
        return await read_view(db, scope)