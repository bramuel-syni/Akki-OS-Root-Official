"""Explicit runtime-limit capability without changing the original engine contract."""
import inspect
from dataclasses import dataclass
from services.northena.execution_ports import EngineAdapter


@dataclass(frozen=True)
class BoundedEngineAdapter(EngineAdapter):
    admit_limits_rpc: object = None

    def __post_init__(self):
        super().__post_init__()
        if not inspect.iscoroutinefunction(self.admit_limits_rpc):
            raise ValueError("An explicit async runtime-limit admission RPC is required.")