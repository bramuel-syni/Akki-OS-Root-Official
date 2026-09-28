"""M6 · Audio-Plane v1.0 · CP-M6-2-2 · Dedup path extension.

Wires the §4.5 P071 contract extension: dedup collapses items by text
(one canonical extraction is stored) while preserving the complete
set of channel/time/condition variants under which identical content
occurred.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §4.5 P071 (V50):
      "The occurrence index already identifies repeated content. Its output contract is extended: for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored; the variant set enters training curricula as a designated robustness stratum at zero acquisition cost. No new detection work; this is a change to what dedup keeps."

- Audio-Plane §4.6 P074 (V52 · invariant gate):
      "A deduplicated item without its instance condition map fails the ingestion invariant test."

- Audio-Plane §14 P216 (V133 · interface summary):
      "Occurrence index (ext.)  ⎢  dedup item → + instance condition map."

CP-M6-2-2 invariant (per M6 grounding brief §C):
  dedup collapse never drops a distinct condition; distinct conditions
  produce distinct variants in the map even when text-identical.

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Deterministic — same input yields same output.
  - Case-agnostic; no executive-domain tokens.

Contract:

    dedup_with_condition_awareness(
        *,
        items: Sequence[DedupInputItem],
    ) -> List[DedupItem]

    - Groups items by `text_ref` (one canonical extraction per text).
    - Preserves DISTINCT `InstanceConditionVariant` records within each
      text group as separate entries in the map's `variants` tuple.
    - Duplicates within a text group (identical variant) collapse to a
      single map entry.
    - Preserves insertion order for both `DedupItem`s and variants
      within each map — determinism through stable ordering.

Refusals:
    ItemsEmptyError    on empty items.
    ItemInvalidError   on non-`DedupInputItem` element.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from services.audio_plane_v1.instance_condition_map import (
    InstanceConditionMap,
    InstanceConditionVariant,
    construct_instance_condition_map,
)


class ItemsEmptyError(Exception):
    """Raised when `items` is empty."""


class ItemInvalidError(Exception):
    """Raised when a `items` element is not a `DedupInputItem`."""


@dataclass(frozen=True)
class DedupInputItem:
    """An input to the dedup path.

    Two carriers:
      - `text_ref` — the opaque text-content identifier used as the
        dedup key (equal `text_ref` values are candidates for
        collapse).
      - `variant` — the `InstanceConditionVariant` recording the
        (segment_ref, channel_time_ref, condition_profile_ref) of this
        specific occurrence.

    Pull-seam discipline: no audio-byte carrier names.
    """

    text_ref: str
    variant: InstanceConditionVariant


@dataclass(frozen=True)
class DedupItem:
    """A deduplicated output item per §14 P216 verbatim
    ("dedup item → + instance condition map").

    Two carriers:
      - `text_ref` — the dedup key.
      - `instance_condition_map` — the §4.5 P071 map attached to this
        dedup item, containing all distinct channel/time/condition
        variants under which the identical text_ref content occurred.
    """

    text_ref: str
    instance_condition_map: InstanceConditionMap


def _validate_items(
    items: Sequence[DedupInputItem],
) -> Tuple[DedupInputItem, ...]:
    if not items:
        raise ItemsEmptyError(
            "dedup path: items must be non-empty; got 0 items"
        )
    coerced = tuple(items)
    for i, it in enumerate(coerced):
        if not isinstance(it, DedupInputItem):
            raise ItemInvalidError(
                f"dedup path: items[{i}] must be a DedupInputItem; "
                f"got {type(it).__name__}"
            )
    return coerced


def dedup_with_condition_awareness(
    *,
    items: Sequence[DedupInputItem],
) -> List[DedupItem]:
    """Dedup items by `text_ref` while preserving distinct condition
    variants per §4.5 P071 verbatim.

    Per §4.5 P071:
      - one canonical extraction per distinct `text_ref` (single
        `DedupItem` per text_ref).
      - the variant set (distinct `InstanceConditionVariant` values) is
        retained in the map.

    CP-M6-2-2 invariant:
      - distinct conditions never dropped · text-identical items with
        different variants produce ONE DedupItem whose map carries all
        distinct variants.

    Deterministic: preserves first-seen ordering for both DedupItems
    and variants within each map.
    """
    validated = _validate_items(items)

    # Order-preserving grouping: text_ref → List[InstanceConditionVariant]
    grouped: Dict[str, List[InstanceConditionVariant]] = {}
    text_order: List[str] = []
    for it in validated:
        if it.text_ref not in grouped:
            grouped[it.text_ref] = []
            text_order.append(it.text_ref)
        # Preserve distinct variants only (dedup within-group by variant equality).
        if it.variant not in grouped[it.text_ref]:
            grouped[it.text_ref].append(it.variant)

    results: List[DedupItem] = []
    for text_ref in text_order:
        variants = tuple(grouped[text_ref])
        icm = construct_instance_condition_map(
            canonical_extraction_ref=f"canonical::{text_ref}",
            occurrence_index_ref=f"occurrence::{text_ref}",
            variants=variants,
        )
        results.append(DedupItem(text_ref=text_ref, instance_condition_map=icm))
    return results
