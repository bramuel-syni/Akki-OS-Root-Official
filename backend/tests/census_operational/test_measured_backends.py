"""Measured backends satisfy the existing §4.3 / §4.4 audio-plane seams and are registered as ratified by owner direction."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'vendored' / 'extraction_akki' / 'backend'))
os.environ.setdefault('MEDIA_ACOUSTICS_MAX_SECONDS', '5400')
from services.audio_plane_v1 import acoustic_observables as ao  # noqa: E402
from services.audio_plane_v1 import measured_backends as mb  # noqa: E402
from services.audio_plane_v1.backend_registry import assert_seam_has_ratified_backend, list_ratified_backends  # noqa: E402
from services.audio_plane_v1.channel_condition_profiler import derive_channel_condition_profile  # noqa: E402
from services.audio_plane_v1.language_identifier import AudioSegment  # noqa: E402
from services.audio_plane_v1.synthesis_attribute_capturer import capture_synthesis_attributes  # noqa: E402

FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures' / 'audio' / 'speech_librivox_heartofamystery_20s.ogg'


@pytest.fixture(scope='module')
def profiles():
    return {'seg-1': ao.measure_file(str(FIXTURE))}


def test_channel_condition_seam_accepts_measured_backend(profiles):
    backend = mb.MeasuredChannelConditionBackend(profiles.get)
    [profile] = derive_channel_condition_profile(segments=[AudioSegment(segment_ref='seg-1', duration_s=20.0)], backend=backend)
    assert profile.channel_condition in {'studio', 'field', 'telephone_band'}
    assert profile.backend_name == 'measured_dsp_v1.channel_condition'
    assert isinstance(profile.transmission_artefacts, tuple)


def test_synthesis_seam_receives_three_measured_families(profiles):
    backend = mb.MeasuredSynthesisAttributeBackend(profiles.get)
    [bundle] = capture_synthesis_attributes(segments=[AudioSegment(segment_ref='seg-1', duration_s=20.0)], backend=backend)
    assert len(bundle.pitch_statistics) == 5 and bundle.pitch_statistics[0] > 0
    assert len(bundle.energy_contours) == 5 and bundle.energy_contours[0] <= bundle.energy_contours[-1]
    assert len(bundle.duration_patterns) == 4


def test_unmeasured_segment_is_refused_not_invented(profiles):
    backend = mb.MeasuredChannelConditionBackend(profiles.get)
    with pytest.raises(mb.ProfileUnavailableError):
        derive_channel_condition_profile(segments=[AudioSegment(segment_ref='never-measured', duration_s=1.0)], backend=backend)


def test_registry_lists_three_ratified_seams():
    ratified = list_ratified_backends(registry=mb.MEASURED_REGISTRY)
    assert {e.seam_name for e in ratified} == {'channel_condition', 'synthesis_attributes', 'general_classification_signature'}
    assert all(e.canon_anchor == mb.OWNER_DIRECTION and e.ratified_at_utc for e in ratified)
    for seam in ('channel_condition', 'synthesis_attributes'):
        assert_seam_has_ratified_backend(registry=mb.MEASURED_REGISTRY, seam_name=seam)
