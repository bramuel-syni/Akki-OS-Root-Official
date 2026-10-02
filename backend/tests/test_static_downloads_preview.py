"""Module: static public download endpoints and artifact integrity on preview URL."""

import hashlib
import os
from pathlib import Path
import zipfile

import pytest
import requests


EXPECTED = {
    "/downloads/RMS_Estate_Report.pptx": {
        "filename": "RMS_Estate_Report.pptx",
        "bytes": 147034,
        "sha256": "dfdecac561ad62527aae0c37d6735a7b60ff897e860fd45d66629c85d8f7e480",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    },
    "/downloads/RMS_Estate_Report.docx": {
        "filename": "RMS_Estate_Report.docx",
        "bytes": 218731,
        "sha256": "5f85e6b342ddc3cb824973f2c3578636a5598550d9ead26efd8bae03188234f0",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
    "/downloads/RMS_Estate_Reports.zip": {
        "filename": "RMS_Estate_Reports.zip",
        "bytes": 338458,
        "sha256": "33399542e89ce651c8c13ea55398c6d36b469b9aac8a2abb1b1060b87d639c20",
        "mime": "application/zip",
    },
}


def _base_url() -> str:
    value = os.environ.get("REACT_APP_BACKEND_URL", "").strip()
    if value:
        return value.rstrip("/")

    env_path = Path("/app/frontend/.env")
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                value = line.split("=", 1)[1].strip()
                if value:
                    return value.rstrip("/")

    pytest.fail("REACT_APP_BACKEND_URL is required")


BASE_URL = _base_url()


@pytest.fixture(scope="module")
def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "*/*"})
    yield s
    s.close()


@pytest.mark.parametrize("path", list(EXPECTED.keys()))
def test_static_download_headers_and_hash(path: str, session: requests.Session):
    expected = EXPECTED[path]
    response = session.get(f"{BASE_URL}{path}", timeout=120)

    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert content_type.split(";")[0].strip() == expected["mime"]

    payload = response.content
    assert payload[:20].lower() != b"<!doctype html>"[:20]
    assert b"<html" not in payload[:200].lower()

    assert len(payload) == expected["bytes"]
    assert hashlib.sha256(payload).hexdigest() == expected["sha256"]


def test_static_zip_contains_exact_reports(session: requests.Session, tmp_path: Path):
    zip_response = session.get(f"{BASE_URL}/downloads/RMS_Estate_Reports.zip", timeout=120)
    assert zip_response.status_code == 200

    zip_path = tmp_path / "RMS_Estate_Reports.zip"
    zip_path.write_bytes(zip_response.content)

    with zipfile.ZipFile(zip_path, "r") as archive:
        names = sorted(archive.namelist())
        assert names == ["RMS_Estate_Report.docx", "RMS_Estate_Report.pptx"]

        docx_bytes = archive.read("RMS_Estate_Report.docx")
        pptx_bytes = archive.read("RMS_Estate_Report.pptx")

        assert len(docx_bytes) == EXPECTED["/downloads/RMS_Estate_Report.docx"]["bytes"]
        assert hashlib.sha256(docx_bytes).hexdigest() == EXPECTED["/downloads/RMS_Estate_Report.docx"]["sha256"]

        assert len(pptx_bytes) == EXPECTED["/downloads/RMS_Estate_Report.pptx"]["bytes"]
        assert hashlib.sha256(pptx_bytes).hexdigest() == EXPECTED["/downloads/RMS_Estate_Report.pptx"]["sha256"]
