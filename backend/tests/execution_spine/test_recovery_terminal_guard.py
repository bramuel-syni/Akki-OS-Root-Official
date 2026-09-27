"""SYNTHETIC protocol regression tests; no native workload or SSH access."""
import asyncio
from services.northena.execution_models import Held
from test_execution_fault_recovery_and_contract_supplemental import _build_stack, _with_scope


def test_conflicting_worker_terminal_receipts_are_explicitly_held():
    async def run():
        _,request,_,executor,_,coordinator=_build_stack("TEST-conflicting-terminal")
        result=await executor.status(request,"test-key",1)
        await coordinator.bank_observation(request,result)
        conflicting=result.model_copy(update={"state":"cancelled","artifacts":(),"receipt_ref":"akki://TEST/other-terminal"})
        try:
            await coordinator.bank_observation(request,conflicting)
        except Held as exc:
            assert exc.reason_code=="EXECUTOR_TERMINAL_OBSERVATION_CONFLICT"
        else:
            raise AssertionError("Contradictory terminal facts were accepted")
    _,request,*_=_build_stack("TEST-conflicting-terminal")
    asyncio.run(_with_scope(request,run()))


def test_delayed_running_reply_reuses_recorded_terminal_facts():
    async def run():
        _,request,_,executor,_,coordinator=_build_stack("TEST-late-running")
        result=await executor.status(request,"test-key",1)
        await coordinator.bank_observation(request,result)
        delayed=result.model_copy(update={"state":"running","artifacts":(),"receipt_ref":"akki://TEST/delayed-running"})
        reconciled=await coordinator.bank_observation(request,delayed)
        assert reconciled==result
        rows=await coordinator.journal.read(request)
        assert not any(r['slot'].startswith('observation:') and r['data']['result']['state']=='running' for r in rows)
    _,request,*_=_build_stack("TEST-late-running")
    asyncio.run(_with_scope(request,run()))


def test_equivalent_terminal_receipts_do_not_duplicate_effect_facts():
    async def run():
        _,request,_,executor,_,coordinator=_build_stack("TEST-equivalent-terminal")
        result=await executor.status(request,"test-key",1)
        await coordinator.bank_observation(request,result)
        await coordinator.bank_observation(request,result.model_copy(update={"receipt_ref":"akki://TEST/another-copy"}))
        rows=await coordinator.journal.read(request)
        assert len([r for r in rows if r["slot"]=="worker_outcome"])==1
    _,request,*_=_build_stack("TEST-equivalent-terminal")
    asyncio.run(_with_scope(request,run()))