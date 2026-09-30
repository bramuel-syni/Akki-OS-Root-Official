"""services.model_registry.registry — additive registry versioning + attest.

Owner Ruling 2026-08-25T23:30Z (W7 GO · Q3 disposition):
  LIFT RMS-IQ-Core-2/backend/services/perception/model_registry.py
  fabric semantics into a top-level `services/model_registry/`
  package. Seed from FACTS only: 7 Emergent Universal models are
  real; whisper-tiny is donor-side (NOT on this estate).

Semantics preserved from RMS 9.2a-E1 α ruling:
  * `current_registry_version()` — scans for highest v(N).json file.
  * `load_registry()` — returns the current models dict.
  * `attest_model(model_id)` — hard-fails if model not present.
  * `register_model(model_id, entry)` — additive v(N)→v(N+1) bump.

W6 DoD applies to any pydantic BaseModel + snapshot: registry entries
are plain dicts (no BaseModel) — no snapshot required. Discipline
follows RMS's own pattern; content shape is anchored in the seed file
docstring and in `test_w7_cp3_model_registry.py::
test_every_seeded_entry_carries_provenance_and_license_fields`.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

log = logging.getLogger(__name__)

_REGISTRY_DIR = Path(__file__).parent
_VERSION_RE = re.compile(r"models_registry\.v(\d+)\.json$")


HONEST_REGISTRY_LOCATION = (
    "This estate's model registry lives at services/model_registry/. "
    "Additive versioning: v(N).json preserved byte-identical; "
    "v(N+1).json adds one model."
)


def _list_versioned_files() -> List[Tuple[int, Path]]:
    hits: List[Tuple[int, Path]] = []
    for p in _REGISTRY_DIR.iterdir():
        m = _VERSION_RE.search(p.name)
        if m:
            hits.append((int(m.group(1)), p))
    hits.sort(key=lambda t: t[0])
    return hits


def current_registry_version() -> Tuple[int, Dict[str, Any]]:
    """Return (highest_version_n, models_dict) of the current registry.

    Raises FileNotFoundError with a clear honest sentence if no seed
    file is present — the seed must ship with the code (Owner ruling
    2026-08-25T23:30Z: 7 Emergent Universal models on record).
    """
    files = _list_versioned_files()
    if not files:
        raise FileNotFoundError(
            "model_registry: no v*.json seed found under "
            f"{_REGISTRY_DIR}. Seed models_registry.v0.json must ship with "
            "the code (7 Emergent Universal models on record · Owner Order "
            "2026-08-25 §2)."
        )
    n, path = files[-1]
    payload = json.loads(path.read_text(encoding="utf-8"))
    return n, dict(payload.get("models", {}))


def load_registry() -> Dict[str, Any]:
    """Return the current models dict (all model_ids on record)."""
    _, models = current_registry_version()
    return models


def attest_model(model_id: str) -> Dict[str, Any]:
    """Hard-fail if `model_id` not present in current registry.

    Returns the registry entry on success. Called by admission ceremony
    fires and workers before loading a model; loading an un-registered
    model produces fabricated telemetry attribution (RMS 9.2a-E1 α
    verbatim rationale, adapted here for estate-side model provenance).
    """
    models = load_registry()
    entry = models.get(model_id)
    if entry is None:
        raise ValueError(
            f"model {model_id!r} not in models_registry (current vocabulary: "
            f"{sorted(models.keys())!r}). Register via additive v(N) → "
            f"v(N+1) bump before use — Owner Ruling 2026-08-25T23:30Z: "
            f"only real models on record."
        )
    return entry


def register_model(model_id: str, entry: Dict[str, Any]) -> int:
    """Additive v(N)→v(N+1) bump for a new model entry.

    v(N).json preserved byte-identical. Returns new version N+1.
    Idempotent-by-model_id: if `model_id` is already registered,
    returns current N without writing.

    The bump is a governance event — the Model Admission ceremony
    (CP4) fires this after the six-criterion MOAC (Canon 4 §26) is
    on record.
    """
    n, models = current_registry_version()
    if model_id in models:
        return n
    new_models = {**models, model_id: {"model_id": model_id, **entry}}
    new_n = n + 1
    new_path = _REGISTRY_DIR / f"models_registry.v{new_n}.json"
    payload = {
        "version": f"v{new_n}",
        "extends": f"v{n}",
        "added_model_id": model_id,
        "authority_source": (
            f"Owner Ruling 2026-08-25T23:30Z (W7 GO) · additive registry "
            f"bump for {model_id!r}. v{n} preserved byte-identical."
        ),
        "models": new_models,
    }
    new_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return new_n



# ---------------------------------------------------------------------------
# W11 B · CP5 · Doc 17 §A17.3 · MOAC M-d lineage extension for trained
# adapters.
#
# Verbatim spec (grounding brief lines 22-23):
#     A17.3 [CANON] Lineage extends to configuration.
#     Every trained model's registry entry MUST cite the recipe_version
#     that trained it. MOAC's lineage criterion (M-d) extends by this
#     field, so 'which configuration produced this model' is answered
#     by reading the registry, never by asking whoever happened to run
#     the job.
# ---------------------------------------------------------------------------


class RecipeVersionMissingError(ValueError):
    """A17.3 refusal: trained-adapter entry lacking a recipe_version."""


TRAINED_ADAPTER_ROLE = "trained_adapter"


def register_adapter(model_id: str, entry: Dict[str, Any]) -> int:
    """Additive v(N)→v(N+1) bump for a trained-adapter entry.

    Enforces Doc 17 §A17.3 M-d extension: the entry MUST carry a
    non-empty `recipe_version` field. Any attempt to register a
    trained adapter without the recipe_version is refused
    (RecipeVersionMissingError).

    Non-trained-adapter entries continue to flow through
    `register_model` (purchased LLM catalogue etc.). This function is
    the trained-adapter chokepoint that answers 'which configuration
    produced this model' from the registry alone (A17.3).
    """
    if entry.get("role") != TRAINED_ADAPTER_ROLE:
        raise ValueError(
            f"register_adapter requires role={TRAINED_ADAPTER_ROLE!r}, "
            f"got {entry.get('role')!r}. For non-adapter entries use "
            f"register_model."
        )
    recipe_version = entry.get("recipe_version")
    if not recipe_version or not isinstance(recipe_version, str):
        raise RecipeVersionMissingError(
            f"trained-adapter {model_id!r} registration refused: "
            "Doc 17 §A17.3 requires every trained model's registry "
            "entry to cite the recipe_version that trained it. Missing "
            "or empty recipe_version breaks MOAC's M-d lineage criterion."
        )
    return register_model(model_id, entry)


def annotate_model(model_id: str, patch: Dict[str, Any], authority_source: str) -> int:
    """Additive v(N)→v(N+1) bump that carries a changed entry for an existing
    model (status · serving · recall). v(N) stays byte-identical; the change
    is a new entry that names its authority (Canon 8 §43 correction-by-new-entry).
    Refuses an unknown model_id."""
    n, models = current_registry_version()
    if model_id not in models:
        raise ValueError(f"model {model_id!r} not in models_registry; nothing to annotate.")
    history = list(models[model_id].get("annotations") or [])
    history.append({"registry_version": f"v{n + 1}", "authority_source": authority_source, "patch": patch})
    new_models = {**models, model_id: {**models[model_id], **patch, "annotations": history}}
    new_n = n + 1
    payload = {
        "version": f"v{new_n}",
        "extends": f"v{n}",
        "annotated_model_id": model_id,
        "authority_source": authority_source,
        "models": new_models,
    }
    (_REGISTRY_DIR / f"models_registry.v{new_n}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return new_n


def trained_adapters() -> Dict[str, Any]:
    return {mid: e for mid, e in load_registry().items() if e.get("role") == TRAINED_ADAPTER_ROLE}
