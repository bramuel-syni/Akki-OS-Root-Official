"""services/solva_v2/engines/candidate_generation.py — CP-S8 skeleton.

Canon anchor (Canon-4 §21): candidate weighing is a reasoning primitive
Solva runs to surface options over which the load-bearing set will be
chosen.  Case-agnostic form.

This skeleton exposes run() and does NOT smuggle executive-domain
content.  The case-agnostic implementation binds to a real candidate
source in a future wave; here it accepts a set of candidate UnitRefs
and returns them as-is (identity), so the surrounding pipeline can be
tested end-to-end without domain assumptions.

Lifted from the STRUCTURAL pattern in
Akki-Executive-Core/backend/services/solva_v2/engines/candidate_generation.py;
all executive-domain tokens stripped.
"""
from __future__ import annotations

from typing import Iterable, Tuple

from contracts.solva_reasoning import UnitRef


def run(candidates: Iterable[UnitRef]) -> Tuple[UnitRef, ...]:
    """Case-agnostic candidate pass: emits the candidate ref set
    unchanged.  A future wave binds this to a real candidate source
    (governed by the matrix)."""
    return tuple(candidates)
