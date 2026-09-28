"""Isolated M1 contract checks for descriptor declaration and durable registry evidence flows."""

import json
import importlib
from pathlib import Path

import pytest


def _import_descriptor_contracts(allow_skip=False):
    try:
        return importlib.import_module("services.census_autonomy.descriptor_contracts")
    except Exception as exc:
        if allow_skip:
            pytest.skip(f"descriptor_contracts import failed: {exc}")
        raise


def _import_registry_durability(allow_skip=False):
    try:
        return importlib.import_module("services.census_autonomy.registry_durability")
    except Exception as exc:
        if allow_skip:
            pytest.skip(f"registry_durability import failed: {exc}")
        raise


def test_r00_descriptor_contracts_module_imports():
    """Descriptor contracts module should import without missing symbol failures."""
    _import_descriptor_contracts()


def test_r01_bind_existing_refuses_foreign_source(monkeypatch):
    """Descriptor bind is tenant-scoped and rejects undeclared source ids."""
    descriptor_contracts = _import_descriptor_contracts(allow_skip=True)
    monkeypatch.setattr(descriptor_contracts, "sources_for", lambda tenant: ["rms_obs"])
    with pytest.raises(ValueError, match="Source outside tenant scope"):
        descriptor_contracts.bind_existing("RMS", "rms_mysql", "RMS DB", "principal-1")


def test_r02_bind_existing_is_idempotent_when_evidence_exists(monkeypatch):
    """Existing descriptor evidence is reused and does not create duplicates."""
    descriptor_contracts = _import_descriptor_contracts(allow_skip=True)
    existing = {"kind": "source_descriptor", "source_group": "rms_mysql", "descriptor": {"source_id": "src_abc"}}
    monkeypatch.setattr(descriptor_contracts, "sources_for", lambda tenant: ["rms_mysql"])
    monkeypatch.setattr(descriptor_contracts, "collection", lambda: object())
    monkeypatch.setattr(descriptor_contracts, "evidence_rows", lambda tenant, kind: [existing])

    payload, created = descriptor_contracts.bind_existing("RMS", "rms_mysql", "Existing RMS", "principal-1")
    assert payload == existing
    assert created is False


def test_r03_bind_existing_creates_declared_only_descriptor(monkeypatch):
    """New descriptor is schema-valid and keeps admission status explicitly non-native."""
    descriptor_contracts = _import_descriptor_contracts(allow_skip=True)
    monkeypatch.setenv('CENSUS_DESCRIPTOR_PORTS', '{"rms_mysql":3306}')
    writes = []
    monkeypatch.setattr(descriptor_contracts, "sources_for", lambda tenant: ["rms_mysql"])
    monkeypatch.setattr(descriptor_contracts, "collection", lambda: object())
    monkeypatch.setattr(descriptor_contracts, "evidence_rows", lambda tenant, kind: [])
    monkeypatch.setattr(descriptor_contracts, "append_census_evidence", lambda asset_ref, tenant, evidence: writes.append((asset_ref, tenant, evidence)))

    payload, created = descriptor_contracts.bind_existing("RMS", "rms_mysql", "RMS MySQL", "principal-1")

    assert created is True
    assert payload["kind"] == "source_descriptor"
    assert payload["descriptor"]["status"] == "declared"
    assert "not inferred" in payload["admission_status"].lower()
    assert len(writes) == 1


def test_r04_restore_results_rejects_tampered_evidence(tmp_path, monkeypatch):
    """Durability restore validates evidence digest before reconstructing files."""
    registry_durability = _import_registry_durability(allow_skip=True)
    bad_doc = {
        "asset_ref": "isolated-tampered-result",
        "tenant_id": "RMS",
        "census_evidence": {
            "kind": "census_result",
            "filename": "result.json",
            "raw_json": '{"tenant_id":"RMS","census_run_id":"cr-1"}',
        },
        "evidence_sha256": "tampered",
    }

    class FakeCollection:
        def find(self, *_args, **_kwargs):
            return [bad_doc]

    monkeypatch.setattr(registry_durability, "collection", lambda: FakeCollection())
    monkeypatch.setattr(registry_durability.engine, "CENSUS_STATE_DIR", tmp_path)
    monkeypatch.setattr(registry_durability.engine, "RESULTS_SUBDIR", "results")

    with pytest.raises(ValueError, match="Durable census evidence mismatch"):
        registry_durability.restore_results("RMS")


def test_r05_restore_results_writes_missing_file(tmp_path, monkeypatch):
    """Restore recreates missing result json exactly from retained raw_json evidence."""
    registry_durability = _import_registry_durability(allow_skip=True)
    content = {"tenant_id": "RMS", "census_run_id": "cr-2", "status": "COMPLETE"}
    evidence = {"kind": "census_result", "filename": "retained.json", "raw_json": json.dumps(content)}

    import hashlib

    digest = hashlib.sha256(json.dumps(evidence, sort_keys=True, default=str).encode()).hexdigest()
    doc = {"asset_ref":"isolated-test-result", "tenant_id": "RMS", "census_evidence": evidence, "evidence_sha256": digest}

    class FakeCollection:
        def find(self, *_args, **_kwargs):
            return [doc]

    monkeypatch.setattr(registry_durability, "collection", lambda: FakeCollection())
    monkeypatch.setattr(registry_durability.engine, "CENSUS_STATE_DIR", tmp_path)
    monkeypatch.setattr(registry_durability.engine, "RESULTS_SUBDIR", "results")

    registry_durability.restore_results("RMS")
    restored = Path(tmp_path / "results" / "retained.json")
    assert restored.exists()
    assert json.loads(restored.read_text()) == content
