"""M6 · doc-studio v1.1 installed as Akki's primary production skill — evals 1–3 from the owner's package run in-pod, plus the
Akki adapter (install manifest, manifest template, frames, census producer, receipt binding, revise/strike/re-verdict) against a
temp commission store. Terminal pytest is the verification of record (owner condition C). No network, no model, no GPU."""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "vendored" / "extraction_akki" / "backend"
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DOC_STUDIO_TOOLS_DIR", str(BACKEND / "services" / "transform_forms" / "doc_studio" / "tools"))

from services.transform_forms.doc_studio import install, store  # noqa: E402
from services.transform_forms.doc_studio.frames import FRAMES, frame_for, verdict_from_frame  # noqa: E402
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief  # noqa: E402
from services.transform_forms.doc_studio.producer_estate import build_content, commission_from_report  # noqa: E402
from services.transform_forms.doc_studio.receipts import bind_receipts  # noqa: E402
from services.transform_forms.doc_studio.skill_env import SCRIPTS_DIR, SKILL_DIR, build_env  # noqa: E402

FIXTURE = SKILL_DIR / "fixtures" / "board-pack"
REPORT = Path("/app/assessment_workspace/phase0/census_autonomy_state/estate_intelligence/eij-1b359b3cbd2e.report.json")
LIBREOFFICE = shutil.which("soffice") is not None


def run(cmd, timeout=280):
    return subprocess.run([sys.executable, *cmd], capture_output=True, text=True, timeout=timeout, env=build_env(), cwd=str(SKILL_DIR))


# ----------------------------------------------------------------------------- install


def test_install_manifest_edit_is_within_approval():
    m = install.read_manifest()
    assert m["version"] == "1.2"
    # v1.1 = condition A (tool paths); v1.2 = owner ruling 3a (declared option-model rows in the workbook spec).
    assert set(m["changed_from_v1_0"]) == {"scripts/build.py", "scripts/qa.py", "scripts/render_xlsx.py", "scripts/studio.py", "schemas/workbook.schema.json"}, m["changed_from_v1_0"]
    assert set(m["approved_edits"]) == set(m["changed_from_v1_0"])
    assert m["edit_within_approval"] is True
    assert m["owner_zip_sha256"] == "8f920f9f70c771a4e4edabf9ab85e142aa6b5ab1554de094818f3039cba56840"
    assert len(m["installed_files_sha256"]) == 39 and len(m["v1_0_files_sha256"]) == 39
    for rel in m["installed_files_sha256"]:
        if rel not in m["changed_from_v1_0"]:
            assert m["v1_0_files_sha256"][rel] == m["installed_files_sha256"][rel], f"{rel} drifted from the owner's package"
        else:
            assert m["v1_0_files_sha256"][rel] != m["installed_files_sha256"][rel], f"{rel} is listed as changed but is byte-identical"


def test_approved_edit_reads_tools_dir_from_environment():
    for name in ("build.py", "qa.py"):
        text = (SCRIPTS_DIR / name).read_text()
        assert 'os.environ.get("DOC_STUDIO_TOOLS_DIR"' in text
        assert 'Path("/mnt/skills/public")' not in text


def test_environment_of_record_is_pinned():
    env = install.environment()
    assert env["python-pptx"] == "1.0.2" and env["matplotlib"] != "missing"
    assert env["libreoffice"].startswith("LibreOffice") if LIBREOFFICE else env["libreoffice"] == "unavailable"


# ----------------------------------------------------------------------------- evals 1–3 (owner package, in-pod)


@pytest.fixture(scope="module")
def eval1(tmp_path_factory):
    build_dir = tmp_path_factory.mktemp("ds") / "board-pack"
    r = run(["scripts/build.py", str(FIXTURE), str(build_dir), "--prove"])
    return build_dir, r


