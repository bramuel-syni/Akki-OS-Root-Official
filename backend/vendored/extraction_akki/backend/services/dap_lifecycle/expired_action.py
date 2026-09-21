"""DAP Request Lifecycle · Expired action surface.

Owner ruling verbatim (STATE/DECISIONS.md R-78 · 2026-09-20T~13:00Z):
    "One value you set fills a gap the spec genuinely had: the 14-day
    expiry with working-day roll-forward. Ratified, DEFAULT-class, and it
    closes the 'no duration stated' finding from earlier. Pair it with the
    requester's recourse the spec was also silent on: Expired offers
    Submit again as a new request, never a reopen."

Additive-only per SO §3.8.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Tuple


def available_actions_for_expired(*, request_id: str) -> Tuple[str, ...]:
    """Return the actions available to a party on an Expired request.

    Owner verbatim: "Submit again as a new request, never a reopen."
    """
    return ("submit_again_as_new_request",)


def submit_again_as_new_request(*, expired_request_id: str) -> Dict[str, Any]:
    """Create a brand-new request seeded from an expired one.

    Owner verbatim: "never a reopen". The new request gets a fresh id;
    the previous id is retained only as a reference, not as a resumption.
    """
    new_request_id = f"FTN-2026-{uuid.uuid4().hex[:8].upper()}"
    return {
        "new_request_id": new_request_id,
        "previous_request_id_reference": expired_request_id,
        "is_reopen": False,
        "seeded_from_expired": True,
    }
