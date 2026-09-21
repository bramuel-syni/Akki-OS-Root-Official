"""W-DAP-STACK 2G · coalition graph + joint disclosure evaluation +
estate-wide DAP-35 bound.

Verbatim DAP-34 [S-23 · Doc 0 Att 3 · Doc 3 A5.18]: 'The system will
treat a coalition as one actor — cumulative conduct across principals
sharing a party, a mandate lineage, or a detected coordination
signature is evaluated jointly, not per principal.'

Verbatim DAP-35 [S-25 · new mandatory baseline]: 'The system will bound
what the estate releases in total — across all parties, all operations,
all time — so that no combination of parties can reconstruct what none
of them is entitled to.  Breaching the bound is a floor violation,
severance-eligible without inference.'

The estate-wide budget number is Security R-7 (OPEN owner ruling).
2G lands the mechanism with `DEFAULT_ESTATE_WIDE_BUDGET =
'DEFAULT-PENDING-OVERRIDE'`.  Silent flip forbidden until R-7 rules.

The coordination-signature threshold is Security R-11 (OPEN).  §5 note:
'R-8 through R-11 are needed before the corresponding gates are built,
and each is proposed as a DEFAULT-class value so that building is not
blocked on a final number.'  2G surfaces this as
`R11_COORDINATION_SIGNATURE_DEFERRED = 'DEFAULT-PENDING-OVERRIDE'`.
Detected-coordination-signature routing is FRICTION-ONLY per A5.2
until R-11 rules.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from pydantic import BaseModel, ConfigDict


# --- deferred owner rulings (flip-forbidden markers) ---------------
DEFAULT_ESTATE_WIDE_BUDGET: str = "DEFAULT-PENDING-OVERRIDE"
R11_COORDINATION_SIGNATURE_DEFERRED: str = "DEFAULT-PENDING-OVERRIDE"


class Coalition(BaseModel):
    """DAP-34 coalition: connected component of the admission graph."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    coalition_id: str
    members: FrozenSet[str]


class JointCeilingCheck(BaseModel):
    """DAP-34 joint ceiling check result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    coalition_id: str
    proposed_quantity: float
    used_so_far: float
    ceiling: float
    within_ceiling: bool


class EstateWideBreachVerdict(BaseModel):
    """DAP-35 verdict: breach is a floor violation, severance-eligible
    without inference."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    party_id: str
    proposed_quantity: float
    used_so_far: float
    ceiling: float
    floor_violation: bool
    severance_eligible: bool
    reason: str


# --- state ---------------------------------------------------------
# admission graph edges: keyed by (estate_id) -> {party_id -> set of link_ids}
_edges: Dict[str, Dict[str, Set[str]]] = {}
# per-party used disclosure
_party_used: Dict[Tuple[str, str], float] = {}   # (estate_id, party_id) -> quantity
# per-coalition ceiling (owner-set numeric)
_coalition_ceiling: Dict[Tuple[str, str], float] = {}   # (estate_id, coalition_id)
# estate-wide ceiling (owner-set numeric; default is the pending-override marker)
_estate_ceiling: Dict[str, float] = {}
_estate_used: Dict[str, float] = {}


def _add_edge(estate_id: str, a: str, b: str) -> None:
    ee = _edges.setdefault(estate_id, {})
    ee.setdefault(a, set()).add(b)
    ee.setdefault(b, set()).add(a)


def link_shared_party(
    *, estate_id: str, party_id: str, parent_party_id: str,
) -> None:
    """DAP-34 structural link: party under parent party is a coalition
    edge."""
    _add_edge(estate_id, party_id, f"party::{parent_party_id}")


def link_shared_mandate_lineage(
    *, estate_id: str, derived_party_id: str, parent_mandate_id: str,
) -> None:
    """DAP-34 structural link: mandate-lineage-derived parties are a
    coalition edge."""
    _add_edge(estate_id, derived_party_id, f"mandate::{parent_mandate_id}")


