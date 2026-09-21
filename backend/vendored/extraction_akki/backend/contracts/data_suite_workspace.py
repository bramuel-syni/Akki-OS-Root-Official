"""W-DATA-SUITE-V2-LIFT · contracts · WorkspaceState + SurfaceClass.

Frozen carrier for a Data-Suite session state; closed 3-value SurfaceClass
enum shared by the workspace boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SurfaceClass(str, Enum):
    """Closed 3-value classifier for Data-Suite surfaces."""

    RAPID = "RAPID"
    DEEP_DIVE = "DEEP_DIVE"
    SOURCES = "SOURCES"


@dataclass(frozen=True)
class WorkspaceState:
    """Frozen record of a Data-Suite workspace session state."""

    session_id: str
    tab_hint: str
    source_refs_count: int
