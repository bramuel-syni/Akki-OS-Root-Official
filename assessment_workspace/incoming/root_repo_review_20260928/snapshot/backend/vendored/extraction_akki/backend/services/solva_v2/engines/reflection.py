"""services/solva_v2/engines/reflection.py — CP-S8 skeleton.

Canon anchor (Canon-4 §21): reflection produces the load-bearing set —
the units the conclusion actually rides on.  Case-agnostic form.

HALT (DPO-S2, declared in the grounding brief):
    The donor
    (Akki-Executive-Core/backend/services/solva_v2/engines/reflection.py)
    hard-codes three executive-domain LOCKED_QUESTIONS about
    'diagnosis'.  Their case-agnostic form is not a token-strip; it is
    a re-authoring of the reflection primitive's shape, and owner
    ruling has NOT been given on what the case-agnostic reflection
    question set should be.  This skeleton HALTS on run(): the caller
    must supply an explicit ReflectionRubric in a subsequent wave that
    owner rules.
"""
from __future__ import annotations

from typing import Iterable, Tuple

from contracts.solva_reasoning import UnitRef


def run(candidate_pairs: Iterable[Tuple[UnitRef, UnitRef]]) -> Tuple[UnitRef, ...]:
    """HALTED skeleton — case-agnostic reflection question set is not
    owner-ruled.

    The primitive shape is preserved (input: tension pairs; output:
    load-bearing set).  The IMPLEMENTATION raises NotImplementedError
    with a HALT message so a calling wave cannot silently substitute
    a domain-shaped reflection contract."""
    raise NotImplementedError(
        "HALT (DPO-S2, W-SOLVA-V2-LIFT grounding brief §C): "
        "case-agnostic reflection question set not owner-ruled.  "
        "The donor's LOCKED_QUESTIONS are executive-domain and were "
        "not lifted.  A subsequent wave binds this reflection primitive "
        "to an owner-ruled case-agnostic reflection contract."
    )
