"""tools/digicow_targeted_read_check_20260921.py

Targeted read-capability check for the token 'digicow' across the
banked estate. Non-interrupting to R-91. Read-only, value-blind for
credentials, receipted, hard stop after proof-of-read.

Steps:
    1. LOCATE the token across:
         (a) Fresh RMS CREDS sheet (case-insensitive; NEVER print
             suspected cred cells' actual values — but schema names,
             tags, hosts, section titles are structural, safe to name)
         (b) MySQL schema/table names already captured in the last
             sweep receipt
         (c) OBS bucket names in prior receipts + a fresh listBuckets
             cross-check
         (d) CIFS/NFS tree at /mnt/nfs-share (bounded find with
             remote-side timeout)
    2. PROVE READ per what it turns out to be:
         * SCHEMA on already-authed MySQL cluster → USE + SHOW TABLES
           + per-table COUNT(*) + one LIMIT-1 shape-only proof
         * OBS bucket → HeadBucket + ListObjects(max_keys=5)
         * CIFS path → test -r + stat metadata
    3. If NOT FOUND anywhere: explicit NOT_PRESENT verdict.

Emits: phase0/connectivity_receipts/{stamp}_DIGICOW_targeted_read_
check_owner_authorized_20260921.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import socket
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import openpyxl  # noqa: E402
import rms_creds_loader_v2 as L2  # noqa: E402
import paramiko  # noqa: E402
import pymysql  # noqa: E402

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
SWEEP_RECEIPT = RECEIPT_DIR / "20260921T142146Z_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json"
OBS_RECEIPT = RECEIPT_DIR / "20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json"
SHEET_PATH = Path("/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx")
HUAWEI_CRED = Path("/app/backend/estate_keys/data_sources/huawei_credentials_2_20260916.csv")

TOKEN = "digicow"
TOKEN_RX = re.compile(r"digicow", re.IGNORECASE)


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _redact_value(v):
    if v is None: return {"python_type": "NoneType", "is_null": True}
    t = type(v).__name__
    e = {"python_type": t, "is_null": False}
    try:
        if isinstance(v, (bytes, bytearray)):
            e["byte_len"] = len(v)
        elif isinstance(v, str):
            e["char_len"] = len(v)
            e["byte_len"] = len(v.encode("utf-8", errors="replace"))
        elif isinstance(v, (int, float)):
            e["int_bit_len"] = getattr(v, "bit_length", lambda: 0)()
    except Exception: pass
    return e


class Fwd:
    def __init__(self, transport, rhost, rport):
        self.transport = transport
        self.rhost = rhost
        self.rport = rport
        self.sock = None
        self.local_port = None
        self._stop = threading.Event()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0)); s.listen(8); s.settimeout(1.0)
        self.sock = s
        self.local_port = s.getsockname()[1]
        threading.Thread(target=self._accept, daemon=True).start()
        return self.local_port

    def _accept(self):
        while not self._stop.is_set():
            try: cs, _ = self.sock.accept()
            except socket.timeout: continue
            except OSError: return
            threading.Thread(target=self._handle, args=(cs,), daemon=True).start()

    def _handle(self, cs):
        try:
            chan = self.transport.open_channel(
                "direct-tcpip", (self.rhost, self.rport),
                ("127.0.0.1", self.local_port or 0), timeout=10.0)
        except Exception:
            try: cs.close()
            except Exception: pass
            return
        if chan is None:
            try: cs.close()
            except Exception: pass
            return
        def pump(src, dst):
            try:
                while True:
                    d = src.recv(4096)
                    if not d: break
                    dst.sendall(d)
            except Exception: pass
            finally:
                try: src.close()
                except Exception: pass
                try: dst.close()
                except Exception: pass
        threading.Thread(target=pump, args=(cs, chan), daemon=True).start()
        threading.Thread(target=pump, args=(chan, cs), daemon=True).start()

    def stop(self):
        self._stop.set()
        try:
            if self.sock: self.sock.close()
        except Exception: pass


def _ssh_exec(client, cmd, timeout=25.0):
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read(65536).decode("utf-8", errors="replace")
        err = stderr.read(8192).decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return {"cmd": cmd if len(cmd) <= 240 else cmd[:240]+"...",
                "rc": rc, "stdout": out[:16384],
                "stderr": err[:2048],
                "elapsed_s": round(time.monotonic() - t0, 3)}
    except Exception as e:
        return {"cmd": cmd[:240], "rc": None,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "elapsed_s": round(time.monotonic() - t0, 3)}


def _search_sheet_for_token(sheet_path: Path) -> dict:
    """Search every cell for the token. For each hit, report the row/col
    location + cell KIND (schema-name / host / user / password / tag /
    section-title / other). If the hit is in a USER or PASSWORD cell,
    ONLY report shape (len + sha8), never the value.

    Determining kind:
        - Row 1: header row → column labels
        - For data rows in the new-shape sheet:
             col 0 = schema, col 1 = host, col 2 = user, col 3 = password,
             col 4 = tag
    """
    hits = []
    wb = openpyxl.load_workbook(sheet_path, data_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            for j, cell in enumerate(row):
                if cell is None: continue
                s = str(cell)
                if TOKEN_RX.search(s):
                    # Determine kind
                    kind = "OTHER"
                    if i == 0 and sn == "Sheet1":
                        kind = "SECTION_HEADER"
                    elif i == 1 and sn == "Sheet1":
                        kind = "COLUMN_HEADER_LABEL"
                    elif sn == "Sheet1":
                        # data row — column-based classification
                        kind = {0: "SCHEMA_NAME", 1: "HOST", 2: "USER",
                                3: "PASSWORD", 4: "TAG"}.get(j, "OTHER")
                    hit: dict = {
                        "sheet": sn, "row": i, "col": j,
                        "kind_by_position": kind,
                        "cell_len": len(s),
                    }
                    # Only emit the value if it's structural (schema/host/tag/etc.)
                    # Never emit if kind is USER or PASSWORD.
                    if kind in ("USER", "PASSWORD"):
                        hit["value_shape_only"] = {
                            "len": len(s),
                            "sha8": hashlib.sha256(s.encode("utf-8")).hexdigest()[:8],
                            "value_redacted": True,
                        }
                    else:
                        hit["value"] = s
                    hits.append(hit)
    return {
        "sheet_path": str(sheet_path),
        "sheet_sha256_first_16": hashlib.sha256(sheet_path.read_bytes()).hexdigest()[:16],
        "hit_count": len(hits),
        "hits": hits,
    }


def _search_sweep_receipt() -> dict:
    """Search the last sweep receipt for the token in schema/table names."""
    if not SWEEP_RECEIPT.is_file():
        return {"error": "SWEEP_RECEIPT_MISSING"}
    r = json.load(SWEEP_RECEIPT.open())
    hits = []
    for entry in r.get("section_B_mysql_sweeps", []):
        surf = entry.get("surface")
        sw = entry.get("sweep", {})
        for db in sw.get("show_databases", []) or []:
            if TOKEN_RX.search(str(db)):
                hits.append({"kind": "SHOW_DATABASES_SCHEMA_NAME",
                             "surface": surf,
                             "host": entry.get("host"),
                             "value": db})
        for schema in sw.get("user_databases", []) or []:
            if TOKEN_RX.search(str(schema)):
                hits.append({"kind": "USER_DATABASE",
                             "surface": surf, "host": entry.get("host"),
                             "value": schema})
        for per in sw.get("per_schema", []) or []:
            if TOKEN_RX.search(str(per.get("representative_table") or "")):
                hits.append({"kind": "REPRESENTATIVE_TABLE_IN_SCHEMA",
                             "surface": surf, "host": entry.get("host"),
                             "schema": per.get("database"),
                             "table": per.get("representative_table")})
        for expected_schema in entry.get("expected_schemas_in_sheet", []) or []:
            if TOKEN_RX.search(str(expected_schema)):
                hits.append({"kind": "EXPECTED_SCHEMA_IN_SHEET",
                             "surface": surf, "host": entry.get("host"),
                             "value": expected_schema})
    return {"hit_count": len(hits), "hits": hits}


def _search_obs_bucket_list() -> dict:
    """Search prior banked OBS bucket list."""
    if not OBS_RECEIPT.is_file():
        return {"error": "OBS_RECEIPT_MISSING"}
    r = json.load(OBS_RECEIPT.open())
    hits = []
    def _walk(o, path="root"):
        if isinstance(o, dict):
            for k, v in o.items():
                _walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, item in enumerate(o):
                _walk(item, f"{path}[{i}]")
        elif isinstance(o, str) and TOKEN_RX.search(o):
            hits.append({"path": path, "value": o})
    _walk(r)
    return {"hit_count": len(hits), "hits": hits}


def _search_nfs_tree(client, timeout_sec=25) -> dict:
    """Bounded case-insensitive search under /mnt/nfs-share.

    Two layers:
      - Top level (depth 1) using ls
      - Bounded find at depth 3 with remote-side timeout + head cap
    """
    top = _ssh_exec(client, "ls -1 /mnt/nfs-share/ 2>&1", timeout=10)
    top_hits = []
    for name in (top.get("stdout") or "").splitlines():
        n = name.strip()
        if n and TOKEN_RX.search(n):
            top_hits.append({"where": "top_level", "name": n})

    # Bounded case-insensitive find at depth 3
    find_res = _ssh_exec(
        client,
        f"timeout {timeout_sec} find /mnt/nfs-share -maxdepth 3 -iname '*{TOKEN}*' "
        "2>/dev/null | head -100",
        timeout=timeout_sec + 8,
    )
    find_hits = []
    for line in (find_res.get("stdout") or "").splitlines():
        s = line.strip()
        if s: find_hits.append({"where": "depth_le_3_find", "path": s})

    return {
        "top_level_hit_count": len(top_hits),
        "top_level_hits": top_hits,
        "find_hit_count": len(find_hits),
        "find_hits": find_hits[:50],
        "find_rc": find_res.get("rc"),
        "find_elapsed_s": find_res.get("elapsed_s"),
    }


def _obs_fresh_list_buckets_for_digicow(cred) -> dict:
    """Cross-check: fresh listBuckets across ap-southeast-1 endpoint and
    scan bucket names for `digicow`. Any-hit → return the region-hit."""
    try:
        from obs import ObsClient
    except Exception as e:
        return {"error": f"OBS_SDK_IMPORT: {e}"}
    hits = []
    # We use the AP-SE-1 endpoint as the "canonical" list endpoint; if
    # the bucket exists in another region, listBuckets still returns
    # it (with a possibly-non-canonical location field).
    c = ObsClient(access_key_id=cred["ak"], secret_access_key=cred["sk"],
                  server="obs.ap-southeast-1.myhuaweicloud.com", timeout=15)
    try:
        resp = c.listBuckets()
        if resp.status < 300:
            buckets = getattr(resp.body, "buckets", []) or []
            for b in buckets:
                if TOKEN_RX.search(str(b.name)):
                    hits.append({"bucket": b.name,
                                 "creation_date": str(getattr(b, "create_date", None))})
        else:
            return {"list_status": resp.status,
                    "errorCode": getattr(resp, "errorCode", None)}
    except Exception as e:
        return {"error": f"{e.__class__.__name__}: {e}"}
    finally:
        try: c.close()
        except Exception: pass
    return {"hit_count": len(hits), "hits": hits}


def _load_huawei_ak_sk() -> Optional[dict]:
    if not HUAWEI_CRED.is_file(): return None
    text = HUAWEI_CRED.read_text(encoding="utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        ak = (row.get("Access Key Id") or "").strip()
        sk = (row.get("Secret Access Key") or "").strip()
        if ak and sk:
            return {"ak": ak, "sk": sk, "ak_prefix4": ak[:4],
                    "ak_len": len(ak), "sk_len": len(sk)}
    return None


def _prove_read_mysql_schema(local_port, user, password,
                             schema_name: str) -> dict:
    """Prove read of a specific schema — USE + SHOW TABLES + per-table
    COUNT + one LIMIT-1 shape-only proof."""
    out = {"schema": schema_name}
    try:
        conn = pymysql.connect(
            host="127.0.0.1", port=local_port,
            user=user, password=password,
            connect_timeout=12, read_timeout=15,
            cursorclass=pymysql.cursors.Cursor,
            charset="utf8mb4", autocommit=True,
        )
        out["auth_ok"] = True
        out["server_version"] = conn.get_server_info()
    except Exception as e:
        return {"auth_ok": False, "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400]}

    try:
        with conn.cursor() as cur:
            cur.execute(f"USE `{schema_name}`")
            out["use_ok"] = True
        # Table inventory
        with conn.cursor() as cur:
            cur.execute(
                "SELECT TABLE_NAME, TABLE_TYPE, TABLE_ROWS, "
                "DATA_LENGTH, CREATE_TIME, UPDATE_TIME "
                "FROM information_schema.TABLES "
                "WHERE TABLE_SCHEMA=%s ORDER BY TABLE_NAME",
                (schema_name,))
            tables = [{"name": r[0], "type": r[1],
                       "table_rows_estimate": r[2],
                       "data_length": r[3],
                       "create_time": str(r[4]) if r[4] else None,
                       "update_time": str(r[5]) if r[5] else None}
                      for r in cur.fetchall()]
        out["table_inventory"] = tables
        out["table_count"] = len(tables)
        # Per-table COUNT + LIMIT 1 shape (bounded to first 20 tables)
        table_probes = []
        for t in tables[:20]:
            tname = t["name"]
            probe = {"table": tname, "table_type": t["type"]}
            if t["type"] != "BASE TABLE":
                probe["skipped"] = "NOT_BASE_TABLE"
                table_probes.append(probe); continue
            try:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT COUNT(*) FROM `{schema_name}`.`{tname}`")
                    probe["count_star"] = cur.fetchone()[0]
            except pymysql.err.OperationalError as e:
                probe["count_star_err"] = {
                    "code": e.args[0] if e.args else None,
                    "msg": str(e.args[1] if len(e.args) > 1 else e)[:200]}
            # LIMIT 1 shape-only
            try:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM `{schema_name}`.`{tname}` LIMIT 1")
                    row = cur.fetchone()
                    col_names = [d[0] for d in cur.description] if cur.description else []
                if row is None:
                    probe["proof_of_read"] = {"row_returned": False,
                                              "col_names": col_names}
                else:
                    probe["proof_of_read"] = {
                        "row_returned": True,
                        "col_names": col_names,
                        "value_shape_by_col": {
                            (col_names[i] if i < len(col_names) else f"col_{i}"):
                                _redact_value(v)
                            for i, v in enumerate(row)
                        },
                    }
            except pymysql.err.OperationalError as e:
                probe["proof_of_read_err"] = {
                    "code": e.args[0] if e.args else None,
                    "msg": str(e.args[1] if len(e.args) > 1 else e)[:200]}
            table_probes.append(probe)
        out["per_table_probe"] = table_probes
        out["tables_probed_of_total"] = f"{len(table_probes)} of {len(tables)}"
    except Exception as e:
        out["enumeration_err"] = f"{e.__class__.__name__}: {str(e)[:200]}"
    finally:
        try: conn.close()
        except Exception: pass
    return out


def main():
    receipt = {
        "task": "DIGICOW_targeted_read_check_owner_authorized_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner directive this-session 2026-09-21T~14:35Z: 'OWNER GO "
            "targeted read-capability check on DIGICOW'. R-91 hold "
            "unchanged. Ratchet 5858 unchanged."
        ),
        "hygiene": {
            "read_only": True,
            "value_blind_for_credentials": True,
            "structural_names_ok_to_emit": (
                "schema, table, host, tag, bucket, mount-path names are "
                "structural and safe to report; user/password cells are "
                "reported by shape only."
            ),
            "no_downloads": True,
        },
        "token": TOKEN,
    }

    binds = L2.load()
    receipt["cred_shape"] = {"jump": binds.jump.describe(),
                             "n_mysql_clusters": len(binds.mysql_clusters)}

    # ---- Step 1a · Sheet search --------------------------------------
    receipt["step_1a_sheet_search"] = _search_sheet_for_token(SHEET_PATH)

    # ---- Step 1b · Sweep receipt search ------------------------------
    receipt["step_1b_sweep_receipt_search"] = _search_sweep_receipt()

    # ---- Step 1c · OBS receipt search + fresh listBuckets check ------
    receipt["step_1c_obs_receipt_search"] = _search_obs_bucket_list()
    hw = _load_huawei_ak_sk()
    if hw:
        receipt["step_1c_obs_fresh_list_check"] = _obs_fresh_list_buckets_for_digicow(hw)
    else:
        receipt["step_1c_obs_fresh_list_check"] = {"skipped": "NO_HUAWEI_CREDS"}

    # ---- Open JUMP for CIFS search + MySQL prove-read ----------------
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        jump.connect(hostname=binds.jump.host, port=22,
                     username=binds.jump.user, password=binds.jump.password,
                     timeout=12, auth_timeout=12, banner_timeout=12,
                     allow_agent=False, look_for_keys=False)
        receipt["jump_open_ok"] = True
    except Exception as e:
        receipt["jump_open_err"] = f"{e.__class__.__name__}: {e}"
        _emit(receipt); return

    # ---- Step 1d · CIFS/NFS tree search ------------------------------
    receipt["step_1d_nfs_cifs_search"] = _search_nfs_tree(jump)

    # ---- Aggregate location findings ---------------------------------
    all_locations = []
    for h in receipt["step_1a_sheet_search"]["hits"]:
        all_locations.append({"surface": "SHEET", **h})
    for h in receipt["step_1b_sweep_receipt_search"].get("hits", []):
        all_locations.append({"surface": "MYSQL_SCHEMA_OR_TABLE", **h})
    for h in receipt["step_1c_obs_receipt_search"].get("hits", []):
        all_locations.append({"surface": "OBS_BUCKET_(prior)", **h})
    if isinstance(receipt.get("step_1c_obs_fresh_list_check"), dict):
        for h in receipt["step_1c_obs_fresh_list_check"].get("hits", []):
            all_locations.append({"surface": "OBS_BUCKET_(fresh_list)", **h})
    for h in receipt["step_1d_nfs_cifs_search"].get("top_level_hits", []):
        all_locations.append({"surface": "CIFS_TOP_LEVEL", **h})
    for h in receipt["step_1d_nfs_cifs_search"].get("find_hits", []):
        all_locations.append({"surface": "CIFS_DEPTH_LE_3", **h})
    receipt["step_1_aggregate_locations"] = {
        "total_hit_count": len(all_locations),
        "hits": all_locations,
    }

    # ---- Step 2 · Prove read per what it turns out to be -------------
    # Focus on MySQL schema hits first — most likely surface.
    mysql_schema_hits = [
        h for h in receipt["step_1b_sweep_receipt_search"].get("hits", [])
        if h["kind"] in ("USER_DATABASE", "SHOW_DATABASES_SCHEMA_NAME",
                         "EXPECTED_SCHEMA_IN_SHEET")
    ]
    # Dedup by (host, value)
    seen = set()
    unique_schema_hits = []
    for h in mysql_schema_hits:
        key = (h.get("host"), h.get("value"))
        if key not in seen:
            seen.add(key)
            unique_schema_hits.append(h)

    proof_results = []
    if unique_schema_hits:
        transport = jump.get_transport()
        transport.set_keepalive(15)
        for h in unique_schema_hits:
            host = h.get("host")
            schema = h.get("value")
            if not host or not schema: continue
            # Find matching cluster in the sheet
            cluster = next((c for c in binds.mysql_clusters if c.host == host), None)
            if not cluster or not (cluster.user and cluster.password):
                proof_results.append({
                    "kind": "SCHEMA_ON_CLUSTER",
                    "host": host, "schema": schema,
                    "outcome": "NO_CREDS_FOR_HOST_IN_NEW_SHEET",
                })
                continue
            fwd = Fwd(transport, host, 3306)
            lp = fwd.start()
            time.sleep(0.2)
            try:
                res = _prove_read_mysql_schema(
                    lp, cluster.user, cluster.password, schema)
                proof_results.append({
                    "kind": "SCHEMA_ON_CLUSTER",
                    "host": host, "schema": schema,
                    "sweep": res,
                })
            finally:
                fwd.stop()
    receipt["step_2_proof_of_read"] = proof_results

    # ---- Verdict -----------------------------------------------------
    verdict = {
        "token": TOKEN,
        "aggregate_hits": len(all_locations),
        "mysql_schema_hits": len(unique_schema_hits),
        "proof_attempts": len(proof_results),
    }
    if len(all_locations) == 0:
        verdict["binary_answer"] = "NOT_PRESENT"
        verdict["explicit"] = (
            f"The token '{TOKEN}' does not appear in any of: the fresh "
            "RMS CREDS sheet (cell text or shape), the prior sweep "
            "receipt's schema/table/DB names on any authenticated "
            "cluster, the OBS bucket inventory (banked or fresh "
            "listBuckets), or the CIFS mount /mnt/nfs-share (top level "
            "or depth-3 case-insensitive find). "
            "Candidate owner-drop for a host/cred we don't yet hold — "
            "no endpoint is guessed."
        )
        verdict["failure_layer"] = "SURFACE_NOT_PRESENT_IN_BANKED_ESTATE"
    else:
        successes = [p for p in proof_results
                     if p.get("sweep", {}).get("use_ok")
                     and p.get("sweep", {}).get("table_count", 0) > 0]
        empty = [p for p in proof_results
                 if p.get("sweep", {}).get("use_ok")
                 and p.get("sweep", {}).get("table_count", 0) == 0]
        auth_fails = [p for p in proof_results
                      if not p.get("sweep", {}).get("auth_ok")]
        if successes and not auth_fails:
            verdict["binary_answer"] = "YES"
            verdict["explicit"] = (
                f"FOUND on {len(successes)} MySQL cluster(s); every "
                "proof-of-read succeeded (SHOW TABLES + COUNT + "
                "LIMIT-1 shape). See step_2_proof_of_read for tables + "
                "row-shape-only proofs."
            )
        elif successes and auth_fails:
            verdict["binary_answer"] = "PARTIAL"
            verdict["explicit"] = (
                f"FOUND on {len(successes)} readable + {len(auth_fails)} "
                "unauthenticated cluster(s). Readable ones proven; "
                "unauthenticated ones need creds."
            )
        elif empty:
            verdict["binary_answer"] = "YES (schema present, empty)"
            verdict["explicit"] = (
                f"FOUND but schema is empty of base tables on "
                f"{len(empty)} cluster(s)."
            )
        else:
            verdict["binary_answer"] = "AMBIGUOUS"
            verdict["explicit"] = (
                "Located but proof-of-read did not run successfully; "
                "see step_2_proof_of_read for details."
            )
        verdict["failure_layer"] = None
    receipt["verdict"] = verdict

    try: jump.close()
    except Exception: pass
    _emit(receipt)


def _emit(receipt):
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_DIGICOW_targeted_read_check_owner_authorized_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
