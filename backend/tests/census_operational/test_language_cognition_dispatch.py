"""Language-cognition control plane: worker bundle provenance, secret-free job records,
bounded status RPC parsing, Northena rows + Track-4 receipt on close; worker span rule."""
import hashlib
import io
import json
import zipfile
from types import SimpleNamespace

import pytest

from services.audio_plane_v1 import language_cognition_dispatch as lc
from services.audio_plane_v1 import language_cognition_worker as worker


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(lc, "_jobs_dir", lambda: tmp_path)
    monkeypatch.setenv("LANGUAGE_COGNITION_HOST", "akki-vm-ii")
    monkeypatch.setenv("LANGUAGE_COGNITION_REMOTE_ROOT", "/mnt/volume_dkgjrkx/akki-lc")
    ledger = []

    async def record(row):
        ledger.append(row)
    monkeypatch.setattr(lc, "ledger_record", record)
    return {"dir": tmp_path, "ledger": ledger}


def test_bundle_ships_only_reviewed_worker_code_with_hash():
    encoded, digest = lc.build_bundle()
    import base64
    raw = base64.b64decode(encoded)
    assert hashlib.sha256(raw).hexdigest() == digest
    names = zipfile.ZipFile(io.BytesIO(raw)).namelist()
    assert set(names) == {"services/audio_plane_v1/language_cognition_worker.py", "services/__init__.py", "services/audio_plane_v1/__init__.py"}
    assert "CODE_HASH_MISMATCH" in lc.BOOTSTRAP and "os.fork()" in lc.BOOTSTRAP and "os.setsid()" in lc.BOOTSTRAP


def test_job_record_never_carries_the_connector(isolated):
    job = {"job_id": "lcj-000000000001", "phase": "corpus_census", "params": {"bucket": "google-transcripts"}, "submitted_at": "t"}
    lc.save_job(job)
    text = (isolated["dir"] / "lcj-000000000001.json").read_text()
    assert "access_key" not in text and lc.load_job("lcj-000000000001")["phase"] == "corpus_census"
    assert [j["job_id"] for j in lc.list_jobs()] == ["lcj-000000000001"]


def _job(status="running"):
    return {"job_id": "lcj-000000000002", "phase": "register_bases", "host": "akki-vm-ii", "status": status, "submitted_at": "2026-09-29T00:00:00Z",
            "started_at": "2026-09-29T00:00:01Z", "northena_run_id": "run-x", "northena_trace_id": "trc-x",
            "governing_artifact_ref": {"artifact_type": "objective_request", "artifact_id": "CP-AIP-LANGUAGE-COGNITION", "version": "lcj-000000000002"},
            "lawful_basis_ref": "/tmp/admit.json", "remote": {"root": "/mnt/volume_dkgjrkx/akki-lc", "job_dir": "/mnt/volume_dkgjrkx/akki-lc/jobs/lcj-000000000002", "pid": 42},
            "ledger_rows": []}


def _receipt(status="completed", result=None):
    body = {"protocol": "akki-language-cognition-v1", "job_id": "lcj-000000000002", "phase": "register_bases", "status": status,
            "finished_at": "2026-09-29T00:10:00Z", "result": result or {"ok": True}}
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
    return {**body, "receipt_sha256": digest}


