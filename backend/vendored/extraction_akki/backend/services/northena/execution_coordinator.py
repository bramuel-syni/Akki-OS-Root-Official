"""Bounded metadata orchestration. No local compute, source reads or scheduler.

One submit claim; uncertainty resumes by stable-key status. Sink idempotency is
an adapter obligation, not a promise of exactly-once network execution.
"""
import json
import time
from uuid import uuid4

from services.ledger_writer.principal_control import CommandConflict
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held, RunView, WorkerResult, Usage
from services.northena.execution_validation import authority_for, result_for
from services.northena.execution_completion import complete, meter, terminal
from services.northena.execution_component_models import Prepared
from services.northena.execution_send import PROTOCOL, claim_send, cancel_unsent


class Coordinator:
    def __init__(self, journal, authority, executors, artifacts, clock=time.time, usage_publisher=None,
                 eligibility=None, handoffs=None, runtime_limits=None, governance=None):
        self.journal, self.authority = journal, authority
        self.executors, self.artifacts, self.clock = dict(executors), artifacts, clock
        self.usage_publisher = usage_publisher
        self.eligibility, self.handoffs = eligibility, handoffs
        self.runtime_limits = runtime_limits
        self.governance = governance

    async def check_inputs(self, request, phase):
        if self.governance is not None:
            await self.governance.check(request, phase)
        if self.eligibility is not None:
            return await self.eligibility.check(request, phase)

    async def release_gates(self, request, phase):
        grant = await self.authorize(request, phase)
        await self.check_inputs(request, phase)
        if request.kind != "source" and self.handoffs is not None:
            await self.handoffs.revalidate(request, grant)

    def executor_for(self, request):
        return self.executors.get((request.kind, request.engine), self.executors.get(request.kind))

    async def prepare(self, request):
        if hasattr(self.authority, "prepare"):
            prepared = await self.authority.prepare(request)
            if not isinstance(prepared, Prepared):
                raise Held("PREPARED_AUTHORITY_INVALID")
            prepared = Prepared.model_validate_json(prepared.model_dump_json())
            grant = authority_for(request, prepared.authority, self.clock(), "dispatch")
            return grant, prepared.commercial_snapshot.model_dump(mode="json")
        return await self.authorize(request, "dispatch"), None

    async def authorize(self, request, phase):
        return authority_for(request, await self.authority.authorize(request, phase), self.clock(), phase)

    def held(self, request, reason):
        return RunView(request_id=request.request_id, phase="held", reason_code=reason)

    async def remember(self, request):
        await self.journal.append(request, "request", {
            "request_sha256": request.digest(), "request": request.model_dump(mode="json")})

    async def advance(self, request):
        try:
            return await self._advance(request)
        except Held as exc:
            return self.held(request, exc.reason_code)

    async def _advance(self, request):
        await self.remember(request)
        rows = await self.journal.read(request)
        slots = {row["slot"]: row for row in rows}
        if "terminal" in slots:
            return await self.retrieve(request)
        if "cancel_intent" in slots:
            return await self.cancel(request)
        dispatch = slots.get("dispatch")
        if dispatch and dispatch["data"].get("action") == "cancel":
            return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_DISPATCH", "unverified")
        executor = self.executor_for(request)
        if executor is None:
            raise Held("EXECUTOR_ADAPTER_UNBOUND")
        submitted = False
        if dispatch is None:
            grant, commercial = await self.prepare(request)
            await self.check_inputs(request, "reserve")
            claim = {"operation_key": digest({"execution": request.request_id, "intent": request.digest()}),
                     "request_sha256": request.digest(), "nonce": uuid4().hex, "action": "submit",
                     "authority": grant.model_dump(mode="json"), "protocol": PROTOCOL}
            if commercial is not None:
                claim["commercial_snapshot"] = commercial
            try:
                dispatch = await self.journal.append(request, "dispatch", claim)
                submitted = True
            except CommandConflict:
                dispatch = next(row for row in await self.journal.read(request) if row["slot"] == "dispatch")
        if dispatch["data"].get("action") == "cancel":
            return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_DISPATCH", "unverified")
        # Resume an already observed terminal worker result without redoing its effect.
        observed = [row for row in rows if row["slot"].startswith("observation:")]
        locked = slots.get("worker_outcome") or slots.get("worker_terminal")
        prior = locked["data"]["result"] if locked else observed[-1]["data"]["result"] if observed else None
        if prior and prior["state"] in {"complete", "cancelled", "failed"}:
            result = WorkerResult.model_validate_json(json.dumps(prior))
        else:
            result = await self._worker(request, executor, dispatch, submitted)
            if result is None:
                return RunView(request_id=request.request_id, phase="unknown", reason_code="EXECUTOR_OUTCOME_UNCERTAIN")
        return await self.observe(request, result, dispatch)

    async def _worker(self, request, executor, dispatch, submitted):
        key, fence = dispatch["data"]["operation_key"], dispatch["seq"]
        submitted, packet = await claim_send(self, request, executor, dispatch)
        try:
            if submitted:
                if packet is not None:
                    value = await executor.submit_delivery(packet)
                else:
                    from services.northena.execution_models import Authority
                    grant = Authority.model_validate_json(json.dumps(dispatch["data"]["authority"]))
                    value = await executor.submit(request, key, fence, grant)
                result = result_for(request, value, dispatch)
                if request.kind != "source" and self.handoffs is not None:
                    await self.handoffs.validate_result(request, result)
                result = await self.bank_observation(request, result)
                if result.state not in {"accepted", "running"}:
                    return result
            # One bounded status RPC, never an in-process polling loop.
            await self.authorize(request, "observe")
            return await executor.status(request, key, fence)
        except (TimeoutError, ConnectionError, OSError):
            await self.journal.append(request, "uncertain:dispatch", {
                "operation_key": key, "fence": fence, "reason_code": "EXECUTOR_OUTCOME_UNCERTAIN"})
            return None

    async def bank_observation(self, request, result):
        rows = await self.journal.read(request)
        previous = [row["data"]["result"] for row in rows
                    if row["slot"].startswith("observation:")]
        if any(row["executor_id"] != result.executor_id for row in previous):
            raise Held("EXECUTOR_IDENTITY_CHANGED")
        if previous and any(row["evidence_mode"] != result.evidence_mode for row in previous):
            raise Held("EXECUTION_EVIDENCE_MODE_CHANGED")
        from services.northena.execution_observations import guard_terminal
        result = await guard_terminal(self.journal, request, result, rows)
        data = result.model_dump(mode="json")
        await self.journal.append(request, "observation:" + digest(data), {"result": data})
        return result

    async def observe(self, request, result, dispatch):
        result = result_for(request, result, dispatch)
        if request.kind != "source" and self.handoffs is not None:
            await self.handoffs.validate_result(request, result)
        result = await self.bank_observation(request, result)
        if result.state == "complete":
            return await complete(self, request, result, dispatch)
        if result.state in {"cancelled", "failed"}:
            await meter(self, request, result, dispatch)
            return await terminal(self, request, result.state, "EXECUTOR_" + result.state.upper(), result.evidence_mode)
        return RunView(request_id=request.request_id,
                       phase="unknown" if result.state == "unknown" else "running",
                       reason_code="EXECUTOR_" + result.state.upper(), evidence_mode=result.evidence_mode)

    async def cancel(self, request):
        try:
            await self.remember(request)
            slots = {row["slot"]: row for row in await self.journal.read(request)}
            if "terminal" in slots:
                return await self.retrieve(request)
            await self.journal.append(request, "cancel_intent", {"request_sha256": request.digest()})
            dispatch = slots.get("dispatch")
            if dispatch is None:
                # The same atomic slot arbitrates submit versus pre-dispatch cancel.
                # A terminal check followed by an unrelated claim is NOT sufficient.
                try:
                    dispatch = await self.journal.append(request, "dispatch", {
                        "action": "cancel", "request_sha256": request.digest(),
                        "operation_key": digest({"execution": request.request_id, "intent": request.digest()}),
                        "protocol": PROTOCOL,
                    })
                except CommandConflict:
                    dispatch = next(row for row in await self.journal.read(request) if row["slot"] == "dispatch")
            if dispatch["data"].get("action") == "cancel":
                await cancel_unsent(self, request, dispatch)
                return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_DISPATCH", "unverified")
            if await cancel_unsent(self, request, dispatch):
                return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_SEND", "unverified")
            await self.authorize(request, "cancel")
            executor = self.executor_for(request)
            if executor is None:
                raise Held("EXECUTOR_ADAPTER_UNBOUND")
            result = await executor.cancel(request, dispatch["data"]["operation_key"], dispatch["seq"])
            return await self.observe(request, result, dispatch)
        except Held as exc:
            return self.held(request, exc.reason_code)
        except (TimeoutError, ConnectionError, OSError):
            return RunView(request_id=request.request_id, phase="unknown", reason_code="CANCEL_ACKNOWLEDGEMENT_UNCERTAIN")

    async def retrieve(self, request):
        try:
            rows = await self.journal.read(request)
            final = next((row for row in rows if row["slot"] == "terminal"), None)
            if final is None:
                raise Held("VERIFIED_RESULT_NOT_AVAILABLE")
            data = final["data"]
            if data["phase"] == "ready":
                await self.release_gates(request, "retrieve")
                if hasattr(self.artifacts, "revalidate"):
                    await self.artifacts.revalidate(request, tuple(data["artifact_refs"]))
            return RunView(request_id=request.request_id, phase=data["phase"], reason_code=data["reason_code"],
                           evidence_mode=data["evidence_mode"], artifact_refs=tuple(data["artifact_refs"]),
                           terms_ref=data.get("terms_ref"),
                           usage=tuple(Usage(**item) for item in data["usage"]) if data.get("usage") is not None else None)
        except Held as exc:
            return self.held(request, exc.reason_code)

    async def view(self, request):
        rows = await self.journal.read(request)
        if any(row["slot"] == "terminal" for row in rows):
            return await self.retrieve(request)
        if any(row["slot"] == "dispatch" for row in rows):
            return RunView(request_id=request.request_id, phase="unknown", reason_code="EXECUTOR_RECONCILIATION_REQUIRED")
        return self.held(request, "EXECUTION_NOT_DISPATCHED")