"""M2 live drill pack against the deployed backend (roadmap M2-T2 release authority · M2-T3 mirage and
marks · M2-T4 response integrity · M2-T5 learn without self-authorising). Ordered; leaves REAL Watch
evidence on disk. Isolated drill subject: demo.dpo (severed, then released by operator + master_admin).
Never POSTs a valid census/training phase — nothing is dispatched to any worker."""
import os
import time

import pytest
import requests

BASE = (os.environ.get("REACT_APP_BACKEND_URL") or "").rstrip("/")
T = 45
ACCOUNTS = {"operator": ("demo.operator@demo.rms.example.com", "demo-operator-pw"),
            "master_admin": ("demo.master_admin@demo.rms.example.com", "demo-master-admin-pw"),
            "dpo": ("demo.dpo@demo.rms.example.com", "demo-dpo-pw")}
DECOY = f"rms-finance-backup-2019-q3-{int(time.time())}"
pytestmark = pytest.mark.skipif(not BASE, reason="REACT_APP_BACKEND_URL is not set")
_state = {}


def _headers(role):
    if role not in _state:
        r = requests.post(f"{BASE}/api/auth/login", json={"email": ACCOUNTS[role][0], "password": ACCOUNTS[role][1]}, timeout=T)
        assert r.status_code == 200, r.text[:200]
        _state[role] = {"Authorization": f"Bearer {r.json()['access_token']}", "Content-Type": "application/json"}
    return _state[role]


def _me(role):
    r = requests.get(f"{BASE}/api/portal/census/overview", headers=_headers(role), timeout=T)
    assert r.status_code == 200
    return r.json()["principal_id"]


def _watch(role="operator"):
    r = requests.get(f"{BASE}/api/portal/watch/state", headers=_headers(role), timeout=T)
    assert r.status_code == 200, r.text[:200]
    return r.json()


def test_t3_operator_plants_decoy_with_measured_isolation():
    r = requests.post(f"{BASE}/api/portal/watch/mirage/plant", headers=_headers("operator"), json={"decoy_ref": DECOY, "ttl_seconds": 86400}, timeout=T)
    assert r.status_code == 200, r.text[:300]
    planted = r.json()["planted"]
    assert planted["isolation_check"]["passed"] is True and planted["isolation_check"]["stores_compared"] == 7
    _state["mirage_id"] = planted["mirage_id"]
    mirage = _watch()["mirage"]
    assert mirage["live"] >= 1 and mirage["isolation_passed"] is True and DECOY not in str(mirage)   # placement never rendered


def test_t3_subject_touching_decoy_is_severed_and_marked():
    r = requests.post(f"{BASE}/api/portal/census/run", headers=_headers("dpo"), json={"source_ids": [DECOY]}, timeout=T)
    assert r.status_code == 403, r.text[:300]
    assert "dual-control" in r.json()["detail"] and "sha256" not in r.json()["detail"]
    subject = f"principal:{_me('dpo')}"
    state = _watch()
    held = [m for m in state["marked"] if m["subject_ref"] == subject and m["standing"] == "held"]
    assert len(held) == 1 and held[0]["dimensions_bound"] == 6 and "credentials" not in held[0]
    open_items = [d for d in state["decisions"] if d["state"] == "open" and d["klass"] == "demark_release" and d["subject_ref"] == subject]
    assert len(open_items) == 1
    _state["decision_id"], _state["action_id"], _state["subject"] = open_items[0]["decision_id"], open_items[0]["refs"]["action_ref"], subject
    row = next(r for r in state["records"] if r["record_id"] == _state["action_id"])
    assert row["state"] == "Held" and row["lane"] == "held" and row["walk"]["complete"] is True and row["walk"]["witness"].startswith("wa_gate_")
    assert row["notice"]["kind"] == "sever"


def test_t3_mark_state_checked_at_every_gate_reads_unaffected():
    r = requests.post(f"{BASE}/api/portal/census/plan", headers=_headers("dpo"), json={}, timeout=T)
    assert r.status_code == 403 and _state["action_id"] in r.json()["detail"]
    r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs", headers=_headers("dpo"), json={"phase": "nope"}, timeout=T)
    assert r.status_code == 403 and _state["action_id"] in r.json()["detail"]
    assert requests.get(f"{BASE}/api/portal/census/overview", headers=_headers("dpo"), timeout=T).status_code == 200
    notices = requests.get(f"{BASE}/api/portal/watch/notices", headers=_headers("dpo"), timeout=T).json()["notices"]
    assert notices[0]["kind"] == "sever" and notices[0]["refs"]["action_ref"] == _state["action_id"]
    effects = _watch()["counts"]["gate_effects"]
    assert effects >= 3


