"""Tests for services.census_autonomy.auth_methods_receipts.run_once durability/safety gates."""

import json
import shutil
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest


def _load_receipts_module():
    import importlib

    return importlib.import_module("services.census_autonomy.auth_methods_receipts")


@pytest.fixture
def admitted_tmp_dir():
    """Module+feature under test: runner uses assessment_workspace-bounded directory only."""
    root = Path("/app/assessment_workspace") / "tmp_auth_methods_receipts_tests" / uuid.uuid4().hex
    root.mkdir(parents=True, exist_ok=False)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _set_valid_env(monkeypatch, diagnostic_dir: Path):
    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(diagnostic_dir))
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", "a" * 64)
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "8")


def _install_inventory(monkeypatch, module, hosts):
    monkeypatch.setattr(module.ssh_seam, "list_hosts", lambda: hosts)
    monkeypatch.setattr(
        module.ssh_seam,
        "get_host_config",
        lambda host: SimpleNamespace(name=host, host=f"10.0.0.{1 if host.endswith('i') else 2}", port=22, username="ubuntu"),
    )


def test_run_once_missing_or_invalid_env_refuses(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: required env and digest shape are mandatory."""
    m = _load_receipts_module()
    _install_inventory(monkeypatch, m, ["akki-vm-i"])

    monkeypatch.delenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", raising=False)
    monkeypatch.delenv("AKKI_RECOVERY_WORKBOOK_SHA256", raising=False)
    monkeypatch.delenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", raising=False)
    with pytest.raises(KeyError):
        m.run_once(lambda *_args, **_kwargs: {"ok": True})

    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(admitted_tmp_dir))
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", "not-a-digest")
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "8")
    with pytest.raises(ValueError) as exc:
        m.run_once(lambda *_args, **_kwargs: {"ok": True})
    assert str(exc.value) == "WORKBOOK_DIGEST_REQUIRED"


def test_run_once_rejects_outside_and_symlinked_outside_dirs(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: path admission rejects outside and symlink-to-outside targets."""
    m = _load_receipts_module()
    _install_inventory(monkeypatch, m, ["akki-vm-i"])

    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", "a" * 64)
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "8")

    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", "/tmp/outside-auth-methods")
    with pytest.raises(ValueError) as exc_outside:
        m.run_once(lambda *_args, **_kwargs: {"ok": True})
    assert str(exc_outside.value) == "DIAGNOSTIC_DIRECTORY_NOT_ADMITTED"

    outside = Path("/tmp") / f"auth-methods-{uuid.uuid4().hex}"
    outside.mkdir(parents=True, exist_ok=False)
    try:
        link_path = admitted_tmp_dir / "to_outside"
        link_path.symlink_to(outside, target_is_directory=True)
        monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(link_path))
        with pytest.raises(ValueError) as exc_symlink:
            m.run_once(lambda *_args, **_kwargs: {"ok": True})
        assert str(exc_symlink.value) == "DIAGNOSTIC_DIRECTORY_NOT_ADMITTED"
    finally:
        shutil.rmtree(outside, ignore_errors=True)


