"""Explicit server-startup integration, never a key/admission factory of its own.

No configuration means no import, network request, local executor or invented root.
Configured factory code belongs to the admitted native runtime, not an HTTP body.
"""
import asyncio
import importlib
import inspect
import re
from dataclasses import dataclass
from services.activation.receipts import NativeReceipts
from services.activation.native_evidence import NativeEvidence
from services.activation.decisions import LedgerActivationDecisions
from services.activation.bounded_adapter import BoundedEngineAdapter
from services.northena.execution_bindings import ExecutionBindings
from services.northena.execution_gate_checks import finite_timeout


@dataclass(frozen=True)
class NativeExecutionBindings(ExecutionBindings):
    principal_lookup: object = None

    def __post_init__(self):
        super().__post_init__()
        if not inspect.iscoroutinefunction(self.principal_lookup):
            raise ValueError("Existing native principal lookup must be async.")


@dataclass(frozen=True)
class NativeRuntime:
    receipts: NativeReceipts
    bindings: NativeExecutionBindings
    evidence_timeout_seconds: float
    close: object = None

    def __post_init__(self):
        finite_timeout(self.evidence_timeout_seconds)
        if (not isinstance(self.receipts, NativeReceipts) or self.receipts.admitted_keys is None
                or not isinstance(self.bindings, NativeExecutionBindings)
                or not isinstance(self.bindings.decisions, LedgerActivationDecisions)
                or self.bindings.decisions.receipts is not self.receipts):
            raise ValueError("Native runtime components must share admitted receipt resolution.")
        if not self.bindings.executors or any(not isinstance(e, BoundedEngineAdapter) for e in self.bindings.executors.values()):
            raise ValueError("Every native executor must support signed bounded-runtime admission.")
        if self.bindings.eligibility is None:
            raise ValueError("Native eligibility must be bound.")
        if any(e.kind != "source" for e in self.bindings.executors.values()):
            if (self.bindings.handoffs is None or self.bindings.handoffs.provider is None
                    or self.bindings.eligibility.provider is None):
                raise ValueError("Model execution requires native eligibility and handoff providers.")
        if self.close is not None and not inspect.iscoroutinefunction(self.close):
            raise ValueError("Native provider shutdown must be async.")


async def install_runtime(app, db, environ):
    target = environ.get("AKKI_NATIVE_RUNTIME_FACTORY")
    timeout_value = environ.get("AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS")
    if target is None and timeout_value is None:
        return False
    runtime = None
    try:
        if not target or not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*:[A-Za-z_]\w*", target):
            raise ValueError("Invalid native startup configuration.")
        timeout = float(timeout_value)
        finite_timeout(timeout)
        module, name = target.split(":")
        factory = getattr(importlib.import_module(module), name)
        if not inspect.iscoroutinefunction(factory):
            raise ValueError("Native factory must be async.")
        runtime = await asyncio.wait_for(factory(db=db), timeout)
        if not isinstance(runtime, NativeRuntime) or runtime.receipts.db is not db:
            raise ValueError("Native providers must use the existing canonical ledger.")
        # Publish only the complete validated composition, never half of a binding.
        app.state.activation_receipts = runtime.receipts
        app.state.activation_evidence = NativeEvidence(runtime.receipts)
        app.state.activation_evidence_timeout_seconds = runtime.evidence_timeout_seconds
        app.state.execution_bindings = runtime.bindings
        app.state.native_runtime = runtime
        return True
    except Exception:
        if isinstance(runtime, NativeRuntime) and runtime.close is not None:
            try:
                await asyncio.wait_for(runtime.close(), runtime.evidence_timeout_seconds)
            except Exception:
                pass
        raise RuntimeError("NATIVE_RUNTIME_CONFIGURATION_INVALID") from None


async def close_runtime(app):
    runtime = getattr(app.state, "native_runtime", None)
    if runtime is not None and runtime.close is not None:
        try:
            await asyncio.wait_for(runtime.close(), runtime.evidence_timeout_seconds)
        except Exception:
            raise RuntimeError("NATIVE_RUNTIME_SHUTDOWN_FAILED") from None