"""Supplemental execution_ports + execution_builders contract tests (no network, MOCKED only)."""

from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from contracts.skill_provisioning_record_v0 import SkillProvisioningRecordV0
from contracts.training_run_v0 import TrainingRunV0
from services.northena.execution_builders import (
    evaluation_request,
    skill_request,
    source_request,
    training_request,
)
from services.northena import execution_composition
from services.northena.execution_models import Artifact, Held, Request, Usage, WorkerResult
from services.northena.execution_ports import EngineAdapter


def _request(kind="source", engine="mtafiti"):
    floor = "non_factual" if kind == "skill" else None
    return Request(
        request_id=f"req-{kind}",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        kind=kind,
        engine=engine,
        objective_sha256="a" * 64,
        input_refs=("akki://input/1",),
        scope_refs=("scope-1",),
        deadline_epoch=9_999_999,
        result_floor=floor,
    )


def _measured_result(request, operation_key="op-1", fence=1):
    art = Artifact(
        ref="akki://artifact/a",
        sha256="b" * 64,
        size_bytes=1,
        tenant_id=request.tenant_id,
        class_label=request.result_floor or "non_factual",
    )
    return WorkerResult(
        operation_key=operation_key,
        request_sha256=request.digest(),
        executor_id="exec-1",
        fence=fence,
        state="complete",
        receipt_ref="akki://receipt/1",
        artifacts=(art,),
        usage=(Usage(unit="tokens", quantity="1"),),
        evidence_mode="measured",
    )


# Module/feature: EngineAdapter requires explicit finite timeout and async callbacks.
def test_engine_adapter_timeout_and_async_callback_contracts():
    async def ok_submit(request, key, fence, authority):
        return _measured_result(request, key, fence)

    async def ok_status(request, key, fence):
        return _measured_result(request, key, fence)

    async def ok_cancel(request, key, fence):
        return _measured_result(request, key, fence)

    with pytest.raises(ValueError):
        EngineAdapter("source", "mtafiti", ok_submit, ok_status, ok_cancel, timeout_seconds=0)

    def bad_sync(*_args, **_kwargs):
        return {}

    with pytest.raises(ValueError):
        EngineAdapter("source", "mtafiti", bad_sync, ok_status, ok_cancel, timeout_seconds=1.0)


# Module/feature: EngineAdapter enforces kind/engine binding, timeout, strict result shape and measured-only admission.
def test_engine_adapter_binding_timeout_and_result_strictness():
    async def slow_submit(_request, _key, _fence, _authority):
        await asyncio.sleep(0.05)
        return {}

    async def mocked_status(request, key, fence):
        measured = _measured_result(request, key, fence)
        return measured.model_copy(update={"evidence_mode": "MOCKED"})

    async def malformed_cancel(_request, _key, _fence):
        return {"bad": "payload"}

    async def measured_submit(request, key, fence, authority):
        return _measured_result(request, key, fence)

    adapter = EngineAdapter(
        kind="source",
        engine="mtafiti",
        submit_rpc=slow_submit,
        status_rpc=mocked_status,
        cancel_rpc=malformed_cancel,
        timeout_seconds=0.01,
    )
    request = _request("source", "mtafiti")

    with pytest.raises(asyncio.TimeoutError):
        asyncio.run(adapter.submit(request, "op-1", 1, object()))

    adapter_fast = EngineAdapter(
        kind="source",
        engine="mtafiti",
        submit_rpc=measured_submit,
        status_rpc=mocked_status,
        cancel_rpc=malformed_cancel,
        timeout_seconds=0.5,
    )

    with pytest.raises(Held):
        asyncio.run(adapter_fast.submit(_request("training", "targeta"), "op-1", 1, object()))
    with pytest.raises(Held):
        asyncio.run(adapter_fast.status(request, "op-1", 1))
    with pytest.raises(Exception):
        asyncio.run(adapter_fast.cancel(request, "op-1", 1))


