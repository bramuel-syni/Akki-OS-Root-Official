"""services.connect.draft_store · in-memory Connect wizard draft persistence.

Owner directive 2026-08-26 (Wave A · R2 verbatim):
    "confirm must reference server-side draft state, not a captured null"

Custody contract (updated for R2):
    * Drafts live in process memory only. Never persisted to disk. Never
      logged. Never included verbatim in any response body except at the
      confirm handler's own outbound call to the pipeline.
    * Drafts expire after TTL_SECONDS (default 900 = 15 minutes).
    * On confirm the draft is CONSUMED (deleted) — replay-safe.
    * Passwords and AWS secrets are attributes on the draft object, kept in
      memory only, cleared on consume.

The store is a single process-scoped singleton, obtained via `get_store()`.
Tests may construct their own DraftStore(ttl_seconds=...) directly.
"""

from __future__ import annotations

import secrets
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


DEFAULT_TTL_SECONDS = 900  # 15 minutes


@dataclass
class Draft:
    draft_id: str
    kind: str
    fields: Dict[str, Any]
    password: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    api_key: Optional[str] = None
    created_at: float = field(default_factory=time.monotonic)


class DraftStore:
    def __init__(self, ttl_seconds: int = DEFAULT_TTL_SECONDS):
        self._ttl = ttl_seconds
        self._store: Dict[str, Draft] = {}
        self._lock = threading.Lock()

    def _now(self) -> float:
        return time.monotonic()

    def _expired(self, d: Draft) -> bool:
        return (self._now() - d.created_at) >= self._ttl

    def put(
        self,
        kind: str,
        fields: Dict[str, Any],
        *,
        password: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> str:
        """Create a new draft and return its opaque id."""
        draft_id = secrets.token_urlsafe(16)
        with self._lock:
            self._store[draft_id] = Draft(
                draft_id=draft_id,
                kind=kind,
                fields=dict(fields),
                password=password,
                aws_secret_access_key=aws_secret_access_key,
                api_key=api_key,
            )
        return draft_id

    def get(self, draft_id: str) -> Optional[Draft]:
        """Return the Draft or None if missing/expired. Sweeps expired
        entries opportunistically."""
        with self._lock:
            d = self._store.get(draft_id)
            if d is None:
                return None
            if self._expired(d):
                del self._store[draft_id]
                return None
            return d

    def patch_field(self, draft_id: str, field_name: str, value: str) -> bool:
        """Update a non-secret field on an existing draft. Returns True
        on success, False if the draft is missing/expired."""
        with self._lock:
            d = self._store.get(draft_id)
            if d is None or self._expired(d):
                return False
            d.fields[field_name] = value
            return True

    def consume(self, draft_id: str) -> Optional[Draft]:
        """Return the draft and delete it — replay-safe."""
        with self._lock:
            d = self._store.pop(draft_id, None)
            if d is None or self._expired(d):
                return None
            return d

    def sweep(self) -> int:
        """Remove all expired drafts; return count swept."""
        with self._lock:
            expired = [k for k, v in self._store.items() if self._expired(v)]
            for k in expired:
                del self._store[k]
            return len(expired)

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)


# ---- Process-scoped singleton ----

_default_store: Optional[DraftStore] = None


def get_store() -> DraftStore:
    global _default_store
    if _default_store is None:
        _default_store = DraftStore()
    return _default_store
