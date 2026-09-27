"""Startup and native descriptor tests use SYNTHETIC providers, never a live root."""
import asyncio
import json
import sys
from types import SimpleNamespace, ModuleType
from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException
import test_native_control_ledger as helpers
from test_native_control_ledger import scope
from services.activation.runtime_binding import install_runtime, close_runtime, NativeRuntime, NativeExecutionBindings
from services.activation.runtime_status import runtime_status
from services.activation.bounded_adapter import BoundedEngineAdapter
from services.activation.decisions import LedgerActivationDecisions
from services.activation.record_shapes import Plan
from services.activation.portal_plans import recover_plan
from services.northena.execution_models import Request, Held
from services.northena.execution_eligibility import InputEligibility
from services.northena import portal_work
from services.portal_operational import execution
from services.portal_operational.models import SubmitRequest
from services.ledger_writer.mongo_control import digest


@pytest.fixture
def estate(): return helpers.estate.__wrapped__()


def build_runtime(estate):
    _,receipts,_=estate
    callback=AsyncMock()
    bindings=NativeExecutionBindings(decisions=LedgerActivationDecisions(receipts),
        inspector=SimpleNamespace(inspect=callback),principal_lookup=callback,
        executors={'source':BoundedEngineAdapter('source','mtafiti',callback,callback,callback,2,admit_limits_rpc=callback)},
        eligibility=InputEligibility(None),gate_timeout_seconds=2)
    return NativeRuntime(receipts=receipts,bindings=bindings,evidence_timeout_seconds=2,close=AsyncMock())


def test_missing_startup_configuration_imports_nothing(monkeypatch,estate):
    app=SimpleNamespace(state=SimpleNamespace())
    def forbidden(*a): raise AssertionError('Must not discover/probe/mint a provider')
    monkeypatch.setattr('services.activation.runtime_binding.importlib.import_module',forbidden)
    assert asyncio.run(install_runtime(app,estate[1].db,{})) is False
    assert runtime_status(app.state).model_dump()['configured'] is False


@pytest.mark.parametrize('config',[
    {'AKKI_NATIVE_RUNTIME_FACTORY':'secrets:not-a-function'},
    {'AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS':'2'},
    {'AKKI_NATIVE_RUNTIME_FACTORY':'TEST_PROVIDER:factory','AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS':'nan'},
    {'AKKI_NATIVE_RUNTIME_FACTORY':'TEST_PROVIDER:factory','AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS':'0'},
])
def test_incomplete_native_configuration_fails_without_secret_disclosure(estate,config):
    app=SimpleNamespace(state=SimpleNamespace())
    with pytest.raises(RuntimeError,match='^NATIVE_RUNTIME_CONFIGURATION_INVALID$'):
        asyncio.run(install_runtime(app,estate[1].db,config))
    assert vars(app.state)=={}


def test_valid_factory_installs_one_coherent_composition(monkeypatch,estate):
    runtime=build_runtime(estate)
    module=ModuleType('TEST_PROVIDER'); module.factory=AsyncMock(return_value=runtime)
    monkeypatch.setitem(sys.modules,'TEST_PROVIDER',module)
    app=SimpleNamespace(state=SimpleNamespace())
    assert asyncio.run(install_runtime(app,estate[1].db,{
        'AKKI_NATIVE_RUNTIME_FACTORY':'TEST_PROVIDER:factory','AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS':'2'}))
    assert app.state.activation_receipts is app.state.execution_bindings.decisions.receipts
    assert app.state.execution_bindings.principal_lookup is runtime.bindings.principal_lookup
    status=runtime_status(app.state)
    assert status.worker_paths_bound==['source']
    assert status.execution_authorized is False and status.live_proof_verified is False


def test_cross_ledger_factory_is_rejected_and_closed(monkeypatch,estate):
    runtime=build_runtime(estate)
    module=ModuleType('TEST_PROVIDER'); module.factory=AsyncMock(return_value=runtime)
    monkeypatch.setitem(sys.modules,'TEST_PROVIDER',module)
    app=SimpleNamespace(state=SimpleNamespace())
    with pytest.raises(RuntimeError):
        asyncio.run(install_runtime(app,{}, {'AKKI_NATIVE_RUNTIME_FACTORY':'TEST_PROVIDER:factory','AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS':'2'}))
    runtime.close.assert_awaited_once()
    assert vars(app.state)=={}


def test_native_shutdown_does_not_leak_provider_errors(estate):
    runtime=build_runtime(estate)
    runtime.close.side_effect=RuntimeError('private-provider-token-and-host')
    app=SimpleNamespace(state=SimpleNamespace(native_runtime=runtime))
    with pytest.raises(RuntimeError,match='^NATIVE_RUNTIME_SHUTDOWN_FAILED$'):
        asyncio.run(close_runtime(app))


