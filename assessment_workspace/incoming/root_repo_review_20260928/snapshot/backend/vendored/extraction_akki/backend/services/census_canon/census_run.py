"""W-CENSUS-CANON-ALIGN · CP-C3 · CensusRun + CensusRunId deterministic gen.

Canon anchors (verbatim quotes carried by this docstring per the
Verbatim-canon standing rule · DECISIONS.md 2026-09-15T~01:40Z):

Canon-4 §4.1 (canon/text/Akki_Canon_4_Operating_Engines.txt:30):
    "Every figure carries its method. Any measurement a surface displays resolves to the census run that produced it, its date, the population measured, and whether the measurement was full or sampled — a sampled measurement is never presented as a full-population one."

Master Requirements Registry Doc-9 B5.3
(canon/drops/20260910/extracted/text/Master_Requirements_Registry.md:147):
    "Every figure resolves to its method"

The census run is the addressable unit that a Measurement's `census_run_id`
(CP-C2) resolves to. The run itself carries a `run_date` (P30 verbatim), a
run-level `population` (count of sources visited by the walk), and a
run-level `full_vs_sampled` — the walk itself is either FULL (an exhaustive
walk of the estate at run time) or SAMPLED (a proper subset of sources
visited under a stated sampling policy).

`generate_census_run_id(...)` is the deterministic method that produces a
`CensusRunId` from a pinned input tuple (platform_version + job manifest
fingerprint + run_started_at). Same inputs -> same run_id; changing any
input shifts the run_id -> no silent aliasing between runs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

# Re-export the CP-C2 shape so callers only need to import from one module
# when they hold both a CensusRun and its Measurements.
from contracts.canon_census_measurement import (
    FullOrSampled,
    SampledPopulationInvalid,
)


# CensusRunId is a canonical str token produced by `generate_census_run_id`.
# Kept as a plain `str` alias (not a `NewType`) so downstream code that
# consumes/emits it as a plain string does not need a cast; the constructor
# is the type discipline.
CensusRunId = str


@dataclass(frozen=True)
class CensusRun:
    """A census run record — the addressable unit referenced by every
    `Measurement.census_run_id` (CP-C2).

    Four carriers per Canon-4 §4.1 P30 verbatim:
      * ``run_id``           — the ``CensusRunId`` a `Measurement` references.
      * ``run_date``         — the date of the run (ISO 8601 string).
      * ``population``       — run-level population count (sources visited).
                               For FULL: total sources visited in the walk.
                               For SAMPLED: sample size (must be > 0).
      * ``full_vs_sampled``  — `FullOrSampled` enum (FULL or SAMPLED).

    Construction of a SAMPLED run with population <= 0 is refused via
    ``SampledPopulationInvalid`` (Canon-4 §4.1 P30 verbatim: "a sampled
    measurement is never presented as a full-population one" — the clause
    fires at the run level too: a SAMPLED walk without a positive sample
    size is not a valid census run).
    """

    run_id: CensusRunId
    run_date: str
    population: int
    full_vs_sampled: FullOrSampled

    def __post_init__(self) -> None:
        if self.full_vs_sampled is FullOrSampled.SAMPLED and self.population <= 0:
            raise SampledPopulationInvalid(
                f"SAMPLED census run requires positive sample size · "
                f"got population={self.population!r} · Canon-4 §4.1 P30 · "
                f"'a sampled measurement is never presented as a "
                f"full-population one'"
            )


def generate_census_run_id(
    *,
    platform_version: str,
    job_manifest_fingerprint: str,
    run_started_at: str,
) -> CensusRunId:
    """Deterministic run-id generator.

    Canonicalises the three inputs into a stable JSON form and hashes with
    sha256, returning the full 64-char hex digest prefixed with ``cr_``.
    Same inputs -> byte-identical output; changing any input shifts the
    output -> no silent aliasing.

    Args:
      platform_version: platform version string (e.g. "platform-v1.0.0").
      job_manifest_fingerprint: fingerprint of the job manifest that mounts
        this walk onto the platform (S5 reframe · CP-C5 landing).
      run_started_at: ISO 8601 UTC timestamp for the run's start
        (e.g. "2026-09-15T02:35:00Z").

    Returns:
      A ``CensusRunId`` of the shape ``cr_<64-hex>``.
    """
    payload = {
        "platform_version": platform_version,
        "job_manifest_fingerprint": job_manifest_fingerprint,
        "run_started_at": run_started_at,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"cr_{digest}"
