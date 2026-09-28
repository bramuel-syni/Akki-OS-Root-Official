"""W-AUDIO-POC · CP-A1 · Read-only OBS guard.

Refuses any OBS call outside {ListObjects, HeadObject, GetObject}.
Refuses any bucket other than the owner-authorised `google-transcripts`.

A separate GATED writer (`write_back.py` at CP-A5) uses `PutObject`
after `release_gate.admit_transcript_release` returns.  This guard is
the READ-SIDE fence only.
"""

from __future__ import annotations


OBS_ALLOWED_OPS: frozenset = frozenset(
    {"ListObjects", "HeadObject", "GetObject"}
)
OBS_ALLOWED_BUCKET: str = "google-transcripts"


class OBSOpNotAllowed(Exception):
    """Raised when an OBS call names an op outside `OBS_ALLOWED_OPS`."""


class OBSBucketNotAllowed(Exception):
    """Raised when an OBS call names a bucket other than
    `OBS_ALLOWED_BUCKET`.
    """


def guarded_obs_call(op: str, bucket: str, key: str) -> None:
    """Refuse unless (op, bucket) both pass the allow-list.

    `key` is accepted as informational only (may be empty for ListObjects).
    Returns None on admit.  Pure-Python gate — no network I/O.
    """
    if op not in OBS_ALLOWED_OPS:
        raise OBSOpNotAllowed(
            f"OBS op refused: {op!r} not in {sorted(OBS_ALLOWED_OPS)}"
        )
    if bucket != OBS_ALLOWED_BUCKET:
        raise OBSBucketNotAllowed(
            f"OBS bucket refused: got {bucket!r}, expected {OBS_ALLOWED_BUCKET!r}"
        )
    return None
