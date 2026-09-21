"""services.grey_mirror.router — /api/grey_mirror/state (W10 CP8).

Read-only rollup of Grey Mirror surface state — mirages + touches +
severances (Canon 8 §15-§16 · BUILD not LIFT · W10 CP2). Every entry
cites its `source_path` (REFERENCE-NOT-COPY · Design Law A8).

Sources:
  * MIRAGES_DIR         → phase0/mirages/mr_*.json
  * MIRAGE_TOUCHES_DIR  → phase0/mirage_touches/mt_*.json
  * SEVERANCES_DIR      → phase0/severances/sv_*.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter


router = APIRouter()

_DEFAULTS = {
    "mirages":           "/app/assessment_workspace/phase0/mirages",
    "touches":           "/app/assessment_workspace/phase0/mirage_touches",
    "severances":        "/app/assessment_workspace/phase0/severances",
    "mirage_artifacts":  "/app/assessment_workspace/phase0/watch_mirage_artifacts",
}
_ENV_KEYS = {
    "mirages":           "MIRAGES_DIR",
    "touches":           "MIRAGE_TOUCHES_DIR",
    "severances":        "SEVERANCES_DIR",
    "mirage_artifacts":  "WATCH_MIRAGE_ARTIFACTS_DIR",
}
_ID_KEYS = {
    "mirages":           "mirage_id",
    "touches":           "touch_id",
    "severances":        "severance_id",
    "mirage_artifacts":  "artifact_id",
}
_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
}


def _dir(kind: str) -> Path:
    return Path(os.environ.get(_ENV_KEYS[kind], _DEFAULTS[kind]))


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v for k, v in d.items()
        if k not in _BANNED_FIELDS and not k.endswith("_raw")
    }


def _load_kind(kind: str) -> List[Dict[str, Any]]:
    d = _dir(kind)
    if not d.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(body, dict):
            continue
        rid = body.get(_ID_KEYS[kind]) or p.stem
        out.append({"record_id": rid, **_sanitize(body), "source_path": str(p)})
    return out


@router.get("/api/grey_mirror/state")
async def get_grey_mirror_state() -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    for kind in _ENV_KEYS:
        entries = _load_kind(kind)
        body[kind] = {"count": len(entries), "entries": entries}
    body["sources"] = {k: str(_dir(k)) for k in _ENV_KEYS}
    body["reference_note"] = (
        "REFERENCE-NOT-COPY · Design Law A8 · Grey Mirror is a BUILD "
        "(not LIFT · Executive-Core carries no mirage-machinery "
        "material). touch_kind grammar is CONTRACT-TIME closed to "
        "{'innocent_read', 'guilty_use'} per R2 (2026-08-26T04:20Z). "
        "Every entry cites source_path on disk."
    )
    return body
