import React, { useCallback, useEffect, useState } from 'react';
import { apiRequest, stamp } from './useModelApproval';

const LANE = { listener: 'Brand listener', story_text: 'Story text', story_voice: 'Invented voice' };
const STATE = { adopted: 'var(--sage)', not_yet_conditioned: 'var(--ink3)', unverified_provisional: 'var(--blue)', superseded: 'var(--oxblood)' };
const TEST = { supported: 'var(--sage)', refuted: 'var(--oxblood)', inconclusive: 'var(--ink3)', pending: 'var(--blue)' };
const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };
const chip = (text, color, testid) => <span data-testid={testid} style={{ padding: '2px 8px', borderRadius: 999, fontSize: 11, border: `1px solid ${color}`, color }}>{text}</span>;

function Hypothesis({ h, canOperate, onVerdict, onBind, busy }) {
  const [condition, setCondition] = useState(''), [delta, setDelta] = useState('');
  const test = h.test?.verdict;
  return <div data-testid={`supervisor-hypothesis-${h.hypothesis_id}`} style={{ padding: '8px 0', borderTop: '1px solid var(--line)' }}>
    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
      {chip(h.archive_state?.replace(/_/g, ' '), STATE[h.archive_state] || 'var(--ink3)', `supervisor-state-${h.hypothesis_id}`)}{chip(h.origin.replace(/_/g, ' '), 'var(--ink2)')}
      {test && chip(`test: ${test}`, TEST[test], `supervisor-test-${h.hypothesis_id}`)}{h.owner_verdict && chip(`owner: ${h.owner_verdict}`, 'var(--blue)')}
      <code style={{ fontSize: 11, color: 'var(--ink3)' }}>{h.hypothesis_id}{h.job_id ? ` · ${h.job_id}` : ''}</code>
    </div>
    <p style={{ margin: '6px 0 2px', fontSize: 12.5 }} data-testid={`supervisor-statement-${h.hypothesis_id}`}>{h.statement}</p>
    {h.change && <p className="estate-note" style={{ margin: '2px 0' }}>Change: {h.change}</p>}
    {h.prediction?.field && <p className="estate-note" style={{ margin: '2px 0' }}>Prediction: {h.prediction.field} for {h.prediction.language} {h.prediction.direction} by ≥ {h.prediction.min_delta}{h.test?.before != null ? ` · measured ${h.test.before} → ${h.test.after}` : ''}</p>}
    {Object.keys(h.recipe_delta || {}).length > 0 && <p className="estate-note" style={{ margin: '2px 0' }}>recipe_delta: <code>{JSON.stringify(h.recipe_delta)}</code></p>}
    {h.missing_condition && <p className="estate-note" style={{ margin: '2px 0', color: 'var(--ink2)' }} data-testid={`supervisor-condition-${h.hypothesis_id}`}>Waits for: {h.missing_condition}</p>}
    {!h.acceptance?.accepted && h.acceptance?.reasons?.filter(r => !r.startsWith('not yet conditioned')).length > 0 && <p className="estate-note" style={{ margin: '2px 0' }}>Acceptance point: {h.acceptance.reasons.filter(r => !r.startsWith('not yet conditioned')).join(' · ')}</p>}
    {canOperate && !h.job_id && <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center', marginTop: 6 }}>
      <button className="estate-btn" data-testid={`supervisor-adopt-${h.hypothesis_id}`} disabled={busy} onClick={() => onVerdict(h, 'adopt', 'owner adopts at the coach seat')}>Adopt</button>
      <button className="estate-btn" data-testid={`supervisor-reject-${h.hypothesis_id}`} disabled={busy} onClick={() => onVerdict(h, 'reject', 'owner rejects at the coach seat')}>Reject</button>
      <input data-testid={`supervisor-defer-condition-${h.hypothesis_id}`} style={{ ...field, maxWidth: 260 }} placeholder="Defer: name the missing condition" value={condition} onChange={e => setCondition(e.target.value)} />
      <button className="estate-btn" data-testid={`supervisor-defer-${h.hypothesis_id}`} disabled={busy || !condition.trim()} onClick={() => onVerdict(h, 'defer', 'owner defers at the coach seat', condition)}>Defer</button>
      {h.origin === 'frontier_cif' && !Object.keys(h.recipe_delta || {}).length && <>
        <input data-testid={`supervisor-bind-delta-${h.hypothesis_id}`} style={{ ...field, maxWidth: 260 }} placeholder='Bind recipe_delta JSON, e.g. {"lr": 0.00005}' value={delta} onChange={e => setDelta(e.target.value)} />
        <button className="estate-btn" data-testid={`supervisor-bind-${h.hypothesis_id}`} disabled={busy || !delta.trim()} onClick={() => onBind(h, delta)}>Bind</button></>}
    </div>}
  </div>;
}

