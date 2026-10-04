import React, { useState } from 'react';
import { stamp } from '../models/useModelApproval';
import { readableText } from '../shared/PresentationDetails';
import { pct, slug } from './useArmi';
import { CompleteForm, ScoreForm } from './ArmiForms';

const TONE = { assigned: 'partial', completed: 'complete', failed: 'blocked', cancelled: 'blocked' };

export function ArmiAssignments({ agent, canOperate, busy, onComplete, onScore }) {
  const [form, setForm] = useState(null);
  const rows = agent.assignments || [];
  return <section className="estate-section" data-testid="armi-assignments" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Assignments</h2><p>Work given to this identity on the register: assign → complete → score. A score without an evidence reference is refused; scores fold into the compliance figure as their own evidence line.</p></div></header>
    {!rows.length ? <p className="estate-note" data-testid="armi-assignments-empty">No assignments recorded.</p> : <div className="estate-table-wrap"><table className="estate-table" data-testid="armi-assignments-table">
      <thead><tr><th>Task</th><th>State</th><th>Collaborators · dependencies</th><th>Result</th><th>Score</th>{canOperate && <th /> }</tr></thead>
      <tbody>{rows.map(r => <tr key={r.assignment_id} data-testid={`armi-assignment-${r.assignment_id}`}>
        <td style={{ whiteSpace: 'normal', maxWidth: 320 }}><b>{r.task}</b><small>{r.objective_ref ? `objective · ${r.objective_ref} · ` : ''}assigned {stamp(r.at)}</small></td>
        <td><span className={`estate-status ${TONE[r.status] || ''}`} data-testid={`armi-assignment-status-${r.assignment_id}`}>{r.status}</span>{r.cancelled_reason && <small>{r.cancelled_reason}</small>}</td>
        <td><small>{(r.collaborators || []).map(readableText).join(', ') || 'none'}</small><small>{r.depends_on?.length ? `depends on ${r.depends_on.map(readableText).join(', ')}` : ''}</small></td>
        <td>{r.result_ref ? readableText(r.result_ref) : '—'}<small>{r.completed_at ? `${stamp(r.completed_at)}` : ''}</small></td>
        <td>{r.score ? <>{pct(r.score.quality)}<small>{r.score.compliant ? 'compliant' : 'non-compliant'} · {readableText(r.score.evidence_ref)}</small></> : '—'}</td>
        {canOperate && <td>{r.status === 'assigned' && <button className="estate-btn" data-testid={`armi-complete-${r.assignment_id}`} onClick={() => setForm(form?.id === r.assignment_id ? null : { id: r.assignment_id, kind: 'complete' })} disabled={Boolean(busy)}>Complete</button>}
          {r.status === 'completed' && !r.score && <button className="estate-btn" data-testid={`armi-score-${r.assignment_id}`} onClick={() => setForm(form?.id === r.assignment_id ? null : { id: r.assignment_id, kind: 'score' })} disabled={Boolean(busy)}>Score</button>}</td>}
      </tr>)}</tbody>
    </table></div>}
    {form?.kind === 'complete' && <CompleteForm busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onComplete(form.id, body)) setForm(null); }} />}
    {form?.kind === 'score' && <ScoreForm busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onScore(form.id, body)) setForm(null); }} />}
    <h3>Lifecycle record</h3>
    <ul className="estate-list" data-testid="armi-lifecycle">{(agent.lifecycle || []).slice().reverse().map((e, i) => <li key={i} data-testid={`armi-lifecycle-${slug(e.action)}-${i}`}><span><b>{e.action.replace('_', ' ')}</b>{e.note ? ` — ${e.note}` : ''}{e.version ? ` → ${e.version}` : ''}</span><small>{stamp(e.at)} · {readableText(String(e.by))}</small></li>)}</ul>
  </section>;
}
