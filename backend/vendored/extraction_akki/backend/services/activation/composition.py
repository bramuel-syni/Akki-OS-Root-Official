"""Explicit owning-engine composition; no automatic trust/worker admission."""
from services.activation.receipts import NativeReceipts
from services.activation.native_evidence import NativeEvidence
from services.activation.decisions import LedgerActivationDecisions
from services.northena.execution_bindings import ExecutionBindings
from services.activation.timed_ports import TimedInspector


def native_activation_bindings(db, *, admitted_keys, inspector, executors, eligibility,
                               handoffs, timeout_seconds, principal_lookup=None):
    if admitted_keys is None:
        raise ValueError("An existing estate-admitted key/provenance resolver is required.")
    receipts = NativeReceipts(db, admitted_keys, timeout_seconds=timeout_seconds)
    from services.activation.runtime_binding import NativeExecutionBindings
    binding_type = NativeExecutionBindings if principal_lookup is not None else ExecutionBindings
    extra = {"principal_lookup": principal_lookup} if principal_lookup is not None else {}
    bindings = binding_type(decisions=LedgerActivationDecisions(receipts), inspector=TimedInspector(inspector, timeout_seconds),
        executors=executors, eligibility=eligibility, handoffs=handoffs,
        gate_timeout_seconds=timeout_seconds, **extra)
    return receipts, NativeEvidence(receipts), bindings