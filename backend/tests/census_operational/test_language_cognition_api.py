"""M2 language-cognition API tests against live backend via REACT_APP_BACKEND_URL."""
import os
import re
import json
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
assert BASE_URL, "REACT_APP_BACKEND_URL required"

OPERATOR = ("demo.operator@demo.rms.example.com", "demo-operator-pw")
ANALYST = ("demo.analyst@demo.rms.example.com", "demo-analyst-pw")
TIMEOUT = 60

JOB_ID_RE = re.compile(r"^lcj-[a-f0-9]{12}$")
EXPECTED_JOBS = {
    "lcj-f96c86a16312": "train_baseline",
    "lcj-4e9283997834": "gate_eval",
    "lcj-e16f26a43d22": "speaker_linkage",
    "lcj-1851c62aee3b": "corpus_census",
}
SECRET_KEYS = ("access_key", "secret", "password")


def _login(email, pw):
    r = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": pw},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text[:200]}"
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def op_headers():
    return {"Authorization": f"Bearer {_login(*OPERATOR)}"}


@pytest.fixture(scope="module")
def an_headers():
    return {"Authorization": f"Bearer {_login(*ANALYST)}"}


def _contains_secret(obj):
    """Recursively check that no dict key looks like secret material."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and any(s in k.lower() for s in SECRET_KEYS):
                return f"secret-like key: {k}"
            found = _contains_secret(v)
            if found:
                return found
    elif isinstance(obj, list):
        for it in obj:
            found = _contains_secret(it)
            if found:
                return found
    return None


# ------ List ------
def test_list_jobs_as_operator(op_headers):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs",
        headers=op_headers, timeout=TIMEOUT,
    )
    assert r.status_code == 200, r.text[:300]
    body = r.json()
    assert body.get("tenant_id") == "RMS", body
    jobs = body.get("jobs")
    assert isinstance(jobs, list) and jobs
    ids = {j["job_id"] for j in jobs}
    for want in EXPECTED_JOBS:
        assert want in ids, f"missing {want} in {ids}"
    for j in jobs:
        assert JOB_ID_RE.match(j["job_id"]), j["job_id"]
        assert "phase" in j and "status" in j and "submitted_at" in j
    leak = _contains_secret(body)
    assert leak is None, f"secret leak in list: {leak}"


# ------ Completed jobs ------
def test_gate_eval_receipt(op_headers):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs/lcj-4e9283997834",
        headers=op_headers, timeout=TIMEOUT,
    )
    assert r.status_code == 200, r.text[:300]
    job = r.json()["job"]
    assert job["status"] == "completed"
    assert job["receipt"]["digest_verified"] is True
    per = job["receipt"]["result"]["per_language"]
    assert per["swa"]["whisper"]["agreement_rate"] == 1.0
    assert per["kik"]["whisper"]["agreement_rate"] == 0.0
    assert job["track4_run_receipt"]["status"] == "completed"
    stages = {row["stage"] for row in job["ledger_rows"]}
    assert {"admit", "gate", "converge"}.issubset(stages), stages


def test_speaker_linkage_receipt(op_headers):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs/lcj-e16f26a43d22",
        headers=op_headers, timeout=TIMEOUT,
    )
    assert r.status_code == 200, r.text[:300]
    job = r.json()["job"]
    result = job["receipt"]["result"]
    assert result["per_language"]["kik"]["presenters"] == 203
    custody = json.dumps(result.get("custody", ""))
    assert "embedding" in custody.lower() and "destroy" in custody.lower(), custody
    body_s = json.dumps(r.json())
    assert "speaker_embedding" not in body_s
    assert "voiceprint" not in body_s


def test_corpus_census_receipt(op_headers):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs/lcj-1851c62aee3b",
        headers=op_headers, timeout=TIMEOUT,
    )
    assert r.status_code == 200, r.text[:300]
    result = r.json()["job"]["receipt"]["result"]
    assert result["measured_on_host"]["kik"]["audio_hours"] == 82.1
    assert result["measured_on_host"]["kik"]["codecs"] == {"mp3": 584}
    origins = result["archives"]["session_origins"]
    assert set(origins.keys()) >= {"folder", "folder+archive", "archive"}


# ------ Full run (completed 2026-09-29T07:07:40Z) ------
def test_train_baseline_full_run_certificate(op_headers):
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs/lcj-f96c86a16312",
        headers=op_headers, timeout=TIMEOUT,
    )
    assert r.status_code == 200, r.text[:300]
    job = r.json()["job"]
    assert job["status"] == "completed" and job["receipt"]["digest_verified"] is True
    result = job["receipt"]["result"]
    assert result["split"]["speaker_linkage_used"] is True and result["artefact"]["final_model"] is False
    assert result["held_out"]["overall_accuracy_on_judged"] == 0.9402 and result["held_out"]["per_language"]["kik"]["accuracy"] == 0.9761
    assert result["held_out"]["per_language"]["lwg"]["accuracy"] == 0.5916          # reported, not hidden
    assert result["archive_test"]["overall_accuracy_on_judged"] == 0.9543
    assert result["artefact"]["moac"]["no_speaker_id_probe_passed"] is False        # measured MUST-DO §4 failure
    cert = job["run_certificate"]
    assert cert["final_model"] is False and cert["sealed_contract_check"]["span_rule_matches_default"] is True
    assert cert["sealed_contract_check"]["languages_meeting_presenter_minimum"] == ["guz", "kam", "kik", "kln", "luo", "lwg", "swa"]
    assert job["track4_run_receipt"]["status"] == "completed"


# ------ 404 ------
def test_missing_job_ids(op_headers):
    for jid in ("lcj-000000000000", "not-a-job-id"):
        r = requests.get(
            f"{BASE_URL}/api/portal/census/language-cognition/jobs/{jid}",
            headers=op_headers, timeout=TIMEOUT,
        )
        assert r.status_code == 404, f"{jid} → {r.status_code}"


# ------ Auth/authz on submit ------
def test_submit_unknown_phase_operator_422(op_headers):
    r = requests.post(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs",
        headers=op_headers, json={"phase": "nope"}, timeout=TIMEOUT,
    )
    assert r.status_code == 422, f"got {r.status_code}: {r.text[:200]}"


def test_submit_unknown_phase_analyst_403(an_headers):
    r = requests.post(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs",
        headers=an_headers, json={"phase": "nope"}, timeout=TIMEOUT,
    )
    assert r.status_code == 403, f"got {r.status_code}: {r.text[:200]}"


def test_anonymous_list_401():
    r = requests.get(
        f"{BASE_URL}/api/portal/census/language-cognition/jobs",
        timeout=TIMEOUT,
    )
    assert r.status_code in (401, 403), r.status_code
