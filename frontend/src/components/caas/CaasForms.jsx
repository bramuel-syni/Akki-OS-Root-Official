import React, { useState } from 'react';

const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };
const Row = ({ label, children }) => <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">{label}</span>{children}</label>;
const Actions = ({ id, busy, label, onCancel, disabled, danger }) => <div className="estate-actions"><button type="submit" className={`estate-btn${danger ? '' : ' primary'}`} data-testid={`caas-${id}-submit`} disabled={Boolean(busy) || disabled}>{busy ? 'Recording…' : label}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid={`caas-${id}-cancel`}>Cancel</button></div>;

export function AdmitForm({ busy, onSubmit, onCancel }) {
  const [v, setV] = useState({ name: '', application: '', contact: '', note: '' });
  const set = k => e => setV(s => ({ ...s, [k]: e.target.value }));
  return <form data-testid="caas-admit-form" className="estate-section" style={{ marginTop: 16 }} onSubmit={e => { e.preventDefault(); onSubmit({ name: v.name, application: v.application, contact: v.contact || null, note: v.note || null }); }}>
    <h2 style={{ font: '400 20px var(--head)', margin: '0 0 12px' }}>Admit a client application</h2>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))', gap: '0 16px' }}>
      <Row label="Client (organisation)"><input data-testid="caas-admit-name" style={field} value={v.name} onChange={set('name')} required maxLength={160} /></Row>
      <Row label="Contact (optional)"><input data-testid="caas-admit-contact" style={field} value={v.contact} onChange={set('contact')} maxLength={200} /></Row>
    </div>
    <Row label="Application and what it does with the context"><textarea data-testid="caas-admit-application" style={{ ...field, minHeight: 56 }} value={v.application} onChange={set('application')} required maxLength={400} /></Row>
    <Row label="Note for the record (optional)"><input data-testid="caas-admit-note" style={field} value={v.note} onChange={set('note')} maxLength={600} /></Row>
    <p className="estate-note">Admission creates the client identity only. Access begins with a licence under a stated purpose, and a key issued under that licence.</p>
    <Actions id="admit" busy={busy} label="Admit client" onCancel={onCancel} disabled={!v.name.trim() || !v.application.trim()} />
  </form>;
}

export function GrantForm({ products, licences, busy, onSubmit, onCancel }) {
  const [purpose, setPurpose] = useState(''), [chosen, setChosen] = useState([]), [allowance, setAllowance] = useState('100'), [period, setPeriod] = useState('month'), [supersedes, setSupersedes] = useState('');
  const toggle = id => setChosen(v => (v.includes(id) ? v.filter(x => x !== id) : [...v, id]));
  const active = (licences || []).filter(l => l.status === 'active');
  return <form data-testid="caas-grant-form" style={{ marginTop: 12 }} onSubmit={e => { e.preventDefault(); onSubmit({ purpose, products: chosen, deliveries_per_period: Number(allowance), period, supersedes: supersedes || null }); }}>
    <Row label="Purpose the licence is granted for"><textarea data-testid="caas-grant-purpose" style={{ ...field, minHeight: 56 }} value={purpose} onChange={e => setPurpose(e.target.value)} required maxLength={600} placeholder="e.g. radio media planning for the client's FMCG brands in Kikuyu, Kamba and Kiswahili" /></Row>
    <span className="estate-label">Context products covered</span>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }} data-testid="caas-grant-products">{Object.entries(products || {}).map(([id, p]) => <button type="button" key={id} className={`estate-chip${chosen.includes(id) ? ' on' : ''}`} data-testid={`caas-grant-product-${id.replace(/[^A-Za-z0-9]+/g, '-')}`} onClick={() => toggle(id)} title={p.deliverable}>{p.title}</button>)}</div>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(180px,1fr))', gap: '0 16px' }}>
      <Row label="Deliveries allowed per period"><input data-testid="caas-grant-allowance" style={field} type="number" min="1" max="100000" value={allowance} onChange={e => setAllowance(e.target.value)} required /></Row>
      <Row label="Period"><select data-testid="caas-grant-period" style={field} value={period} onChange={e => setPeriod(e.target.value)}><option value="month">per month</option><option value="day">per day</option></select></Row>
      {active.length > 0 && <Row label="Supersedes (retires that licence)"><select data-testid="caas-grant-supersedes" style={field} value={supersedes} onChange={e => setSupersedes(e.target.value)}><option value="">— new licence —</option>{active.map(l => <option key={l.licence_id} value={l.licence_id}>{l.licence_id} · {l.terms.purpose.slice(0, 40)}</option>)}</select></Row>}
    </div>
    <p className="estate-note">Terms are frozen at grant. A change of purpose or scope is a new licence; receipts already issued keep their terms identifier.</p>
    <Actions id="grant" busy={busy} label="Grant licence" onCancel={onCancel} disabled={!purpose.trim() || !chosen.length} />
  </form>;
}

export function ReasonForm({ id, title, label, busy, onSubmit, onCancel }) {
  const [reason, setReason] = useState('');
  return <form data-testid={`caas-${id}-form`} style={{ marginTop: 12 }} onSubmit={e => { e.preventDefault(); onSubmit(reason); }}>
    <Row label={title}><input data-testid={`caas-${id}-reason`} style={field} value={reason} onChange={e => setReason(e.target.value)} required maxLength={600} /></Row>
    <Actions id={id} busy={busy} label={label} onCancel={onCancel} disabled={!reason.trim()} danger />
  </form>;
}

export function TransitionForm({ action, busy, onSubmit, onCancel }) {
  const [note, setNote] = useState('');
  const label = { suspend: 'Suspend client', reinstate: 'Reinstate client', revoke: 'Revoke client' }[action];
  return <form data-testid={`caas-${action}-form`} style={{ marginTop: 12 }} onSubmit={e => { e.preventDefault(); onSubmit({ action, note: note || null }); }}>
    <Row label="Note for the record"><input data-testid={`caas-${action}-note`} style={field} value={note} onChange={e => setNote(e.target.value)} maxLength={600} placeholder={action === 'revoke' ? 'Why this client leaves service (irreversible; every active licence and key is withdrawn)' : 'Optional'} /></Row>
    <Actions id={action} busy={busy} label={label} onCancel={onCancel} danger={action !== 'reinstate'} />
  </form>;
}
