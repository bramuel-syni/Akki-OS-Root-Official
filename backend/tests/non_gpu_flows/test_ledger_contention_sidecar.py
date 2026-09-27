"""No Canon byte edits: conflict backoff lives outside the pinned writer."""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from pymongo.errors import DuplicateKeyError
from services.ledger_writer.contention_control import _Collection
from services.ledger_writer.conditional_control import HeadChanged


def test_conflict_yields_without_swallowing_original_cas_failure(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr('services.ledger_writer.contention_control.asyncio.sleep', sleep)
    insert = AsyncMock(side_effect=DuplicateKeyError('TEST collision'))
    async def run():
        wrapper = _Collection(SimpleNamespace(insert_one=insert))
        for _ in range(3):
            with pytest.raises(DuplicateKeyError): await wrapper.insert_one({'TEST': 'metadata'})
        assert sleep.await_count == 3
        assert all(0 < call.args[0] < 0.052 for call in sleep.await_args_list)
    asyncio.run(run())


def test_stale_head_is_not_retried_by_backoff_sidecar(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr('services.ledger_writer.contention_control.asyncio.sleep', sleep)
    async def run():
        insert = AsyncMock(side_effect=HeadChanged('TEST stale budget'))
        wrapper = _Collection(SimpleNamespace(insert_one=insert))
        with pytest.raises(HeadChanged): await wrapper.insert_one({'TEST': 'metadata'})
        sleep.assert_not_awaited()
    asyncio.run(run())