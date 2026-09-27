"""Isolated scope/authz matrix checks for execution advance concealment semantics."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

import pytest
from fastapi import HTTPException

from routers import portal_requests
from services.portal_operational import execution


# Module/feature: write-authorized foreign principal still receives 404 concealment (isolated scoped gate).
def test_execution_advance_write_authorized_foreign_principal_receives_404(monkeypatch):
    @asynccontextmanager
    async def _operator_scope(_request, write=False):
        assert write is True
        yield {"tenant_id": "DIGICOW", "principal_id": "operator-foreign", "roles": ["operator"]}

    async def _events_for(_db, scope, request_id=None):
        assert scope["principal_id"] == "operator-foreign"
        assert request_id == "req-owned-by-other"
        return []

    monkeypatch.setattr(portal_requests, "portal_scope", _operator_scope)
    monkeypatch.setattr(execution.portal_work, "events_for", _events_for)

    with pytest.raises(HTTPException) as exc:
        asyncio.run(
            portal_requests.advance_execution(
                "req-owned-by-other",
                execution.ExecutionBudget(deadline_epoch=1_900_000_000),
                request=object(),
            )
        )
    assert exc.value.status_code == 404
