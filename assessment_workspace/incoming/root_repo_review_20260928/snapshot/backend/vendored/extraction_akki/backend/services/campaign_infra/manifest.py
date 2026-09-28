"""campaign_infra.manifest — campaign manifest schema (v0) + validation.

A manifest describes an ordered list of training runs a campaign will
execute. Runs run STRICTLY SEQUENTIALLY on a host; parallelism is banned
by construction (see run_queue.execute_campaign fcntl-lock).

Schema (v0):
    {
      "schema_version": 0,
      "campaign_id": str,        // unique, e.g. "cmp-001"
      "runs": [
        {
          "run_name": str,       // unique WITHIN the campaign
          "model_size_class": str,  // e.g. "0.5B", "1.5B", "7B"
          "corpus_variant": str, // e.g. "fixture_v0"
          "seed": int,           // deterministic seed (must be int)
          "hyperparams": dict,   // any dict (v0: not schema-validated)
          "held_out_slice_spec": str,  // e.g. "20pct_tail"
        },
        ...
      ]
    }

Wave-honest-limits (v0):
    - hyperparams shape is not validated (any dict accepted)
    - model_size_class is a string, not a rigorous enum
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List


class ManifestInvalid(ValueError):
    """Raised when a manifest fails validation."""


REQUIRED_RUN_FIELDS = (
    "run_name",
    "model_size_class",
    "corpus_variant",
    "seed",
    "hyperparams",
    "held_out_slice_spec",
)


def validate_manifest(manifest: Dict[str, Any]) -> None:
    """Raise ManifestInvalid on any schema violation."""
    if not isinstance(manifest, dict):
        raise ManifestInvalid(
            f"manifest must be a dict, got {type(manifest).__name__}"
        )
    if manifest.get("schema_version") != 0:
        raise ManifestInvalid(
            f"unsupported schema_version {manifest.get('schema_version')!r} "
            "(only v0 supported this wave)"
        )
    if not isinstance(manifest.get("campaign_id"), str) or \
            not manifest["campaign_id"]:
        raise ManifestInvalid("campaign_id missing or not a non-empty string")
    runs = manifest.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ManifestInvalid("runs missing or not a non-empty list")
    seen_names = set()
    for i, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ManifestInvalid(f"run[{i}] not a dict")
        missing = [f for f in REQUIRED_RUN_FIELDS if f not in run]
        if missing:
            raise ManifestInvalid(
                f"run[{i}] missing required field(s): {missing}"
            )
        rn = run["run_name"]
        if rn in seen_names:
            raise ManifestInvalid(f"duplicate run_name {rn!r}")
        seen_names.add(rn)
        if not isinstance(run["seed"], int) or isinstance(run["seed"], bool):
            raise ManifestInvalid(
                f"run[{i}] seed must be an int, got "
                f"{type(run['seed']).__name__}"
            )
        if not isinstance(run["hyperparams"], dict):
            raise ManifestInvalid(
                f"run[{i}] hyperparams must be a dict"
            )


def load_manifest(path: str) -> Dict[str, Any]:
    """Load a manifest JSON file, validate, and return the parsed dict."""
    p = Path(path)
    if not p.exists():
        raise ManifestInvalid(f"manifest file not found: {path}")
    try:
        manifest = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestInvalid(f"manifest JSON parse error: {exc}") from exc
    validate_manifest(manifest)
    return manifest


def iter_runs(manifest: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """Iterate runs in the declared order. No re-ordering."""
    for run in manifest.get("runs", []):
        yield run
