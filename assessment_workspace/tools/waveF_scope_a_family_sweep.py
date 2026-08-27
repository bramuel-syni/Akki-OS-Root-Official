#!/usr/bin/env python3
"""Wave F · Scope A · Path 1 · Attempt 2 · family-ordered un-quarantine sweep.

Owner ruling verbatim (2026-08-27T~19:00Z, Finding-2 amendment i):
"if Attempt 1 is clean, un-quarantine in FAMILY order (charter rows),
 measuring after each family rather than all-at-once — if a family regresses,
 you know which one without bisecting"

Invocation:
    python3 tools/waveF_scope_a_family_sweep.py --range START:STOP
    python3 tools/waveF_scope_a_family_sweep.py --status
    python3 tools/waveF_scope_a_family_sweep.py --revert-all

Runs from workspace root: /app/assessment_workspace/

For each family (1-indexed against charter row order):
  1. Un-quarantine that family's file (remove skip markers).
  2. Run `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/`.
  3. Parse `BASELINE_GUARD receipt` line + short summary.
  4. If clean (status OK · exit 0 · no new failures): keep un-quarantined,
     record ACCEPT to state ledger.
  5. If regression (any new failure OR V1 trip OR non-zero exit): revert the
     one file via `git checkout`, record REGRESS to state ledger with
     failing test node ids captured for Path-2 escalation.

State ledger: /app/assessment_workspace/phase0/drill_receipts/waveF_scope_a_sweep_state.json
Per-family receipts: /app/assessment_workspace/phase0/drill_receipts/{TS}_wave_f_scope_a_path_1_attempt_2_family_{NN}_{filename}.log
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
REPO = WORKSPACE / "repos" / "Extraction-Akki"
BACKEND = REPO / "backend"
RECEIPTS = WORKSPACE / "phase0" / "drill_receipts"

# Overridable via --tag CLI (default retains Path 1 name for legacy).
TAG = "path_1_attempt_2"


def _state_path() -> Path:
    return RECEIPTS / f"waveF_scope_a_sweep_state_{TAG}.json"

# Charter row order (from notes/waveF_retirement_charter.md §Scope table).
# 19 partial-skip families + 2 Q1 legacy full-skip families = 21 families.
FAMILIES = [
    # (row, file, skip_type, expected_skip_count)
    (1,  "test_phase_5_stage_b_async_delivery.py",         "partial", 19),
    (2,  "test_phase_8_seam_3_sub_stage_1.py",             "partial", 12),  # 17 tests · 12 defs
    (3,  "test_phase_8_b_5a_compliance.py",                "partial", 10),
    (4,  "test_phase_8_seam_3_sub_stage_2.py",             "partial", 8),
    (5,  "test_composed_conclusion_dispatch.py",           "partial", 5),
    (6,  "test_dispatch_shape_responsive.py",              "partial", 4),
    (7,  "test_feasibility_honesty_under_absence.py",      "partial", 4),
    (8,  "test_qualified_data_selection.py",               "partial", 4),
    (9,  "test_engineer_key_grant_ledger.py",              "partial", 3),
    (10, "test_feasibility_dual_consumer_schema.py",       "partial", 3),
    (11, "test_master_admin_tier_lock_path_a_ledger.py",   "partial", 2),
    (12, "test_memory_service_m_g1_to_m_g9.py",            "partial", 2),
    (13, "test_8_ext.py",                                  "partial", 1),
    (14, "test_connect_ui1c_gates.py",                     "partial", 1),
    (15, "test_engineer_key_grant_e2_taxonomy.py",         "partial", 1),
    (16, "test_master_admin_auth_reconciliation.py",       "partial", 1),
    (17, "test_memory_engineer_key_grant_e2e_propagation.py", "partial", 1),
    (18, "test_phase_7_stage_b_1_wizard.py",               "partial", 1),
    (19, "test_qualified_data_outer_gate_ride.py",         "partial", 1),
    # Q1 legacy full-skip
    (20, "test_phase_8_b_5b.py",                           "q1_legacy", 26),
    (21, "test_phase_8_seam_3_sub_stage_3.py",             "q1_legacy", 45),
]

PARTIAL_SKIP_MARKER = (
    '@pytest.mark.skip(reason="D1a-1 residue under pytest-asyncio 1.2.0 · '
    "Wave F retirement charter · CP-D6 Q2 grant 2026-08-27 "
    "(verbatim: 'Q2 is then GRANTED in advance for exactly those files')\")"
)

# Q1 legacy pytestmark block spans multiple lines; we match on the anchoring
# comment + block start/end. Both Q1 files share identical text.
Q1_COMMENT = "# W11 D · CP-D1a · rung-4 quarantine (owner ruling 2026-08-27)."
Q1_BLOCK_START = "pytestmark = pytest.mark.skip("
Q1_BLOCK_REASON = (
    'reason="D1a-1 residual quarantine · pytest-asyncio 1.2.0 upgrade '
    "(CP-D5 · owner Q1 authorised) partially resolved the cross-loop "
    "teardown; this file remains 100%% errored under 1.2.0 (26/45 tests, "
    "cross-loop mismatch in setup path not just teardown). Deferred to "
    "Wave F pytest-asyncio 1.4.0-compatible refactor OR targeted fixture "
    "split per test module. Preserves the V2b invariant.\""
)


def _now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_state() -> dict:
    STATE = _state_path()
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {
        "attempt": TAG,
        "started_at_utc": None,
        "families": {},  # row -> {"file", "status", "receipt", ...}
    }


def _save_state(state: dict) -> None:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    _state_path().write_text(json.dumps(state, indent=2, sort_keys=True))


def _unquarantine_partial(fpath: Path, expected_count: int) -> int:
    """Remove all @pytest.mark.skip(...) partial-skip lines. Returns count removed."""
    text = fpath.read_text()
    # Each occurrence should be exactly the same string.
    count = text.count(PARTIAL_SKIP_MARKER)
    if count != expected_count:
        raise RuntimeError(
            f"{fpath.name}: expected {expected_count} skip markers, "
            f"found {count}. Halt for owner review (pattern drift?)."
        )
    # Remove the marker line + its trailing newline (line-oriented).
    lines = text.splitlines(keepends=True)
    kept = [l for l in lines if l.strip() != PARTIAL_SKIP_MARKER]
    if len(lines) - len(kept) != count:
        raise RuntimeError(
            f"{fpath.name}: line-based removal count mismatch. "
            f"lines={len(lines)} kept={len(kept)} expected_removed={count}"
        )
    fpath.write_text("".join(kept))
    return count


def _unquarantine_q1(fpath: Path) -> int:
    """Remove Q1 legacy file-level pytestmark block. Returns 1 on success."""
    text = fpath.read_text()
    if Q1_COMMENT not in text:
        raise RuntimeError(f"{fpath.name}: missing Q1 anchor comment")
    if Q1_BLOCK_START not in text:
        raise RuntimeError(f"{fpath.name}: missing pytestmark block start")
    if Q1_BLOCK_REASON not in text:
        raise RuntimeError(f"{fpath.name}: Q1 reason text drifted")
    # The block is:
    #   # W11 D · CP-D1a · rung-4 quarantine (owner ruling 2026-08-27).
    #   pytestmark = pytest.mark.skip(
    #       reason="..."
    #   )
    # Followed by a blank line. Remove all four lines.
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    removed = False
    while i < len(lines):
        if lines[i].rstrip() == Q1_COMMENT and (i + 1) < len(lines) \
                and lines[i + 1].rstrip() == Q1_BLOCK_START:
            # Skip: comment + pytestmark = pytest.mark.skip( + reason=... + )
            # Advance until we find the closing ')' on its own line.
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != ")":
                j += 1
            if j >= len(lines):
                raise RuntimeError(f"{fpath.name}: unterminated pytestmark block")
            # Also swallow a trailing blank line if present.
            end = j + 1
            if end < len(lines) and lines[end].strip() == "":
                end += 1
            i = end
            removed = True
        else:
            out.append(lines[i])
            i += 1
    if not removed:
        raise RuntimeError(f"{fpath.name}: pytestmark block not removed")
    fpath.write_text("".join(out))
    return 1


def _revert_file(fpath: Path) -> None:
    """git checkout HEAD -- fpath (restores the file from programme/track-a HEAD)."""
    rel = fpath.relative_to(REPO).as_posix()
    subprocess.run(
        ["git", "checkout", "HEAD", "--", rel],
        cwd=REPO,
        check=True,
        capture_output=True,
    )


def _run_measure(receipt_path: Path, family_row: int, family_file: str) -> dict:
    """Run BASELINE_GUARD=1 pytest, tee output to receipt_path, return summary dict."""
    header = f"""================================================================================
