"""DAP Request Lifecycle · party_halted backend-only prorated compute billing (R-85 · TC-BLK-24).

Owner ruling FORK-CON-INGEST-3 verbatim: "TC-BLK-24 partial-compute-billed-
backend-only".

Journey v2 anchor verbatim (extraction_request_approval_journey_v2.md):

    L241: "**Partial compute on a halt is billed, prorated, entirely on the
    backend.** No DAP-21 receipt — that rule holds everywhere, unchanged.
    Billing exists as a separate backend ledger the party never sees a figure
    from, resolving what would otherwise be a real gap: the compose screen
    promises usage is counted for future billing, and an unmetered halt
    would have quietly broken that promise. Scoped to party-initiated halts
    only, not `check` or owner-triggered `suspended`."

    L260 (Resolved question): "yes, prorated, entirely on the backend. No
    DAP-21 receipt (that rule is unchanged everywhere), but billing is
    computed and recorded outside the party-facing receipt entirely — no
    figure ever appears on the party's screen, including in the Stop confirm
    itself. Scoped to party-initiated halts only; `check` and owner-triggered
    `suspended` (from `Executing`) are not the party's choice and aren't
    billed the same way — that distinction is implicit in this ruling and
    worth stating explicitly if it's ever questioned."

    L366 (Stop confirm on Executing surface): "**Stop** — a plain confirm,
    no reason asked: 'Stop this request? What's run so far will still be
    billed; nothing further will execute.' [...] No figure, percentage, or
    amount appears in this confirm or anywhere else the party sees;
    proration happens entirely on the backend."

    L402 (Explicitly excluded on party_halted drawer): "no figure,
    percentage, or billed amount anywhere on a party_halted block —
    proration happens entirely on the backend and is never shown to the
    party."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Final


# =============================================================================
# journey v2 L241 verbatim · rule constants · party-facing DAP-21 receipt is
# NOT emitted for party_halted · backend ledger only
# =============================================================================

PARTY_HALTED_EMITS_DAP21_RECEIPT: Final[bool] = False
PARTY_HALTED_BILLED_BACKEND_ONLY: Final[bool] = True
PARTY_HALTED_PARTY_FACING_FIGURE: Final[bool] = False


# =============================================================================
# Backend-only ledger entry structure · party never sees any of these fields
# =============================================================================


def record_party_halted_prorated_backend_billing(
    *,
    request_id: str,
    partial_compute_units: float,
    prorated_amount: float,
    halted_at_stage: str,
    halted_by: str,
) -> Dict[str, Any]:
    """Record a party-initiated halt as a backend-only prorated billing entry.

    Journey v2 L241 + L260 + L402 verbatim behavior:
    - No DAP-21 receipt (DAP-21 rule holds everywhere unchanged; party_halted
      is scoped OUT of DAP-21 metering).
    - Backend ledger entry emitted with `party_visible=False` and
      `no_dap21_receipt=True` so downstream reporting layers can enforce
      non-disclosure structurally rather than by convention.
    - Prorated amount is quantified in this backend record but MUST NEVER be
      surfaced to the party via any receipt, drawer, confirm, or notification.
    - Scoped to party-initiated halts only; check-kind and owner-triggered
      suspension have their own billing paths (not this module).

    Returns the backend ledger entry payload · caller (billing pipeline)
    persists it via the usual backend ledger surface (NOT via DAP-21
    receipt emission).
    """
    return {
        "request_id": request_id,
        "ledger_kind": "party_halted_prorated_backend",
        "partial_compute_units": partial_compute_units,
        "prorated_amount": prorated_amount,
        "halted_at_stage": halted_at_stage,
        "halted_by": halted_by,
        # Structural disclosure guards · fixed constants surface the rule:
        "party_visible": False,
        "no_dap21_receipt": PARTY_HALTED_EMITS_DAP21_RECEIPT is False,
        "billed_backend_only": PARTY_HALTED_BILLED_BACKEND_ONLY,
    }


# =============================================================================
# journey v2 L366 verbatim · Stop confirm copy on Executing surface
# =============================================================================


PARTY_HALT_STOP_CONFIRM_COPY: Final[str] = (
    "Stop this request? What's run so far will still be billed; nothing "
    "further will execute."
)


def render_stop_confirm_body(*, request_id: str) -> Dict[str, Any]:
    """Render the Stop confirm body per journey v2 L366 verbatim copy.

    No figure, percentage, or amount appears in this confirm (journey v2
    L366 + L402 verbatim). Only the fixed copy and the request_id are
    emitted at the party-facing surface.
    """
    return {
        "request_id": request_id,
        "confirm_copy": PARTY_HALT_STOP_CONFIRM_COPY,
        # Structural disclosure guards on the confirm payload:
        "figure_present": False,
        "percentage_present": False,
        "amount_present": False,
    }

