"""Live API contracts for activation profile + certificate validation endpoints."""

from __future__ import annotations

import json
import os
import re
import uuid
from pathlib import Path

import pytest
import requests

from test_activation_validation_red import _base_document


def _env_value(path: str, key: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


BASE_URL = (os.environ.get("REACT_APP_BACKEND_URL") or _env_value("/app/frontend/.env", "REACT_APP_BACKEND_URL")).strip().rstrip("/")


def _read_existing_demo_credentials() -> tuple[tuple[str, str], tuple[str, str]]:
    text = Path("/app/memory/test_credentials.md").read_text(encoding="utf-8")
    operator = re.search(r"\|\s*(demo\.operator@[^|\s]+)\s*\|\s*([^|\s]+)", text)
    analyst = re.search(r"\|\s*(demo\.analyst@[^|\s]+)\s*\|\s*([^|\s]+)", text)
    if not operator or not analyst:
        pytest.skip("Operator/analyst credentials not found in /app/memory/test_credentials.md")
    return (operator.group(1), operator.group(2)), (analyst.group(1), analyst.group(2))


def _require_base_url() -> None:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")


def _login(email: str, password: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def operator_headers() -> dict:
    _require_base_url()
    (operator_email, operator_password), _ = _read_existing_demo_credentials()
    return _login(operator_email, operator_password)


@pytest.fixture(scope="session")
def analyst_headers() -> dict:
    _require_base_url()
    _, (analyst_email, analyst_password) = _read_existing_demo_credentials()
    return _login(analyst_email, analyst_password)


def _operator_scope(operator_headers: dict) -> tuple[str, str]:
    me = requests.get(f"{BASE_URL}/api/auth/me", headers=operator_headers, timeout=20)
    assert me.status_code == 200
    principal_id = me.json().get("user_id")
    assert isinstance(principal_id, str) and principal_id

    census = requests.get(f"{BASE_URL}/api/census/records", headers=operator_headers, timeout=20)
    assert census.status_code == 200
    tenant_id = census.json().get("tenant_id")
    assert isinstance(tenant_id, str) and tenant_id
    return tenant_id, principal_id


def _valid_certificate_for_scope(tenant_id: str, principal_id: str) -> dict:
    _ = principal_id
    cert = _base_document()
    cert["certificate_id"] = f"cert_{uuid.uuid4().hex}"
    cert["identity"]["estate_id"] = tenant_id
    cert["identity"].pop("proposing_principal_id", None)
    cert["identity"]["tenant_id"] = tenant_id
    return cert


# Module/feature: profile endpoint auth gate + canonical metadata.
def test_activation_profile_auth_and_shape(operator_headers):
    _require_base_url()
    anon = requests.get(f"{BASE_URL}/api/portal/activation/profile", timeout=20)
    assert anon.status_code == 401

    ok = requests.get(f"{BASE_URL}/api/portal/activation/profile", headers=operator_headers, timeout=20)
    assert ok.status_code == 200
    data = ok.json()
    assert data.get("profile_id") == "akki.activation.validation/1"
    assert data.get("certificate_issuance") is False
    assert isinstance(data.get("owner_schema_sha256"), str) and len(data["owner_schema_sha256"]) == 64
    assert isinstance(data.get("crossing_policy_sha256"), str) and len(data["crossing_policy_sha256"]) == 64


# Module/feature: validate endpoint authz matrix.
def test_activation_validate_authz(analyst_headers):
    _require_base_url()
    minimal = {"certificate": {"certificate_id": "x"}}

    anon = requests.post(f"{BASE_URL}/api/portal/activation/certificates/validate", json=minimal, timeout=20)
    assert anon.status_code == 401

    non_operator = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/validate",
        headers=analyst_headers,
        json=minimal,
        timeout=20,
    )
    assert non_operator.status_code == 403


# Module/feature: malformed, duplicate-key, non-finite, and oversized payloads are rejected.
def test_activation_validate_rejects_malformed_and_oversized(operator_headers):
    _require_base_url()
    endpoint = f"{BASE_URL}/api/portal/activation/certificates/validate"

    dup_key_raw = '{"certificate": {"certificate_id": "a", "certificate_id": "b"}}'
    dup = requests.post(endpoint, headers=operator_headers, data=dup_key_raw, timeout=20)
    assert dup.status_code == 422

    nan_raw = '{"certificate": {"certificate_id": "a", "schema_version": NaN}}'
    nan = requests.post(endpoint, headers=operator_headers, data=nan_raw, timeout=20)
    assert nan.status_code == 422

    huge = {"certificate": {"filler": "x" * 300000}}
    over = requests.post(endpoint, headers=operator_headers, json=huge, timeout=20)
    assert over.status_code == 413


# Module/feature: strict body forbids caller-submitted evidence/verifier fields.
def test_activation_validate_rejects_extra_top_level_fields(operator_headers):
    _require_base_url()
    response = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/validate",
        headers=operator_headers,
        json={"certificate": _base_document(), "evidence": {"forged": True}, "verifier": "forged"},
        timeout=20,
    )
    assert response.status_code == 422


# Module/feature: scope mismatch body receives 403 on shape-valid submission.
def test_activation_validate_scope_mismatch_returns_403(operator_headers):
    _require_base_url()
    tenant_id, principal_id = _operator_scope(operator_headers)
    cert = _valid_certificate_for_scope(tenant_id, principal_id)
    cert["identity"]["estate_id"] = "DIGICOW" if tenant_id != "DIGICOW" else "RMS"

    response = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/validate",
        headers=operator_headers,
        json={"certificate": cert},
        timeout=20,
    )
    assert response.status_code == 403


# Module/feature: own-scope valid shape/semantic body returns held evidence-not-bound observation.
def test_activation_validate_own_scope_returns_held_not_issued_with_audit_ref(operator_headers):
    _require_base_url()
    tenant_id, principal_id = _operator_scope(operator_headers)
    cert = _valid_certificate_for_scope(tenant_id, principal_id)

    response = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/validate",
        headers=operator_headers,
        json={"certificate": cert},
        timeout=20,
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("valid") is False
    assert data.get("schema_valid") is True
    assert data.get("semantics_valid") is True
    assert data.get("certificate_issued") is False
    assert data.get("execution_authorized") is False
    assert isinstance(data.get("audit_ref"), str) and data["audit_ref"]
    issue_codes = [i.get("code") for i in data.get("issues", []) if isinstance(i, dict)]
    assert "EVIDENCE_VERIFIER_NOT_BOUND" in issue_codes


# Module/feature: response redaction never leaks submitted signature/secret-like strings.
def test_activation_validate_response_redacts_submitted_signature_text(operator_headers):
    _require_base_url()
    tenant_id, principal_id = _operator_scope(operator_headers)
    cert = _valid_certificate_for_scope(tenant_id, principal_id)
    leak_probe = "SECRET_SIGNATURE_SHOULD_NOT_LEAK_9f1d2b"
    cert["issuer"]["signature"] = leak_probe

    response = requests.post(
        f"{BASE_URL}/api/portal/activation/certificates/validate",
        headers=operator_headers,
        json={"certificate": cert},
        timeout=20,
    )
    assert response.status_code == 200
    body_text = json.dumps(response.json())
    assert leak_probe not in body_text
