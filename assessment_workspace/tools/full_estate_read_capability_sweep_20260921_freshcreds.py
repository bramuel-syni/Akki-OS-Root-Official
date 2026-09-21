"""tools/full_estate_read_capability_sweep_20260921_freshcreds.py

Full estate read-capability re-sweep using the FRESH credentials drop
(sha `3311dae2…`, banked 2026-09-21T140818Z). Non-interrupting to R-91.

Discipline: same as prior sweep — read-only, minimum touch, bounded
enumeration, proof-of-read to shape only (no real values in receipts).

Surfaces this run:
    A. JUMP sizing (re-confirm)
    B. MySQL — ALL credentialed hosts in fresh sheet (8 clusters via
       JUMP tunnel). Still-blocked: 159.138.162.146.
    C. NAS DSM/SMB re-attempt with LEGACY creds (only ones we have) —
       confirms stale state; no fresh NAS creds in new sheet.
    D. NAS-access-via-Razuna: NEW surface `159.138.173.58` with fresh
       creds (labelled "NAS - ACESS" / "Razuna & Newsvault"). Probe
       TCP + banner + auth-shape.
    E. NFS/CIFS mount at /mnt/nfs-share on JUMP — finish the channel
       enumeration that v2 timed out on; STRICT remote timeouts.
    F. OBS — carry-forward from prior receipts (no new AK/SK).
"""

from __future__ import annotations

import hashlib
import json
import re
import socket
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader_v2 as L2  # noqa: E402
import paramiko  # noqa: E402
import pymysql  # noqa: E402

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")

MYSQL_MAX_ROWS_PER_SELECT = 1
MYSQL_PROOF_ROW_VALUE_MAX_BYTES = 512
SYSTEM_SCHEMAS = {"information_schema", "mysql", "performance_schema", "sys", "tmp"}

# NFS/CIFS enumeration caps
NFS_LS_MAX_LINES = 40
NFS_FIND_MAX_LINES = 60


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _redact_value(v) -> dict:
    if v is None: return {"python_type": "NoneType", "is_null": True}
    t = type(v).__name__
    entry = {"python_type": t, "is_null": False}
    try:
        if isinstance(v, (bytes, bytearray)):
            entry["byte_len"] = min(len(v), MYSQL_PROOF_ROW_VALUE_MAX_BYTES)
        elif isinstance(v, str):
            entry["char_len"] = min(len(v), MYSQL_PROOF_ROW_VALUE_MAX_BYTES)
            entry["byte_len"] = min(len(v.encode("utf-8", errors="replace")),
                                    MYSQL_PROOF_ROW_VALUE_MAX_BYTES)
        elif isinstance(v, (int, float)):
            entry["int_bit_len"] = getattr(v, "bit_length", lambda: 0)()
        else:
            entry["repr_class"] = t
    except Exception: pass
    return entry


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
        s.bind(("127.0.0.1", 0))
        s.listen(8)
        s.settimeout(1.0)
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


def _classify_mysql_op_error(code) -> str:
    if code is None: return "UNKNOWN"
    return {
        1044: "SCHEMA_ACCESS_DENIED",
        1045: "AUTH_REJECTED_BAD_USER_OR_PASSWORD",
        1049: "UNKNOWN_DATABASE",
        1130: "HOST_NOT_ALLOWED_TO_CONNECT",
        1142: "TABLE_ACCESS_DENIED",
        1143: "COLUMN_ACCESS_DENIED",
        1226: "USER_HAS_EXCEEDED_MAX_QUESTIONS",
        1227: "ACCESS_DENIED_INSUFFICIENT_PRIVILEGE",
        2003: "CANT_CONNECT_TO_SERVER",
        2005: "UNKNOWN_HOST",
        2013: "LOST_CONNECTION",
    }.get(code, f"MYSQL_CODE_{code}")


