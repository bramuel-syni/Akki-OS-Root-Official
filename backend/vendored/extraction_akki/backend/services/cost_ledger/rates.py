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


LANES: Dict[str, Dict[str, Any]] = {
    "models": {"key": "model_id", "rate_fields": ("rate_per_million_tokens_in", "rate_per_million_tokens_out")},
    "gpu_hours": {"key": "node_id", "rate_fields": ("rate_per_hour",)},
    "training": {"key": "training_id", "rate_fields": ("rate_per_gpu_hour", "rate_per_1k_tokens", "rate_per_run")},
    "caas": {"key": "product_id", "rate_fields": ("rate_per_delivery",)},
}
BANNED_FIELDS = ("key", "api_key", "secret", "token", "credential")


def load_rates() -> Dict[str, List[Dict[str, Any]]]:
    """Return every owner-supplied rate on record by lane (models · gpu_hours · training · caas).

    W7 CP1 · training lane added for adapter-training-run economics
    (Doc 13 §20 · Doc 14 §32 · MOAC.5 cost-per-op); Mα MA-30 · caas lane.
    Rate rows are OWNER-SUPPLIED FACTS or ABSENT (honest gap · Canon 1 §4.4).
    """
    return {lane: _load_json_dir(lane) for lane in LANES}


def rate_for_caas_product(product_id: str) -> Optional[Dict[str, Any]]:
    """Per-delivery rate for a CaaS context product, or None; wildcard `product_id=='*'` is the fallback."""
    if not product_id:
        return None
    entries = _load_json_dir("caas")
    for r in entries:
        if r.get("product_id") == product_id:
            return r
    for r in entries:
        if r.get("product_id") == "*":
            return r
    return None


def author_rate(lane: str, record: Dict[str, Any], actor: str) -> Dict[str, Any]:
    """Write ONE governed rate row (owner-supplied fact) into the register. Requires the lane key, a non-placeholder
    `source` and at least one positive rate field; a previous row for the same id is kept inside the new file."""
    from datetime import datetime, timezone
    spec = LANES.get(lane)
    if not spec:
        raise ValueError(f"Unknown rate lane {lane!r}; one of {', '.join(LANES)}")
    ident = str(record.get(spec["key"]) or "").strip()
    if not ident:
        raise ValueError(f"A {lane} rate needs its {spec['key']}")
    source = str(record.get("source") or "").strip()
    if not source or "placeholder" in source.lower():
        raise ValueError("A rate without a real source is a claim, not a fact; give the invoice, quote or owner channel it comes from")
    if any(b in k.lower() for k in record for b in BANNED_FIELDS):
        raise ValueError("Credential-like fields are banned from the rates register")
    rates = {f: float(record[f]) for f in spec["rate_fields"] if record.get(f) is not None}
    if not rates or any(v <= 0 for v in rates.values()):
        raise ValueError(f"At least one positive rate field is required: {', '.join(spec['rate_fields'])}")
    directory = _rates_dir() / lane
    directory.mkdir(parents=True, exist_ok=True)
    slug = "wildcard" if ident == "*" else "".join(c if c.isalnum() or c in "-_." else "-" for c in ident)
    path = directory / f"{slug}.json"
    previous = json.loads(path.read_text()) if path.is_file() else None
    row = {spec["key"]: ident, **rates, "currency": str(record.get("currency") or "USD"), "source": source, "notes": str(record.get("notes") or "")[:600],
           "authored_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "authored_by": actor, "lane": lane}
    if previous:
        row["supersedes"] = {k: previous.get(k) for k in (*rates, "source", "authored_at", "authored_by")}
    path.write_text(json.dumps(row, indent=2))
    return row


def remove_rate(lane: str, ident: str) -> bool:
    spec = LANES.get(lane)
    if not spec:
        raise ValueError(f"Unknown rate lane {lane!r}")
    slug = "wildcard" if ident == "*" else "".join(c if c.isalnum() or c in "-_." else "-" for c in ident)
    path = _rates_dir() / lane / f"{slug}.json"
    if not path.is_file():
        return False
    path.unlink()
    return True


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
    "LANES",
    "load_rates",
    "rate_for_model",
    "rate_for_gpu_hour",
    "rate_for_training_run",
    "rate_for_caas_product",
    "author_rate",
    "remove_rate",
    "default_model_for_purpose",
]
