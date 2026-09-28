"""services.dap.m3_remainder — W-M3-SW11 · DAP-33/DAP-34/DAP-35 M3-remainder pin.

Canon anchors (verbatim, `MILESTONE_PROMISE_BINDING_20260913.md §M3`):

* S-22 · DAP-33 M3 remainder — Watch reproduction-probe (R-8
  baseline-period-deferred) + boundary gate.
* S-23 · DAP-34 M3 remainder — Watch coordination-signature threshold
  (R-11 baseline-period-deferred).
* S-25 · DAP-35/DAP-36 M3 remainder — Estate-level accumulator;
  BLOCKED on Security R-7 owner-input.

The mechanism-side constants live at:
  * `services.rulings.default_class_constants.SECURITY_R8_APPROACH`
  * `services.rulings.default_class_constants.SECURITY_R11_APPROACH`
  * `services.dap.disclosure_budget.DEFAULT_RELEASE_BUDGET`
  * `services.dap.coalition.DEFAULT_ESTATE_WIDE_BUDGET`

This module pins the M3-remainder markers to those mechanism-side
constants; silent flip breaks the ratchet.
"""

from __future__ import annotations

from services.rulings.default_class_constants import (
    SECURITY_R8_APPROACH,
    SECURITY_R11_APPROACH,
)
from services.dap.disclosure_budget import DEFAULT_RELEASE_BUDGET
from services.dap.coalition import DEFAULT_ESTATE_WIDE_BUDGET


# ---------------------------------------------------------------------------
# §A · S-22 · DAP-33 M3 remainder
# ---------------------------------------------------------------------------

S_22_M3_REMAINDER_VERBATIM: str = (
    "S-22 · Output-inspection deterministic gate (proposed A5.15 · "
    "DAP-33) — remainder from M1 discharged by M3's Watch reproduction-"
    "probe (R-8 baseline-period-deferred) + boundary gate."
)

R_8_BASELINE_PERIOD: str = "baseline_period"


# ---------------------------------------------------------------------------
# §B · S-23 · DAP-34 M3 remainder
# ---------------------------------------------------------------------------

S_23_M3_REMAINDER_VERBATIM: str = (
    "S-23 · Coalition as one actor (Doc-0 Attr-3 · proposed A5.18 · "
    "DAP-34) — remainder from M1 discharged by M3's coordination-"
    "signature threshold (R-11 baseline-period-deferred)."
)

R_11_BASELINE_PERIOD: str = "baseline_period"


# ---------------------------------------------------------------------------
# §C · S-25 · DAP-35/DAP-36 M3 remainder
# ---------------------------------------------------------------------------

S_25_M3_REMAINDER_VERBATIM: str = (
    "S-25 · Estate-level release budget (DAP-35 · DAP-36 · Doc-0 "
    "Attr-7) — remainder from M1 discharged by M3's estate-level "
    "accumulator; BLOCKED on Security R-7 owner-input."
)

R_7_BLOCKED_ON_OWNER_INPUT: str = "BLOCKED-PENDING-OWNER-INPUT"


# ---------------------------------------------------------------------------
# §D · pin helpers
# ---------------------------------------------------------------------------


class MarkerDriftError(RuntimeError):
    """A DEFAULT-PENDING-OVERRIDE marker has been silently flipped."""


def assert_r8_matches_ruling() -> None:
    if SECURITY_R8_APPROACH != R_8_BASELINE_PERIOD:
        raise MarkerDriftError(
            f"R-8 mechanism approach={SECURITY_R8_APPROACH!r} ≠ "
            f"canon anchor {R_8_BASELINE_PERIOD!r}"
        )


def assert_r11_matches_ruling() -> None:
    if SECURITY_R11_APPROACH != R_11_BASELINE_PERIOD:
        raise MarkerDriftError(
            f"R-11 mechanism approach={SECURITY_R11_APPROACH!r} ≠ "
            f"canon anchor {R_11_BASELINE_PERIOD!r}"
        )


def assert_r7_estate_budget_pending_override() -> None:
    """R-7 has TWO mechanism-side markers: the per-party surface in
    disclosure_budget.py, and the estate-wide surface in coalition.py.
    Silent flip of either breaks the ratchet.
    """
    if DEFAULT_RELEASE_BUDGET != "DEFAULT-PENDING-OVERRIDE":
        raise MarkerDriftError(
            f"disclosure_budget.DEFAULT_RELEASE_BUDGET="
            f"{DEFAULT_RELEASE_BUDGET!r} — silent flip forbidden"
        )
    if DEFAULT_ESTATE_WIDE_BUDGET != "DEFAULT-PENDING-OVERRIDE":
        raise MarkerDriftError(
            f"coalition.DEFAULT_ESTATE_WIDE_BUDGET="
            f"{DEFAULT_ESTATE_WIDE_BUDGET!r} — silent flip forbidden"
        )


__all__ = [
    "S_22_M3_REMAINDER_VERBATIM",
    "S_23_M3_REMAINDER_VERBATIM",
    "S_25_M3_REMAINDER_VERBATIM",
    "R_8_BASELINE_PERIOD",
    "R_11_BASELINE_PERIOD",
    "R_7_BLOCKED_ON_OWNER_INPUT",
    "MarkerDriftError",
    "assert_r8_matches_ruling",
    "assert_r11_matches_ruling",
    "assert_r7_estate_budget_pending_override",
]
