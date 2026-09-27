"""Non-GPU callable-skill query contracts (SYNTHETIC signed fixtures + live API status checks)."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
import requests

sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")
sys.path.insert(0, "/app/backend/tests/activation_controls")
sys.path.insert(0, "/app/backend/tests/portal_operational")

import test_native_control_ledger as native_helpers
import test_native_certificate_chain_paths_bc as native_chain
from contracts.callable_skill_provisioning_v0 import CallableSkillProvisioningV0
from services.activation.native_evidence import Observation
from services.activation.record_shapes import Plan
from services.enforce.control_scope import bind_control_scope
from services.enforce.principal_context_adapter import principal_context
from services.ledger_writer.mongo_control import digest
from services.northena.execution_models import Artifact, Request
from services.portal_operational import query_intents, query_evidence
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held
from services.activation.model_proofs import Grounding


def _env_value(path: str, key: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _base_url() -> str:
    return (os.environ.get("REACT_APP_BACKEND_URL") or _env_value("/app/frontend/.env", "REACT_APP_BACKEND_URL")).strip().rstrip("/")


BASE_URL = _base_url()


@pytest.fixture
def scope_ctx():
    with principal_context("operator"), bind_control_scope({"principal_id": "operator", "tenant_id": "tenant-SYNTHETIC"}):
        yield


@pytest.fixture
def estate():
    return native_helpers.estate.__wrapped__()


def _provisioning(skill_id: str = "skill-synthetic") -> CallableSkillProvisioningV0:
    return CallableSkillProvisioningV0(
        skill_id=skill_id,
        corpus_slice_ref="akki://TEST/deployed-skill",
        key_grant_id="grant-1",
        floor="non_factual",
        scope="source-scope",
        endpoint_path=f"/api/callable_skill/{skill_id}/query",
        provisioned_at="2026-01-01T00:00:00+00:00",
        revoked_at=None,
    )


def _login(email: str, password: str) -> dict[str, str]:
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": password}, timeout=20)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# Module/feature: same idempotency key should replay stable query id for identical body (expected contract).
def test_query_intent_same_key_identical_replay_expected_stable(scope_ctx, estate):
    async def run():
        _, receipts, _ = estate
        scope = {"tenant_id": "tenant-SYNTHETIC", "principal_id": "operator"}
        body = query_intents.QueryIntentBody(query="What is allowed?", idempotency_key="query-idem-001")
        first = await query_intents.submit(receipts.db, scope, "skill-1", _provisioning("skill-1"), body)
        second = await query_intents.submit(receipts.db, scope, "skill-1", _provisioning("skill-1"), body)
        assert first["row"]["run_id"] == second["row"]["run_id"]

    asyncio.run(run())


# Module/feature: changed query under same key conflicts to protect frozen identity.
def test_query_intent_changed_query_conflicts(scope_ctx, estate):
    async def run():
        _, receipts, _ = estate
        scope = {"tenant_id": "tenant-SYNTHETIC", "principal_id": "operator"}
        await query_intents.submit(
            receipts.db,
            scope,
            "skill-1",
            _provisioning("skill-1"),
            query_intents.QueryIntentBody(query="Question A", idempotency_key="query-idem-002"),
        )
        with pytest.raises(Held, match="SKILL_QUERY_IDEMPOTENCY_CONFLICT"):
            await query_intents.submit(
                receipts.db,
                scope,
                "skill-1",
                _provisioning("skill-1"),
                query_intents.QueryIntentBody(query="Question B", idempotency_key="query-idem-002"),
            )

    asyncio.run(run())


# Module/feature: signed skill grounding result is verified via native evidence (SYNTHETIC chain only).
def test_signed_skill_grounding_positive_synthetic(scope_ctx, estate):
    async def run():
        keys, receipts, _ = estate
        keys.permission_override = (
            "activation:plan",
            "activation:allocation",
            "activation:worker",
            "activation:approval:scope-group",
            "activation:approval:spend-group",
            "activation:approval:answering-group",
            "activation:observation:anchor",
            "activation:observation:skill_response",
        )
        request = Request(
            request_id="REQ-QUERY-GROUNDING-SYNTHETIC",
            tenant_id="tenant-SYNTHETIC",
            principal_id="operator",
            kind="skill",
            engine="solva",
            objective_sha256="a" * 64,
            input_refs=("akki://TEST/deployed-skill", "akki://TEST/query"),
            scope_refs=("source-scope",),
            deadline_epoch=keys.now + 900,
            result_floor="non_factual",
        )
        allocation_ref = await receipts.record(keys.receipt("allocation", {
            "terms_ref": "terms-1",
            "limits": [
                {"dimension": "spend", "unit": "USD", "quantity": "7"},
                {"dimension": "wall_clock", "unit": "seconds", "quantity": "100"},
            ],
        }))
        worker_ref = await receipts.record(keys.receipt("worker", {
            "runtime_id": "worker-SYNTHETIC",
            "executor_version": "test-1",
            "kinds": ["skill"],
            "enforced_dimensions": ["spend", "wall_clock"],
            "enforcement_protocol": "akki.runtime.limits/1",
            "implementation_workspace_touched_data": False,
        }, signer="worker"))
        plan = Plan.model_validate_json(json.dumps({
            "request": request.model_dump(mode="json"),
            "groups": [
                {"group": "scope-group", "purpose": "scope", "members": ["scope-person"], "quorum": 1},
                {"group": "spend-group", "purpose": "expenditure", "members": ["finance-person"], "quorum": 1},
                {"group": "answering-group", "purpose": "answering", "members": ["answering-person"], "quorum": 1},
            ],
            "purposes": ["answering"],
            "acceptance_script_sha256": "1" * 64,
            "snapshot_hashes": ["b" * 64],
            "limits": [
                {"dimension": "spend", "unit": "USD", "quantity": "7"},
                {"dimension": "wall_clock", "unit": "seconds", "quantity": "100"},
            ],
            "allocation_ref": allocation_ref,
            "worker_ref": worker_ref,
            "terms_ref": "terms-1",
            "policy_epoch": 1,
            "dial_versions": {
                "custody_floor": "v1",
                "approving_authority": "v1",
                "external_crossing": "v1",
                "disclosure_counterparties": "v1",
            },
            "policy_versions": {
                "crossing_decision_table": "v1",
                "acceptance_standard": "v1",
                "cleanliness_pack": "v1",
            },
            "termination_grace_seconds": 5,
        }))
        plan_ref = await receipts.record(keys.receipt("plan", plan.model_dump(mode="json"), signer="owner", request=request))
        for signer, group in (("scope-person", "scope-group"), ("finance-person", "spend-group"), ("answering-person", "answering-group")):
            await receipts.record(keys.receipt("approval", {
                "plan_ref": plan_ref,
                "group": group,
                "decision": "approved",
                "reason": "SYNTHETIC approval",
            }, signer=signer, request=request))

        journal = LedgerJournal(receipts.db)
        await journal.append(request, "request", {"request_sha256": request.digest(), "request": request.model_dump(mode="json")})
        artifact = Artifact(
            ref="akki://TEST/skill-answer",
            sha256="e" * 64,
            size_bytes=1,
            tenant_id=request.tenant_id,
            class_label="non_factual",
        )
        await journal.append(request, "registry", {
            "evidence_mode": "measured",
            "artifacts": [artifact.model_dump(mode="json")],
        })
        anchor_payload = {
            "snapshot_sha256": "b" * 64,
            "anchor_sha256": "9" * 64,
            "answer_sha256": artifact.sha256,
            "query_ref": request.input_refs[-1],
        }
        anchor_ref = await receipts.record(keys.receipt("observation", {
            "category": "anchor",
            "context_sha256": request.digest(),
            "claim_sha256": digest(anchor_payload),
            "evidence_mode": "measured",
        }, signer="anchorer", request=request))
        grounding = Grounding(
            query_ref=request.input_refs[-1],
            answer_sha256=artifact.sha256,
            anchors=({
                "snapshot_sha256": "b" * 64,
                "anchor_sha256": "9" * 64,
                "source_receipt_ref": anchor_ref,
            },),
            context_lost=False,
            context_loss_disclosed=False,
        )
        await receipts.record(keys.receipt("observation", Observation(
            category="skill_response",
            context_sha256=request.digest(),
            claim_sha256=digest({
                "request_sha256": request.digest(),
                "artifact": artifact.model_dump(mode="json"),
                "grounding": grounding.model_dump(mode="json"),
            }),
            evidence_mode="measured",
            grounding=grounding,
        ).model_dump(mode="json"), signer="worker", request=request))

        runtime = SimpleNamespace(receipts=receipts)
        coordinator = SimpleNamespace(journal=LedgerJournal(receipts.db))
        result = await query_evidence.grounding(runtime, coordinator, request)
        assert result["outcome"] == "ready"
        assert result["execution_verified"] is True
        assert "artifact_refs" in result and result["artifact_refs"]
        assert "answer" not in result and "answer_stub" not in result

    asyncio.run(run())


# Module/feature: live unauthenticated endpoints fail closed and never 500.
def test_live_non_gpu_endpoints_anonymous_fail_closed():
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")
    request_id = uuid4().hex
    query_id = uuid4().hex
    delivery_id = uuid4().hex
    endpoints = [
        ("post", f"{BASE_URL}/api/callable_skill/{uuid4().hex}/query-intents", {"query": "hello", "idempotency_key": "live-idem-001"}),
        ("get", f"{BASE_URL}/api/callable_skill/{uuid4().hex}/queries/{query_id}", None),
        ("post", f"{BASE_URL}/api/portal/requests/{request_id}/delivery", {"artifact_ref": "akki://TEST/a", "idempotency_key": "live-idem-002"}),
        ("get", f"{BASE_URL}/api/portal/requests/{request_id}/deliveries/{delivery_id}", None),
    ]
    for method, url, payload in endpoints:
        response = requests.request(method, url, json=payload, timeout=20)
        assert response.status_code in {401, 403, 404, 409, 422}
        assert response.status_code != 500
        assert len(response.text) < 6000


# Module/feature: analyst cannot read operator-owned synthetic query id via principal-scoped records.
def test_live_analyst_cannot_cross_query_scope_if_query_exists():
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")
    operator = _login("demo.operator@demo.rms.example.com", "demo-operator-pw")
    analyst = _login("demo.analyst@demo.rms.example.com", "demo-analyst-pw")
    skill_id = f"missing-skill-{uuid4().hex}"
    query_id = f"skill-query-{hashlib.sha256(f'{skill_id}-x'.encode()).hexdigest()}"

    op_read = requests.get(f"{BASE_URL}/api/callable_skill/{skill_id}/queries/{query_id}", headers=operator, timeout=20)
    an_read = requests.get(f"{BASE_URL}/api/callable_skill/{skill_id}/queries/{query_id}", headers=analyst, timeout=20)
    assert op_read.status_code in {404, 409}
    assert an_read.status_code in {404, 409, 403}
    assert an_read.status_code != 500
