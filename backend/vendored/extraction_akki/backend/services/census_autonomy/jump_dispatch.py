"""Jump-routed non-GPU census dispatch.

Some estate hosts (internal 10.10.x, and external hosts whose MySQL grants are
pinned to the estate's own egress IP) are NOT reachable from the pod directly.
The owner's estate guide provides a Jump Server that sits on the internal network
and carries the allow-listed egress. This dispatcher runs the aggregate-only
census read ON that admitted jump host over SSH (using its `mysql` client),
exactly the way remote_dispatch runs the worker on an admitted GPU host — the pod
still never opens the source connection itself.

Selected via AKKI_CENSUS_EXECUTION_MODE=non_gpu_jump. Jump credentials live in a
0600 custody file referenced by AKKI_CENSUS_JUMP_CONFIG (never in .env plaintext).
"""
import json
import os
import shlex
import time
from pathlib import Path

import paramiko

from services.census_autonomy.operational_validation import PROTOCOL
from services.census_autonomy import operational_store as store
from services.census_autonomy.estate_connector_registry import (
    resolve_connector, ConnectorResolutionError,
)

_AGG_SQL = ("SELECT COUNT(DISTINCT TABLE_SCHEMA), COUNT(*), "
            "COALESCE(SUM(TABLE_ROWS), 0) FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA NOT IN "
            "('mysql','information_schema','performance_schema','sys')")
_SCHEMA_SQL = ("SELECT GROUP_CONCAT(DISTINCT TABLE_SCHEMA) FROM information_schema.TABLES "
               "WHERE TABLE_SCHEMA NOT IN "
               "('mysql','information_schema','performance_schema','sys')")


def _jump_config():
    return json.loads(Path(os.environ["AKKI_CENSUS_JUMP_CONFIG"]).read_text())["jump"]


def _connect_jump(cfg, timeout):
    client = paramiko.SSHClient()
    known = os.environ["AKKI_CENSUS_JUMP_KNOWN_HOSTS"]
    client.load_host_keys(known)
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(cfg["jump_host"], int(cfg["jump_port"]), username=cfg["jump_user"],
                   password=cfg["jump_password"], look_for_keys=False, allow_agent=False,
                   timeout=timeout, auth_timeout=timeout, banner_timeout=timeout)
    return client


def _run(client, cmd, timeout):
    _in, out, err = client.exec_command(cmd, timeout=timeout)
    data = out.read().decode(errors="replace").strip()
    return data, err.read().decode(errors="replace").strip()


def _mysql_cmd(conn, sql, connect_timeout):
    pwd = shlex.quote(conn["password"])
    host = shlex.quote(str(conn["host"]))
    user = shlex.quote(conn["user"])
    port = shlex.quote(str(conn.get("port", 3306)))
    return (f"MYSQL_PWD={pwd} mysql --connect-timeout={connect_timeout} -h {host} "
            f"-P {port} -u {user} -N -B -e {shlex.quote(sql)} 2>&1")


def _blocked(run_id, tenant, source, reason_code):
    return {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
            "source_id": source, "execution_location": "control_plane",
            "observed_at": store.now(), "status": "blocked", "worker_receipt_id": None,
            "source_rows_returned": 0, "reason_code": reason_code}


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    import hashlib
    remaining = int(deadline - time.time())
    if remaining <= 4:
        return _blocked(run_id, tenant, source, "BUDGET_EXHAUSTED")
    try:
        connector_path, manifest = resolve_connector(run_id, tenant, source, lawful_hash)
    except ConnectorResolutionError as exc:
        _bank(run_id, source, {"stage": "connector", "reason_code": exc.reason_code})
        return _blocked(run_id, tenant, source, "AKKI_CONNECTOR_" + exc.reason_code)
    try:
        connections = json.loads(connector_path.read_text())["sources"][source]["connections"]
    finally:
        try:
            connector_path.unlink()
        except OSError:
            pass

    max_db = int(os.environ["CENSUS_MAX_DATABASES"])
    result = {"protocol": PROTOCOL, "census_run_id": run_id, "tenant_id": tenant,
              "source_id": source, "execution_location": "akki_host", "source_rows_returned": 0,
              "observed_at": store.now(), "status": "blocked"}
    details, dbs, tbls, rows, ok = [], 0, 0, 0, 0
    client = None
    try:
        cfg = _jump_config()
        client = _connect_jump(cfg, min(20, remaining))
        for index, conn in enumerate(connections):
            if time.time() >= deadline - 2:
                break
            fp = hashlib.sha256(str(conn["host"]).encode()).hexdigest()[:12]
            entry = {"index": index, "host_fingerprint": fp, "label": conn.get("label"), "status": "blocked"}
            try:
                agg, aerr = _run(client, _mysql_cmd(conn, _AGG_SQL, 8), min(30, int(deadline - time.time())))
                line = agg.splitlines()[-1] if agg else ""
                parts = line.split("\t")
                if len(parts) != 3 or not all(p.strip().lstrip("-").isdigit() for p in parts):
                    raise ValueError(agg.split(":", 1)[0][:40] if agg else "NO_OUTPUT")
                d, t, r = (int(p) for p in parts)
                if d > max_db:
                    raise ValueError("DATABASE_BOUND_EXCEEDED")
                sc, _ = _run(client, _mysql_cmd(conn, _SCHEMA_SQL, 8), min(20, int(deadline - time.time())))
                schemas = [s for s in (sc.splitlines()[-1].split(",") if sc else []) if s]
                dbs += d; tbls += t; rows += r; ok += 1
                entry.update(status="complete", database_count=d, table_count=t,
                             row_count_estimate=r, schemas=schemas)
            except Exception as exc:  # noqa: BLE001 per-host isolation
                entry["reason_code"] = str(exc)[:60] if isinstance(exc, ValueError) else type(exc).__name__
            details.append(entry)
        if ok:
            result.update(status="complete", database_count=dbs, table_count=tbls, row_count_estimate=rows)
        else:
            result["reason_code"] = "ALL_CONNECTIONS_UNAVAILABLE"
    except Exception as exc:  # noqa: BLE001
        result["reason_code"] = "AKKI_JUMP_" + type(exc).__name__
    finally:
        if client:
            client.close()
    result["worker_receipt_id"] = "cwr-" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    _bank(run_id, source, {"stage": "jump", "estate_manifest": manifest, "route": "jump_server",
                           "worker_status": result["status"], "connections_total": len(details),
                           "connections_read": ok, "connections": details})
    return result


def _bank(run_id, source, payload):
    path = store.cursor_dir() / f"transport-{run_id}-{source}.json"
    path.write_text(json.dumps({"census_run_id": run_id, "source_id": source, "at_utc": store.now(),
                                "execution_location": "non_gpu_jump", **payload}, indent=2))
