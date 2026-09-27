"""DAP request/OS work adapters over one append-only Northena record."""
from fastapi import APIRouter, Request
from core import db
from services.northena import portal_work
from services.portal_operational.access import portal_scope, validate_units
from services.portal_operational.models import SubmitRequest, WorkList, WorkView
from services.portal_operational.actions import stop, retry, result
from services.portal_operational import execution
from services.northena.execution_models import RunView

router = APIRouter(prefix="/api/portal/requests", tags=["portal-requests"])
work_router = APIRouter(prefix="/api/os/work", tags=["os-work"])


@work_router.get("", response_model=WorkList)
@router.get("/work", response_model=WorkList)
@router.get("", response_model=WorkList)
async def list_requests(request: Request):
    async with portal_scope(request) as scope:
        rows = await portal_work.listing(db, scope)
        return WorkList(principal_id=scope["principal_id"], rows=rows, count=len(rows))


@router.post("/submit", status_code=202, response_model=WorkView)
@router.post("", status_code=202, response_model=WorkView)
async def submit_request(payload: SubmitRequest, request: Request):
    async with portal_scope(request, write=True) as scope:
        validate_units(payload, scope)
        return await portal_work.submit(db, scope, payload)


@work_router.get("/{request_id}", response_model=WorkView)
@router.get("/{request_id}", response_model=WorkView)
async def get_request(request_id: str, request: Request):
    async with portal_scope(request) as scope:
        return await portal_work.detail(db, scope, request_id)


@router.post("/{request_id}/stop", response_model=WorkView)
async def stop_request(request_id: str, request: Request):
    async with portal_scope(request, write=True) as scope:
        return await stop(db, scope, request_id, bindings=getattr(request.app.state, "execution_bindings", None))


@router.post("/{request_id}/retry")
async def retry_request(request_id: str, request: Request):
    async with portal_scope(request, write=True) as scope:
        return await retry(db, scope, request_id, bindings=getattr(request.app.state, "execution_bindings", None))


@router.get("/{request_id}/result")
async def get_result(request_id: str, request: Request):
    async with portal_scope(request) as scope:
        return await result(db, scope, request_id, bindings=getattr(request.app.state, "execution_bindings", None))


@router.post("/{request_id}/execution/advance", response_model=RunView)
async def advance_execution(request_id: str, payload: execution.ExecutionBudget, request: Request):
    async with portal_scope(request, write=True) as scope:
        return await execution.advance(db, scope, request_id, payload,
                                       bindings=getattr(request.app.state, "execution_bindings", None),
                                       receipts=getattr(request.app.state, "activation_receipts", None))