Wave F · Scope A · {TAG} · Family {family_row} measure
================================================================================
Timestamp (UTC):     {_now_ts()}
Family:              {family_row} / 21
File:                {family_file}
Cumulative state:    families 1..{family_row} un-quarantined progressively
Sweep tag:           {TAG}
Invocation:          cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/
--------------------------------------------------------------------------------
"""
    receipt_path.write_text(header)
    env = dict(os.environ)
    env["BASELINE_GUARD"] = "1"
    proc = subprocess.run(
        ["python", "-m", "pytest", "tests/invariants/"],
        cwd=BACKEND,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    with receipt_path.open("a") as fh:
        fh.write(output)
        fh.write(f"\n--- pytest exit code: {proc.returncode} ---\n")

    # Parse receipt line
    m_receipt = re.search(
        r"passed=(\d+)\s*/\s*baseline-failures-remaining=(\d+)\s*/\s*quarantined=(\d+)",
        output,
    )
    m_status = re.search(r"status:\s*(OK|.*HALT AND REPORT.*)", output)
    m_tally = re.search(
        r"(\d+)\s+passed(?:,\s*(\d+)\s+skipped)?(?:,\s*(\d+)\s+warnings)?", output
    )
    passed = int(m_receipt.group(1)) if m_receipt else None
    remaining = int(m_receipt.group(2)) if m_receipt else None
    quarantined = int(m_receipt.group(3)) if m_receipt else None
    ok = bool(m_status and "OK" in m_status.group(0)) and proc.returncode == 0
    # Parse any FAILED lines
    failed_nodes = re.findall(r"^FAILED\s+(\S+)", output, re.MULTILINE)
    return {
        "exit_code": proc.returncode,
        "passed": passed,
        "baseline_failures_remaining": remaining,
        "quarantined": quarantined,
        "status_ok": ok,
        "failed_nodes": failed_nodes[:20],
        "receipt": receipt_path.as_posix(),
    }


def cmd_range(start: int, stop: int) -> int:
    """Process families in the [start, stop] closed row range (1-indexed)."""
    state = _load_state()
    if state.get("started_at_utc") is None:
        state["started_at_utc"] = _now_ts()
        _save_state(state)

    ts = _now_ts()
    for row, fname, skip_type, expected in FAMILIES:
        if row < start or row > stop:
            continue
        row_key = str(row)
        if row_key in state["families"] and state["families"][row_key].get("status") in ("ACCEPT", "REGRESS_REVERTED"):
            print(f"[skip] family {row} already processed: {state['families'][row_key]['status']}")
            continue

        fpath = BACKEND / "tests" / "invariants" / fname
        print(f"[family {row:2d}] {fname} ({skip_type} · expected={expected})")
        try:
            if skip_type == "partial":
                removed = _unquarantine_partial(fpath, expected)
            else:
                removed = _unquarantine_q1(fpath)
            print(f"  removed {removed} skip marker(s)")
        except Exception as exc:
            print(f"  HALT: un-quarantine failed: {exc}")
            state["families"][row_key] = {
                "file": fname,
                "skip_type": skip_type,
                "status": "HALT_UNQUARANTINE_ERROR",
                "error": str(exc),
                "ts": _now_ts(),
            }
            _save_state(state)
            return 2

        receipt = RECEIPTS / f"{ts}_wave_f_scope_a_{TAG}_family_{row:02d}_{fname.replace('.py','')}.log"
        result = _run_measure(receipt, row, fname)
        print(f"  passed={result['passed']} · remaining={result['baseline_failures_remaining']} · quarantined={result['quarantined']} · exit={result['exit_code']} · ok={result['status_ok']}")

        if result["status_ok"] and (result["baseline_failures_remaining"] == 0):
            status = "ACCEPT"
        else:
            # Regression → revert
            _revert_file(fpath)
            status = "REGRESS_REVERTED"
            print(f"  REVERTED {fname}")

        state["families"][row_key] = {
            "file": fname,
            "skip_type": skip_type,
            "expected_skip_count": expected,
            "status": status,
            "passed": result["passed"],
            "baseline_failures_remaining": result["baseline_failures_remaining"],
            "quarantined": result["quarantined"],
            "exit_code": result["exit_code"],
            "failed_nodes": result["failed_nodes"],
            "receipt": result["receipt"],
            "ts": _now_ts(),
        }
        _save_state(state)

    return 0


def cmd_status() -> int:
    state = _load_state()
    accept = [r for r, f in state.get("families", {}).items() if f.get("status") == "ACCEPT"]
    regress = [r for r, f in state.get("families", {}).items() if f.get("status") == "REGRESS_REVERTED"]
    halt = [r for r, f in state.get("families", {}).items() if f.get("status") == "HALT_UNQUARANTINE_ERROR"]
    print(f"Tag:              {TAG}")
    print(f"Sweep started:    {state.get('started_at_utc')}")
    print(f"Families ACCEPT:  {len(accept)}  rows={sorted(int(r) for r in accept)}")
    print(f"Families REGRESS: {len(regress)}  rows={sorted(int(r) for r in regress)}")
    print(f"Families HALT:    {len(halt)}  rows={sorted(int(r) for r in halt)}")
    print(f"Total processed:  {len(state.get('families', {}))} / 21")
    print(f"State file:       {_state_path()}")
    return 0


def cmd_revert_all() -> int:
    """Revert every quarantined file back to programme/track-a HEAD."""
    for _, fname, _, _ in FAMILIES:
        fpath = BACKEND / "tests" / "invariants" / fname
        _revert_file(fpath)
        print(f"reverted {fname}")
    return 0


def main() -> int:
    global TAG
    p = argparse.ArgumentParser()
    p.add_argument("--range", help="1-indexed row range START:STOP inclusive")
    p.add_argument("--status", action="store_true")
    p.add_argument("--revert-all", action="store_true")
    p.add_argument("--tag", default=TAG, help="Attempt tag used in state + receipt file names")
    args = p.parse_args()

    TAG = args.tag

    if args.status:
        return cmd_status()
    if args.revert_all:
        return cmd_revert_all()
    if args.range:
        start_s, stop_s = args.range.split(":")
        return cmd_range(int(start_s), int(stop_s))
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
