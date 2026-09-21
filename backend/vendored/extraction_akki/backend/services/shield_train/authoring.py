"""shield_train.authoring — masking-policy authoring surface (Doc 02 §A5.2).

Contract:
  * `add_entry(prev_policy, new_entry) -> new_policy` — pure function;
    returns a NEW dict with the entry appended to `ledger` and
    `schema_version` bumped by 1. prev is never mutated.
  * `add_drawer_entry(prev_policy, drawer_entry) -> new_policy` — same
    shape but appends to `clarification_drawer` (Ruling #5 shape).
  * `resolve_drawer_entry(prev_policy, question_id, resolution)
      -> new_policy` — closes an open drawer entry with a resolution
    dict (classification_authority + ruled_at_utc + ruling_text +
    evidence_record).

Every mutation returns a NEW policy dict (never in-place); the on-disk
`masking_policy.v0.json` is the seed. Later versions land as sibling
files `masking_policy.v1.json`, `v2.json`, … or the caller re-writes
`v0.json` with the incremented `schema_version` — that's a caller
choice, not the authoring module's responsibility.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any, Dict


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _clone(policy: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(policy)


def add_entry(prev_policy: Dict[str, Any],
              new_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Return a NEW policy with `new_entry` appended to `ledger` and
    `schema_version` incremented.

    `new_entry` MUST carry: table, column, class, action, rationale,
    ruling_ref, declassification_path.  `entered_at_utc` is auto-filled
    if absent.
    """
    new_policy = _clone(prev_policy)
    entry = dict(new_entry)
    entry.setdefault("entered_at_utc", _iso_now())
    new_policy["ledger"].append(entry)
    new_policy["schema_version"] = int(prev_policy.get("schema_version", 0)) + 1
    new_policy["authored_at_utc"] = _iso_now()
    return new_policy


def add_drawer_entry(prev_policy: Dict[str, Any],
                     drawer_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Return a NEW policy with `drawer_entry` appended to
    `clarification_drawer` (Ruling #5 shape) and `schema_version`
    incremented.

    Required drawer fields on input: `question_id`, `field`,
    `cautious_default_applied`. Auto-filled if absent: `opened_at_utc`,
    `state='open'`, `resolution=None`.
    """
    new_policy = _clone(prev_policy)
    entry = dict(drawer_entry)
    entry.setdefault("opened_at_utc", _iso_now())
    entry.setdefault("state", "open")
    entry.setdefault("resolution", None)
    new_policy["clarification_drawer"].append(entry)
    new_policy["schema_version"] = int(prev_policy.get("schema_version", 0)) + 1
    new_policy["authored_at_utc"] = _iso_now()
    return new_policy


def resolve_drawer_entry(prev_policy: Dict[str, Any],
                          question_id: str,
                          resolution: Dict[str, Any]) -> Dict[str, Any]:
    """Close an open drawer entry by `question_id`. `resolution` MUST
    carry: classification_authority, ruled_at_utc, ruling_text,
    evidence_record. Returns a NEW policy; raises KeyError if the
    question_id doesn't match an open drawer entry."""
    new_policy = _clone(prev_policy)
    for e in new_policy["clarification_drawer"]:
        if e.get("question_id") == question_id and e.get("state") == "open":
            e["state"] = "resolved"
            e["resolution"] = dict(resolution)
            new_policy["schema_version"] = int(prev_policy.get("schema_version", 0)) + 1
            new_policy["authored_at_utc"] = _iso_now()
            return new_policy
    raise KeyError(
        f"no open drawer entry with question_id={question_id!r}"
    )
