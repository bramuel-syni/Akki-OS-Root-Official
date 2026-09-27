"""Live auth/runtime checks against public URL; no local host assumptions."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest
import requests


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


def _login(email: str, password: str) -> requests.Response:
    return requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )


@pytest.fixture(scope="module")
def operator_headers() -> dict:
    _require_base_url()
    (operator_email, operator_password), _ = _read_existing_demo_credentials()
    response = _login(operator_email, operator_password)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# Module/feature: login + me baseline for bearer-token session.
def test_login_and_me_with_existing_operator(operator_headers):
    _require_base_url()
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=operator_headers, timeout=20)
    assert response.status_code == 200
    data = response.json()
    assert data.get("email") == "demo.operator@demo.rms.example.com"
    assert isinstance(data.get("roles"), list) and data["roles"]


# Module/feature: runtime status endpoint is auth-scoped and safe by default.
def test_runtime_endpoint_auth_scope_and_safe_defaults(operator_headers):
    _require_base_url()
    anon = requests.get(f"{BASE_URL}/api/portal/activation/runtime", timeout=20)
    assert anon.status_code == 401

    ok = requests.get(f"{BASE_URL}/api/portal/activation/runtime", headers=operator_headers, timeout=20)
    assert ok.status_code == 200
    data = ok.json()
    assert data.get("configured") is False
    assert data.get("worker_paths_bound") == []
    assert data.get("execution_authorized") is False
    assert data.get("live_proof_verified") is False


# Module/feature: runtime payload excludes obvious secrets/identifiers.
def test_runtime_payload_omits_sensitive_fields(operator_headers):
    _require_base_url()
    body = requests.get(f"{BASE_URL}/api/portal/activation/runtime", headers=operator_headers, timeout=20).json()
    assert isinstance(body, dict)
    forbidden_keys = {
        "factory",
        "runtime_factory",
        "principal_id",
        "principal_ids",
        "signer_id",
        "admitted_keys",
        "secret",
        "private_key",
        "api_key",
        "token",
        "url",
        "endpoint",
    }
    assert not any(key in body for key in forbidden_keys)


# Module/feature: current auth is bearer-token based; cookie channel currently absent.
def test_login_cookie_channel_observation():
    _require_base_url()
    (operator_email, operator_password), _ = _read_existing_demo_credentials()
    response = _login(operator_email, operator_password)
    assert response.status_code == 200
    # Observation-only guard: if cookies exist they must be HttpOnly.
    cookie_header = response.headers.get("set-cookie", "")
    if cookie_header:
        assert "httponly" in cookie_header.lower()


# Module/feature: repeated failed login attempts should fail closed without 5xx.
def test_failed_login_attempts_fail_closed_without_server_error():
    _require_base_url()
    statuses = []
    for _ in range(6):
        response = _login("invalid-user@example.com", "invalid-password")
        statuses.append(response.status_code)
    assert all(code in {401, 423, 429} for code in statuses)