@pytest.mark.skipif(not LIBREOFFICE, reason="LibreOffice is the environment of record for the workbook recalc")
def test_eval1_board_pack_proves_byte_identical(eval1):
    build_dir, r = eval1
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    assert "[prove] byte-identical across two builds: 4 outputs" in r.stdout
    ma, mb = (json.loads((build_dir / x / "out" / "build-manifest.json").read_text()) for x in ("a", "b"))
    assert ma["outputs_sha256"] == mb["outputs_sha256"]
    assert set(ma["outputs_sha256"]) == {"northline-depot-automation-review.html", "northline-depot-automation.docx", "northline-depot-automation.pptx", "northline-depot-automation.xlsx"}
    assert ma["environment"]["libreoffice"].startswith("LibreOffice 7.4")
    assert json.loads((build_dir / "a" / "out" / "qa-report.json").read_text())["status"] == "PASS"
    validate = json.loads((build_dir / "a" / "resolved" / "validate-report.json").read_text())
    assert validate["status"] == "PASS" and validate["blockers"] == []


@pytest.mark.skipif(not LIBREOFFICE, reason="LibreOffice is the environment of record for the workbook recalc")
def test_eval1_pptx_hash_matches_owner_manifest_and_others_are_reported(eval1):
    """Same python-pptx (1.0.2) → identical pptx bytes to the owner's shipped manifest; html/docx/xlsx differ by environment and are reported, not hidden."""
    build_dir, _ = eval1
    ma = json.loads((build_dir / "a" / "out" / "build-manifest.json").read_text())
    shipped = json.loads(Path("/app/assessment_workspace/incoming/doc_studio_20260930/owner_artifacts/build-manifest.json").read_text())
    assert ma["outputs_sha256"]["northline-depot-automation.pptx"] == shipped["outputs_sha256"]["northline-depot-automation.pptx"]
    assert ma["environment"]["libreoffice"] != shipped["environment"]["libreoffice"]


@pytest.mark.skipif(not LIBREOFFICE, reason="LibreOffice is the environment of record for the workbook recalc")
def test_eval2_content_revision_preserves_look_no_strike(eval1, tmp_path):
    build_dir, _ = eval1
    new_fixture, new_build = tmp_path / "fixture", tmp_path / "build"
    r = run(["scripts/revise.py", str(FIXTURE), str(new_fixture), str(build_dir / "a"), str(new_build), "content.options.O2.capex=28.5", "content.options.O2.annual_saving=8.4"])
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    report = json.loads((new_build / "revision-report.json").read_text())
    assert report["content_ref"] == "northline-depot-automation@2"
    assert report["look_preserved"] is True and report["strikes"] == [] and report["release"] == "clear"
    assert set(report["outputs_changed"]) >= {"northline-depot-automation.pptx", "northline-depot-automation.docx", "northline-depot-automation.xlsx"}


@pytest.mark.skipif(not LIBREOFFICE, reason="LibreOffice is the environment of record for the workbook recalc")
def test_eval3_brief_change_strikes_manifest_and_blocks_release(eval1, tmp_path):
    build_dir, _ = eval1
    r = run(["scripts/revise.py", str(FIXTURE), str(tmp_path / "fixture"), str(build_dir / "a"), str(tmp_path / "build"), "brief.setting.printed=false"])
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    report = json.loads((tmp_path / "build" / "revision-report.json").read_text())
    assert [s["manifest"] for s in report["strikes"]] == ["M3"]
    assert report["strikes"][0]["flips"] == ["palette_field", "full_bleed_disallowed"]
    assert report["release"] == "blocked pending re-verdict"


# ----------------------------------------------------------------------------- adapter: template, frames, producer


def brief_stub(**over):
    b = {"brief_id": "BR-x", "content_ref": "c@1", "purpose": {"kind": "decide", "statement": "choose"}, "audience": {"who": "Estate owner", "knowledge": "high", "priorities": ["cost", "quality"], "detail": "summary"},
         "setting": {"mode": "read-ahead", "read_unattended": True, "printed": True}, "content": {}, "brand": {"house": "house-neutral", "formality": "formal", "expressiveness": "restrained", "variation_allowed": "within-family"},
         "outputs": [{"format": "pptx", "role": "deck"}]}
    for k, v in over.items():
        b[k] = v
    return b


