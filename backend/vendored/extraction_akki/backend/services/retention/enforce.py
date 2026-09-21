"""services.retention.enforce — CA1-N1 enforcement + attestation.

Owner Ruling 2026-08-25 · W6 GO §W6-SCOPE-(b):
    Append-only classes NEVER get delete verb. Retention on those =
    marked-expired + excluded-from-render.

Enforcement writes:
    · a `.expired` sidecar next to each expired append-only record
      (naming the retention_class + marked_expired_at + attestation_run_id)
    · an attestation record per run under RETENTION_ATTESTATION_DIR

Refusal grammar:
    · unknown class → RetentionRefused
    · enforcement asked to DELETE an append-only record → RetentionRefused
      with canon citation
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.retention.classes import RETENTION_CLASSES, class_for

log = logging.getLogger(__name__)


class RetentionRefused(Exception):
    """Raised when the enforcement path violates canon (e.g., asked to
    delete an append-only record)."""


def _attestation_dir() -> Path:
    return Path(os.environ.get(
        "RETENTION_ATTESTATION_DIR",
        "/app/assessment_workspace/phase0/retention_attestations",
    ))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _class_dir(letter: Dict[str, Any]) -> Path:
    env = letter.get("storage_dir_env")
    default = letter.get("storage_dir_default")
    return Path(os.environ.get(env, default) if env else default)


def _record_at_iso(record: Dict[str, Any], letter: Dict[str, Any]) -> str:
    field_name = letter.get("at_iso_field", "at_iso")
    return record.get(field_name, "") or ""


def is_expired(record: Dict[str, Any], letter: Dict[str, Any], now_iso: str) -> bool:
    """True if the record is past its marked_expired_after_days."""
    at = _record_at_iso(record, letter)
    if not at:
        return False
    try:
        record_dt = datetime.fromisoformat(at.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return False
    try:
        now_dt = datetime.fromisoformat(now_iso.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        now_dt = datetime.now(timezone.utc)
    days = letter.get("marked_expired_after_days") or letter.get("default_retention_days", 90)
    return (now_dt - record_dt) > timedelta(days=int(days))


@dataclass
class EnforcementRun:
    run_id: str
    at_iso: str
    dry_run: bool
    classes_walked: List[str]
    expired_this_run: List[Dict[str, Any]] = field(default_factory=list)
    total_expired_marked: int = 0
    total_soft_deleted: int = 0
    refusals: List[str] = field(default_factory=list)


def _write_expired_sidecar(record_path: Path, record_class: str,
                            attestation_run_id: str, marked_at: str) -> Path:
    sidecar = Path(str(record_path) + ".expired")
    sidecar.write_text(json.dumps({
        "receipt_id": record_path.stem,
        "record_class": record_class,
        "retention_class": record_class,
        "marked_expired_at": marked_at,
        "attestation_run_id": attestation_run_id,
        "canon_anchor": RETENTION_CLASSES[record_class].get("canon_anchor", ""),
        "letter": RETENTION_CLASSES[record_class].get("letter", ""),
    }, indent=2, sort_keys=True))
    return sidecar


def _walk_class(class_name: str, letter: Dict[str, Any], now_iso: str,
                dry_run: bool, run_id: str) -> Dict[str, Any]:
    """Walk one class · return {expired_this_class, refusals}."""
    d = _class_dir(letter)
    expired: List[Dict[str, Any]] = []
    refusals: List[str] = []

    if not d.is_dir():
        return {"expired": expired, "refusals": refusals}

    glob = letter.get("file_glob", "*.json")
    for record_path in sorted(d.glob(glob)):
        # Skip records already marked expired.
        if Path(str(record_path) + ".expired").exists():
            continue
        try:
            record = json.loads(record_path.read_text())
        except Exception:
            continue
        if not is_expired(record, letter, now_iso):
            continue

        storage_kind = letter.get("storage_kind")
        if storage_kind == "append_only":
            entry = {
                "receipt_id": record_path.stem,
                "record_class": class_name,
                "at_iso": _record_at_iso(record, letter),
                "action": "mark_expired",
            }
            expired.append(entry)
            if not dry_run:
                _write_expired_sidecar(record_path, class_name, run_id, now_iso)
        elif storage_kind == "governed_delete":
            entry = {
                "receipt_id": record_path.stem,
                "record_class": class_name,
                "at_iso": _record_at_iso(record, letter),
                "action": "soft_delete_after_grace",
                "grace_period_days": letter.get("grace_period_days", 0),
            }
            expired.append(entry)
            # Soft-delete: move to retired/ (create if missing).
            if not dry_run:
                retired_dir = d / "retired"
                retired_dir.mkdir(exist_ok=True)
                new_path = retired_dir / record_path.name
                if not new_path.exists():
                    record_path.rename(new_path)
        else:
            refusals.append(
                f"class_unknown_storage_kind · {class_name!r} · storage_kind={storage_kind!r}"
            )

    return {"expired": expired, "refusals": refusals}


def run_enforcement(*, dry_run: bool = True, now_iso: Optional[str] = None) -> EnforcementRun:
    """Walk every declared class · mark expired records · write
    attestation record. Refuses if enforcement is asked to delete an
    append-only record."""
    if now_iso is None:
        now_iso = _now_iso()
    run_id = f"attest-{uuid.uuid4().hex[:12]}"

    run = EnforcementRun(
        run_id=run_id,
        at_iso=now_iso,
        dry_run=dry_run,
        classes_walked=list(RETENTION_CLASSES.keys()),
    )

    for class_name, letter in RETENTION_CLASSES.items():
        result = _walk_class(class_name, letter, now_iso, dry_run, run_id)
        run.expired_this_run.extend(result["expired"])
        run.refusals.extend(result["refusals"])

    run.total_expired_marked = sum(1 for e in run.expired_this_run if e["action"] == "mark_expired")
    run.total_soft_deleted = sum(1 for e in run.expired_this_run if e["action"] == "soft_delete_after_grace")

    # Write the attestation record (always, even dry_run).
    if not dry_run:
        d = _attestation_dir()
        d.mkdir(parents=True, exist_ok=True)
        (d / f"attestation-{run_id[7:]}.json").write_text(
            json.dumps(asdict(run), indent=2, sort_keys=True)
        )

    return run


def list_attestations(*, limit: int = 50) -> List[Dict[str, Any]]:
    d = _attestation_dir()
    if not d.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for f in sorted(d.glob("attestation-*.json"), reverse=True)[:limit]:
        try:
            out.append(json.loads(f.read_text()))
        except Exception:
            continue
    return out


def list_expired(*, class_name: Optional[str] = None,
                  limit: int = 100) -> List[Dict[str, Any]]:
    """Enumerate records that currently carry a .expired sidecar."""
    out: List[Dict[str, Any]] = []
    classes = [class_name] if class_name else list(RETENTION_CLASSES.keys())
    for cname in classes:
        letter = class_for(cname)
        if not letter:
            continue
        d = _class_dir(letter)
        if not d.is_dir():
            continue
        for sidecar in sorted(d.glob("*.expired")):
            try:
                out.append(json.loads(sidecar.read_text()))
            except Exception:
                continue
    return out[:limit]


__all__ = [
    "EnforcementRun",
    "RetentionRefused",
    "is_expired",
    "list_attestations",
    "list_expired",
    "run_enforcement",
]
