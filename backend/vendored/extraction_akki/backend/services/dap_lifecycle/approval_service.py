"""DAP Request Lifecycle · approval decision service + identity discipline.

Spec verbatim (extraction_request_approval_journey.md):
    - L25: "The instant a request is approved, it moves directly into Executing
      […] the approver's name is never shown to the party."
    - L26: "A decision (approved or declined) is permanent and recorded against
      the request. It cannot be reopened, appealed, or edited from this view."
    - L36: "The individual user who submitted, and who retrieved, is shown."
    - L212: "The approver's name is never shown to the party. In Approval
      already hides who is reviewing; approval and refusal show the date and
      the role ('the records authority at {{ dataOwner }}'), or the data owner
      alone when no role is named. The name stays in the platform's record.
      No initials or partial names."
    - L272: "A fixed permanence line: 'This decision is final and can't be
      reopened here. A new request needs a fresh submission.'"

Owner test-addition (this-session · verbatim):
    "the decision-service tests should assert the identity discipline from
    the journey spec — submitter identity recorded and surfaceable, approver
    identity NEVER surfaced to the party (role + data-owner name only),
    decisions permanent (no reopen path). Those three are testable now and
    are the spine of the approval surface."

Additive-only per SO §3.8. Consumers of this module for downstream ledger
writes must use the existing `services.request_context.ledger_actor_binding`
adapter per PRIN-10; this module records but does not write to any sealed
writer.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from services.dap_lifecycle.fail_closed import NotYetSpecified


# Journey L272 verbatim · fixed permanence line surfaced to party:
PERMANENCE_LINE_VERBATIM: str = (
    "This decision is final and can't be reopened here. "
    "A new request needs a fresh submission."
)


def record_decision(
    *,
    request_id: str,
    disposition: str,
    approver_id: str,
    approver_role: str,
    data_owner_name: str,
    reason: Optional[str],
) -> Dict[str, Any]:
    """Record a decision. Accepts 'accept' or 'refuse' only.

    DAP-LIFECYCLE-Q3 (partial release) is HARD HOLD — 'partial_release'
    disposition raises NotYetSpecified.

    The approver identity is stored on the record (approver_id) but the
    party-visible surface (`render_party_view_for_drawer`) never emits it.
    """
    if disposition == "accept":
        new_state = "Executing"
    elif disposition == "refuse":
        new_state = "Refused"
    elif disposition == "partial_release":
        raise NotYetSpecified(
            "DAP-LIFECYCLE-Q3 partial-release disposition is HARD HOLD · see "
            "STATE/dap_lifecycle_pending_rulings.md · all-or-nothing default."
        )
    else:
        raise NotYetSpecified(
            f"DAP-LIFECYCLE-Q3 · unknown decision disposition {disposition!r} · "
            "only 'accept' and 'refuse' are ruled at this wave · see "
            "STATE/dap_lifecycle_pending_rulings.md"
        )

    return {
        "request_id": request_id,
        "disposition": disposition,
        "new_state": new_state,
        "approver_id": approver_id,          # stored in record
        "approver_role": approver_role,      # party-visible via drawer render
        "data_owner_name": data_owner_name,  # party-visible via drawer render
        "reason": reason,
        "permanence_line": PERMANENCE_LINE_VERBATIM,
    }


def render_party_view_for_drawer(
    *,
    request_id: str,
    state: str,
    submitter_id: str,
    submitter_display_name: str,
    approver_id: Optional[str] = None,
    approver_display_name: Optional[str] = None,
    approver_role: Optional[str] = None,
    data_owner_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Render the party-facing drawer surface for a request.

    Identity discipline (journey L212):
        - submitter identity IS surfaced (name and display name emitted verbatim).
        - approver identity is NEVER surfaced (no name, no id, no initials, no
          partial names).
        - Sign-off line = "the {role} at {data_owner_name}" · or the data-owner
          alone when no role is named.
    """
    if approver_role and data_owner_name:
        signoff_line = f"the {approver_role} at {data_owner_name}"
    elif data_owner_name:
        signoff_line = data_owner_name
    else:
        signoff_line = ""

    return {
        "request_id": request_id,
        "state": state,
        "submitter_display_name": submitter_display_name,
        "submitter_line": f"submitted by {submitter_display_name}",
        "signoff_line": signoff_line,
        # NOTE: approver_id / approver_display_name are DELIBERATELY absent
        # from the returned dict per journey L212 identity discipline.
    }


# ============================================================================
# Q2 · Standing approval for Download (owner ruling R-78 · 2026-09-20T~13:00Z)
# ============================================================================
#
# Owner ruling verbatim:
#   "Q2 standing approval satisfies DAP-16 if it names the egress —
#   approve, tightened. DAP-17 already requires named units; for raw
#   download the standing approval must name the units and the operation.
#   A standing approval naming units for Connect does not cover Download.
#   Redaction runs per release regardless — approval never waives the gate."
#
# ============================================================================


def check_standing_approval_covers_operation(
    *,
    standing_approval_operations,
    standing_approval_units,
    requested_operation: str,
    requested_units,
) -> bool:
    """Return True iff the standing approval scope covers this request.

    Requires:
      - the requested operation is named in the standing approval's
        operations tuple, AND
      - every requested unit is named in the standing approval's units
        tuple.

    Connect approval never covers Download because a Connect-only
    operations tuple lacks `download`.
    """
    ops = set(standing_approval_operations or ())
    if requested_operation not in ops:
        return False
    unit_scope = set(standing_approval_units or ())
    for u in (requested_units or ()):
        if u not in unit_scope:
            return False
    return True


def redaction_gate_runs_per_release(
    *,
    standing_approval_covers: bool,
    release_number: int,
) -> bool:
    """Redaction runs per release regardless of approval scope.

    Owner verbatim: "Redaction runs per release regardless — approval
    never waives the gate." Returns True on every release (release_number
    is accepted for auditability; the answer does not depend on it).
    """
    _ = standing_approval_covers  # deliberately ignored per owner ruling
    _ = release_number
    return True
