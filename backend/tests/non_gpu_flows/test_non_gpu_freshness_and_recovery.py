"""Non-GPU metadata only: SYNTHETIC signatures, fake worker/custody. No live source access."""
import asyncio
import json
from pydantic import SecretStr
import pytest
import test_custody_delivery_non_gpu as custody_tests
import test_skill_queries_non_gpu as query_tests
from services.custody_delivery import ledger
from services.custody_delivery.models import DeliveryDescriptor, DeliveryRequest
from services.custody_delivery.ports import CustodyBinding, ProviderState, origin_of
from services.custody_delivery.service import CustodyDelivery
from services.portal_operational import query_intents, query_execution
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Held


@pytest.fixture
def estate(): return custody_tests.estate_and_request.__wrapped__()


async def configured(estate):
    keys,db,receipts,request=estate
    coordinator=custody_tests.FakeCoordinator(db,request,custody_tests._artifact(),now_epoch=keys.now)
    await coordinator.seed_registry()
    provider=custody_tests.FakeProvider()
    binding=CustodyBinding(receipts,provider,'custodian',('https://custody.example.invalid',),120,1,clock=lambda:keys.now)
    service=CustodyDelivery(binding,coordinator)
    body=DeliveryRequest(artifact_ref=custody_tests._artifact().ref,idempotency_key='SYNTHETIC-delivery')
    descriptor=DeliveryDescriptor(delivery_id=digest({'request':request.digest(),'key':body.idempotency_key}),
        request_id=request.request_id,request_sha256=request.digest(),tenant_id=request.tenant_id,principal_id=request.principal_id,
        scope_refs=request.scope_refs,artifact=custody_tests._artifact(),registry_receipt_ref=(await coordinator.journal.read(request))[1]['hash'])
    url='https://custody.example.invalid/get?token=SYNTHETIC-CAPABILITY'
    grant=custody_tests._grant_receipt(keys,request,descriptor.digest(),descriptor.delivery_id,url,expires=keys.now+30)
    provider.prepare_state=ProviderState(grant=grant,url=SecretStr(url))
    return service,provider,coordinator,body,descriptor,grant,url


def test_concurrent_duplicate_prepares_have_one_native_dispatch(estate):
    async def run():
        service,provider,_,body,_,_,url=await configured(estate)
        values=await asyncio.gather(service.prepare(estate[3],body),service.prepare(estate[3],body))
        assert provider.prepare_calls==1
        assert provider.status_calls==1
        assert len({v.delivery_id for v in values})==1
        assert url not in json.dumps(await estate[2].events())
    with custody_tests.scope(): asyncio.run(run())


def test_completed_delivery_remains_auditable_after_capability_expiry(estate):
    async def run():
        keys,_,_,request=estate
        keys.now-=50  # Advance the synthetic verification clock without future-dating native ledger events.
        service,provider,_,body,descriptor,_,_=await configured(estate)
        offered=await service.prepare(request,body)
        completed_at=keys.now
        keys.now+=40
        completion=custody_tests._completion_receipt(keys,request,descriptor.digest(),descriptor.delivery_id,
            offered.receipt_ref,redeemed=completed_at,completed=completed_at)
        provider.status_state=ProviderState(completion=completion)
        done=await service.status(request,descriptor.delivery_id)
        assert done.state=='completed' and done.delivery_verified and done.url is None
        assert (await service.status(request,descriptor.delivery_id)).completion_receipt_ref==done.completion_receipt_ref
        assert provider.prepare_calls==1
    with custody_tests.scope(): asyncio.run(run())


def test_no_completion_and_expired_grant_never_returns_capability(estate):
    async def run():
        service,_,_,body,descriptor,_,_=await configured(estate)
        await service.prepare(estate[3],body)
        estate[0].now+=40
        result=await service.status(estate[3],descriptor.delivery_id)
        assert result.state=='expired' and result.url is None and not result.delivery_verified
    with custody_tests.scope(): asyncio.run(run())