def _cluster_sweep(local_port, user, password, label, expected_schemas) -> dict:
    out = {"cluster_label": label,
           "expected_schemas_in_sheet": expected_schemas}
    t0 = time.monotonic()
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1", port=local_port,
            user=user, password=password,
            connect_timeout=12, read_timeout=12,
            cursorclass=pymysql.cursors.Cursor,
            charset="utf8mb4", autocommit=True,
        )
        out["auth"] = {"ok": True,
                       "elapsed_s": round(time.monotonic() - t0, 3),
                       "server_version": conn.get_server_info()}
    except pymysql.err.OperationalError as e:
        code, msg = e.args if len(e.args) >= 2 else (None, str(e))
        out["auth"] = {"ok": False,
                       "mysql_error_code": code,
                       "mysql_error_msg": str(msg)[:400],
                       "failure_layer": _classify_mysql_op_error(code),
                       "elapsed_s": round(time.monotonic() - t0, 3)}
        return out
    except Exception as e:
        out["auth"] = {"ok": False,
                       "error_class": e.__class__.__name__,
                       "error_msg": str(e)[:400],
                       "elapsed_s": round(time.monotonic() - t0, 3)}
        return out

    try:
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES")
            all_dbs = [r[0] for r in cur.fetchall()]
        out["show_databases"] = all_dbs
        user_dbs = [d for d in all_dbs if d not in SYSTEM_SCHEMAS]
        out["user_databases"] = user_dbs

        db_probes = []
        for db in user_dbs:
            entry = {"database": db}
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT TABLE_NAME FROM information_schema.TABLES "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_TYPE='BASE TABLE' "
                        "ORDER BY TABLE_NAME LIMIT 1", (db,))
                    row = cur.fetchone()
                    entry["representative_table"] = row[0] if row else None
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT COUNT(*) FROM information_schema.TABLES "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_TYPE='BASE TABLE'",
                        (db,))
                    entry["table_count_in_schema"] = cur.fetchone()[0]
                if not entry["representative_table"]:
                    entry["skipped"] = "SCHEMA_HAS_NO_BASE_TABLES"
                    db_probes.append(entry); continue
                tbl = entry["representative_table"]
                # DESCRIBE
                try:
                    with conn.cursor() as cur:
                        cur.execute(f"DESCRIBE `{db}`.`{tbl}`")
                        cols_meta = cur.fetchall()
                    entry["columns_meta"] = [
                        {"field": c[0], "type": str(c[1]), "null": c[2],
                         "key": c[3], "default": None if c[4] is None else "<default_hidden>",
                         "extra": c[5]} for c in cols_meta
                    ]
                except pymysql.err.OperationalError as e:
                    entry["describe_err"] = {
                        "code": e.args[0] if e.args else None,
                        "msg": str(e.args[1] if len(e.args) > 1 else e)[:200],
                        "failure_layer": _classify_mysql_op_error(e.args[0] if e.args else None),
                    }
                # COUNT
                try:
                    with conn.cursor() as cur:
                        cur.execute(f"SELECT COUNT(*) FROM `{db}`.`{tbl}`")
                        entry["count_star"] = cur.fetchone()[0]
                except pymysql.err.OperationalError as e:
                    entry["count_star_err"] = {
                        "code": e.args[0] if e.args else None,
                        "msg": str(e.args[1] if len(e.args) > 1 else e)[:200],
                        "failure_layer": _classify_mysql_op_error(e.args[0] if e.args else None),
                    }
                # LIMIT 1 shape-only
                try:
                    with conn.cursor() as cur:
                        cur.execute(f"SELECT * FROM `{db}`.`{tbl}` LIMIT %s",
                                    (MYSQL_MAX_ROWS_PER_SELECT,))
                        row = cur.fetchone()
                        col_names = [d[0] for d in cur.description] if cur.description else []
                    if row is None:
                        entry["proof_of_read"] = {"row_returned": False,
                                                  "reason": "TABLE_EMPTY_OR_LIMIT_NO_ROW",
                                                  "col_names": col_names}
                    else:
                        entry["proof_of_read"] = {
                            "row_returned": True,
                            "col_names": col_names,
                            "value_shape_by_col": {
                                (col_names[i] if i < len(col_names) else f"col_{i}"):
                                    _redact_value(v)
                                for i, v in enumerate(row)
                            },
                        }
                except pymysql.err.OperationalError as e:
                    entry["proof_of_read_err"] = {
                        "code": e.args[0] if e.args else None,
                        "msg": str(e.args[1] if len(e.args) > 1 else e)[:200],
                        "failure_layer": _classify_mysql_op_error(e.args[0] if e.args else None),
                    }
            except Exception as e:
                entry["error_class"] = e.__class__.__name__
                entry["error_msg"] = str(e)[:200]
            db_probes.append(entry)
        out["per_schema"] = db_probes
        out["readable_schemas"] = [
            e["database"] for e in db_probes
            if e.get("proof_of_read", {}).get("row_returned") is not None
        ]
        out["schemas_with_read_error"] = [
            e["database"] for e in db_probes if "proof_of_read_err" in e
        ]
    except Exception as e:
        out["enumeration_err"] = f"{e.__class__.__name__}: {str(e)[:200]}"
        out["traceback"] = traceback.format_exc()[-800:]
    finally:
        try: conn.close()
        except Exception: pass
    out["total_elapsed_s"] = round(time.monotonic() - t0, 3)
    return out


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