# Module/feature: descriptor builders enforce lawful/hash refs and keep mutable training progress out of frozen identity.
def test_execution_descriptor_builders_with_real_models_and_hash_ref_guards():
    src = source_request(
        {
            "census_run_id": "run-1",
            "tenant_id": "DIGICOW",
            "connect_source_descriptor": {
                "version": "operational-v1",
                "source_ids": ["rms_mysql"],
                "lawful_basis_sha256": "c" * 64,
            },
        },
        principal_id="principal-1",
        deadline_epoch=123,
    )
    assert src.kind == "source"

    with pytest.raises(Held):
        source_request(
            {
                "census_run_id": "run-1",
                "tenant_id": "DIGICOW",
                "connect_source_descriptor": {
                    "version": "operational-v1",
                    "source_ids": ["rms_mysql"],
                    "lawful_basis_sha256": "invalid",
                },
            },
            principal_id="principal-1",
            deadline_epoch=123,
        )

    provisioning = SkillProvisioningRecordV0(
        skill_id="skill-1",
        corpus_slice_ref="akki://corpus/slice-1",
        key_grant_id="grant-1",
        floor="non_factual",
        scope="scope://skill",
        endpoint_path="/api/callable_skill/skill-1/query",
        provisioned_at="2026-01-01T00:00:00+00:00",
        revoked_at=None,
    )
    skill = skill_request(
        provisioning,
        request_id="skill-req-1",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        query_ref="akki://query/q1",
        query_sha256="d" * 64,
        deadline_epoch=123,
    )
    assert skill.kind == "skill"

    with pytest.raises(Held):
        skill_request(
            provisioning.model_copy(update={"revoked_at": "2026-02-01T00:00:00+00:00"}),
            request_id="skill-req-2",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            query_ref="akki://query/q2",
            query_sha256="d" * 64,
            deadline_epoch=123,
        )
    with pytest.raises(Held):
        skill_request(
            provisioning.model_copy(update={"corpus_slice_ref": "http://foreign"}),
            request_id="skill-req-3",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            query_ref="akki://query/q3",
            query_sha256="d" * 64,
            deadline_epoch=123,
        )
    with pytest.raises(Held):
        skill_request(
            provisioning,
            request_id="skill-req-4",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            query_ref="akki://query/q4",
            query_sha256="not-a-hash",
            deadline_epoch=123,
        )
    with pytest.raises(ValidationError):
        skill_request(
            provisioning,
            request_id="skill-req-5",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            query_ref="http://query/unsafe",
            query_sha256="d" * 64,
            deadline_epoch=123,
        )

    run_admitted = TrainingRunV0(
        run_id="tr-1",
        recipe_version="training_params@v0/r1",
        base_model_id="base-1",
        adapter_kind="lora",
        material_admit_ref="admit-1",
        ssh_mode="mock",
        status="admitted",
        started_at="2026-01-01T00:00:00+00:00",
    )
    run_progressed = run_admitted.model_copy(update={"status": "running_mock"})

    tr1 = training_request(
        run_admitted,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        corpus_manifest_ref="akki://corpus/manifest-a",
        moac_criteria_ref="akki://moac/criteria-a",
        scope_refs=["scope://training"],
        deadline_epoch=123,
    )
    tr2 = training_request(
        run_progressed,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        corpus_manifest_ref="akki://corpus/manifest-a",
        moac_criteria_ref="akki://moac/criteria-a",
        scope_refs=["scope://training"],
        deadline_epoch=123,
    )
    assert tr1.objective_sha256 == tr2.objective_sha256

    tr3 = training_request(
        run_admitted,
        tenant_id="DIGICOW",
        principal_id="principal-1",
        corpus_manifest_ref="akki://corpus/manifest-b",
        moac_criteria_ref="akki://moac/criteria-a",
        scope_refs=["scope://training"],
        deadline_epoch=123,
    )
    assert tr1.objective_sha256 != tr3.objective_sha256

    ev1 = evaluation_request(
        request_id="ev-1",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        model_artifact_ref="akki://model/a",
        heldout_manifest_ref="akki://heldout/a",
        moac_criteria_ref="akki://moac/a",
        scope_refs=["scope://eval"],
        deadline_epoch=123,
    )
    ev2 = evaluation_request(
        request_id="ev-1",
        tenant_id="DIGICOW",
        principal_id="principal-1",
        model_artifact_ref="akki://model/a",
        heldout_manifest_ref="akki://heldout/b",
        moac_criteria_ref="akki://moac/a",
        scope_refs=["scope://eval"],
        deadline_epoch=123,
    )
    assert ev1.objective_sha256 != ev2.objective_sha256
    with pytest.raises(ValidationError):
        evaluation_request(
            request_id="ev-2",
            tenant_id="DIGICOW",
            principal_id="principal-1",
            model_artifact_ref="file:///tmp/model.bin",
            heldout_manifest_ref="akki://heldout/a",
            moac_criteria_ref="akki://moac/a",
            scope_refs=["scope://eval"],
            deadline_epoch=123,
        )


# Module/feature: production composition remains UNBOUND (no mock success claims) across source/skill/training/evaluation.
@pytest.mark.parametrize(
    "kind,engine,floor",
    [
        ("source", "mtafiti", None),
        ("skill", "solva", "non_factual"),
        ("training", "targeta", None),
        ("evaluation", "targeta", None),
    ],
)
def test_production_authority_boundary_stays_unbound_for_all_kinds(monkeypatch, kind, engine, floor):
    async def _admitted(_db, _scope):
        return {"licence_admitted": True}

    monkeypatch.setattr(execution_composition, "read_view", _admitted)
    boundary = execution_composition.ExistingAuthorityBoundary(db=object())
    request = _request(kind=kind, engine=engine)
    if floor:
        request = request.model_copy(update={"result_floor": floor})
    with pytest.raises(Held) as exc:
        asyncio.run(boundary.authorize(request, "dispatch"))
    assert exc.value.reason_code == "OPERATION_AUTHORITY_NOT_BOUND"
