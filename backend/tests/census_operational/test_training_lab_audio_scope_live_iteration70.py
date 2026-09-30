"""Live + offline regression for training-lab audio-first scope and guarded queue semantics."""

# Module covers: training-lab API auth/contracts, cron idempotency, statistics/music/value contracts, queue idempotency, and mocked specialist-review contract checks.
import json
import os
import sys
import time
import types
import uuid
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values
import re


VENDORED_BACKEND = Path("/app/backend/vendored/extraction_akki/backend")
if str(VENDORED_BACKEND) not in sys.path:
    sys.path.insert(0, str(VENDORED_BACKEND))

from services.training_lab import reviewers, store  # noqa: E402


BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/")
TIMEOUT = 35

def _credentials(label):
    text = Path('/app/memory/test_credentials.md').read_text()
    match = re.search(r'\|\s*(' + re.escape(label) + r')\s*\|\s*([^|]+?)\s*\|', text)
    assert match, 'Existing test credential missing'
    return match.group(1), match.group(2).strip()


RMS_OPERATOR_EMAIL, RMS_OPERATOR_PASSWORD = _credentials('demo.operator@demo.rms.example.com')
RMS_ANALYST_EMAIL, RMS_ANALYST_PASSWORD = _credentials('demo.analyst@demo.rms.example.com')
DIGICOW_OPERATOR_EMAIL, DIGICOW_OPERATOR_PASSWORD = _credentials('demo.operator@demo.digicow.example.com')

OWNER_IDEMPOTENCY_KEY = "owner-audio-music-assessment-20260930"
OWNER_BODY = {
    "title": "Audio cognition and music readiness",
    "host": "akki-vm",
    "inspect_existing_data": True,
    "model_reviews": True,
}


def _read_backend_env_key(name: str):
    value = os.environ.get(name)
    if value:
        return value
    env_path = Path("/app/backend/.env")
    if not env_path.exists():
        return None
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == name:
            return v.strip()
    return None


def _ensure_backend_env(keys: list[str]):
    values = dotenv_values('/app/backend/.env')
    for key in keys:
        os.environ[key] = values[key]


def _token(email: str, password: str) -> str:
    r = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"Login failed for {email}: {r.status_code} {r.text[:220]}"
    body = r.json()
    assert "access_token" in body and isinstance(body["access_token"], str)
    assert "identity" in body and body["identity"]["email"] == email
    return body["access_token"]


@pytest.fixture(scope="session")
def auth_headers():
    rms_operator = _token(RMS_OPERATOR_EMAIL, RMS_OPERATOR_PASSWORD)
    rms_analyst = _token(RMS_ANALYST_EMAIL, RMS_ANALYST_PASSWORD)
    digicow_operator = _token(DIGICOW_OPERATOR_EMAIL, DIGICOW_OPERATOR_PASSWORD)
    return {
        "rms_operator": {"Authorization": f"Bearer {rms_operator}"},
        "rms_analyst": {"Authorization": f"Bearer {rms_analyst}"},
        "digicow_operator": {"Authorization": f"Bearer {digicow_operator}"},
    }


def test_skills_catalogue_and_auth_contract(auth_headers):
    anon = requests.get(f"{BASE_URL}/api/training/lab/skills", timeout=TIMEOUT)
    assert anon.status_code == 401

    r = requests.get(
        f"{BASE_URL}/api/training/lab/skills",
        headers=auth_headers["rms_operator"],
        timeout=TIMEOUT,
    )
    assert r.status_code == 200
    body = r.json()
    skills = body["skills"]
    advisory = [s for s in skills if s["kind"] == "model_advisory"]
    deterministic = [s for s in skills if s["kind"] == "deterministic"]
    assert len(advisory) == 5
    assert len(deterministic) == 4
    assert body["training_authorized"] is False
    assert body["music_detector_admitted"] is False


def test_analyst_cannot_mutate_training_lab(auth_headers):
    r1 = requests.post(
        f"{BASE_URL}/api/training/lab/skills/statistics/invoke",
        headers=auth_headers["rms_analyst"],
        json={"operation": "wilson", "successes": 3, "n": 8},
        timeout=TIMEOUT,
    )
    assert r1.status_code == 403

    r2 = requests.post(
        f"{BASE_URL}/api/training/lab/runs",
        headers={**auth_headers["rms_analyst"], "idempotency-key": OWNER_IDEMPOTENCY_KEY},
        json=OWNER_BODY,
        timeout=TIMEOUT,
    )
    assert r2.status_code == 403

    r3 = requests.put(
        f"{BASE_URL}/api/training/lab/watch",
        headers=auth_headers["rms_analyst"],
        json={"enabled": True, "max_checkpoints_per_job": 4},
        timeout=TIMEOUT,
    )
    assert r3.status_code == 403