def test_run_once_enforces_host_count_and_unique_aliases(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: admitted host set is max-two and unique aliases only."""
    m = _load_receipts_module()
    _set_valid_env(monkeypatch, admitted_tmp_dir)

    _install_inventory(monkeypatch, m, ["h1", "h1"])
    with pytest.raises(ValueError) as exc_dup:
        m.run_once(lambda *_args, **_kwargs: {"ok": True})
    assert str(exc_dup.value) == "ADMITTED_HOST_SET_INVALID"

    _install_inventory(monkeypatch, m, ["h1", "h2", "h3"])
    with pytest.raises(ValueError) as exc_many:
        m.run_once(lambda *_args, **_kwargs: {"ok": True})
    assert str(exc_many.value) == "ADMITTED_HOST_SET_INVALID"


def test_run_once_requires_admitted_host_alias_pattern(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: host alias regex gate blocks unknown alias characters."""
    m = _load_receipts_module()
    _set_valid_env(monkeypatch, admitted_tmp_dir)
    _install_inventory(monkeypatch, m, ["invalid.host"])
    with pytest.raises(ValueError) as exc:
        m.run_once(lambda *_args, **_kwargs: {"ok": True})
    assert str(exc.value) == "ADMITTED_HOST_ALIAS_INVALID"


def test_run_once_writes_intent_before_diagnostic_and_names_are_digest_host(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: durable intent exists before callback; file names pin digest+host once."""
    m = _load_receipts_module()
    digest = "b" * 64
    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(admitted_tmp_dir))
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", digest)
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "5")
    _install_inventory(monkeypatch, m, ["akki-vm-i"])

    observed = {}

    def _diagnose(config, timeout):
        intent_name = f"auth-none-{digest}-{config.name}.intent.json"
        observed["intent_exists_pre_callback"] = (admitted_tmp_dir / intent_name).is_file()
        observed["timeout"] = timeout
        return {
            "host_alias": config.name,
            "pin_match": True,
            "allowed_methods": ["publickey"],
            "authenticated": False,
            "error_code": "AUTH_NONE_REJECTED",
        }

    rows = m.run_once(_diagnose)
    assert observed["intent_exists_pre_callback"] is True
    assert observed["timeout"] == 5.0
    assert len(rows) == 1
    assert rows[0]["workbook_sha256"] == digest
    assert rows[0]["intent_ref"] == f"auth-none-{digest}-akki-vm-i.intent.json"


def test_run_once_retry_replays_prior_receipt_without_new_diagnose_call(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: rerun returns existing receipt and performs zero new callback calls."""
    m = _load_receipts_module()
    _set_valid_env(monkeypatch, admitted_tmp_dir)
    _install_inventory(monkeypatch, m, ["akki-vm-i"])

    calls = {"n": 0}

    def _diagnose(config, timeout):
        calls["n"] += 1
        return {
            "host_alias": config.name,
            "pin_match": True,
            "allowed_methods": ["publickey"],
            "authenticated": False,
            "error_code": "AUTH_NONE_REJECTED",
        }

    first = m.run_once(_diagnose)
    second = m.run_once(_diagnose)
    assert calls["n"] == 1
    assert first == second


def test_run_once_preexisting_orphan_intent_consumes_attempt_without_callback(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: orphaned intent means consumed attempt and zero diagnostic callback."""
    m = _load_receipts_module()
    digest = "c" * 64
    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(admitted_tmp_dir))
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", digest)
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "8")
    _install_inventory(monkeypatch, m, ["akki-vm-i"])

    intent_path = admitted_tmp_dir / f"auth-none-{digest}-akki-vm-i.intent.json"
    intent_path.write_text(json.dumps({"operation": "pinned_auth_none_only"}), encoding="utf-8")

    called = {"value": False}

    def _diagnose(*_args, **_kwargs):
        called["value"] = True
        return {}

    rows = m.run_once(_diagnose)
    assert called["value"] is False
    assert rows == [{"host_alias": "akki-vm-i", "error_code": "ATTEMPT_ALREADY_CONSUMED"}]


def test_run_once_diagnostic_exception_consumes_intent_and_no_retry_for_same_host(monkeypatch, admitted_tmp_dir):
    """Module+feature under test: callback exception leaves durable intent; later run never retries that host."""
    m = _load_receipts_module()
    digest = "d" * 64
    monkeypatch.setenv("AKKI_RECOVERY_DIAGNOSTIC_DIR", str(admitted_tmp_dir))
    monkeypatch.setenv("AKKI_RECOVERY_WORKBOOK_SHA256", digest)
    monkeypatch.setenv("AKKI_RECOVERY_PROBE_TIMEOUT_SEC", "8")
    _install_inventory(monkeypatch, m, ["akki-vm-i", "akki-vm-ii"])

    calls = []

    def _diagnose(config, timeout):
        calls.append(config.name)
        if config.name == "akki-vm-i":
            raise RuntimeError("forced diagnostic boom")
        return {
            "host_alias": config.name,
            "pin_match": True,
            "allowed_methods": ["publickey"],
            "authenticated": False,
            "error_code": "AUTH_NONE_REJECTED",
        }

    with pytest.raises(RuntimeError):
        m.run_once(_diagnose)
    assert calls == ["akki-vm-i"]

    replay = m.run_once(_diagnose)
    assert calls == ["akki-vm-i", "akki-vm-ii"]
    consumed = [row for row in replay if row.get("error_code") == "ATTEMPT_ALREADY_CONSUMED"]
    assert consumed and consumed[0]["host_alias"] == "akki-vm-i"
