"""Bound native metadata providers without changing sealed engine consumers."""
import asyncio
from services.northena.execution_gate_checks import finite_timeout
from services.northena.execution_models import Held


class TimedInspector:
    def __init__(self, inspector, timeout_seconds):
        finite_timeout(timeout_seconds)
        if not asyncio.iscoroutinefunction(getattr(inspector, "inspect", None)):
            raise ValueError("An async native inspector is required.")
        self.inspector, self.timeout = inspector, timeout_seconds

    async def inspect(self, *args):
        try:
            return await asyncio.wait_for(self.inspector.inspect(*args), self.timeout)
        except (TimeoutError, ConnectionError, OSError):
            raise Held("NATIVE_INSPECTOR_UNAVAILABLE") from None