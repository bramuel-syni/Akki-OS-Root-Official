"""Canonical envelope → native Mkondo projection → verified receiver acknowledgement."""
import time
from datetime import datetime, timezone
from contracts.handoff_contract import HandoffActor, HandoffContract_v0
from services.ledger_writer.mongo_control import digest
from services.ledger_writer.principal_control import CommandConflict
from services.northena.execution_models import Held
from services.northena.execution_gate_checks import async_provider, bounded, typed
from services.mkondo.execution_delivery import ReceiverBinding, HandoffAck, ExecutionDelivery, receiver_task_id, shape_sha256
from services.mkondo.execution_projection import configured_directory, project


class UnboundHandoff:
    async def prepare(self, *args):
        raise Held("HANDOFF_PRODUCER_NOT_BOUND")

    async def revalidate(self, *args):
        raise Held("HANDOFF_PRODUCER_NOT_BOUND")

    async def validate_result(self, *args):
        raise Held("HANDOFF_PRODUCER_NOT_BOUND")


class MkondoHandoff:
    def __init__(self, journal, authority, provider=None, timeout_seconds=None, clock=time.time):
        self.directory = configured_directory()
        async_provider(provider, ("receiver", "acknowledge"), timeout_seconds)
        self.journal, self.authority, self.provider = journal, authority, provider
        self.timeout_seconds, self.clock = timeout_seconds, clock

    def bind(self, journal, authority, timeout_seconds):
        return MkondoHandoff(journal, authority, self.provider, timeout_seconds, self.clock)

    async def receiver(self, request, grant, dispatch):
        if self.provider is None:
            raise Held("HANDOFF_PRODUCER_NOT_BOUND")
        key, fence = dispatch["data"]["operation_key"], dispatch["seq"]
        binding = typed(await bounded(self.provider.receiver, self.timeout_seconds, request, grant, key, fence),
                        ReceiverBinding, "RECEIVER_BINDING_INVALID")
        if (binding.request_sha256 != request.digest() or binding.authority_ref != grant.authority_ref
                or binding.operation_key != key or binding.scope_refs != request.scope_refs
                or binding.receiver_principal_id == request.principal_id
                or binding.receiver_task_id != receiver_task_id(request.request_id, key, binding.receiver_principal_id)
                or binding.receiver_task_id == request.request_id or binding.shape_sha256 != shape_sha256(request)
                or binding.evidence_mode != "measured"):
            raise Held("RECEIVER_BINDING_MISMATCH")
        if binding.expires_epoch <= self.clock():
            raise Held("RECEIVER_BINDING_EXPIRED")
        # Resolve existing admission; never create a principal or enter receiver context.
        if hasattr(self.authority, "current_principal"):
            await self.authority.current_principal(binding.receiver_principal_id)
        else:
            self.authority.principal(binding.receiver_principal_id)
        return binding

    @staticmethod
    def basis(binding):
        return binding.model_dump(mode="json", exclude={"expires_epoch"})

    def contract(self, request, binding, dispatch):
        return HandoffContract_v0(
            handoff_id="ho_" + digest({"request": request.digest(), "operation": binding.operation_key,
                                      "fence": dispatch["seq"], "receiver": binding.receiver_principal_id}),
            what=request.kind + ":" + request.digest(), shape="ExecutionDelivery_v1:" + binding.shape_sha256,
            identity_source=HandoffActor(app="akki", role="author", actor_id=request.principal_id),
            identity_destination=HandoffActor(app=binding.receiver_app, role=binding.receiver_role,
                                             actor_id=binding.receiver_principal_id),
            receipt_kind="canonical execution_flow handoff_ack and receiver receipt",
            authored_at=datetime.fromtimestamp(dispatch["at_epoch"], timezone.utc).isoformat(),
            authored_by=request.principal_id)

    async def prepare(self, request, grant, dispatch):
        binding = await self.receiver(request, grant, dispatch)
        contract = self.contract(request, binding, dispatch)
        data = {"contract": contract.model_dump(mode="json"), "binding": self.basis(binding),
                "fence": dispatch["seq"], "operation_key": binding.operation_key}
        try:
            handoff = await self.journal.append(request, "handoff", data)
        except CommandConflict as exc:
            raise Held("HANDOFF_BASIS_CHANGED") from exc
        project(contract, self.directory)
        ack = typed(await bounded(self.provider.acknowledge, self.timeout_seconds, request, contract, binding,
                                  binding.operation_key, dispatch["seq"]), HandoffAck, "HANDOFF_ACK_INVALID")
        # Validate every cross-binding before persisting anything labelled an ACK.
        self.packet(request, grant, dispatch, contract, binding, ack, handoff["hash"], "0" * 64, "0" * 64, "0" * 64)
        if ack.expires_epoch <= self.clock():
            raise Held("HANDOFF_ACK_EXPIRED")
        rows = await self.journal.read(request)
        if not any(r["slot"] == "handoff_ack" for r in rows):
            try:
                await self.journal.append(request, "handoff_ack", {"ack": ack.model_dump(mode="json")})
            except CommandConflict:
                pass  # Another valid receipt won; current verified receipt is also banked below.
        check = await self.journal.append(request, "handoff_ack_check:" + digest(ack.model_dump(mode="json")),
                                          {"ack": ack.model_dump(mode="json")})
        return contract, binding, ack, handoff, check

    @staticmethod
    def packet(request, grant, dispatch, contract, binding, ack, handoff_ref, ack_ref, send_ref, eligibility_ref):
        try:
            return ExecutionDelivery(protocol="acknowledged_v1", request=request, authority=grant,
                                     operation_key=dispatch["data"]["operation_key"], fence=dispatch["seq"],
                                     contract=contract, binding=binding, acknowledgement=ack,
                                     handoff_ref=handoff_ref, ack_ref=ack_ref, send_ref=send_ref,
                                     eligibility_ref=eligibility_ref)
        except ValueError as exc:
            raise Held("HANDOFF_ACK_BINDING_INVALID") from exc

    async def revalidate(self, request, grant):
        rows = {r["slot"]: r for r in await self.journal.read(request)}
        if "handoff" not in rows or "dispatch" not in rows:
            raise Held("HANDOFF_NOT_RECORDED")
        binding = await self.receiver(request, grant, rows["dispatch"])
        if self.basis(binding) != rows["handoff"]["data"]["binding"]:
            raise Held("HANDOFF_BASIS_CHANGED")
        project(HandoffContract_v0.model_validate(rows["handoff"]["data"]["contract"]), self.directory)

    async def validate_result(self, request, result):
        rows = {r["slot"]: r for r in await self.journal.read(request)}
        if ("handoff" not in rows or "handoff_ack" not in rows or "send" not in rows
                or rows["send"]["data"].get("action") != "submit"
                or result.executor_id != rows["handoff"]["data"]["binding"]["receiver_principal_id"]):
            raise Held("EXECUTOR_RECEIVER_MISMATCH")