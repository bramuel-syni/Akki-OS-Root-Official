"""M6 · Audio-Plane v1.0 · CP-M6-6-2 · Collection Schema type (baseline tier + objective tier).

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §9.1 P148 (V95 · definition):
      "The declared data dictionary of a commission: what is extracted from the sound, for what purpose, at what quality bar. It is the admission standard of the audio estate, per objective (§1.1). It has two tiers."

- Audio-Plane §9.2 P150 (V96 · baseline tier · v1.0 five-item content set · seam-governed changes):
      "Standing, objective-independent, collected at first ingestion for all admitted material. Membership criterion: cheap to collect now, unaffordable to collect later. Contents at v1.0: language identification, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group-level acoustics (§4). Changes to the baseline are seam-governed — ceremony, countersignature, waiting period — because silently narrowing the baseline is how an estate quietly becomes unre-readable."

- Audio-Plane §9.3 P152 (V97 · objective tier · priced-before-collection · candidates through §8.3 only):
      "Declared per commission by the Objective Wizard. Collected against material already in governed scope, priced before collection starts, recorded in the commission's registry namespace. Candidate columns enter through propose–qualify–graduate (§8.3) only."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Baseline-tier changes are seam-governed per §9.2 P150 — frozen
    5-tuple at module level, extension is owner-ratification-only.
  - Case-agnostic; no executive-domain tokens.
  - Synthetic-fixtures-only in tests.
  - §3.1 P038 tokens-not-waveforms discipline preserved.

Contract:

    BASELINE_TIER_CONTENTS_V1_0 — frozen 5-tuple in verbatim
      canonical order (§9.2 P150).

    SCHEMA_TIER_VALUES — frozenset {"baseline", "objective"}
      (§9.1 P148 verbatim two-tier).

    CollectionSchemaColumn — frozen 4-carrier: column_name · tier ·
      quality_bar · provenance_ref.  Refuses invalid tier at
      __post_init__.

    CollectionSchema — frozen 3-carrier: schema_id · commission_id ·
      columns.  Columns is an immutable tuple.

    construct_collection_schema(*, schema_id, commission_id, columns)
        -> CollectionSchema
      Refuses:
        - `BaselineTierIncompleteError` if any of 5 v1.0 baseline
          contents is missing.
        - `ObjectiveTierProvenanceMissingError` if any objective-tier
          column has None provenance_ref (§9.3 P152 verbatim).

Refusals:
    SchemaTierInvalidError · BaselineTierIncompleteError ·
    ObjectiveTierProvenanceMissingError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Iterable, Optional, Tuple


BASELINE_TIER_CONTENTS_V1_0: Tuple[str, ...] = (
    "language_identification",
    "code_switch_points",
    "condition_profile",
    "dedup_instance_condition_map",
    "synthesis_relevant_group_level_acoustics",
)
"""§9.2 P150 verbatim: 'Contents at v1.0: language identification,
code-switch points, condition profile, dedup instance condition map,
synthesis-relevant group-level acoustics (§4).'

