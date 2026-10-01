"""Native eligibility and Mkondo-handoff providers for the deterministic callable-skill executor.

Eligibility is read from the worker-signed quality register already on the tenant Ledger plus the current rights
graph; nothing is classified here. The handoff receiver is the admitted worker runtime of the approved Plan, and the
acknowledgement is signed on that runtime, not in E1.
"""
import time
from services.activation.approvals import approved_plan
from services.estate_admission.runtimes import runtime_by_id
from services.extraction_runtime import remote
from services.extraction_runtime.adapter import CALL_SECONDS
from services.ledger_writer.mongo_control import digest
from services.mkondo.execution_delivery import HandoffAck, ReceiverBinding, receiver_task_id, shape_sha256
from services.non_gpu_governance import proofs
from services.non_gpu_governance.rights import RightsGate
from services.northena.execution_eligibility import EligibilityReceipt
from services.northena.execution_models import Held

TTL_SECONDS = 3600


async def worker_descriptor(db, receipts, request):
    plan, _, _, _, events = await approved_plan(receipts, request)
    worker = await receipts.resolve(plan.worker_ref, kind='worker', events=events)
    descriptor = await runtime_by_id(db, request.tenant_id, worker.claims['runtime_id'])
    if descriptor['principal_id'] != worker.signer_id:
        raise Held('WORKER_RUNTIME_SIGNER_MISMATCH')
    return plan, descriptor, events


class SkillEligibility:
    def __init__(self, db, receipts):
        self.db, self.receipts = db, receipts

    async def evaluate(self, request, purpose, phase):
        plan, _, _, _, events = await approved_plan(self.receipts, request)
        quality_ref, _, quality = await proofs.one(self.receipts, request, events, 'quality_register', 'quality_register')
        junk = [r.unit_ref for r in quality.records if r.stratum == 'Junk']
        reason = 'QUALIFIED_UNITS_IN_SCOPE'
        try:
            await RightsGate(self.receipts).check(request, request.input_refs, events)
        except Held as exc:
            reason = exc.reason_code
        if junk:
            reason = 'JUNK_STRATUM_UNIT'
        return EligibilityReceipt(request_sha256=request.digest(), input_refs=request.input_refs, scope_refs=request.scope_refs,
            purpose=purpose, policy_ref='akki://receipt/' + quality.policy_receipt_ref,
            rule_pack_refs=('akki://quality-pack/' + quality.pack.version,),
            snapshot_refs=('akki://snapshot/' + quality.snapshot_sha256,), decision_ref='akki://receipt/' + quality_ref,
            disposition='eligible' if reason == 'QUALIFIED_UNITS_IN_SCOPE' else 'ineligible', reason_code=reason,
            expires_epoch=int(time.time()) + TTL_SECONDS, evidence_mode='measured')


class SkillHandoff:
    def __init__(self, db, receipts):
        self.db, self.receipts = db, receipts

    async def receiver(self, request, grant, operation_key, fence):
        plan, descriptor, _ = await worker_descriptor(self.db, self.receipts, request)
        return ReceiverBinding(request_sha256=request.digest(), authority_ref=grant.authority_ref, operation_key=operation_key,
            receiver_principal_id=descriptor['principal_id'], receiver_app='mkondo', receiver_role='worker',
            receiver_task_id=receiver_task_id(request.request_id, operation_key, descriptor['principal_id']),
            scope_refs=request.scope_refs, shape_sha256=shape_sha256(request), mandate_ref='akki://receipt/' + plan.worker_ref,
            expires_epoch=min(request.deadline_epoch, int(time.time()) + TTL_SECONDS), evidence_mode='measured')

    async def acknowledge(self, request, contract, binding, operation_key, fence):
        _, descriptor, _ = await worker_descriptor(self.db, self.receipts, request)
        if descriptor['principal_id'] != binding.receiver_principal_id:
            raise Held('RECEIVER_BINDING_MISMATCH')
        document = contract.model_dump(mode='json')
        control = {'mode': 'handoff_ack', 'tenant_id': request.tenant_id, 'request_sha256': request.digest(),
                   'operation_key': operation_key, 'fence': fence, 'scope_refs': list(request.scope_refs), 'contract': document}
        value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        if value.get('status') != 'acknowledged' or value.get('contract_sha256') != digest(document):
            raise Held('HANDOFF_ACK_REFUSED')
        return HandoffAck(handoff_id=contract.handoff_id, contract_sha256=value['contract_sha256'], request_sha256=request.digest(),
            operation_key=operation_key, fence=fence, receiver_principal_id=binding.receiver_principal_id,
            receiver_task_id=binding.receiver_task_id, scope_refs=request.scope_refs, shape_sha256=binding.shape_sha256,
            receipt_ref=f"akki://runtime/{descriptor['runtime_id']}/handoff/{value['receipt_id']}",
            expires_epoch=min(request.deadline_epoch, int(time.time()) + TTL_SECONDS), evidence_mode='measured')