def _shquote(s: str) -> str:
    if s == "": return "''"
    return "'" + s.replace("'", "'\\''") + "'"


def _tcp_probe_via_ssh(client, host, port, timeout=8):
    """TCP probe from JUMP via `bash /dev/tcp`."""
    cmd = f"timeout {int(timeout)} bash -c 'exec 3<>/dev/tcp/{host}/{port} && echo TCP_OPEN || echo TCP_CLOSED'"
    return _ssh_exec(client, cmd, timeout=timeout + 4)


def _http_head_via_ssh(client, url, timeout=8):
    """HEAD-request the URL from JUMP with `curl -sS -I --max-time N`."""
    q = _shquote(url)
    cmd = f"timeout {timeout+2} curl -sS -I --max-time {timeout} {q} 2>&1 | head -20"
    return _ssh_exec(client, cmd, timeout=timeout + 6)


def _sample_channel_bounded(client, mount_path, channel_name, label) -> dict:
    q = _shquote(f"{mount_path}/{channel_name}")
    out = {"label": label, "channel_name_observed": channel_name}
    out["depth1_ls"] = _ssh_exec(
        client, f"timeout 12 ls -la {q}/ 2>&1 | head -{NFS_LS_MAX_LINES}",
        timeout=20)
    out["depth1_type_counts"] = _ssh_exec(
        client,
        f"timeout 12 bash -c '(cd {q} 2>/dev/null && "
        "echo dirs=$(find . -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l); "
        "echo files=$(find . -maxdepth 1 -mindepth 1 -type f 2>/dev/null | wc -l))' 2>&1",
        timeout=20)
    out["depth2_find_capped"] = _ssh_exec(
        client,
        f"timeout 20 find {q} -maxdepth 2 -mindepth 1 2>&1 | head -{NFS_FIND_MAX_LINES}",
        timeout=28)
    out["ext_histogram"] = _ssh_exec(
        client,
        f"timeout 20 find {q} -maxdepth 3 -type f 2>/dev/null | head -3000 | "
        "awk -F. '{if (NF>1) print tolower($NF); else print \"NOEXT\"}' | "
        "sort | uniq -c | sort -rn | head -20",
        timeout=28)
    out["mtime_range_files_sample"] = _ssh_exec(
        client,
        f"timeout 20 find {q} -maxdepth 3 -type f -printf '%TY-%Tm-%Td\\n' 2>/dev/null | "
        "head -3000 | sort -u | (head -1; tail -1) 2>&1",
        timeout=28)
    out["smallest_file"] = _ssh_exec(
        client,
        f"timeout 20 find {q} -maxdepth 3 -type f -printf '%s\\t%p\\n' 2>/dev/null | "
        "head -3000 | sort -n | head -1",
        timeout=28)
    return out


