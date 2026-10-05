/*
 * ShieldRegister.jsx — v2 OS · admin tab · Shield (Rules & Rails) · LIVE.
 *
 * The supplied Shield surface bound to the tenant confidentiality register (/api/shield/register): categories by name, by pattern and
 * by context, each enforced on every model crossing or advisory; drafts proposed from documents read inside the boundary; declarations
 * adopted but pending approval (Doc 2 A4: adopt → pending → approve → in force); retirement through the counter-signed countdown
 * ceremony (A5.4); workbook intake from the vault; the rails that have no off switch; and the recent model crossings with what the gate
 * found, rewrote and inspected. DPO / master admin act; operators read, test passages and review reach.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { apiRequest, stamp } from '@/components/models/useModelApproval';
import { readableText } from '@/components/shared/PresentationDetails';
import { useShieldRegister, KIND_LABEL, TONE } from '@/components/shield/useShieldRegister';
import { ShieldCategoryDetail } from '@/components/shield/ShieldCategoryDetail';
import { AuthorCategoryForm, ProposeForm, TestPassage, VaultIntakeForm } from '@/components/shield/ShieldTools';
import '@/components/estate/estate.css';

const TABS = [['force', 'In force'], ['pending', 'Pending'], ['drafts', 'Drafts'], ['crossings', 'Crossings'], ['rails', 'Rails']];
const RAILS = [
  'Every model call passes one chokepoint. The prompt and the system message are de-identified together before anything leaves; the same entity carries the same token on both paths.',
  'Categories enforced on every crossing become typed placeholders the model never sees through; replies are rebound to the real values inside the estate. Withheld categories never leave at all.',
  'The outbound text is inspected against every enforced value before dispatch — literal, compacted and digit-run forms. One survivor refuses the call and the refusal is receipted.',
  'Hostility is scored from the payload content by a declared rule list (instruction override, prompt or data exfiltration, persona hijack, fetch and rehydration requests, injected markup). Hold or block refuses the call before it is made. It is a rule detector, not a learned model, and the receipt says so.',
  'Confidential-document workflows send an external planner the task and structure only; an internal worker binds the plan to the real records. A task that asks for protected meaning is refused before any call.',
  'Approval, not adoption, is the gate to enforcement: a pending declaration never touches a crossing. Retiring a declaration needs a second signature and a visible 48 h countdown, and is re-verified at the crossing when applied. The list and the crossing read one entity set.',
  'Watch behavioural profiles are never read here or exported anywhere for management scoring (W13).',
];

export default function ShieldRegister() {
  const session = usePrototypeSession();
  const canAuthor = Boolean(session.data?.roles?.some(r => ['dpo', 'master_admin'].includes(r)));
  const { register, crossings, loading, busy, error, notice, forbidden, preview, reach, vault, reload, act, test, review, intake, clearPreview, clearReach } = useShieldRegister(Boolean(session.data));
  const [tab, setTab] = useState('force'), [selected, setSelected] = useState(null), [tool, setTool] = useState(null), [files, setFiles] = useState(null);
  useEffect(() => { if (tool === 'vault' && files === null) apiRequest('/api/media/files').then(r => setFiles(r.files || [])).catch(() => setFiles([])); }, [tool, files]);
  const cats = register?.categories || [];
  const active = cats.filter(c => c.status === 'active'), pending = cats.filter(c => c.status === 'pending'), drafts = cats.filter(c => c.status === 'draft'), retired = cats.filter(c => ['removed', 'withdrawn'].includes(c.status));
  const inCeremony = active.filter(c => c.removal);
  const category = useMemo(() => cats.find(c => c.name === selected && c.status !== 'superseded' && c.status !== 'withdrawn') || cats.find(c => c.name === selected) || null, [cats, selected]);
  const banner = forbidden ? 'The confidentiality register is read by admitted operators and the DPO. Your role cannot open it.' : error || notice || (loading ? 'Reading the register…' : '');
  const row = c => { const [color, bg] = TONE[c.status] || TONE.superseded; return { key: `${c.name}-${c.status}`, text: `${c.name} — ${c.description}${c.removal ? ` · RETIREMENT ${c.removal.state.toUpperCase()}${c.removal.applies_at ? ` until ${stamp(c.removal.applies_at)}` : ''}` : ''}`, cls: `${KIND_LABEL[c.kind]} · ${c.enforcement}${c.status === 'pending' ? ' · awaits approval' : ''}`, clsColor: c.removal ? 'var(--oxblood)' : color, clsBg: c.removal ? 'rgba(184,57,91,.08)' : bg, who: readableText(String(c.approved_by || c.adopted_by || c.authored_by || c.proposed_by || '')), when: stamp(c.approved_at || c.adopted_at || c.authored_at || c.proposed_at), onWalk: () => setSelected(c.name) }; };
  const crossingRow = x => ({ key: x.receipt_id, text: `${x.purpose || x.kind} · ${x.model || 'model not recorded'} · ${x.register ? `${Object.values(x.register.register_enforced || {}).reduce((a, b) => a + b, 0)} enforced span(s) rewritten, ${Object.values(x.register.register_advisory || {}).reduce((a, b) => a + b, 0)} advisory finding(s), egress ${x.register.egress_clean ? 'clean' : 'REFUSED'}, hostility ${x.register.hostility}` : 'before the register gate · de-identifier only'}`,
    cls: x.kind.endsWith('_refused') ? 'refused' : x.register ? 'gated' : 'legacy', clsColor: x.kind.endsWith('_refused') ? 'var(--oxblood)' : x.register ? 'var(--sage)' : 'var(--ink3)', clsBg: x.kind.endsWith('_refused') ? 'rgba(184,57,91,.08)' : x.register ? 'rgba(29,122,110,.08)' : 'var(--surface2)', who: `${x.tokens_in ?? 0} in · ${x.tokens_out ?? 0} out`, when: stamp(x.at), onWalk: undefined });
  const rows = tab === 'force' ? active.map(row) : tab === 'pending' ? pending.map(row) : tab === 'drafts' ? drafts.map(row) : tab === 'crossings' ? (crossings?.crossings || []).map(crossingRow) : [];
  const counts = { force: active.length, pending: pending.length, drafts: drafts.length };
  const model = {
    isTrustGroup: true, isTrustRules: true, isRulesInForce: tab !== 'rails', isRulesChange: false, isRulesRails: tab === 'rails', hasSessionBanner: Boolean(banner), sessionBanner: readableText(banner), sessionBannerColor: error || forbidden ? 'var(--oxblood)' : 'var(--ink3)',
    rulesTabsView: TABS.map(([k, label]) => ({ key: k, label: k in counts ? `${label} (${counts[k]})` : label, color: tab === k ? 'var(--ink)' : 'var(--ink3)', border: tab === k ? 'var(--accent)' : 'transparent', onClick: () => { setTab(k); setSelected(null); } })),
    rulesRowsView: rows, railsRowsView: RAILS.map((text, i) => ({ key: i, text })), lockIcon: '◆',
    hasPageTopline: true, pageEyebrow: 'Shield · SyniSense + Solva', pageHeadline: 'What leaves the box is reconstructed, never raw.',
    pageSub: register ? `${active.filter(c => c.enforcement === 'enforced').length} categories enforced on every crossing · ${active.filter(c => c.enforcement === 'advisory').length} advisory · ${pending.length} pending approval · ${drafts.length} draft(s) · ${inCeremony.length} retirement ceremony(ies) in flight · ${retired.length} retired or withdrawn · ${crossings?.gated_in_window ?? 0} of the latest ${crossings?.window ?? 0} crossings carry the gate's summary (${crossings?.total_on_record ?? 0} on record).` : '',
  };
  const walkTestId = c => ({ 'data-testid': `shield-row-walk-${(c.r.key || '').replace(/[^A-Za-z0-9]+/g, '-').toLowerCase()}`, ...(c.r.onWalk ? {} : { hidden: true }) });
  const post = (label, path, body) => act(label, path, body);
  return <OwnerWorkspace session={session} title="Shield" group="Rules & Rails" section="trust" model={model} returnTo="/os?nav=admin"
    enhance={{ 4539: c => ({ 'data-testid': `shield-tab-${c.t.key}` }), 4546: c => ({ 'data-testid': `shield-row-${(c.r.key || '').replace(/[^A-Za-z0-9]+/g, '-').toLowerCase()}` }), 4551: walkTestId }}>
    {!forbidden && session.data && <div className="estate" data-testid="shield-surface" style={{ maxWidth: 1180, marginTop: 8 }}>
      <div className="estate-actions" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <button className="estate-btn" data-testid="shield-reload" onClick={reload} disabled={loading}>{loading ? 'Reading…' : 'Refresh'}</button>
        {canAuthor && <button className="estate-btn primary" data-testid="shield-author-open" onClick={() => setTool(tool === 'author' ? null : 'author')}>Declare a category</button>}
        {canAuthor && <button className="estate-btn" data-testid="shield-propose-open" onClick={() => setTool(tool === 'propose' ? null : 'propose')}>Propose from a document</button>}
        {canAuthor && <button className="estate-btn" data-testid="shield-vault-open" onClick={() => setTool(tool === 'vault' ? null : 'vault')}>Bring in a vault workbook</button>}
        <button className="estate-btn" data-testid="shield-test-open" onClick={() => setTool(tool === 'test' ? null : 'test')}>Test a passage</button>
        {!canAuthor && <span className="estate-note" style={{ margin: 0 }} data-testid="shield-readonly-note">Declaring, adopting, approving, re-scoping and retiring categories are DPO acts; this view is read, test and review for your role.</span>}
      </div>
      {tool === 'author' && canAuthor && <AuthorCategoryForm busy={busy} onCancel={() => setTool(null)} onSubmit={async body => { const r = await post('Declaration', '/api/shield/register', body); if (r) { setTool(null); setTab('pending'); setSelected(r.category.name); } }} />}
      {tool === 'propose' && canAuthor && <ProposeForm busy={busy} onCancel={() => setTool(null)} onSubmit={async (text, ref) => { const r = await post('Proposal', '/api/shield/register/propose', { text, source_ref: ref }); if (r) { setTool(null); setTab('drafts'); setSelected(r.drafts[0]?.name || null); } }} />}
      {tool === 'vault' && canAuthor && <VaultIntakeForm busy={busy} files={files} result={vault} onCancel={() => setTool(null)} onSubmit={async (fileId, ref) => { const r = await intake(fileId, ref); if (r?.pending?.length) { setTab('pending'); } }} />}
      {tool === 'test' && <TestPassage busy={busy} preview={preview} onTest={test} onClear={clearPreview} />}
      {category && <ShieldCategoryDetail category={category} canAuthor={canAuthor} principalId={register?.principal_id} busy={busy} reach={reach} onClose={() => { setSelected(null); clearReach(); }}
        onEnforce={(name, enforcement) => post('Scope change', `/api/shield/register/${name}/enforcement`, { enforcement })}
        onRemove={(name, reason) => act('Retirement proposal', `/api/shield/register/${name}?reason=${encodeURIComponent(reason)}`, undefined, 'DELETE')}
        onAdopt={async name => { if (await post('Adoption', `/api/shield/register/${name}/adopt`, {})) setTab('pending'); }}
        onApprove={async name => { if (await post('Approval', `/api/shield/register/${name}/approve`)) setTab('force'); }}
        onWithdraw={async (name, reason) => { if (await post('Withdrawal', `/api/shield/register/${name}/withdraw`, { reason })) setSelected(null); }}
        onDiscard={async name => { if (await act('Discard', `/api/shield/register/${name}/draft`, undefined, 'DELETE')) setSelected(null); }}
        onCountersign={name => post('Counter-signature', `/api/shield/register/${name}/removal/countersign`)}
        onCancelRemoval={(name, reason) => post('Retirement cancelled', `/api/shield/register/${name}/removal/cancel`, { reason })}
        onApply={name => post('Retirement applied', `/api/shield/register/${name}/removal/apply`)}
        onReview={review} onClearReach={clearReach} />}
      {tab === 'force' && retired.length > 0 && !category && <p className="estate-note" data-testid="shield-retired-note">{retired.length} retired or withdrawn categor{retired.length === 1 ? 'y' : 'ies'} stay on the record: {retired.map(c => c.name).join(', ')}.</p>}
      {tab === 'pending' && pending.length === 0 && !category && <p className="estate-note" data-testid="shield-pending-empty">Nothing awaits approval. Declarations the DPO adopts land here until a DPO or master admin approves them into force.</p>}
    </div>}
  </OwnerWorkspace>;
}
