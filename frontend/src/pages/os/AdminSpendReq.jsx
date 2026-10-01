/*
 * AdminSpendReq.jsx — v2 OS · admin tab · APPROVALS Spend Requests leaf · LIVE.
 *
 * The signed-in approver's queue: every commissioned request whose pending approval groups seat them. Approve or
 * decline records a signed decision with a reason that stays with the job (M3-T2). Layout is the supplied
 * Approvals HTML, bound to /api/portal/approvals/*.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { useApprovalsQueue } from '@/components/portal/useApprovalsQueue';
import { stamp } from '@/components/prototype/evidence';
import '@/components/census/census.css';
import '@/components/estate/estate.css';

const TILES = [['Spend Requests', '/os/admin/spendreq'], ['Rules Updates', '/os/admin/rulesupd'], ['Model Approval', '/os/admin/modeladmission']];

export default function AdminSpendReq() {
  const session = usePrototypeSession();
  const navigate = useNavigate();
  const [decision, setDecision] = useState(null), [reason, setReason] = useState('');
  const { rows, requests, loading, error, busy, reload, decide } = useApprovalsQueue(Boolean(session.data));
  const pending = (rows || []).filter(r => r.pending_for_you.length);
  const decided = (rows || []).filter(r => !r.pending_for_you.length);
  const start = (row, kind) => { setDecision({ row, kind, group: row.pending_for_you[0] }); setReason(''); };
  const submit = async () => { if (!decision || !reason.trim()) return; const ok = await decide(decision.row.request_id, decision.group, decision.kind, reason.trim()); if (ok) setDecision(null); };
  const rowFor = (r, i) => { const req = requests[r.request_id]; return { key: `${r.request_id}-${i}`, text: req?.objective_text || `Request on ${r.scope_refs.join(', ')}`, state: r.pending_for_you.length ? 'Waiting on you' : r.state === 'approved' ? 'Approved' : r.state === 'refused' ? 'Refused' : 'Waiting on others',
    stateColor: r.state === 'refused' ? 'var(--oxblood)' : r.state === 'approved' ? 'var(--sage)' : 'var(--brass)', stateBg: r.state === 'refused' ? 'rgba(184,57,91,.08)' : r.state === 'approved' ? 'rgba(29,122,110,.08)' : 'rgba(176,141,46,.09)',
    meta: `${req ? stamp(req.created_at) : ''} · ${r.kind.replace(/[._]/g, ' ')} · ${r.pending_for_you.length ? `your sign-off needed for ${r.pending_for_you.join(', ')}` : `${r.groups.filter(g => g.satisfied).length} of ${r.groups.length} groups signed`} · decide by ${stamp(new Date(r.deadline_epoch * 1000).toISOString())}`,
    pending: r.pending_for_you.length > 0, onApprove: () => start(r, 'approved'), onDecline: () => start(r, 'refused') }; };
  const model = { isApprovalsGroup: true, approvalsTitle: 'Spend Requests', approvalsOneliner: rows ? `${pending.length} waiting on you` : '',
    hasSessionBanner: Boolean(error || loading), sessionBanner: error || 'Loading your approvals…', sessionBannerColor: error ? 'var(--oxblood)' : 'var(--ink3)',
    approvalsTilesView: TILES.map(([label, path]) => ({ key: path, label, border: label === 'Spend Requests' ? 'var(--blue)' : 'var(--line)', bg: label === 'Spend Requests' ? 'var(--blue)' : '#fff', color: label === 'Spend Requests' ? '#fff' : 'var(--ink2)', onClick: () => navigate(path) })),
    approvalsStats: [{ v: rows ? pending.length : '—', l: 'waiting on you' }, { v: rows ? decided.length : '—', l: 'already signed or routed elsewhere' }, { v: rows ? rows.filter(r => r.state === 'approved').length : '—', l: 'fully approved' }, { v: rows ? rows.filter(r => r.state === 'refused').length : '—', l: 'refused' }],
    approvalsRows: [...pending, ...decided].map(rowFor) };
  return <OwnerWorkspace session={session} title="Spend Requests" group="Approvals" section="approvals" model={model} returnTo="/os?nav=admin"
    replace={{ 4307: rows && !rows.length ? 'Nothing is waiting on you' : 'Requests seated with you' }}
    enhance={{ 4296: { 'data-testid': 'admin-spendreq-title' }, 4316: c => ({ 'data-testid': `approvals-approve-${c.rw.key}`, hidden: !c.rw.pending, disabled: busy }), 4317: c => ({ 'data-testid': `approvals-decline-${c.rw.key}`, hidden: !c.rw.pending, disabled: busy }) }}>
    <div className="estate" data-testid="admin-spendreq-surface" style={{ maxWidth: 1180, marginTop: 24 }}>
      <button className="estate-btn" onClick={reload} disabled={loading} data-testid="admin-spendreq-reload">{loading ? 'Refreshing…' : 'Refresh queue'}</button>
      {rows && !rows.length && <p className="estate-note" data-testid="admin-spendreq-empty">No commissioned request currently needs your signature. Requests appear here when an approval group that seats you is still pending and the request has not expired.</p>}
      {decision && <div className="estate-card" data-testid="approvals-decision-form" style={{ marginTop: 16 }}>
        <p className="estate-note">{decision.kind === 'approved' ? 'Approve' : 'Decline'} this request for the <b>{decision.group}</b> group. Your reason is signed and kept with the job; it covers exactly what was submitted.</p>
        <textarea data-testid="approvals-reason" aria-label="Reason" value={reason} onChange={e => setReason(e.target.value)} maxLength={200} rows={3} style={{ width: '100%', marginTop: 8, padding: 8, border: '1px solid var(--line)', borderRadius: 7, font: 'inherit' }} placeholder="Why you are signing this decision (required)" />
        <div className="estate-actions" style={{ display: 'flex', gap: 8, marginTop: 8 }}>
          <button className="estate-btn primary" data-testid="approvals-decision-submit" disabled={busy || !reason.trim()} onClick={submit}>{busy ? 'Recording…' : decision.kind === 'approved' ? 'Sign approval' : 'Sign refusal'}</button>
          <button className="estate-btn" data-testid="approvals-decision-cancel" onClick={() => setDecision(null)}>Cancel</button>
        </div>
      </div>}
    </div>
  </OwnerWorkspace>;
}
