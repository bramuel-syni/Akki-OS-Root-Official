"""DAP Request Lifecycle · state machine.

Spec verbatim (extraction_request_approval_journey.md · §4 rail states ·
L25/L55-58/L60/L91):
    - L25: "The instant a request is approved, it moves directly into Executing
      — there is no separate 'waiting to start' bucket."
    - L55: "Approved — moves immediately into Executing."
    - L56: "Refused — stops permanently. The reason is recorded and visible. A
      new request needs a fresh submission."
    - L57: "Expired — no decision before the 14-day review window closes.
      Distinct from Refused: nobody said no."
    - L58: "Blocked (only if a gate stops the request)."
    - L60: "Retrieved — the party retrieves it […]. The request is now closed
      out on this rail; it still counts toward Total."
    - L91: "A suspension-triggered block, DAP-27, is terminal wherever it lands
      — In Approval, Executing, or Ready — and doesn't resume when the
      suspension lifts."

Terminal states are exactly three: Refused / Blocked / Expired. Retrieved is
closed-out on the rail but still counted toward Total; per journey semantics it
is a rest state, not a terminal in the fail-closed sense.

Additive-only per SO §3.8.
"""

from __future__ import annotations

import enum
from typing import Iterable, Tuple


class RequestState(enum.Enum):
    """The 10 states of the DAP request lifecycle · flow (7) + terminals (3)."""

    Compose = "Compose"
    Submitted = "Submitted"
    Routing = "Routing"
    InApproval = "InApproval"
    Executing = "Executing"
    Ready = "Ready"
    Retrieved = "Retrieved"
    Refused = "Refused"
    Blocked = "Blocked"
    Expired = "Expired"
    # Q-UNLOCK sub-wave · owner ruling R-78 verbatim (2026-09-20T~13:00Z):
    #   "Q7 'Interrupted (platform fault)' — approve as a new non-terminal
    #    state. Right call not to overload check: check is a gate outcome
    #    with resubmit semantics, and a pod drop is neither."
    Interrupted = "Interrupted"

    # R-100 · CP-PORTAL-WRITE-SURFACE · additive request-level terminal state.
    # Owner ruling this-session verbatim (2026-09-21T~07:50Z condition 2):
    #   "A requester stopping their own executing request is not [DAP-27];
    #    it's a request-level terminal transition — Executing → Stopped —
    #    charged only to the point of the stop, receipted. ... The stop-
    #    confirm copy may be reused if its text is request-scoped; party_halt
    #    stays behind the owner surface. A requester must never be able to
    #    halt a party, including their own."
    # Additive-only precedent: R-78 Interrupted addition. Owner authorised
    # verbatim: "the state machine may need the additive Executing → Stopped
    # transition if it doesn't exist — additive only, verify first". Verified.
    Stopped = "Stopped"


TERMINAL_STATES: Tuple[RequestState, ...] = (
    RequestState.Refused,
    RequestState.Blocked,
    RequestState.Expired,
    # R-100 · CP-PORTAL-WRITE-SURFACE · additive request-level terminal.
    # Owner verbatim (2026-09-21T~07:50Z): "a request-level terminal
    # transition — Executing → Stopped — charged only to the point of the
    # stop, receipted." Fail-closed semantics per DAP-28 apply once Stopped.
    RequestState.Stopped,
)


ALLOWED_EDGES: Tuple[Tuple[RequestState, RequestState], ...] = (
    (RequestState.Compose, RequestState.Submitted),
    (RequestState.Submitted, RequestState.Routing),
    # Routing branches on touches-controlled-data (DAP-14 · touchesControlled prop):
    (RequestState.Routing, RequestState.InApproval),
    (RequestState.Routing, RequestState.Executing),
    # In Approval branches:
    (RequestState.InApproval, RequestState.Executing),
    (RequestState.InApproval, RequestState.Refused),
    (RequestState.InApproval, RequestState.Expired),
    # DAP-27 suspension while In Approval lands in terminal Blocked (journey L91):
    (RequestState.InApproval, RequestState.Blocked),
    # Executing branches:
    (RequestState.Executing, RequestState.Ready),
    # DAP-28 gate-stop-post-approval + DAP-27 suspension while Executing:
    (RequestState.Executing, RequestState.Blocked),
    # Ready branches:
    (RequestState.Ready, RequestState.Retrieved),
    # DAP-27 suspension while Ready lands in terminal Blocked (Q5 hard-hold placement,
    # superseded post-Q-unlock by escrow module · edge retained for terminal DAP-27):
    (RequestState.Ready, RequestState.Blocked),
    # Q-UNLOCK sub-wave · Q7 Interrupted (platform fault) new non-terminal state
    # (owner ruling R-78 verbatim):
    #   Executing → Interrupted (platform fault mid-execution)
    #   Interrupted → Executing (bounded auto-retry, DEFAULT 3 · re-runs every gate)
    #   Interrupted → Blocked   (exhaustion → Blocked·check per owner)
    (RequestState.Executing, RequestState.Interrupted),
    (RequestState.Interrupted, RequestState.Executing),
    (RequestState.Interrupted, RequestState.Blocked),
    # R-100 · CP-PORTAL-WRITE-SURFACE · additive request-scoped stop edge.
    # Owner ruling this-session verbatim (2026-09-21T~07:50Z condition 2):
    #   "Wire POST /requests/{id}/stop to that transition in the state
    #    machine." · request-level terminal transition Executing → Stopped
    #    · charged only to the point of the stop, receipted. Requester
    #    stops their own request only; party_halt stays behind the owner
    #    surface (DAP-27 remains owner-only).
    (RequestState.Executing, RequestState.Stopped),
)


class IllegalTransition(Exception):
    """Raised when a transition is not in ALLOWED_EDGES · fail-closed per DAP-28."""


def transition(from_state: RequestState, to_state: RequestState) -> RequestState:
    """Apply a transition. Fail-closed if the edge is not in ALLOWED_EDGES."""
    if (from_state, to_state) not in ALLOWED_EDGES:
        raise IllegalTransition(
            f"illegal transition {from_state.name} -> {to_state.name} · "
            f"edge not in ALLOWED_EDGES · fail-closed per DAP-28"
        )
    return to_state
