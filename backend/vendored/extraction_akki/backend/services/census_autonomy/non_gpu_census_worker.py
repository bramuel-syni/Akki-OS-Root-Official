"""Non-GPU census worker — the local-runtime counterpart to remote_worker.py.

This module is executed as a *separate process* (never imported into the API
request thread) exactly the way the GPU worker's remote_worker.py is shipped and
run on an admitted host: the dispatcher ships this source via
``python3 -c <code> <b64-control>``. It is the admitted non-GPU execution
authority — an Akki-owned worker that performs the source read outside the pod's
request path.

Contract parity with the GPU worker:
- Reads a host-local connector custody document via AKKI_CENSUS_CONNECTOR_FILE
  (operator-owned, mode 0600). Each source declares tenant_id,
  lawful_basis_sha256, driver and connections.
- Emits the SAME aggregate-only receipt shape validated by
  services.census_autonomy.operational_validation. No secrets, source rows,
  table names or schema names appear in the receipt printed to stdout.

Difference from the GPU worker (intentional, product requirement):
- The GPU worker is all-or-nothing across its connection set. A partially-ready
  estate (some hosts "NOT YET UHURU") would otherwise block the whole source.
  This worker isolates each connection: a per-connection failure is recorded in
  the custody-restricted detail file (AKKI_CENSUS_WORKER_DETAIL_FILE) and the
  source completes over the connections that are genuinely connected. Per-host
  schema detail stays in the restricted detail file, never in the receipt.
"""
import base64
import fcntl
import hashlib
import json
import os
import signal
import socket
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL = "akki-census-aggregate-v1"
_PERMITTED = {
    "HOST_IDENTITY_MISMATCH", "CONNECTOR_CUSTODY_UNCONFIGURED",
    "CONNECTOR_CUSTODY_PERMISSIONS", "SOURCE_ADMISSION_MISMATCH",
    "SOURCE_DRIVER_NOT_BOUND", "CONNECTOR_BOUND_EXCEEDED",
    "CONNECTOR_CUSTODY_INVALID", "DATABASE_BOUND_EXCEEDED",
    "ALL_CONNECTIONS_UNAVAILABLE",
}
_AGGREGATE_SQL = (
    "SELECT TABLE_SCHEMA, COUNT(*), COALESCE(SUM(TABLE_ROWS), 0) "
    "FROM information_schema.TABLES WHERE TABLE_SCHEMA NOT IN "
    "('mysql','information_schema','performance_schema','sys') "
    "GROUP BY TABLE_SCHEMA LIMIT %s"
)


def _expired(*_):
    raise TimeoutError("deadline")


