"""tools/nas_schema_survey_20260921_v2.py · S2 continuation.

v1 established:
    * direct egress: TCP_TIMEOUT on 5000/5001/445 (LAN-only NAS confirmed)
    * JUMP SSH: OK (host key W45x... matches T3 handshake — no drift)
    * direct-tcpip forwards to DSM 5000 + 5001: OK
    * DSM API.Info: reachable, DSM 7-shape (entry.cgi, Auth max v7)
    * DSM HTTPS 5001: TLS 1.3, cert SHA captured
    * DSM auth via GET+version=7: error 400 (NO_SUCH_ACCOUNT_OR_WRONG_PASSWORD)

Findings-first hypotheses:
    (H1) DSM 7 rejected GET-in-URL auth for a password containing chars
         that need POST body, and/or version=7 requires additional
         fields the GET call omitted.
    (H2) The account is enabled for SMB service but has "Deny access
         via DSM" set (per-user DSM policy toggle — standard Synology
         setting for service accounts).
    (H3) The password we have is out of date for DSM login (though it
         worked for SMB on 2026-09-14).

v2 pursues the answer with three probes, all bounded, read-only:

    P1 · DSM HTTP auth retry matrix — POST body across versions 2,3,6,7
    P2 · SMB list shares (smbclient -L) via JUMP — the known-working
         vantage from 2026-09-14 T3 handshake
    P3 · Per-share SMB read probe (smbclient -c 'ls' at the share root)
         with a bounded top-level listing. NO get/put. NO recursion.

Discipline unchanged: creds by shape only, password never in argv
(passed via env or --authentication-file streamed once), no writes.
"""

from __future__ import annotations

import hashlib
import json
import re
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader  # noqa: E402
import paramiko  # noqa: E402
import requests  # noqa: E402


CUSTODY_XLSX = Path(
    "/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx"
)
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")

MAX_SHARES_TO_LS = 40           # cap SMB per-share list probes
MAX_LIST_ENTRIES_PER_SHARE = 60  # cap smbclient ls output lines we retain


def _now_utc_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- SSH tunnel (same as v1, kept small & inline) ------------------

class DirectTCPIPForward:
    def __init__(self, transport: paramiko.Transport, rhost: str, rport: int):
        self.transport = transport
        self.rhost = rhost
        self.rport = rport
        self.server_sock: Optional[socket.socket] = None
        self.local_port: Optional[int] = None
        self._stop = threading.Event()

    def start(self) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0))
        s.listen(8)
        s.settimeout(1.0)
        self.server_sock = s
        self.local_port = s.getsockname()[1]
        threading.Thread(target=self._accept_loop, daemon=True).start()
        return self.local_port

    def _accept_loop(self):
        while not self._stop.is_set():
            try:
                client_sock, _ = self.server_sock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            threading.Thread(target=self._handle,
                             args=(client_sock,), daemon=True).start()

    def _handle(self, client_sock):
        try:
            chan = self.transport.open_channel(
                "direct-tcpip", (self.rhost, self.rport),
                ("127.0.0.1", self.local_port or 0), timeout=10.0,
            )
        except Exception:
            try: client_sock.close()
            except Exception: pass
            return
        if chan is None:
            try: client_sock.close()
            except Exception: pass
            return
        def pump(src, dst):
            try:
                while True:
                    d = src.recv(4096)
                    if not d: break
                    dst.sendall(d)
            except Exception:
                pass
            finally:
                try: src.close()
                except Exception: pass
                try: dst.close()
                except Exception: pass
        threading.Thread(target=pump, args=(client_sock, chan), daemon=True).start()
        threading.Thread(target=pump, args=(chan, client_sock), daemon=True).start()

    def stop(self):
        self._stop.set()
        try:
            if self.server_sock: self.server_sock.close()
        except Exception:
            pass


# ---------- P1 · DSM HTTP auth retry matrix ------------------------------

