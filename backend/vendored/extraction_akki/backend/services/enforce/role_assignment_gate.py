"""services/enforce/role_assignment_gate.py · M11-W3 · Option C thin-adapter."""
from __future__ import annotations
from typing import Any, Mapping

from services.data.repository import Repository
from services.platform_control_plane.role_assignment import (
    RoleAssignment,
    assert_role_assignment_valid,
)


COLLECTION_NAME: str = "role_assignment"


async def create_role_assignment(*, repo: Repository, doc: Mapping[str, Any]) -> Any:
    """M9 refuser assert_role_assignment_valid runs FIRST; Repository insert runs SECOND."""
    assignment = RoleAssignment(**doc)
    assert_role_assignment_valid(assignment=assignment)
    return await repo.insert_one(dict(doc))
