"""services.entitlement_service_v1.allowance · ENT-22 derived allowance.

ENT-22 (§7 verbatim): "Credits are debited by computing metered tokens × the
row's credit rate at the time of the event, from the Ledger. Allowance
remaining is a derived value, recomputed from events, never a stored counter
that can drift from them."

ENT-21 (§7 verbatim): "The bill for a period is a query over the Ledger's
metered events for the licence. There is no second billing store. An invoice
line that cannot be derived from a receipted event does not exist." [B.4;
DAP-29]

This module is a pure derivation function. No stored counter, no cache, no
persisted balance. Every call recomputes from the input event list.

Sealed identity import: `contracts.dap.MeteredEvent` (DAP-21 · CCS3 W1.1
metered-event pin sha256 `b354818c…`). No new event type authored per ENT-20
verbatim ("No entitlement-specific event type exists").

ENT-49 discipline: the derived-view model authored here is named
`LicenceAllowanceState` (name prefix `Licence` compliant per §15 four-
allowed-shapes verbatim: licence field · catalog row · credential in the
plane · Ledger event). Structurally the view IS a per-call view over
`Licence.credits_per_seat_per_period × seat_count` reduced by the Ledger
event stream — semantically it is the licence's derived-allowance
projection, so binding the shape name to the `Licence` prefix is the
faithful classification. The view is NEVER persisted; it is a return-only
computation.
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# Sealed identity import per SO §3.8 additive-only
# contracts.dap.MeteredEvent is the DAP-21 sealed shape · CCS3 W1.1 pin
# `b354818c8147539f36d21c09bf0c7b43b1a53994b8cd57e2867694778d499b45`
from contracts.dap import MeteredEvent


class LicenceAllowanceState(BaseModel):
    """ENT-22 · Licence's derived allowance-remaining view. NOT a stored
    counter. Returned by `derive_allowance_remaining` on demand. Never
    persisted.

    Name prefix `Licence` per ENT-49 four-allowed-shapes discipline: the
    view IS the licence's per-period projection of allowance debits (a
    licence-field-derived computation over the Ledger event stream),
    faithfully classified under the `Licence` prefix.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    licence_terms_id: str = Field(..., min_length=1, description="ENT-7 terms identifier bound at derivation time.")
    period_iso: str = Field(..., min_length=1, description="ENT-6 period · e.g., '2026-09'.")
    credits_debited: int = Field(..., ge=0, description="Sum of debits (tokens × credit_rate) over the period's events.")
    credits_allowance: int = Field(..., ge=0, description="From Licence.credits_per_seat_per_period × seat_count OR org pool.")
    credits_remaining: int = Field(..., description="allowance − debited · signed so negatives are visible before ceiling refuses.")


def derive_allowance_remaining(
    *,
    licence_terms_id: str,
    period_iso: str,
    credits_allowance: int,
    ledger_events: List[MeteredEvent],
    credit_rate_by_terms_id: Optional[dict] = None,
) -> LicenceAllowanceState:
    """ENT-22 pure derivation of allowance remaining.

    Arguments:
      · licence_terms_id — ENT-7 terms identifier in force at derivation
      · period_iso       — ENT-6 period label to filter Ledger events by
      · credits_allowance — ENT-6 credits_per_seat_per_period × seat_count OR
                            organisation pool amount
      · ledger_events    — the sealed contracts.dap.MeteredEvent stream for
                            the licence over the period (queried by caller
                            from the Ledger surface · ENT-21 verbatim
                            'query over the Ledger's metered events')
      · credit_rate_by_terms_id — optional map of terms_id → credit_rate for
                            reseller-frontier rows (ENT-9 verbatim only
                            reseller-frontier rows carry credit_rate)

    Returns LicenceAllowanceState with credits_remaining = allowance − Σ(debits).
    A debit is: `event.quantity × credit_rate` for the terms_id in force at
    the event.

    NOTE: This function performs NO persistence side-effect. Every call
    recomputes from the input events. There is NO cached balance, NO
    stored counter, NO adjacent state.
    """
    rate_map = credit_rate_by_terms_id or {}
    total_debited = 0
    for event in ledger_events:
        # ENT-22 verbatim "metered tokens × the row's credit rate at the time"
        # ENT-7 verbatim "MUST NOT alter the terms identifier cited on any receipt"
        # · so the terms_id on the event dictates which credit_rate applies
        rate = rate_map.get(event.terms_id, 0)
        # `quantity` is the metered token count per DAP-21 field (accessed_scope
        # + quantity + quantity_unit); rate=0 means "not a reseller-frontier
        # row · no credits debited". A local-served row uses no credits.
        total_debited += int(event.quantity * rate)
    return LicenceAllowanceState(
        licence_terms_id=licence_terms_id,
        period_iso=period_iso,
        credits_debited=total_debited,
        credits_allowance=credits_allowance,
        credits_remaining=credits_allowance - total_debited,
    )
