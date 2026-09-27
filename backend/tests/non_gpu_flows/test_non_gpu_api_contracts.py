"""In-process HTTP contracts with SYNTHETIC signed custody and scoped fake identity.

Live application authentication is tested separately. No source bytes or GPU access.
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import test_custody_delivery_non_gpu as custody_helpers
import test_skill_queries_non_gpu as skill_helpers
from test_non_gpu_freshness_and_recovery import configured
from routers import custody_delivery, skill_queries
from services.northena import portal_work
from services.portal_operational.models import SubmitRequest


@pytest.fixture
def fixture_app(monkeypatch):
    estate=custody_helpers.estate_and_request.__wrapped__()
    scoped={'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'}
    @asynccontextmanager
    async def access(request,write=False):
        with custody_helpers.scope(): yield scoped
    with custody_helpers.scope():
        own=asyncio.run(portal_work.submit(estate[1],scoped,SubmitRequest(objective_text='SYNTHETIC result handoff',
            operation='browse_estate',units=['source-scope'],idempotency_key='SYNTHETIC-custody-request')))
    estate=(*estate[:3],estate[3].model_copy(update={'request_id':own.request_id,'objective_sha256':own.objective_hash}))
    provision=[skill_helpers._provisioning('skill-1')]
    async def gate(*a): return provision[0]
    monkeypatch.setattr(custody_delivery,'db',estate[1])
    monkeypatch.setattr(custody_delivery,'portal_scope',access)
    monkeypatch.setattr(skill_queries,'db',estate[1])
    monkeypatch.setattr(skill_queries,'portal_scope',access)
    monkeypatch.setattr(skill_queries,'require_governed_skill_query',gate)
    app=FastAPI();app.include_router(custody_delivery.router);app.include_router(skill_queries.router)
    return app,estate,provision


def test_query_http_replay_conflict_scope_and_freshness(fixture_app):
    app,estate,provision=fixture_app
    body={'query':'SYNTHETIC question never persisted','idempotency_key':'SYNTHETIC-question-1'}
    with TestClient(app) as client:
        first=client.post('/api/callable_skill/skill-1/query-intents',json=body)
        assert first.status_code==201,first.text
        assert 'no-store' in first.headers['cache-control']
        qid=first.json()['query_id']
        assert client.post('/api/callable_skill/skill-1/query-intents',json=body).json()['query_id']==qid
        conflict=client.post('/api/callable_skill/skill-1/query-intents',json={**body,'query':'changed'})
        assert conflict.status_code==409 and conflict.json()['reason_code']=='SKILL_QUERY_IDEMPOTENCY_CONFLICT'
        read=client.get(f'/api/callable_skill/skill-1/queries/{qid}')
        assert read.status_code==200 and not read.json()['execution_verified']
        unknown=client.get(f'/api/callable_skill/other-skill/queries/{qid}')
        assert unknown.status_code==404
        advanced=client.post(f'/api/callable_skill/skill-1/queries/{qid}/advance')
        assert advanced.status_code==409 and advanced.json()['reason_code']=='SKILL_EXECUTOR_UNADMITTED'
        provision[0]=provision[0].model_copy(update={'corpus_slice_ref':'akki://TEST/changed'})
        stale=client.get(f'/api/callable_skill/skill-1/queries/{qid}')
        assert stale.status_code==409 and stale.json()['reason_code']=='SKILL_PROVISIONING_CHANGED'
    assert body['query'] not in str(estate[1]['ledger_v1_control_events'].docs)


def test_delivery_http_offers_capability_without_claiming_completion(fixture_app,monkeypatch):
    app,estate,_=fixture_app
    with custody_helpers.scope(): values=asyncio.run(configured(estate))
    service,provider,_,body,descriptor,_,url=values
    monkeypatch.setattr(custody_delivery,'service',lambda request:service)
    with TestClient(app) as client:
        offered=client.post(f'/api/portal/requests/{estate[3].request_id}/delivery',json=body.model_dump())
        assert offered.status_code==200,offered.text
        assert offered.json()['url']==url and offered.json()['delivery_verified'] is False
        assert offered.headers['referrer-policy']=='no-referrer'
        assert 'no-store' in offered.headers['cache-control']
        assert provider.prepare_calls==1
        status=client.get(f'/api/portal/requests/{estate[3].request_id}/deliveries/{descriptor.delivery_id}')
        assert status.status_code==200 and status.json()['url'] is None and not status.json()['delivery_verified']
        unknown=client.get(f'/api/portal/requests/{estate[3].request_id}/deliveries/'+'f'*64)
        assert unknown.status_code==404
    assert url not in str(estate[1]['ledger_v1_control_events'].docs)


def test_work_history_records_delivery_without_overclaiming_partial_result(fixture_app):
    app,estate,_=fixture_app
    async def run():
        service,provider,coordinator,body,descriptor,_,url=await configured(estate)
        await coordinator.journal.append(estate[3],'terminal',{'phase':'ready','reason_code':'VERIFIED_RESULT_RECORDED',
            'evidence_mode':'measured','artifact_refs':[descriptor.artifact.ref,'akki://TEST/another-artifact']})
        offered=await service.prepare(estate[3],body)
        work=await portal_work.detail(estate[1],{'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'},estate[3].request_id)
        assert work.delivery_verified is False and work.delivery_state=='grant'
        assert any(h.event=='custody_grant' for h in work.history)
        receipt=custody_helpers._completion_receipt(estate[0],estate[3],descriptor.digest(),descriptor.delivery_id,
            offered.receipt_ref,redeemed=estate[0].now-1,completed=estate[0].now-1)
        from services.custody_delivery.ports import ProviderState
        provider.status_state=ProviderState(completion=receipt)
        completed=await service.status(estate[3],descriptor.delivery_id)
        work=await portal_work.detail(estate[1],{'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'},estate[3].request_id)
        assert not work.delivery_verified and work.delivery_state=='partial'
        assert completed.completion_receipt_ref in work.delivery_receipt_refs
        assert url not in work.model_dump_json()
        from services.portal_operational.delivery_history import project
        partial=work.model_copy(update={'history':[]})
        full=await project(estate[1],{'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'},partial,expected=[descriptor.artifact.ref])
        assert full.delivery_verified
    with custody_helpers.scope(): asyncio.run(run())