"""Worker acknowledgement tests; async MOCK metadata RPC only, no workload."""
import asyncio
from types import SimpleNamespace
import pytest
import test_native_control_ledger as helpers
from test_native_control_ledger import scope, prepare
from services.activation.worker_gate import WorkerLimitGate
from services.activation.bounded_adapter import BoundedEngineAdapter
from services.ledger_writer.mongo_control import digest
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held


@pytest.fixture
def estate():
    return helpers.estate.__wrapped__()


@pytest.mark.parametrize('defect',[None,'missing_rpc','wrong_envelope','wrong_signer','wrong_fence','expired'])
def test_native_worker_limit_acknowledgement_before_send(estate,defect):
    async def run():
        keys,receipts,_=estate
        plan,_,_=await prepare(estate)
        coordinator=SimpleNamespace(journal=LedgerJournal(receipts.db))
        calls=[]
        async def forbidden(*a): raise AssertionError('NO workload calls allowed')
        async def admit(req,key,fence,envelope):
            calls.append(envelope)
            receipt=keys.receipt('observation',{'category':'runtime','context_sha256':req.digest(),
                'claim_sha256':'f'*64 if defect=='wrong_envelope' else digest(envelope.model_dump(mode='json')),
                'evidence_mode':'measured'},signer='not-worker' if defect=='wrong_signer' else 'worker',request=req)
            if defect=='expired': keys.now+=1001
            return receipt
        executor=BoundedEngineAdapter(kind='source',engine='mtafiti',submit_rpc=forbidden,status_rpc=forbidden,
            cancel_rpc=forbidden,timeout_seconds=2,admit_limits_rpc=admit)
        if defect=='missing_rpc': executor=SimpleNamespace(admit_limits_rpc=None)
        dispatch={'seq':1,'data':{'operation_key':'TEST-operation'}}
        gate=WorkerLimitGate(receipts)
        if defect in {'missing_rpc','wrong_envelope','wrong_signer','expired'}:
            with pytest.raises(Held): await gate.admit(coordinator,plan.request,executor,dispatch)
        else:
            ref=await gate.admit(coordinator,plan.request,executor,dispatch)
            if defect=='wrong_fence':
                with pytest.raises(Held,match='ACK_BINDING_MISMATCH'):
                    await gate.admit(coordinator,plan.request,executor,{**dispatch,'seq':2})
            else:
                assert ref==await gate.admit(coordinator,plan.request,executor,dispatch)
                assert len(calls)==1
    with scope(): asyncio.run(run())