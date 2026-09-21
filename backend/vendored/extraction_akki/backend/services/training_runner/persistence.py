"""Trainer-runner persistence · Doc 17 · write-once JSONL for admits + runs.

Two write-once JSONL stores, keyed by admit_id / run_id. Discipline
mirrors CP4/CP5/CP6 stores exactly.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.training_material_admit_v0 import TrainingMaterialAdmitV0
from contracts.training_run_v0 import TrainingRunV0


class WriteOnceViolation(RuntimeError):
    pass


_ADMITS_DIR: Optional[Path] = None
_RUNS_DIR: Optional[Path] = None


def _default_dir(env_key: str, subpath: str) -> Path:
    return Path(os.environ.get(
        env_key,
        f"/app/assessment_workspace/phase0/training_runner/{subpath}",
    ))


def _configure_for_tests(admits_dir: Path, runs_dir: Path) -> None:
    global _ADMITS_DIR, _RUNS_DIR
    _ADMITS_DIR = Path(admits_dir)
    _RUNS_DIR = Path(runs_dir)
    _ADMITS_DIR.mkdir(parents=True, exist_ok=True)
    _RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _active_admits_dir() -> Path:
    if _ADMITS_DIR is not None:
        return _ADMITS_DIR
    d = _default_dir("TRAINING_RUNNER_ADMITS_DIR", "admits")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _active_runs_dir() -> Path:
    if _RUNS_DIR is not None:
        return _RUNS_DIR
    d = _default_dir("TRAINING_RUNNER_RUNS_DIR", "runs")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _admits_file() -> Path:
    return _active_admits_dir() / "admits.jsonl"


def _runs_file() -> Path:
    return _active_runs_dir() / "runs.jsonl"


def append_admit(admit: TrainingMaterialAdmitV0) -> TrainingMaterialAdmitV0:
    if get_admit(admit.admit_id) is not None:
        raise WriteOnceViolation(
            f"admit_id {admit.admit_id!r} already on record."
        )
    with _admits_file().open("a", encoding="utf-8") as fh:
        fh.write(admit.model_dump_json())
        fh.write("\n")
    return admit


def read_admits() -> List[TrainingMaterialAdmitV0]:
    f = _admits_file()
    if not f.exists():
        return []
    out: List[TrainingMaterialAdmitV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(TrainingMaterialAdmitV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_admit(admit_id: str) -> Optional[TrainingMaterialAdmitV0]:
    for a in read_admits():
        if a.admit_id == admit_id:
            return a
    return None


def _write_runs(rows: List[TrainingRunV0]) -> None:
    """Rewrite runs.jsonl - runs mutate through status transitions."""
    tmp = _runs_file().with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(r.model_dump_json())
            fh.write("\n")
    tmp.replace(_runs_file())


def upsert_run(run: TrainingRunV0) -> TrainingRunV0:
    """Insert or update by run_id."""
    rows = [r for r in read_runs() if r.run_id != run.run_id]
    rows.append(run)
    _write_runs(rows)
    return run


def read_runs() -> List[TrainingRunV0]:
    f = _runs_file()
    if not f.exists():
        return []
    out: List[TrainingRunV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(TrainingRunV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_run(run_id: str) -> Optional[TrainingRunV0]:
    for r in read_runs():
        if r.run_id == run_id:
            return r
    return None
