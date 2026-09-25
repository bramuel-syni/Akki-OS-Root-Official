"""Executed ONLY on an admitted Akki host, never imported to read data in the pod.

Host-local custody contract: AKKI_CENSUS_CONNECTOR_FILE and AKKI_CENSUS_STATE_DIR.
The connector document is operator-owned, mode 0600, with a sources dictionary.
Each source declares tenant_id, lawful_basis_sha256, driver, and connections.
No secrets, source rows, table names or schema names are emitted.
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


def _expired(*_):
    raise TimeoutError("deadline")


def run(request):
    result = {"protocol": "akki-census-aggregate-v1", "census_run_id": request["census_run_id"],
              "tenant_id": request["tenant_id"], "source_id": request["source_id"],
              "execution_location": "akki_host", "source_rows_returned": 0,
              "observed_at": datetime.now(timezone.utc).isoformat(), "status": "blocked"}
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
        import pymysql  # Only imported after remote custody and admission checks.
        databases = tables = rows = 0
        for config in connections:
            if not all(k in config for k in ("host", "port", "user", "password")):
                raise ValueError("CONNECTOR_CUSTODY_INVALID")
            kwargs = {k: config[k] for k in ("host", "port", "user", "password")}
            if config.get("ssl"):
                kwargs["ssl"] = config["ssl"]
            with pymysql.connect(**kwargs, connect_timeout=10, read_timeout=15, write_timeout=10) as conn:
                with conn.cursor() as cur:
                    cur.execute("SET SESSION TRANSACTION READ ONLY")
                    cur.execute("SELECT TABLE_SCHEMA, COUNT(*), COALESCE(SUM(TABLE_ROWS), 0) "
                                "FROM information_schema.TABLES WHERE TABLE_SCHEMA NOT IN "
                                "('mysql','information_schema','performance_schema','sys') "
                                "GROUP BY TABLE_SCHEMA LIMIT %s", (request["max_databases"] + 1,))
                    metadata = cur.fetchall()
                    if len(metadata) > request["max_databases"]:
                        raise ValueError("DATABASE_BOUND_EXCEEDED")
                    databases += len(metadata)
                    tables += sum(int(r[1]) for r in metadata)
                    rows += sum(int(r[2]) for r in metadata)
                    del metadata
        result.update(status="complete", database_count=databases, table_count=tables, row_count_estimate=rows)
    except Exception as exc:
        # Never stringify provider errors: these may include hosts, SQL or secrets.
        permitted = {"HOST_IDENTITY_MISMATCH", "CONNECTOR_CUSTODY_UNCONFIGURED", "CONNECTOR_CUSTODY_PERMISSIONS",
                     "SOURCE_ADMISSION_MISMATCH", "SOURCE_DRIVER_NOT_BOUND", "CONNECTOR_BOUND_EXCEEDED",
                     "CONNECTOR_CUSTODY_INVALID", "DATABASE_BOUND_EXCEEDED"}
        code = str(exc) if isinstance(exc, ValueError) and str(exc) in permitted else type(exc).__name__
        result["reason_code"] = code
    result["worker_receipt_id"] = "cwr-" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    return result


def main():
    request = json.loads(base64.b64decode(sys.argv[1]))
    signal.signal(signal.SIGALRM, _expired)
    signal.alarm(int(request["max_seconds"]))
    # A missing remote state binding is a refusal, not an ephemeral success.
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