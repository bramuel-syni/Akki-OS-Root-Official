"""M6 · Audio-Plane v1.0 · CP-M6-5-1 · Unsupervised clustering algorithm registration.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §5.3 P089 (V59 · clustering clause):
      "Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."

- M6 Sub-wave 5 grounding brief §C · CP-M6-5-1 (verbatim):
      "CP-M6-5-1 · Unsupervised clustering algorithm registration (§5.3 clause 1). New behaviour: register a pluggable clustering algorithm seam that operates over CharacterRegister.entries (from CP-M6-3-1) and emits CandidateStratum records."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes / voiceprints / per-utterance embeddings cross the seam.
  - §3.1 P038 tokens-not-waveforms discipline preserved.
  - §5.3 clause 2 discipline preserved: no cluster carrier carries a
    human-readable name.
  - Case-agnostic; no executive-domain tokens.
  - Synthetic fixtures only in tests.

Contract:

    CandidateStratum — frozen 3-carrier dataclass:
      stratum_id · member_attribute_names · backend_name.
      §5.3 clause 2: no `human_name` / `label` / `display_name` /
      `speaker_name` carrier.

    ClusteringBackend — Protocol · `.name` + `.cluster(entries) ->
      Tuple[CandidateStratum, ...]`.

    UnratifiedInferredClusteringBackend — placeholder refuses live
      invocation with `[INFERRED-pending-ratification]` marker per D10
      pluggable-seam discipline.

    cluster_character_register(*, character_register, backend) ->
      Tuple[CandidateStratum, ...]
      · Refuses `CharacterRegisterEmptyError` on empty register.
      · Delegates to `backend.cluster(entries=...)` and returns its
        verbatim output.

Refusals:
    CharacterRegisterEmptyError
    ClusteringBackendUnratifiedError
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Tuple

from services.audio_plane_v1.character_register import CharacterRegister


class CharacterRegisterEmptyError(Exception):
    """Raised when `cluster_character_register` receives a
    `CharacterRegister` with zero entries.

    §5.3 clause 1 verbatim: clustering runs OVER the character
    stream — an empty stream means no clustering to do."""


class ClusteringBackendUnratifiedError(Exception):
    """Raised by an unratified clustering backend when its `.cluster`
    method is invoked live.  D10 pluggable-seam discipline preserved:
    no live clustering runs without owner ratification of the backend
    choice.  Same refusal pattern as CP-M6-1-1..1-4 pluggable seams."""


@dataclass(frozen=True)
class CandidateStratum:
    """A single candidate stratum emitted by the clustering seam.

    Three carriers:
      - `stratum_id` — opaque identifier assigned by the backend.  A
        cluster's identity is 'distinct variant exists', not a
        human-readable name (§5.3 clause 2 verbatim: "not what it is
        called").
      - `member_attribute_names` — immutable tuple of `attribute_name`
        strings referencing CharacterRegister entries.  No audio-byte
        / voiceprint / speaker-identity carriers (§3.1 P038 + §6.2
        P098).
      - `backend_name` — the name of the clustering backend that
        emitted this stratum (provenance to backend, not to speaker
        identity per §6.2 P098).
    """

    stratum_id: str
    member_attribute_names: Tuple[str, ...]
    backend_name: str


class ClusteringBackend(Protocol):
    """Protocol for clustering backends.

    Case-agnostic Protocol: no coupling to a specific ML library.
    Backends implement `.name` (str) + `.cluster(entries) ->
    Tuple[CandidateStratum, ...]`.  Duck-typed at the seam; the seam
    itself never imports a concrete backend.
    """

    name: str

    def cluster(self, *, entries: Tuple[Any, ...]) -> Tuple[
        CandidateStratum, ...
    ]:
        ...


class UnratifiedInferredClusteringBackend:
    """Placeholder clustering backend.

    Refuses live invocation with `ClusteringBackendUnratifiedError`
    carrying the `[INFERRED-pending-ratification]` marker per D10
    pluggable-seam discipline (owner ruling on unratified backends,
    same pattern as CP-M6-1-1 `UnratifiedInferredBackend`,
    CP-M6-1-2 `UnratifiedCodeSwitchInferredBackend`, etc.).
    """

    name: str = "unratified-inferred"

    def cluster(self, *, entries: Tuple[Any, ...]) -> Tuple[
        CandidateStratum, ...
    ]:
        raise ClusteringBackendUnratifiedError(
            "clustering backend is [INFERRED-pending-ratification] "
            "per D10; live invocation refused until owner ratifies a "
            "clustering backend for the audio plane (§5.3 clause 1)"
        )


def cluster_character_register(
    *,
    character_register: CharacterRegister,
    backend: ClusteringBackend,
) -> Tuple[CandidateStratum, ...]:
    """Run the pluggable clustering seam over `character_register.entries`.

    Refusals:
      - `CharacterRegisterEmptyError` when the register has zero
        entries (§5.3 clause 1 — no stream, no clustering).
      - Whatever the backend raises (e.g.
        `ClusteringBackendUnratifiedError` for the unratified
        placeholder) propagates unchanged.

    Composition trust: the seam does not interpret backend output; it
    returns whatever the backend produces verbatim, preserving the
    backend's authoritative view of the strata.
    """
    if len(character_register.entries) == 0:
        raise CharacterRegisterEmptyError(
            "cluster_character_register: character_register has zero "
            "entries; no clustering to do (§5.3 clause 1 verbatim: "
            "clustering runs over the character stream)"
        )
    return backend.cluster(entries=character_register.entries)
