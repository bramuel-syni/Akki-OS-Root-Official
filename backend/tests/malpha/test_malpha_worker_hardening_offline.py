"""Mα worker hardening offline tests: evidence projection, policy gates, intake v2 and dispatch validation."""

import asyncio
import base64
import io
import json
import math
import os
import tarfile
import tempfile
import zipfile
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from dotenv import load_dotenv

load_dotenv("/app/backend/.env")

import sys

sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")

from services.training_lab import malpha_learning as ml  # noqa: E402
from services.training_lab import malpha_internet_worker as miw  # noqa: E402
from services.training_lab import malpha_worker as mw  # noqa: E402
from services.training_lab import malpha_worker_policy as policy  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402

def _fake_stage(monkeypatch):
    """WP-A5 offline: the Shield stage is faked at its seam — the artifact carries the caller's items verbatim; `_payload` merges the JSON items back for assertions."""
    from services.synisense.shield import stage as st

    async def fake(*, question, data=None, tenant_id, purpose, actor, custody_class='tenant_estate', system_message=None, objective_ref=None, session_id=None, retain=True):
        return st.SafeArtifact(artifact_id='sa-fake', tenant_id=tenant_id, purpose=purpose, custody_class=custody_class, safe_items=[question] + ([data] if data else []), safe_system=system_message,
                               objective_ref=objective_ref, receipt={}, protected_digest='', created_at='2026-10-05T00:00:00Z', seal='fake')
    monkeypatch.setattr(st, 'stage', fake)


def _payload(kwargs):
    out = {}
    for item in kwargs['safe_artifact'].safe_items: out.update(json.loads(item))
    return out



def test_aggregate_evidence_never_exports_raw_transcripts_paths_or_vectors():
    jobs = [
        {
            "lane": "story_voice",
            "status": "completed",
            "iteration": 4,
            "result": {
                "steps": 320,
                "recipe": {"secret": "do-not-export"},
                "raw_transcript": "PRIVATE-LINE",
                "speaker_vectors": [[0.1, 0.2]],
                "path": "/mnt/private/session.wav",
                "dev": {
                    "mentions": {
                        "kik": {"precision": 0.9, "recall": 0.8},
                        "kam": {"precision": float("nan"), "recall": 0.7},
                        "swa": {"precision": float("inf"), "recall": 0.6},
                    },
                    "words": {"kik": {"wer": 0.2}, "kam": {"wer": 0.3}, "swa": {"wer": 0.4}},
                    "per_language": {
                        "kik": {"dev_perplexity": 12.1, "base_perplexity": 13.0, "language_fidelity_rate": 1.0, "behaviour": {"overall_similarity": 0.93}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.22}},
                        "kam": {"dev_perplexity": None, "base_perplexity": 14.0, "language_fidelity_rate": 0.8, "behaviour": {"overall_similarity": 0.91}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.21}},
                        "swa": {"dev_perplexity": 15.2, "base_perplexity": 15.9, "language_fidelity_rate": 0.7, "behaviour": {"overall_similarity": 0.89}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.39}},
                    },
                },
            },
        }
    ]

    evidence = ml.aggregate_evidence(jobs)
    assert list(evidence) == ["story_voice-result-1"]
    row = evidence["story_voice-result-1"]
    assert set(row) == {"lane", "iteration", "steps", "languages"}
    assert row["languages"]["kam"]["precision"] is None
    assert row["languages"]["swa"]["precision"] is None
    dumped = json.dumps(evidence, sort_keys=True)
    assert "PRIVATE-LINE" not in dumped
    assert "speaker_vectors" not in dumped
    assert "/mnt/private" not in dumped
    assert "do-not-export" not in dumped


class _FakeCollection:
    def __init__(self):
        self.rows = {}

    def create_index(self, *_args, **_kwargs):
        return None

    def insert_one(self, row):
        self.rows[row["review_id"]] = dict(row)

    def find_one(self, query, _projection=None):
        return dict(self.rows[query["review_id"]]) if query["review_id"] in self.rows else None

    def update_one(self, query, update):
        row = self.rows[query["review_id"]]
        if "$set" in update:
            row.update(update["$set"])
        return SimpleNamespace(modified_count=1)


