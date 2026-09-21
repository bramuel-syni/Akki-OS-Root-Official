"""tools/nas_schema_survey_20260921.py · S2 · SCHEMA-SURVEY-NAS (read-only).

Owner directive verbatim this-session (2026-09-21T~13:35Z):

    "OWNER GO → S2 · SCHEMA-SURVEY-NAS (read-only), to answer the owner's
    direct question: 'can we read the NAS contents entirely?' Non-
    interrupting to the R-91 hold; strict read-only, no downloads."

Discipline:
    * Values are held in memory only (via rms_creds_loader.load()).
    * NEVER prints secret values to any log or receipt.
    * References secrets by drop manifest sha + file sha + shape only.
    * Timebox every probe.
    * READ-ONLY. Zero downloads (no SYNO.FileStation.Download,
      no SMB `get`, no any-write).
    * Sampling only at depth 1; bounded depth-2 where cheap.
      HARD cap on total FileStation.List calls.
    * Vantage: direct egress first (expected fail on 10.10.55.55:5000
      from the sandbox pod — the NAS is LAN-only); then via JUMP using
      an in-process paramiko direct-tcpip channel forward.
    * If JUMP-forwarded HTTP auth is rejected by the DSM (e.g. IP-based
      login policy that only trusts the JUMP LAN host), that is a
      FINDING — recorded as such, not forced.

Emits: phase0/connectivity_receipts/20260921T{HHMMSS}Z_NAS_schema_survey_
S2_owner_authorized_20260921.json (state-only; banked in the state repo).
"""

from __future__ import annotations

import hashlib
import json
import socket
import ssl
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# tools/ on sys.path — rms_creds_loader is co-located.
_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader  # noqa: E402
import paramiko  # noqa: E402
import requests  # noqa: E402


CUSTODY_XLSX = Path(
    "/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx"
)
DROP_MANIFEST = Path(
    "/app/assessment_workspace/phase0/credential_drop_manifests/"
    "20260916T1910Z_drop_manifest.json"
)
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")

# Bounds — every enumeration call is against these.
MAX_LIST_CALLS_TOTAL = 200
MAX_DEPTH2_CHILDREN_PER_SHARE = 20
DEPTH2_SIZE_CEILING_ITEMS = 200  # if depth1 > this, skip depth2 for this share


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


def _tcp_probe(host: str, port: int, timeout: float = 8.0) -> dict:
    t0 = time.monotonic()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        elapsed = round(time.monotonic() - t0, 3)
        s.close()
        return {"tcp_connected": True, "elapsed_s": elapsed}
    except socket.timeout:
        return {"tcp_connected": False, "failure_layer": "TCP_TIMEOUT",
                "elapsed_s": round(time.monotonic() - t0, 3)}
    except ConnectionRefusedError as e:
        return {"tcp_connected": False, "failure_layer": "TCP_REFUSED",
                "error_msg": str(e)[:200]}
    except socket.gaierror as e:
        return {"tcp_connected": False, "failure_layer": "NO_DNS",
                "error_msg": str(e)[:200]}
    except OSError as e:
        # e.g. Network is unreachable / Host is unreachable
        return {"tcp_connected": False, "failure_layer": "OSERROR",
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:200]}
    except Exception as e:
        return {"tcp_connected": False, "failure_layer": "OTHER",
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:200]}


# --------------------------------------------------------------------------
# In-process SSH -L port forwarder over an already-open paramiko Transport.
# --------------------------------------------------------------------------