def test_digicow_cannot_access_rms_run_or_submit(auth_headers):
    run_resp = requests.get(
        f"{BASE_URL}/api/training/lab/runs/lab-34569b6b04eb44fa",
        headers=auth_headers["digicow_operator"],
        timeout=TIMEOUT,
    )
    assert run_resp.status_code in (403, 404)

    submit_resp = requests.post(
        f"{BASE_URL}/api/training/lab/runs",
        headers={**auth_headers["digicow_operator"], "idempotency-key": OWNER_IDEMPOTENCY_KEY},
        json=OWNER_BODY,
        timeout=TIMEOUT,
    )
    assert submit_resp.status_code == 403


def test_statistics_wilson_bootstrap_and_invalid_contracts(auth_headers):
    h = auth_headers["rms_operator"]

    w = requests.post(
        f"{BASE_URL}/api/training/lab/skills/statistics/invoke",
        headers=h,
        json={"operation": "wilson", "successes": 0, "n": 1, "confidence": 0.95},
        timeout=TIMEOUT,
    )
    assert w.status_code == 200
    wb = w.json()["result"]
    assert wb["method"] == "wilson_score" and wb["n"] == 1 and 0 <= wb["low"] <= wb["high"] <= 1

    payload = {
        "operation": "bootstrap",
        "values": [0.2, 0.6, 0.8, 0.4],
        "seed": 77,
        "draws": 400,
        "confidence": 0.9,
    }
    b1 = requests.post(f"{BASE_URL}/api/training/lab/skills/statistics/invoke", headers=h, json=payload, timeout=TIMEOUT)
    b2 = requests.post(f"{BASE_URL}/api/training/lab/skills/statistics/invoke", headers=h, json=payload, timeout=TIMEOUT)
    assert b1.status_code == 200 and b2.status_code == 200
    assert b1.json()["result"] == b2.json()["result"]

    grouped = {
        "operation": "bootstrap",
        "values": [1.0, 2.0, 3.0, 4.0],
        "groups": [1, 1, 2, 2],
        "seed": 41,
        "draws": 300,
    }
    gr = requests.post(f"{BASE_URL}/api/training/lab/skills/statistics/invoke", headers=h, json=grouped, timeout=TIMEOUT)
    assert gr.status_code == 200
    assert gr.json()["result"]["method"] == "group_percentile_bootstrap"

    paired = {
        "operation": "bootstrap",
        "values": [0.5, 0.7, 0.9],
        "paired": [0.4, 0.6, 0.8],
        "seed": 5,
        "draws": 300,
    }
    pr = requests.post(f"{BASE_URL}/api/training/lab/skills/statistics/invoke", headers=h, json=paired, timeout=TIMEOUT)
    assert pr.status_code == 200
    assert pr.json()["result"]["paired"] is True

    invalids = [
        {"operation": "bootstrap", "values": [1.0, "nan"], "seed": 1, "draws": 200},
        {"operation": "bootstrap", "values": [], "seed": 1, "draws": 200},
        {"operation": "bootstrap", "values": [1.0, 2.0], "paired": [1.0], "seed": 1, "draws": 200},
    ]
    for bad in invalids:
        resp = requests.post(f"{BASE_URL}/api/training/lab/skills/statistics/invoke", headers=h, json=bad, timeout=TIMEOUT)
        assert resp.status_code == 422


def test_statistics_power_law_and_monitor_contracts(auth_headers):
    h = auth_headers["rms_operator"]

    power_payload = {
        "operation": "power_law",
        "points": [[100, 0.5], [200, 0.42], [400, 0.35]],
        "exponent_bounds": [0.1, 1.2],
        "irreducible_bounds": [0.05, 0.2],
        "floor": 0.9,
        "cap": 150,
    }
    p = requests.post(
        f"{BASE_URL}/api/training/lab/skills/statistics/invoke",
        headers=h,
        json=power_payload,
        timeout=TIMEOUT,
    )
    assert p.status_code == 200
    result = p.json()["result"]
    assert result["evidence_class"] == "prior_sensitivity_not_confidence_interval"
    assert "scenarios" in result and len(result["scenarios"]) == 9
    assert any((s["examples"] or 0) > power_payload["cap"] for s in result["scenarios"] if s["examples"] is not None)

    missing_cal = requests.post(
        f"{BASE_URL}/api/training/lab/skills/statistics/invoke",
        headers=h,
        json={"operation": "monitor", "values": [0.2, 0.3], "false_alert_rate": 0.1},
        timeout=TIMEOUT,
    )
    assert missing_cal.status_code == 422

    monitor = requests.post(
        f"{BASE_URL}/api/training/lab/skills/statistics/invoke",
        headers=h,
        json={
            "operation": "monitor",
            "values": [0.1, 0.2, 0.3, 0.4],
            "false_alert_rate": 0.1,
            "calibration_ref": "calib-20260930",
        },
        timeout=TIMEOUT,
    )
    assert monitor.status_code == 200
    mon = monitor.json()["result"]
    assert mon["validated_false_alert_rate"] is None


