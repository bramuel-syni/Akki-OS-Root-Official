"""services.cost_ledger.rates — OWNER-SUPPLIED rates, honestly absent
otherwise. NEVER invented.

Reads from `phase0/rates_register/models/*.json` +
`phase0/rates_register/gpu_hours/*.json`. Each file is a governed value —
one rate per file, authored by the owner, with a `source` and `authored_at`.

Canon 1 §4.4 · "No figure enters the system as a claim." Rates are
declared facts (owner-supplied) or absent (honest gap).
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)


HONEST_GAP_SENTENCE = (
    "This figure has not been measured on the estate's own material "
    "yet — quantity is on record, rate is not. Add a rate under "
    "phase0/rates_register/ to close the gap."
)


_DEFAULT_RATES_DIR = "/app/assessment_workspace/phase0/rates_register"


def _rates_dir() -> Path:
    return Path(os.environ.get("RATES_REGISTER_DIR", _DEFAULT_RATES_DIR))


def _load_json_dir(subdir: str) -> List[Dict[str, Any]]:
    d = _rates_dir() / subdir
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(f.read_text()))
        except Exception as exc:  # pragma: no cover
            log.warning("skipping unreadable rate %s: %s", f, type(exc).__name__)
    return out


def load_rates() -> Dict[str, List[Dict[str, Any]]]:
    """Return {'models': [...], 'gpu_hours': [...], 'training': [...]}
    — all owner-supplied rates on record.

    W7 CP1 · training lane added for adapter-training-run economics
    (Doc 13 §20 · Doc 14 §32 · MOAC.5 cost-per-op). Rate rows are
    OWNER-SUPPLIED FACTS or ABSENT (honest gap · Canon 1 §4.4).
    """
    return {
        "models": _load_json_dir("models"),
        "gpu_hours": _load_json_dir("gpu_hours"),
        "training": _load_json_dir("training"),
    }


def rate_for_model(model_id: str) -> Optional[Dict[str, Any]]:
    """Return the rate record for `model_id` or None (honest absence)."""
    if not model_id:
        return None
    for r in _load_json_dir("models"):
        if r.get("model_id") == model_id:
            return r
    return None


def rate_for_gpu_hour(node_id: str) -> Optional[Dict[str, Any]]:
    """Return the per-GPU-hour rate for `node_id` or None. Falls back
    through a wildcard entry `node_id=='*'` if present."""
    if not node_id:
        return None
    entries = _load_json_dir("gpu_hours")
    for r in entries:
        if r.get("node_id") == node_id:
            return r
    for r in entries:
        if r.get("node_id") == "*":
            return r
    return None


def rate_for_training_run(training_id: str) -> Optional[Dict[str, Any]]:
    """Return the training-run rate row for `training_id` or None
    (honest gap · Canon 1 §4.4).

    W7 CP1 · Doc 13 §20 adapter-training economics + Doc 14 §32
    baseline curation + MOAC.5 cost-per-op. Owner-supplied under
    `phase0/rates_register/training/*.json`, one row per file.
    """
    if not training_id:
        return None
    for r in _load_json_dir("training"):
        if r.get("training_id") == training_id:
            return r
    return None


def default_model_for_purpose(purpose: str) -> Optional[str]:
    """Which model would have been picked as the DEFAULT for this purpose,
    if the caller hadn't chosen a cheaper one? Owner-supplied via
    `is_default_for_purposes` list on the rate file. Returns model_id
    or None (no default declared)."""
    if not purpose:
        return None
    for r in _load_json_dir("models"):
        defaults = r.get("is_default_for_purposes") or []
        if purpose in defaults:
            return r.get("model_id")
    return None


__all__ = [
    "HONEST_GAP_SENTENCE",
    "load_rates",
    "rate_for_model",
    "rate_for_gpu_hour",
    "rate_for_training_run",
    "default_model_for_purpose",
]
