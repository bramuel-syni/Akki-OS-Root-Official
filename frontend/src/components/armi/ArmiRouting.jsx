import React, { useCallback, useEffect, useState } from 'react';
import { apiRequest, stamp } from '../models/useModelApproval';
import { pct } from './useArmi';

const ms = v => (v == null ? '—' : v >= 1000 ? `${Math.round(v / 100) / 10} s` : `${v} ms`);
const key = m => String(m).replace(/[^A-Za-z0-9]+/g, '-').toLowerCase();

// Mα MA-08: a role's model rests on a measured trial — every candidate ran the same fixed task set through the same Shield boundary.
export function ArmiRouting({ role, canOperate }) {
  const [state, setState] = useState({ assignment: null, trials: null, trial: null, busy: null, error: null });
  const load = useCallback(async () => {
    try {
      const [a, t] = await Promise.all([apiRequest('/api/routing/assignments'), apiRequest(`/api/routing/trials?role=${role}`)]);
      const latest = t.trials?.[0]; const full = latest ? (await apiRequest(`/api/routing/trials/${latest.trial_id}`)).trial : null;
      setState(s => ({ ...s, assignment: a.roles.find(r => r.role === role), trials: t.trials, trial: full, error: null }));
    } catch (e) { setState(s => ({ ...s, error: e.message })); }
  }, [role]);
  useEffect(() => { load(); }, [load]);
  useEffect(() => { if (state.trial?.status === 'running') { const id = setTimeout(load, 8000); return () => clearTimeout(id); } return undefined; }, [state.trial, load]);
  const act = async (label, path, body) => { setState(s => ({ ...s, busy: label, error: null })); try { await apiRequest(path, { method: 'POST', body: JSON.stringify(body || {}) }); await load(); } catch (e) { setState(s => ({ ...s, error: e.message })); } setState(s => ({ ...s, busy: null })); };
  const { assignment: a, trial: t, busy, error } = state;
  if (!a) return null;
  const d = a.decision;
  return <section className="estate-section" data-testid="armi-routing" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Measured routing</h2>
      <p data-testid="armi-routing-basis">{d ? <>Adopted on measured evidence: <b>{d.model}</b> from trial {d.trial_id} ({stamp(d.adopted_at)}); configured fallback {a.configured_model}. </> : <>Configured assignment <b>{a.model}</b>; no measured trial adopted yet. </>}
        Candidates run the same fixed task set (version {a.task_set_version || t?.task_set_version || '—'}) through the Shield chokepoint on SYNTHETIC briefs and licensed aggregates; the lowest-cost candidate meeting every floor is recommended. Cost is owner-priced or stated unknown — never estimated.</p></div>
      {canOperate && <div className="estate-actions" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {a.task_set_defined ? <button className="estate-btn primary" data-testid="armi-routing-run" disabled={Boolean(busy) || t?.status === 'running'} onClick={() => act('trial', '/api/routing/trials', { role })}>{t?.status === 'running' ? 'Measuring…' : 'Run trial'}</button> : <span className="estate-note" style={{ margin: 0 }} data-testid="armi-routing-no-taskset">No fixed task set for this role yet — a trial would be catalogue rank, not evidence.</span>}
        {d && <button className="estate-btn" data-testid="armi-routing-revert" disabled={Boolean(busy)} onClick={() => act('revert', '/api/routing/revert', { role, note: 'reverted to configured assignment' })}>Revert to configured</button>}
      </div>}
    </header>
    {error && <p className="estate-alert" data-testid="armi-routing-error">{error}</p>}
    {!t ? <p className="estate-note" data-testid="armi-routing-empty">No trial recorded for this role.</p> : <>
      <div className="estate-meta" data-testid="armi-routing-trial-meta"><span>trial {t.trial_id}</span><span>{t.status}{t.reason ? ` · ${t.reason}` : ''}</span><span>{t.tasks.length} tasks · {t.candidates.length} candidates</span><span>floors: pass {pct(t.floors.pass_rate)} · JSON {pct(t.floors.json_rate)} · p50 ≤ {ms(t.floors.latency_ms_p50_max)} · refusals ≤ {t.floors.refusals_max}</span><span>{stamp(t.started_at)}</span></div>
      <div className="estate-table-wrap"><table className="estate-table" data-testid="armi-routing-table">
        <thead><tr><th>Candidate</th><th>Accepted</th><th>Strict JSON</th><th>Refusals</th><th>Latency p50</th><th>Tokens in / out</th><th>Cost</th><th>Floors</th>{canOperate && <th />}</tr></thead>
        <tbody>{t.candidates.map(c => <tr key={c.model} data-testid={`armi-routing-row-${key(c.model)}`}>
          <td data-label="Candidate" style={{ whiteSpace: 'normal' }}><b>{c.model}</b><small>{c.provider}{c.incumbent ? ' · incumbent' : ''}{t.recommendation?.model === c.model ? ' · recommended' : ''}{d?.model === c.model && d?.trial_id === t.trial_id ? ' · adopted' : ''}</small></td>
          <td data-label="Accepted">{pct(c.pass_rate)}</td><td data-label="Strict JSON">{pct(c.json_rate)}</td><td data-label="Refusals">{c.refusals ?? '—'}</td><td data-label="Latency p50">{ms(c.latency_ms_p50)}</td>
          <td data-label="Tokens">{c.tokens_in == null ? '—' : `${c.tokens_in} / ${c.tokens_out}`}</td><td data-label="Cost">{c.cost_usd == null ? <small>{c.cost_basis ? 'unknown' : '—'}</small> : `$${c.cost_usd}`}</td>
          <td data-label="Floors"><span className={`estate-status ${c.meets_floors == null ? '' : c.meets_floors ? 'complete' : 'blocked'}`} data-testid={`armi-routing-floors-${key(c.model)}`}>{c.meets_floors == null ? 'measuring' : c.meets_floors ? 'met' : 'not met'}</span></td>
          {canOperate && <td data-label="Adopt">{t.status === 'measured' && c.meets_floors && !(d?.model === c.model) && <button className="estate-btn" data-testid={`armi-routing-adopt-${key(c.model)}`} disabled={Boolean(busy)} onClick={() => act('adopt', `/api/routing/trials/${t.trial_id}/adopt`, { model: c.model, note: 'adopted from measured trial' })}>Adopt</button>}</td>}
        </tr>)}</tbody></table></div>
      {t.recommendation && <p className="estate-note" data-testid="armi-routing-recommendation"><b>Recommendation:</b> {t.recommendation.model || 'none'} — {t.recommendation.basis}</p>}
      {t.candidates.some(c => c.tasks?.some(x => !x.accepted)) && <details data-testid="armi-routing-findings"><summary className="estate-label" style={{ cursor: 'pointer' }}>Why candidates failed</summary><ul className="estate-list">{t.candidates.flatMap(c => (c.tasks || []).filter(x => !x.accepted).map(x => <li key={`${c.model}-${x.task_id}`}><span><b>{c.model}</b> · {x.task_id} · {x.product}</span><small>{(x.findings || []).join(' · ')}</small></li>))}</ul></details>}
    </>}
  </section>;
}
