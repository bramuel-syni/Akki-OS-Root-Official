"""services/solva_v2/assertion_boundary.py — CP-S2 (LANDS FIRST).

Canon-4 §23.1 verbatim: 'The class computation takes the load-bearing
units and nothing else — no confidence, no reasoning strength, no
evidence weight.  The signature is the guard, and a signature
assertion in the test suite is what keeps it one.'

This file deliberately does NOT import from reasoning_faculty
(Doc-0 §BR-2.1 two-faculty seam).  The boundary is blind to how units
were chosen; it takes the LoadBearingSet and returns a class.

Owner directive (this session): 'the parameterless assertion-boundary
signature must be built and asserted BEFORE the load-bearing reasoning
function — this is the seam that proves Solva cannot fabricate.'
"""
from __future__ import annotations

from contracts.solva_reasoning import AssertionClass, LoadBearingSet


def compute_class(load_bearing: LoadBearingSet) -> AssertionClass:
    """Canon-4 §23.1 parameterless class-computation.

    Exactly one parameter — the load-bearing set.  No confidence, no
    strength, no weight, no evidence, no score.  Return is the
    AssertionClass floor.

    Thin-kernel implementation: with zero units the class is
    non_factual (Canon-4 §4.1 unmeasured is a first-class value);
    otherwise the floor is utterance (Canon-4 §23 'the weakest
    load-bearing unit sets the ceiling for the whole').  A future
    wave binds this to real unit-class lookup through opaque handles
    per Canon-4 §23 'the floor and the class verdict are read-only;
    Solva reads them, it never sets or relaxes them.'
    """
    if not load_bearing.units:
        return AssertionClass.NON_FACTUAL
    return AssertionClass.UTTERANCE
