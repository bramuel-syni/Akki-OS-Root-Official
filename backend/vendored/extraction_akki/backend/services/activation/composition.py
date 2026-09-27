"""Explicit owning-engine composition; no automatic trust/worker admission."""
from services.activation.receipts import NativeReceipts
from services.activation.native_evidence import NativeEvidence
from services.activation.decisions import LedgerActivationDecisions
from services.northena.execution_bindings import ExecutionBindings
from services.activation.timed_ports import TimedInspector


def native_activation_bindings(db, *, admitted_keys, inspector, executors, eligibility,
                               handoffs, timeout_seconds):
    if admitted_keys is None:
        raise ValueError("An existing estate-admitted key/provenance resolver is required.")
    receipts = NativeReceipts(db, admitted_keys, timeout_seconds=timeout_seconds)
    bindings = ExecutionBindings(decisions=LedgerActivationDecisions(receipts), inspector=TimedInspector(inspector, timeout_seconds),
        executors=executors, eligibility=eligibility, handoffs=handoffs,
        gate_timeout_seconds=timeout_seconds)
    return receipts, NativeEvidence(receipts), bindings