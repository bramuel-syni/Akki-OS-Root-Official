"""W-DATA-SUITE-V2-LIFT · CP-D4 · Analyze-tab contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


ANALYZE_TAB_KINDS: frozenset = frozenset({"rapid", "deep_dive", "sources"})


class AnalyzeTabInvalid(Exception):
    """Raised when a tab construction violates the tab_kind contract."""


def _refuse_bad_kind(expected: str, actual: str) -> None:
    if actual != expected:
        raise AnalyzeTabInvalid(
            f"tab_kind mismatch: expected {expected!r}, got {actual!r}"
        )


@dataclass(frozen=True)
class AnalyzeRapid:
    session_id: str
    tab_kind: str
    unit_ref_count: int

    def __post_init__(self):
        _refuse_bad_kind("rapid", self.tab_kind)


@dataclass(frozen=True)
class AnalyzeDeepDive:
    session_id: str
    tab_kind: str
    synthesis_sha256_hex: str

    def __post_init__(self):
        _refuse_bad_kind("deep_dive", self.tab_kind)


@dataclass(frozen=True)
class AnalyzeSources:
    session_id: str
    tab_kind: str
    unit_refs: Sequence[str]

    def __post_init__(self):
        _refuse_bad_kind("sources", self.tab_kind)
