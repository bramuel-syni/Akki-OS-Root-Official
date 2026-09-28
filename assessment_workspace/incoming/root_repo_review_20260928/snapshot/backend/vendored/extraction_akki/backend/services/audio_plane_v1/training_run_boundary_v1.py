"""CP-AIP-10-TRAINING-RUNS · training_run_boundary_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.10
CP-AIP-10-TRAINING-RUNS and nothing else. Additive-only per SO §3.8.
No sealed carrier edit. Terminal pytest only. RED-first mechanical.

Spec anchors (verbatim):
- AIP v1.0 §11.6 P189a: 'A run without a passed calibration is
  refused by the planner.'
- §11.6 P190a-d: completion certificate carries compute_consumed,
  data_touched, manifest_hash, per_stratum_results.
- §11.6 P190e: 'Failed strata are reported as plainly as passed ones.'
- §11.5 P185a: 'Every training example carries its provenance into
  the training manifest.'
- §11.5 P187: 'A rights lapse yields the enumerable set of affected
  models.'
- Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: 'E1's role = build and
  WIRE the seams INTO the Census Autonomy Service so Akki runs them
  autonomously — then STEP BACK. E1's pod is never the training host
  and never a data path.'
- §1.2: modality-extension composes sealed symbols; no redeclaration.
- §1.4: measure-don't-assert; measured cost receipt discipline.

Sealed carriers composed (UNCHANGED per SO §3.8):
- backend/services/audio_plane_v1/sampling_reflection_boundary_v1.py
  (CP-AIP-8 · S&R boundary + calibration gate).
- backend/services/audio_plane_v1/target_outcome_planner_boundary_v1.py
  (CP-AIP-7 · planner boundary · upstream).
- backend/services/audio_plane_v1/training_planner.py (CP-M6-7-2/3 ·
  CostQuoteWithCI).
- backend/services/perception/audio_codec/pretraining_contract_v1.py
  (CP-AIP-4 · pretraining contract seat · HONEST_GAP_V1_POSTURE
  pattern this seal follows).
"""
from __future__ import annotations

import dataclasses
from typing import Dict, Final, FrozenSet, Iterable, List, Literal, Optional

from backend.services.audio_plane_v1.sampling_reflection_boundary_v1 import (
    PlanWithoutCalibrationAtSRBoundary,
    enter_sr_with_planner_result,
)


# ---------------------------------------------------------------------------
# §1.4 + §11.6 posture markers (Final str)
# ---------------------------------------------------------------------------


HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE: Final[str] = (
    "CP-AIP-10-TRAINING-RUNS · §11.6 verbatim: 'quoted before start' + "
    "§1.4 verbatim: measure-don't-assert measured-cost-receipt "
    "discipline. Heavy fine-tune runs are DEFERRED to a commissioned "
    "job with a measured cost receipt; this boundary lands the "
    "contract + refusal machinery + Census-Autonomy-Service "
    "registration seam. No heavy training executes in E1's pod at "
    "this seal. This is posture-only per §1.4 measure-don't-assert; "
    "the pattern mirrors sealed CP-AIP-4 pretraining_contract_v1 "
    "HONEST_GAP_V1_POSTURE."
)


POD_IS_NEVER_DATA_PATH_POSTURE: Final[str] = (
    "CP-AIP-10-TRAINING-RUNS · Ruling (b) AKKI-RUNS-IT verbatim "
    "2026-02-23: 'E1's role = build and WIRE the seams INTO the "
    "Census Autonomy Service so Akki runs them autonomously — then "
    "STEP BACK. E1's pod is never the training host and never a "
    "data path.' The registration seam structurally refuses any "
    "engine_response_queue_ref or data_source_adapter_ref that "
    "starts with pod://* or /app/* prefix (§1.5 unrepresentable "
    "posture at the boundary)."
)


_POD_REF_PREFIXES: Final[tuple[str, ...]] = ("pod://", "/app/")


# ---------------------------------------------------------------------------
# Refusal hierarchy · all subclass TrainingRunCommissionedJobRefused
# ---------------------------------------------------------------------------


class TrainingRunCommissionedJobRefused(Exception):
    """Base class for every CP-AIP-10 training-run boundary refusal.

    Ledger check - CP-AIP-10 refusal boundary. Additive-only.
    """


class CalibrationMissingAtTrainingRunError(TrainingRunCommissionedJobRefused):
    """§11.6 P189a verbatim: run refused without passed §11.2 calibration."""