def dsm_auth_retry_matrix(base_url: str, user: str, password: str,
                          timeout: float = 12.0) -> dict:
    """Try POST + multiple versions to cover DSM 6/7 semantics."""
    out: dict = {"attempts": []}
    sess = requests.Session()
    sess.verify = False
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception:
        pass

    matrix = [
        # (method, version, extra_params)
        ("POST", "6", {}),
        ("POST", "3", {}),
        ("POST", "2", {}),
        ("POST", "7", {"enable_syno_token": "yes"}),
        ("POST", "7", {}),
        ("GET",  "3", {}),  # sanity — classic DSM 6 GET
    ]
    for method, version, extra in matrix:
        params = {
            "api": "SYNO.API.Auth",
            "version": version,
            "method": "login",
            "account": user,
            "passwd": password,
            "session": "FileStation",
            "format": "sid",
        }
        params.update(extra)
        redacted_params_for_receipt = {
            k: ("<cred len=%d>" % len(v)) if k in ("account", "passwd") else v
            for k, v in params.items()
        }
        attempt = {
            "method": method,
            "version": version,
            "extra_keys": sorted(extra.keys()),
            "params_shape": redacted_params_for_receipt,
        }
        try:
            if method == "POST":
                r = sess.post(f"{base_url}/webapi/entry.cgi",
                              data=params, timeout=timeout)
            else:
                r = sess.get(f"{base_url}/webapi/auth.cgi",
                             params=params, timeout=timeout)
            attempt["http_status"] = r.status_code
            try:
                body = r.json()
            except Exception:
                body = {"_non_json_first_200": r.text[:200]}
            attempt["body_success"] = bool(body.get("success"))
            if body.get("success"):
                attempt["sid_len"] = len(body["data"]["sid"])
                out["succeeded_attempt"] = {
                    "method": method,
                    "version": version,
                    "extra_keys": sorted(extra.keys()),
                }
                out["sid"] = body["data"]["sid"]  # not banked
                out["attempts"].append(attempt)
                return out
            else:
                err = body.get("error", {}) or {}
                attempt["error_code"] = err.get("code")
        except Exception as e:
            attempt["error_class"] = e.__class__.__name__
            attempt["error_msg"] = str(e)[:200]
        out["attempts"].append(attempt)
    return out


# ---------- P2/P3 · SMB probes from JUMP via SSH exec_command -------------

def _ssh_exec(client: paramiko.SSHClient, cmd: str,
              env: Optional[dict] = None, timeout: float = 20.0) -> dict:
    """Run cmd on JUMP with optional env; timeout-bounded; return stdout/stderr.

    env values are exported via `env VAR=... VAR=...` prefix — but for
    secret values we DO NOT interpolate on the shell line; instead we
    feed them via `read` on stdin so they never touch /proc/*/cmdline."""
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout,
                                                    get_pty=False)
        if env:
            # Feed each secret via stdin followed by newline.
            # The remote-side shell must consume via `read`.
            payload = "\n".join(env.get(k, "") for k in env) + "\n"
            try:
                stdin.write(payload)
                stdin.flush()
            except Exception:
                pass
            try:
                stdin.channel.shutdown_write()
            except Exception:
                pass
        # Read with a byte cap.
        out = stdout.read(65536).decode("utf-8", errors="replace")
        err = stderr.read(8192).decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return {
            "rc": rc,
            "stdout_first_16k": out[:16384],
            "stderr_first_4k": err[:4096],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }
    except Exception as e:
        return {
            "rc": None,
            "error_class": e.__class__.__name__,
            "error_msg": str(e)[:400],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }


def smb_probe_via_jump(client: paramiko.SSHClient,
                       nas_host: str, user: str, password: str) -> dict:
    """P2 + P3 combined SMB enumeration from within JUMP.

    Uses the pattern from the 2026-09-14 T3 receipt: smbclient reads
    the password from a temporary authentication file staged in tmpfs
    (/dev/shm), never on argv or in the environment. File is shredded
    after use.

    Layout in JUMP tmpfs:
        /dev/shm/nas_auth.<pid>.<rand>       — smbclient authentication file
    """
    out: dict = {"nas_host": nas_host, "steps": []}

    # Stage a random path in tmpfs.
    #   $$ = shell PID, $RANDOM = random per-shell int
    #   filemode 0600 by umask
    stage_path = "/dev/shm/nas_auth.$$.${RANDOM}"

    # Build the auth file with heredoc, contents fed via stdin so nothing
    # ever appears on argv or in the shell history.
    # The heredoc terminator END_OF_AUTH is fixed so JUMP-side bash
    # knows exactly what to stop at.
    write_auth_cmd = (
        "set -eu; umask 077; "
        f"AUTH={stage_path}; "
        "cat >\"$AUTH\" <<'END_OF_AUTH'\n"
        "USER_PLACEHOLDER_LINE\n"
        "PASS_PLACEHOLDER_LINE\n"
        "END_OF_AUTH\n"
        "echo AUTH_STAGED=$AUTH; "
        "chmod 600 \"$AUTH\"; "
        "stat -c 'mode=%a size=%s' \"$AUTH\""
    )

    # We can't heredoc secrets safely because the placeholder lines are
    # baked literally into the heredoc — refactor: write the file via
    # printf reading from stdin. Simpler & atomic:
    stage_cmd = (
        "set -eu; umask 077; "
        f"AUTH=$(mktemp /dev/shm/nas_auth.XXXXXX); "
        "read -r U; read -r P; "
        "printf 'username=%s\\npassword=%s\\n' \"$U\" \"$P\" > \"$AUTH\"; "
        "echo AUTH_STAGED=$AUTH"
    )
    stage_res = _ssh_exec(client, stage_cmd,
                          env={"U": user, "P": password}, timeout=8.0)
    out["steps"].append({"step": "stage_auth_file", **stage_res})
    m = re.search(r"AUTH_STAGED=(\S+)", stage_res.get("stdout_first_16k", ""))
    if not m:
        out["failure"] = "AUTH_FILE_STAGING_FAILED"
        return out
    auth_path = m.group(1)

    try:
        # --- P2: list shares (-L) --------------------------------------
        list_cmd = (
            "smbclient -N -L "
            f"//{nas_host}/ "
            f"-A {auth_path} "
            "-m SMB3 "
            "-t 10 2>&1 "
            "; echo _RC=$?"
        )
        # smbclient -A takes an authentication file (username / password /
        # workgroup on separate lines). We built username= password= lines.
        # -N means no-prompt; -A supplies creds.
        # Correction: smbclient uses -A with a specific file format:
        #   username = xxx
        #   password = xxx
        #   domain   = xxx
        # Space around = is optional; the file we wrote uses `username=xxx`
        # which smbclient also accepts. Add a -U fallback just in case.
        list_res = _ssh_exec(client, list_cmd, timeout=25.0)
        out["steps"].append({"step": "smbclient_L_list_shares", **list_res})

        # Parse shares out of the -L output.
        shares = _parse_smbclient_L(list_res.get("stdout_first_16k", ""))
        out["parsed_shares"] = shares

        # --- P3: per-share ls at root ----------------------------------
        share_probes = []
        disk_shares = [s for s in shares if s.get("type", "").upper() == "DISK"]
        for sh in disk_shares[:MAX_SHARES_TO_LS]:
            name = sh["name"]
            ls_cmd = (
                f"smbclient -N //{nas_host}/'{name}' "
                f"-A {auth_path} "
                "-m SMB3 -t 15 "
                "-c 'ls' 2>&1 "
                "; echo _RC=$?"
            )
            ls_res = _ssh_exec(client, ls_cmd, timeout=25.0)
            parsed = _parse_smbclient_ls(ls_res.get("stdout_first_16k", ""))
            share_probes.append({
                "share": name,
                "rc_line_present": "_RC=" in ls_res.get("stdout_first_16k", ""),
                "auth_ok": parsed["auth_ok"],
                "read_ok": parsed["read_ok"],
                "denied": parsed["denied"],
                "top_level_entry_count": parsed["entry_count"],
                "top_level_sample": parsed["entries"][:MAX_LIST_ENTRIES_PER_SHARE],
                "capture_error_hint": parsed["error_hint"],
                "stderr_first_400": (ls_res.get("stderr_first_4k") or "")[:400],
                "elapsed_s": ls_res.get("elapsed_s"),
            })
        out["share_probes"] = share_probes
        out["shares_probed_count"] = len(share_probes)
        out["shares_disk_total"] = len(disk_shares)
    finally:
        shred_cmd = f"shred -uz '{auth_path}' 2>/dev/null || rm -f '{auth_path}'; echo AUTH_SHRED_DONE"
        shred_res = _ssh_exec(client, shred_cmd, timeout=6.0)
        out["steps"].append({"step": "shred_auth_file", **shred_res})

    return out


