"""W-DAP-STACK 2F · DAP-28 fail-closed gate composer + DAP-29
unrecorded-extraction refusal.

Verbatim DAP-28 [FPT_FLS.1]: 'Every gate in DAP fails closed.  An
approval service that cannot be reached, a metering write that cannot
complete, a terms resolution that returns nothing, a ceiling check that
errors — each refuses the operation.  No path returns estate data, an
artefact, or a query result when a governing check could not complete.'

Verbatim DAP-29 [I-4 pattern]: 'A metered event that cannot be written
to the Ledger refuses the operation it meters.  An unrecorded
extraction is not permitted to have happened.'
"""

from __future__ import annotations

from typing import Callable, Optional

from contracts.dap import MeteredEvent
from services.dap import metering


class FailedClosed(RuntimeError):
    """DAP-28 / DAP-29 refusal marker.  Message names the anchor."""


def governed_operation(
    *,
    party_id: str,
    estate_id: str,
    custody_class: str,
    operation: str,
    proposed_quantity: float,
    approval_probe: Callable[..., bool],
    terms_probe: Callable[..., Optional[str]],
    ceiling_probe: Callable[..., bool],
) -> MeteredEvent:
    """Compose the four DAP-28 governing checks + DAP-21/DAP-29
    write-before-return.  Each failure raises `FailedClosed` naming the
    anchor.  No result is returned when any check fails."""

    # DAP-28 item 1 — approval service reachable + says True
    try:
        approved = approval_probe(
            party_id=party_id, estate_id=estate_id, operation=operation,
        )
    except Exception as exc:
        raise FailedClosed(
            f"DAP-28: approval service unreachable ({exc!r}); operation refused."
        ) from exc
    if not approved:
        raise FailedClosed(
            f"DAP-28: approval refused for party={party_id!r} op={operation!r}."
        )

    # DAP-28 item 3 — terms resolution returns something
    try:
        terms_id = terms_probe(
            estate_id=estate_id, custody_class=custody_class, party_id=party_id,
        )
    except Exception as exc:
        raise FailedClosed(
            f"DAP-28: terms resolution errored ({exc!r}); operation refused."
        ) from exc
    if not terms_id:
        raise FailedClosed(
            f"DAP-28: terms resolution returned nothing for estate={estate_id!r} "
            f"custody_class={custody_class!r} party={party_id!r}; operation refused."
        )

    # DAP-28 item 4 — ceiling check completes without error and passes
    try:
        within = ceiling_probe(
            estate_id=estate_id, party_id=party_id,
            proposed_quantity=proposed_quantity,
        )
    except Exception as exc:
        raise FailedClosed(
            f"DAP-28: ceiling check errored ({exc!r}); operation refused."
        ) from exc
    if not within:
        raise FailedClosed(
            f"DAP-28: ceiling exceeded for party={party_id!r}; operation refused."
        )

    # DAP-28 item 2 + DAP-29 — metered event write MUST complete or
    # operation is refused ('an unrecorded extraction is not permitted
    # to have happened').
    try:
        ev = metering.record_metered_event(
            operation_type=operation,
            accessed_scope=f"{estate_id}/{custody_class}",
            quantity=proposed_quantity,
            quantity_unit="units",
            terms_id=terms_id,
            party_id=party_id,
        )
    except Exception as exc:
        raise FailedClosed(
            f"DAP-28+DAP-29: metering write refused ({exc!r}); operation refused. "
            "An unrecorded extraction is not permitted to have happened."
        ) from exc

    return ev
