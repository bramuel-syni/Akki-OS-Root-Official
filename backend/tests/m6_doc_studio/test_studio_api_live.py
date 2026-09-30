"""M6 · /api/studio/* live against the preview control plane: identity gates, skill state, the census producer (idempotent per day),
downloads with correct media types, PDF export, and refusal paths for bad revisions (mutating semantics are proven offline). Uses the existing RMS operator/analyst identities from
memory/test_credentials.md; creates no accounts. Builds are real (skill subprocess), so this suite stays small."""
import os

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
OPERATOR = (os.environ.get("AKKI_TEST_RMS_OPERATOR_EMAIL", "demo.operator@demo.rms.example.com"), os.environ.get("AKKI_TEST_RMS_OPERATOR_PASSWORD", "demo-operator-pw"))
ANALYST = (os.environ.get("AKKI_TEST_RMS_ANALYST_EMAIL", "demo.analyst@demo.rms.example.com"), os.environ.get("AKKI_TEST_RMS_ANALYST_PASSWORD", "demo-analyst-pw"))
JOB = "eij-1b359b3cbd2e"
T = 290


def _login(email, password):
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": password}, timeout=30)
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}", "Content-Type": "application/json"}


@pytest.fixture(scope="module")
def operator():
    return _login(*OPERATOR)


@pytest.fixture(scope="module")
def analyst():
    return _login(*ANALYST)


@pytest.fixture(scope="module")
def state():
    return {}


def test_identity_gates(analyst):
    assert requests.get(f"{BASE_URL}/api/studio/commissions", timeout=30).status_code == 401
    assert requests.get(f"{BASE_URL}/api/studio/commissions", headers=analyst, timeout=30).status_code == 200
    r = requests.post(f"{BASE_URL}/api/studio/producers/estate-intelligence/{JOB}", headers=analyst, json={}, timeout=30)
    assert r.status_code == 403 and "operator" in r.json()["detail"]


def test_skill_state(operator):
    r = requests.get(f"{BASE_URL}/api/studio/skill", headers=operator, timeout=30)
    assert r.status_code == 200
    s = r.json()
    assert s["skill"] == "doc-studio" and s["version"] == "1.1" and s["edit_within_approval"] is True
    assert s["changed_from_v1_0"] == ["scripts/build.py", "scripts/qa.py"]
    assert s["environment"]["libreoffice"].startswith("LibreOffice") and s["direction_stage"]["llm_chokepoint_path"].startswith("none")


def test_producer_is_idempotent_per_day_and_releases(operator, state):
    r = requests.post(f"{BASE_URL}/api/studio/producers/estate-intelligence/{JOB}", headers=operator, json={}, timeout=T)
    assert r.status_code == 201, r.text
    c = r.json()["commission"]
    state["id"] = c["commission_id"]
    again = requests.post(f"{BASE_URL}/api/studio/producers/estate-intelligence/{JOB}", headers=operator, json={}, timeout=T).json()
    assert again["created"] is False and again["commission"]["commission_id"] == c["commission_id"]
    assert all(v["binding"] == "platform" for v in c["receipts"].values())
    if c["release"]["state"] == "unbuilt":
        c = requests.post(f"{BASE_URL}/api/studio/commissions/{c['commission_id']}/build", headers=operator, timeout=T).json()["commission"]
    assert c["builds"], "a released commission has at least one build"
    released = [b for b in c["builds"] if b["status"] == "released"]
    assert released, c["builds"][-1]
    state["build"] = released[-1]
    assert state["build"]["prove"]["byte_identical"] is True and state["build"]["qa"]["status"] == "PASS"
    assert requests.post(f"{BASE_URL}/api/studio/producers/estate-intelligence/eij-000000000000", headers=operator, json={}, timeout=30).status_code == 404


def test_downloads_carry_media_types(operator, state):
    b = state["build"]
    for o in b["outputs"]:
        r = requests.get(f"{BASE_URL}/api/studio/commissions/{state['id']}/builds/{b['build_id']}/artifact/{o['name']}", headers=operator, timeout=60)
        assert r.status_code == 200 and len(r.content) == o["size"], o["name"]
        assert {"pptx": "presentationml", "docx": "wordprocessingml", "html": "text/html"}[o["format"]] in r.headers["content-type"]
    r = requests.get(f"{BASE_URL}/api/studio/commissions/{state['id']}/builds/{b['build_id']}/artifact/build-manifest.json", headers=operator, timeout=30)
    assert r.status_code == 200 and set(r.json()["outputs_sha256"]) == {o["name"] for o in b["outputs"]}
    assert requests.get(f"{BASE_URL}/api/studio/commissions/{state['id']}/builds/{b['build_id']}/artifact/secret.txt", headers=operator, timeout=30).status_code == 404


def test_export_pdf(operator, state):
    b = state["build"]
    r = requests.post(f"{BASE_URL}/api/studio/commissions/{state['id']}/builds/{b['build_id']}/export-pdf", headers=operator, timeout=T)
    assert r.status_code == 201, r.text
    entry = next(x for x in r.json()["commission"]["builds"] if x["build_id"] == b["build_id"])
    pdf = entry["exports"]["pdf"]
    assert pdf["exported"] is True and pdf["check"]["survives"] is True
    d = requests.get(f"{BASE_URL}/api/studio/commissions/{state['id']}/builds/{b['build_id']}/artifact/review.pdf", headers=operator, timeout=60)
    assert d.status_code == 200 and d.content[:4] == b"%PDF"


def test_mutations_are_refused_for_bad_paths_without_touching_the_record(operator, state):
    """Revise/strike/re-verdict semantics are proven offline on a temp store (test_doc_studio_install.py); against the tenant's real
    commission this suite only proves the refusal paths, so no test value ever lands on the record."""
    cid = state["id"]
    before = requests.get(f"{BASE_URL}/api/studio/commissions/{cid}", headers=operator, timeout=30).json()["commission"]
    assert requests.post(f"{BASE_URL}/api/studio/commissions/{cid}/revise", headers=operator, json={"changes": [{"path": "verdict.adopted", "value": "D2"}]}, timeout=T).status_code == 422
    assert requests.post(f"{BASE_URL}/api/studio/commissions/{cid}/revise", headers=operator, json={"changes": [{"path": "content.facts.F999.value", "value": 1}]}, timeout=T).status_code == 422
    assert requests.post(f"{BASE_URL}/api/studio/commissions/{cid}/revise", headers=operator, json={"changes": "nope"}, timeout=T).status_code == 422
    assert requests.post(f"{BASE_URL}/api/studio/commissions/{cid}/reverdict", headers=operator, timeout=T).status_code == 422, "no strike pending → refused"
    after = requests.get(f"{BASE_URL}/api/studio/commissions/{cid}", headers=operator, timeout=30).json()["commission"]
    assert after["current_content_version"] == before["current_content_version"] and len(after["revisions"]) == len(before["revisions"])
