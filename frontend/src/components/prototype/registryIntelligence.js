import { registryBytes, registryCount } from './registryHistory';

const tile = (label, value, note) => ({ label, value, note });
const pct = ratio => ratio == null ? 'Not measured' : `${registryCount(Math.round(ratio * 1000) / 10)}%`;
const pctOf = (ratio, min = 0) => `${Math.max(min, Math.min(100, Math.round((ratio || 0) * 100)))}%`;
const colors = { clean: 'var(--sage)', duplicates: 'var(--brass)', degraded: 'var(--oxblood)', incomplete: 'var(--hair)', stale: 'var(--blue)' };
const stamp = iso => iso ? new Date(iso).toLocaleString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC' : 'not recorded';

export const intelligenceReading = ei => {
  if (ei?.latest) return ei.latest.reading;
  if (ei?.running) return `The estate intelligence census ${ei.running.job_id} is measuring the RMS estate now (${ei.running.databases_done} databases measured so far). Figures appear here once the worker's receipt is verified.`;
  return 'No estate intelligence census has completed. Duplication, quality, degradation and monetisation figures are not yet measured.';
};

export const intelligenceHeader = ei => ei?.latest ? `Data connected — estate intelligence ${ei.latest.job_id}` : 'Data connected — no verified estate intelligence yet';
export const intelligenceBasis = ei => ei?.latest
  ? `See what your estate holds, as measured ${stamp(ei.latest.measured_at)} by the census worker on akki-vm through the jump host. Ratios come from complete passes or stratified samples; row totals are estimates.`
  : 'Figures below stay unmeasured until an estate intelligence census completes and its receipt is digest-verified.';
export const opportunitiesLead = ei => ei?.latest?.data_products?.length
  ? `${ei.latest.data_products.length} things could be built from what was measured. Two are listed here; the rest open in the drawer.`
  : 'No build candidate is established yet: candidates are inferred from measured dimensions, not assumed.';

function drawerCards(latest) {
  const products = latest.data_products.map((p, i) => ({ q: `${i + 1}. ${p.title} — grade ${p.readiness_grade}`, hasArrow: false, hasControls: false,
    a: `${p.use} ${p.tables} supporting tables, ≈${registryCount(p.rows_estimate)} rows across ${p.databases.length} databases (${p.databases.slice(0, 3).join(', ')}${p.databases.length > 3 ? '…' : ''}). Blockers: ${p.blockers.join(' · ')}` }));
  const strategies = latest.cost_strategies.filter(s => s.bytes).map(s => ({ q: `Cost: ${s.title}`, hasArrow: false, hasControls: false,
    a: `${s.bytes_label}${s.share_of_estate != null ? ` (${pct(s.share_of_estate)} of the estate)` : ''}${s.monthly_saving != null ? ` · ≈${s.monthly_saving}/month` : ''}. ${s.action}` }));
  return [{ q: 'What the census found', a: latest.reading, hasArrow: false, hasControls: false }, ...products, ...strategies,
    { q: 'Method and limits', a: `${latest.coverage_note} ${latest.currency_note}`, hasArrow: false, hasControls: false }];
}

