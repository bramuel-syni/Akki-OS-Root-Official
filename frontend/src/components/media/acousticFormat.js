export const CLASS_NAMES = { speech: 'Speech', music: 'Music', mixed: 'Speech and music', noise: 'Noise', silence: 'Silence' };
export const CHAINS = [['wave', 'Wave'], ['frequency', 'Frequency'], ['tone', 'Tone'], ['energy', 'Energy and rhythm'], ['timbre', 'Timbre'], ['channel', 'Channel']];
export const CHARTS = new Set(['long_term_spectrum_db', 'energy_contour_1s_dbfs', 'pitch_class_profile', 'band_energy_ratios', 'mfcc_mean', 'mfcc_std', 'analysis_sample_rate_hz', 'noise_floor_method', 'channel_condition_basis']);
export const formatDuration = s => s == null ? '—' : `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
export const humanize = v => v == null ? '—' : String(v).replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());

export function formatValue(value, unit, key) {
  if (key === 'duration_seconds' && typeof value === 'number') return formatDuration(value);
  if (key === 'source_channels' && typeof value === 'number') return value === 1 ? 'Mono' : value === 2 ? 'Stereo' : `${value} channels`;
  if (value == null) return key === 'mains_hum_hz' ? 'None detected' : 'Not measurable here';
  if (Array.isArray(value)) return value.length ? value.map(v => formatValue(v, unit)).join(' · ') : 'None detected';
  if (typeof value === 'object') return `${formatValue(value.p50, unit)} (${formatValue(value.p10, unit)} – ${formatValue(value.p90, unit)})`;
  if (typeof value === 'string') return humanize(value);
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  switch (unit) {
    case 'Hz': return value >= 10000 ? `${(value / 1000).toFixed(1)} kHz` : `${Math.round(value)} Hz`;
    case 'dB': case 'dBFS': case 'dB/octave': return `${value.toFixed(1)} ${unit}`;
    case 'ratio': return `${(value * 100).toFixed(value < 0.01 && value > 0 ? 2 : 0)}%`;
    case 's': return `${value.toFixed(2)} s`;
    case 'm': return `${value.toFixed(2)} m`;
    case 'BPM': return `${Math.round(value)} BPM`;
    case 'semitones': case 'semitones/frame': return `${value.toFixed(1)} st`;
    case 'crossings/s': case '1/s': return `${value.toFixed(1)} per s`;
    case '1/min': return `${value.toFixed(1)} per min`;
    case 'index 0–1': return value.toFixed(2);
    default: return Number.isInteger(value) ? String(value) : value.toFixed(2);
  }
}

