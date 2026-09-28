"""services.request_context — CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9.

Request-context propagation implementing PRIN-11..PRIN-13 (spec §5):
    PRIN-11  Propagation by construction; downstream write with no
             principal in the calling context fails closed rather than
             writing under a default or empty actor.
    PRIN-12  The Ledger's `actor` field is populated only from
             propagated principal context, never from a caller-supplied
             string.  Prospective-only correction (existing entries
             written before this component exists are not retroactively
             altered).
    PRIN-13  Principal context is read-only once it enters propagation
             for a given request — the same discipline Northena's
             objective freeze applies to scope.

Concurrency model: `contextvars.ContextVar` (async-safe under FastAPI /
asyncio · thread-locals would leak across await boundaries).  Owner
ratification this-session verbatim: 'ContextVar — async-safe is the
only correct choice under FastAPI/asyncio.'

Fail-closed on absence: `downstream_write` raises
`PrincipalContextAbsent` when the ContextVar is empty; the context
never defaults to an anonymous actor (owner ratification this-session
verbatim: 'unresolvable principal is FP-2's refusing gate, the same
doctrine the owner cited when rejecting Optional tenant_id').

Additive-only per SO §3.8.  The Ledger actor-string upgrade is a
wrapper (`ledger_actor_binding.write_ledger_row`), NOT an in-place edit
to `services.memory.ledger.append_row` or any other sealed writer —
consistent with the owner reminder this-session verbatim: 'if any
sealed writer needs its actor semantics upgraded in place, that's a
fork, not an edit'.
"""
from __future__ import annotations

from services.request_context.context import (
    PrincipalContextAbsent,
    PrincipalContextRefusal,
    PrincipalRequestContext,
    current_principal_id,
    downstream_write,
    enter_propagation,
)

__all__ = (
    "PrincipalContextAbsent",
    "PrincipalContextRefusal",
    "PrincipalRequestContext",
    "current_principal_id",
    "downstream_write",
    "enter_propagation",
)
