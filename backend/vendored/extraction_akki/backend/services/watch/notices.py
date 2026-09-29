"""Watch notices — the notify posture (Canon 8 §12/§20 default until the owner rules the
reconciliation mode). Append-only per-tenant ledger; a notice is what the subject was actually
told, so 'silent success-that-wasn't' never happens. Read back only by the subject or the console."""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path


def _dir():
    return Path(os.environ.get("WATCH_NOTICES_DIR", "/app/assessment_workspace/phase0/watch_notices"))


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def rows(tenant_id):
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


def send(tenant_id, principal_id, kind, text, refs=None, now=None):
    now = now or datetime.now(timezone.utc)
    row = {"notice_id": f"wn_{uuid.uuid4().hex[:12]}", "kind": kind, "at": _iso(now), "tenant_id": tenant_id,
           "principal_id": principal_id, "text": text, "refs": refs or {}, "channel": "portal_notice",
           "posture": "notify (owner default until the reconciliation mode is ruled)"}
    _dir().mkdir(parents=True, exist_ok=True)
    with (_dir() / f"{tenant_id}.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def for_principal(tenant_id, principal_id):
    return sorted((r for r in rows(tenant_id) if r["principal_id"] == principal_id), key=lambda r: r["at"], reverse=True)


def by_ref(tenant_id, key, value):
    return [r for r in rows(tenant_id) if r.get("refs", {}).get(key) == value]
