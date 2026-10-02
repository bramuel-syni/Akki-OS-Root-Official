import React from 'react';
import { bytes, count, stamp } from './useEstateReport';

const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`estate-content-tile-${id}`}>
  <span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;

const hours = value => value == null ? '—' : `${count(Math.round(value * 10) / 10)} h`;
const langs = map => Object.entries(map || {}).slice(0, 5).map(([code, h]) => `${code} ${hours(h)}`).join(' · ') || '—';
const ACCESS = { readable: 'Readable', denied: 'Key refused GetObject', archived: 'Archived · restore needed', no_media: 'No media' };

function Live({ runs }) {
  if (!runs?.length) return null;
  return <p className="estate-note" data-testid="estate-content-live">Runs in flight: {runs.map(r => `${r.worker_id} · ${r.stage}${r.reason_code ? ` (${r.reason_code.toLowerCase().replace(/_/g, ' ')})` : ''}${r.not_before ? ` · re-enters ${stamp(new Date(r.not_before * 1000).toISOString())}` : ''}`).join('; ')}.</p>;
}

function Store({ id, title, c }) {
  if (!c?.measured && !c?.live_runs?.length) return <div data-testid={`estate-content-${id}`}><h3>{title}</h3><p className="estate-note">{c?.note || 'No full-content pass has been commissioned for this store.'}</p></div>;
  const readPct = c.media_bytes ? Math.round(100 * c.bytes_read / c.media_bytes) : 0;
  return <div data-testid={`estate-content-${id}`}>
    <h3 data-testid={`estate-content-heading-${id}`}>{title} <small>{count(c.sources_complete)} of {count(c.sources)} stores finished · {c.eta_hours != null ? `≈${count(c.eta_hours)} h to go at ${count(c.throughput_mb_per_s)} MB/s` : c.objects_pending ? 'estimate pending the next run' : 'nothing pending'}</small></h3>
    <div className="estate-tiles">
      <Tile id={`${id}-read`} label="Bytes read in full" value={bytes(c.bytes_read)} note={`${readPct}% of ${bytes(c.media_bytes)} media listed · ${count(c.objects_read)} of ${count(c.media_objects)} files · ${bytes(c.bytes_verified)} verified by sha256/size/ETag`} tone="sage" />
      <Tile id={`${id}-speech`} label="Speech hours (detected)" value={hours(c.hours_speech)} note={`${hours(c.hours_decoded)} decoded · ${hours(c.hours_music)} music · ${hours(c.hours_silence)} silence`} tone="brass" />
      <Tile id={`${id}-languages`} label="Speech by language" value={langs(c.hours_by_language).split(' · ')[0] || '—'} note={langs(c.hours_by_language)} />
      <Tile id={`${id}-denied`} label="Listed but not readable" value={bytes((c.bytes_denied || 0) + (c.bytes_archived || 0))} note={`${count(c.objects_denied)} files refused by the key · ${count(c.objects_archived)} in archive storage · ${count(c.objects_failed)} read failures`} tone={c.bytes_denied ? 'oxblood' : undefined} />
    </div>
    <Live runs={c.live_runs} />
    <div className="estate-table-wrap"><table className="estate-table" data-testid={`estate-content-table-${id}`}>
      <thead><tr><th>Store</th><th>Access</th><th>Read</th><th>Hours</th><th>Languages</th><th>Quality</th></tr></thead>
      <tbody>{(c.source_rows || []).map(r => <tr key={r.label} data-testid={`estate-content-row-${r.label}`}>
        <td data-label="Store"><b>{r.label}</b><small>{count(r.media_objects)} media files · {bytes(r.media_bytes)}{r.inventory_complete ? '' : ' · listing continues'}</small></td>
        <td data-label="Access">{ACCESS[r.access] || r.access}<small>{r.measurement === 'full' ? 'every file read' : r.measurement === 'partial' ? `${count(r.objects_pending)} files to go` : r.measurement}</small></td>
        <td data-label="Read">{bytes(r.bytes_read)}<small>{count(r.objects_read)} files · {r.objects_failed ? `${count(r.objects_failed)} failed` : 'no failures'}</small></td>
        <td data-label="Hours">{hours(r.hours_speech)} speech<small>{hours(r.hours_decoded)} decoded · {hours(r.hours_music)} music</small></td>
        <td data-label="Languages"><small>{langs(r.hours_by_language)}</small></td>
        <td data-label="Quality"><small>{r.quality?.sample_rates ? Object.entries(r.quality.sample_rates).slice(0, 2).map(([k, v]) => `${k} Hz ×${count(v)}`).join(', ') : '—'}{r.quality?.level_dbfs_mean != null ? ` · ${r.quality.level_dbfs_mean} dBFS` : ''}{r.mean_confidence != null ? ` · confidence ${r.mean_confidence}` : ''}</small></td>
      </tr>)}</tbody>
    </table></div>
    <p className="estate-note">Bytes are facts: every object is read to its last byte and checked against the listing. Hours are model detections on every two-second window (admitted music detector, current audio language model), not human labels; what counts as clean, eligible speech is decided in the report, not by the reader. Files the key cannot read are counted, never estimated.</p>
  </div>;
}

export function EstateContentCensus({ report }) {
  const stores = report.stores || {};
  return <section className="estate-section" data-testid="estate-content-census">
    <header className="estate-head"><div><h2>Full-content audio census</h2>
      <p>Owner order: read everything. Both GPU hosts read every media object in the object store and on the NAS shares byte for byte, decode it in full and judge every two-second window. Successive bounded runs resume until nothing readable is left; progress below is the live, verified state.</p></div></header>
    <Store id="obs" title="OBS object store" c={stores.obs?.content} />
    <div style={{ marginTop: 32 }}><Store id="nas" title="NAS file shares" c={stores.nas?.content} /></div>
  </section>;
}
