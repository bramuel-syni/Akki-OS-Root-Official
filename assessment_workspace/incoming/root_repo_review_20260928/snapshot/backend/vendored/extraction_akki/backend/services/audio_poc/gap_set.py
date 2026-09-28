"""W-AUDIO-POC · CP-A4 · Gap-set compute over pairings.

Pure function: given a pairing registry, return the RecordingKey
subset that needs gap-fill transcription — i.e. pairs whose state is
RECORDING_ONLY (no transcript) or RECORDING_ONLY_PARTIAL (transcript
exists but not FINISHED).

TRANSCRIPT_ONLY pairs (orphan transcripts) are NOT included: they
correspond to no recording and cannot be transcribed.
"""

from __future__ import annotations

from typing import Sequence

from services.audio_poc.pairing_registry import AudioTranscriptPair
from services.audio_poc.recording_inventory import RecordingKey


_GAP_STATES = frozenset({"RECORDING_ONLY", "RECORDING_ONLY_PARTIAL"})


def compute_gap_set(
    pairs: Sequence[AudioTranscriptPair],
) -> Sequence[RecordingKey]:
    """Return the recording-side keys that need gap-fill transcription.

    Deterministic ordering (input pairs are assumed already sorted; the
    output preserves that order).
    """
    return tuple(
        RecordingKey(
            station=p.station,
            date_utc=p.date_utc,
            slot=p.slot,
            filename_stem=p.filename_stem,
        )
        for p in pairs
        if p.pair_state in _GAP_STATES
    )
