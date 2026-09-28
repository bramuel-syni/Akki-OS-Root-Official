"""services.model_admission.ceremony — the admission state machine.

Canon 4 §26/§27/§28 · Doc 13 §20-§28 · CA1-004 baseline line ·
CA1-011 SPLIT (W7 register + W9 named seam).

Owner Ruling 2026-08-25T23:30Z (W7 GO · Q2): MOAC evidence source =
Registry census facts by default (structure-only, purpose-safe). Fresh
estate-sample passes require a named purpose id; missing purpose ⇒
NAME THE GAP (refuse with reason `estate_sample_without_named_purpose`).
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from contracts.model_acceptance_card import ModelAcceptanceCard_v0
from services.model_registry.registry import register_model

log = logging.getLogger(__name__)


_DEFAULT_ADMITS_DIR = "/app/assessment_workspace/phase0/model_admission_records"

# CA1-011 SPLIT · orchestrator ruling 2026-08-25T23:15Z
# W7 names the seam; W9 binds enforcement to it.
CA1_011_WATCH_SEAM = "services.watch.route_recheck_failure (lands W9)"


@dataclass(frozen=True)
class AdmissionOutcome:
    """The ceremony's structured decision.

    Written to phase0/model_admission_records/ verbatim (append-only,
    governance surface reads).
    """
    outcome: str                      # "admitted" | "refused" | "quarantined"
    model_id: str
    reason: str                       # "" for admitted; short snake_case for refused
    refusal_note: str                 # human sentence for the refusal card
    registry_version_after: Optional[int]   # None on refusal
    ca1_011_watch_seam: str = CA1_011_WATCH_SEAM
    computed_at: str = ""


def _admits_dir() -> Path:
    return Path(os.environ.get("MODEL_ADMISSION_RECORDS_DIR", _DEFAULT_ADMITS_DIR))


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _refuse(model_id: str, reason: str, note: str) -> AdmissionOutcome:
    return AdmissionOutcome(
        outcome="refused",
        model_id=model_id,
        reason=reason,
        refusal_note=note,
        registry_version_after=None,
        computed_at=_now_iso(),
    )


def _check_floors(card: ModelAcceptanceCard_v0) -> Optional[str]:
    """Return the name of the first criterion whose floor is missed,
    or None if all pass (or no floor on record — honest gap)."""
    criteria = {
        "accuracy_uncurated": card.accuracy_uncurated,
        "coverage_strata": card.coverage_strata,
        "refusal_behaviour": card.refusal_behaviour,
        "provenance_integrity": card.provenance_integrity,
        "cost_per_operation": card.cost_per_operation,
        "time_to_answer_p95": card.time_to_answer_p95,
    }
    for name, c in criteria.items():
        # Cost/latency criteria: lower is better; floors are "at most X".
        # Others: higher is better; floors are "at least X".
        # For the v0 shape we honor a single semantic: measured_value <
        # floor_value ⇒ fail (higher-is-better default). Cost/latency
        # floor-check inversion is a P1 refinement (owner ruling item).
        if c.floor_value is None:
            continue
        if name in ("cost_per_operation", "time_to_answer_p95"):
            if c.measured_value > c.floor_value:
                return name
        else:
            if c.measured_value < c.floor_value:
                return name
    return None


def _write_record(payload: Dict[str, Any]) -> None:
    d = _admits_dir()
    d.mkdir(parents=True, exist_ok=True)
    filename = (
        f"admit_{payload['candidate_model_id']}_{payload['computed_at']}_"
        f"{uuid.uuid4().hex[:8]}.json"
    )
    (d / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def _record_payload(
    card: ModelAcceptanceCard_v0,
    outcome: AdmissionOutcome,
) -> Dict[str, Any]:
    """Compose the on-disk admission record. NEVER carries credentials
    (Owner Order 2026-08-25 §4)."""
    return {
        "candidate_model_id": card.candidate_model_id,
        "outcome": outcome.outcome,
        "reason": outcome.reason,
        "refusal_note": outcome.refusal_note,
        "registry_version_after": outcome.registry_version_after,
        "moac_card": card.model_dump(),
        "ca1_011_watch_seam": outcome.ca1_011_watch_seam,
        "computed_at": outcome.computed_at,
    }


def run_admission(card_payload: Dict[str, Any]) -> AdmissionOutcome:
    """Fire the Model Admission ceremony against a MOAC card payload.

    Accepts a dict (constructs the ModelAcceptanceCard_v0 internally so
    pydantic's validation surface is the first refusal path — curated
    benchmarks are unrepresentable at the type level per C4-038).

    Order of refusal checks (owner-facing narration):
      1. Contract validation (Literal / Field constraints).
      2. Estate-sample evidence requires named purpose (Owner Q2).
      3. Training lineage resolved (§28 / C4-039).
      4. All floors met (§26.1-§26.6 · floors are owner-supplied).
    On all pass: register_model additive bump; write admitted record.
    """
    # 1. Contract validation (pydantic raises on curated_benchmark or
    #    missing fields; caller sees the ValidationError).
    card = ModelAcceptanceCard_v0(**card_payload)
    computed_at = _now_iso()

    # 2. Estate-sample requires named purpose (Owner Q2).
    if (
        card.evidence_source_kind == "uncurated_estate_sample"
        and not (card.evidence_purpose_id or "").strip()
    ):
        outcome = AdmissionOutcome(
            outcome="refused",
            model_id=card.candidate_model_id,
            reason="estate_sample_without_named_purpose",
            refusal_note=(
                "MOAC evidence_source_kind is 'uncurated_estate_sample' but "
                "evidence_purpose_id is not populated. Per Owner Ruling "
                "2026-08-25T23:30Z (W7 GO · Q2): fresh estate-sample passes "
                "require a named purpose on record. Name the gap or select a "
                "purpose before firing this ceremony."
            ),
            registry_version_after=None,
            computed_at=computed_at,
        )
        _write_record(_record_payload(card, outcome))
        return outcome

    # 3. Training lineage resolved (§28).
    if not card.training_lineage_resolved:
        outcome = AdmissionOutcome(
            outcome="refused",
            model_id=card.candidate_model_id,
            reason="training_lineage_unresolved",
            refusal_note=(
                f"Canon 4 §28 (C4-039): adapters whose training lineage "
                f"cannot be resolved do not ship. Lineage note on record: "
                f"{card.training_lineage_note!r}."
            ),
            registry_version_after=None,
            computed_at=computed_at,
        )
        _write_record(_record_payload(card, outcome))
        return outcome

    # 4. Floors (owner-supplied · honest gap on absence).
    missed = _check_floors(card)
    if missed is not None:
        outcome = AdmissionOutcome(
            outcome="refused",
            model_id=card.candidate_model_id,
            reason="moac_criterion_below_floor",
            refusal_note=(
                f"MOAC criterion {missed!r} did not meet the owner-supplied "
                f"floor at measurement time. See admission record for the "
                f"exact measured_value / floor_value pair."
            ),
            registry_version_after=None,
            computed_at=computed_at,
        )
        _write_record(_record_payload(card, outcome))
        return outcome

    # Admitted · register_model bumps v(N) → v(N+1).
    # CA1-011 W7 half: stamp re_check_due_at on the trained-adapter
    # entry (90-day default cadence). W9 Watch route fires on state
    # 'overdue' — the enforcement seam is named on the outcome.
    re_check_due = (
        datetime.now(timezone.utc) + timedelta(days=90)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {
        "provider": "trained_on_this_estate",
        "custody_kind": "estate_trained",
        "connected_at": computed_at,
        "role": "trained_adapter",
        "license_note": (
            "Adapter trained on rights-held tenant material · lineage "
            "resolved · MOAC on record at admission."
        ),
        "moac_card_computed_at": card.computed_at,
        "evidence_source_kind": card.evidence_source_kind,
        "re_check_due_at": re_check_due,
    }
    new_n = register_model(card.candidate_model_id, entry)

    outcome = AdmissionOutcome(
        outcome="admitted",
        model_id=card.candidate_model_id,
        reason="",
        refusal_note="",
        registry_version_after=new_n,
        computed_at=computed_at,
    )
    _write_record(_record_payload(card, outcome))
    return outcome
