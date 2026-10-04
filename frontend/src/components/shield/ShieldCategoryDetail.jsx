import React, { useState } from 'react';
import { stamp } from '../models/useModelApproval';
import { readableText } from '../shared/PresentationDetails';
import { KIND_LABEL, ENFORCEMENT_LABEL, TONE } from './useShieldRegister';

const Pills = ({ id, items, empty }) => items?.length ? <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }} data-testid={id}>{items.map((x, i) => <code key={i} style={{ fontSize: 11.5, background: 'var(--surface2)', padding: '3px 7px', borderRadius: 4, overflowWrap: 'anywhere' }}>{x}</code>)}</div> : <p className="estate-note" style={{ margin: 0 }}>{empty}</p>;

export function ShieldCategoryDetail({ category: c, canAuthor, busy, onEnforce, onRemove, onAdopt, onDiscard, onClose }) {
  const [reason, setReason] = useState(''), [confirm, setConfirm] = useState(null);
  const [color, bg] = TONE[c.status] || TONE.superseded;
  const draft = c.status === 'draft', active = c.status === 'active';
  return <section className="estate-section" data-testid="shield-category-detail" style={{ marginTop: 16 }}>
    <header className="estate-head"><div>
      <span className="estate-label">{KIND_LABEL[c.kind]} · {c.action} · version {c.version}</span>
      <h2 data-testid="shield-category-name">{c.name}</h2>
      <p data-testid="shield-category-description">{c.description}</p>
    </div><div style={{ textAlign: 'right' }}>
      <span className="estate-status" data-testid="shield-category-status" style={{ background: bg, color }}>{c.status}</span>
      <div className="estate-meta" style={{ justifyContent: 'flex-end' }}><span data-testid="shield-category-enforcement">{ENFORCEMENT_LABEL[c.enforcement] || c.enforcement}</span></div>
    </div></header>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))', gap: 18 }}>
      {c.kind === 'contextual' && <div><h3>Cues that signal the meaning</h3><Pills id="shield-category-cues" items={c.cues} empty="No cues." />{c.targets?.length ? <p className="estate-note">Protects: {c.targets.join(', ').toLowerCase().replace(/_/g, ' ')}</p> : null}</div>}
      {c.kind === 'pattern' && <div><h3>Patterns</h3><Pills id="shield-category-patterns" items={c.patterns} empty="No patterns." /></div>}
      {c.kind === 'exact' && <div><h3>Literal values ({c.values?.length || 0})</h3><p className="estate-note" style={{ margin: '0 0 6px' }}>Visible to the DPO only; never sent to a model.</p><Pills id="shield-category-values" items={(c.values || []).slice(0, 40)} empty="No values." /></div>}
      <div><h3>Record</h3><ul className="estate-list" data-testid="shield-category-history">{(c.history || []).slice().reverse().map((h, i) => <li key={i}><span>{h.change}</span><small>{stamp(h.at)} · {readableText(String(h.by))}</small></li>)}</ul>
        {c.removal_reason && <p className="estate-note" data-testid="shield-category-removal">Removed: {c.removal_reason}</p>}</div>
    </div>
    {canAuthor && <div style={{ marginTop: 18 }} data-testid="shield-category-actions">
      <div className="estate-actions" style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {draft && <button className="estate-btn primary" data-testid="shield-adopt" onClick={() => onAdopt(c.name)} disabled={Boolean(busy)}>Adopt into force</button>}
        {draft && <button className="estate-btn" data-testid="shield-discard" onClick={() => onDiscard(c.name)} disabled={Boolean(busy)}>Discard draft</button>}
        {active && <button className="estate-btn" data-testid="shield-toggle-enforcement" onClick={() => onEnforce(c.name, c.enforcement === 'enforced' ? 'advisory' : 'enforced')} disabled={Boolean(busy)}>{c.enforcement === 'enforced' ? 'Make advisory' : 'Enforce on every crossing'}</button>}
        {active && <button className="estate-btn" data-testid="shield-remove-open" onClick={() => setConfirm(confirm ? null : 'remove')} disabled={Boolean(busy)}>Retire category</button>}
        <button className="estate-btn" data-testid="shield-detail-close" onClick={onClose}>Close</button>
      </div>
      {confirm === 'remove' && <form data-testid="shield-remove-form" onSubmit={e => { e.preventDefault(); onRemove(c.name, reason); }} style={{ marginTop: 12 }}>
        <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">Reason for retirement (on the record)</span><input data-testid="shield-remove-reason" style={{ width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', boxSizing: 'border-box' }} value={reason} onChange={e => setReason(e.target.value)} required maxLength={300} /></label>
        <div className="estate-actions"><button type="submit" className="estate-btn" data-testid="shield-remove-submit" disabled={Boolean(busy) || !reason.trim()}>Retire</button><button type="button" className="estate-btn" onClick={() => setConfirm(null)}>Cancel</button></div>
      </form>}
    </div>}
  </section>;
}
