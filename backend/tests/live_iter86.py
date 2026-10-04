"""Iteration 86 — MA-08 measured routing deep live checks (safe: no new trial POST, adoption reverted)."""
import os
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
OP = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}
AN = {"email": "demo.analyst@demo.rms.example.com", "password": "demo-analyst-pw"}


def _login(c):
    r = requests.post(f"{BASE_URL}/api/auth/login", json=c, timeout=20)
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_assignments_shape():
    op = _login(OP)
    body = requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=30).json()
    roles = {r["role"]: r for r in body["roles"]}
    assert set(roles) == {"assistant", "planner", "reviewer", "writer"}
    p = roles["planner"]
    assert p["task_set_defined"] is True
    assert len(p["candidates"]) == 5
    for other in ("assistant", "reviewer", "writer"):
        assert roles[other]["task_set_defined"] is False
    assert body["floors"] == {"pass_rate": 1.0, "json_rate": 1.0, "latency_ms_p50_max": 120000, "refusals_max": 0}
    assert body["task_set_version"] == "planner-caas-v2"
    assert body["planner_reviewer_distinct_families"] is True
    # when none adopted, basis should mention "configured" and "no measured trial adopted"
    for r in body["roles"]:
        if not r["decision"]:
            assert "configured" in r["basis"].lower() and "no measured trial adopted" in r["basis"].lower()


def test_trials_list_and_detail():
    op = _login(OP)
    lst = requests.get(f"{BASE_URL}/api/routing/trials?role=planner", headers=op, timeout=30).json()
    trials = lst["trials"]
    assert len(trials) >= 2
    ids = [t["trial_id"] for t in trials]
    print("trial_ids:", ids)
    # no per-task rows in list
    for t in trials:
        for c in t.get("candidates", []):
            assert "tasks" not in c
    # detail for rt-a5201bf3bb
    r = requests.get(f"{BASE_URL}/api/routing/trials/rt-a5201bf3bb", headers=op, timeout=30)
    assert r.status_code == 200, r.text
    t = r.json()["trial"]
    assert t["status"] == "measured"
    assert t["recommendation"]["model"] == "gpt-5.4-mini"
    assert set(t["recommendation"]["eligible"]) == {"gpt-6-astra", "gpt-5.4-mini", "claude-sonnet-5-5"}
    by_model = {c["model"]: c for c in t["candidates"]}
    assert by_model["claude-haiku-4-5-20251001"]["meets_floors"] is False
    assert by_model["gemini-3-flash-preview"]["meets_floors"] is False
    # findings mention invented figures somewhere on failing candidates
    all_findings = " ".join(f for c in t["candidates"] if not c["meets_floors"] for row in c.get("tasks", []) for f in row.get("findings", []))
    assert "invented" in all_findings.lower() or "figure" in all_findings.lower(), all_findings
    for c in t["candidates"]:
        assert len(c["tasks"]) == 3
        for row in c["tasks"]:
            assert set(row.keys()) >= {"task_id", "product", "status", "json_valid", "accepted", "findings", "tokens_in", "tokens_out", "latency_ms", "receipt_id"}
    # shield mentions SYNTHETIC
    shield_blob = str(t.get("shield", ""))
    assert "SYNTHETIC" in shield_blob or "synthetic" in shield_blob.lower()


def test_auth_refusals():
    op = _login(OP); an = _login(AN)
    assert requests.get(f"{BASE_URL}/api/routing/trials", headers=an, timeout=20).status_code == 200
    assert requests.post(f"{BASE_URL}/api/routing/trials", headers=an, json={"role": "planner"}, timeout=20).status_code == 403
    assert requests.post(f"{BASE_URL}/api/routing/trials", json={"role": "planner"}, timeout=20).status_code == 401
    assert requests.post(f"{BASE_URL}/api/routing/trials", headers=op, json={"role": "writer"}, timeout=20).status_code == 409
    assert requests.get(f"{BASE_URL}/api/routing/trials/rt-doesnotexist", headers=op, timeout=20).status_code == 404
    # haiku failed floors → 409
    r = requests.post(f"{BASE_URL}/api/routing/trials/rt-a5201bf3bb/adopt", headers=op, json={"model": "claude-haiku-4-5-20251001"}, timeout=20)
    assert r.status_code == 409, r.text
    r = requests.post(f"{BASE_URL}/api/routing/trials/rt-a5201bf3bb/adopt", headers=op, json={"model": "not-a-candidate"}, timeout=20)
    assert r.status_code == 409
    # interrupted trial cannot be adopted
    r = requests.post(f"{BASE_URL}/api/routing/trials/rt-797ce9f4f3/adopt", headers=op, json={"model": "gpt-5.4-mini"}, timeout=20)
    assert r.status_code == 409
    # revert with nothing adopted → 404
    r = requests.post(f"{BASE_URL}/api/routing/revert", headers=op, json={"role": "planner"}, timeout=20)
    assert r.status_code == 404, r.text


def test_adoption_round_trip_and_armi_sync():
    op = _login(OP)
    # ensure nothing adopted first (revert if any)
    requests.post(f"{BASE_URL}/api/routing/revert", headers=op, json={"role": "planner", "note": "pre-cleanup"}, timeout=20)
    before = {r["role"]: r for r in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=20).json()["roles"]}["planner"]
    assert before["model"] == "gpt-6-astra" and before["decision"] is None

    r = requests.post(f"{BASE_URL}/api/routing/trials/rt-a5201bf3bb/adopt", headers=op, json={"model": "gpt-5.4-mini", "note": "QA"}, timeout=30)
    assert r.status_code == 200, r.text
    dec = r.json()["decision"]
    assert dec["role"] == "planner" and dec["model"] == "gpt-5.4-mini" and dec["sdk_provider"] == "openai" and dec["trial_id"] == "rt-a5201bf3bb"
    assert "measured" in dec

    try:
        a = {r["role"]: r for r in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=20).json()["roles"]}["planner"]
        assert a["model"] == "gpt-5.4-mini"
        assert a["basis"].startswith("measured routing trial rt-a5201bf3bb"), a["basis"]
        assert a["configured_model"] == "gpt-6-astra"
        assert a["decision"]["trial_id"] == "rt-a5201bf3bb"

        # armi sync & lookup
        requests.post(f"{BASE_URL}/api/armi/sync", headers=op, timeout=60)
        agents = requests.get(f"{BASE_URL}/api/armi/agents", headers=op, timeout=30).json().get("agents", [])
        planner_agent = next((x for x in agents if x.get("agent_id") == "llm:planner:gpt-5.4-mini"), None)
        assert planner_agent is not None, [x.get("agent_id") for x in agents if "planner" in str(x.get("agent_id"))]
        admission = planner_agent.get("admission", {})
        decision_txt = admission.get("decision", "")
        assert decision_txt.startswith("measured routing trial"), decision_txt
    finally:
        rv = requests.post(f"{BASE_URL}/api/routing/revert", headers=op, json={"role": "planner", "note": "QA end"}, timeout=30)
        assert rv.status_code == 200, rv.text
        requests.post(f"{BASE_URL}/api/armi/sync", headers=op, timeout=60)

    restored = {r["role"]: r for r in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=20).json()["roles"]}["planner"]
    assert restored["model"] == "gpt-6-astra" and restored["decision"] is None
