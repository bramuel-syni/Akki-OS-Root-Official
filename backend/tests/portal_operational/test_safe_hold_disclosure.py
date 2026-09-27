"""Requester-safe projection checks; no raw native errors or hidden identities."""
from services.portal_operational.hold_reasons import disclosure
from services.portal_operational.execution_records import project
from services.portal_operational.models import WorkView
import pytest


def test_unknown_native_error_is_not_disclosed():
    secret='TOKEN=private-internal-host:8888/other-principal'
    result=disclosure(secret)
    assert secret not in str(result)
    assert result['reason_code']=='EXECUTION_HELD'


def test_actual_hold_has_a_precise_safe_next_action():
    result=disclosure('ALLOCATION_CAPACITY_EXCEEDED',receipt_ref='a'*64)
    assert result['reason_code']=='ALLOCATION_CAPACITY_EXCEEDED'
    assert 'allocation' in result['reason']
    assert 'Reconcile' in result['next_action']
    assert result['reason_receipt_ref']=='a'*64


def test_crash_before_portal_view_is_reconcilable_not_assumed_running():
    work=WorkView(request_id='TEST',work_id='TEST',objective_text='TEST',objective_hash='a'*64,
        operation='browse_estate',units=['source'],state='routing',lifecycle_state='Routing',governing_engine='mtafiti',
        created_at='2026-01-01T00:00:00Z',reason_code='ADMISSION_UNRESOLVED',reason='held',history=[])
    events=[{'row':{'hash':'b'*64,'at':{'epoch_s':100}},'payload':{'slot':'dispatch','data':{'action':'submit'}}}]
    projected=project(work,events)
    assert projected.state=='interrupted'
    assert projected.reason_code=='EXECUTOR_RECONCILIATION_REQUIRED'
    assert projected.permitted_actions==['retry','stop']
    assert projected.execution_verified is False


@pytest.mark.parametrize('mode,state',[('measured','ready'),('MOCKED','blocked')])
def test_late_running_view_does_not_reopen_a_canonical_terminal(mode,state):
    work=WorkView(request_id='TEST',work_id='TEST',objective_text='TEST',objective_hash='a'*64,
        operation='browse_estate',units=['source'],state='routing',lifecycle_state='Routing',governing_engine='mtafiti',
        created_at='2026-01-01T00:00:00Z',reason_code='ADMISSION_UNRESOLVED',reason='held',history=[])
    def row(slot,data,ref): return {'row':{'hash':ref,'at':{'epoch_s':100}},'payload':{'slot':slot,'data':data}}
    events=[row('dispatch',{'action':'submit'},'a'*64),
        row('terminal',{'phase':'ready','reason_code':'VERIFIED_RESULT_RECORDED','evidence_mode':mode},'b'*64),
        row('portal_view:late',{'phase':'running','reason_code':'EXECUTOR_RUNNING','evidence_mode':mode},'c'*64)]
    projected=project(work,events)
    assert projected.state==state
    assert projected.reason_receipt_ref=='b'*64
    assert projected.execution_verified==(mode=='measured')
    assert 'stop' not in projected.permitted_actions