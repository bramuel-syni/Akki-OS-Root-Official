"""WPW Tier 2 on Mα runs (WPW-8, WPW-9, WPW-10, A4, A6) — SYNTHETIC run records, no GPU, no network, no Mongo. The fixtures are labelled synthetic
and are not model measurements. Checked: nine fixed sections in order; the six acceptance criteria named with numbers where instrumented and
"not instrumented" where not; every rendered figure resolves mechanically (A4) and an unresolvable receipt line is refused, never rendered;
a failed run and a target-missed run both draft with the refusal and its numbers (A6); the internal marker is present (WPW-10)."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "vendored" / "extraction_akki" / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
os.environ.setdefault("WPW_NOTEBOOK_DIR", "/tmp/wpw_tier2_malpha_test_notebook")

from services.wpw import tier1_notebook as nb  # noqa: E402
from services.wpw import tier2_malpha as t2  # noqa: E402
from services.wpw.tier2_report import ACCEPTANCE_CRITERIA_ORDER, INTERNAL_ONLY_MARKER, SECTION_SKELETON  # noqa: E402

CID = "SYNTH-LISTEN-TEST"
LANGS = ["kik", "kam", "swa"]


def _mentions(p, r, n=40):
    return {"segments": 300, "segments_with_mentions": n, "tp": 1, "fp": 0, "fn": 0, "precision": p, "recall": r, "f1": None, "false_positives_per_hour": 0.1, "hours_evaluated": 0.5, "abstained_segments": 3, "per_brand": {}}


def _completed_job(job_id, p, r):
    dev = {"words": {l: {"wer": 0.31, "cer": 0.12, "n": 300} for l in LANGS}, "mentions": {l: _mentions(p[l], r[l]) for l in LANGS}, "latency": {"real_time_factor": 0.21, "audio_seconds": 1800.0, "wall_seconds": 380.0}, "step": 6000}
    return {"job_id": job_id, "phase": "malpha_listener_train", "host": "akki-vm", "status": "completed", "code_sha256": "ab" * 32,
            "params": {"recipe": {"base": "openai/whisper-small", "lr": 1e-4, "max_steps": 6000}, "languages": LANGS, "gpu_index": 0, "budget_mode": "uncapped_until_billing", "seed": 7, "iteration": 1, "aip_db_dir": "/tmp/aip", "brand_lexicon": [{"brand": "X", "aliases": []}]},
            "remote_state": {"progress": {"elapsed_s": 3600}, "stages": {"data": {"train_segments": 100, "dev_segments": 30}}},
            "receipt": {"digest_verified": True, "result": {"dev": dev, "data": {"train_segments": 100, "dev_segments": 30, "train_hours": 1.2}, "steps": 6000, "history": [dev], "artefact": {"path": "/tmp/a.pt", "sha256": "cd" * 32, "bytes": 968 * 2 ** 20},
                                                             "compute": {"wall_seconds": 3600.0, "gpu_seconds": 3600.0, "gpu_hours": 1.0, "gpu_peak_gb": 20.1, "device": "SYNTHETIC H200"}, "sealed_admission_read": False}}}


def _failed_job(job_id):
    return {"job_id": job_id, "phase": "malpha_listener_train", "host": "akki-vm", "status": "failed", "reason": "AttributeError: synthetic fault", "code_sha256": "ab" * 32,
            "params": {"recipe": {"base": "openai/whisper-small"}, "languages": LANGS, "gpu_index": 0, "budget_mode": "uncapped_until_billing", "seed": 7, "iteration": 1, "aip_db_dir": "/tmp/aip"},
            "remote_state": {"progress": {}, "stages": {"data": {"train_segments": 100, "dev_segments": 30}}}, "receipt": {"status": "failed", "error": {"type": "AttributeError", "message": "synthetic fault"}}}


def _aip_job():
    return {"job_id": "m9j-aaaaaaaaaaaa", "phase": "malpha_aip_build", "host": "akki-vm", "status": "completed", "lane": "aip_build", "iteration": 0, "commission_id": CID,
            "result": {"segments": {l: {"train": {"segments": 100, "hours": 1.0}, "dev": {"segments": 30, "hours": 0.1}, "admission": {"segments": 20, "hours": 0.05}} for l in LANGS}},
            "receipt": {"result": {"segments": {l: {"train": {"segments": 100, "hours": 1.0}, "dev": {"segments": 30, "hours": 0.1}, "admission": {"segments": 20, "hours": 0.05}} for l in LANGS},
                                   "files": {l: {"files": 3, "read": 3} for l in LANGS}, "layers": ["content", "timing"], "feature_columns": ["f0_mean_hz"], "split_rule": "synthetic", "raw_media_exported": False}}}


def _wire(monkeypatch, jobs_on_disk, recs):
    from services.training_lab import malpha
    from services.training_runner import m9_dispatch
    monkeypatch.setattr(m9_dispatch, "load_job", lambda jid: jobs_on_disk.get(jid))
    monkeypatch.setattr(malpha, "job_detail", lambda jid: recs.get(jid))
    monkeypatch.setattr(malpha, "commission", lambda cid: {"commission_id": CID, "title": "Synthetic listener", "product": "synthetic product", "aip_dev_requalified": True, "evaluation_exposure": {}})
    monkeypatch.setattr(malpha, "jobs", lambda **q: [j for j in [_aip_job()] if all(j.get(k) == v for k, v in q.items())])
    nb.attach_to_run(CID)
    if not any(e["event_kind"] == "commissioning_reflection" for e in nb.list_entries(CID)):
        nb.record_event(CID, "commissioning_reflection", "observed", f"malpha://commission/{CID}", {"title": "Synthetic listener", "budget_mode": "uncapped_until_billing", "definition_sha256": "ff" * 32,
                                                                                                 "target_outcome": {"task": "synthetic task", "domain": "synthetic", "admission": {l: {"mention_precision": 0.9, "mention_recall": 0.9} for l in LANGS}, "gate_policy": "every language", "metric_contract_status": "synthetic"}})


def _rec(job, lane="listener", iteration=1, gpu_seconds=3600):
    return {"job_id": job["job_id"], "commission_id": CID, "lane": lane, "phase": job["phase"], "iteration": iteration, "host": "akki-vm", "gpu_index": 0, "params": job["params"], "status": job["status"], "reason": job.get("reason"),
            "gpu_seconds": gpu_seconds, "result": (job.get("receipt") or {}).get("result"), "code_sha256": job["code_sha256"]}


def test_nine_sections_six_criteria_and_internal_marker(monkeypatch):
    job = _completed_job("m9j-111111111111", {l: 0.95 for l in LANGS}, {l: 0.93 for l in LANGS})
    _wire(monkeypatch, {job["job_id"]: job}, {job["job_id"]: _rec(job)})
    report = t2.draft(job["job_id"])
    assert tuple(report["sections"]) == SECTION_SKELETON
    assert [c["name"] for c in report["criteria"]] == list(ACCEPTANCE_CRITERIA_ORDER)
    held = report["criteria"][0]
    assert held["pass"] is True and held["value"] == 0.93 and "0.93" in held["measured"]
    assert next(c for c in report["criteria"] if c["name"] == "refusal_rate_on_out_of_domain")["measured"].startswith("not instrumented")
    assert next(c for c in report["criteria"] if c["name"] == "adapter_size_mib")["value"] == 968.0
    assert report["metadata"]["settlement"] == "accepted" and report["metadata"]["internal_only"] is True
    assert report["body"].count(INTERNAL_ONLY_MARKER) == 2
    assert "SYNTHETIC H200" in report["sections"]["setup_and_reproducibility"]["body"]


def test_every_rendered_figure_resolves_and_unresolvable_is_refused(monkeypatch):
    job = _completed_job("m9j-222222222222", {l: 0.95 for l in LANGS}, {l: 0.93 for l in LANGS})
    del job["receipt"]["result"]["compute"]  # the cost figure must then point at the host progress, which is present
    job["remote_state"]["progress"] = {}  # ... and now that is absent too → the cost figure must refuse, not render
    _wire(monkeypatch, {job["job_id"]: job}, {job["job_id"]: _rec(job)})
    report = t2.draft(job["job_id"])
    for f in report["figures"]:
        assert t2.resolve_receipt_line(f["receipt_line"]) is not None, f
        assert f["evidence_class"] in ("measured", "estimated", "observed")
    refused = {f["figure_id"] for f in report["refused_figures"]}
    assert "criterion_cost_actual_vs_estimate" in refused
    assert "receipt did not resolve" in report["sections"]["results_on_held_out"]["body"]
    assert report["metadata"]["figures_total"] == len(report["figures"]) + len(report["refused_figures"])


def test_target_missed_run_is_refused_with_its_numbers(monkeypatch):
    job = _completed_job("m9j-333333333333", {"kik": 0.95, "kam": 0.61, "swa": 0.9}, {"kik": 0.92, "kam": 0.88, "swa": 0.9})
    _wire(monkeypatch, {job["job_id"]: job}, {job["job_id"]: _rec(job)})
    report = t2.draft(job["job_id"])
    assert report["metadata"]["settlement"] == "refused"
    assert "0.61" in report["metadata"]["refusal_reason"]
    assert "Admission bar not met" in report["sections"]["negative_results"]["body"] and "kam: P 0.61" in report["sections"]["results_on_held_out"]["body"]


def test_failed_run_drafts_with_refusal_and_measured_cost(monkeypatch):
    job = _failed_job("m9j-444444444444")
    _wire(monkeypatch, {job["job_id"]: job}, {job["job_id"]: _rec(job, gpu_seconds=0)})
    report = t2.draft(job["job_id"])
    assert report["metadata"]["settlement"] == "refused" and report["metadata"]["status"] == "failed"
    assert "synthetic fault" in report["sections"]["negative_results"]["body"]
    assert report["criteria"][0]["pass"] is False and "run ended failed" in report["criteria"][0]["measured"]
    assert "the record is silent" in report["body"]
    assert any(f["figure_id"] == "run_data" and f["evidence_class"] == "observed" for f in report["figures"])  # data stage observed on the host before the fault


def test_walk_and_unknown_receipt_scheme():
    assert t2._walk({"a": [{"b": 1}]}, "a.0.b") == 1
    assert t2._walk({"a": [{"b": 1}]}, "a.3.b") is None
    assert t2.resolve_receipt_line("ftp://nowhere") is None
