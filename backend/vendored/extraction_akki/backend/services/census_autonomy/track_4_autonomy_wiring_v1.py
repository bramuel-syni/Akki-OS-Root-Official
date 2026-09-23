"""CP-TRACK-4-AUTONOMY-WIRING · track_4_autonomy_wiring_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.11.e
CP-TRACK-4-AUTONOMY-WIRING and nothing else. Additive-only per SO §3.8.
Sealed CP-SO-6.9-LID-WAVE + CP-CENSUS-THREE-WAVES + CP-AIP-10-TRAINING-RUNS
UNCHANGED. Terminal pytest only. RED-first mechanical.

Owner directive verbatim (SO §6.9 amendment §6 item 6 + Ruling (b) AKKI-RUNS-IT):
    'Register LID pass + corpus census + training seam as Census Autonomy
     Service jobs. Verification of autonomy pickup (receipt from the
     autonomy engine's run log showing the job ran) is the EXIT EVIDENCE
     for each such wiring seal. E1 wires the seams INTO the Census
     Autonomy Service so Akki runs them autonomously — then STEPS BACK.
     E1's pod is NEVER the training host and NEVER a data path.'

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Literal, Tuple

# Compose (never redeclare) sealed carriers per §1.2 modality-extension.
from backend.services.audio_plane_v1 import lid_wave_overlay_and_admission_v1 as _LID
from backend.services.audio_plane_v1 import census_three_waves_v1 as _CENSUS
from backend.services.audio_plane_v1 import training_run_boundary_v1 as _TRAINING


# ---------------------------------------------------------------------------
# Track-4 job kinds (Literal-closed 3-tuple)
# ---------------------------------------------------------------------------


TRACK_4_JOB_KINDS: Final[Tuple[str, str, str]] = (
    "lid_pass",
    "census_three_waves",
    "training_runs",
)


TRACK_4_JOB_KIND_LITERAL = Literal["lid_pass", "census_three_waves", "training_runs"]


TRACK_4_RUN_STATUS_LITERAL = Literal["completed", "failed", "refused"]

_TRACK_4_RUN_STATUS_VALUES = ("completed", "failed", "refused")


# ---------------------------------------------------------------------------
# Refusal hierarchy
# ---------------------------------------------------------------------------


class Track4BoundaryRefused(Exception):
    """Base for all Track-4 boundary refusals."""


class PodIsNeverDataPathAtTrack4Error(Track4BoundaryRefused):
    """Ruling (b) AKKI-RUNS-IT verbatim: pod is never data path at Track-4 seat."""


class Track4JobKindRefused(Track4BoundaryRefused):
    """job_kind not in TRACK_4_JOB_KINDS."""


class AutonomyEngineRunReceiptStatusRefused(Track4BoundaryRefused):
    """status not in Literal['completed','failed','refused']."""


# ---------------------------------------------------------------------------
# Posture markers (Final str)
# ---------------------------------------------------------------------------


TRACK_4_AUTONOMY_WIRING_POSTURE: Final[str] = (
    "CP-TRACK-4-AUTONOMY-WIRING · Item 5.11.e · owner verbatim: 'Register "
    "LID pass + corpus census + training seam as Census Autonomy Service "
    "jobs. Verification of autonomy pickup (receipt from the autonomy "
    "engine's run log showing the job ran) is the EXIT EVIDENCE for each "
    "such wiring seal. E1 wires the seams INTO the Census Autonomy "
    "Service so Akki runs them autonomously — then steps back.' Track-4 "
    "composes three sealed registration seats (LID pass + census-three-"
    "waves + training-runs) and emits an autonomy-engine run receipt per "
    "job. E1 STEPS BACK after wiring."
)


POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4: Final[str] = (
    "Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1's pod is NEVER the "
    "training host and NEVER a data path. Track-4 registration seats "
    "refuse pod://* and /app/* prefixed engine_response_queue_ref or "
    "data_source_adapter_ref (PodIsNeverDataPathAtTrack4Error). The "
    "Census Autonomy Service — running INSIDE the live Akki OS system — "
    "picks up the registered job, executes it within the tenant compute "
    "+ custody boundary, and emits a run-log receipt as EXIT EVIDENCE."
)


E1_STEPS_BACK_AFTER_WIRING_POSTURE: Final[str] = (
    "Ruling (b) AKKI-RUNS-IT verbatim: 'E1 wires the seams INTO the "
    "Census Autonomy Service so Akki runs them autonomously — then "
    "STEPS BACK.' Track-4 registration seats emit registration objects; "
    "the autonomy engine picks them up. E1's role ENDS at wire-in; the "
    "job runs inside Akki's boundary without further E1 involvement. "
    "The autonomy-engine run receipt returning to Track-4 is proof E1 "
    "correctly stepped back (E1 did not orchestrate the run)."
)


# ---------------------------------------------------------------------------
# Frozen carriers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Track4LidPassRegistration_v1:
    """LID-pass job registration for Census Autonomy Service.

    Composes sealed CP-SO-6.9-LID-WAVE WHISPER_LID_REGISTRATION +
    VOXLINGUA107_REGISTRATION as the LID model identities the autonomy
    engine will exercise when it picks up the job.
    """
    job_kind: str  # always "lid_pass"
    engine_response_queue_ref: str
    data_source_adapter_ref: str
    sealed_lid_registrations: Tuple[object, ...]  # sealed LID registrations by identity


@dataclass(frozen=True)
class Track4AllJobsRegistered_v1:
    """Aggregate registration receipt for Track-4 boundary.

    Composes the three sealed registration seats into one Track-4-scoped
    aggregate. Autonomy engine references this to know all three jobs
    were wired in the same seal.
    """
    lid_pass_registration: Track4LidPassRegistration_v1
    census_three_waves_registration: object  # CensusThreeWavesCensusAutonomyRegistration_v1 (sealed)
    training_runs_registration: object  # TrainingRunCensusAutonomyRegistration_v1 (sealed)
    total_jobs_registered: int


@dataclass(frozen=True)
class AutonomyEngineRunReceipt_v1:
    """EXIT EVIDENCE — a receipt from the autonomy engine's run log
    showing that a Track-4 wired job actually ran inside Akki's boundary.

    Owner verbatim: 'Verification of autonomy pickup (receipt from the
    autonomy engine's run log showing the job ran) is the EXIT EVIDENCE
    for each such wiring seal.'
    """
    job_kind: str  # one of TRACK_4_JOB_KINDS
    run_id: str
    started_at_utc: str
    finished_at_utc: str
    status: str  # one of "completed" / "failed" / "refused"
    provenance_ref: str  # census_autonomy_service://run_log/<run_id>


# ---------------------------------------------------------------------------
# Ruling (b) refusal helper — pod://* or /app/* refused at seam
# ---------------------------------------------------------------------------


def _refuse_pod_prefixed_ref(ref: str, kind: str) -> None:
    """Raises PodIsNeverDataPathAtTrack4Error for pod://* or /app/* prefixes."""
    if ref.startswith("pod://") or ref.startswith("/app/"):
        raise PodIsNeverDataPathAtTrack4Error(
            f"Ruling (b) verbatim: pod is never data path. Refused "
            f"{kind}={ref!r} at Track-4 registration seat."
        )


