import React, { useState } from 'react';

const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };
const Row = ({ label, children }) => <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">{label}</span>{children}</label>;
const list = v => v.split(/[\n,]/).map(s => s.trim()).filter(Boolean);

export function TransitionForm({ action, busy, onSubmit, onCancel }) {
  const [note, setNote] = useState(''), [version, setVersion] = useState('');
  const bind = action === 'bind_version';
  return <form data-testid={`armi-${action}-form`} onSubmit={e => { e.preventDefault(); onSubmit({ action, note: note || null, version: bind ? version : null }); }} style={{ marginTop: 12 }}>
    {bind && <Row label="Version or artefact digest to bind"><input data-testid="armi-bind-version-input" style={field} value={version} onChange={e => setVersion(e.target.value)} required maxLength={200} /></Row>}
    <Row label="Note for the record"><input data-testid={`armi-${action}-note`} style={field} value={note} onChange={e => setNote(e.target.value)} maxLength={600} placeholder={action === 'revoke' ? 'Why this identity leaves service (irreversible)' : 'Optional'} /></Row>
    <div className="estate-actions"><button type="submit" className={`estate-btn ${action === 'revoke' ? '' : 'primary'}`} data-testid={`armi-${action}-submit`} disabled={Boolean(busy)}>{busy ? 'Recording…' : action === 'bind_version' ? 'Bind version' : action[0].toUpperCase() + action.slice(1)}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid={`armi-${action}-cancel`}>Cancel</button></div>
  </form>;
}

export function AssignForm({ agents, busy, onSubmit, onCancel }) {
  const [task, setTask] = useState(''), [objective, setObjective] = useState(''), [collab, setCollab] = useState([]), [deps, setDeps] = useState([]);
  const toggle = (set, id) => set(v => (v.includes(id) ? v.filter(x => x !== id) : [...v, id]));
  return <form data-testid="armi-assign-form" onSubmit={e => { e.preventDefault(); onSubmit({ task, objective_ref: objective || null, collaborators: collab, depends_on: deps }); }} style={{ marginTop: 12 }}>
    <Row label="Task"><textarea data-testid="armi-assign-task" style={{ ...field, minHeight: 64 }} value={task} onChange={e => setTask(e.target.value)} required maxLength={1200} /></Row>
    <Row label="Business objective served (reference)"><input data-testid="armi-assign-objective" style={field} value={objective} onChange={e => setObjective(e.target.value)} placeholder="e.g. Mα MA-29 · ARMI lifecycle" /></Row>
    <span className="estate-label">Collaborators</span>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }}>{agents.map(a => <button type="button" key={a.agent_id} className={`estate-chip${collab.includes(a.agent_id) ? ' on' : ''}`} data-testid={`armi-assign-collab-${a.key}`} onClick={() => toggle(setCollab, a.agent_id)}>{a.name}</button>)}</div>
    <span className="estate-label">Depends on (must be active)</span>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }}>{agents.map(a => <button type="button" key={a.agent_id} className={`estate-chip${deps.includes(a.agent_id) ? ' on' : ''}`} data-testid={`armi-assign-dep-${a.key}`} onClick={() => toggle(setDeps, a.agent_id)}>{a.name}</button>)}</div>
    <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="armi-assign-submit" disabled={Boolean(busy) || !task.trim()}>{busy ? 'Recording…' : 'Assign work'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="armi-assign-cancel">Cancel</button></div>
  </form>;
}

