"""DAP Request Lifecycle · suspension notices.

Owner ruling verbatim (STATE/DECISIONS.md R-78 · 2026-09-20T~13:00Z):
    "Suspension notices to org admin and affected submitters only —
    approve. Minimal disclosure, consistent with DAP-27."

DAP-27 (owner-verbatim companion): suspension is terminal in the lifecycle
sense but the notice envelope is minimal — org admin plus affected
submitters, nothing broader; and the notice body says only that this
party's request has been suspended · no estate-level context (DAP-35
non-disclosure of estate release budget still holds).

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple


def compute_notice_recipients(
    *,
    org_admin_id: str,
    affected_submitter_ids: Iterable[str],
    unaffected_org_member_ids: Iterable[str] = (),
) -> Tuple[str, ...]:
    """Compute the notice recipient set per owner R-78 minimal disclosure.

    - org admin: always included.
    - affected submitters: always included (those whose requests are
      suspended).
    - unaffected org members: NEVER included · minimal disclosure DAP-27.
    """
    recipients = {org_admin_id, *affected_submitter_ids}
    # Explicitly discard unaffected members even if some caller passes them.
    for uid in unaffected_org_member_ids:
        recipients.discard(uid)
    return tuple(sorted(recipients))


def render_suspension_notice(
    *,
    party_id: str,
    reason_kind: str,
) -> Dict[str, Any]:
    """Render the notice body per minimal-disclosure grammar.

    The body says only that this party's suspension has landed; no estate
    information, no cross-party leakage, no ceiling numbers, no other
    party data. Consistent with DAP-27 and DAP-35.
    """
    return {
        "party_id": party_id,
        "reason_kind": reason_kind,
        "body": (
            f"Your organisation's data-access request(s) have been suspended. "
            f"Please contact your account manager for follow-up."
        ),
        "estate_level_details_disclosed": False,
    }
