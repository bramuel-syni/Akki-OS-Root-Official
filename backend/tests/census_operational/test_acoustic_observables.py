"""Measured sound observables on SYNTHETIC signals: speech-like, music-like, silence, noise, telephone band + hum."""
import os
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'vendored' / 'extraction_akki' / 'backend'))
os.environ.setdefault('MEDIA_ACOUSTICS_MAX_SECONDS', '5400')
from services.audio_plane_v1 import acoustic_observables as ao  # noqa: E402

SR = 16000
rng = np.random.default_rng(7)


def write(tmp_path, name, x, sr=SR):
    path = tmp_path / name
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
    return str(path)


def speech_like(seconds=12, sr=SR):
    t = np.arange(int(seconds * sr)) / sr
    from scipy.signal import lfilter
    f0 = np.full(len(t), 120.0); syllables = np.zeros_like(t); frication = np.zeros_like(t); pos = 0; pieces = []
    while pos < len(t):
        length = int(sr * rng.uniform(0.12, 0.34)); seg = np.arange(min(length, len(t) - pos)); n = len(seg)
        start_semi, end_semi = rng.uniform(-4, 4), rng.uniform(-4, 4)
        jitter = lfilter(np.ones(160) / 160, [1], rng.standard_normal(n)) * 0.35
        f0[pos:pos + n] = 120 * 2 ** (np.linspace(start_semi, end_semi, n) / 12) * (1 + jitter)
        syllables[pos:pos + n] = np.sin(np.pi * seg / max(n, 1)) ** 1.5 * rng.uniform(0.5, 1.0)
        if rng.random() < 0.3: frication[pos:pos + n // 3] = rng.standard_normal(n // 3) * 0.5
        pieces.append((pos, pos + n, rng.uniform(300, 800), rng.uniform(1000, 2400)))
        pos += length
        if rng.random() < 0.18: pos += int(sr * rng.uniform(0.3, 0.9))
    phase = 2 * np.pi * np.cumsum(f0) / sr
    voice = sum(np.sin(h * phase) / h for h in range(1, 24))
    shaped = np.zeros_like(voice)
    for start, end, f1, f2 in pieces:
        chunk = voice[start:end]
        for formant in (f1, f2):
            r = np.exp(-np.pi * 90 / sr); theta = 2 * np.pi * formant / sr
            chunk = lfilter([1 - r], [1, -2 * r * np.cos(theta), r * r], chunk)
        shaped[start:end] = chunk / (np.max(np.abs(chunk)) + 1e-9)
    x = shaped * syllables + 0.4 * frication
    return 0.3 * x / np.max(np.abs(x))


def music_like(seconds=12, sr=SR, bpm=120):
    t = np.arange(int(seconds * sr)) / sr
    notes = [261.63, 329.63, 392.0]
    chord = sum(sum(np.sin(2 * np.pi * h * f * t) / h for h in range(1, 6)) for f in notes)
    env = 0.6 + 0.4 * np.sin(2 * np.pi * t / 4)
    beat = np.zeros_like(t); period = int(sr * 60 / bpm)
    for start in range(0, len(t), period):
        beat[start:start + 400] += np.exp(-np.arange(min(400, len(t) - start)) / 60) * rng.standard_normal(min(400, len(t) - start))
    x = chord * env + 1.5 * beat
    return 0.4 * x / np.max(np.abs(x))


FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures' / 'audio'


def test_register_lists_six_chains():
    chains = {row['chain'] for row in ao.register()}
    assert chains == {'wave', 'frequency', 'tone', 'energy', 'timbre', 'channel'}
    assert all(row['unit'] and row['method'] for row in ao.register())


def test_real_public_domain_speech_reads_as_speech():
    profile = ao.measure_file(str(FIXTURES / 'speech_librivox_heartofamystery_20s.ogg'))
    assert profile['signature']['reads_as'] == 'speech', profile['signature']['window_shares']
    tone = profile['observables']['tone']
    assert 80 <= tone['f0_median_hz'] <= 300 and tone['stable_partial_ratio'] < 0.25
    assert profile['observables']['wave']['low_energy_frame_ratio'] > 0.2
    assert profile['observables']['wave']['duration_seconds'] == pytest.approx(20, abs=0.2)


def test_real_public_domain_piano_reads_as_music():
    profile = ao.measure_file(str(FIXTURES / 'music_musopen_chopin_prelude_20s.ogg'))
    assert profile['signature']['reads_as'] == 'music', profile['signature']['window_shares']
    tone = profile['observables']['tone']
    assert tone['stable_partial_ratio'] > 0.35 and tone['sustained_tone_ratio'] > 0.3


def test_tonal_synthetic_voice_keeps_syllable_rhythm_measurements(tmp_path):
    profile = ao.measure_file(write(tmp_path, 'voice.wav', speech_like()))
    tone = profile['observables']['tone']
    assert 90 <= tone['f0_median_hz'] <= 160
    assert profile['observables']['energy']['syllable_rate_proxy_hz'] > 2
    assert profile['observables']['wave']['low_energy_frame_ratio'] > 0.3
    assert profile['observables']['wave']['duration_seconds'] == pytest.approx(12, abs=0.1)


def test_music_like_signal_reads_as_music_with_tempo(tmp_path):
    profile = ao.measure_file(write(tmp_path, 'music.wav', music_like()))
    assert profile['signature']['reads_as'] == 'music', profile['signature']['window_shares']
    energy = profile['observables']['energy']
    assert energy['tempo_bpm'] is not None and (abs(energy['tempo_bpm'] - 120) < 6 or abs(energy['tempo_bpm'] - 60) < 4)
    assert profile['observables']['tone']['sustained_tone_ratio'] > 0.3
    assert profile['observables']['energy']['pulse_clarity'] > 0.4


def test_silence_and_noise_are_named(tmp_path):
    silent = ao.measure_file(write(tmp_path, 'silence.wav', np.zeros(SR * 6)))
    assert silent['signature']['reads_as'] == 'silence'
    noise = ao.measure_file(write(tmp_path, 'noise.wav', 0.2 * rng.standard_normal(SR * 8)))
    assert noise['signature']['reads_as'] == 'noise'
    assert noise['observables']['frequency']['spectral_flatness']['mean'] > 0.3
    assert noise['observables']['channel']['channel_condition'] == 'field'


def test_telephone_band_and_mains_hum_are_detected(tmp_path):
    from scipy.signal import butter, sosfiltfilt
    sos = butter(10, [300, 3400], btype='band', fs=SR, output='sos')
    x = sosfiltfilt(sos, sosfiltfilt(sos, speech_like())) + 0.02 * np.sin(2 * np.pi * 50 * np.arange(SR * 12) / SR)
    profile = ao.measure_file(write(tmp_path, 'phone.wav', x))
    channel = profile['observables']['channel']
    assert channel['channel_condition'] == 'telephone_band', profile['observables']['frequency']
    assert 'band_limited' in channel['transmission_artefacts'] and 'mains_hum_50hz' in channel['transmission_artefacts']
    assert profile['observables']['frequency']['mains_hum_hz'] == 50
    assert profile['observables']['frequency']['effective_bandwidth_hz'] < 4000


def test_studio_condition_for_clean_wideband_recording(tmp_path):
    t = np.arange(SR * 12) / SR
    tones = sum(np.sin(2 * np.pi * f * t) / 3 for f in (261.63, 329.63, 392.0, 1046.5, 2093.0)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 3))
    profile = ao.measure_file(write(tmp_path, 'clean.wav', 0.5 * tones / np.max(np.abs(tones)) + 3e-5 * rng.standard_normal(SR * 12)))
    assert profile['observables']['channel']['channel_condition'] == 'studio', (profile['observables']['channel'], profile['observables']['frequency'])
    assert profile['observables']['wave']['clipping_ratio'] == 0
    assert 'band_limited' not in profile['observables']['channel']['transmission_artefacts']


