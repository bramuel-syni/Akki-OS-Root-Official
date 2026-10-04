"""Mα MA-30 (T30) — rate coverage and honest pricing. Rates are owner-supplied facts or absent: metered GPU-hours and CaaS deliveries become
money only through a governed rate row with a source. In-process arithmetic uses a temporary register so no test rate ever enters the
product register; the live API checks cover authorisation and refusal paths that write nothing."""
import json
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


@pytest.fixture
def register(tmp_path, monkeypatch):
    monkeypatch.setenv("RATES_REGISTER_DIR", str(tmp_path))
    from services.cost_ledger import rates
    return rates


def test_rates_are_absent_until_authored(register):
    assert register.load_rates() == {"models": [], "gpu_hours": [], "training": [], "caas": []}
    assert register.rate_for_gpu_hour("akki-vm") is None and register.rate_for_caas_product("domain.media_plan") is None


def test_author_rate_refuses_claims_and_credentials(register):
    with pytest.raises(ValueError): register.author_rate("gpu_hours", {"node_id": "*", "rate_per_hour": 3.5, "source": "placeholder guess"}, "t")
    with pytest.raises(ValueError): register.author_rate("gpu_hours", {"node_id": "*", "rate_per_hour": 3.5}, "t")
    with pytest.raises(ValueError): register.author_rate("gpu_hours", {"node_id": "*", "rate_per_hour": 0, "source": "invoice 1"}, "t")
    with pytest.raises(ValueError): register.author_rate("gpu_hours", {"node_id": "*", "rate_per_hour": 2, "source": "invoice 1", "api_key": "x"}, "t")
    with pytest.raises(ValueError): register.author_rate("nonsense", {"x": 1, "source": "invoice 1"}, "t")
    assert register.load_rates()["gpu_hours"] == []


def test_wildcard_and_exact_rates_price_measured_hours(register, tmp_path):
    from services.training_lab import malpha
    rows = [{"host": "akki-vm", "gpu_seconds": 3600}, {"host": "akki-vm-ii", "gpu_seconds": 1800}]
    unpriced = malpha.price_gpu(rows)
    assert unpriced["cost_usd"] is None and unpriced["unpriced_gpu_hours"] == 1.5 and unpriced["rate_usd_per_gpu_hour"] is None
    register.author_rate("gpu_hours", {"node_id": "*", "rate_per_hour": 2.0, "source": "provider invoice TEST-1"}, "tester")
    assert (tmp_path / "gpu_hours" / "wildcard.json").is_file()
    priced = malpha.price_gpu(rows)
    assert priced["cost_usd"] == 3.0 and priced["priced_gpu_hours"] == 1.5 and priced["unpriced_gpu_hours"] == 0
    register.author_rate("gpu_hours", {"node_id": "akki-vm", "rate_per_hour": 4.0, "source": "provider invoice TEST-2"}, "tester")
    assert malpha.price_gpu(rows)["cost_usd"] == 5.0  # exact host row wins over the wildcard
    second = json.loads((tmp_path / "gpu_hours" / "akki-vm.json").read_text()); assert "supersedes" not in second
    register.author_rate("gpu_hours", {"node_id": "akki-vm", "rate_per_hour": 4.5, "source": "provider invoice TEST-3"}, "tester")
    third = json.loads((tmp_path / "gpu_hours" / "akki-vm.json").read_text()); assert third["supersedes"]["rate_per_hour"] == 4.0
    assert register.remove_rate("gpu_hours", "akki-vm") and malpha.price_gpu(rows)["cost_usd"] == 3.0


def test_caas_product_rate_resolution(register):
    register.author_rate("caas", {"product_id": "*", "rate_per_delivery": 10, "source": "licence schedule TEST"}, "tester")
    register.author_rate("caas", {"product_id": "domain.media_plan", "rate_per_delivery": 25, "source": "licence schedule TEST"}, "tester")
    assert register.rate_for_caas_product("domain.media_plan")["rate_per_delivery"] == 25
    assert register.rate_for_caas_product("brand.mention_inventory")["rate_per_delivery"] == 10


def test_live_rates_endpoint_and_write_authorisation():
    r = requests.get(f"{BASE_URL}/api/cost_ledger/rates", timeout=30); assert r.status_code == 200
    body = r.json(); assert set(body["lanes"]) == {"models", "gpu_hours", "training", "caas"} and all(isinstance(body[k], list) for k in body["lanes"])
    analyst = _login(ANALYST)
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/gpu_hours", headers=analyst, json={"node_id": "*", "rate_per_hour": 1, "source": "test"}, timeout=30).status_code == 403
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/gpu_hours", json={"node_id": "*", "rate_per_hour": 1, "source": "test"}, timeout=30).status_code == 401
    op = _login(OPERATOR)
    # refusals that write nothing: missing source (422 from the schema), placeholder source, unknown lane, no positive rate
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/gpu_hours", headers=op, json={"node_id": "*", "rate_per_hour": 1}, timeout=30).status_code == 422
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/gpu_hours", headers=op, json={"node_id": "*", "rate_per_hour": 1, "source": "placeholder pending owner"}, timeout=30).status_code == 422
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/nonsense", headers=op, json={"x": "*", "source": "invoice"}, timeout=30).status_code == 422
    assert requests.post(f"{BASE_URL}/api/cost_ledger/rates/caas", headers=op, json={"product_id": "*", "source": "licence schedule"}, timeout=30).status_code == 422
    assert requests.delete(f"{BASE_URL}/api/cost_ledger/rates/gpu_hours/never-authored-host", headers=op, timeout=30).status_code == 404
    after = requests.get(f"{BASE_URL}/api/cost_ledger/rates", timeout=30).json()
    assert after["gpu_hours"] == body["gpu_hours"] and after["caas"] == body["caas"]


def test_live_metering_is_honest_about_pricing():
    op = _login(OPERATOR)
    m = requests.get(f"{BASE_URL}/api/training/malpha/status", headers=op, timeout=60).json()["metering"]
    assert m["budget_mode"] == "uncapped_until_billing" and m["numeric_cap"] is None and m["gpu_hours_total"] > 0
    assert (m["cost_usd"] is None) == (m["priced_gpu_hours"] == 0)
    assert abs(m["priced_gpu_hours"] + m["unpriced_gpu_hours"] - m["gpu_hours_total"]) < 0.01
    for lane in m["by_lane"].values(): assert set(lane) == {"jobs", "gpu_hours", "cost_usd"}
    o = requests.get(f"{BASE_URL}/api/armi/overview", headers=op, timeout=60).json()
    assert set(o["contribution"]) >= {"deliveries_total", "attributed", "unattributed", "amount_usd", "rule"} and o["contribution"]["attributed"] + o["contribution"]["unattributed"] == o["contribution"]["deliveries_total"]
    assert set(o["rate_card"]) == {"models", "gpu_hours", "training", "caas"}
    c = requests.get(f"{BASE_URL}/api/caas/metering", headers=op, timeout=60).json()
    for line in c["lines"]: assert line["priced_quantity"] + line["unpriced_quantity"] == line["quantity"] and (line["amount_usd"] is None) == (line["priced_quantity"] == 0)