def _read_one(config, max_databases):
    import pymysql
    if not all(k in config for k in ("host", "port", "user", "password")):
        raise ValueError("CONNECTOR_CUSTODY_INVALID")
    kwargs = {k: config[k] for k in ("host", "port", "user", "password")}
    if config.get("ssl"):
        kwargs["ssl"] = config["ssl"]
    with pymysql.connect(**kwargs, connect_timeout=6, read_timeout=20,
                         write_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("SET SESSION TRANSACTION READ ONLY")
            cur.execute(_AGGREGATE_SQL, (max_databases + 1,))
            metadata = cur.fetchall()
    if len(metadata) > max_databases:
        raise ValueError("DATABASE_BOUND_EXCEEDED")
    return metadata


def run(request):
    result = {"protocol": PROTOCOL, "census_run_id": request["census_run_id"],
              "tenant_id": request["tenant_id"], "source_id": request["source_id"],
              "execution_location": "akki_host", "source_rows_returned": 0,
              "observed_at": datetime.now(timezone.utc).isoformat(), "status": "blocked"}
    details = []
    try:
        if socket.gethostname() != request["hostname_expected"]:
            raise ValueError("HOST_IDENTITY_MISMATCH")
        if not os.environ.get("AKKI_CENSUS_CONNECTOR_FILE") or not os.environ.get("AKKI_CENSUS_STATE_DIR"):
            raise ValueError("CONNECTOR_CUSTODY_UNCONFIGURED")
        source_file = Path(os.environ["AKKI_CENSUS_CONNECTOR_FILE"])
        if source_file.is_symlink() or stat.S_IMODE(source_file.stat().st_mode) & 0o077:
            raise ValueError("CONNECTOR_CUSTODY_PERMISSIONS")
        source = json.loads(source_file.read_text())["sources"][request["source_id"]]
        if source.get("tenant_id") != request["tenant_id"] or source.get("lawful_basis_sha256") != request["lawful_basis_sha256"]:
            raise ValueError("SOURCE_ADMISSION_MISMATCH")
        if source.get("driver") != "mysql_metadata":
            raise ValueError("SOURCE_DRIVER_NOT_BOUND")
        connections = source.get("connections", [])
        if not 1 <= len(connections) <= request["max_connections"]:
            raise ValueError("CONNECTOR_BOUND_EXCEEDED")
        databases = tables = rows = succeeded = 0
        for index, config in enumerate(connections):
            fingerprint = hashlib.sha256(str(config.get("host", "")).encode()).hexdigest()[:12]
            entry = {"index": index, "host_fingerprint": fingerprint,
                     "label": config.get("label"), "status": "blocked"}
            try:
                metadata = _read_one(config, request["max_databases"])
                d = len(metadata)
                t = sum(int(r[1]) for r in metadata)
                r = sum(int(r[2]) for r in metadata)
                databases += d
                tables += t
                rows += r
                succeeded += 1
                entry.update(status="complete", database_count=d, table_count=t,
                             row_count_estimate=r, schemas=[m[0] for m in metadata])
            except Exception as exc:  # noqa: BLE001 per-connection isolation
                code = str(exc) if isinstance(exc, ValueError) and str(exc) in _PERMITTED else type(exc).__name__
                entry["reason_code"] = code
            details.append(entry)
        if succeeded == 0:
            raise ValueError("ALL_CONNECTIONS_UNAVAILABLE")
        result.update(status="complete", database_count=databases, table_count=tables,
                      row_count_estimate=rows)
    except Exception as exc:  # noqa: BLE001
        code = str(exc) if isinstance(exc, ValueError) and str(exc) in _PERMITTED else type(exc).__name__
        result["reason_code"] = code
    result["worker_receipt_id"] = "cwr-" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    detail_path = os.environ.get("AKKI_CENSUS_WORKER_DETAIL_FILE")
    if detail_path:
        try:
            manifest = {"census_run_id": request["census_run_id"], "source_id": request["source_id"],
                        "at_utc": result["observed_at"], "connections_total": len(details),
                        "connections_read": sum(1 for d in details if d["status"] == "complete"),
                        "connections": details}
            tmp = Path(detail_path).with_suffix(".detail.tmp")
            tmp.write_text(json.dumps(manifest, indent=2, sort_keys=True))
            os.chmod(tmp, 0o600)
            os.replace(tmp, detail_path)
        except OSError:
            pass
    return result


def main():
    request = json.loads(base64.b64decode(sys.argv[1]))
    signal.signal(signal.SIGALRM, _expired)
    signal.alarm(int(request["max_seconds"]))
    if not os.environ.get("AKKI_CENSUS_STATE_DIR"):
        print(json.dumps(run(request)))
        return
    name = hashlib.sha256(json.dumps([request["census_run_id"], request["tenant_id"], request["source_id"]]).encode()).hexdigest()
    root = Path(os.environ["AKKI_CENSUS_STATE_DIR"])
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = root / (name + ".json")
    with (root / (name + ".lock")).open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        if path.exists():
            result = json.loads(path.read_text())
        else:
            result = run(request)
            temp = path.with_suffix(".tmp")
            with temp.open("w") as output:
                json.dump(result, output, sort_keys=True)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temp, path)
        print(json.dumps(result))


if __name__ == "__main__":
    main()
