import React, { useState } from 'react';
import { stamp } from '../models/useModelApproval';
import { readableText } from '../shared/PresentationDetails';
import { KIND_LABEL, ENFORCEMENT_LABEL, STATUS_LABEL, TONE } from './useShieldRegister';

const Pills = ({ id, items, empty }) => items?.length ? <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }} data-testid={id}>{items.map((x, i) => <code key={i} style={{ fontSize: 11.5, background: 'var(--surface2)', padding: '3px 7px', borderRadius: 4, overflowWrap: 'anywhere' }}>{x}</code>)}</div> : <p className="estate-note" style={{ margin: 0 }}>{empty}</p>;
const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', boxSizing: 'border-box' };

const ReasonForm = ({ id, label, submit, onSubmit, onCancel, busy }) => {
  const [reason, setReason] = useState('');
  return <form data-testid={`${id}-form`} onSubmit={e => { e.preventDefault(); onSubmit(reason); }} style={{ marginTop: 12 }}>
    <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">{label}</span><input data-testid={`${id}-reason`} style={field} value={reason} onChange={e => setReason(e.target.value)} required minLength={3} maxLength={300} /></label>
    <div className="estate-actions"><button type="submit" className="estate-btn" data-testid={`${id}-submit`} disabled={Boolean(busy) || reason.trim().length < 3}>{submit}</button><button type="button" className="estate-btn" onClick={onCancel}>Cancel</button></div>
  </form>;
};

// Removal is the consequential direction (Doc 2 A5.4): proposed → second signature → visible countdown (cancellable) → applied → re-verified.
function RemovalCeremony({ c, principalId, canAuthor, busy, onCountersign, onCancelRemoval, onApply }) {
  const [cancelling, setCancelling] = useState(false);
  const r = c.removal; if (!r) return null;
  const elapsed = r.applies_at && new Date(r.applies_at) <= new Date();
  const isProposer = principalId && r.proposed_by === principalId;
  return <div className="estate-section" data-testid="shield-removal-ceremony" style={{ marginTop: 14, borderColor: 'var(--oxblood)' }}>
    <span className="estate-label" style={{ color: 'var(--oxblood)' }}>Retirement ceremony · {r.state}</span>
    <p style={{ margin: '6px 0', fontSize: 13 }} data-testid="shield-removal-state">{r.state === 'proposed' ? `Proposed by ${readableText(String(r.proposed_by))} on ${stamp(r.proposed_at)}: "${r.reason}". A second DPO or master admin must counter-sign before the ${r.countdown_hours} h countdown starts. The category keeps protecting meanwhile.`
      : `Counter-signed by ${readableText(String(r.counter_signed_by))} on ${stamp(r.counter_signed_at)}. ${elapsed ? 'The countdown has elapsed; the retirement can now be applied and re-verified.' : `Visible countdown runs until ${stamp(r.applies_at)}; it can be cancelled until then. The category keeps protecting meanwhile.`}`}</p>
    {canAuthor && <div className="estate-actions" style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
      {r.state === 'proposed' && <button className="estate-btn primary" data-testid="shield-removal-countersign" onClick={() => onCountersign(c.name)} disabled={Boolean(busy) || isProposer} title={isProposer ? 'The proposer cannot counter-sign their own removal' : ''}>Counter-sign</button>}
      {r.state === 'countdown' && <button className="estate-btn primary" data-testid="shield-removal-apply" onClick={() => onApply(c.name)} disabled={Boolean(busy) || !elapsed}>{elapsed ? 'Apply retirement' : 'Apply (after countdown)'}</button>}
      <button className="estate-btn" data-testid="shield-removal-cancel-open" onClick={() => setCancelling(v => !v)} disabled={Boolean(busy)}>Cancel retirement</button>
    </div>}
    {isProposer && r.state === 'proposed' && <p className="estate-note" data-testid="shield-removal-proposer-note">You proposed this retirement; a different DPO or master admin must counter-sign it.</p>}
    {cancelling && <ReasonForm id="shield-removal-cancel" label="Why the retirement is cancelled (on the record)" submit="Cancel the retirement" busy={busy} onCancel={() => setCancelling(false)} onSubmit={reason => { setCancelling(false); onCancelRemoval(c.name, reason); }} />}
  </div>;
}

