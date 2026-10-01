# Measured sound observables — research note and implementation record (2026-10-01)

Owner direction: "research sound queryable observations or spectra that make it from wavelength to tone, to energy to
frequency — every data point that can be measured in recorded sound — registered as data where the unique patterns
associated with a particular general classification can be identified. Akki is supposed to have this capability."

## What a recorded waveform lets us measure (the chain)

| Chain | Observable | Unit | Method |
|---|---|---|---|
| Wave | duration, source sample rate/channels, peak, average level (RMS), crest factor, dynamic range, noise floor, SNR estimate, silence share, low-energy-frame share, clipping, DC offset, zero-crossing rate | s · Hz · dBFS · dB · ratio | 32 ms Hann frames, 16 ms hop, 16 kHz mono rendering |
| Frequency | spectral centroid and its wavelength (343 m/s ÷ f), spread, 95 % roll-off, effective bandwidth (99 % long-term energy), flatness, entropy, flux, spectral tilt, alpha ratio, Hammarberg index, seven band shares 20 Hz–8 kHz, telephone-band share, cut-off drop above 3.4 kHz, low-cut drop below 250 Hz, minimum-statistics floor, mains hum (50/60 Hz) | Hz · m · dB · ratio | short-time spectrum + 4096-point long-term average spectrum |
| Tone | F0 median/p10/p90, range, variability, voiced share, harmonicity, pitch movement, sustained-tone share, stable partials, 12-bin pitch-class profile and spread | Hz · semitones · ratio | normalised autocorrelation 60–500 Hz; spectral-peak continuity; chroma |
| Energy / rhythm | 2–8 Hz (syllable-rate) modulation share, modulation peak, onsets per second, tempo, pulse clarity, energy contour (percentiles and one value per second), voiced-run and pause lengths, pauses per minute, syllable-rate proxy | ratio · Hz · BPM · dBFS · s | envelope modulation spectrum; onset-envelope autocorrelation 40–200 BPM |
| Timbre | 13 MFCC means and spreads, brightness, arousal proxy (uncalibrated) | coef · ratio | 40 mel bands, DCT-II |
| Channel | channel condition {studio, field, telephone_band} with stated basis, background class, transmission artefacts | class | rules over the observables above |

Sources consulted: Scheirer & Slaney (ICASSP 1997) speech/music features (4 Hz modulation energy, low-energy frame
percentage, roll-off/centroid/flux and their variances, zero-crossing rate, pulse metric); eGeMAPS v02 descriptor set
(pitch in semitones, jitter/shimmer, HNR, alpha ratio, Hammarberg index, spectral slopes, loudness-peak rate, voiced /
unvoiced run lengths); ITU-R BS.1770 level conventions (dBFS, true-peak idea); ITU-T narrowband telephony band
300–3400 Hz. LUFS is deliberately not claimed: levels are reported as RMS dBFS on a 16 kHz rendering.

## General classification signature

Per 4 s window, cue scores for speech / music / noise are combined from: syllable-rate modulation, low-energy frame
share, stable partials, pulse clarity, sustained tones, chroma stability, dynamic range, zero-crossing variability,
pitch movement, voiced share, harmonicity, flatness, flux variability. Windows read as silence when inactive. The
file reads as speech, music, mixed (both ≥ 20 % of sounding windows), noise or silence. This is **cue scoring, not a
trained model**; the pattern register (per-class medians, 10th–90th ranges, most separating observables and agreement
with human-reviewed labels) is the calibration surface.

Validation on real recordings (not training data): three public-domain speech recordings (1908 phonograph,
two LibriVox readers) read as speech at 98–100 %; five owner songs (incl. an instrumental) and a Musopen Chopin
prelude read as music at 89–100 %; white noise reads as noise; digital silence reads as silence. Synthetic checks:
telephone band (steep 3.4 kHz cut + 50 Hz hum) → telephone_band with `band_limited` and `mains_hum_50hz`; clean
sustained tones at −90 dBFS floor → studio. Two 20 s public-domain fixtures live in `backend/tests/fixtures/audio`.

## Where it lives

- Engine: `services/audio_plane_v1/acoustic_observables.py` (numpy/scipy, streaming 30 s blocks, static ffmpeg decode
  via imageio-ffmpeg, soundfile available; ~5 s compute and ~210 MB peak for a 20-minute MP3; ~1 s for a 4-minute song).
- Seams: `services/audio_plane_v1/measured_backends.py` — concrete `ChannelConditionProfilerBackend` and
  `SynthesisAttributeCapturerBackend`, registered **ratified** under anchor
  `owner-direction:2026-10-01:measured-sound-observables` (the previous placeholders remain in their modules).
- Library jobs: `services/media_library/acoustics.py` — Mongo `media_acoustics` (one row per file, leased claims,
  one in-process daemon worker started at app startup, replay for identical bytes, re-measure on profile-version change).
- API (`/api/media`): `GET acoustics/register`, `GET acoustics`, `GET acoustics/patterns`, `GET|POST files/{id}/acoustics`,
  `POST acoustics/batch`. Watch boundary `media.acoustics`. Operator role for POST; tenant scoped.
- UI: Media library → wave icon per audio file → Sound profile dialog (reading, window timeline, spectrum, energy contour,
  band shares, pitch classes, six measurement groups); "Measure sound" on selections; "Sound patterns" register.

## Limits stated honestly

- Analysis band is 0–8 kHz (16 kHz rendering); the source sample rate is recorded but content above 8 kHz is not measured.
- Language, speaker, and mood are **not** identified: the layer produces the measurable descriptors (pitch statistics,
  prosodic rates, brightness, arousal proxy) a model would consume. The arousal proxy is uncalibrated.
- Channel condition for continuous content without pauses uses a spectral-valley floor; it cannot see a floor hidden
  under dense music. The basis string is attached to every verdict.
- Jobs run on the control-plane pod for library files (≤ 55 MB, ≤ 90 minutes measured); estate-scale runs belong on
  Akki workers through the same backend.