def test_manifest_template_generates_from_brief_not_fixture():
    printed = manifest_from_brief(brief_stub(), has_options=True)
    assert [m["id"] for m in printed] == ["M1", "M2", "M3", "M4", "M5", "M6"]
    assert printed[0]["assumption"] == "Audience is Estate owner; the pack must let them decide"
    assert printed[2]["assumption"] == "Pack will be printed" and printed[2]["source"] == "brief.setting.printed"
    screen = manifest_from_brief(brief_stub(setting={"mode": "live", "read_unattended": False, "printed": False}), has_options=False)
    assert [m["id"] for m in screen] == ["M1", "M2", "M3", "M4", "M5"]
    assert screen[1]["flips"] == ["so_what_brevity", "no_paper_output"] and screen[2]["assumption"] == "Pack is screen-only"
    fixture_manifest = json.loads((FIXTURE / "verdict.json").read_text())["manifest"]
    assert [m["assumption"] for m in printed] != [m["assumption"] for m in fixture_manifest]


def test_standing_frame_covers_routine_and_refuses_non_routine():
    assert frame_for(brief_stub())["frame_id"] == "FR-strategy-decide-v1"
    assert frame_for(brief_stub(purpose={"kind": "inspire", "statement": "x"})) is None
    v = verdict_from_frame(FRAMES["FR-strategy-decide-v1"], brief_stub(), "V-1", manifest_from_brief(brief_stub(), True), "operator-1", "2026-09-30T00:00:00Z")
    assert v["adopted"] == "D1" and {c["verdict"] for c in v["candidates"]} == {"adopt", "defer", "reject"}
    assert "cost, quality" in v["candidates"][0]["rationale"] and v["confirmed_by"] == "operator-1"


@pytest.fixture(scope="module")
def report():
    if not REPORT.exists():
        pytest.skip("banked estate intelligence report not present")
    return json.loads(REPORT.read_text())


def test_producer_content_model_is_receipted_and_schema_valid(report):
    import jsonschema
    content = build_content(report, "RMS")
    jsonschema.validate(content, json.loads((SKILL_DIR / "schemas" / "content.schema.json").read_text()))
    assert all("platform_ref" in r for r in content["receipts"].values())
    assert all(f["class"] in ("measured", "estimated", "sample") and f["receipt"] in content["receipts"] for f in content["facts"].values())
    assert content["coverage"]["cannot_say"] and content["census_ref"] == report["job_id"]


def test_producer_seed_and_stamp_are_derived_and_specs_hold_no_numbers(report):
    import jsonschema
    now = datetime(2026, 9, 30, 12, 0, 0, tzinfo=timezone.utc)
    plan = commission_from_report(report, "RMS", "principal-1", now)
    assert plan["seed"] == f"estate-intelligence-{report['job_id']}/decide/2026-09-30"
    assert plan["build_stamp"] == "2026-09-30T12:00:00Z"
    assert plan["commission_id"].startswith("com-") and plan["frame_ref"] == "FR-strategy-decide-v1"
    for name in ("deck.json", "paper.json", "workbook.json"):
        spec = plan["files"][name]
        jsonschema.validate(spec, json.loads((SKILL_DIR / "schemas" / f"{spec['spec_type']}.schema.json").read_text()))
        assert spec["seed"] == plan["seed"] and spec["build_stamp"] == plan["build_stamp"]
    sys.path.insert(0, str(SCRIPTS_DIR))
    import validate as va  # noqa: E402
    assert va.retyped_numbers(plan["files"]["deck.json"]) == []
    assert va.retyped_numbers(plan["files"]["paper.json"]) == []
    assert plan["files"]["verdict.json"]["manifest"][0]["source"] == "brief.purpose, brief.audience"
    # v1.2 (owner ruling 3a): the workbook declares its option rows/checks in the spec; the option model is live, not fixture-shaped.
    options = next(s for s in plan["files"]["workbook.json"]["sheets"] if s["kind"] == "options_model")
    assert options["options"] == ["O1", "O2", "O3"] and {r["field"] for r in options["rows"]} == {"reclaimable_gib", "monthly_saving_usd"}
    assert {s["kind"] for s in plan["files"]["workbook.json"]["sheets"]} == {"cover", "inputs", "options_model", "series", "checks"}


def test_receipts_bind_platform_refs_and_block_unresolvable(report):
    content = build_content(report, "RMS")
    bound, blockers = bind_receipts(content)
    assert blockers == [] and all(b["binding"] == "platform" for b in bound.values())
    content["receipts"]["R09"] = {"resolves_to": "a made-up receipt that resolves nowhere", "platform_ref": "eij-000000000000"}
    content["receipts"]["R10"] = {"resolves_to": "a declared, non-platform receipt"}
    bound, blockers = bind_receipts(content)
    assert [b["receipt"] for b in blockers] == ["R09"] and bound["R10"]["binding"] == "declared"


