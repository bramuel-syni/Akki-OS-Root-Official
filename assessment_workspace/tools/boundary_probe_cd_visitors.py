"""Boundary probe tool · CD (citizen_digital) + Visitors MySQL 3306 reachability.

Owner-ratified 2026-09-15T~22:30Z as part of Redaction Hardening Option 1
(Ruling 3 of that turn): version-control this probe tool using the new
custody helper + env-injection pattern, never echo creds, bank shape-only
probe JSON receipts.

Discipline enforced by this tool:
  1. Custody-file access ONLY via services.secret_hygiene.custody_file
     (path-scope checked via CUSTODY_PATH_PREFIXES; JSON read via
     read_custody_metadata; CSV read via private env-injection helper
     that never returns values to any caller-visible scope).
  2. Env-injection for SSH: password lands in sshpass's SSHPASS env var,
     never appears on argv, never echoed to stdout/stderr, never assigned
     to a Python variable that outlives the subprocess.Popen call.
  3. Probe receipt shape mirrors phase0/boundary_probes/probe_53*.json:
     {probe_id, at_utc, wave_boundary, results: [{name, verdict,
     elapsed_s, errno}]}.  Only shell-level tokens + timing + errno codes
     appear on disk; no credential material.
  4. NEVER writes credential values to any log, receipt, or exception
     message.  Failures cite command class + host tag, never the value.

Usage:
    python3 /app/assessment_workspace/tools/boundary_probe_cd_visitors.py \\
        --wave-boundary "<label>" \\
        --probe-index <N> \\
        [--dry-run]

Exits:
    0 = probe fired, receipt banked (regardless of PASS/FAIL verdict).
    2 = configuration error (custody file missing / unsupported / etc.).
    3 = SEC halt in force (do not fire; write NOTE-SKIPPED receipt).

This tool refuses to fire until:
    (a) the JUMP custody file is in JSON format (currently CSV; rotation
        pending per SEC incident sec_incident_jump_cred_leak_20260915).
    (b) OR the operator explicitly passes --allow-csv-custody (opt-in
        env-injection path that reads column-0 into an env var without
        ever assigning to a caller-visible scope).

Even with --allow-csv-custody, no credential value is printed anywhere
in this tool's output.
"""
from __future__ import annotations

import argparse
import datetime as _datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path


# Load the shape-only helper from the code repo (the production module lives
# under repos/Extraction-Akki/backend/ · this tool sits in the state repo).
_CODE_REPO_BACKEND = "/app/assessment_workspace/repos/Extraction-Akki/backend"
if _CODE_REPO_BACKEND not in sys.path:
    sys.path.insert(0, _CODE_REPO_BACKEND)

from services.secret_hygiene.custody_file import (  # noqa: E402
    CUSTODY_PATH_PREFIXES,
    CustodyFileFormatUnsupportedError,
    NonCustodyPathRefused,
    read_custody_metadata,
)


JUMP_CUSTODY_PATH = "/app/backend/estate_keys/bastion/jump_server_radio_system.csv"

# Probe targets: (host_tag, ip, port).  Coordinates read from
# notes/ADMIN_BINDS_20260915.md §A on disk 2026-09-15; not from any
# transcript or hand-off summary.
PROBE_TARGETS = (
    ("citizen_digital", "159.138.164.103", 3306),
    ("visitors",        "110.238.75.83",   3306),
)

PROBE_RECEIPT_DIR = Path(
    "/app/assessment_workspace/phase0/boundary_probes/",
)

# 6-second connect timeout matches prior probes #48..#53 on disk.
PROBE_TIMEOUT_S = 6.0


def _iso_utc() -> str:
    return _datetime.datetime.now(_datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ",
    )


def _compact_ts() -> str:
    return _datetime.datetime.now(_datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ",
    )


def _refuse_non_custody_path(path: str) -> None:
    """Path-scope check — refuses paths outside CUSTODY_PATH_PREFIXES.
    Mirrors the helper's NonCustodyPathRefused semantics but usable
    for any file this tool touches, not only via read_custody_metadata."""
    if not any(path.startswith(p) for p in CUSTODY_PATH_PREFIXES):
        raise NonCustodyPathRefused(
            f"path {path!r} not under CUSTODY_PATH_PREFIXES "
            f"{sorted(CUSTODY_PATH_PREFIXES)!r}"
        )


