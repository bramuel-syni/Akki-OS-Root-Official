"""Whole-estate Monte Carlo forecast (owner order 3 Oct 2026): the engine on synthetic strata (deterministic, no network), the real retained
receipts (consistency: every interval brackets its estimate, the measured part is a subset of the whole), and the estate producer leading
its story with the forecast. Terminal pytest is the verification of record."""
import copy
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "vendored" / "extraction_akki" / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
os.environ.setdefault("DOC_STUDIO_TOOLS_DIR", str(BACKEND / "services" / "transform_forms" / "doc_studio" / "tools"))

from services.census_autonomy import estate_forecast  # noqa: E402


def _folder(name, files, size, kind, *, rate=None, hours=None, speech=None, music=None, langs=None, read=0, status="planned", probed=0):
    est = {"speech": {"est": speech, "se": 0.0}, "music": {"est": music, "se": 0.0}, "silence": {"est": 0.0, "se": 0.0}, "decoded": {"est": hours, "se": 0.0},
           "languages": {code: {"est": h, "se": 0.0} for code, h in (langs or {}).items()}}
    return {"folder": name, "files": files, "bytes": size, "kinds": {kind: files}, "hours": {"est": hours, "se": 0.0, "probed_files": probed, "seconds_per_mb": rate},
            "sample": {"target": read, "read": read, "resolved": read, "status": status}, "estimates": est}


def _outcomes():
    """One readable bucket with an audio and a video donor; one refused bucket with an audio and a video folder of equal bytes."""
    readable = {"label": "readable-bucket", "content": {"access": "readable", "media_audio_objects": 100, "media_video_objects": 100, "folders": [
        _folder("podcasts", 100, 100 * 10_000_000, "audio", rate=36.0, hours=10_000.0, speech=8_000.0, music=2_000.0, langs={"swa": 5_000.0, "kik": 3_000.0}, read=30, status="sampled", probed=100),
        _folder("clips", 100, 100 * 10_000_000, "video", rate=9.0, hours=2_500.0, speech=500.0, music=2_000.0, langs={"swa": 500.0}, read=30, status="sampled", probed=100)]}}
    denied = {"label": "refused-bucket", "content": {"access": "denied", "media_audio_objects": 1000, "media_video_objects": 1000, "folders": [
        _folder("radio-backup · audio", 1000, 1000 * 10_000_000, "audio"), _folder("raw-footage · video", 1000, 1000 * 10_000_000, "video")]}}
    return {"obs": {"result_receipt": "synthetic_result.json", "observed_at": "2026-10-03T00:00:00Z", "sources": [readable, denied]}}


def test_refused_folders_borrow_the_same_kind_donor_and_scale_by_bytes():
    estate_forecast._CACHE.clear()
    fc = estate_forecast.forecast(_outcomes(), simulations=400)
    assert fc["strata"] == 4 and fc["donors"]["strata"] == 2
    denied = fc["by_basis"]["forecast_denied"]
    # audio folder: 10,000 MB × 36 s/MB = 100 h; video folder: 10,000 MB × 9 s/MB = 25 h — a single donor per kind leaves no spread.
    assert denied["hours"]["est"] == pytest.approx(125.0, rel=1e-6) and denied["hours"]["lo"] == denied["hours"]["hi"] == denied["hours"]["est"]
    assert denied["speech"]["est"] == pytest.approx(100 * 0.8 + 25 * 0.2, rel=1e-6)
    assert denied["languages"]["swa"]["est"] == pytest.approx(80 * (5_000 / 8_000) + 5 * 1.0, rel=1e-6)
    measured = fc["by_basis"]["measured"]
    assert measured["hours"]["est"] == pytest.approx(12_500.0) and fc["estate"]["hours"]["est"] == pytest.approx(12_625.0, rel=1e-6)
    assert fc["measured_share_of_hours"] == pytest.approx(12_500 / 12_625, abs=1e-4)
    assert fc["sources"][0]["label"] == "readable-bucket" and fc["sources"][0]["basis"] == "measured"
    assert fc["sources"][1]["label"] == "refused-bucket" and fc["sources"][1]["basis"] == "forecast"
    assert {f["basis"] for f in fc["folders"]} == {"measured", "forecast_denied"}
    assert all(f["donor"] for f in fc["folders"] if f["basis"] == "forecast_denied")


def test_measured_uncertainty_and_two_donors_give_a_real_interval_and_the_seed_makes_it_reproducible():
    estate_forecast._CACHE.clear()
    outcomes = _outcomes()
    folders = outcomes["obs"]["sources"][0]["content"]["folders"]
    folders.append(_folder("news", 100, 100 * 10_000_000, "audio", rate=72.0, hours=20_000.0, speech=18_000.0, music=1_000.0, langs={"luo": 9_000.0}, read=40, status="sampled", probed=100))
    folders[0]["hours"]["se"] = 300.0
    folders[0]["estimates"]["speech"]["se"] = 400.0
    first = estate_forecast.forecast(copy.deepcopy(outcomes), simulations=600)
    estate_forecast._CACHE.clear()
    second = estate_forecast.forecast(copy.deepcopy(outcomes), simulations=600)
    assert first == second
    denied = first["by_basis"]["forecast_denied"]
    assert denied["hours"]["lo"] < denied["hours"]["hi"] and denied["hours"]["lo"] <= denied["hours"]["est"] <= denied["hours"]["hi"]
    assert 100 <= denied["hours"]["est"] - 25 <= 200  # the audio folder sits between its two donors' rates (36 and 72 s/MB)
    measured = first["by_basis"]["measured"]
    assert measured["hours"]["lo"] < measured["hours"]["est"] < measured["hours"]["hi"]
    assert "luo" in first["estate"]["languages"]


