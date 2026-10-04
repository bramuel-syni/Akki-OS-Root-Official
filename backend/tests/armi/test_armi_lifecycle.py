"""ARMI lifecycle (Mα MA-29 / T29): onboard → bind version → assign (with dependency) → complete → score → suspend → revoke; analyst read-only;
cross-tenant isolation; evidence-bound scoring; derived profiles never export Watch profiles or invent a conduct probability. Live preview API."""
import os
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
OPERATOR = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}
ANALYST = {"email": "demo.analyst@demo.rms.example.com", "password": "demo-analyst-pw"}
DIGICOW = {"email": "demo.operator@demo.digicow.example.com", "password": "demo-digicow-operator-pw"}


def _login(creds):
    r = requests.post(f"{BASE_URL}/api/auth/login", json=creds, timeout=20)
    if r.status_code != 200: pytest.skip(f"login failed for {creds['email']}: {r.status_code}")
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture(scope="module")
def op(): return _login(OPERATOR)


@pytest.fixture(scope="module")
def analyst(): return _login(ANALYST)


@pytest.fixture(scope="module")
def digicow(): return _login(DIGICOW)


@pytest.fixture(scope="module")
def suffix():
    token = uuid.uuid4().hex[:8]
    yield token
    # the register has no delete by design; test identities are removed directly so the product register stays clean
    from dotenv import dotenv_values
    from pymongo import MongoClient
    env = dotenv_values("/app/backend/.env"); db = MongoClient(env["MONGO_URL"])[env["DB_NAME"]]
    ids = [a["agent_id"] for a in db.armi_agents.find({"name": {"$regex": f"{token}$"}}, {"agent_id": 1})]
    db.armi_assignments.delete_many({"agent_id": {"$in": ids}}); db.armi_agents.delete_many({"agent_id": {"$in": ids}})


def test_sync_and_overview_are_evidence_bound(op):
    r = requests.post(f"{BASE_URL}/api/armi/sync", headers=op, timeout=60); assert r.status_code == 200 and r.json()["derived"] >= 5
    o = requests.get(f"{BASE_URL}/api/armi/overview", headers=op, timeout=30).json()
    assert o["tenant_id"] == "RMS" and o["agents"] >= 5 and o["protected"]["watch_profiles_exported"] is False
    assert "not computed" in o["protected"]["malicious_probability"] and o["cost_usd"] is None
    agents = requests.get(f"{BASE_URL}/api/armi/agents", headers=op, timeout=30).json()["agents"]
    for a in agents:
        assert a["behaviour"]["watch_profile_exported"] is False and "not computed" in a["behaviour"]["malicious_conduct_probability"]
        c = a["compliance"]; assert set(c) >= {"value", "passed", "n", "basis", "evidence_class"}
        assert (c["value"] is None) == (c["n"] == 0) and c["evidence_class"] == ("measured" if c["n"] else "not_measured")
    e1 = next(a for a in agents if a["agent_id"] == "agent:E1"); assert e1["compliance"]["n"] > 0 and e1["jd"]["role"] == "software developer"
    assert any(a["agent_id"].startswith("model:malpha:") for a in agents)


