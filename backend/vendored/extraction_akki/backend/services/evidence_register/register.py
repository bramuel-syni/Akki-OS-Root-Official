"""Evidence register persistence · Doc 19B §19B.5 · write-once JSONL append.

Discipline mirrors services.skill_files.persistence (CP4) +
services.training.recipe_seat (CP5): a JSONL sidecar under a workspace
path, keyed uniquely by figure_id, write-once on append.

EP-4 note (grounding brief line 52 + Doc 19 line 242):
    EP-4 remains OPEN — hard ordering constraint that the register and
    dual-judge protocol must exist before the terminal test runs. This
    module lands the register (EP-1) so the ordering constraint can be
    honoured; EP-4 itself is a config slot that flips when Owner
    ratifies the ordering (never a build gate).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.evidence_register_row_v0 import EvidenceRegisterRowV0


class WriteOnceViolation(RuntimeError):
    """Attempted second append for the same figure_id (§19B.6 absolute)."""


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "EVIDENCE_REGISTER_DIR",
        "/app/assessment_workspace/phase0/evidence_register",
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
    return _active_dir() / "register.jsonl"


def append(row: EvidenceRegisterRowV0) -> EvidenceRegisterRowV0:
    """§19B.6 · figure_id is unique across the register."""
    if get_by_figure_id(row.figure_id) is not None:
        raise WriteOnceViolation(
            f"figure_id {row.figure_id!r} already on record. §19B.6: "
            "'No figure reaches an external document without a "
            "resolvable register row' — figure_id is unique."
        )
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with _store_file().open("a", encoding="utf-8") as fh:
        fh.write(row.model_dump_json())
        fh.write("\n")
    return row


def read_all() -> List[EvidenceRegisterRowV0]:
    """REFERENCE-NOT-COPY read · deserialises from disk each call."""
    f = _store_file()
    if not f.exists():
        return []
    out: List[EvidenceRegisterRowV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(EvidenceRegisterRowV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_figure_id(figure_id: str) -> Optional[EvidenceRegisterRowV0]:
    for r in read_all():
        if r.figure_id == figure_id:
            return r
    return None


def is_empty_register() -> bool:
    """§19B.5 · register ships EMPTY at CP6 landing."""
    return len(read_all()) == 0
