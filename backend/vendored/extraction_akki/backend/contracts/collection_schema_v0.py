"""CP-AIP-6-OBJECTIVE-WIZARD · CollectionSchema_v0 contract · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-6-OBJECTIVE-WIZARD and nothing else.

Spec anchor: AIP v1.0 §9 Collection Schema.

§9.1 verbatim: 'The declared data dictionary of a commission: what is
extracted from the sound, for what purpose, at what quality bar. It is
the admission standard of the audio estate, per objective (§1.1). It
has two tiers.'

§9.2 baseline tier verbatim v1.0 contents:
    'language identification, code-switch points, condition profile,
    dedup instance condition map, synthesis-relevant group-level
    acoustics (§4).'

§9.3 objective tier verbatim: 'Declared per commission by the Objective
Wizard. Collected against material already in governed scope, priced
before collection starts, recorded in the commission's registry
namespace.'

§9.2 last sentence verbatim: 'Changes to the baseline are seam-governed
— ceremony, countersignature, waiting period — because silently
narrowing the baseline is how an estate quietly becomes
unre-readable.' Encoded as a frozen constant · additive change requires
ceremony.

Additive-only per SO §3.8.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Tuple


# §9.2 verbatim v1.0 baseline tier contents · PENDING-OWNER-CONFIRMATION
# per owner working default 2026-02-23T04:15Z.  Frozen constant · any
# change is ceremony-governed per §9.2 last sentence.
BASELINE_TIER_V1_0_CONTENTS: Final[Tuple[str, ...]] = (
    "language_identification",
    "code_switch_points",
    "condition_profile",
    "dedup_instance_condition_map",
    "synthesis_relevant_group_level_acoustics",
)


# §6.2 custody-violation forbidden tokens (mirrors CP-AIP-3 write-
# boundary discipline).  A CollectionSchema column whose name carries
# any of these tokens is refused at compile time.
CUSTODY_VIOLATING_TOKENS: Final[Tuple[str, ...]] = (
    "voiceprint",
    "per_utterance_embedding",
    "speaker_id",
    "speaker_embedding",
    "raw_audio",
    "utterance_bytes",
    "audio_bytes",
    "exemplar",
)


@dataclass(frozen=True)
class CollectionSchema_v0:
    """§9 verbatim two-tier Collection Schema.

    Fields:
      - baseline_tier · §9.2 verbatim - standing, objective-independent
        columns.  Membership criterion verbatim: cheap to collect now,
        unaffordable to collect later.
      - objective_tier · §9.3 verbatim - declared per commission.
    """

    baseline_tier: Tuple[str, ...]
    objective_tier: Tuple[str, ...]

    def all_columns(self) -> Tuple[str, ...]:
        """All columns in this schema · baseline + objective."""
        return self.baseline_tier + self.objective_tier