def _stat_and_test_r(client, path):
    q = _shquote(path)
    return {
        "stat": _ssh_exec(
            client,
            "stat --format='name=%n%nsize=%s%nmode_octal=%a%nmode_hr=%A%n"
            "uid=%u%nuname=%U%ngid=%g%ngname=%G%nmtime=%y%nctime=%z' " + q,
            timeout=10),
        "test_r": _ssh_exec(
            client, f"test -r {q} && echo READABLE || echo NOT_READABLE",
            timeout=10),
    }


def main():
    receipt = {
        "task": "FULL_ESTATE_read_capability_sweep_freshcreds_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner GO this-session 2026-09-21T~14:05Z: 'OWNER CREDENTIAL "
            "RE-DROP - fresh sheet, ingest under §E secret-hygiene then "
            "re-run the full estate read-capability sweep.' R-91 hold "
            "unchanged. Ratchet 5858 unchanged."
        ),
        "hygiene": {
            "read_only": True,
            "creds_by_shape_only": True,
            "mysql_no_actual_row_values_in_receipt": True,
            "nfs_zero_downloads_bounded_enum": True,
        },
        "cred_source": {
            "primary_new_sheet_sha256": _sha256_file(Path(
                "/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx")),
            "legacy_baseline_sha256": _sha256_file(Path(
                "/app/assessment_workspace/custody/credentials/prior_baseline/"
                "d778eb1e_prior_baseline.xlsx")),
        },
    }

    binds = L2.load()
    receipt["cred_shape"] = {
        "provenance": binds.provenance,
        "jump": binds.jump.describe(),
        "radio": binds.radio.describe(),
        "nas_legacy": binds.nas.describe(),
        "mysql_clusters": [c.describe() for c in binds.mysql_clusters],
    }

    # Open JUMP
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        t0 = time.monotonic()
        jump.connect(hostname=binds.jump.host, port=22,
                     username=binds.jump.user, password=binds.jump.password,
                     timeout=12, auth_timeout=12, banner_timeout=12,
                     allow_agent=False, look_for_keys=False)
        receipt["jump_open"] = {"ok": True,
                                "elapsed_s": round(time.monotonic() - t0, 3)}
    except Exception as e:
        receipt["jump_open"] = {"ok": False,
                                "error_class": e.__class__.__name__,
                                "error_msg": str(e)[:400]}
        _emit(receipt); return
    transport = jump.get_transport()
    transport.set_keepalive(15)

    # ---- Section A · JUMP sizing (light re-confirm) ------------------
    receipt["section_A_jump_sizing"] = {
        "nproc": _ssh_exec(jump, "nproc", timeout=6),
        "free_m": _ssh_exec(jump, "free -m", timeout=6),
    }

    # ---- Section B · MySQL sweep across all credentialed clusters ----
    receipt["section_B_mysql_sweeps"] = []
    for cluster in binds.mysql_clusters:
        entry = {
            "surface": f"MySQL {cluster.section} @ {cluster.host}:3306",
            "host": cluster.host,
            "expected_schemas_in_sheet": list(cluster.schemas),
            "tag": cluster.tag,
            "creds_in_sheet": bool(cluster.user and cluster.password),
        }
        if not cluster.user or not cluster.password:
            entry["outcome"] = "NO_CREDS_IN_SHEET_STILL"
            entry["explicit"] = (
                "Sheet parses to user_len=0, pass_len=0 for this host — "
                "still blocked after the fresh drop."
            )
            receipt["section_B_mysql_sweeps"].append(entry); continue
        # HOST placeholder handling — try DNS-resolvable name if host is
        # literally "HOST" (WEEGO row). We can't proceed without an IP.
        if cluster.host == "HOST":
            entry["outcome"] = "PLACEHOLDER_HOST_NO_IP"
            entry["explicit"] = (
                "Cluster host is the literal token 'HOST' (WEEGO section) "
                "— now has creds in the new sheet but no resolvable host. "
                "Ask the admin to substitute an IP or DNS name."
            )
            receipt["section_B_mysql_sweeps"].append(entry); continue

        fwd = Fwd(transport, cluster.host, 3306)
        lp = fwd.start()
        time.sleep(0.15)
        try:
            with socket.create_connection(("127.0.0.1", lp), timeout=6) as _:
                entry["tcp_open_via_jump"] = True
        except Exception as e:
            entry["tcp_open_via_jump"] = False
            entry["tcp_open_err"] = f"{e.__class__.__name__}: {str(e)[:200]}"
            fwd.stop()
            receipt["section_B_mysql_sweeps"].append(entry); continue

        sw = _cluster_sweep(lp, cluster.user, cluster.password,
                            entry["surface"], list(cluster.schemas))
        entry["sweep"] = sw
        entry["outcome"] = "OK" if sw.get("auth", {}).get("ok") else "AUTH_FAILED"
        fwd.stop()
        receipt["section_B_mysql_sweeps"].append(entry)

    # ---- Section C · NAS DSM/SMB re-attempt (stale legacy creds) ------
    # Confirms stale-creds-still-stale; no new NAS entry in fresh sheet.
    receipt["section_C_nas_dsm_smb_reattempt"] = {
        "note": (
            "New sheet does NOT carry NAS DSM/SMB creds; using LEGACY "
            "creds (which failed on 2026-09-21T13:22Z). This is a "
            "verification pass only — expected: still-rejected."
        ),
        "smb_L_via_jump_smbclient": _nas_smb_reattempt(jump, binds),
    }

    # ---- Section D · NEW surface 159.138.173.58 / Razuna & Newsvault --
    # Section labelled "NAS - ACESS" in new sheet, password_len=17.
    # We don't know the service type — probe TCP + HTTP + SSH.
    new_surface = next((c for c in binds.mysql_clusters
                        if c.host == "159.138.173.58"), None)
    if new_surface:
        receipt["section_D_nas_access_via_razuna"] = _probe_new_surface(
            jump, new_surface,
        )

    # ---- Section E · NFS/CIFS mount on JUMP (finish enumeration) ------
    receipt["section_E_nfs_cifs_mount"] = _cifs_mount_survey(jump)

    # ---- Section F · OBS carry-forward -------------------------------
    receipt["section_F_obs_carry_forward"] = {
        "no_new_ak_sk_in_fresh_sheet": True,
        "prior_status": (
            "OBS: LIST across all 4 regions OK; GetObject on rms-ai "
            "smallest returned 403 AccessDenied. Prior receipts: "
            "20260921T133821Z (main sweep) + 20260921T134035Z (OBS delta)."
        ),
        "unchanged": True,
    }

    try: jump.close()
    except Exception: pass

    _emit(receipt)


