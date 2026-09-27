"""Identity-scoped, read-only entitlement projection; absence is not a grant."""
from fastapi import APIRouter, Request, Query
from core import db
from services.portal_operational.access import portal_scope
from services.portal_operational.entitlements import LicencePortalView, read_view
from services.portal_operational.billing import LicenceInvoiceView, read_invoice

router = APIRouter(prefix="/api/portal/entitlement", tags=["portal-entitlement"])


@router.get("/licence", response_model=LicencePortalView)
@router.get("/catalog/listed", response_model=LicencePortalView)
@router.get("/allowance", response_model=LicencePortalView)
@router.get("/badges", response_model=LicencePortalView)
async def get_entitlement(request: Request):
    async with portal_scope(request) as scope:
        return await read_view(db, scope)


@router.get('/billing', response_model=LicenceInvoiceView)
async def get_billing(request: Request, period: str = Query(min_length=1, max_length=100, pattern=r'^[A-Za-z0-9_.:-]+$')):
    async with portal_scope(request) as scope:
        return await read_invoice(db, scope, period)