@pytest.mark.parametrize('field,value,expected',[
    ('delivered_bytes',4,'CUSTODY_COMPLETION_NOT_PROVED'),
    ('observed_sha256','f'*64,'CUSTODY_COMPLETION_NOT_PROVED'),
    ('principal_id','someone-else','CUSTODY_RECEIPT_BINDING_MISMATCH'),
])
def test_freshly_signed_bad_completion_is_rejected(estate,field,value,expected):
    async def run():
        keys,_,_,request=estate
        service,provider,_,body,descriptor,_,_=await configured(estate)
        offered=await service.prepare(request,body)
        receipt=custody_tests._completion_receipt(keys,request,descriptor.digest(),descriptor.delivery_id,
            offered.receipt_ref,redeemed=keys.now-1,completed=keys.now-1)
        claims=json.loads(json.dumps(receipt.claims));claims['delivery'][field]=value
        claims['claim_sha256']=digest(claims['delivery'])
        provider.status_state=ProviderState(completion=keys.receipt('observation',claims,signer='custodian',request=request))
        with pytest.raises(Held,match=expected): await service.status(request,descriptor.delivery_id)
        assert not any(e['payload']['slot']=='completed' for e in await ledger.rows(estate[1],descriptor.delivery_id))
    with custody_tests.scope(): asyncio.run(run())


def test_expiry_during_final_rights_check_never_releases_url(estate):
    async def run():
        service,_,coordinator,body,_,_,_=await configured(estate)
        original=coordinator.retrieve
        async def racing(request):
            result=await original(request)
            if coordinator._retrieve_calls==2: estate[0].now+=40
            return result
        coordinator.retrieve=racing
        with pytest.raises(Held,match='SIGNER_OR_RECEIPT_NOT_CURRENT'): await service.prepare(estate[3],body)
    with custody_tests.scope(): asyncio.run(run())


@pytest.mark.parametrize('value',['https://custody.example.invalid:0/x','http://custody.example.invalid/x',
    'https://custody.example.invalid@evil.invalid/x','https://127.0.0.1/x','https://custody.example.invalid/x#token',
    'https://custody.example.invalid\\@evil.invalid/x','https://custody.example.invalid/\r\nsecret'])
def test_unsafe_origins_fail_before_any_network(value):
    with pytest.raises(Held): origin_of(value)


def test_query_status_blocks_changed_provisioning_before_old_view(estate):
    async def run():
        scope={'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'}
        provision=query_tests._provisioning()
        intent=await query_intents.submit(estate[1],scope,provision.skill_id,provision,
            query_intents.QueryIntentBody(query='SYNTHETIC private question',idempotency_key='query-freshness'))
        await query_intents.record_view(estate[1],scope,intent,{'outcome':'ready','reason_code':'GROUNDED_SKILL_RESULT_VERIFIED',
            'artifact_refs':['akki://TEST/old-answer'],'execution_verified':True,'delivery_verified':False})
        changed=provision.model_copy(update={'floor':'verified', 'corpus_slice_ref':'akki://TEST/different-corpus'})
        with pytest.raises(Held,match='SKILL_PROVISIONING_CHANGED'):
            await query_execution.current_status(estate[1],scope,provision.skill_id,intent['row']['run_id'],changed,None)
        held=await query_execution.current_status(estate[1],scope,provision.skill_id,intent['row']['run_id'],provision,None)
        assert held['outcome']=='held' and not held['execution_verified'] and 'artifact_refs' not in held
        assert 'SYNTHETIC private question' not in json.dumps(await estate[2].events())
    with custody_tests.scope(): asyncio.run(run())


def test_query_sessions_and_principals_are_separate(estate):
    async def run():
        scoped={'tenant_id':'tenant-SYNTHETIC','principal_id':'operator'}
        provision=query_tests._provisioning()
        values=[]
        for i in range(3):
            values.append(await query_intents.submit(estate[1],scoped,provision.skill_id,provision,
                query_intents.QueryIntentBody(query=f'Question {i}',idempotency_key=f'query-session-{i}')))
        assert len({v['row']['run_id'] for v in values})==3
        return values[0]['row']['run_id'],provision.skill_id
    with custody_tests.scope(): query_id,skill_id=asyncio.run(run())
    async def stranger():
        with pytest.raises(Held,match='SKILL_QUERY_NOT_FOUND'):
            await query_intents.events(estate[1],{'tenant_id':'tenant-SYNTHETIC','principal_id':'other-principal'},skill_id,query_id)
    with custody_tests.scope(principal='other-principal'): asyncio.run(stranger())