export function ReachReport({ reach, onClose }) {
  if (!reach) return null;
  const rows = Object.entries(reach.by_declaration || {});
  return <div className="estate-section" data-testid="shield-reach" style={{ marginTop: 14 }}>
    <span className="estate-label">Review · reach over measured material</span>
    {rows.map(([name, r]) => <p key={name} style={{ margin: '6px 0', fontSize: 13 }} data-testid={`shield-reach-${name}`}><b>{name}</b>: {r.matches} match(es) in {r.documents_matched} of {reach.measured_documents} measured document(s).</p>)}
    <p className="estate-note" data-testid="shield-reach-unmeasured">{reach.unmeasured}</p>
    {reach.measurement_errors?.length ? <p className="estate-note" style={{ color: 'var(--oxblood)' }}>{reach.measurement_errors.length} measured file(s) could not be read from storage; they are not represented.</p> : null}
    <div className="estate-actions"><button className="estate-btn" data-testid="shield-reach-close" onClick={onClose}>Close</button></div>
  </div>;
}

export function ShieldCategoryDetail({ category: c, canAuthor, principalId, busy, reach, onEnforce, onRemove, onAdopt, onApprove, onWithdraw, onDiscard, onCountersign, onCancelRemoval, onApply, onReview, onClearReach, onClose }) {
  const [confirm, setConfirm] = useState(null);
  const [color, bg] = TONE[c.status] || TONE.superseded;
  const draft = c.status === 'draft', pending = c.status === 'pending', active = c.status === 'active', inCeremony = active && Boolean(c.removal);
  return <section className="estate-section" data-testid="shield-category-detail" style={{ marginTop: 16 }}>
    <header className="estate-head"><div>
      <span className="estate-label">{KIND_LABEL[c.kind]} · {c.action} · version {c.version}{c.entity_type ? ` · entity ${c.entity_type}` : ''}{c.provenance ? ` · ${c.provenance.replace(/_/g, ' ')}` : ''}</span>
      <h2 data-testid="shield-category-name">{c.name}</h2>
      <p data-testid="shield-category-description">{c.description}</p>
    </div><div style={{ textAlign: 'right' }}>
      <span className="estate-status" data-testid="shield-category-status" style={{ background: bg, color }}>{STATUS_LABEL[c.status] || c.status}</span>
      <div className="estate-meta" style={{ justifyContent: 'flex-end' }}><span data-testid="shield-category-enforcement">{ENFORCEMENT_LABEL[c.enforcement] || c.enforcement}</span></div>
    </div></header>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))', gap: 18 }}>
      {c.kind === 'contextual' && <div><h3>Cues that signal the meaning</h3><Pills id="shield-category-cues" items={c.cues} empty="No cues." />{c.targets?.length ? <p className="estate-note">Protects: {c.targets.join(', ').toLowerCase().replace(/_/g, ' ')}</p> : null}</div>}
      {c.kind === 'pattern' && <div><h3>Patterns</h3><Pills id="shield-category-patterns" items={c.patterns} empty="No patterns." /></div>}
      {c.kind === 'exact' && <div><h3>Literal values ({c.values?.length || 0})</h3><p className="estate-note" style={{ margin: '0 0 6px' }}>Visible to the DPO only; never sent to a model.</p><Pills id="shield-category-values" items={(c.values || []).slice(0, 40)} empty="No values." />{(c.values?.length || 0) > 40 && <p className="estate-note">… and {c.values.length - 40} more.</p>}</div>}
      <div><h3>Record</h3>
        <div className="estate-meta" data-testid="shield-category-provenance" style={{ flexWrap: 'wrap' }}>
          {c.adopted_by && <span>adopted by {readableText(String(c.adopted_by))} · {stamp(c.adopted_at)}</span>}
          {c.approved_by && <span>approved by {readableText(String(c.approved_by))} · {stamp(c.approved_at)}</span>}
          {pending && <span>awaiting approval</span>}
        </div>
        <ul className="estate-list" data-testid="shield-category-history">{(c.history || []).slice().reverse().map((h, i) => <li key={i}><span>{h.change}</span><small>{stamp(h.at)} · {readableText(String(h.by))}</small></li>)}</ul>
        {c.removal_reason && c.status === 'removed' && <p className="estate-note" data-testid="shield-category-removal">Retired: {c.removal_reason}{c.removal?.re_verified ? ` · re-verified at the crossing: ${c.removal.re_verified.clean ? 'clean' : 'NOT clean'}` : ''}</p>}</div>
    </div>
    <RemovalCeremony c={c} principalId={principalId} canAuthor={canAuthor} busy={busy} onCountersign={onCountersign} onCancelRemoval={onCancelRemoval} onApply={onApply} />
    <ReachReport reach={reach} onClose={onClearReach} />
    <div style={{ marginTop: 18 }} data-testid="shield-category-actions">
      <div className="estate-actions" style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {canAuthor && draft && <button className="estate-btn primary" data-testid="shield-adopt" onClick={() => onAdopt(c.name)} disabled={Boolean(busy)}>Adopt (to pending)</button>}
        {canAuthor && draft && <button className="estate-btn" data-testid="shield-discard" onClick={() => onDiscard(c.name)} disabled={Boolean(busy)}>Discard draft</button>}
        {canAuthor && pending && <button className="estate-btn primary" data-testid="shield-approve" onClick={() => onApprove(c.name)} disabled={Boolean(busy)}>Approve into force</button>}
        {canAuthor && pending && <button className="estate-btn" data-testid="shield-withdraw-open" onClick={() => setConfirm(confirm === 'withdraw' ? null : 'withdraw')} disabled={Boolean(busy)}>Withdraw</button>}
        {canAuthor && active && !inCeremony && <button className="estate-btn" data-testid="shield-toggle-enforcement" onClick={() => onEnforce(c.name, c.enforcement === 'enforced' ? 'advisory' : 'enforced')} disabled={Boolean(busy)}>{c.enforcement === 'enforced' ? 'Make advisory' : 'Enforce on every crossing'}</button>}
        {canAuthor && active && !inCeremony && <button className="estate-btn" data-testid="shield-remove-open" onClick={() => setConfirm(confirm === 'remove' ? null : 'remove')} disabled={Boolean(busy)}>Propose retirement</button>}
        {(draft || pending || active) && <button className="estate-btn" data-testid="shield-review-reach" onClick={() => onReview(c.name)} disabled={busy === 'Reach'}>{busy === 'Reach' ? 'Measuring…' : 'Review reach'}</button>}
        <button className="estate-btn" data-testid="shield-detail-close" onClick={onClose}>Close</button>
      </div>
      {confirm === 'remove' && <ReasonForm id="shield-remove" label="Reason for retirement (on the record) — a second DPO must counter-sign, then a 48 h countdown runs" submit="Propose retirement" busy={busy} onCancel={() => setConfirm(null)} onSubmit={reason => { setConfirm(null); onRemove(c.name, reason); }} />}
      {confirm === 'withdraw' && <ReasonForm id="shield-withdraw" label="Why this pending declaration is withdrawn (on the record)" submit="Withdraw" busy={busy} onCancel={() => setConfirm(null)} onSubmit={reason => { setConfirm(null); onWithdraw(c.name, reason); }} />}
    </div>
  </section>;
}
