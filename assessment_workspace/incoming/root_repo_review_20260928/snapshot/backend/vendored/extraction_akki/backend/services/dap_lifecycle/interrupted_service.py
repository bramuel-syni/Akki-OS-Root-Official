"""DAP Request Lifecycle · Q7 Interrupted (platform fault) state handler.

Owner ruling verbatim (STATE/DECISIONS.md R-78 · 2026-09-20T~13:00Z):
    "Q7 'Interrupted (platform fault)' — approve as a new non-terminal
    state. Right call not to overload check: check is a gate outcome with
    resubmit semantics, and a pod drop is neither. Auto-retry is permitted
    because it's not a gate bypass — every gate re-runs on retry, output is
    never partial, attempts are bounded (DEFAULT 3, receipted), and
    exhaustion resolves to Blocked · check. The interruption is visible on
    the surface throughout."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict


INTERRUPTED_MAX_ATTEMPTS_DEFAULT: int = 3


def handle_platform_fault(
    *,
    request_id: str,
    attempt_number: int,
    fault_description: str,
) -> Dict[str, Any]:
    """Handle an interrupted (platform-fault) request.

    Rules (owner R-78):
        - Attempts 1..N (N=INTERRUPTED_MAX_ATTEMPTS_DEFAULT=3): auto-retry
          to Executing · re-runs every gate · output never partial · each
          attempt is receipted.
        - Attempt N+1 (beyond bound): exhaustion resolves to Blocked·check.
    """
    if attempt_number <= INTERRUPTED_MAX_ATTEMPTS_DEFAULT:
        return {
            "request_id": request_id,
            "attempt_number": attempt_number,
            "disposition": "auto_retry",
            "next_state": "Executing",
            "re_runs_all_gates": True,
            "output_partial": False,
            "receipted": True,
            "fault_description": fault_description,
        }

    # Exhaustion: owner verbatim "exhaustion resolves to Blocked · check".
    return {
        "request_id": request_id,
        "attempt_number": attempt_number,
        "disposition": "exhausted",
        "next_state": "Blocked",
        "blocked_kind": "check",
        "re_runs_all_gates": True,
        "output_partial": False,
        "receipted": True,
        "fault_description": fault_description,
    }


def surface_visibility_for_interrupted(
    *,
    request_id: str,
    attempt_number: int,
) -> Dict[str, Any]:
    """Render the surface visibility for an Interrupted request.

    Owner verbatim: "The interruption is visible on the surface throughout."
    """
    return {
        "request_id": request_id,
        "state": "Interrupted",
        "visible_on_surface": True,
        "surface_line": (
            f"This request is being retried after a platform interruption. "
            f"Attempt {attempt_number} of {INTERRUPTED_MAX_ATTEMPTS_DEFAULT}."
        ),
    }
