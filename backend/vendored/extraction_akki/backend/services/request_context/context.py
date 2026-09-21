"""services.request_context.context — Principal Model Spec v1 §5 propagation.

PRIN-11 · PRIN-13 enforcement, additive-only.

PRIN-11 verbatim: 'Every request entering the platform on behalf of a
principal carries that principal's identity through to every service
it touches, by construction — not by convention, not by a caller
choosing to pass it along.  A downstream write with no principal in
its calling context fails closed rather than writing under a default
or empty actor.'

PRIN-13 verbatim: 'Principal context is read-only once it enters
propagation for a given request.  A service receiving it cannot widen,
narrow, or substitute the principal it was given — the same discipline
Northena's objective freeze already applies to scope.'

Concurrency: `contextvars.ContextVar` (async-safe under FastAPI /
asyncio).  Owner ratification this-session verbatim (Q3 response):
'ContextVar — async-safe is the only correct choice under FastAPI /
asyncio; thread-locals leak across await boundaries.  Ensure the
context REFUSES (fail-closed) when principal identity is absent rather
than defaulting.'
"""
from __future__ import annotations

from contextvars import ContextVar
from typing import Any, Dict, Optional


# Async-safe propagation surface.  Default `None` triggers fail-closed
# on any downstream write; the context never defaults to an anonymous
# actor.
_CURRENT_PRINCIPAL_ID: ContextVar[Optional[str]] = ContextVar(
    "principal_model_current_principal_id", default=None,
)


class PrincipalContextAbsent(RuntimeError):
    """PRIN-11 fail-closed exception.

    Raised when a downstream write is attempted with no principal in
    the calling context.  Failure posture verbatim from spec §7:
    'Propagation context absent → fail-closed, no default actor.'
    """


class PrincipalContextRefusal(RuntimeError):
    """PRIN-13 refusal exception.

    Raised when a receiving service attempts to widen, narrow, or
    substitute the principal it was given.  Kinship with Northena's
    Promise #32 objective-freeze mechanism.
    """


class PrincipalRequestContext:
    """Immutable-by-refusal request-context carrier.

    PRIN-13 verbatim: 'A service receiving it cannot widen, narrow, or
    substitute the principal it was given.'  Any attempt to reassign
    `principal_id` after construction raises
    `PrincipalContextRefusal`.
    """

    __slots__ = ("_principal_id", "_sealed")

    def __init__(self, principal_id: str) -> None:
        object.__setattr__(self, "_principal_id", principal_id)
        object.__setattr__(self, "_sealed", True)

    @property
    def principal_id(self) -> str:
        return object.__getattribute__(self, "_principal_id")

    def __setattr__(self, name: str, value: Any) -> None:
        if object.__getattribute__(self, "_sealed"):
            raise PrincipalContextRefusal(
                f"PRIN-13 · principal context read-only once in "
                f"propagation; attempt to set {name!r} refused.  A "
                "service receiving it cannot widen, narrow, or "
                "substitute the principal it was given."
            )
        object.__setattr__(self, name, value)


def enter_propagation(principal_id: str) -> PrincipalRequestContext:
    """PRIN-11 · start of a propagation window for a given request.

    The ContextVar is set to the principal identity by construction;
    every downstream service reads the same identity through
    `current_principal_id()`.
    """

    _CURRENT_PRINCIPAL_ID.set(principal_id)
    return PrincipalRequestContext(principal_id=principal_id)


def current_principal_id() -> Optional[str]:
    """Read the current propagated principal identity, or None if the
    context is absent.  Callers MUST fail closed on None (PRIN-11)."""

    return _CURRENT_PRINCIPAL_ID.get()


def downstream_write(
    record_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """PRIN-11 verbatim: 'A downstream write with no principal in its
    calling context fails closed rather than writing under a default
    or empty actor.'
    """

    principal_id = _CURRENT_PRINCIPAL_ID.get()
    if principal_id is None:
        raise PrincipalContextAbsent(
            "PRIN-11 · downstream write refused: no principal in "
            "calling context.  The context never defaults to an "
            "anonymous actor."
        )
    return {
        "principal_id": principal_id,
        "payload": record_payload,
    }
