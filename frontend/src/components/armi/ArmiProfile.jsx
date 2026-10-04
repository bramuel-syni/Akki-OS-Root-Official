import React, { useState } from 'react';
import { stamp } from '../models/useModelApproval';
import { readableText } from '../shared/PresentationDetails';
import { pct, hoursLabel, STATUS_TONE, slug } from './useArmi';
import { TransitionForm, AssignForm } from './ArmiForms';

const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`armi-tile-${id}`}><span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;
const Pills = ({ id, items, empty }) => items?.length ? <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }} data-testid={`armi-${id}`}>{items.map((x, i) => <span key={i} className="estate-status" style={{ textTransform: 'none', fontFamily: 'var(--body)!important' }}>{x}</span>)}</div> : <p className="estate-note" style={{ margin: 0 }}>{empty}</p>;
const Score = s => (s?.value == null ? 'not measured' : pct(s.value));
const scoreNote = s => (s ? `${s.passed} of ${s.n} · ${s.basis}` : 'no basis recorded');
// Derived evidence leads; scored manual assignments are their own evidence line and carry the figure when nothing else is measured.
const compliance = (comp, asg) => {
  const manual = asg?.compliance;
  if (!manual?.n) return [comp, scoreNote(comp)];
  if (!comp?.n) return [manual, scoreNote(manual)];
  return [comp, `${scoreNote(comp)} · plus ${manual.passed} of ${manual.n} scored assignments compliant`];
};

export function ArmiProfile({ agent, agents, canOperate, busy, onTransition, onAssign }) {
  const [form, setForm] = useState(null);
  const [color, bg] = STATUS_TONE[agent.status] || STATUS_TONE.onboarded;
  const jd = agent.jd || {}, asg = agent.assignment_summary, res = agent.resources || {}, work = agent.work || {}, contrib = agent.contribution || {};
  const [comp, compNote] = compliance(agent.compliance, asg);
  const peers = (agents || []).filter(a => a.agent_id !== agent.agent_id).map(a => ({ agent_id: a.agent_id, name: a.name, key: slug(a.agent_id) }));
  const actions = agent.status === 'revoked' ? [] : [agent.status === 'active' ? ['suspend', 'Suspend'] : ['activate', 'Activate'], ['bind_version', 'Bind version'], ['revoke', 'Revoke']];
  return <section className="estate-section" data-testid="armi-profile">
    <header className="estate-head"><div>
      <span className="estate-label">{agent.kind} · {readableText(agent.agent_id)}</span>
      <h2 data-testid="armi-profile-name">{readableText(agent.name)}</h2>
      <p data-testid="armi-profile-jd">{jd.role ? <b>{jd.role}. </b> : null}{jd.job}</p>
    </div><div style={{ textAlign: 'right' }}>
      <span className="estate-status" data-testid="armi-profile-status" style={{ background: bg, color }}>{agent.status}</span>
      <div className="estate-meta" style={{ justifyContent: 'flex-end' }}><span data-testid="armi-profile-version">version {agent.version || 'not bound'}</span><span>synced {stamp(agent.synced_at)}</span></div>
    </div></header>
    <div className="estate-tiles">
      <Tile id="compliance" label="Compliance" value={Score(comp)} note={compNote} tone={comp?.value == null ? undefined : comp.value >= 0.9 ? 'sage' : 'brass'} />
      <Tile id="admission" label="Admission" value={String(agent.admission?.decision || 'not recorded')} note={agent.admission?.record ? `record · ${readableText(String(agent.admission.record))}` : 'no admission record'} />
      <Tile id="resources" label="Resources consumed" value={hoursLabel(res.gpu_hours)} note={res.cost_usd == null ? (res.cost_note || 'cost not priced — no governed rate card') : `$${res.cost_usd} · ${res.cost_note || 'owner-supplied rate'}`} />
      <Tile id="work" label="Work completed" value={String(work.assignments_completed ?? 0)} note={`${work.kind || 'assignments'}${work.assignments_failed ? ` · ${work.assignments_failed} failed` : ''}${asg ? ` · ${asg.completed} manual assignments done, quality ${asg.mean_quality ?? '—'}` : ''}`} />
      <Tile id="behaviour" label="Conduct risk" value="not computed" note={agent.behaviour?.malicious_conduct_probability || 'Watch profiles are never exported here'} tone="oxblood" />
      <Tile id="contribution" label="Business contribution" value={contrib.deliveries ? `${contrib.deliveries} deliveries` : '—'} tone={contrib.deliveries ? 'sage' : undefined}
        note={contrib.deliveries ? `${contrib.revenue_attributed_usd == null ? 'unpriced' : `$${contrib.revenue_attributed_usd} metered`} · ${contrib.basis}` : (contrib.basis || contrib.revenue_note || 'no attributed contribution')} />
    </div>
    <div className="estate-columns" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))', gap: 18, marginTop: 18 }}>
      <div><h3>Strengths</h3><Pills id="strengths" items={jd.strengths} empty="None recorded." /></div>
      <div><h3>Can do</h3><Pills id="can-do" items={jd.can_do} empty="None recorded." /></div>
      <div><h3>Cannot do</h3><Pills id="cannot-do" items={jd.cannot_do} empty="None recorded." /></div>
      <div><h3>Business objectives served</h3><Pills id="objectives" items={agent.objectives} empty="No objective bound." /></div>
      <div><h3>Capabilities</h3><Pills id="capabilities" items={agent.capabilities} empty="None recorded." /></div>
      <div><h3>Limits</h3><Pills id="limits" items={agent.limits} empty="None recorded." /></div>
    </div>
    <h3>Collaborators</h3>
    <Pills id="collaborators" items={(agent.collaborators || []).map(c => `${readableText(c.agent_id)} · ${c.shared}`)} empty="No recorded co-work." />
    {canOperate && <div style={{ marginTop: 18 }}>
      <div className="estate-actions" data-testid="armi-profile-actions" style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {agent.status !== 'revoked' && <button className="estate-btn primary" data-testid="armi-action-assign" onClick={() => setForm(form === 'assign' ? null : 'assign')} disabled={Boolean(busy)}>Assign work</button>}
        {actions.map(([a, label]) => <button key={a} className="estate-btn" data-testid={`armi-action-${a}`} onClick={() => setForm(form === a ? null : a)} disabled={Boolean(busy)}>{label}</button>)}
        {agent.status === 'revoked' && <span className="estate-note" style={{ margin: 0 }} data-testid="armi-revoked-note">Revoked identities cannot be reactivated; onboard a new identity with its own record.</span>}
      </div>
      {form === 'assign' && <AssignForm agents={peers} busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onAssign(body)) setForm(null); }} />}
      {form && form !== 'assign' && <TransitionForm action={form} busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onTransition(body)) setForm(null); }} />}
    </div>}
  </section>;
}