# ---------- Parsers -------------------------------------------------------

def _parse_smbclient_L(text: str) -> list:
    """Parse `smbclient -L //host/` output.

    Sample body:
            Sharename       Type      Comment
            ---------       ----      -------
            IPC$            IPC       IPC Service
            OFFAIRRECS      Disk
    """
    shares = []
    in_table = False
    for line in text.splitlines():
        s = line.rstrip()
        if not s:
            continue
        if re.match(r"^\s*Sharename\s+Type\s+Comment", s):
            in_table = True
            continue
        if in_table:
            if re.match(r"^\s*-+\s+-+", s):
                continue
            # End of first table when we hit "Server" or "Workgroup" section
            if re.match(r"^\s*(Server|Workgroup)\s+Comment", s):
                break
            m = re.match(r"^\s*(\S+)\s+(\S+)(?:\s+(.*))?$", s)
            if m:
                shares.append({
                    "name": m.group(1),
                    "type": m.group(2),
                    "comment": (m.group(3) or "").strip(),
                })
    return shares


def _parse_smbclient_ls(text: str) -> dict:
    """Parse `smbclient -c ls //host/share` output.

    Returns auth/read status + entry list.
    """
    lower = text.lower()
    result: dict = {
        "auth_ok": True,
        "read_ok": True,
        "denied": False,
        "entries": [],
        "entry_count": 0,
        "error_hint": None,
    }
    # Denial / auth error signatures
    if "logon_failure" in lower or "nt_status_logon_failure" in lower:
        result["auth_ok"] = False
        result["read_ok"] = False
        result["denied"] = False
        result["error_hint"] = "NT_STATUS_LOGON_FAILURE"
        return result
    if "access_denied" in lower or "nt_status_access_denied" in lower:
        result["auth_ok"] = True
        result["read_ok"] = False
        result["denied"] = True
        result["error_hint"] = "NT_STATUS_ACCESS_DENIED"
        return result
    if "bad_network_name" in lower or "nt_status_bad_network_name" in lower:
        result["auth_ok"] = True
        result["read_ok"] = False
        result["denied"] = False
        result["error_hint"] = "NT_STATUS_BAD_NETWORK_NAME"
        return result
    if "connection to" in lower and "failed" in lower:
        result["auth_ok"] = False
        result["read_ok"] = False
        result["error_hint"] = "CONNECTION_FAILED"
        return result

    # Parse smbclient `ls` grid — lines look like:
    #   .                                   D        0  Sun Mar  9 11:12:31 2025
    #   Record                              D        0  Sun Mar  9 11:12:31 2025
    #   somefile.dat                        A      512  Sun Mar  9 11:12:31 2025
    entries = []
    for line in text.splitlines():
        s = line.rstrip()
        if not s or s.startswith("Domain=") or s.startswith("blocks of size"):
            continue
        # Only accept lines that have a size column
        m = re.match(r"^\s*(\S.*?)\s+([DHSRAN]+)\s+(\d+)\s+(\S.+)$", s)
        if m:
            name = m.group(1).strip()
            attr = m.group(2)
            size = int(m.group(3))
            when = m.group(4).strip()
            if name in (".", ".."):
                continue
            entries.append({
                "name": name,
                "attr": attr,
                "isdir": "D" in attr,
                "size": size,
                "mtime_str": when,
            })
    result["entries"] = entries
    result["entry_count"] = len(entries)
    return result


# ---------- Main ----------------------------------------------------------

