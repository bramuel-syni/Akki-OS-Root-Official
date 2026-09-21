"""services.business_continuity.anchors — BCA verbatim canon-anchor pin.

Canon anchors (verbatim, `Business_Continuity_Annex_v1` Document 3 Part D):

* S-10 (§1)
* BC-1 (§1)
* BC-2 (§1)
* S-11 (§2)
* BC-3 / BC-4 (§3) — OPEN, DEFAULT-PENDING-OVERRIDE

The BCA anchors pin the mechanism that already landed at:
  * `services/watch/continuity.py` + `continuity_policy.v0.json`
    (Wave E CP-E1 CA1-N5 · Wave G5c Ruling #1 RTO=3600)
  * `services/n_series/breach.py` + `breach_policy.v0.json`
    (Wave E CP-E2 CA1-N2 · 72h window)

This module is the CANONICAL VERBATIM SURFACE.  The assertion helpers
read the on-disk policy JSON that the mechanism reads at runtime and
raise if the mechanism drifts away from the canon anchor.  Drift
therefore fires a mechanical RED, not a silent flip.
"""

from __future__ import annotations

import json
from pathlib import Path

from services.watch import continuity as _continuity_module
from services.n_series import breach as _breach_module


# ---------------------------------------------------------------------------
# §A · S-10 (verbatim §1)
# ---------------------------------------------------------------------------

S_10_VERBATIM: str = (
    "The system will restore Ledger continuity within 3,600 "
    "seconds, under independent countersign, following any "
    "continuity-affecting incident."
)

S_10_RTO_SECONDS: int = 3600


# ---------------------------------------------------------------------------
# §B · BC-1 (verbatim §1)
# ---------------------------------------------------------------------------

BC_1_VERBATIM: str = (
    "Restoration MUST be countersigned by someone independent of the "
    "primary Ledger writer's own infrastructure — the same logic as "
    "the Watch's external witness: the verifier cannot be the thing "
    "that might be down.  A countersigner whose own access depends on "
    "the failed infrastructure does not satisfy this."
)


# ---------------------------------------------------------------------------
# §C · BC-2 (verbatim §1)
# ---------------------------------------------------------------------------

BC_2_VERBATIM: str = (
    "Ledger continuity is itself attested on a standing cadence, "
    "independent of any incident — proposed quarterly, DEFAULT-class, "
    "revisable on evidence.  This is a routine health check, not a "
    "response to failure; its purpose is confirming the RTO would "
    "hold if tested, before it has to be."
)

BC_2_CADENCE: str = "quarterly"
BC_2_CADENCE_CLASS: str = "default"


# ---------------------------------------------------------------------------
# §D · S-11 (verbatim §2)
# ---------------------------------------------------------------------------

S_11_VERBATIM: str = (
    "The system will issue breach notification within 72 hours of a "
    "qualifying incident, to the parties and authorities the incident "
    "requires."
)

S_11_WINDOW_HOURS: int = 72


# ---------------------------------------------------------------------------
# §E · BC-3 / BC-4 (open markers · silent flip forbidden)
# ---------------------------------------------------------------------------

BC_3_PENDING_OVERRIDE: str = "DEFAULT-PENDING-OVERRIDE"
BC_4_PENDING_OVERRIDE: str = "DEFAULT-PENDING-OVERRIDE"


# ---------------------------------------------------------------------------
# §F · pin helpers — read the runtime policies and assert alignment
# ---------------------------------------------------------------------------


class BCADriftError(RuntimeError):
    """Mechanism has drifted from the BCA canon anchor."""


def _load_continuity_policy() -> dict:
    p = Path(_continuity_module.__file__).with_name(
        "continuity_policy.v0.json"
    )
    return json.loads(p.read_text())


def _load_breach_policy() -> dict:
    p = Path(_breach_module.__file__).with_name("breach_policy.v0.json")
    return json.loads(p.read_text())


def assert_ca1_n5_rto_matches_s10() -> None:
    """S-10 (3,600 s) pins CA1-N5 policy `rto_target_seconds`."""
    policy = _load_continuity_policy()
    rto = policy.get("rto_target_seconds")
    # policy stores the number as a string per Wave G5c ruling
    if str(rto) != str(S_10_RTO_SECONDS):
        raise BCADriftError(
            f"CA1-N5 rto_target_seconds={rto!r} ≠ BCA S-10 "
            f"{S_10_RTO_SECONDS!r}"
        )


def assert_ca1_n5_countersigner_independence_matches_bc1() -> None:
    """BC-1 pins the CA1-N5 witness-independence check.

    The mechanism at `services.watch.continuity._witness_or_refuse`
    checks `WitnessIdentity_v0.independent_of_authorities is True`.
    """
    # The pin is the presence of the check.  Import the check and
    # verify it exists at module scope so drift (removal of the check)
    # fires here.
    if not hasattr(_continuity_module, "_witness_or_refuse"):
        raise BCADriftError(
            "CA1-N5 mechanism drift: _witness_or_refuse missing; "
            "BC-1 countersigner-independence pin cannot bind"
        )


def assert_ca1_n5_cadence_matches_bc2() -> None:
    """BC-2 pins CA1-N5 policy cadence + class."""
    policy = _load_continuity_policy()
    if policy.get("cadence") != BC_2_CADENCE:
        raise BCADriftError(
            f"CA1-N5 cadence={policy.get('cadence')!r} ≠ BCA BC-2 "
            f"{BC_2_CADENCE!r}"
        )
    if policy.get("cadence_class") != BC_2_CADENCE_CLASS:
        raise BCADriftError(
            f"CA1-N5 cadence_class={policy.get('cadence_class')!r} ≠ "
            f"BCA BC-2 {BC_2_CADENCE_CLASS!r}"
        )


def assert_ca1_n2_window_matches_s11() -> None:
    """S-11 (72 h) pins CA1-N2 policy `window_hours`."""
    policy = _load_breach_policy()
    if policy.get("window_hours") != S_11_WINDOW_HOURS:
        raise BCADriftError(
            f"CA1-N2 window_hours={policy.get('window_hours')!r} ≠ "
            f"BCA S-11 {S_11_WINDOW_HOURS!r}"
        )


__all__ = [
    "S_10_VERBATIM",
    "BC_1_VERBATIM",
    "BC_2_VERBATIM",
    "S_11_VERBATIM",
    "S_10_RTO_SECONDS",
    "BC_2_CADENCE",
    "BC_2_CADENCE_CLASS",
    "S_11_WINDOW_HOURS",
    "BC_3_PENDING_OVERRIDE",
    "BC_4_PENDING_OVERRIDE",
    "BCADriftError",
    "assert_ca1_n5_rto_matches_s10",
    "assert_ca1_n5_countersigner_independence_matches_bc1",
    "assert_ca1_n5_cadence_matches_bc2",
    "assert_ca1_n2_window_matches_s11",
]
