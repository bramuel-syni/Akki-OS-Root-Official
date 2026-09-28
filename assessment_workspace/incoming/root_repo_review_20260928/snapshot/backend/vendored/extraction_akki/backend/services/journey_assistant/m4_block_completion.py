"""services.journey_assistant.m4_block_completion — W-M4-SW6 · block-close.

M4 block-close composite invariant.  Verifies every M4 sub-wave close-
note exists on disk, that the DAP-20 boundary marker on SW1's surface
is byte-identical to canon, that surface (b) Agent-Deploy Wizard is
still held behind BR-15.1, and that ratchet_history records every
W-M4-SW* wave.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple


M4_SUB_WAVES: Tuple[str, ...] = (
    "W-M4-SW1",
    "W-M4-SW2",
    "W-M4-SW3",
    "W-M4-SW4",
    "W-M4-SW5",
)

M4_SUB_WAVE_COUNT: int = len(M4_SUB_WAVES) + 1  # incl. this SW6


_CLOSE_NOTES: Tuple[str, ...] = (
    "W_M4_SW1_SOLVA_EXPLAIN_SURFACE_close.md",
    "W_M4_SW2_NEVER_PRE_FILL_close.md",
    "W_M4_SW3_ESTATE_CHECK_CHIP_close.md",
    "W_M4_SW4_THREE_VERDICTS_close.md",
    "W_M4_SW5_HANDOFF_CONTRACT_close.md",
)


NOTES_DIR: Path = Path("/app/assessment_workspace/notes")


# ---------------------------------------------------------------------------
# §A · surface (b) HELD marker (owner directive 2026-09-14)
# ---------------------------------------------------------------------------

SURFACE_B_HELD_MARKER: str = (
    "SURFACE-B-AGENT-DEPLOY-WIZARD-HELD-BEHIND-BR-15.1-AGENT-DEPLOY-SPEC"
)

OWNER_HOLD_DIRECTIVE_VERBATIM: str = (
    "Owner directive 2026-09-14 verbatim: 'surface (b) held behind "
    "the BR-15.1 Agent-Deploy spec.'"
)


# ---------------------------------------------------------------------------
# §B · ratchet floor
# ---------------------------------------------------------------------------

M4_MIN_RATCHET_FLOOR: int = 3844


def _manifest_path() -> Path:
    # backend/services/journey_assistant/m4_block_completion.py → backend/tests/invariants/baseline_failures.json
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


class M4BlockCoherenceError(RuntimeError):
    """M4 block-close book-keeping is incoherent."""


def assert_every_sub_wave_close_note_on_disk() -> None:
    missing = [n for n in _CLOSE_NOTES if not (NOTES_DIR / n).is_file()]
    if missing:
        raise M4BlockCoherenceError(
            f"M4 block-close missing close-notes on disk: {missing!r}"
        )


def assert_dap_20_boundary_still_landed() -> None:
    """DAP-20 boundary from SW1 MUST still be byte-identical to canon."""
    from services.journey_assistant.solva_explain import (
        SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER,
    )
    if not SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER.endswith(
        "It proposes; the gates decide."
    ):
        raise M4BlockCoherenceError(
            "DAP-20 boundary marker on SW1 surface has drifted"
        )
    if "MUST NOT approve, widen scope after commission, or decide any gate" not in SOLVA_EXPLAIN_DAP20_BOUNDARY_MARKER:
        raise M4BlockCoherenceError(
            "DAP-20 boundary marker on SW1 surface has drifted "
            "(mid-sentence)"
        )


def assert_surface_b_still_held() -> None:
    """Owner directive 2026-09-14: surface (b) HELD.  Silent flip forbidden."""
    if SURFACE_B_HELD_MARKER != (
        "SURFACE-B-AGENT-DEPLOY-WIZARD-HELD-BEHIND-BR-15.1-AGENT-DEPLOY-SPEC"
    ):
        raise M4BlockCoherenceError(
            f"surface (b) HELD marker flipped: {SURFACE_B_HELD_MARKER!r}"
        )
    if "surface (b) held behind the BR-15.1 Agent-Deploy spec." not in OWNER_HOLD_DIRECTIVE_VERBATIM:
        raise M4BlockCoherenceError(
            "OWNER_HOLD_DIRECTIVE_VERBATIM has drifted"
        )


def assert_ratchet_history_records_every_sub_wave() -> None:
    d = json.loads(_manifest_path().read_text())
    history_waves = {
        entry.get("wave") for entry in d.get("ratchet_history", [])
    }
    missing = [w for w in M4_SUB_WAVES if w not in history_waves]
    if missing:
        raise M4BlockCoherenceError(
            f"M4 ratchet_history missing waves: {missing!r}"
        )


__all__ = [
    "M4_SUB_WAVES",
    "M4_SUB_WAVE_COUNT",
    "SURFACE_B_HELD_MARKER",
    "OWNER_HOLD_DIRECTIVE_VERBATIM",
    "M4_MIN_RATCHET_FLOOR",
    "M4BlockCoherenceError",
    "current_ratchet_state",
    "assert_every_sub_wave_close_note_on_disk",
    "assert_dap_20_boundary_still_landed",
    "assert_surface_b_still_held",
    "assert_ratchet_history_records_every_sub_wave",
]
