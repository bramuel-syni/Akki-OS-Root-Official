"""services.training.optimizer_harness · Doc 17 §A17.5-A17.6 two-arm harness.

Owner-verbatim spec (grounding brief lines 29-30):
    'Quality parity on M-a and M-b is mandatory for the candidate to
     remain eligible at all; compute-to-convergence is reported, never
     gating — a faster optimizer that regresses quality is not eligible
     regardless of its speed.'
    'The adopt/reject decision is then an Owner ruling made on the
     measured results, with no adoption threshold fixed in advance of
     the evidence, and verdict samples are uncurated per the platform's
     standing D-7 doctrine (evaluation inputs may be engineered;
     evaluation samples may not).'

Harness responsibilities:
  * Open a comparison shell with identical conditions frozen
    (base_model_id, evaluation_sets, budget_cap, smallest_stratum).
  * Record arm measurements (all four measured outputs; D-7 uncurated).
  * Compute eligibility: quality parity on M-a AND M-b mandatory —
    the harness itself flips verdict to 'ineligible' if the candidate
    regresses on either quality axis, without Owner intervention.
  * Route the ratifiable comparisons to Owner ruling (adopt/reject);
    'no adoption threshold fixed in advance of the evidence' — the
    harness never auto-adopts, only auto-refuses on quality-parity
    breach.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from contracts.optimizer_comparison_v0 import (
    ArmMeasurements,
    OptimizerComparisonV0,
)


class ComparisonNotFound(KeyError):
    """No comparison shell on record for the given id."""


class VerdictRefused(RuntimeError):
    """Owner ruling attempted on a comparison whose harness verdict is
    already 'ineligible' (quality-parity failed on M-a/M-b)."""


class QualityParityBreach(RuntimeError):
    """Harness auto-verdict: candidate regressed on M-a or M-b."""


class UncuratedFlagMissing(ValueError):
    """D-7 doctrine: evaluation_samples_uncurated MUST be True."""


_STORE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    return Path(os.environ.get(
        "TRAINING_OPTIMIZER_HARNESS_DIR",
        "/app/assessment_workspace/phase0/training/optimizer_harness",
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
    return _active_dir() / "comparisons.jsonl"


def _write_all(rows: List[OptimizerComparisonV0]) -> None:
    tmp = _store_file().with_suffix(".jsonl.tmp")
    _store_file().parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(r.model_dump_json())
            fh.write("\n")
    tmp.replace(_store_file())


def open_comparison(
    comparison_id: str,
    base_model_id: str,
    evaluation_sets: List[str],
    budget_cap_wallclock_seconds: int,
    budget_cap_gpu_hours: float,
    smallest_stratum: str,
    opened_at: str,
) -> OptimizerComparisonV0:
    """Open a shell · identical conditions frozen · verdict=awaiting_owner.
    Rewritten each call because record-updates require rewrite (append-only
    would require reconciliation reads)."""
    if get_by_id(comparison_id) is not None:
        raise ValueError(
            f"comparison_id {comparison_id!r} already on record."
        )
    shell = OptimizerComparisonV0(
        comparison_id=comparison_id,
        base_model_id=base_model_id,
        evaluation_sets=evaluation_sets,
        budget_cap_wallclock_seconds=budget_cap_wallclock_seconds,
        budget_cap_gpu_hours=budget_cap_gpu_hours,
        smallest_stratum=smallest_stratum,
        opened_at=opened_at,
    )
    rows = read_all() + [shell]
    _write_all(rows)
    return shell


def record_arm_measurements(
    comparison_id: str,
    arm: str,
    measurements: ArmMeasurements,
) -> OptimizerComparisonV0:
    """Record one arm's four measured outputs (A17.5 'without
    exception'). If both arms recorded, computes quality-parity
    eligibility: on M-a or M-b regression, harness auto-flips verdict
    to 'ineligible'."""
    if arm not in ("baseline", "muon"):
        raise ValueError(f"arm must be 'baseline' or 'muon', got {arm!r}")
    if not measurements.evaluation_samples_uncurated:
        raise UncuratedFlagMissing(
            "D-7 doctrine: evaluation samples MUST be uncurated. Set "
            "evaluation_samples_uncurated=True on the measurement."
        )
    current = get_by_id(comparison_id)
    if current is None:
        raise ComparisonNotFound(comparison_id)
    payload = current.model_dump()
    payload[f"{arm}_measurements"] = measurements.model_dump()
    updated = OptimizerComparisonV0.model_validate(payload)
    # Quality-parity check when both arms landed and verdict still pending.
    if (
        updated.baseline_measurements is not None
        and updated.muon_measurements is not None
        and updated.verdict == "awaiting_owner"
    ):
        b = updated.baseline_measurements
        m = updated.muon_measurements
        # Muon must not regress on M-a (target improvement should be >=
        # baseline) or M-b (non-target regression should be <= baseline).
        if m.moac_m_a_improvement < b.moac_m_a_improvement:
            payload["verdict"] = "ineligible"
            payload["verdict_note"] = (
                f"quality_parity_breach on M-a: candidate {m.moac_m_a_improvement}"
                f" < baseline {b.moac_m_a_improvement}"
            )
            updated = OptimizerComparisonV0.model_validate(payload)
        elif m.moac_m_b_regression > b.moac_m_b_regression:
            payload["verdict"] = "ineligible"
            payload["verdict_note"] = (
                f"quality_parity_breach on M-b: candidate {m.moac_m_b_regression}"
                f" > baseline {b.moac_m_b_regression}"
            )
            updated = OptimizerComparisonV0.model_validate(payload)
    rows = [r for r in read_all() if r.comparison_id != comparison_id]
    rows.append(updated)
    _write_all(rows)
    return updated


def rule_on_comparison(
    comparison_id: str,
    verdict: str,
    ratified_at: str,
    verdict_note: str = "",
) -> OptimizerComparisonV0:
    """Owner ruling · adopt or reject. Refuses if harness already flipped
    to 'ineligible' (quality-parity gate). Write-once per A17.5.
    On first 'adopted' verdict, ALSO fills the recipe seat with a
    governed TrainingParamsV0 row derived from the comparison (Doc 17
    A17.5 verbatim: 'On adoption, the winning arm writes
    training_params@v0 v1 with the comparison attached')."""
    if verdict not in ("adopted", "rejected"):
        raise ValueError(f"Owner ruling verdict must be 'adopted' or 'rejected', got {verdict!r}")
    current = get_by_id(comparison_id)
    if current is None:
        raise ComparisonNotFound(comparison_id)
    if current.verdict == "ineligible":
        raise VerdictRefused(
            f"comparison {comparison_id!r} is ineligible per harness quality-parity check: "
            f"{current.verdict_note}. No adoption is possible on quality-regression."
        )
    if current.verdict != "awaiting_owner":
        # A17.5 write-once verdict discipline: once ruled, cannot re-rule.
        raise VerdictRefused(
            f"comparison {comparison_id!r} already ruled ({current.verdict!r}). "
            "A17.5 verdict is write-once per adoption ceremony; open a fresh "
            "comparison for a new probe."
        )
    if current.baseline_measurements is None or current.muon_measurements is None:
        raise VerdictRefused(
            f"comparison {comparison_id!r} missing arm measurements; "
            "both arms must record all four measured outputs before ruling."
        )
    payload = current.model_dump()
    payload["verdict"] = verdict
    payload["verdict_note"] = verdict_note
    payload["ratified_at"] = ratified_at
    updated = OptimizerComparisonV0.model_validate(payload)
    rows = [r for r in read_all() if r.comparison_id != comparison_id]
    rows.append(updated)
    _write_all(rows)
    # A17.5 verbatim: 'On adoption, the winning arm writes
    # training_params@v0 v1 with the comparison attached.' Fire the
    # governed seat-fill AFTER the comparison verdict is persisted, so
    # a subsequent read from recipe_seat.append's verdict-check sees
    # verdict='adopted' on the comparison.
    if verdict == "adopted":
        from services.training import recipe_seat
        try:
            recipe_seat.write_from_adopted_comparison(updated, ratified_at)
        except recipe_seat.WriteOnceViolation:
            # Idempotent · seat already filled from this comparison.
            pass
    return updated


def read_all() -> List[OptimizerComparisonV0]:
    f = _store_file()
    if not f.exists():
        return []
    out: List[OptimizerComparisonV0] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(OptimizerComparisonV0.model_validate_json(line))
        except (ValueError, json.JSONDecodeError):
            continue
    return out


def get_by_id(comparison_id: str) -> Optional[OptimizerComparisonV0]:
    for r in read_all():
        if r.comparison_id == comparison_id:
            return r
    return None


def is_empty_harness() -> bool:
    """True iff no comparison shell has been opened yet · A17.5 first-run."""
    return len(read_all()) == 0