Frozen 5-tuple in verbatim canonical order.  Changes to the baseline
are seam-governed per §9.2 P150: ceremony, countersignature, waiting
period — extension is an owner-ratification-only path (same discipline
as HUMAN_NAME_ATTRIBUTE_NAMES from CP-M6-5-3)."""


SCHEMA_TIER_VALUES: FrozenSet[str] = frozenset({"baseline", "objective"})
"""§9.1 P148 verbatim: 'It has two tiers.'  §9.2 baseline + §9.3
objective are the two members."""


class SchemaTierInvalidError(Exception):
    """Raised by `CollectionSchemaColumn.__post_init__` when the
    `tier` value is outside `SCHEMA_TIER_VALUES`.  §9.1 P148 verbatim
    two-tier discipline."""


class BaselineTierIncompleteError(Exception):
    """Raised by `construct_collection_schema` when the columns
    input does not include all 5 v1.0 baseline contents.

    §9.2 P150 verbatim: 'Contents at v1.0: language identification,
    code-switch points, condition profile, dedup instance condition
    map, synthesis-relevant group-level acoustics (§4).'  Missing
    any of the 5 refuses; extension requires owner-ratified ceremony
    (§9.2 P150 seam-governance)."""


class ObjectiveTierProvenanceMissingError(Exception):
    """Raised by `construct_collection_schema` when an objective-tier
    column has None `provenance_ref`.

    §9.3 P152 verbatim: 'Candidate columns enter through
    propose–qualify–graduate (§8.3) only.'  An objective-tier column
    without a provenance_ref back to the qualify/graduate ceremony
    violates this discipline."""


@dataclass(frozen=True)
class CollectionSchemaColumn:
    """A single column in a Collection Schema.

    Four carriers:
      - `column_name` — opaque column identifier.
      - `tier` — one of `SCHEMA_TIER_VALUES` (`baseline` or
        `objective`).  §9.1 P148 verbatim two-tier discipline.
      - `quality_bar` — §9.1 P148 verbatim: 'at what quality bar'.
      - `provenance_ref` — Optional[str].  For objective-tier columns,
        MUST be non-None (points to propose–qualify–graduate ceremony
        per §9.3 P152 verbatim).  For baseline-tier columns, MAY be
        None (baseline is standing, objective-independent per §9.2
        P150).
    """

    column_name: str
    tier: str
    quality_bar: str
    provenance_ref: Optional[str]

    def __post_init__(self) -> None:
        if self.tier not in SCHEMA_TIER_VALUES:
            raise SchemaTierInvalidError(
                f"CollectionSchemaColumn: tier {self.tier!r} outside "
                f"§9.1 P148 verbatim two-tier discipline "
                f"{sorted(SCHEMA_TIER_VALUES)!r}"
            )


@dataclass(frozen=True)
class CollectionSchema:
    """The Collection Schema for a commission.

    Three carriers:
      - `schema_id` — opaque schema identifier.
      - `commission_id` — the commission this schema binds to (§12.1
        P195 registry namespace).
      - `columns` — immutable tuple of `CollectionSchemaColumn`.
    """

    schema_id: str
    commission_id: str
    columns: Tuple[CollectionSchemaColumn, ...]


def construct_collection_schema(
    *,
    schema_id: str,
    commission_id: str,
    columns: Iterable[CollectionSchemaColumn],
) -> CollectionSchema:
    """Construct a `CollectionSchema` from a Sequence/Iterable of
    columns.

    Refuses:
      - `BaselineTierIncompleteError` if any of the 5 v1.0 baseline
        contents (`BASELINE_TIER_CONTENTS_V1_0`) is missing from the
        columns input.
      - `ObjectiveTierProvenanceMissingError` if any objective-tier
        column has None `provenance_ref`.

    Coerces Iterable input to Tuple for the frozen `CollectionSchema`
    carrier.
    """
    columns_tuple = tuple(columns)

    # §9.2 P150: all 5 v1.0 baseline contents MUST be present.
    baseline_names_present = {
        c.column_name for c in columns_tuple if c.tier == "baseline"
    }
    missing_baseline = [
        name for name in BASELINE_TIER_CONTENTS_V1_0
        if name not in baseline_names_present
    ]
    if missing_baseline:
        raise BaselineTierIncompleteError(
            f"construct_collection_schema: baseline tier is "
            f"incomplete — missing v1.0 contents {missing_baseline!r}; "
            f"§9.2 P150 verbatim: 'Contents at v1.0: language "
            f"identification, code-switch points, condition profile, "
            f"dedup instance condition map, synthesis-relevant "
            f"group-level acoustics (§4)'.  Extension requires "
            f"owner-ratified ceremony per §9.2 P150 seam-governance."
        )

    # §9.3 P152: objective-tier columns MUST carry provenance_ref.
    for c in columns_tuple:
        if c.tier == "objective" and c.provenance_ref is None:
            raise ObjectiveTierProvenanceMissingError(
                f"construct_collection_schema: objective-tier column "
                f"{c.column_name!r} has no provenance_ref; §9.3 P152 "
                f"verbatim: 'Candidate columns enter through "
                f"propose\u2013qualify\u2013graduate (\u00a78.3) only.'  A "
                f"provenance_ref back to the qualify/graduate "
                f"ceremony is mandatory."
            )

    return CollectionSchema(
        schema_id=schema_id,
        commission_id=commission_id,
        columns=columns_tuple,
    )
