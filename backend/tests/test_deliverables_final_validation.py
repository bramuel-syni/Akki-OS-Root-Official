"""Final delivery validation for downloadable report artifacts and endpoint contract."""

import hashlib
import os
from pathlib import Path
import re
import zipfile

import pytest
import requests


# Module: public deliverables API + released artifact integrity checks
DELIVERABLES = [
    "RMS_Estate_Intelligence_and_Language_Opportunities.pptx",
    "RMS_Estate_Intelligence_and_Language_Opportunities.docx",
]


def _read_base_url() -> str:
    base = os.environ.get("REACT_APP_BACKEND_URL", "").strip()
    if base:
        return base.rstrip("/")

    env_path = Path("/app/frontend/.env")
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                value = line.split("=", 1)[1].strip()
                if value:
                    return value.rstrip("/")

    pytest.fail("REACT_APP_BACKEND_URL is required for public endpoint verification")


BASE_URL = _read_base_url()
LOCAL_DIR = Path("/app/backend/deliverables")
RELEASE_A_OUT = Path("/app/assessment_workspace/deliverables/estate_intelligence_20261001/release/a/out")
RELEASE_B_OUT = Path("/app/assessment_workspace/deliverables/estate_intelligence_20261001/release/b/out")


@pytest.fixture(scope="module")
def http() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "*/*"})
    yield s
    s.close()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _local_bytes(filename: str) -> bytes:
    return (LOCAL_DIR / filename).read_bytes()


def test_deliverables_list_contains_expected_reports(http: requests.Session):
    resp = http.get(f"{BASE_URL}/api/deliverables", timeout=60)
    assert resp.status_code == 200
    data = resp.json()
    names = [item["name"] for item in data.get("items", [])]
    for expected in DELIVERABLES:
        assert expected in names


@pytest.mark.parametrize(
    "filename,expected_mime",
    [
        (DELIVERABLES[0], "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
        (DELIVERABLES[1], "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ],
)
def test_public_download_headers_and_bytes(http: requests.Session, filename: str, expected_mime: str):
    local = _local_bytes(filename)
    resp = http.get(f"{BASE_URL}/api/deliverables/{filename}", timeout=120)

    assert resp.status_code == 200
    assert resp.headers.get("content-type") == expected_mime
    content_disposition = resp.headers.get("content-disposition", "")
    assert "attachment" in content_disposition.lower()
    assert filename in content_disposition
    assert resp.content == local


def test_deliverables_reject_non_allowlisted_file(http: requests.Session):
    resp = http.get(f"{BASE_URL}/api/deliverables/not-allowlisted.bin", timeout=60)
    assert resp.status_code == 404


@pytest.mark.parametrize("filename", DELIVERABLES)
def test_zip_integrity_for_downloaded_artifacts(filename: str):
    path = LOCAL_DIR / filename
    with zipfile.ZipFile(path, "r") as zf:
        assert zf.testzip() is None


def test_pptx_has_expected_slide_count_and_slide_23_accuracy_text():
    pptx_path = LOCAL_DIR / DELIVERABLES[0]
    with zipfile.ZipFile(pptx_path, "r") as zf:
        slide_names = []
        for name in zf.namelist():
            if not (name.startswith("ppt/slides/") and name.endswith(".xml")):
                continue
            match = re.search(r"ppt/slides/slide(\d+)\.xml$", name)
            if match:
                slide_names.append((int(match.group(1)), name))

        slides = [name for _, name in sorted(slide_names, key=lambda pair: pair[0])]
        assert len(slides) == 43

        slide_23_xml = zf.read("ppt/slides/slide23.xml").decode("utf-8", "ignore")
        slide_23_text = " ".join(re.findall(r"<a:t>(.*?)</a:t>", slide_23_xml))
        assert "Conditional macro accuracy is 97.213%" in slide_23_text
        assert "across all presented examples" in slide_23_text
        assert "does not certify the whole estate" in slide_23_text


@pytest.mark.parametrize("filename", DELIVERABLES)
def test_release_a_b_and_backend_deliverable_are_byte_identical(filename: str):
    mapped = filename.replace("RMS_Estate_Intelligence_and_Language_Opportunities", "rms-estate-and-local-language-opportunities")
    local = _local_bytes(filename)
    a_bytes = (RELEASE_A_OUT / mapped).read_bytes()
    b_bytes = (RELEASE_B_OUT / mapped).read_bytes()

    assert a_bytes == b_bytes
    assert local == a_bytes
    assert _sha256_bytes(local) == _sha256_bytes(a_bytes)
