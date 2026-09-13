"""JUMP-side TCP reachability probe to candidate DB IPs.

Read-only. Uses bash /dev/tcp for TCP-connect only (no protocol traffic).
Reports OPEN/REFUSED/TIMEOUT per (host, port).
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import pty
import select
import sys
import time
from pathlib import Path


CSV_PATH = Path("/app/backend/estate_keys/bastion/jump_server_radio_system.csv")
KNOWN_HOSTS = Path("/app/backend/estate_keys/known_hosts")
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/db_connect_receipts")

# Candidates from db_credentials_2.csv (WEEGO)
CANDIDATE_HOSTS = [
    "159.138.162.146",   # analytics
    "159.138.164.124",   # citizen_digital
    "110.238.75.83",     # citizen_digital (alt)
    "203.123.83.144",    # citizen-pulse
]
CANDIDATE_PORTS = [3306, 5432, 27017]


def load_jump():
    with CSV_PATH.open() as f:
        rows = list(csv.reader(f))
    return {"ip": rows[1][0], "user": rows[2][0], "cred": rows[3][0]}


def _run_ssh(user, ip, pw, remote_cmd, timeout=45):
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
        stdout = stdout.replace(pw, "<SCRUBBED_SECRET>")
    exit_code = os.WEXITSTATUS(status) if status else None
    return {"exit_code": exit_code, "stdout_scrubbed": stdout}


def main():
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"probe start {at_iso}")

    j = load_jump()

    # Build bash script: for each (host, port), attempt a bounded connect
    # via bash /dev/tcp — the shell built-in, no clients required. Timeout
    # via `timeout 3`.
    parts = []
    for h in CANDIDATE_HOSTS:
        for p in CANDIDATE_PORTS:
            tag = f"{h}:{p}"
            parts.append(f"echo '===TAG:{tag}==='")
            parts.append(
                f"(timeout 3 bash -c 'exec 3<>/dev/tcp/{h}/{p} && echo OPEN' "
                f"2>&1 || echo CLOSED_OR_TIMEOUT)"
            )
            parts.append(f"echo '===END:{tag}==='")
    script = "; ".join(parts)

    result = _run_ssh(j["user"], j["ip"], j["cred"], script, timeout=120)
    print(f"exit_code={result['exit_code']}")

    # parse
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
    print("=== reachability matrix ===")
    for tag, v in parsed.items():
        print(f"  {tag:30s} -> {v['verdict']:20s} raw={v['raw'][:80]!r}")

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_3_REACHABILITY_PROBE_FROM_JUMP",
        "method": "bash /dev/tcp exec 3<>/dev/tcp/HOST/PORT (read-only TCP connect)",
        "read_only": True,
        "candidates": {
            "hosts_from": "db_credentials_2.csv (WEEGO)",
            "hosts": CANDIDATE_HOSTS,
            "ports": {"3306": "MySQL/MariaDB", "5432": "PostgreSQL", "27017": "MongoDB"},
        },
        "matrix": parsed,
    }
    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step3_reachability_probe.json"
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
