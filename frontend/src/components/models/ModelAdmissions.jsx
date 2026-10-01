import React from 'react';
import { stamp, statusClass } from './useModelApproval';
import { modelName } from './ModelRegistry';
import { readableText } from '../shared/PresentationDetails';

const languages = { guz: 'Gusii', kam: 'Kamba', kik: 'Kikuyu', kln: 'Kalenjin', luo: 'Luo', lwg: 'Luhya', swa: 'Swahili' };

export function ModelAdmissions({ records, models }) {
  const rows = records || [];
  const jobs = [...new Set(rows.map(r => r.job_id))];
  return <section className="estate-section" data-testid="models-admissions">
    <div className="estate-head"><h2>Evaluation decisions</h2></div>
    {!rows.length && <p data-testid="models-admissions-empty">No evaluation decisions recorded.</p>}
    {rows.length > 0 && <table className="estate-table" data-testid="models-admissions-table">
      <thead><tr><th>Candidate</th><th>Decision & next step</th><th>Languages passed</th><th>Accuracy · candidate / base</th><th>Minimum</th></tr></thead>
      <tbody>{rows.map((r, i) => { const model = models?.trained_adapters?.find(m => m.model_id === r.model_id); const failed = Object.entries(r.per_stratum || {}).filter(([, s]) => !s.passes); return <tr key={`${r.model_id}-${r.at}`} data-testid={`models-admission-${r.model_id}-${i}`}>
        <td data-label="Candidate"><b>{model ? modelName(model) : `Language candidate ${jobs.indexOf(r.job_id) + 1}`} · {r.variant === 'pruned' ? 'Reduced' : 'Full'}</b><small>{stamp(r.at)}</small></td>
        <td data-label="Decision"><span className={`estate-status ${statusClass(r.readjudicated?.outcome)}`}>{r.readjudicated?.outcome}</span><small data-testid={`models-admission-next-${i}`}>{failed.length ? `Review ${failed.map(([key, s]) => `${languages[key] || key}: ${!s.no_regression_below_base ? 'below base performance' : 'below required accuracy'}`).join('; ')} before resubmission.` : r.readjudicated?.outcome === 'admitted' ? 'Approved. Serving is managed separately.' : readableText(r.readjudicated?.refusal_note || r.readjudicated?.reason || 'Review the evaluation before resubmission.')}</small></td>
        <td data-label="Languages passed">{Object.values(r.per_stratum || {}).filter(s => s.passes).length} of {Object.keys(r.per_stratum || {}).length}</td>
        <td data-label="Accuracy" className="estate-dims">{Object.entries(r.per_stratum || {}).map(([s, v]) => <span key={s} style={v.passes ? undefined : { background: 'rgba(184,57,91,.12)', color: 'var(--oxblood)' }}>{languages[s] || s} {(v.accuracy * 100).toFixed(1)}% / {(v.base_accuracy * 100).toFixed(1)}%</span>)}</td>
        <td data-label="Minimum">{r.outcome_floor == null ? 'Not recorded' : `${(r.outcome_floor * 100).toFixed(0)}%`}<small>No regression below the base</small></td>
      </tr>; })}</tbody>
    </table>}
  </section>;
}

export function ModelCapabilities({ capabilities }) {
  if (!capabilities) return null;
  return <section className="estate-section" data-testid="models-capabilities"><div className="estate-head"><h2>Available capabilities</h2></div>
    <div className="estate-columns"><div><h3>Active</h3><ul className="estate-list">{capabilities.activated.map((c, i) => <li key={c.capability} data-testid={`models-capability-activated-${i}`}><span><b>{readableText(c.capability).replaceAll('_', ' ')}</b><small>{c.admitted_models.length} approved models · {c.served_models.length} serving</small></span><small>{c.modality}</small></li>)}</ul></div>
      <div><h3>Not activated</h3><ul className="estate-list">{capabilities.dormant.map((c, i) => <li key={c.capability} data-testid={`models-capability-dormant-${i}`}><span><b>{readableText(c.capability).replaceAll('_', ' ')}</b><small>{readableText(c.why)}</small>{c.reactivation && <small>Before activation: {readableText(c.reactivation)}</small>}</span></li>)}</ul></div></div>
  </section>;
}