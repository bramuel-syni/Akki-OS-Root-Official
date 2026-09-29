import React, { useState } from 'react';
import { count, pct } from './useEstateReport';

function Product({ p, rank }) {
  const [open, setOpen] = useState(rank === 1);
  return <article className={`estate-product g-${p.readiness_grade.toLowerCase()}`} data-testid={`estate-product-${p.key}`}>
    <button className="estate-product-head" onClick={() => setOpen(o => !o)} aria-expanded={open} data-testid={`estate-product-toggle-${p.key}`}>
      <span className="estate-rank">{rank}</span>
      <span className="estate-product-title"><b>{p.title}</b><small>{count(p.tables)} tables · ≈{count(p.rows_estimate)} rows · {p.databases.length} databases · readiness {p.readiness_grade} ({p.readiness_score})</small></span>
      <span className={`estate-grade g-${p.readiness_grade.toLowerCase()}`}>{p.readiness_grade}</span>
    </button>
    {open && <div className="estate-product-body">
      <p>{p.use}</p>
      <dl>
        <dt>Dimensions</dt><dd>required {p.required_dimensions.join(', ')} · supporting {p.supporting_dimensions.join(', ')}</dd>
        <dt>Licensable grain</dt><dd data-testid={`estate-product-grain-${p.key}`}>{p.licensable_units?.length ? <ul>{p.licensable_units.map((u, i) => <li key={i}>{u}</li>)}</ul> : 'not measurable from column statistics'}<small>Inferred from column names and measured distinct ratios; a grain is a candidate unit of licence, not a rights finding.</small></dd>
        <dt>Top tables</dt><dd><ul className="estate-inline">{p.top_tables.slice(0, 6).map(t => <li key={t.table}><b>{t.table}</b> {count(t.rows_estimate)} rows · {t.grade}{t.pii_ratio > 0.05 ? ` · PII ${pct(t.pii_ratio, 0)}` : ''}{t.staleness_days > 365 ? ` · stale ${count(t.staleness_days)} d` : ''}</li>)}</ul></dd>
        <dt>Blockers</dt><dd><ul className="estate-blockers">{p.blockers.map((b, i) => <li key={i}>{b}</li>)}</ul></dd>
      </dl>
      <p className="estate-note">{pct(p.pii_table_share, 0)} of supporting tables carry PII markers · {pct(p.stale_table_share, 0)} not written for over a year · score {p.score}.</p>
    </div>}
  </article>;
}

export function EstateProducts({ report }) {
  return <section className="estate-section" data-testid="estate-products">
    <header className="estate-head"><div><h2>What the data can do — dimensional monetisation</h2><p>Candidates are inferred from the dimensions measured on each table (time, geo, entity, money, content, channel, engagement, product, identity) and ranked by rows × readiness × supporting dimensions. Every candidate is an aggregate or de-identified product; use rights are declared at Connect and never established by a census.</p></div></header>
    <div className="estate-products">{report.data_products.map((p, i) => <Product key={p.key} p={p} rank={i + 1} />)}</div>
    {!report.data_products.length && <p className="estate-note">No build candidate is established: none of the measured tables carries a complete dimension set.</p>}
  </section>;
}
