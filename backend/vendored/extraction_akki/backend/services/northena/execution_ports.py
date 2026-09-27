"""Server-owned adapters for bounded metadata RPCs to Akki-owned elements.

Not a public plugin/admission registry. No callback/default invokes a local model
or source. Existing sealed remote transports are supplied by their owning engine.
"""
import asyncio
import inspect
import json
from dataclasses import dataclass
from services.northena.execution_models import Held, WorkerResult


@dataclass(frozen=True)
class EngineAdapter:
    kind: str
    engine: str
    submit_rpc: object
    status_rpc: object
    cancel_rpc: object
    timeout_seconds: float

    def __post_init__(self):
        if (type(self.timeout_seconds) not in (float, int)
                or not 0 < self.timeout_seconds < float("inf")):
            raise ValueError("A measured/configured finite RPC timeout is required.")
        if not all(inspect.iscoroutinefunction(f) for f in (self.submit_rpc, self.status_rpc, self.cancel_rpc)):
            raise ValueError("Adapters require async metadata RPCs, not local workload functions.")

    async def _call(self, fn, request, key, fence, *args):
        if (request.kind, request.engine) != (self.kind, self.engine):
            raise Held("ENGINE_BINDING_MISMATCH")
        value = await asyncio.wait_for(fn(request, key, fence, *args), timeout=self.timeout_seconds)
        result = WorkerResult.model_validate_json(
            value.model_dump_json() if isinstance(value, WorkerResult) else json.dumps(value))
        if result.evidence_mode != "measured":
            raise Held("MOCKED_EXECUTOR_NOT_ADMITTED")
        return result

    async def submit(self, request, operation_key, fence, authority):
        return await self._call(self.submit_rpc, request, operation_key, fence, authority)

    async def status(self, request, operation_key, fence):
        return await self._call(self.status_rpc, request, operation_key, fence)

    async def cancel(self, request, operation_key, fence):
        return await self._call(self.cancel_rpc, request, operation_key, fence)