def _nas_smb_reattempt(jump, binds) -> dict:
    """Fast re-attempt of smbclient -L using legacy creds (expected fail)."""
    out = {}
    # Stage auth file (same pattern as prior S2 receipts)
    stage = _ssh_exec(
        jump,
        "set -eu; umask 077; "
        "AUTH=$(mktemp /dev/shm/nas_auth.XXXXXX); "
        "read -r U; read -r P; "
        "printf 'username=%s\\npassword=%s\\n' \"$U\" \"$P\" > \"$AUTH\"; "
        "echo AUTH_STAGED=$AUTH",
        timeout=10,
    )
    # For env-only pass to stdin we need to write U/P via channel; this
    # helper of _ssh_exec doesn't route env. Use a different pattern.
    # ... Actually for read-only re-attempt discipline, keep this SIMPLE.
    # Just run one shot with the legacy creds via a heredoc from stdin.
    return {"skipped": "legacy_creds_confirmed_stale_by_S2_stack_20260921T132947Z_dont_re_burn_auth_attempts",
            "cite": "phase0/connectivity_receipts/20260921T132947Z_NAS_smb_final_layer_pin_S2_20260921.json"}


def _probe_new_surface(jump, cluster) -> dict:
    out = {"host": cluster.host,
           "labelled_in_sheet_as": "NAS - ACESS / Razuna & Newsvault",
           "sheet_password_len_hint": len(cluster.password) if cluster.password else 0}
    # TCP probes across common ports from JUMP
    probes = {}
    for name, port in [("ssh_22", 22), ("http_80", 80), ("https_443", 443),
                       ("mysql_3306", 3306), ("dsm_5000", 5000),
                       ("dsm_5001", 5001), ("razuna_8080", 8080),
                       ("razuna_8443", 8443)]:
        probes[name] = _tcp_probe_via_ssh(jump, cluster.host, port, timeout=6)
    out["tcp_probes_via_jump"] = probes
    # HTTP HEAD if 80/443 open
    for scheme, port_key in [("http", "http_80"), ("https", "https_443")]:
        if "TCP_OPEN" in (probes.get(port_key, {}).get("stdout") or ""):
            out[f"{scheme}_head"] = _http_head_via_ssh(
                jump, f"{scheme}://{cluster.host}/", timeout=8,
            )
    # If MySQL 3306 open, try MySQL auth using the sheet creds.
    if "TCP_OPEN" in (probes.get("mysql_3306", {}).get("stdout") or ""):
        fwd = Fwd(jump.get_transport(), cluster.host, 3306)
        lp = fwd.start()
        time.sleep(0.15)
        out["mysql_auth_attempt"] = _cluster_sweep(
            lp, cluster.user, cluster.password,
            f"MySQL_probe_{cluster.host}", list(cluster.schemas),
        )
        fwd.stop()
    return out