def _load_jump_via_env_injection(
    *, csv_path: str, sshpass_env_name: str,
) -> tuple[str, str]:
    """Read column-0 values from the JUMP CSV DIRECTLY into local
    scope, publish the password to `sshpass_env_name` in os.environ,
    then delete every local reference to raw values.

    Returns: (ip, user)  ← plaintext OK; not secrets.
    Side effect: os.environ[sshpass_env_name] carries the pw.

    This function is the CSV-custody env-injection path.  It NEVER
    returns the pw to any caller-visible scope.  It NEVER assigns
    the pw to any long-lived variable.  It reads → env-injects →
    drops the local reference.
    """
    _refuse_non_custody_path(csv_path)
    import csv
    with open(csv_path, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 4:
        raise ValueError(
            f"JUMP custody CSV at {csv_path!r} has <4 rows; expected "
            f"row0=header, row1=ip, row2=user, row3=pw"
        )
    ip = rows[1][0]
    user = rows[2][0]
    # Env-inject then drop the reference in the same statement.
    os.environ[sshpass_env_name] = rows[3][0]
    del rows  # break the reference chain
    return ip, user


def _fire_tcp_probe_via_jump(
    *, jump_ip: str, jump_user: str, sshpass_env_name: str,
    target_ip: str, target_port: int, timeout_s: float,
) -> dict:
    """SSH to JUMP via sshpass (env-injection · SSHPASS from
    sshpass_env_name), run a bash /dev/tcp connect probe against
    target_ip:target_port with a bounded timeout, report the outcome
    as {verdict, elapsed_s, errno}.

    No password appears on argv.  No password appears in the returned
    dict.  No password appears in any exception message.
    """
    remote_cmd = (
        f"timeout {timeout_s} bash -c "
        f"'exec 3<>/dev/tcp/{target_ip}/{target_port} && "
        f"echo OPEN && exec 3<&- 3>&-'"
    )
    argv = [
        "sshpass", "-e",
        "ssh",
        "-o", "UserKnownHostsFile=/app/backend/estate_keys/known_hosts",
        "-o", "StrictHostKeyChecking=yes",
        "-o", "PubkeyAuthentication=no",
        "-o", "PreferredAuthentications=password,keyboard-interactive",
        "-o", "NumberOfPasswordPrompts=1",
        "-o", f"ConnectTimeout={int(timeout_s) + 2}",
        "-o", "LogLevel=ERROR",
        f"{jump_user}@{jump_ip}",
        remote_cmd,
    ]
    env = dict(os.environ)  # sshpass reads SSHPASS from env
    # Assert env var name matches expected sshpass convention.
    if sshpass_env_name != "SSHPASS":
        raise ValueError(
            "sshpass_env_name must be 'SSHPASS' for `sshpass -e` to consume it"
        )
    t_start = time.monotonic()
    try:
        result = subprocess.run(
            argv, env=env, capture_output=True, text=True,
            timeout=timeout_s + 4,
        )
        elapsed = round(time.monotonic() - t_start, 3)
        # Never echo result.stdout / result.stderr — they may contain
        # ssh-side artefacts.  Interpret verdict from returncode + probe
        # marker.
        if result.returncode == 0 and "OPEN" in result.stdout:
            verdict = "PASS"
            errno = None
        else:
            verdict = "FAIL"
            # Try to parse errno from stderr in a bounded way.
            errno = None
            for line in result.stderr.splitlines():
                if "errno=" in line.lower():
                    try:
                        errno = int(line.lower().split("errno=")[1].split()[0])
                    except (IndexError, ValueError):
                        pass
    except subprocess.TimeoutExpired:
        elapsed = round(time.monotonic() - t_start, 3)
        verdict = "FAIL"
        errno = 110  # ETIMEDOUT convention
    return {
        "verdict": verdict,
        "elapsed_s": elapsed,
        "errno": errno,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Boundary probe · CD + Visitors MySQL 3306 · "
                    "custody-hygiene compliant.",
    )
    parser.add_argument(
        "--wave-boundary", required=True,
        help="Human-readable label of the boundary being probed.",
    )
    parser.add_argument(
        "--probe-index", type=int, required=True,
        help="Sequential probe index (e.g. 55).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Do not fire; emit a NOTE-SKIPPED receipt.",
    )
    parser.add_argument(
        "--allow-csv-custody", action="store_true",
        help="Opt in to the CSV env-injection path (default: refuse; "
             "wait for JSON custody rotation).",
    )
    args = parser.parse_args()

    ts_iso = _iso_utc()
    ts_compact = _compact_ts()
    PROBE_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = (
        PROBE_RECEIPT_DIR / f"probe_{args.probe_index}_{ts_compact}.json"
    )

    if args.dry_run:
        receipt = {
            "probe_id": f"boundary_probe_{args.probe_index}",
            "at_utc": ts_iso,
            "wave_boundary": args.wave_boundary,
            "status": "DRY-RUN",
            "results": [],
        }
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"probe {args.probe_index}: DRY-RUN receipt banked at {receipt_path}")
        return 0

    # Decide custody path.  JSON path takes precedence when available.
    jump_json_candidate = JUMP_CUSTODY_PATH.replace(".csv", ".json")
    if Path(jump_json_candidate).exists():
        # JSON custody available — read via helper.  Values stay in scope
        # of a private handler; env-inject then drop the reference.
        try:
            md = read_custody_metadata(path=jump_json_candidate)
        except (NonCustodyPathRefused, CustodyFileFormatUnsupportedError) as exc:
            _write_config_error_receipt(
                receipt_path=receipt_path,
                ts_iso=ts_iso,
                wave_boundary=args.wave_boundary,
                probe_index=args.probe_index,
                reason=f"helper refused JSON custody: {type(exc).__name__}",
            )
            return 2
        # Shape check — expect keys: ip, user, password (or equivalents).
        # Actual value fetch is a follow-on function that ONLY appears
        # after JSON custody lands.  For now this branch is aspirational
        # (JUMP custody is CSV as of 2026-09-15).
        _write_config_error_receipt(
            receipt_path=receipt_path,
            ts_iso=ts_iso,
            wave_boundary=args.wave_boundary,
            probe_index=args.probe_index,
            reason=(
                "JSON JUMP custody detected but value-fetch path not yet "
                "implemented in CP-SW6-HYG-1 scope. Land follow-on when "
                "JUMP custody rotation moves to JSON."
            ),
        )
        return 2

    # CSV custody fallback path.
    if not args.allow_csv_custody:
        # Refuse to fire — respect the SEC halt discipline.
        receipt = {
            "probe_id": f"boundary_probe_{args.probe_index}",
            "at_utc": ts_iso,
            "wave_boundary": args.wave_boundary,
            "status": "NOTE-SKIPPED",
            "skip_reason": (
                "JUMP custody is CSV at snapshot time.  Tool refuses to "
                "invoke the CSV env-injection path without --allow-csv-"
                "custody opt-in.  Awaiting JUMP custody rotation to JSON."
            ),
            "results": [],
        }
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"probe {args.probe_index}: NOTE-SKIPPED (CSV custody · opt-in required)")
        return 3

    # Opt-in path: env-inject from CSV, fire probe, bank result.
    try:
        _refuse_non_custody_path(JUMP_CUSTODY_PATH)
        jump_ip, jump_user = _load_jump_via_env_injection(
            csv_path=JUMP_CUSTODY_PATH,
            sshpass_env_name="SSHPASS",
        )
    except (NonCustodyPathRefused, ValueError) as exc:
        _write_config_error_receipt(
            receipt_path=receipt_path,
            ts_iso=ts_iso,
            wave_boundary=args.wave_boundary,
            probe_index=args.probe_index,
            reason=f"{type(exc).__name__}: {exc}",
        )
        return 2

    results = []
    for name, ip, port in PROBE_TARGETS:
        r = _fire_tcp_probe_via_jump(
            jump_ip=jump_ip, jump_user=jump_user,
            sshpass_env_name="SSHPASS",
            target_ip=ip, target_port=port,
            timeout_s=PROBE_TIMEOUT_S,
        )
        results.append({"name": name, **r})

    receipt = {
        "probe_id": f"boundary_probe_{args.probe_index}",
        "at_utc": ts_iso,
        "wave_boundary": args.wave_boundary,
        "results": results,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"probe {args.probe_index}: receipt banked at {receipt_path}")

    # Immediately clear the sshpass env var to shrink the value's
    # lifetime in process memory.
    os.environ.pop("SSHPASS", None)

    return 0


def _write_config_error_receipt(
    *, receipt_path: Path, ts_iso: str, wave_boundary: str,
    probe_index: int, reason: str,
) -> None:
    receipt = {
        "probe_id": f"boundary_probe_{probe_index}",
        "at_utc": ts_iso,
        "wave_boundary": wave_boundary,
        "status": "CONFIG-ERROR",
        "reason": reason,
        "results": [],
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    sys.exit(main())
