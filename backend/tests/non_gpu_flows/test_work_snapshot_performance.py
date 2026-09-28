"""SYNTHETIC work fixtures: fewer verified reads, exactly the same public views."""
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).parents[1] / 'activation_controls'))
sys.path.insert(0, str(Path(__file__).parents[1] / 'portal_operational'))
import test_native_control_ledger as helpers
from services.northena import portal_work
from services.portal_operational import work_snapshot
from services.portal_operational import execution_records, delivery_history
from services.portal_operational.models import SubmitRequest

SCOPE = {'tenant_id': 'tenant-SYNTHETIC', 'principal_id': 'operator'}


async def seed(db, amount):
    results = []
    for i in range(amount):
        results.append(await portal_work.submit(db, SCOPE, SubmitRequest(objective_text='TEST-only objective '+str(i),
            operation='browse_estate', units=['source-scope'], idempotency_key='TEST-only-key-'+str(i))))
    return results


async def legacy_projection(db):
    # The previous read shape: three independently validated prefixes, no fake flags.
    requests, executions = {}, {}
    for event in await portal_work.events_for(db, SCOPE):
        requests.setdefault(event['row']['run_id'], []).append(event)
    for event in await execution_records.events_for(db, SCOPE):
        executions.setdefault(event['row']['run_id'], []).append(event)
    deliveries = await delivery_history.grouped(db, SCOPE)
    result = []
    for key in reversed(list(requests)):
        execution = executions.get(key, [])
        work = execution_records.project(portal_work.project(requests[key]), execution)
        result.append(await delivery_history.project(db, SCOPE, work, deliveries.get(key, []),
            expected=delivery_history.expected_artifacts(execution)))
    return result


@pytest.mark.parametrize('amount', [0, 1, 25])
def test_listing_matches_previous_projection_with_one_verified_prefix(monkeypatch, amount):
    _, receipts, _ = helpers.estate.__wrapped__()
    async def run():
        await seed(receipts.db, amount)
        before = [v.model_dump() for v in await legacy_projection(receipts.db)]
        read = AsyncMock(wraps=work_snapshot.read_events)
        monkeypatch.setattr(work_snapshot, 'read_events', read)
        after = [v.model_dump() for v in await portal_work.listing(receipts.db, SCOPE)]
        assert before == after
        assert read.await_count == 1
        assert read.call_args.args[1] == {'row.tenant_id': SCOPE['tenant_id'], 'payload.principal_id': SCOPE['principal_id']}
    with helpers.scope(): asyncio.run(run())


def test_detail_is_one_prefix_and_absent_request_stays_404(monkeypatch):
    _, receipts, _ = helpers.estate.__wrapped__()
    async def run():
        seeded = await seed(receipts.db, 2)
        read = AsyncMock(wraps=work_snapshot.read_events)
        monkeypatch.setattr(work_snapshot, 'read_events', read)
        detail = await portal_work.detail(receipts.db, SCOPE, seeded[0].request_id)
        assert detail == seeded[0] and read.await_count == 1
        read.reset_mock()
        with pytest.raises(HTTPException) as exc: await portal_work.detail(receipts.db, SCOPE, 'foreign-or-absent')
        assert exc.value.status_code == 404 and read.await_count == 1
    with helpers.scope(): asyncio.run(run())


def test_snapshot_cannot_accept_misrouted_identity_or_ignore_read_failure(monkeypatch):
    async def run():
        bad = {'row': {'tenant_id': 'other', 'resource_type': 'dap_request', 'run_id': 'foreign'},
               'payload': {'principal_id': 'operator'}}
        monkeypatch.setattr(work_snapshot, 'read_events', AsyncMock(return_value=[bad]))
        with pytest.raises(ValueError, match='identity mismatch'): await work_snapshot.read_snapshot(object(), SCOPE)
        monkeypatch.setattr(work_snapshot, 'read_events', AsyncMock(side_effect=ValueError('TEST corrupt prefix')))
        with pytest.raises(ValueError, match='corrupt prefix'): await work_snapshot.read_snapshot(object(), SCOPE)
    asyncio.run(run())