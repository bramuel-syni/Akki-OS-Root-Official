"""Requester disclosure allowlist; never interpolate native errors or hidden facts."""
from dataclasses import dataclass


@dataclass(frozen=True)
class PublicReason:
    code: str
    message: str
    next_action: str | None


_REASONS = {}


def _group(codes, message, action=None):
    for code in codes.split():
        _REASONS[code] = PublicReason(code, message, action)


_group("ADMISSION_UNRESOLVED", "Execution is held: operation rights, approval authority, terms and an admitted executor are not established.", "Complete the native admission checks for this frozen request.")
_group("EXECUTOR_ADAPTER_UNBOUND WORKER_LIMIT_ADMISSION_RPC_UNBOUND", "Execution is held: the admitted worker interface for this operation is not connected.", "Connect the admitted worker and its limit-acknowledgement interface.")
_group("ADMITTED_SIGNER_RESOLVER_UNBOUND OPERATION_AUTHORITY_NOT_BOUND NATIVE_BINDINGS_UNBOUND", "Execution is held: native admission records cannot yet be verified.", "Bind the existing estate admission service; a login or a submitted request is not an execution grant.")
_group("ACTIVATION_PLAN_MISSING_OR_AMBIGUOUS", "Execution is held: one current signed activation plan is required.", "Resolve the signed plan for this exact objective, scope and deadline.")
_group("APPROVAL_GROUP_PENDING", "Execution is held: a required approval group is not satisfied.", "Complete the outstanding native approval ceremony without changing the frozen request.")
_group("ALLOCATION_CAPACITY_EXCEEDED", "Execution is held: the effective allocation cannot cover this reservation.", "Reconcile prior measured usage or obtain an authorised allocation change.")
_group("ALLOCATION_LEDGER_BUSY", "Execution is held while a competing allocation decision is reconciled.", "Retry the same frozen request; do not create a duplicate workload.")
_group("EXECUTOR_OUTCOME_UNCERTAIN EXECUTOR_RECONCILIATION_REQUIRED CANCEL_ACKNOWLEDGEMENT_UNCERTAIN", "The worker outcome is uncertain. No new execution or successful stop is being assumed.", "Reconcile the recorded operation with its admitted worker. Existing reservations remain held.")
_group("ACTIVATION_PORTAL_DESCRIPTOR_MISMATCH ACTIVATION_PORTAL_OPERATION_MISMATCH RESERVATION_PLAN_CHANGED", "Execution is held because the native plan does not match this frozen request.", "Recover the matching signed descriptor. A changed objective or scope requires a new request.")
_group("ACTIVATION_PLAN_LOOKUP_UNAVAILABLE OPERATION_AUTHORITY_UNAVAILABLE ADMITTED_SIGNER_RESOLVER_UNAVAILABLE NATIVE_INSPECTOR_UNAVAILABLE WORKER_LIMIT_ACK_UNAVAILABLE", "A required native verification service is currently unavailable.", "Retry reconciliation after the admitted service is available; no local fallback is allowed.")
_group("ACTIVATION_PLAN_RECORD_INVALID NATIVE_CONTROL_LEDGER_INTEGRITY_FAILURE RECEIPT_SIGNATURE_INVALID RECEIPT_PROVENANCE_MISMATCH", "The native control evidence could not be verified.", "Have the evidence reconciled through the existing governing service; do not replace the recorded receipt.")
_group("RECEIPT_REVOKED RIGHTS_WITHDRAWN SIGNER_OR_RECEIPT_NOT_CURRENT", "The authority or evidence required for this operation is no longer current.", "Use the native revalidation process. Earlier approval does not override withdrawal or expiry.")
_group("RUNTIME_LIMITS_UNENFORCEABLE WORKER_LIMIT_ACK_BINDING_MISMATCH", "Execution is held: the worker has not proved the required limit admission.", "Verify the worker's signed acknowledgement against the exact plan and reservation.")
_group("DEADLINE_EXCEEDED REQUEST_DEADLINE_EXCEEDED TERMINATION_WINDOW_UNAVAILABLE", "The execution or safe-termination window is no longer available.", "Do not extend this frozen request. A new authorised commission is required.")
_group("ARTIFACT_INSPECTOR_UNBOUND ARTIFACT_VERIFICATION_UNBOUND VERIFIED_RESULT_NOT_AVAILABLE", "A verified result is not available for release.", "Complete independent artifact, custody and current retrieval checks.")
_group("MOCKED_RESULT_NOT_RELEASABLE", "The recorded result is MOCKED and cannot be released as live evidence.", "Obtain genuinely measured results through the admitted runtime.")
_group("NATIVE_SKILL_PROVISIONING_BINDING_REQUIRED", "This skill-building request has no admitted provisioning descriptor.", "Recover the native provisioning plan; do not substitute an answering or training job.")
_group("PRINCIPAL_NOT_ADMITTED PRINCIPAL_UNAVAILABLE PRINCIPAL_LOOKUP_NOT_BOUNDED PRINCIPAL_ADMISSION_UNAVAILABLE", "Current native principal admission could not be established.", "Revalidate admission through the existing estate service; application login alone is not sufficient.")
_group("NATIVE_CUSTODY_DELIVERY_REQUIRED", "This request has no admitted custody-delivery binding.", "Complete the native retrieval and delivery checks before releasing data.")
_group("REQUEST_STOPPED CANCELLED_BEFORE_DISPATCH CANCELLED_BEFORE_SEND EXECUTOR_CANCELLED", "This request is stopped. No party-wide halt was issued.")
_group("EXECUTION_RESERVED EXECUTOR_ACCEPTED EXECUTOR_RUNNING", "The operation is recorded. Verified completion has not yet been established.")
_group("VERIFIED_RESULT_RECORDED", "Measured execution is recorded. Result access and delivered bytes are checked separately.")
_group("EXECUTOR_FAILED", "The admitted worker reported a failed operation.", "Inspect its recorded evidence before commissioning any new work.")
_group("EXECUTION_FINALISATION_REQUIRED", "The worker outcome is recorded, but verification and accounting are not yet complete.", "Resume reconciliation of this same operation; do not run the workload again.")
_group("EXECUTOR_TERMINAL_OBSERVATION_CONFLICT", "Worker terminal reports conflict for this operation.", "Resolve the conflicting receipts through the governing service. No replacement result or new workload is assumed.")


def public_reason(code):
    return _REASONS.get(code, PublicReason("EXECUTION_HELD", "The operation requires native verification before it can proceed.",
        "Inspect this request's recorded evidence through its governing service."))


def disclosure(code, *, receipt_ref=None):
    value = public_reason(code)
    return {"reason_code": value.code, "reason": value.message,
            "next_action": value.next_action, "reason_receipt_ref": receipt_ref}