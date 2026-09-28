"""Offline tests for the non-GPU census worker, its credential resolver and its
dispatch authority. No live DB/network: MySQL reads are monkeypatched so the
suite is hermetic and deterministic.
"""
import base64
import json
import os
import socket
import stat
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parents[2] / 'vendored/extraction_akki/backend'))
from services.census_autonomy import estate_connector_registry as reg
from services.census_autonomy import non_gpu_census_worker as worker
from services.census_autonomy import non_gpu_dispatch as dispatch
from services.census_autonomy.operational_validation import validate_output


RMS_CSV = (
    "VIUSASA\n"
    "DATABASE NAME,HOST,USERNAME,PASSWORD,STATUS\n"
    "good_db,10.0.0.1,bramuel,secret-a,OK\n"
    "pending_db,10.0.0.2,bramuel,secret-b,NOT YET UHURU\n"
    "no_creds_db,10.0.0.9,,,OK\n"
    "NAS - ACESS\n"
    "10.0.0.3,Bramwel,nas-secret\n"
)


def _write_estate_csv(tmp_path):
    path = tmp_path / "rms.csv"
    path.write_text(RMS_CSV)
    os.chmod(path, 0o600)
    return path


def _custody_env(tmp_path, monkeypatch):
    monkeypatch.setenv("AKKI_RMS_ESTATE_CSV", str(_write_estate_csv(tmp_path)))
    monkeypatch.setenv("AKKI_CENSUS_CONNECTOR_DIR", str(tmp_path / "connectors"))
    monkeypatch.setenv("AKKI_CENSUS_WORKER_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("CENSUS_MAX_CONNECTIONS", "16")
    monkeypatch.setenv("CENSUS_MAX_DATABASES", "100")
    monkeypatch.setenv("AKKI_RMS_MYSQL_PORT", "3306")


# --------------------------------------------------------------------------
# estate_connector_registry
# --------------------------------------------------------------------------

def test_registry_builds_rms_mysql_connector_0600(tmp_path, monkeypatch):
    _custody_env(tmp_path, monkeypatch)
    path, manifest = reg.resolve_connector("cr-aaaaaaaaaaaa", "RMS", "rms_mysql", "hash123")
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    doc = json.loads(path.read_text())
    src = doc["sources"]["rms_mysql"]
    assert src["tenant_id"] == "RMS" and src["driver"] == "mysql_metadata"
    assert src["lawful_basis_sha256"] == "hash123"
    hosts = {c["host"] for c in src["connections"]}
    # Two rows carry the bramuel MySQL account; the no-creds row and the NAS
    # (Bramwel) row are excluded.
    assert hosts == {"10.0.0.1", "10.0.0.2"}
    assert all(c["user"] == "bramuel" and c["port"] == 3306 for c in src["connections"])
    assert {m["estate_status"] for m in manifest} == {"OK", "NOT YET UHURU"}


@pytest.mark.parametrize("tenant,source", [
    ("DIGICOW", "digicow_rds"), ("DIGICOW", "digicow_s3"),
    ("RMS", "rms_obs"), ("RMS", "rms_nas"),
])
def test_registry_refuses_sources_without_native_secret(tmp_path, monkeypatch, tenant, source):
    _custody_env(tmp_path, monkeypatch)
    with pytest.raises(reg.ConnectorResolutionError) as exc:
        reg.resolve_connector("cr-aaaaaaaaaaaa", tenant, source, "h")
    assert exc.value.reason_code == "NATIVE_SECRET_RESOLVER_UNAVAILABLE"


def test_registry_refuses_source_not_admitted_to_tenant(tmp_path, monkeypatch):
    _custody_env(tmp_path, monkeypatch)
    with pytest.raises(reg.ConnectorResolutionError) as exc:
        reg.resolve_connector("cr-aaaaaaaaaaaa", "DIGICOW", "rms_mysql", "h")
    assert exc.value.reason_code == "SOURCE_NOT_ADMITTED_TO_TENANT"


def test_registry_refuses_loose_custody_permissions(tmp_path, monkeypatch):
    _custody_env(tmp_path, monkeypatch)
    csv = Path(os.environ["AKKI_RMS_ESTATE_CSV"])
    os.chmod(csv, 0o644)
    with pytest.raises(reg.ConnectorResolutionError) as exc:
        reg.resolve_connector("cr-aaaaaaaaaaaa", "RMS", "rms_mysql", "h")
    assert exc.value.reason_code == "ESTATE_CUSTODY_PERMISSIONS"


# --------------------------------------------------------------------------
# non_gpu_census_worker
# --------------------------------------------------------------------------

def _connector_file(tmp_path, connections, tenant="RMS", lawful="h", driver="mysql_metadata"):
    path = tmp_path / "connector.json"
    path.write_text(json.dumps({"sources": {"rms_mysql": {
        "tenant_id": tenant, "lawful_basis_sha256": lawful, "driver": driver,
        "connections": connections}}}))
    os.chmod(path, 0o600)
    return path


def _control(tmp_path, **over):
    base = {"census_run_id": "cr-bbbbbbbbbbbb", "tenant_id": "RMS", "source_id": "rms_mysql",
            "lawful_basis_sha256": "h", "hostname_expected": socket.gethostname(),
            "max_seconds": 30, "max_databases": 100, "max_connections": 16}
    base.update(over)
    return base


def test_worker_completes_over_reachable_and_isolates_failures(tmp_path, monkeypatch):
    conns = [{"host": "good", "port": 3306, "user": "u", "password": "p", "label": "good"},
             {"host": "bad", "port": 3306, "user": "u", "password": "p", "label": "bad"}]
    monkeypatch.setenv("AKKI_CENSUS_CONNECTOR_FILE", str(_connector_file(tmp_path, conns)))
    monkeypatch.setenv("AKKI_CENSUS_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("AKKI_CENSUS_WORKER_DETAIL_FILE", str(tmp_path / "detail.json"))

    def fake_read(config, max_db):
        if config["host"] == "bad":
            raise RuntimeError("boom")
        return [("schema_x", 10, 1000), ("schema_y", 5, 500)]

    monkeypatch.setattr(worker, "_read_one", fake_read)
    result = worker.run(_control(tmp_path))
    assert result["status"] == "complete"
    assert result["database_count"] == 2 and result["table_count"] == 15
    assert result["row_count_estimate"] == 1500
    assert result["execution_location"] == "akki_host"
    validate_output(result, "cr-bbbbbbbbbbbb", "RMS", "rms_mysql")  # contract-compliant
    detail = json.loads((tmp_path / "detail.json").read_text())
    assert detail["connections_total"] == 2 and detail["connections_read"] == 1
    assert stat.S_IMODE((tmp_path / "detail.json").stat().st_mode) == 0o600


def test_worker_blocks_when_all_connections_fail(tmp_path, monkeypatch):
    conns = [{"host": "bad", "port": 3306, "user": "u", "password": "p", "label": "bad"}]
    monkeypatch.setenv("AKKI_CENSUS_CONNECTOR_FILE", str(_connector_file(tmp_path, conns)))
    monkeypatch.setenv("AKKI_CENSUS_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setattr(worker, "_read_one", lambda c, m: (_ for _ in ()).throw(RuntimeError("x")))
    result = worker.run(_control(tmp_path))
    assert result["status"] == "blocked"
    assert result["reason_code"] == "ALL_CONNECTIONS_UNAVAILABLE"


def test_worker_refuses_host_identity_mismatch(tmp_path, monkeypatch):
    monkeypatch.setenv("AKKI_CENSUS_CONNECTOR_FILE", str(_connector_file(tmp_path, [{"host": "h"}])))
    monkeypatch.setenv("AKKI_CENSUS_STATE_DIR", str(tmp_path / "state"))
    result = worker.run(_control(tmp_path, hostname_expected="not-this-host"))
    assert result["status"] == "blocked" and result["reason_code"] == "HOST_IDENTITY_MISMATCH"


def test_worker_refuses_wrong_driver(tmp_path, monkeypatch):
    path = _connector_file(tmp_path, [{"host": "h", "port": 1, "user": "u", "password": "p"}], driver="obs")
    monkeypatch.setenv("AKKI_CENSUS_CONNECTOR_FILE", str(path))
    monkeypatch.setenv("AKKI_CENSUS_STATE_DIR", str(tmp_path / "state"))
    result = worker.run(_control(tmp_path))
    assert result["reason_code"] == "SOURCE_DRIVER_NOT_BOUND"


# --------------------------------------------------------------------------
# non_gpu_dispatch
# --------------------------------------------------------------------------

def test_dispatch_blocks_on_connector_refusal(tmp_path, monkeypatch):
    _custody_env(tmp_path, monkeypatch)
    monkeypatch.setenv("CENSUS_AUTONOMY_STATE_DIR", str(tmp_path / "autonomy"))
    import time
    res = dispatch.execute_source("cr-cccccccccccc", "DIGICOW", "digicow_rds", "h", time.time() + 60)
    assert res["status"] == "blocked"
    assert res["reason_code"] == "AKKI_CONNECTOR_NATIVE_SECRET_RESOLVER_UNAVAILABLE"
    assert res["execution_location"] == "control_plane"


def test_dispatch_passes_worker_receipt_through(tmp_path, monkeypatch):
    _custody_env(tmp_path, monkeypatch)
    monkeypatch.setenv("CENSUS_AUTONOMY_STATE_DIR", str(tmp_path / "autonomy"))
    import time

    receipt = {"protocol": "akki-census-aggregate-v1", "census_run_id": "cr-dddddddddddd",
               "tenant_id": "RMS", "source_id": "rms_mysql", "execution_location": "akki_host",
               "source_rows_returned": 0, "observed_at": "2026-09-28T00:00:00+00:00",
               "status": "complete", "database_count": 2, "table_count": 119,
               "row_count_estimate": 2198643, "worker_receipt_id": "cwr-x"}

    class _Done:
        returncode = 0
        stdout = json.dumps(receipt).encode()

    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Done())
    res = dispatch.execute_source("cr-dddddddddddd", "RMS", "rms_mysql", "h", time.time() + 60)
    assert res["status"] == "complete" and res["table_count"] == 119
    validate_output(res, "cr-dddddddddddd", "RMS", "rms_mysql")
