import React from 'react';
import { stamp, statusClass } from './useModelApproval';
import { readableText } from '../shared/PresentationDetails';

export const modelName = r => r.base?.registry_id ? r.base.registry_id.replace(/-base$/, '').replace(/-/g, ' ').replace(/^qwen/i, 'Qwen') : r.name || 'Language model';

export function ModelRegistry({ models, health, checking, onCheck }) {
  const rows = models?.trained_adapters || [];
  return <section className="estate-section" data-testid="models-registry">
    <div className="estate-head"><h2>Approved models</h2><span className="estate-status" data-testid="models-registry-version">{rows.length} registered</span></div>
    {!rows.length && <p data-testid="models-registry-empty">No models have been approved.</p>}
    {rows.length > 0 && <table className="estate-table" data-testid="models-registry-table">
      <thead><tr><th>Model</th><th>Approval</th><th>Availability</th><th>Next check</th><th>Action</th></tr></thead>
      <tbody>{rows.map(r => { const h = health[r.model_id]; return <tr key={r.model_id} data-testid={`models-row-${r.model_id}`}>
        <td data-label="Model"><b>{modelName(r)} · {r.variant === 'pruned' ? 'Reduced' : 'Full'}</b><small>{r.cited_units?.toLocaleString('en-GB')} training units{r.excluded_unit_ids?.length ? ` · ${r.excluded_unit_ids.length} excluded after rights withdrawal` : ''}</small></td>
        <td data-label="Approval"><span className={`estate-status ${statusClass(r.status)}`} data-testid={`models-status-${r.model_id}`}>{r.status}</span>{r.withdrawal && <small>{readableText(r.withdrawal.reason)}</small>}{r.recall && <small>Recall recorded</small>}</td>
        <td data-label="Availability"><span data-testid={`models-serving-${r.model_id}`}>{r.serving?.status === 'running' ? 'Serving' : r.serving?.status || 'Not serving'}</span>{h && <small data-testid={`models-health-${r.model_id}`}>{readableText(h.status)}{h.health?.artefact_unaltered != null ? ` · Model file ${h.health.artefact_unaltered ? 'verified' : 'changed — review required'}` : ''}{h.health?.served_texts != null ? ` · ${h.health.served_texts} texts served` : ''}{h.health?.latency_seconds?.p95 != null ? ` · 95% of requests within ${h.health.latency_seconds.p95}s` : ''}{h.error ? ` · ${readableText(h.error)}` : ''}</small>}</td>
        <td data-label="Next check">{stamp(r.re_check_due_at)}<small>Approved {stamp(r.connected_at)}</small></td>
        <td data-label="Action">{r.serving?.status === 'running' && <button className="estate-btn" onClick={() => onCheck(r.model_id)} disabled={checking === r.model_id} data-testid={`models-check-${r.model_id}`}>{checking === r.model_id ? 'Checking…' : 'Check health'}</button>}</td>
      </tr>; })}</tbody>
    </table>}
  </section>;
}