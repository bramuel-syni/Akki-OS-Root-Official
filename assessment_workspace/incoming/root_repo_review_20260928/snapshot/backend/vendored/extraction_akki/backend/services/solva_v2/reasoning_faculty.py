"""services/solva_v2/reasoning_faculty.py — CP-S1 + CP-S3.

Canon-4 §22: 'Solva chooses the units; it does not choose what those
units imply.'  This faculty produces the LoadBearingSet.  It does NOT
import assertion_boundary.compute_class — Doc-0 §BR-2.1 seam.

Discipline (Doc-0 §BR-2.1): the two-faculty seam is enforced by import,
not coding convention.  A caller ABOVE both faculties combines the
LoadBearingSet from here with compute_class() from assertion_boundary.
Neither faculty imports the other.
"""
from __future__ import annotations

from typing import Iterable

from contracts.solva_reasoning import LoadBearingSet, UnitRef


def identify_load_bearing_units(
    candidate_units: Iterable[UnitRef],
) -> LoadBearingSet:
    """Canon-4 §22 load-bearing set builder.

    Returns UnitRef objects only — no class field, no class parameter.
    The reasoning side chooses WHICH units; the class is decided by
    the boundary (assertion_boundary.compute_class) once the caller
    ABOVE both faculties passes this set to it.
    """
    seen_ids: set[str] = set()
    ordered: list[UnitRef] = []
    for u in candidate_units:
        if u.unit_id in seen_ids:
            continue
        seen_ids.add(u.unit_id)
        ordered.append(u)
    return LoadBearingSet(units=tuple(ordered))
