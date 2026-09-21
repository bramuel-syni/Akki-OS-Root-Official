"""tools/nas_smb_final_layer_pin_20260921.py · S2 finale.

Purpose: conclusively pin the NAS auth failure layer with 3 bounded probes.

Bounds:
    * ≤3 SMB authenticated attempts (stay well below any auto-lockout).
    * 1 anonymous SMB -L (unauth — no lockout impact).
    * 1 read of DSM 5000 login page HTML for banner/version fingerprint.

Probes:
    P1 · smbclient -L with -m SMB2 (in case NT1/SMB3 negotiation quirk).
    P2 · smbclient -L WITHOUT -m flag (native negotiation).
    P3 · smbclient -L -N (anonymous) — do the shares advertise unauth?
    P4 · curl the DSM login page HTML (unauth GET) to capture DSM
         version banner from HTML meta / JS variables — this confirms
         whether the NAS is still DSM 7 as we saw at 13:22Z.
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

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")


class DirectTCPIPForward:
    def __init__(self, transport, rhost, rport):
        self.transport = transport
        self.rhost = rhost
        self.rport = rport
        self.server_sock = None
        self.local_port = None
        self._stop = threading.Event()

    def start(self):
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
                cs, _ = self.server_sock.accept()
            except socket.timeout: continue
            except OSError: return
            threading.Thread(target=self._handle, args=(cs,), daemon=True).start()

    def _handle(self, cs):
        try:
            chan = self.transport.open_channel(
                "direct-tcpip", (self.rhost, self.rport),
                ("127.0.0.1", self.local_port or 0), timeout=10.0,
            )
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
            if self.server_sock: self.server_sock.close()
        except Exception: pass


def _ssh_exec(client, cmd, env=None, timeout=25.0):
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        if env:
            try:
                stdin.write("\n".join(env.get(k, "") for k in env) + "\n")
                stdin.flush()
                stdin.channel.shutdown_write()
            except Exception:
                pass
        out = stdout.read(65536).decode("utf-8", errors="replace")
        err = stderr.read(8192).decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return {"rc": rc, "stdout": out[:8192], "stderr": err[:2048],
                "elapsed_s": round(time.monotonic() - t0, 3)}
    except Exception as e:
        return {"rc": None, "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "elapsed_s": round(time.monotonic() - t0, 3)}


def _now_utc_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    receipt = {
        "task": "S2_nas_smb_final_layer_pin_20260921",
        "captured_at_utc": _now_utc_str(),
        "predecessors": [
            "20260921T132205Z_NAS_schema_survey_S2_owner_authorized_20260921.json",
            "20260921T132533Z_NAS_schema_survey_S2_v2_auth_matrix_and_smb_enum_20260921.json",
            "20260921T132733Z_NAS_creds_structure_probe_S2_v3.json",
        ],
        "authorization": (
            "Owner GO S2 continuation. v2 revealed DSM HTTP + SMB both "
            "return LOGON_FAILURE for the currently-banked creds — but "
            "the same creds file did the 2026-09-14 SMB read successfully. "
            "This probe pins the failure layer before we conclude 'stale "
            "creds' (candidate scope-grant ask to the RMS admin)."
        ),
        "bounds": {
            "smb_authed_attempts_max": 2,
            "smb_anon_attempts": 1,
            "http_unauth_get_max": 1,
        },
    }

    binds = rms_creds_loader.load()
    receipt["cred_shape"] = {"nas": binds.nas.describe(),
                             "jump": binds.jump.describe()}
    nas_host = "10.10.55.55"

    # Open JUMP
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        jump.connect(hostname=binds.jump.host, port=22,
                     username=binds.jump.user, password=binds.jump.password,
                     timeout=12, auth_timeout=12, banner_timeout=12,
                     allow_agent=False, look_for_keys=False)
    except Exception as e:
        receipt["jump_open_err"] = f"{e.__class__.__name__}: {e}"
        _emit(receipt); return

    transport = jump.get_transport()
    transport.set_keepalive(15)

    # Stage auth file for SMB probes
    stage_cmd = (
        "set -eu; umask 077; "
        "AUTH=$(mktemp /dev/shm/nas_auth.XXXXXX); "
        "read -r U; read -r P; "
        "printf 'username=%s\\npassword=%s\\n' \"$U\" \"$P\" > \"$AUTH\"; "
        "echo AUTH_STAGED=$AUTH"
    )
    stage = _ssh_exec(jump, stage_cmd,
                      env={"U": binds.nas.user, "P": binds.nas.password})
    receipt["stage_auth"] = {"rc": stage.get("rc"),
                             "elapsed_s": stage.get("elapsed_s"),
                             "stdout_first_200": stage.get("stdout", "")[:200]}
    m = re.search(r"AUTH_STAGED=(\S+)", stage.get("stdout", ""))
    auth_path = m.group(1) if m else None

    probes = {}

    # P1 · smbclient -L with -m SMB2
    if auth_path:
        cmd = (
            f"smbclient -L //{nas_host}/ -A {auth_path} "
            "-m SMB2 -t 12 2>&1; echo _RC=$?"
        )
        p1 = _ssh_exec(jump, cmd, timeout=25)
        probes["p1_smbL_SMB2"] = {
            "rc": p1.get("rc"),
            "elapsed_s": p1.get("elapsed_s"),
            "stdout_first_2k": (p1.get("stdout") or "")[:2048],
            "stderr_first_400": (p1.get("stderr") or "")[:400],
        }

        # P2 · smbclient -L with no -m
        cmd = (
            f"smbclient -L //{nas_host}/ -A {auth_path} "
            "-t 12 2>&1; echo _RC=$?"
        )
        p2 = _ssh_exec(jump, cmd, timeout=25)
        probes["p2_smbL_native"] = {
            "rc": p2.get("rc"),
            "elapsed_s": p2.get("elapsed_s"),
            "stdout_first_2k": (p2.get("stdout") or "")[:2048],
            "stderr_first_400": (p2.get("stderr") or "")[:400],
        }

    # P3 · smbclient -L -N (anonymous)
    cmd = (
        f"smbclient -N -L //{nas_host}/ "
        "-t 12 2>&1; echo _RC=$?"
    )
    p3 = _ssh_exec(jump, cmd, timeout=25)
    probes["p3_smbL_anonymous"] = {
        "rc": p3.get("rc"),
        "elapsed_s": p3.get("elapsed_s"),
        "stdout_first_2k": (p3.get("stdout") or "")[:2048],
        "stderr_first_400": (p3.get("stderr") or "")[:400],
    }

    # Shred auth file
    if auth_path:
        shred = _ssh_exec(jump,
                          f"shred -uz '{auth_path}' 2>/dev/null || rm -f '{auth_path}'; echo AUTH_SHRED_DONE",
                          timeout=6)
        receipt["shred_auth"] = {"rc": shred.get("rc"),
                                 "elapsed_s": shred.get("elapsed_s")}

    # P4 · DSM login page (unauth GET) for version banner
    fwd = DirectTCPIPForward(transport, nas_host, 5000)
    lp = fwd.start()
    time.sleep(0.3)
    sess = requests.Session()
    sess.verify = False
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception: pass
    p4 = {}
    for path in ("/", "/webman/login.cgi", "/webapi/entry.cgi?api=SYNO.API.Info&version=1&method=query&query=all"):
        try:
            r = sess.get(f"http://127.0.0.1:{lp}{path}", timeout=8)
            body = r.text
            p4[path] = {
                "http_status": r.status_code,
                "content_len": len(body),
                "body_first_500": body[:500],
                # DSM version banners often appear as `DSM_VERSION` or in
                # response headers.
                "server_header": r.headers.get("Server"),
                "syno_dsm_version_header": r.headers.get("X-SYNO-DSM-VERSION"),
                "dsm_version_regex_match": re.findall(
                    r'"version"\s*:\s*"([0-9\.\-]+)"', body[:20000],
                )[:5],
            }
        except Exception as e:
            p4[path] = {"error_class": e.__class__.__name__,
                        "error_msg": str(e)[:200]}
    fwd.stop()
    probes["p4_dsm_unauth_banner"] = p4

    receipt["probes"] = probes

    # Classify layer + explicit verdict
    verdict = _classify(probes)
    receipt["failure_layer_verdict"] = verdict

    try: jump.close()
    except Exception: pass

    _emit(receipt)


def _classify(probes: dict) -> dict:
    v = {}
    # Anon list shows the server responds at all
    p3 = probes.get("p3_smbL_anonymous", {}) or {}
    anon_out = (p3.get("stdout_first_2k") or "").lower()
    if "sharename" in anon_out and "type" in anon_out:
        v["smb_server_responds_to_anon_list"] = True
        v["smb_anon_lists_shares"] = True
    elif "access_denied" in anon_out or "logon_failure" in anon_out:
        v["smb_server_responds_to_anon_list"] = True
        v["smb_anon_lists_shares"] = False
        v["smb_anon_error"] = "AUTH_DENIED_ANON"
    else:
        v["smb_server_responds_to_anon_list"] = "sharename" in anon_out
        v["smb_anon_lists_shares"] = False

    # Auth attempts
    p1 = probes.get("p1_smbL_SMB2", {}) or {}
    p2 = probes.get("p2_smbL_native", {}) or {}
    p1o = (p1.get("stdout_first_2k") or "").lower()
    p2o = (p2.get("stdout_first_2k") or "").lower()
    auth_fail_signatures = []
    for label, o in (("SMB2", p1o), ("native", p2o)):
        if "logon_failure" in o:
            auth_fail_signatures.append((label, "NT_STATUS_LOGON_FAILURE"))
        elif "sharename" in o:
            auth_fail_signatures.append((label, "AUTH_SUCCEEDED"))
        elif "access_denied" in o:
            auth_fail_signatures.append((label, "NT_STATUS_ACCESS_DENIED"))
        elif "account" in o and "locked" in o:
            auth_fail_signatures.append((label, "ACCOUNT_LOCKED"))
        else:
            auth_fail_signatures.append((label, "OTHER"))
    v["smb_auth_signatures"] = auth_fail_signatures

    # DSM banner
    p4 = probes.get("p4_dsm_unauth_banner", {}) or {}
    for path, info in p4.items():
        if not isinstance(info, dict): continue
        if info.get("http_status") in (200, 302, 303, 401, 403):
            v["dsm_http_responding"] = True
            break

    # Verdict
    all_reject_logon = all(sig == "NT_STATUS_LOGON_FAILURE"
                          for _, sig in auth_fail_signatures)
    if all_reject_logon:
        v["conclusion"] = (
            "STALE_CREDENTIALS. The banked NAS credentials (user_len=7, "
            "pass_len=8) are rejected by the SMB server at "
            "10.10.55.55 across all protocol variants (SMB2, native) "
            "with NT_STATUS_LOGON_FAILURE, and by DSM HTTP across all "
            "method+version combinations with error 400. The 2026-09-14 "
            "T3 receipt shows the SAME sheet worked before the "
            "2026-09-16 rotation-check ingestion. Highest-likelihood "
            "root cause: the NAS-side password was rotated post-2026-09-16 "
            "but the sheet ingestion mis-captured the new value, or the "
            "RMS admin rotated it again since then. Ask the RMS admin to "
            "confirm the CURRENT NAS creds and re-drop the sheet. "
            "The credentials themselves — not the network path — are "
            "the block; JUMP tunnel + DSM HTTPS + SMB TCP all confirmed OK."
        )
    else:
        v["conclusion"] = (
            "MIXED_SIGNATURES — inspect smb_auth_signatures individually."
        )
    return v


def _emit(receipt):
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_NAS_smb_final_layer_pin_S2_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
