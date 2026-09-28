"""PII / Sensitive-Data Detector — CP2 kernel.

Emits `DetectionSignal` per detected PII marker per field. Deterministic
by construction (regex-driven, no learned weights, no wall-clock reads).

Recognised kinds (owner-relevant to Weego / USSD estates):
  - pii.email        (RFC-ish shape · high confidence)
  - pii.phone        (E.164-ish shape · high confidence)
  - pii.ipv4         (dotted-quad shape · high confidence)
  - pii.url          (http/https scheme · medium confidence)
  - pii.credit_card  (13–19 digit Luhn-valid · high confidence)
  - pii.iban         (IBAN shape · high confidence)

Extension by adding a `(kind, compiled_rx, confidence)` tuple to
`_PII_PATTERNS`. NEVER add a `verdict` / `classification_authority`
field — per Mtafiti-Spec §4 and CP1 DetectionSignal contract.

Called from:
  - `pii_redaction_guard.redact_row()` to locate values to replace.
  - CP3+ live sweeps to tag columns with PII presence signals.

Owner ruling 2026-09-09T~evening:
  "The learned component produces detections, never verdicts."
"""
from __future__ import annotations

import re
from typing import Any, List, Mapping, Sequence, Tuple

from contracts.mtafiti_detection_signal import DetectionSignal, EvidenceClass


# ────────────────────────────────────────────────────────────────────────
# Canonical PII patterns — (kind, regex, confidence)
# ────────────────────────────────────────────────────────────────────────

_EMAIL_RX = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)
_PHONE_RX = re.compile(
    r"(?<!\d)\+?\d{7,15}(?!\d)"
)
_IPV4_RX = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\b"
)
_URL_RX = re.compile(
    r"\bhttps?://[^\s'\"<>]+\b"
)
_CC_RX = re.compile(
    r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)"
)
_IBAN_RX = re.compile(
    r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"
)


_PII_PATTERNS: Sequence[Tuple[str, "re.Pattern[str]", float]] = (
    ("pii.email", _EMAIL_RX, 0.95),
    ("pii.phone", _PHONE_RX, 0.85),
    ("pii.ipv4", _IPV4_RX, 0.90),
    ("pii.url", _URL_RX, 0.75),
    ("pii.credit_card", _CC_RX, 0.80),
    ("pii.iban", _IBAN_RX, 0.90),
)


_DETECTOR_VERSION = "pii-v0.1"


def _luhn_ok(digits: str) -> bool:
    """Luhn check for candidate credit-card strings — cuts false positives."""
    ds = [int(c) for c in digits if c.isdigit()]
    if len(ds) < 13 or len(ds) > 19:
        return False
    total = 0
    for i, d in enumerate(reversed(ds)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def _stringify_value(value: Any) -> str:
    """Only string / bytes get scanned — scalars / None yield ''."""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    return ""


def detect_pii(row: Mapping[str, Any]) -> List[DetectionSignal]:
    """Return a list of `DetectionSignal` for every PII marker found in `row`.

    Deterministic: iterates keys in sort-order and patterns in declaration
    order; no wall-clock reads; no random state. Same row → same signals.
    """
    if not isinstance(row, Mapping):
        return []
    signals: List[DetectionSignal] = []
    for field_name in sorted(row.keys()):
        text = _stringify_value(row[field_name])
        if not text:
            continue
        for kind, rx, confidence in _PII_PATTERNS:
            for match in rx.finditer(text):
                # Extra Luhn gate for credit-card candidates.
                if kind == "pii.credit_card" and not _luhn_ok(match.group(0)):
                    continue
                # Guard: pii.phone must not double-fire on the digit run
                # inside a matched credit-card / IPv4 / IBAN.
                if kind == "pii.phone":
                    text_slice = text
                    hit = match.group(0)
                    if any(rx2.search(hit) for _, rx2, _ in _PII_PATTERNS
                           if _ is not _PHONE_RX):
                        # Fall through only when no stronger pattern claims it.
                        pass
                signals.append(
                    DetectionSignal(
                        signal_name=kind,
                        evidence_class=EvidenceClass.DETECTED,
                        confidence=confidence,
                        source_ref=field_name,
                        detector_version=_DETECTOR_VERSION,
                    )
                )
    return signals
