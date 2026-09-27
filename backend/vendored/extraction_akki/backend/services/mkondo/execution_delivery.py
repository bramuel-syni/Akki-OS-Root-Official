"""Closed metadata packet for the acknowledged Akki → Mkondo execution crossing."""
from typing import Annotated, Literal
from pydantic import Field, model_validator
from contracts.handoff_contract import HandoffContract_v0
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Frozen, Hash, Handle, Name, Request, Authority


def receiver_task_id(request_id, operation_key, receiver_principal_id):
    return "rx_" + digest({"request": request_id, "operation": operation_key, "receiver": receiver_principal_id})


def shape_sha256(request):
    return digest({"schema": "ExecutionDelivery_v1", "kind": request.kind, "engine": request.engine,
                   "request_sha256": request.digest()})


class ReceiverBinding(Frozen):
    request_sha256: Hash
    authority_ref: Name
    operation_key: Name
    receiver_principal_id: Name
    receiver_app: Literal["mkondo"]
    receiver_role: Literal["worker"]
    receiver_task_id: Name
    scope_refs: tuple[Name, ...]
    shape_sha256: Hash
    mandate_ref: Handle
    expires_epoch: Annotated[int, Field(gt=0)]
    evidence_mode: Literal["measured", "MOCKED"]


class HandoffAck(Frozen):
    handoff_id: Name
    contract_sha256: Hash
    request_sha256: Hash
    operation_key: Name
    fence: Annotated[int, Field(gt=0)]
    receiver_principal_id: Name
    receiver_task_id: Name
    scope_refs: tuple[Name, ...]
    shape_sha256: Hash
    receipt_ref: Handle
    expires_epoch: Annotated[int, Field(gt=0)]
    evidence_mode: Literal["measured", "MOCKED"]


class ExecutionDelivery(Frozen):
    protocol: Literal["acknowledged_v1"]
    request: Request
    authority: Authority
    operation_key: Name
    fence: Annotated[int, Field(gt=0)]
    contract: HandoffContract_v0
    binding: ReceiverBinding
    acknowledgement: HandoffAck
    handoff_ref: Hash
    ack_ref: Hash
    send_ref: Hash
    eligibility_ref: Hash

    @model_validator(mode="after")
    def cross_bound(self):
        r, a, b, ack, c = self.request, self.authority, self.binding, self.acknowledgement, self.contract
        if (a.request_sha256 != r.digest() or a.principal_id != r.principal_id or a.tenant_id != r.tenant_id
                or a.engine != r.engine or a.scope_refs != r.scope_refs
                or b.request_sha256 != r.digest() or b.authority_ref != a.authority_ref
                or b.operation_key != self.operation_key or b.scope_refs != r.scope_refs
                or b.receiver_principal_id == r.principal_id
                or b.receiver_task_id != receiver_task_id(r.request_id, self.operation_key, b.receiver_principal_id)
                or b.receiver_task_id == r.request_id or b.shape_sha256 != shape_sha256(r)
                or b.evidence_mode != "measured" or ack.evidence_mode != "measured"
                or c.authored_by != r.principal_id or c.identity_source.actor_id != r.principal_id
                or (c.identity_source.app, c.identity_source.role) != ("akki", "author")
                or (c.identity_destination.actor_id, c.identity_destination.app, c.identity_destination.role)
                   != (b.receiver_principal_id, b.receiver_app, b.receiver_role)
                or c.shape != "ExecutionDelivery_v1:" + b.shape_sha256
                or c.what != r.kind + ":" + r.digest() or c.receipt_ref is not None
                or ack.handoff_id != c.handoff_id or ack.contract_sha256 != digest(c.model_dump(mode="json"))
                or ack.request_sha256 != r.digest() or ack.operation_key != self.operation_key
                or ack.fence != self.fence or ack.receiver_principal_id != b.receiver_principal_id
                or ack.receiver_task_id != b.receiver_task_id or ack.scope_refs != r.scope_refs
                or ack.shape_sha256 != b.shape_sha256):
            raise ValueError("Delivery cross-binding invalid.")
        return self