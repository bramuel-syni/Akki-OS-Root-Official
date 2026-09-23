"""CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · census_three_waves_v1 · additive §1.2 modality-extension.

Ledger check - this seal implements EXECUTION_ORDER.md Item 5.11.c
CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY and nothing else. Additive-only
per SO §3.8. No sealed carrier edit. Terminal pytest only. RED-first
mechanical.

SO §6.9 amendment §6 item 8 verbatim:
    'The census proceeds in its three waves — complete the walk with
     the unmeasured register, the full B3 dimension set with the
     defensibility matrix and sensitivity classification, then the
     perception pathway — and language labels from item 4 enter it
     as overlay from the first run.'

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23:
    'E1's role = build and WIRE the seams INTO the Census Autonomy
     Service so Akki runs them autonomously — then STEP BACK. E1's
     pod is never the training host and never a data path.'

Composes sealed CP-SO-6.9-LID-WAVE lid_wave_overlay_and_admission_v1
(WHISPER_LID_REGISTRATION + VOXLINGUA107_REGISTRATION +
LidModelRegistration_v1) at the module boundary. §1.2 modality-extension
— no redeclaration of sealed symbols. Sealed carriers UNCHANGED per
SO §3.8 additive-only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Optional, Tuple

from backend.services.audio_plane_v1.lid_wave_overlay_and_admission_v1 import (
    LidModelRegistration_v1,
    VOXLINGUA107_REGISTRATION,
    WHISPER_LID_REGISTRATION,
)


# ---------------------------------------------------------------------------
# Posture markers (Final str) — SO §6.9 amendment §6 item 8 verbatim
# ---------------------------------------------------------------------------


LID_OVERLAY_ENTERS_FROM_FIRST_RUN_POSTURE: Final[str] = (
    "CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · SO §6.9 amendment §6 "
    "item 8 verbatim: 'The census proceeds in its three waves — "
    "complete the walk with the unmeasured register, the full B3 "
    "dimension set with the defensibility matrix and sensitivity "
    "classification, then the perception pathway — and language "
    "labels from item 4 enter it as overlay from the first run.' "
    "LID overlay entering the perception pathway MUST trace to "
    "CP-SO-6.9-LID-WAVE sealed registrations (WHISPER_LID or "
    "VOXLINGUA107). Any other registration object is refused at "
    "the boundary; the overlay marker remains INFERRED per B5.4 "
    "shown-not-counted line."
)


POD_IS_NEVER_DATA_PATH_POSTURE_THREE_WAVES: Final[str] = (
    "CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · Ruling (b) "
    "AKKI-RUNS-IT verbatim 2026-02-23: 'E1's role = build and WIRE "
    "the seams INTO the Census Autonomy Service so Akki runs them "
    "autonomously — then STEP BACK. E1's pod is never the training "
    "host and never a data path.' The registration seam "
    "structurally refuses any engine_response_queue_ref or "
    "data_source_adapter_ref that starts with pod://* or /app/* "
    "prefix (§1.5 unrepresentable posture at the boundary)."
)


# ---------------------------------------------------------------------------
# Three-wave ordered tuple — SO §6.9 amendment §6 item 8 verbatim
# ---------------------------------------------------------------------------


CENSUS_THREE_WAVES: Final[Tuple[str, str, str]] = (
    "unmeasured_register",
    "b3_dimension_set",
    "perception_pathway",
)


WaveName = Literal["unmeasured_register", "b3_dimension_set", "perception_pathway"]


_POD_REF_PREFIXES: Final[Tuple[str, ...]] = ("pod://", "/app/")


# ---------------------------------------------------------------------------
# Refusal hierarchy · all subclass CensusWaveBoundaryRefused
# ---------------------------------------------------------------------------


class CensusWaveBoundaryRefused(Exception):
    """Base for all Census-three-waves boundary refusals."""


class CensusWaveNameRefused(CensusWaveBoundaryRefused):
    """Wave name not in CENSUS_THREE_WAVES 3-tuple."""


class CensusWaveOutOfOrderError(CensusWaveBoundaryRefused):
    """Wave N cannot open until Wave N-1 completed.

    Enforces SO §6.9 amendment §6 item 8 verbatim: three waves proceed
    in order — unmeasured register → B3 dim set → perception pathway.
    """


class PodIsNeverDataPathError(CensusWaveBoundaryRefused):
    """Registration seam refused: pod:// or /app/ prefixed ref detected.

    Enforces Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23. E1 wires the
    seam INTO Census Autonomy Service — pod is never data path.
    """


# ---------------------------------------------------------------------------
# Wave output shapes (frozen)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class UnmeasuredRegisterWave_v1:
    """Wave 1 output: unmeasured character-register batch.

    B5.4 shown-not-counted line: no dimension has been measured yet;
    dimensions_measured is False and downstream counted measures
    cannot admit this row until Wave 2 promotes it.
    """
    register_entries_count: int
    dimensions_measured: bool
    completed_at_utc: str


@dataclass(frozen=True)
class B3DimensionSetWave_v1:
    """Wave 2 output: full B3 dimension set + defensibility matrix + sensitivity class.

    Owner verbatim (SO §6.9 amendment §6 item 8): 'the full B3 dimension
    set with the defensibility matrix and sensitivity classification'.
    - b3_attachment_markedness: detection layer output per Canon 4 §5.1.
    - b3_genre_form: detection layer output (event-anchored vs monologic).
    - b3_corroboration: detection layer output (independent-unit corroboration).
    - defensibility_matrix_rule_ref: qmatrix rule reference producing the
      defensibility class (Canon 4 §5.1 verdict layer).
    - sensitivity_class: CP-C1 sensitivity classification (Canon 4 §5.1
      + Canon 7 §3 conservative default when no manifest).
    """
    b3_attachment_markedness: float
    b3_genre_form: str
    b3_corroboration: float
    defensibility_matrix_rule_ref: str
    sensitivity_class: str
    completed_at_utc: str


@dataclass(frozen=True)
class PerceptionPathwayWave_v1:
    """Wave 3 output: perception-pathway hand-off + LID overlay from first run.

    lid_overlay_source_registration MUST be one of the CP-SO-6.9-LID-WAVE
    sealed registrations (WHISPER_LID_REGISTRATION or VOXLINGUA107_REGISTRATION).
    lid_overlay_marker MUST be 'INFERRED' at Wave 3 exit — B5.4
    shown-not-counted line preserved by construction; regime promotion is
    a receipted act (canon 8 §4 W2) landed in the sealed LID module.
    """
    lid_overlay_source_registration: LidModelRegistration_v1
    lid_overlay_marker: Literal["INFERRED", "unmeasured"]
    completed_at_utc: str


@dataclass(frozen=True)
class WaveOpenReceipt_v1:
    """Structural receipt of a wave-open event at the boundary."""
    name: str
    opened_after: Optional[str]


@dataclass(frozen=True)
class CensusThreeWavesCensusAutonomyRegistration_v1:
    """Registration record wiring the three-wave census into Census Autonomy Service.

    Ruling (b) AKKI-RUNS-IT verbatim: pod is never data path. Both refs
    must resolve outside pod://* + /app/* prefixes.
    """
    engine_response_queue_ref: str
    data_source_adapter_ref: str


# ---------------------------------------------------------------------------
# Boundary callables
# ---------------------------------------------------------------------------


def open_wave(name: str, prior_wave_completed: Optional[str]) -> WaveOpenReceipt_v1:
    """Open one of the three waves at the boundary.

    Refuses:
    - name not in CENSUS_THREE_WAVES → CensusWaveNameRefused.
    - Wave N with prior_wave_completed != CENSUS_THREE_WAVES[N-1] →
      CensusWaveOutOfOrderError.
    """
    if name not in CENSUS_THREE_WAVES:
        raise CensusWaveNameRefused(
            f"unknown wave name {name!r}; must be one of {CENSUS_THREE_WAVES}"
        )
    idx = CENSUS_THREE_WAVES.index(name)
    if idx == 0:
        # Wave 1 opens without prior wave.
        return WaveOpenReceipt_v1(name=name, opened_after=None)
    expected_prior = CENSUS_THREE_WAVES[idx - 1]
    if prior_wave_completed != expected_prior:
        raise CensusWaveOutOfOrderError(
            f"wave {name!r} requires prior wave {expected_prior!r} completed; "
            f"got prior_wave_completed={prior_wave_completed!r}"
        )
    return WaveOpenReceipt_v1(name=name, opened_after=expected_prior)


def lid_overlay_source_is_sealed_registration(source: object) -> bool:
    """Return True iff `source` is one of the sealed CP-SO-6.9-LID-WAVE registrations.

    Identity-check against sealed module singletons (WHISPER_LID_REGISTRATION,
    VOXLINGUA107_REGISTRATION). Fabricated shape-equivalent objects are refused.
    """
    return source is WHISPER_LID_REGISTRATION or source is VOXLINGUA107_REGISTRATION


def register_census_three_waves_as_census_autonomy_job(
    engine_response_queue_ref: str,
    data_source_adapter_ref: str,
) -> CensusThreeWavesCensusAutonomyRegistration_v1:
    """Wire the three-wave census into Census Autonomy Service.

    Ruling (b) AKKI-RUNS-IT verbatim: refuses any pod://* or /app/*
    prefixed ref on either arm. E1 wires the seam; pod is never data path.
    """
    for ref, label in (
        (engine_response_queue_ref, "engine_response_queue_ref"),
        (data_source_adapter_ref, "data_source_adapter_ref"),
    ):
        for prefix in _POD_REF_PREFIXES:
            if ref.startswith(prefix):
                raise PodIsNeverDataPathError(
                    f"{label}={ref!r} starts with reserved prefix {prefix!r}; "
                    f"pod is never data path (Ruling (b) AKKI-RUNS-IT verbatim)"
                )
    return CensusThreeWavesCensusAutonomyRegistration_v1(
        engine_response_queue_ref=engine_response_queue_ref,
        data_source_adapter_ref=data_source_adapter_ref,
    )
