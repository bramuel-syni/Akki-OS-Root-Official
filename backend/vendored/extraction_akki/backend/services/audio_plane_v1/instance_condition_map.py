"""M6 · Audio-Plane v1.0 · CP-M6-2-1 · Instance condition map schema.

Contract-extension of the occurrence index per §4.5 P071 verbatim:
"for each deduplicated item, the instance condition map — the set of
channel/time/condition variants under which identical content occurred
— is retained."

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.5 P071 (V50):
      "The occurrence index already identifies repeated content. Its output contract is extended: for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored; the variant set enters training curricula as a designated robustness stratum at zero acquisition cost. No new detection work; this is a change to what dedup keeps."

- Audio-Plane §4.6 P074 (V52 · invariant gate):
      "A deduplicated item without its instance condition map fails the ingestion invariant test."

- Audio-Plane §15 P230 (build sequence · verbatim):
      "Dedup instance condition map (§4.5) — Contract change to existing machinery; near-zero new detection work."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes cross into these carrier shapes — variants and maps
    reference their sources via opaque caller-scoped handles.
  - Case-agnostic; no executive-domain tokens.

Pattern departure from sub-wave 1:
  - CP-M6-1-* landed pluggable-seam mechanisms with `Unratified*Backend`
    placeholders per D10-family discipline.
  - CP-M6-2-1 lands a pure schema + constructor (no backend, no seam).
    §4.5 P071 says "No new detection work" — there is no detection to
    plug.  The map's population is caller-driven from already-collected
    §4.1..§4.4 outputs.  CP-M6-2-2 wires the dedup path to attach an
    `InstanceConditionMap` per dedup item.

Contract:

    construct_instance_condition_map(
        *,
        canonical_extraction_ref: str,
        occurrence_index_ref: str,
        variants: Sequence[InstanceConditionVariant],
    ) -> InstanceConditionMap

    dedup_item_has_instance_condition_map(item) -> bool
        §4.6 P074 gate helper · fail-closed on missing/None/wrong-type.

Refusals:
    VariantsEmptyError   on empty variants (§4.5 P071 verbatim requires
                          a non-empty variant set — the dedup item exists
                          BECAUSE identical content occurred at least once).
    VariantInvalidError  on non-`InstanceConditionVariant` element.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, Tuple


class VariantsEmptyError(Exception):
    """Raised when constructing an `InstanceConditionMap` with empty
    `variants`. §4.5 P071 verbatim requires the variant set exist
    ("the set of channel/time/condition variants under which identical
    content occurred") — an empty set is not a map."""


class VariantInvalidError(Exception):
    """Raised when a `variants` element is not an
    `InstanceConditionVariant` instance."""


@dataclass(frozen=True)
class InstanceConditionVariant:
    """A single per-instance variant record per Audio-Plane §4.5 P071
    verbatim "channel/time/condition variants".

    Three carriers:
      - `segment_ref` — the source segment where this variant occurred.
      - `channel_time_ref` — an opaque caller-scoped identifier for the
        (channel × time) coordinate at which this variant occurred.
      - `condition_profile_ref` — an opaque caller-scoped handle to the
        §4.3 `ChannelConditionProfile` record for this variant.

    Pull-seam discipline: no audio-byte carrier names on this shape.
    """

    segment_ref: str
    channel_time_ref: str
    condition_profile_ref: str


@dataclass(frozen=True)
class InstanceConditionMap:
    """The instance condition map attached to a deduplicated item per
    Audio-Plane §4.5 P071 verbatim.

    Three carriers:
      - `canonical_extraction_ref` — reference to the one canonical
        extraction that is stored ("One canonical extraction is stored").
      - `occurrence_index_ref` — reference to the dedup / occurrence
        index item this map is attached to.
      - `variants` — the immutable tuple of `InstanceConditionVariant`
        instances comprising "the set of channel/time/condition variants
        under which identical content occurred".

    Pull-seam discipline: no audio-byte carrier names on this shape.
    """

    canonical_extraction_ref: str
    occurrence_index_ref: str
    variants: Tuple[InstanceConditionVariant, ...]


def _validate_variants(
    variants: Sequence[InstanceConditionVariant],
) -> Tuple[InstanceConditionVariant, ...]:
    if not variants:
        raise VariantsEmptyError(
            "instance condition map: variants must be non-empty; "
            "got 0 variants (§4.5 P071 verbatim: 'the set of "
            "channel/time/condition variants under which identical "
            "content occurred')"
        )
    coerced = tuple(variants)
    for i, v in enumerate(coerced):
        if not isinstance(v, InstanceConditionVariant):
            raise VariantInvalidError(
                f"instance condition map: variants[{i}] must be an "
                f"InstanceConditionVariant; got {type(v).__name__}"
            )
    return coerced


def construct_instance_condition_map(
    *,
    canonical_extraction_ref: str,
    occurrence_index_ref: str,
    variants: Sequence[InstanceConditionVariant],
) -> InstanceConditionMap:
    """Construct an `InstanceConditionMap` per §4.5 P071.

    Coerces `variants` to a tuple so the frozen dataclass is genuinely
    immutable; refuses empty/invalid variants per module docstring.
    """
    coerced = _validate_variants(variants)
    return InstanceConditionMap(
        canonical_extraction_ref=canonical_extraction_ref,
        occurrence_index_ref=occurrence_index_ref,
        variants=coerced,
    )


def dedup_item_has_instance_condition_map(item: Any) -> bool:
    """§4.6 P074 verbatim gate helper: "A deduplicated item without its
    instance condition map fails the ingestion invariant test."

    Returns True iff `item.instance_condition_map` is a non-None
    `InstanceConditionMap` with a non-empty `variants` tuple.  Any
    other shape (missing attribute, None, wrong type, empty variants)
    returns False — fail-closed by design so §4.6 P074 gates dedup
    items that lack a map for any reason.
    """
    m = getattr(item, "instance_condition_map", None)
    if m is None:
        return False
    if not isinstance(m, InstanceConditionMap):
        return False
    if not m.variants:
        return False
    return True
