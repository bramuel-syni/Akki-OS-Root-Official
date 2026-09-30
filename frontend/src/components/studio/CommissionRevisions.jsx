import React, { useState } from 'react';
import { releaseClass, stamp } from './useStudio';

export function CommissionDirection({ commission }) {
  const verdict = commission.files?.['verdict.json'];
  const receipts = Object.entries(commission.receipts || {});
  return <section className="estate-section" data-testid="studio-direction">
    <div className="estate-head"><div><h2>Direction, manifest and receipts</h2><p>Creativity entered once, at the direction verdict under a standing frame; the manifest below is generated from this commission's brief and is what strike detection watches. Every figure resolves to a receipt.</p></div>
      <span className="estate-status" data-testid="studio-verdict-id">{commission.verdict_id}</span></div>
    <div className="estate-columns">
      <div>
        <h3>Verdict · {commission.frame_ref}</h3>
        <ul className="estate-list" data-testid="studio-candidates">{(verdict?.candidates || []).map(c => <li key={c.idea_id}><span><b>{c.idea_id} · {c.name}</b><small>{c.assembly?.narrative} · {c.assembly?.treatment} · {c.assembly?.density} · imagery {c.assembly?.imagery}</small><small>{c.rationale || c.conditions}</small></span><small><span className={`estate-status ${c.verdict === 'adopt' ? 'complete' : c.verdict === 'defer' ? 'partial' : 'blocked'}`}>{c.verdict}</span></small></li>)}</ul>
        <div className="estate-note">confirmed by {verdict?.confirmed_by} · {stamp(verdict?.confirmed_at)}{verdict?.re_verdict_of ? ` · re-verdict of ${verdict.re_verdict_of}` : ''} · seed <code>{commission.seed}</code> · build stamp <code>{commission.build_stamp}</code></div>
      </div>
      <div>
        <h3>Manifest (from the brief)</h3>
        <ul className="estate-list" data-testid="studio-manifest">{(commission.manifest || []).map(m => <li key={m.id}><span><b>{m.id} · {m.assumption}</b><small>rests on {m.source} · flips {m.flips.join(', ')}</small></span><small><span className="estate-status">{m.class}</span></small></li>)}</ul>
      </div>
    </div>
    <h3 style={{ marginTop: 14 }}>Receipts</h3>
    <ul className="estate-list" data-testid="studio-receipts">{receipts.map(([id, r]) => <li key={id}><span><b>{id}</b> <small>{r.resolves_to}</small>{r.platform_ref && <small>platform ref <code>{r.platform_ref}</code>{r.kind ? ` · ${r.kind}` : ''}{r.verified != null ? ` · ${r.verified ? 'digest verified' : 'NOT verified'}` : ''}</small>}</span><small><span className={`estate-status ${r.binding === 'platform' ? 'complete' : r.binding === 'declared' ? 'partial' : 'blocked'}`}>{r.binding}</span></small></li>)}</ul>
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
    <div className="estate-head"><div><h2>Revisions</h2><p>A revision creates a new content version and rebuilds; it never edits in place. Content changes flow through the references and the look holds by construction. A change to a brief field the manifest rests on is a strike: the build runs, release is blocked until the coach seat re-verdicts.</p></div>
      <span className={`estate-status ${releaseClass(commission.release?.state)}`} data-testid="studio-release-state">{commission.release?.state}</span></div>
    {!revisions.length && <div className="estate-note" data-testid="studio-revisions-empty">No revision yet.</div>}
    {revisions.length > 0 && <ul className="estate-list" data-testid="studio-revision-list">{revisions.slice().reverse().map(r => <li key={r.rev_id} data-testid={`studio-revision-${r.rev_id}`}>
      <span><b>v{r.from_version} → v{r.to_version}</b> <small>{r.changes.length ? r.changes.map(c => `${c.path}: ${JSON.stringify(c.old)} → ${JSON.stringify(c.new)}`).join(' · ') : r.re_verdict ? `re-verdict ${r.re_verdict}` : 'no change'}</small>
        <small>{stamp(r.at)} · build {r.build_id || '—'} · look {r.look_preserved == null ? 'n/a' : r.look_preserved ? 'preserved' : 'CHANGED'} · outputs changed {r.outputs_changed == null ? 'n/a' : r.outputs_changed.length}</small>
        {r.strikes?.length ? <small data-testid={`studio-strikes-${r.rev_id}`}>strike {r.strikes.map(s => `${s.manifest} (${s.assumption}; flips ${s.flips.join(', ')})`).join(' · ')}</small> : null}</span>
      <small><span className={`estate-status ${releaseClass(r.release)}`}>{r.release}</span></small></li>)}</ul>}
    {canOperate && <form onSubmit={submit} style={{ marginTop: 14 }} data-testid="studio-revise-form">
      <h3>Revise</h3>
      {rows.map((r, i) => <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 6, flexWrap: 'wrap' }}>
        <input value={r.path} onChange={e => setRows(rs => rs.map((x, j) => j === i ? { ...x, path: e.target.value } : x))} placeholder="content.facts.F005.value or brief.setting.printed" data-testid={`studio-revise-path-${i}`} style={{ flex: '2 1 260px', padding: '7px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5 }} />
        <input value={r.value} onChange={e => setRows(rs => rs.map((x, j) => j === i ? { ...x, value: e.target.value } : x))} placeholder="new value (number, true/false or text)" data-testid={`studio-revise-value-${i}`} style={{ flex: '1 1 160px', padding: '7px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5 }} />
      </div>)}
      <div className="estate-actions" style={{ justifyContent: 'flex-start' }}>
        <button type="button" className="estate-btn" onClick={() => setRows(rs => [...rs, { path: '', value: '' }])} data-testid="studio-revise-add">Add change</button>
        <button type="submit" className="estate-btn primary" disabled={Boolean(busy)} data-testid="studio-revise-submit">{busy === 'Revise' ? 'Revising…' : 'Revise and rebuild'}</button>
        {blocked && <button type="button" className="estate-btn" onClick={onReverdict} disabled={Boolean(busy)} data-testid="studio-reverdict">{busy === 'Re-verdict' ? 'Re-verdicting…' : 'Re-verdict under the standing frame'}</button>}
      </div>
    </form>}
  </section>;
}
