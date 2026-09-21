"""TTL enforcement for C.13 scoped keys.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "TTL enforcement".

Public surface: `is_expired(*, key_issued_at_iso, now_iso, ttl_seconds)
-> bool` returning True iff `now_iso >= key_issued_at_iso + ttl_seconds`
(inclusive at expiry boundary · fail-closed).

Refuses non-ISO-8601 input + negative TTL at boundary (raises
ValueError). Pure-data-in per M14-W4 precedent 2026-09-19 verbatim ("a
code path is a code path"). No wall-clock call (both timestamps are
input arguments · determinism preserved).

Canon 8 §W11 structural role separation: this module carries ONLY the
is_expired predicate. No persistence · no signing · no side effects.
"""
from __future__ import annotations

from datetime import datetime, timedelta


def _parse_iso(value: str, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"is_expired · {field_name} MUST be a non-empty ISO-8601 "
            f"string · got {type(value).__name__}={value!r}"
        )
    # Normalize Z suffix to +00:00 for fromisoformat
    normalised = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalised)
    except ValueError as exc:
        raise ValueError(
            f"is_expired · {field_name} MUST parse as ISO-8601 · "
            f"got {value!r} · fromisoformat error: {exc}"
        ) from exc
    return parsed


def is_expired(
    *,
    key_issued_at_iso: str,
    now_iso: str,
    ttl_seconds: int,
) -> bool:
    """Return True iff `now_iso >= key_issued_at_iso + ttl_seconds`.

    Boundary discipline:
      - Inclusive at expiry (`now == issued + ttl` returns True).
      - Both timestamps MUST be ISO-8601 parseable.
      - `ttl_seconds` MUST be non-negative.
    """
    if not isinstance(ttl_seconds, int) or isinstance(ttl_seconds, bool):
        raise ValueError(
            f"is_expired · ttl_seconds MUST be an int · got "
            f"{type(ttl_seconds).__name__}={ttl_seconds!r}"
        )
    if ttl_seconds < 0:
        raise ValueError(
            f"is_expired · ttl_seconds MUST be non-negative · "
            f"got {ttl_seconds}"
        )
    issued = _parse_iso(key_issued_at_iso, "key_issued_at_iso")
    now = _parse_iso(now_iso, "now_iso")
    expiry = issued + timedelta(seconds=ttl_seconds)
    return now >= expiry
