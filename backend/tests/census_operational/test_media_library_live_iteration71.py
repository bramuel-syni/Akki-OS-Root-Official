"""Live media library API contracts: storage, permissions, metadata, assessments, archival."""

import hashlib
import json
import uuid
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values


FRONTEND_ENV = dotenv_values("/app/frontend/.env")
_BASE = (FRONTEND_ENV.get("REACT_APP_BACKEND_URL") or "").rstrip("/")
if not _BASE:
    raise RuntimeError("REACT_APP_BACKEND_URL missing in /app/frontend/.env")
BASE_URL = f"{_BASE}/api"


def _creds(email: str) -> tuple[str, str]:
    lines = Path("/app/memory/test_credentials.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        if "|" not in line or email not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 3 and parts[0] == email:
            return parts[0], parts[1]
    raise RuntimeError(f"Credentials not found for {email}")


def _login(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    assert response.status_code == 200, f"login failed for {email}: {response.status_code}"
    body = response.json()
    assert "access_token" in body and isinstance(body["access_token"], str)
    return body["access_token"]


def _headers(token: str | None = None, idem: str | None = None, octet: bool = False) -> dict:
    out = {}
    if token:
        out["Authorization"] = f"Bearer {token}"
    if idem:
        out["Idempotency-Key"] = idem
    if octet:
        out["Content-Type"] = "application/octet-stream"
    return out


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _prepare(token: str, idem: str, filename: str, blob: bytes) -> requests.Response:
    return requests.post(
        f"{BASE_URL}/media/uploads",
        headers=_headers(token, idem),
        json={
            "filename": filename,
            "size_bytes": len(blob),
            "sha256": _sha(blob),
            "storage_permission_confirmed": True,
        },
        timeout=60,
    )


def _upload_content(token: str, file_id: str, blob: bytes) -> requests.Response:
    return requests.put(
        f"{BASE_URL}/media/files/{file_id}/content",
        headers=_headers(token, octet=True),
        data=blob,
        timeout=120,
    )


@pytest.fixture(scope="session")
def auth_tokens():
    rms_operator = _creds("demo.operator@demo.rms.example.com")
    rms_analyst = _creds("demo.analyst@demo.rms.example.com")
    digicow_operator = _creds("demo.operator@demo.digicow.example.com")
    return {
        "rms_operator": _login(*rms_operator),
        "rms_analyst": _login(*rms_analyst),
        "digicow_operator": _login(*digicow_operator),
    }


@pytest.fixture(scope="session")
def uploaded_assets(auth_tokens):
    token = auth_tokens["rms_operator"]
    wav = b"RIFF" + (36).to_bytes(4, "little") + b"WAVEfmt " + b"\x10\x00\x00\x00"
    wav += b"\x01\x00\x01\x00" + (8000).to_bytes(4, "little") + (16000).to_bytes(4, "little")
    wav += b"\x02\x00\x10\x00" + b"data" + (0).to_bytes(4, "little")
    mp3 = b"ID3\x03\x00\x00\x00\x00\x00\x0FTESTAUDIOFRAME"
    txt = "hello transcript\nline 2".encode("utf-8")
    jsn = json.dumps({"labels": [{"start": 0, "end": 1.2, "tag": "speech"}]}).encode("utf-8")
    csv_data = b"start,end,label\n0,1.2,speech\n"

    payloads = {
        "wav": ("TEST_IT71_audio.wav", wav),
        "mp3": ("TEST_IT71_music.mp3", mp3),
        "txt": ("TEST_IT71_notes.txt", txt),
        "json": ("TEST_IT71_labels.json", jsn),
        "csv": ("TEST_IT71_manifest.csv", csv_data),
    }

    files = {}
    for key, (name, blob) in payloads.items():
        idem = f"it71-{key}-{uuid.uuid4().hex[:20]}"
        pre = _prepare(token, idem, name, blob)
        assert pre.status_code == 201, pre.text
        body = pre.json()
        file_id = body["file"]["file_id"]
        put = _upload_content(token, file_id, blob)
        assert put.status_code == 200, put.text
        files[key] = {
            "file_id": file_id,
            "filename": name,
            "blob": blob,
            "sha": _sha(blob),
            "size": len(blob),
        }

    yield files

    # Archive synthetic fixtures for retention-safe cleanup; no hard delete.
    rows = requests.get(f"{BASE_URL}/media/files", headers=_headers(token), timeout=60).json().get("files", [])
    rev_map = {r["file_id"]: r["revision"] for r in rows}
    for info in files.values():
        fid = info["file_id"]
        revision = rev_map.get(fid)
        if not revision:
            continue
        requests.post(
            f"{BASE_URL}/media/files/{fid}/archive",
            headers=_headers(token),
            json={"revision": revision, "retention_acknowledged": True},
            timeout=60,
        )


def test_media_config_ready_and_limits(auth_tokens):
    response = requests.get(f"{BASE_URL}/media/config", headers=_headers(auth_tokens["rms_operator"]), timeout=30)
    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "RMS"
    assert body["storage_ready"] is True
    assert body["hard_delete_supported"] is False
    assert body["direct_upload_supported"] is False
    assert body["max_batch_files"] == 20


def test_permissions_anonymous_and_read_only(auth_tokens):
    anon = requests.get(f"{BASE_URL}/media/files", timeout=20)
    assert anon.status_code == 401
    analyst_attempt = requests.post(
        f"{BASE_URL}/media/uploads",
        headers=_headers(auth_tokens["rms_analyst"], f"it71-analyst-{uuid.uuid4().hex[:16]}"),
        json={
            "filename": "TEST_IT71_blocked.wav",
            "size_bytes": 16,
            "sha256": hashlib.sha256(b"RIFFWAVEcontent").hexdigest(),
            "storage_permission_confirmed": True,
        },
        timeout=30,
    )
    assert analyst_attempt.status_code == 403


def test_prepare_validation_and_idempotency_quota(auth_tokens):
    token = auth_tokens["rms_operator"]
    before = requests.get(f"{BASE_URL}/media/config", headers=_headers(token), timeout=30).json()["reserved_bytes"]

    bad_ext = requests.post(
        f"{BASE_URL}/media/uploads",
        headers=_headers(token, f"it71-badext-{uuid.uuid4().hex[:16]}"),
        json={
            "filename": "bad.exe",
            "size_bytes": 10,
            "sha256": _sha(b"abcdefghij"),
            "storage_permission_confirmed": True,
        },
        timeout=30,
    )
    assert bad_ext.status_code == 422

    no_permission = requests.post(
        f"{BASE_URL}/media/uploads",
        headers=_headers(token, f"it71-noperm-{uuid.uuid4().hex[:16]}"),
        json={
            "filename": "TEST_IT71_noperm.txt",
            "size_bytes": 4,
            "sha256": _sha(b"test"),
            "storage_permission_confirmed": False,
        },
        timeout=30,
    )
    assert no_permission.status_code == 422

    blob = b"ID3\x03\x00\x00\x00\x00\x00\x10SAME"
    idem = f"it71-idem-{uuid.uuid4().hex[:18]}"
    first = _prepare(token, idem, "TEST_IT71_idem.mp3", blob)
    assert first.status_code == 201
    first_file = first.json()["file"]["file_id"]
    second = _prepare(token, idem, "TEST_IT71_idem.mp3", blob)
    assert second.status_code == 201
    second_body = second.json()
    assert second_body["created"] is False
    assert second_body["file"]["file_id"] == first_file

    conflict = requests.post(
        f"{BASE_URL}/media/uploads",
        headers=_headers(token, idem),
        json={
            "filename": "TEST_IT71_idem_changed.mp3",
            "size_bytes": len(blob),
            "sha256": _sha(blob),
            "storage_permission_confirmed": True,
        },
        timeout=30,
    )
    assert conflict.status_code == 409

    after = requests.get(f"{BASE_URL}/media/config", headers=_headers(token), timeout=30).json()["reserved_bytes"]
    assert after >= before


def test_content_validation_4xx_not_500(auth_tokens):
    token = auth_tokens["rms_operator"]
    valid = b"ID3\x03\x00\x00\x00\x00\x00\x10GOOD"
    pre = _prepare(token, f"it71-content-{uuid.uuid4().hex[:18]}", "TEST_IT71_content.mp3", valid)
    assert pre.status_code == 201
    fid = pre.json()["file"]["file_id"]

    # Hash mismatch
    mismatch = _upload_content(token, fid, b"ID3\x03\x00\x00\x00\x00\x00\x10BADD")
    assert mismatch.status_code == 422

    # Corrupt signature with new reservation
    fake_mp3 = b"not-an-mp3-but-text"
    pre2 = _prepare(token, f"it71-corrupt-{uuid.uuid4().hex[:18]}", "TEST_IT71_corrupt.mp3", fake_mp3)
    assert pre2.status_code == 201
    sig_fail = _upload_content(token, pre2.json()["file"]["file_id"], fake_mp3)
    assert sig_fail.status_code == 422

    # Invalid JSON syntax
    invalid_json = b"{\"labels\":["
    pre3 = _prepare(token, f"it71-json-{uuid.uuid4().hex[:18]}", "TEST_IT71_invalid.json", invalid_json)
    assert pre3.status_code == 201
    json_fail = _upload_content(token, pre3.json()["file"]["file_id"], invalid_json)
    assert json_fail.status_code == 422


def test_uploaded_download_hash_and_public_fields(auth_tokens, uploaded_assets):
    token = auth_tokens["rms_operator"]
    rows_response = requests.get(f"{BASE_URL}/media/files", headers=_headers(token), timeout=60)
    assert rows_response.status_code == 200
    rows = rows_response.json()["files"]
    assert rows
    for row in rows:
        assert "storage_path" not in row
        assert "upload_token" not in row
        assert "upload_key" not in row

    wav = uploaded_assets["wav"]
    dl = requests.get(f"{BASE_URL}/media/files/{wav['file_id']}/download", headers=_headers(token), timeout=60)
    assert dl.status_code == 200
    assert hashlib.sha256(dl.content).hexdigest() == wav["sha"]
    assert len(dl.content) == wav["size"]


def test_tenant_isolation_with_known_foreign_id(auth_tokens, uploaded_assets):
    rms_file_id = uploaded_assets["wav"]["file_id"]
    digi_list = requests.get(f"{BASE_URL}/media/files", headers=_headers(auth_tokens["digicow_operator"]), timeout=30)
    assert digi_list.status_code == 200
    assert all(item["file_id"] != rms_file_id for item in digi_list.json()["files"])

    foreign_download = requests.get(
        f"{BASE_URL}/media/files/{rms_file_id}/download",
        headers=_headers(auth_tokens["digicow_operator"]),
        timeout=30,
    )
    assert foreign_download.status_code == 404


def test_metadata_revision_conflict_and_rights_requirements(auth_tokens, uploaded_assets):
    token = auth_tokens["rms_operator"]
    file_id = uploaded_assets["mp3"]["file_id"]
    files = requests.get(f"{BASE_URL}/media/files", headers=_headers(token), timeout=30).json()["files"]
    row = next(r for r in files if r["file_id"] == file_id)

    missing_basis = requests.patch(
        f"{BASE_URL}/media/files/{file_id}",
        headers=_headers(token),
        json={
            "revision": row["revision"],
            "title": "X" * 140,
            "language": "en",
            "event_label": "music",
            "label_status": "human_reviewed",
            "rights_status": "declared",
            "rights_basis": "",
            "rights_reference": "",
            "training_permission_confirmed": False,
        },
        timeout=30,
    )
    assert missing_basis.status_code == 422

    valid = requests.patch(
        f"{BASE_URL}/media/files/{file_id}",
        headers=_headers(token),
        json={
            "revision": row["revision"],
            "title": "X" * 140,
            "language": "Swahili",
            "event_label": "music",
            "label_status": "human_reviewed",
            "rights_status": "declared",
            "rights_basis": "licensed",
            "rights_reference": "contract-IT71",
            "training_permission_confirmed": True,
        },
        timeout=30,
    )
    assert valid.status_code == 200
    updated = valid.json()["file"]
    assert updated["title"] == "X" * 140
    assert updated["rights_status"] == "declared"

    stale = requests.patch(
        f"{BASE_URL}/media/files/{file_id}",
        headers=_headers(token),
        json={
            "revision": row["revision"],
            "title": "stale-write",
            "language": "",
            "event_label": "music",
            "label_status": "human_reviewed",
            "rights_status": "declared",
            "rights_basis": "licensed",
            "rights_reference": "contract-IT71",
            "training_permission_confirmed": True,
        },
        timeout=30,
    )
    assert stale.status_code == 409


def test_assessment_idempotency_and_rights_withdrawal_stale(auth_tokens, uploaded_assets):
    token = auth_tokens["rms_operator"]
    target = uploaded_assets["mp3"]["file_id"]
    idem = f"it71-assess-{uuid.uuid4().hex[:18]}"

    first = requests.post(
        f"{BASE_URL}/media/assessments",
        headers=_headers(token, idem),
        json={"file_ids": [target], "title": "IT71 readiness"},
        timeout=60,
    )
    assert first.status_code == 201
    run_a = first.json()["run"]
    assert run_a["kind"] == "dataset_readiness"
    assert run_a["status"] == "complete"
    assert run_a["dataset_assessment"]["scope"] == "uploaded_file_metadata_only"

    replay = requests.post(
        f"{BASE_URL}/media/assessments",
        headers=_headers(token, idem),
        json={"file_ids": [target], "title": "IT71 readiness"},
        timeout=60,
    )
    assert replay.status_code == 201
    assert replay.json()["created"] is False
    assert replay.json()["run"]["run_id"] == run_a["run_id"]

    collision = requests.post(
        f"{BASE_URL}/media/assessments",
        headers=_headers(token, idem),
        json={"file_ids": [target], "title": "different-title"},
        timeout=60,
    )
    assert collision.status_code == 409

    # Rights withdrawal should block download + new assessments, and stale old run.
    rows = requests.get(f"{BASE_URL}/media/files", headers=_headers(token), timeout=30).json()["files"]
    row = next(r for r in rows if r["file_id"] == target)
    withdraw = requests.patch(
        f"{BASE_URL}/media/files/{target}",
        headers=_headers(token),
        json={
            "revision": row["revision"],
            "title": row["title"],
            "language": row["language"],
            "event_label": row["event_label"],
            "label_status": row["label_status"],
            "rights_status": "withdrawn",
            "rights_basis": "",
            "rights_reference": "",
            "training_permission_confirmed": False,
        },
        timeout=30,
    )
    assert withdraw.status_code == 200

    blocked_download = requests.get(f"{BASE_URL}/media/files/{target}/download", headers=_headers(token), timeout=30)
    assert blocked_download.status_code == 403

    blocked_assess = requests.post(
        f"{BASE_URL}/media/assessments",
        headers=_headers(token, f"it71-assess-block-{uuid.uuid4().hex[:16]}"),
        json={"file_ids": [target], "title": "blocked"},
        timeout=30,
    )
    assert blocked_assess.status_code == 403

    run_check = requests.get(f"{BASE_URL}/training/lab/runs/{run_a['run_id']}", headers=_headers(token), timeout=30)
    assert run_check.status_code == 200
    assert run_check.json()["run"]["current_validity"]["stale"] is True


def test_archive_semantics_and_idempotency(auth_tokens, uploaded_assets):
    token = auth_tokens["rms_operator"]
    target = uploaded_assets["txt"]["file_id"]
    rows = requests.get(f"{BASE_URL}/media/files", headers=_headers(token), timeout=30).json()["files"]
    row = next(r for r in rows if r["file_id"] == target)

    first = requests.post(
        f"{BASE_URL}/media/files/{target}/archive",
        headers=_headers(token),
        json={"revision": row["revision"], "retention_acknowledged": True},
        timeout=30,
    )
    assert first.status_code == 200
    archived = first.json()["file"]
    assert archived["is_deleted"] is True

    download_410 = requests.get(f"{BASE_URL}/media/files/{target}/download", headers=_headers(token), timeout=30)
    assert download_410.status_code == 410

    edit_410 = requests.patch(
        f"{BASE_URL}/media/files/{target}",
        headers=_headers(token),
        json={
            "revision": archived["revision"],
            "title": archived["title"],
            "language": archived["language"],
            "event_label": archived["event_label"],
            "label_status": archived["label_status"],
            "rights_status": archived["rights_status"],
            "rights_basis": archived["rights_basis"],
            "rights_reference": archived["rights_reference"],
            "training_permission_confirmed": archived["training_permission_confirmed"],
        },
        timeout=30,
    )
    assert edit_410.status_code == 410

    replay = requests.post(
        f"{BASE_URL}/media/files/{target}/archive",
        headers=_headers(token),
        json={"revision": archived["revision"], "retention_acknowledged": True},
        timeout=30,
    )
    assert replay.status_code == 200
    assert replay.json()["file"]["is_deleted"] is True


def test_assessment_listing_and_analyst_mutation_block(auth_tokens, uploaded_assets):
    token = auth_tokens["rms_operator"]
    listing = requests.get(f"{BASE_URL}/media/assessments", headers=_headers(token), timeout=30)
    assert listing.status_code == 200
    assert isinstance(listing.json().get("runs"), list)

    analyst = auth_tokens["rms_analyst"]
    file_id = uploaded_assets["wav"]["file_id"]
    analyst_archive = requests.post(
        f"{BASE_URL}/media/files/{file_id}/archive",
        headers=_headers(analyst),
        json={"revision": 1, "retention_acknowledged": True},
        timeout=30,
    )
    assert analyst_archive.status_code == 403
