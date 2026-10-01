import React, { useState } from 'react';
import { bytes, count, pct, signed } from './useEstateReport';

const Grade = ({ grade, score }) => <span className={`estate-grade g-${(grade || 'u').toLowerCase()}`} title={score != null ? `score ${score}` : 'unmeasured'}>{grade}</span>;

export function EstateDatabases({ report }) {
  const [sort, setSort] = useState('rows');
  const degradation = Object.fromEntries(report.degradation.databases.map(d => [`${d.connection}/${d.database}`, d]));
  const rows = [...report.databases].sort((a, b) => sort === 'grade' ? (a.readiness.score ?? 101) - (b.readiness.score ?? 101) : sort === 'bytes' ? b.bytes - a.bytes : b.rows_estimate - a.rows_estimate);
  return <section className="estate-section" data-testid="estate-databases">
    <header className="estate-head">
      <div><h2>Database inventory</h2><p>Prioritise the lowest readiness grades for a data-owner review. Row counts are estimates.</p></div>
      <div className="estate-sort" role="group" aria-label="Sort databases">
        {[['rows', 'Rows'], ['bytes', 'Bytes'], ['grade', 'Worst grade first']].map(([key, label]) => <button key={key} className={`estate-chip${sort === key ? ' on' : ''}`} data-testid={`estate-db-sort-${key}`} onClick={() => setSort(key)}>{label}</button>)}
      </div>
    </header>
    <div className="estate-table-wrap">
      <table className="estate-table" data-testid="estate-database-table">
        <thead><tr><th>Connection / database</th><th>Tables</th><th>Rows est.</th><th>Bytes</th><th>Grade</th><th>Degraded</th><th>Dead cols</th><th>Stale</th><th>Last write</th><th>Rows Δ</th><th>Dimensions</th></tr></thead>
        <tbody>
          {rows.map(p => {
            const d = degradation[`${p.connection}/${p.database}`] || {};
            return <tr key={`${p.connection}/${p.database}`} data-testid={`estate-db-row-${p.connection}-${p.database}`}>
              <td data-label="Database"><b>{p.database}</b><small>{p.connection}{p.failed_tables ? ` · ${p.failed_tables} failed` : ''}</small></td>
              <td data-label="Tables">{count(p.tables)}<small>{count(p.measured_tables)} measured</small></td>
              <td data-label="Estimated rows">{count(p.rows_estimate)}</td>
              <td data-label="Storage">{bytes(p.bytes)}</td>
              <td data-label="Readiness"><Grade grade={p.readiness.grade === 'unmeasured' ? '—' : p.readiness.grade} score={p.readiness.score} /></td>
              <td data-label="Degraded">{d.degraded_ratio == null ? '—' : pct(d.degraded_ratio)}{d.worst_table ? <small>{d.worst_table.table}</small> : null}</td>
              <td data-label="Empty columns">{d.columns ? `${count(d.dead_columns)} / ${count(d.columns)}` : '—'}</td>
              <td data-label="Stale tables">{count(p.stale_tables)}<small>of {count(p.measured_tables)}</small></td>
              <td data-label="Last write">{d.days_since_last_write == null ? 'No timestamps' : `${count(d.days_since_last_write)} days ago`}{d.write_span_days != null ? <small>{count(d.write_span_days)} days of writes</small> : null}</td>
              <td data-label="Rows changed">{signed(d.growth?.rows_delta)}{d.schema_drift_tables?.length ? <small>{d.schema_drift_tables.length} changed schemas</small> : null}</td>
              <td data-label="Dimensions" className="estate-dims">{Object.entries(p.dimensions).slice(0, 6).map(([k, v]) => <span key={k}>{k} <b>{v}</b></span>)}</td>
            </tr>;
          })}
        </tbody>
      </table>
    </div>
  </section>;
}
