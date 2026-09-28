"""PII Redaction Guard — CP2 kernel.

Deterministic, salted PII redaction for anything mtafiti persists.

Contract:
  `redact_row(row) -> row_redacted`   — replaces detected-PII values with
                                         `<REDACTED:pii.<kind>:<hash16>>`
                                         deterministic tokens.
  `assert_no_raw_pii(payload)`         — raises `RawPiiLeakForbidden` when
                                         any canonical PII pattern appears
                                         anywhere in the payload's string
                                         values (recursively).

Owner ruling this session:
  "Persist measurement/detection OUTPUT (classifications, counts, strata,
  signatures, minimal REDACTED samples) — NOT raw PII dumps. Redact/hash
  PII in any persisted sample."

Determinism: hash = sha256(SALT || '|' || kind || '|' || value)[:16].
Salt is `gpu_discovery_constants.MTAFITI_PII_HASH_SALT`. Same input →
same token; idempotent by construction (a token has no PII shape, so
`detect_pii(redacted_row)` returns empty and `redact_row` is a no-op).
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, Mapping

from services.mtafiti.detectors.pii_detector import (
    _PII_PATTERNS,
    _luhn_ok,
    _stringify_value,
    detect_pii,
)
from services.mtafiti.gpu_discovery_constants import MTAFITI_PII_HASH_SALT


class RawPiiLeakForbidden(Exception):
    """Raised by `assert_no_raw_pii` when raw PII appears in a payload."""


def _hash16(kind: str, value: str) -> str:
    return hashlib.sha256(
        (MTAFITI_PII_HASH_SALT + "|" + kind + "|" + value).encode()
    ).hexdigest()[:16]


def _redact_text(text: str) -> str:
    """Redact every PII marker inside a string, preserving surrounding chars."""
    out = text
    # Iterate patterns in the same order as pii_detector to guarantee
    # deterministic redaction of overlapping matches.
    for kind, rx, _confidence in _PII_PATTERNS:
        def _repl(match: "re.Match[str]", _kind: str = kind) -> str:
            hit = match.group(0)
            if _kind == "pii.credit_card" and not _luhn_ok(hit):
                return hit  # not a valid CC → leave untouched
            return f"<REDACTED:{_kind}:{_hash16(_kind, hit)}>"
        out = rx.sub(_repl, out)
    return out


def redact_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a shallow-copy row where every detected PII string value
    has been replaced with a deterministic redaction token.

    Non-string values pass through unchanged. Keys are preserved.
    Idempotent: `redact_row(redact_row(x)) == redact_row(x)`.
    """
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if isinstance(v, str):
            out[k] = _redact_text(v)
        elif isinstance(v, bytes):
            out[k] = _redact_text(_stringify_value(v))
        else:
            out[k] = v
    return out


def _payload_string_values(payload: Any):
    """Yield every string value found anywhere in a nested payload."""
    if isinstance(payload, str):
        yield payload
    elif isinstance(payload, bytes):
        yield _stringify_value(payload)
    elif isinstance(payload, Mapping):
        for v in payload.values():
            yield from _payload_string_values(v)
    elif isinstance(payload, (list, tuple, set, frozenset)):
        for v in payload:
            yield from _payload_string_values(v)
    # scalars: ignored


_REDACTED_TOKEN_RX = re.compile(r"<REDACTED:pii\.[a-z0-9_]+:[0-9a-f]{16}>")


def _text_has_raw_pii(text: str) -> bool:
    """Detect any canonical PII pattern in `text`, IGNORING already-redacted
    tokens (which have PII-free shape by construction)."""
    if not text:
        return False
    # Strip redaction tokens before scanning — the token itself is safe.
    scrubbed = _REDACTED_TOKEN_RX.sub(" ", text)
    for kind, rx, _confidence in _PII_PATTERNS:
        for match in rx.finditer(scrubbed):
            if kind == "pii.credit_card" and not _luhn_ok(match.group(0)):
                continue
            return True
    return False


def assert_no_raw_pii(payload: Any) -> None:
    """Raise `RawPiiLeakForbidden` if `payload` carries any raw PII.

    Persistence layers (Registry writes, phase0 sample banks, WPW drafts)
    call this before writing. It's a defence-in-depth check — the primary
    line is that samples are always fed through `redact_row` first.
    """
    for text in _payload_string_values(payload):
        if _text_has_raw_pii(text):
            raise RawPiiLeakForbidden(
                "raw PII detected in payload; call redact_row() before persisting."
            )