def test_reconstruct_binds_plan_review_purposes_and_allowed_refs(monkeypatch):
    calls = []
    collection = _FakeCollection()

    class _Resp:
        def __init__(self, text):
            self.text = text
            self.model_id = "m"
            self.receipt_id = "r"
            self.tokens_in = 1
            self.tokens_out = 1
            self.latency_ms = 1

    _fake_stage(monkeypatch)

    async def fake_invoke(**kwargs):
        calls.append(kwargs)
        payload = _payload(kwargs)
        assert kwargs["purpose"] in {"malpha.learning_plan", "malpha.learning_review"}
        assert set(payload["allowed_evidence_refs"]) >= {"listener-result-1", "design-listener"}
        if kwargs["purpose"] == "malpha.learning_plan":
            return _Resp(
                json.dumps(
                    {
                        "findings": ["f1"],
                        "experiments": [
                            {
                                "lane": "listener",
                                "hypothesis": "h",
                                "evidence_refs": ["listener-result-1", "design-listener"],
                                "change": "c",
                                "measurement": "m",
                                "failure_condition": "fc",
                            }
                        ],
                        "limitations": ["l"],
                    }
                )
            )
        return _Resp(json.dumps({"verdict": "revise", "findings": ["ok"], "required_changes": ["rc"]}))

    def fake_resolve(role):
        if role == "planner":
            return {"sdk_provider": "p1", "connection": "c1", "model": "m1", "role": "planner"}
        return {"sdk_provider": "p2", "connection": "c2", "model": "m2", "role": "reviewer"}

    monkeypatch.setattr("services.chokepoint.llm.invoke", fake_invoke)
    monkeypatch.setattr("services.chokepoint.model_roles.resolve", fake_resolve)
    monkeypatch.setattr(ml.store, "db", lambda: SimpleNamespace(malpha_learning_reviews=collection))
    monkeypatch.setattr(
        "services.training_lab.malpha.jobs",
        lambda **_q: [
            {
                "lane": "listener",
                "status": "completed",
                "iteration": 1,
                "result": {
                    "steps": 10,
                    "raw_transcript": "must-never-leak",
                    "dev": {
                        "mentions": {
                            "kik": {"precision": 0.9, "recall": 0.9},
                            "kam": {"precision": 0.9, "recall": 0.9},
                            "swa": {"precision": 0.9, "recall": 0.9},
                        },
                        "words": {"kik": {"wer": 0.1}, "kam": {"wer": 0.1}, "swa": {"wer": 0.1}},
                        "per_language": {
                            "kik": {"dev_perplexity": 1.0, "base_perplexity": 2.0, "language_fidelity_rate": 1.0, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                            "kam": {"dev_perplexity": 1.0, "base_perplexity": 2.0, "language_fidelity_rate": 1.0, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                            "swa": {"dev_perplexity": 1.0, "base_perplexity": 2.0, "language_fidelity_rate": 1.0, "behaviour": {"overall_similarity": 0.9}, "identity_gate": {"max_cosine_to_any_corpus_speaker": 0.1}},
                        },
                    },
                },
            }
        ],
    )
    monkeypatch.setattr("services.training_lab.malpha.COMMISSIONS", [])
    monkeypatch.setattr("services.training_lab.malpha.wpw.record_event", lambda *a, **k: None)

    result = asyncio.run(ml.reconstruct("tester"))
    assert result["status"] == "reviewed"
    assert [c["purpose"] for c in calls] == ["malpha.learning_plan", "malpha.learning_review"]
    assert all("must-never-leak" not in " ".join(c["safe_artifact"].safe_items) for c in calls)  # WP-A5: the prompt crosses inside the sealed artifact


def test_story_score_language_completeness_and_ranking_contract():
    missing = {"per_language": {"kik": {"language_fidelity_rate": 1.0, "dev_perplexity": 10}, "kam": {"language_fidelity_rate": 1.0, "dev_perplexity": 10}}}
    assert policy.story_score(missing) is None

    ev_a = {"per_language": {l: {"language_fidelity_rate": v, "dev_perplexity": p, "base_perplexity": 20.0} for l, v, p in (("kik", 1.0, 10.0), ("kam", 1.0, 9.0), ("swa", 0.8, 8.0))}}
    ev_b = {"per_language": {l: {"language_fidelity_rate": v, "dev_perplexity": p, "base_perplexity": 20.0} for l, v, p in (("kik", 1.0, 10.0), ("kam", 1.0, 9.0), ("swa", 0.9, 8.0))}}
    score_a = policy.story_score(ev_a)
    score_b = policy.story_score(ev_b)
    assert score_a is not None and score_b is not None
    assert score_b > score_a  # higher worst-language fidelity wins first
    assert score_b[0] == 1  # all perplexities below base


def test_rendered_identity_gate_failclosed_for_incomplete_nan_missing_and_threshold():
    assert policy.rendered_identity_gate([0.2, 0.3], prompts=3, rendered=2, comparators=10)["passes"] is False
    assert policy.rendered_identity_gate([0.2], prompts=1, rendered=1, comparators=0)["passes"] is False
    assert policy.rendered_identity_gate([float("nan")], prompts=1, rendered=1, comparators=2)["passes"] is False
    assert policy.rendered_identity_gate([0.4], prompts=1, rendered=1, comparators=2)["passes"] is False
    assert policy.rendered_identity_gate([0.39], prompts=1, rendered=1, comparators=2)["passes"] is True


def test_balanced_weights_equalises_language_mass():
    rows = [
        {"language": "kik"},
        {"language": "kik"},
        {"language": "kam"},
        {"language": "swa"},
        {"language": "swa"},
        {"language": "swa"},
    ]
    out = policy.balanced_weights(rows, [1, 2, 5, 1, 1, 2])
    totals = {l: sum(w for r, w in zip(rows, out) if r["language"] == l) for l in ("kik", "kam", "swa")}
    assert all(math.isclose(v, 1.0, rel_tol=1e-6) for v in totals.values())
    with pytest.raises(ValueError):
        policy.balanced_weights([{"language": "kik"}, {"language": "kam"}], [1, 1])


def test_source_rows_manifest_tar_train_only_and_safe_tar(monkeypatch, tmp_path):
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(
        "\n".join(
            [
                json.dumps({"split": "train", "shard": "ok.tar", "key": "a1", "text": "hello", "speaker_id": "s1"}),
                json.dumps({"split": "dev", "shard": "ok.tar", "key": "b2", "text": "skip", "speaker_id": "s2"}),
            ]
        )
    )
    tar_path = tmp_path / "ok.tar"
    payload = b"FLACBYTES"
    with tarfile.open(tar_path, "w") as tf:
        info = tarfile.TarInfo("a1.flac")
        info.size = len(payload)
        tf.addfile(info, io.BytesIO(payload))
        info2 = tarfile.TarInfo("b2.flac")
        info2.size = len(payload)
        tf.addfile(info2, io.BytesIO(payload))

    def fake_download(_repo, filename, repo_type=None, revision=None):  # noqa: ARG001
        if filename == "manifest.jsonl":
            return str(manifest)
        if filename == "shards/ok.tar":
            return str(tar_path)
        raise AssertionError(filename)

    monkeypatch.setattr("huggingface_hub.hf_hub_download", fake_download)
    rows = list(miw.source_rows({"repo": "x/y", "format": "manifest_tar"}, "rev1"))
    assert len(rows) == 1
    assert rows[0]["text"] == "hello"
    assert rows[0]["source_key"] == "a1"
    assert rows[0]["blob"] == payload

    bad_manifest = tmp_path / "manifest_bad.jsonl"
    bad_manifest.write_text(json.dumps({"split": "train", "shard": "../evil.tar", "key": "x", "text": "t"}))

    def bad_download(_repo, filename, repo_type=None, revision=None):  # noqa: ARG001
        return str(bad_manifest) if filename == "manifest.jsonl" else str(tar_path)

    monkeypatch.setattr("huggingface_hub.hf_hub_download", bad_download)
    with pytest.raises(ValueError, match="Unsafe shard name"):
        list(miw.source_rows({"repo": "x/y", "format": "manifest_tar"}, "rev2"))


def _minimal_intake_control(root):
    return {
        "aip_db_dir": str(root),
        "commission_id": "LISTEN-KIK-KAM-SWA",
        "languages": ["kik"],
        "datasets": [{"repo": "acme/corpus", "config": None, "language": "kik"}],
        "brand_lexicon": [{"brand": "Safaricom", "aliases": ["safaricom"]}],
        "max_hours_per_dataset": None,
    }


def _prepare_root(tmp_path):
    (tmp_path / "manifest.json").write_text("{}")
    return tmp_path


def test_ingest_refuses_licence_before_fetch(monkeypatch, tmp_path):
    root = _prepare_root(tmp_path)
    called = {"source_rows": False}

    monkeypatch.setattr(mw, "_hf_qualify", lambda repo, allow: (SimpleNamespace(card_data={"license": "cc-by-4.0"}, sha="r1"), "licence_not_admitted:cc-by-4.0"))
    monkeypatch.setattr(miw, "source_rows", lambda *a, **k: called.__setitem__("source_rows", True))
    monkeypatch.setattr(mw, "load_rows", lambda *a, **k: [])
    monkeypatch.setattr(mw, "brand_inventory", lambda *a, **k: None)
    monkeypatch.setattr(mw, "_write_rows_atomic", lambda *a, **k: None)
    monkeypatch.setattr(mw, "now", lambda: "2026-10-04T00:00:00Z")

    result = miw.ingest(_minimal_intake_control(root), SimpleNamespace(update=lambda **k: None))
    assert result["datasets"][0]["status"] == "refused"
    assert called["source_rows"] is False


def test_ingest_journal_reuse_is_idempotent(monkeypatch, tmp_path):
    root = _prepare_root(tmp_path)
    key = "acme/corpus:default"
    journal = root / ("intake-" + mw._sha(key)[:16] + ".json")
    journal.write_text(json.dumps({"revision": "rev-fixed", "cursor": 10, "exhausted": True, "skipped": {}, "result": {"repo": "acme/corpus", "config": None, "language": "kik", "status": "ingested", "rows": 12}}))

    monkeypatch.setattr(mw, "_hf_qualify", lambda repo, allow: (SimpleNamespace(card_data={"license": "cc-by-4.0"}, sha="newer"), None))
    monkeypatch.setattr(mw, "load_rows", lambda *a, **k: [])
    monkeypatch.setattr(mw, "brand_inventory", lambda *a, **k: None)
    monkeypatch.setattr(mw, "_write_rows_atomic", lambda *a, **k: None)
    monkeypatch.setattr(mw, "now", lambda: "2026-10-04T00:00:00Z")

    result = miw.ingest(_minimal_intake_control(root), SimpleNamespace(update=lambda **k: None))
    rec = result["datasets"][0]
    assert rec["reused"] is True
    assert rec["rows"] == 12


def test_ingest_partial_source_failure_and_heldout_rejection(monkeypatch, tmp_path):
    root = _prepare_root(tmp_path)
    state = SimpleNamespace(update=lambda **k: None)

    def fake_rows(_spec, _rev):
        yield {"text": "held line", "blob": b"A", "speaker": "sp1"}
        yield {"text": "kept line", "blob": b"B", "speaker": "sp2"}
        raise RuntimeError("upstream")

    def fake_load_rows(_root, _lang, with_text=False, dataset="radio", splits=None):  # noqa: ARG001
        if dataset == "internet":
            return []
        if splits is None:
            return [{"split": "dev", "text_sha256": mw._sha("held line")}]
        return []

    monkeypatch.setattr(miw, "source_rows", fake_rows)
    monkeypatch.setattr(mw, "_hf_qualify", lambda repo, allow: (SimpleNamespace(card_data={"license": "cc-by-4.0"}, sha="pin-rev"), None))
    monkeypatch.setattr(mw, "load_rows", fake_load_rows)
    monkeypatch.setattr(mw, "_decode_bytes", lambda blob, sr: np.ones(sr, dtype=np.float32))
    monkeypatch.setattr(mw, "spectrum_features", lambda y, sr, chars: {"duration_s": 1.0})
    monkeypatch.setattr(mw, "brand_inventory", lambda *a, **k: None)
    monkeypatch.setattr(mw, "_write_rows_atomic", lambda path, rows, key=None: path.write_text("\n".join(json.dumps(r) for r in rows)))
    monkeypatch.setattr(mw, "now", lambda: "2026-10-04T00:00:00Z")
    monkeypatch.setattr(miw.shutil, "disk_usage", lambda p: SimpleNamespace(total=10 * 1024**3, free=9 * 1024**3))

    result = miw.ingest(_minimal_intake_control(root), state)
    rec = result["datasets"][0]
    assert rec["status"] == "partial"
    assert rec["reason"].startswith("source_error:RuntimeError")
    assert rec["revision"] == "pin-rev"
    assert rec["rows_added_this_run"] == 1
    assert rec["skipped"]["heldout_text_overlap"] == 1

    saved = [json.loads(line) for line in (root / "segments_internet_kik.jsonl").read_text().splitlines() if line.strip()]
    assert len(saved) == 1
    assert saved[0]["source"]["row_index"] == 1
    assert saved[0]["source"]["revision"] == "pin-rev"


def test_ingest_disk_backpressure_not_reported_as_success(monkeypatch, tmp_path):
    root = _prepare_root(tmp_path)
    state = SimpleNamespace(update=lambda **k: None)

    monkeypatch.setattr(miw, "source_rows", lambda *_a, **_k: iter([{"text": "x", "blob": b"y", "speaker": "s"}]))
    monkeypatch.setattr(mw, "_hf_qualify", lambda repo, allow: (SimpleNamespace(card_data={"license": "cc-by-4.0"}, sha="rev"), None))
    monkeypatch.setattr(mw, "load_rows", lambda *a, **k: [])
    monkeypatch.setattr(mw, "_decode_bytes", lambda blob, sr: np.ones(sr, dtype=np.float32))
    monkeypatch.setattr(mw, "spectrum_features", lambda y, sr, chars: {"duration_s": 1.0})
    monkeypatch.setattr(mw, "brand_inventory", lambda *a, **k: None)
    monkeypatch.setattr(mw, "_write_rows_atomic", lambda *a, **k: None)
    monkeypatch.setattr(mw, "now", lambda: "2026-10-04T00:00:00Z")
    monkeypatch.setattr(miw.shutil, "disk_usage", lambda p: SimpleNamespace(total=10 * 1024**3, free=100))

    result = miw.ingest(_minimal_intake_control(root), state)
    rec = result["datasets"][0]
    assert rec["status"] == "partial"
    assert rec["stop_reason"] == "disk_backpressure"
    assert rec["exhausted"] is False


def test_m9_bundle_contains_malpha_modules_and_validation_rules():
    bundle_b64, _sha = m9_dispatch.build_bundle()
    raw = base64.b64decode(bundle_b64)
    with zipfile.ZipFile(io.BytesIO(raw), "r") as zf:
        names = set(zf.namelist())
    assert "services/training_lab/malpha_internet_worker.py" in names
    assert "services/training_lab/malpha_worker_policy.py" in names
    assert "services/training_lab/malpha_voice_worker.py" in names

    host = os.environ["M9_TRAINING_HOSTS"].split(",")[0].strip()
    common = {
        "commission_id": "LISTEN-KIK-KAM-SWA",
        "languages": ["kik", "kam", "swa"],
        "gpu_index": 0,
        "budget_mode": "uncapped_until_billing",
        "owner_order_ref": "owner",
        "seed": 1,
        "iteration": 0,
        "aip_db_dir": os.environ["LANGUAGE_COGNITION_REMOTE_ROOT"] + "/malpha/aip_db_v1",
        "brand_lexicon": [{"brand": "Safaricom", "aliases": ["safaricom"]}],
    }
    m9_dispatch.validate(
        "malpha_internet_corpus",
        {**common, "datasets": [{"repo": "google/fleurs", "config": "sw_ke", "language": "swa"}], "max_hours_per_dataset": None, "data_revision": 2},
        host,
    )
    with pytest.raises(ValueError, match="MALPHA_INTERNET_CORPUS_INVALID"):
        m9_dispatch.validate(
            "malpha_internet_corpus",
            {**common, "datasets": [{"repo": "bad repo", "language": "swa"}], "max_hours_per_dataset": None, "data_revision": 2},
            host,
        )
