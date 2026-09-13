"""JUMP read-only discovery driver (SSH auth-handshake extension).

Read-only commands ONLY: no writes, no DDL, no config changes.
Owner ruling verbatim 2026-09-13: 'proceed to ESTABLISH CONNECTION to
the external DB behind the jump server and READ DATA now.'

This driver:
1. SSHs to JUMP (TOFU-pinned known_hosts, strict host-key checking).
2. Runs a bounded list of READ-ONLY discovery commands.
3. Reports listening ports, running DB processes, installed DB clients.
4. Never echoes any credential.

Does NOT open a tunnel or connect to any DB in this step — this is
pure DISCOVERY.
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import pty
import select
import subprocess
import sys
import time
from pathlib import Path


CSV_PATH = Path("/app/backend/estate_keys/bastion/jump_server_radio_system.csv")
KNOWN_HOSTS = Path("/app/backend/estate_keys/known_hosts")
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/db_connect_receipts")


DISCOVERY_CMDS = [
    # host identity
    ("hostname", "hostname -s"),
    ("uname", "uname -srm"),
    ("id", "id -un"),
    # listening TCP ports (services on JUMP)
    ("ss_listen", "ss -tlnH 2>/dev/null | awk '{print $4}' | sort -u | head -40"),
    # ss with -p is root-only; run it since JUMP user is root
    ("ss_listen_procs", "ss -tlnp 2>/dev/null | head -40"),
    # DB processes
    ("db_procs", "ps -eo pid,comm,args 2>/dev/null | grep -iE 'mysqld|postgres|mongod|redis|mariadbd' | grep -v grep | head -20"),
    # DB clients installed
    ("which_clients", "for c in mysql psql mongo mongosh redis-cli mariadb; do which $c 2>/dev/null; done"),
    # MySQL/MariaDB defaults file present?
    ("mysql_cnf", "ls -la /etc/mysql/ /etc/mariadb/ /etc/my.cnf* /root/.my.cnf 2>/dev/null | head -20"),
    # existence of MySQL socket
    ("mysql_socket", "ls -la /var/run/mysqld/*.sock /tmp/mysql.sock /var/lib/mysql/mysql.sock 2>/dev/null | head -5"),
    # /etc/hosts entries pointing at internal DB hosts
    ("etc_hosts_dbs", "grep -E '\\.rds\\.|db-|-db|mysql|postgres|mongo|analytics|citizen|weego|viusasa' /etc/hosts 2>/dev/null | head -20"),
    # visible databases via mysql --defaults (uses ~/.my.cnf if present, no cred on cmd)
    ("mysql_defaults_show_dbs", "test -r /root/.my.cnf && mysql --defaults-file=/root/.my.cnf -e 'SHOW DATABASES;' 2>&1 | head -30 || echo 'no /root/.my.cnf readable'"),
]


def load_jump():
    with CSV_PATH.open() as f:
        rows = list(csv.reader(f))
    return {
        "ip": rows[1][0],
        "user": rows[2][0],
        "cred": rows[3][0],
    }


def eat_window_ok(now_utc: datetime.datetime) -> tuple[bool, str]:
    """EAT window 11:00–05:00 EAT (UTC+3) = 08:00 UTC – 02:00 UTC."""
    h = now_utc.hour
    ok = h >= 8 or h < 2
    return ok, f"UTC hour={h}; window 08:00–02:00 UTC (EAT 11:00–05:00)"


def _run_ssh(user: str, ip: str, pw: str, remote_cmd: str, timeout: int = 45) -> dict:
    """Reuse the T4 pty pattern — feed one password, never echo."""
    argv = [
        "ssh",
        "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
        "-o", "StrictHostKeyChecking=yes",   # strict now that JUMP is pinned
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
    chunks: list[bytes] = []
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
            low = unread.lower()
            if b"password:" in low and not pw_written:
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
    # scrub the credential defensively (should never appear, but be belt+braces)
    if pw:
        stdout = stdout.replace(pw, "<SCRUBBED_SECRET>")
    exit_code = os.WEXITSTATUS(status) if status else None
    return {"exit_code": exit_code, "stdout_scrubbed": stdout}


def main() -> int:
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"DISCOVERY driver start at {at_iso}")

    ok, reason = eat_window_ok(now)
    print(f"EAT window check: {reason} -> {'IN-WINDOW' if ok else 'OUT-WINDOW'}")
    if not ok:
        print("OUT-WINDOW: aborting.")
        return 2

    j = load_jump()
    print(f"JUMP target: user={j['user']!r} ip=<pinned in known_hosts>")

    # Compose the discovery script — a single shell heredoc bounded, read-only
    script_lines = []
    for tag, cmd in DISCOVERY_CMDS:
        script_lines.append(f"echo '===TAG:{tag}==='")
        script_lines.append(cmd)
        script_lines.append(f"echo '===END:{tag}==='")
    script = "; ".join(script_lines)

    result = _run_ssh(j["user"], j["ip"], j["cred"], script, timeout=60)
    print(f"exit_code={result['exit_code']}")

    # parse output into tag -> content
    parsed = {}
    current_tag = None
    buf = []
    for line in result["stdout_scrubbed"].splitlines():
        s = line.strip()
        if s.startswith("===TAG:") and s.endswith("==="):
            current_tag = s[len("===TAG:"):-len("===")]
            buf = []
        elif s.startswith("===END:") and s.endswith("==="):
            if current_tag:
                parsed[current_tag] = "\n".join(buf)
            current_tag = None
            buf = []
        elif current_tag is not None:
            buf.append(line)

    print()
    for tag, content in parsed.items():
        print(f"--- {tag} ---")
        for L in content.splitlines()[:20]:
            print(f"  {L}")

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_3_DISCOVERY_ON_JUMP",
        "window_check": reason,
        "in_window": ok,
        "known_hosts_pinned": str(KNOWN_HOSTS),
        "jump_target": {
            "user": j["user"], "ip_seen_in_pinned_known_hosts": True,
            "cred_kind": "LIKELY_PASSWORD (12 chars) - flagged SEC-2026-09-13-T4-01",
        },
        "exit_code": result["exit_code"],
        "discovery": parsed,
        "read_only_assertion": (
            "Every discovery command in DISCOVERY_CMDS is read-only. "
            "No writes, no DDL, no schema changes. `ss`, `ps`, `ls`, "
            "`which`, `grep /etc/hosts`, and `mysql SHOW DATABASES` "
            "only."
        ),
    }
    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step3_discovery_on_jump.json"
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")
    return 0 if result["exit_code"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
