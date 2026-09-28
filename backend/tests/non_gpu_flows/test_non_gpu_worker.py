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


# --------------------------------------------------------------------------
# jump_dispatch (SSH monkeypatched — no real network)
# --------------------------------------------------------------------------

from services.census_autonomy import jump_dispatch


def test_jump_dispatch_reads_over_jump_and_isolates_failures(tmp_path, monkeypatch):
    import time
    monkeypatch.setenv("CENSUS_MAX_DATABASES", "100")
    monkeypatch.setenv("CENSUS_AUTONOMY_STATE_DIR", str(tmp_path / "autonomy"))
    conns = [{"host": "good", "port": 3306, "user": "u", "password": "p", "label": "good"},
             {"host": "bad", "port": 3306, "user": "u", "password": "p", "label": "bad"}]
    cpath = _connector_file(tmp_path, conns)
    monkeypatch.setattr(jump_dispatch, "resolve_connector",
                        lambda r, t, s, h: (cpath, [{"label": "good"}, {"label": "bad"}]))
    monkeypatch.setattr(jump_dispatch, "_jump_config", lambda: {"jump_host": "x", "jump_user": "u", "jump_password": "p"})

    class _Client:
        def close(self): pass

    monkeypatch.setattr(jump_dispatch, "_connect_jump", lambda cfg, t: _Client())

    def fake_run(client, cmd, timeout):
        if "'good'" in cmd or " good " in cmd:
            return ("2\t119\t2198643" if "COUNT(DISTINCT" in cmd else "news_vault,razuna"), ""
        return ("ERROR 2003 (HY000): timeout", "") if "COUNT(DISTINCT" in cmd else ("", "")

    monkeypatch.setattr(jump_dispatch, "_run", fake_run)
    res = jump_dispatch.execute_source("cr-eeeeeeeeeeee", "RMS", "rms_mysql", "h", time.time() + 60)
    assert res["status"] == "complete"
    assert res["database_count"] == 2 and res["table_count"] == 119 and res["row_count_estimate"] == 2198643
    validate_output(res, "cr-eeeeeeeeeeee", "RMS", "rms_mysql")


def test_jump_dispatch_blocks_on_connector_refusal(tmp_path, monkeypatch):
    import time
    monkeypatch.setenv("CENSUS_MAX_DATABASES", "100")
    monkeypatch.setenv("CENSUS_AUTONOMY_STATE_DIR", str(tmp_path / "autonomy"))

    def _refuse(r, t, s, h):
        raise reg.ConnectorResolutionError("NATIVE_SECRET_RESOLVER_UNAVAILABLE")

    monkeypatch.setattr(jump_dispatch, "resolve_connector", _refuse)
    res = jump_dispatch.execute_source("cr-ffffffffffff", "DIGICOW", "digicow_rds", "h", time.time() + 60)
    assert res["status"] == "blocked"
    assert res["reason_code"] == "AKKI_CONNECTOR_NATIVE_SECRET_RESOLVER_UNAVAILABLE"


# --------------------------------------------------------------------------
# census_dq_producer (live producer off real census detail)
# --------------------------------------------------------------------------

from services.census_autonomy import census_dq_producer as dq


def test_dq_producer_banks_actionable_item_for_blocked_host(tmp_path, monkeypatch):
    # Fake transport detail manifest with one complete + one denied host.
    cursor = tmp_path / "dispatch"
    cursor.mkdir()
    monkeypatch.setattr(dq.store, "cursor_dir", lambda: cursor)
    (cursor / "transport-cr-111111111111-rms_mysql.json").write_text(json.dumps({
        "source_id": "rms_mysql",
        "connections": [
            {"label": "razuna", "status": "complete", "database_count": 2},
            {"label": "artists_app", "status": "blocked", "reason_code": "ERROR 1045 (28000)"},
        ]}))
    banked = []
    monkeypatch.setattr(dq, "bank_response_required_item",
                        lambda **kw: banked.append(kw) or f"rri-{len(banked)}")
    monkeypatch.setattr(dq, "_existing_signatures", lambda t: set())
    ids = dq.emit_from_run("cr-111111111111", "RMS")
    assert len(ids) == 1
    item = banked[0]
    assert item["refusal_code"] == "BLOCKED_SURFACE_UNREACHABLE"
    assert "Grant read" in item["reason_text"] and "artists_app" in item["reason_text"]
    assert item["tenant_id"] == "RMS"


def test_dq_producer_skips_fully_complete_run(tmp_path, monkeypatch):
    cursor = tmp_path / "dispatch"
    cursor.mkdir()
    monkeypatch.setattr(dq.store, "cursor_dir", lambda: cursor)
    (cursor / "transport-cr-222222222222-rms_mysql.json").write_text(json.dumps({
        "source_id": "rms_mysql",
        "connections": [{"label": "razuna", "status": "complete", "database_count": 2}]}))
    monkeypatch.setattr(dq, "bank_response_required_item", lambda **kw: "rri-x")
    monkeypatch.setattr(dq, "_existing_signatures", lambda t: set())
    assert dq.emit_from_run("cr-222222222222", "RMS") == []


