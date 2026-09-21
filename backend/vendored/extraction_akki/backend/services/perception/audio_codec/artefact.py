"""M6 · Audio-Plane v1.0 · CP-M6-4-2 · CodecArtefact + codec_version invariants.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §3.2 P047 (V35 · output shape):
      "{ content_tokens[], character_stream, codec_version } · Target token rate 50–100 tokens/second of audio."

- Audio-Plane §3.2 P048 (V36 · codec_version mandatory in downstream provenance):
      "codec_version is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens."

- M6 grounding brief §Sub-wave 4 Fold-in D7 (verbatim):
      "grounding-brief anchor for D7 lands at CP-M6-4-2 as an invariant: every codec artefact carries codec_version and the version identifier is a first-class carrier in the census surface."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - §3.1 P038 tokens-not-waveforms: no audio-byte carriers.
  - Case-agnostic; no executive-domain tokens.

Contract:

    CodecArtefact — frozen 3-carrier dataclass per §3.2 P047 verbatim
      output shape:
        content_tokens · character_stream · codec_version
      Refuses empty codec_version at construction time.

    require_codec_version(*, artefact) -> None
      Refuses any object without a non-empty `codec_version` attribute.

    assert_downstream_carries_codec_version(*, provenance) -> None
      §3.2 P048 helper for downstream artefact provenance mappings.

Refusals:
    MissingCodecVersionError
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple


class MissingCodecVersionError(Exception):
    """Raised by CP-M6-4-2 helpers when a codec artefact or downstream
    provenance mapping does not carry a non-empty `codec_version`.

    §3.2 P048 verbatim: 'codec_version is a mandatory field of every
    downstream artifact's provenance.'  D7 fold-in invariant: no
    silent absence."""


@dataclass(frozen=True)
class CodecArtefact:
    """The §3.2 P047 verbatim codec output shape.

    Three carriers:
      - `content_tokens` — immutable tuple of content-stream token ids
        (§3.1 P039 verbatim: 'the content stream (what was said)').
      - `character_stream` — immutable nested tuple carrying the
        character-stream frames (§3.1 P039 verbatim: 'the character
        stream (how it was said) — input to the Character Register.
        The character stream is retained and routed, never discarded
        as noise.').
      - `codec_version` — the codec's version identifier.  Must be
        non-empty at construction (D7 fold-in invariant).

    Pull-seam / §3.1 P038 tokens-not-waveforms discipline: no
    `audio_bytes` / `waveform` / `samples` carriers.
    """

    content_tokens: Tuple[int, ...]
    character_stream: Tuple[Tuple[int, ...], ...]
    codec_version: str

    def __post_init__(self) -> None:  # noqa: D401 · frozen-dataclass hook
        if not self.codec_version:
            raise MissingCodecVersionError(
                "CodecArtefact: codec_version must be non-empty "
                "(§3.2 P047 verbatim output shape · D7 fold-in "
                "invariant); got empty string"
            )


def require_codec_version(*, artefact: Any) -> None:
    """Assert `artefact.codec_version` is a non-empty string.

    Refuses (`MissingCodecVersionError`) when the attribute is absent,
    None, or empty.  This is the §3.2 P048 gate applied to any
    downstream artefact object.
    """
    value = getattr(artefact, "codec_version", None)
    if value is None or (isinstance(value, str) and not value):
        raise MissingCodecVersionError(
            f"artefact {type(artefact).__name__} lacks a non-empty "
            f"codec_version (§3.2 P048 verbatim: 'codec_version is a "
            f"mandatory field of every downstream artifact's provenance')"
        )


def assert_downstream_carries_codec_version(
    *,
    provenance: Mapping[str, Any],
) -> None:
    """Assert a downstream artefact's provenance mapping carries a
    non-empty `codec_version` key.

    §3.2 P048 verbatim: 'codec_version is a mandatory field of every
    downstream artifact's provenance. A transcript states which codec
    produced its tokens.'
    """
    value = provenance.get("codec_version")
    if not value:
        raise MissingCodecVersionError(
            "downstream provenance is missing a non-empty codec_version "
            "(§3.2 P048 verbatim: 'codec_version is a mandatory field of "
            "every downstream artifact's provenance')"
        )
