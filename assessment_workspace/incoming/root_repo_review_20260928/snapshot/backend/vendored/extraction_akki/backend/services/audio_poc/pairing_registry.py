"""W-AUDIO-POC · CP-A4 · Pairing registry — join recordings & transcripts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Sequence

from services.audio_poc.recording_inventory import RecordingEntry, RecordingKey
from services.audio_poc.transcript_inventory import TranscriptEntry, TranscriptKey


PAIR_STATES: frozenset = frozenset({
    "PAIRED",
    "RECORDING_ONLY",
    "TRANSCRIPT_ONLY",
    "RECORDING_ONLY_PARTIAL",
})


@dataclass(frozen=True)
class AudioTranscriptPair:
    """One pairing between an OFFAIRRECS recording and its transcript.

    `recording_sha256_hex` and `transcript_sha256_hex` are set to the
    empty string on the side that is missing.
    """

    station: str
    date_utc: str
    slot: str
    filename_stem: str
    pair_state: str
    recording_sha256_hex: str
    transcript_sha256_hex: str


def _canon_key(entry) -> tuple:
    return (entry.station, entry.date_utc, entry.slot, entry.filename_stem)


def pair_inventories(
    recordings: Sequence[RecordingEntry],
    transcripts: Sequence[TranscriptEntry],
) -> Sequence[AudioTranscriptPair]:
    """Deterministic join over the canonical key.

    Sort output by `(station, date_utc, slot, filename_stem)`.  Pair
    state:
      PAIRED                  — recording & transcript, transcript FINISHED.
      RECORDING_ONLY_PARTIAL  — recording & transcript, transcript not FINISHED.
      RECORDING_ONLY          — recording only.
      TRANSCRIPT_ONLY         — transcript only (orphan; not a gap target).
    """
    r_by_key = {_canon_key(r): r for r in recordings}
    t_by_key = {_canon_key(t): t for t in transcripts}
    all_keys = sorted(set(r_by_key) | set(t_by_key))
    pairs = []
    for k in all_keys:
        r = r_by_key.get(k)
        t = t_by_key.get(k)
        station, date_utc, slot, filename_stem = k
        if r is not None and t is not None:
            state = "PAIRED" if t.transcript_status == "FINISHED" else "RECORDING_ONLY_PARTIAL"
            r_sha = r.sha256_hex
            t_sha = t.sha256_hex
        elif r is not None:
            state = "RECORDING_ONLY"
            r_sha = r.sha256_hex
            t_sha = ""
        else:
            state = "TRANSCRIPT_ONLY"
            r_sha = ""
            t_sha = t.sha256_hex  # type: ignore[union-attr]
        pairs.append(
            AudioTranscriptPair(
                station=station,
                date_utc=date_utc,
                slot=slot,
                filename_stem=filename_stem,
                pair_state=state,
                recording_sha256_hex=r_sha,
                transcript_sha256_hex=t_sha,
            )
        )
    return tuple(pairs)


def pairing_snapshot_sha256(pairs: Sequence[AudioTranscriptPair]) -> str:
    """Deterministic sha256 hex over canonical-JSON serialisation."""
    serialised = json.dumps(
        [asdict(p) for p in pairs],
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialised).hexdigest()
