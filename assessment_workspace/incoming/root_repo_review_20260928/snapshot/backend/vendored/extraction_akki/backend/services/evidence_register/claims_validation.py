"""A-4 claims validation persistence · Doc 19B §19B.4 · EP-3.

Companion to services.evidence_register.register: records three-arm
re-entry attempts and bake-off decisions. NEVER GATES — §19B.6 · 'A-4
never becomes a gate by drift — its scope is validation and re-entry,
and staying there is a condition of adoption, not a detail.'

The store discipline mirrors register.py exactly (write-once JSONL by
claim_id). Separate module because the shape and grammar are distinct
and the OpenAPI surfaces must not conflate them.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.claims_validation_row_v0 import ClaimsValidationRowV0


class WriteOnceViolation(RuntimeError):
    pass


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "CLAIMS_VALIDATION_DIR",
        "/app/assessment_workspace/phase0/evidence_register/claims_validation",
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
    return _active_dir() / "claims_validation.jsonl"


def append(row: ClaimsValidationRowV0) -> ClaimsValidationRowV0:
    if get_by_claim_id(row.claim_id) is not None:
        raise WriteOnceViolation(
            f"claim_id {row.claim_id!r} already on record; "
            "a re-entry attempt uses a fresh claim_id."
        )
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with _store_file().open("a", encoding="utf-8") as fh:
        fh.write(row.model_dump_json())
        fh.write("\n")
    return row


def read_all() -> List[ClaimsValidationRowV0]:
    f = _store_file()
    if not f.exists():
        return []
    out: List[ClaimsValidationRowV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(ClaimsValidationRowV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_claim_id(claim_id: str) -> Optional[ClaimsValidationRowV0]:
    for r in read_all():
        if r.claim_id == claim_id:
            return r
    return None


def is_empty_ledger() -> bool:
    return len(read_all()) == 0