# ----------------------------------------------------------------------------- adapter: lifecycle on a temp store


@pytest.fixture(scope="module")
def studio_store(tmp_path_factory, report):
    os.environ["AKKI_STUDIO_STORE_DIR"] = str(tmp_path_factory.mktemp("studio_store"))
    from services.transform_forms.doc_studio import service
    return service


def test_lifecycle_commission_build_revise_strike_reverdict(studio_store, report, monkeypatch):
    service = studio_store
    import services.census_autonomy.estate_intelligence_report as eir
    monkeypatch.setattr(eir, "report_for", lambda job_id, **kw: report if job_id == report["job_id"] else None)
    rec, created = service.create_from_estate(report["job_id"], "RMS", "operator-1")
    assert created and rec["release"]["state"] == "unbuilt" and rec["receipt_blockers"] == []
    again, created_again = service.create_from_estate(report["job_id"], "RMS", "operator-1")
    assert not created_again and again["commission_id"] == rec["commission_id"], "same census, purpose and day → the same commission, never a duplicate"
    rec = service.build("RMS", rec["commission_id"], "operator-1")
    b = rec["builds"][-1]
    assert b["status"] == "released" and b["prove"]["byte_identical"] is True, (b.get("error"), b.get("validate"), b.get("qa"))
    assert {o["format"] for o in b["outputs"]} == {"pptx", "docx", "html", "xlsx"} and b["validate"]["blockers"] == [] and b["qa"]["status"] == "PASS"
    assert b["exports"]["thumbnails"]["rendered"] is True and b["exports"]["thumbnails"]["count"] >= 10, b["exports"]["thumbnails"]
    assert service.thumbnail("RMS", rec["commission_id"], b["build_id"], 1)[:8] == b"\x89PNG\r\n\x1a\n"
    assert service.thumbnail("RMS", rec["commission_id"], b["build_id"], 499) is None
    assert rec["release"]["state"] == "clear" and rec["economics"]["renders_total"] == 2 and rec["economics"]["authoring_tokens_total"] == 0
    rec = service.revise("RMS", rec["commission_id"], "operator-1", [{"path": "content.facts.F005.value", "value": 16.0}])
    rev = rec["revisions"][-1]
    assert rec["current_content_version"] == 2 and rev["strikes"] == [] and rev["look_preserved"] is True and rev["release"] == "clear"
    assert set(rev["outputs_changed"]) and rec["builds"][-1]["status"] == "released"
    v2 = json.loads((store.version_dir("RMS", rec["commission_id"], 2) / "content.json").read_text())
    v1 = json.loads((store.version_dir("RMS", rec["commission_id"], 1) / "content.json").read_text())
    assert v2["facts"]["F005"]["value"] == 16.0 and v1["facts"]["F005"]["value"] != 16.0 and v2["version"] == 2
    rec = service.revise("RMS", rec["commission_id"], "operator-1", [{"path": "brief.setting.printed", "value": False}])
    rev = rec["revisions"][-1]
    assert [s["manifest"] for s in rev["strikes"]] == ["M3"] and rec["release"]["state"] == "blocked pending re-verdict"
    assert rec["builds"][-1]["status"] == "released", "a strike blocks release, not the build"
    with pytest.raises(ValueError):
        service.revise("RMS", rec["commission_id"], "operator-1", [{"path": "content.facts.F999.value", "value": 1}])
    rec = service.reverdict("RMS", rec["commission_id"], "operator-1")
    assert rec["release"]["state"] == "clear" and rec["verdict_id"].endswith("-r4")
    assert next(m for m in rec["manifest"] if m["id"] == "M3")["assumption"] == "Pack is screen-only"
    hit = service.artifact("RMS", rec["commission_id"], rec["builds"][-1]["build_id"], next(o["name"] for o in rec["builds"][-1]["outputs"] if o["format"] == "pptx"))
    assert hit and hit[0][:2] == b"PK" and "presentationml" in hit[1]
    assert service.artifact("RMS", rec["commission_id"], rec["builds"][-1]["build_id"], "../../etc/passwd") is None
    assert service.get_commission("OTHER", rec["commission_id"]) is None
