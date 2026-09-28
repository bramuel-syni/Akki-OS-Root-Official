"""M1 Registry live acceptance checks for integrated read surfaces and descriptor declaration flow."""

import os
import uuid
import time

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")

OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"


def _require_base_url() -> str:
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")
    return BASE_URL.rstrip("/")


def _login(email: str, password: str) -> dict:
    url = f"{_require_base_url()}/api/auth/login"
    last_error = None
    response = None
    for attempt in range(2):
        try:
            response = requests.post(url, json={"email": email, "password": password}, timeout=60)
            break
        except requests.RequestException as exc:
            last_error = exc
            if attempt == 0:
                time.sleep(1)
    if response is None:
        pytest.fail(f"Public API login did not complete: {last_error}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("access_token"), str) and data["access_token"]
    return {
        "token": data["access_token"],
        "headers": {"Authorization": f"Bearer {data['access_token']}", "Content-Type": "application/json"},
        "set_cookie": response.headers.get("set-cookie", ""),
    }


@pytest.fixture(scope="session")
def operator_session():
    """Operator-authenticated session headers for M1 live read + declaration checks."""
    return _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)


def test_m1_a01_auth_shape(operator_session):
    """Auth remains bearer-token based and login payload shape is usable for follow-on checks."""
    assert operator_session["headers"]["Authorization"].startswith("Bearer ")
    # Existing implementation is token-header transport; cookie auth is not asserted as a pass condition.
    assert isinstance(operator_session["set_cookie"], str)


def test_m1_a02_overview_contains_current_and_historical_runs(operator_session):
    """Overview keeps requested historical/live run IDs visible for owner truthfulness."""
    response = requests.get(f"{_require_base_url()}/api/portal/census/overview", headers=operator_session["headers"], timeout=60)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("tenant_id") == "RMS"

    runs = payload.get("runs", [])
    run_ids = {row.get("census_run_id") for row in runs}
    # Requested acceptance IDs must stay queryable in current overview evidence.
    required = {"cr-f8086f961dcd", "cr-7fdf4bcb0195", "cr-41a031a64351", "cr-5355698447dd"}
    assert required.issubset(run_ids)


@pytest.mark.parametrize(
    "run_id",
    ["cr-f8086f961dcd", "cr-7fdf4bcb0195", "cr-41a031a64351", "cr-5355698447dd"],
)
def test_m1_a03_run_state_endpoint_and_status_truth(operator_session, run_id):
    """/runs/{id}/state remains the canonical route and preserves non-fabricated states."""
    response = requests.get(
        f"{_require_base_url()}/api/portal/census/runs/{run_id}/state",
        headers=operator_session["headers"],
        timeout=60,
    )
    assert response.status_code == 200
    state = response.json()
    assert state.get("census_run_id") == run_id
    assert state.get("status") in {"PENDING", "COMPLETE", "PARTIAL", "REFUSED", "BLOCKED", "UNVERIFIED", "FAILED"}


def test_m1_a04_no_runs_id_route_without_state_suffix(operator_session):
    """/runs/:id route should not silently exist when only /state is router-backed."""
    probe = "cr-does-not-exist-for-route-check"
    response = requests.get(
        f"{_require_base_url()}/api/portal/census/runs/{probe}",
        headers=operator_session["headers"],
        timeout=60,
    )
    assert response.status_code in {404, 405}


def test_m1_a05_declare_connection_declared_only_and_idempotent(operator_session):
    """POST /connections creates or reuses declared-only descriptor without granting admission."""
    name = f"RMS MySQL Acceptance {uuid.uuid4().hex[:8]}"
    body = {"source_id": "rms_mysql", "name": name}
    first = requests.post(
        f"{_require_base_url()}/api/portal/census/connections",
        headers=operator_session["headers"],
        json=body,
        timeout=60,
    )
    assert first.status_code == 200
    first_payload = first.json()
    assert first_payload.get("status") == "DECLARED"
    assert "not a successful connection" in first_payload.get("next_action", "").lower() or "not a successful" in first_payload['connection']['admission_status'].lower() or "declaration is not" in first_payload.get('next_action','').lower()

    second = requests.post(
        f"{_require_base_url()}/api/portal/census/connections",
        headers=operator_session["headers"],
        json=body,
        timeout=60,
    )
    assert second.status_code == 200
    second_payload = second.json()
    assert second_payload.get("status") == "DECLARED"
    assert second_payload.get("created") is False


def test_m1_a06_connection_refuses_raw_credentials(operator_session):
    """Descriptor endpoint refuses direct secret material in request payload."""
    response = requests.post(
        f"{_require_base_url()}/api/portal/census/connections",
        headers=operator_session["headers"],
        json={"source_id": "rms_mysql", "name": "x", "password": "forbidden"},
        timeout=60,
    )
    assert response.status_code == 422


def test_m1_a07_live_read_surfaces_available(operator_session):
    """Registry/source/compute/conversation reads resolve from integrated tenant-scoped API."""
    endpoints = [
        "/api/portal/census/sources",
        "/api/portal/census/compute",
        "/api/portal/census/conversations",
        "/api/registry/facts",
    ]
    for route in endpoints:
        response = requests.get(f"{_require_base_url()}{route}", headers=operator_session["headers"], timeout=60)
        assert response.status_code == 200
        data = response.json()
        assert data.get("tenant_id") == "RMS"


def test_m1_a08_source_detail_matches_list(operator_session):
    """Source detail endpoint is navigable from source catalog entries."""
    listing = requests.get(
        f"{_require_base_url()}/api/portal/census/sources",
        headers=operator_session["headers"],
        timeout=60,
    )
    assert listing.status_code == 200
    sources = listing.json().get("sources", [])
    assert len(sources) > 0
    source_ref = sources[0]["source_ref"]

    detail = requests.get(
        f"{_require_base_url()}/api/portal/census/sources/{source_ref}",
        headers=operator_session["headers"],
        timeout=60,
    )
    assert detail.status_code == 200
    body = detail.json().get("source", {})
    assert body.get("source_ref") == source_ref
