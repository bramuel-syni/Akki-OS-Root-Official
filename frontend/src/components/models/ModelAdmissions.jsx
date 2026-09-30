import React from 'react';
import { stamp, statusClass } from './useModelApproval';

export function ModelAdmissions({ records }) {
  const rows = records || [];
  return <section className="estate-section" data-testid="models-admissions">
    <div className="estate-head"><div><h2>Admission decisions</h2><p>Per-stratum acceptance is the Outcome's recorded threshold plus no regression below the base (Docs 17–19 · owner ruling 2026-09-30 1a). The aggregate +5-point M-a criterion stays global. Original refusals remain on file; each decision here is a new record.</p></div></div>
    {!rows.length && <div className="estate-note" data-testid="models-admissions-empty">No re-adjudication is on record.</div>}
    {rows.length > 0 && <div className="estate-table-wrap"><table className="estate-table" data-testid="models-admissions-table">
      <thead><tr><th>Candidate</th><th>Decision</th><th>Strata meeting floor</th><th>Per stratum (adapter / base)</th><th>Floor</th><th>Decided</th></tr></thead>
      <tbody>{rows.map(r => <tr key={`${r.model_id}-${r.at}`} data-testid={`models-admission-${r.model_id}`}>
        <td><b>{r.model_id}</b><small>{r.variant} artefact · run {r.job_id}</small></td>
        <td><span className={`estate-status ${statusClass(r.readjudicated?.outcome)}`}>{r.readjudicated?.outcome}</span>{r.readjudicated?.registry_version_after != null && <small>registry v{r.readjudicated.registry_version_after}</small>}{r.readjudicated?.reason && <small>{r.readjudicated.reason}</small>}</td>
        <td><b>{Math.round((r.coverage_strata || 0) * 100)}%</b><small>{Object.values(r.per_stratum || {}).filter(s => s.passes).length} of {Object.keys(r.per_stratum || {}).length}</small></td>
        <td className="estate-dims">{Object.entries(r.per_stratum || {}).map(([s, v]) => <span key={s} style={v.passes ? undefined : { background: 'rgba(184,57,91,.12)', color: 'var(--oxblood)' }}>{s} {(v.accuracy * 100).toFixed(1)} / {(v.base_accuracy * 100).toFixed(1)}</span>)}</td>
        <td>{r.outcome_floor}<small>{r.floor_source}</small></td>
        <td>{stamp(r.at)}</td>
      </tr>)}</tbody>
    </table></div>}
  </section>;
}

export function ModelCapabilities({ capabilities }) {
  if (!capabilities) return null;
  return <section className="estate-section" data-testid="models-capabilities">
    <div className="estate-head"><div><h2>Capability account for G9</h2><p>{capabilities.owner_ruling_ref}</p></div></div>
    <div className="estate-columns">
      <div><h3>Activated</h3><ul className="estate-list">{capabilities.activated.map(c => <li key={c.capability} data-testid="models-capability-activated"><span><b>{c.capability}</b><small>{c.evidence}</small><small>admitted {c.admitted_models.join(', ') || 'none'} · served {c.served_models.join(', ') || 'none'}</small></span><small><span className="estate-status complete">{c.modality}</span></small></li>)}</ul></div>
      <div><h3>Dormant · not claimed</h3><ul className="estate-list">{capabilities.dormant.map(c => <li key={c.capability} data-testid="models-capability-dormant"><span><b>{c.capability}</b><small>{c.status}</small><small>{c.why}</small>{c.reactivation && <small>Reactivation: {c.reactivation}</small>}{c.arms_on_record?.length ? <small>{c.arms_on_record.length} research arms on record, all NOT ADMISSIBLE</small> : null}</span><small><span className="estate-status blocked">{c.modality}</span></small></li>)}</ul></div>
    </div>
  </section>;
}
