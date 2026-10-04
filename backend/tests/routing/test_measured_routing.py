"""Mα MA-08 (T08) — measured routing. Recommendation and floor logic are checked in-process on fixed summaries (no model spend); the live API
checks cover assignments, trial listing, adoption refusals and authorisation. Trials are NOT started by this file (each costs 15 metered
calls); adoption of a real trial is exercised only when an already-measured trial exists and is reverted at the end."""
import os
import sys

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
OPERATOR = {"email": "demo.operator@demo.rms.example.com", "password": "demo-operator-pw"}
ANALYST = {"email": "demo.analyst@demo.rms.example.com", "password": "demo-analyst-pw"}
sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")


def _login(creds):
    r = requests.post(f"{BASE_URL}/api/auth/login", json=creds, timeout=20)
    if r.status_code != 200: pytest.skip(f"login failed for {creds['email']}: {r.status_code}")
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _summary(model, provider, accepted, latency, tokens_out, cost=None):
    from services.chokepoint import routing
    rows = [{"task_id": f"T{i}", "status": "answered", "json_valid": True, "accepted": a, "tokens_in": 1000, "tokens_out": tokens_out, "latency_ms": latency, "findings": []} for i, a in enumerate(accepted)]
    s = routing._summarise({"model": model, "provider": provider}, rows, incumbent="gpt-6-astra")
    if cost is not None: s["cost_usd"] = cost
    return s


def test_floors_and_recommendation_prefer_known_cost_then_tokens():
    from services.chokepoint import routing
    a = _summary("gpt-6-astra", "openai", [True, True, True], 20000, 2000)
    b = _summary("gpt-5.4-mini", "openai", [True, True, True], 8000, 1700)
    c = _summary("claude-haiku-4-5-20251001", "anthropic", [False, True, True], 9000, 1500)
    assert a["meets_floors"] and b["meets_floors"] and not c["meets_floors"] and a["incumbent"] and not b["incumbent"]
    rec = routing._recommend([a, b, c])
    assert rec["model"] == "gpt-5.4-mini" and rec["cost_known_for_all"] is False and "proxy" in rec["basis"] and "claude-haiku-4-5-20251001" not in rec["eligible"]
    a2, b2 = dict(a, cost_usd=0.05), dict(b, cost_usd=0.08)
    rec2 = routing._recommend([a2, b2, c])
    assert rec2["model"] == "gpt-6-astra" and rec2["cost_known_for_all"] is True and "lowest owner-priced" in rec2["basis"]
    assert routing._recommend([c])["model"] is None


def test_refusal_and_slow_candidates_fail_floors():
    from services.chokepoint import routing
    slow = _summary("x", "openai", [True, True, True], routing.FLOORS["latency_ms_p50_max"] + 1, 10)
    assert not slow["meets_floors"]
    rows = [{"task_id": "T0", "status": "refused", "json_valid": False, "accepted": False, "tokens_in": 0, "tokens_out": 0, "latency_ms": 10, "findings": ["LLMShieldFailure: x"]}]
    refused = routing._summarise({"model": "y", "provider": "openai"}, rows, incumbent="z")
    assert refused["refusals"] == 1 and not refused["meets_floors"] and refused["pass_rate"] == 0


def test_acceptance_gate_normalises_figures_and_ignores_clock_times():
    from services.caas import service as caas
    ctx = {"brand_mention_inventory": {"by_language": {"kik": [{"brand": "X", "segments": 274}]}, "share": 0.874}}
    ok = {s: "text" for s in caas.PRODUCTS["domain.media_plan"]["sections"]}
    ok["dayparts"] = "06:00–09:00 and 18:00–21:00; share 0.8740; 274 segments"
    assert caas.accept("domain.media_plan", ok, ctx)["accepted"] is True
    bad = dict(ok, budget_split="allocate 1234.5 to kik")
    res = caas.accept("domain.media_plan", bad, ctx); assert res["accepted"] is False and "1234.5" in res["findings"][0]


def test_live_assignments_trials_and_authorisation():
    op = _login(OPERATOR); an = _login(ANALYST)
    a = requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=30); assert a.status_code == 200
    body = a.json(); roles = {r["role"]: r for r in body["roles"]}
    assert set(roles) == {"assistant", "planner", "reviewer", "writer"} and roles["planner"]["task_set_defined"] is True and len(roles["planner"]["candidates"]) >= 2
    assert body["planner_reviewer_distinct_families"] is True and set(body["floors"]) == {"pass_rate", "json_rate", "latency_ms_p50_max", "refusals_max"}
    for r in body["roles"]: assert r["basis"].startswith("measured routing trial") == bool(r["decision"])
    t = requests.get(f"{BASE_URL}/api/routing/trials?role=planner", headers=op, timeout=30); assert t.status_code == 200
    assert requests.get(f"{BASE_URL}/api/routing/trials", headers=an, timeout=30).status_code == 200
    assert requests.post(f"{BASE_URL}/api/routing/trials", headers=an, json={"role": "planner"}, timeout=30).status_code == 403
    assert requests.post(f"{BASE_URL}/api/routing/trials", json={"role": "planner"}, timeout=30).status_code == 401
    assert requests.post(f"{BASE_URL}/api/routing/trials", headers=op, json={"role": "writer"}, timeout=30).status_code == 409  # no task set yet → refused, no spend
    assert requests.get(f"{BASE_URL}/api/routing/trials/rt-doesnotexist", headers=op, timeout=30).status_code == 404
    assert requests.post(f"{BASE_URL}/api/routing/trials/rt-doesnotexist/adopt", headers=op, json={"model": "x"}, timeout=30).status_code == 404


def test_live_adoption_is_floor_bound_and_reversible():
    op = _login(OPERATOR)
    trials = [x for x in requests.get(f"{BASE_URL}/api/routing/trials?role=planner", headers=op, timeout=30).json()["trials"] if x["status"] == "measured"]
    if not trials: pytest.skip("no measured planner trial on record")
    t = requests.get(f"{BASE_URL}/api/routing/trials/{trials[0]['trial_id']}", headers=op, timeout=30).json()["trial"]
    failing = next((c for c in t["candidates"] if not c["meets_floors"]), None)
    if failing: assert requests.post(f"{BASE_URL}/api/routing/trials/{t['trial_id']}/adopt", headers=op, json={"model": failing["model"]}, timeout=30).status_code == 409
    assert requests.post(f"{BASE_URL}/api/routing/trials/{t['trial_id']}/adopt", headers=op, json={"model": "not-a-candidate"}, timeout=30).status_code == 409
    before = {r["role"]: r for r in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=30).json()["roles"]}["planner"]
    rec = t["recommendation"]["model"]
    if not rec or before["decision"]: pytest.skip("no recommendation or a decision is already adopted; not changing production routing from a test")
    r = requests.post(f"{BASE_URL}/api/routing/trials/{t['trial_id']}/adopt", headers=op, json={"model": rec, "note": "T08 test"}, timeout=30); assert r.status_code == 200, r.text
    try:
        after = {x["role"]: x for x in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=30).json()["roles"]}["planner"]
        assert after["model"] == rec and after["basis"].startswith("measured routing trial") and after["decision"]["trial_id"] == t["trial_id"]
    finally:
        rv = requests.post(f"{BASE_URL}/api/routing/revert", headers=op, json={"role": "planner", "note": "T08 test end"}, timeout=30); assert rv.status_code == 200
    restored = {x["role"]: x for x in requests.get(f"{BASE_URL}/api/routing/assignments", headers=op, timeout=30).json()["roles"]}["planner"]
    assert restored["model"] == before["model"] and restored["decision"] is None
