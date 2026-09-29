import React from 'react';
import { bytes, count, pctValue } from './useEstateReport';

const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`estate-tile-${id}`}>
  <span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;

export function EstateHeadline({ report }) {
  const h = report.headline;
  const cb = report.condition_bytes;
  const total = cb.total || 1;
  const bar = [['clean', 'No flagged condition', cb.clean, 'var(--sage)'], ['duplicate', 'Exact duplicates', cb.duplicate, 'var(--brass)'], ['degraded', 'Degraded', cb.degraded, 'var(--oxblood)'],
    ['incomplete', 'Rows with empty fields', cb.incomplete, '#c9a24a'], ['not_read', 'Not read / unmeasured', cb.not_read + cb.unmeasured, '#b8b0a0']];
  return <section className="estate-section" data-testid="estate-headline">
    <div className="estate-tiles">
      <Tile id="bytes" label="Data held" value={h.bytes_label} note={`data + index across ${h.connections} connections`} />
      <Tile id="databases" label="Databases" value={count(h.databases)} note={h.blocked_connections.length ? `${h.blocked_connections.join(', ')} blocked` : 'every reachable connection measured'} />
      <Tile id="tables" label="Tables" value={count(h.tables)} note={`${count(h.tables_measured)} measured · ${count(h.empty_tables)} empty · ${count(h.failed_tables)} failed`} />
      <Tile id="rows" label="Rows (estimate)" value={count(h.rows_estimate)} note={`${count(h.rows_measured)} rows actually measured`} />
      <Tile id="duplicates" label="Exact duplicate rows" value={pctValue(h.exact_duplicate_pct)} note={`normalised ${pctValue(h.normalised_duplicate_pct)} · ${count(h.duplicate_table_pairs)} same-schema table pairs`} tone="brass" />
      <Tile id="degraded" label="Degraded rows" value={pctValue(h.degraded_pct)} note="placeholder · mojibake · truncation · invalid format" tone="oxblood" />
      <Tile id="incomplete" label="Rows with empty fields" value={pctValue(h.null_bearing_pct)} note="at least one empty required-looking field" />
      <Tile id="pii" label="Rows with PII markers" value={pctValue(h.pii_pct)} note={`of ${count(h.pii_rows_checked)} sampled rows`} tone="oxblood" />
      <Tile id="stale" label="Stale bytes" value={pctValue(h.stale_pct_of_bytes)} note="in tables not written for over a year" />
      <Tile id="reclaimable" label="Reclaimable" value={h.reclaimable_label} note={`${pctValue(h.reclaimable_pct)} of the estate, before pricing`} tone="sage" />
    </div>
    <div className="estate-bar" data-testid="estate-condition-bar" aria-label="Byte-weighted condition of what was read">
      {bar.filter(([, , v]) => v > 0).map(([key, label, v, color]) => <span key={key} style={{ width: `${Math.max(0.5, (v / total) * 100)}%`, background: color }} title={`${label} · ${bytes(v)}`} />)}
    </div>
    <ul className="estate-legend">
      {bar.map(([key, label, v, color]) => <li key={key}><i style={{ background: color }} />{label} <b>{((v / total) * 100).toFixed(1)}%</b> <small>{bytes(v)}</small></li>)}
    </ul>
    <p className="estate-note">Byte-weighted; a row can carry more than one condition, so “no flagged condition” is the remainder. Grades across measured tables: {Object.entries(h.grades).map(([g, n]) => `${g} ${count(n)}`).join(' · ')}.</p>
  </section>;
}