export function CompleteForm({ busy, onSubmit, onCancel }) {
  const [outcome, setOutcome] = useState('completed'), [ref, setRef] = useState('');
  return <form data-testid="armi-complete-form" onSubmit={e => { e.preventDefault(); onSubmit({ outcome, result_ref: ref || null }); }} style={{ marginTop: 10 }}>
    <Row label="Outcome"><select data-testid="armi-complete-outcome" style={field} value={outcome} onChange={e => setOutcome(e.target.value)}><option value="completed">Completed</option><option value="failed">Failed</option></select></Row>
    <Row label="Result reference (artefact, receipt, job)"><input data-testid="armi-complete-result" style={field} value={ref} onChange={e => setRef(e.target.value)} maxLength={400} /></Row>
    <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="armi-complete-submit" disabled={Boolean(busy)}>{busy ? 'Recording…' : 'Record outcome'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="armi-complete-cancel">Cancel</button></div>
  </form>;
}

export function ScoreForm({ busy, onSubmit, onCancel }) {
  const [quality, setQuality] = useState('0.9'), [compliant, setCompliant] = useState(true), [evidence, setEvidence] = useState('');
  return <form data-testid="armi-score-form" onSubmit={e => { e.preventDefault(); onSubmit({ quality: Number(quality), compliant, evidence_ref: evidence }); }} style={{ marginTop: 10 }}>
    <Row label="Quality (share of acceptance met, 0–1)"><input data-testid="armi-score-quality" style={field} type="number" min="0" max="1" step="0.01" value={quality} onChange={e => setQuality(e.target.value)} required /></Row>
    <label style={{ display: 'flex', gap: 8, alignItems: 'center', fontSize: 12.5, marginBottom: 10 }}><input data-testid="armi-score-compliant" type="checkbox" checked={compliant} onChange={e => setCompliant(e.target.checked)} /> Compliant with the rules and Shield boundaries that applied</label>
    <Row label="Evidence (gate, test or review this score rests on — required)"><input data-testid="armi-score-evidence" style={field} value={evidence} onChange={e => setEvidence(e.target.value)} required maxLength={400} placeholder="test_reports/iteration_83.json · QA PASS" /></Row>
    <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="armi-score-submit" disabled={Boolean(busy) || !evidence.trim()}>{busy ? 'Recording…' : 'Record score'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="armi-score-cancel">Cancel</button></div>
  </form>;
}

export function OnboardForm({ busy, onSubmit, onCancel }) {
  const [v, setV] = useState({ kind: 'agent', name: '', role: '', job: '', can_do: '', cannot_do: '', objectives: '', version: '' });
  const set = k => e => setV(s => ({ ...s, [k]: e.target.value }));
  return <form data-testid="armi-onboard-form" onSubmit={e => { e.preventDefault(); onSubmit({ kind: v.kind, name: v.name, version: v.version || null, jd: { role: v.role, job: v.job, strengths: [], can_do: list(v.can_do), cannot_do: list(v.cannot_do) }, objectives: list(v.objectives) }); }} className="estate-section" style={{ marginTop: 16 }}>
    <h2 style={{ font: '400 20px var(--head)', margin: '0 0 12px' }}>Onboard an agent, model, LLM or skill</h2>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))', gap: '0 16px' }}>
      <Row label="Kind"><select data-testid="armi-onboard-kind" style={field} value={v.kind} onChange={set('kind')}>{['agent', 'llm', 'model', 'skill', 'worker'].map(k => <option key={k} value={k}>{k}</option>)}</select></Row>
      <Row label="Name"><input data-testid="armi-onboard-name" style={field} value={v.name} onChange={set('name')} required maxLength={160} /></Row>
      <Row label="Role (JD)"><input data-testid="armi-onboard-role" style={field} value={v.role} onChange={set('role')} required maxLength={120} /></Row>
      <Row label="Version (optional)"><input data-testid="armi-onboard-version" style={field} value={v.version} onChange={set('version')} maxLength={200} /></Row>
    </div>
    <Row label="Job description"><textarea data-testid="armi-onboard-job" style={{ ...field, minHeight: 56 }} value={v.job} onChange={set('job')} required maxLength={1200} /></Row>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))', gap: '0 16px' }}>
      <Row label="Can do (comma-separated)"><input data-testid="armi-onboard-can" style={field} value={v.can_do} onChange={set('can_do')} /></Row>
      <Row label="Cannot do (comma-separated)"><input data-testid="armi-onboard-cannot" style={field} value={v.cannot_do} onChange={set('cannot_do')} /></Row>
      <Row label="Business objectives served (comma-separated)"><input data-testid="armi-onboard-objectives" style={field} value={v.objectives} onChange={set('objectives')} /></Row>
    </div>
    <p className="estate-note">Onboarding records an identity as <b>onboarded, not yet admitted</b>. Admission remains a separate ceremony; activate it only once that record exists.</p>
    <div className="estate-actions" style={{ marginTop: 10 }}><button type="submit" className="estate-btn primary" data-testid="armi-onboard-submit" disabled={Boolean(busy)}>{busy ? 'Recording…' : 'Onboard'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="armi-onboard-cancel">Cancel</button></div>
  </form>;
}