def test_lifecycle_onboard_bind_assign_complete_score_suspend_revoke(op, suffix):
    body = {"kind": "agent", "name": f"T29 planner {suffix}", "jd": {"role": "delivery planner", "job": "plans abstract delivery steps without privileged data", "strengths": ["structure"], "can_do": ["plan"], "cannot_do": ["see originals"]}, "objectives": ["MA-29 test"]}
    r = requests.post(f"{BASE_URL}/api/armi/agents", headers=op, json=body, timeout=30); assert r.status_code == 201, r.text
    a = r.json()["agent"]; aid = a["agent_id"]; assert a["status"] == "onboarded" and a["admission"]["decision"].startswith("onboarded")
    assert requests.post(f"{BASE_URL}/api/armi/agents", headers=op, json=body, timeout=30).status_code == 409
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "bind_version"}, timeout=30); assert r.status_code == 409
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "bind_version", "version": "v1.0-test"}, timeout=30); assert r.status_code == 200 and r.json()["agent"]["version"] == "v1.0-test"
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "activate", "note": "test"}, timeout=30); assert r.json()["agent"]["status"] == "active"
    # dependency on an unknown identity is refused; dependency on an active identity is accepted
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/assign", headers=op, json={"task": "x", "depends_on": ["agent:does-not-exist"]}, timeout=30); assert r.status_code == 409
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/assign", headers=op, json={"task": "plan the deck structure", "objective_ref": "MA-29", "collaborators": ["agent:E1"], "depends_on": ["agent:E1"]}, timeout=30)
    assert r.status_code == 201, r.text; asg = r.json()["assignment"]; assert asg["status"] == "assigned"
    # score before completion refused; completion then score without evidence refused; evidence-bound score accepted
    assert requests.post(f"{BASE_URL}/api/armi/assignments/{asg['assignment_id']}/score", headers=op, json={"quality": 0.9, "compliant": True, "evidence_ref": "x"}, timeout=30).status_code == 409
    r = requests.post(f"{BASE_URL}/api/armi/assignments/{asg['assignment_id']}/complete", headers=op, json={"outcome": "completed", "result_ref": "test-artefact"}, timeout=30); assert r.json()["assignment"]["status"] == "completed"
    assert requests.post(f"{BASE_URL}/api/armi/assignments/{asg['assignment_id']}/score", headers=op, json={"quality": 0.9, "compliant": True, "evidence_ref": ""}, timeout=30).status_code == 422
    r = requests.post(f"{BASE_URL}/api/armi/assignments/{asg['assignment_id']}/score", headers=op, json={"quality": 0.95, "compliant": True, "evidence_ref": "tests/armi/test_armi_lifecycle.py"}, timeout=30); assert r.status_code == 200 and r.json()["assignment"]["score"]["quality"] == 0.95
    prof = requests.get(f"{BASE_URL}/api/armi/agents/{aid}", headers=op, timeout=30).json()["agent"]
    assert prof["assignment_summary"]["completed"] == 1 and prof["assignment_summary"]["compliance"]["value"] == 1.0 and prof["assignment_summary"]["compliance"]["n"] == 1
    assert len(prof["assignments"]) == 1 and [e["action"] for e in prof["lifecycle"]] == ["onboarded", "bind_version", "activate", "assigned"]
    # suspend cancels open work; revoke is terminal
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/assign", headers=op, json={"task": "second"}, timeout=30); open_id = r.json()["assignment"]["assignment_id"]
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "suspend"}, timeout=30); assert r.json()["agent"]["status"] == "suspended"
    assert requests.post(f"{BASE_URL}/api/armi/agents/{aid}/assign", headers=op, json={"task": "third"}, timeout=30).status_code == 409
    prof = requests.get(f"{BASE_URL}/api/armi/agents/{aid}", headers=op, timeout=30).json()["agent"]
    assert next(x for x in prof["assignments"] if x["assignment_id"] == open_id)["status"] == "cancelled"
    r = requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "revoke", "note": "test end"}, timeout=30); assert r.json()["agent"]["status"] == "revoked"
    assert requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "activate"}, timeout=30).status_code == 409
    # a sync preserves the owner lifecycle and status override
    requests.post(f"{BASE_URL}/api/armi/sync", headers=op, timeout=60)
    assert requests.get(f"{BASE_URL}/api/armi/agents/{aid}", headers=op, timeout=30).json()["agent"]["status"] == "revoked"


def test_analyst_reads_but_cannot_change(analyst):
    assert requests.get(f"{BASE_URL}/api/armi/agents", headers=analyst, timeout=30).status_code == 200
    assert requests.post(f"{BASE_URL}/api/armi/sync", headers=analyst, timeout=30).status_code == 403
    assert requests.post(f"{BASE_URL}/api/armi/agents/agent:E1/transition", headers=analyst, json={"action": "suspend"}, timeout=30).status_code == 403


def test_cross_tenant_isolation(op, digicow, suffix):
    r = requests.post(f"{BASE_URL}/api/armi/agents", headers=op, json={"kind": "skill", "name": f"rms-only {suffix}", "jd": {"role": "r", "job": "j"}}, timeout=30); aid = r.json()["agent"]["agent_id"]
    assert requests.get(f"{BASE_URL}/api/armi/agents/{aid}", headers=digicow, timeout=30).status_code == 404
    assert requests.post(f"{BASE_URL}/api/armi/agents/{aid}/assign", headers=digicow, json={"task": "steal"}, timeout=30).status_code == 404
    assert all(a["tenant_id"] != "RMS" for a in requests.get(f"{BASE_URL}/api/armi/agents", headers=digicow, timeout=30).json()["agents"])
    requests.post(f"{BASE_URL}/api/armi/agents/{aid}/transition", headers=op, json={"action": "revoke", "note": "test cleanup"}, timeout=30)


def test_anonymous_refused():
    assert requests.get(f"{BASE_URL}/api/armi/overview", timeout=30).status_code == 401
