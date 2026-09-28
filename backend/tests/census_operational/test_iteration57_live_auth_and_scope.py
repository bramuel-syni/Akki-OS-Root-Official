"""Iteration 57 live regressions: auth responsiveness and census submission scope guards."""

import os
import time

import pytest
import requests


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
    response = requests.post(
        f"{_require_base_url()}/api/auth/login",
        json={"email": email, "password": password},
        timeout=timeout_seconds,
    )
    return response


@pytest.fixture(scope="session")
def operator_headers():
    """Operator auth for authenticated census reads/writes in this suite."""
    response = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    token = payload.get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def analyst_headers():
    """Analyst auth for role-guard checks."""
    response = _login(ANALYST_EMAIL, ANALYST_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    token = payload.get("access_token")
    assert isinstance(token, str) and token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def test_i57_auth_login_body_delivery_and_shape():
    """Auth login responds with complete JSON body and token pair (no stall)."""
    response = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload.get("access_token"), str) and payload["access_token"]
    assert isinstance(payload.get("refresh_token"), str) and payload["refresh_token"]
    assert payload.get("token_type") == "Bearer"
    identity = payload.get("identity") or {}
    assert identity.get("email") == OPERATOR_EMAIL


def test_i57_auth_me_after_login(operator_headers):
    """/api/auth/me remains responsive and aligned with signed-in identity."""
    response = requests.get(f"{_require_base_url()}/api/auth/me", headers=operator_headers, timeout=45)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("email") == OPERATOR_EMAIL
    assert "operator" in (payload.get("roles") or [])


def test_i57_auth_http_only_cookie_present_on_login_response():
    """Auth response should set an HttpOnly cookie for browser session hardening."""
    response = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie", "")
    assert "HttpOnly" in set_cookie


def test_i57_auth_bruteforce_lockout_after_five_failures():
    """After repeated wrong-password attempts, valid login should be blocked temporarily."""
    for _ in range(5):
        failed = _login(OPERATOR_EMAIL, "definitely-wrong-password", timeout_seconds=20)
        assert failed.status_code == 401
        time.sleep(0.1)

    post_fail_valid = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD, timeout_seconds=25)
    assert post_fail_valid.status_code in {423, 429}


def test_i57_cors_preflight_credentials_and_explicit_origin():
    """CORS preflight should not use wildcard origin when credentials are enabled."""
    origin = "https://pensive-goodall-6.preview.emergentagent.com"
    response = requests.options(
        f"{_require_base_url()}/api/auth/login",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,authorization",
        },
        timeout=30,
    )
    assert response.status_code in {200, 204}
    assert response.headers.get("access-control-allow-credentials") == "true"
    assert response.headers.get("access-control-allow-origin") == origin


def test_i57_role_guard_analyst_cannot_submit_run(analyst_headers):
    """Analyst remains read-only and cannot commission census work."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=analyst_headers,
        json={"source_ids": ["rms_mysql"]},
        timeout=45,
    )
    assert response.status_code == 403


def test_i57_submission_rejects_wrong_worker(operator_headers):
    """Submission blocks unregistered worker IDs before queue enqueue."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "worker_id": "worker-not-registered"},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "registered external worker" in detail.lower()


def test_i57_submission_rejects_raw_credentials_or_shell_fields(operator_headers):
    """Submission payload refuses unsupported keys like shell/credential material."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "password": "forbidden", "shell": "uname -a"},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "only admitted source references" in detail.lower()


def test_i57_submission_rejects_cross_tenant_source(operator_headers):
    """RMS operator cannot submit DIGICOW source IDs."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["digicow_rds"]},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "not admitted to your tenant" in detail.lower()


def test_i57_source_refs_type_validation(operator_headers):
    """source_refs must be list of canonical source_<24hex> identities."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "source_refs": "not-a-list"},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "source-region references" in detail.lower()


def test_i57_source_refs_membership_validation(operator_headers):
    """source_refs outside selected source group are rejected."""
    sources = requests.get(f"{_require_base_url()}/api/portal/census/sources", headers=operator_headers, timeout=45)
    assert sources.status_code == 200
    items = sources.json().get("sources", [])
    mysql_refs = [s["source_ref"] for s in items if s.get("source_id") == "rms_mysql"]
    other_refs = [s["source_ref"] for s in items if s.get("source_id") != "rms_mysql"]
    if not mysql_refs or not other_refs:
        pytest.skip("Insufficient heterogeneous source refs for membership validation")

    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql"], "source_refs": [other_refs[0]]},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "outside the commissioned tenant/scope" in detail.lower() or "selected source group" in detail.lower()


def test_i57_source_refs_requires_each_selected_group_has_region(operator_headers):
    """When multiple source_ids are selected, each must have at least one selected region."""
    sources = requests.get(f"{_require_base_url()}/api/portal/census/sources", headers=operator_headers, timeout=45)
    assert sources.status_code == 200
    items = sources.json().get("sources", [])
    by_group = {}
    for row in items:
        by_group.setdefault(row.get("source_id"), []).append(row.get("source_ref"))

    if not by_group.get("rms_mysql") or not by_group.get("rms_obs"):
        pytest.skip("Need refs from at least rms_mysql and rms_obs for this validation")

    response = requests.post(
        f"{_require_base_url()}/api/portal/census/run",
        headers=operator_headers,
        json={"source_ids": ["rms_mysql", "rms_obs"], "source_refs": [by_group["rms_mysql"][0]]},
        timeout=45,
    )
    assert response.status_code == 422
    detail = response.json().get("detail", "")
    assert "each selected source group must have a selected region" in detail.lower()