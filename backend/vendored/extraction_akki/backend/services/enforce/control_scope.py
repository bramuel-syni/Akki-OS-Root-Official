"""Request-lifetime control scope; composes, never replaces, PRIN propagation.

This is the existing held-work account membership, NOT organisation admission.
The lease prevents copied child contexts from authorizing later writes.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field

from services.request_context.context import current_principal_id


@dataclass
class _Lease:
    closed: bool = False


@dataclass(frozen=True)
class ControlScope:
    principal_id: str
    tenant_id: str
    _lease: _Lease = field(default_factory=_Lease, repr=False, compare=False)


_CURRENT = ContextVar("akki_control_request_scope", default=None)


def require_control_scope():
    scope = _CURRENT.get()
    if scope is None or scope._lease.closed:
        raise ValueError("An active control request scope is required.")
    if current_principal_id() != scope.principal_id:
        raise ValueError("Propagated principal substitution refused.")
    return scope


@contextmanager
def bind_control_scope(scope):
    principal, tenant = scope.get("principal_id"), scope.get("tenant_id")
    if any(not isinstance(value, str) or not value.strip() for value in (principal, tenant)):
        raise ValueError("A nonblank principal and tenant are required.")
    if principal != current_principal_id():
        raise ValueError("Control scope must match existing principal propagation.")
    previous = _CURRENT.get()
    if previous is not None:
        previous = require_control_scope()
        if (principal, tenant) != (previous.principal_id, previous.tenant_id):
            raise ValueError("Control request scope substitution refused.")
        yield previous
        return
    bound = ControlScope(principal, tenant)
    token = _CURRENT.set(bound)
    try:
        yield bound
    finally:
        bound._lease.closed = True
        _CURRENT.reset(token)


@contextmanager
def bind_authenticated_request_scope(scope):
    """Start a re-authenticated HTTP request, not a continuation of old work.

    ASGI task/connection contexts can retain a previous request's *closed* lease.
    Only the HTTP boundary, AFTER census_identity has validated the new request,
    may discard that dead carrier. Ordinary bind/require still refuse it, and
    active nested scopes still cannot change identity. No auth/native grant is
    renewed: this creates only the already-authenticated request's local lease.
    """
    previous = _CURRENT.get()
    token = _CURRENT.set(None) if previous is not None and previous._lease.closed else None
    try:
        with bind_control_scope(scope) as bound:
            yield bound
    finally:
        if token is not None:
            _CURRENT.reset(token)