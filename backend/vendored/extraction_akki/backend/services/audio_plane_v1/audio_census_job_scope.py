"""services.audio_plane_v1.audio_census_job_scope — CP-M7-W2-CONTRACT-1.

Audio-census `scope` sub-carrier + `stations_owner_ratified` gate.

CP-M7-W2-CONTRACT-1 · sealed 2026-09-16 under owner steer verbatim
2026-09-16T~08:35Z ("advance the milestone frontier as far as existing
owner law allows... Do NOT cross the standing lines: no training on
estate audio, no biometric material, no enforcement hard-gate, no
speculative shapes beyond existing owner law.").

Charter from M7 W2..W9 gating triage §1 W2 buildable slice verbatim:
    "audio-census `scope` sub-carrier + `stations_owner_ratified: bool`
     gate. Extends existing services/work_supervisor/job_manifest.py
     with an audio-census `scope` sub-carrier as a frozen dataclass
     with opaque strings for station identifiers · stations_owner_
     ratified: bool = False gate that refuses mount until owner
     ratification lands."

Composition surface (case-agnostic decoupling matches CP-M7-W9-CONTRACT-1):
- `job_manifest_ref` is a caller-supplied opaque str referencing a
  services.work_supervisor.job_manifest JobManifest v0 binding; this
  module does not import that surface. Caller-side composition binds.
- `output_contract_ref` is a caller-supplied opaque str referencing a
  services.audio_plane_v1.corpus_deliverable_v1 output-contract
  target; this module does not import that surface. Caller-side
  composition binds.
- `station_refs` are caller-supplied opaque strings; no station
  identifier grammar imposed. Case-agnostic within audio-plane scope
  (station identity is a caller concern; this module carries opaque
  refs).

Preventive-charter pattern (matches CP-M8-CTCC-1 and CP-M7-W9-CONTRACT-1):
- Runtime enforcement fires only when caller invokes
  `assert_mount_allowed(scope=...)`. No global gate.
- The `stations_owner_ratified: bool = False` default MUST be flipped
  to True by the caller in a code-path anchored to a banked owner
  ratification (this is the standing line "no enforcement hard-gate"
  — the mechanism is scope-shape-frozen; runtime enforcement is a
  caller-invoked assertion, not a global refusal).

Standing lines held:
- No training on estate audio (SW-10 remains deferred; this scope
  carrier describes admissibility, not training).
- No biometric material (station_refs are opaque strings; no
  speaker/voiceprint carriers).
- No enforcement hard-gate (preventive-charter · caller invokes).
- No speculative shapes (4-field carrier corresponds directly to
  the M7 W2 buildable-slice charter: opaque station refs +
  owner-ratification gate + composition refs into job manifest and
  output contract).
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


# Verbatim anchor · required-verbatim phrase for gating invariant #6:
# "stations_owner_ratified: bool = False gate that refuses mount until
#  owner ratification lands"
AUDIO_CENSUS_SCOPE_ANCHOR = (
    "M7 W2..W9 gating triage §1 W2 verbatim: 'audio-census `scope` "
    "sub-carrier + `stations_owner_ratified: bool` gate ... "
    "stations_owner_ratified: bool = False gate that refuses mount "
    "until owner ratification lands.'"
)


class AudioCensusJobScopeRefused(Exception):
    """Root refusal class for audio_census_job_scope contract violations."""


class StationsNotOwnerRatifiedError(AudioCensusJobScopeRefused):
    """Refusal raised (when a caller invokes assert_mount_allowed) if
    the scope carrier's `stations_owner_ratified` field is False.
    Standing line preserved: no enforcement hard-gate; the caller
    invokes the assertion at its own composition boundary."""


class StationRefsEmptyError(AudioCensusJobScopeRefused):
    """Refusal raised (when a caller invokes assert_mount_allowed) if
    the scope carrier's `station_refs` tuple is empty. A zero-station
    scope carries no admissible payload."""


@dataclasses.dataclass(frozen=True)
class AudioCensusJobScope:
    """Audio-census job scope sub-carrier.

    Exact-order 4 carriers. Frozen.

    - `job_manifest_ref` (str) — opaque caller-supplied ref into a
      services.work_supervisor.job_manifest.JobManifest v0 binding.
      Case-agnostic: no ref-grammar imposed.
    - `station_refs` (Tuple[str, ...]) — opaque caller-supplied
      station identifier strings. Case-agnostic within audio-plane
      scope; no station identifier grammar imposed.
    - `stations_owner_ratified` (bool) — owner-ratification gate.
      Default False. Flipping to True is a caller responsibility
      anchored to a banked owner ratification.
    - `output_contract_ref` (str) — opaque caller-supplied ref into
      a services.audio_plane_v1.corpus_deliverable_v1 output-contract
      target (Path C default in force per §C.2; upgrade paths ride
      Ruling #5 sub-verdicts).
    """
    job_manifest_ref: str
    station_refs: Tuple[str, ...]
    stations_owner_ratified: bool
    output_contract_ref: str


def assert_mount_allowed(*, scope: AudioCensusJobScope) -> None:
    """Preventive-charter refusal wrapper.

    Fires only when caller invokes. Refuses with
    `StationRefsEmptyError` if scope.station_refs is empty; refuses
    with `StationsNotOwnerRatifiedError` if
    scope.stations_owner_ratified is False.

    Returns None on success. Does not mutate scope.
    """
    if not scope.station_refs:
        raise StationRefsEmptyError(
            "station_refs must be a non-empty tuple; got empty tuple. "
            "Audio-census scope with zero stations carries no "
            "admissible payload."
        )
    if not scope.stations_owner_ratified:
        raise StationsNotOwnerRatifiedError(
            "stations_owner_ratified is False; mount refused until "
            "owner ratifies the station selection. This is the "
            "audio-census scope gate per M7 W2 buildable-slice "
            "charter."
        )


__all__ = [
    "AUDIO_CENSUS_SCOPE_ANCHOR",
    "AudioCensusJobScope",
    "AudioCensusJobScopeRefused",
    "StationsNotOwnerRatifiedError",
    "StationRefsEmptyError",
    "assert_mount_allowed",
]
