"""services.watch.persistence · Doc 8 · verdict + action write-once JSON.

§Line 39 verbatim: 'The Watch maintains no account of anything but its
own events, and its records are classes in the platform's one record
per the matrix of Document 9. The deception the mirage shows an
attacker is a rendering. The record never lies inward.'

Per-file JSON records under WATCH_VERDICTS_DIR / WATCH_ACTIONS_DIR so
the shared state rollup (services.watch.router._load_kind) picks
them up automatically. Write-once by {verdict_id | action_id}.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.watch_action_v0 import WatchActionV0
from services.watch.macho import MachoVerdict


class WriteOnceViolation(RuntimeError):
    pass


_DEFAULT_VERDICTS_DIR = "/app/assessment_workspace/phase0/watch_verdicts"
_DEFAULT_ACTIONS_DIR = "/app/assessment_workspace/phase0/watch_actions"


def _verdicts_dir() -> Path:
    d = Path(os.environ.get("WATCH_VERDICTS_DIR", _DEFAULT_VERDICTS_DIR))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _actions_dir() -> Path:
    d = Path(os.environ.get("WATCH_ACTIONS_DIR", _DEFAULT_ACTIONS_DIR))
    d.mkdir(parents=True, exist_ok=True)
    return d


def append_verdict(v: MachoVerdict) -> MachoVerdict:
    """Write-once persistence of a MachoVerdict (§Line 39)."""
    if get_verdict(v.verdict_id) is not None:
        raise WriteOnceViolation(f"verdict_id {v.verdict_id!r} already on record")
    path = _verdicts_dir() / f"{v.verdict_id}.json"
    path.write_text(v.model_dump_json(indent=2), encoding="utf-8")
    return v


def read_verdicts() -> List[MachoVerdict]:
    d = _verdicts_dir()
    if not d.is_dir():
        return []
    out: List[MachoVerdict] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # Skip legacy WatchVerdictRow_v0 shape (has 'at_iso' / 'sensor')
        # so both stores can co-exist under WATCH_VERDICTS_DIR/. Legacy
        # rows continue to be read by macho.load_verdicts.
        if "verdict_class" not in body:
            continue
        try:
            out.append(MachoVerdict(**body))
        except (ValueError, TypeError):
            continue
    return out


def get_verdict(verdict_id: str) -> Optional[MachoVerdict]:
    for v in read_verdicts():
        if v.verdict_id == verdict_id:
            return v
    return None


def append_action(a: WatchActionV0) -> WatchActionV0:
    """Write-once persistence of a WatchActionV0 (§Line 32.5 · atomic
    act-and-attest)."""
    if get_action(a.action_id) is not None:
        raise WriteOnceViolation(f"action_id {a.action_id!r} already on record")
    path = _actions_dir() / f"{a.action_id}.json"
    path.write_text(a.model_dump_json(indent=2), encoding="utf-8")
    return a


def read_actions() -> List[WatchActionV0]:
    d = _actions_dir()
    if not d.is_dir():
        return []
    out: List[WatchActionV0] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # Skip legacy WatchActionRecord_v0 shape (has 'at_iso' / 'responder')
        # so both stores can co-exist. Legacy rows continue to be read by
        # mkono.load_actions.
        if "action_class" not in body or "reversible" not in body:
            continue
        try:
            out.append(WatchActionV0(**body))
        except (ValueError, TypeError):
            continue
    return out


def get_action(action_id: str) -> Optional[WatchActionV0]:
    for a in read_actions():
        if a.action_id == action_id:
            return a
    return None


def is_empty() -> bool:
    return not read_verdicts() and not read_actions()
