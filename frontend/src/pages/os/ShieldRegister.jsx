/*
 * ShieldRegister.jsx — v2 OS · admin tab · Shield (Rules & Rails) · LIVE.
 *
 * The supplied Shield surface bound to the tenant confidentiality register (/api/shield/register): categories by name, by pattern and
 * by context, each enforced on every model crossing or advisory; drafts proposed from documents read inside the boundary; the rails
 * that have no off switch; and the recent model crossings with what the gate found, rewrote and inspected. DPO / master admin act
 * (declare, propose, adopt, re-scope, retire); operators read and test passages. The prototype's demo "change in flight" is not shown.
 */
import React, { useMemo, useState } from 'react';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { stamp } from '@/components/models/useModelApproval';
import { readableText } from '@/components/shared/PresentationDetails';
import { useShieldRegister, KIND_LABEL, TONE } from '@/components/shield/useShieldRegister';
import { ShieldCategoryDetail } from '@/components/shield/ShieldCategoryDetail';
import { AuthorCategoryForm, ProposeForm, TestPassage } from '@/components/shield/ShieldTools';
import '@/components/estate/estate.css';

const TABS = [['force', 'In force'], ['drafts', 'Drafts'], ['crossings', 'Crossings'], ['rails', 'Rails']];
const RAILS = [
  'Every model call passes one chokepoint. The prompt and the system message are de-identified together before anything leaves; the same entity carries the same token on both paths.',
  'Categories enforced on every crossing become typed placeholders the model never sees through; replies are rebound to the real values inside the estate. Withheld categories never leave at all.',
  'The outbound text is inspected against every enforced value before dispatch — literal, compacted and digit-run forms. One survivor refuses the call and the refusal is receipted.',
  'Hostility is scored from the payload content by a declared rule list (instruction override, prompt or data exfiltration, persona hijack, fetch and rehydration requests, injected markup). Hold or block refuses the call before it is made. It is a rule detector, not a learned model, and the receipt says so.',
  'Confidential-document workflows send an external planner the task and structure only; an internal worker binds the plan to the real records. A task that asks for protected meaning is refused before any call.',
  'Watch behavioural profiles are never read here or exported anywhere for management scoring (W13).',
];

