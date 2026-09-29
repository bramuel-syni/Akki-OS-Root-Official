"""Iteration 59: M2 watch operational reader + legacy boundary regression checks."""

# Module focus: tenant-scoped watch read routes, role guards, and legacy refusal boundaries.

import os
from typing import Dict, List

import pytest
import requests

from services.watch import operational_reads as watch_operational_reads


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
OPERATOR_EMAIL = "demo.operator@demo.rms.example.com"
OPERATOR_PASSWORD = "demo-operator-pw"
ANALYST_EMAIL = "demo.analyst@demo.rms.example.com"
ANALYST_PASSWORD = "demo-analyst-pw"

WATCH_STATE_ENDPOINTS = [
    "/api/portal/watch/state",
    "/api/watch/state",
    "/api/grey_mirror/state",
]

LEGACY_WRITE_ENDPOINTS = [
    "/api/watch/verdict",
    "/api/watch/act",
    "/api/watch/mark",
]


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


@pytest.mark.parametrize("endpoint", WATCH_STATE_ENDPOINTS)
def test_i59_watch_state_anonymous_is_401(endpoint):
    response = requests.get(f"{_require_base_url()}{endpoint}", timeout=45)
    assert response.status_code == 401


@pytest.mark.parametrize("endpoint", WATCH_STATE_ENDPOINTS)
def test_i59_watch_state_analyst_is_403(endpoint, analyst_headers):
    response = requests.get(f"{_require_base_url()}{endpoint}", headers=analyst_headers, timeout=45)
    assert response.status_code == 403


def test_i59_watch_state_operator_200_and_matches_census_run_cursor(operator_headers):
    watch_response = requests.get(f"{_require_base_url()}/api/portal/watch/state", headers=operator_headers, timeout=45)
    assert watch_response.status_code == 200
    watch_payload = watch_response.json()
    assert watch_payload.get("tenant_id") == "RMS"

    records = watch_payload.get("records") or []
    observation_run_ids = {
        row.get("census_run_id")
        for row in records
        if row.get("kind") == "observation" and isinstance(row.get("census_run_id"), str)
    }

    overview_response = requests.get(f"{_require_base_url()}/api/portal/census/overview", headers=operator_headers, timeout=45)
    assert overview_response.status_code == 200
    overview_payload = overview_response.json()
    census_run_ids = {
        row.get("census_run_id")
        for row in (overview_payload.get("runs") or [])
        if isinstance(row.get("census_run_id"), str)
    }

    assert watch_payload.get("counts", {}).get("observations") == len(census_run_ids)
    assert observation_run_ids == census_run_ids


def test_i59_watch_state_aliases_return_same_run_ids(operator_headers):
    run_sets = []
    for endpoint in WATCH_STATE_ENDPOINTS:
        response = requests.get(f"{_require_base_url()}{endpoint}", headers=operator_headers, timeout=45)
        assert response.status_code == 200
        payload = response.json()
        run_ids = {
            row.get("census_run_id")
            for row in (payload.get("records") or [])
            if row.get("kind") == "observation" and isinstance(row.get("census_run_id"), str)
        }
        run_sets.append(run_ids)

    assert run_sets[0] == run_sets[1] == run_sets[2]


def test_i59_watch_state_no_digicow_or_unassigned_or_raw_profile_leak(operator_headers):
    response = requests.get(f"{_require_base_url()}/api/portal/watch/state", headers=operator_headers, timeout=45)
    assert response.status_code == 200
    payload = response.json()
    records = payload.get("records") or []

    serialized = str(records).lower()
    assert "digicow" not in serialized
    assert "unassigned" not in serialized
    assert "_raw" not in serialized
    assert "password" not in serialized


@pytest.mark.parametrize("endpoint", LEGACY_WRITE_ENDPOINTS)
def test_i59_watch_legacy_authority_anonymous_401(endpoint):
    response = requests.post(f"{_require_base_url()}{endpoint}", json={}, timeout=45)
    assert response.status_code == 401


def test_i59_watch_legacy_authority_auth_bound_409_and_no_mutation(operator_headers):
    before = requests.get(f"{_require_base_url()}/api/portal/watch/state", headers=operator_headers, timeout=45)
    assert before.status_code == 200
    before_counts = before.json().get("counts") or {}

    refusal_bodies: List[Dict] = []
    for endpoint in LEGACY_WRITE_ENDPOINTS:
        response = requests.post(
            f"{_require_base_url()}{endpoint}",
            headers=operator_headers,
            json={},
            timeout=45,
        )
        assert response.status_code == 409
        body = response.json()
        refusal_bodies.append(body)
        detail = (body.get("detail") or "").lower()
        assert "no watch record or protection was changed" in detail

    after = requests.get(f"{_require_base_url()}/api/portal/watch/state", headers=operator_headers, timeout=45)
    assert after.status_code == 200
    after_counts = after.json().get("counts") or {}

    for key in ("verdicts", "actions", "marks"):
        assert before_counts.get(key) == after_counts.get(key)
    assert len(refusal_bodies) == len(LEGACY_WRITE_ENDPOINTS)


def test_i59_watch_tenant_filter_conflicting_explicit_tenant_and_census_ref_isolated(monkeypatch):
    actor = {"principal_id": "u1", "tenant_id": "RMS", "roles": ["operator"]}
    mock_runs = [
        {
            "census_run_id": "cr-a1b2c3d4e5f6",
            "source_ids": ["rms_mysql"],
            "principal_id": "u1",
            "status": "COMPLETE",
            "created_at": "2026-02-01T00:00:00Z",
        }
    ]

    def _mock_load_kind(kind: str):
        if kind != "verdicts":
            return []
        return [
            {"record_id": "v-conflict", "tenant_id": "DIGICOW", "census_run_id": "cr-a1b2c3d4e5f6", "verdict_class": "x"},
            {"record_id": "v-linked-none", "tenant_id": None, "census_run_id": "cr-a1b2c3d4e5f6", "verdict_class": "x"},
            {"record_id": "v-unlinked-none", "tenant_id": None, "census_run_id": "cr-ffffffffffff", "verdict_class": "x"},
            {"record_id": "v-owned", "tenant_id": "RMS", "census_run_id": "cr-123456789abc", "verdict_class": "x"},
        ]

    monkeypatch.setattr(watch_operational_reads.operational_store, "runs", lambda tenant: mock_runs if tenant == "RMS" else [])
    monkeypatch.setattr(watch_operational_reads, "_load_kind", _mock_load_kind)

    state = watch_operational_reads.state_for(actor)
    visible_verdict_rows = [row for row in state.get("records", []) if row.get("kind") == "verdict"]
    visible_ids = {row.get("record_id") for row in visible_verdict_rows}

    assert "v-conflict" not in visible_ids
    assert "v-unlinked-none" not in visible_ids
    assert visible_ids == {"v-linked-none", "v-owned"}