def test_refresh_parses_state_receipt_and_closes_with_track4_receipt(isolated, monkeypatch):
    lc.save_job(_job())
    state = {"phase": "register_bases", "status": "completed", "progress": {"x": 1}}
    stdout = json.dumps(state) + "\n__RECEIPT__\n" + json.dumps(_receipt()) + "\n__LOG__\nlast lines\n__ALIVE__\nno\n"
    monkeypatch.setattr("services.training_runner.ssh_seam.execute_remote_command",
                        lambda host, cmd, purpose, timeout: SimpleNamespace(rc=0, stdout_redacted=stdout, stderr_redacted="", receipt_id="gpurcp-1"))
    monkeypatch.setattr(lc, "_bank_base_registration", lambda result: {"banked": True})
    job = lc.refresh("lcj-000000000002")
    assert job["status"] == "completed" and job["receipt"]["digest_verified"] is True and job["process_alive"] is False
    assert job["remote_state"]["progress"] == {"x": 1} and job["worker_log_tail"] == "last lines"
    assert job["track4_run_receipt"]["job_kind"] == "training_runs" and job["track4_run_receipt"]["status"] == "completed"
    assert job["training_base_registration"] == {"banked": True}
    assert [(r.stage, r.decision) for r in isolated["ledger"]] == [("converge", "terminate_success")]
    # A closed job is not re-queried.
    monkeypatch.setattr("services.training_runner.ssh_seam.execute_remote_command", lambda *a, **k: pytest.fail("must not RPC a closed job"))
    assert lc.refresh("lcj-000000000002")["status"] == "completed"


def test_refresh_flags_tampered_receipt_and_dead_worker(isolated, monkeypatch):
    lc.save_job(_job())
    bad = _receipt(); bad["result"] = {"ok": False}
    stdout = "\n__RECEIPT__\n" + json.dumps(bad) + "\n__LOG__\n\n__ALIVE__\nno\n"
    monkeypatch.setattr("services.training_runner.ssh_seam.execute_remote_command",
                        lambda host, cmd, purpose, timeout: SimpleNamespace(rc=0, stdout_redacted=stdout, stderr_redacted="", receipt_id="r"))
    monkeypatch.setattr(lc, "_bank_base_registration", lambda result: {})
    assert lc.refresh("lcj-000000000002")["receipt"]["digest_verified"] is False
    lc.save_job(dict(_job(), job_id="lcj-000000000003", remote={"root": "/r", "job_dir": "/r/jobs/x", "pid": 1}))
    monkeypatch.setattr("services.training_runner.ssh_seam.execute_remote_command",
                        lambda host, cmd, purpose, timeout: SimpleNamespace(rc=0, stdout_redacted="\n__RECEIPT__\n\n__LOG__\n\n__ALIVE__\nno\n", stderr_redacted="", receipt_id="r"))
    gone = lc.refresh("lcj-000000000003")
    assert gone["status"] == "failed" and gone["track4_run_receipt"]["status"] == "failed"


def _train_result():
    return {"split": {"per_language": {"kik": {"meets_presenter_minimum_n": True}, "bxk": {"meets_presenter_minimum_n": False}}},
            "training": {"steps": 10, "elapsed_seconds": 5, "device": "cuda"},
            "held_out": {"per_language": {"kik": {"accuracy": 0.95, "abstention_rate": 0.1, "windows": 20}, "bxk": {"accuracy": None, "abstention_rate": None, "windows": 0}}},
            "archive_test": {"windows": 3}, "no_speaker_id_probe": {"measured": False, "reason": "x"},
            "span_rule": {"window_seconds": 2.0, "min_span_seconds": 0.5, "hysteresis_windows": 2},
            "artefact": {"sha256": "a" * 64, "training_manifest_sha256": "b" * 64, "moac": {"verdict": "NOT ADMISSIBLE — test"}}}


def test_train_baseline_close_banks_run_certificate_against_sealed_defaults(isolated, monkeypatch):
    lc.save_job(dict(_job(), phase="train_baseline"))
    receipt = _receipt(result=_train_result()); receipt["phase"] = "train_baseline"
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
    stdout = "\n__RECEIPT__\n" + json.dumps(receipt) + "\n__LOG__\n\n__ALIVE__\nno\n"
    monkeypatch.setattr("services.training_runner.ssh_seam.execute_remote_command",
                        lambda host, cmd, purpose, timeout: SimpleNamespace(rc=0, stdout_redacted=stdout, stderr_redacted="", receipt_id="r"))
    job = lc.refresh("lcj-000000000002")
    cert = job["run_certificate"]
    assert cert["sealed_contract_check"]["span_rule_matches_default"] is True
    assert cert["sealed_contract_check"]["languages_meeting_presenter_minimum"] == ["kik"]
    assert cert["per_stratum"] == {"kik": {"accuracy": 0.95, "abstention_rate": 0.1, "windows": 20, "meets_default": True}}
    assert cert["final_model"] is False and cert["verdict"].startswith("NOT ADMISSIBLE")
    assert (isolated["dir"] / "run_certificate_lcj-000000000002.json").exists()
    assert "speaker_linkage" in lc.PHASES


