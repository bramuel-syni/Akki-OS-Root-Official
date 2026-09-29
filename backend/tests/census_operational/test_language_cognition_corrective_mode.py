"""Corrective train mode contract tests: strict params, host-only bundle, split safety, receipt integrity."""
import base64
import hashlib
import io
import json
import zipfile
from types import SimpleNamespace

import pytest

from services.audio_plane_v1 import language_cognition_dispatch as lc
from services.audio_plane_v1.corrective_data import corrective_assignments
from services.audio_plane_v1.corrective_training import validate


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


def _valid_params():
    return {
        "baseline_job_id": "lcj-f96c86a16312",
        "gpu_index": 0,
        "seed": 11,
        "epochs": 20,
        "batch_size": 256,
        "physical_batch_size": 64,
        "max_windows_per_file": 60,
        "parallelism": 24,
        "lr": 3e-4,
        "adversary_strength": 0.2,
        "noise_multiplier": 1.0,
        "max_grad_norm": 1.0,
        "delta": 1e-6,
        "smoke_steps": 0,
        "owner_order_ref": "OWNER_ORDER_AND_RECIPE.md",
    }


def test_train_corrective_validate_strict_schema_and_baseline_lock():
    validate(_valid_params())

    with pytest.raises(ValueError, match="CORRECTIVE_PARAMETERS_REQUIRED"):
        validate({**_valid_params(), "connector": {"unexpected": True}})

    with pytest.raises(ValueError, match="UNREVIEWED_BASELINE_REQUIRES_A_NEW_RECIPE"):
        validate({**_valid_params(), "baseline_job_id": "lcj-some-other-baseline"})


def test_train_corrective_bundle_contains_only_worker_and_corrective_code():
    encoded, digest = lc.build_bundle("train_corrective")
    raw = base64.b64decode(encoded)
    assert hashlib.sha256(raw).hexdigest() == digest

    names = set(zipfile.ZipFile(io.BytesIO(raw)).namelist())
    assert names == {
        "services/audio_plane_v1/language_cognition_worker.py",
        "services/audio_plane_v1/corrective_data.py",
        "services/audio_plane_v1/corrective_model.py",
        "services/audio_plane_v1/corrective_training.py",
        "services/__init__.py",
        "services/audio_plane_v1/__init__.py",
    }


def test_corrective_assignments_protects_archive_held_and_excludes_unknown_presenters():
    items = [
        ("kik", "kik:train_a", "folder"),
        ("kik", "kik:train_a", "folder"),
        ("kik", "kik:train_b", "folder"),
        ("kik", "kik:archive_x", "archive"),
        ("kik", "kik:held_x", "folder"),
        ("kik", "kik:unknown_x", "folder"),
    ]
    legacy = {
        "kik:train_a": "train",
        "kik:train_b": "train",
        "kik:held_x": "held",
        "kik:archive_x": "train",
    }

    split = corrective_assignments(items, legacy, seed=31)
    pairs = list(zip(items, split))

    assert [s for (row, s) in pairs if row[1] == "kik:archive_x"] == ["archive_test"]
    assert [s for (row, s) in pairs if row[1] == "kik:held_x"] == ["held"]
    assert [s for (row, s) in pairs if row[1] == "kik:unknown_x"] == ["excluded"]

    # Same presenter cannot straddle sets.
    train_a_splits = {s for (row, s) in pairs if row[1] == "kik:train_a"}
    assert len(train_a_splits) == 1

    # Dev (if selected) must come only from legacy train presenters.
    dev_presenters = {row[1] for (row, s) in pairs if s == "dev"}
    assert dev_presenters.issubset({"kik:train_a", "kik:train_b"})


def test_refresh_refuses_receipt_job_or_phase_tamper_and_never_banks_success(isolated, monkeypatch):
    job_id = "lcj-000000000111"
    job = {
        "job_id": job_id,
        "phase": "train_corrective",
        "host": "akki-vm-ii",
        "status": "running",
        "submitted_at": "2026-09-29T00:00:00Z",
        "started_at": "2026-09-29T00:00:01Z",
        "northena_run_id": "run-x",
        "northena_trace_id": "trc-x",
        "governing_artifact_ref": {"artifact_type": "objective_request", "artifact_id": "CP-AIP-LANGUAGE-COGNITION", "version": job_id},
        "lawful_basis_ref": "/tmp/admit.json",
        "remote": {"root": "/mnt/volume_dkgjrkx/akki-lc", "job_dir": f"/mnt/volume_dkgjrkx/akki-lc/jobs/{job_id}", "pid": 4242},
        "ledger_rows": [],
    }
    lc.save_job(job)

    receipt_body = {
        "protocol": "akki-language-cognition-v1",
        "job_id": "lcj-ffffffffffff",  # tampered id
        "phase": "train_baseline",      # tampered phase
        "status": "completed",
        "finished_at": "2026-09-29T00:10:00Z",
        "result": {"ok": True},
    }
    receipt_body["receipt_sha256"] = hashlib.sha256(json.dumps(receipt_body, sort_keys=True, default=str).encode()).hexdigest()
    stdout = "\n__RECEIPT__\n" + json.dumps(receipt_body) + "\n__LOG__\nworker tail\n__ALIVE__\nno\n"

    monkeypatch.setattr(
        "services.training_runner.ssh_seam.execute_remote_command",
        lambda host, cmd, purpose, timeout: SimpleNamespace(rc=0, stdout_redacted=stdout, stderr_redacted="", receipt_id="gpurcp-x"),
    )
    monkeypatch.setattr(lc, "_bank_run_certificate", lambda *_: pytest.fail("tampered receipt must not bank success certificate"))

    refreshed = lc.refresh(job_id)
    assert refreshed["status"] == "failed"
    assert refreshed["reason"] == "WORKER_RECEIPT_INTEGRITY_FAILED"
    assert refreshed["track4_run_receipt"]["status"] == "failed"
    assert "run_certificate" not in refreshed
