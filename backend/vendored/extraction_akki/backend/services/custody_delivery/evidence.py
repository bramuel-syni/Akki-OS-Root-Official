import hashlib
import json
from services.activation.native_evidence import Observation
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held
from services.custody_delivery.ports import origin_of


async def historical_grant(binding, descriptor, grant_ref, completion):
    """An expired link cannot be redeemed again, but its measured past delivery remains auditable.

    Only a CURRENT authenticated completion determines the historical verification
    time. This never returns a URL or issues a capability; current release gates
    still apply and the current admitted-key resolver still supplies trust/revocation.
    """
    from services.activation.receipts import NativeReceipts
    completion = await binding.receipts.verify_signature(completion)
    proof = Observation.model_validate_json(json.dumps(completion.claims))
    details = proof.delivery
    if (proof.category != 'delivery_completion' or details is None or details.stage != 'completed'
            or completion.signer_id != binding.custodian_principal_id or details.grant_receipt_ref != grant_ref
            or proof.context_sha256 != descriptor.digest() or details.completed_epoch > binding.clock()):
        raise Held('CUSTODY_COMPLETION_NOT_PROVED')
    historical = NativeReceipts(binding.receipts.db, binding.receipts.admitted_keys,
        timeout_seconds=binding.receipts.timeout, clock=lambda: details.redeemed_epoch)
    return await historical.resolve(grant_ref, kind='observation', request_sha256=descriptor.request_sha256)


async def check(binding, descriptor, receipt, *, stage, authority, url=None, grant=None, grant_ref=None):
    receipt = await binding.receipts.verify_signature(receipt)
    proof = Observation.model_validate_json(json.dumps(receipt.claims))
    details = proof.delivery
    if (receipt.kind != 'observation' or receipt.signer_id != binding.custodian_principal_id
            or receipt.request_sha256 != descriptor.request_sha256 or receipt.tenant_id != descriptor.tenant_id
            or not set(descriptor.scope_refs) <= set(receipt.scope_refs)
            or proof.category != 'delivery_' + ('grant' if stage == 'grant' else 'completion')
            or proof.evidence_mode != 'measured' or proof.context_sha256 != descriptor.digest()
            or proof.grounding is not None or proof.evaluation is not None or proof.refusal is not None or proof.quantities
            or details is None or details.stage != stage or details.delivery_id != descriptor.delivery_id
            or details.principal_id != descriptor.principal_id or details.artifact_sha256 != descriptor.artifact.sha256
            or details.artifact_size_bytes != descriptor.artifact.size_bytes
            or proof.claim_sha256 != digest(details.model_dump(mode='json'))):
        raise Held('CUSTODY_RECEIPT_BINDING_MISMATCH')
    now = binding.clock()
    if stage == 'grant':
        if (receipt.expires_epoch - receipt.issued_epoch > binding.max_grant_seconds
                or receipt.expires_epoch > authority.expires_epoch or details.origin not in binding.allowed_origins):
            raise Held('CUSTODY_GRANT_BOUNDS_INVALID')
        if url is not None:
            endpoint = url.get_secret_value()
            if (origin_of(endpoint) != details.origin or
                    hashlib.sha256(endpoint.encode()).hexdigest() != details.endpoint_sha256):
                raise Held('CUSTODY_CAPABILITY_BINDING_MISMATCH')
    elif (grant is None or details.grant_receipt_ref != grant_ref or not proof.terminal
          or not grant.issued_epoch <= details.redeemed_epoch <= details.completed_epoch <= receipt.issued_epoch <= now
          or details.redeemed_epoch >= grant.expires_epoch or details.observed_sha256 != descriptor.artifact.sha256
          or details.delivered_bytes != descriptor.artifact.size_bytes):
        raise Held('CUSTODY_COMPLETION_NOT_PROVED')
    return receipt