def test_music_decision_labels_and_untrained_head_disclosure(auth_headers):
    h = auth_headers["rms_operator"]
    base = {"speech_threshold": 0.6, "music_threshold": 0.6, "calibration_ref": "calib-ref"}
    cases = [
        ({"speech": 0.8, "music": 0.2}, "speech"),
        ({"speech": 0.2, "music": 0.8}, "music"),
        ({"speech": 0.9, "music": 0.9}, "mixed"),
        ({"speech": 0.1, "music": 0.1}, "unknown"),
    ]
    for payload, expected in cases:
        resp = requests.post(
            f"{BASE_URL}/api/training/lab/skills/music/invoke",
            headers=h,
            json={**base, **payload},
            timeout=TIMEOUT,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["music_detector_admitted"] is False
        assert body["result"]["label"] == expected
        assert "not_verified_inference" in body["result"]["evidence_class"]


def test_value_and_postmortem_contracts(auth_headers):
    h = auth_headers["rms_operator"]

    value_ok = requests.post(
        f"{BASE_URL}/api/training/lab/skills/value/invoke",
        headers=h,
        json={
            "monthly_benefit": 1200,
            "monthly_cost": 450,
            "setup_cost": 8000,
            "adoption_probability": 0.65,
            "delay_months": 2,
            "horizon_months": 24,
            "annual_discount_rate": 0.12,
            "next_best_npv": 500,
        },
        timeout=TIMEOUT,
    )
    assert value_ok.status_code == 200
    v = value_ok.json()["result"]
    assert "risk_adjusted_npv" in v and "incremental_npv" in v

    value_bad = requests.post(
        f"{BASE_URL}/api/training/lab/skills/value/invoke",
        headers=h,
        json={
            "monthly_benefit": 100,
            "monthly_cost": 120,
            "setup_cost": 100,
            "adoption_probability": 0.5,
            "delay_months": 10,
            "horizon_months": 3,
            "annual_discount_rate": 0.1,
            "next_best_npv": 0,
        },
        timeout=TIMEOUT,
    )
    assert value_bad.status_code == 422

    pm_ok = requests.post(
        f"{BASE_URL}/api/training/lab/skills/postmortem/invoke",
        headers=h,
        json={
            "predictions": [
                {
                    "role": "researcher",
                    "low": 0.5,
                    "high": 0.8,
                    "actual": 0.7,
                    "prediction_ref": "pred-1",
                    "actual_ref": "act-1",
                }
            ]
        },
        timeout=TIMEOUT,
    )
    assert pm_ok.status_code == 200
    assert "coverage" in pm_ok.json()["result"]

    pm_bad = requests.post(
        f"{BASE_URL}/api/training/lab/skills/postmortem/invoke",
        headers=h,
        json={
            "predictions": [
                {
                    "role": "researcher",
                    "low": 0.8,
                    "high": 0.7,
                    "actual": 0.75,
                    "prediction_ref": "same-ref",
                    "actual_ref": "same-ref",
                }
            ]
        },
        timeout=TIMEOUT,
    )
    assert pm_bad.status_code == 422


def test_assessment_idempotency_and_conflict_contract(auth_headers):
    h = auth_headers["rms_operator"]

    def submit_with_shape_retry(payload):
        resp = requests.post(
            f"{BASE_URL}/api/training/lab/runs",
            headers={**h, "idempotency-key": OWNER_IDEMPOTENCY_KEY},
            json=payload,
            timeout=TIMEOUT,
        )
        return resp

    first = submit_with_shape_retry(OWNER_BODY)
    assert first.status_code == 202
    first_body = first.json()
    assert "run" in first_body and isinstance(first_body["run"]["run_id"], str)

    time.sleep(0.2)
    second = submit_with_shape_retry(OWNER_BODY)
    assert second.status_code == 202
    second_body = second.json()
    assert second_body["run"]["run_id"] == first_body["run"]["run_id"]
    assert second_body["created"] is False

    conflict = submit_with_shape_retry({**OWNER_BODY, "host": "akki-vm-ii"})
    assert conflict.status_code == 409


def test_cron_auth_body_and_idempotent_acknowledgement():
    secret = _read_backend_env_key("WEBHOOK_CRON_SECRET")
    assert secret, "WEBHOOK_CRON_SECRET missing"
    endpoint = f"{BASE_URL}/api/training/lab/cron"

    wrong = requests.post(
        endpoint,
        headers={"Authorization": "Bearer wrong-secret"},
        json={"event": "schedule.triggered", "run_id": "run-1", "data": None},
        timeout=TIMEOUT,
    )
    assert wrong.status_code == 401

    malformed = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {secret}"},
        json={"event": "not-triggered", "run_id": "", "data": {}},
        timeout=TIMEOUT,
    )
    assert malformed.status_code == 400

    hook_id = f"pytest-lab-cron-{uuid.uuid4().hex[:12]}"
    payload = {"event": "schedule.triggered", "run_id": f"run-{uuid.uuid4().hex[:8]}", "data": None}
    ok1 = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {secret}", "x-webhook-id": hook_id},
        json=payload,
        timeout=TIMEOUT,
    )
    assert ok1.status_code == 200
    assert ok1.json() == {"accepted": True, "duplicate": False}

    ok2 = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {secret}", "x-webhook-id": hook_id},
        json=payload,
        timeout=TIMEOUT,
    )
    assert ok2.status_code == 200
    assert ok2.json() == {"accepted": True, "duplicate": True}


