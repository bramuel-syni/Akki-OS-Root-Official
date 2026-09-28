"""services.n_series — CA1-N2 breach notification + CA1-N3 erasure.

STRUCTURAL SCAFFOLDING ONLY at W8 CP4. Both services refuse to fire
while any policy field is at OWNER_POLICY_PENDING. See
phase0/fidelity_ledger/FL-P4-W8-01.json for the seven policy
questions surfaced to the owner.

Fire path exists so W9 (Watch) has a binding point for CA1-N5
ledger continuity, but the service GATES until owner rules the
policy fields — an honest stop-and-report by mechanism, not by
skipping the mechanism.
"""
from services.n_series.breach import (
    fire_breach_notification,
    load_breach_notifications,
)
from services.n_series.erasure import (
    fire_erasure_request,
    load_erasure_requests,
)

__all__ = [
    "fire_breach_notification",
    "load_breach_notifications",
    "fire_erasure_request",
    "load_erasure_requests",
]
