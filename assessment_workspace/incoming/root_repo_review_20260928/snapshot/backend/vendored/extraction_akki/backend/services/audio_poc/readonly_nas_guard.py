"""W-AUDIO-POC · CP-A1 · Read-only NAS guard.

Refuses any SMB/Synology-FileStation call outside {List, Read, Status}.
Refuses any path that is not under the owner-authorised share
`OFFAIRRECS`.

Wave-honest limit: this guard is a CALL-SHAPE gate, not a network gate.
The caller is trusted to route through JUMP-hosted smbclient (per
`phase0/connectivity_receipts/20260914T113109Z_NAS_share_access_survey.json`
and the connectivity-redo close 2026-09-14).  This guard freezes the
op/path allow-list as an invariant so a future caller cannot silently
add Write / Delete / Move.
"""

from __future__ import annotations


NAS_ALLOWED_OPS: frozenset = frozenset({"List", "Read", "Status"})
NAS_ALLOWED_SHARE: str = "OFFAIRRECS"


class NASOpNotAllowed(Exception):
    """Raised when a NAS call names an op outside `NAS_ALLOWED_OPS`."""


class NASPathNotAllowed(Exception):
    """Raised when a NAS call names a path outside the allowed share."""


def guarded_nas_call(op: str, path: str) -> None:
    """Refuse the call unless the op AND path both pass the allow-list.

    Returns None on admit.  Never touches the network — this is a
    pure-Python gate that upstream call sites invoke BEFORE their SMB
    client is instantiated.
    """
    if op not in NAS_ALLOWED_OPS:
        raise NASOpNotAllowed(
            f"NAS op refused: {op!r} not in {sorted(NAS_ALLOWED_OPS)}"
        )
    # Path check: the share name must appear as a top-level path segment
    # (avoids trivial-bypass by embedding the share name in a filename).
    if not path:
        raise NASPathNotAllowed("NAS path refused: empty path")
    parts = [p for p in path.replace("\\", "/").split("/") if p]
    if NAS_ALLOWED_SHARE not in parts:
        raise NASPathNotAllowed(
            f"NAS path refused: share {NAS_ALLOWED_SHARE!r} not in path segments"
        )
    return None