# ---------------------------------------------------------------------------
# Individual seam registrations (LID pass + census-three-waves + training-runs)
# ---------------------------------------------------------------------------


def register_lid_pass_as_census_autonomy_job(
    *, engine_response_queue_ref: str, data_source_adapter_ref: str
) -> Track4LidPassRegistration_v1:
    """Wire the LID pass (Whisper-LID + VoxLingua107 sealed registrations)
    into Census Autonomy Service.

    Refuses pod://* and /app/* prefixed refs (Ruling (b) verbatim).
    Composes sealed CP-SO-6.9-LID-WAVE `WHISPER_LID_REGISTRATION` +
    `VOXLINGUA107_REGISTRATION` by identity.
    """
    _refuse_pod_prefixed_ref(engine_response_queue_ref, "engine_response_queue_ref")
    _refuse_pod_prefixed_ref(data_source_adapter_ref, "data_source_adapter_ref")
    return Track4LidPassRegistration_v1(
        job_kind="lid_pass",
        engine_response_queue_ref=engine_response_queue_ref,
        data_source_adapter_ref=data_source_adapter_ref,
        sealed_lid_registrations=(
            _LID.WHISPER_LID_REGISTRATION,
            _LID.VOXLINGUA107_REGISTRATION,
        ),
    )