export default function ShieldRegister() {
  const session = usePrototypeSession();
  const canAuthor = Boolean(session.data?.roles?.some(r => ['dpo', 'master_admin'].includes(r)));
  const { register, crossings, loading, busy, error, notice, forbidden, preview, reload, act, test, clearPreview } = useShieldRegister(Boolean(session.data));
  const [tab, setTab] = useState('force'), [selected, setSelected] = useState(null), [tool, setTool] = useState(null);
  const cats = register?.categories || [];
  const active = cats.filter(c => c.status === 'active'), drafts = cats.filter(c => c.status === 'draft'), retired = cats.filter(c => c.status === 'removed');
  const category = useMemo(() => cats.find(c => c.name === selected && c.status !== 'superseded') || null, [cats, selected]);
  const banner = forbidden ? 'The confidentiality register is read by admitted operators and the DPO. Your role cannot open it.' : error || notice || (loading ? 'Reading the register…' : '');
  const row = c => { const [color, bg] = TONE[c.status] || TONE.superseded; return { key: `${c.name}-${c.status}`, text: `${c.name} — ${c.description}`, cls: `${KIND_LABEL[c.kind]} · ${c.enforcement}`, clsColor: color, clsBg: bg, who: readableText(String(c.authored_by || c.proposed_by || '')), when: stamp(c.authored_at || c.proposed_at), onWalk: () => setSelected(c.name) }; };
  const crossingRow = x => ({ key: x.receipt_id, text: `${x.purpose || x.kind} · ${x.model || 'model not recorded'} · ${x.register ? `${Object.values(x.register.register_enforced || {}).reduce((a, b) => a + b, 0)} enforced span(s) rewritten, ${Object.values(x.register.register_advisory || {}).reduce((a, b) => a + b, 0)} advisory finding(s), egress ${x.register.egress_clean ? 'clean' : 'REFUSED'}, hostility ${x.register.hostility}` : 'before the register gate · de-identifier only'}`,
    cls: x.kind.endsWith('_refused') ? 'refused' : x.register ? 'gated' : 'legacy', clsColor: x.kind.endsWith('_refused') ? 'var(--oxblood)' : x.register ? 'var(--sage)' : 'var(--ink3)', clsBg: x.kind.endsWith('_refused') ? 'rgba(184,57,91,.08)' : x.register ? 'rgba(29,122,110,.08)' : 'var(--surface2)', who: `${x.tokens_in ?? 0} in · ${x.tokens_out ?? 0} out`, when: stamp(x.at), onWalk: undefined });
  const rows = tab === 'force' ? active.map(row) : tab === 'drafts' ? drafts.map(row) : tab === 'crossings' ? (crossings?.crossings || []).map(crossingRow) : [];
  const model = {
    isTrustGroup: true, isTrustRules: true, isRulesInForce: tab !== 'rails', isRulesChange: false, isRulesRails: tab === 'rails', hasSessionBanner: Boolean(banner), sessionBanner: readableText(banner), sessionBannerColor: error || forbidden ? 'var(--oxblood)' : 'var(--ink3)',
    rulesTabsView: TABS.map(([k, label]) => ({ key: k, label: k === 'drafts' ? `${label} (${drafts.length})` : k === 'force' ? `${label} (${active.length})` : label, color: tab === k ? 'var(--ink)' : 'var(--ink3)', border: tab === k ? 'var(--accent)' : 'transparent', onClick: () => { setTab(k); setSelected(null); } })),
    rulesRowsView: rows, railsRowsView: RAILS.map((text, i) => ({ key: i, text })), lockIcon: '◆',
    hasPageTopline: true, pageEyebrow: 'Shield · SyniSense + Solva', pageHeadline: 'What leaves the box is reconstructed, never raw.',
    pageSub: register ? `${active.filter(c => c.enforcement === 'enforced').length} categories enforced on every crossing · ${active.filter(c => c.enforcement === 'advisory').length} advisory · ${drafts.length} draft(s) awaiting the DPO · ${retired.length} retired · ${crossings?.gated_in_window ?? 0} of the latest ${crossings?.window ?? 0} crossings carry the gate's summary (${crossings?.total_on_record ?? 0} on record).` : '',
  };
  const walkTestId = c => ({ 'data-testid': `shield-row-walk-${(c.r.key || '').replace(/[^A-Za-z0-9]+/g, '-').toLowerCase()}`, ...(c.r.onWalk ? {} : { hidden: true }) });
  return <OwnerWorkspace session={session} title="Shield" group="Rules & Rails" section="trust" model={model} returnTo="/os?nav=admin"
    enhance={{ 4539: c => ({ 'data-testid': `shield-tab-${c.t.key}` }), 4546: c => ({ 'data-testid': `shield-row-${(c.r.key || '').replace(/[^A-Za-z0-9]+/g, '-').toLowerCase()}` }), 4551: walkTestId }}>
    {!forbidden && session.data && <div className="estate" data-testid="shield-surface" style={{ maxWidth: 1180, marginTop: 8 }}>
      <div className="estate-actions" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <button className="estate-btn" data-testid="shield-reload" onClick={reload} disabled={loading}>{loading ? 'Reading…' : 'Refresh'}</button>
        {canAuthor && <button className="estate-btn primary" data-testid="shield-author-open" onClick={() => setTool(tool === 'author' ? null : 'author')}>Declare a category</button>}
        {canAuthor && <button className="estate-btn" data-testid="shield-propose-open" onClick={() => setTool(tool === 'propose' ? null : 'propose')}>Propose from a document</button>}
        <button className="estate-btn" data-testid="shield-test-open" onClick={() => setTool(tool === 'test' ? null : 'test')}>Test a passage</button>
        {!canAuthor && <span className="estate-note" style={{ margin: 0 }} data-testid="shield-readonly-note">Declaring, adopting, re-scoping and retiring categories are DPO acts; this view is read-and-test for your role.</span>}
      </div>
      {tool === 'author' && canAuthor && <AuthorCategoryForm busy={busy} onCancel={() => setTool(null)} onSubmit={async body => { const r = await act('Declaration', '/api/shield/register', body); if (r) { setTool(null); setTab('force'); setSelected(r.category.name); } }} />}
      {tool === 'propose' && canAuthor && <ProposeForm busy={busy} onCancel={() => setTool(null)} onSubmit={async (text, ref) => { const r = await act('Proposal', '/api/shield/register/propose', { text, source_ref: ref }); if (r) { setTool(null); setTab('drafts'); setSelected(r.drafts[0]?.name || null); } }} />}
      {tool === 'test' && <TestPassage busy={busy} preview={preview} onTest={test} onClear={clearPreview} />}
      {category && <ShieldCategoryDetail category={category} canAuthor={canAuthor} busy={busy} onClose={() => setSelected(null)}
        onEnforce={(name, enforcement) => act('Scope change', `/api/shield/register/${name}/enforcement`, { enforcement })}
        onRemove={async (name, reason) => { if (await act('Retirement', `/api/shield/register/${name}?reason=${encodeURIComponent(reason)}`, undefined, 'DELETE')) setSelected(null); }}
        onAdopt={async name => { if (await act('Adoption', `/api/shield/register/${name}/adopt`, {})) setTab('force'); }}
        onDiscard={async name => { if (await act('Discard', `/api/shield/register/${name}/draft`, undefined, 'DELETE')) setSelected(null); }} />}
      {tab === 'force' && retired.length > 0 && !category && <p className="estate-note" data-testid="shield-retired-note">{retired.length} retired categor{retired.length === 1 ? 'y' : 'ies'} stay on the record: {retired.map(c => c.name).join(', ')}.</p>}
    </div>}
  </OwnerWorkspace>;
}
