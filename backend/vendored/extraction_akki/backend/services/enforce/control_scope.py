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