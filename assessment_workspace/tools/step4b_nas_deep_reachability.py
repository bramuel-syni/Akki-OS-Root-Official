"""Second-pass NAS reachability probe from JUMP.

Adds:
  1) Expanded port set: FTP/FTPS, NetBIOS, HTTP-alt, Synology mobile,
     iSCSI, LDAPS, NAS-DAAP, Syncthing.
  2) ICMP ping (1 packet, 2s deadline) per candidate for layer-3 sanity.
  3) Repeated TCP-connect (3 attempts × 3s) on RADIO ports to distinguish
     "flaky/rate-limited/half-open" from "hard-closed".
Read-only. Position-redaction preserved.
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import ipaddress
import json
import os
import pty
import select
import sys
import time
from pathlib import Path

BASTION_CSV = Path("/app/backend/estate_keys/bastion/jump_server_radio_system.csv")
DB_CSV = Path("/app/backend/estate_keys/data_sources/db_credentials.csv")
WEEGO_CSV = Path("/app/backend/estate_keys/data_sources/db_credentials_2.csv")
KNOWN_HOSTS = Path("/app/backend/estate_keys/known_hosts")
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/nas_connect_receipts")

# Ports from first pass + additions.
NAS_PORTS = {
    21: "FTP",
    22: "SSH",
    111: "NFS_PORTMAP",
    137: "NBNS",
    139: "NBSS_SMB",
    445: "SMB",
    548: "AFP",
    873: "RSYNC",
    990: "FTPS",
    2049: "NFS",
    3260: "ISCSI",
    5000: "DSM_HTTP",
    5001: "DSM_HTTPS",
    5005: "WEBDAV_ALT",
    5006: "WEBDAV_ALT_TLS",
    5555: "DSM_MOBILE",
    6690: "DSM_DRIVE",
    8080: "HTTP_ALT",
    8384: "SYNCTHING",
    8443: "HTTPS_ALT",
}


def _is_ipv4(s: str) -> bool:
    try:
        ipaddress.IPv4Address(s); return True
    except Exception:
        return False


def load_candidates():
    with BASTION_CSV.open() as f:
        b = list(csv.reader(f))
    jump_ip = b[1][0]
    radio_ip = b[1][1]
    jump_user = b[2][0]
    jump_cred = b[3][0]

    cands = [
        {"handle": "JUMP", "ip": jump_ip, "public_handle_ok": True,
         "source": "bastion_csv[1,0]"},
        {"handle": "RADIO", "ip": radio_ip, "public_handle_ok": False,
         "source": "bastion_csv[1,1]"},
        {"handle": "HUAWEI_RDS_1", "ip": "159.138.162.146",
         "public_handle_ok": True, "source": "prior_receipt"},
    ]
    seen = {c["ip"] for c in cands}
    for path, tag in [(DB_CSV, "VIUSASA"), (WEEGO_CSV, "WEEGO")]:
        if not path.exists():
            continue
        with path.open() as f:
            rows = list(csv.reader(f))
        for ri, r in enumerate(rows):
            for ci, cell in enumerate(r):
                cell = cell.strip()
                if _is_ipv4(cell) and cell not in seen:
                    cands.append({
                        "handle": f"{tag}_HOST_{len(cands)+1}",
                        "ip": cell,
                        "public_handle_ok": False,
                        "source": f"{path.name}[{ri},{ci}]",
                    })
                    seen.add(cell)
    return cands, {"ip": jump_ip, "user": jump_user, "cred": jump_cred}


def _run_ssh(user, ip, pw, remote_cmd, timeout=180):
    argv = [
        "ssh",
        "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
        "-o", "StrictHostKeyChecking=yes",
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password,keyboard-interactive",
        "-o", "NumberOfPasswordPrompts=1",
        "-o", "ConnectTimeout=15",
        "-o", "LogLevel=ERROR",
        f"{user}@{ip}",
        remote_cmd,
    ]
    pid, fd = pty.fork()
    if pid == 0:
        try:
            os.execvp("ssh", argv)
        except Exception as exc:
            print(f"execvp_failed: {exc!r}", flush=True)
            os._exit(127)
    pw_written = False
    consumed = 0
    chunks = []
    deadline = time.time() + timeout
    status = None
    while time.time() < deadline:
        r, _, _ = select.select([fd], [], [], 0.5)
        if fd in r:
            try:
                chunk = os.read(fd, 8192)
            except OSError:
                break
            if not chunk:
                break
            chunks.append(chunk)
            joined = b"".join(chunks)
            unread = joined[consumed:]
            if b"password:" in unread.lower() and not pw_written:
                os.write(fd, (pw + "\n").encode())
                pw_written = True
                consumed = len(joined)
                chunks.append(b"\n<pw_written>\n")
        try:
            waited_pid, s = os.waitpid(pid, os.WNOHANG)
            if waited_pid != 0:
                status = s
                break
        except ChildProcessError:
            break
    try:
        os.close(fd)
    except OSError:
        pass
    stdout = b"".join(chunks).decode("utf-8", errors="replace")
    if pw:
        stdout = stdout.replace(pw, "<SCRUBBED_JUMP_CRED>")
    exit_code = os.WEXITSTATUS(status) if status else None
    return {"exit_code": exit_code, "stdout_scrubbed": stdout}


def main():
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"deep probe start {at_iso}")

    cands, jump = load_candidates()
    print(f"candidates: {len(cands)}")

    parts = []
    # 1) ICMP ping per candidate: 1 packet, 2s deadline.
    for c in cands:
        tag = f"PING:{c['handle']}"
        parts.append(f"echo '===TAG:{tag}==='")
        parts.append(f"(timeout 3 ping -c 1 -W 2 {c['ip']} >/dev/null 2>&1 && echo ICMP_REPLY || echo ICMP_NO_REPLY)")
        parts.append(f"echo '===END:{tag}==='")
    # 2) TCP port matrix per (candidate, port).
    for c in cands:
        for p, _proto in NAS_PORTS.items():
            tag = f"TCP:{c['handle']}:{p}"
            parts.append(f"echo '===TAG:{tag}==='")
            parts.append(
                f"(timeout 3 bash -c 'exec 3<>/dev/tcp/{c['ip']}/{p} && echo OPEN' "
                f"2>&1 || echo CLOSED_OR_TIMEOUT)"
            )
            parts.append(f"echo '===END:{tag}==='")
    # 3) Repeated TCP:22 to RADIO — 5 attempts × 3s + short sleep between.
    radio = next((c for c in cands if c["handle"] == "RADIO"), None)
    if radio:
        for i in range(5):
            tag = f"TCP_RETRY:RADIO:22:r{i}"
            parts.append(f"echo '===TAG:{tag}==='")
            parts.append(
                f"(timeout 4 bash -c 'exec 3<>/dev/tcp/{radio['ip']}/22 && echo OPEN' "
                f"2>&1 || echo CLOSED_OR_TIMEOUT)"
            )
            parts.append(f"echo '===END:{tag}==='")
            parts.append("sleep 1")

    script = "; ".join(parts)
    result = _run_ssh(jump["user"], jump["ip"], jump["cred"], script, timeout=900)
    print(f"exit_code={result['exit_code']}")

    parsed = {}
    cur = None
    buf = []
    for line in result["stdout_scrubbed"].splitlines():
        s = line.strip()
        if s.startswith("===TAG:") and s.endswith("==="):
            cur = s[len("===TAG:"):-len("===")]
            buf = []
        elif s.startswith("===END:") and s.endswith("==="):
            if cur:
                content = "\n".join(buf).strip()
                if content in ("OPEN", "ICMP_REPLY"):
                    verdict = content
                elif content in ("CLOSED_OR_TIMEOUT", "ICMP_NO_REPLY"):
                    verdict = content
                elif "refused" in content.lower():
                    verdict = "REFUSED"
                else:
                    verdict = "OTHER"
                parsed[cur] = {"verdict": verdict, "raw": content[:200]}
            cur = None
            buf = []
        elif cur is not None:
            buf.append(line)

    print()
    print("=== ICMP (layer-3) ===")
    for c in cands:
        tag = f"PING:{c['handle']}"
        v = parsed.get(tag, {"verdict": "MISSING"})["verdict"]
        print(f"  {c['handle']:20s} -> {v}")
    print()
    print("=== TCP matrix by handle ===")
    handles = [c["handle"] for c in cands]
    for h in handles:
        opens = [t for t in parsed if t.startswith(f"TCP:{h}:") and parsed[t]["verdict"] == "OPEN"]
        print(f"  {h:20s} OPEN_ports={[t.split(':')[-1] for t in opens]}")
    print()
    print("=== RADIO:22 retry series ===")
    for i in range(5):
        tag = f"TCP_RETRY:RADIO:22:r{i}"
        v = parsed.get(tag, {"verdict": "MISSING"})["verdict"]
        print(f"  attempt {i}: {v}")

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_candidates = []
    salt = hashlib.sha256(BASTION_CSV.read_bytes()).hexdigest()[:16]
    for c in cands:
        entry = {"handle": c["handle"], "source": c["source"]}
        if c["public_handle_ok"]:
            entry["ip"] = c["ip"]
        else:
            entry["ip_sha256_salted"] = hashlib.sha256(
                (salt + c["ip"]).encode()
            ).hexdigest()[:16]
        receipt_candidates.append(entry)

    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_4B_NAS_DEEP_REACHABILITY_FROM_JUMP",
        "method": "ICMP ping (1 pkt / 2s) + bash /dev/tcp (3s timeout per port) + 5-round retry on RADIO:22",
        "read_only": True,
        "position_redaction": True,
        "ports_probed": NAS_PORTS,
        "candidates": receipt_candidates,
        "matrix": parsed,
    }
    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step4b_nas_deep_reachability.json"
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
