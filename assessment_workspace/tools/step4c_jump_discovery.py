"""Discovery on JUMP itself: mounts, routes, local NAS refs.

Read-only introspection on JUMP; no writes; no egress beyond JUMP.
"""
from __future__ import annotations
import csv, datetime, json, os, pty, select, sys, time
from pathlib import Path

BASTION_CSV = Path("/app/backend/estate_keys/bastion/jump_server_radio_system.csv")
KNOWN_HOSTS = Path("/app/backend/estate_keys/known_hosts")
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/nas_connect_receipts")


def load_jump():
    with BASTION_CSV.open() as f:
        rows = list(csv.reader(f))
    return {"ip": rows[1][0], "user": rows[2][0], "cred": rows[3][0]}


def _run_ssh(user, ip, pw, remote_cmd, timeout=120):
    argv = [
        "ssh",
        "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
        "-o", "StrictHostKeyChecking=yes",
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password,keyboard-interactive",
        "-o", "NumberOfPasswordPrompts=1",
        "-o", "ConnectTimeout=15",
        "-o", "LogLevel=ERROR",
        f"{user}@{ip}", remote_cmd,
    ]
    pid, fd = pty.fork()
    if pid == 0:
        try:
            os.execvp("ssh", argv)
        except Exception as exc:
            print(f"execvp_failed: {exc!r}", flush=True); os._exit(127)
    pw_written = False; consumed = 0; chunks = []
    deadline = time.time() + timeout; status = None
    while time.time() < deadline:
        r, _, _ = select.select([fd], [], [], 0.5)
        if fd in r:
            try: chunk = os.read(fd, 8192)
            except OSError: break
            if not chunk: break
            chunks.append(chunk)
            joined = b"".join(chunks); unread = joined[consumed:]
            if b"password:" in unread.lower() and not pw_written:
                os.write(fd, (pw + "\n").encode()); pw_written = True
                consumed = len(joined); chunks.append(b"\n<pw_written>\n")
        try:
            waited_pid, s = os.waitpid(pid, os.WNOHANG)
            if waited_pid != 0: status = s; break
        except ChildProcessError: break
    try: os.close(fd)
    except OSError: pass
    stdout = b"".join(chunks).decode("utf-8", errors="replace")
    if pw: stdout = stdout.replace(pw, "<SCRUBBED_JUMP_CRED>")
    exit_code = os.WEXITSTATUS(status) if status else None
    return {"exit_code": exit_code, "stdout_scrubbed": stdout}


def main():
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"jump discovery start {at_iso}")
    jump = load_jump()

    # Segments delimited by tags for parseability.
    cmds = [
        ("OS_RELEASE",   "cat /etc/os-release 2>/dev/null | head -20"),
        ("KERNEL",       "uname -srmn"),
        ("IF_ADDR",      "ip -4 -o addr show 2>/dev/null | awk '{print $2, $4}'"),
        ("ROUTES",       "ip route 2>/dev/null"),
        ("RESOLV",       "cat /etc/resolv.conf 2>/dev/null | head -20"),
        ("HOSTS_FILE",   "cat /etc/hosts 2>/dev/null"),
        ("MOUNTS",       "mount 2>/dev/null | grep -iE '(nfs|cifs|smb|9p|fuse)' | head -20 || true"),
        ("FSTAB",        "cat /etc/fstab 2>/dev/null | head -40"),
        ("EXPORTS",      "cat /etc/exports 2>/dev/null | head -20 || true"),
        ("SAMBA_CONF",   "ls -la /etc/samba/ 2>/dev/null | head -20 || true"),
        ("LOCAL_LISTEN", "ss -H -tln 2>/dev/null | awk '{print $4}' | sort -u | head -40"),
        ("LOCAL_LISTEN_UDP","ss -H -uln 2>/dev/null | awk '{print $4}' | sort -u | head -40"),
        ("ARP",          "ip neigh show 2>/dev/null | head -40"),
        ("KNOWN_HOSTS_SSH","ls -la ~/.ssh/ 2>/dev/null | head -10 && cat ~/.ssh/known_hosts 2>/dev/null | awk '{print $1, $2}' | head -20"),
        ("NAS_TOOLS",    "for t in smbclient mount.cifs mount.nfs showmount rsync curl wget nc nmap tcpdump ping; do command -v $t >/dev/null 2>&1 && echo AVAIL:$t || echo MISSING:$t; done"),
        ("SCAN_FSTAB_LOCAL","for f in /etc/fstab /etc/exports /etc/samba/smb.conf /etc/nfs.conf /etc/auto.master /etc/auto.direct; do if [ -f $f ]; then echo EXISTS:$f; wc -l < $f | awk '{print \"lines:\"$1}'; else echo MISSING:$f; fi; done"),
        ("USER_ID",      "id"),
    ]

    parts = []
    for tag, cmd in cmds:
        parts.append(f"echo '===TAG:{tag}==='")
        parts.append(f"({cmd}) 2>&1 || true")
        parts.append(f"echo '===END:{tag}==='")
    script = "; ".join(parts)

    result = _run_ssh(jump["user"], jump["ip"], jump["cred"], script, timeout=180)
    print(f"exit_code={result['exit_code']}")

    parsed = {}
    cur=None; buf=[]
    for line in result["stdout_scrubbed"].splitlines():
        s=line.strip()
        if s.startswith("===TAG:") and s.endswith("==="):
            cur=s[len("===TAG:"):-len("===")]; buf=[]
        elif s.startswith("===END:") and s.endswith("==="):
            if cur: parsed[cur]="\n".join(buf).rstrip()
            cur=None; buf=[]
        elif cur is not None:
            buf.append(line)

    # ==== Console print, filtered for readability ====
    for k in ["OS_RELEASE","KERNEL","IF_ADDR","ROUTES","RESOLV","HOSTS_FILE","MOUNTS","FSTAB","EXPORTS","SAMBA_CONF","NAS_TOOLS","SCAN_FSTAB_LOCAL","USER_ID"]:
        v=parsed.get(k,"<missing>")
        print(f"\n== {k} ==\n{v[:2000]}")

    print(f"\n== LOCAL_LISTEN (tcp) — first line-shape only ==")
    print(parsed.get("LOCAL_LISTEN","<missing>")[:800])
    print(f"\n== ARP neighbours ==")
    print(parsed.get("ARP","<missing>")[:600])
    print(f"\n== KNOWN_HOSTS_SSH ==")
    print(parsed.get("KNOWN_HOSTS_SSH","<missing>")[:1200])

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "at_utc": at_iso,
        "phase": "STEP_4C_JUMP_DISCOVERY_LOCAL_NAS_HINTS",
        "method": "read-only introspection on JUMP (mount / fstab / routes / listeners / arp / /etc/hosts / ~/.ssh)",
        "read_only": True,
        "sections": parsed,
    }
    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_step4c_jump_discovery.json"
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"\nreceipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
