"""W-AUDIO-POC · CP-A3 · OBS `google-transcripts` transcript inventory.

Parses OBS `ListObjects` output for the `google-transcripts` bucket
into a deterministic, canonically-keyed transcript inventory.  Live
OBS invocation happens upstream through the SDK guarded by
`services.audio_poc.readonly_obs_guard.guarded_obs_call`.

Canonical OBS key: `<station>/<YYYYMMDD>/<YYYYMMDD>_<HHMM>_<stem>.json`
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from typing import Sequence, Tuple


_OBS_KEY_REGEX = re.compile(
    r"^(channel\d{2})/(\d{8})/(\d{8})_(\d{4})_(.+)\.json$"
)

# Threshold below which a canonical-shape transcript is classed PARTIAL
# instead of FINISHED.  Set to 512 bytes: a real JSON transcript with
# metadata + segments will exceed this; a truncated / placeholder
# transcript will fall below.
FINISHED_MIN_BYTES: int = 512

# Allowed transcript statuses AT INVENTORY (MISSING is a pairing surface,
# not an inventory surface).
TranscriptStatus: frozenset = frozenset({"FINISHED", "PARTIAL", "MALFORMED"})


class TranscriptKeyInvalid(Exception):
    """Raised when an OBS key cannot be parsed into a canonical transcript key."""


@dataclass(frozen=True)
class TranscriptKey:
    """Canonical identity of a transcript.  Hashable, ordering key."""

    station: str
    date_utc: str
    slot: str
    filename_stem: str


@dataclass(frozen=True)
class TranscriptEntry:
    """Full inventory row for a transcript."""

    station: str
    date_utc: str
    slot: str
    filename_stem: str
    size_bytes: int
    mtime_utc: str
    sha256_hex: str
    transcript_status: str


def extract_transcript_canonical_key(obs_key: str) -> TranscriptKey:
    """Parse an OBS key into a `TranscriptKey`.

    Refuses via `TranscriptKeyInvalid` on any shape mismatch (missing
    station-dir, missing date-dir, wrong extension, mismatched dates
    between dir and filename, etc.).
    """
    if not obs_key:
        raise TranscriptKeyInvalid("empty key")
    m = _OBS_KEY_REGEX.match(obs_key)
    if not m:
        raise TranscriptKeyInvalid(
            f"OBS key does not match canonical shape: "
            f"expected <station>/<YYYYMMDD>/<YYYYMMDD>_<HHMM>_<stem>.json"
        )
    station, date_dir, date_file, slot, stem = m.groups()
    if date_dir != date_file:
        raise TranscriptKeyInvalid(
            f"date-dir {date_dir!r} does not match filename date {date_file!r}"
        )
    return TranscriptKey(
        station=station,
        date_utc=date_dir,
        slot=slot,
        filename_stem=f"{date_file}_{slot}_{stem}",
    )


def classify_transcript_status(obs_key: str, size_bytes: int) -> str:
    """Return the `transcript_status` string for a listed OBS object.

    * `MALFORMED` if the key doesn't match the canonical shape.
    * `FINISHED` if the shape matches AND `size_bytes >= FINISHED_MIN_BYTES`.
    * `PARTIAL` if the shape matches AND `size_bytes <  FINISHED_MIN_BYTES`.
    """
    try:
        extract_transcript_canonical_key(obs_key)
    except TranscriptKeyInvalid:
        return "MALFORMED"
    if size_bytes >= FINISHED_MIN_BYTES:
        return "FINISHED"
    return "PARTIAL"


def canonicalize_transcript_inventory(
    raw_entries: Sequence[Tuple[str, int, str, str]],
) -> Sequence[TranscriptEntry]:
    """Deterministic, sorted, deduplicated TranscriptEntry sequence.

    Sort: `(station, date_utc, slot, filename_stem)`.
    Dedup: first-occurrence wins.
    Silent-skip: MALFORMED keys are omitted (their status is derivable
    at classify time but not carried into the inventory itself, since
    the canonical key is required to appear in a pairing).
    """
    by_key = {}
    for obs_key, size_bytes, mtime_utc, sha256_hex in raw_entries:
        try:
            key = extract_transcript_canonical_key(obs_key)
        except TranscriptKeyInvalid:
            continue
        if key in by_key:
            continue  # first-occurrence wins
        status = classify_transcript_status(obs_key, int(size_bytes))
        by_key[key] = TranscriptEntry(
            station=key.station,
            date_utc=key.date_utc,
            slot=key.slot,
            filename_stem=key.filename_stem,
            size_bytes=int(size_bytes),
            mtime_utc=str(mtime_utc),
            sha256_hex=str(sha256_hex),
            transcript_status=status,
        )
    return tuple(
        sorted(
            by_key.values(),
            key=lambda e: (e.station, e.date_utc, e.slot, e.filename_stem),
        )
    )


def transcript_inventory_snapshot_sha256(
    entries: Sequence[TranscriptEntry],
) -> str:
    """Deterministic sha256 hex over the canonical-JSON serialisation."""
    serialised = json.dumps(
        [asdict(e) for e in entries],
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialised).hexdigest()
