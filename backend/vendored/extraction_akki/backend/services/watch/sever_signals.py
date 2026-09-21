"""services.watch.sever_signals · Doc 8 §Line 31 verbatim ·
write-once JSONL persistence for the closed six-signal registry.

'The closed sever-certainty registry — canary touch, attestation
failure, mark hit, witness-write attempt, floor violation, mirage
incrimination — is the whole of what may unlock the Watch's maximum
autonomous force. ... The certainty computation is a function with
no parameter through which a detector's confidence can enter —
Solva's own assertion boundary, transplanted: the signature is the
guard.'                                              — Canon 8 §Line 31

This module holds the on-disk store for signals of the closed six
kinds. Membership in the six-kind grammar is enforced by
`SeverCertaintySignalV0.signal_kind` (Literal). This module ONLY
persists and reads back — it never widens the grammar.

Records: WATCH_SEVER_SIGNALS_DIR/signals.jsonl · append-only ·
write-once by signal_id.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.sever_certainty_signal_v0 import SeverCertaintySignalV0


class WriteOnceViolation(RuntimeError):
    pass


_DEFAULT_DIR = "/app/assessment_workspace/phase0/watch_sever_signals"


def _dir() -> Path:
    d = Path(os.environ.get("WATCH_SEVER_SIGNALS_DIR", _DEFAULT_DIR))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _file() -> Path:
    return _dir() / "signals.jsonl"


def append_sever_signal(s: SeverCertaintySignalV0) -> SeverCertaintySignalV0:
    """Write-once persistence of a sever-certainty signal (§Line 31
    closed six-registry). Duplicate signal_id raises WriteOnceViolation."""
    if get_sever_signal(s.signal_id) is not None:
        raise WriteOnceViolation(
            f"sever_certainty_signal_id {s.signal_id!r} already on record."
        )
    payload = s.model_dump()
    with _file().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload))
        fh.write("\n")
    return s


def read_sever_signals() -> List[SeverCertaintySignalV0]:
    f = _file()
    if not f.exists():
        return []
    out: List[SeverCertaintySignalV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            out.append(SeverCertaintySignalV0(**row))
        except (ValueError, json.JSONDecodeError, TypeError):
            # Silent skip; the store is append-only and best-effort
            # readable. Corruption of a single line does not gate
            # the rest of the registry.
            continue
    return out


def get_sever_signal(signal_id: str) -> Optional[SeverCertaintySignalV0]:
    for s in read_sever_signals():
        if s.signal_id == signal_id:
            return s
    return None
