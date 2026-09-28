"""W-DATA-SUITE-V2-LIFT · CP-D7 · Analysis-lifecycle state machine.

Case-agnostic re-shape of the donor's implicit upload → active → session-close
lifecycle (`Akki-Executive-Core/backend/services/analysis_lifecycle.py`, 2026)
into a canonical 4-state closed set {DRAFT, PROCESSING, READY, ARCHIVED}.

The `Analysis` lifecycle is deliberately a DISTINCT type from CP-D2's
`Workspace` lifecycle even though the state names coincide: callers cannot
accidentally cross an Analysis state with a Workspace state.

Wave-honest limit: no async / GridFS / HTTP / DB call is lifted from the
donor here — this module is contract-only. The donor's actual upload +
GridFS + session-close mechanics stay OUT-OF-SCOPE per the grounding brief
(that plumbing is an out-of-wave concern; the wave lifts only the lifecycle
shape).
"""

from __future__ import annotations

from enum import Enum


class AnalysisLifecycleState(str, Enum):
    """Closed 4-value canonical lifecycle state for a Data-Suite Analysis."""

    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    READY = "READY"
    ARCHIVED = "ARCHIVED"


ANALYSIS_TRANSITIONS: frozenset = frozenset({
    (AnalysisLifecycleState.DRAFT, AnalysisLifecycleState.PROCESSING),
    (AnalysisLifecycleState.PROCESSING, AnalysisLifecycleState.READY),
    (AnalysisLifecycleState.READY, AnalysisLifecycleState.ARCHIVED),
})


ANALYSIS_TERMINAL_STATES: frozenset = frozenset({AnalysisLifecycleState.ARCHIVED})


class IllegalAnalysisTransition(Exception):
    """Raised when a caller attempts a transition not in `ANALYSIS_TRANSITIONS`."""


def assert_analysis_transition_legal(
    src: AnalysisLifecycleState,
    dst: AnalysisLifecycleState,
) -> None:
    """Refuse via `IllegalAnalysisTransition` if (src, dst) not declared."""
    if (src, dst) not in ANALYSIS_TRANSITIONS:
        raise IllegalAnalysisTransition(
            f"illegal analysis transition: {src.value!r} -> {dst.value!r} · "
            f"legal transitions: "
            f"{sorted((a.value, b.value) for a, b in ANALYSIS_TRANSITIONS)}"
        )
