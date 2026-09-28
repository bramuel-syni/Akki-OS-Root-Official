"""services.request_context.ledger_actor_binding — PRIN-12 adapter.

PRIN-12 verbatim (spec §5): 'The Ledger's `actor` field is populated
only from propagated principal context, never from a caller-supplied
string.  Existing entries written before this component exists are not
retroactively altered — the fix is prospective, consistent with how
every other prospective-only correction in this canon has been
handled.'

Owner reminder this-session verbatim: 'the Ledger actor-string upgrade
(real principal semantics) ... keep them additive (wrappers/adapters),
and if any sealed writer needs its actor semantics upgraded in place,
that's a fork, not an edit.'

This module is a wrapper/adapter, NOT an in-place edit to
`services.memory.ledger.append_row` or any other sealed writer.
Consumers that want the new discipline call `write_ledger_row` here;
existing consumers of the sealed writer continue to work under the
prospective-only correction rule.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from services.request_context.context import (
    PrincipalContextAbsent,
    current_principal_id,
)


class CallerSuppliedActorRefused(RuntimeError):
    """PRIN-12 refusal exception.

    Raised when a caller attempts to supply the ledger `actor` field
    directly.  The actor is populated ONLY from propagated principal
    context; a caller-supplied string bypasses the propagation gate
    and is refused fail-closed.
    """


def write_ledger_row(
    data_class: str,
    caller_supplied_actor: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """PRIN-12 verbatim: 'The Ledger's `actor` field is populated only
    from propagated principal context, never from a caller-supplied
    string.'

    If a caller passes `caller_supplied_actor`, the write is refused.
    Otherwise the actor is drawn from the propagated context via
    `current_principal_id()`; if the context is absent, the write is
    also refused (PRIN-11 fail-closed kinship).
    """

    if caller_supplied_actor is not None:
        raise CallerSuppliedActorRefused(
            "PRIN-12 · ledger write refused: `actor` is populated only "
            "from propagated principal context, never from a "
            "caller-supplied string.  Enter propagation via "
            "`services.request_context.enter_propagation(principal_id)` "
            "before writing."
        )
    actor = current_principal_id()
    if actor is None:
        raise PrincipalContextAbsent(
            "PRIN-12 · ledger write refused: no principal in calling "
            "context, and PRIN-12 forbids caller-supplied actors."
        )
    return {
        "data_class": data_class,
        "actor": actor,
        "payload": payload or {},
    }
