"""Real process/Mongo recovery, SYNTHETIC worker/authority/inspection.

Processes share this host; this is NOT proof of independent physical-host custody.
No source reads, SSH, model work, credentials or native admissions are created.
Append-only TEST-SYNTHETIC tenant evidence is retained after each drill.
"""
import asyncio
import json
import multiprocessing
import os
import time
from uuid import uuid4
import pytest
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from services.enforce.principal_context_adapter import principal_context
from services.enforce.control_scope import bind_control_scope
from services.ledger_writer.principal_control import append_event, read_events
from services.ledger_writer.mongo_control import digest
from services.northena.execution_coordinator import Coordinator
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Request, WorkerResult, Authority, Artifact, Usage


class CrashJournal:
    def __init__(self, journal, stage): self.journal,self.stage=journal,stage
    async def read(self,request): return await self.journal.read(request)
    async def append(self,request,slot,data):
        if (self.stage=='before_send' and slot=='send' or
            self.stage=='before_terminal' and slot=='terminal' or
            self.stage=='before_observation' and slot.startswith('observation:')):
            os._exit(86)
        return await self.journal.append(request,slot,data)


class SyntheticAuthority:
    async def authorize(self,request,phase):
        return Authority(authority_ref='akki://TEST/authority',request_sha256=request.digest(),
            tenant_id=request.tenant_id,principal_id=request.principal_id,scope_refs=request.scope_refs,
            engine=request.engine,expires_epoch=request.deadline_epoch,terms_ref='akki://TEST/terms',policy_epoch=1)


class SyntheticInspector:
    async def verify(self,request,result,key): return result.artifacts


class PersistentSyntheticWorker:
    def __init__(self,db,stage): self.db,self.stage=db,stage

    async def record(self,request,key,event_type,payload,command):
        # Consumer audit actor stays the requester. Synthetic producer identity
        # is metadata, never a nested identity switch or a live worker admission.
        return await append_event(self.db,tenant_id=request.tenant_id,run_id=request.request_id,command_id=command,
            event_type=event_type,resource_type='TEST_recovery_worker',decision='SYNTHETIC_ONLY',reason_code='MOCKED',
            payload={'principal_id':request.principal_id,'synthetic_producer':'TEST-worker','operation_key':key,**payload})

    async def submit(self,request,key,fence,grant):
        await self.record(request,key,'test.rpc.submit',{'fence':fence},uuid4().hex)
        result=WorkerResult(operation_key=key,request_sha256=request.digest(),executor_id='TEST-worker',fence=fence,
            state='complete',receipt_ref='akki://TEST/receipt',evidence_mode='MOCKED',usage=(Usage(unit='tokens',quantity='1'),),
            artifacts=(Artifact(ref='akki://TEST/artifact',sha256='b'*64,size_bytes=1,tenant_id=request.tenant_id,class_label='non_factual'),))
        event=await self.record(request,key,'test.worker.effect',{'result':result.model_dump(mode='json')},digest({'TEST_effect':key}))
        if self.stage=='after_effect': os._exit(86)
        return WorkerResult.model_validate_json(json.dumps(event['payload']['result']))

    async def status(self,request,key,fence):
        await self.record(request,key,'test.rpc.status',{'fence':fence},uuid4().hex)
        events=await read_events(self.db,{'row.tenant_id':request.tenant_id,'row.resource_type':'TEST_recovery_worker'})
        rows=[e for e in events if e['row']['event_type']=='test.worker.effect']
        if len(rows)!=1: raise RuntimeError('TEST_WORKER_EFFECT_MISSING')
        return WorkerResult.model_validate_json(json.dumps(rows[0]['payload']['result']))

    async def cancel(self,*args): raise AssertionError('No cancellation RPC belongs to this drill')


def child(request_json,stage,queue):
    async def run():
        cfg=dotenv_values('/app/backend/.env')
        client=AsyncIOMotorClient(cfg['MONGO_URL']); db=client[cfg['DB_NAME']]
        request=Request.model_validate_json(request_json)
        try:
            with principal_context(request.principal_id),bind_control_scope({'tenant_id':request.tenant_id,'principal_id':request.principal_id}):
                coordinator=Coordinator(CrashJournal(LedgerJournal(db),stage),SyntheticAuthority(),
                    {'source':PersistentSyntheticWorker(db,stage)},SyntheticInspector())
                view=await coordinator.advance(request)
                rows=await read_events(db,{'row.tenant_id':request.tenant_id})
                queue.put({'pid':os.getpid(),'view':view.model_dump(mode='json'),
                    'effects':sum(e['row']['event_type']=='test.worker.effect' for e in rows),
                    'submits':sum(e['row']['event_type']=='test.rpc.submit' for e in rows),
                    'status_calls':sum(e['row']['event_type']=='test.rpc.status' for e in rows),
                    'metered':sum(e['payload'].get('slot')=='metered' for e in rows),
                    'terminal':sum(e['payload'].get('slot')=='terminal' for e in rows),
                    'fences':sorted({e['payload']['fence'] for e in rows if 'fence' in e['payload']})})
        except Exception as exc:
            import traceback
            queue.put({'error_type':type(exc).__name__, 'frames':[(os.path.basename(f.filename),f.lineno,f.name)
                       for f in traceback.extract_tb(exc.__traceback__)[-5:]]})
            raise RuntimeError('TEST_PROCESS_RECONCILIATION_FAILED') from None
        finally: client.close()
    asyncio.run(run())


@pytest.mark.parametrize('crash_stage',['before_send','after_effect','before_observation','before_terminal'])
def test_process_crash_reconciles_stable_operation_without_duplicate_work(crash_stage):
    request=Request(request_id='TEST-'+uuid4().hex,tenant_id='TEST-SYNTHETIC-recovery-'+uuid4().hex,
        principal_id='TEST-requester',kind='source',engine='mtafiti',objective_sha256='a'*64,
        input_refs=('akki://TEST/source-descriptor',),scope_refs=('TEST-scope',),deadline_epoch=int(time.time())+600)
    ctx=multiprocessing.get_context('spawn'); queue=ctx.Queue()
    first=ctx.Process(target=child,args=(request.model_dump_json(),crash_stage,queue)); first.start(); first.join(35)
    if first.is_alive(): first.terminate(); first.join(); pytest.fail('Synthetic crash process timed out')
    assert first.exitcode==86,queue.get(timeout=5)
    resumed=ctx.Process(target=child,args=(request.model_dump_json(),'resume',queue)); resumed.start(); resumed.join(35)
    if resumed.is_alive(): resumed.terminate(); resumed.join(); pytest.fail('Synthetic recovery process timed out')
    assert resumed.exitcode==0,queue.get(timeout=5)
    result=queue.get(timeout=5); queue.close(); queue.join_thread()
    assert result['pid']!=first.pid
    assert result['view']['phase']=='ready'
    assert result['view']['evidence_mode']=='MOCKED' and result['view']['execution_verified'] is False
    assert result['effects']==result['submits']==result['metered']==result['terminal']==1,result
    assert result['status_calls']==(1 if crash_stage=='after_effect' else 0),result
    assert len(result['fences'])==1
    print('SYNTHETIC_RECOVERY',crash_stage,request.tenant_id,first.pid,result['pid'])