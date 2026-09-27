"""Live architecture contract tests for /execution/advance held-control seam.

These tests hit the public URL and verify truthful held/unbound behavior.
"""

from __future__ import annotations

import os
import time
import uuid
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

OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PASSWORD = "demo-analyst-pw"


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
    return _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)


@pytest.fixture(scope="session")
def analyst_headers() -> dict:
    _require_base_url()
    return _login(ANALYST_EMAIL, ANALYST_PASSWORD)


def _create_request(headers: dict, *, operation: str) -> str:
    payload = {
        "objective_text": f"execution advance contract {operation}",
        "operation": operation,
        "units": ["rms_mysql"],
        "idempotency_key": f"exec-advance-{uuid.uuid4().hex}",
    }
    response = requests.post(f"{BASE_URL}/api/portal/requests", headers=headers, json=payload, timeout=20)
    assert response.status_code == 202
    request_id = response.json().get("request_id")
    assert isinstance(request_id, str) and request_id
    return request_id


# Module/feature: held advance records control intent with unbound executor and immutable deadline semantics.
def test_execution_advance_held_unbound_replay_and_changed_deadline_conflict(operator_headers):
    _require_base_url()
    request_id = _create_request(operator_headers, operation="browse_estate")
    deadline = int(time.time()) + 3600

    first = requests.post(
        f"{BASE_URL}/api/portal/requests/{request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": deadline},
        timeout=20,
    )
    assert first.status_code == 200
    first_data = first.json()
    assert first_data["phase"] == "held"
    assert first_data["reason_code"] == "EXECUTOR_ADAPTER_UNBOUND"
    assert first_data.get("execution_verified") is False

    replay = requests.post(
        f"{BASE_URL}/api/portal/requests/{request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": deadline},
        timeout=20,
    )
    assert replay.status_code == 200
    replay_data = replay.json()
    assert replay_data["phase"] == "held"
    assert replay_data["reason_code"] == "EXECUTOR_ADAPTER_UNBOUND"

    changed = requests.post(
        f"{BASE_URL}/api/portal/requests/{request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": deadline + 1},
        timeout=20,
    )
    assert changed.status_code == 409


# Module/feature: execution advance authz/refusal matrix for anonymous, analyst, unknown, and foreign principal access.
def test_execution_advance_authz_unknown_and_foreign_request_refusals(operator_headers, analyst_headers):
    _require_base_url()
    own_request_id = _create_request(operator_headers, operation="browse_estate")
    unknown = requests.post(
        f"{BASE_URL}/api/portal/requests/req-unknown-{uuid.uuid4().hex}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert unknown.status_code == 404

    anonymous = requests.post(
        f"{BASE_URL}/api/portal/requests/{own_request_id}/execution/advance",
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert anonymous.status_code == 401

    analyst = requests.post(
        f"{BASE_URL}/api/portal/requests/{own_request_id}/execution/advance",
        headers=analyst_headers,
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert analyst.status_code == 403

    analyst_unknown = requests.post(
        f"{BASE_URL}/api/portal/requests/req-unknown-analyst-{uuid.uuid4().hex}/execution/advance",
        headers=analyst_headers,
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert analyst_unknown.status_code == 403

    operator_created = _create_request(operator_headers, operation="browse_estate")
    foreign = requests.post(
        f"{BASE_URL}/api/portal/requests/{operator_created}/execution/advance",
        headers=analyst_headers,
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert foreign.status_code == 403


# Module/feature: unsupported operation and malformed payload must fail closed.
def test_execution_advance_unsupported_operation_and_malformed_payload_refused(operator_headers):
    _require_base_url()
    unsupported_request_id = _create_request(operator_headers, operation="processed_intelligence")
    unsupported = requests.post(
        f"{BASE_URL}/api/portal/requests/{unsupported_request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": int(time.time()) + 3600},
        timeout=20,
    )
    assert unsupported.status_code == 409

    browse_request_id = _create_request(operator_headers, operation="browse_estate")
    malformed = requests.post(
        f"{BASE_URL}/api/portal/requests/{browse_request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": "soon"},
        timeout=20,
    )
    assert malformed.status_code == 422

    extra = requests.post(
        f"{BASE_URL}/api/portal/requests/{browse_request_id}/execution/advance",
        headers=operator_headers,
        json={"deadline_epoch": int(time.time()) + 3600, "extra": True},
        timeout=20,
    )
    assert extra.status_code == 422
