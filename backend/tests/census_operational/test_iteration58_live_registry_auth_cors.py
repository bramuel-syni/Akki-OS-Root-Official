"""Iteration 58: live auth/CORS and registry submission guard regression checks."""

# Module focus: auth authority checks + CORS behavior + read-only scope guards.

import os
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

from services.auth import password_hash, user_store


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PASSWORD = "demo-analyst-pw"


def _require_base_url() -> str:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")
    return BASE_URL.rstrip("/")


def _login(email: str, password: str, timeout_seconds: int = 45):
    return requests.post(
        f"{_require_base_url()}/api/auth/login",
        json={"email": email, "password": password},
        timeout=timeout_seconds,
    )


@pytest.fixture(scope="session")
def operator_headers():
    response = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    token = payload.get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def analyst_headers():
    response = _login(ANALYST_EMAIL, ANALYST_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    token = payload.get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def test_i58_auth_login_and_me(operator_headers):
    """Existing operator credentials should login and resolve /auth/me identity."""
    me = requests.get(f"{_require_base_url()}/api/auth/me", headers=operator_headers, timeout=45)
    assert me.status_code == 200
    payload = me.json()
    assert payload.get("email") == OPERATOR_EMAIL
    assert "operator" in (payload.get("roles") or [])


def test_i58_password_hash_uses_bcrypt_2b_prefix():
    """Hash helper still emits canonical bcrypt $2b$ format."""
    hashed = password_hash.hash_password("iteration58-password")
    assert hashed.startswith("$2b$")


def test_i58_auth_code_has_no_lockout_authority_path():
    """Source-level authority check: no lockout policy implementation currently exists."""
    router_code = Path("/app/backend/vendored/extraction_akki/backend/routers/auth.py").read_text().lower()
    store_code = Path("/app/backend/vendored/extraction_akki/backend/services/auth/user_store.py").read_text().lower()
    assert "lockout" not in router_code + store_code
    assert "failed_attempt" not in router_code + store_code


def test_i58_cors_preflight_allowed_and_unlisted_origins_observed():
    """CORS allows configured preview origin and denies unlisted origins."""
    allowed_origin = "https://pensive-goodall-6.preview.emergentagent.com"
    unlisted_origin = "https://disallowed-origin.example"

    allowed = requests.options(
        f"{_require_base_url()}/api/auth/login",
        headers={
            "Origin": allowed_origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,authorization",
        },
        timeout=30,
    )
    denied = requests.options(
        f"{_require_base_url()}/api/auth/login",
        headers={
            "Origin": unlisted_origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,authorization",
        },
        timeout=30,
    )

    assert allowed.status_code in {200, 204}
    assert denied.status_code == 400
    assert allowed.headers.get("access-control-allow-credentials") == "true"
    allowed_origin_echo = allowed.headers.get("access-control-allow-origin")
    assert isinstance(allowed_origin_echo, str) and allowed_origin_echo
    assert allowed_origin_echo != "*"
    assert denied.headers.get("access-control-allow-origin") in {None, ""}


def test_i58_seed_admin_is_create_only_not_password_rotation(monkeypatch):
    """Current seed_admin_if_absent behavior: existing admin is not updated."""
    existing = {"_id": "abc", "email": "admin@example.com", "password_hash": "$2b$old"}

    class _FakeUsers:
        async def find_one(self, query):
            if query.get("email") == "admin@example.com":
                return existing
            return None

        async def insert_one(self, doc):
            raise AssertionError("insert_one should not run for existing admin")

    monkeypatch.setattr(user_store, "db", SimpleNamespace(users=_FakeUsers()))

    import asyncio

    asyncio.run(user_store.seed_admin_if_absent("admin@example.com", "new-pass"))


def test_i58_analyst_cannot_submit_run(analyst_headers):
    """Analyst remains read-only and cannot commission census work."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=analyst_headers,
        json={"source_ids": ["rms_mysql"]},
        timeout=45,
    )
    assert response.status_code == 403


def test_i58_submission_rejects_wrong_worker(operator_headers):
    """Unknown worker IDs are rejected before enqueue."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "worker_id": "worker-not-registered"},
        timeout=45,
    )
    assert response.status_code == 422
    assert "registered external worker" in response.json().get("detail", "").lower()


def test_i58_submission_rejects_raw_credentials(operator_headers):
    """Submission rejects direct credential/shell payload keys."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "password": "forbidden", "shell": "uname -a"},
        timeout=45,
    )
    assert response.status_code == 422
    assert "only admitted source references" in response.json().get("detail", "").lower()


def test_i58_submission_rejects_cross_tenant_source(operator_headers):
    """RMS operator cannot submit DIGICOW source IDs."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["digicow_rds"]},
        timeout=45,
    )
    assert response.status_code == 422
    assert "not admitted to your tenant" in response.json().get("detail", "").lower()
