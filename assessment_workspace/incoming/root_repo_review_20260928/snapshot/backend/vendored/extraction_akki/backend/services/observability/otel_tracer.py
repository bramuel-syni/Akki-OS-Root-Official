"""OTel-shaped tracing wrapper · M13-W3 · §6.4 pre-ruling 4 verbatim.

**Additive-only per SO §3.8:** this module exposes a `traced_call`
context-manager surface. It does NOT edit any sealed module. Actual
integration with the chokepoint / ledger_writer / watch.input_seat /
watch.verdict_interface call surfaces attaches at each caller's
thin-adapter layer under `services/enforce/*` at a subsequent CP.

**Closed alphabet (Canon 8 §Line 31 pattern applied to OTel):**
`TELEMETRY_ATTR_ALPHABET` enumerates the ONLY attribute names that may
appear on a span emitted through this wrapper. Any other name is
refused at span-open time via `TelemetryAttrOutOfAlphabet`. This
mirrors the closed sever-certainty registry doctrine (Canon 8 §Line
31) transplanted to observability.

**§4.1 §E discipline extended to telemetry:** attribute values that
match credential-shaped patterns (Bearer/JWT-like/password=... form)
are refused at span-open time via `TelemetryValueRefused`.

**Design note (post-wire-in):** at wire-in time the returned context
value will be a real OTel `Span`. Pre-wire-in the wrapper yields a
lightweight `_SpanHandle` dict-like shim so tests can validate the
surface without a live OTel collector.
"""
from __future__ import annotations

import re
from contextlib import contextmanager
from typing import Any, Iterator, Mapping


#: Card MUST-DO 3 verbatim (closed set · SO §3.10-α tuple[str] discipline).
#: Any attribute name outside this alphabet is refused at span-open.
TELEMETRY_ATTR_ALPHABET: tuple[str, ...] = (
    "tenant_id",
    "run_id",
    "event_type",
    "decision",
    "reason_code",
    "resource_type",
    "resource_id",
    "task_id",
    "actor_id",
    "actor_type",
)


class TelemetryAttrOutOfAlphabet(Exception):
    """Raised when a span attribute name is not in
    `TELEMETRY_ATTR_ALPHABET`. Canon 8 §Line 31 pattern applied to
    OTel."""


class TelemetryValueRefused(Exception):
    """Raised when a span attribute value matches a credential-shaped
    pattern. §4.1 §E discipline extended to telemetry."""


# Credential-shape patterns (deliberately narrow · matches obvious
# credential leakage, not adversarial evasion). Same regime as
# secret_hygiene sibling module.
_CREDENTIAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Bearer tokens
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    # JWT-looking header sequences
    re.compile(r"\beyJ[A-Za-z0-9._-]{16,}"),
    # password=... / passwd=... / secret=... / token=... / apikey=... forms
    re.compile(
        r"\b(password|passwd|secret|token|api[_-]?key|apikey|auth)\s*=\s*\S+",
        re.IGNORECASE,
    ),
)


def _value_looks_like_credential(value: Any) -> str | None:
    """Return the matched pattern string if `value` looks like a
    credential; None otherwise. Values that are not strings are
    considered safe (structured attributes are not string-shaped)."""
    if not isinstance(value, str):
        return None
    for pattern in _CREDENTIAL_PATTERNS:
        m = pattern.search(value)
        if m:
            return m.group(0)
    return None


class _SpanHandle(dict[str, Any]):
    """Pre-wire-in span shim · behaves as a dict of `{attr: value}`
    plus an `attributes` view alias. Callers may treat it as either.
    Post-wire-in this is replaced by a real OTel `Span`."""

    @property
    def attributes(self) -> Mapping[str, Any]:
        return self


@contextmanager
def traced_call(
    span_name: str, *, attributes: Mapping[str, Any] | None = None
) -> Iterator[_SpanHandle]:
    """Open a traced span with the given `span_name` and `attributes`.

    Refuses:
    - any attribute name outside `TELEMETRY_ATTR_ALPHABET`
      (raises `TelemetryAttrOutOfAlphabet`);
    - any attribute value matching a credential-shaped pattern
      (raises `TelemetryValueRefused`).

    Yields a `_SpanHandle` (pre-wire-in shim). Post-wire-in this will
    yield a real OTel `Span`.
    """
    if not isinstance(span_name, str) or not span_name:
        raise ValueError(
            f"span_name must be a non-empty string; got {span_name!r}"
        )
    attributes = dict(attributes or {})

    # 1. Refuse out-of-alphabet attribute names.
    for name in attributes:
        if name not in TELEMETRY_ATTR_ALPHABET:
            raise TelemetryAttrOutOfAlphabet(
                f"attribute name {name!r} is not in TELEMETRY_ATTR_ALPHABET "
                f"(closed set per Canon 8 §Line 31 · known attrs: "
                f"{TELEMETRY_ATTR_ALPHABET})"
            )

    # 2. Refuse credential-shaped values.
    for name, value in attributes.items():
        matched = _value_looks_like_credential(value)
        if matched is not None:
            raise TelemetryValueRefused(
                f"attribute {name!r} value looks like credential material "
                f"(matched pattern {matched!r}) — §4.1 §E discipline "
                f"bans credential material in telemetry"
            )

    handle = _SpanHandle(attributes)
    try:
        yield handle
    finally:
        # Pre-wire-in: nothing to flush. Post-wire-in: this is where the
        # OTel span exits its context.
        pass