def test_crons_yml_shape_contract():
    import yaml

    content = yaml.safe_load(Path("/app/.emergent/crons.yml").read_text())
    assert isinstance(content, dict) and isinstance(content.get("crons"), list)
    target = [c for c in content["crons"] if c.get("name") == "training-lab-review"]
    assert len(target) == 1
    row = target[0]
    assert row["cron"] == "*/15 * * * *"
    assert row["endpoint"] == "{{BASE_URL}}/api/training/lab/cron"
    assert row["method"] == "POST"
    assert row["enabled"] is True


def test_existing_followup_is_idempotent_and_cannot_recurse(auth_headers):
    h=auth_headers['rms_operator']
    r=requests.post(f'{BASE_URL}/api/training/lab/runs/lab-34569b6b04eb44fa/review',headers={**h,'idempotency-key':'owner-advisory-quality-followup-20260930'},timeout=TIMEOUT)
    assert r.status_code==202 and r.json()['created'] is False
    child=r.json()['run']['run_id']
    nested=requests.post(f'{BASE_URL}/api/training/lab/runs/{child}/review',headers={**h,'idempotency-key':'test-do-not-recursively-dispatch'},timeout=TIMEOUT)
    assert nested.status_code==409


def test_checkpoint_projection_and_numeric_advice_quality():
    from services.training_lab.evidence import checkpoint_evidence
    from services.training_lab.contracts import Advisory
    data=checkpoint_evidence({'remote_state':{'lab_checkpoint':{'epoch':2,'step':20,'epsilon':1.3,'dev':{'per_language':{'swa':{'accuracy':0.7,'abstention_rate':0.2,'windows':100,'raw_text':'DO NOT EXPORT'}}},'heldout':{'secret':'DO NOT EXPORT'}}}})
    assert data['checkpoint']['evaluation_split']=='development_only'
    assert 'DO NOT EXPORT' not in json.dumps(data)
    result=Advisory(role='ml_ops_engineer',advisory_only=True,uncertainties=[],findings=[{'severity':'review','evidence_refs':['development_checkpoint'],'observation':'Used 2700 GPU hours','recommendation':'Review the evidence','evidence_class':'measured'}])
    assert reviewers.quality_findings(result)[0]['code']=='numeric_claim_requires_evidence_table'


