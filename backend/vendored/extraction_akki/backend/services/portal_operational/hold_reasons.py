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


_group('CUSTODY_PROVIDER_UNBOUND', 'Verified result references exist, but no admitted custody delivery service is connected.',
       'Connect the existing authorised custody service; no source bytes will be downloaded through this workspace.')
_group('CUSTODY_DELIVERY_REQUESTED', 'A custody handoff is recorded; delivery is not yet proved.')
_group('CUSTODY_CAPABILITY_ISSUED', 'A short-lived custody link was issued; that is not proof of byte delivery.')
_group('CUSTODY_COMPLETION_RECORDED', 'Measured custody delivery is recorded. Current access is checked separately.')
_group('CUSTODY_DELIVERY_NOT_FOUND SKILL_QUERY_NOT_FOUND', 'The requested record is not available within your current scope.')
_group('CUSTODY_PROVIDER_OUTCOME_UNCERTAIN CUSTODY_PROVIDER_RESPONSE_INVALID', 'The custody service has not supplied verified completion evidence.',
       'Reconcile the same delivery identifier; issuing a link is not proof of delivery.')
_group('CUSTODY_ORIGIN_UNAVAILABLE', 'The verified result rests in your estate\'s own store; no retrieval origin is ruled for it, so Akki issues no link.',
       'Retrieve it where that store is mounted, or have an HTTPS retrieval origin ruled for this estate\'s custody.')
_group('CUSTODY_GRANT_REFUSED CUSTODY_COMPLETION_REFUSED CUSTODY_OBJECT_SIZE_MISMATCH CUSTODY_AUTHORITY_WINDOW_TOO_SHORT SEALED_OBJECT_UNRESOLVED CUSTODY_DESCRIPTOR_UNRESOLVED',
       'The custodian could not match the sealed result to this delivery.', 'Reconcile the same delivery identifier against the recorded sealed object; nothing is downloaded meanwhile.')

_group('CUSTODY_IDEMPOTENCY_CONFLICT SKILL_QUERY_IDEMPOTENCY_CONFLICT', 'This retry identifier belongs to a different frozen request.',
       'Do not alter the original request while retrying it.')
_group('CUSTODY_RESULT_NOT_CURRENTLY_ADMITTED CUSTODY_SCOPE_MISMATCH CUSTODY_REGISTERED_ARTIFACT_CHANGED',
       'This result is not currently authorised for delivery.', 'Revalidate the governing rights and exact registered artifact.')
_group('CUSTODY_ORIGIN_INVALID CUSTODY_CAPABILITY_BINDING_MISMATCH CUSTODY_UNSIGNED_CAPABILITY CUSTODY_GRANT_BOUNDS_INVALID CUSTODY_GRANT_CHANGED CUSTODY_RECEIPT_BINDING_MISMATCH CUSTODY_COMPLETION_NOT_PROVED CUSTODY_COMPLETION_CONFLICT CUSTODY_REGISTRY_NOT_VERIFIED CUSTODY_ARTIFACT_NOT_REGISTERED',
       'Custody evidence could not be matched to this authorised result.', 'No download or successful delivery is being assumed.')
_group('SKILL_NATIVE_PLAN_REQUIRED SKILL_NATIVE_PLAN_INVALID SKILL_NATIVE_PLAN_MISMATCH SKILL_EXECUTOR_UNADMITTED SKILL_PLAN_LOOKUP_UNAVAILABLE',
       'This question needs a matching admitted native skill plan.', 'Use the existing skill admission path; no local answer is generated.')
_group('SKILL_PROVISIONING_CHANGED SKILL_PROVISIONING_REVOKED', 'The skill provisioning has changed or been withdrawn.',
       'A frozen question cannot be silently moved to a different skill or corpus.')
_group('SKILL_OUTCOME_CONFLICT SKILL_GROUNDING_RECEIPT_REQUIRED SKILL_GROUNDING_BINDING_MISMATCH SKILL_ANSWER_ARTIFACT_MISMATCH SKILL_ANSWER_CLASS_OR_HASH_MISMATCH SKILL_INDEPENDENT_ANCHOR_NOT_PROVED SKILL_RESPONSE_BELOW_FLOOR SKILL_ANSWER_REGISTRY_UNVERIFIED SKILL_NATIVE_VERIFICATION_UNAVAILABLE SKILL_NATIVE_EVIDENCE_INVALID SKILL_REFUSAL_AMBIGUOUS SKILL_REFUSAL_NOT_PROVED',
       'A grounded answer or genuine refusal has not yet been verified.', 'No answer text, class or live success is being fabricated.')

_group('NATIVE_RIGHTS_PROOF_REQUIRED ARTIFACT_LINEAGE_REQUIRED',
       'Current rights and source-to-result lineage have not been proved.',
       'Resolve the native rights and lineage receipts for the frozen inputs and result.')
_group('DESCENDANT_RIGHTS_WITHDRAWN', 'A source supporting this result has been withdrawn.',
       'Recall the affected result or admit a separately verified replacement; old links cannot restore rights.')
_group('QUALITY_REGISTER_PROOF_REQUIRED QUALITY_PLAN_BINDING_MISMATCH QUALITY_POLICY_NOT_CONFIRMED QUALITY_POPULATION_MISMATCH TRAINING_QUALITY_NOT_ELIGIBLE',
       'The confirmed quality pack and complete assessed population have not been reconciled.',
       'Complete the native quality assessment; unassessed records are not Clean.')
_group('CONTEXT_WINDOW_PROOF_REQUIRED CONTEXT_QUALITY_OR_OBJECTIVE_MISMATCH CONTEXT_POLICY_MISMATCH CONTEXT_QUALIFIED_POPULATION_MISMATCH CONTEXT_CONTENT_HASH_MISMATCH CONTEXT_QUALITY_CLASS_VIOLATION',
       'The qualified context window, class and exclusions could not be reconstructed.',
       'Reconcile the pinned native context evidence without replacing the frozen objective.')
_group('MEMORY_IDENTITY_OR_CLASS_MISMATCH MEMORY_PUBLICATION_MISMATCH MEMORY_PUBLICATION_ORDER_INVALID',
       'The compacted context cannot be released with its current evidence.',
       'Verify its publication receipt, retained-source rights and recorded class.')
_group('GOVERNANCE_EVIDENCE_PREFIX_CHANGED', 'Governing evidence changed during verification.',
       'Reconcile this same request against the current ledger; do not duplicate execution.')


def disclosure(code, *, receipt_ref=None):
    value = public_reason(code)
    return {"reason_code": value.code, "reason": value.message,
            "next_action": value.next_action, "reason_receipt_ref": receipt_ref}