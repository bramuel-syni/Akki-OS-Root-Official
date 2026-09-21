"""W-CENSUS-CANON-ALIGN · CP-C6a · SourceStratumMeasurement — the eight
per-stratum output-field carriers Canon-4 §4.1 P28 names verbatim.

Canon anchor (verbatim, canon/text/Akki_Canon_4_Operating_Engines.txt:28):
    "Per source and per stratum: volume, media types, languages, era distribution, quality strata, the share already verified, the share carrying personal data, the share licensed for external use — and, explicitly, what has not been measured."

Each of the eight dimensions carries either a `Measurement` (CP-C2, a
figure with its method + population + full-vs-sampled + census_run_id +
run_date) or an `Unmeasured` (CP-C2, first-class sentinel per §4.1 P29
'A dimension not measured is recorded as unmeasured, never as zero,
absent, or clean.'). The union type makes 'what has not been measured'
explicit at the type level — a reader cannot mistake an unmeasured
dimension for a measured-zero.

Note on canon-name → field-name mapping (verbatim → snake-case, no
paraphrase, no reordering):
    volume                            → volume
    media types                       → media_types
    languages                         → languages
    era distribution                  → era_distribution
    quality strata                    → quality_strata
    the share already verified        → verified_share
    the share carrying personal data  → pii_share
    the share licensed for external use → licence_share
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from contracts.canon_census_measurement import Measurement, Unmeasured


# Union type for per-stratum dimensions — either a measured figure (with
# method, population, full-vs-sampled, run link) or the first-class
# unmeasured sentinel.
DimensionValue = Union[Measurement, Unmeasured]


@dataclass(frozen=True)
class SourceStratumMeasurement:
    """Eight per-stratum dimensions per Canon-4 §4.1 P28 verbatim ordering.

    Each dimension is a `Measurement | Unmeasured` (CP-C2 union). A stratum
    where nothing has been measured yet is a valid instance — all eight
    fields are `Unmeasured` with an explanatory reason. Partial strata
    (some measured, some not) are also valid; this is the first-run
    ordinary case per §4.1 P29 ('Unmeasured is a first-class value').
    """

    volume: DimensionValue
    media_types: DimensionValue
    languages: DimensionValue
    era_distribution: DimensionValue
    quality_strata: DimensionValue
    verified_share: DimensionValue
    pii_share: DimensionValue
    licence_share: DimensionValue
