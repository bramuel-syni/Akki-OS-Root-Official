import React from 'react';
import { bytes, count, pct, pctValue } from './useEstateReport';

const Metric = ({ id, label, value, children }) => <div className="estate-decision-metric" data-testid={`estate-tile-${id}`}>
  <span>{label}</span><strong>{value}</strong><p>{children}</p>
</div>;

export function EstateHeadline({ report }) {
  const h = report.headline;
  const dup = report.summary.duplication;
  const obs = report.stores?.obs;
  const nas = report.stores?.nas;
  const objectDuplicates = obs?.measured && obs.duplicate_bytes_estimate != null;
  return <section className="estate-decision-summary" data-testid="estate-headline">
    <h2 data-testid="estate-takeaway">{objectDuplicates && obs.duplicate_bytes_estimate > 0 ? 'Start with duplicate objects. Verify before removing.' : 'Review duplicate candidates before making changes.'}</h2>
    <div className="estate-decision-metrics">
      <Metric id="object-duplicates" label="Object-store duplicate candidates" value={objectDuplicates ? bytes(obs.duplicate_bytes_estimate) : 'Not measured'}>
        {objectDuplicates ? <>{obs.bytes > 0 ? `${pct(obs.duplicate_bytes_estimate / obs.bytes)} of ${bytes(obs.bytes)} listed` : 'Storage share not measured'} · {count(obs.duplicate_candidates)} candidates. Matching metadata, not confirmed copies.</> : 'No verified duplicate measurement is available.'}
      </Metric>
      <Metric id="duplicates" label="Repeated database rows · estimate" value={bytes(dup.within_table_duplicate_bytes_estimate)}>
        {h.bytes_total > 0 && dup.within_table_duplicate_bytes_estimate != null ? `${pct(dup.within_table_duplicate_bytes_estimate / h.bytes_total, 2)} of ${bytes(h.bytes_total)} database storage. ` : ''}Within-table repeats; not a deletion allowance.
      </Metric>
      <Metric id="nas-duplicates" label="File-share duplication" value={nas?.measured && nas.duplicate_bytes_estimate != null ? bytes(nas.duplicate_bytes_estimate) : 'Not measured'}>
        {nas?.measured ? `${bytes(nas.bytes)} of files listed. ` : ''}{nas?.duplicate_candidates == null ? 'Content comparison is still needed.' : 'Candidate copies need verification.'}
      </Metric>
    </div>
    <p className="estate-scope-note" data-testid="estate-decision-scope">These are separate storage scopes, not a whole-estate duplicate percentage. {obs?.sources_blocked ? `${count(obs.sources_blocked)} object-store sources could not be read. ` : ''}{h.blocked_connections?.length ? `Database access blocked: ${h.blocked_connections.join(', ')}. ` : ''}{h.failed_tables ? `${count(h.failed_tables)} tables failed measurement.` : ''}</p>
    <div className="estate-inline-facts" data-testid="estate-secondary-findings">
      <span><b>{bytes(report.summary.storage?.redundant_index_bytes_estimate)}</b> estimated redundant indexes</span>
      <span><b>{pctValue(h.degraded_pct)}</b> estimated degraded database rows</span>
      <span><b>{count(h.tables_measured)} / {count(h.tables)}</b> tables measured</span>
    </div>
  </section>;
}