import React, { useState } from 'react';
import { bytes, pct } from './useEstateReport';

function Strategy({ s }) {
  const [open, setOpen] = useState(false);
  return <li className="estate-strategy" data-testid={`estate-strategy-${s.key}`}>
    <div className="estate-strategy-row">
      <span className="estate-strategy-title"><b>{s.title}</b><small>{s.action}</small></span>
      <span className="estate-strategy-bytes"><b>{s.bytes ? bytes(s.bytes) : '—'}</b><small>{s.bytes && s.share_of_estate != null ? `${pct(s.share_of_estate)} of the estate` : s.bytes_label}{s.monthly_saving != null ? ` · ≈${s.monthly_saving}/month` : ''}</small></span>
      <button className="estate-chip" onClick={() => setOpen(o => !o)} aria-expanded={open} data-testid={`estate-strategy-toggle-${s.key}`}>{open ? 'Hide evidence' : 'Evidence'}</button>
    </div>
    {open && <div className="estate-strategy-body">
      {s.evidence?.length ? <ul>{s.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul> : <p className="estate-note">No table met this strategy's threshold in this census.</p>}
      <p className="estate-risk"><b>Risk</b> {s.risk}</p>
    </div>}
  </li>;
}

export function EstateStrategies({ report }) {
  const c = report.cost_strategies;
  const total = c.items.reduce((n, s) => n + (s.bytes || 0), 0);
  return <section className="estate-section" data-testid="estate-strategies">
    <header className="estate-head"><div><h2>Strategies to reduce cost</h2><p>{bytes(total)} across all strategies (overlaps possible). {c.currency_note}</p></div></header>
    <ul className="estate-strategies">{c.items.map(s => <Strategy key={s.key} s={s} />)}</ul>
  </section>;
}
