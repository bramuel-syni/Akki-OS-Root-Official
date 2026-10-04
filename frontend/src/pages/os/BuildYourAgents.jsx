/*
 * BuildYourAgents.jsx — v2 OS · Your Resources · Your Agents · LIVE (ARMI).
 *
 * The supplied "Your Agents" list is bound to the tenant's ARMI register (/api/armi/agents); choosing a row opens the operational
 * profile — JD, objectives, capabilities and limits, admission, evidence-based compliance, resources, work, collaborators, lifecycle
 * and assignments. Operators onboard, activate/suspend/revoke, bind versions, assign, complete and score. The prototype's four-step
 * "Deploy" wizard is not shown: it has no real backing yet, and lifecycle changes are recorded through the profile instead.
 */
import React, { useState } from 'react';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { readableText } from '@/components/shared/PresentationDetails';
import { useArmi, pct, hoursLabel, STATUS_TONE, slug } from '@/components/armi/useArmi';
import { ArmiProfile } from '@/components/armi/ArmiProfile';
import { ArmiAssignments } from '@/components/armi/ArmiAssignments';
import { OnboardForm } from '@/components/armi/ArmiForms';
import { ArmiRateCard } from '@/components/armi/ArmiRateCard';
import { ArmiRouting } from '@/components/armi/ArmiRouting';
import '@/components/estate/estate.css';

const KIND = { agent: 'Agent', llm: 'LLM role', model: 'Model', skill: 'Skill', worker: 'Worker' };

