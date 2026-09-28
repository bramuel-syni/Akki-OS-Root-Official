"""services.enforce.principal_context_adapter · R-100-UNWIND · SO §3.8 cure.

Purpose (owner ruling this-session verbatim, 2026-09-21T~11:00Z at the
UNWIND directive):

    "Modifying the sealed PrincipalRequestContext class in
    services/request_context/context.py to add __enter__/__exit__ is an
    edit to a sealed class — SO §3.8 forbids it. Unwind to a wrapper:
    revert context.py byte-identically to its sealed state, author a
    context-manager adapter inside services/enforce/ that owns the
    protocol, re-point the R-100 portal routers to the wrapper, seal
    as a self-reported §3.8 lapse cured, regenerate the three continuity
    bundles, pin their sha256s in STATE/PINS.md, then hold at the R-91
    horizon (no expedite)."

What this module owns:
    The `with ...:` context-manager protocol for entering a PRIN-11
    propagation window. The sealed carrier (`PrincipalRequestContext`)
    stays byte-identical to its authored form at Commit 4b3b5e0
    (sha256 ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb;
    pinned structurally by
    tests/invariants/test_principal_context_adapter.py::
    test_context_py_sealed_bytes_sha256_pinned).

Semantics (verbatim owner constraint at UNWIND directive):
    "The PRIN-11 propagation semantics land identically to the cured
    behavior (enter sets propagation, exit clears it, exceptions
    propagate cleanly without leaking the context)."

    On __enter__: the propagation ContextVar is set to `principal_id`;
        the yielded value is the sealed `PrincipalRequestContext`
        carrier (PRIN-13 immutable-by-refusal, unchanged).
    On __exit__ (normal): the propagation ContextVar is reset to the
        exact prior value via its Token — no leak of the entered
        principal into the surrounding scope.
    On __exit__ (exceptional): the try/finally reset runs regardless;
        the exception propagates unchanged (context manager does not
        swallow it).

Consumers of this wrapper (this-wave):
    routers/portal_requests.py (5 R-100 endpoints)
    routers/portal_entitlement.py (4 R-100 endpoints)

Consumers may continue calling `services.request_context.enter_propagation`
directly when the sealed side-effect propagation semantics suffice (no
`with` block wanted). This wrapper is additive; it does not deprecate
or replace the sealed entry point.

Additive-only per SO §3.8. Zero sealed edit. Zero refactor. This module
is the ONE new file introduced by the UNWIND on the code branch.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from services.request_context import context as _rc_context
from services.request_context.context import PrincipalRequestContext


__all__ = ("principal_context",)


@contextmanager
def principal_context(principal_id: str) -> Iterator[PrincipalRequestContext]:
    """Context-manager wrapper over PRIN-11 propagation entry.

    Usage:
        with principal_context(identity.user_id) as request_ctx:
            # inside: current_principal_id() == identity.user_id
            ...
        # outside: propagation cleared, prior value restored

    Enter-sets: sets the propagation ContextVar to `principal_id`; yields
        the sealed PrincipalRequestContext carrier.
    Exit-clears: resets the propagation ContextVar to its prior value
        via the token returned by ContextVar.set(). Exit-clears runs on
        both normal exit and exceptional exit (try/finally).

    The sealed carrier's PRIN-13 immutable-by-refusal semantics are
    preserved verbatim; this wrapper only owns the with-block protocol,
    not the identity binding.
    """

    token = _rc_context._CURRENT_PRINCIPAL_ID.set(principal_id)
    try:
        yield PrincipalRequestContext(principal_id=principal_id)
    finally:
        _rc_context._CURRENT_PRINCIPAL_ID.reset(token)
