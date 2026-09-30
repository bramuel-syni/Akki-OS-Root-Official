import React, { useState } from 'react';
import { bytes, pct } from './useEstateReport';

const money = (value, currency) => value == null ? null : `${currency || ''} ${value.toLocaleString('en-GB', { maximumFractionDigits: 2 })}`.trim();

function Strategy({ s }) {
  const [open, setOpen] = useState(false);
  return <li className="estate-strategy" data-testid={`estate-strategy-${s.key}`}>
    <div className="estate-strategy-row">
      <span className="estate-strategy-title"><b>{s.title}</b><small>{s.action}</small></span>
      <span className="estate-strategy-bytes"><b>{s.bytes ? bytes(s.bytes) : '—'}</b><small>{s.bytes && s.share_of_estate != null ? `${pct(s.share_of_estate)} of the database estate` : s.store === 'object' && s.bytes ? 'object store' : s.bytes_label}{s.monthly_saving != null ? <span data-testid={`estate-strategy-saving-${s.key}`} title={s.saving_basis || undefined}> · ≈{s.saving_basis?.startsWith('upper bound') ? 'up to ' : ''}{money(s.monthly_saving, s.currency)}/month</span> : ''}</small></span>
      <button className="estate-chip" onClick={() => setOpen(o => !o)} aria-expanded={open} data-testid={`estate-strategy-toggle-${s.key}`}>{open ? 'Hide evidence' : 'Evidence'}</button>
    </div>
    {open && <div className="estate-strategy-body">
      {s.evidence?.length ? <ul>{s.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul> : <p className="estate-note">No table met this strategy's threshold in this census.</p>}
      <p className="estate-risk"><b>Risk</b> {s.risk}{s.saving_basis ? <> <b>Pricing</b> {s.saving_basis}.</> : null}</p>
    </div>}
  </li>;
}

export function EstateStrategies({ report }) {
  const c = report.cost_strategies;
  const total = c.items.reduce((n, s) => n + (s.bytes || 0), 0);
  return <section className="estate-section" data-testid="estate-strategies">
    <header className="estate-head"><div><h2>Strategies to reduce cost</h2>
      <p>{bytes(total)} across all strategies (overlaps possible){c.monthly_saving_total != null ? <> · <b data-testid="estate-strategies-total-saving">≈{money(c.monthly_saving_total, c.currency)}/month</b> if every priced strategy lands</> : null}. <span data-testid="estate-strategies-tariff-note">{c.currency_note}</span></p></div></header>
    <ul className="estate-strategies">{c.items.map(s => <Strategy key={s.key} s={s} />)}</ul>
  </section>;
}
