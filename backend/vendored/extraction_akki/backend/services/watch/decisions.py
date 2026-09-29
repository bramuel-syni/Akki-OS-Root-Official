"""The reserved human set (Canon 8 §13 Decisions · §10 de-marking · §15 disagreement).

Every item is an append-only event stream per tenant. Removing protection is never autonomous:
`demark_release` and `requirement_ratification` execute only when TWO DISTINCT estate operators
approve (dual control). Acknowledging an item changes nothing but the acknowledgement record —
active protection stays until its own release authority acts. Items rank by blast radius."""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

BLAST = {"demark_release": 3, "requirement_ratification": 2, "redeclaration": 1}
REQUIRED_APPROVALS = 2


def _dir():
    return Path(os.environ.get("WATCH_DECISIONS_DIR", "/app/assessment_workspace/phase0/watch_decisions"))


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def _events(tenant_id):
    path = _dir() / f"{tenant_id}.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _append(tenant_id, row):
    _dir().mkdir(parents=True, exist_ok=True)
    with (_dir() / f"{tenant_id}.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def fold(tenant_id):
    items = {}
    for ev in _events(tenant_id):
        if ev["kind"] == "opened":
            items[ev["decision_id"]] = {**ev, "approvals": [], "acknowledged_by": [], "declined": None, "executed": None, "state": "open"}
            continue
        item = items.get(ev["decision_id"])
        if item is None:
            continue
        if ev["kind"] == "approval":
            item["approvals"].append(ev)
        elif ev["kind"] == "acknowledged":
            item["acknowledged_by"].append(ev["by"])
        elif ev["kind"] == "declined":
            item["declined"] = ev
            item["state"] = "declined"
        elif ev["kind"] == "executed":
            item["executed"] = ev
            item["state"] = "executed"
    for item in items.values():
        item["approvers"] = sorted({a["by"] for a in item["approvals"]})
        item["approvals_needed"] = REQUIRED_APPROVALS
        item["blast"] = BLAST.get(item["klass"], 0)
    return items


def open_decision(tenant_id, klass, subject_ref, refs, opened_by, title, now=None):
    """Idempotent per (class, subject) while open: the panel never shows the same case twice."""
    for item in fold(tenant_id).values():
        if item["state"] == "open" and item["klass"] == klass and item["subject_ref"] == subject_ref:
            return item
    now = now or datetime.now(timezone.utc)
    row = {"kind": "opened", "decision_id": f"wd_{uuid.uuid4().hex[:12]}", "klass": klass, "subject_ref": subject_ref,
           "refs": refs, "opened_by": opened_by, "opened_at": _iso(now), "title": title, "tenant_id": tenant_id}
    _append(tenant_id, row)
    return fold(tenant_id)[row["decision_id"]]


def act(tenant_id, decision_id, principal_id, action, note, now=None):
    now = now or datetime.now(timezone.utc)
    item = fold(tenant_id).get(decision_id)
    if item is None:
        raise LookupError("No open Watch decision with that reference exists in your tenant.")
    if action == "acknowledge":
        _append(tenant_id, {"kind": "acknowledged", "decision_id": decision_id, "by": principal_id, "at": _iso(now)})
        return {**fold(tenant_id)[decision_id], "protection_changed": False}
    if item["state"] != "open":
        raise ValueError(f"This decision is already {item['state']}; a closed item is corrected by a new item, never reopened.")
    if not (note or "").strip():
        raise ValueError("One line is required: what you decided, and why.")
    if action == "decline":
        _append(tenant_id, {"kind": "declined", "decision_id": decision_id, "by": principal_id, "note": note, "at": _iso(now)})
        return {**fold(tenant_id)[decision_id], "protection_changed": False}
    if action != "approve":
        raise ValueError("Decision actions are approve, decline or acknowledge.")
    if principal_id in item["approvers"]:
        raise ValueError("Dual control: the second approval must come from a different estate operator.")
    _append(tenant_id, {"kind": "approval", "decision_id": decision_id, "by": principal_id, "note": note, "at": _iso(now)})
    item = fold(tenant_id)[decision_id]
    if len(item["approvers"]) < REQUIRED_APPROVALS:
        return {**item, "protection_changed": False}
    effect = _execute(tenant_id, item, now)
    _append(tenant_id, {"kind": "executed", "decision_id": decision_id, "by": item["approvers"], "at": _iso(now), "effect": effect})
    return {**fold(tenant_id)[decision_id], "protection_changed": effect.get("protection_changed", False)}


def _execute(tenant_id, item, now):
    from services.watch import commission_gate, learning_loop
    if item["klass"] == "demark_release":
        return commission_gate.release_sever(tenant_id, item["subject_ref"], item["refs"], item["approvers"], now)
    if item["klass"] == "requirement_ratification":
        return learning_loop.ratify(tenant_id, item["refs"], item["approvers"], now)
    return {"protection_changed": False, "note": "recorded only"}
