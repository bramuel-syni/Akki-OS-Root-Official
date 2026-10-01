"""Measured sound observables: every quantity Akki reads off a recorded waveform.

Chain: wave -> frequency -> tone -> energy/rhythm -> timbre -> channel.
Streaming DSP (numpy/scipy) over 16 kHz mono blocks; bounded memory; deterministic.
Methods follow Scheirer & Slaney (1997) speech/music cues, eGeMAPS voice descriptors,
ITU-T narrowband (300-3400 Hz) and ITU-R BS.1770 level conventions where applicable.
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import time
from collections.abc import Iterator

import numpy as np
from scipy.fft import irfft, rfft
from scipy.signal import get_window

SR = 16000
FRAME = 512
HOP = 256
FPS = SR / HOP
PITCH_FRAME = 1024
LTAS_FRAME = 4096
BLOCK_SECONDS = 30
SPEED_OF_SOUND = 343.0
WINDOW_SECONDS = 4.0
PROFILE_VERSION = 'measured_dsp_v1'
EPS = 1e-10

FREQS = np.fft.rfftfreq(FRAME, 1 / SR)
LTAS_FREQS = np.fft.rfftfreq(LTAS_FRAME, 1 / SR)
BANDS = (('sub_bass', 20, 60), ('bass', 60, 250), ('low_mid', 250, 500), ('mid', 500, 2000),
         ('upper_mid', 2000, 4000), ('presence', 4000, 6000), ('brilliance', 6000, 8000))
F_MIN, F_MAX = 60.0, 500.0
LAG_MIN, LAG_MAX = int(SR / F_MAX), int(SR / F_MIN)

REGISTER = [
    ('wave', 'duration_seconds', 'Duration', 's', 'decoded sample count / sample rate'),
    ('wave', 'source_sample_rate_hz', 'Source sample rate', 'Hz', 'container header'),
    ('wave', 'source_channels', 'Source channels', 'count', 'container header'),
    ('wave', 'peak_dbfs', 'Peak level', 'dBFS', 'max |x| over all samples'),
    ('wave', 'rms_dbfs', 'Average level', 'dBFS', '20·log10 of RMS over active frames'),
    ('wave', 'crest_factor_db', 'Crest factor', 'dB', 'peak minus RMS'),
    ('wave', 'dynamic_range_db', 'Dynamic range', 'dB', 'p95 minus p5 of frame RMS (32 ms frames)'),
    ('wave', 'noise_floor_dbfs', 'Noise floor', 'dBFS', 'p5 of frame RMS'),
    ('wave', 'snr_estimate_db', 'Signal-to-noise estimate', 'dB', 'p95 frame RMS minus noise floor'),
    ('wave', 'silence_ratio', 'Silence share', 'ratio', 'frames within 6 dB of the noise floor'),
    ('wave', 'low_energy_frame_ratio', 'Low-energy frame share', 'ratio', 'frames below 50% of the 1 s mean RMS (Scheirer & Slaney)'),
    ('wave', 'clipping_ratio', 'Clipped samples', 'ratio', '|x| ≥ 0.999'),
    ('wave', 'dc_offset', 'DC offset', 'ratio', 'mean sample value'),
    ('wave', 'zero_crossing_rate_hz', 'Zero-crossing rate', 'crossings/s', 'sign changes per second per frame'),
    ('frequency', 'spectral_centroid_hz', 'Spectral centroid', 'Hz', 'power-weighted mean frequency'),
    ('frequency', 'centroid_wavelength_m', 'Centroid wavelength', 'm', '343 m/s ÷ centroid'),
    ('frequency', 'spectral_bandwidth_hz', 'Spectral spread', 'Hz', 'power-weighted std around centroid'),
    ('frequency', 'spectral_rolloff95_hz', 'Spectral rolloff (95%)', 'Hz', 'frequency below which 95% of power lies'),
    ('frequency', 'effective_bandwidth_hz', 'Effective bandwidth', 'Hz', '99% of long-term spectrum energy'),
    ('frequency', 'spectral_flatness', 'Spectral flatness', 'ratio', 'geometric ÷ arithmetic mean of power'),
    ('frequency', 'spectral_entropy', 'Spectral entropy', 'ratio', 'normalised Shannon entropy of power'),
    ('frequency', 'spectral_flux', 'Spectral flux', 'ratio', 'L2 change of normalised spectrum between frames'),
    ('frequency', 'spectral_tilt_db_per_octave', 'Spectral tilt', 'dB/octave', 'regression on long-term spectrum 100–8000 Hz'),
    ('frequency', 'alpha_ratio_db', 'Alpha ratio', 'dB', 'energy 50–1000 Hz vs 1–5 kHz (eGeMAPS)'),
    ('frequency', 'hammarberg_index_db', 'Hammarberg index', 'dB', 'peak 0–2 kHz minus peak 2–5 kHz (eGeMAPS)'),
    ('frequency', 'telephone_band_energy_ratio', 'Telephone-band energy share', 'ratio', 'energy within 300–3400 Hz'),
    ('frequency', 'cutoff_drop_db', 'Cut-off drop above 3.4 kHz', 'dB', 'long-term level 2.8–3.3 kHz minus 4.5–6 kHz'),
    ('frequency', 'low_cut_drop_db', 'Low-cut drop below 250 Hz', 'dB', 'long-term level 500–1000 Hz minus 100–250 Hz'),
    ('frequency', 'noise_floor_minstat_dbfs', 'Noise floor (spectral valleys)', 'dBFS', 'quietest fifth of per-bin minimum-statistics power, 60 Hz–8 kHz, as white-noise equivalent'),
    ('frequency', 'snr_minstat_db', 'Signal-to-noise (minimum statistics)', 'dB', 'long-term level minus minimum-statistics floor'),
    ('frequency', 'band_energy_ratios', 'Band energy shares', 'ratio', 'seven named bands 20 Hz–8 kHz'),
    ('frequency', 'mains_hum_hz', 'Mains hum', 'Hz', '50/60 Hz line prominence in long-term spectrum'),
    ('frequency', 'mains_hum_prominence_db', 'Mains hum prominence', 'dB', 'best 50/60 Hz harmonic set above its spectral neighbours'),
    ('tone', 'f0_median_hz', 'Pitch (median)', 'Hz', 'normalised autocorrelation, 60–500 Hz, voiced frames'),
    ('tone', 'f0_p10_hz', 'Pitch (10th percentile)', 'Hz', 'voiced frames'),
    ('tone', 'f0_p90_hz', 'Pitch (90th percentile)', 'Hz', 'voiced frames'),
    ('tone', 'f0_range_semitones', 'Pitch range', 'semitones', 'p90 ÷ p10 in semitones'),
    ('tone', 'f0_std_semitones', 'Pitch variability', 'semitones', 'std of log pitch'),
    ('tone', 'voiced_ratio', 'Voiced share', 'ratio', 'frames with harmonic periodicity'),
    ('tone', 'harmonicity', 'Harmonicity', 'ratio', 'mean autocorrelation peak on voiced frames'),
    ('tone', 'pitch_jump_semitones', 'Pitch movement', 'semitones/frame', 'mean |Δ| between consecutive voiced frames'),
    ('tone', 'sustained_tone_ratio', 'Sustained-tone share', 'ratio', 'voiced frames holding ±0.3 semitone for ≥130 ms'),
    ('tone', 'pitch_class_entropy', 'Pitch-class spread', 'ratio', 'entropy of 12-bin chroma (1 = even)'),
    ('tone', 'stable_partial_ratio', 'Stable partials', 'ratio', 'spectral peaks holding within ±1 bin for ≥100 ms'),
    ('energy', 'modulation_4hz_ratio', 'Syllable-rate modulation', 'ratio', 'envelope energy 2–8 Hz ÷ 0.5–20 Hz'),
    ('energy', 'modulation_peak_hz', 'Envelope modulation peak', 'Hz', 'dominant envelope rhythm'),
    ('energy', 'onset_rate_per_s', 'Onsets per second', '1/s', 'peaks of half-wave rectified spectral flux'),
    ('energy', 'tempo_bpm', 'Tempo estimate', 'BPM', 'onset-envelope autocorrelation 40–200 BPM'),
    ('energy', 'pulse_clarity', 'Pulse clarity', 'ratio', 'normalised autocorrelation peak at the tempo lag'),
    ('energy', 'energy_contour_dbfs', 'Energy contour', 'dBFS', 'p5/p25/p50/p75/p95 of frame RMS'),
    ('energy', 'voiced_run_mean_s', 'Voiced run length', 's', 'mean duration of continuous voiced stretches'),
    ('energy', 'pause_mean_s', 'Pause length', 's', 'mean duration of silent gaps ≥ 150 ms'),
    ('energy', 'pause_rate_per_min', 'Pauses per minute', '1/min', 'silent gaps ≥ 150 ms'),
    ('energy', 'syllable_rate_proxy_hz', 'Syllable-rate proxy', 'Hz', 'envelope peaks per active second (2–10 Hz band)'),
    ('timbre', 'mfcc_mean', 'MFCC mean (13)', 'coef', '40 mel bands, DCT-II'),
    ('timbre', 'mfcc_std', 'MFCC variability (13)', 'coef', 'std over frames'),
    ('timbre', 'brightness', 'Brightness', 'ratio', 'energy above 1.5 kHz ÷ total'),
    ('timbre', 'arousal_proxy', 'Arousal proxy', 'index 0–1', 'uncalibrated blend of level variance, tempo, brightness and pitch variability'),
    ('channel', 'channel_condition', 'Channel condition', 'class', 'studio / field / telephone_band'),
    ('channel', 'background_class', 'Background', 'class', 'quiet / steady_noise / fluctuating_noise / hum'),
    ('channel', 'transmission_artefacts', 'Transmission artefacts', 'list', 'clipping, dc_offset, band_limited, mains_hum, low_sample_rate'),
]

_window = get_window('hann', FRAME, fftbins=True).astype(np.float32)
_pitch_window = get_window('hann', PITCH_FRAME, fftbins=True).astype(np.float32)
_ltas_window = get_window('hann', LTAS_FRAME, fftbins=True).astype(np.float32)


def _mel_filterbank(n_mels=40, fmin=40.0, fmax=SR / 2):
    mel = lambda f: 2595 * np.log10(1 + f / 700)
    points = 700 * (10 ** (np.linspace(mel(fmin), mel(fmax), n_mels + 2) / 2595) - 1)
    bins = np.floor((FRAME + 1) * points / SR).astype(int)
    bank = np.zeros((n_mels, len(FREQS)), dtype=np.float32)
    for m in range(1, n_mels + 1):
        lo, mid, hi = bins[m - 1], bins[m], bins[m + 1]
        if mid == lo: mid += 1
        if hi == mid: hi += 1
        bank[m - 1, lo:mid] = (np.arange(lo, mid) - lo) / (mid - lo)
        bank[m - 1, mid:hi] = (hi - np.arange(mid, hi)) / (hi - mid)
    return bank


_MEL = _mel_filterbank()
_DCT = np.array([[math.cos(math.pi / 40 * (n + 0.5) * k) for n in range(40)] for k in range(13)], dtype=np.float32)
_CHROMA_MASK = (FREQS >= 60) & (FREQS <= 4000)
_CHROMA_CLASS = np.where(_CHROMA_MASK, (np.round(12 * np.log2(np.maximum(FREQS, 1) / 440.0)) + 69).astype(int) % 12, -1)


class DecodeError(Exception):
    pass


def _ffmpeg():
    import shutil
    found = os.environ.get('AKKI_FFMPEG') or shutil.which('ffmpeg')
    if found: return found
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _probe(stderr: str):
    info = {}
    m = re.search(r'Audio: .*?(\d+) Hz, ([^,]+)', stderr)
    if m:
        info['source_sample_rate_hz'] = int(m.group(1))
        layout = m.group(2).strip()
        info['source_channels'] = {'mono': 1, 'stereo': 2}.get(layout, int(re.match(r'(\d+)', layout).group(1)) if re.match(r'\d', layout) else None)
    m = re.search(r'Duration: (\d+):(\d+):(\d+\.?\d*)', stderr)
    if m:
        info['container_duration_seconds'] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return info


def decode_blocks(path: str, max_seconds: float) -> tuple[dict, Iterator[np.ndarray]]:
    """Yield float32 mono 16 kHz blocks via static ffmpeg; soundfile fallback."""
    cmd = [_ffmpeg(), '-nostdin', '-nostats', '-v', 'info', '-i', path, '-t', str(max_seconds), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    header = {}

    def blocks():
        size = SR * BLOCK_SECONDS * 4
        while True:
            chunk = proc.stdout.read(size)
            if not chunk: break
            yield np.frombuffer(chunk, dtype=np.float32)
        proc.stdout.close()
        err = proc.stderr.read().decode('utf-8', 'replace')
        proc.wait()
        header.update(_probe(err))
        if proc.returncode != 0 and not header:
            raise DecodeError('The audio could not be decoded')
    return header, blocks()


def _frames(x: np.ndarray, size: int, hop: int) -> np.ndarray:
    n = 1 + (len(x) - size) // hop if len(x) >= size else 0
    if n <= 0: return np.empty((0, size), dtype=np.float32)
    idx = np.arange(size)[None, :] + hop * np.arange(n)[:, None]
    return x[idx]


class Accumulator:
    def __init__(self):
        self.n_samples = 0; self.peak = 0.0; self.clipped = 0; self.dc_sum = 0.0
        self.rms_db = []; self.zcr = []; self.centroid = []; self.bandwidth = []; self.rolloff = []
        self.flatness = []; self.entropy = []; self.flux = []; self.onset = []; self.chroma = []; self.stable = []
        self.mfcc_sum = np.zeros(13); self.mfcc_sq = np.zeros(13); self.mfcc_n = 0
        self.f0 = []; self.ac_peak = []
        self.ltas = np.zeros(len(LTAS_FREQS)); self.ltas_n = 0; self.ltas_min = np.full(len(LTAS_FREQS), np.inf)
        self._prev_spec = None; self._carry = np.zeros(0, dtype=np.float32); self._pitch_carry = np.zeros(0, dtype=np.float32)
        self._ltas_carry = np.zeros(0, dtype=np.float32)

    def push(self, block: np.ndarray):
        self.n_samples += len(block)
        self.peak = max(self.peak, float(np.max(np.abs(block))) if len(block) else 0.0)
        self.clipped += int(np.count_nonzero(np.abs(block) >= 0.999)); self.dc_sum += float(np.sum(block, dtype=np.float64))
        x = np.concatenate([self._carry, block]); frames = _frames(x, FRAME, HOP)
        used = len(frames) * HOP; self._carry = x[used:]
        if len(frames): self._spectral(frames)
        xp = np.concatenate([self._pitch_carry, block]); pf = _frames(xp, PITCH_FRAME, HOP)
        self._pitch_carry = xp[len(pf) * HOP:]
        if len(pf): self._pitch(pf)
        xl = np.concatenate([self._ltas_carry, block]); lf = _frames(xl, LTAS_FRAME, LTAS_FRAME // 2)
        self._ltas_carry = xl[len(lf) * (LTAS_FRAME // 2):]
        if len(lf):
            spec = np.abs(rfft(lf * _ltas_window, axis=1)) ** 2
            self.ltas += spec.sum(axis=0); self.ltas_n += len(lf)
            k = min(8, len(spec)); cs = np.cumsum(np.vstack([np.zeros((1, spec.shape[1])), spec]), axis=0)
            smooth = (cs[k:] - cs[:-k]) / k
            self.ltas_min = np.minimum(self.ltas_min, smooth.min(axis=0))

    def _spectral(self, frames):
        rms = np.sqrt(np.mean(frames ** 2, axis=1) + EPS)
        self.rms_db.append(20 * np.log10(rms))
        self.zcr.append(np.mean(np.abs(np.diff(np.signbit(frames).astype(np.int8), axis=1)), axis=1) * SR)
        spec = np.abs(rfft(frames * _window, axis=1)).astype(np.float32); power = spec ** 2
        total = power.sum(axis=1) + EPS
        centroid = (power * FREQS).sum(axis=1) / total
        self.centroid.append(centroid)
        self.bandwidth.append(np.sqrt((power * (FREQS - centroid[:, None]) ** 2).sum(axis=1) / total))
        cum = np.cumsum(power, axis=1) / total[:, None]
        self.rolloff.append(FREQS[np.argmax(cum >= 0.95, axis=1)])
        logp = np.log(power + EPS)
        self.flatness.append(np.exp(logp.mean(axis=1)) / (power.mean(axis=1) + EPS))
        p = power / total[:, None]
        self.entropy.append(-(p * np.log(p + EPS)).sum(axis=1) / math.log(power.shape[1]))
        norm = spec / (spec.sum(axis=1, keepdims=True) + EPS)
        prev = self._prev_spec if self._prev_spec is not None else norm[:1]
        shifted = np.vstack([prev, norm[:-1]])
        self.flux.append(np.sqrt(((norm - shifted) ** 2).sum(axis=1)))
        comp = np.log1p(spec * 100); prev_c = np.vstack([np.log1p(prev * 100) if self._prev_spec is not None else comp[:1], comp[:-1]])
        self.onset.append(np.maximum(comp - prev_c, 0).sum(axis=1))
        self._prev_spec = norm[-1:]
        db = 10 * np.log10(power + EPS); floor = np.median(db, axis=1, keepdims=True) + 12
        peaks = np.zeros_like(db, dtype=bool)
        peaks[:, 1:-1] = (db[:, 1:-1] > db[:, :-2]) & (db[:, 1:-1] >= db[:, 2:]) & (db[:, 1:-1] > floor) & (FREQS[1:-1] >= 60)
        stable = peaks.copy()
        for i in range(1, 7):
            nxt = peaks[i:]; dil = nxt.copy(); dil[:, 1:] |= nxt[:, :-1]; dil[:, :-1] |= nxt[:, 1:]
            stable[:-i] &= dil; stable[-i:] = False
        counts = peaks.sum(axis=1); self.stable.append(np.where(counts > 0, stable.sum(axis=1) / np.maximum(counts, 1), 0.0).astype(np.float32))
        chroma = np.zeros((len(frames), 12), dtype=np.float32)
        for k in range(12): chroma[:, k] = power[:, _CHROMA_CLASS == k].sum(axis=1)
        self.chroma.append(chroma)
        mel = np.log(power @ _MEL.T + EPS); mfcc = mel @ _DCT.T
        self.mfcc_sum += mfcc.sum(axis=0); self.mfcc_sq += (mfcc ** 2).sum(axis=0); self.mfcc_n += len(mfcc)

    def _pitch(self, frames):
        w = frames * _pitch_window; w = w - w.mean(axis=1, keepdims=True)
        spec = rfft(w, n=2 * PITCH_FRAME, axis=1); ac = irfft(spec * np.conj(spec), axis=1)[:, :PITCH_FRAME]
        r0 = ac[:, :1] + EPS; norm = ac / r0
        seg = norm[:, LAG_MIN:LAG_MAX + 1]
        lag = np.argmax(seg, axis=1) + LAG_MIN; peak = seg[np.arange(len(seg)), lag - LAG_MIN]
        self.f0.append((SR / lag).astype(np.float32)); self.ac_peak.append(peak.astype(np.float32))


def _pct(a, q): return float(np.percentile(a, q)) if len(a) else None
def _r(v, d=3): return None if v is None or (isinstance(v, float) and not math.isfinite(v)) else round(float(v), d)


def _runs(mask):
    if not len(mask): return []
    edges = np.flatnonzero(np.diff(np.concatenate([[0], mask.astype(np.int8), [0]])))
    return [(s, e) for s, e in zip(edges[::2], edges[1::2])]


def _mod_spectrum(rms_db):
    env = 10 ** (rms_db / 20); env = env / (env.mean() + EPS) - 1
    if len(env) < 32 or not np.any(env): return 0.0, None
    spec = np.abs(rfft(env * get_window('hann', len(env)))) ** 2; f = np.fft.rfftfreq(len(env), 1 / FPS)
    band = (f >= 0.5) & (f <= 20); syl = (f >= 2) & (f <= 8)
    tot = spec[band].sum() + EPS
    return float(spec[syl].sum() / tot), float(f[band][np.argmax(spec[band])]) if band.any() else None


def _sustained(voiced, semis, span=None, tolerance=0.75):
    """Share of voiced frames inside a ≥130 ms stretch whose pitch range stays within tolerance."""
    span = span or int(0.13 * FPS)
    if len(voiced) < span or not voiced.any(): return 0.0
    from numpy.lib.stride_tricks import sliding_window_view
    v = sliding_window_view(voiced, span).all(axis=1)
    s = sliding_window_view(semis, span); ok = v & ((s.max(axis=1) - s.min(axis=1)) <= tolerance)
    covered = np.convolve(ok.astype(np.int32), np.ones(span, dtype=np.int32)) > 0
    return float(np.sum(covered[:len(voiced)] & voiced) / voiced.sum())


def _gate(rms):
    """Frame activity gate: pauses exist when the median sits well above the floor; otherwise an absolute gate."""
    floor = _pct(rms, 5); pauses = (_pct(rms, 50) - floor) >= 15
    return (floor if pauses else _pct(rms, 1)), ((floor + 6) if pauses else -60.0), pauses


def _pulse(onset):
    onset = onset - onset.mean()
    if len(onset) < int(FPS * 2) or not np.any(onset): return None, 0.0
    spec = rfft(onset, n=2 * len(onset)); ac = irfft(spec * np.conj(spec))[:len(onset)]
    ac = ac / (ac[0] + EPS); lo, hi = int(FPS * 60 / 200), int(FPS * 60 / 40)
    if hi >= len(ac): return None, 0.0
    lag = int(np.argmax(ac[lo:hi])) + lo
    return 60.0 * FPS / lag, float(max(ac[lag], 0.0))


def _hum(ltas):
    db = 10 * np.log10(ltas + EPS); found = None; best = 0.0
    for base in (50, 60):
        prom = []
        for h in (1, 2, 3):
            f = base * h; i = int(np.argmin(np.abs(LTAS_FREQS - f)))
            neigh = np.concatenate([db[max(i - 6, 0):i - 2], db[i + 3:i + 7]])
            if len(neigh): prom.append(db[i] - np.median(neigh))
        score = float(np.mean(prom)) if prom else 0.0
        if score > best: best, found = score, base
    return found if best >= 12 else None, _r(best, 1)


def _window_cues(fr, voiced, semis, gate_db):
    """Cues over one analysis window of frame indices; returns class scores."""
    rms = fr['rms']; active = float(np.mean(rms > gate_db))
    if active < 0.15 or np.mean(rms) < -60: return {'silence': 1.0, 'speech': 0.0, 'music': 0.0, 'noise': 0.0}, {'active': active}
    mod4, _ = _mod_spectrum(rms); tempo, clarity = _pulse(fr['onset'])
    env = 10 ** (rms / 20); mean_rms = np.convolve(env, np.ones(int(FPS)) / int(FPS), mode='same')
    low_energy = float(np.mean(env < 0.5 * mean_rms))
    vr = float(np.mean(voiced)); harm = float(np.mean(fr['ac'][voiced])) if voiced.any() else 0.0
    dv = np.abs(np.diff(semis)); both = voiced[1:] & voiced[:-1]; jump = float(np.mean(dv[both])) if both.any() else 0.0
    sus = _sustained(voiced, semis)
    ch = fr['chroma'].sum(axis=0); p = ch / (ch.sum() + EPS); ch_ent = float(-(p * np.log(p + EPS)).sum() / math.log(12))
    flat = float(np.median(fr['flat'])); flux_std = float(np.std(fr['flux'])); zcr_cv = float(np.std(fr['zcr']) / (np.mean(fr['zcr']) + EPS))
    act = rms > gate_db
    partials = float(np.mean(fr['stable'][act])) if act.any() else 0.0
    dyn = float(np.percentile(rms[act], 95) - np.percentile(rms[act], 5)) if act.sum() > 4 else 0.0
    chroma_n = fr['chroma'] / (np.linalg.norm(fr['chroma'], axis=1, keepdims=True) + EPS)
    pair = act[1:] & act[:-1]; chroma_stab = float(np.mean(np.sum(chroma_n[1:] * chroma_n[:-1], axis=1)[pair])) if pair.any() else 0.0
    sig = lambda v, c, w: 1 / (1 + math.exp(-(v - c) / w))
    speech = (1.1 * sig(low_energy, 0.3, 0.07) + 1.0 * (1 - sig(partials, 0.2, 0.05)) + 0.9 * (1 - sig(clarity, 0.38, 0.06)) + 0.8 * sig(mod4, 0.55, 0.06)
              + 0.7 * (1 - sig(sus, 0.4, 0.1)) + 0.6 * sig(dyn, 26, 3) + 0.6 * (1 - sig(chroma_stab, 0.85, 0.04)) + 0.5 * sig(zcr_cv, 0.6, 0.15)
              + 0.5 * sig(jump, 0.35, 0.12) + 0.4 * sig(vr, 0.2, 0.08) * (1 - sig(vr, 0.85, 0.05)))
    music = (1.8 * sig(clarity, 0.38, 0.06) + 1.5 * sig(partials, 0.2, 0.05) + 1.2 * sig(sus, 0.45, 0.1) + 1.0 * sig(chroma_stab, 0.85, 0.04)
             + 0.8 * (1 - sig(low_energy, 0.25, 0.07)) + 0.6 * (1 - sig(dyn, 18, 3)) + 0.6 * (1 - sig(mod4, 0.5, 0.06))
             + 0.5 * sig(harm, 0.7, 0.06) + 0.3 * (1 - sig(zcr_cv, 0.6, 0.15)) + 0.3 * (1 - sig(jump, 0.35, 0.12)))
    noise = (1.6 * sig(flat, 0.3, 0.07) + 1.0 * (1 - sig(vr, 0.08, 0.03)) + 0.8 * (1 - sig(flux_std, 0.05, 0.015)) + 0.6 * (1 - sig(clarity, 0.25, 0.08))
             + 0.6 * (1 - sig(zcr_cv, 0.4, 0.1)) + 0.6 * (1 - sig(partials, 0.15, 0.05)))
    raw = {'speech': speech, 'music': music, 'noise': noise}; total = sum(raw.values()) + EPS
    scores = {k: v / total for k, v in raw.items()}; scores['silence'] = 0.0
    cues = {'active': active, 'modulation_4hz_ratio': mod4, 'low_energy_frame_ratio': low_energy, 'dynamic_range_db': dyn, 'stable_partial_ratio': partials,
            'chroma_stability': chroma_stab, 'voiced_ratio': vr, 'harmonicity': harm, 'pitch_jump_semitones': jump, 'sustained_tone_ratio': sus,
            'pitch_class_entropy': ch_ent, 'pulse_clarity': clarity, 'tempo_bpm': tempo, 'spectral_flatness': flat, 'spectral_flux_std': flux_std, 'zcr_cv': zcr_cv}
    return scores, {k: _r(v) for k, v in cues.items()}


def finalize(acc: Accumulator, header: dict, elapsed: float, truncated: bool) -> dict:
    if acc.n_samples < SR // 2:
        raise DecodeError('Less than half a second of audio was decoded')
    rms = np.concatenate(acc.rms_db); n = len(rms)
    def cat(parts, length=n):
        a = np.concatenate(parts) if parts else np.zeros(0); return a[:length] if len(a) >= length else np.pad(a, (0, length - len(a)), constant_values=a[-1] if len(a) else 0)
    zcr, cen, bw, roll, flat, ent, flux, onset, stable = (cat(acc.zcr), cat(acc.centroid), cat(acc.bandwidth), cat(acc.rolloff), cat(acc.flatness), cat(acc.entropy), cat(acc.flux), cat(acc.onset), cat(acc.stable))
    chroma = np.concatenate(acc.chroma)[:n]
    f0 = cat(acc.f0); ac = cat(acc.ac_peak)
    noise_floor, gate_db, has_pauses = _gate(rms); active = rms > gate_db
    voiced = (ac > 0.6) & (rms > ((noise_floor + 10) if has_pauses else gate_db)) & (f0 >= F_MIN) & (f0 <= F_MAX)
    semis = 12 * np.log2(np.maximum(f0, 1) / 440.0)
    duration = acc.n_samples / SR
    fr = {'rms': rms, 'onset': onset, 'ac': ac, 'chroma': chroma, 'flat': flat, 'flux': flux, 'zcr': zcr, 'stable': stable}
    step = int(WINDOW_SECONDS * FPS); timeline = []; tally = {'speech': 0, 'music': 0, 'noise': 0, 'silence': 0}
    for start in range(0, n, step):
        sl = slice(start, min(start + step, n))
        if sl.stop - sl.start < step // 2 and timeline: break
        scores, cues = _window_cues({k: v[sl] for k, v in fr.items()}, voiced[sl], semis[sl], gate_db)
        label = max(scores, key=scores.get); tally[label] += 1
        timeline.append({'start_s': _r(start / FPS, 1), 'end_s': _r(sl.stop / FPS, 1), 'reads_as': label, 'confidence': _r(scores[label], 2),
                         'scores': {k: _r(v, 2) for k, v in scores.items()}, 'cues': cues})
    windows = max(len(timeline), 1); shares = {k: round(v / windows, 3) for k, v in tally.items()}
    sounding = 1 - shares['silence'] or EPS
    sp, mu = shares['speech'] / sounding, shares['music'] / sounding
    if shares['silence'] >= 0.9: reads = 'silence'
    elif sp >= 0.2 and mu >= 0.2: reads = 'mixed'
    elif sp >= mu and sp >= shares['noise'] / sounding: reads = 'speech'
    elif mu >= shares['noise'] / sounding: reads = 'music'
    else: reads = 'noise'
    confidence = min(1.0, {'silence': shares['silence'], 'mixed': min(sp, mu) * 2, 'speech': sp, 'music': mu, 'noise': shares['noise'] / sounding}[reads])
    vf0 = f0[voiced]; both = voiced[1:] & voiced[:-1]; dv = np.abs(np.diff(semis))
    sustained = _sustained(voiced, semis)
    vruns = [(e - s) / FPS for s, e in _runs(voiced)]; pauses = [(e - s) / FPS for s, e in _runs(~active) if (e - s) / FPS >= 0.15]
    mod4, mod_peak = _mod_spectrum(rms); tempo, clarity = _pulse(onset)
    env = 10 ** (rms / 20); mean1s = np.convolve(env, np.ones(int(FPS)) / int(FPS), mode='same')
    sm = np.convolve(env, np.ones(5) / 5, mode='same'); peaks = (sm[1:-1] > sm[:-2]) & (sm[1:-1] > sm[2:]) & (sm[1:-1] > noise_floor_lin(noise_floor) * 2)
    active_seconds = max(float(active.sum()) / FPS, EPS)
    onset_thr = onset.mean() + onset.std(); onsets = int(np.sum((onset[1:-1] > onset[:-2]) & (onset[1:-1] >= onset[2:]) & (onset[1:-1] > onset_thr)))
    ltas = acc.ltas / max(acc.ltas_n, 1); ltas_db = 10 * np.log10(ltas + EPS)
    cum = np.cumsum(ltas) / (ltas.sum() + EPS); eff_bw = float(LTAS_FREQS[np.argmax(cum >= 0.99)])
    fit = (LTAS_FREQS >= 100) & (LTAS_FREQS <= 8000); tilt = float(np.polyfit(np.log2(LTAS_FREQS[fit]), ltas_db[fit], 1)[0])
    alpha = 10 * math.log10((ltas[(LTAS_FREQS >= 50) & (LTAS_FREQS < 1000)].sum() + EPS) / (ltas[(LTAS_FREQS >= 1000) & (LTAS_FREQS <= 5000)].sum() + EPS))
    hamm = float(ltas_db[(LTAS_FREQS <= 2000)].max() - ltas_db[(LTAS_FREQS > 2000) & (LTAS_FREQS <= 5000)].max())
    hum_hz, hum_prom = _hum(ltas)
    bandsum = lambda lo, hi, src=ltas: float(src[(LTAS_FREQS >= lo) & (LTAS_FREQS < hi)].sum())
    whole = bandsum(0, SR) + EPS
    tel = bandsum(300, 3400.1) / whole; tel_core = bandsum(300, 3400.1) / (bandsum(60, SR) + EPS); brightness = bandsum(1500, SR) / whole
    level = lambda lo, hi: float(np.mean(ltas_db[(LTAS_FREQS >= lo) & (LTAS_FREQS < hi)]))
    cutoff_drop = level(2800, 3300) - level(4500, 6000); lowcut_drop = level(500, 1000) - level(100, 250)
    to_dbfs = lambda power_sum: 10 * math.log10(2 * power_sum / (LTAS_FRAME ** 2 * 0.375) + EPS)
    ltas_min = np.where(np.isfinite(acc.ltas_min), acc.ltas_min, 0.0)
    valley = np.sort(ltas_min[LTAS_FREQS >= 60]); floor_psd = float(np.median(valley[:max(len(valley) // 5, 1)]))
    floor_minstat = to_dbfs(floor_psd * len(valley)); level_ltas = to_dbfs(bandsum(60, SR)); snr_minstat = level_ltas - floor_minstat
    peak_db = 20 * math.log10(acc.peak + EPS); rms_active = float(20 * np.log10(np.sqrt(np.mean(env[active] ** 2)) + EPS)) if active.any() else float(np.mean(rms))
    dc = acc.dc_sum / acc.n_samples; clip = acc.clipped / acc.n_samples
    src_sr = header.get('source_sample_rate_hz')
    band_limited = cutoff_drop >= 30 and (tel_core >= 0.9 or lowcut_drop >= 15)
    artefacts = [a for a, hit in (('clipping', clip > 1e-4), ('dc_offset', abs(dc) > 0.01), ('band_limited', band_limited),
                                  (f'mains_hum_{hum_hz}hz' if hum_hz else '', bool(hum_hz)), ('low_sample_rate', bool(src_sr and src_sr < 16000))) if hit and a]
    floor_var = float(np.std(rms[~active])) if (~active).any() else 0.0
    snr = (_pct(rms, 95) - noise_floor) if has_pauses else snr_minstat
    if hum_hz: background = 'hum'
    elif not has_pauses: background = 'continuous_sound'
    elif noise_floor < -65: background = 'quiet'
    elif floor_var < 3: background = 'steady_noise'
    else: background = 'fluctuating_noise'
    clean = not hum_hz and clip <= 1e-4 and abs(dc) <= 0.01
    if band_limited: condition, basis = 'telephone_band', 'steep cut above 3.4 kHz with the 300–3400 Hz band carrying the energy'
    elif clean and has_pauses and noise_floor < -58 and snr > 35: condition, basis = 'studio', 'pause noise floor below −58 dBFS with >35 dB signal-to-noise'
    elif clean and not has_pauses and floor_minstat < -55 and snr_minstat > 35: condition, basis = 'studio', 'no pauses; minimum-statistics floor below −55 dBFS with >35 dB signal-to-noise'
    else: condition, basis = 'field', 'audible floor, artefacts or low signal-to-noise'
    mstd = np.sqrt(np.maximum(acc.mfcc_sq / max(acc.mfcc_n, 1) - (acc.mfcc_sum / max(acc.mfcc_n, 1)) ** 2, 0))
    chroma_tot = chroma[active].sum(axis=0) if active.any() else chroma.sum(axis=0); pc = chroma_tot / (chroma_tot.sum() + EPS)
    f0_std = float(np.std(12 * np.log2(vf0 / 440.0))) if len(vf0) else None
    arousal = float(np.clip(0.3 * min(float(np.std(rms[active])) / 12, 1) + 0.25 * (min((tempo or 0) / 180, 1) * clarity) + 0.25 * min(brightness / 0.5, 1) + 0.2 * min((f0_std or 0) / 6, 1), 0, 1)) if active.any() else 0.0
    observables = {
        'wave': {'duration_seconds': _r(duration, 2), 'source_sample_rate_hz': src_sr, 'source_channels': header.get('source_channels'),
                 'analysis_sample_rate_hz': SR, 'peak_dbfs': _r(peak_db, 2), 'rms_dbfs': _r(rms_active, 2), 'crest_factor_db': _r(peak_db - rms_active, 2),
                 'dynamic_range_db': _r(_pct(rms, 95) - _pct(rms, 5), 2), 'noise_floor_dbfs': _r(noise_floor, 2),
                 'noise_floor_method': 'pause_frames' if has_pauses else 'lower_envelope_no_pauses', 'snr_estimate_db': _r(snr, 2),
                 'silence_ratio': _r(1 - float(np.mean(active))), 'low_energy_frame_ratio': _r(float(np.mean(env < 0.5 * mean1s))),
                 'clipping_ratio': _r(clip, 6), 'dc_offset': _r(dc, 5), 'zero_crossing_rate_hz': _stats(zcr[active] if active.any() else zcr, 0)},
        'frequency': {'spectral_centroid_hz': _stats(cen[active] if active.any() else cen, 0), 'centroid_wavelength_m': _r(SPEED_OF_SOUND / max(float(np.median(cen[active] if active.any() else cen)), 1), 3),
                      'spectral_bandwidth_hz': _stats(bw, 0), 'spectral_rolloff95_hz': _stats(roll, 0), 'effective_bandwidth_hz': _r(eff_bw, 0),
                      'spectral_flatness': _stats(flat), 'spectral_entropy': _stats(ent), 'spectral_flux': _stats(flux), 'spectral_tilt_db_per_octave': _r(tilt, 2),
                      'alpha_ratio_db': _r(alpha, 2), 'hammarberg_index_db': _r(hamm, 2), 'telephone_band_energy_ratio': _r(tel), 'cutoff_drop_db': _r(cutoff_drop, 1),
                      'low_cut_drop_db': _r(lowcut_drop, 1), 'noise_floor_minstat_dbfs': _r(floor_minstat, 1), 'snr_minstat_db': _r(snr_minstat, 1),
                      'band_energy_ratios': {name: _r(bandsum(lo, hi) / whole) for name, lo, hi in BANDS}, 'mains_hum_hz': hum_hz, 'mains_hum_prominence_db': hum_prom,
                      'long_term_spectrum_db': [_r(v, 1) for v in np.interp(np.geomspace(40, 8000, 48), LTAS_FREQS[1:], ltas_db[1:])]},
        'tone': {'f0_median_hz': _r(_pct(vf0, 50), 1), 'f0_p10_hz': _r(_pct(vf0, 10), 1), 'f0_p90_hz': _r(_pct(vf0, 90), 1),
                 'f0_range_semitones': _r(12 * math.log2(_pct(vf0, 90) / _pct(vf0, 10)), 2) if len(vf0) and _pct(vf0, 10) > 0 else None,
                 'f0_std_semitones': _r(f0_std, 2), 'voiced_ratio': _r(float(np.mean(voiced))), 'harmonicity': _r(float(np.mean(ac[voiced])) if voiced.any() else None),
                 'pitch_jump_semitones': _r(float(np.mean(dv[both])) if both.any() else None), 'sustained_tone_ratio': _r(sustained),
                 'pitch_class_entropy': _r(float(-(pc * np.log(pc + EPS)).sum() / math.log(12))), 'pitch_class_profile': [_r(v) for v in pc],
                 'stable_partial_ratio': _r(float(np.mean(stable[active])) if active.any() else 0.0)},
        'energy': {'modulation_4hz_ratio': _r(mod4), 'modulation_peak_hz': _r(mod_peak, 2), 'onset_rate_per_s': _r(onsets / active_seconds, 2),
                   'tempo_bpm': _r(tempo, 1), 'pulse_clarity': _r(clarity), 'energy_contour_dbfs': [_r(_pct(rms, q), 1) for q in (5, 25, 50, 75, 95)],
                   'energy_contour_1s_dbfs': [_r(v, 1) for v in 20 * np.log10(np.array([np.sqrt(np.mean(env[i:i + int(FPS)] ** 2)) for i in range(0, n - int(FPS) + 1, int(FPS))] or [np.sqrt(np.mean(env ** 2))]) + EPS)][:3600],
                   'voiced_run_mean_s': _r(float(np.mean(vruns)) if vruns else None, 3), 'pause_mean_s': _r(float(np.mean(pauses)) if pauses else None, 3),
                   'pause_rate_per_min': _r(len(pauses) / (duration / 60), 2), 'syllable_rate_proxy_hz': _r(int(peaks.sum()) / active_seconds, 2)},
        'timbre': {'mfcc_mean': [_r(v, 3) for v in acc.mfcc_sum / max(acc.mfcc_n, 1)], 'mfcc_std': [_r(v, 3) for v in mstd], 'brightness': _r(brightness), 'arousal_proxy': _r(arousal)},
        'channel': {'channel_condition': condition, 'channel_condition_basis': basis, 'background_class': background, 'transmission_artefacts': artefacts},
    }
    return {'profile_version': PROFILE_VERSION, 'backend_name': PROFILE_VERSION, 'analysis_band_hz': [0, SR // 2], 'frame_ms': round(1000 * FRAME / SR, 1),
            'hop_ms': round(1000 * HOP / SR, 1), 'frames': int(n), 'compute_seconds': _r(elapsed, 2), 'truncated': truncated,
            'observables': observables,
            'signature': {'reads_as': reads, 'confidence': _r(confidence, 2), 'window_shares': shares, 'windows': windows, 'window_seconds': WINDOW_SECONDS,
                          'method': 'heuristic cue scoring per 4 s window; not a trained model', 'timeline': timeline}}


def noise_floor_lin(db): return 10 ** (db / 20)


def _stats(a, d=3):
    a = np.asarray(a)
    if not len(a): return None
    return {'mean': _r(float(np.mean(a)), d), 'std': _r(float(np.std(a)), d), 'p10': _r(_pct(a, 10), d), 'p50': _r(_pct(a, 50), d), 'p90': _r(_pct(a, 90), d)}


def measure_file(path: str, *, max_seconds: float | None = None) -> dict:
    limit = max_seconds or float(os.environ['MEDIA_ACOUSTICS_MAX_SECONDS'])
    started = time.monotonic(); header, blocks = decode_blocks(path, limit)
    acc = Accumulator(); total = 0
    for block in blocks:
        acc.push(block); total += len(block)
    container = header.get('container_duration_seconds')
    truncated = bool(container and container > limit + 0.5)
    return finalize(acc, header, time.monotonic() - started, truncated)


def register() -> list[dict]:
    return [{'chain': c, 'key': k, 'label': l, 'unit': u, 'method': m} for c, k, l, u, m in REGISTER]


FEATURE_PATHS = ('wave.rms_dbfs', 'wave.crest_factor_db', 'wave.dynamic_range_db', 'wave.silence_ratio', 'wave.low_energy_frame_ratio',
                 'wave.zero_crossing_rate_hz.p50', 'wave.zero_crossing_rate_hz.std', 'frequency.spectral_centroid_hz.p50', 'frequency.spectral_centroid_hz.std',
                 'frequency.spectral_bandwidth_hz.p50', 'frequency.spectral_rolloff95_hz.p50', 'frequency.effective_bandwidth_hz', 'frequency.spectral_flatness.p50',
                 'frequency.spectral_entropy.p50', 'frequency.spectral_flux.p50', 'frequency.spectral_flux.std', 'frequency.spectral_tilt_db_per_octave',
                 'frequency.alpha_ratio_db', 'frequency.hammarberg_index_db', 'frequency.telephone_band_energy_ratio', 'tone.f0_median_hz', 'tone.f0_range_semitones',
                 'tone.f0_std_semitones', 'tone.voiced_ratio', 'tone.harmonicity', 'tone.pitch_jump_semitones', 'tone.sustained_tone_ratio', 'tone.pitch_class_entropy',
                 'tone.stable_partial_ratio', 'energy.modulation_4hz_ratio', 'energy.modulation_peak_hz', 'energy.onset_rate_per_s', 'energy.tempo_bpm',
                 'energy.pulse_clarity', 'energy.voiced_run_mean_s', 'energy.pause_mean_s', 'energy.pause_rate_per_min', 'energy.syllable_rate_proxy_hz',
                 'timbre.brightness', 'timbre.arousal_proxy')
FEATURE_NAMES = FEATURE_PATHS + tuple(f'timbre.mfcc_mean.{i}' for i in range(13)) + tuple(f'timbre.mfcc_std.{i}' for i in range(13))
WINDOW_CUES = ('modulation_4hz_ratio', 'low_energy_frame_ratio', 'dynamic_range_db', 'stable_partial_ratio', 'chroma_stability', 'voiced_ratio', 'harmonicity',
               'pitch_jump_semitones', 'sustained_tone_ratio', 'pitch_class_entropy', 'pulse_clarity', 'tempo_bpm', 'spectral_flatness', 'spectral_flux_std', 'zcr_cv')


def features(profile: dict) -> dict:
    """Flat, fixed-order scalar features of one measured profile (None where not measurable)."""
    out = {}
    for path in FEATURE_PATHS:
        node = profile['observables']
        for part in path.split('.'):
            node = node.get(part) if isinstance(node, dict) else None
        out[path] = node if isinstance(node, (int, float)) and not isinstance(node, bool) else None
    for stat in ('mfcc_mean', 'mfcc_std'):
        values = profile['observables']['timbre'].get(stat) or []
        for i in range(13): out[f'timbre.{stat}.{i}'] = values[i] if i < len(values) else None
    return out


def compact(profile: dict) -> dict:
    """Small per-file record for corpus-scale exports: reading, channel, features; no paths, no raw audio."""
    sig, channel = profile['signature'], profile['observables']['channel']
    windows = sig['timeline']
    return {'profile_version': profile['profile_version'], 'duration_s': profile['observables']['wave']['duration_seconds'], 'reads_as': sig['reads_as'],
            'confidence': sig['confidence'], 'window_shares': sig['window_shares'], 'windows': sig['windows'],
            'music_windows': sum(w['reads_as'] == 'music' for w in windows), 'speech_windows': sum(w['reads_as'] == 'speech' for w in windows),
            'channel_condition': channel['channel_condition'], 'artefacts': channel['transmission_artefacts'], 'features': features(profile)}
