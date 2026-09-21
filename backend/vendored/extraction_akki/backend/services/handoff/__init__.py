"""services.handoff — CA1-009 generalized handoff contract registry.

Doc 15 §33 Promise #32: every cross-app crossing MUST be expressed
in a HandoffContract_v0 before it ships. Attest at cross-time.
"""
from services.handoff.contracts import (
    attest_handoff,
    load_handoffs,
    register_handoff,
)

__all__ = ["register_handoff", "load_handoffs", "attest_handoff"]
