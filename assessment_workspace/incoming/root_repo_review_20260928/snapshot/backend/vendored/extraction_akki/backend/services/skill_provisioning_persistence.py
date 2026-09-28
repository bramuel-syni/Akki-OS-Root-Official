"""Callable-Skill Provisioning Record persistence · write-once slice-binding guardrail.

Doc 18 §A18.2 verbatim (Wave B grounding brief · Canon-of-Record):
    'A18.2  [CANON] The slice freezes; it never edits. Corpus slice binds
     at freeze, an endpoint is provisioned against it, and a key is scoped
     to that endpoint. The slice persists via the artifact store,
     write-once. If the underlying material needs to change, the platform
     provisions a new skill against a new slice — it does not mutate the
     old one.'

Write-once discipline:
  * Same `skill_id` twice = WriteOnceViolation (mirrors sealed A18.7
    persistence pattern at `services/skill_files/persistence.py`).
  * Same `corpus_slice_ref` twice = WriteOnceViolation (canon:
    "new slice = new skill" · one endpoint per slice · one slice per skill).
  * Field-level mutation of an existing record via append() = impossible
    by construction (append() only checks presence · in-place mutation
    is not exposed by the module).
  * Revocation as a separate lifecycle event is DEFERRED to a follow-on
    sub-slice via event-sourced tombstone appends (banked-not-blocking
    per owner ruling that revocation is a distinct lifecycle from the
    frozen tuple).

Distinct from sealed A18.7 write-once (services/skill_files/persistence.py):
  * A18.7 write-once anchor = `skill_id` only (buyer-facing chain).
  * A18-2 write-once anchors = BOTH `skill_id` AND `corpus_slice_ref`
    (owner-facing frozen tuple + slice-per-skill canon binding).

Storage:
  * JSONL append-only at `SKILL_PROVISIONING_RECORD_DIR/records.jsonl`
    (defaults to `/app/assessment_workspace/phase0/skill_provisioning/`).
  * Test-configurable via `_configure_for_tests(dir_)`.
  * REFERENCE-NOT-COPY read (deserialises from disk each call · no
    in-memory cache to invalidate).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.skill_provisioning_record_v0 import SkillProvisioningRecordV0


class WriteOnceViolation(RuntimeError):
    """Attempted second append that violates A18-2 slice-freezes-never-edits.

    Raised when:
      * A record with the same `skill_id` already exists.
      * A record with the same `corpus_slice_ref` already exists (new
        material must yield new slice AND new skill_id).
    """


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "SKILL_PROVISIONING_RECORD_DIR",
        "/app/assessment_workspace/phase0/skill_provisioning",
    ))


def _configure_for_tests(dir_: Path) -> None:
    global _STORE_DIR
    _STORE_DIR = Path(dir_)
    _STORE_DIR.mkdir(parents=True, exist_ok=True)


def _active_dir() -> Path:
    if _STORE_DIR is not None:
        return _STORE_DIR
    d = _default_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _store_file() -> Path:
    return _active_dir() / "records.jsonl"


def append(record: SkillProvisioningRecordV0) -> SkillProvisioningRecordV0:
    """Append a fresh provisioning record · write-once on skill_id AND corpus_slice_ref.

    Enforces A18-2 slice-freezes-never-edits at write time. In-place
    mutation is impossible because this module does not expose a mutator
    (only append() + REFERENCE-NOT-COPY reads).
    """
    if get_by_skill_id(record.skill_id) is not None:
        raise WriteOnceViolation(
            f"skill_id {record.skill_id!r} already provisioned · "
            f"Doc 18 §A18.2: new slice = new skill · cannot re-provision "
            f"an existing skill_id."
        )
    if get_by_corpus_slice_ref(record.corpus_slice_ref) is not None:
        raise WriteOnceViolation(
            f"corpus_slice_ref {record.corpus_slice_ref!r} already bound to "
            f"an existing skill · Doc 18 §A18.2: one endpoint per slice · "
            f"new material must yield new corpus_slice_ref AND new skill_id."
        )
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with _store_file().open("a", encoding="utf-8") as fh:
        fh.write(record.model_dump_json())
        fh.write("\n")
    return record


def read_all() -> List[SkillProvisioningRecordV0]:
    """REFERENCE-NOT-COPY read · deserialises from disk each call."""
    f = _store_file()
    if not f.exists():
        return []
    out: List[SkillProvisioningRecordV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(SkillProvisioningRecordV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_skill_id(skill_id: str) -> Optional[SkillProvisioningRecordV0]:
    """Lookup a record by `skill_id` (returns None if absent)."""
    for r in read_all():
        if r.skill_id == skill_id:
            return r
    return None


def get_by_corpus_slice_ref(
    corpus_slice_ref: str,
) -> Optional[SkillProvisioningRecordV0]:
    """Lookup a record by `corpus_slice_ref` (returns None if absent).

    Second write-once anchor per A18-2 slice-per-skill binding.
    """
    for r in read_all():
        if r.corpus_slice_ref == corpus_slice_ref:
            return r
    return None
