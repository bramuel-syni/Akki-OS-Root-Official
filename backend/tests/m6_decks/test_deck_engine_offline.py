"""M6.1 Deck Rendering Engine — DR-R13 gates, offline (no network, no model, temp store). Each test names its gate."""
import copy
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "vendored" / "extraction_akki" / "backend"))

from services.transform_forms.deck_engine import render as R  # noqa: E402
from services.transform_forms.deck_engine import service  # noqa: E402
from services.transform_forms.deck_engine.validate import DeckValidationError, lint, validate  # noqa: E402

KNOWN = {"rcp-000000000001": {"kind": "rcp", "status": "recorded", "verified": True}, "eij-aaaaaaaaaaaa": {"kind": "eij", "status": "completed", "verified": True}}


def resolver(ref):
    return KNOWN.get(ref)


def spec():
    return {
        "deck_id": "deck-test-1", "spec_version": "v1", "register": "R4",
        "meta": {"title": "Test estate deck", "audience_line": "Owner", "date": "2026-09-30", "rights_posture_ref": "census-only", "sample_deck": False},
        "selection_manifest": {"register_why": "commission close", "overrides": []},
        "slides": [
            {"type": "title", "title": "The estate holds 351 GiB across 20 databases."},
            {"type": "big_number", "title": "Most bytes sit in ten tables.", "plate": "P11",
             "figures": [{"value": 351.3, "unit": "GiB", "class": "measured", "receipt_refs": ["eij-aaaaaaaaaaaa"]}]},
            {"type": "table", "title": "Condition is measured, not assumed.", "plate": "P3",
             "data": {"columns": ["Condition", "Share"], "rows": [["Exact duplicates", "1.5%"], ["PII rows", {"value": None, "unmeasured": True, "caption": "not sampled"}]]},
             "receipt_refs": ["rcp-000000000001"]},
            {"type": "exhibit", "title": "Two databases carry most of the bytes.", "plate": "P4",
             "data": {"unit": "GiB", "series": [{"label": "a", "value": 120, "class": "measured"}, {"label": "b", "value": None, "unmeasured": True, "caption": "blocked", "class": "measured"}]},
             "receipt_refs": ["eij-aaaaaaaaaaaa"]},
        ],
        "coverage_and_limits": {"covered_basis_ref": "eij-aaaaaaaaaaaa", "limits": [{"reason": "blocked_source", "statement": "artists_app unreadable", "closing_condition": "GRANT"}]},
        "appendix": {"exhibit_index_auto": True, "extra_slides": []},
    }


@pytest.fixture(autouse=True)
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("AKKI_DECK_STORE_DIR", str(tmp_path / "decks"))
    yield tmp_path


def errors_of(bad):
    with pytest.raises(DeckValidationError) as exc:
        validate(bad, resolver)
    return {e["rule"] for e in exc.value.errors}, exc.value.errors


def test_gate_determinism_byte_identical():
    a = service.render_deck(spec(), "RMS", "p1", resolver=resolver)
    b = service.render_deck(spec(), "RMS", "p1", resolver=resolver)
    assert a["current_spec_hash"] == b["current_spec_hash"]
    assert b["versions"][0]["byte_identical_rerender"] is True
    assert b["economics"]["renders_total"] == 2 and b["economics"]["rerender_authoring_tokens"] == 0
    html = service.artifact_bytes("RMS", "deck-test-1", None, "html")
    assert html == R.render_html(validate(spec(), resolver)["spec"], validate(spec(), resolver)["plate_models"])
    assert b"Receipts:" in html and b"chip-measured" in html and b"Covered basis" in html and b"repeating-linear-gradient" in html


def test_gate_unreceipted_exhibit_refuses():
    bad = spec(); bad["slides"][2]["receipt_refs"] = ["rcp-does-not-exist"]
    rules, errs = errors_of(bad)
    assert "unreceipted_exhibit" in rules and any(e["slide_index"] == 2 for e in errs)
    bad2 = spec(); bad2["slides"][2]["receipt_refs"] = []
    assert "unreceipted_exhibit" in errors_of(bad2)[0]


def test_gate_missing_class_refuses():
    bad = spec(); del bad["slides"][1]["figures"][0]["class"]
    rules, errs = errors_of(bad)
    assert "missing_class" in rules and any(e["slide_index"] == 1 for e in errs)