function Lane({ lane, data, canOperate, onVerdict, onBind, busy }) {
  const [showAll, setShowAll] = useState(false);
  const g = data.gap || {}; const hyps = data.hypotheses || []; const shown = showAll ? hyps : hyps.slice(0, 6);
  return <div data-testid={`supervisor-lane-${lane}`} style={{ marginTop: 12, padding: 14, border: '1px solid var(--line)', borderRadius: 10, background: '#fff' }}>
    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'baseline' }}><h3 style={{ fontSize: 13, margin: 0 }}>{LANE[lane]}</h3>{chip(`class: ${g.class || '—'}`, 'var(--ink2)', `supervisor-class-${lane}`)}{g.worst_language && chip(`load-bearing: ${g.target_field} · ${g.worst_language}`, 'var(--oxblood)')}
      {data.intent_audit?.divergence && chip('intent divergence', 'var(--oxblood)', `supervisor-divergence-${lane}`)}</div>
    <p className="estate-note" data-testid={`supervisor-conclusion-${lane}`} style={{ marginTop: 6 }}>{g.conclusion}</p>
    <p className="estate-note" style={{ margin: '4px 0' }}>Archive: {Object.entries(data.archive || {}).map(([k, v]) => `${k.replace(/_/g, ' ')} ${v}`).join(' · ')} · Tests: {Object.entries(data.tests || {}).map(([k, v]) => `${k} ${v}`).join(' · ')}{data.rent_expired?.length ? ` · rent expired ${data.rent_expired.length}` : ''}</p>
    {data.adopted && <p className="estate-note" data-testid={`supervisor-adopted-${lane}`} style={{ margin: '4px 0', color: 'var(--ink)' }}>Running under hypothesis {data.adopted.hypothesis_id} ({data.adopted.origin.replace(/_/g, ' ')}) · {data.adopted.job_id}</p>}
    {!hyps.length && <p className="estate-note" data-testid={`supervisor-empty-${lane}`}>No hypothesis on the ledger yet — the first supervised pick is made when this lane's next iteration is dispatched.</p>}
    {shown.map(h => <Hypothesis key={h.hypothesis_id} h={h} canOperate={canOperate} onVerdict={onVerdict} onBind={onBind} busy={busy} />)}
    {hyps.length > 6 && <button className="estate-btn" data-testid={`supervisor-more-${lane}`} onClick={() => setShowAll(s => !s)}>{showAll ? 'Show fewer' : `Show all ${hyps.length}`}</button>}
  </div>;
}

