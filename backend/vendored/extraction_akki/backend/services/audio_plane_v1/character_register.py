"""M6 · Audio-Plane v1.0 · CP-M6-3-1 · Character Register schema.

Frozen dataclass carriers for the Character Register per Audio-Plane
§5.1..§5.2 + §6.1..§6.2 verbatim.  Schema only — this CP does NOT land
the leakage-path invariant harness (CP-M6-3-2), the write-path
leakage-refusal boundary (CP-M6-3-3), or the §6.4 read-path scope
enforcement (CP-M6-3-4).  Those follow.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §5.1 P078 (V54):
      "A registry-modality store of learned, group-level audio characteristics, built from the character stream. Same doctrine as the fact registry: every entry carries provenance to source material and an occurrence count. It is Mtafiti's qualification-and-index doctrine applied to acoustic observations — an extension, not a sibling (§1.2)."

- Audio-Plane §5.2 P082..P085 (V55..V58 · four layers):
      P082 "Phonetic ⎢ Per-lexeme pronunciation variants, frequency, regional distribution."
      P083 "Prosodic ⎢ Intonation contours, stress, rate distributions, pause structure."
      P084 "Condition ⎢ Channel and environment profiles."
      P085 "Code-switch ⎢ Switch-point patterns, language pairs, context classes."

- Audio-Plane §6.1 P092 (V60 · prohibition):
      "Organic characteristics are anatomical — vocal tract length, formant structure, glottal source, fundamental frequency range. They cannot be acquired or shed; they are what speaker verification keys on; they are biometric. They are never registered."

- Audio-Plane §6.1 P093 (V61):
      "Learned characteristics are acquired from a speech community — phonological inventory, pronunciation variants, prosody, code-switching habits. They are group properties by construction. Only learned characteristics may be registered."

- Audio-Plane §6.2 P098 (V65 · condition 4):
      "Stored as description, not exemplar. Centroids, distributions, frequencies. Never stored audio; never per-utterance speaker embeddings. Embeddings used during clustering are destroyed after cluster assignment. Provenance points to material, not to speaker identity."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes / voiceprints / per-utterance embeddings in carriers.
  - Case-agnostic; no executive-domain tokens.

Contract:

    REGISTER_LAYER_VALUES = frozenset({
        "phonetic", "prosodic", "condition", "code_switch",
    })  # §5.2 P082..P085 verbatim four-set (Python-identifier form).

    construct_character_entry(*, attribute_name, layer, description,
        provenance_material_ref, occurrence_count, n_distinct_speakers,
        is_learned) -> CharacterEntry
      · Validates layer ∈ REGISTER_LAYER_VALUES (raises LayerInvalidError).
      · CP-M6-3-1 scope stops here: is_learned=False is NOT refused at
        construction — §6.1 P093 write-path refusal is CP-M6-3-3 scope.

    construct_character_register(*, entries) -> CharacterRegister
      · Coerces `entries` Sequence to immutable tuple.

Refusals:
    LayerInvalidError  on `layer` outside REGISTER_LAYER_VALUES.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Sequence, Tuple


REGISTER_LAYER_VALUES: FrozenSet[str] = frozenset({
    "phonetic",
    "prosodic",
    "condition",
    "code_switch",
})


class LayerInvalidError(Exception):
    """Raised when a `layer` value is outside `REGISTER_LAYER_VALUES`.

    §5.2 vocabulary discipline: the Character Register is layered per
    §5.2 P082..P085 four-set; entries outside this vocabulary are not
    representable in the schema."""


@dataclass(frozen=True)
class CharacterEntry:
    """A single character-register entry per §5.1 P078 + §6.2 P098
    verbatim contracts.

    Seven carriers:
      - `attribute_name` — what the entry describes.
      - `layer` — one of `REGISTER_LAYER_VALUES` (§5.2 P082..P085).
      - `description` — immutable tuple of floats (centroid / distribution
        / frequency summary vector per §6.2 P098 verbatim
        "Centroids, distributions, frequencies").
      - `provenance_material_ref` — §6.2 P098 verbatim: "Provenance
        points to material, not to speaker identity".
      - `occurrence_count` — §5.1 P078 verbatim: "every entry carries…
        an occurrence count".
      - `n_distinct_speakers` — §6.2 cond-2 P096 shared-attribute count.
      - `is_learned` — §6.1 P092/P093 classifier (organic characteristics
        excluded at write-path in CP-M6-3-3).

    Pull-seam discipline + §6.2 cond-4: no audio-byte / voiceprint /
    per-utterance-embedding / speaker-identity carriers.  Provenance
    points to material (governed by `provenance_material_ref`), never
    to speaker identity.
    """

    attribute_name: str
    layer: str
    description: Tuple[float, ...]
    provenance_material_ref: str
    occurrence_count: int
    n_distinct_speakers: int
    is_learned: bool


@dataclass(frozen=True)
class CharacterRegister:
    """The Character Register container per §5.1 P078.

    One carrier: `entries` — immutable tuple of `CharacterEntry`.
    """

    entries: Tuple[CharacterEntry, ...]


def _validate_layer(value: str) -> str:
    if value not in REGISTER_LAYER_VALUES:
        raise LayerInvalidError(
            f"character register: layer {value!r} outside §5.2 verbatim "
            f"vocabulary {sorted(REGISTER_LAYER_VALUES)!r}"
        )
    return value


def construct_character_entry(
    *,
    attribute_name: str,
    layer: str,
    description: Sequence[float],
    provenance_material_ref: str,
    occurrence_count: int,
    n_distinct_speakers: int,
    is_learned: bool,
) -> CharacterEntry:
    """Construct a `CharacterEntry` with layer-vocabulary validation.

    Coerces `description` to a tuple for frozen-dataclass immutability.
    Does NOT refuse `is_learned=False` — write-path refusal per §6.1
    P093 is CP-M6-3-3 scope.
    """
    _validate_layer(layer)
    return CharacterEntry(
        attribute_name=attribute_name,
        layer=layer,
        description=tuple(description),
        provenance_material_ref=provenance_material_ref,
        occurrence_count=occurrence_count,
        n_distinct_speakers=n_distinct_speakers,
        is_learned=is_learned,
    )


def construct_character_register(
    *,
    entries: Sequence[CharacterEntry],
) -> CharacterRegister:
    """Construct a `CharacterRegister`, coercing entries to a tuple.

    Does NOT run the four-leakage-path invariant harness (CP-M6-3-2) or
    write-path refusals (CP-M6-3-3) — schema-only this CP.
    """
    return CharacterRegister(entries=tuple(entries))
