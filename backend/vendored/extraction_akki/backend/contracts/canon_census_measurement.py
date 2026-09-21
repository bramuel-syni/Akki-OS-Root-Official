"""W-CENSUS-CANON-ALIGN · CP-C2 · Unmeasured + Measurement contracts.

Canon anchors (verbatim quotes carried in this docstring per the
Verbatim-canon standing rule · DECISIONS.md 2026-09-15T~01:40Z):

Canon-4 §4.1 (canon/text/Akki_Canon_4_Operating_Engines.txt:29):
    "Unmeasured is a first-class value. A dimension not measured is recorded
     as unmeasured, never as zero, absent, or clean. A blank that reads as
     clean makes the whole instrument dishonest."

Canon-4 §4.1 (:30):
    "Every figure carries its method. Any measurement a surface displays
     resolves to the census run that produced it, its date, the population
     measured, and whether the measurement was full or sampled — a sampled
     measurement is never presented as a full-population one."

Master Requirements Registry Doc-9:
    B5.2 (:146): "Unmeasured is recorded as unmeasured"
    B5.3 (:147): "Every figure resolves to its method"
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FullOrSampled(str, Enum):
    """Closed 2-value enum for §4.1 P30 'full or sampled' carrier."""

    FULL = "FULL"
    SAMPLED = "SAMPLED"


class SampledPopulationInvalid(Exception):
    """Raised when a SAMPLED Measurement is constructed with population <= 0.

    Canon-4 §4.1 P30 verbatim: "a sampled measurement is never presented as
    a full-population one." Sample size (the `population` field on a SAMPLED
    measurement) must be a positive integer or the construction is refused.
    """


@dataclass(frozen=True)
class Unmeasured:
    """First-class sentinel value for §4.1 P29 'Unmeasured is a first-class
    value.'

    A dimension not measured is recorded as ``Unmeasured(reason=...)``, never
    as zero / None / empty. Carries a ``reason`` string so a downstream
    reader can distinguish "no method exists at this census run" from
    "connector unreachable" from "sensitivity classification refused
    disclosure at this depth".
    """

    reason: str


@dataclass(frozen=True)
class Measurement:
    """A single measured figure, carrying its method per §4.1 P30.

    Six carriers (§4.1 P30 verbatim):
      * ``value`` — the measured value.
      * ``method`` — string identifying the measurement method
        (Canon-4 §4.1 P30: 'Every figure carries its method').
      * ``population`` — the population measured. For FULL: full-population
        count. For SAMPLED: sample size (must be > 0).
      * ``full_vs_sampled`` — FullOrSampled enum.
      * ``census_run_id`` — the run that produced this figure.
      * ``run_date`` — the date of that run (ISO 8601 string).

    Construction of a SAMPLED measurement with population <= 0 is refused
    via ``SampledPopulationInvalid`` (Canon-4 §4.1 P30 verbatim: 'a sampled
    measurement is never presented as a full-population one').
    """

    value: Any
    method: str
    population: int
    full_vs_sampled: FullOrSampled
    census_run_id: str
    run_date: str

    def __post_init__(self) -> None:
        if self.full_vs_sampled is FullOrSampled.SAMPLED and self.population <= 0:
            raise SampledPopulationInvalid(
                f"SAMPLED measurement requires positive sample size · "
                f"got population={self.population!r} · Canon-4 §4.1 P30 · "
                f"'a sampled measurement is never presented as a "
                f"full-population one'"
            )