def test_percussive_music_with_broadband_hits_is_not_called_telephone(tmp_path):
    profile = ao.measure_file(write(tmp_path, 'drums.wav', music_like()))
    assert profile['observables']['channel']['channel_condition'] in ('studio', 'field')
    assert 'band_limited' not in profile['observables']['channel']['transmission_artefacts']


def test_stereo_44k_source_is_resampled_and_described(tmp_path):
    t = np.arange(44100 * 3) / 44100
    stereo = np.stack([np.sin(2 * np.pi * 440 * t), np.sin(2 * np.pi * 440 * t)], axis=1)
    path = tmp_path / 'stereo.wav'
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes((stereo * 20000).astype('<i2').tobytes())
    profile = ao.measure_file(str(path))
    wave_obs = profile['observables']['wave']
    assert wave_obs['source_sample_rate_hz'] == 44100 and wave_obs['source_channels'] == 2
    assert abs(profile['observables']['tone']['f0_median_hz'] - 440) < 5
    assert profile['observables']['frequency']['centroid_wavelength_m'] == pytest.approx(343 / 440, rel=0.1)


def test_measure_is_deterministic(tmp_path):
    path = write(tmp_path, 'repeat.wav', speech_like(6))
    a, b = ao.measure_file(path), ao.measure_file(path)
    a.pop('compute_seconds'); b.pop('compute_seconds')
    assert a == b