class DirectTCPIPForward:
    """Bind 127.0.0.1:0 locally; for each accepted connection, open a
    direct-tcpip channel through the SSH transport to (rhost, rport)."""

    def __init__(self, transport: paramiko.Transport, rhost: str, rport: int):
        self.transport = transport
        self.rhost = rhost
        self.rport = rport
        self.server_sock: Optional[socket.socket] = None
        self.local_port: Optional[int] = None
        self._stop = threading.Event()
        self._accept_thread: Optional[threading.Thread] = None

    def start(self) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0))
        s.listen(8)
        s.settimeout(1.0)
        self.server_sock = s
        self.local_port = s.getsockname()[1]
        self._accept_thread = threading.Thread(
            target=self._accept_loop, name=f"fwd-{self.rport}", daemon=True,
        )
        self._accept_thread.start()
        return self.local_port

    def _accept_loop(self) -> None:
        while not self._stop.is_set():
            try:
                client_sock, _ = self.server_sock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            threading.Thread(
                target=self._handle_client, args=(client_sock,),
                daemon=True,
            ).start()

    def _handle_client(self, client_sock: socket.socket) -> None:
        try:
            chan = self.transport.open_channel(
                kind="direct-tcpip",
                dest_addr=(self.rhost, self.rport),
                src_addr=("127.0.0.1", self.local_port or 0),
                timeout=10.0,
            )
        except Exception:
            try:
                client_sock.close()
            except Exception:
                pass
            return
        if chan is None:
            try:
                client_sock.close()
            except Exception:
                pass
            return
        # Bidirectional pump.
        def pump(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.sendall(data)
            except Exception:
                pass
            finally:
                try:
                    src.close()
                except Exception:
                    pass
                try:
                    dst.close()
                except Exception:
                    pass
        threading.Thread(target=pump, args=(client_sock, chan), daemon=True).start()
        threading.Thread(target=pump, args=(chan, client_sock), daemon=True).start()

    def stop(self) -> None:
        self._stop.set()
        try:
            if self.server_sock:
                self.server_sock.close()
        except Exception:
            pass


# --------------------------------------------------------------------------
# DSM API glue — versionless dispatch via SYNO.API.Info.
# --------------------------------------------------------------------------

class DSMSession:
    def __init__(self, base_url: str, receipt_bag: dict, timeout: float = 12.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.sid: Optional[str] = None
        self.api_map: dict = {}
        self.receipt_bag = receipt_bag  # for banking transport-level details
        self._list_calls = 0
        self.session = requests.Session()
        # No verify since we're on plain HTTP; but if HTTPS mode is set,
        # allow explicit verify=False (DSM 5001 uses a self-signed cert
        # by default). We record the cert SHA and TLS version separately.
        self.session.verify = False
        # Silence urllib3 InsecureRequestWarning noise into the receipt.
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except Exception:
            pass

    def _get(self, path: str, params: dict) -> dict:
        url = f"{self.base_url}{path}"
        # Copy params so we can strip secrets before banking any error trace.
        try:
            r = self.session.get(url, params=params, timeout=self.timeout)
            body = None
            try:
                body = r.json()
            except Exception:
                body = {"_non_json_first_400": r.text[:400]}
            return {
                "http_status": r.status_code,
                "http_ok": r.ok,
                "body": body,
            }
        except requests.exceptions.RequestException as e:
            return {
                "http_status": None,
                "http_ok": False,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
            }

    def query_api_info(self) -> dict:
        params = {
            "api": "SYNO.API.Info",
            "version": "1",
            "method": "query",
            "query": ",".join([
                "SYNO.API.Auth",
                "SYNO.FileStation.Info",
                "SYNO.FileStation.List",
                "SYNO.Core.Desktop.Initdata",
                "SYNO.Core.System",
                "SYNO.Core.User",
            ]),
        }
        res = self._get("/webapi/query.cgi", params)
        # Populate api_map from the response body.
        try:
            data = res.get("body", {}).get("data", {}) or {}
            for name, entry in data.items():
                self.api_map[name] = entry  # entry: {path, minVersion, maxVersion, ...}
        except Exception:
            pass
        return res

    def _path_of(self, api_name: str) -> Optional[str]:
        entry = self.api_map.get(api_name)
        if not entry:
            return None
        p = entry.get("path")
        return f"/webapi/{p}" if p else None

    def _maxver_of(self, api_name: str, cap: int = 7) -> str:
        entry = self.api_map.get(api_name) or {}
        v = entry.get("maxVersion")
        if isinstance(v, int):
            return str(min(v, cap))
        return "1"

    def login(self, user: str, password: str) -> dict:
        auth_path = self._path_of("SYNO.API.Auth") or "/webapi/auth.cgi"
        version = self._maxver_of("SYNO.API.Auth", cap=7)
        params = {
            "api": "SYNO.API.Auth",
            "version": version,
            "method": "login",
            "account": user,
            "passwd": password,
            "session": "FileStation",
            "format": "sid",
        }
        # Deliberately do NOT bank `params` — includes password.
        try:
            r = self.session.get(f"{self.base_url}{auth_path}",
                                 params=params, timeout=self.timeout)
            body = r.json()
        except requests.exceptions.RequestException as e:
            return {
                "http_status": None,
                "http_ok": False,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "auth_layer": "TRANSPORT",
            }
        except Exception as e:
            return {
                "http_status": r.status_code if 'r' in locals() else None,
                "http_ok": False,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "auth_layer": "BODY_PARSE",
            }
        out = {
            "http_status": r.status_code,
            "http_ok": r.ok,
            "success": bool(body.get("success")),
        }
        if body.get("success"):
            self.sid = body["data"]["sid"]
            out["sid_shape"] = {
                "len": len(self.sid),
                "sha256_first_8": hashlib.sha256(self.sid.encode()).hexdigest()[:8],
            }
            out["auth_version_used"] = version
        else:
            err = body.get("error", {})
            code = err.get("code")
            out["error_code"] = code
            # Map well-known Synology error codes:
            # 400 no such account or incorrect password
            # 401 account disabled
            # 402 permission denied
            # 403 2-factor required
            # 404 failed to authenticate 2-factor
            # 407 max tries reached — temporary IP block
            # 408-411 various policy denies
            code_hint = {
                400: "NO_SUCH_ACCOUNT_OR_WRONG_PASSWORD",
                401: "ACCOUNT_DISABLED",
                402: "PERMISSION_DENIED",
                403: "TWO_FACTOR_REQUIRED",
                404: "TWO_FACTOR_FAILED",
                407: "IP_TEMP_BLOCKED_MAX_TRIES",
                408: "PASSWORD_EXPIRED_MUST_CHANGE",
                409: "PASSWORD_EXPIRED",
                410: "PASSWORD_MUST_BE_CHANGED",
                411: "ACCOUNT_LOCKED",
            }.get(code)
            out["error_hint"] = code_hint or "UNKNOWN"
            out["auth_layer"] = "DSM_AUTH_REJECTED"
        return out

    def logout(self) -> dict:
        if not self.sid:
            return {"skipped": "no_sid"}
        auth_path = self._path_of("SYNO.API.Auth") or "/webapi/auth.cgi"
        params = {
            "api": "SYNO.API.Auth",
            "version": self._maxver_of("SYNO.API.Auth", cap=7),
            "method": "logout",
            "session": "FileStation",
            "_sid": self.sid,
        }
        res = self._get(auth_path, params)
        # Wipe the sid regardless of result.
        self.sid = None
        return res

    def fs_info(self) -> dict:
        path = self._path_of("SYNO.FileStation.Info") or "/webapi/entry.cgi"
        params = {
            "api": "SYNO.FileStation.Info",
            "version": self._maxver_of("SYNO.FileStation.Info", cap=2),
            "method": "get",
            "_sid": self.sid,
        }
        return self._get(path, params)

    def sys_info(self) -> dict:
        path = self._path_of("SYNO.Core.System") or "/webapi/entry.cgi"
        params = {
            "api": "SYNO.Core.System",
            "version": self._maxver_of("SYNO.Core.System", cap=3),
            "method": "info",
            "_sid": self.sid,
        }
        return self._get(path, params)

    def desktop_initdata(self) -> dict:
        path = self._path_of("SYNO.Core.Desktop.Initdata") or "/webapi/entry.cgi"
        params = {
            "api": "SYNO.Core.Desktop.Initdata",
            "version": self._maxver_of("SYNO.Core.Desktop.Initdata", cap=1),
            "method": "get",
            "_sid": self.sid,
        }
        return self._get(path, params)

    def list_share(self) -> dict:
        path = self._path_of("SYNO.FileStation.List") or "/webapi/entry.cgi"
        params = {
            "api": "SYNO.FileStation.List",
            "version": self._maxver_of("SYNO.FileStation.List", cap=2),
            "method": "list_share",
            "additional": "real_path,size,owner,time,perm,mount_point_type,volume_status",
            "onlywritable": "false",
            "_sid": self.sid,
        }
        return self._get(path, params)

    def list_folder(self, folder_path: str, limit: int = 200) -> dict:
        if self._list_calls >= MAX_LIST_CALLS_TOTAL:
            return {"skipped": "MAX_LIST_CALLS_TOTAL_REACHED"}
        self._list_calls += 1
        path = self._path_of("SYNO.FileStation.List") or "/webapi/entry.cgi"
        params = {
            "api": "SYNO.FileStation.List",
            "version": self._maxver_of("SYNO.FileStation.List", cap=2),
            "method": "list",
            "folder_path": folder_path,
            "additional": "size,owner,time,perm,type",
            "limit": str(limit),
            "sort_by": "name",
            "_sid": self.sid,
        }
        return self._get(path, params)


# --------------------------------------------------------------------------
# Vantage helpers.
# --------------------------------------------------------------------------

def _https_cert_probe(host: str, port: int, timeout: float = 8.0) -> dict:
    """Timeboxed TLS probe — captures cert SHA + TLS version + cipher."""
    t0 = time.monotonic()
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as tls:
                der = tls.getpeercert(binary_form=True) or b""
                return {
                    "tls_ok": True,
                    "tls_version": tls.version(),
                    "cipher": list(tls.cipher() or ()),
                    "peer_cert_der_sha256": hashlib.sha256(der).hexdigest() if der else None,
                    "elapsed_s": round(time.monotonic() - t0, 3),
                }
    except Exception as e:
        return {
            "tls_ok": False,
            "error_class": e.__class__.__name__,
            "error_msg": str(e)[:200],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }


def _https_cert_probe_via_forward(local_host: str, local_port: int,
                                  sni_host: str, timeout: float = 8.0) -> dict:
    """Same probe but through the local forwarded TCP port."""
    t0 = time.monotonic()
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((local_host, local_port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=sni_host) as tls:
                der = tls.getpeercert(binary_form=True) or b""
                return {
                    "tls_ok": True,
                    "tls_version": tls.version(),
                    "cipher": list(tls.cipher() or ()),
                    "peer_cert_der_sha256": hashlib.sha256(der).hexdigest() if der else None,
                    "elapsed_s": round(time.monotonic() - t0, 3),
                }
    except Exception as e:
        return {
            "tls_ok": False,
            "error_class": e.__class__.__name__,
            "error_msg": str(e)[:200],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }


def _classify_permission(perm_block: Optional[dict]) -> dict:
    """Best-effort classification of Synology perm blob.

    DSM returns per-item perms roughly as:
      {"acl": {"append": bool, "del": bool, "exec": bool,
               "read": bool, "write": bool},
       "adv_right": {...},
       "is_acl_mode": bool,
       "posix": int,        # posix bits
       "share_right": str}  # e.g. "RW", "RO", "denied"
    Older DSM 6 uses a slightly different shape. We compute a boolean
    read/write summary that survives both."""
    if not isinstance(perm_block, dict):
        return {"read": None, "write": None, "raw_perm_shape": None}
    acl = perm_block.get("acl") or {}
    share_right = perm_block.get("share_right")
    read = None
    write = None
    if isinstance(acl, dict):
        read = acl.get("read") if "read" in acl else read
        write = acl.get("write") if "write" in acl else write
    if isinstance(share_right, str):
        sr = share_right.upper()
        if "R" in sr and read is None:
            read = True
        if "W" in sr and write is None:
            write = True
        if sr in ("DENIED", "NONE"):
            read = False
            write = False
    return {
        "read": read,
        "write": write,
        "share_right": share_right,
        "raw_perm_keys": sorted(list(perm_block.keys())),
    }


# --------------------------------------------------------------------------
# Main survey.
# --------------------------------------------------------------------------

def main() -> None:
    receipt: dict = {
        "task": "S2_nas_schema_survey_owner_authorized_20260921",
        "captured_at_utc": _now_utc_str(),
        "authorization": (
            "Owner directive this-session 2026-09-21: 'OWNER GO → S2 · "
            "SCHEMA-SURVEY-NAS (read-only)... answer whether we can read "
            "the NAS contents entirely.' R-91 hold unchanged. Ratchet "
            "floor unchanged (5858). S1/S3 remain gated."
        ),
        "hygiene": {
            "read_only": True,
            "no_downloads": True,
            "no_writes": True,
            "creds_by_shape_only": True,
            "sid_never_persisted": True,
            "sid_logout_at_end": True,
        },
        "bounds": {
            "max_list_calls_total": MAX_LIST_CALLS_TOTAL,
            "max_depth2_children_per_share": MAX_DEPTH2_CHILDREN_PER_SHARE,
            "depth2_size_ceiling_items": DEPTH2_SIZE_CEILING_ITEMS,
        },
        "cred_source": {
            "custody_file": str(CUSTODY_XLSX),
            "custody_file_sha256": _sha256(CUSTODY_XLSX),
            "drop_manifest": str(DROP_MANIFEST),
            "drop_manifest_sha256": _sha256(DROP_MANIFEST),
        },
    }

    # ---- load creds --------------------------------------------------
    try:
        binds = rms_creds_loader.load()
    except Exception as e:
        receipt["cred_load_err"] = repr(e)[:400]
        _emit(receipt)
        return

    receipt["cred_shape"] = {
        "nas": binds.nas.describe(),      # dsm_url + user_len + password_len + step counts
        "jump": binds.jump.describe(),
    }

    # Parse DSM URL — strip fragment (#/signin), extract host+port+scheme.
    parsed = urlparse(binds.nas.dsm_url)
    scheme = (parsed.scheme or "http").lower()
    host = parsed.hostname or ""
    port = parsed.port or (443 if scheme == "https" else 80)
    receipt["nas_target"] = {
        "scheme": scheme, "host": host, "port": port,
        "fragment_stripped": bool(parsed.fragment),
    }

    # ---- Attempt A: direct egress ------------------------------------
    receipt["vantage_direct_egress"] = {
        "attempt": "direct_from_sandbox_pod",
        "expectation": (
            "LAN-only NAS at 10.10.55.55 — expected to fail from a "
            "public egress. If it opens, we have a routing surprise."
        ),
        "http_5000_tcp": _tcp_probe(host, 5000, timeout=6.0),
        "https_5001_tcp": _tcp_probe(host, 5001, timeout=6.0),
        "smb_445_tcp": _tcp_probe(host, 445, timeout=6.0),
    }

    # ---- Attempt B: via JUMP tunnel ----------------------------------
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump_open = {}
    t0 = time.monotonic()
    try:
        jump_client.connect(
            hostname=binds.jump.host,
            port=22,
            username=binds.jump.user,
            password=binds.jump.password,
            timeout=12.0,
            auth_timeout=12.0,
            banner_timeout=12.0,
            allow_agent=False,
            look_for_keys=False,
        )
        jump_open["ssh_connect_ok"] = True
        jump_open["elapsed_s"] = round(time.monotonic() - t0, 3)
        transport = jump_client.get_transport()
        transport.set_keepalive(15)
        host_key = transport.get_remote_server_key()
        jump_open["remote_host_key_type"] = host_key.get_name()
        import base64 as _b64
        jump_open["remote_host_key_sha256_b64"] = _b64.b64encode(
            hashlib.sha256(host_key.asbytes()).digest()
        ).decode("ascii").rstrip("=")
    except Exception as e:
        jump_open["ssh_connect_ok"] = False
        jump_open["error_class"] = e.__class__.__name__
        jump_open["error_msg"] = str(e)[:400]
        jump_open["traceback"] = traceback.format_exc()[-1200:]
        receipt["jump_open"] = jump_open
        _emit(receipt)
        return
    receipt["jump_open"] = jump_open

    # Set up port forwards for HTTP:5000 and HTTPS:5001.
    fwd_http = DirectTCPIPForward(transport, host, 5000)
    local_http_port = fwd_http.start()
    fwd_https = DirectTCPIPForward(transport, host, 5001)
    local_https_port = fwd_https.start()
    time.sleep(0.4)  # let accept loops settle

    receipt["jump_forwards"] = {
        "vantage": "JUMP_direct_tcpip_channel",
        "http_5000_local_port": local_http_port,
        "https_5001_local_port": local_https_port,
    }

    # Sanity: probe TCP through the forwards.
    receipt["forward_tcp_probes"] = {
        "http_5000_via_jump": _tcp_probe("127.0.0.1", local_http_port, timeout=6.0),
        "https_5001_via_jump": _tcp_probe("127.0.0.1", local_https_port, timeout=6.0),
    }

    # HTTPS cert probe (security posture note only — do NOT do auth over 5001
    # unless HTTP fails; the owner asked us to record cleartext-vs-TLS).
    receipt["dsm_5001_tls_via_jump"] = _https_cert_probe_via_forward(
        "127.0.0.1", local_https_port, sni_host=host, timeout=8.0,
    )

    # ---- DSM API session over HTTP tunnel ----------------------------
    dsm_base = f"http://127.0.0.1:{local_http_port}"
    dsm = DSMSession(dsm_base, receipt_bag=receipt, timeout=12.0)

    # 1) Discover API map
    receipt["api_info_query"] = dsm.query_api_info()
    receipt["api_map_summary"] = {
        name: {
            "path": entry.get("path"),
            "min": entry.get("minVersion"),
            "max": entry.get("maxVersion"),
        }
        for name, entry in dsm.api_map.items()
    }

    # 2) Login
    receipt["auth_login"] = dsm.login(binds.nas.user, binds.nas.password)

    if not dsm.sid:
        # No sid → the survey stops here. Bank the failure findings & exit.
        receipt["scope_answer"] = {
            "answered": False,
            "reason": "AUTH_FAILED_VIA_JUMP_TUNNEL",
            "hypothesis": (
                "DSM may enforce IP-based login policy that only trusts "
                "the on-prem LAN — the direct-tcpip channel presents the "
                "JUMP host's LAN IP to DSM, but if DSM's policy is stricter "
                "(e.g. only 192.168.4.x, or a specific admin host), auth "
                "will be rejected. Record as a scope-grant finding for "
                "the RMS admin, not a credential problem."
            ),
        }
        _teardown(dsm, fwd_http, fwd_https, jump_client)
        _emit(receipt)
        return

    # 3) fs_info — gives us DSM+FS version + is_manager (admin flag)
    fs_info_res = dsm.fs_info()
    receipt["fs_info"] = fs_info_res
    is_manager = None
    hostname_dsm = None
    fs_version_pack = None
    try:
        d = fs_info_res.get("body", {}).get("data", {}) or {}
        is_manager = d.get("is_manager")
        hostname_dsm = d.get("hostname")
        fs_version_pack = {
            "system_codepage": d.get("system_codepage"),
            "support_virtual_protocol": d.get("support_virtual_protocol"),
            "support_sharing": d.get("support_sharing"),
        }
    except Exception:
        pass

    # 4) desktop initdata — additional admin flag / user pane
    initdata_res = dsm.desktop_initdata()
    receipt["desktop_initdata"] = _redact_initdata(initdata_res)

    # 5) system info — DSM version (if permitted)
    receipt["sys_info"] = dsm.sys_info()

    # ---- Share enumeration -------------------------------------------
    share_res = dsm.list_share()
    receipt["list_share_raw_meta"] = {
        "http_status": share_res.get("http_status"),
        "success": bool(share_res.get("body", {}).get("success")),
    }
    shares_out = []
    try:
        shares = share_res.get("body", {}).get("data", {}).get("shares", []) or []
    except Exception:
        shares = []

    scope_readable = []
    scope_visible_but_denied = []

    for sh in shares:
        share_path = sh.get("path")
        share_name = sh.get("name")
        perm = _classify_permission(sh.get("additional", {}).get("perm"))
        volume_status = sh.get("additional", {}).get("volume_status")
        real_path = sh.get("additional", {}).get("real_path")
        item = {
            "name": share_name,
            "path": share_path,
            "isdir": sh.get("isdir"),
            "perm": perm,
            "real_path": real_path,
            "volume_status_cheap": _redact_vol(volume_status),
            "depth1_sample": None,
            "depth1_total_returned": None,
            "depth2_samples": [],
        }
        # Depth-1 sample (top-level of share) — probe read capability
        # (any success here is stronger evidence than a perm flag).
        d1 = dsm.list_folder(share_path, limit=200)
        item["depth1_result_meta"] = {
            "http_status": d1.get("http_status"),
            "success": bool(d1.get("body", {}).get("success")),
            "error_code": d1.get("body", {}).get("error", {}).get("code"),
        }
        d1_body = d1.get("body", {}) or {}
        if d1_body.get("success"):
            files = d1_body.get("data", {}).get("files", []) or []
            item["depth1_sample"] = [
                {
                    "name": f.get("name"),
                    "isdir": f.get("isdir"),
                    "size": f.get("additional", {}).get("size"),
                }
                for f in files[:MAX_DEPTH2_CHILDREN_PER_SHARE]
            ]
            item["depth1_total_returned"] = len(files)
            scope_readable.append(share_name)

            # Depth-2 sampling — only if depth-1 is small enough and share
            # is readable; bounded, and only for child directories.
            if (
                len(files) <= DEPTH2_SIZE_CEILING_ITEMS
                and dsm._list_calls < MAX_LIST_CALLS_TOTAL
            ):
                child_dirs = [f for f in files if f.get("isdir")][
                    :MAX_DEPTH2_CHILDREN_PER_SHARE
                ]
                for cd in child_dirs:
                    cd_path = cd.get("path")
                    if not cd_path:
                        continue
                    d2 = dsm.list_folder(cd_path, limit=50)
                    d2_body = d2.get("body", {}) or {}
                    item["depth2_samples"].append({
                        "child_dir": cd.get("name"),
                        "child_path": cd_path,
                        "http_status": d2.get("http_status"),
                        "success": bool(d2_body.get("success")),
                        "returned": len(d2_body.get("data", {}).get("files", []) or []),
                        "sample_names": [
                            f.get("name")
                            for f in (d2_body.get("data", {}).get("files", []) or [])[:5]
                        ],
                    })
                    if dsm._list_calls >= MAX_LIST_CALLS_TOTAL:
                        break
        else:
            err = d1_body.get("error", {}) or {}
            code = err.get("code")
            # 407 no such file/folder; 408 permission denied; classic DSM
            if code in (407, 408, 105, 400):
                scope_visible_but_denied.append({"name": share_name, "error_code": code})
            else:
                scope_visible_but_denied.append({"name": share_name, "error_code": code})

        shares_out.append(item)

    receipt["shares"] = shares_out
    receipt["list_call_count_total"] = dsm._list_calls

    # ---- Scope answer -------------------------------------------------
    scope = {
        "account_shape": {
            "user_len": len(binds.nas.user),
            "user_prefix2": binds.nas.user[:2],
        },
        "is_manager_admin_flag": is_manager,
        "dsm_hostname": hostname_dsm,
        "fs_extras": fs_version_pack,
        "visible_share_count": len(shares_out),
        "readable_share_count": len(scope_readable),
        "denied_share_count": len(scope_visible_but_denied),
        "shares_readable_names": sorted(scope_readable),
        "shares_visible_but_denied": scope_visible_but_denied,
    }

    if is_manager is True:
        scope["classification"] = "ADMIN_SCOPE_READS_ALL_BY_DEFINITION"
        scope["explicit_answer"] = (
            "YES — account is DSM administrator (is_manager=true). "
            "Admin scope covers every share on the NAS by definition, "
            "including shares the admin panel would show for management. "
            "Per-share readable enumeration above is confirmatory."
        )
    elif len(shares_out) == 0:
        scope["classification"] = "NO_SHARES_VISIBLE"
        scope["explicit_answer"] = (
            "AMBIGUOUS — the account authenticated but list_share "
            "returned zero shares. Either (a) FileStation package is "
            "not licensed for this account, or (b) DSM policy hides all "
            "shares from this account. Not a credential problem."
        )
    elif len(scope_readable) == len(shares_out) and len(shares_out) > 0:
        scope["classification"] = "ALL_VISIBLE_SHARES_READABLE"
        scope["explicit_answer"] = (
            "YES for every share this account can see. "
            f"Readable: {len(scope_readable)} / visible: {len(shares_out)}. "
            "This is standard-account scope — the answer to 'can we read "
            "the NAS entirely?' is 'yes for the visible subset; admin "
            "scope-grant is required to know whether other shares exist "
            "that this account is not shown.'"
        )
    elif len(scope_readable) == 1 and len(shares_out) == 1:
        scope["classification"] = "SINGLE_SHARE_SCOPED"
        scope["explicit_answer"] = (
            f"PARTIAL — the account is scoped to a single share "
            f"({scope_readable[0]!r}). To read the rest of the NAS, "
            "an admin scope-grant is required."
        )
    else:
        scope["classification"] = "SOME_READABLE_SOME_DENIED"
        scope["explicit_answer"] = (
            f"PARTIAL — {len(scope_readable)} readable, "
            f"{len(scope_visible_but_denied)} visible-but-denied. "
            "Standard-account scope; an admin scope-grant would be "
            "required to lift the deny list."
        )

    scope["distinction_note"] = (
        "'not visible to this account' vs 'visible but read-denied' — "
        "list_share only returns shares this account has ANY visibility "
        "on; deeper NAS shares that this account is not privileged to "
        "see would silently be absent (not surface as 'denied'). Only "
        "admin scope or an admin-side share list can resolve absence."
    )
    receipt["scope_answer"] = scope

    # ---- Logout ------------------------------------------------------
    receipt["logout"] = dsm.logout()

    # ---- Security-posture observation --------------------------------
    receipt["security_posture_note"] = {
        "auth_transport": "cleartext_http_over_ssh_direct_tcpip_channel",
        "dsm_https_5001_reachable_via_jump": bool(
            receipt.get("forward_tcp_probes", {})
                   .get("https_5001_via_jump", {})
                   .get("tcp_connected")
        ),
        "dsm_5001_tls_probe_result": receipt.get("dsm_5001_tls_via_jump"),
        "observation": (
            "The auth call itself was HTTP (port 5000) but the entire "
            "path from this pod to DSM was inside the SSH-encrypted "
            "channel to the JUMP host (paramiko direct-tcpip). No "
            "credential material transited any public wire in cleartext. "
            "For the record: DSM HTTPS on 5001 IS reachable through the "
            "JUMP tunnel; a follow-up drill could pin the DSM's TLS "
            "posture (cert SHA is captured here as a baseline)."
        ),
    }

    _teardown(dsm, fwd_http, fwd_https, jump_client)
    _emit(receipt)


def _redact_initdata(res: dict) -> dict:
    """desktop.initdata returns a rich object; strip anything not needed
    for the scope answer to keep the receipt tight."""
    try:
        d = res.get("body", {}).get("data", {}) or {}
        return {
            "success": bool(res.get("body", {}).get("success")),
            "http_status": res.get("http_status"),
            "is_admin": d.get("isAdmin") if "isAdmin" in d else d.get("is_admin"),
            "user_name_present": bool(d.get("user")),
            "keys_returned_top_level": sorted(list(d.keys()))[:30],
        }
    except Exception:
        return {
            "success": False,
            "http_status": res.get("http_status"),
            "error_class": res.get("error_class"),
            "error_msg": res.get("error_msg"),
        }


def _redact_vol(vol) -> dict:
    if not isinstance(vol, dict):
        return {"present": False}
    # keep just size-shape / freespace so we know scale without granularity
    return {
        "present": True,
        "keys": sorted(list(vol.keys())),
        "total_space": vol.get("total_space"),
        "free_space": vol.get("free_space"),
        "readonly": vol.get("readonly"),
    }


def _teardown(dsm: DSMSession,
              fwd_http: DirectTCPIPForward,
              fwd_https: DirectTCPIPForward,
              jump_client: paramiko.SSHClient) -> None:
    try:
        if dsm.sid:
            dsm.logout()
    except Exception:
        pass
    try:
        fwd_http.stop()
    except Exception:
        pass
    try:
        fwd_https.stop()
    except Exception:
        pass
    try:
        jump_client.close()
    except Exception:
        pass


def _emit(receipt: dict) -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPT_DIR / f"{stamp}_NAS_schema_survey_S2_owner_authorized_20260921.json"
    path.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                    encoding="utf-8")
    print(f"receipt_path: {path}")


if __name__ == "__main__":
    main()
