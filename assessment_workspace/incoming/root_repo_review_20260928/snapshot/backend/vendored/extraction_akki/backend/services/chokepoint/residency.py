"""services.chokepoint.residency — governed region allowlist (CA1-N4).

Real facts on record this cycle:
  - aws.rds.db-restore-603-cluster.digicow_live · resource.region = eu-west-1
  - aws.rds.db-restore-603-cluster.ndume         · resource.region = eu-west-1
  - commissioning_akki-vm_..._ACCEPTED.json      · NO region on record
    (a real gap; the Data Shield surface renders this drawn-not-blank).

Allowlist source: services.chokepoint.residency_allowlist.v0.json.
Adding a region requires an Owner ruling.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ResidencyRefused(ValueError):
    """Raised when a crossing endpoint's region is not on the allowlist."""


_ALLOWLIST_PATH = Path(__file__).resolve().parent / "residency_allowlist.v0.json"


def _load_allowlist() -> Dict[str, Any]:
    # M12-W1c · SEC-1 runtime wire: unverifiable policy = closed gate.
    from services.chokepoint.policy_integrity import load_policy_with_integrity
    return load_policy_with_integrity(_ALLOWLIST_PATH)


def allowlisted_regions() -> List[str]:
    """Return the list of regions admissible for outbound crossings."""
    return sorted(entry["region"] for entry in _load_allowlist().get("regions", []))


def validate_region(region: str) -> None:
    """Raises ResidencyRefused if region is not on the allowlist.

    The 'not_on_record' sentinel is EXPLICITLY refused — a crossing must
    assert a region. Doc 01 §A5.6 + CA1-N4: silence is not admissible.
    """
    if not region:
        raise ResidencyRefused(
            "region_required — the crossing endpoint must declare a region."
        )
    if region == "not_on_record":
        raise ResidencyRefused(
            "region_not_on_record — the source record does not carry a region. "
            "Add region to the source's declaration before this path handles data."
        )
    if region not in allowlisted_regions():
        raise ResidencyRefused(
            f"region_off_allowlist — {region!r} not admissible for this estate. "
            f"Allowlisted regions on record: {allowlisted_regions()!r}. "
            "Adding a region requires an Owner ruling (CA1-N4 · residency)."
        )