# --------------------------------------------------------------------------
# rds_data_dispatch (DigiCow Aurora via RDS Data API — boto3 monkeypatched)
# --------------------------------------------------------------------------

from services.census_autonomy import rds_data_dispatch as rds
from services.census_autonomy import obs_dispatch as obs
from services.census_autonomy import census_router as router


def _estate_cfg(tmp_path, monkeypatch):
    cfg = {"digicow": {"provider": "aws_rds_data", "region": "eu-west-1",
                       "cluster_arn": "arn:c", "secret_arn": "arn:s",
                       "databases": ["digicow_live", "ndume"],
                       "aws_access_key_id": "AKIA", "aws_secret_access_key": "sk"},
           "obs": {"provider": "huawei_obs", "region": "af-south-1",
                   "endpoint": "https://obs.af-south-1.myhuaweicloud.com",
                   "access_key_id": "HPUA", "secret_access_key": "sk"}}
    path = tmp_path / "estate_access.json"
    path.write_text(json.dumps(cfg))
    monkeypatch.setenv("AKKI_ESTATE_ACCESS_CONFIG", str(path))
    monkeypatch.setenv("CENSUS_MAX_DATABASES", "100")


def test_rds_data_dispatch_completes_over_databases(tmp_path, monkeypatch):
    import time, boto3
    _estate_cfg(tmp_path, monkeypatch)
    monkeypatch.setattr(rds.store, "cursor_dir", lambda: tmp_path)

    class _Client:
        def execute_statement(self, **kw):
            n = {"digicow_live": (126, 5298351), "ndume": (113, 610205)}[kw["database"]]
            return {"records": [[{"longValue": n[0]}, {"longValue": n[1]}]]}

    monkeypatch.setattr(boto3, "client", lambda *a, **k: _Client())
    res = rds.execute_source("cr-777777777777", "DIGICOW", "digicow_rds", "h", time.time() + 60)
    assert res["status"] == "complete"
    assert res["database_count"] == 2 and res["table_count"] == 239 and res["row_count_estimate"] == 5908556
    validate_output(res, "cr-777777777777", "DIGICOW", "digicow_rds")


def test_rds_data_dispatch_blocks_when_api_fails(tmp_path, monkeypatch):
    import time, boto3
    _estate_cfg(tmp_path, monkeypatch)
    monkeypatch.setattr(rds.store, "cursor_dir", lambda: tmp_path)

    def _boom(*a, **k):
        raise RuntimeError("no aws")

    monkeypatch.setattr(boto3, "client", _boom)
    res = rds.execute_source("cr-888888888888", "DIGICOW", "digicow_rds", "h", time.time() + 60)
    assert res["status"] == "blocked" and res["reason_code"].startswith("AKKI_RDS_")


# --------------------------------------------------------------------------
# obs_dispatch (Huawei OBS inventory — boto3 monkeypatched)
# --------------------------------------------------------------------------

def test_obs_dispatch_inventories_buckets(tmp_path, monkeypatch):
    import time, boto3
    _estate_cfg(tmp_path, monkeypatch)
    monkeypatch.setattr(obs.store, "cursor_dir", lambda: tmp_path)

    class _S3:
        def list_buckets(self):
            return {"Buckets": [{"Name": f"b{i}"} for i in range(106)]}

    monkeypatch.setattr(boto3, "client", lambda *a, **k: _S3())
    res = obs.execute_source("cr-999999999999", "RMS", "rms_obs", "h", time.time() + 60)
    assert res["status"] == "complete" and res["database_count"] == 106
    assert res["table_count"] == 0 and res["row_count_estimate"] == 0
    validate_output(res, "cr-999999999999", "RMS", "rms_obs")


# --------------------------------------------------------------------------
# census_router
# --------------------------------------------------------------------------

@pytest.mark.parametrize("source,module_attr", [
    ("digicow_rds", "rds_data_dispatch"), ("rms_obs", "obs_dispatch"),
])
def test_router_routes_managed_sources(monkeypatch, source, module_attr):
    import services.census_autonomy as pkg
    target = getattr(__import__(f"services.census_autonomy.{module_attr}", fromlist=["x"]), "execute_source")
    calls = {}
    mod = __import__(f"services.census_autonomy.{module_attr}", fromlist=["x"])
    monkeypatch.setattr(mod, "execute_source",
                        lambda *a, **k: (calls.__setitem__("hit", a[2]), {"ok": True})[1])
    out = router.execute_source("cr-aaaaaaaaaaaa", "T", source, "h", 0)
    assert out == {"ok": True} and calls["hit"] == source


def test_router_rms_mysql_honours_mode(monkeypatch):
    monkeypatch.setenv("AKKI_CENSUS_EXECUTION_MODE", "non_gpu_jump")
    from services.census_autonomy import jump_dispatch
    monkeypatch.setattr(jump_dispatch, "execute_source", lambda *a, **k: {"routed": "jump"})
    assert router.execute_source("cr-bbbbbbbbbbbb", "RMS", "rms_mysql", "h", 0) == {"routed": "jump"}
