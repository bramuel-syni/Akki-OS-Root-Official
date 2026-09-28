"""W-CENSUS-CANON-ALIGN · CP-C6b · ActivationList — census activates
matrix rows.

Canon anchor (verbatim, canon/text/Akki_Canon_4_Operating_Engines.txt:291):
    "The census activates matrix rows. A class with no material in the estate stays dormant — registered, instrumented on paper, zero build. A class the census actually observes activates: its checkpoints join the estate's first-measurement sample and its thresholds bind before that class enters production mining."

`ActivationList` records the two-way partition of the class matrix into
activated (observed by the census walk) and dormant (no observation → no
build). `compute_activation_list` derives the partition from an
observation set plus the matrix; the result is deterministic (both tuples
sorted) so downstream readers see a stable identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass(frozen=True)
class ActivationList:
    """Two-tuple partition of the class matrix per Canon-4 §Class-activation.

    Carriers:
      * ``activated`` — canonically-sorted tuple of class names the census
        actually observed (their checkpoints join the estate's first-
        measurement sample and their thresholds bind before that class
        enters production mining).
      * ``dormant`` — canonically-sorted tuple of class names with no
        observation in this census run (registered, instrumented on paper,
        zero build).

    The two tuples are disjoint and their union equals the input matrix.
    """

    activated: Tuple[str, ...]
    dormant: Tuple[str, ...]


def compute_activation_list(
    *,
    observed: Iterable[str],
    matrix_classes: Iterable[str],
) -> ActivationList:
    """Derive an `ActivationList` from an observation set and a class
    matrix. Deterministic ordering (sorted). Membership check ignores
    ordering + duplicates in the inputs; only the sets matter.
    """
    observed_set = set(observed)
    matrix_set = set(matrix_classes)
    activated_set = observed_set & matrix_set
    dormant_set = matrix_set - observed_set
    return ActivationList(
        activated=tuple(sorted(activated_set)),
        dormant=tuple(sorted(dormant_set)),
    )