def _bfs_component(estate_id: str, start: str) -> Set[str]:
    ee = _edges.get(estate_id, {})
    seen: Set[str] = set()
    queue: List[str] = [start]
    while queue:
        node = queue.pop()
        if node in seen:
            continue
        seen.add(node)
        for nb in ee.get(node, ()):
            if nb not in seen:
                queue.append(nb)
    return seen


def resolve_coalition(*, estate_id: str, party_id: str) -> Coalition:
    """Return the coalition containing this party (may be size 1)."""
    component = _bfs_component(estate_id, party_id)
    # coalition_id = deterministic canonical member (sorted min real member)
    real_members = frozenset(m for m in component if not m.startswith(("party::", "mandate::")))
    if not real_members:
        real_members = frozenset({party_id})
    coalition_id = "coalition::" + "|".join(sorted(real_members))
    return Coalition(coalition_id=coalition_id, members=real_members)


def record_joint_disclosure(
    *, estate_id: str, party_id: str, quantity: float,
) -> None:
    """Record cumulative disclosure for both per-party and estate-wide
    accumulators."""
    _party_used[(estate_id, party_id)] = (
        _party_used.get((estate_id, party_id), 0.0) + quantity
    )
    _estate_used[estate_id] = _estate_used.get(estate_id, 0.0) + quantity


def joint_disclosure_used(*, estate_id: str, coalition_id: str) -> float:
    """DAP-34: sum of used disclosure across every member of the coalition."""
    total = 0.0
    for (e_id, p_id), q in _party_used.items():
        if e_id != estate_id:
            continue
        # is this party in the same coalition?
        c = resolve_coalition(estate_id=e_id, party_id=p_id)
        if c.coalition_id == coalition_id:
            total += q
    return total


def set_coalition_ceiling(
    *, estate_id: str, coalition_id: str, ceiling: float,
) -> None:
    _coalition_ceiling[(estate_id, coalition_id)] = ceiling


def check_joint_ceiling(
    *, estate_id: str, party_id: str, proposed_quantity: float,
) -> JointCeilingCheck:
    """DAP-34 + AC-10: evaluate the coalition jointly."""
    c = resolve_coalition(estate_id=estate_id, party_id=party_id)
    used = joint_disclosure_used(estate_id=estate_id, coalition_id=c.coalition_id)
    ceiling = _coalition_ceiling.get((estate_id, c.coalition_id), float("inf"))
    return JointCeilingCheck(
        coalition_id=c.coalition_id,
        proposed_quantity=proposed_quantity,
        used_so_far=used,
        ceiling=ceiling,
        within_ceiling=(used + proposed_quantity <= ceiling),
    )


def set_estate_wide_ceiling(*, estate_id: str, ceiling: float) -> None:
    """Owner-set numeric ceiling.  In production, this number comes
    from R-7 owner ruling; today, marker is DEFAULT-PENDING-OVERRIDE."""
    _estate_ceiling[estate_id] = ceiling


def check_estate_wide_ceiling(
    *, estate_id: str, proposed_quantity: float,
) -> bool:
    """DAP-35: sum across ALL parties/operations/time."""
    ceiling = _estate_ceiling.get(estate_id, float("inf"))
    used = _estate_used.get(estate_id, 0.0)
    return (used + proposed_quantity) <= ceiling


def evaluate_estate_wide_breach(
    *, estate_id: str, party_id: str, proposed_quantity: float,
) -> EstateWideBreachVerdict:
    """DAP-35: breach is a floor violation, severance-eligible without
    inference."""
    ceiling = _estate_ceiling.get(estate_id, float("inf"))
    used = _estate_used.get(estate_id, 0.0)
    projected = used + proposed_quantity
    breach = projected > ceiling
    return EstateWideBreachVerdict(
        party_id=party_id,
        proposed_quantity=proposed_quantity,
        used_so_far=used,
        ceiling=ceiling,
        floor_violation=breach,
        severance_eligible=breach,
        reason=(
            f"DAP-35: projected={projected} ceiling={ceiling}; "
            f"{'floor violation' if breach else 'within bound'}."
        ),
    )


def reset_state() -> None:
    """Test-only helper."""
    _edges.clear()
    _party_used.clear()
    _coalition_ceiling.clear()
    _estate_ceiling.clear()
    _estate_used.clear()
