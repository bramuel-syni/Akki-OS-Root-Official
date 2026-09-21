"""acceptance_parser.py — maps real acceptance.sh stdout lines to check-result dicts.

Called by services.connect.gpu_submit._run_acceptance after seam.execute() returns.
Pure function — no I/O, no state. Fed the raw stdout string + exit_code; returns a
list of {name, ok, sentence} dicts that render into the four-questions after-state.

Log-line shapes recognised (from phase0/acceptance.sh output format):
  === Phase-0 Acceptance · <TS> ===       phase-start marker (info)
  hardening.mode: <text>                   info measurement
  hss.size_tb: <N>                          info measurement
  hss.writable: ok (<path>)                info measurement
  gpu.h200_count: <N>                       info measurement
  gpu.nvlink: <status>                      info measurement
  ephemeral.size_tb: <N>                    info measurement
  sshd.password_auth: <status>              info measurement
  FAIL: <message>                           failing check (ok=False)
  WARN: <message>                           warning (ok=True, noted)
  === ALL CHECKS GREEN ===                  green marker (info)

Any measurement line whose value is 'ok' or a numeric-in-range is ok=True; any
FAIL: line is ok=False with the message verbatim in the sentence.

The parser does not invent facts — every sentence draws from the actual line.
Only the sentence templating (turning `hss.size_tb: 30` into
`The high-speed storage is 30 TB.`) is our language, and each template is a
fixed, small, auditable mapping. Anything unrecognised is passed through as an
info line rather than dropped.
"""
from __future__ import annotations

import re
from typing import Any


_PHASE_START = re.compile(r"^===\s*Phase-0 Acceptance\s*·\s*(\S+)\s*===\s*$")
_ALL_GREEN = re.compile(r"^===\s*ALL CHECKS GREEN\s*===\s*$")
_FAIL = re.compile(r"^FAIL:\s*(.*)$")
_WARN = re.compile(r"^WARN:\s*(.*)$")
_INFO = re.compile(r"^([a-z][a-z0-9_.]+):\s*(.*)$")


def _sentence_for_info(key: str, value: str) -> str:
    """Turn a `key: value` info line into a plain English sentence.

    Small, exhaustive map for the eight measurement lines acceptance.sh emits.
    Unknown keys fall through to a generic 'The <key> is <value>.' template.
    """
    v = value.strip()
    if key == "hardening.mode":
        return f"Hardening mode: {v}."
    if key == "hss.size_tb":
        return f"The high-speed storage is {v} TB."
    if key == "hss.writable":
        return f"The high-speed storage is writable: {v}."
    if key == "gpu.h200_count":
        return f"The machine has {v} H200 GPU(s)."
    if key == "gpu.nvlink":
        return f"NVLink status: {v}."
    if key == "ephemeral.size_tb":
        return f"Ephemeral storage is {v} TB."
    if key == "sshd.password_auth":
        return f"Password authentication is {v}."
    return f"{key.replace('_', ' ').replace('.', ' ')} is {v}."


def _sentence_for_fail(message: str) -> str:
    """Failure sentences render the acceptance message verbatim, framed as a check."""
    m = message.strip()
    if not m:
        return "Check failed (no message)."
    # If the message already reads as a sentence, keep it. Otherwise wrap.
    if m[-1] in ".!?":
        return m
    return f"Check failed: {m}."


def parse_output(stdout: str, *, exit_code: int) -> list[dict[str, Any]]:
    """Parse acceptance.sh stdout into a list of check dicts.

    Every returned dict has keys: name (str), ok (bool), sentence (str).

    The overall pass/fail is derived by the caller from exit_code (0 = green;
    non-zero = held). This parser produces the per-check evidence; the caller
    binds it to the after-state grammar.
    """
    checks: list[dict[str, Any]] = []
    saw_all_green = False

    for raw in stdout.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        m = _PHASE_START.match(stripped)
        if m:
            checks.append({
                "name": "phase0_start",
                "ok": True,
                "sentence": f"Phase-0 acceptance began at {m.group(1)}.",
            })
            continue

        if _ALL_GREEN.match(stripped):
            saw_all_green = True
            checks.append({
                "name": "all_checks_green",
                "ok": True,
                "sentence": "All acceptance checks reported green.",
            })
            continue

        m = _FAIL.match(stripped)
        if m:
            checks.append({
                "name": _slug_from_fail(m.group(1)),
                "ok": False,
                "sentence": _sentence_for_fail(m.group(1)),
            })
            continue

        m = _WARN.match(stripped)
        if m:
            checks.append({
                "name": _slug_from_fail(m.group(1)) + ".warn",
                "ok": True,
                "sentence": f"Warning: {m.group(1).strip()}.",
            })
            continue

        m = _INFO.match(stripped)
        if m:
            key, value = m.group(1), m.group(2)
            checks.append({
                "name": key,
                "ok": True,
                "sentence": _sentence_for_info(key, value),
            })
            continue

        # Unknown / indented / narrative line — record without dropping.
        # Guards against silent parser drift when acceptance.sh grows a new line.
        if stripped:
            checks.append({
                "name": "raw",
                "ok": True,
                "sentence": stripped,
            })

    # If exit_code says non-zero but we saw no FAIL and no ALL-GREEN, mark it.
    if exit_code != 0 and not any(c["ok"] is False for c in checks) and not saw_all_green:
        checks.append({
            "name": f"exit_code_{exit_code}",
            "ok": False,
            "sentence": f"acceptance.sh exited with code {exit_code} without an explicit FAIL line.",
        })
    return checks


def _slug_from_fail(msg: str) -> str:
    """Best-effort short name for a failure line.

    e.g., '/mnt/hss not mounted' → 'hss_mount'; 'expected 4× H200, got 0' → 'gpu_h200_count'.
    """
    m = msg.lower()
    if "/mnt/hss" in m or "hss" in m:
        return "hss_check"
    if "h200" in m or "nvidia-smi" in m or "nvlink" in m or "gpu" in m:
        return "gpu_check"
    if "ephemeral" in m:
        return "ephemeral_check"
    if "password" in m or "sshd" in m:
        return "sshd_check"
    if "hardening" in m or "harden" in m:
        return "hardening_check"
    # Fallback: first two lowercase alnum words joined by underscore.
    words = re.findall(r"[a-z0-9]+", m)[:2]
    return "_".join(words) if words else "unknown_check"
