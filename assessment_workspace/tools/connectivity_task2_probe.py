"""tools/connectivity_task2_probe.py — Task 2 connectivity orchestrator.

Owner rulings (2026-09-14, verbatim):
  * "Combine option 1 and 2 - run the test - implement the requirements
    to connect as guided by the admin."
  * "Use the credentials I shared."
  * "these are file labels but no confidential information. We have
    full rights on this data."  (content-read HOLD lifted; bounded
    samples permitted)
  * "rotation happens AFTER connection is established" (SEC-T4 items
    stay USER-VERIFICATION-PENDING; do not block)

Discipline (this orchestrator enforces):
  * Position-redaction on every credential/secret cell (prints length
    only, never the value).
  * Bounded samples ONLY — cap on listing/enumerate.
  * Local receipts under phase0/connectivity_receipts/; no egress
    outside probes.
  * EAT window: 08:00-02:00 UTC.
"""
from __future__ import annotations

import csv
import json
import os
import shlex
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RECEIPTS = Path("/app/assessment_workspace/phase0/connectivity_receipts")
RECEIPTS.mkdir(parents=True, exist_ok=True)


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _bank(name: str, payload: dict) -> Path:
    stamp = _now_stamp()
    p = RECEIPTS / f"{stamp}_{name}.json"
    p.write_text(json.dumps(payload, indent=2, default=str))
    return p


def load_bastion_csv() -> dict:
    """Return {'jump': {'host','user','password_len','password'},
                'radio':{'host','user','password_len','password'}}.

    Values are held in memory; we only print `len(...)` on any secret.
    """
    p = "/app/backend/estate_keys/bastion/jump_server_radio_system.csv"
    with open(p) as fh:
        rows = list(csv.reader(fh))
    # Row 0 = header ["Jump Server","Radio news system."]
    # Rows 1..3 = [host, user, password] per column
    jump = {"host": rows[1][0], "user": rows[2][0], "password": rows[3][0]}
    radio = {"host": rows[1][1], "user": rows[2][1], "password": rows[3][1]}
    return {"jump": jump, "radio": radio}


def tcp_probe(host: str, port: int, timeout: float = 12.0) -> dict:
    t0 = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(4.0)
            try:
                banner = s.recv(200)
            except Exception:
                banner = b""
        return {
            "ok": True,
            "elapsed_ms": int((time.monotonic() - t0) * 1000),
            "banner_bytes": len(banner),
            "banner_prefix_ascii": banner[:24].decode("ascii", errors="replace"),
        }
    except Exception as exc:
        return {
            "ok": False,
            "elapsed_ms": int((time.monotonic() - t0) * 1000),
            "error_class": type(exc).__name__,
            "error_message": str(exc)[:200],
        }


def ssh_keyscan(host: str, port: int = 22) -> dict:
    try:
        out = subprocess.run(
            ["ssh-keyscan", "-T", "5", "-p", str(port), host],
            capture_output=True, text=True, timeout=15,
        )
        keys = []
        for line in out.stdout.splitlines():
            parts = line.strip().split(None, 2)
            if len(parts) >= 3:
                keys.append({"kind": parts[1], "keydata_prefix": parts[2][:32]})
        return {"ok": bool(keys), "n_keys": len(keys), "keys": keys}
    except Exception as exc:
        return {"ok": False, "error": str(exc)[:200]}


if __name__ == "__main__":
    print("connectivity_task2_probe loaded; call from Python REPL / driver scripts")
