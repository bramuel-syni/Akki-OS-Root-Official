"""W-CENSUS-CANON-ALIGN · CP-C5 · JobManifest frozen carrier per S5 reframe.

Canon anchors (verbatim quotes carried by this docstring per the
Verbatim-canon standing rule · DECISIONS.md 2026-09-15T~01:40Z):

Owner S5 reframe (notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md:4,25):
    "build as a GENERIC, SCALABLE SYSTEM (a platform), NOT structured to this specific case … there is 'what the system should be' and separately 'mounting THIS job onto the system.'"
    "the platform builds estate-agnostic + modality-agnostic primitives. A job (audio census on 16 Kenyan stations OR text training on Aurora DBs OR an image-taxonomy census on an S3 bucket) is a mounting artifact — a JobManifest that binds the platform's registered planes to a concrete instance. Nothing case-specific may live in the platform code path."

Wave-honest-limit E.4 (notes/wave_census_canon_align_grounding_brief.md):
    "JobManifest is a shape-and-binding contract, not a runtime
     orchestrator this wave. CP-C5 lands the frozen carrier. Wiring
     existing audio-poc surfaces (recording_inventory, transcript_inventory,
     pairing_registry) as registered plane implementations behind the
     JobManifest is deliberate follow-on. This wave keeps the JobManifest
     as a data-only contract per Solva-V2 CP-S2 parameterless-boundary
     precedent."
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class JobManifest:
    """A mounting artifact per the S5 reframe: binds the platform's
    registered planes to a concrete estate instance.

    Five carriers:
      * ``job_id`` — deterministic id for this job instance (opaque string
        provided by the caller; not gated by this contract).
      * ``job_kind`` — string tag naming the job kind (e.g., "audio_census",
        "text_training", "image_taxonomy_census").
      * ``estate_instance`` — identifier for the concrete estate the job
        is mounted onto (e.g., "16_kenyan_stations", "aurora_dbs",
        "s3_bucket_x").
      * ``planes_bound`` — tuple of (plane_name, plane_binding) pairs.
        The tuple-of-tuples shape keeps the manifest hashable and
        canonicalisable for `compute_manifest_fingerprint`.
      * ``capabilities_declared`` — tuple of capability strings this job
        declares against the platform.

    Data-only per grounding brief §E.4: no `execute`, `run`, `dispatch`,
    `start`, `stop`, `step`, `iterate`, `process`, `commission`, `trigger`
    method. Runtime orchestration is a deliberate follow-on wave.
    """

    job_id: str
    job_kind: str
    estate_instance: str
    planes_bound: Tuple[Tuple[str, str], ...]
    capabilities_declared: Tuple[str, ...]


def compute_manifest_fingerprint(manifest: JobManifest) -> str:
    """Deterministic canonicalisation-and-hash of a `JobManifest`.

    Returns a stable `jm_<64-hex>` string. Same manifest → byte-identical
    fingerprint; changing any single carrier → distinct fingerprint. This
    fingerprint is the value that CP-C3's `generate_census_run_id` carries
    as its `job_manifest_fingerprint` input — the census run's identity
    resolves to the mounting artifact that produced it (§4.1 P30 verbatim:
    'Any measurement a surface displays resolves to the census run that
    produced it').
    """
    payload = {
        "job_id": manifest.job_id,
        "job_kind": manifest.job_kind,
        "estate_instance": manifest.estate_instance,
        "planes_bound": [list(p) for p in manifest.planes_bound],
        "capabilities_declared": list(manifest.capabilities_declared),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"jm_{digest}"
