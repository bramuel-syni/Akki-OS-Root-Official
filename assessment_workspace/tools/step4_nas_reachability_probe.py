"""JUMP-side TCP reachability probe for NAS-protocol ports.

Owner-authorized ops task 2026-09-13: locate + reach NAS behind JUMP.
Read-only. `bash /dev/tcp` connect only; no protocol traffic sent.
Candidates: JUMP itself, RADIO (bastion CSV row 1 col 1), Huawei RDS
(known-reachable at :3306), plus WEEGO + VIUSASA host lists.

Position-redaction only. No CSV cell value is echoed to stdout or into the
receipt. Candidates are logged by opaque handle (e.g. "RADIO",
"WEEGO_HOST_2") when they come from a credentials file; publicly-known
handles (JUMP=159.138.173.250, Huawei RDS=159.138.162.146) already banked
in prior receipts are kept as-is.
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

# NAS-protocol ports (owner-directed set).
NAS_PORTS = {
    22: "SSH",
    111: "NFS_PORTMAP",
    445: "SMB",
    548: "AFP",
    873: "RSYNC",
    2049: "NFS",
    5000: "DSM_HTTP",
    5001: "DSM_HTTPS",
    5005: "WEBDAV_ALT",
    5006: "WEBDAV_ALT_TLS",
}


def _is_ipv4(s: str) -> bool:
    try:
        ipaddress.IPv4Address(s)
        return True
    except Exception:
        return False


def load_candidates():
    """Return (candidates, jump_creds).

    candidates: list of {handle, ip, source}. ip is the plain IPv4 for probing
    (needed on the wire); handle is the opaque public label the receipt uses
    when the ip came from a credentials file.
    jump_creds: {ip, user, cred} kept in-memory only.
    """
    # JUMP + RADIO from bastion CSV (row 1 = ip line, row 2 = user, row 3 = cred).
    with BASTION_CSV.open() as f:
        b = list(csv.reader(f))
    jump_ip = b[1][0]
    radio_ip = b[1][1]
    jump_user = b[2][0]
    jump_cred = b[3][0]

    candidates = []
    # JUMP handle is public (already in prior receipts).
    candidates.append({"handle": "JUMP", "ip": jump_ip, "public_handle_ok": True,
                       "source": "bastion_csv[1,0]"})
    # RADIO: cell value from credentials file - opaque handle only.
    candidates.append({"handle": "RADIO", "ip": radio_ip, "public_handle_ok": False,
                       "source": "bastion_csv[1,1]"})

    # Huawei RDS (analytics + weego) - public handle from prior receipts.
    candidates.append({"handle": "HUAWEI_RDS_1", "ip": "159.138.162.146",
                       "public_handle_ok": True, "source": "prior_receipt"})

    # Additional hosts from db_credentials.csv (viusasa) - values only, opaque handles.
    if DB_CSV.exists():
        with DB_CSV.open() as f:
            rows = list(csv.reader(f))
        seen = {c["ip"] for c in candidates}
        for ri, r in enumerate(rows):
            for ci, cell in enumerate(r):
                cell = cell.strip()
                if _is_ipv4(cell) and cell not in seen:
                    candidates.append({
                        "handle": f"VIUSASA_HOST_{len(candidates)+1}",
                        "ip": cell,
                        "public_handle_ok": False,
                        "source": f"db_credentials.csv[{ri},{ci}]",
                    })
                    seen.add(cell)

    # WEEGO hosts.
    if WEEGO_CSV.exists():
        with WEEGO_CSV.open() as f:
            rows = list(csv.reader(f))
        seen = {c["ip"] for c in candidates}
        for ri, r in enumerate(rows):
            for ci, cell in enumerate(r):
                cell = cell.strip()
                if _is_ipv4(cell) and cell not in seen:
                    candidates.append({
                        "handle": f"WEEGO_HOST_{len(candidates)+1}",
                        "ip": cell,
                        "public_handle_ok": False,
                        "source": f"db_credentials_2.csv[{ri},{ci}]",
                    })
                    seen.add(cell)

    jump_creds = {"ip": jump_ip, "user": jump_user, "cred": jump_cred}
    return candidates, jump_creds


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
    # Position-based scrub: strip the exact JUMP password if it appears.
    if pw:
        stdout = stdout.replace(pw, "<SCRUBBED_JUMP_CRED>")
    exit_code = os.WEXITSTATUS(status) if status else None
    return {"exit_code": exit_code, "stdout_scrubbed": stdout}


def main():
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"probe start {at_iso}")

    candidates, jump = load_candidates()
    print(f"candidates: {len(candidates)}")
    for c in candidates:
        # DO NOT print IP for non-public handles.
        if c["public_handle_ok"]:
            print(f"  {c['handle']:20s} ip={c['ip']} source={c['source']}")
        else:
            print(f"  {c['handle']:20s} ip=<masked:ipv4> source={c['source']}")

    # Build one big bash script; probe every (candidate, port).
    parts = []
    for c in candidates:
        for p, proto in NAS_PORTS.items():
            tag = f"{c['handle']}:{p}"
            parts.append(f"echo '===TAG:{tag}==='")
            parts.append(
                f"(timeout 3 bash -c 'exec 3<>/dev/tcp/{c['ip']}/{p} && echo OPEN' "
                f"2>&1 || echo CLOSED_OR_TIMEOUT)"
            )
            parts.append(f"echo '===END:{tag}==='")
    script = "; ".join(parts)

    result = _run_ssh(jump["user"], jump["ip"], jump["cred"], script, timeout=600)
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
                if "OPEN" == content:
                    verdict = "OPEN"
                elif "CLOSED_OR_TIMEOUT" in content:
                    verdict = "CLOSED_OR_TIMEOUT"
                elif "No route" in content or "no route" in content:
                    verdict = "NO_ROUTE"
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
    print("=== NAS reachability matrix ===")
    handles_sorted = sorted({t.split(":")[0] for t in parsed})
    for h in handles_sorted:
        opens = [t for t in parsed if t.startswith(h + ":") and parsed[t]["verdict"] == "OPEN"]
        others = [t for t in parsed if t.startswith(h + ":") and parsed[t]["verdict"] != "OPEN"]
        print(f"  {h:20s} OPEN={[t.split(':')[1] for t in opens]}  "
              f"other={len(others)}")

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    # Build receipt: for non-public handles we store handle+source only.
    receipt_candidates = []
    for c in candidates:
        entry = {"handle": c["handle"], "source": c["source"]}
        if c["public_handle_ok"]:
            entry["ip"] = c["ip"]
        else:
            # sha256 of ip is deterministic + non-reversible for the small
            # IPv4 space so we salt with the file sha256 to prevent trivial
            # rainbow lookup.
            salt = hashlib.sha256(BASTION_CSV.read_bytes()).hexdigest()[:16]
            entry["ip_sha256_salted"] = hashlib.sha256(
                (salt + c["ip"]).encode()
            ).hexdigest()[:16]
        receipt_candidates.append(entry)

    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_4_NAS_REACHABILITY_PROBE_FROM_JUMP",
        "method": "bash /dev/tcp exec 3<>/dev/tcp/HOST/PORT (read-only TCP connect); 3s bounded timeout per probe",
        "read_only": True,
        "position_redaction": True,
        "ports_probed": NAS_PORTS,
        "candidates": receipt_candidates,
        "matrix_by_handle_port": parsed,
    }
    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step4_nas_reachability.json"
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
