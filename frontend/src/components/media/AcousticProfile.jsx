import React from 'react';
import { CHAINS, CHARTS, CLASS_NAMES, formatDuration, formatValue, humanize } from './acousticFormat';
import { SoundCharts } from './SoundCharts';

const Timeline = ({ timeline }) => <div className="sound-timeline" data-testid="work-media-sound-timeline" role="img" aria-label="How each four-second window reads">
  {timeline.map(w => <span key={w.start_s} className={`sound-window ${w.reads_as}`} style={{ flex: w.end_s - w.start_s }} title={`${formatDuration(w.start_s)}–${formatDuration(w.end_s)} · ${CLASS_NAMES[w.reads_as]} ${(w.confidence * 100).toFixed(0)}%`} />)}
</div>;

const Signature = ({ signature, human }) => <section className="sound-signature" data-testid="work-media-sound-signature">
  <p className="sound-reads" data-testid="work-media-sound-reads-as">Reads as <strong>{CLASS_NAMES[signature.reads_as]}</strong><span data-testid="work-media-sound-confidence">{(signature.confidence * 100).toFixed(0)}% of the sounding windows</span></p>
  {human && <p className="sound-human" data-testid="work-media-sound-human-label">Human-reviewed label: {CLASS_NAMES[human]}{human === signature.reads_as ? ' · agrees' : ' · differs'}</p>}
  <Timeline timeline={signature.timeline} />
  <ul className="sound-shares" data-testid="work-media-sound-shares">{Object.entries(signature.window_shares).filter(([, v]) => v > 0).map(([k, v]) => <li key={k} className={k}><i /> {CLASS_NAMES[k]} {(v * 100).toFixed(0)}%</li>)}</ul>
</section>;

const Chain = ({ chain, title, values, labels }) => {
  const rows = Object.entries(values).filter(([k, v]) => !CHARTS.has(k) && v !== undefined);
  return <section className="sound-chain" data-testid={`work-media-sound-chain-${chain}`}>
    <h3>{title}</h3>
    <dl>{rows.map(([k, v]) => { const meta = labels[k] || {}; return <div key={k} data-testid={`work-media-sound-metric-${k}`}><dt title={meta.method || ''}>{meta.label || humanize(k)}</dt><dd>{formatValue(v, meta.unit, k)}</dd></div>; })}</dl>
    {chain === 'channel' && values.channel_condition_basis && <p className="sound-basis" data-testid="work-media-sound-channel-basis">{values.channel_condition_basis}</p>}
  </section>;
};

export const AcousticProfile = ({ profile, register, human }) => {
  const labels = Object.fromEntries((register?.observables || []).map(o => [o.key, o]));
  return <div className="sound-profile">
    <Signature signature={profile.signature} human={human} />
    <SoundCharts observables={profile.observables} />
    <div className="sound-chains">{CHAINS.map(([chain, title]) => <Chain key={chain} chain={chain} title={title} values={profile.observables[chain]} labels={labels} />)}</div>
    <p className="media-note" data-testid="work-media-sound-method">Measured on a 16 kHz mono rendering, 32 ms frames, 0–8 kHz. The reading is cue scoring over 4 s windows, not a trained model.{profile.truncated ? ' Only the first 90 minutes were measured.' : ''}</p>
  </div>;
};
