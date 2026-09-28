"""Deterministic Adaptive Walker — CP1 kernel.

Owner ruling verbatim (STATE/DECISIONS.md 2026-09-09T~evening):
    "Adaptive sampling admitted ONLY in determinised form (pinned
    policy + fixed seed, C4-013 repeatability preserved). Online /
    path-dependent adaptive stays OUT pending a separate owner ruling."

Canon binding · C4-013 (Repeatable):
    "Every Mtafiti measurement is repeatable — same inputs, same
    time-boundary, same declaration set → same measured output."

Contract:
  `deterministic_walk(inputs, sample_size)` returns a JSON-serialisable
  manifest carrying:
    - policy_id  (POLICY_ID, pinned)
    - seed       (MTAFITI_GPU_SAMPLING_SEED, pinned)
    - inputs_sha256           (canonical sha256 of the input list)
    - sample_size             (min(sample_size, len(inputs)))
    - sample                  (list of inputs, walker-selected)
    - manifest_sha256         (sha256 of the manifest sans this field)

Same inputs + same sample_size → byte-identical manifest.
"""
from __future__ import annotations

import hashlib
import json
import random
from typing import Any, Sequence

from services.mtafiti.gpu_discovery_constants import (
    MTAFITI_GPU_SAMPLING_SEED,
    POLICY_ID,
)


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def deterministic_walk(inputs: Sequence[Any], sample_size: int) -> dict:
    """Return a deterministic sample manifest of `inputs`.

    The walker's policy is trivially "seeded-uniform sample" for CP1.
    The determinism guarantee — same inputs → same manifest — is what
    matters for C4-013; policy sophistication is the province of later
    CPs (CP9 adds a determinised bandit; CP11 wires this into the live
    Weego / USSD fixtures).
    """
    inputs_list = list(inputs)
    ordered = sorted(
        inputs_list,
        key=lambda x: _canonical_sha256(x),
    )
    rng = random.Random(MTAFITI_GPU_SAMPLING_SEED)
    k = max(0, min(int(sample_size), len(ordered)))
    sample: list = []
    remaining = list(ordered)
    for _ in range(k):
        idx = rng.randrange(0, len(remaining))
        sample.append(remaining.pop(idx))

    manifest = {
        "policy_id": POLICY_ID,
        "seed": MTAFITI_GPU_SAMPLING_SEED,
        "inputs_sha256": _canonical_sha256(inputs_list),
        "sample_size": len(sample),
        "sample": sample,
    }
    manifest["manifest_sha256"] = _canonical_sha256(manifest)
    return manifest