def test_gate_no_silent_blank():
    bad = spec(); bad["slides"][2]["data"]["rows"][1][1] = None
    assert "no_silent_blank" in errors_of(bad)[0]
    bad2 = spec(); bad2["slides"][3]["data"]["series"][1] = {"label": "b", "value": None, "class": "measured"}
    assert "no_silent_blank" in errors_of(bad2)[0]


def test_gate_coverage_slide_required():
    bad = spec(); del bad["coverage_and_limits"]
    assert "coverage_slide_required" in errors_of(bad)[0]


def test_gate_style_unrepresentable():
    bad = spec(); bad["slides"][1]["color"] = "#ff0000"
    assert "style_unrepresentable" in errors_of(bad)[0]
    bad2 = spec(); bad2["slides"][3]["data"]["series"][0]["accent"] = True
    assert "style_unrepresentable" in errors_of(bad2)[0]
    bad3 = spec(); bad3["meta"]["font"] = "Comic Sans"
    assert "style_unrepresentable" in errors_of(bad3)[0]


def test_all_violations_enumerated_in_one_pass():
    bad = spec(); del bad["slides"][1]["figures"][0]["class"]; bad["slides"][1]["color"] = "x"; del bad["coverage_and_limits"]
    rules, errs = errors_of(bad)
    assert {"missing_class", "style_unrepresentable", "coverage_slide_required"} <= rules and len(errs) >= 3


def test_gate_register_purity_and_selection_recorded():
    bad = spec(); bad["selection_manifest"]["overrides"] = [{"field": "register", "value": "R1", "why": "owner pick"}]
    assert "register_purity" in errors_of(bad)[0]
    ok = spec(); ok["selection_manifest"]["overrides"] = [{"slide_index": 3, "field": "plate", "value": "P4", "why": "owner pick"}]
    rec = service.render_deck(ok, "RMS", "p1", resolver=resolver)
    assert b"override plate=P4" in service.artifact_bytes("RMS", "deck-test-1", rec["current_spec_hash"], "html")


def test_p11_estimated_is_demoted_mechanically():
    s = spec(); s["slides"][1]["figures"][0]["class"] = "estimated"
    rec = service.render_deck(s, "RMS", "p1", resolver=resolver)
    html = service.artifact_bytes("RMS", "deck-test-1", rec["current_spec_hash"], "html")
    assert b"big-number demoted" in html and b"Demoted: only a measured figure" in html


def test_sample_badge_and_v0_shell_not_renderable():
    s = spec(); s["meta"]["sample_deck"] = True
    rec = service.render_deck(s, "RMS", "p1", resolver=resolver)
    assert b"badge-sample" in service.artifact_bytes("RMS", "deck-test-1", rec["current_spec_hash"], "html")
    assert "spec_not_renderable" in errors_of({"deck_id": "x", "spec_version": "v0"})[0]


def test_lint_is_advisory_and_recorded():
    s = spec(); s["slides"][0]["title"] = "SUMMARY?"
    rec = service.render_deck(s, "RMS", "p1", resolver=resolver)
    assert any(w["rule"] == "title_sentence_form" for w in rec["lint"]) and rec["errors"] == []
    assert lint(validate(s, resolver)["spec"])


def test_determinism_breach_is_refused_not_overwritten(tmp_path):
    rec = service.render_deck(spec(), "RMS", "p1", resolver=resolver)
    path = Path(rec["versions"][0]["artifact"]["html"]["path"])
    path.write_bytes(path.read_bytes() + b"<!-- tampered -->")
    with pytest.raises(DeckValidationError) as exc:
        service.render_deck(spec(), "RMS", "p1", resolver=resolver)
    assert exc.value.errors[0]["rule"] == "determinism_breach"


def test_tenant_isolation_of_records():
    service.render_deck(spec(), "RMS", "p1", resolver=resolver)
    assert service.load("DIGICOW", "deck-test-1") is None and service.list_decks("DIGICOW") == []
    assert service.load("RMS", "deck-test-1")["deck_id"] == "deck-test-1"


@pytest.mark.skipif(not R.pdf_capability()["available"], reason="no headless browser on this host")
def test_gate_export_furniture_survives():
    rec = service.render_deck(spec(), "RMS", "p1", resolver=resolver, want_pdf=True)
    pdf = rec["versions"][0]["artifact"]["pdf"]
    assert pdf["exported"] is True, pdf
    assert pdf["check"]["checked"] and pdf["check"]["survives"], pdf["check"]
    assert service.artifact_bytes("RMS", "deck-test-1", None, "pdf")[:4] == b"%PDF"
