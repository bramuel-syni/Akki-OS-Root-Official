"""Iteration 87 live read-only Mα API checks (login + GET status/learning/tier2/job)."""

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


def _login() -> str:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=OPERATOR, timeout=30)
    if response.status_code != 200:
        pytest.skip(f"operator login failed: {response.status_code}")
    token = response.json().get("access_token")
    assert isinstance(token, str) and len(token) > 20
    return token


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {_login()}"}


# Module/feature: Mα status serialization read-only contract.
def test_malpha_status_readonly_contract(auth_headers):
    response = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=auth_headers, timeout=60)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get("tenant_id") == "RMS"
    assert isinstance(data.get("commissions"), list)
    assert isinstance(data.get("jobs"), list)
    assert isinstance(data.get("metering"), dict)


# Module/feature: Mα learning review list read-only contract.
def test_malpha_learning_readonly_contract(auth_headers):
    response = requests.get(f"{BASE_URL}/api/training/malpha/learning", headers=auth_headers, timeout=60)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get("tenant_id") == "RMS"
    assert isinstance(data.get("reviews"), list)


# Module/feature: Mα Tier2 report list read-only contract.
def test_malpha_tier2_readonly_contract(auth_headers):
    response = requests.get(f"{BASE_URL}/api/training/malpha/tier2", headers=auth_headers, timeout=60)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get("tenant_id") == "RMS"
    assert data.get("internal_only") is True
    assert isinstance(data.get("reports"), list)


# Module/feature: Mα job detail GET contract for an existing job when available.
def test_malpha_job_detail_if_any(auth_headers):
    status = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=auth_headers, timeout=60)
    assert status.status_code == 200
    jobs = status.json().get("jobs", [])
    if not jobs:
        pytest.skip("No Mα jobs available for job detail GET check")
    job_id = jobs[0].get("job_id")
    response = requests.get(f"{BASE_URL}/api/training/malpha/jobs/{job_id}", headers=auth_headers, timeout=60)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get("tenant_id") == "RMS"
    assert isinstance(data.get("job"), dict)
    assert data["job"].get("job_id") == job_id
