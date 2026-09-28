"""W-AUDIO-POC · CP-A2 · NAS OFFAIRRECS recording inventory.

Parses SMB `ls` output into a deterministic, canonically-keyed
recording inventory.  Live SMB invocation happens upstream through
JUMP-hosted smbclient (per connectivity redo close 2026-09-14);
this module is the parse + canonicalise + fingerprint contract.

Governance: every path fed here should be pre-guarded upstream by
`services.audio_poc.readonly_nas_guard.guarded_nas_call`.

Canonical NAS path shape: `//<host>/OFFAIRRECS/Record/channel<NN>/
<YYYYMMDD>_<HHMM>_<stem>.<ext>`
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from typing import Optional, Sequence, Tuple


# Path parse regex for canonical key extraction.
_PATH_REGEX = re.compile(
    r"/OFFAIRRECS/Record/(channel\d{2})/(\d{8})_(\d{4})_(.+)\.(\w+)$"
)

# smbclient ls line parse regex.  smbclient formats one entry as:
#   <filename>  <attrs>   <size>   <weekday mon day hh:mm:ss year>
# `filename` may contain spaces; `attrs` is a short letter code
# (A / D / S / H / R / N …); `size` is decimal; weekday+month are 3-letter.
_SMB_LINE_REGEX = re.compile(
    r"^\s*(?P<filename>\S(?:.*\S)?)\s+(?P<attrs>[ADSHRN]+)\s+(?P<size>\d+)\s+"
    r"(?P<wday>\w{3})\s+(?P<mon>\w{3})\s+(?P<mday>\d{1,2})\s+"
    r"(?P<hh>\d{2}):(?P<mm>\d{2}):(?P<ss>\d{2})\s+(?P<year>\d{4})\s*$"
)

_MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


class RecordingKeyInvalid(Exception):
    """Raised when a NAS path cannot be parsed into a canonical key."""


@dataclass(frozen=True)
class RecordingKey:
    """Canonical identity of a recording.  Hashable, ordering key."""

    station: str
    date_utc: str
    slot: str
    filename_stem: str


@dataclass(frozen=True)
class RecordingEntry:
    """Full inventory row for a recording."""

    station: str
    date_utc: str
    slot: str
    filename_stem: str
    size_bytes: int
    mtime_utc: str
    sha256_hex: str


def extract_canonical_key(nas_path: str) -> RecordingKey:
    """Parse an OFFAIRRECS path into a `RecordingKey`.

    Refuses via `RecordingKeyInvalid` if the path does not match the
    canonical shape (missing OFFAIRRECS/channel segment, missing
    date/slot in filename, etc.).
    """
    if not nas_path:
        raise RecordingKeyInvalid("empty path")
    # Normalise Windows-style backslashes.
    normalised = nas_path.replace("\\", "/")
    m = _PATH_REGEX.search(normalised)
    if not m:
        raise RecordingKeyInvalid(
            f"path does not match OFFAIRRECS canonical shape: "
            f"expected /OFFAIRRECS/Record/channel<NN>/<YYYYMMDD>_<HHMM>_<stem>.<ext>"
        )
    station, date_utc, slot, stem, _ext = m.groups()
    return RecordingKey(
        station=station,
        date_utc=date_utc,
        slot=slot,
        filename_stem=f"{date_utc}_{slot}_{stem}",
    )


def parse_smbclient_ls_line(line: str) -> Optional[Tuple[str, int, str]]:
    """Parse one smbclient `ls` line.

    Returns `(filename, size_bytes, mtime_utc)` on a valid FILE row
    (attribute contains 'A' but not 'D'); returns None on directory
    entries, dot entries, or malformed lines.  Never raises.
    """
    if not line or not line.strip():
        return None
    m = _SMB_LINE_REGEX.match(line)
    if not m:
        return None
    filename = m.group("filename").strip()
    attrs = m.group("attrs")
    if "D" in attrs:  # directory
        return None
    if filename in (".", ".."):
        return None
    try:
        size_bytes = int(m.group("size"))
    except ValueError:
        return None
    try:
        month = _MONTH_MAP[m.group("mon")]
    except KeyError:
        return None
    try:
        dt = datetime(
            year=int(m.group("year")),
            month=month,
            day=int(m.group("mday")),
            hour=int(m.group("hh")),
            minute=int(m.group("mm")),
            second=int(m.group("ss")),
            tzinfo=timezone.utc,
        )
    except ValueError:
        return None
    mtime_utc = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return (filename, size_bytes, mtime_utc)


def canonicalize_inventory(
    raw_entries: Sequence[Tuple[str, int, str, str]],
) -> Sequence[RecordingEntry]:
    """Turn raw (path, size, mtime, sha256) tuples into a deterministic,
    canonically-sorted, deduplicated sequence of `RecordingEntry`.

    Sort order: `(station, date_utc, slot, filename_stem)`.
    Deduplication: first-occurrence wins on collision.
    Invalid paths (fail `extract_canonical_key`) are silently skipped.
    """
    by_key = {}
    for nas_path, size_bytes, mtime_utc, sha256_hex in raw_entries:
        try:
            key = extract_canonical_key(nas_path)
        except RecordingKeyInvalid:
            continue
        if key in by_key:
            continue  # first-occurrence wins
        by_key[key] = RecordingEntry(
            station=key.station,
            date_utc=key.date_utc,
            slot=key.slot,
            filename_stem=key.filename_stem,
            size_bytes=int(size_bytes),
            mtime_utc=str(mtime_utc),
            sha256_hex=str(sha256_hex),
        )
    return tuple(
        sorted(
            by_key.values(),
            key=lambda e: (e.station, e.date_utc, e.slot, e.filename_stem),
        )
    )


def inventory_snapshot_sha256(
    entries: Sequence[RecordingEntry],
) -> str:
    """Return a deterministic sha256 hex over the canonical serialisation
    of the inventory.

    Serialisation: canonical-JSON of a list of dicts (sorted keys, no
    whitespace, ensure_ascii=False).  Sensitive to any field change.
    """
    serialised = json.dumps(
        [asdict(e) for e in entries],
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialised).hexdigest()
