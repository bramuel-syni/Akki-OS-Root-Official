"""W-DATA-SUITE-V2-LIFT · CP-D5 · Analysis-session record (Canon-3 §9.3 append-only).

Data-Suite analysis records never overwrite; each session emits a new snapshot
with a deterministic fingerprint. Duplicate `session_id` is refused at the
append surface.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Sequence, Tuple


class AnalysisSessionCollision(Exception):
    """Raised when a caller attempts to append a session whose id already exists."""


@dataclass(frozen=True)
class AnalysisSession:
    session_id: str
    session_kind: str
    created_at_iso: str
    snapshot_fingerprint_hex: str
    source_ref_count: int


def compute_snapshot_fingerprint(
    session_id: str,
    session_kind: str,
    source_unit_refs: Sequence[str],
) -> str:
    """Deterministic sha256-hex fingerprint over the session identity + source order.

    Order of `source_unit_refs` is significant: the same set in a different
    order yields a different fingerprint (callers canonicalise upstream if they
    want order-invariance).
    """
    payload = json.dumps(
        {
            "session_id": session_id,
            "session_kind": session_kind,
            "source_unit_refs": list(source_unit_refs),
        },
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def append_session(
    new_session: AnalysisSession,
    *,
    existing: Sequence[AnalysisSession],
) -> Tuple[AnalysisSession, ...]:
    """Return a new tuple `existing + (new_session,)`; refuse on id collision.

    Canon-3 §9.3 · append-only ledger spirit: no overwrite path is provided.
    """
    for s in existing:
        if s.session_id == new_session.session_id:
            raise AnalysisSessionCollision(
                f"session_id already recorded: {new_session.session_id!r}"
            )
    return tuple(existing) + (new_session,)
