"""Closed request-context carrier recovery does not resurrect prior authority."""
import asyncio
import contextvars
import sys
from pathlib import Path
from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).parents[2] / 'vendored/extraction_akki/backend'))
from services.enforce.control_scope import bind_control_scope, bind_authenticated_request_scope, require_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.portal_operational import access


def dead_context():
    with principal_context('old-actor'), bind_control_scope({'principal_id': 'old-actor', 'tenant_id': 'old-tenant'}):
        return contextvars.copy_context()


def test_closed_inherited_context_still_rejects_direct_reads_and_plain_rebind():
    context = dead_context()
    def later():
        with pytest.raises(ValueError, match='active control'): require_control_scope()
        with principal_context('old-actor'):
            with pytest.raises(ValueError, match='active control'):
                with bind_control_scope({'principal_id': 'old-actor', 'tenant_id': 'old-tenant'}): pass
    context.run(later)


def test_fresh_http_identity_uses_own_scope_and_cannot_revive_the_old_carrier(monkeypatch):
    scope = {'principal_id': 'new-actor', 'tenant_id': 'new-tenant', 'roles': ['operator']}
    auth = AsyncMock(return_value=scope)
    monkeypatch.setattr(access, 'census_identity', auth)
    async def next_request():
        with pytest.raises(ValueError): require_control_scope()
        async with access.portal_scope(object(), write=True) as current:
            assert current == scope and auth.await_count == 1
            bound = require_control_scope()
            assert (bound.principal_id, bound.tenant_id) == ('new-actor', 'new-tenant')
            await asyncio.sleep(0)
            assert require_control_scope() is bound
            inherited = contextvars.copy_context()
        with pytest.raises(ValueError): require_control_scope()
        with pytest.raises(ValueError): inherited.run(require_control_scope)
    async def run():
        await asyncio.create_task(next_request(), context=dead_context())
    asyncio.run(run())


def test_failed_authentication_never_installs_a_replacement_scope(monkeypatch):
    monkeypatch.setattr(access, 'census_identity', AsyncMock(side_effect=HTTPException(401, 'expired')))
    async def attempt():
        with pytest.raises(HTTPException) as exc:
            async with access.portal_scope(object()): pytest.fail('Unauthenticated scope was yielded')
        assert exc.value.status_code == 401
        with pytest.raises(ValueError): require_control_scope()
    async def run(): await asyncio.create_task(attempt(), context=dead_context())
    asyncio.run(run())


def test_active_nested_request_still_refuses_identity_substitution():
    with principal_context('actor'), bind_control_scope({'principal_id': 'actor', 'tenant_id': 'tenant'}):
        with bind_authenticated_request_scope({'principal_id': 'actor', 'tenant_id': 'tenant'}) as same:
            assert same is require_control_scope()
        with principal_context('other'):
            with pytest.raises(ValueError):
                with bind_authenticated_request_scope({'principal_id': 'other', 'tenant_id': 'other'}): pass


def test_cancelled_request_closes_its_child_context(monkeypatch):
    monkeypatch.setattr(access, 'census_identity', AsyncMock(return_value={'principal_id': 'actor', 'tenant_id': 'tenant', 'roles': ['operator']}))
    copied = []
    async def run():
        ready = asyncio.Event()
        async def request():
            async with access.portal_scope(object()):
                copied.append(contextvars.copy_context()); ready.set()
                await asyncio.Event().wait()
        task = asyncio.create_task(request()); await ready.wait(); task.cancel()
        with pytest.raises(asyncio.CancelledError): await task
        with pytest.raises(ValueError): copied[0].run(require_control_scope)
    asyncio.run(run())