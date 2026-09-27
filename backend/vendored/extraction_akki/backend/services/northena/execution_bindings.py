"""Frozen server-only composition. Never accepted from HTTP or a model answer."""
import inspect
from dataclasses import dataclass
from types import MappingProxyType
from services.northena.execution_ports import EngineAdapter


@dataclass(frozen=True)
class ExecutionBindings:
    decisions: object
    inspector: object
    executors: object

    def __post_init__(self):
        if not inspect.iscoroutinefunction(getattr(self.decisions, "resolve", None)):
            raise ValueError("A server-owned async decision producer is required.")
        if not inspect.iscoroutinefunction(getattr(self.inspector, "inspect", None)):
            raise ValueError("A server-owned async artifact inspector is required.")
        try:
            bindings = dict(self.executors)
        except (TypeError, ValueError) as exc:
            raise ValueError("Executor bindings must be a mapping.") from exc
        for key, adapter in bindings.items():
            if not isinstance(adapter, EngineAdapter) or key not in (adapter.kind, (adapter.kind, adapter.engine)):
                raise ValueError("Executor binding must match its typed engine adapter.")
            allowed = {"source": {"mtafiti", "synisense"}, "skill": {"solva"},
                       "training": {"targeta"}, "evaluation": {"targeta"}}
            if adapter.kind not in allowed or adapter.engine not in allowed[adapter.kind]:
                raise ValueError("Executor binding must use the declared governing engine.")
        object.__setattr__(self, "executors", MappingProxyType(bindings))


def build_coordinator(db, bindings=None):
    # Local imports keep the composition boundary free of circular dependencies.
    from services.northena.execution_coordinator import Coordinator
    from services.northena.execution_journal import LedgerJournal
    from services.northena.execution_authority import ComponentAuthority
    from services.mtafiti.execution_registry import CanonicalRegistry
    from services.northena.execution_usage import LedgerUsagePublisher
    if bindings is not None and not isinstance(bindings, ExecutionBindings):
        raise ValueError("Execution bindings are server-owned typed configuration.")
    journal = LedgerJournal(db)
    authority = ComponentAuthority(db, decisions=bindings.decisions if bindings else None)
    return Coordinator(journal, authority, bindings.executors if bindings else {},
                       CanonicalRegistry(journal, authority, bindings.inspector if bindings else None),
                       usage_publisher=LedgerUsagePublisher(db, journal))