export default function BuildYourAgents() {
  const session = usePrototypeSession();
  const canOperate = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const { overview, agents, agent, selected, loading, busy, error, notice, reload, select, act } = useArmi(Boolean(session.data));
  const [onboarding, setOnboarding] = useState(false), [kind, setKind] = useState('all');
  const rows = (agents || []).filter(a => kind === 'all' || a.kind === kind);
  const banner = error || notice || (loading ? 'Reading the agent register…' : '');
  const model = {
    isBuildGroup: true, isBuildYourAgents: true, hasSessionBanner: Boolean(banner), sessionBanner: readableText(banner), sessionBannerColor: error ? 'var(--oxblood)' : 'var(--ink3)',
    agentsListView: rows.map(a => { const [statusColor, statusBg] = STATUS_TONE[a.status] || STATUS_TONE.onboarded; const c = a.compliance; return { key: slug(a.agent_id), id: a.agent_id, name: readableText(a.name), status: a.status, statusColor, statusBg, canDeploy: false, selected: selected === a.agent_id,
      scope: `${KIND[a.kind] || a.kind} · ${a.jd?.role || 'no job description'}${c?.value != null ? ` · compliance ${pct(c.value)} (n=${c.n})` : ' · compliance not measured'}${a.resources?.gpu_hours ? ` · ${hoursLabel(a.resources.gpu_hours)}` : ''}`, onOpen: () => select(selected === a.agent_id ? null : a.agent_id) }; }),
  };
  const on = (label, path, body, id) => act(label, path, body, id ?? selected);
  return <OwnerWorkspace session={session} title="Your Agents" group="Your Resources" section="build" model={model}
    enhance={{ 167: { 'data-testid': 'workspace-title' }, 8008: (c, props) => ({ role: 'button', tabIndex: 0, 'data-testid': `armi-agent-row-${c.ag.key}`, 'aria-pressed': c.ag.selected, onClick: c.ag.onOpen, onKeyDown: e => { if (['Enter', ' '].includes(e.key)) { e.preventDefault(); c.ag.onOpen(); } }, style: { ...props.style, cursor: 'pointer', borderColor: c.ag.selected ? 'var(--blue)' : undefined, background: c.ag.selected ? 'var(--surface)' : '#fff' } }) }}>
    <div className="estate" data-testid="armi-surface" style={{ maxWidth: 1180, marginTop: 24 }}>
      {overview && <section className="estate-section" data-testid="armi-overview">
        <header className="estate-head"><div><h2>Agent Resource Management</h2><p>Every admitted agent, LLM role, model, skill and worker working in this estate, with the evidence behind each figure. Watch behavioural profiles are never exported here and no conduct probability is invented.</p></div>
          <div className="estate-actions" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button className="estate-btn" data-testid="armi-reload" onClick={reload} disabled={loading}>{loading ? 'Reading…' : 'Refresh'}</button>
            {canOperate && <button className="estate-btn" data-testid="armi-sync" onClick={() => on('Register sync', '/api/armi/sync', {}, null)} disabled={Boolean(busy)}>{busy === 'Register sync' ? 'Deriving…' : 'Re-derive from records'}</button>}
            {canOperate && <button className="estate-btn primary" data-testid="armi-onboard-open" onClick={() => setOnboarding(v => !v)}>{onboarding ? 'Close' : 'Onboard'}</button>}
          </div></header>
        <div className="estate-tiles">
          <div className="estate-tile" data-testid="armi-overview-agents"><span className="estate-label">On the register</span><b>{overview.agents}</b><small>{Object.entries(overview.by_kind || {}).map(([k, v]) => `${v} ${KIND[k] || k}${v === 1 ? '' : 's'}`).join(' · ')}</small></div>
          <div className="estate-tile sage" data-testid="armi-overview-status"><span className="estate-label">Lifecycle</span><b>{overview.by_status?.active ?? 0} active</b><small>{overview.by_status?.onboarded ?? 0} onboarded · {overview.by_status?.suspended ?? 0} suspended · {overview.by_status?.revoked ?? 0} revoked</small></div>
          <div className="estate-tile brass" data-testid="armi-overview-gpu"><span className="estate-label">Resources metered</span><b>{hoursLabel(overview.gpu_hours_total)}</b><small>{overview.cost_usd == null ? overview.cost_note : `$${overview.cost_usd} · ${overview.cost_note}`}</small></div>
          <div className="estate-tile" data-testid="armi-overview-contribution"><span className="estate-label">Business contribution</span><b>{overview.contribution?.deliveries_total ?? 0} deliveries</b><small>{overview.contribution?.attributed ?? 0} credited to an authoring role · {overview.contribution?.unattributed ?? 0} platform aggregates · {overview.contribution?.amount_usd == null ? 'unpriced' : `$${overview.contribution.amount_usd} metered`}</small></div>
          <div className="estate-tile oxblood" data-testid="armi-overview-protected"><span className="estate-label">Protected</span><b>Watch not exported</b><small>{overview.protected?.malicious_probability}</small></div>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 14 }} data-testid="armi-kind-filter">{['all', 'agent', 'llm', 'model', 'skill', 'worker'].map(k => <button key={k} className={`estate-chip${kind === k ? ' on' : ''}`} data-testid={`armi-filter-${k}`} onClick={() => setKind(k)}>{k === 'all' ? `All (${(agents || []).length})` : `${KIND[k]}s (${(agents || []).filter(a => a.kind === k).length})`}</button>)}</div>
      </section>}
      {onboarding && canOperate && <OnboardForm busy={busy} onCancel={() => setOnboarding(false)} onSubmit={async body => { const r = await on('Onboarding', '/api/armi/agents', body, null); if (r) { setOnboarding(false); select(r.agent.agent_id); } }} />}
      <ArmiRateCard canOperate={canOperate} onChanged={reload} />
      {selected && !agent && !error && <p className="estate-note" data-testid="armi-profile-loading">Reading the profile…</p>}
      {agent && <div style={{ marginTop: 16 }}>
        <ArmiProfile agent={agent} agents={agents} canOperate={canOperate} busy={busy}
          onTransition={body => on(body.action === 'bind_version' ? 'Version binding' : body.action[0].toUpperCase() + body.action.slice(1), `/api/armi/agents/${agent.agent_id}/transition`, body)}
          onAssign={body => on('Assignment', `/api/armi/agents/${agent.agent_id}/assign`, body)} />
        {agent.kind === 'llm' && <ArmiRouting role={agent.agent_id.split(':')[1]} canOperate={canOperate} />}
        <ArmiAssignments agent={agent} canOperate={canOperate} busy={busy}
          onComplete={(id, body) => on('Outcome', `/api/armi/assignments/${id}/complete`, body)}
          onScore={(id, body) => on('Score', `/api/armi/assignments/${id}/score`, body)} />
      </div>}
      {!canOperate && session.data && <p className="estate-note" data-testid="armi-readonly-note">Lifecycle changes need an admitted operator; this view is read-only for your role.</p>}
    </div>
  </OwnerWorkspace>;
}
