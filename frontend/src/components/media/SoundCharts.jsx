import React from 'react';

const Line = ({ values, testId, label, unit = 'dB' }) => {
  if (!values?.length) return null;
  const nums = values.filter(v => v != null); const min = Math.min(...nums), max = Math.max(...nums), span = max - min || 1;
  const points = values.map((v, i) => `${(i / (values.length - 1)) * 100},${v == null ? 30 : 30 - ((v - min) / span) * 28}`).join(' ');
  return <figure className="sound-chart" data-testid={testId}>
    <svg viewBox="0 0 100 32" preserveAspectRatio="none" aria-hidden="true"><polyline points={points} fill="none" stroke="#16274a" strokeWidth="1" vectorEffect="non-scaling-stroke" /></svg>
    <figcaption>{label} · {min.toFixed(0)} to {max.toFixed(0)} {unit}</figcaption>
  </figure>;
};

const BAND_NAMES = { sub_bass: 'sub', bass: 'bass', low_mid: 'low-mid', mid: 'mid', upper_mid: 'hi-mid', presence: 'pres.', brilliance: 'brill.' };
const PITCH = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B'];
const Bars = ({ entries, testId, label }) => {
  if (!entries?.length) return null;
  const max = Math.max(...entries.map(([, v]) => v || 0)) || 1;
  return <figure className="sound-chart sound-bars" data-testid={testId}>
    <div>{entries.map(([k, v]) => <span key={k} title={`${k}: ${((v || 0) * 100).toFixed(0)}%`}><i style={{ height: `${Math.max(((v || 0) / max) * 100, 2)}%` }} /><small>{k}</small></span>)}</div>
    <figcaption>{label}</figcaption>
  </figure>;
};

export const SoundCharts = ({ observables }) => <div className="sound-charts">
  <Line values={observables.frequency.long_term_spectrum_db} testId="work-media-sound-spectrum" label="Long-term spectrum, 40 Hz to 8 kHz (log axis)" />
  <Line values={observables.energy.energy_contour_1s_dbfs} testId="work-media-sound-energy-contour" label="Energy contour, one value per second" unit="dBFS" />
  <Bars entries={Object.entries(observables.frequency.band_energy_ratios || {}).map(([k, v]) => [BAND_NAMES[k] || k, v])} testId="work-media-sound-bands" label="Where the energy sits, seven bands 20 Hz to 8 kHz" />
  <Bars entries={(observables.tone.pitch_class_profile || []).map((v, i) => [PITCH[i], v])} testId="work-media-sound-chroma" label="Pitch classes carrying the energy" />
</div>;