async def signed_portal_plan(estate):
    keys,receipts,_=estate
    scoped={'principal_id':'operator','tenant_id':'tenant-SYNTHETIC'}
    submitted=await portal_work.submit(receipts.db,scoped,SubmitRequest(objective_text='SYNTHETIC grounded objective',
        operation='processed_intelligence',units=['source-scope'],idempotency_key='synthetic-native-model-plan'))
    descriptor=Request(request_id=submitted.request_id,tenant_id=scoped['tenant_id'],principal_id='operator',kind='skill',engine='solva',
        objective_sha256=digest(submitted.objective_text),input_refs=('akki://TEST/deployed-skill','akki://TEST/grant','akki://TEST/query'),
        scope_refs=('source-scope',),deadline_epoch=keys.now+900,result_floor='non_factual')
    plan=Plan.model_validate_json(json.dumps({'request':descriptor.model_dump(mode='json'),
        'groups':[{'group':p,'purpose':p,'members':['TEST-owner'],'quorum':1} for p in ['scope','expenditure','answering']],
        'purposes':['answering'],'acceptance_script_sha256':'b'*64,'snapshot_hashes':['c'*64],
        'limits':[{'dimension':'spend','unit':'USD','quantity':'0'},{'dimension':'wall_clock','unit':'seconds','quantity':'100'}],
        'allocation_ref':'d'*64,'worker_ref':'e'*64,'terms_ref':'TEST-terms','policy_epoch':1,
        'dial_versions':{k:'v1' for k in ['custody_floor','approving_authority','external_crossing','disclosure_counterparties']},
        'policy_versions':{k:'v1' for k in ['crossing_decision_table','acceptance_standard','cleanliness_pack']},'termination_grace_seconds':5}))
    await receipts.record(keys.receipt('plan',plan.model_dump(mode='json'),request=descriptor))
    return scoped,submitted,descriptor


def test_signed_model_descriptor_is_recovered_without_fabricating_inputs(estate):
    async def run():
        scoped,submitted,descriptor=await signed_portal_plan(estate)
        recovered=await execution.frozen_request(estate[1].db,scoped,submitted.request_id,
            execution.ExecutionBudget(deadline_epoch=descriptor.deadline_epoch),receipts=estate[1])
        assert recovered==descriptor
        assert not any(v.startswith('akki://source/') for v in recovered.input_refs)
        # A signed descriptor is not approval and cannot execute through an unbound worker.
        held=await execution.advance(estate[1].db,scoped,submitted.request_id,
            execution.ExecutionBudget(deadline_epoch=descriptor.deadline_epoch),receipts=estate[1])
        assert held.phase=='held' and held.reason_code=='EXECUTOR_ADAPTER_UNBOUND'
    with scope(): asyncio.run(run())


@pytest.mark.parametrize('change',['scope','objective','deadline','principal','operation'])
def test_native_descriptor_cannot_widen_frozen_intent(estate,change):
    async def run():
        scoped,submitted,descriptor=await signed_portal_plan(estate)
        frozen=(await portal_work.events_for(estate[1].db,scoped,submitted.request_id))[0]['payload'].copy()
        deadline=descriptor.deadline_epoch
        if change=='scope': frozen['units']=['other-source']
        if change=='objective': frozen['objective_text']='changed'
        if change=='deadline': deadline+=1
        if change=='principal': scoped={**scoped,'principal_id':'other-principal'}
        if change=='operation': frozen['operation']='fine_tune_model'
        with pytest.raises(Held): await recover_plan(estate[1],scoped,frozen,deadline)
    with scope(): asyncio.run(run())


def test_missing_descriptor_is_receipted_without_creating_execution_inputs(estate):
    async def run():
        scoped,submitted,descriptor=await signed_portal_plan(estate)
        with pytest.raises(HTTPException) as caught:
            await execution.advance(estate[1].db,scoped,submitted.request_id,
                execution.ExecutionBudget(deadline_epoch=descriptor.deadline_epoch))
        assert caught.value.status_code==409
        work=await portal_work.detail(estate[1].db,scoped,submitted.request_id)
        assert work.reason_code=='ADMITTED_SIGNER_RESOLVER_UNBOUND' and work.next_action
        assert work.history[-1].event=='descriptor_held'
        assert not [e for e in await estate[1].events() if e['row']['resource_type']=='execution_flow']
    with scope(): asyncio.run(run())