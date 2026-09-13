"""T4 side-task driver — auth handshake through JUMP → RADIO.

Discipline (owner rulings 2026-09-13 · admin bastion Q&A):
- TOFU host-key pinning: JUMP pins already verified against T2 fingerprints
  and written to /app/backend/estate_keys/known_hosts (0600).  RADIO
  first-connect uses `StrictHostKeyChecking=accept-new` against the same
  file (TOFU).
- Auth handshake ONLY: `id -un && uname -srm`.  No operational commands.
- Egress window: EAT (11:00 EAT / 08:00 UTC — 05:00 EAT / 02:00 UTC).
  Current run gated by wall-clock check before ssh spawn.
- Secret handling: never echo any credential to stdout, stderr, log,
  git tree, or process argv.  Credentials are read from CSV in-process
  and fed through pty writes to child stdin only.
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
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/drill_receipts")


def load_targets() -> dict:
    with CSV_PATH.open() as f:
        rows = list(csv.reader(f))
    headers = rows[0]
    targets = {}
    for c in range(len(headers)):
        targets[headers[c]] = {
            "ip": rows[1][c],
            "user": rows[2][c],
            "cred": rows[3][c],
        }
    return targets


def eat_window_ok(now_utc: datetime.datetime) -> tuple[bool, str]:
    """EAT window 11:00–05:00 EAT (UTC+3) = 08:00 UTC – 02:00 UTC."""
    h = now_utc.hour
    ok = h >= 8 or h < 2
    reason = f"UTC hour={h}; window 08:00–02:00 UTC (EAT 11:00–05:00)"
    return ok, reason


def _run_ssh_two_password(
    jump_ip: str,
    jump_user: str,
    jump_pw: str,
    radio_ip: str,
    radio_user: str,
    radio_pw: str,
    remote_cmd: str,
    timeout: int = 45,
) -> dict:
    """Spawn `ssh -J user1@jump user2@radio remote_cmd` in a pty; feed
    the two passwords in order on `password:` prompts.  Never log
    credentials."""

    argv = [
        "ssh",
        "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
        "-o", "StrictHostKeyChecking=accept-new",   # TOFU on RADIO first connect
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password,keyboard-interactive",
        "-o", "NumberOfPasswordPrompts=1",
        "-o", "ConnectTimeout=15",
        "-o", "LogLevel=ERROR",
        "-J", f"{jump_user}@{jump_ip}",
        f"{radio_user}@{radio_ip}",
        remote_cmd,
    ]

    pid, fd = pty.fork()
    if pid == 0:  # child
        try:
            os.execvp("ssh", argv)
        except Exception as exc:
            print(f"execvp_failed: {exc!r}", flush=True)
            os._exit(127)

    pw_queue = [jump_pw, radio_pw]
    pw_prompts_seen = 0
    fingerprint_prompts_seen = 0
    output_chunks: list[bytes] = []
    # Tracks how many bytes of the joined buffer have been "consumed"
    # by prompt detection, so a stale "password:" or "authenticity"
    # substring is not re-matched.
    consumed_bytes = 0
    deadline = time.time() + timeout
    child_status = None

    try:
        while time.time() < deadline:
            r, _, _ = select.select([fd], [], [], 0.5)
            if fd in r:
                try:
                    chunk = os.read(fd, 8192)
                except OSError:
                    break
                if not chunk:
                    break
                output_chunks.append(chunk)
                joined = b"".join(output_chunks)
                # Only scan the region AFTER what we already consumed.
                unread = joined[consumed_bytes:]
                low = unread.lower()
                # password prompt
                if b"password:" in low and pw_prompts_seen < len(pw_queue):
                    os.write(fd, (pw_queue[pw_prompts_seen] + "\n").encode())
                    pw_prompts_seen += 1
                    consumed_bytes = len(joined)   # burn everything so far
                    output_chunks.append(b"\n<pw_written>\n")
                # fingerprint acceptance prompt (TOFU accept-new usually
                # bypasses this, but be robust)
                elif (b"authenticity" in low
                        and b"(yes/no" in low
                        and fingerprint_prompts_seen == 0):
                    os.write(fd, b"yes\n")
                    fingerprint_prompts_seen += 1
                    consumed_bytes = len(joined)
                    output_chunks.append(b"\n<fp_accepted>\n")
            # check for child exit
            try:
                waited_pid, status = os.waitpid(pid, os.WNOHANG)
                if waited_pid != 0:
                    child_status = status
                    break
            except ChildProcessError:
                break
        else:
            # deadline reached
            os.kill(pid, 15)
            waited_pid, status = os.waitpid(pid, 0)
            child_status = status
    finally:
        try:
            os.close(fd)
        except OSError:
            pass

    stdout_full = b"".join(output_chunks).decode("utf-8", errors="replace")
    # SCRUB any credential leak from stdout defensively (shouldn't happen
    # because ssh echoes '*' or nothing for pw prompts, but just in case)
    for cred in (jump_pw, radio_pw):
        if cred:
            stdout_full = stdout_full.replace(cred, "<SCRUBBED_SECRET>")

    exit_code = os.WEXITSTATUS(child_status) if child_status else None
    return {
        "exit_code": exit_code,
        "pw_prompts_seen": pw_prompts_seen,
        "fp_prompts_seen": fingerprint_prompts_seen,
        "stdout_scrubbed": stdout_full,
    }


def main() -> int:
    now = datetime.datetime.now(datetime.UTC)
    at_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"T4 driver start at {at_iso}")

    ok, reason = eat_window_ok(now)
    print(f"EAT window check: {reason} -> {'IN-WINDOW' if ok else 'OUT-WINDOW'}")
    if not ok:
        print("OUT-WINDOW: T4 deferred; no ssh will be spawned.")
        return 2

    targets = load_targets()
    j = targets["Jump Server"]
    r = targets["Radio news system."]

    # Classify RADIO cred shape (never echo)
    import re
    rc = r["cred"]
    if rc.startswith("/") and Path(rc).exists():
        rk = "FILEPATH_TO_KEY"
    elif "-----BEGIN" in rc and "PRIVATE KEY-----" in rc:
        rk = "INLINE_PRIVATE_KEY"
    elif re.match(r"^[A-Za-z0-9!@#$%^&*()_+\-=.,]{4,32}$", rc):
        rk = "LIKELY_PASSWORD"
    elif len(rc) > 100:
        rk = "LIKELY_INLINE_KEY_MATERIAL"
    else:
        rk = "OPAQUE_UNKNOWN_but_treated_as_password"
    print(f"RADIO cred classification: {rk} (len={len(rc)})")

    print(f"Running ssh -J {j['user']}@JUMP {r['user']}@RADIO 'id -un && uname -srm' ...")
    result = _run_ssh_two_password(
        jump_ip=j["ip"], jump_user=j["user"], jump_pw=j["cred"],
        radio_ip=r["ip"], radio_user=r["user"], radio_pw=r["cred"],
        remote_cmd="id -un && uname -srm",
    )

    print(f"exit_code={result['exit_code']}")
    print(f"pw_prompts_seen={result['pw_prompts_seen']}")
    print(f"fp_prompts_seen={result['fp_prompts_seen']}")
    print("scrubbed stdout tail:")
    print("\n".join(result["stdout_scrubbed"].splitlines()[-40:]))

    # Bank the receipt (no secrets ever)
    receipt = {
        "at_utc": at_iso,
        "window_check": reason,
        "in_window": ok,
        "known_hosts_pinned": {
            "path": str(KNOWN_HOSTS),
            "mode": oct(KNOWN_HOSTS.stat().st_mode & 0o777),
            "size_bytes": KNOWN_HOSTS.stat().st_size,
            "T2_match": "3/3 SHA256 fingerprints (rsa/ecdsa/ed25519) verified vs precheck record",
        },
        "targets": {
            "JUMP": {
                "user": j["user"], "cred_kind": "LIKELY_PASSWORD",
                "cred_len": len(j["cred"]),
            },
            "RADIO": {
                "user": r["user"], "cred_kind": rk,
                "cred_len": len(rc),
            },
        },
        "auth_handshake": {
            "remote_cmd": "id -un && uname -srm",
            "exit_code": result["exit_code"],
            "pw_prompts_seen": result["pw_prompts_seen"],
            "fp_prompts_seen": result["fp_prompts_seen"],
            "stdout_scrubbed_tail": "\n".join(
                result["stdout_scrubbed"].splitlines()[-40:]
            ),
        },
        "security_observations": [
            "SEC-2026-09-13-T4-01: earlier session-cell inadvertently "
            "echoed the JUMP password from CSV row 3 col 0 (12 chars) "
            "into my transcript. Owner-side rotation required (adds to "
            "SEC-2026-09-12-01 pending rotation).",
            "SEC-2026-09-13-T4-02 [from admin ruling 4]: Public-internet "
            "root SSH with password auth on JUMP is a hardening risk. "
            "Recorded for owner's later attention; NOT acted on per admin "
            "instruction 'do not change any server config'.",
        ],
    }
    return_code = 0 if result["exit_code"] == 0 else 1
    receipt["overall_verdict"] = "PASS" if return_code == 0 else "FAIL"

    receipt_path = RECEIPT_DIR / f"{now.strftime('%Y%m%dT%H%M%SZ')}_T4_bastion_handshake.json"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")
    return return_code


if __name__ == "__main__":
    sys.exit(main())
