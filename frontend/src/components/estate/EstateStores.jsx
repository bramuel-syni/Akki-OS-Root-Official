import React from 'react';
import { bytes, count, pctValue, stamp } from './useEstateReport';

const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`estate-store-tile-${id}`}>
  <span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;

function Store({ id, title, st }) {
  if (!st?.measured) return <div data-testid={`estate-store-${id}`}><h3>{title}</h3><p className="estate-note">{st?.note || 'Not measured.'}</p></div>;
  const fingerprinted = st.duplicate_candidates != null;
  return <div data-testid={`estate-store-${id}`}>
    <h3>{title} <small>census <code>{st.census_run_id}</code> · {st.status} · {stamp(st.observed_at)}</small></h3>
    <div className="estate-tiles">
      <Tile id={`${id}-bytes`} label="Bytes held" value={st.bytes_label} note={`${count(st.units)} ${st.unit_name} in ${count(st.sources_complete)} of ${count(st.sources)} sources`} />
      <Tile id={`${id}-duplicates`} label="Duplicate candidates" value={fingerprinted ? count(st.duplicate_candidates) : 'Unmeasured'} note={fingerprinted ? `${pctValue(st.duplicate_pct_of_units)} of ${st.unit_name} · ≈${bytes(st.duplicate_bytes_estimate)} (estimate)` : 'no fingerprints in this pass'} tone={fingerprinted ? 'brass' : undefined} />
      <Tile id={`${id}-cold`} label="Not written for a year" value={bytes(st.cold_bytes)} note={`${count(st.cold_sources)} sources by last object write`} />
      <Tile id={`${id}-frontier`} label="Enumeration frontier" value={st.frontier_complete ? 'Complete' : 'Open'} note={st.sources_blocked ? `${count(st.sources_blocked)} sources blocked` : 'every reachable source fully listed'} tone={st.frontier_complete ? 'sage' : undefined} />
    </div>
    <div className="estate-table-wrap"><table className="estate-table" data-testid={`estate-store-table-${id}`}>
      <thead><tr><th>Source</th><th>Status</th><th>{st.unit_name}</th><th>Bytes</th><th>Duplicates</th><th>Last write</th><th>Formats</th></tr></thead>
      <tbody>{st.top_sources.map(r => <tr key={r.label}>
        <td><b>{r.label}</b></td>
        <td>{r.status}{r.reason_code ? <small>{r.reason_code}</small> : null}</td>
        <td>{count(r.units)}</td><td>{bytes(r.bytes)}</td>
        <td>{r.duplicate_candidates == null ? '—' : <>{count(r.duplicate_candidates)}<small>≈{bytes(r.duplicate_bytes_estimate)}</small></>}</td>
        <td>{r.last_write ? <>{stamp(r.last_write)}{r.cold ? <small>cold · {count(r.idle_days)} days idle</small> : null}</> : '—'}</td>
        <td><small>{r.top_formats.join(' · ') || '—'}</small></td>
      </tr>)}</tbody>
    </table></div>
    {st.blocked?.length ? <p className="estate-note" data-testid={`estate-store-blocked-${id}`}>Blocked: {st.blocked.slice(0, 10).map(b => `${b.label} (${b.reason_code})`).join('; ')}{st.blocked.length > 10 ? ` … ${st.blocked.length - 10} more` : ''}</p> : null}
    <p className="estate-note">{st.duplication_note}</p>
  </div>;
}

export function EstateStores({ report }) {
  const stores = report.stores || {};
  return <section className="estate-section" data-testid="estate-stores">
    <header className="estate-head"><div><h2>Object and file estate</h2>
      <p>OBS buckets and NAS shares from their retained enumeration receipts: listing and stat only — sizes, dates and ETag+size fingerprints; no object or file body was read.</p></div></header>
    <Store id="obs" title="OBS object store" st={stores.obs} />
    <div style={{ marginTop: 32 }}><Store id="nas" title="NAS file shares" st={stores.nas} /></div>
  </section>;
}