class CompletionCertificateSchemaMismatchError(TrainingRunCommissionedJobRefused):
    """§11.6 P190a-d verbatim: certificate shape violation."""


class StratumMissingFromCertificateError(TrainingRunCommissionedJobRefused):
    """§11.6 P190e verbatim: 'failed strata reported as plainly as
    passed ones' — omitting a stratum is a structural refusal.
    """


class ProvenanceRefMissingAtTrainingManifestError(TrainingRunCommissionedJobRefused):
    """§11.5 P185a verbatim: 'every training example carries its
    provenance into the training manifest' — empty provenance_ref
    refused at manifest append boundary.
    """


class PodAsDataPathAtRegistrationError(TrainingRunCommissionedJobRefused):
    """Ruling (b) verbatim: E1's pod is never a data path.

    Refuses data_source_adapter_ref that starts with pod://* or /app/*.
    """


class PodAsTrainingHostAtRegistrationError(TrainingRunCommissionedJobRefused):
    """Ruling (b) verbatim: E1's pod is never the training host.

    Refuses engine_response_queue_ref that starts with pod://* or
    /app/*.
    """


# ---------------------------------------------------------------------------
# §11.6 P190a-d verbatim · CompletionCertificate_v1 · 4-field frozen shape
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class PerStratumResult_v1:
    """§11.6 P190e verbatim: 'Failed strata are reported as plainly as
    passed ones.' Status Literal enforced; identical surface shape
    across passed/failed rows.
    """

    stratum_id: str
    status: Literal["passed", "failed"]
    detail: str


@dataclasses.dataclass(frozen=True)
class CompletionCertificate_v1:
    """§11.6 P190a-d verbatim · exactly four fields in this order:
    compute_consumed, data_touched, manifest_hash, per_stratum_results.
    """

    compute_consumed: str
    data_touched: str
    manifest_hash: str
    per_stratum_results: tuple  # tuple[PerStratumResult_v1, ...]

    def render(self, *, expected_strata: Iterable[str]) -> Dict[str, object]:
        """Render the certificate. Refuses via
        `StratumMissingFromCertificateError` if any expected stratum
        is absent from per_stratum_results.
        """
        present = {r.stratum_id for r in self.per_stratum_results}
        expected = set(expected_strata)
        missing = expected - present
        if missing:
            raise StratumMissingFromCertificateError(
                f"CP-AIP-10 · §11.6 P190e verbatim: 'Failed strata are "
                f"reported as plainly as passed ones.' Certificate "
                f"refuses to render with strata missing: "
                f"{sorted(missing)!r}"
            )
        return {
            "compute_consumed": self.compute_consumed,
            "data_touched": self.data_touched,
            "manifest_hash": self.manifest_hash,
            "per_stratum_results": [
                {
                    "stratum_id": r.stratum_id,
                    "status": r.status,
                    "detail": r.detail,
                }
                for r in self.per_stratum_results
            ],
        }


# ---------------------------------------------------------------------------
# §11.5 P185a-P187 verbatim · TrainingManifest_v1 with per-example provenance
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class TrainingManifestExampleRow_v1:
    """§11.5 P185a verbatim: every training example carries its
    provenance into the training manifest. provenance_ref is a
    non-empty string; rights_id names the rights envelope for §11.5
    P187 rights-lapse enumeration.
    """

    example_id: str
    provenance_ref: str
    rights_id: str


class TrainingManifest_v1:
    """§11.5 P185a verbatim: append-only manifest that refuses rows
    with empty or whitespace-only provenance_ref.
    """

    def __init__(self) -> None:
        self._rows: List[TrainingManifestExampleRow_v1] = []

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def append_row(self, row: TrainingManifestExampleRow_v1) -> None:
        if not row.provenance_ref or not row.provenance_ref.strip():
            raise ProvenanceRefMissingAtTrainingManifestError(
                f"CP-AIP-10 · §11.5 P185a verbatim: 'every training "
                f"example carries its provenance into the training "
                f"manifest.' Row {row.example_id!r} has empty or "
                f"whitespace-only provenance_ref; refused at append "
                f"boundary."
            )
        self._rows.append(row)


