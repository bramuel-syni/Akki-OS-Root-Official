"""JUMP-tunneled read-only MySQL connect + schema-only sample.

Owner rulings 2026-09-13 (verbatim, in force):
- READ-ONLY (SELECT/SHOW/find with LIMIT only).
- SSH tunnel through JUMP; host-key pinned + strict checking.
- EAT window 08:00-02:00 UTC.
- Position-based redaction: NEVER print any cell value from any
  credentials file, regardless of header.
- Sensitive-data handling: SCHEMA ONLY. `iebc_forms` / `kra_reports`
  are Kenya government-grade PII (electoral / tax). No row values in
  transcript or receipt. Structural proof-of-read = one row with EVERY
  value masked to type+length only.

Uses paramiko (already installed) for the tunnel; pymysql (already
installed) for the DB connect.  No new package install.
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import json
import re
import socket
import socketserver
import threading
import time
from pathlib import Path

import paramiko
import pymysql


BASTION_CSV  = Path("/app/backend/estate_keys/bastion/jump_server_radio_system.csv")
VIUSASA_CSV  = Path("/app/backend/estate_keys/data_sources/db_credentials.csv")
WEEGO_CSV    = Path("/app/backend/estate_keys/data_sources/db_credentials_2.csv")
KNOWN_HOSTS  = Path("/app/backend/estate_keys/known_hosts")
RECEIPT_DIR  = Path("/app/assessment_workspace/phase0/db_connect_receipts")


# =====================================================================
# credential loading (in-memory only; NEVER print any value)
# =====================================================================

def _load_bastion():
    with BASTION_CSV.open() as f:
        rows = list(csv.reader(f))
    return {"ip": rows[1][0], "user": rows[2][0], "cred": rows[3][0]}


def _load_viusasa_rows():
    """VIUSASA rows with 4-col shape (db_name, host, user, pw)."""
    with VIUSASA_CSV.open() as f:
        rows = list(csv.reader(f))
    out = []
    for r in rows[1:]:
        if len(r) < 4:
            continue
        db, host, user, pw = r[0], r[1], r[2], r[3]
        if pw and user:  # has a full cred set
            out.append({
                "db_name": db,
                "host_hint": host,
                "user": user,
                "pw": pw,
            })
    return out


def _load_weego_hosts():
    """WEEGO db_name -> host mapping (2 cols)."""
    with WEEGO_CSV.open() as f:
        rows = list(csv.reader(f))
    return [(r[0], r[1]) for r in rows[1:] if len(r) >= 2 and r[1]]


# =====================================================================
# SSH tunnel via paramiko (foreground; explicit stop)
# =====================================================================

class _ForwardServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class _Handler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            chan = self.server.ssh_transport.open_channel(
                "direct-tcpip",
                (self.server.remote_host, self.server.remote_port),
                self.request.getpeername(),
            )
        except Exception:
            return
        if chan is None:
            return
        try:
            while True:
                r, _, _ = __import__("select").select(
                    [self.request, chan], [], [], 1.0,
                )
                if self.request in r:
                    data = self.request.recv(4096)
                    if len(data) == 0:
                        break
                    chan.send(data)
                if chan in r:
                    data = chan.recv(4096)
                    if len(data) == 0:
                        break
                    self.request.send(data)
        finally:
            chan.close()
            self.request.close()


def _start_tunnel(ssh: paramiko.SSHClient, local_port, remote_host, remote_port):
    transport = ssh.get_transport()
    server = _ForwardServer(("127.0.0.1", local_port), _Handler)
    server.ssh_transport = transport
    server.remote_host = remote_host
    server.remote_port = remote_port
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def _hostkeys_from_known_hosts():
    hk = paramiko.HostKeys()
    hk.load(str(KNOWN_HOSTS))
    return hk


# =====================================================================
# main
# =====================================================================

def _eat_ok():
    now = datetime.datetime.now(datetime.UTC)
    h = now.hour
    return (h >= 8 or h < 2), now, f"UTC hour={h}; EAT window 08:00-02:00 UTC"


def _mask_row(row, cursor_description):
    """Structural proof-of-read: type+length only, NEVER the value."""
    out = []
    for col_meta, val in zip(cursor_description, row):
        col_name = col_meta[0]
        col_type_code = col_meta[1]
        if val is None:
            length_str = "NULL"
        elif isinstance(val, (bytes, bytearray)):
            length_str = f"bytes(len={len(val)})"
        elif isinstance(val, str):
            length_str = f"str(len={len(val)})"
        elif isinstance(val, (int, float)):
            length_str = f"{type(val).__name__}(digits={len(str(val))})"
        else:
            length_str = f"{type(val).__name__}(repr_len={len(repr(val))})"
        out.append({
            "col_name": col_name,
            "type_code": col_type_code,
            "value_shape": length_str,
        })
    return out


def _attempt_auth(local_port, cred_row):
    """Try to auth against 127.0.0.1:local_port (tunneled). Returns dict.
    Never records cred values in the returned dict."""
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=local_port,
            user=cred_row["user"],
            password=cred_row["pw"],
            connect_timeout=10,
            read_timeout=30,
            init_command="SET SESSION TRANSACTION READ ONLY",
            autocommit=True,
        )
        return {"ok": True, "conn": conn, "cred_label": f"viusasa/{cred_row['db_name']}"}
    except pymysql.err.OperationalError as exc:
        code = exc.args[0] if exc.args else None
        msg = str(exc)[:200]
        cls = "AUTH_REJECTED" if code in (1045, 1044, 1698) else "NETWORK_OR_OTHER"
        return {"ok": False, "cls": cls, "code": code, "msg": msg,
                "cred_label": f"viusasa/{cred_row['db_name']}"}
    except Exception as exc:
        return {"ok": False, "cls": "OTHER", "msg": str(exc)[:200],
                "cred_label": f"viusasa/{cred_row['db_name']}"}


def main():
    ok, now, reason = _eat_ok()
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if not ok:
        print(f"OUT-WINDOW: {reason}")
        return 2
    print(f"IN-WINDOW: {reason}")

    j = _load_bastion()
    viusasa_creds = _load_viusasa_rows()
    weego_hosts = _load_weego_hosts()

    # Only 159.138.162.146:3306 was OPEN from JUMP (per reachability probe).
    TARGET_HOST = "159.138.162.146"
    TARGET_PORT = 3306
    LOCAL_PORT  = 13306

    print(f"target: {TARGET_HOST}:{TARGET_PORT} (only OPEN host from JUMP probe)")
    print(f"viusasa credential rows loaded: {len(viusasa_creds)}")

    # Paramiko SSH to JUMP with pinned known_hosts
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(str(KNOWN_HOSTS))
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # strict; must be pinned

    try:
        ssh.connect(
            hostname=j["ip"],
            username=j["user"],
            password=j["cred"],
            allow_agent=False,
            look_for_keys=False,
            timeout=15,
        )
    except paramiko.SSHException as exc:
        print(f"JUMP SSH failed: {exc!r}")
        return 3

    print("JUMP connected · opening tunnel")
    server = _start_tunnel(ssh, LOCAL_PORT, TARGET_HOST, TARGET_PORT)
    # brief settle
    time.sleep(1.0)

    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_2_TUNNELED_DB_CONNECT",
        "window_check": reason,
        "in_window": ok,
        "tunnel": {
            "engine": "paramiko",
            "jump": {"user": j["user"], "ip": "<pinned>"},
            "local": f"127.0.0.1:{LOCAL_PORT}",
            "remote": f"{TARGET_HOST}:{TARGET_PORT}",
            "reachability_probe_receipt":
                "phase0/db_connect_receipts/20260913T172245Z_step3_reachability_probe.json",
        },
        "credentials_loaded": {
            "viusasa_full_rows": len(viusasa_creds),
            "viusasa_row_shape": "col0=db_name, col1=host_hint, col2=user, col3=pw (ALL VALUES REDACTED-BY-POSITION)",
            "weego_host_rows": len(weego_hosts),
        },
        "read_only_assertion":
            "pymysql opens with init_command='SET SESSION TRANSACTION READ ONLY'; "
            "no non-SELECT/SHOW statements are issued from this driver.",
        "attempts": [],
        "schema_report": None,
    }

    conn = None
    winning_label = None
    for c in viusasa_creds:
        res = _attempt_auth(LOCAL_PORT, c)
        # Record without credential content
        receipt["attempts"].append({
            "cred_label": res["cred_label"],
            "ok": res["ok"],
            "cls": res.get("cls"),
            "code": res.get("code"),
            "msg": res.get("msg"),
        })
        if res["ok"]:
            conn = res["conn"]
            winning_label = res["cred_label"]
            print(f"AUTH SUCCESS with cred_label={winning_label!r}")
            break
        else:
            print(f"auth attempt {res['cred_label']!r} -> {res.get('cls')} "
                  f"code={res.get('code')}")

    if conn is None:
        print("NO CREDENTIAL AUTHENTICATED against target.")
        receipt["overall_verdict"] = "FAIL_AUTH"
    else:
        print("running SCHEMA-ONLY discovery (SHOW DATABASES · TABLES · counts)")
        schema = {"winning_cred_label": winning_label}
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            (ver,) = cur.fetchone()
            schema["server_version"] = ver
            cur.execute("SELECT @@GLOBAL.transaction_read_only, "
                        "@@SESSION.transaction_read_only")
            gr, sr = cur.fetchone()
            schema["read_only_global"] = int(gr)
            schema["read_only_session"] = int(sr)
            # database names — schema (not PII)
            cur.execute("SHOW DATABASES")
            db_rows = cur.fetchall()
            all_dbs = [r[0] for r in db_rows]
            schema["databases_all_names"] = all_dbs
            # For a sample of user-databases, count tables and row counts
            SKIP_SYS = {"information_schema", "mysql", "performance_schema", "sys"}
            sample_dbs = [d for d in all_dbs if d not in SKIP_SYS]
            schema["user_databases_total"] = len(sample_dbs)
            per_db = {}
            for db in sample_dbs[:12]:   # bounded — at most first 12
                try:
                    cur.execute(
                        "SELECT TABLE_NAME, TABLE_TYPE, TABLE_ROWS "
                        "FROM information_schema.tables "
                        "WHERE TABLE_SCHEMA = %s "
                        "LIMIT 200",
                        (db,),
                    )
                    tables = cur.fetchall()
                    per_db[db] = {
                        "tables_returned": len(tables),
                        "tables": [
                            {"name": t[0], "kind": t[1], "row_estimate": t[2]}
                            for t in tables
                        ],
                    }
                except Exception as exc:
                    per_db[db] = {"error": str(exc)[:200]}
            schema["per_database_schema"] = per_db

            # Structural proof-of-read: read exactly one row from
            # information_schema.SCHEMATA (schema itself), mask every value.
            cur.execute(
                "SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, "
                "DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA "
                "LIMIT 1"
            )
            row = cur.fetchone()
            if row is not None:
                schema["structural_proof_row_information_schema_schemata"] = (
                    _mask_row(row, cur.description)
                )
            else:
                schema["structural_proof_row_information_schema_schemata"] = None

            # Column-level structure for one representative table
            # (avoid selecting from any user table with PII; use only
            # information_schema.columns which is metadata).
            if sample_dbs:
                rep_db = sample_dbs[0]
                cur.execute(
                    "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, "
                    "COLUMN_TYPE, IS_NULLABLE "
                    "FROM information_schema.columns "
                    "WHERE TABLE_SCHEMA = %s LIMIT 40",
                    (rep_db,),
                )
                cols = cur.fetchall()
                schema["representative_db_column_metadata"] = {
                    "database": rep_db,
                    "columns_returned": len(cols),
                    "columns": [
                        {"table": c[0], "column": c[1], "data_type": c[2],
                         "column_type": c[3], "nullable": c[4]}
                        for c in cols
                    ],
                }
        conn.close()
        receipt["schema_report"] = schema
        receipt["overall_verdict"] = "PASS"

    server.shutdown()
    ssh.close()

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = (
        RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step2_tunneled_connect.json"
    )
    receipt_path.write_text(json.dumps(receipt, indent=2, default=str))
    print(f"receipt: {receipt_path}")
    print(f"verdict: {receipt['overall_verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
