import React from 'react';
import { bytes, count, pct, signed, stamp } from './useEstateReport';

const Row = ({ t, value, note }) => <li><span><b>{t.table}</b><small>{t.database} · {count(t.rows_estimate)} rows · {String(t.method || '').replace(/_/g, ' ')}</small></span><em>{value}</em>{note ? <small>{note}</small> : null}</li>;

export function EstateQuality({ report }) {
  const q = report.summary.quality;
  const d = report.degradation;
  const trend = d.trend;
  const kinds = Object.entries(d.kinds).sort((a, b) => b[1] - a[1]);
  const deltaLabels = { bytes_total: ['Bytes held', bytes], rows_estimate: ['Rows (est.)', count], tables: ['Tables', count], tables_measured: ['Tables measured', count], exact_duplicate_pct: ['Exact duplicates (pts)', v => v.toFixed(1)],
    degraded_pct: ['Degraded (pts)', v => v.toFixed(1)], null_bearing_pct: ['Empty fields (pts)', v => v.toFixed(1)], pii_pct: ['PII (pts)', v => v.toFixed(1)], stale_pct_of_bytes: ['Stale bytes (pts)', v => v.toFixed(1)],
    reclaimable_bytes: ['Reclaimable', bytes], empty_tables: ['Empty tables', count], failed_tables: ['Failed tables', count], duplicate_table_pairs: ['Duplicate pairs', count] };
  return <section className="estate-section" data-testid="estate-quality">
    <header className="estate-head"><div><h2>Quality, degradation and trend</h2><p>Damage kinds are measured per column and weighted by rows; never-populated columns are schema carried without data; the trend compares this census with the previous verified one.</p></div></header>
    <div className="estate-columns three">
      <div data-testid="estate-degradation-kinds">
        <h3>Damage kinds</h3>
        <ul className="estate-bars">{kinds.map(([k, v]) => <li key={k}><span>{k.replace('_', ' ')}</span><i style={{ width: `${Math.max(1, Math.min(100, v * 100))}%` }} /><b>{pct(v)}</b></li>)}</ul>
        <p className="estate-note">{d.kinds_note}</p>
        <div className="estate-fact" data-testid="estate-dead-columns"><b>{count(d.dead_columns)} of {count(d.columns_measured)}</b><span>columns never populated ({pct(d.dead_column_share)}). {d.dead_columns_note}</span></div>
      </div>
      <div data-testid="estate-trend">
        <h3>Trend against the previous census</h3>
        {trend ? <>
          <p className="estate-note" data-testid="estate-trend-date">Previous census: {stamp(trend.previous_measured_at)}.{trend.coverage_changed ? ' Coverage changed; differences include newly reached tables, not only data changes.' : ''}</p>
          <ul className="estate-deltas">{Object.entries(trend.deltas).filter(([, v]) => v != null).map(([k, v]) => <li key={k}><span>{deltaLabels[k]?.[0] || k}</span><b className={v > 0 ? 'up' : v < 0 ? 'down' : ''}>{signed(v, deltaLabels[k]?.[1] || count)}</b></li>)}</ul>
          <p className="estate-note">{count(trend.schema_drift_tables)} tables changed schema · {count(trend.databases_grown)} databases grew · {count(trend.databases_shrunk)} shrank.</p>
        </> : <p className="estate-note">{d.trend_note}</p>}
      </div>
      <div data-testid="estate-orphans">
        <h3>Orphaned references</h3>
        <ul className="estate-list">{q.orphaned_references.slice(0, 10).map((o, i) => <li key={i}><span><b>{o.table}.{o.column}</b><small>→ {o.target}</small></span><em>{pct(o.orphan_ratio, 0)}</em><small>of {count(o.sampled)} sampled</small></li>)}</ul>
        <p className="estate-note">Targets are inferred from column names (x_id → x / xs); a missing target may be a naming convention rather than a broken key.</p>
      </div>
    </div>
    <div className="estate-columns">
      <div data-testid="estate-top-degraded"><h3>Most degraded tables</h3><ul className="estate-list">{q.top_degraded.slice(0, 10).map((t, i) => <Row key={i} t={t} value={pct(t.degraded_row_ratio)} note={t.staleness_days != null ? `${count(t.staleness_days)} d since last write` : null} />)}</ul></div>
      <div data-testid="estate-top-pii"><h3>PII-dense tables</h3><ul className="estate-list">{q.top_pii.slice(0, 10).map((t, i) => <Row key={i} t={t} value={pct(t.pii_row_ratio)} note={bytes(t.data_bytes)} />)}</ul>
        <p className="estate-note">Markers found: {Object.entries(q.pii_kinds).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k.split('.').pop()} ${count(v)}`).join(' · ')}. Deterministic and sampled — absence of a marker is not absence of personal data.</p></div>
    </div>
  </section>;
}