def register_all_three_track_4_jobs(
    *,
    lid_pass_engine_response_queue_ref: str,
    lid_pass_data_source_adapter_ref: str,
    census_three_waves_engine_response_queue_ref: str,
    census_three_waves_data_source_adapter_ref: str,
    training_runs_engine_response_queue_ref: str,
    training_runs_data_source_adapter_ref: str,
    training_runs_run_id: str = "run-track4-training-default",
    training_runs_commissioned_job_contract_ref: str = "census_autonomy://commissioned_job_contract/track4",
) -> Track4AllJobsRegistered_v1:
    """Compose the three sealed registration seats into a Track-4 aggregate.

    Delegates to sealed carriers for census-three-waves + training-runs;
    provides the LID pass registration here. All three seats refuse
    pod://* and /app/* prefixed refs (Ruling (b)).
    """
    lid_reg = register_lid_pass_as_census_autonomy_job(
        engine_response_queue_ref=lid_pass_engine_response_queue_ref,
        data_source_adapter_ref=lid_pass_data_source_adapter_ref,
    )
    census_reg = _CENSUS.register_census_three_waves_as_census_autonomy_job(
        engine_response_queue_ref=census_three_waves_engine_response_queue_ref,
        data_source_adapter_ref=census_three_waves_data_source_adapter_ref,
    )
    training_reg_obj = _TRAINING.TrainingRunCensusAutonomyRegistration_v1(
        run_id=training_runs_run_id,
        engine_response_queue_ref=training_runs_engine_response_queue_ref,
        data_source_adapter_ref=training_runs_data_source_adapter_ref,
        commissioned_job_contract_ref=training_runs_commissioned_job_contract_ref,
    )
    _TRAINING.register_training_run_as_census_autonomy_job(registration=training_reg_obj)
    return Track4AllJobsRegistered_v1(
        lid_pass_registration=lid_reg,
        census_three_waves_registration=census_reg,
        training_runs_registration=training_reg_obj,
        total_jobs_registered=3,
    )


# ---------------------------------------------------------------------------
# Autonomy engine run receipt (EXIT EVIDENCE)
# ---------------------------------------------------------------------------


def emit_autonomy_engine_run_receipt(
    *,
    job_kind: str,
    run_id: str,
    started_at_utc: str,
    finished_at_utc: str,
    status: str,
    provenance_ref: str,
) -> AutonomyEngineRunReceipt_v1:
    """Emit an autonomy-engine run receipt.

    Owner verbatim: 'Verification of autonomy pickup (receipt from the
    autonomy engine's run log showing the job ran) is the EXIT EVIDENCE
    for each such wiring seal.'

    Refuses:
    - job_kind not in TRACK_4_JOB_KINDS → Track4JobKindRefused.
    - status not in {'completed','failed','refused'} → AutonomyEngineRunReceiptStatusRefused.
    """
    if job_kind not in TRACK_4_JOB_KINDS:
        raise Track4JobKindRefused(
            f"job_kind={job_kind!r} not in TRACK_4_JOB_KINDS={TRACK_4_JOB_KINDS}"
        )
    if status not in _TRACK_4_RUN_STATUS_VALUES:
        raise AutonomyEngineRunReceiptStatusRefused(
            f"status={status!r} not in {_TRACK_4_RUN_STATUS_VALUES}"
        )
    return AutonomyEngineRunReceipt_v1(
        job_kind=job_kind,
        run_id=run_id,
        started_at_utc=started_at_utc,
        finished_at_utc=finished_at_utc,
        status=status,
        provenance_ref=provenance_ref,
    )
