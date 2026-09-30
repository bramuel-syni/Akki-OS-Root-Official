import React from 'react';
import { short, stamp, statusClass } from './useModelApproval';

export function ModelRegistry({ models, health, checking, onCheck }) {
  const rows = models?.trained_adapters || [];
  return <section className="estate-section" data-testid="models-registry">
    <div className="estate-head">
      <div><h2>Trained adapters on the registry</h2><p>Every row is a registry entry with its admission on record: artefact hash pinned on the host, recipe version (A17.3), the ruling it was admitted under, and whether it is being served, withdrawn or recalled.</p></div>
      <span className="estate-status" data-testid="models-registry-version">registry {models?.registry_version || '—'}</span>
    </div>
    {!rows.length && <div className="estate-note" data-testid="models-registry-empty">No trained adapter is on the registry. Admission writes the first entry; nothing is listed from a plan.</div>}
    {rows.length > 0 && <div className="estate-table-wrap"><table className="estate-table" data-testid="models-registry-table">
      <thead><tr><th>Model</th><th>Status</th><th>Base</th><th>Artefact</th><th>Ingredients</th><th>Admitted</th><th>Serving</th><th /></tr></thead>
      <tbody>{rows.map(r => {
        const h = health[r.model_id];
        return <tr key={r.model_id} data-testid={`models-row-${r.model_id}`}>
          <td><b>{r.model_id}</b><small>{r.variant} · {r.recipe_version?.slice(0, 28)}…{r.rederived_from ? ` · re-derived from ${r.rederived_from}` : ''}</small></td>
          <td><span className={`estate-status ${statusClass(r.status)}`} data-testid={`models-status-${r.model_id}`}>{r.status}</span>{r.recall && <small>recall · unit {r.recall.unit_id?.slice(0, 24)}…</small>}{r.withdrawal && <small>{r.withdrawal.reason}</small>}</td>
          <td>{r.base?.registry_id}<small>weights {short(r.base?.weight_sha256)}</small></td>
          <td><code>{short(r.artefact_sha256)}</code><small>{r.host}</small></td>
          <td>{r.cited_units?.toLocaleString('en-GB')} units{r.excluded_unit_ids?.length ? <small>{r.excluded_unit_ids.length} excluded by rights withdrawal</small> : null}</td>
          <td>{stamp(r.connected_at)}<small>re-check due {stamp(r.re_check_due_at)}</small></td>
          <td>{r.serving ? <><span className={`estate-status ${statusClass(r.serving.status)}`}>{r.serving.status}</span><small>{r.serving.host}:{r.serving.port} · {r.serving.job_id}</small></> : <small>not served</small>}
            {h && <small data-testid={`models-health-${r.model_id}`}>{h.status}{h.health?.artefact_unaltered != null ? ` · artefact ${h.health.artefact_unaltered ? 'unaltered' : 'ALTERED'}` : ''}{h.health?.served_texts != null ? ` · ${h.health.served_texts} texts served, ${h.health.refused_requests} refused` : ''}{h.health?.latency_seconds?.p95 != null ? ` · p95 ${h.health.latency_seconds.p95}s` : ''}{h.error ? ` · ${h.error}` : ''}</small>}</td>
          <td>{r.serving?.status === 'running' && <button className="estate-btn" onClick={() => onCheck(r.model_id)} disabled={checking === r.model_id} data-testid={`models-check-${r.model_id}`}>{checking === r.model_id ? 'Reading…' : 'Check health'}</button>}</td>
        </tr>;
      })}</tbody>
    </table></div>}
  </section>;
}
