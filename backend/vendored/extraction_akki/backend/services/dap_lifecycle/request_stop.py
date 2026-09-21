"""services.dap_lifecycle.request_stop · R-100 CP-PORTAL-WRITE-SURFACE.

Wave R-100 · additive-only per SO §3.8. Authors a NEW request-scoped stop
rendering module for the requester portal's POST /requests/{id}/stop.

Owner ruling this-session verbatim (2026-09-21T~07:50Z CONDITION 2):
    "The stop-confirm copy may be reused if its text is request-scoped;
     party_halt stays behind the owner surface. A requester must never be
     able to halt a party, including their own."

The confirm-copy TEXT already sealed in `party_halt_billing.py` at
`PARTY_HALT_STOP_CONFIRM_COPY` reads: "Stop this request? What's run so
far will still be billed; nothing further will execute." — this is
REQUEST-scoped (uses "this request", not "this party"), so per the owner
ruling MAY be reused. HOWEVER, importing directly from
`party_halt_billing` would functionally couple the requester portal to
the owner-only party_halt module — the invariant
`test_r100_condition2_stop_endpoint_never_imports_party_halt_billing`
forbids this coupling.

Resolution: this NEW module carries the request-scoped confirm-copy text
BYTE-VERBATIM (a pure-data restatement) and exposes
`render_request_stop_confirm_body(*, request_id)`. The party_halt module
stays intact and separate; the requester portal consumes this module
exclusively.

Standing bounds: additive-only per SO §3.8 · zero external I/O · zero
subprocess · deterministic pure-function surface.
"""

from __future__ import annotations

from typing import Any, Dict, Final


# BYTE-VERBATIM restatement of the request-scoped confirm-copy text
# originally sealed at `services.dap_lifecycle.party_halt_billing.
# PARTY_HALT_STOP_CONFIRM_COPY` per owner ruling this-session:
# "The stop-confirm copy may be reused if its text is request-scoped".
# This copy IS request-scoped (subject: "this request", not "this party").
REQUEST_STOP_CONFIRM_COPY: Final[str] = (
    "Stop this request? What's run so far will still be billed; nothing "
    "further will execute."
)


def render_request_stop_confirm_body(*, request_id: str) -> Dict[str, Any]:
    """Render the request-scoped Stop confirm body.

    CONDITION 2 owner ruling verbatim: request-level terminal transition
    Executing → Stopped, charged only to the point of the stop, receipted.
    A requester stopping their OWN executing request; NEVER party_halt.

    No figure, percentage, or amount appears in this confirm (matches the
    disclosure discipline of the party-halt path per journey v2 L366 +
    L402). Only the fixed request-scoped copy and the request_id are
    emitted at the party-facing surface.

    Structural disclosure guards on the confirm payload:
      · figure_present     = False
      · percentage_present = False
      · amount_present     = False

    These booleans are audit-visible receipts that no amount leaked into
    the confirm.
    """
    return {
        "request_id": request_id,
        "confirm_copy": REQUEST_STOP_CONFIRM_COPY,
        "figure_present": False,
        "percentage_present": False,
        "amount_present": False,
        "scope": "request",  # NEVER "party" · CONDITION 2 discipline
    }
