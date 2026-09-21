"""services.approvals.rules_update_lifecycle — Rules Updates ceremony
remainder (countdown → apply → re-check) records R/W.

Doc 15 §17 discipline (verbatim): the five states are propose ·
counter-sign · countdown · apply · re-check. This module implements
the last three. Service-time invariants:

  - start_countdown: decision must exist AND verdict == 'approved'.
  - apply_rules_update: countdown must exist AND now ≥ countdown_ends_at.
  - recheck_rules_update: applied record must exist.
  - Each transition is one-per-upstream (idempotency).

Records: phase0/rules_update_lifecycle/{countdowns,applies,rechecks}/.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.rules_update_lifecycle import (
    CountdownStarted_v0,
    RulesUpdateApplied_v0,
    RulesUpdateReChecked_v0,
)
from services.approvals.approvals import load_decisions


_DEFAULT_DIR = "/app/assessment_workspace/phase0/rules_update_lifecycle"


def _dir() -> Path:
    return Path(os.environ.get("RULES_UPDATE_LIFECYCLE_DIR", _DEFAULT_DIR))


def _countdowns_dir() -> Path:
    return _dir() / "countdowns"


def _applies_dir() -> Path:
    return _dir() / "applies"


def _rechecks_dir() -> Path:
    return _dir() / "rechecks"


def load_countdowns() -> List[CountdownStarted_v0]:
    d = _countdowns_dir()
    if not d.is_dir():
        return []
    return sorted(
        (CountdownStarted_v0(**json.loads(p.read_text()))
         for p in d.glob("cds_*.json")),
        key=lambda c: c.countdown_id,
    )


def load_applies() -> List[RulesUpdateApplied_v0]:
    d = _applies_dir()
    if not d.is_dir():
        return []
    return sorted(
        (RulesUpdateApplied_v0(**json.loads(p.read_text()))
         for p in d.glob("app_*.json")),
        key=lambda a: a.applied_id,
    )


def load_rechecks() -> List[RulesUpdateReChecked_v0]:
    d = _rechecks_dir()
    if not d.is_dir():
        return []
    return sorted(
        (RulesUpdateReChecked_v0(**json.loads(p.read_text()))
         for p in d.glob("rec_*.json")),
        key=lambda r: r.recheck_id,
    )


def _find_countdown_for_decision(decision_id: str) -> Optional[CountdownStarted_v0]:
    for c in load_countdowns():
        if c.decision_id == decision_id:
            return c
    return None


def _find_countdown(countdown_id: str) -> Optional[CountdownStarted_v0]:
    for c in load_countdowns():
        if c.countdown_id == countdown_id:
            return c
    return None


def _find_apply_for_countdown(countdown_id: str) -> Optional[RulesUpdateApplied_v0]:
    for a in load_applies():
        if a.countdown_id == countdown_id:
            return a
    return None


def _find_apply(applied_id: str) -> Optional[RulesUpdateApplied_v0]:
    for a in load_applies():
        if a.applied_id == applied_id:
            return a
    return None


def _find_recheck_for_apply(applied_id: str) -> Optional[RulesUpdateReChecked_v0]:
    for r in load_rechecks():
        if r.applied_id == applied_id:
            return r
    return None


def start_countdown(payload: Dict[str, Any]) -> CountdownStarted_v0:
    """Begin a countdown on an APPROVED decision. Refuses:
      - decision not on record
      - verdict != 'approved'
      - countdown already started for this decision (idempotency)
    """
    c = CountdownStarted_v0(**payload)
    decision = None
    for d in load_decisions():
        if d.decision_id == c.decision_id:
            decision = d
            break
    if decision is None:
        raise ValueError(
            f"decision {c.decision_id!r} not on record. Register + "
            f"decide the approval before starting the countdown."
        )
    if decision.verdict != "approved":
        raise ValueError(
            f"decision {c.decision_id!r} verdict is {decision.verdict!r}; "
            f"countdown only runs on 'approved' decisions (Doc 15 §17)."
        )
    if _find_countdown_for_decision(c.decision_id) is not None:
        raise ValueError(
            f"decision {c.decision_id!r} already has a countdown on record. "
            f"Second countdown attempts are load-bearing conflicts."
        )
    d = _countdowns_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{c.countdown_id}.json").write_text(
        json.dumps(c.model_dump(), indent=2, ensure_ascii=False)
    )
    return c


def apply_rules_update(payload: Dict[str, Any],
                       now_iso: str) -> RulesUpdateApplied_v0:
    """Record an apply. Refuses if now_iso < countdown_ends_at, if the
    countdown is not on record, or if this countdown already has an apply.

    `now_iso` is injected so tests can drive the clock; production
    callers pass datetime.now(tz=UTC).isoformat().
    """
    a = RulesUpdateApplied_v0(**payload)
    countdown = _find_countdown(a.countdown_id)
    if countdown is None:
        raise ValueError(
            f"countdown {a.countdown_id!r} not on record. Start the "
            f"countdown before applying."
        )
    if now_iso < countdown.countdown_ends_at:
        raise ValueError(
            f"countdown {a.countdown_id!r} has not elapsed (now={now_iso!r}, "
            f"ends_at={countdown.countdown_ends_at!r}). Doc 15 §17: apply "
            f"must wait until countdown_ends_at."
        )
    if _find_apply_for_countdown(a.countdown_id) is not None:
        raise ValueError(
            f"countdown {a.countdown_id!r} already has an apply on record. "
            f"Second apply attempts are load-bearing conflicts."
        )
    d = _applies_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{a.applied_id}.json").write_text(
        json.dumps(a.model_dump(), indent=2, ensure_ascii=False)
    )
    return a


def recheck_rules_update(payload: Dict[str, Any]) -> RulesUpdateReChecked_v0:
    """Record a re-check on an applied change. Refuses if apply not on
    record, or if this apply already has a re-check."""
    r = RulesUpdateReChecked_v0(**payload)
    if _find_apply(r.applied_id) is None:
        raise ValueError(
            f"apply {r.applied_id!r} not on record. Apply the rules "
            f"update before re-checking."
        )
    if _find_recheck_for_apply(r.applied_id) is not None:
        raise ValueError(
            f"apply {r.applied_id!r} already has a re-check on record. "
            f"Second re-check attempts are load-bearing conflicts."
        )
    d = _rechecks_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{r.recheck_id}.json").write_text(
        json.dumps(r.model_dump(), indent=2, ensure_ascii=False)
    )
    return r
