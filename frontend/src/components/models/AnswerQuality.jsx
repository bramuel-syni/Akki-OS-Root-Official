import React, { useCallback, useEffect, useState } from 'react';
import { apiRequest, stamp, statusClass } from './useModelApproval';

const pct = v => (v == null ? '—' : `${Math.round(v * 100)}%`);
const CLASSES = { reference: 'Reference questions', unanswerable: 'Unanswerable figures', out_of_scope: 'Off-subject questions', weak_match: 'Loosely matching questions', fresh: 'Missing data slices' };

function Summary({ run }) {
  const s = run.summary;
  if (!s) return null;
  const b = s.buckets;
  return <>
    <div className="estate-tiles" data-testid="answer-quality-tiles">
      <div className="estate-tile sage"><b>{pct(s.pass_rate)}</b><small>checks passed</small><small>{s.passed} of {s.tasks} tasks</small></div>
      <div className="estate-tile"><b>{pct(s.reference_hit_rate)}</b><small>reference units cited</small><small>{pct(s.reference_retrieval_rate)} retrieved into the window</small></div>
      <div className="estate-tile"><b>{s.latency_ms?.p50 != null ? `${(s.latency_ms.p50 / 1000).toFixed(1)} s` : '—'}</b><small>typical answer time</small><small>slowest in 20: {s.latency_ms?.p95 != null ? `${(s.latency_ms.p95 / 1000).toFixed(1)} s` : '—'}</small></div>
      <div className={`estate-tile ${s.source_dispatches ? 'brass' : 'sage'}`}><b>{s.source_dispatches}</b><small>estate reads</small><small>{s.paths.warm} answered from qualified data · {s.paths.fresh_or_refused} drafted or refused</small></div>
    </div>
    <ul className="estate-legend" style={{ marginTop: 12 }} data-testid="answer-quality-buckets">
      {[['Answered', b.answered, 'var(--sage)'], ['Answered in part', b.narrow, 'var(--brass)'], ['Refused', b.refused, 'var(--ink3)'], ['Data slice drafted', b.fresh, 'var(--blue)'], ['Held', b.held, 'var(--oxblood)'], ['Timed out', b.timeout, 'var(--oxblood)'], ['Errors', b.error, 'var(--oxblood)']]
        .map(([label, n, color]) => <li key={label}><i style={{ background: color }} />{label}<small>{n}</small></li>)}
    </ul>
    <ul className="estate-list" data-testid="answer-quality-classes">
      {Object.entries(s.by_class).map(([key, c]) => <li key={key}><span><b>{CLASSES[key] || key}</b><small>{c.passed} of {c.tasks} passed</small></span><small><span className={`estate-status ${c.passed === c.tasks ? 'complete' : 'partial'}`}>{pct(c.tasks ? c.passed / c.tasks : null)}</span></small></li>)}
    </ul>
    <div className="estate-note">Model tokens used: {s.tokens.in.toLocaleString('en-GB')} in · {s.tokens.out.toLocaleString('en-GB')} out. Working-memory hits {pct(s.memory.hit_ratio)}. {s.accounted ? 'Every task is accounted for.' : 'Accounting mismatch — review the run.'}</div>
  </>;
}

export function AnswerQuality({ signedIn, canRun }) {
  const [state, setState] = useState({ rows: null, error: null, starting: false });
  const load = useCallback(async () => {
    try { const body = await apiRequest('/api/chat/evaluations'); setState(s => ({ ...s, rows: body.rows, error: null })); }
    catch (error) { setState(s => ({ ...s, error: error.message })); }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const running = (state.rows || []).some(r => r.state === 'running');
  useEffect(() => { if (!running) return undefined; const t = setInterval(load, 15000); return () => clearInterval(t); }, [running, load]);
  const start = async () => {
    setState(s => ({ ...s, starting: true, error: null }));
    try { await apiRequest('/api/chat/evaluations', { method: 'POST', body: JSON.stringify({ size: 200 }) }); await load(); }
    catch (error) { setState(s => ({ ...s, error: error.message })); }
    setState(s => ({ ...s, starting: false }));
  };
  const rows = state.rows || [];
  const latest = rows[0];
  return <section className="estate-section" data-testid="answer-quality">
    <div className="estate-head"><div><h2>Answer quality</h2><p>Each run asks the governed answerer real questions built from your qualified data and checks that the right record is cited, that nothing is invented, and that off-subject questions are refused.</p></div>
      {canRun && <button className="estate-btn" onClick={start} disabled={state.starting || running} data-testid="answer-quality-run">{running ? 'Run in progress…' : state.starting ? 'Starting…' : 'Run 200-question check'}</button>}</div>
    {state.error && <div className="estate-note" role="alert" data-testid="answer-quality-error">{state.error}</div>}
    {state.rows && !rows.length && <div className="estate-note" data-testid="answer-quality-empty">No answer-quality run on record yet.</div>}
    {latest && <div data-testid="answer-quality-latest">
      <div className="estate-note"><span className={`estate-status ${latest.state === 'completed' ? 'complete' : latest.state === 'running' ? 'partial' : 'blocked'}`} data-testid="answer-quality-state">{latest.state}</span>{' '}
        {latest.completed_tasks} of {latest.planned || latest.requested} questions · started {stamp(latest.created_at)}{latest.finished_at ? ` · finished ${stamp(latest.finished_at)}` : ''}{latest.resumed ? ` · resumed ${latest.resumed}×` : ''}{latest.reason ? ` · ${latest.reason}` : ''}</div>
      <Summary run={latest} />
    </div>}
    {rows.length > 1 && <ul className="estate-list" data-testid="answer-quality-history">{rows.slice(1).map(r => <li key={r.evaluation_id}><span><b>{stamp(r.created_at)}</b><small>{r.completed_tasks} questions · {r.summary ? `${pct(r.summary.pass_rate)} passed · ${pct(r.summary.reference_hit_rate)} references cited` : r.reason || 'no summary'}</small></span><small><span className={`estate-status ${statusClass(r.state === 'completed' ? 'PASS' : r.state === 'running' ? 'partial' : 'FAIL')}`}>{r.state}</span></small></li>)}</ul>}
  </section>;
}
