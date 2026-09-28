"""W-DATA-SUITE-V2-LIFT · CP-D3 · Source registry (UnitRefs-only, Canon-4 §22)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


SOURCE_KINDS: frozenset = frozenset({"file", "query", "url", "note"})


class SourceRefInvalid(Exception):
    """Raised when a SourceRef would violate the UnitRef/kind contract."""


@dataclass(frozen=True)
class SourceRef:
    unit_ref: str
    kind: str
    size_bytes: int

    def __post_init__(self):
        if not self.unit_ref:
            raise SourceRefInvalid("SourceRef.unit_ref must be non-empty")
        if self.kind not in SOURCE_KINDS:
            raise SourceRefInvalid(
                f"SourceRef.kind {self.kind!r} not in {sorted(SOURCE_KINDS)}"
            )


def list_sources(session_id: str) -> Sequence[SourceRef]:
    """Return `SourceRef` tuple for the session.

    Wave-scope: implementation returns empty tuple; live-session
    integration is a follow-on (out of this wave's CP scope).
    """
    _ = session_id  # signature-locked; live lookup follow-on
    return ()
