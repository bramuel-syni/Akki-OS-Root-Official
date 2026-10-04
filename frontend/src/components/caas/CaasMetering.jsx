import React, { useState } from 'react';
import { apiRequest, stamp } from '../models/useModelApproval';
import { productTitle } from './useCaas';

const text = v => (Array.isArray(v) ? v.map(text).join(' · ') : v && typeof v === 'object' ? Object.entries(v).map(([k, x]) => `${k}: ${text(x)}`).join('; ') : String(v ?? ''));

function DeliveryDetail({ id }) {
  const [doc, setDoc] = useState(null), [error, setError] = useState(null);
  React.useEffect(() => { let live = true; apiRequest(`/api/caas/deliveries/${id}`).then(r => { if (live) setDoc(r.delivery); }).catch(e => { if (live) setError(e.message); }); return () => { live = false; }; }, [id]);
  if (error) return <p className="estate-alert" data-testid={`caas-delivery-detail-error-${id}`}>{error}</p>;
  if (!doc) return <p className="estate-note">Reading the delivery…</p>;
  const r = doc.result || {}, body = r.deliverable || r, acc = r.acceptance || {};
  return <div data-testid={`caas-delivery-detail-${id}`} style={{ padding: '10px 12px', background: 'var(--surface)', borderRadius: 8, marginTop: 6 }}>
    <div className="estate-meta"><span>terms {doc.terms_identifier}</span><span>meter {doc.meter_id}</span>{doc.authored && <span>authored by {doc.authored.model} · {doc.authored.tokens_in}/{doc.authored.tokens_out} tokens · receipt {doc.authored.receipt_id}</span>}</div>
    {acc.findings?.length > 0 && <p className="estate-alert" style={{ marginTop: 8 }}>{acc.findings.join(' · ')}</p>}
    <dl style={{ margin: '8px 0 0', display: 'grid', gridTemplateColumns: 'minmax(120px,180px) 1fr', gap: '6px 12px', fontSize: 12.5 }}>
      {Object.entries(body || {}).filter(([k]) => !['acceptance', 'context_basis'].includes(k)).map(([k, v]) => <React.Fragment key={k}><dt style={{ color: 'var(--ink3)' }}>{k.replace(/_/g, ' ')}</dt><dd style={{ margin: 0, overflowWrap: 'anywhere' }}>{text(v).slice(0, 900)}</dd></React.Fragment>)}
    </dl>
  </div>;
}

export function CaasDeliveries({ deliveries, products, clients }) {
  const [open, setOpen] = useState(null);
  const name = id => clients?.find(c => c.client_id === id)?.name || id;
  return <section className="estate-section" data-testid="caas-deliveries" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Deliveries</h2><p>Every governed delivery handed to a client application, with its acceptance and the metered event written before it was returned. Raw estate rows never appear here or in the delivery.</p></div></header>
    {!deliveries?.length ? <p className="estate-note" data-testid="caas-deliveries-empty">No delivery yet. A client calls <code>POST /api/caas/client/deliver</code> with its key.</p> : <div className="estate-table-wrap"><table className="estate-table" data-testid="caas-deliveries-table">
      <thead><tr><th>Delivery</th><th>Client</th><th>Product</th><th>Accepted</th><th>When</th><th /></tr></thead>
      <tbody>{deliveries.map(d => <React.Fragment key={d.delivery_id}><tr data-testid={`caas-delivery-row-${d.delivery_id}`}>
        <td data-label="Delivery" style={{ whiteSpace: 'normal' }}><b>{d.delivery_id}</b><small>{d.licence_id} · {d.key_id}</small></td><td data-label="Client" style={{ whiteSpace: 'normal' }}>{name(d.client_id)}</td><td data-label="Product" style={{ whiteSpace: 'normal' }}>{productTitle(products, d.product)}</td>
        <td data-label="Accepted"><span className={`estate-status ${d.accepted ? 'complete' : 'blocked'}`} data-testid={`caas-delivery-accepted-${d.delivery_id}`}>{d.accepted ? 'accepted' : 'findings'}</span></td>
        <td data-label="When"><small>{stamp(d.at)}</small></td><td data-label="Detail"><button className="estate-btn" data-testid={`caas-delivery-open-${d.delivery_id}`} onClick={() => setOpen(open === d.delivery_id ? null : d.delivery_id)}>{open === d.delivery_id ? 'Close' : 'Open'}</button></td>
      </tr>{open === d.delivery_id && <tr><td colSpan={6} style={{ whiteSpace: 'normal' }}><DeliveryDetail id={d.delivery_id} /></td></tr>}</React.Fragment>)}</tbody>
    </table></div>}
  </section>;
}

export function CaasMetering({ metering, products, clients }) {
  const name = id => clients?.find(c => c.client_id === id)?.name || id;
  return <section className="estate-section" data-testid="caas-metering" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Metering</h2><p>{metering?.cost_note || 'Usage is metered per licence, product and period.'}</p></div>
      <div className="estate-meta"><span data-testid="caas-metering-events">{metering?.events ?? 0} metered events</span><span data-testid="caas-metering-cost">cost {metering?.cost_usd == null ? 'not priced' : `$${metering.cost_usd}`}</span></div></header>
    {!metering?.lines?.length ? <p className="estate-note" data-testid="caas-metering-empty">No usage metered yet.</p> : <div className="estate-table-wrap"><table className="estate-table" data-testid="caas-metering-table">
      <thead><tr><th>Client</th><th>Licence · terms</th><th>Product</th><th>Period</th><th>Quantity</th><th>Amount</th></tr></thead>
      <tbody>{metering.lines.map((l, i) => <tr key={i} data-testid={`caas-metering-line-${i}`}>
        <td data-label="Client" style={{ whiteSpace: 'normal' }}>{name(l.client_id)}</td><td data-label="Licence · terms" style={{ whiteSpace: 'normal' }}><small>{l.licence_id}</small><small style={{ fontFamily: 'var(--mono)', overflowWrap: 'anywhere' }}>{l.terms_identifier}</small></td><td data-label="Product" style={{ whiteSpace: 'normal' }}>{productTitle(products, l.product)}</td>
        <td data-label="Period">{l.period}</td><td data-label="Quantity">{l.quantity} <small>{l.unit}</small></td><td data-label="Amount">{l.amount_usd == null ? <small>no rate card</small> : `$${l.amount_usd}`}</td>
      </tr>)}</tbody>
    </table></div>}
  </section>;
}
