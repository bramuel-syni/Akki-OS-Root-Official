"""Native metadata intake/readiness; no new accounts, roots, data reads or workers."""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, ConfigDict
from core import db
from services.portal_operational.access import portal_scope
from services.northena.execution_models import Request as ExecutionRequest, Held
from services.ledger_writer.principal_control import CommandConflict
from services.activation.receipts import NativeReceipts, SignedReceipt
from services.activation.approvals import approved_plan
from services.activation.issuance import issue_certificate
from services.activation.reservations import Reservations
from routers.activation_controls import bounded_payload, ValidationBody

router = APIRouter(prefix="/api/portal/activation", tags=["activation-controls"])
from services.activation.runtime_status import RuntimeStatus, runtime_status


@router.get("/runtime", response_model=RuntimeStatus)
async def runtime_configuration(request: Request):
    async with portal_scope(request):
        return runtime_status(request.app.state)


class RecordResponse(BaseModel):
    status: str
    receipt_ref: str | None = None
    reason_code: str | None = None
    execution_authorized: bool = False
    certificate_issued: bool = False


class SettlementBody(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    reservation_ref: str
    observation_ref: str


def native(request):
    value = getattr(request.app.state, "activation_receipts", None)
    if value is None:
        return NativeReceipts(db)
    if not isinstance(value, NativeReceipts):
        raise HTTPException(503, "Native activation receipt binding is invalid.")
    return value


@router.post("/receipts", response_model=RecordResponse)
async def record(request: Request):
    async with portal_scope(request, write=True):
        receipt = await bounded_payload(request, SignedReceipt)
        try:
            ref = await native(request).record(receipt)
            return RecordResponse(status="recorded", receipt_ref=ref)
        except Held as exc:
            return RecordResponse(status="held", reason_code=exc.reason_code)
        except CommandConflict:
            raise HTTPException(409, "Receipt command identity conflicts with its recorded event.") from None
        except (ValueError, TypeError, KeyError):
            raise HTTPException(422, "Receipt metadata failed native validation.") from None


@router.post("/readiness", response_model=RecordResponse)
async def readiness(request: Request):
    async with portal_scope(request) as scope:
        descriptor = await bounded_payload(request, ExecutionRequest)
        if (descriptor.tenant_id, descriptor.principal_id) != (scope["tenant_id"], scope["principal_id"]):
            raise HTTPException(403, "Request is outside the authenticated scope.")
        try:
            _, ref, _, _, _ = await approved_plan(native(request), descriptor)
            return RecordResponse(status="approvals_verified", receipt_ref=ref)
        except Held as exc:
            return RecordResponse(status="held", reason_code=exc.reason_code)


@router.post("/reservations/settle", response_model=RecordResponse)
async def settle(request: Request):
    async with portal_scope(request, write=True):
        body = await bounded_payload(request, SettlementBody)
        try:
            ref = await Reservations(native(request)).settle(body.reservation_ref, body.observation_ref)
            return RecordResponse(status="settled", receipt_ref=ref)
        except Held as exc:
            return RecordResponse(status="held", reason_code=exc.reason_code)
        except CommandConflict:
            raise HTTPException(409, "A reservation already has a different terminal measurement.") from None


@router.post("/certificates/issue", response_model=RecordResponse)
async def issue(request: Request):
    async with portal_scope(request, write=True):
        body = await bounded_payload(request, ValidationBody)
        receipts = native(request)
        if receipts.admitted_keys is None:
            return RecordResponse(status="held", reason_code="ADMITTED_SIGNER_RESOLVER_UNBOUND")
        try:
            _, ref = await issue_certificate(body.certificate, receipts,
                timeout_seconds=getattr(request.app.state, "activation_evidence_timeout_seconds", None))
            return RecordResponse(status="issued", receipt_ref=ref, certificate_issued=True)
        except Held as exc:
            return RecordResponse(status="held", reason_code=exc.reason_code)
        except CommandConflict:
            raise HTTPException(409, "Certificate identity already belongs to a different proof.") from None
        except (ValueError, TypeError):
            raise HTTPException(422, "Certificate metadata or verifier configuration is invalid.") from None