"""Authenticated certificate diagnostics; never an issuer or a caller-supplied grant."""
import json
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, ValidationError
from core import db
from services.portal_operational.access import portal_scope
from services.activation.validation import validate_certificate, ValidationResult
from services.activation.schema import MAX_BYTES, PROFILE_ID, PROFILE_SHA, IMPLEMENTATION_SHA, ORIGINAL_SHA, POLICY_SHA
from services.ledger_writer.principal_control import append_event

router = APIRouter(prefix="/api/portal/activation", tags=["activation-controls"])


class ValidationBody(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    certificate: dict


class ValidationResponse(ValidationResult):
    audit_ref: str
    certificate_issued: bool = False


async def bounded_body(request):
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > MAX_BYTES:
            raise HTTPException(413, "Certificate metadata exceeds the admitted envelope.")
    def invalid_constant(_):
        raise ValueError("Non-finite JSON value")
    def unique_keys(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("Duplicate JSON member")
            out[key] = value
        return out
    try:
        parsed = json.loads(raw, parse_constant=invalid_constant, object_pairs_hook=unique_keys)
        return ValidationBody.model_validate(parsed)
    except (ValueError, TypeError, ValidationError, RecursionError):
        raise HTTPException(422, "A bounded, unambiguous certificate object is required.") from None


@router.get("/profile")
async def profile(request: Request):
    async with portal_scope(request):
        return {"profile_id": PROFILE_ID, "owner_schema_sha256": ORIGINAL_SHA,
                "profile_sha256": PROFILE_SHA, "implementation_sha256": IMPLEMENTATION_SHA,
                "crossing_policy_sha256": POLICY_SHA, "certificate_issuance": False}


@router.post("/certificates/validate", response_model=ValidationResponse)
async def validate(request: Request):
    async with portal_scope(request, write=True) as scope:
        body = await bounded_body(request)
        try:
            result = await validate_certificate(body.certificate, tenant_id=scope["tenant_id"],
                principal_id=scope["principal_id"], evidence=getattr(request.app.state, "activation_evidence", None),
                timeout_seconds=getattr(request.app.state, "activation_evidence_timeout_seconds", None),
                now=datetime.now(timezone.utc))
        except (ValueError, TypeError, RecursionError):
            raise HTTPException(422, "Certificate metadata or verifier configuration is invalid.") from None
        if any(x.code == "CERTIFICATE_SCOPE_MISMATCH" for x in result.issues):
            raise HTTPException(403, "Certificate is outside the authenticated request scope.")
        # Audit observation only; no certificate, authority or signature is minted.
        event = await append_event(db, tenant_id=scope["tenant_id"],
            run_id="av_" + result.certificate_sha256, command_id=uuid4().hex,
            event_type="activation.validation.observed", resource_type="activation_validation",
            decision="verified" if result.valid else "held", reason_code="ACTIVATION_VALIDATION",
            payload={"principal_id": scope["principal_id"], **result.model_dump(mode="json")})
        return ValidationResponse(**result.model_dump(), audit_ref=event["row"]["hash"])