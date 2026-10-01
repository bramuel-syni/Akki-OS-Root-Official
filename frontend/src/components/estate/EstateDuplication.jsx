import React from 'react';
import { bytes, count, pct } from './useEstateReport';

export function EstateDuplication({ report }) {
  const dup = report.summary.duplication;
  const within = report.within_table_duplicates || [];
  return <section className="estate-section" data-testid="estate-duplication">
    <header className="estate-head"><div><h2>Duplication</h2>
      <p>{count(dup.cross_table_pairs)} same-schema table pairs share content ({bytes(dup.cross_table_duplicate_bytes_estimate)} in the smaller copies, {count(dup.same_schema_groups)} schema groups); {bytes(dup.within_table_duplicate_bytes_estimate)} of rows repeat exactly inside tables. Overlap is a bottom-256 sketch Jaccard estimate; row-level diffs were never taken.</p></div></header>
    <div className="estate-columns">
      <div>
        <h3>Same-schema pairs with content overlap</h3>
        <div className="estate-table-wrap"><table className="estate-table" data-testid="estate-duplicate-pairs">
          <thead><tr><th>Copy A</th><th>Copy B</th><th>Overlap</th><th>Smaller copy</th></tr></thead>
          <tbody>{dup.top_pairs.slice(0, 15).map((p, i) => <tr key={i}><td data-label="Copy A">{p.a}</td><td data-label="Copy B">{p.b}</td><td data-label="Overlap">{pct(p.content_overlap_estimate, 0)}</td><td data-label="Smaller copy">{bytes(p.bytes_smaller)}<small>{count(p.rows_smaller)} rows</small></td></tr>)}</tbody>
        </table></div>
      </div>
      <div>
        <h3>Exact repeats inside a table</h3>
        <div className="estate-table-wrap"><table className="estate-table" data-testid="estate-within-duplicates">
          <thead><tr><th>Table</th><th>Exact</th><th>Normalised</th><th>Rows est.</th><th>Data</th></tr></thead>
          <tbody>{within.slice(0, 15).map((t, i) => <tr key={i}><td data-label="Table"><b>{t.table}</b><small>{t.database} · {t.method.replace(/_/g, ' ')}</small></td><td data-label="Exact repeats">{pct(t.exact_duplicate_ratio)}</td><td data-label="Normalised repeats">{t.normalised_duplicate_ratio == null ? '—' : pct(t.normalised_duplicate_ratio)}</td><td data-label="Estimated rows">{count(t.rows_estimate)}</td><td data-label="Data">{bytes(t.data_bytes)}</td></tr>)}</tbody>
        </table></div>
        {!within.length && <p className="estate-note">No measured table repeats more than 1% of its rows exactly.</p>}
      </div>
    </div>
  </section>;
}
