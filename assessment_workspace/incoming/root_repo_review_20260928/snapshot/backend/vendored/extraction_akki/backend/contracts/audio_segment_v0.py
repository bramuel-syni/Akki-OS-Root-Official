"""AudioSegmentV0 · Audio Intelligence Plane §3.1-3.2 · codec-tokenised segment.

Verbatim spec anchors (canon/w11_new_docs/audio_intel_plane.md §3.1-3.2):

    §3.1 verbatim:
      'All downstream audio work - extraction, character analysis,
       training - operates on discrete token sequences produced by a
       neural audio codec, not on waveforms.'
      'Tokenization exposes two separable streams per segment: the
       content stream (what was said - input to ASR/NER) and the
       character stream (how it was said - input to the Character
       Register). The character stream is retained and routed, never
       discarded as noise.'
      'Failure behaviour: audio in an unsupported condition fails
       closed with a stated reason. The codec never silently degrades
       quality.'

    §1.5 verbatim (governing doctrine):
      'Unrepresentable, not policed. Safety boundaries are enforced
       by making the violating state impossible to express in the
       contract - the pattern established by the assertion floor -
       not by review after the fact.'

Contract shape follows §1.5: content_stream + character_stream are
BOTH required and NON-EMPTY; a segment cannot exist without both.

Same-commit DoD:
  * ConfigDict(extra='forbid', frozen=True).
  * Snapshot in tests/invariants/audio_segment_v0.contract_snapshot.json.
  * Parity map bump 66 -> 67.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class AudioSegmentV0(BaseModel):
    """Codec-tokenised audio segment · §1.5 unrepresentable invariants.

    Both streams are required at construction. A missing character stream
    (§3.1 verbatim: 'never discarded as noise') is a contract refusal,
    not a runtime warning.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    segment_id: str = Field(..., min_length=1)
    estate_ref: str = Field(
        ...,
        min_length=1,
        description="§1.1 recursive framing: 'a single file is an estate'. "
                    "estate_ref cites the containing estate.",
    )
    codec_service: Literal["perception/audio_codec"] = Field(
        default="perception/audio_codec",
        description="§3.2 verbatim: 'perception/audio_codec/ - registered "
                    "like any other perception model'. No parallel codec "
                    "services (§1.2).",
    )
    content_stream_tokens: List[int] = Field(
        ...,
        min_length=1,
        description="§3.1 verbatim: 'content stream (what was said - input "
                    "to ASR/NER)'.",
    )
    character_stream_tokens: List[int] = Field(
        ...,
        min_length=1,
        description="§3.1 verbatim: 'character stream (how it was said - "
                    "input to the Character Register). The character stream "
                    "is retained and routed, never discarded as noise.'",
    )
    condition_profile: str = Field(
        ...,
        min_length=1,
        description="§3.2 · declared or detected condition profile.",
    )
    bounds_start_ms: int = Field(..., ge=0)
    bounds_end_ms: int = Field(..., ge=0)
    tokenised_at: str = Field(..., min_length=1)