// Training supervisor: Solva reading (load-bearing units → class → conclusion) over the CIF hypothesis ledger; the owner's coach seat adopts, rejects, defers, binds or originates.
export function TrainingSupervisor({ canOperate }) {
  const [data, setData] = useState(null), [error, setError] = useState(null), [busy, setBusy] = useState(false), [notice, setNotice] = useState(null);
  const [lane, setLane] = useState('listener'), [statement, setStatement] = useState(''), [delta, setDelta] = useState('');
  const load = useCallback(() => apiRequest('/api/training/malpha/supervisor').then(setData).catch(e => setError(e.message)), []);
  useEffect(() => { load(); }, [load]);
  const act = async (fn) => { setBusy(true); setError(null); setNotice(null); try { await fn(); await load(); } catch (e) { setError(e.message); } setBusy(false); };
  const onVerdict = (h, verdict, reason, missing_condition) => act(() => apiRequest(`/api/training/malpha/supervisor/hypotheses/${h.hypothesis_id}/verdict`, { method: 'POST', body: JSON.stringify({ verdict, reason, missing_condition }) }));
  const onBind = (h, json) => act(async () => { await apiRequest(`/api/training/malpha/supervisor/hypotheses/${h.hypothesis_id}/bind`, { method: 'POST', body: JSON.stringify({ recipe_delta: JSON.parse(json) }) }); });
  const originate = () => act(async () => { const r = await apiRequest('/api/training/malpha/supervisor/hypotheses', { method: 'POST', body: JSON.stringify({ lane, statement, recipe_delta: JSON.parse(delta) }) }); setNotice(r.hypothesis.acceptance?.accepted ? `Hypothesis ${r.hypothesis.hypothesis_id} accepted; it competes at the next free device.` : `Refused at the acceptance point: ${(r.hypothesis.acceptance?.reasons || []).join(' · ')}`); setStatement(''); setDelta(''); });
  const lanes = data?.lanes || {};
  return <section className="estate-section" data-testid="training-supervisor" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Training supervisor · Solva + CIF</h2>
      <p>Every dispatched iteration runs under one hypothesis with a measured prediction. Solva reads the load-bearing units and classes the conclusion (dev labels are transcript-derived → “was stated”, never fact); CIF keeps the ideas — the measurement rule, frontier-reviewed experiments and yours — with manifests, archive states and rent, and only the deterministic acceptance point lets one through. Floors (0.90/0.90 mentions, &lt;0.40 identity cosine, the seal) are read-only.{data?.cif_halted ? ' CIF is HALTED — frontier ideas are excluded until cleared.' : ''}</p></div></header>
    {error && <p className="estate-alert" data-testid="training-supervisor-error">{error}</p>}
    {notice && <p className="estate-note" data-testid="training-supervisor-notice">{notice}</p>}
    {!data && !error && <p className="estate-note">Loading the supervisor ledger…</p>}
    {data && <>
      {Object.entries(lanes).map(([l, d]) => <Lane key={l} lane={l} data={d} canOperate={canOperate} onVerdict={onVerdict} onBind={onBind} busy={busy} />)}
      {data.findings?.length > 0 && <div data-testid="supervisor-findings" style={{ marginTop: 12 }}><h3 style={{ fontSize: 13, margin: '0 0 6px' }}>Frame-candidate findings for the owner ({data.findings.length})</h3>
        {data.findings.map(f => <p key={f.finding_id} className="estate-note" data-testid={`supervisor-finding-${f.finding_id}`}>{stamp(f.at)} · {LANE[f.lane]} · {f.signature}: {f.what} · naivety pass {f.naivety_pass} · struck constraint: {f.struck_constraint}</p>)}</div>}
      {canOperate && <div data-testid="supervisor-originate" style={{ marginTop: 12, padding: 14, border: '1px solid var(--line)', borderRadius: 10, background: '#fff' }}>
        <h3 style={{ fontSize: 13, margin: '0 0 6px' }}>Coach seat · originate a hypothesis</h3>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <select data-testid="supervisor-originate-lane" style={{ ...field, width: 'auto' }} value={lane} onChange={e => setLane(e.target.value)}>{Object.entries(LANE).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
          <input data-testid="supervisor-originate-statement" style={{ ...field, flex: 1, minWidth: 220 }} placeholder="What do you expect to move, and why" value={statement} onChange={e => setStatement(e.target.value)} />
          <input data-testid="supervisor-originate-delta" style={{ ...field, maxWidth: 300 }} placeholder={`recipe_delta JSON over: ${Object.keys(data.tunables?.[lane] || {}).join(', ')}`} value={delta} onChange={e => setDelta(e.target.value)} />
          <button className="estate-btn primary" data-testid="supervisor-originate-submit" disabled={busy || !statement.trim() || !delta.trim()} onClick={originate}>Submit to the acceptance point</button>
        </div>
      </div>}
    </>}
  </section>;
}