@dataclasses.dataclass(frozen=True)
class RightsLapseDetector_v1:
    """§11.5 P187 verbatim: 'A rights lapse yields the enumerable set
    of affected models.' `model_manifests` maps model_id → manifest.
    """

    model_manifests: Dict[str, TrainingManifest_v1]

    def enumerate_affected_model_ids(
        self, *, lapsed_rights_id: str
    ) -> FrozenSet[str]:
        """Return the frozenset of model_ids whose manifests carry at
        least one row with rights_id == lapsed_rights_id. Never None;
        empty frozenset if no models affected.
        """
        affected: set[str] = set()
        for model_id, manifest in self.model_manifests.items():
            if any(r.rights_id == lapsed_rights_id for r in manifest.rows):
                affected.add(model_id)
        return frozenset(affected)


# ---------------------------------------------------------------------------
# Ruling (b) AKKI-RUNS-IT verbatim · TrainingRunCensusAutonomyRegistration_v1
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class TrainingRunCensusAutonomyRegistration_v1:
    """Ruling (b) verbatim 2026-02-23: LID + corpus census + CP-AIP-10
    training must be registered as Census Autonomy Service jobs
    (engine + response queue + data-source adapter that already exist
    from Phase 3), so the running Akki system schedules and executes
    them.

    Four Final field names in this exact order:
    - run_id
    - engine_response_queue_ref
    - data_source_adapter_ref
    - commissioned_job_contract_ref
    """

    run_id: str
    engine_response_queue_ref: str
    data_source_adapter_ref: str
    commissioned_job_contract_ref: str


def register_training_run_as_census_autonomy_job(
    *, registration: TrainingRunCensusAutonomyRegistration_v1
) -> None:
    """Register a training run as a Census Autonomy Service job.

    Refuses via `PodAsDataPathAtRegistrationError` when
    `data_source_adapter_ref` starts with pod://* or /app/*.
    Refuses via `PodAsTrainingHostAtRegistrationError` when
    `engine_response_queue_ref` starts with pod://* or /app/*.
    Ruling (b) verbatim: E1's pod is never the training host and
    never a data path.
    """
    for prefix in _POD_REF_PREFIXES:
        if registration.data_source_adapter_ref.startswith(prefix):
            raise PodAsDataPathAtRegistrationError(
                f"CP-AIP-10 · Ruling (b) verbatim 2026-02-23: 'E1's "
                f"pod is never a data path.' Refusing "
                f"data_source_adapter_ref={registration.data_source_adapter_ref!r} "
                f"which starts with {prefix!r}."
            )
    for prefix in _POD_REF_PREFIXES:
        if registration.engine_response_queue_ref.startswith(prefix):
            raise PodAsTrainingHostAtRegistrationError(
                f"CP-AIP-10 · Ruling (b) verbatim 2026-02-23: 'E1's "
                f"pod is never the training host.' Refusing "
                f"engine_response_queue_ref={registration.engine_response_queue_ref!r} "
                f"which starts with {prefix!r}."
            )


# ---------------------------------------------------------------------------
# §11.6 P189a verbatim · open_training_run · run refused without calibration
# ---------------------------------------------------------------------------


def open_training_run(*, plan_has_calibration_output: bool) -> None:
    """§11.6 P189a verbatim: 'A run without a passed calibration is
    refused by the planner.' Composes sealed CP-AIP-8
    `enter_sr_with_planner_result` and surfaces its refusal as
    `CalibrationMissingAtTrainingRunError` at this compose boundary.
    """
    try:
        enter_sr_with_planner_result(
            plan_has_calibration_output=plan_has_calibration_output
        )
    except PlanWithoutCalibrationAtSRBoundary as exc:
        raise CalibrationMissingAtTrainingRunError(
            f"CP-AIP-10 · §11.6 P189a verbatim: 'A run without a "
            f"passed calibration is refused by the planner.' Sealed "
            f"CP-AIP-8 refusal surfaced at training-run compose "
            f"boundary: {exc}"
        ) from exc


__all__ = (
    "HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE",
    "POD_IS_NEVER_DATA_PATH_POSTURE",
    "TrainingRunCommissionedJobRefused",
    "CalibrationMissingAtTrainingRunError",
    "CompletionCertificateSchemaMismatchError",
    "StratumMissingFromCertificateError",
    "ProvenanceRefMissingAtTrainingManifestError",
    "PodAsDataPathAtRegistrationError",
    "PodAsTrainingHostAtRegistrationError",
    "PerStratumResult_v1",
    "CompletionCertificate_v1",
    "TrainingManifestExampleRow_v1",
    "TrainingManifest_v1",
    "RightsLapseDetector_v1",
    "TrainingRunCensusAutonomyRegistration_v1",
    "register_training_run_as_census_autonomy_job",
    "open_training_run",
)