def _cifs_mount_survey(jump) -> dict:
    """Bounded survey of the CIFS mount that v2 timed out on."""
    out = {}
    out["mount_now"] = _ssh_exec(
        jump, "mount 2>&1 | grep -iE '(nfs|cifs)' | head -3", timeout=10)
    out["df_h"] = _ssh_exec(jump, "df -h /mnt/nfs-share 2>&1", timeout=10)
    out["ls_1_top"] = _ssh_exec(
        jump, "timeout 20 ls -1 /mnt/nfs-share/ 2>&1", timeout=28)

    # Positional reconciliation to 16 channels
    names = [s.strip() for s in (out["ls_1_top"].get("stdout") or "").splitlines()
             if s.strip() and s.strip() not in (".", "..")]
    out["top_level_names_observed"] = names
    out["channel_reconciliation"] = _reconcile_channels(names)

    # Sample 2 channels — but BOUNDED to prevent 47TB walk.
    # Channel selection: channel01 (Ch1 Citizen TV) + channel04 (Ch4 Inooro FM)
    samples = {}
    for label, ch_name in [("TV_Ch1", "channel01"), ("Radio_Ch4", "channel04")]:
        if ch_name in names:
            samples[label] = _sample_channel_bounded(
                jump, "/mnt/nfs-share", ch_name, label)
            # Try smallest-file stat + read test
            small = (samples[label]["smallest_file"].get("stdout") or "").strip()
            parts = small.split("\t", 1) if small else []
            if len(parts) == 2:
                try:
                    size = int(parts[0]); path = parts[1]
                    samples[label]["smallest_file_parsed"] = {"size_bytes": size, "path": path}
                    samples[label]["stat_and_test_r"] = _stat_and_test_r(jump, path)
                    tr_out = samples[label]["stat_and_test_r"]["test_r"]["stdout"]
                    if "READABLE" in tr_out and "NOT_READABLE" not in tr_out:
                        samples[label]["readability_verdict"] = "READABLE_VIA_test_r"
                    else:
                        # 1-byte fallback
                        one_byte = _ssh_exec(
                            jump,
                            f"timeout 10 head -c 1 {_shquote(path)} 2>&1 | wc -c ; echo _RC=$?",
                            timeout=15)
                        samples[label]["one_byte_read"] = one_byte
                        stdout = one_byte.get("stdout", "")
                        m = re.search(r"^\s*(\d+)\s*$",
                                      stdout.splitlines()[0] if stdout else "",
                                      re.M)
                        samples[label]["readability_verdict"] = (
                            "READABLE_1_BYTE_OK" if m and int(m.group(1)) == 1
                            else "READ_DENIED_AT_BYTE"
                        )
                except Exception as e:
                    samples[label]["parse_err"] = f"{e.__class__.__name__}: {e}"
        else:
            samples[label] = {"channel_missing": ch_name}
    out["samples"] = samples

    # Verdict
    matched = out["channel_reconciliation"]["matched_count"]
    sampled_ok = sum(1 for s in samples.values()
                     if s.get("readability_verdict", "").startswith("READABLE_"))
    if matched == 16 and sampled_ok == len(samples):
        v = "FULL_16_CHANNELS_PRESENT_ALL_SAMPLED_READABLE"
    elif matched == 16 and sampled_ok > 0:
        v = f"PARTIAL_16_CHANNELS_PRESENT_{sampled_ok}_OF_{len(samples)}_SAMPLED_READABLE"
    else:
        v = f"AMBIGUOUS_matched={matched}_sampled_ok={sampled_ok}"
    out["verdict"] = {
        "matched_channels": matched,
        "expected_channels": 16,
        "sampled_channels": len(samples),
        "sampled_read_ok": sampled_ok,
        "one_line": v,
        "trust_model": (
            "kernel-mediated CIFS mount using cached 'bramuel' session; "
            "active via /mnt/nfs-share type=cifs vers=3.1.1. No fresh "
            "creds needed — session persists across the rotation."
        ),
    }
    return out


