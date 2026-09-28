"""services.governance.router — /api/governance/state (W10 CP8).

Read-only rollup of governance surface state — spans approvals fabric
(Rules Updates + Spend Requests + Generic + Reserved Decisions) + Rules
Updates lifecycle (countdowns / applies / rechecks) drawn from on-disk
records. Every entry cites its `source_path` (REFERENCE-NOT-COPY ·
Design Law A8).

Sources (env-overridable per test seam):
  * APPROVAL_RECORDS_DIR    → phase0/approval_records/{requests,decisions}/
  * RULES_UPDATE_LIFECYCLE_DIR → phase0/rules_update_lifecycle/{...}/

Body shape:
  {approvals, rules_updates, reserved_decisions}: each {count, entries}
  entries: [{record_id, source_path, ...short summary fields...}]
  sources: {approvals: <path>, rules_updates: <path>, reserved_decisions: <path>}
  reference_note: "REFERENCE-NOT-COPY ..."
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter


router = APIRouter()

_DEFAULT_APPROVALS = "/app/assessment_workspace/phase0/approval_records"
_DEFAULT_RULES_UPDATE = "/app/assessment_workspace/phase0/rules_update_lifecycle"

# Fields that MUST NOT appear in any returned entry (Owner Order
# 2026-08-25 §4 · raw signing material / secrets never in surface).
_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
}


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v for k, v in d.items()
        if k not in _BANNED_FIELDS and not k.endswith("_raw")
    }


def _load_dir(d: Path, prefixes: List[str]) -> List[Dict[str, Any]]:
    if not d.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        if prefixes and not any(p.stem.startswith(pre) for pre in prefixes):
            continue
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(body, dict):
            continue
        out.append({**_sanitize(body), "source_path": str(p)})
    return out


def _approvals_dir() -> Path:
    return Path(os.environ.get("APPROVAL_RECORDS_DIR", _DEFAULT_APPROVALS))


def _rules_update_dir() -> Path:
    return Path(os.environ.get("RULES_UPDATE_LIFECYCLE_DIR",
                               _DEFAULT_RULES_UPDATE))


@router.get("/api/governance/state")
async def get_governance_state() -> Dict[str, Any]:
    ap = _approvals_dir()
    ru = _rules_update_dir()
    requests_dir = ap / "requests"
    decisions_dir = ap / "decisions"

    requests = _load_dir(requests_dir, ["req_"])
    decisions = _load_dir(decisions_dir, ["dc_", "d_"])
    reserved = [
        {"record_id": r.get("request_id"), **r}
        for r in requests
        if r.get("reserved_decision_kind") is not None
    ]
    approvals_entries = [
        {"record_id": r.get("request_id"), **r}
        for r in requests
    ] + [
        {"record_id": d.get("decision_id") or d.get("request_id"), **d}
        for d in decisions
    ]

    # Rules updates lifecycle spans 3 sub-dirs; roll them up in order.
    rules_entries: List[Dict[str, Any]] = []
    for sub, prefix in (
        ("countdowns", "cd_"),
        ("applies", "ap_"),
        ("rechecks", "rc_"),
    ):
        for r in _load_dir(ru / sub, [prefix]):
            rules_entries.append({
                "record_id": r.get("countdown_id") or r.get("apply_id")
                             or r.get("recheck_id") or Path(r["source_path"]).stem,
                "lifecycle_stage": sub[:-1],  # countdown / apply / recheck
                **r,
            })

    return {
        "approvals": {"count": len(approvals_entries), "entries": approvals_entries},
        "rules_updates": {"count": len(rules_entries), "entries": rules_entries},
        "reserved_decisions": {"count": len(reserved), "entries": reserved},
        "sources": {
            "approvals": str(ap),
            "rules_updates": str(ru),
            "reserved_decisions": str(requests_dir),
        },
        "reference_note": (
            "REFERENCE-NOT-COPY · Design Law A8 · every entry cites its "
            "source_path on disk; the surface renders record ids + short "
            "provenance rather than embedding record bodies. Original "
            "records live under phase0/ where each producer wrote them."
        ),
    }