def test_no_donor_means_no_forecast():
    estate_forecast._CACHE.clear()
    outcomes = _outcomes()
    outcomes["obs"]["sources"] = outcomes["obs"]["sources"][1:]
    assert estate_forecast.forecast(outcomes) is None


# ----------------------------------------------------------------------------- real retained receipts

def _real_outcomes():
    from services.census_autonomy import estate_intelligence_report as eir
    outcomes = {k: eir._latest_store_outcome(sid, "RMS") for k, sid in (("obs", "rms_obs"), ("nas", "rms_nas"))}
    if not any(outcomes.values()):
        pytest.skip("no retained store receipts in this environment")
    return outcomes


def test_real_receipts_forecast_is_consistent():
    estate_forecast._CACHE.clear()
    fc = estate_forecast.forecast(_real_outcomes())
    assert fc and fc["donors"]["strata"] > 0
    est = fc["estate"]
    assert est["hours"]["lo"] <= est["hours"]["est"] <= est["hours"]["hi"]
    assert est["speech"]["est"] + est["music"]["est"] <= est["hours"]["hi"] * 1.05
    assert sum(v["hours"]["est"] for v in fc["by_basis"].values()) == pytest.approx(est["hours"]["est"], rel=0.05)
    assert sum(v["files"] for v in fc["by_basis"].values()) == est["files"] == sum(s["files"] for s in fc["sources"])
    assert fc["by_basis"]["measured"]["hours"]["est"] < est["hours"]["est"]
    assert 0 < fc["measured_share_of_hours"] < 1
    for s in fc["sources"]:
        assert s["hours"]["lo"] <= s["hours"]["est"] <= s["hours"]["hi"]
        assert s["basis"] in ("measured", "forecast", "mixed")
    denied = [s for s in fc["sources"] if s["access"] == "denied"]
    assert denied and all(s["basis"] == "forecast" and s["hours"]["est"] > 0 for s in denied)
    assert all(f["hours"]["est"] >= 0 for f in fc["folders"]) and fc["folders"] == sorted(fc["folders"], key=lambda f: -f["hours"]["est"])


def test_store_estate_exposes_the_forecast():
    from services.census_autonomy import estate_intelligence_report as eir
    stores = eir.store_estate("RMS")
    if not stores.get("content_total"):
        pytest.skip("no content census banked")
    fc = stores["content_forecast"]
    assert fc["estate"]["hours"]["est"] >= stores["content_total"]["hours_held"]["est"]


# ----------------------------------------------------------------------------- the producer leads with the forecast

def test_estate_pack_leads_with_the_whole_estate_forecast():
    from services.census_autonomy import estate_intelligence_report as eir
    from services.transform_forms.doc_studio import author
    from services.transform_forms.doc_studio.producer_estate import build_brief, build_content, build_workbook
    from services.transform_forms.doc_studio.skill.scripts import validate
    report = eir.report_for("eij-1b359b3cbd2e", cached_only=True)
    if not report or not (report.get("stores") or {}).get("content_forecast"):
        pytest.skip("no banked estate report with a forecast")
    content = build_content(report, "RMS")
    validate.schema_check("content", content)
    facts, tables, claims = content["facts"], content["tables"], content["claims"]
    assert {"F130", "F131", "F132", "F133", "F134"} <= set(facts) and facts["F130"]["unit"] == "hours" and facts["F130"]["class"] == "estimated"
    assert "95 % forecast interval" in facts["F130"]["measurement_scope"]
    assert {"T047", "T048", "T049", "T050"} <= set(tables) and {"S030", "S031", "S032"} <= set(content["series"])
    assert tables["T047"]["columns"][6] == "Hours (95 %)" and len(tables["T047"]["deck_columns"]) <= 7
    assert tables["T013"]["rows"][0][0] == "D0" and "forecast" in tables["T013"]["rows"][0][1]
    assert "R11" in content["receipts"] and "Monte Carlo" in content["receipts"]["R11"]["resolves_to"]
    story = content["story"]
    assert len(story) == 6 and story[0]["answers_with"][0] == "F130" and "T047" in story[0]["tables"]
    assert story[-1]["tables"][0] == "T013"
    assert any("whole estate" in c["text"].lower() for c in claims.values())
    brief = build_brief(content, "RMS", "2026-10-03")
    assert "Lead with answers" in brief["constraints"]["report_scope"]
    plan = author.plan(content, brief)
    slots = [s["slot"] for s in plan["slots"]]
    assert plan["slots"][0]["needs"][0] == "F130"
    assert slots.index("glossary1") > slots.index("risks") > slots.index("chapter6")
    assert slots.count("table_T047_2") == 1 and "table_T046_2" not in slots  # secondary tables take one deck page
    assert any(g["term"] == "Whole-estate forecast" for g in content["glossary"])
    workbook = build_workbook(content, brief, {"verdict_id": "V-test"}, "seed", "2026-10-03T00:00:00Z", "voice")
    assert {s["name"] for s in workbook["sheets"]} >= {"Estate forecast by store", "Forecast by basis", "Forecast by folder", "Forecast donors"}
    assert not author._resolvable("O1", content) and not author._resolvable("S030", content) and author._resolvable("F130", content)