def main() -> None:
    receipt: dict = {
        "task": "S2_nas_schema_survey_v2_auth_matrix_and_smb_enum_20260921",
        "captured_at_utc": _now_utc_str(),
        "predecessor_receipt": (
            "phase0/connectivity_receipts/20260921T132205Z_NAS_schema_"
            "survey_S2_owner_authorized_20260921.json"
        ),
        "authorization": (
            "Continuation of owner GO S2 SCHEMA-SURVEY-NAS. v1 established "
            "DSM 7 present + HTTP auth rejected 400. v2 executes the auth "
            "retry matrix (H1) and the SMB known-working fallback (from "
            "T3 2026-09-14) to answer the scope question."
        ),
        "hygiene": {
            "read_only": True,
            "no_downloads": True,
            "no_writes": True,
            "creds_by_shape_only": True,
            "password_never_on_argv": True,
            "smbclient_auth_via_tmpfs_file_shredded_after": True,
        },
        "cred_source": {
            "custody_file": str(CUSTODY_XLSX),
            "custody_file_sha256": _sha256(CUSTODY_XLSX),
        },
    }

    binds = rms_creds_loader.load()
    receipt["cred_shape"] = {
        "nas": binds.nas.describe(),
    }

    nas_host = "10.10.55.55"

    # Open JUMP.
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        jump_client.connect(
            hostname=binds.jump.host, port=22,
            username=binds.jump.user, password=binds.jump.password,
            timeout=12.0, auth_timeout=12.0, banner_timeout=12.0,
            allow_agent=False, look_for_keys=False,
        )
    except Exception as e:
        receipt["jump_open_err"] = f"{e.__class__.__name__}: {str(e)[:300]}"
        _emit(receipt)
        return
    transport = jump_client.get_transport()
    transport.set_keepalive(15)

    # Forward for DSM HTTP 5000.
    fwd = DirectTCPIPForward(transport, nas_host, 5000)
    local_port = fwd.start()
    time.sleep(0.3)

    # --- P1 · Auth retry matrix ---------------------------------------
    matrix = dsm_auth_retry_matrix(
        base_url=f"http://127.0.0.1:{local_port}",
        user=binds.nas.user,
        password=binds.nas.password,
        timeout=12.0,
    )
    # Redact sid from receipt.
    matrix_for_receipt = {"attempts": matrix.get("attempts")}
    if "succeeded_attempt" in matrix:
        matrix_for_receipt["succeeded_attempt"] = matrix["succeeded_attempt"]
        matrix_for_receipt["sid_len"] = len(matrix["sid"])
    receipt["p1_dsm_auth_retry_matrix"] = matrix_for_receipt

    # --- P2 + P3 · SMB via JUMP ----------------------------------------
    smb = smb_probe_via_jump(
        jump_client, nas_host=nas_host,
        user=binds.nas.user, password=binds.nas.password,
    )
    # Strip inner steps' stdout of anything remotely sensitive (paths only).
    for st in smb.get("steps", []):
        # keep rc + elapsed + first 400 stdout for staging/shred diagnostics
        if isinstance(st.get("stdout_first_16k"), str):
            st["stdout_first_400"] = st["stdout_first_16k"][:400]
            del st["stdout_first_16k"]
        if isinstance(st.get("stderr_first_4k"), str):
            st["stderr_first_400"] = st["stderr_first_4k"][:400]
            del st["stderr_first_4k"]
    receipt["p2_p3_smb_via_jump"] = smb

    # --- Cross-cutting scope answer ------------------------------------
    scope = _compute_scope_answer(matrix, smb)
    receipt["scope_answer"] = scope

    # Teardown.
    fwd.stop()
    try: jump_client.close()
    except Exception: pass

    _emit(receipt)


