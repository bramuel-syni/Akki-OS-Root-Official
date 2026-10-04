"""Iteration 88 live read-only Mα API checks (status/learning/capacity job JSON)."""

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


def _headers():
    login = requests.post(f"{BASE_URL}/api/auth/login", json=OPERATOR, timeout=30)
    if login.status_code != 200:
        pytest.skip(f"operator login failed: {login.status_code}")
    token = login.json().get("access_token")
    if not token:
        pytest.skip("operator access_token missing")
    return {"Authorization": f"Bearer {token}"}


# Module/feature: live status envelope read-only contract.
def test_malpha_status_learning_and_capacity_fields_readonly():
    headers = _headers()
    response = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("tenant_id") == "RMS"
    assert isinstance(body.get("commissions"), list)
    assert isinstance(body.get("jobs"), list)
    assert isinstance(body.get("metering"), dict)

    # Capacity reallocation is optional; if present, it must be JSON-safe and must not expose Mongo _id.
    for commission in body.get("commissions", []):
        if "capacity_reallocation" in commission:
            cap = commission["capacity_reallocation"]
            assert isinstance(cap, dict)
            assert "_id" not in cap


# Module/feature: learning review list is GET-only and JSON-bounded.
def test_malpha_learning_reviews_readonly_contract():
    headers = _headers()
    response = requests.get(f"{BASE_URL}/api/training/malpha/learning", headers=headers, timeout=60)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("tenant_id") == "RMS"
    assert isinstance(body.get("reviews"), list)
    for review in body["reviews"]:
        assert "_id" not in review


# Module/feature: job detail JSON projection remains read-only and secret-free.
def test_malpha_job_detail_readonly_if_available():
    headers = _headers()
    status = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=headers, timeout=60)
    assert status.status_code == 200, status.text
    jobs = status.json().get("jobs", [])
    if not jobs:
        pytest.skip("No Mα jobs available for detail read")
    job_id = jobs[0].get("job_id")
    assert isinstance(job_id, str) and job_id.startswith("m9j-")
    detail = requests.get(f"{BASE_URL}/api/training/malpha/jobs/{job_id}", headers=headers, timeout=60)
    assert detail.status_code == 200, detail.text
    body = detail.json()
    assert body.get("tenant_id") == "RMS"
    assert isinstance(body.get("job"), dict)
    assert body["job"].get("job_id") == job_id
    assert "_id" not in body["job"]
