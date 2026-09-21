"""DAP Request Lifecycle · fail-closed placeholders + ruled-behavior gateways.

Owner ruling R-78 (2026-09-20T~13:00Z) unlocked Q1/Q2/Q4/Q5/Q7 · this
module now delegates ruled behaviors to dedicated Q-unlock service modules
while preserving the Q-marker surface for grep-discoverability. HARD HOLDs
(Q3 partial-release · Q6 owner-turnaround-line) remain as fail-closed
placeholders.

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, List


class NotYetSpecified(Exception):
    """Raised for any DAP-LIFECYCLE-Q question whose disposition is HARD HOLD."""


# Re-exported from blocked_kinds so consumers of fail_closed can grep in one place:
from services.dap_lifecycle.blocked_kinds import NonGateExecutionFaultNotYetSpecified  # noqa: F401,E402


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q1 · Retry after check block (RULED · owner R-78 verbatim)
#   Retry-for-check-only · hash-identical objective · same units · unexpired
#   approval · full gate re-run from failed stage · attempt counter ·
#   receipted attempts · bounded DEFAULT 3.
#   Ruled behavior lives at services.dap_lifecycle.retry_service · this
#   module keeps the marker surface for grep-discoverability.
# ---------------------------------------------------------------------------

def q1_retry_after_check_block_marker() -> str:
    """Return the Q1 marker string · ruled behavior at retry_service."""
    return "DAP-LIFECYCLE-Q1"


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q2 · Standing approval (RULED · owner R-78 verbatim)
#   DAP-16 satisfied if egress named · DAP-17 requires named units ·
#   Download standing-approval must name units AND operation ·
#   Connect approval never covers Download · redaction runs per release.
#   Ruled behavior lives at services.dap_lifecycle.approval_service.
# ---------------------------------------------------------------------------

STANDING_APPROVAL_BRANCH_REACHABLE_AT_RUNTIME: bool = True


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q3 · Partial release (HARD HOLD · not ruled)
# ---------------------------------------------------------------------------

def q3_partial_release(*, request_id: str) -> None:
    """Q3 HARD HOLD · Does a partial release exist as an outcome? ·
    All-or-nothing default · TC-RET-16 stays held."""
    raise NotYetSpecified(
        f"DAP-LIFECYCLE-Q3 · partial-release disposition for request "
        f"{request_id} · all-or-nothing default · see "
        "STATE/dap_lifecycle_pending_rulings.md · fail-closed"
    )


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q4 · Spend-ceiling breach (RULED · owner R-78 verbatim)
#   Folds into In Approval reason line · DAP-14's approval already carries
#   "the terms that would apply"; spend is one of them · one approval state,
#   not two.
# ---------------------------------------------------------------------------

def q4_spend_ceiling_breach(
    *,
    request_id: str,
    breach_amount: float,
    ceiling_amount: float,
) -> Dict[str, Any]:
    """Q4 RULED · folds spend-ceiling breach into In Approval reason line.

    Returns the drawer surface for In Approval with the spend reason line
    included. One approval state, not two.
    """
    return {
        "request_id": request_id,
        "new_state": "InApproval",
        "reason_line": (
            f"Spend for this request ({breach_amount:.2f}) would exceed the "
            f"party's ceiling ({ceiling_amount:.2f}). The reviewer sees the "
            "terms that would apply, including spend, per DAP-14."
        ),
        "one_approval_state": True,
        "separate_state": False,
        "banked_marker": "DAP-LIFECYCLE-Q4",  # for audit trail
    }


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q5 · Suspension-from-Ready (RULED · owner R-78 verbatim)
#   Output held in escrow on suspension · Ready-on-lift · termination
#   destruction = receipted Ledger event retaining artefact hash.
#   Ruled behavior lives at services.dap_lifecycle.escrow · this function
#   returns the escrow-entry summary.
# ---------------------------------------------------------------------------

def q5_suspension_from_ready(*, request_id: str) -> Dict[str, Any]:
    """Q5 RULED · returns escrow-entry summary on suspension from Ready.

    See services.dap_lifecycle.escrow for the full escrow lifecycle
    (hold-on-suspension · lift-to-Ready · terminate-and-destroy with hash).
    """
    return {
        "request_id": request_id,
        "escrowed": True,
        "ready_on_lift": True,
        "termination_destroys_but_retains_hash": True,
        "banked_marker": "DAP-LIFECYCLE-Q5",  # for audit trail
    }


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q6 · Owner turnaround line (HARD HOLD · not ruled)
# ---------------------------------------------------------------------------

Q6_OWNER_TURNAROUND_LINE_ENABLED: bool = False


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q7 · Non-gate execution fault (RULED as Interrupted state ·
# owner R-78 verbatim)
#   Interrupted (platform fault) new non-terminal state · bounded auto-retry
#   DEFAULT 3 · exhaustion → Blocked·check · visible on surface throughout.
#   Ruled behavior lives at services.dap_lifecycle.interrupted_service.
# ---------------------------------------------------------------------------

def q7_non_gate_execution_fault_marker() -> str:
    """Return the Q7 marker string · ruled behavior at interrupted_service."""
    return "DAP-LIFECYCLE-Q7"


# ---------------------------------------------------------------------------
# DAP-LIFECYCLE-Q8 · Destination removal · RATIFIED (owner R-78 verbatim)
#   BUILD TO YES-READING: removal blocks future use only · historical
#   receipts untouched (DAP-26 no-retroactive-change by analogy).
# ---------------------------------------------------------------------------

DESTINATION_REMOVAL_HISTORICAL_UNTOUCHED: bool = True
Q8_RATIFICATION_STATUS: str = "ratified_pending_full_ruling"


def apply_destination_removal(
    *,
    party_id: str,
    destination_id: str,
    historical_receipts: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Apply a destination removal.

    Under the DEFAULT-class YES-reading (owner R-78 ratified): future use is
    blocked; historical receipts remain byte-identical.
    """
    # Historical receipts are returned WITHOUT mutation:
    return {
        "party_id": party_id,
        "destination_id": destination_id,
        "future_use_blocked": True,
        "historical_receipts": historical_receipts,
        "historical_untouched": DESTINATION_REMOVAL_HISTORICAL_UNTOUCHED,
        "ratification_status": Q8_RATIFICATION_STATUS,
    }