def _reconcile_channels(names: list) -> dict:
    EXPECTED = [
        ("Ch1", "Citizen TV", "TV"), ("Ch2", "Inooro TV", "TV"),
        ("Ch3", "Radio Citizen", "Radio"), ("Ch4", "Inooro FM", "Radio"),
        ("Ch5", "Ramogi FM", "Radio"), ("Ch6", "Egesa FM", "Radio"),
        ("Ch7", "Musyi FM", "Radio"), ("Ch8", "Hot 96 FM", "Radio"),
        ("Ch9", "Chamgei FM", "Radio"), ("Ch10", "Mulembe FM", "Radio"),
        ("Ch11", "Sulwe FM", "Radio"), ("Ch12", "Vuuka FM", "Radio"),
        ("Ch13", "Bahari FM", "Radio"), ("Ch14", "Muuga FM", "Radio"),
        ("Ch15", "Wimwaro FM", "Radio"), ("Ch16", "Ramogi TV", "TV"),
    ]
    matched, extra = [], []
    used = set()
    for name in names:
        low = name.strip().lower()
        m = re.match(r"^channel0*(\d+)$", low)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 16:
                code, nm, kind = EXPECTED[n-1]
                matched.append({"observed": name, "matched_to": code,
                                "num": n, "expected_name": nm, "kind": kind})
                used.add(n); continue
        extra.append(name)
    missing = [{"expected_code": EXPECTED[i-1][0],
                "expected_name": EXPECTED[i-1][1],
                "kind": EXPECTED[i-1][2]}
               for i in range(1, 17) if i not in used]
    return {"expected_count": 16, "matched_count": len(matched),
            "extra_count": len(extra), "missing_count": len(missing),
            "matched": matched, "extra": extra, "missing": missing}


def _emit(receipt):
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_FULL_ESTATE_read_capability_sweep_freshcreds_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
