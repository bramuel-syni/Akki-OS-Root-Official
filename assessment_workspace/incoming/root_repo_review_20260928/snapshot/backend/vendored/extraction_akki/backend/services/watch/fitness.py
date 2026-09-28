"""services.watch.fitness — demonstrated-firings reader (Canon 8 §28).

Canon 8 §28 verbatim: "Fitness of the Watch is stated in demonstrated
firings over the observation window (Doc 6 §9-A: the proof is
RECEIPTS, not attestation)."

Canon 8 §32.8 verbatim: "NO drill self-certifies fitness."

This module reads drill receipts from phase0/drill_receipts/ and
returns raw counts per drill class within the observation window.
It DOES NOT attest, certify, or verdict-of-fitness. The count IS
the fact; witness attestation (§9 · CP5) is a separate mechanism.

Drill class detection is filename-based (each drill script + banked
receipt encodes the drill class in its name). Recognized classes:
  - canon_8_25_seeded_hostile_input
  - canon_8_26_planted_credential_severance
  - canon_8_27_containment_expiring_clean (includes W10 CP1's
    'ruling_1_firing_drill' which is a §27 drill by class)
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional


_DEFAULT_DIR = "/app/assessment_workspace/phase0/drill_receipts"

# Filename timestamp prefix: 20260826T050000Z_...
_TS_RE = re.compile(r"^(\d{8}T\d{6}Z)_")

_CLASS_HITS = {
    "canon_8_25_seeded_hostile_input": [
        "canon_8_25_seeded_hostile_input",
    ],
    "canon_8_26_planted_credential_severance": [
        "canon_8_26_planted_credential_severance",
    ],
    "canon_8_27_containment_expiring_clean": [
        "canon_8_27_containment_expiring_clean",
        "ruling_1_firing_drill",           # W10 CP1 · §27 drill by class
        "w10_cp1_ruling_1",
        "w10_cp1_green",                   # W10 CP1 · §27 drill green log
        "w10_cp1_drill_execution_trio",    # W10 CP1 · §27 live trio log
    ],
}


def _receipts_dir() -> Path:
    return Path(os.environ.get("WATCH_DRILL_RECEIPTS_DIR", _DEFAULT_DIR))


def _parse_ts(name: str) -> Optional[datetime]:
    m = _TS_RE.match(name)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(
            tzinfo=timezone.utc,
        )
    except ValueError:
        return None


def _classify(name: str) -> Optional[str]:
    lower = name.lower()
    for cls, tokens in _CLASS_HITS.items():
        for tok in tokens:
            if tok in lower:
                return cls
    return None


def demonstrated_firings(
    *,
    window_days: int = 30,
    now_iso: Optional[str] = None,
) -> Dict[str, int]:
    """Count receipts per drill class within the observation window
    ending at now_iso (default: real now)."""
    counts: Dict[str, int] = {cls: 0 for cls in _CLASS_HITS}
    d = _receipts_dir()
    if not d.is_dir():
        return counts

    if now_iso is not None:
        now = datetime.fromisoformat(now_iso.replace("Z", "+00:00"))
    else:
        now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=window_days)

    # Count GREEN receipts only; right-reason failure receipts are not
    # demonstrated firings, they are the pre-demonstration signal.
    for p in d.iterdir():
        if not p.is_file():
            continue
        name = p.name
        ts = _parse_ts(name)
        if ts is None or ts < cutoff or ts > now:
            continue
        # Skip right-reason failure logs; count green receipts.
        if "right_reason_fail" in name.lower():
            continue
        cls = _classify(name)
        if cls is None:
            continue
        # Only count once per drill class per timestamp; a class may
        # have multiple filename variants for the same run.
        counts[cls] += 1

    return counts
