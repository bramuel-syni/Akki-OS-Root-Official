"""services.lowered_standard.sessions — CA1-010 session store.

Session ceiling: 24h (86400s). Every open + close writes a governance
receipt via services.chokepoint.register_crossing so the session
lifecycle is on the trust log.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.chokepoint import register_crossing

log = logging.getLogger(__name__)


CEILING_SECONDS = 86400  # 24 hours per CA1-010 letter
MIN_REASON_LENGTH = 12


def _dir() -> Path:
    return Path(os.environ.get(
        "LOWERED_STANDARD_DIR",
        "/app/assessment_workspace/phase0/lowered_standard_sessions",
    ))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def _parse_iso(s: str) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


@dataclass
class LoweredStandardSession:
    session_id: str
    actor: str
    reason: str
    purpose_scope: List[str]
    started_at: str
    expires_at: str
    state: str = "active"           # 'active' · 'closed' · 'expired'
    closed_at: str = ""
    open_receipt_id: str = ""
    close_receipt_id: str = ""


def _load(session_id: str) -> Optional[LoweredStandardSession]:
    f = _dir() / f"{session_id}.json"
    if not f.exists():
        return None
    try:
        body = json.loads(f.read_text())
        return LoweredStandardSession(**body)
    except Exception:
        return None


def _persist(sess: LoweredStandardSession) -> None:
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{sess.session_id}.json").write_text(
        json.dumps(asdict(sess), indent=2, sort_keys=True)
    )


def _all_files() -> List[Path]:
    d = _dir()
    if not d.is_dir():
        return []
    return sorted(d.glob("ls-*.json"))


def open_session(
    *,
    actor: str,
    reason: str,
    purpose_scope: List[str],
    expires_in_seconds: int = 1800,
) -> LoweredStandardSession:
    """Open a session-scoped lowered standard. Writes attestation receipt
    on the trust log."""
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("actor_required — non-empty string.")
    if not isinstance(reason, str) or len(reason.strip()) < MIN_REASON_LENGTH:
        raise ValueError(
            f"reason_required · minimum {MIN_REASON_LENGTH} characters. "
            "CA1-010 · sessions must be logged with named intent."
        )
    if not isinstance(purpose_scope, list) or not purpose_scope:
        raise ValueError("purpose_scope_required · list of Solva purpose IDs.")
    if not isinstance(expires_in_seconds, int) or expires_in_seconds <= 0:
        raise ValueError("expires_in_seconds_required · positive integer.")
    if expires_in_seconds > CEILING_SECONDS:
        raise ValueError(
            f"expires_in_seconds_ceiling · CA1-010 letter caps at "
            f"{CEILING_SECONDS} seconds (24h). Got {expires_in_seconds}."
        )

    now = _now()
    expires_at = now + timedelta(seconds=expires_in_seconds)
    session_id = f"ls-{uuid.uuid4().hex[:12]}"

    # Attestation receipt on the trust log (kind: governance_read).
    receipt = register_crossing(
        kind="governance_read",
        endpoint={"host": "in-process", "region": "in_process"},
        verb="lowered_standard_open",
        payload_shape={
            "session_id": session_id,
            "purpose_scope": ",".join(purpose_scope),
            "expires_at": _iso(expires_at),
            "reason_excerpt": reason[:80],
        },
        actor=actor,
        masking_tier="receipt_only",
    )

    sess = LoweredStandardSession(
        session_id=session_id,
        actor=actor,
        reason=reason,
        purpose_scope=purpose_scope,
        started_at=_iso(now),
        expires_at=_iso(expires_at),
        state="active",
        open_receipt_id=receipt.receipt_id,
    )
    _persist(sess)
    return sess


def close_session(*, session_id: str, actor: str) -> LoweredStandardSession:
    """Close a session · writes close attestation receipt."""
    sess = _load(session_id)
    if not sess:
        raise ValueError(f"session_not_found · {session_id!r}")
    if sess.state != "active":
        # Idempotent close.
        return sess

    receipt = register_crossing(
        kind="governance_read",
        endpoint={"host": "in-process", "region": "in_process"},
        verb="lowered_standard_close",
        payload_shape={
            "session_id": session_id,
            "opened_by": sess.actor,
            "closed_by": actor,
        },
        actor=actor,
        masking_tier="receipt_only",
    )
    sess.state = "closed"
    sess.closed_at = _iso(_now())
    sess.close_receipt_id = receipt.receipt_id
    _persist(sess)
    return sess


def _project_state(sess: LoweredStandardSession) -> LoweredStandardSession:
    """Compute state (active/closed/expired) from stored data + wall clock."""
    if sess.state == "closed":
        return sess
    expires_dt = _parse_iso(sess.expires_at)
    if expires_dt and _now() > expires_dt:
        # Not persisted as expired; project it live (avoids race-condition
        # concerns · a later close call reads the same wall clock).
        expired = LoweredStandardSession(**asdict(sess))
        expired.state = "expired"
        return expired
    return sess


def active_sessions() -> List[LoweredStandardSession]:
    """Non-expired · not-closed sessions."""
    out: List[LoweredStandardSession] = []
    for f in _all_files():
        try:
            sess = LoweredStandardSession(**json.loads(f.read_text()))
        except Exception:
            continue
        projected = _project_state(sess)
        if projected.state == "active":
            out.append(projected)
    return out


def all_sessions() -> List[LoweredStandardSession]:
    """All sessions with projected state (active/closed/expired)."""
    out: List[LoweredStandardSession] = []
    for f in _all_files():
        try:
            sess = LoweredStandardSession(**json.loads(f.read_text()))
        except Exception:
            continue
        out.append(_project_state(sess))
    return sorted(out, key=lambda s: s.started_at, reverse=True)


def is_active_for(*, actor: str, purpose: str) -> bool:
    """True iff an active session covers this actor + purpose."""
    if not actor or not purpose:
        return False
    for sess in active_sessions():
        if sess.actor == actor and purpose in sess.purpose_scope:
            return True
    return False


__all__ = [
    "CEILING_SECONDS",
    "LoweredStandardSession",
    "active_sessions",
    "all_sessions",
    "close_session",
    "is_active_for",
    "open_session",
]
