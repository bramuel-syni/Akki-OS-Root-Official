"""services/solva_v2/engines/tension_detector.py — CP-S8 skeleton.

Canon anchor (Canon-4 §21): tension surfacing is a reasoning primitive
Solva runs over the candidate set to expose disagreements the load-
bearing set must resolve.  Case-agnostic form.

Lifted from
Akki-Executive-Core/backend/services/solva_v2/engines/tension_detector.py
STRUCTURAL pattern; all executive-domain tokens stripped.
"""
from __future__ import annotations

from typing import Iterable, Tuple

from contracts.solva_reasoning import UnitRef


def run(candidates: Iterable[UnitRef]) -> Tuple[Tuple[UnitRef, UnitRef], ...]:
    """Case-agnostic tension pass: enumerates ordered pairs of
    candidates that could be in tension.  Thin-kernel returns the
    trivial empty tuple for zero-or-one candidates; for two-or-more
    candidates returns adjacent pairs so the pipeline shape is
    exercisable.  Future wave binds to real tension-scoring."""
    ordered = tuple(candidates)
    if len(ordered) < 2:
        return ()
    return tuple((ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1))
