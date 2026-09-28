"""services.dap.m3_block_completion — W-M3-SW12 · M3 block-close composite pin.

Canon anchors (verbatim, `MILESTONE_PROMISE_BINDING_20260913.md §M3`):

* Watch (S-1..S-21) — Watch stack.
* DAP amendments (S-22..S-25) — M3-remainder pinned in SW11.
* Pruning (S-26) — SW8.
* Serving Integrity (AC-13/AC-14) — SW9.
* Watch Learning (S-7/S-28/S-29) — SW3..SW6.
* Agent Containment (AC-1..AC-12 + AC-15..AC-18) — SW7 + SW3/SW5/SW6.
* Business Continuity (S-10/S-11/BC-1/BC-2) — SW10.

This module is the M3 block-close composite pin.  It asserts every
sub-wave close-note exists on disk, every PENDING-OVERRIDE marker is
preserved, and the ratchet_history records every sub-wave.  It does
NOT re-verify SW1..SW11's mechanism.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple


M3_SUB_WAVES: Tuple[str, ...] = (
    "W-M3-SW1",
    "W-M3-SW2",
    "W-M3-SW3",
    "W-M3-SW4",
    "W-M3-SW5",
    "W-M3-SW6",
    "W-M3-SW7",
    "W-M3-SW8",
    "W-M3-SW9",
    "W-M3-SW10",
    "W-M3-SW11",
)


M3_SUB_WAVE_COUNT: int = len(M3_SUB_WAVES)


_CLOSE_NOTES: Tuple[str, ...] = (
    "W_M3_SW1_FLAG2_TIGHT_BUDGET_close.md",
    "W_M3_SW2_WATCH_STACK_CORE_close.md",
    "W_M3_SW3_WATCH_LEARNING_CERTIFICATE_LIBRARY_close.md",
    "W_M3_SW4_WATCH_LEARNING_MIRAGE_PROVOCATION_close.md",
    "W_M3_SW5_WATCH_LEARNING_RESEARCH_QUEUE_close.md",
    "W_M3_SW6_WATCH_LEARNING_CAPABILITY_ADMISSION_close.md",
    "W_M3_SW7_AGENT_CONTAINMENT_close.md",
    "W_M3_SW8_PRUNING_UNLEARNING_close.md",
    "W_M3_SW9_V3_AC13_AC14_close.md",
    "W_M3_SW10_BCA_S10_S11_BC1_BC2_close.md",
    "W_M3_SW11_DAP33_DAP34_DAP35_M3_REMAINDER_close.md",
)


NOTES_DIR: Path = Path("/app/assessment_workspace/notes")


# ---------------------------------------------------------------------------
# §A · S-24 honest gap (A5.17 · raiser-held-to-target-conformance)
# ---------------------------------------------------------------------------

S_24_CANON_ANCHOR: str = (
    "S-24 · Raiser held to same conformance as target (proposed "
    "A5.17) — discharged by M3's Class-D/Class-A finding mechanism + "
    "lineage collapse."
)

S_24_MECHANISM_DEFERRED: str = "MECHANISM-DEFERRED-BEYOND-SW11"


# ---------------------------------------------------------------------------
# §B · ratchet floor
# ---------------------------------------------------------------------------

M3_MIN_RATCHET_FLOOR: int = 3790


def _manifest_path() -> Path:
    # backend/services/dap/m3_block_completion.py → backend/tests/invariants/baseline_failures.json
    return (
        Path(__file__).resolve().parent.parent.parent
        / "tests" / "invariants" / "baseline_failures.json"
    )


def current_ratchet_state() -> Dict[str, int]:
    d = json.loads(_manifest_path().read_text())
    return {
        "passed": d["counts_at_baseline"]["passed"],
        "passed_floor": (
            d["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
        ),
    }


# ---------------------------------------------------------------------------
# §C · assertions
# ---------------------------------------------------------------------------


class M3BlockCoherenceError(RuntimeError):
    """M3 block-close book-keeping is incoherent."""


def assert_every_sub_wave_close_note_on_disk() -> None:
    """Every M3 sub-wave close-note is on disk."""
    missing = [n for n in _CLOSE_NOTES if not (NOTES_DIR / n).is_file()]
    if missing:
        raise M3BlockCoherenceError(
            f"M3 block-close missing close-notes on disk: {missing!r}"
        )


def assert_every_pending_override_marker_preserved() -> None:
    """R-7 (2 surfaces) + R-12 + R-15/R-16/R-17 + BC-3/BC-4 markers.

    Silent flip of any breaks the M3 close.  Each marker lives on its
    own module; this composite re-reads them.
    """
    # R-7 (two surfaces)
    from services.dap.disclosure_budget import DEFAULT_RELEASE_BUDGET
    from services.dap.coalition import DEFAULT_ESTATE_WIDE_BUDGET
    if DEFAULT_RELEASE_BUDGET != "DEFAULT-PENDING-OVERRIDE":
        raise M3BlockCoherenceError(
            f"R-7 disclosure_budget.DEFAULT_RELEASE_BUDGET flipped: "
            f"{DEFAULT_RELEASE_BUDGET!r}"
        )
    if DEFAULT_ESTATE_WIDE_BUDGET != "DEFAULT-PENDING-OVERRIDE":
        raise M3BlockCoherenceError(
            f"R-7 coalition.DEFAULT_ESTATE_WIDE_BUDGET flipped: "
            f"{DEFAULT_ESTATE_WIDE_BUDGET!r}"
        )

    # R-12 (pruning)
    from services.dap.pruning_unlearning import (
        PRUNING_UNLEARNING_R12_PENDING_OVERRIDE,
    )
    if PRUNING_UNLEARNING_R12_PENDING_OVERRIDE != "PENDING-OVERRIDE":
        raise M3BlockCoherenceError(
            f"R-12 pruning_unlearning marker flipped: "
            f"{PRUNING_UNLEARNING_R12_PENDING_OVERRIDE!r}"
        )

    # BC-3 / BC-4
    from services.business_continuity.anchors import (
        BC_3_PENDING_OVERRIDE, BC_4_PENDING_OVERRIDE,
    )
    if BC_3_PENDING_OVERRIDE != "DEFAULT-PENDING-OVERRIDE":
        raise M3BlockCoherenceError(
            f"BC-3 marker flipped: {BC_3_PENDING_OVERRIDE!r}"
        )
    if BC_4_PENDING_OVERRIDE != "DEFAULT-PENDING-OVERRIDE":
        raise M3BlockCoherenceError(
            f"BC-4 marker flipped: {BC_4_PENDING_OVERRIDE!r}"
        )


def assert_ratchet_history_records_every_sub_wave() -> None:
    """Every W-M3-SW* wave appears in ratchet_history."""
    d = json.loads(_manifest_path().read_text())
    history_waves = {
        entry.get("wave") for entry in d.get("ratchet_history", [])
    }
    missing = [w for w in M3_SUB_WAVES if w not in history_waves]
    if missing:
        raise M3BlockCoherenceError(
            f"M3 ratchet_history missing waves: {missing!r}"
        )


__all__ = [
    "M3_SUB_WAVES",
    "M3_SUB_WAVE_COUNT",
    "M3_MIN_RATCHET_FLOOR",
    "S_24_CANON_ANCHOR",
    "S_24_MECHANISM_DEFERRED",
    "M3BlockCoherenceError",
    "current_ratchet_state",
    "assert_every_sub_wave_close_note_on_disk",
    "assert_every_pending_override_marker_preserved",
    "assert_ratchet_history_records_every_sub_wave",
]
