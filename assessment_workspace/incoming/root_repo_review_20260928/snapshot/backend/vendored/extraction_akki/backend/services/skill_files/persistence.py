"""Skill Files provenance persistence · write-once JSONL append.

Doc 18 A18.7 · TF-E4 (b) α · write-once discipline: same skill_id twice
is a WriteOnceViolation. Revocation is a separate lifecycle (deferred
per Owner ruling · non-blocking to CP4).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.skill_file_provenance_v0 import SkillFileProvenanceV0


class WriteOnceViolation(RuntimeError):
    """Attempted second append for the same skill_id."""


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "SKILL_FILE_PROVENANCE_DIR",
        "/app/assessment_workspace/phase0/skill_files/provenance",
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
    return _active_dir() / "provenance.jsonl"


def append(record: SkillFileProvenanceV0) -> SkillFileProvenanceV0:
    """Append a provenance record · write-once on skill_id."""
    if get_by_skill_id(record.skill_id) is not None:
        raise WriteOnceViolation(
            f"skill_id {record.skill_id!r} already provisioned · "
            f"Doc 18 TF-E4 (b) α: new slice = new skill_id."
        )
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with _store_file().open("a", encoding="utf-8") as fh:
        fh.write(record.model_dump_json())
        fh.write("\n")
    return record


def read_all() -> List[SkillFileProvenanceV0]:
    """REFERENCE-NOT-COPY read · deserialises from disk each call."""
    f = _store_file()
    if not f.exists():
        return []
    out: List[SkillFileProvenanceV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(SkillFileProvenanceV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_skill_id(skill_id: str) -> Optional[SkillFileProvenanceV0]:
    for r in read_all():
        if r.skill_id == skill_id:
            return r
    return None
