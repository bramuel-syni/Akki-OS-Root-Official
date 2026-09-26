"""Callable-skill query safety tests (live auth gates + TEST-ONLY/MOCKED refusal path)."""

import asyncio
import hashlib
import json
import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests
from pydantic import ValidationError

from routers import transform_forms
from services.portal_operational import skill_query


def _env_value(path: str, key: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _resolve_base_url() -> str:
    return (os.environ.get("REACT_APP_BACKEND_URL") or _env_value("/app/frontend/.env", "REACT_APP_BACKEND_URL")).strip().rstrip("/")


BASE_URL = _resolve_base_url()
OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"


def _require_base_url() -> None:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")


def _login(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert isinstance(token, str) and token
    return token


@pytest.fixture(scope="session")
def operator_headers() -> dict:
    _require_base_url()
    token = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# Module/feature: strict SkillQuery accepts query only and rejects extras/blank query
def test_skill_query_strict_payload_rejection_unit():
    with pytest.raises(ValidationError):
        skill_query.SkillQuery.model_validate({"query": "ok", "answer_stub": "x", "class_label": "y"})
    with pytest.raises(ValidationError):
        skill_query.SkillQuery.model_validate({"query": "   "})


# Module/feature: refusal route propagates canonical refusal from admitted gate fixture (MOCKED)
def test_query_route_mocked_gate_propagates_refusal_record(monkeypatch):
    query_text = "Can this be executed?"
    body = skill_query.SkillQuery(query=query_text)
    expected_sha = hashlib.sha256(query_text.encode()).hexdigest()

    async def _gate_ok(request, skill_id, db):
        return SimpleNamespace(skill_id=skill_id)

    @asynccontextmanager
    async def _scope(_request):
        yield {"tenant_id": "DIGICOW", "principal_id": "principal-1"}

    async def _refuse(_db, _scope_value, skill_id, _query):
        return {
            "outcome": "refused",
            "reason_code": "SKILL_EXECUTOR_UNADMITTED",
            "skill_id": skill_id,
            "query_sha256": expected_sha,
            "receipt_hash": "row-hash-1",
            "execution_verified": False,
        }

    monkeypatch.setattr(transform_forms, "require_governed_skill_query", _gate_ok)
    monkeypatch.setattr(transform_forms, "portal_scope", _scope)
    monkeypatch.setattr(transform_forms, "refuse_unadmitted", _refuse)

    response = asyncio.run(transform_forms.query_callable_skill("skill-mocked", request=object(), body=body))
    payload = json.loads(response.body.decode("utf-8"))

    assert response.status_code == 409
    assert payload["reason_code"] == "SKILL_EXECUTOR_UNADMITTED"
    assert payload["query_sha256"] == expected_sha
    assert "answer_stub" not in payload and "class_label" not in payload


# Module/feature: refusal ledger payload stores query hash only (no raw query leak)
def test_refuse_unadmitted_hashes_query_and_omits_raw_query(monkeypatch):
    captured = {}
    scope = {"tenant_id": "DIGICOW", "principal_id": "principal-1"}
    body = skill_query.SkillQuery(query="sensitive ask")

    async def _append_event(_db, **kwargs):
        captured.update(kwargs)
        return {"row": {"hash": "receipt-hash-1"}}

    monkeypatch.setattr(skill_query, "append_event", _append_event)
    result = asyncio.run(skill_query.refuse_unadmitted(db=object(), scope=scope, skill_id="skill-1", query=body))

    expected_sha = hashlib.sha256("sensitive ask".encode()).hexdigest()
    payload = captured["payload"]

    assert result["outcome"] == "refused"
    assert result["reason_code"] == "SKILL_EXECUTOR_UNADMITTED"
    assert result["receipt_hash"] == "receipt-hash-1"
    assert payload["query_sha256"] == expected_sha
    assert "query" not in payload
    assert "answer_stub" not in result and "class_label" not in result


# Module/feature: ledger writer outage propagates and fails closed
def test_refuse_unadmitted_ledger_outage_fails_closed(monkeypatch):
    async def _raise(*_args, **_kwargs):
        raise RuntimeError("ledger unavailable")

    monkeypatch.setattr(skill_query, "append_event", _raise)
    with pytest.raises(RuntimeError):
        asyncio.run(
            skill_query.refuse_unadmitted(
                db=object(),
                scope={"tenant_id": "DIGICOW", "principal_id": "principal-1"},
                skill_id="skill-1",
                query=skill_query.SkillQuery(query="health check"),
            )
        )


# Module/feature: live API denies anonymous query attempts
def test_live_callable_skill_query_anonymous_401():
    _require_base_url()
    response = requests.post(
        f"{BASE_URL}/api/callable_skill/{uuid.uuid4().hex}/query",
        json={"query": "hello"},
        timeout=20,
    )
    assert response.status_code == 401


# Module/feature: live API returns skill-not-found for authenticated caller
def test_live_callable_skill_query_authenticated_missing_skill_404(operator_headers):
    _require_base_url()
    skill_id = f"missing-skill-{uuid.uuid4().hex}"
    response = requests.post(
        f"{BASE_URL}/api/callable_skill/{skill_id}/query",
        headers=operator_headers,
        json={"query": "hello"},
        timeout=20,
    )
    assert response.status_code == 404
    data = response.json()
    assert data.get("reason") == "skill_not_found"


# Module/feature: live strict body gate rejects forged result/class fields
def test_live_callable_skill_query_forged_answer_class_rejected_422(operator_headers):
    _require_base_url()
    response = requests.post(
        f"{BASE_URL}/api/callable_skill/{uuid.uuid4().hex}/query",
        headers=operator_headers,
        json={"query": "hello", "answer_stub": "forged", "class_label": "forged"},
        timeout=20,
    )
    assert response.status_code == 422
