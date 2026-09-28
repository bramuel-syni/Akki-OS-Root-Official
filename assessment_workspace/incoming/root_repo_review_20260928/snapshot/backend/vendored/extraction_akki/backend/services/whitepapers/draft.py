"""services.whitepapers.draft — CA1-005 whitepaper drafter (W10 CP6).

Doc 14 §33 CITATION invariant: whitepaper MUST cite an admission
record + a baseline-line record on disk. Service verifies both
citations resolve to files under phase0/. Refuses if either is
off-record.

Records: phase0/whitepapers/wp_*.json (append-only · §43).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from contracts.whitepaper_draft import WhitepaperDraft_v0


_DEFAULT_DIR = "/app/assessment_workspace/phase0/whitepapers"
_DEFAULT_ADMITS_DIR = "/app/assessment_workspace/phase0/model_admission_records"
_DEFAULT_BASELINE_DIR = "/app/assessment_workspace/phase0/baseline_lines"


def _dir() -> Path:
    return Path(os.environ.get("WHITEPAPERS_DIR", _DEFAULT_DIR))


def _admission_exists(admission_id: str) -> bool:
    d = Path(os.environ.get(
        "MODEL_ADMISSION_RECORDS_DIR", _DEFAULT_ADMITS_DIR
    ))
    if not d.is_dir():
        return False
    # Admission record filenames encode the model id + timestamp + uuid;
    # accept either an exact filename match OR any file containing the
    # admission_id as a substring (records the model id in the name).
    if (d / f"{admission_id}.json").exists():
        return True
    return any(admission_id in p.name for p in d.glob("*.json"))


def _baseline_exists(baseline_id: str) -> bool:
    d = Path(os.environ.get("BASELINE_LINES_DIR", _DEFAULT_BASELINE_DIR))
    return d.is_dir() and (d / f"{baseline_id}.json").exists()


def draft_whitepaper(payload: Dict[str, Any]) -> WhitepaperDraft_v0:
    """Draft a whitepaper. Refuses if either citation is off-record
    (§33 CITATION invariant) or if whitepaper_id exists (§43)."""
    w = WhitepaperDraft_v0(**payload)
    if not _admission_exists(w.cites_model_admission_id):
        raise ValueError(
            f"cites_model_admission_id {w.cites_model_admission_id!r} "
            f"not on record. Doc 14 §33: cite the admission."
        )
    if not _baseline_exists(w.cites_baseline_line_id):
        raise ValueError(
            f"cites_baseline_line_id {w.cites_baseline_line_id!r} not "
            f"on record. Doc 14 §33: cite the baseline."
        )
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{w.whitepaper_id}.json"
    if path.exists():
        raise ValueError(
            f"whitepaper {w.whitepaper_id!r} already on record. §43."
        )
    path.write_text(json.dumps(w.model_dump(), indent=2, ensure_ascii=False))
    return w


def load_whitepapers() -> List[WhitepaperDraft_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return sorted(
        (WhitepaperDraft_v0(**json.loads(p.read_text()))
         for p in d.glob("wp_*.json")),
        key=lambda w: (w.drafted_at, w.whitepaper_id),
    )
