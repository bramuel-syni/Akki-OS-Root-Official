"""Owner-directed measured backends for the §4.3 channel-condition and §4.4 synthesis-attribute seams.

Profiles come from `acoustic_observables.measure_file`; only the segment_ref crosses the seam.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping

from services.audio_plane_v1 import acoustic_observables as ao
from services.audio_plane_v1.backend_registry import BackendRegistrySurface, register_backend

OWNER_DIRECTION = 'owner-direction:2026-10-01:measured-sound-observables'
RATIFIED_AT = '2026-10-01T00:00:00+00:00'
ProfileLookup = Callable[[str], Mapping[str, Any]]


class ProfileUnavailableError(LookupError):
    """No measured profile exists for the segment_ref."""


def _profile(lookup: ProfileLookup, segment_ref: str) -> Mapping[str, Any]:
    profile = lookup(segment_ref)
    if not profile or 'observables' not in profile:
        raise ProfileUnavailableError(f'no measured profile for segment_ref={segment_ref!r}')
    return profile


class MeasuredChannelConditionBackend:
    backend_name = f'{ao.PROFILE_VERSION}.channel_condition'

    def __init__(self, lookup: ProfileLookup):
        self._lookup = lookup

    def derive(self, segment_ref: str, duration_s: float) -> Mapping[str, Any]:
        channel = _profile(self._lookup, segment_ref)['observables']['channel']
        return {'channel_condition': channel['channel_condition'], 'transmission_artefacts': list(channel['transmission_artefacts']),
                'background_class': channel['background_class']}


class MeasuredSynthesisAttributeBackend:
    backend_name = f'{ao.PROFILE_VERSION}.synthesis_attributes'

    def __init__(self, lookup: ProfileLookup):
        self._lookup = lookup

    def capture(self, segment_ref: str, duration_s: float) -> Mapping[str, Any]:
        observables = _profile(self._lookup, segment_ref)['observables']
        tone, energy = observables['tone'], observables['energy']
        return {'pitch_statistics': [tone['f0_median_hz'] or 0.0, tone['f0_p10_hz'] or 0.0, tone['f0_p90_hz'] or 0.0, tone['f0_std_semitones'] or 0.0, tone['voiced_ratio']],
                'energy_contours': list(energy['energy_contour_dbfs']),
                'duration_patterns': [energy['voiced_run_mean_s'] or 0.0, energy['pause_mean_s'] or 0.0, energy['pause_rate_per_min'], energy['syllable_rate_proxy_hz']]}


def _registry() -> BackendRegistrySurface:
    registry = BackendRegistrySurface(entries=())
    for seam, name in (('channel_condition', MeasuredChannelConditionBackend.backend_name),
                       ('synthesis_attributes', MeasuredSynthesisAttributeBackend.backend_name),
                       ('general_classification_signature', f'{ao.PROFILE_VERSION}.signature')):
        registry = register_backend(registry=registry, seam_name=seam, backend_name=name, ratification_state='ratified',
                                    canon_anchor=OWNER_DIRECTION, ratified_at_utc=RATIFIED_AT)
    return registry


MEASURED_REGISTRY = _registry()
