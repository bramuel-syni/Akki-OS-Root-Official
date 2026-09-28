"""services.watch.mirage_artifacts · Doc 8 §Line 136 + §Line 183 verbatim ·
isolated write plane for MirageArtifactV0.

§Line 136 verbatim (canon/text/Akki_Canon_8_The_Watch.txt):
    'The mirage lies outward, never inward. Every mirage interaction
     writes truthfully marked records; the deception is a rendering
     shown to the suspect, never a falsification of anything beneath.
     And mirage state shares no store with production — bleed is
     unrepresentable, not filtered.'

§Line 183 verbatim:
    'Mirage isolation. Synthetic state shares no store with production;
     synthetic provenance is carried internally on every mirage
     artifact.'

Enforcement discipline:
  * The mirage-artifacts directory (WATCH_MIRAGE_ARTIFACTS_DIR) MUST
    be a peer of every production Watch store (verdicts, actions,
    sever_signals, marks). Same directory OR a subdirectory of any
    production store is refused at write time - MirageStoreBleedError.
  * Records write per-file JSON, keyed by artifact_id. Write-once.
  * No production-writer imports/calls from within this module (§Line
    136: 'the mirage lies outward, never inward').
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.mirage_artifact_v0 import MirageArtifactV0


class WriteOnceViolation(RuntimeError):
    pass


class MirageStoreBleedError(RuntimeError):
    """§Line 136/183 verbatim invariant refusal: the mirage store
    cannot share a filesystem handle with any production Watch store."""


_DEFAULT_DIR = "/app/assessment_workspace/phase0/watch_mirage_artifacts"

# The peer production Watch stores this module MUST NOT overlap with.
# Their environment variable names — resolved at write time.
_PRODUCTION_STORE_ENV_KEYS: tuple = (
    "WATCH_VERDICTS_DIR",
    "WATCH_ACTIONS_DIR",
    "WATCH_SEVER_SIGNALS_DIR",
    "WATCH_MARKS_DIR",
)


def _dir() -> Path:
    d = Path(os.environ.get("WATCH_MIRAGE_ARTIFACTS_DIR", _DEFAULT_DIR))
    return d


def _production_dirs() -> List[Path]:
    out: List[Path] = []
    for k in _PRODUCTION_STORE_ENV_KEYS:
        v = os.environ.get(k)
        if v:
            out.append(Path(v).resolve())
    return out


def _is_same_or_subpath(candidate: Path, base: Path) -> bool:
    """True when candidate == base or candidate is inside base."""
    try:
        candidate.resolve().relative_to(base)
        return True
    except ValueError:
        return False


def _assert_no_production_bleed(mirage_dir: Path) -> None:
    """§Line 136/183 · mirage store shares no handle with production."""
    resolved = mirage_dir.resolve()
    for prod in _production_dirs():
        # Two-way check: mirage inside production OR production inside mirage.
        if _is_same_or_subpath(resolved, prod) or _is_same_or_subpath(prod, resolved):
            raise MirageStoreBleedError(
                f"WATCH_MIRAGE_ARTIFACTS_DIR ({resolved}) shares no store "
                f"with production ({prod}). Doc 8 §Line 183 verbatim: "
                "'Mirage isolation. Synthetic state shares no store with "
                "production; synthetic provenance is carried internally "
                "on every mirage artifact.'"
            )


def _safe_filename(artifact_id: str) -> str:
    """Turn 'art/001' → 'art_001.json' so per-file writes work with
    slashy artifact ids (which are legitimate stable surrogates)."""
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", artifact_id)
    return f"{safe}.json"


def write_mirage_artifact(payload: Dict[str, Any]) -> MirageArtifactV0:
    """Land a mirage artifact in the isolated mirage store.

    Refuses:
      * MirageArtifactV0 grammar violation (§Line 183 unrepresentable
        posture: is_synthetic must be True, production_store_leak_check
        must be 'passed', outward_lie_only must be True).
      * MirageStoreBleedError (§Line 136/183) when the mirage
        directory overlaps any production Watch store.
      * WriteOnceViolation on duplicate artifact_id (§Line 39).
    """
    artifact = MirageArtifactV0(**payload)
    d = _dir()
    _assert_no_production_bleed(d)
    d.mkdir(parents=True, exist_ok=True)
    path = d / _safe_filename(artifact.artifact_id)
    if path.exists():
        raise WriteOnceViolation(
            f"mirage artifact_id {artifact.artifact_id!r} already on record."
        )
    path.write_text(artifact.model_dump_json(indent=2), encoding="utf-8")
    return artifact


def read_mirage_artifacts() -> List[MirageArtifactV0]:
    """Read all mirage artifacts from the isolated store only.
    Never reads from any production store (§Line 136 · outward, not
    inward)."""
    d = _dir()
    if not d.is_dir():
        return []
    out: List[MirageArtifactV0] = []
    for p in sorted(d.glob("*.json")):
        try:
            body = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        try:
            out.append(MirageArtifactV0(**body))
        except (ValueError, TypeError):
            continue
    return out


def get_mirage_artifact(artifact_id: str) -> Optional[MirageArtifactV0]:
    for a in read_mirage_artifacts():
        if a.artifact_id == artifact_id:
            return a
    return None