def test_store_queue_idempotency_tenant_isolation_and_stale_lease():
    _ensure_backend_env(["MONGO_URL", "DB_NAME"])
    mongo_url = os.environ.get("MONGO_URL", "")
    if not (mongo_url.startswith("mongodb://") or mongo_url.startswith("mongodb+srv://")):
        pytest.skip("MONGO_URL is not a Mongo URI in this shell; skipping direct store lease test")
    tenant_a = "TEST_TL_IT70_A"
    tenant_b = "TEST_TL_IT70_B"
    key = f"pytest-it70-{uuid.uuid4().hex[:8]}"
    body = {"title": "it70", "host": "akki-vm", "inspect_existing_data": True, "model_reviews": False}

    created = []
    db = store.db()
    try:
        row1, new1 = store.enqueue(tenant_a, "principal-a", key, body)
        created.append(row1["run_id"])
        assert new1 is True

        row2, new2 = store.enqueue(tenant_a, "principal-a", key, body)
        assert new2 is False
        assert row2["run_id"] == row1["run_id"]

        with pytest.raises(ValueError):
            store.enqueue(tenant_a, "principal-a", key, {**body, "host": "akki-vm-ii"})

        row_other_tenant, new_other_tenant = store.enqueue(tenant_b, "principal-b", key, body)
        created.append(row_other_tenant["run_id"])
        assert new_other_tenant is True

        stale = {
            "run_id": f"lab-{uuid.uuid4().hex[:16]}",
            "tenant_id": tenant_a,
            "actor": "principal-a",
            "idempotency_key": f"stale-{uuid.uuid4().hex[:8]}",
            "request_hash": "x",
            "request": body,
            "kind": "assessment",
            "title": "stale",
            "status": "dispatching",
            "created_at": store.now(),
            "updated_at": store.now(),
            "attempts": 0,
            "lease_until": "1970-01-01T00:00:00+00:00",
            "training_authorized": False,
            "training_started": False,
            "model_admission": "not_requested",
        }
        queued = {
            "run_id": f"lab-{uuid.uuid4().hex[:16]}",
            "tenant_id": tenant_a,
            "actor": "principal-a",
            "idempotency_key": f"queued-{uuid.uuid4().hex[:8]}",
            "request_hash": "y",
            "request": body,
            "kind": "assessment",
            "title": "queued",
            "status": "queued",
            "created_at": store.now(),
            "updated_at": store.now(),
            "attempts": 0,
            "training_authorized": False,
            "training_started": False,
            "model_admission": "not_requested",
        }
        db.training_lab_runs.insert_many([stale, queued])
        created.extend([stale["run_id"], queued["run_id"]])

        claimed = store.claim(tenant=tenant_a)
        assert claimed is not None
        stale_db = db.training_lab_runs.find_one({"run_id": stale["run_id"]}, {"_id": 0})
        assert stale_db["status"] == "held"
        assert "hold_reason" in stale_db
    finally:
        db.training_lab_runs.delete_many({"run_id": {"$in": created}})


@pytest.mark.anyio
async def test_specialist_reviews_contract_with_mocked_provider(monkeypatch):
    captured = []
    for key,value in {'TRAINING_LAB_CONNECTION':'emergent','TRAINING_LAB_MODEL':'gpt-5.4'}.items():
        monkeypatch.setenv(key,value)

    class FakeResponse:
        def __init__(self, role):
            self.text = json.dumps(
                {
                    "role": role,
                    "findings": [
                        {
                            "severity": "review",
                            "evidence_refs": ["historical_audio_1"],
                            "observation": "Observed trend from approved aggregates.",
                            "recommendation": "Hold retraining until labelled music corpus and floor contract are approved.",
                            "evidence_class": "measured",
                        }
                    ],
                    "uncertainties": ["No independent blind-set update yet"],
                    "advisory_only": True,
                }
            )
            self.receipt_id = "r-test"
            self.model_id = "gpt-5.4"
            self.tokens_in = 10
            self.tokens_out = 15
            self.latency_ms = 12

    async def fake_invoke(**kwargs):
        payload = json.loads(kwargs["prompt"])
        captured.append(payload)
        if payload["role"] == "entrepreneur":
            raise RuntimeError("provider down")
        return FakeResponse(payload["role"])

    monkeypatch.setitem(sys.modules, "services.chokepoint.llm", types.SimpleNamespace(invoke=fake_invoke))

    evidence = {
        "historical_audio": [{"ref": "historical_audio_1", "per_language": {"swa": {"accuracy": 0.7}}}],
        "authority": {"ref": "owner_scope", "training_authorized": False},
    }
    out = await reviewers.reviews(evidence, tenant="RMS", actor="principal-x", run_id="lab-test")
    assert len(out) == 5
    assert len(captured) == 5
    assert sum(r['status']=='complete' for r in out)==4
    assert any(r["status"] == "unavailable" and r["role"] == "entrepreneur" for r in out)
    assert all(r["status"] in {"complete", "unavailable"} for r in out)
    for r in [x for x in out if x["status"] == "unavailable"]:
        assert "Advisory review unavailable" in r["message"]

    if captured:
        for payload in captured:
            assert "allowed_evidence_refs" in payload
            assert set(payload["allowed_evidence_refs"]) == {"historical_audio_1", "owner_scope"}
            assert "aggregate_evidence" in payload
            assert "client_text" not in payload
