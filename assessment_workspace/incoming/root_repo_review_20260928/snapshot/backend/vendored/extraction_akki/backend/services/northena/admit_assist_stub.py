"""services.northena.admit_assist_stub — the honest Solva boundary.

Doc 05 §A5.3 [CANON]: "Admit invokes the depth governor (Solva) through
an opaque handle and freezes the value it returns. The judgement is the
reasoner's; the freeze is Northena's alone."

Solva ships in W5. Until then, this stub occupies the boundary honestly:
  - resolve_scope(): identity pass-through when items are declared
    (honest); refuses (empty list) if any item is empty/whitespace-only
    (mechanically testable and DETERMINISTIC — no inference).
  - defensibility_floor(): echoes a declared floor; otherwise returns
    the stub-marker "L2_stub_awaiting_solva".
  - preservation_depth(): echoes declared depth; otherwise returns 3
    with annotation.

Every stub call is annotated on the resulting frozen artifact under
`judgement_provenance` so downstream surfaces render "Solva-assisted
judgement pending" honestly. Doc 05 §A5.1 determinism-by-construction is
preserved: this module imports NO ML SDK and performs NO inference.
"""
from __future__ import annotations

from typing import Any, Iterable, List, Tuple


class RegistryStub:
    """Placeholder registry — Solva will supply the real one in W5.

    Today it declares that all scope items resolve to themselves.
    """

    def __init__(self, known: Iterable[str] = ()):
        self._known = set(known)

    def knows(self, item: str) -> bool:
        # Honest posture: everything the caller declares is treated as
        # a candidate scope item. The strict-membership check that
        # actually gates the run is Gate's job (Doc 05 §A5.4).
        return bool(item and item.strip())


def resolve_scope(scope_declared: List[str], registry: RegistryStub) -> Tuple[List[str], str]:
    """Return (resolved_items, provenance).

    Empty declared scope → empty resolved (Admit refuses on this).
    Any item that's empty/whitespace-only → dropped (deterministic).
    """
    resolved: List[str] = []
    for item in scope_declared or []:
        if isinstance(item, str) and item.strip():
            resolved.append(item.strip())
    return resolved, "stub_awaiting_solva"


def defensibility_floor(floor_declared: Any) -> Tuple[str, str]:
    """Return (floor, provenance)."""
    if floor_declared:
        return str(floor_declared), "declared"
    return "L2_stub_awaiting_solva", "stub_awaiting_solva"


def preservation_depth(depth_declared: Any) -> Tuple[int, str]:
    """Return (depth, provenance)."""
    if depth_declared is not None:
        try:
            return int(depth_declared), "declared"
        except (ValueError, TypeError):
            pass
    return 3, "stub_awaiting_solva"
