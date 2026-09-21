"""DAP Request Lifecycle · notification event-emission surface.

Spec verbatim (extraction_request_approval_journey.md):
    - L47: "A persistent inline note at the top of the blank draft reads
      'Submitted as FTN-2026-0121 — waiting for sign-off. Expires 3 Oct 2026 if
      no decision is made.' (or '— running now' for a request that skips
      approval, no expiry line)."
    - L48: "A toast fires alongside the note, not instead of it. Top-right, one
      line, 6 seconds, dismissible, pauses on hover: 'Submitted FTN-2026-0121 —
      waiting for sign-off' / '— running now', with a 'View' action."
    - L50: "On failure: nothing resets, nothing is added to the rail, no toast
      fires, the error shows inline in plain language, and the submit control
      re-enables."
    - L225: "A toast now fires on retrieval completion, mirroring the one already
      specified for submission — never on confirm, never on transfer start,
      never on failure."
    - L397: "A toast fires on completion, not on confirm or on transfer start:
      'Downloaded — FTN-2026-0120' (model/skill/data) or 'Report opened —
      FTN-2026-0111' (Get Intelligence, on first open)."

Owner scope directive (this-session verbatim): "Add the notification
event-emission surface to Phase 2/3 scope (toast events at submission +
retrieval per the journey spec; email as stub/queue behind flag OFF — DEFAULT-
class, already banked)."

Additive-only per SO §3.8. This module emits event records; the presentation
layer (frontend) renders them per the drawer/toast spec.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


# DEFAULT-class banking per drop manifest deliberately_deferred[0]:
#   "Org-admin status emails — submitter-only remains the current rule per
#   owner directive verbatim (product decision · nothing blocked)"
EMAIL_NOTIFICATIONS_ENABLED: bool = False
EMAIL_NOTIFICATIONS_CLASS: str = "DEFAULT"


def emit_request_submitted_notification(
    *,
    request_id: str,
    variant: str,  # "waiting_for_sign_off" or "running_now"
    window_ends_at_iso: Optional[str] = None,
) -> Dict[str, Any]:
    """Emit a toast notification for a fresh submission (journey L48).

    Toast text mirrors L48 verbatim. Duration = 6 seconds. Dismissible.
    Failure path (see L50) is caller's responsibility · this function is
    called ONLY on successful submission.
    """
    if variant == "waiting_for_sign_off":
        body = f"Submitted {request_id} — waiting for sign-off"
    elif variant == "running_now":
        body = f"Submitted {request_id} — running now"
    else:
        body = f"Submitted {request_id}"

    return {
        "kind": "toast",
        "event": "request_submitted",
        "request_id": request_id,
        "body": body,
        "duration_seconds": 6,
        "dismissible": True,
        "pauses_on_hover": True,
        "action_label": "View",
        "window_ends_at_iso": window_ends_at_iso,  # None for skips-approval variant
    }


def emit_request_retrieved_notification(
    *,
    request_id: str,
    mode: str,
    is_first_open: bool,
    is_completion: bool,
) -> Dict[str, Any]:
    """Emit a toast notification for retrieval completion (journey L225, L397).

    Never on confirm. Never on transfer start. Never on failure.
    Only when the transfer/first-open completes successfully.
    """
    if not is_completion:
        # Deliberately silent · not an error, just no emission.
        return {"kind": "none", "reason": "not_a_completion_event"}

    if mode == "get_intelligence_open_report" and is_first_open:
        body = f"Report opened — {request_id}"
    elif mode == "get_intelligence_open_report" and not is_first_open:
        # Re-opens are not metered but also do not emit toast (per journey L408).
        return {"kind": "none", "reason": "report_reopen_no_toast"}
    else:
        # download_model / download_skill / download_raw_data
        body = f"Downloaded — {request_id}"

    return {
        "kind": "toast",
        "event": "request_retrieved",
        "request_id": request_id,
        "body": body,
        "duration_seconds": 6,
        "dismissible": True,
        "pauses_on_hover": True,
        "action_label": "View",
    }


def emit_email_notification_stub(
    *,
    recipient: str,
    request_id: str,
    event: str,
) -> Dict[str, Any]:
    """Email notification stub · behind EMAIL_NOTIFICATIONS_ENABLED flag OFF at
    DEFAULT-class · returns dispatched=False, queued=False when disabled.

    No external side-effect (no SMTP call, no queue write). Callers may
    inspect the returned reason to log the disabled disposition.
    """
    if not EMAIL_NOTIFICATIONS_ENABLED:
        return {
            "dispatched": False,
            "queued": False,
            "reason": "email_notifications_disabled_default_class",
            "recipient": recipient,
            "request_id": request_id,
            "event": event,
        }

    # If ever enabled by ratification, this branch is where the queue write
    # would land · deliberately NOT implemented at this wave.
    return {
        "dispatched": False,
        "queued": True,
        "reason": "email_notifications_enabled_but_transport_not_implemented",
        "recipient": recipient,
        "request_id": request_id,
        "event": event,
    }
