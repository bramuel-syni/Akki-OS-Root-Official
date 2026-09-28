"""DAP Request Lifecycle · Blocked 3-kind + Q7 non-gate execution fault.

Spec verbatim (extraction_request_approval_journey.md):
    - L30: "Two kinds, and the drawer states which: request (the request itself
      won't pass this gate — resubmitting it unchanged is blocked again) and
      check (a gate couldn't complete for reasons unrelated to the request).
      The approval stamp survives either way. […] A block caused by the
      estate's own release budget is a third kind, estate; its reason is
      deliberately uninformative, since DAP-35 prohibits disclosing anything
      about the estate's remaining budget."
    - L201: "Blocked has three kinds, not one flat state: request, check, estate."
    - L243: "The reason shown to the party on a Blocked (kind request or check)
      drawer is plain-language text the backend records at the time. Someone
      owns translating platform state into that text; the front end can't.
      (Kind estate is different and settled — its reason is deliberately fixed,
      uninformative copy, not backend-generated, per DAP-35.)"

Q7 disposition (STATE/DECISIONS.md R-77 · §6-hunt receipt banked):
    Blocked stays 3-kind. Non-gate execution fault surfaces as banked TODO
    marker fail-closed via NonGateExecutionFaultNotYetSpecified.

Additive-only per SO §3.8.
"""

from __future__ import annotations

import enum
from typing import Any, Dict


class BlockedKind(enum.Enum):
    """The 3 kinds of Blocked · request / check / estate."""

    request = "request"
    check = "check"
    estate = "estate"


# Journey L243 verbatim disposition · fixed uninformative copy for estate kind.
# DAP-35 prohibits disclosing anything about the estate's remaining budget.
ESTATE_BLOCK_FIXED_COPY: str = (
    "A release-budget check stopped this request. No further detail is disclosed."
)


class NonGateExecutionFaultNotYetSpecified(Exception):
    """Q7 HARD HOLD · non-gate execution fault has no ruled state · fail-closed."""


def surface_gate_fault(
    *,
    request_id: str,
    gate_name: str,
    kind: BlockedKind,
    plain_reason: str,
    approval_stamp: Dict[str, Any],
) -> Dict[str, Any]:
    """Surface a gate fault as a Blocked-drawer payload.

    - request / check kinds: backend-recorded plain_reason is emitted verbatim.
    - estate kind: plain_reason is DISCARDED and replaced with ESTATE_BLOCK_FIXED_COPY.
    - approval_stamp survives all three kinds (journey L30 verbatim).
    """
    if kind is BlockedKind.estate:
        party_visible_reason = ESTATE_BLOCK_FIXED_COPY
    else:
        party_visible_reason = plain_reason

    return {
        "request_id": request_id,
        "state": "Blocked",
        "kind": kind.value,
        "gate_name": gate_name,
        "party_visible_reason": party_visible_reason,
        "approval_stamp": approval_stamp,
        "approval_stamp_survives": True,
    }


def surface_non_gate_execution_fault(
    *,
    request_id: str,
    fault_description: str,
) -> None:
    """Q7 HARD HOLD placeholder for non-gate execution faults · fail-closed.

    Journey L247 verbatim (open question):
        "Does a non-gate execution fault exist as its own state? DAP-28 covers
        gates failing closed; it says nothing about a fault with no gate
        involved — a training job crashing mid-run for a reason unrelated to
        approval, redaction, metering, or the budget. If that's a real case,
        it may need a state Blocked doesn't cover, or Blocked needs a fourth
        kind. Unconfirmed either way."

    §6-hunt receipt: DAP-Spec §6 "Failure Posture" (DAP-28/29/30) confirms no
    fourth kind of Blocked · disposition STANDS · non-gate fault surfaces as
    banked TODO marker until owner rules.
    """
    raise NonGateExecutionFaultNotYetSpecified(
        f"DAP-LIFECYCLE-Q7 · non-gate execution fault surfaced for request "
        f"{request_id} · fault_description={fault_description!r} · "
        "spec §6 hunt receipt banked at "
        "phase0/spec_hunt_receipts/20260920T1200Z_dap_spec_section6_hunt.json · "
        "see STATE/dap_lifecycle_pending_rulings.md DAP-LIFECYCLE-Q7 · fail-closed"
    )
