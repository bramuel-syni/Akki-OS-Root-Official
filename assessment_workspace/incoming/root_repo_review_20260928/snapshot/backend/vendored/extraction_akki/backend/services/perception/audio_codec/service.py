"""M6 · Audio-Plane v1.0 · CP-M6-4-1 · perception/audio_codec/ service skeleton.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §3.1 P038 (V29):
      "All downstream audio work — extraction, character analysis, training — operates on discrete token sequences produced by a neural audio codec, not on waveforms."

- Audio-Plane §3.2 P045 (V33 · service path · N4 anchor):
      "perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."

- Audio-Plane §3.2 P047 (V35 · output shape + token-rate target):
      "{ content_tokens[], character_stream, codec_version } · Target token rate 50–100 tokens/second of audio."

- Audio-Plane §3.2 P049 (V37 · pretraining):
      "The codec pretrains unsupervised on unlabelled estate audio, under the standard commissioned-job contract."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - No audio bytes in the carrier shape (§3.1 P038 tokens-not-waveforms).
  - Case-agnostic; no executive-domain tokens.

Contract:

    AUDIO_CODEC_SERVICE_PATH: str = "perception/audio_codec/"

    AudioCodecServiceDescriptor — frozen 3-carrier dataclass:
      service_path · pretraining_contract · token_rate_target (min, max).

    build_service_descriptor() -> AudioCodecServiceDescriptor
      Returns the canon-verbatim descriptor.

    assert_registered_like_perception_model(descriptor) -> None
      Asserts the descriptor carries the §3.2 P045 verbatim
      registration fields.  Refuses with `PerceptionRegistrationError`
      when service_path or token_rate_target deviates.

Refusals:
    PerceptionRegistrationError
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


AUDIO_CODEC_SERVICE_PATH: str = "perception/audio_codec/"


class PerceptionRegistrationError(Exception):
    """Raised when an `AudioCodecServiceDescriptor` deviates from the
    §3.2 P045 verbatim registration contract."""


@dataclass(frozen=True)
class AudioCodecServiceDescriptor:
    """The canon-anchored perception-model registration descriptor for
    the audio codec service.

    Three carriers:
      - `service_path` — §3.2 P045 verbatim: `"perception/audio_codec/"`.
      - `pretraining_contract` — §3.2 P049 verbatim: the codec pretrains
        unsupervised on unlabelled estate audio, under the standard
        commissioned-job contract.
      - `token_rate_target` — §3.2 P047 verbatim: (50, 100)
        tokens/second of audio (inclusive min–max range).

    Pull-seam / §3.1 P038 discipline: no `audio_bytes` · `waveform` ·
    `samples` · `raw_audio` carriers.  Tokens-not-waveforms.
    """

    service_path: str
    pretraining_contract: str
    token_rate_target: Tuple[int, int]


def build_service_descriptor() -> AudioCodecServiceDescriptor:
    """Build the canon-verbatim `AudioCodecServiceDescriptor` for the
    audio codec service."""
    return AudioCodecServiceDescriptor(
        service_path=AUDIO_CODEC_SERVICE_PATH,
        pretraining_contract=(
            "The codec pretrains unsupervised on unlabelled estate "
            "audio, under the standard commissioned-job contract."
        ),
        token_rate_target=(50, 100),
    )


def assert_registered_like_perception_model(
    descriptor: AudioCodecServiceDescriptor,
) -> None:
    """Assert the descriptor carries the §3.2 P045 verbatim registration
    fields.  Refuses with `PerceptionRegistrationError` on any deviation.

    Sub-wave 4 core invariant: the codec service satisfies the
    §3.2 P045 verbatim 'registered like any other perception model'
    contract.
    """
    # §3.2 P045: service path is verbatim.
    if descriptor.service_path != AUDIO_CODEC_SERVICE_PATH:
        raise PerceptionRegistrationError(
            f"perception audio_codec: service_path drift "
            f"{descriptor.service_path!r} vs §3.2 P045 verbatim "
            f"{AUDIO_CODEC_SERVICE_PATH!r}"
        )
    # §3.2 P047: token_rate_target must be within the verbatim range.
    lo, hi = descriptor.token_rate_target
    if not (50 <= lo <= hi <= 100):
        raise PerceptionRegistrationError(
            f"perception audio_codec: token_rate_target "
            f"{descriptor.token_rate_target!r} outside §3.2 P047 "
            f"verbatim range 50–100 tokens/second"
        )
    return None
