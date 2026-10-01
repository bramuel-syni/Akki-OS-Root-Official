"""Live production-route regression for training lab production and whitepaper handoff.
Only uses existing identities and existing measured job records.
"""
import os
import time
import uuid

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")

RMS_OPERATOR = {
    "email": os.environ.get('AKKI_ALIGNMENT_TEST_EMAIL', 'demo.operator@demo.rms.example.com'),
    "password": os.environ.get('AKKI_ALIGNMENT_TEST_PASSWORD', 'demo-operator-pw'),
}
DIGICOW_OPERATOR = {
    "email": "demo.operator@demo.digicow.example.com",
    "password": "demo-digicow-operator-pw",
}

ASSEMBLE_JOB = "m9j-9a46b862f339"
CALIBRATION_JOB = "m9j-c4bec2810778"
COMPARISON_JOB = "m9j-1e1b97ce8e1c"
TRAINING_JOB = "m9j-74af7cef0a85"


def _require_base_url():
    if not BASE_URL:
        pytest.skip("REACT_APP_BACKEND_URL is not set")


def _login(creds):
    _require_base_url()
    response = requests.post(f"{BASE_URL}/api/auth/login", json=creds, timeout=30)
    if response.status_code != 200:
        pytest.skip(f"Login failed for {creds['email']}: {response.status_code} {response.text[:200]}")
    token = response.json().get("access_token")
    assert token, f"No access_token returned for {creds['email']}"
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="module")
def rms_headers():
    return _login(RMS_OPERATOR)


@pytest.fixture(scope="module")
def digicow_headers():
    return _login(DIGICOW_OPERATOR)


@pytest.fixture(scope="module")
def cleanup_state(rms_headers):
    state = {"run_ids": []}
    yield state
    for run_id in state["run_ids"]:
        try:
            requests.delete(f"{BASE_URL}/api/training/lab/board/{run_id}", headers=rms_headers, timeout=20)
        except Exception:
            pass
    # Explicitly remove only this fixture's temporary records, including retained
    # plan/conversation artifacts. Never leave test objectives on the owner's board.
    from services.training_lab import store
    ids = state['run_ids']
    for name in ['training_board_runs', 'training_production_plans', 'training_lab_conversations']:
        store.db()[name].delete_many({'tenant_id': 'RMS', 'run_id': {'$in': ids}})


# Production routes: catalogue + tenant isolation
def test_catalogue_and_tenant_scope(rms_headers, digicow_headers):
    rms = requests.get(f"{BASE_URL}/api/training/lab/production/catalogue", headers=rms_headers, timeout=30)
    assert rms.status_code == 200, rms.text[:400]
    rms_data = rms.json()
    assert isinstance(rms_data.get("registers"), list)
    register_ids = {r.get("register_ref") for r in rms_data["registers"]}
    assert ASSEMBLE_JOB in register_ids

    digicow = requests.get(f"{BASE_URL}/api/training/lab/production/catalogue", headers=digicow_headers, timeout=30)
    assert digicow.status_code == 200, digicow.text[:400]
    assert digicow.json().get("registers") == []


def _new_shaping_run(headers):
    response = requests.post(f"{BASE_URL}/api/training/lab/board/new", json={}, headers=headers, timeout=30)
    assert response.status_code == 201, response.text[:400]
    run_id = response.json().get("run_id")
    assert run_id and run_id.startswith("shape-")
    return run_id


def _definition_from_catalogue_row(row):
    strata = sorted(list((row.get("strata") or {}).keys()))
    assert strata, "Expected catalogue row to include strata"
    acceptance = {s: {"accuracy": 0.8, "coverage": 0.8} for s in strata}
    return {
        "target_outcome": {
            "task": "Language identification",
            "domain": "Text",
            "population_register_ref": row["register_ref"],
            "stratum_refs": strata,
            "acceptance": acceptance,
            "gate_policy": "missed_stratum_gates_release",
            "test_set_ref": (row.get("test_set") or {}).get("held_ids_sha256"),
            "constraints": {
                "latency": "<= 1s",
                "compute_budget": "<= 4 GPU hours",
                "deployment_target": "Existing registered worker",
            },
        },
        "collection_schema": {
            "baseline_tier": ["SourceID", "UnitID", "LanguageID", "RightsRef", "Window"],
            "objective_tier": [],
            "provenance_refs": {},
        },
        "planned_epochs": 2,
        "gpu_hour_cap": 4,
        "legal_basis": "Authorized source reference",
    }


@pytest.fixture(scope="module")
def compiled_plan(rms_headers, cleanup_state):
    catalogue = requests.get(f"{BASE_URL}/api/training/lab/production/catalogue", headers=rms_headers, timeout=30)
    assert catalogue.status_code == 200, catalogue.text[:400]
    rows = catalogue.json().get("registers") or []
    row = next((r for r in rows if r.get("register_ref") == ASSEMBLE_JOB), rows[0] if rows else None)
    assert row, "No production catalogue row available"

    run_id = _new_shaping_run(rms_headers)
    cleanup_state["run_ids"].append(run_id)

    definition = _definition_from_catalogue_row(row)
    define = requests.post(
        f"{BASE_URL}/api/training/lab/production/runs/{run_id}/definition",
        json=definition,
        headers=rms_headers,
        timeout=40,
    )
    assert define.status_code == 200, define.text[:500]
    assert define.json().get("definition", {}).get("target_outcome", {}).get("population_register_ref") == row["register_ref"]

    compiled = requests.post(
        f"{BASE_URL}/api/training/lab/production/runs/{run_id}/compile",
        headers=rms_headers,
        timeout=40,
    )
    assert compiled.status_code == 200, compiled.text[:500]
    plan = compiled.json().get("plan")
    assert isinstance(plan, dict) and plan.get("plan_id")
    return plan


