"""Live API verification: authenticated GET list + GET metadata only (no submissions)."""
import json
import os
import re

import pytest
import requests


if os.environ.get('AKKI_LC_LIVE_TEST') != '1':
    pytest.skip('Opt-in live metadata checks; no training submissions.', allow_module_level=True)

BASE_URL = os.environ['REACT_APP_BACKEND_URL'].rstrip('/')

TIMEOUT = 60
RMS_OPERATOR = (os.environ['AKKI_TEST_OPERATOR_EMAIL'], os.environ['AKKI_TEST_OPERATOR_PASSWORD'])
SMOKE_JOB_ID = "lcj-07c848c58923"
JOB_ID_RE = re.compile(r"^lcj-[a-f0-9]{12}$")


def _login(email, password):
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, f"login failed: {response.status_code} {response.text[:200]}"
    body = response.json()
    assert isinstance(body.get("access_token"), str) and body["access_token"]
    return body["access_token"]


@pytest.fixture(scope="module")
def operator_headers():
    return {"Authorization": f"Bearer {_login(*RMS_OPERATOR)}"}


def test_get_jobs_list_authenticated(operator_headers):
    response = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs",
        headers=operator_headers,
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text[:300]
    payload = response.json()
    assert payload.get("tenant_id") == "RMS"
    jobs = payload.get("jobs")
    assert isinstance(jobs, list) and jobs

    by_id = {job.get("job_id"): job for job in jobs}
    assert SMOKE_JOB_ID in by_id
    assert JOB_ID_RE.match(SMOKE_JOB_ID)
    assert by_id[SMOKE_JOB_ID].get("phase") == "train_corrective"


def test_get_smoke_job_metadata_integrity_and_dp_fields(operator_headers):
    response = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs/{SMOKE_JOB_ID}",
        headers=operator_headers,
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text[:300]
    job = response.json().get("job", {})

    assert job.get("job_id") == SMOKE_JOB_ID
    assert job.get("status") == "completed"
    receipt = job.get("receipt") or {}
    assert receipt.get("digest_verified") is True

    result = (receipt.get("result") or {})
    dp = result.get("dp_sgd") or {}
    checkpoint = result.get("checkpoint") or {}
    certificate = job.get("run_certificate") or {}

    assert dp.get("applied") is True
    assert dp.get("poisson_sampling") is True
    assert dp.get("accountant") == "rdp"
    assert checkpoint.get("optimizer_saved") is True
    assert checkpoint.get("rng_saved") is True
    assert dp.get("checkpoint_accountant_verified") is True

    # Metadata-only checks: no labels/audio/checkpoint payloads should be inline in API response.
    serialized = json.dumps(job)
    assert "segments.jsonl" not in serialized
    assert "files.jsonl" not in serialized
    assert "best_internal.pt" not in serialized
    assert "checkpoint.pt" in serialized  # checkpoint path reference only

    assert certificate.get("final_model") is False
