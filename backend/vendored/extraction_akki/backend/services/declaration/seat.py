"""Declaration seat — Canon 3 §6, Build Order 01 §4.A1.

Writer for record class `Actor.Declaration` (see
`contracts.record_matrix.THIN_KERNEL`). Captures declarations at setup
morning, checks in-force declarations at admit, records supersession.

No live actor — human, agent, or connector service — enters undeclared.
This banks Ruling-1 precondition (a).

Storage: `actor_declarations` collection (append-only via supersession
chain; never in-place mutate — Canon 8 §41 discipline).
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from contracts.actor_declaration import (
    DECLARATION_COLLECTION,
    ActorDeclaration,
    DeclarationVerdict,
)


# In-memory store for the thin kernel. Tests exercise this shape;
# production wiring plugs Motor collection through the same call sites.
_DECLARATIONS: Dict[str, ActorDeclaration] = {}


async def capture(declaration: ActorDeclaration) -> ActorDeclaration:
    """Capture (or supersede) an actor declaration. Append-only chain.

    Task identity: `declaration.capture` (registered — Canon 8 W11).
    """
    prior = _DECLARATIONS.get(declaration.actor_id)
    if prior is not None:
        # Supersession — link the prior via a new record whose
        # `superseded_by` field points to the new declaration id.
        prior_superseded = prior.model_copy(
            update={"superseded_by": declaration.actor_id + "::" + declaration.declared_at.isoformat()}
        )
        # Keep prior addressable by its supersession key.
        _DECLARATIONS[prior_superseded.superseded_by] = prior_superseded
    _DECLARATIONS[declaration.actor_id] = declaration
    return declaration


async def check(
    actor_id: str,
    *,
    required_scope: Optional[list[str]] = None,
    at: Optional[datetime] = None,
) -> DeclarationVerdict:
    """Return the declaration verdict for an actor at time `at`.

    Task identity: `declaration.check.per_admit` (registered).
    """
    at = at or datetime.now(timezone.utc)
    decl = _DECLARATIONS.get(actor_id)
    if decl is None:
        return "missing"
    if decl.superseded_by is not None:
        return "superseded"
    if decl.expires_at is not None and decl.expires_at < at:
        return "expired"
    if required_scope:
        scope_set = set(decl.scope)
        needed = set(required_scope)
        if not needed.issubset(scope_set):
            return "scope_mismatch"
    return "in_force"


def _reset_for_test() -> None:
    """Test-only reset. Not exported by the public API."""
    _DECLARATIONS.clear()


def _known_actors() -> list[str]:
    """Test-only introspection."""
    return list(_DECLARATIONS.keys())