def test_t2_acknowledgement_and_single_approval_do_not_release():
    url = f"{BASE}/api/portal/watch/decisions/{_state['decision_id']}"
    ack = requests.post(url, headers=_headers("operator"), json={"act": "acknowledge"}, timeout=T)
    assert ack.status_code == 200 and ack.json()["decision"]["state"] == "open" and ack.json()["decision"]["protection_changed"] is False
    first = requests.post(url, headers=_headers("operator"), json={"act": "approve", "note": "Drill subject reviewed; release."}, timeout=T)
    assert first.status_code == 200 and first.json()["decision"]["state"] == "open" and len(first.json()["decision"]["approvers"]) == 1
    again = requests.post(url, headers=_headers("operator"), json={"act": "approve", "note": "again"}, timeout=T)
    assert again.status_code == 409 and "different estate operator" in again.json()["detail"]
    r = requests.post(f"{BASE}/api/portal/census/plan", headers=_headers("dpo"), json={}, timeout=T)
    assert r.status_code == 403 and _state["action_id"] in r.json()["detail"]        # still held


def test_t2_second_distinct_operator_releases_and_gate_admits_again():
    url = f"{BASE}/api/portal/watch/decisions/{_state['decision_id']}"
    second = requests.post(url, headers=_headers("master_admin"), json={"act": "approve", "note": "Concur; drill release."}, timeout=T)
    assert second.status_code == 200, second.text[:300]
    assert second.json()["decision"]["state"] == "executed" and second.json()["decision"]["protection_changed"] is True
    time.sleep(1)
    r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs", headers=_headers("dpo"), json={"phase": "nope"}, timeout=T)
    assert r.status_code == 422, r.text[:300]                                        # handler reached: restoration is real; nothing dispatched
    state = _watch()
    row = next(r for r in state["records"] if r["record_id"] == _state["action_id"])
    assert row["state"] == "Released" and "released_by_dual_control" in row["basis"]
    assert all(m["standing"] != "held" for m in state["marked"] if m["subject_ref"] == _state["subject"])
    notices = requests.get(f"{BASE}/api/portal/watch/notices", headers=_headers("dpo"), timeout=T).json()["notices"]
    assert [n["kind"] for n in notices[:2]] == ["release", "sever"]


def test_t4_standing_break_in_measures_immutability():
    r = requests.post(f"{BASE}/api/portal/watch/witness/break-in", headers=_headers("operator"), json={"action_id": _state["action_id"]}, timeout=T)
    assert r.status_code == 200, r.text[:300]
    result = r.json()["break_in"]
    assert result["immutability_measurement"] == "passed" and result["attempt_result"] == "refused" and "write_once" in result["refusal_reason"]
    tiles = _watch()["tiles"]
    assert tiles["checks"]["value"] >= 1 and tiles["recovery"]["value"] >= 1


def test_t4_analyst_and_legacy_boundaries_hold():
    analyst = requests.post(f"{BASE}/api/auth/login", json={"email": "demo.analyst@demo.rms.example.com", "password": "demo-analyst-pw"}, timeout=T).json()["access_token"]
    h = {"Authorization": f"Bearer {analyst}", "Content-Type": "application/json"}
    assert requests.get(f"{BASE}/api/portal/watch/state", headers=h, timeout=T).status_code == 403
    assert requests.post(f"{BASE}/api/portal/watch/decisions/{_state['decision_id']}", headers=h, json={"act": "approve", "note": "x"}, timeout=T).status_code == 403
    assert requests.post(f"{BASE}/api/portal/watch/mirage/plant", headers=h, json={"decoy_ref": "analyst-decoy-attempt"}, timeout=T).status_code == 403
    assert requests.get(f"{BASE}/api/portal/watch/notices", headers=h, timeout=T).status_code == 200      # own notices only
    assert requests.post(f"{BASE}/api/watch/verdict", headers=_headers("operator"), json={"x": 1}, timeout=T).status_code == 409
    assert requests.get(f"{BASE}/api/portal/watch/notices", timeout=T).status_code == 401


def test_t5_finding_enters_research_loop_and_two_operators_ratify_v1():
    r = requests.post(f"{BASE}/api/portal/watch/learning/propose", headers=_headers("operator"), json={}, timeout=T)
    assert r.status_code == 200, r.text[:300]
    item = r.json()["decision"]
    assert item["klass"] == "requirement_ratification" and item["refs"]["routing"] == "research_loop_appended"
    before = _watch()["learning"]
    url = f"{BASE}/api/portal/watch/decisions/{item['decision_id']}"
    one = requests.post(url, headers=_headers("master_admin"), json={"act": "approve", "note": "Pin the operating thresholds as v1."}, timeout=T)
    assert one.status_code == 200 and one.json()["decision"]["state"] == "open"
    assert _watch()["learning"]["requirements_version"] == before["requirements_version"]        # one operator cannot ratify
    two = requests.post(url, headers=_headers("operator"), json={"act": "approve", "note": "Concur."}, timeout=T)
    assert two.status_code == 200 and two.json()["decision"]["state"] == "executed"
    learning = _watch()["learning"]
    assert learning["requirements_version"] == (before["requirements_version"] or 0) + 1 and learning["label"].startswith("requirements=v")
    assert [s["stage"] for s in learning["steps"][-2:]] == ["proposed", "ratified"]
