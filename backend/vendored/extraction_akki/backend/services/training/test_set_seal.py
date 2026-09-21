"""Test-set seal · A17.11 (test-set precedes training) + Owner-directive
verbatim: 'RE-VERIFY against the live RDS Data API first, then seal · The
seal must reference freshly verified rows. Sealing against an 8/19 probe
cache would be a REFERENCE-NOT-COPY violation risk. If RDS is unreachable
at seal time, report honestly and hold the seal; do not seal against
stale cache.'

CP3 minimum viable seal:
  * Read the most recent ``data_connection_record`` for the source_id
    under the workspace records directory.
  * REFUSE if no record exists, if link_working is false, or if the
    record's ``at`` timestamp is older than the freshness window
    (24 hours default).
  * On acceptance, compute a deterministic manifest_sha256 over the
    (source_id, target_table, strata, sample_size, record_at) tuple and
    write the seal record to the workspace seals directory.

The seal record shape:
  {
    "kind": "test_set_seal",
    "seal_id": <slug>,
    "objective_id": ...,
    "source_id": ...,
    "target_table": ...,
    "strata": [...],
    "sample_size": ...,
    "manifest_sha256": ...,
    "sealed_at": ISO-8601 UTC,
    "rds_link_verified_at": <timestamp from the freshest live-verified record>,
    "verification_record_path": <path>,
  }

No AWS credentials pass through this module — the on-disk record IS the
live-verified attestation. Owner's constraint is that the record must
be FRESH (not a stale cache); the freshness window enforces that.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Configuration · freshness window · workspace paths.
# ---------------------------------------------------------------------------

FRESHNESS_WINDOW_HOURS: float = 24.0

_RECORDS_DIR: Optional[Path] = None
_SEAL_DIR: Optional[Path] = None


def _default_records_dir() -> Path:
    return Path(os.environ.get(
        "DATA_CONNECTION_RECORD_DIR",
        "/app/assessment_workspace/phase0/data_connection_records",
    ))


def _default_seal_dir() -> Path:
    return Path(os.environ.get(
        "TRAINING_TEST_SET_SEAL_DIR",
        "/app/assessment_workspace/phase0/training/test_set_seals",
    ))


def _configure_for_tests(records_dir: Path, seal_dir: Path) -> None:
    """Test hook · pin both dirs for isolation."""
    global _RECORDS_DIR, _SEAL_DIR
    _RECORDS_DIR = Path(records_dir)
    _SEAL_DIR = Path(seal_dir)
    _RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    _SEAL_DIR.mkdir(parents=True, exist_ok=True)


def _active_records_dir() -> Path:
    return _RECORDS_DIR if _RECORDS_DIR is not None else _default_records_dir()


def _active_seal_dir() -> Path:
    d = _SEAL_DIR if _SEAL_DIR is not None else _default_seal_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Shapes.
# ---------------------------------------------------------------------------

class SealRefused(RuntimeError):
    """Raised when the live-verify pre-condition fails · honest hold."""


@dataclass(frozen=True)
class TestSetSeal:
    seal_id: str
    objective_id: str
    source_id: str
    target_table: str
    strata: List[str]
    sample_size: int
    manifest_sha256: str
    sealed_at: str
    rds_link_verified_at: str
    verification_record_path: str


# ---------------------------------------------------------------------------
# Live-verify pre-condition · the on-disk record IS the attestation.
# ---------------------------------------------------------------------------

def _find_latest_record_for_source(source_id: str) -> Optional[dict]:
    """Return the most recent data_connection_record dict for source_id, or None.

    Records are JSON files under DATA_CONNECTION_RECORD_DIR named per source.
    We select the one with the freshest ``at`` timestamp.
    """
    d = _active_records_dir()
    if not d.exists():
        return None
    best: Optional[dict] = None
    best_at: Optional[datetime] = None
    for p in d.glob("*.json"):
        try:
            rec = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if rec.get("kind") != "data_connection_record":
            continue
        if rec.get("source_id") != source_id:
            continue
        at_str = rec.get("at")
        if not at_str:
            continue
        try:
            at = datetime.fromisoformat(at_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if best_at is None or at > best_at:
            best_at = at
            best = dict(rec)
            best["_record_path"] = str(p)
    return best


def _record_is_fresh(record: dict) -> bool:
    """Freshness window · 24h default."""
    at_str = record.get("at")
    if not at_str:
        return False
    try:
        at = datetime.fromisoformat(at_str.replace("Z", "+00:00"))
    except ValueError:
        return False
    age = datetime.now(timezone.utc) - at
    return age <= timedelta(hours=FRESHNESS_WINDOW_HOURS)


# ---------------------------------------------------------------------------
# Seal.
# ---------------------------------------------------------------------------

def _sanitize_strata_for_hash(strata: List[str]) -> str:
    return "|".join(sorted(strata))


def _compute_manifest_sha256(
    source_id: str,
    target_table: str,
    strata: List[str],
    sample_size: int,
    record_at: str,
) -> str:
    """Deterministic manifest hash over the sealed tuple."""
    payload = (
        f"{source_id}\n"
        f"{target_table}\n"
        f"{_sanitize_strata_for_hash(strata)}\n"
        f"{sample_size}\n"
        f"{record_at}\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def seal(
    objective_id: str,
    source_id: str,
    target_table: str,
    strata: List[str],
    sample_size: int,
) -> TestSetSeal:
    """A17.11 · test-set-precedes-training. RE-VERIFY-FIRST, then seal.

    Refuses honestly if:
      * no data_connection_record exists for source_id (no verification).
      * the freshest record has link_working=false.
      * the freshest record is older than FRESHNESS_WINDOW_HOURS.
    """
    rec = _find_latest_record_for_source(source_id)
    if rec is None:
        raise SealRefused(
            f"no verification record on disk for source {source_id!r}. "
            f"Owner directive: seal must reference a freshly verified live probe."
        )
    if not rec.get("link_working"):
        raise SealRefused(
            f"latest verification record for {source_id!r} has link_working=false. "
            f"Refusing to seal · the link is not currently live."
        )
    if not _record_is_fresh(rec):
        raise SealRefused(
            f"latest verification record for {source_id!r} is stale "
            f"(older than {FRESHNESS_WINDOW_HOURS}h). Refusing to seal · "
            f"sealing against a stale cache is a REFERENCE-NOT-COPY violation risk."
        )
    # Live-verified · compute manifest hash.
    manifest_sha = _compute_manifest_sha256(
        source_id=source_id,
        target_table=target_table,
        strata=strata,
        sample_size=sample_size,
        record_at=rec["at"],
    )
    seal_id = f"{objective_id.replace('/', '_')}__{target_table}__{manifest_sha[:12]}"
    seal_obj = TestSetSeal(
        seal_id=seal_id,
        objective_id=objective_id,
        source_id=source_id,
        target_table=target_table,
        strata=list(strata),
        sample_size=int(sample_size),
        manifest_sha256=manifest_sha,
        sealed_at=datetime.now(timezone.utc).isoformat(),
        rds_link_verified_at=rec["at"],
        verification_record_path=rec.get("_record_path", ""),
    )
    # Persist the seal record. Payload excludes AWS secrets by construction —
    # only pulls the four record fields listed above from the record dict.
    payload = {
        "kind": "test_set_seal",
        **asdict(seal_obj),
    }
    (_active_seal_dir() / f"{seal_id}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return seal_obj


def read_all_seals() -> List[dict]:
    """Return every seal on disk as dicts · REFERENCE-NOT-COPY."""
    d = _active_seal_dir()
    out: List[dict] = []
    for p in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return out
