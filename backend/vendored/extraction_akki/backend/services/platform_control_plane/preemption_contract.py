"""services.platform_control_plane.preemption_contract — CP-P4-CP8 · M9.

Preventive-charter preemption-admission refusal wrapper per Akki OS
Pilot Platform Reference v0.2 §6.4 M-Cp-4 verbatim (CONTRACT-MODELED
· verify-on-real-infra):

    Reserved-capacity jobs are never pre-empted. Burst jobs are
    pre-emptible by another tenant's reserved-capacity jobs within
    SLA.

Vocabulary (§6.4 verbatim capacity kinds):
- CAPACITY_KINDS = ("reserved", "burst") · OPEN str · case-sensitive.

Refusals (fail-fast order):
1. victim_capacity_kind not in CAPACITY_KINDS → UnknownCapacityKindRefused
2. attacker_capacity_kind not in CAPACITY_KINDS → UnknownCapacityKindRefused
3. victim_capacity_kind == "reserved" → PreemptingReservedRefused (M-Cp-4 clause 1)
4. attacker_capacity_kind != "reserved" (i.e., burst preemptor on
   burst victim) → BurstPreemptorMustBeReservedRefused (M-Cp-4 clause 2)

Cross-tenant vs same-tenant is CONTRACT-MODELED at caller (the
"another tenant's" sub-clause of M-Cp-4 clause 2 is left as a
caller-composition against integration.tenant_id / allocation.
tenant_id).

Standing-line proof:
- Pure function · no side effects · caller composes.
- CONTRACT-MODELED shape-freeze · runtime binding is bind-only.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

from typing import Tuple


PREEMPTION_CONTRACT_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §6.4 "
    "M-Cp-4 verbatim: Reserved-capacity jobs are never pre-empted. "
    "Burst jobs are pre-emptible by another tenant's reserved-"
    "capacity jobs within SLA. (CONTRACT-MODELED · verify-on-real-"
    "infra.)"
)


# §6.4 verbatim capacity vocabulary · OPEN str · case-sensitive.
CAPACITY_KINDS: Tuple[str, ...] = (
    "reserved",
    "burst",
)


class PreemptionContractRefused(Exception):
    """Root refusal for preemption-contract invariants."""


class UnknownCapacityKindRefused(PreemptionContractRefused):
    """Refused: capacity kind not in CAPACITY_KINDS (case-sensitive).
    §6.4 verbatim: reserved | burst."""


class PreemptingReservedRefused(PreemptionContractRefused):
    """Refused: victim is reserved-capacity · §6.4 M-Cp-4 clause 1
    'Reserved-capacity jobs are never pre-empted'."""


class BurstPreemptorMustBeReservedRefused(PreemptionContractRefused):
    """Refused: burst attacker cannot preempt burst victim · §6.4
    M-Cp-4 clause 2 specifies burst is pre-emptible ONLY by
    reserved-capacity jobs."""


def assert_preemption_admissible(
    *,
    victim_capacity_kind: str,
    attacker_capacity_kind: str,
) -> None:
    """Preventive-charter refusal wrapper · caller-invoked only.

    Refusal order (fail fast):
    1. victim_capacity_kind not in CAPACITY_KINDS → UnknownCapacityKindRefused.
    2. attacker_capacity_kind not in CAPACITY_KINDS → UnknownCapacityKindRefused.
    3. victim_capacity_kind == "reserved" → PreemptingReservedRefused (M-Cp-4 clause 1).
    4. attacker_capacity_kind != "reserved" → BurstPreemptorMustBeReservedRefused (M-Cp-4 clause 2).

    Cross-tenant ("another tenant's") sub-clause is CONTRACT-MODELED
    at caller.

    Returns None on admit."""
    kinds = frozenset(CAPACITY_KINDS)
    if victim_capacity_kind not in kinds:
        raise UnknownCapacityKindRefused(
            f"unknown-capacity-kind refused: victim_capacity_kind "
            f"not among {len(CAPACITY_KINDS)} §6.4 kinds "
            f"(case-sensitive)."
        )
    if attacker_capacity_kind not in kinds:
        raise UnknownCapacityKindRefused(
            f"unknown-capacity-kind refused: attacker_capacity_kind "
            f"not among {len(CAPACITY_KINDS)} §6.4 kinds "
            f"(case-sensitive)."
        )
    if victim_capacity_kind == "reserved":
        raise PreemptingReservedRefused(
            f"preempting-reserved refused: reserved-capacity jobs "
            f"are never pre-empted · §6.4 M-Cp-4."
        )
    if attacker_capacity_kind != "reserved":
        raise BurstPreemptorMustBeReservedRefused(
            f"burst-preemptor-must-be-reserved refused: burst "
            f"victim is pre-emptible only by reserved attackers · "
            f"§6.4 M-Cp-4."
        )
    return None


__all__ = [
    "PREEMPTION_CONTRACT_ANCHOR",
    "CAPACITY_KINDS",
    "PreemptionContractRefused",
    "UnknownCapacityKindRefused",
    "PreemptingReservedRefused",
    "BurstPreemptorMustBeReservedRefused",
    "assert_preemption_admissible",
]
