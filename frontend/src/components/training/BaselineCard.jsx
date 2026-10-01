import React, { useState } from 'react';
import { Gauge } from 'lucide-react';
import { pct } from './useTrainingLab';

const Metric = ({ label, value, testId }) => <div className="lab-metric" data-testid={testId}><dt>{label}</dt><dd>{value}</dd></div>;

const Baseline = ({ title, block, testId }) => block && <section className="lab-baseline" data-testid={testId}>
  <h4>{title}</h4><p className="lab-method">{block.method}</p>
  <dl>
    <Metric label="Accuracy" value={pct(block.accuracy)} testId={`${testId}-accuracy`} />
    <Metric label="Finds music (recall)" value={pct(block.recall)} testId={`${testId}-recall`} />
    <Metric label="Right when it says music (precision)" value={pct(block.precision)} testId={`${testId}-precision`} />
    <Metric label="Clears non-music (specificity)" value={pct(block.specificity)} testId={`${testId}-specificity`} />
  </dl>
  {block.accuracy_bootstrap && <p className="lab-footnote">Resampled accuracy {pct(block.accuracy_bootstrap)} over {block.accuracy_bootstrap.independent_units} recordings.</p>}
</section>;

const Result = ({ run }) => {
  const r = run.result;
  if (!r) return null;
  if (r.status !== 'complete') return <p className="lab-hold" data-testid="lab-baseline-insufficient">{r.reason}</p>;
  return <div className="lab-result" data-testid={`lab-baseline-result-${run.run_id}`}>
    <p className="lab-lede" data-testid="lab-baseline-summary"><strong>{r.items} recordings</strong> · {r.positives} with music, {r.negatives} without · {Object.entries(r.composition).map(([k, v]) => `${v} ${k.replace('·', ' from ').replace(/_/g, ' ')}`).join(' · ')}</p>
    <div className="lab-baselines"><Baseline title="Baseline 1 · the reading" block={r.baseline_reading} testId="lab-baseline-reading" /><Baseline title="Baseline 2 · learned on the measurements" block={r.baseline_learned} testId="lab-baseline-learned" /></div>
    {r.window_level && <p className="lab-footnote" data-testid="lab-baseline-windows">Per four-second window ({r.window_level.windows} windows from {r.window_level.files} recordings): reading {pct(r.window_level.reading.accuracy)}, learned {pct(r.window_level.learned_grouped_5fold.accuracy)}. {r.window_level.note}</p>}
    <details className="lab-details" data-testid="lab-baseline-drivers"><summary>What the learned baseline leans on</summary><ul>{r.drivers.map(d => <li key={d.feature}><span>{d.feature.replace(/\./g, ' · ').replace(/_/g, ' ')}</span><em>{d.direction}</em></li>)}</ul></details>
    <details className="lab-details" data-testid="lab-baseline-items"><summary>Every recording in the set</summary><table><thead><tr><th>Recording</th><th>Label</th><th>Reads as</th><th>Learned</th></tr></thead><tbody>{r.per_item.map(i => <tr key={i.item_id} className={i.reading_correct ? '' : 'miss'}><td>{i.title}</td><td>{i.label} <small>{i.label_source.replace(/_/g, ' ')}</small></td><td>{i.reads_as}</td><td>{(i.learned_probability_music * 100).toFixed(0)}% music</td></tr>)}</tbody></table></details>
    {r.corpus_test && <section className="lab-corpus-test" data-testid="lab-baseline-corpus"><h4>Test on the staged corpus · {r.corpus_test.files} recordings</h4><p className="lab-method">{r.corpus_test.reading}</p>
      <table><thead><tr><th>Language</th><th>Files</th><th>Hours</th><th>Read as music</th><th>Learned says music</th><th>Music-window share</th><th>For review</th></tr></thead>
        <tbody>{Object.entries(r.corpus_test.per_language).map(([lang, v]) => <tr key={lang}><td>{lang}</td><td>{v.files}</td><td>{v.hours}</td><td>{pct(v.read_share)}</td><td>{pct(v.learned_share)}</td><td>{(v.music_window_share * 100).toFixed(1)}%</td><td>{v.files_with_music_windows}</td></tr>)}</tbody></table></section>}
    <ul className="lab-limits" data-testid="lab-baseline-limits">{r.limitations.map(l => <li key={l}>{l}</li>)}</ul>
  </div>;
};

export const BaselineCard = ({ lab, canOperate }) => {
  const [busy, setBusy] = useState(false), [error, setError] = useState(''), [policy, setPolicy] = useState('music'), [corpusTest, setCorpusTest] = useState(true);
  const latest = lab.baselines[0];
  const run = async () => { setBusy(true); setError(''); try { await lab.post('/baselines/music', { unlabelled_library_audio: policy, include_synthetic: true, include_corpus_test: corpusTest }); } catch (e) { setError(e.message); } finally { setBusy(false); } };
  return <section className="lab-card" data-testid="lab-baseline-card">
    <header><h2><Gauge size={18} />Music identification baseline</h2><p>The number a trained detector must beat, measured on the library's labelled recordings.</p></header>
    {canOperate && <div className="lab-controls">
      <label>Unlabelled library audio<select value={policy} onChange={e => setPolicy(e.target.value)} data-testid="lab-baseline-policy"><option value="music">Count as music (owner declaration)</option><option value="excluded">Leave out</option></select></label>
      <label className="lab-check"><input type="checkbox" checked={corpusTest} onChange={e => setCorpusTest(e.target.checked)} data-testid="lab-baseline-corpus-toggle" />Test on the staged corpus when measured</label>
      <button className="estate-btn primary" onClick={run} disabled={busy} data-testid="lab-baseline-run">{busy ? 'Starting…' : 'Run baseline'}</button>
    </div>}
    {error && <p className="media-error" role="alert" data-testid="lab-baseline-error">{error}</p>}
    {!latest && <p className="media-note" data-testid="lab-baseline-empty">No baseline yet.</p>}
    {latest && <article className="lab-run" data-testid="lab-baseline-latest">
      <p className="lab-status" data-testid="lab-baseline-status">{latest.status === 'waiting_measurements' ? `Waiting · ${latest.hold_reason}` : latest.status === 'complete' ? `Established ${new Date(latest.finished_at).toLocaleString()}` : latest.status}</p>
      {latest.reference_set?.pending?.length > 0 && <p className="lab-footnote">Still measuring: {latest.reference_set.pending.map(p => p.title).join(' · ')}</p>}
      <Result run={latest} />
    </article>}
    {lab.baselines.length > 1 && <p className="lab-footnote" data-testid="lab-baseline-history">{lab.baselines.length - 1} earlier {lab.baselines.length === 2 ? 'run' : 'runs'} kept.</p>}
  </section>;
};