# Production routes: define/compile/read + order/unknown stage checks
def test_plan_read_and_stage_order_rules(rms_headers, compiled_plan):
    plan_id = compiled_plan["plan_id"]

    read = requests.get(f"{BASE_URL}/api/training/lab/production/plans/{plan_id}", headers=rms_headers, timeout=30)
    assert read.status_code == 200, read.text[:400]
    assert read.json()["plan"]["plan_id"] == plan_id

    comparison_before_calibration = requests.post(
        f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/evidence/comparison",
        json={"job_id": COMPARISON_JOB},
        headers=rms_headers,
        timeout=40,
    )
    assert comparison_before_calibration.status_code == 422
    assert "calibrated" in comparison_before_calibration.text.lower()

    unknown = requests.post(
        f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/evidence/not-a-stage",
        json={"job_id": CALIBRATION_JOB},
        headers=rms_headers,
        timeout=30,
    )
    assert unknown.status_code == 422


# Production routes: attach evidence + recipe revisions + concurrency + immutability + MOAC
def test_historical_comparison_cannot_cross_calibrated_bases(rms_headers, compiled_plan):
    plan_id = compiled_plan["plan_id"]

    cal = requests.post(
        f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/evidence/calibration",
        json={"job_id": CALIBRATION_JOB},
        headers=rms_headers,
        timeout=40,
    )
    assert cal.status_code == 200, cal.text[:500]
    plan = cal.json()["plan"]
    assert plan.get("stages", {}).get("calibration", {}).get("job_id") == CALIBRATION_JOB

    cmp = requests.post(
        f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/evidence/comparison",
        json={"job_id": COMPARISON_JOB},
        headers=rms_headers,
        timeout=40,
    )
    # The historical comparator used 1.7B; calibration selected 8B. Never
    # weaken the product's same-base rule to make historical evidence pass.
    assert cmp.status_code == 422, cmp.text[:500]
    assert 'calibrated' in cmp.text.lower()
    moac = requests.get(f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/moac", headers=rms_headers, timeout=30)
    assert moac.status_code == 422, moac.text[:400]
    assert 'measured training' in moac.text.lower()


# Production routes: dataset bind refusal path (no fake media fixtures)
def test_dataset_requires_real_available_files(rms_headers, compiled_plan):
    plan_id = compiled_plan["plan_id"]
    bogus_file = f"missing-file-{uuid.uuid4().hex[:10]}"
    res = requests.post(
        f"{BASE_URL}/api/training/lab/production/plans/{plan_id}/dataset",
        json={"file_ids": [bogus_file]},
        headers=rms_headers,
        timeout=30,
    )
    assert res.status_code == 404
    assert "no longer available" in res.text.lower() or "available" in res.text.lower()


# Whitepaper handoff: board action should return commission and build should be retrievable
def test_whitepaper_handoff_build_and_download(rms_headers):
    action = requests.post(
        f"{BASE_URL}/api/training/lab/board/{TRAINING_JOB}/actions",
        json={"action": "white_paper"},
        headers=rms_headers,
        timeout=90,
    )
    assert action.status_code == 200, action.text[:500]
    payload = action.json()
    messages = payload.get("messages") or []
    note = messages[-1] if messages else {}
    commission_id = note.get("commission_id")
    assert commission_id, f"No commission_id in white paper response: {payload}"

    commission = requests.get(f"{BASE_URL}/api/studio/commissions/{commission_id}", headers=rms_headers, timeout=40)
    assert commission.status_code == 200, commission.text[:500]
    record = commission.json().get("commission")
    assert record.get("source_ref") == TRAINING_JOB

    builds = record.get("builds") or []
    released = [b for b in builds if b.get("status") == "released"]
    if not released:
        built = requests.post(f"{BASE_URL}/api/studio/commissions/{commission_id}/build", headers=rms_headers, timeout=180)
        assert built.status_code == 201, built.text[:500]
        record = built.json().get("commission")
        released = [b for b in (record.get("builds") or []) if b.get("status") == "released"]

    assert released, f"No released build found for commission {commission_id}"
    build = released[-1]
    outputs = build.get("outputs") or []
    assert outputs, "Released build has no outputs"

    html_artifact = next((o for o in outputs if o.get("name", "").endswith(".html")), outputs[0])
    download = requests.get(
        f"{BASE_URL}/api/studio/commissions/{commission_id}/builds/{build['build_id']}/artifact/{html_artifact['name']}",
        headers=rms_headers,
        timeout=60,
    )
    assert download.status_code == 200, download.text[:300]
    assert len(download.content) == html_artifact.get("size")


def test_two_turn_objective_conversation_keeps_session_without_inventing_definition(rms_headers, cleanup_state):
    run_id = _new_shaping_run(rms_headers)
    cleanup_state['run_ids'].append(run_id)
    for text in ['I want language identification from authorised estate transcripts. What do you need first?',
                 'I have not chosen accuracy or coverage thresholds. Keep those unresolved and ask me the next question.']:
        response = requests.post(f'{BASE_URL}/api/training/lab/board/{run_id}/messages', headers=rms_headers, json={'text': text}, timeout=150)
        assert response.status_code == 200, response.text[:300]
        assert response.json()['training_started'] is False
        assert response.json()['messages'][-1].get('widget') != 'refusal', response.json()['messages'][-1]['text']
    board = requests.get(f'{BASE_URL}/api/training/lab/board', headers=rms_headers, timeout=60).json()
    run = next(r for r in board['runs'] if r['run_id'] == run_id)
    assert len([m for m in run['messages'] if m['role'] == 'user']) == 2
    assert run['ready'] is False
    assert not (run['evidence'].get('definition') or {}).get('target_outcome')
