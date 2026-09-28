"""services.baseline_line.records — CA1-004 record R/W with registry attest.

Records live at phase0/baseline_lines/ (or override via BASELINE_LINES_DIR).
One JSON file per baseline line. Append-only (governance surface reads).

`record_baseline_line` calls `attest_model` before writing, so an
unregistered starting model hard-fails at record time (RMS 9.2a-E1 α
adapted for estate-side baseline lines).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from contracts.baseline_line import BaselineLine_v0
from services.model_registry.registry import attest_model


_DEFAULT_DIR = "/app/assessment_workspace/phase0/baseline_lines"


def _dir() -> Path:
    return Path(os.environ.get("BASELINE_LINES_DIR", _DEFAULT_DIR))


def record_baseline_line(
    training_run_id: str,
    starting_model_id: str,
    authored_by: str,
    notes: Optional[str] = None,
) -> BaselineLine_v0:
    """Attest starting_model in registry, then record the line.

    Raises ValueError (from attest_model) if starting_model_id is not
    on record.
    """
    entry = attest_model(starting_model_id)
    line = BaselineLine_v0(
        baseline_line_id=f"bl_{training_run_id}",
        training_run_id=training_run_id,
        starting_model_id=starting_model_id,
        starting_model_license_note=entry.get("license_note", "no license note on record"),
        authored_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        authored_by=authored_by,
        notes=notes,
    )
    _dir().mkdir(parents=True, exist_ok=True)
    (_dir() / f"{line.baseline_line_id}.json").write_text(
        json.dumps(line.model_dump(), indent=2, ensure_ascii=False)
    )
    return line


def load_baseline_lines() -> List[BaselineLine_v0]:
    """Return every baseline line on record (append-only history)."""
    d = _dir()
    if not d.is_dir():
        return []
    out: List[BaselineLine_v0] = []
    for p in sorted(d.glob("bl_*.json")):
        out.append(BaselineLine_v0(**json.loads(p.read_text())))
    return out
