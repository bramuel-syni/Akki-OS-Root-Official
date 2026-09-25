"""Live API contract checks for CP-CENSUS-OPERATIONAL-V1 using public URL only."""

import json
import os
import uuid
from pathlib import Path

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")

OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PASSWORD = "demo-analyst-pw"


def _require_base_url():
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")


def _login(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("access_token"), str) and data["access_token"]
    return data["access_token"]


@pytest.fixture(scope="session")
def operator_headers():
    """Operator-authenticated headers for census read/write-gated endpoint checks."""
    _require_base_url()
    token = _login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def analyst_headers():
    """Analyst-authenticated headers for role restriction checks."""
    _require_base_url()
    token = _login(ANALYST_EMAIL, ANALYST_PASSWORD)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def test_t01_disk_continuity_artifacts_present():
    """Continuity/prototype artifacts remain on disk and non-empty."""
    files = [
        Path("/app/assessment_workspace/notes/census_operational_v1/GROUNDING.md"),
        Path("/app/assessment_workspace/STATE/OBJECTIVES/CP_CENSUS_OPERATIONAL_V1.md"),
    ]
    for path in files:
        assert path.exists() and path.is_file()
        assert path.read_text(encoding="utf-8").strip()


@pytest.mark.parametrize(
    "route",
    [
        "/api/portal/census/overview",
        "/api/portal/census/records",
        "/api/portal/census/latest",
        "/api/census/latest",
        "/api/census/records",
        "/api/census/history",
        "/api/registry/facts",
    ],
)
def test_t02_login_required_before_reads(route):
    """Current and legacy census/registry reads deny anonymous users."""
    _require_base_url()
    response = requests.get(f"{BASE_URL}{route}", timeout=20)
    assert response.status_code == 401


def test_t03_server_owned_membership_and_rms_scope(operator_headers):
    """Tenant membership is server-derived and RMS responses exclude legacy Digicow census 1/2."""
    response = requests.get(f"{BASE_URL}/api/portal/census/overview", headers=operator_headers, timeout=20)
    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == "RMS"
    assert isinstance(data.get("records"), list)
    numbers = {r.get("census_number") for r in data["records"]}
    assert 1 not in numbers and 2 not in numbers
    assert all(r.get("tenant_id") == "RMS" for r in data["records"])


def test_t03_forged_tenant_in_submission_rejected(operator_headers):
    """Client-provided foreign tenant in body is rejected."""
    body = {
        "tenant_id": "DIGICOW",
        "source_ids": ["rms_mysql"],
        "idempotency_key": f"test-{uuid.uuid4().hex[:24]}",
    }
    response = requests.post(f"{BASE_URL}/api/portal/census/run", headers=operator_headers, json=body, timeout=20)
    assert response.status_code == 422


def test_t04_records_and_latest_agree_for_census4(operator_headers):
    """/records and /latest expose tenant-scoped real census data including census4."""
    records_response = requests.get(f"{BASE_URL}/api/portal/census/records", headers=operator_headers, timeout=20)
    latest_response = requests.get(f"{BASE_URL}/api/census/latest", headers=operator_headers, timeout=20)
    record4_response = requests.get(f"{BASE_URL}/api/portal/census/records/4", headers=operator_headers, timeout=20)

    assert records_response.status_code == 200
    assert latest_response.status_code == 200
    assert record4_response.status_code == 200

    records = records_response.json()["records"]
    latest = latest_response.json().get("census")
    rec4 = record4_response.json()["record"]

    assert any(r.get("census_number") == 4 for r in records)
    assert rec4.get("census_number") == 4
    assert rec4.get("tenant_id") == "RMS"
    if latest:
        top = records[0]
        assert latest.get("record_id") == top.get("record_id")


def test_t05_estimated_counts_and_no_sensitive_leak(operator_headers):
    """Census metrics are aggregate and responses do not leak SQL/topology/credentials."""
    response = requests.get(f"{BASE_URL}/api/portal/census/latest", headers=operator_headers, timeout=20)
    assert response.status_code == 200
    payload = response.json()
    census = payload.get("census") or {}

    # Owner-provided expected census4 aggregate signal.
    assert census.get("database_count") == 41
    assert census.get("table_count") == 2642
    assert census.get("row_count_estimate") == 428786937
    assert census.get("volume_bytes") is None
    assert census.get("quality_percent") is None
    assert census.get("licensed_percent") is None

    serialized = json.dumps(payload).lower()
    forbidden = ["password", "cluster_host", "select ", "information_schema", "credentials", "private_ip"]
    assert all(marker not in serialized for marker in forbidden)


def test_t06_analyst_cannot_run(analyst_headers):
    """Analyst role is read-only and cannot commission census."""
    body = {
        "source_ids": ["rms_mysql"],
        "idempotency_key": f"test-{uuid.uuid4().hex[:24]}",
    }
    response = requests.post(f"{BASE_URL}/api/portal/census/run", headers=analyst_headers, json=body, timeout=20)
    assert response.status_code == 403


def test_t06_rejects_malformed_or_forbidden_submission_fields(operator_headers):
    """Foreign source, malformed body, and client command/credential injection are refused."""
    invalid_payloads = [
        {"source_ids": ["digicow_rds"], "idempotency_key": f"test-{uuid.uuid4().hex[:24]}"},
        {"source_ids": [], "idempotency_key": f"test-{uuid.uuid4().hex[:24]}"},
        {"source_ids": ["rms_mysql"], "password": "x", "idempotency_key": f"test-{uuid.uuid4().hex[:24]}"},
        {"source_ids": ["rms_mysql"], "sql": "SELECT * FROM secret", "idempotency_key": f"test-{uuid.uuid4().hex[:24]}"},
    ]
    for payload in invalid_payloads:
        response = requests.post(f"{BASE_URL}/api/portal/census/run", headers=operator_headers, json=payload, timeout=20)
        assert response.status_code == 422


def test_t08_t14_known_live_attempt_is_truthfully_blocked(operator_headers):
    """Known attempted live run remains blocked/unverified, never falsely COMPLETE."""
    run_id = "cr-a29e3b7b16ae"
    response = requests.get(
        f"{BASE_URL}/api/portal/census/runs/{run_id}/state",
        headers=operator_headers,
        timeout=20,
    )
    assert response.status_code == 200
    row = response.json()
    assert row.get("status") != "COMPLETE"
    assert row.get("stage") in {"blocked", "unverified", "partial", "interrupted"}


def test_t11_portal_and_registry_views_match(operator_headers):
    """/dap and /os/admin/estate backend views come from same tenant-scoped source data."""
    portal = requests.get(f"{BASE_URL}/api/portal/census/overview", headers=operator_headers, timeout=20)
    registry = requests.get(f"{BASE_URL}/api/registry/facts", headers=operator_headers, timeout=20)
    assert portal.status_code == 200
    assert registry.status_code == 200

    portal_data = portal.json()
    registry_data = registry.json()
    assert portal_data.get("tenant_id") == registry_data.get("tenant_id") == "RMS"
    assert portal_data.get("latest", {}).get("record_id") == registry_data.get("latest", {}).get("record_id")
    assert len(portal_data.get("records", [])) == len(registry_data.get("records", []))
