"""
Iteration 79 — training lab board & studio producers (idempotent read-only tests).
Scope: login, board view keys, approve_plan refuses second signature,
white_paper idempotent, estate producer idempotent + negatives,
unauthenticated board 401, download endpoints.
"""
import os
import time
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
if not BASE_URL:
    # Fallback: read frontend .env
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = line.split("=", 1)[1].strip().rstrip("/")

EMAIL = "demo.operator@demo.rms.example.com"
PASSWORD = "demo-operator-pw"

MUSIC_DIGEST = "689f1edfb8d48a526db1d0031d43aabace9000d899c1069b42d0ef9281c1d175"
LWG_DIGEST = "d4c27b6e9871074b7ab8869a647bc548f6346aabb51ace1106f65bc6370c3613"
EXPECTED_COMMISSION = "com-1178b6d9b486"
ESTATE_JOB = "eij-1b359b3cbd2e"
ESTATE_COMMISSION = "com-4a07a8fa312e"


@pytest.fixture(scope="session")
def token():
    r = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=20,
    )
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    data = r.json()
    assert "access_token" in data, f"missing access_token: {data}"
    return data["access_token"]


@pytest.fixture
def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_login_access_token_present(token):
    assert isinstance(token, str) and len(token) > 20


def test_board_view_keys(auth):
    r = requests.get(f"{BASE_URL}/api/training/lab/board", headers=auth, timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    for key in ("tenant_id", "runs", "counts", "training_authorized", "signoffs", "music_detector_admitted"):
        assert key in data, f"missing key {key}"
    assert data["training_authorized"] is True
    assert "music-identification" in data["signoffs"]
    assert "reinforcement-lwg" in data["signoffs"]
    assert data["music_detector_admitted"] is True

    runs = {r_.get("run_id") or r_.get("id"): r_ for r_ in data["runs"]}
    assert "music-identification" in runs
    assert "reinforcement-lwg" in runs

    mi = runs["music-identification"]
    assert mi["status"] == "In service", f"status={mi['status']}"
    approval = mi.get("approval", {})
    signed = approval.get("signed", {})
    assert signed.get("by") == "Demo · Operator", f"signer={signed.get('by')}"
    assert approval.get("line", "").startswith("Signed off by Demo · Operator")
    assert isinstance(mi.get("checks"), list) and len(mi["checks"]) > 0
    assert all(c.get("passes") is True for c in mi["checks"])
    record_rows = mi.get("record_rows", []) or mi.get("record", {}).get("rows", [])
    flat = []
    def collect_strs(x):
        if isinstance(x, str):
            flat.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                collect_strs(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                collect_strs(v)
    collect_strs(record_rows)
    for needed in ("Signed plan", "Compute", "Acceptance", "Artefact"):
        assert any(needed in s for s in flat), f"missing record row {needed}"

    lwg = runs["reinforcement-lwg"]
    assert lwg["status"] in ("In training", "Testing", "In service", "Refused"), f"lwg status={lwg['status']}"
    assert lwg.get("approval", {}).get("signed")
    if lwg["status"] in ("In training", "Testing"):
        assert lwg.get("progress", {}).get("stage"), "progress.stage must be non-empty while training"


def test_approve_plan_music_refuses_second_signature(auth):
    r = requests.post(
        f"{BASE_URL}/api/training/lab/board/music-identification/actions",
        headers=auth,
        json={"action": "approve_plan", "value": MUSIC_DIGEST},
        timeout=30,
    )
    assert r.status_code == 200, f"status={r.status_code} body={r.text}"
    body = r.json()
    text = str(body).lower()
    assert "not done" in text and "signature" in text, body


def test_approve_plan_lwg_refuses_second_signature(auth):
    r = requests.post(
        f"{BASE_URL}/api/training/lab/board/reinforcement-lwg/actions",
        headers=auth,
        json={"action": "approve_plan", "value": LWG_DIGEST},
        timeout=30,
    )
    assert r.status_code == 200, f"status={r.status_code} body={r.text}"
    body = r.json()
    text = str(body).lower()
    assert "not done" in text and "signature" in text, body


def test_white_paper_idempotent(auth):
    r = requests.post(
        f"{BASE_URL}/api/training/lab/board/music-identification/actions",
        headers=auth,
        json={"action": "white_paper"},
        timeout=120,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    # The response contains a `messages` array with the akki response carrying widget=doc + commission_id
    messages = body.get("messages", [])
    akki_doc = next((m for m in messages if m.get("widget") == "doc"), None)
    assert akki_doc is not None, f"no widget=doc message: {body}"
    commission_id = akki_doc.get("commission_id")
    assert commission_id == EXPECTED_COMMISSION, f"got {commission_id}"

    cr = requests.get(f"{BASE_URL}/api/studio/commissions/{commission_id}", headers=auth, timeout=30)
    assert cr.status_code == 200, cr.text
    comm = cr.json().get("commission", {})
    assert comm.get("release", {}).get("state") == "clear"
    assert comm.get("authoring", {}).get("pipeline") == "frontier"
    assert comm.get("authoring", {}).get("model") == "claude-sonnet-5-5"


def test_estate_producer_idempotent(auth):
    r = requests.post(
        f"{BASE_URL}/api/studio/producers/estate-intelligence/{ESTATE_JOB}",
        headers=auth,
        timeout=120,
    )
    assert r.status_code == 201, f"status={r.status_code} body={r.text}"
    body = r.json()
    assert body.get("created") is False, body
    commission_id = body.get("commission_id") or body.get("id")
    # Fetch commission
    cid = commission_id or ESTATE_COMMISSION
    cr = requests.get(f"{BASE_URL}/api/studio/commissions/{cid}", headers=auth, timeout=30)
    assert cr.status_code == 200, cr.text
    comm = cr.json().get("commission", {})
    assert comm.get("release", {}).get("state") == "clear"
    assert comm.get("authoring", {}).get("pipeline") == "frontier"


def test_estate_producer_unknown_job_404(auth):
    r = requests.post(
        f"{BASE_URL}/api/studio/producers/estate-intelligence/eij-000000000000",
        headers=auth,
        timeout=30,
    )
    assert r.status_code == 404, f"status={r.status_code} body={r.text}"


def test_board_unauth_401():
    r = requests.get(f"{BASE_URL}/api/training/lab/board", timeout=20)
    assert r.status_code in (401, 403), f"got {r.status_code}"


def test_commission_music_downloads(auth):
    cr = requests.get(f"{BASE_URL}/api/studio/commissions/{EXPECTED_COMMISSION}", headers=auth, timeout=30)
    assert cr.status_code == 200, cr.text
    comm = cr.json().get("commission", {})
    builds = comm.get("builds", [])
    assert builds, "no builds on commission"
    build = builds[-1]
    build_id = build.get("build_id")
    outputs = build.get("outputs") or []
    names = []
    if isinstance(outputs, dict):
        names = list(outputs.keys())
    elif isinstance(outputs, list):
        for o in outputs:
            if isinstance(o, dict) and o.get("name"):
                names.append(o["name"])
            elif isinstance(o, str):
                names.append(o)
    if not names:
        names = ["paper.docx", "paper.html"]
    tried = 0
    for name in names[:4]:
        url = f"{BASE_URL}/api/studio/commissions/{EXPECTED_COMMISSION}/builds/{build_id}/artifact/{name}"
        dr = requests.get(url, headers=auth, timeout=60)
        if dr.status_code == 200:
            assert len(dr.content) > 100, f"{name} empty"
            tried += 1
    assert tried >= 1, f"no artifact downloaded; names tried={names} build={build_id}"
