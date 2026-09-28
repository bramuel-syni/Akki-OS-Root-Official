"""DAP Request Lifecycle · Retrieval → MeteredEvent wiring (DAP-21).

Spec verbatim (extraction_request_approval_journey.md):
    - L60: "Retrieval is not one-shot for every mode: a report stays openable
      indefinitely with no new receipt, and a model, skill, or data package can
      be downloaded again — each repeat is its own metered event with its own
      receipt (DAP-21), never a silent re-pull."
    - L149: "flips to Retrieved […] only on verified checksum match."
    - L150: "Retrieved cards keep an action for three of the four modes. Get
      Intelligence keeps Open report (re-opening is never a new event).
      Model/skill/data show Download again instead — no one-shot confirm this
      time, since the original one-shot already happened; each press is its own
      metered event with its own receipt."
    - L408: "Get Intelligence keeps Open report on both the card and here —
      reading again is never a new event, never a new receipt, no toast beyond
      the one on first open."

DAP-Spec §6 (Failure Posture):
    - DAP-29: "A metered event that cannot be written to the Ledger refuses
      the operation it meters. An unrecorded extraction is not permitted to
      have happened."

Additive-only per SO §3.8. This module composes but does not edit the sealed
`contracts.dap.MeteredEvent` shape (per CCS3 seal `379e455` DAP-21 pin
`b354818c8147539f36d21c09bf0c7b43b1a53994b8cd57e2867694778d499b45`).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class ReportReopenIsNotAMeteredEvent(Exception):
    """Journey L408: Get Intelligence report re-open is never a new metered event."""


class ChecksumNotVerified(Exception):
    """Journey L149: Ready → Retrieved fires only on verified checksum match · fail-closed."""


class LedgerWriteRefused(Exception):
    """DAP-29: a metered event that cannot be written to the Ledger refuses the operation."""


_GET_INTELLIGENCE_MODE: str = "get_intelligence_open_report"


def emit_retrieval_metered_event(
    *,
    request_id: str,
    mode: str,
    party_id: str,
    terms_id: str,
    quantity: int,
    quantity_unit: str,
    checksum_verified: bool,
    is_first_open: Optional[bool] = None,
    ledger_writer_stub_status: str = "ok",
) -> Dict[str, Any]:
    """Emit a MeteredEvent for a retrieval on the single chain (DAP-21).

    Rules:
        - Report re-open (mode=get_intelligence_open_report, is_first_open=False):
          raises ReportReopenIsNotAMeteredEvent · no metered event, no receipt.
        - Report first open (is_first_open=True): emits one metered event.
        - model / skill / data download completion (checksum_verified=True):
          emits one metered event per completion (repeats included).
        - checksum_verified=False on a download mode: raises ChecksumNotVerified.
        - ledger_writer_stub_status='unreachable': raises LedgerWriteRefused (DAP-29).
    """
    # DAP-29: fail-closed on ledger unreachable BEFORE anything else can proceed.
    if ledger_writer_stub_status == "unreachable":
        raise LedgerWriteRefused(
            f"DAP-29 · Ledger unreachable for request {request_id} · "
            "unrecorded extraction is not permitted to have happened · fail-closed"
        )

    if mode == _GET_INTELLIGENCE_MODE:
        # Report modes: first open only emits a metered event.
        if is_first_open is False:
            raise ReportReopenIsNotAMeteredEvent(
                f"Get Intelligence report re-open for request {request_id} · "
                "reading again is never a new event (journey L408) · no receipt written"
            )
        # is_first_open True or None (defaulted first-open) proceeds.
    else:
        # Download modes require checksum verification per journey L149.
        if not checksum_verified:
            raise ChecksumNotVerified(
                f"Ready → Retrieved requires verified checksum match for request "
                f"{request_id} mode {mode!r} · fail-closed"
            )

    # Shape mirrors sealed contracts.dap.MeteredEvent (7 required fields per
    # CCS3 W1.2 pin) · this module composes, it does not edit the sealed shape.
    return {
        "operation_type": "retrieval",
        "accessed_scope": f"request:{request_id}:{mode}",
        "quantity": quantity,
        "quantity_unit": quantity_unit,
        "terms_id": terms_id,
        "party_id": party_id,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "mode": mode,
        "request_id": request_id,
    }
