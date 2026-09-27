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


class Coordinator:
    def __init__(self, journal, authority, executors, artifacts, clock=time.time):
        self.journal, self.authority = journal, authority
        self.executors, self.artifacts, self.clock = dict(executors), artifacts, clock

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
        executor = self.executors.get(request.kind)
        if executor is None:
            raise Held("EXECUTOR_ADAPTER_UNBOUND")
        submitted = False
        if dispatch is None:
            grant = await self.authorize(request, "dispatch")
            claim = {"operation_key": digest({"execution": request.request_id, "intent": request.digest()}),
                     "request_sha256": request.digest(), "nonce": uuid4().hex, "action": "submit",
                     "authority": grant.model_dump(mode="json")}
            try:
                dispatch = await self.journal.append(request, "dispatch", claim)
                submitted = True
            except CommandConflict:
                dispatch = next(row for row in await self.journal.read(request) if row["slot"] == "dispatch")
        if dispatch["data"].get("action") == "cancel":
            return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_DISPATCH", "unverified")
        # Resume an already observed terminal worker result without redoing its effect.
        observed = [row for row in rows if row["slot"].startswith("observation:")]
        prior = observed[-1]["data"]["result"] if observed else None
        if prior and prior["state"] in {"complete", "cancelled", "failed"}:
            result = WorkerResult.model_validate_json(json.dumps(prior))
        else:
            result = await self._worker(request, executor, dispatch, submitted)
            if result is None:
                return RunView(request_id=request.request_id, phase="unknown", reason_code="EXECUTOR_OUTCOME_UNCERTAIN")
        return await self.observe(request, result, dispatch)

    async def _worker(self, request, executor, dispatch, submitted):
        key, fence = dispatch["data"]["operation_key"], dispatch["seq"]
        try:
            if submitted:
                # Recheck after durable claim, before any external effect.
                grant = await self.authorize(request, "dispatch")
                if grant.model_dump(mode="json") != dispatch["data"]["authority"]:
                    raise Held("AUTHORITY_CHANGED_BEFORE_DISPATCH")
                current = await self.journal.read(request)
                if any(row["slot"] in {"terminal", "cancel_intent"} for row in current):
                    raise Held("CANCEL_OR_TERMINAL_BEFORE_DISPATCH")
                result = result_for(request, await executor.submit(request, key, fence, grant), dispatch)
                await self.bank_observation(request, result)
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
        previous = [row["data"]["result"] for row in await self.journal.read(request)
                    if row["slot"].startswith("observation:")]
        if any(row["executor_id"] != result.executor_id for row in previous):
            raise Held("EXECUTOR_IDENTITY_CHANGED")
        if previous and any(row["evidence_mode"] != result.evidence_mode for row in previous):
            raise Held("EXECUTION_EVIDENCE_MODE_CHANGED")
        data = result.model_dump(mode="json")
        return await self.journal.append(request, "observation:" + digest(data), {"result": data})

    async def observe(self, request, result, dispatch):
        result = result_for(request, result, dispatch)
        await self.bank_observation(request, result)
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
                    })
                except CommandConflict:
                    dispatch = next(row for row in await self.journal.read(request) if row["slot"] == "dispatch")
            if dispatch["data"].get("action") == "cancel":
                return await terminal(self, request, "cancelled", "CANCELLED_BEFORE_DISPATCH", "unverified")
            await self.authorize(request, "cancel")
            executor = self.executors.get(request.kind)
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
                await self.authorize(request, "retrieve")
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