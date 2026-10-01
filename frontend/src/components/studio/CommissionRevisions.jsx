import React, { useState } from 'react';
import { releaseClass, stamp } from './useStudio';
import { readableText } from '../shared/PresentationDetails';

export function CommissionDirection({ commission }) {
  const verdict = commission.files?.['verdict.json'];
  const receipts = Object.entries(commission.receipts || {});
  return <section className="estate-section" data-testid="studio-direction">
    <div className="estate-head"><h2>Editorial direction & sources</h2></div>
    <div className="estate-columns">
      <div>
        <h3>Selected direction</h3>
        <ul className="estate-list" data-testid="studio-candidates">{(verdict?.candidates || []).map(c => <li key={c.idea_id}><span><b>{c.name}</b><small>{readableText(c.rationale || c.conditions)}</small></span><small><span className={`estate-status ${c.verdict === 'adopt' ? 'complete' : c.verdict === 'defer' ? 'partial' : 'blocked'}`}>{c.verdict === 'adopt' ? 'Selected' : c.verdict}</span></small></li>)}</ul>
        <p className="estate-note" data-testid="studio-direction-date">Confirmed {stamp(verdict?.confirmed_at)}</p>
      </div>
      <div>
        <h3>Assumptions to review if the brief changes</h3>
        <ul className="estate-list" data-testid="studio-manifest">{(commission.manifest || []).map(m => <li key={m.id}><span><b>{readableText(m.assumption)}</b><small>{readableText(m.source)}</small></span></li>)}</ul>
      </div>
    </div>
    <h3 style={{ marginTop: 14 }}>Source evidence</h3>
    <ul className="estate-list" data-testid="studio-receipts">{receipts.map(([id, r], i) => <li key={id}><span><b>Source {i + 1}</b><small>{readableText(r.resolves_to)}</small></span><small><span className={`estate-status ${r.verified ? 'complete' : 'partial'}`}>{r.verified ? 'Verified' : r.binding === 'declared' ? 'Declared' : 'Not verified'}</span></small></li>)}</ul>
  </section>;
}

export function CommissionRevisions({ commission, canOperate, busy, onRevise, onReverdict }) {
  const [rows, setRows] = useState([{ path: '', value: '' }]);
  const revisions = commission.revisions || [];
  const blocked = commission.release?.state === 'blocked pending re-verdict';
  const submit = e => {
    e.preventDefault();
    const changes = rows.filter(r => r.path.trim()).map(r => ({ path: r.path.trim(), value: r.value }));
    if (changes.length) onRevise(changes);
  };
  return <section className="estate-section" data-testid="studio-revisions">
    <div className="estate-head"><div><h2>Revisions</h2>{blocked && <p data-testid="studio-revision-action">The brief changed. Review the editorial direction before release.</p>}</div>
      <span className={`estate-status ${releaseClass(commission.release?.state)}`} data-testid="studio-release-state">{commission.release?.state}</span></div>
    {!revisions.length && <div className="estate-note" data-testid="studio-revisions-empty">No revision yet.</div>}
    {revisions.length > 0 && <ul className="estate-list" data-testid="studio-revision-list">{revisions.slice().reverse().map(r => <li key={r.rev_id} data-testid={`studio-revision-${r.rev_id}`}>
      <span><b>v{r.from_version} → v{r.to_version}</b> <small>{r.changes.length ? readableText(r.changes.map(c => `${c.path}: ${JSON.stringify(c.old)} → ${JSON.stringify(c.new)}`).join(' · ')) : r.re_verdict ? 'Editorial direction reviewed' : 'No change'}</small>
        <small>{stamp(r.at)} · {r.look_preserved == null ? 'Design not checked' : r.look_preserved ? 'Design preserved' : 'Design changed'}</small>
        {r.strikes?.length ? <small data-testid={`studio-strikes-${r.rev_id}`}>strike {r.strikes.map(s => `${s.manifest} (${s.assumption}; flips ${s.flips.join(', ')})`).join(' · ')}</small> : null}</span>
      <small><span className={`estate-status ${releaseClass(r.release)}`}>{r.release}</span></small></li>)}</ul>}
    {canOperate && <form onSubmit={submit} style={{ marginTop: 14 }} data-testid="studio-revise-form">
      <h3>Revise</h3>
      {rows.map((r, i) => <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 6, flexWrap: 'wrap' }}>
        <input aria-label={`Field path ${i + 1}`} value={r.path} onChange={e => setRows(rs => rs.map((x, j) => j === i ? { ...x, path: e.target.value } : x))} placeholder="Field path, e.g. content.facts.F005.value" data-testid={`studio-revise-path-${i}`} style={{ flex: '2 1 260px', padding: '7px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5 }} />
        <input aria-label={`New value ${i + 1}`} value={r.value} onChange={e => setRows(rs => rs.map((x, j) => j === i ? { ...x, value: e.target.value } : x))} placeholder="New value" data-testid={`studio-revise-value-${i}`} style={{ flex: '1 1 160px', padding: '7px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5 }} />
      </div>)}
      <div className="estate-actions" style={{ justifyContent: 'flex-start' }}>
        <button type="button" className="estate-btn" onClick={() => setRows(rs => [...rs, { path: '', value: '' }])} data-testid="studio-revise-add">Add change</button>
        <button type="submit" className="estate-btn primary" disabled={Boolean(busy) || !rows.some(r => r.path.trim())} data-testid="studio-revise-submit">{busy === 'Revise' ? 'Revising…' : 'Save & rebuild'}</button>
        {blocked && <button type="button" className="estate-btn" onClick={onReverdict} disabled={Boolean(busy)} data-testid="studio-reverdict">{busy === 'Re-verdict' ? 'Reviewing…' : 'Reassess editorial direction'}</button>}
      </div>
    </form>}
  </section>;
}
