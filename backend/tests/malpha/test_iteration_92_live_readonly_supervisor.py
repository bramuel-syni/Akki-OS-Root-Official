"""Iteration 92 live read-only checks: operator login, supervisor GET, Mα status GET, and actual health-route discovery."""

import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv("/app/frontend/.env")

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    raise RuntimeError("REACT_APP_BACKEND_URL is required")
BASE_URL = BASE_URL.rstrip("/")

OPERATOR = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}


# Module/feature: read-only operator auth + supervisor route contract.
def _operator_headers():
    login = requests.post(f"{BASE_URL}/api/auth/login", json=OPERATOR, timeout=30)
    if login.status_code != 200:
        pytest.skip(f"operator login failed: {login.status_code}")
    token = login.json().get("access_token")
    if not token:
        pytest.skip("operator access_token missing")
    return {"Authorization": f"Bearer {token}"}


def test_supervisor_endpoint_is_readonly_get_with_operator_token():
    headers = _operator_headers()
    response = requests.get(f"{BASE_URL}/api/training/malpha/supervisor", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("tenant_id") == "RMS"
    assert isinstance(body.get("lanes"), dict)
    for lane_name, lane in body["lanes"].items():
        assert isinstance(lane_name, str)
        assert isinstance(lane, dict)


# Module/feature: read-only Mα status evidence without dispatch/submit/tick calls.
def test_malpha_status_get_only_snapshot_contract():
    headers = _operator_headers()
    response = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("tenant_id") == "RMS"
    assert isinstance(body.get("jobs"), list)
    assert isinstance(body.get("commissions"), list)


# Module/feature: actual shield health/readiness route discovery for this fork.
def test_legacy_health_routes_unmounted_and_shield_allowlists_reachable():
    shield_route = requests.get(f"{BASE_URL}/api/healthz/shield", timeout=30)
    assert shield_route.status_code == 404

    health = requests.get(f"{BASE_URL}/api/healthz", timeout=30)
    assert health.status_code == 404

    ready = requests.get(f"{BASE_URL}/api/readyz", timeout=30)
    assert ready.status_code == 404

    # Actual live Shield route in this fork.
    allowlists = requests.get(f"{BASE_URL}/api/shield/allowlists", timeout=30)
    assert allowlists.status_code == 200, allowlists.text
    body = allowlists.json()
    assert isinstance(body.get("masking_tiers"), list)
    assert isinstance(body.get("residency"), dict)
