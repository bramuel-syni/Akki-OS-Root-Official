"""services.evidence_register.terminal_test_guard · Doc 19B §EP-4 verbatim.

Owner directive verbatim (2026-08-26T~12:40Z · Batch 1 · reclassification 1):
    'the evidence register and dual-judge protocol must exist before
     the terminal test runs, or that test's verdict is single-judge
     permanently — no retroactive fix once it's run.'

W11 D · CP-D0 landing · authorized outside Wave D reusable scope
because owner marked EP-4 blocking on the live-GPU critical path
(SSH-key sequence pre-authorized to fire).

The guard is a MEASUREMENT (§Doc 8 line 170 last-sentence pattern):
it actually reads the evidence register from disk each invocation
and computes readiness. Never a cached bool, never a config flag.

Called as a PRECONDITION before any terminal_test execution site.
Refusal is structured, citing §EP-4 verbatim. Passing returns a
receipt-shaped dict the caller stamps into the terminal-test run
record.
"""
from __future__ import annotations

from typing import Any, Dict, List

from contracts.evidence_register_row_v0 import EvidenceRegisterRowV0
from services.evidence_register import register


# --- §EP-4 verbatim spec text · load-bearing in the refusal envelope ---
EP4_VERBATIM: str = (
    "the evidence register and dual-judge protocol must exist before "
    "the terminal test runs, or that test's verdict is single-judge "
    "permanently — no retroactive fix once it's run"
)


EP2_VERBATIM: str = (
    "Dual-judge scoring (A-2) applies at every named site in §19B.4, "
    "plus any future site where a judgement call becomes a published "
    "number"
)


class TerminalTestGuardRefusal(RuntimeError):
    """§EP-4 structural refusal. Precondition unmet — the terminal
    test cannot fire. Do not swallow; do not suppress."""


def _terminal_test_rows_on_record() -> List[EvidenceRegisterRowV0]:
    """§EP-4 measurement · reads the register file from disk."""
    return [r for r in register.read_all() if r.named_site == "terminal_test"]


def precheck_terminal_test_ready() -> Dict[str, Any]:
    """Structural precondition check for §19B.4 terminal_test execution.

    Refuses (TerminalTestGuardRefusal) when:
      1. Evidence register is empty (no rows at all).
      2. Register is non-empty but carries NO row with
         named_site='terminal_test'.
      3. A terminal_test row exists but carries <2 judges OR the
         judges/judge_versions counts mismatch (defense-in-depth
         against hand-edited JSONL).

    Returns (on pass) a receipt dict:
      {
        'ready': True,
        'resolved_row_id': '<figure_id>',
        'judges_count': int,
        'kappa': float,
        'rubric_version': str,
        'spec_verbatim_ep4': str,  # so the caller can stamp it.
      }
    """
    all_rows = register.read_all()
    if not all_rows:
        raise TerminalTestGuardRefusal(
            f"Doc 19B §EP-4 verbatim: '{EP4_VERBATIM}.' "
            "Evidence register is EMPTY · precondition unmet · terminal "
            "test cannot fire. Land a dual-judge terminal_test row "
            "(POST /api/evidence-register) before invoking the terminal "
            "test site."
        )

    terminal_rows = _terminal_test_rows_on_record()
    if not terminal_rows:
        raise TerminalTestGuardRefusal(
            f"Doc 19B §EP-4 verbatim: '{EP4_VERBATIM}.' "
            "Evidence register is active but carries NO row for "
            "named_site='terminal_test' · precondition unmet. Doc 19B "
            f"§EP-2 verbatim: '{EP2_VERBATIM}.'"
        )

    # Defense-in-depth: contract already enforces min 2 judges + count
    # parity, but honour disk-level tamper by re-checking here.
    for row in terminal_rows:
        if len(row.judges) < 2:
            raise TerminalTestGuardRefusal(
                f"Doc 19B §EP-2 verbatim: '{EP2_VERBATIM}.' "
                f"terminal_test row {row.figure_id!r} carries "
                f"{len(row.judges)} judge(s) · dual-judge minimum is 2 "
                "· row rejected."
            )
        if len(row.judges) != len(row.judge_versions):
            raise TerminalTestGuardRefusal(
                f"Doc 19B §EP-2 verbatim: '{EP2_VERBATIM}.' "
                f"terminal_test row {row.figure_id!r} carries "
                f"{len(row.judges)} judges vs {len(row.judge_versions)} "
                "judge_versions · counts must match · row rejected."
            )

    # First (or only) valid terminal_test row wins the receipt.
    resolved = terminal_rows[0]
    return {
        "ready": True,
        "resolved_row_id": resolved.figure_id,
        "judges_count": len(resolved.judges),
        "kappa": resolved.kappa,
        "rubric_version": resolved.rubric_version,
        "spec_verbatim_ep4": EP4_VERBATIM,
        "spec_verbatim_ep2": EP2_VERBATIM,
    }
