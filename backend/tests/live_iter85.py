"""Live backend regression for iter_85: MA-30 economics + MA-29 ARMI attribution."""
import os
import requests

BASE = "https://pensive-goodall-6.preview.emergentagent.com"
OP = ("demo.operator@demo.rms.example.com", "demo-operator-pw")
AN = ("demo.analyst@demo.rms.example.com", "demo-analyst-pw")


def login(email, pw):
    s = requests.Session()
    r = s.post(f"{BASE}/api/auth/login", json={"email": email, "password": pw}, timeout=20)
    assert r.status_code == 200, (r.status_code, r.text[:200])
    tok = r.json()["access_token"]
    s.headers.update({"Authorization": f"Bearer {tok}"})
    return s


def test_rates_public_shape():
    r = requests.get(f"{BASE}/api/cost_ledger/rates", timeout=20)
    assert r.status_code == 200
    j = r.json()
    for k in ("models", "gpu_hours", "training", "caas", "lanes"):
        assert k in j, f"missing {k}"
    assert isinstance(j["lanes"], dict)


def test_rates_write_refusal_matrix():
    # 401 (no auth)
    r = requests.post(f"{BASE}/api/cost_ledger/rates/gpu_hours", json={}, timeout=20)
    assert r.status_code == 401, r.status_code

    # 403 (analyst)
    an = login(*AN)
    r = an.post(f"{BASE}/api/cost_ledger/rates/gpu_hours",
                json={"identifier": "mi300x", "rate_usd": 1.0, "unit": "gpu_hour",
                      "source": "test owner rate"}, timeout=20)
    assert r.status_code == 403, (r.status_code, r.text[:200])

    op = login(*OP)
    # 422 missing source
    r = op.post(f"{BASE}/api/cost_ledger/rates/gpu_hours",
                json={"identifier": "mi300x", "rate_usd": 1.0, "unit": "gpu_hour"}, timeout=20)
    assert r.status_code == 422, (r.status_code, r.text[:200])
    # 422 placeholder source
    r = op.post(f"{BASE}/api/cost_ledger/rates/gpu_hours",
                json={"identifier": "mi300x", "rate_usd": 1.0, "unit": "gpu_hour",
                      "source": "placeholder for later"}, timeout=20)
    assert r.status_code == 422, (r.status_code, r.text[:200])
    # 422 unknown lane
    r = op.post(f"{BASE}/api/cost_ledger/rates/unknown_lane",
                json={"identifier": "x", "rate_usd": 1.0,
                      "source": "real owner note"}, timeout=20)
    assert r.status_code == 422, (r.status_code, r.text[:200])
    # 404 delete never-authored
    r = op.delete(f"{BASE}/api/cost_ledger/rates/gpu_hours/never-authored", timeout=20)
    assert r.status_code == 404, (r.status_code, r.text[:200])

    # After refusals: rates unchanged (gpu_hours/caas empty)
    j = requests.get(f"{BASE}/api/cost_ledger/rates", timeout=20).json()
    assert j["gpu_hours"] == [] or len(j["gpu_hours"]) == 0, j["gpu_hours"]
    assert j["caas"] == [] or len(j["caas"]) == 0, j["caas"]


def test_training_malpha_status_shape():
    op = login(*OP)
    r = op.get(f"{BASE}/api/training/malpha/status", timeout=30)
    assert r.status_code == 200, (r.status_code, r.text[:400])
    j = r.json()
    m = j.get("metering") or j
    # dig into metering
    assert "metering" in j, list(j.keys())
    m = j["metering"]
    assert m["budget_mode"] == "uncapped_until_billing", m["budget_mode"]
    assert m["numeric_cap"] is None, m["numeric_cap"]
    gh = m["gpu_hours_total"]
    assert gh > 0, gh
    priced = m["priced_gpu_hours"]
    unpriced = m["unpriced_gpu_hours"]
    assert abs((priced + unpriced) - gh) < 1e-6, (priced, unpriced, gh)
    if priced == 0:
        assert m["cost_usd"] is None, m["cost_usd"]
    for lane, row in (m.get("by_lane") or {}).items():
        for k in ("jobs", "gpu_hours", "cost_usd"):
            assert k in row, (lane, k, row)


def test_armi_overview_contribution():
    op = login(*OP)
    r = op.get(f"{BASE}/api/armi/overview", timeout=20)
    assert r.status_code == 200, r.text[:400]
    j = r.json()
    c = j["contribution"]
    for k in ("deliveries_total", "attributed", "unattributed", "amount_usd", "rule"):
        assert k in c, k
    assert c["attributed"] + c["unattributed"] == c["deliveries_total"]
    rc = j["rate_card"]
    for k in ("models", "gpu_hours", "training", "caas"):
        assert k in rc, k
    assert j["cost_usd"] is None
    assert "cost_note" in j and "no governed" in j["cost_note"].lower() or "rate card" in j["cost_note"].lower()
    assert j["protected"]["watch_profiles_exported"] is False


def test_armi_agents_shape():
    op = login(*OP)
    r = op.get(f"{BASE}/api/armi/agents", timeout=30)
    assert r.status_code == 200
    agents = r.json().get("agents") or r.json()
    found_malpha = False
    for a in agents:
        aid = a.get("agent_id") or a.get("id") or ""
        if a.get("kind") == "llm":
            c = a.get("contribution") or {}
            assert "basis" in c, (aid, c)
            assert "rule" in c, (aid, c)
        if aid.startswith("model:malpha"):
            found_malpha = True
            res = a.get("resources") or {}
            assert res.get("cost_usd") is None, res
            assert "cost_note" in res, res
    assert found_malpha, "no model:malpha:* agent in /api/armi/agents"


def test_caas_metering_live():
    op = login(*OP)
    r = op.get(f"{BASE}/api/caas/metering", timeout=20)
    assert r.status_code == 200, r.text[:200]
    j = r.json()
    lines = j.get("lines") or j.get("items") or []
    top_cost_note = j.get("cost_note")
    for ln in lines:
        q = ln["quantity"]
        pq = ln["priced_quantity"]
        uq = ln["unpriced_quantity"]
        assert pq + uq == q, ln
        if pq == 0:
            assert ln["amount_usd"] is None, ln
        else:
            assert ln["amount_usd"] is not None, ln
        # cost_note may be per-line or top-level
        assert ("cost_note" in ln) or top_cost_note, ln