export function registryIntelligence({ data, show }) {
  const ei = data?.estate_intelligence;
  const latest = ei?.latest;
  const running = ei?.running;
  if (!latest) {
    const measured = 'Not measured';
    const note = running ? 'Estate intelligence census running' : 'No estate intelligence census completed';
    return {
      measureHeld: [tile('Data held', measured, note), tile('Databases', measured, note), tile('Tables', measured, note), tile('Rows (estimate)', measured, note)],
      measureRead: [tile('Read', measured, note), tile('Complete passes', measured, note), tile('Sampled', measured, note), tile('Not read', measured, note)],
      measureCare: [tile('Personal details', measured, note), tile('Restricted use', measured, 'Rights are declared at Connect, not measured'), tile('Read with problems', measured, note), tile('Possible duplicates', measured, note)],
      estateCensusCount: running ? `Census ${running.job_id} running · ${running.databases_done} databases measured` : 'No verified estate intelligence',
      estateConditionBar: [{ label: 'Condition not measured', w: '100%', color: 'var(--hair)', pct: '' }],
      estateConditionRows: ['Duplicates', 'Degraded', 'Incomplete records', 'Stale'].map(label => ({ label, value: measured, pct: 'no coverage claim', w: '0%', color: 'var(--hair)' })),
      estateConditionSources: running ? `Measuring now: ${running.progress?.connection || ''} ${running.progress?.database || ''}`.trim() : 'No measured quality or duplicate inventory is attached.',
      estateHeldRows: [], regQualBar: [], opportunitiesView: [{ key: 'unmeasured', title: 'Not established by this census', body: 'Build candidates are inferred from measured dimensions; none are measured yet.' }],
      openOppDrawerNew: () => show({ title: 'What your data can do', body: intelligenceReading(ei), code: running ? 'Running' : 'Not yet assessed' }),
      efGapsHook: 'Duplication, quality, degradation, PII density, freshness and storage economics await the estate intelligence receipt. Languages and rights are not measured by this census.',
      regQualReading: 'No condition classification is claimed until the estate intelligence receipt is verified.',
    };
  }
  const h = latest.headline;
  const c = latest.condition;
  const dup = c.exact_duplicate_ratio || 0, degraded = c.degraded_row_ratio || 0, incomplete = c.null_bearing_row_ratio || 0;
  const clean = Math.max(0, 1 - dup - degraded - incomplete);
  const staleShare = h.bytes_total ? latest.stale_bytes / h.bytes_total : 0;
  const totalBytes = latest.connections.reduce((n, x) => n + x.bytes, 0) || 1;
  const methods = latest.method_shares;
  const methodTotal = Object.values(methods).reduce((n, v) => n + v, 0) || 1;
  const topPii = latest.top_pii[0];
  const topDegraded = latest.top_degraded[0];
  return {
    measureHeld: [tile('Data held', h.bytes_label, `Data + index bytes across ${h.connections} connections`), tile('Databases', registryCount(h.databases), `${h.blocked_connections.length ? `${h.blocked_connections.join(', ')} blocked` : 'every reachable connection measured'}`),
      tile('Tables', registryCount(h.tables), `${registryCount(h.tables_measured)} measured · ${registryCount(h.empty_tables)} empty`), tile('Rows (estimate)', registryCount(h.rows_estimate), `TABLE_ROWS estimate · ${registryCount(h.rows_measured)} rows actually measured`)],
    measureRead: [tile('Read', `${registryCount(h.tables_measured)} tables`, 'Complete or stratified keyset passes; rows measured then discarded'), tile('Complete passes', registryCount(methods.complete_tables), 'Every row read for tables ≤100k rows'),
      tile('Sampled', registryCount(methods.sampled_tables + methods.head_sampled_tables), `${registryCount(methods.sampled_tables)} stratified · ${registryCount(methods.head_sampled_tables)} head samples`), tile('Not read', registryCount(methods.failed_tables), h.blocked_connections.length ? `Failed tables; ${h.blocked_connections.join(', ')} connection blocked` : 'Tables that refused or timed out')],
    measureCare: [tile('Personal details', pct(c.pii_row_ratio), topPii ? `of sampled rows carry PII markers · densest: ${topPii.database}.${topPii.table}` : 'of sampled rows carry PII markers'),
      tile('Restricted use', 'Not measured', 'Rights are declared at Connect; census does not establish them'),
      tile('Read with problems', pct(c.degraded_row_ratio), topDegraded ? `rows with placeholder, mojibake or truncation · worst: ${topDegraded.database}.${topDegraded.table}` : 'rows with placeholder, mojibake or truncation'),
      tile('Possible duplicates', `${registryCount(h.duplicate_table_pairs)} pairs`, `same-schema tables with content overlap · ${pct(c.exact_duplicate_ratio)} of rows repeat exactly · ${h.reclaimable_label} reclaimable`)],
    estateCensusCount: `Estate intelligence ${latest.job_id} · ${latest.status}`,
    estateConditionBar: [{ label: 'No flagged condition', w: pctOf(clean), color: colors.clean, pct: pct(clean) }, { label: 'Exact duplicates', w: pctOf(dup), color: colors.duplicates, pct: pct(dup) },
      { label: 'Degraded', w: pctOf(degraded), color: colors.degraded, pct: pct(degraded) }, { label: 'Rows with empty fields', w: pctOf(incomplete), color: colors.incomplete, pct: pct(incomplete) }],
    estateConditionRows: [{ label: 'Duplicates', value: pct(dup), pct: `${registryCount(h.duplicate_table_pairs)} table pairs`, w: pctOf(dup, 1), color: colors.duplicates },
      { label: 'Degraded', value: pct(degraded), pct: 'placeholder · mojibake · truncation', w: pctOf(degraded, 1), color: colors.degraded },
      { label: 'Incomplete records', value: pct(incomplete), pct: 'rows with ≥1 empty field', w: pctOf(incomplete, 1), color: colors.incomplete },
      { label: 'Stale', value: pct(staleShare), pct: 'bytes not written for > 1 year', w: pctOf(staleShare, 1), color: colors.stale }],
    estateConditionSources: `${registryCount(h.failed_tables)} tables failed${h.blocked_connections.length ? `; ${h.blocked_connections.join(', ')} refused the connection` : ''}. Measures overlap: one row may count under more than one condition. Ratios are weighted by estimated rows.`,
    estateHeldRows: latest.connections.map(x => ({ key: x.connection, label: x.connection, value: registryBytes(x.bytes), pct: pct(x.bytes / totalBytes), w: pctOf(x.bytes / totalBytes, 1), color: 'var(--blue)' })),
    regQualBar: [['complete_tables', 'Complete pass', 'var(--sage)'], ['sampled_tables', 'Stratified sample', 'var(--blue)'], ['head_sampled_tables', 'Head sample', 'var(--brass)'], ['failed_tables', 'Failed', 'var(--oxblood)']]
      .map(([key, label, fill]) => ({ label, size: `${registryCount(methods[key])} tables`, w: pctOf(methods[key] / methodTotal), fill })),
    opportunitiesView: latest.data_products.slice(0, 2).map(p => ({ key: p.key, title: `${p.title} — grade ${p.readiness_grade}`, body: `${p.tables} tables · ≈${registryCount(p.rows_estimate)} rows · ${p.databases.length} databases. ${p.use}` })),
    openOppDrawerNew: () => show({ title: 'What your data can do', subtitle: `Estate intelligence ${latest.job_id} · aggregates only, no row values`, code: latest.status, cards: drawerCards(latest),
      actions: [{ label: 'Open the full report', border: 'var(--blue)', bg: 'var(--blue)', color: '#fff', onClick: () => window.location.assign('/os/admin/estate/intelligence') },
        ...(latest.brief_path ? [{ label: 'Download the brief', border: 'var(--blue)', bg: 'transparent', color: 'var(--blue)', onClick: () => window.open(latest.brief_path, '_blank', 'noopener') }] : [])] }),
    efGapsHook: latest.coverage_note,
    regQualReading: `${registryCount(h.grades?.A || 0)} tables grade A, ${registryCount(h.grades?.E || 0)} grade E on completeness, duplication, damage, freshness and PII.`,
  };
}
