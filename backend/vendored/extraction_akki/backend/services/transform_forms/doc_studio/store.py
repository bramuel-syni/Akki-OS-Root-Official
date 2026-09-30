"""File-backed, tenant-scoped commission store (owner condition D: nothing on the shared database until Mongo-per-tenant lands).

AKKI_STUDIO_STORE_DIR/<tenant>/<commission_id>/
  record.json          the commission record (read by the API)
  v<N>/                the commission directory for content version N: brief, content, verdict and one spec per output
  builds/<build_id>/   a/ and b/ (build_once outputs), prove.json, log.txt, exports/
Commission directories and build outputs are written once; a revision creates v<N+1>, never edits v<N>."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

SAFE = re.compile(r"[^A-Za-z0-9_.-]")


def root(tenant_id: str) -> Path:
    base = Path(os.environ["AKKI_STUDIO_STORE_DIR"]) / SAFE.sub("_", tenant_id)
    base.mkdir(parents=True, exist_ok=True)
    return base


def commission_dir(tenant_id: str, commission_id: str) -> Path:
    return root(tenant_id) / SAFE.sub("_", commission_id)


def version_dir(tenant_id: str, commission_id: str, version: int) -> Path:
    return commission_dir(tenant_id, commission_id) / f"v{version}"


def build_dir(tenant_id: str, commission_id: str, build_id: str) -> Path:
    return commission_dir(tenant_id, commission_id) / "builds" / SAFE.sub("_", build_id)


def write_json(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True, default=str) + "\n")
    os.replace(tmp, path)


def read_json(path: Path) -> Optional[Any]:
    return json.loads(path.read_text()) if path.exists() else None


def save_record(record: Dict[str, Any]) -> Dict[str, Any]:
    write_json(commission_dir(record["tenant_id"], record["commission_id"]) / "record.json", record)
    return record


def load_record(tenant_id: str, commission_id: str) -> Optional[Dict[str, Any]]:
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", commission_id or ""):
        return None
    return read_json(commission_dir(tenant_id, commission_id) / "record.json")


def list_records(tenant_id: str) -> List[Dict[str, Any]]:
    out = []
    for path in root(tenant_id).glob("*/record.json"):
        rec = read_json(path)
        if rec:
            out.append(rec)
    return sorted(out, key=lambda r: r.get("updated_at") or "", reverse=True)
