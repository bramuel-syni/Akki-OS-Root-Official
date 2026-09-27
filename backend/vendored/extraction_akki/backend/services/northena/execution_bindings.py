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
    eligibility: object = None
    handoffs: object = None
    gate_timeout_seconds: float | None = None

    def __post_init__(self):
        from services.northena.execution_eligibility import InputEligibility
        from services.mkondo.execution_handoff import MkondoHandoff
        from services.northena.execution_gate_checks import finite_timeout
        if self.eligibility is not None and not isinstance(self.eligibility, InputEligibility):
            raise ValueError("Eligibility must use the native receipt gate.")
        if self.handoffs is not None and not isinstance(self.handoffs, MkondoHandoff):
            raise ValueError("Handoffs must use the native Mkondo gate.")
        if self.eligibility is not None or self.handoffs is not None or self.gate_timeout_seconds is not None:
            finite_timeout(self.gate_timeout_seconds)
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
    from services.northena.execution_eligibility import InputEligibility
    from services.mkondo.execution_handoff import UnboundHandoff
    if bindings is not None and not isinstance(bindings, ExecutionBindings):
        raise ValueError("Execution bindings are server-owned typed configuration.")
    journal = LedgerJournal(db)
    lookup = getattr(bindings, "principal_lookup", None)
    authority = ComponentAuthority(db, decisions=bindings.decisions if bindings else None,
                                   **({"principal_lookup": lookup} if lookup is not None else {}))
    eligibility = (bindings.eligibility.bind(journal, bindings.gate_timeout_seconds)
                   if bindings and bindings.eligibility else InputEligibility(journal))
    handoffs = (bindings.handoffs.bind(journal, authority, bindings.gate_timeout_seconds)
                if bindings and bindings.handoffs else UnboundHandoff())
    from services.activation.decisions import LedgerActivationDecisions
    from services.activation.worker_gate import WorkerLimitGate
    runtime_limits = (WorkerLimitGate(bindings.decisions.receipts)
                      if bindings and isinstance(bindings.decisions, LedgerActivationDecisions) else None)
    from services.non_gpu_governance.gate import NativeGovernance
    governance = (NativeGovernance(bindings.decisions.receipts, journal) if runtime_limits else None)
    return Coordinator(journal, authority, bindings.executors if bindings else {},
                       CanonicalRegistry(journal, authority, bindings.inspector if bindings else None),
                       usage_publisher=LedgerUsagePublisher(db, journal),
                       eligibility=eligibility, handoffs=handoffs, runtime_limits=runtime_limits,
                       governance=governance)