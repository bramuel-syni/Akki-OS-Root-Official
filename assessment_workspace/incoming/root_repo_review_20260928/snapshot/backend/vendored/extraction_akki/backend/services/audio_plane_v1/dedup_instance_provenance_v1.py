"""CP-AIP-2-DEDUP-CONDITION-MAP · AIP v1.0 §4.5 dedup instance-condition-map provenance carriers.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-2-DEDUP-CONDITION-MAP and nothing else.

Spec anchor (AIP v1.0):
- §4.5 Deduplication as augmentation - instance condition map = set of
  channel/time/condition variants under which identical content occurred;
  one canonical extraction stored; variant set enters training curricula
  as designated robustness stratum at ZERO ACQUISITION COST.
- §4.6 (b) Acceptance criterion - a deduplicated item without its
  instance condition map fails the ingestion invariant test.
- §1.2 Modality extension - compose sealed InstanceConditionMap +
  InstanceConditionVariant + IngestionSegmentProvenance_v1; do not
  redeclare.
- §1.5 Unrepresentable, not policed - required carriers refuse at
  construction time.

Sealed carriers composed by this module (UNCHANGED per SO §3.8):
- backend/services/audio_plane_v1/instance_condition_map.py (CP-M6-2-1 · §4.5 schema + constructor + gate helper)
- backend/services/audio_plane_v1/ingestion_provenance_v1.py (CP-AIP-1 · sealed this-session)

Design:
- RobustnessStratumTag_v1 carries the §4.5 verbatim provenance
  ("designated robustness stratum at zero acquisition cost").
- DedupInstanceProvenance_v1 wraps a CP-AIP-1 IngestionSegmentProvenance
  and attaches the sealed InstanceConditionMap plus §4.5 role + stratum
  tag. `instance_condition_map` field name matches sealed
  `dedup_item_has_instance_condition_map(item)` gate helper's
  attribute lookup (composition contract).
"""
from __future__ import annotations

import dataclasses
from typing import Literal

from backend.services.audio_plane_v1.instance_condition_map import (
    InstanceConditionMap,
)
from backend.services.audio_plane_v1.ingestion_provenance_v1 import (
    IngestionSegmentProvenance_v1,
)


# =============================================================================
# Refusal class
# =============================================================================


class DedupInstanceProvenanceIncomplete(Exception):
    """§4.5 refusal · a DedupInstanceProvenance is unrepresentable if any
    required carrier is missing (base_provenance None, instance_condition_
    map None, robustness_stratum missing zero_acquisition_cost=True, or
    dedup_role invalid).
    """


# =============================================================================
# §4.5 RobustnessStratumTag_v1 · zero-acquisition-cost provenance
# =============================================================================


_DEDUP_ROLE = Literal["canonical", "variant"]


@dataclasses.dataclass(frozen=True)
class RobustnessStratumTag_v1:
    """§4.5 verbatim: 'the variant set enters training curricula as a
    designated robustness stratum at zero acquisition cost.'

    Frozen (facts-not-metadata · §4.2 pattern). Two carriers:
      - stratum_name (str): opaque caller-defined name of the stratum
        (e.g. 'dedup_variant_channel_time_condition').
      - zero_acquisition_cost (bool): §4.5 verbatim provenance flag.
        REQUIRED True for §4.5 conformance; refused if False at
        __post_init__ (§1.5 unrepresentable-not-policed).
    """
    stratum_name: str
    zero_acquisition_cost: bool

    def __post_init__(self) -> None:
        if self.zero_acquisition_cost is not True:
            raise DedupInstanceProvenanceIncomplete(
                "RobustnessStratumTag_v1 refuses zero_acquisition_cost="
                f"{self.zero_acquisition_cost!r} - §4.5 verbatim requires "
                "'zero acquisition cost' as True. Structural refusal per "
                "§1.5 unrepresentable-not-policed."
            )


# =============================================================================
# §4.5 DedupInstanceProvenance_v1 · wraps CP-AIP-1 base + sealed map
# =============================================================================


@dataclasses.dataclass(frozen=True)
class DedupInstanceProvenance_v1:
    """§4.5 dedup instance-condition-map provenance carrier.

    Composes (§1.2 modality-extension):
      - CP-AIP-1 IngestionSegmentProvenance_v1 via `base_provenance` field.
      - CP-M6-2-1 InstanceConditionMap via `instance_condition_map` field
        (attribute name matches sealed `dedup_item_has_instance_condition_
        map(item)` helper's lookup key).

    §4.5 verbatim carriers:
      - `dedup_role` Literal["canonical", "variant"]: encodes §4.5 verbatim
        "One canonical extraction is stored; the variant set enters
        training curricula..." distinction structurally.
      - `robustness_stratum` RobustnessStratumTag_v1: §4.5 provenance
        with zero_acquisition_cost=True.

    §4.6 (b) verbatim: 'A deduplicated item without its instance
    condition map fails the ingestion invariant test.' The
    `instance_condition_map` field being typed non-Optional makes the
    missing-map state unrepresentable-by-construction per §1.5. The
    additional runtime gate lives in `dedup_capture_v1.py` and re-checks
    via sealed `dedup_item_has_instance_condition_map` helper.
    """
    base_provenance: IngestionSegmentProvenance_v1
    instance_condition_map: InstanceConditionMap
    dedup_role: Literal["canonical", "variant"]
    robustness_stratum: RobustnessStratumTag_v1

    def __post_init__(self) -> None:
        # §4.5 defensive: base_provenance must be a genuine sealed shape.
        if not isinstance(self.base_provenance, IngestionSegmentProvenance_v1):
            raise DedupInstanceProvenanceIncomplete(
                "DedupInstanceProvenance_v1 refuses base_provenance of "
                f"type {type(self.base_provenance).__name__} - §1.2 "
                "composition discipline requires the sealed CP-AIP-1 "
                "IngestionSegmentProvenance_v1."
            )
        # §4.6 (b) defensive: instance_condition_map must be the sealed shape.
        if not isinstance(self.instance_condition_map, InstanceConditionMap):
            raise DedupInstanceProvenanceIncomplete(
                "DedupInstanceProvenance_v1 refuses instance_condition_map "
                f"of type {type(self.instance_condition_map).__name__} - "
                "§4.6 (b) requires the sealed CP-M6-2-1 InstanceConditionMap."
            )
        # §4.5 dedup_role guard - Python does not enforce Literal at runtime.
        if self.dedup_role not in ("canonical", "variant"):
            raise DedupInstanceProvenanceIncomplete(
                f"DedupInstanceProvenance_v1 refuses dedup_role="
                f"{self.dedup_role!r} - §4.5 requires \"canonical\" or "
                "\"variant\" literal."
            )


__all__ = [
    "DedupInstanceProvenanceIncomplete",
    "RobustnessStratumTag_v1",
    "DedupInstanceProvenance_v1",
]
