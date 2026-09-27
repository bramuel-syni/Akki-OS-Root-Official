"""Record an already signed certificate only after native proof verification.

This service never creates a signing key or signs on an owner's behalf.
"""
from services.activation.native_evidence import NativeEvidence
from services.activation.validation import validate_certificate
from services.ledger_writer.conditional_control import append_at_head, HeadChanged
from services.ledger_writer.mongo_control import digest
from services.enforce.control_scope import require_control_scope
from services.northena.execution_models import Held


async def issue_certificate(document, receipts, *, timeout_seconds):
    scope = require_control_scope()
    events = await receipts.events()
    result = await validate_certificate(document, tenant_id=scope.tenant_id,
        principal_id=scope.principal_id, evidence=NativeEvidence(receipts), timeout_seconds=timeout_seconds)
    if not result.valid:
        raise Held(result.issues[0].code if result.issues else "CERTIFICATE_PROOF_NOT_VERIFIED")
    # One identity cannot name two different signed certificates. Ledger head CAS
    # also catches concurrent revocation/supersession and requires revalidation.
    try:
        event = await append_at_head(receipts.db, events, tenant_id=scope.tenant_id,
            run_id=document["identity"]["frozen_request_id"],
            command_id=digest({"activation_certificate_id": document["certificate_id"]}),
            event_type="activation.certificate.issued", resource_type="activation_certificate",
            decision=result.derived_state, reason_code="NATIVE_ACTIVATION_PROOF_VERIFIED",
            payload={"principal_id": scope.principal_id, "certificate": document,
                     "validation": result.model_dump(mode="json")})
    except HeadChanged:
        raise Held("CERTIFICATE_EVIDENCE_PREFIX_CHANGED") from None
    return result, event["row"]["hash"]