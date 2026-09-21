"""W-DAP-STACK 2H · component boundary + composition close.

Anchors:
* DAP-30 (honesty grammar) · browse degrades, never silently complete.
* DAP-31+ / DAP-32+ (Serving_Integrity_Amendment §B V-2) · declared
  dependency markers on SFP-8 (M2 Rules-Service scope).
* A1 (compute-to-data) · every egress configuration refused + recorded.
* DAP-Spec §7 · DAP composes; DAP does not execute.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
from typing import Dict, List, Tuple

from pydantic import BaseModel, ConfigDict


# --- DAP-31+ / DAP-32+ declared dependency markers -------------------
DAP_31_PLUS_DEPENDS_ON_SFP_8: dict = {
    "anchor": "DAP-31+",
    "verbatim": (
        "The reproduction probe MUST execute on an SFP-8-conforming "
        "serving path.  A probe result computed on a non-conforming "
        "path is not a valid gate decision."
    ),
    "depends_on": "SFP-8",
    "scope": "M2_RULES_SERVICE",
    "posture": "DECLARED_DEPENDENCY_NOT_GUESS",
    "amendment": "Serving_Integrity_Amendment_v1 §B V-2 · §7 M1 note",
}

DAP_32_PLUS_DEPENDS_ON_SFP_8: dict = {
    "anchor": "DAP-32+",
    "verbatim": (
        "Battery results are valid only from an SFP-8-conforming path "
        "— deviation observed in the mirage is attributable to the "
        "model under test because the engine is required to contribute "
        "none."
    ),
    "depends_on": "SFP-8",
    "scope": "M2_RULES_SERVICE",
    "posture": "DECLARED_DEPENDENCY_NOT_GUESS",
    "amendment": "Serving_Integrity_Amendment_v1 §B V-2 · §7 M1 note",
}


# --- DAP-30 browse degradation surface -------------------------------
class BrowseSnapshot(BaseModel):
    """DAP-30: honest grammar — carry payload + staleness + as-of."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    estate_id: str
    units: Tuple[str, ...]
    stale: bool
    as_of_iso: str
    refused: bool


def browse_degraded_with_as_of(
    *,
    estate_id: str,
    available_units: Tuple[str, ...],
    census_complete: bool,
    as_of_iso: str,
    census_expected_size: int = 0,
) -> BrowseSnapshot:
    """DAP-30: return what we have, marked as stale with as-of time.
    Refuses the silent-complete presentation of an incomplete estate."""
    if census_complete and census_expected_size and len(available_units) < census_expected_size:
        raise ValueError(
            f"DAP-30 verbatim ban: 'never silently presents an incomplete "
            f"estate as complete' — census_complete=True but "
            f"available={len(available_units)} < expected={census_expected_size}"
        )
    return BrowseSnapshot(
        estate_id=estate_id,
        units=tuple(available_units),
        stale=(not census_complete),
        as_of_iso=as_of_iso,
        refused=False,
    )


# --- A1 · chokepoint refuse-if-egress --------------------------------
class EgressRefused(RuntimeError):
    """A1 + DAP-28 fail-closed chokepoint: egress-outside-perimeter refused."""


_egress_log: Dict[str, List[Dict]] = {}


_ALLOWED_DESTINATIONS = frozenset({
    # In production these would be RESOLVED against Rules Service.
    # In-perimeter destinations that the estate ACCEPTS as compute-to-data.
    "in_perimeter_compute_pool",
    "estate_local_targeta_worker",
})


def refuse_if_egress(
    *,
    operation: str,
    estate_id: str,
    destination: str,
    party_id: str,
) -> None:
    """A1: 'No configuration permits it; every attempt refused and
    recorded.'  Any destination outside the estate perimeter refuses."""
    entry = {
        "operation": operation,
        "estate_id": estate_id,
        "destination": destination,
        "party_id": party_id,
        "outcome": "refused",
    }
    _egress_log.setdefault(estate_id, []).append(entry)
    if destination not in _ALLOWED_DESTINATIONS:
        raise EgressRefused(
            f"A1 + DAP §7 §4.1 fail-closed: egress refused. "
            f"operation={operation!r} estate={estate_id!r} "
            f"destination={destination!r} party={party_id!r}. "
            f"No configuration permits estate-data egress outside the perimeter."
        )
    # If destination is somehow in the allowed set, still record but as accepted;
    # any allowed destination would need Rules-Service ceremony to admit — not built.


def record_refused_egress_attempt(
    *, estate_id: str, operation: str, destination: str, party_id: str,
) -> None:
    """Explicit recorder for A1 audit trail (composes with refuse_if_egress)."""
    _egress_log.setdefault(estate_id, []).append({
        "operation": operation,
        "estate_id": estate_id,
        "destination": destination,
        "party_id": party_id,
        "outcome": "refused",
    })


def listed_refused_egress_attempts(*, estate_id: str) -> List[Dict]:
    return list(_egress_log.get(estate_id, []))


# --- DAP-Spec §7 · component boundary — compose, never execute -------
_FORBIDDEN_VERB_PATTERNS = (
    re.compile(r"^execute(_|$)"),
    re.compile(r"^serve(_|$)"),
    re.compile(r"^run_extraction(_|$)"),
    re.compile(r"^invoke_model(_|$)"),
    re.compile(r"^perform_extraction(_|$)"),
)


def assert_composes_only() -> None:
    """DAP-Spec §7: DAP composes; DAP does not execute.  Scan every
    services.dap.* submodule for forbidden execution verbs in its
    public callable surface.  Raise AssertionError on any hit."""
    import services.dap as dap_pkg
    offenders: List[str] = []
    for m in pkgutil.iter_modules(dap_pkg.__path__, prefix="services.dap."):
        mod = importlib.import_module(m.name)
        for name in dir(mod):
            if name.startswith("_"):
                continue
            attr = getattr(mod, name, None)
            if not callable(attr):
                continue
            for pat in _FORBIDDEN_VERB_PATTERNS:
                if pat.match(name):
                    offenders.append(f"{m.name}.{name}")
    if offenders:
        raise AssertionError(
            f"DAP-Spec §7 breach: DAP surface exposes execution verbs — "
            f"{offenders}.  DAP composes; DAP does not execute."
        )


def reset_state() -> None:
    """Test-only helper."""
    _egress_log.clear()