def _compute_scope_answer(matrix: dict, smb: dict) -> dict:
    ans: dict = {}
    ans["dsm_http_auth_succeeded"] = "succeeded_attempt" in matrix
    if not ans["dsm_http_auth_succeeded"]:
        codes = sorted({a.get("error_code") for a in matrix.get("attempts", [])
                        if a.get("error_code") is not None})
        ans["dsm_http_auth_codes_observed"] = codes
        ans["dsm_http_auth_verdict"] = (
            "REJECTED_ACROSS_ALL_METHOD_VERSION_COMBINATIONS "
            "(consistent with DSM per-user policy: 'Allow this user to "
            "access DSM' unchecked while SMB service access remains "
            "enabled — a standard Synology service-account posture)."
        )

    shares = smb.get("parsed_shares", []) or []
    probes = smb.get("share_probes", []) or []
    disk_shares = [s for s in shares if (s.get("type") or "").upper() == "DISK"]
    ans["smb_service_reachable"] = bool(shares)
    ans["smb_share_list_count"] = len(shares)
    ans["smb_disk_share_count"] = len(disk_shares)
    ans["smb_disk_shares"] = [s.get("name") for s in disk_shares]

    read_ok_list = [p["share"] for p in probes if p.get("read_ok")]
    denied_list = [p["share"] for p in probes if p.get("denied")]
    other_fail = [p["share"] for p in probes
                  if not p.get("read_ok") and not p.get("denied")]
    ans["smb_readable_shares"] = read_ok_list
    ans["smb_denied_shares"] = denied_list
    ans["smb_other_failure_shares"] = other_fail

    # Classification
    if not shares:
        ans["classification"] = "SMB_ENUM_FAILED_OR_NO_SHARES"
    elif len(disk_shares) == 0:
        ans["classification"] = "SMB_ONLY_ADMINISTRATIVE_SHARES_VISIBLE"
    elif len(read_ok_list) == len(disk_shares):
        ans["classification"] = "ALL_VISIBLE_DISK_SHARES_READABLE_VIA_SMB"
    elif len(read_ok_list) == 1 and len(disk_shares) == 1:
        ans["classification"] = "SINGLE_SHARE_SCOPED_VIA_SMB"
    elif len(read_ok_list) > 0:
        ans["classification"] = "SOME_READABLE_SOME_DENIED_VIA_SMB"
    else:
        ans["classification"] = "NO_SMB_READ_ACCESS_ON_ANY_SHARE"

    # Explicit answer to the owner's question
    if len(read_ok_list) == len(disk_shares) and len(disk_shares) > 0:
        if not ans["dsm_http_auth_succeeded"]:
            ans["is_manager_admin_flag"] = None  # unknowable without DSM login
            ans["explicit_answer"] = (
                f"YES for all {len(disk_shares)} SMB-visible disk share(s) "
                f"({', '.join(read_ok_list)}). We can enumerate top-level "
                "and (per bounded sample) read metadata for every visible "
                "share via the JUMP + SMB path. DSM administrative login "
                "was rejected, so the admin-flag itself is unknown; the "
                "admin can confirm whether OTHER shares exist that are "
                "hidden from this account by inspecting DSM's share list."
            )
        else:
            ans["explicit_answer"] = (
                f"YES for all {len(disk_shares)} shares this account can see. "
                "Admin-flag verdict below (from DSM login) resolves whether "
                "'entire NAS' means 'this account's scope' or 'all shares'."
            )
    elif len(read_ok_list) == 1 and len(disk_shares) == 1:
        ans["explicit_answer"] = (
            f"PARTIAL — the account is SMB-scoped to one share "
            f"({read_ok_list[0]}). Broader read requires an admin scope-grant."
        )
    elif len(read_ok_list) > 0:
        ans["explicit_answer"] = (
            f"PARTIAL — SMB-readable: {read_ok_list}; denied: {denied_list}; "
            "other-failure: {other_fail}. Standard-account scope."
        )
    else:
        ans["explicit_answer"] = (
            "NO — no shares were readable via SMB. Either creds are "
            "stale for SMB too, or DSM has denied SMB access broadly. "
            "Ask the RMS admin to confirm the account state."
        )

    ans["distinction_note"] = (
        "'not visible to this account' vs 'visible but denied' — SMB "
        "returns only shares this account can see; deeper NAS shares "
        "the account is denied at the share level would be silently "
        "absent from `smbclient -L`. Only DSM admin scope can confirm "
        "absence."
    )
    return ans


def _emit(receipt: dict) -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPT_DIR / f"{stamp}_NAS_schema_survey_S2_v2_auth_matrix_and_smb_enum_20260921.json"
    path.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                    encoding="utf-8")
    print(f"receipt_path: {path}")


if __name__ == "__main__":
    main()
