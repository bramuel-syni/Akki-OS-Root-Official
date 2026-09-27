"""Pre-send native worker limit acknowledgement, persisted on the same journal."""
import asyncio
import json
from decimal import Decimal
from services.activation.approvals import approved_plan
from services.activation.reservations import Reservations
from services.activation.runtime_limits import RuntimeEnvelope
from services.activation.native_evidence import Observation
from services.activation.receipts import SignedReceipt
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


class WorkerLimitGate:
    def __init__(self, receipts):
        self.receipts = receipts

    async def admit(self, coordinator, request, executor, dispatch):
        plan, plan_ref, _, _, _ = await approved_plan(self.receipts, request)
        reservation_ref = await Reservations(self.receipts).reserve(plan, plan_ref)
        worker = await self.receipts.resolve(plan.worker_ref, kind="worker")
        if getattr(executor, "admit_limits_rpc", None) is None:
            raise Held("WORKER_LIMIT_ADMISSION_RPC_UNBOUND")
        existing = next((r for r in await coordinator.journal.read(request) if r["slot"] == "runtime_limits"), None)
        if existing:
            envelope = RuntimeEnvelope.model_validate_json(json.dumps(existing["data"]["envelope"]))
            ack_ref = existing["data"]["ack_ref"]
        else:
            start = int(self.receipts.clock())
            runtime = next(Decimal(q.quantity) for q in plan.limits if q.dimension == "wall_clock")
            end = min(request.deadline_epoch, start + int(runtime))
            if end - plan.termination_grace_seconds <= start:
                raise Held("TERMINATION_WINDOW_UNAVAILABLE")
            envelope = RuntimeEnvelope(protocol="akki.runtime.limits/1", request_sha256=request.digest(),
                plan_ref=plan_ref, reservation_ref=reservation_ref, runtime_id=worker.claims["runtime_id"],
                operation_key=dispatch["data"]["operation_key"], fence=dispatch["seq"],
                limits=plan.limits, starts_epoch=start, stop_work_by_epoch=end-plan.termination_grace_seconds,
                terminate_by_epoch=end)
            try:
                ack = await asyncio.wait_for(executor.admit_limits_rpc(request,
                    dispatch["data"]["operation_key"], dispatch["seq"], envelope), executor.timeout_seconds)
            except (TimeoutError, ConnectionError, OSError):
                raise Held("WORKER_LIMIT_ACK_UNAVAILABLE") from None
            if not isinstance(ack, SignedReceipt):
                raise Held("WORKER_LIMIT_ACK_INVALID")
            ack_ref = await self.receipts.record(ack)
        ack = await self.receipts.resolve(ack_ref, kind="observation", request_sha256=request.digest())
        proof = Observation.model_validate_json(json.dumps(ack.claims))
        if (ack.signer_id != worker.signer_id or proof.category != "runtime" or proof.evidence_mode != "measured"
                or proof.claim_sha256 != digest(envelope.model_dump(mode="json"))
                or proof.context_sha256 != request.digest() or envelope.plan_ref != plan_ref
                or envelope.reservation_ref != reservation_ref or envelope.limits != plan.limits
                or envelope.operation_key != dispatch["data"]["operation_key"] or envelope.fence != dispatch["seq"]
                or self.receipts.clock() >= envelope.stop_work_by_epoch):
            raise Held("WORKER_LIMIT_ACK_BINDING_MISMATCH")
        if existing is None:
            from services.ledger_writer.principal_control import CommandConflict
            try:
                await coordinator.journal.append(request, "runtime_limits", {
                    "envelope": envelope.model_dump(mode="json"), "ack_ref": ack_ref})
            except CommandConflict:
                # Reconcile the winning immutable admission, never send this loser.
                raise Held("WORKER_LIMIT_ADMISSION_RACE_RETRY") from None
        return ack_ref