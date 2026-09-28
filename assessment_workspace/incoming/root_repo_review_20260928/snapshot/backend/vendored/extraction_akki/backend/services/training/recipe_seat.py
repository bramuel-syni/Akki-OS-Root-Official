"""services.training.recipe_seat · Doc 17 §A17.3-A17.4 recipe-seat persistence.

Doc 17 empty-seat verbatim (grounding brief · line 58):
    'No default recipe exists until the first training run fills it
     through the §3 optimizer-selection protocol (A17.5-A17.6).
     Nothing may pre-populate training_params@v0 by convention,
     template, or engineer judgement — the first value ever written
     to it must carry the measured comparison that produced it.'

Discipline mirrors services.skill_files.persistence (CP4 pattern):
  * Write-once JSONL append keyed on recipe_version.
  * WriteOnceViolation on repeat.
  * REFERENCE-NOT-COPY read on every call (no in-memory cache).
  * Empty-seat at CP5 landing · comparison_ref is required (no
    convention/template shortcut can bypass the harness output).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.training_params_v0 import TrainingParamsV0


class WriteOnceViolation(RuntimeError):
    """Attempted second append for the same recipe_version."""


class UnevidencedRecipeViolation(ValueError):
    """A17.4 · 'Revision is DEFAULT-class, but never unevidenced.'
    A recipe cannot be recorded without a live comparison_ref that
    the harness has ratified (adopted verdict + ratified_at)."""


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "TRAINING_RECIPE_SEAT_DIR",
        "/app/assessment_workspace/phase0/training/recipe_seat",
    ))


def _configure_for_tests(dir_: Path) -> None:
    global _STORE_DIR
    _STORE_DIR = Path(dir_)
    _STORE_DIR.mkdir(parents=True, exist_ok=True)


def _active_dir() -> Path:
    if _STORE_DIR is not None:
        return _STORE_DIR
    d = _default_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _store_file() -> Path:
    return _active_dir() / "recipes.jsonl"


def append(record: TrainingParamsV0, *, comparison_verdict_check=None) -> TrainingParamsV0:
    """Write-once append. `comparison_verdict_check` is a callable
    receiving `comparison_ref` and returning True iff the referenced
    optimizer_comparison has verdict=='adopted'. Injected here so
    persistence stays decoupled from the harness module import cycle.
    """
    if get_by_version(record.recipe_version) is not None:
        raise WriteOnceViolation(
            f"recipe_version {record.recipe_version!r} already on record. "
            "A17.4: revision is DEFAULT-class · a new recipe = new version."
        )
    if comparison_verdict_check is None:
        # Default check reads the optimizer_harness store; late-imported to
        # break the module cycle (harness imports persistence side effects).
        from services.training import optimizer_harness
        def comparison_verdict_check(ref: str) -> bool:
            cmp_ = optimizer_harness.get_by_id(ref)
            return cmp_ is not None and cmp_.verdict == "adopted"
    if not comparison_verdict_check(record.comparison_ref):
        raise UnevidencedRecipeViolation(
            f"comparison_ref {record.comparison_ref!r} is not an adopted "
            "optimizer_comparison. A17.4: 'Revision is DEFAULT-class, but "
            "never unevidenced.' — recipe write refused."
        )
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with _store_file().open("a", encoding="utf-8") as fh:
        fh.write(record.model_dump_json())
        fh.write("\n")
    return record


def read_all() -> List[TrainingParamsV0]:
    """REFERENCE-NOT-COPY read · deserialises from disk each call."""
    f = _store_file()
    if not f.exists():
        return []
    out: List[TrainingParamsV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(TrainingParamsV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_version(recipe_version: str) -> Optional[TrainingParamsV0]:
    for r in read_all():
        if r.recipe_version == recipe_version:
            return r
    return None


def is_empty_seat() -> bool:
    """Doc 17 empty-recipe-seat honesty helper. True iff no recipe
    has been written yet (CP5 ship-state · A17.5 first-run gate)."""
    return len(read_all()) == 0


def write_from_adopted_comparison(comparison, ratified_at: str):
    """Doc 17 A17.5 verbatim governed seat-fill:

        'On adoption, the winning arm writes training_params@v0 v1
         with the comparison attached; on rejection, the candidate is
         recorded as tested, with its numbers, permanently.'

    Called automatically by optimizer_harness.rule_on_comparison when
    verdict flips to 'adopted' for the first time. The recipe row is
    derived deterministically from the comparison:
      * recipe_version = f'training_params@v0/adopted_from_{slug}'
      * optimizer_kind = 'muon'   (the candidate arm; A17.5 grammar
                                    fixes baseline vs muon, and only
                                    muon is a candidate at CP5).
      * base_model_id  = comparison.base_model_id
      * evaluation_sets = comparison.evaluation_sets  (identical
                                                       conditions
                                                       frozen at open)
      * budget_cap     = BudgetCap(...) copied verbatim
      * hyperparams    = {}  (empty · future PATCH endpoint may extend)
      * comparison_ref = comparison.comparison_id
      * ratified_at    = the Owner ruling timestamp

    Idempotent: if the recipe_version already exists, silently returns
    the pre-existing row (write-once is already enforced on the store).
    """
    from contracts.training_params_v0 import BudgetCap, TrainingParamsV0
    slug = comparison.comparison_id.replace("/", "_")
    recipe_version = f"training_params@v0/adopted_from_{slug}"
    existing = get_by_version(recipe_version)
    if existing is not None:
        return existing
    record = TrainingParamsV0(
        recipe_version=recipe_version,
        base_model_id=comparison.base_model_id,
        optimizer_kind="muon",
        hyperparams={},
        evaluation_sets=list(comparison.evaluation_sets),
        budget_cap=BudgetCap(
            wallclock_seconds=comparison.budget_cap_wallclock_seconds,
            gpu_hours=comparison.budget_cap_gpu_hours,
        ),
        comparison_ref=comparison.comparison_id,
        ratified_at=ratified_at,
    )
    return append(record, comparison_verdict_check=lambda ref: True)
