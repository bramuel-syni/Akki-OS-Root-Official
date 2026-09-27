"""SYNTHETIC clocks/trainer only. Tests never invoke actual SSH or process source data."""
from dataclasses import replace
from types import SimpleNamespace
import pytest
from services.activation.runtime_limits import RuntimeEnvelope, RuntimeLimiter
from services.activation.record_shapes import Quantity
from services.northena.execution_models import Held
from services.training_runner import runner, persistence, recorded_effect, moac_emitter
from services.training_runner.ssh_seam import SeamResult
from contracts.training_run_v0 import TrainingRunV0


def limiter():
    clock=[100,0]
    envelope=RuntimeEnvelope(protocol="akki.runtime.limits/1",request_sha256="a"*64,plan_ref="b"*64,
        reservation_ref="c"*64,runtime_id="TEST-worker",operation_key="TEST-operation",fence=1,
        starts_epoch=100,stop_work_by_epoch=190,terminate_by_epoch=200,
        limits=(Quantity(dimension="wall_clock",unit="seconds",quantity="100"),
                Quantity(dimension="scanned_records",unit="records",quantity="10"),
                Quantity(dimension="spend",unit="USD",quantity="0")))
    return RuntimeLimiter(envelope,wall_clock=lambda:clock[0],monotonic_clock=lambda:clock[1]),clock


def test_scan_ceiling_checked_before_batch():
    guard,_=limiter()
    guard.before_batch((Quantity(dimension="scanned_records",unit="records",quantity="10"),))
    with pytest.raises(Held,match="WOULD_BE_EXCEEDED"):
        guard.before_batch((Quantity(dimension="scanned_records",unit="records",quantity="1"),))


def test_zero_external_spend_is_enforced():
    guard,_=limiter()
    with pytest.raises(Held,match="WOULD_BE_EXCEEDED"):
        guard.before_batch((Quantity(dimension="spend",unit="USD",quantity="0.01"),))


def test_monotonic_deadline_survives_wall_clock_rollback():
    guard,clock=limiter(); clock[:]=[50,91]
    with pytest.raises(Held,match="TERMINATION_REQUIRED"):
        guard.before_batch((Quantity(dimension="spend",unit="USD",quantity="0"),))


def test_termination_is_inside_the_ceiling():
    guard,clock=limiter(); clock[:]=[201,101]
    with pytest.raises(Held,match="TERMINATION_CEILING_EXCEEDED"): guard.termination_observed()


def test_late_worker_admission_does_not_reset_monotonic_budget():
    original,_=limiter()
    clock=[150,0]
    guard=RuntimeLimiter(original.envelope,wall_clock=lambda:clock[0],monotonic_clock=lambda:clock[1])
    clock[:]=[110,40]
    with pytest.raises(Held,match="TERMINATION_REQUIRED"):
        guard.before_batch((Quantity(dimension="spend",unit="USD",quantity="0"),))


@pytest.fixture
def training(tmp_path,monkeypatch):
    monkeypatch.setattr(persistence,"_ADMITS_DIR",tmp_path/"admits")
    monkeypatch.setattr(persistence,"_RUNS_DIR",tmp_path/"runs")
    (tmp_path/"admits").mkdir(); (tmp_path/"runs").mkdir()
    monkeypatch.setenv("CROSSING_RECEIPT_DIR",str(tmp_path/"meter"))
    monkeypatch.setenv("AKKI_GPU_HOST","TEST-not-a-host")
    run=TrainingRunV0(run_id="TEST-single",recipe_version="TEST-recipe",base_model_id="TEST-base",adapter_kind="lora",
                      material_admit_ref="TEST-material",ssh_mode="mock",started_at="2026-01-01T00:00:00Z")
    persistence.upsert_run(run)
    calls=[]
    result=SeamResult(mocked=True,exit_code=0,stdout_summary="SYNTHETIC",m_a_input=.1,m_b_input=.05,
                      wallclock_seconds=10,gpu_hours=.01,m_e_input=.85)
    monkeypatch.setattr(runner.ssh_seam,"execute_lora_train",lambda *a:(calls.append(a) or result))
    from services.critic_pass import producer_seam
    monkeypatch.setattr(producer_seam,"route_through_seam",lambda **k:SimpleNamespace())
    monkeypatch.setattr(producer_seam,"verdict_summary",lambda v:{"findings_count":0,"critic_instance_id":"TEST"})
    from services.whitepapers import draft
    monkeypatch.setattr(draft,"draft_whitepaper",lambda v:SimpleNamespace(whitepaper_id="TEST-wp"))
    return run,calls,result,tmp_path


def test_execute_emit_close_and_replays_make_one_training_call(training):
    run,calls,_,root=training
    runner.execute_run(run.run_id); runner.execute_run(run.run_id)
    card=runner.emit_moac_for_run(run.run_id)["moac_card"]
    assert runner.emit_moac_for_run(run.run_id)["moac_card"]==card
    closed=runner.close_run(run.run_id,card)
    assert closed.status=="closed_rejected"
    runner.close_run(run.run_id,card); runner.execute_run(run.run_id)
    assert len(calls)==1
    assert not list((root/"meter").glob("*.json"))


def test_reporting_before_execution_never_trains(training):
    run,calls,_,_=training
    with pytest.raises(RuntimeError,match="NOT_RECORDED"): runner.emit_moac_for_run(run.run_id)
    assert calls==[]


def test_unknown_outcome_is_not_replayed(training,monkeypatch):
    run,_,_,_=training
    calls=[]
    def failed(*a): calls.append(a); raise TimeoutError("SYNTHETIC uncertainty")
    monkeypatch.setattr(runner.ssh_seam,"execute_lora_train",failed)
    with pytest.raises(TimeoutError): runner.execute_run(run.run_id)
    with pytest.raises(RuntimeError,match="OUTCOME_UNCERTAIN"): runner.execute_run(run.run_id)
    assert len(calls)==1


def test_close_cannot_accept_caller_invented_release(training):
    run,_,_,_=training
    runner.execute_run(run.run_id)
    card=runner.emit_moac_for_run(run.run_id)["moac_card"]
    with pytest.raises(ValueError): runner.close_run(run.run_id,{**card,"accept_for_service":True})


@pytest.mark.parametrize("mocked",[True,False])
def test_absent_evaluation_is_null_not_zero_or_live(training,mocked):
    run,_,result,_=training
    card=moac_emitter.emit_six_check_card(run.run_id,replace(result,mocked=mocked),run.recipe_version,run.base_model_id)
    assert all(c["measured_value"] is None and c["measurement_status"]=="not_measured" for c in card["criteria"])
    assert card["accept_for_service"] is False
    assert card["evidence_state"]==("MOCKED" if mocked else "PARTIALLY LIVE")