def test_submit_refuses_unknown_phase_and_pod_refs(isolated):
    with pytest.raises(ValueError):
        lc.submit("nope", {}, "p1", "/tmp/admit.json")
    sealed = lc._sealed_language_cognition()
    with pytest.raises(sealed.PodAsDataPathRefused):
        sealed.commission_language_cognition_training_run(has_code_switched_material=True, speaker_disjoint_split_ref="/app/x",
                                                          base_registration_ref="h://b", moac_contract_ref="m", corpus_assembly_ref="h://c")
    with pytest.raises(sealed.CleanMonolingualOnlyRefused):
        sealed.commission_language_cognition_training_run(has_code_switched_material=False, speaker_disjoint_split_ref="h://s",
                                                          base_registration_ref="h://b", moac_contract_ref="m", corpus_assembly_ref="h://c")


def test_span_rule_is_deterministic_with_hysteresis_and_min_span():
    seq = [(0.0, "kik", 0.9), (2.0, "kik", 0.9), (4.0, "swa", 0.7), (6.0, "kik", 0.9), (8.0, "kik", 0.9),
           (10.0, "luo", 0.8), (12.0, "luo", 0.8), (14.0, "luo", 0.8)]
    spans = worker.spans(seq, min_span=1.0, hysteresis=2)
    assert spans == worker.spans(list(seq), min_span=1.0, hysteresis=2)
    assert [s["label"] for s in spans] == ["kik", "luo"]           # single-window swa flicker absorbed by hysteresis
    assert spans[0] == {"start": 0.0, "end": 12.0, "label": "kik"} and spans[1] == {"start": 10.0, "end": 16.0, "label": "luo"}
    short = worker.spans([(0.0, "kik", 0.9)], min_span=3.0, hysteresis=2)
    assert short[0]["label"] == "unmeasured"                       # below the minimum span is unmeasured, never labelled


def test_corpus_census_measures_pairing_and_skips_directory_markers(monkeypatch, tmp_path):
    keys = [("datasets/", 0), ("datasets/kik/", 0), ("datasets/kik/audio/a1.wav", 10), ("datasets/kik/audio/a2.mp3", 20),
            ("datasets/kik/transcript/a1.txt", 1), ("datasets/swa/audio/b1.wav", 30), ("datasets/swa/transcript/b1.txt", 2),
            ("datasets/swa/transcript/b9.txt", 2), ("datasets/readme.txt", 5)]

    class SDK:
        def list_objects_v2(self, **kw):
            return {"Contents": [{"Key": k, "Size": s} for k, s in keys], "IsTruncated": False}
    monkeypatch.setattr(worker, "_s3", lambda config: SDK())
    state = worker.State(tmp_path / "job")
    out = worker.corpus_census({"connector": {}, "root": str(tmp_path), "stage": False, "survey": False}, state)
    assert out["object_count"] == 7 and out["volume_bytes"] == 70
    kik = out["languages"]["kik"]
    assert kik["language"] == "Kikuyu" and kik["audio"]["objects"] == 2 and kik["audio"]["extensions"] == {".wav": 1, ".mp3": 1}
    assert kik["pairing"] == {"matched_pairs": 1, "audio_without_transcript": 1, "transcript_without_audio": 0}
    assert out["languages"]["swa"]["pairing"]["transcript_without_audio"] == 1
    assert out["languages"]["_unclassified"]["objects"] == 1
    assert out["target_five_coverage"] == {"Kikuyu": True, "Luo": False, "Sheng": False, "Swahili": True, "English": False}
    assert out["code_switched_spans_labelled"] == 0
