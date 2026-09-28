"""services/solva_v2/trace.py — CP-S5.

Canon-4 §26: trace from the first commit.  Every Solva session emits
one SolvaTrace containing the reasoning path, load-bearing units,
computed class, and conclusion.

R-C2 marker: SolvaTrace.au_3b_defensible defaults to False (Doc-0 G-8
not built).  Silent flip forbidden by CP-S5 invariant.
"""
from __future__ import annotations

from typing import Iterable

from contracts.solva_reasoning import AssertionClass, SolvaTrace, UnitRef


def record_trace(
    *,
    session_id: str,
    reasoning_path: Iterable[str],
    load_bearing_units: Iterable[UnitRef],
    computed_class: AssertionClass,
    conclusion: str,
) -> SolvaTrace:
    return SolvaTrace(
        session_id=session_id,
        reasoning_path=tuple(reasoning_path),
        load_bearing_units=tuple(load_bearing_units),
        computed_class=computed_class,
        conclusion=conclusion,
        # R-C2: not defensible under AU-3(b) until Doc-0 G-8 closes.
        au_3b_defensible=False,
    )
