import React, { useCallback, useEffect, useState } from 'react';
import { apiRequest, stamp } from '../models/useModelApproval';

const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };
const Row = ({ label, children }) => <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">{label}</span>{children}</label>;
const LANE = { gpu_hours: { label: 'GPU hour', id: 'node_id', idHint: '* for every host, or akki-vm / akki-vm-ii', rate: 'rate_per_hour', unit: 'USD per GPU-hour' }, caas: { label: 'CaaS delivery', id: 'product_id', idHint: '* for every product, or e.g. domain.media_plan', rate: 'rate_per_delivery', unit: 'USD per delivery' } };
const rateOf = r => Object.entries(r).find(([k, v]) => k.startsWith('rate_') && typeof v === 'number');

// Owner-supplied rate card (cost_ledger rates register). Measured hours and deliveries become money only through a row authored here with its source.
export function ArmiRateCard({ canOperate, onChanged }) {
  const [rates, setRates] = useState(null), [open, setOpen] = useState(false), [busy, setBusy] = useState(false), [error, setError] = useState(null);
  const [v, setV] = useState({ lane: 'gpu_hours', id: '*', rate: '', source: '', notes: '' });
  const load = useCallback(() => apiRequest('/api/cost_ledger/rates').then(setRates).catch(e => setError(e.message)), []);
  useEffect(() => { load(); }, [load]);
  const spec = LANE[v.lane]; const set = k => e => setV(s => ({ ...s, [k]: e.target.value }));
  const rows = rates ? Object.entries(rates).filter(([k, x]) => Array.isArray(x) && k !== 'lanes').flatMap(([lane, xs]) => xs.map(r => ({ lane, ...r }))) : [];
  const submit = async e => {
    e.preventDefault(); setBusy(true); setError(null);
    try { await apiRequest(`/api/cost_ledger/rates/${v.lane}`, { method: 'POST', body: JSON.stringify({ [spec.id]: v.id.trim(), [spec.rate]: Number(v.rate), source: v.source, notes: v.notes || null }) }); setOpen(false); setV(s => ({ ...s, rate: '', source: '', notes: '' })); await load(); onChanged?.(); }
    catch (err) { setError(err.message || 'The rate could not be recorded.'); }
    setBusy(false);
  };
  return <section className="estate-section" data-testid="armi-rate-card" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Rate card</h2><p>Owner-supplied rates only. Hours and deliveries are measured; they are priced solely through a row recorded here with the invoice, quote or owner channel it comes from. Nothing is estimated.</p></div>
      {canOperate && <button className="estate-btn" data-testid="armi-rate-open" onClick={() => setOpen(o => !o)}>{open ? 'Close' : 'Record a rate'}</button>}</header>
    {error && <p className="estate-alert" data-testid="armi-rate-error">{error}</p>}
    {!rows.length ? <p className="estate-note" data-testid="armi-rate-empty">No rate on record — GPU hours and CaaS deliveries stay unpriced until the owner supplies one.</p> : <div className="estate-table-wrap"><table className="estate-table" data-testid="armi-rate-table">
      <thead><tr><th>Lane</th><th>Applies to</th><th>Rate</th><th>Source</th><th>Recorded</th></tr></thead>
      <tbody>{rows.map((r, i) => { const [k, val] = rateOf(r) || []; const id = r.model_id || r.node_id || r.training_id || r.product_id; return <tr key={i} data-testid={`armi-rate-row-${r.lane}-${String(id).replace(/[^A-Za-z0-9]+/g, '-')}`}>
        <td data-label="Lane">{r.lane.replace('_', ' ')}</td><td data-label="Applies to" style={{ whiteSpace: 'normal' }}>{id === '*' ? 'every' : id}</td><td data-label="Rate">{val != null ? `${r.currency || 'USD'} ${val}` : '—'}<small>{k ? k.replace(/_/g, ' ') : ''}</small></td>
        <td data-label="Source" style={{ whiteSpace: 'normal' }}><small style={{ overflowWrap: 'anywhere' }}>{r.source}{/placeholder/i.test(r.source || '') ? ' · PLACEHOLDER, not applied' : ''}</small></td><td data-label="Recorded"><small>{stamp(r.authored_at)}</small></td></tr>; })}</tbody></table></div>}
    {open && canOperate && <form data-testid="armi-rate-form" onSubmit={submit} style={{ marginTop: 12 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))', gap: '0 16px' }}>
        <Row label="Lane"><select data-testid="armi-rate-lane" style={field} value={v.lane} onChange={e => setV(s => ({ ...s, lane: e.target.value, id: '*' }))}>{Object.entries(LANE).map(([k, l]) => <option key={k} value={k}>{l.label}</option>)}</select></Row>
        <Row label={`Applies to (${spec.idHint})`}><input data-testid="armi-rate-id" style={field} value={v.id} onChange={set('id')} required maxLength={120} /></Row>
        <Row label={spec.unit}><input data-testid="armi-rate-value" style={field} type="number" min="0.0001" step="0.0001" value={v.rate} onChange={set('rate')} required /></Row>
      </div>
      <Row label="Source — invoice, quote or owner channel (required)"><input data-testid="armi-rate-source" style={field} value={v.source} onChange={set('source')} required minLength={3} maxLength={400} placeholder="e.g. provider invoice INV-2026-10 · H200 on-demand" /></Row>
      <Row label="Notes"><input data-testid="armi-rate-notes" style={field} value={v.notes} onChange={set('notes')} maxLength={600} /></Row>
      <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="armi-rate-submit" disabled={busy || !v.source.trim() || !v.rate}>{busy ? 'Recording…' : 'Record rate'}</button><button type="button" className="estate-btn" data-testid="armi-rate-cancel" onClick={() => setOpen(false)}>Cancel</button></div>
    </form>}
  </section>;
}
