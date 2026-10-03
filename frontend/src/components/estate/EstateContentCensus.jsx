import React from 'react';
import { bytes, count, stamp } from './useEstateReport';
import { EstateContentFolders } from './EstateContentFolders';
import { EstateContentAccess } from './EstateContentAccess';
import { hours, interval, langs, usd } from './contentFormat';

const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`estate-content-tile-${id}`}>
  <span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;

const ACCESS = { readable: 'Readable', denied: 'Key refused GetObject', archived: 'Archived · restore needed', no_media: 'No media' };
const MEASUREMENT = { estimated: 'sample complete', census: 'every file read', partial: 'sampling', listing: 'listing', denied: 'denied', archived: 'archived', no_media: 'no media' };

const n = v => v == null ? '—' : count(v);

function Live({ runs, window }) {
  if (!runs?.length && !window) return null;
  return <p className="estate-note" data-testid="estate-content-live">
    {runs?.length ? `Runs in flight: ${runs.map(r => `${r.worker_id} · ${r.stage}${r.reason_code ? ` (${r.reason_code.toLowerCase().replace(/_/g, ' ')})` : ''}${r.not_before ? ` · re-enters ${stamp(new Date(r.not_before * 1000).toISOString())}` : ''}`).join('; ')}. ` : ''}
    {window ? `NAS files are read only in the off-peak window ${window.utc} UTC (20:00–06:00 EAT); listing and header probes run at any hour. ${window.open ? 'Window open now.' : `Next window opens ${stamp(window.next_open_at)}.`}` : ''}
  </p>;
}

function Store({ id, title, c }) {
  if (!c?.measured && !c?.live_runs?.length) return <div data-testid={`estate-content-${id}`}><h3>{title}</h3><p className="estate-note">{c?.note || 'No content pass has been commissioned for this store.'}</p></div>;
  const h = c.headers || {}, s = c.sample || {}, est = c.estimates || {};
  return <div data-testid={`estate-content-${id}`}>
    <h3 data-testid={`estate-content-heading-${id}`}>{title} <small>{count(c.sources_complete)} of {count(c.sources)} stores finished{c.sources_listing ? ` · ${count(c.sources_listing)} still listing` : ''} · {c.eta_hours != null ? `≈${count(c.eta_hours)} h of reading to go at ${count(c.throughput_files_per_hour)} files/h` : c.objects_pending ? `${count(c.objects_pending)} sampled files to read` : 'nothing pending'}</small></h3>
    <div className="estate-tiles">
      <Tile id={`${id}-listed`} label="Media listed (fact)" value={bytes(c.media_bytes)} note={`${count(c.media_objects)} files · ${count(c.audio_objects)} audio · ${count(c.video_objects)} video`} />
      <Tile id={`${id}-hours`} label="Hours held (header-measured)" value={hours(h.hours_est)} note={`${h.hours_lo != null ? `${hours(h.hours_lo)}–${hours(h.hours_hi)} · ` : ''}${count(h.probed_files)} files probed · ${hours(h.probed_hours)} measured directly, the rest by folder rate`} tone="sage" />
      <Tile id={`${id}-speech`} label="Speech hours (estimate · 95%)" value={hours(est.speech?.est)} note={`${interval(est.speech)} · music ${interval(est.music)} · silence ${hours(est.silence?.est)}`} tone="brass" />
      <Tile id={`${id}-languages`} label="Speech by language (estimate)" value={langs(est.languages, 1) || '—'} note={langs(est.languages, 6)} />
      <Tile id={`${id}-sample`} label="Sample read in full" value={`${count(s.read_files)} / ${count(s.planned_files)}`} note={`${count(s.strata)} folders · ${count(s.census_strata)} read whole · ${hours(s.hours_decoded)} decoded · ${bytes(c.bytes_read)} verified`} />
      <Tile id={`${id}-egress`} label={id === 'obs' ? 'OBS egress so far' : 'Transfer so far'} value={id === 'obs' ? usd(c.egress?.usd_estimate) : bytes(c.egress?.bytes)} note={id === 'obs' ? `${bytes(c.egress?.bytes)} at an assumed $${c.egress?.usd_per_gb_assumed ?? '—'}/GB · billed to ${c.egress?.billed_to || 'RMS'}` : c.egress?.billed_to || ''} tone={id === 'obs' ? 'oxblood' : undefined} />
      <Tile id={`${id}-denied`} label="Listed but not readable" value={bytes((c.bytes_denied || 0) + (c.bytes_archived || 0))} note={`${count(c.objects_denied)} files refused by the key · ${count(c.objects_archived)} in archive storage · ${count(c.objects_failed)} read failures`} />
    </div>
    <Live runs={c.live_runs} window={c.read_window} />
    <EstateContentAccess id={id} blocked={c.access_blocked} readable={c.readable} classes={c.storage_classes} />
    <div className="estate-table-wrap"><table className="estate-table" data-testid={`estate-content-table-${id}`}>
      <thead><tr><th>Store</th><th>Access · state</th><th>Hours held</th><th>Speech (95%)</th><th>Languages</th><th>Sample</th></tr></thead>
      <tbody>{(c.source_rows || []).map(r => <tr key={r.label} data-testid={`estate-content-row-${r.label}`}>
        <td data-label="Store"><b>{r.label}</b><small>{count(r.media_objects)} media files · {bytes(r.media_bytes)}{r.inventory_complete ? '' : ' · listing continues'}</small></td>
        <td data-label="Access · state">{ACCESS[r.access] || r.access}<small>{MEASUREMENT[r.measurement] || r.measurement}{r.egress_usd != null && id === 'obs' ? ` · ${usd(r.egress_usd)}` : ''}</small></td>
        <td data-label="Hours held">{r.access === 'readable' ? hours(r.hours?.est) : 'not measurable'}<small>{r.access !== 'readable' ? 'counted, never estimated' : `${r.hours?.lo != null ? `${hours(r.hours.lo)}–${hours(r.hours.hi)} · ` : ''}${n(r.hours?.probed_files)} probed`}</small></td>
        <td data-label="Speech (95%)">{hours(r.speech?.est)}<small>{interval(r.speech)} · music {hours(r.music?.est)}</small></td>
        <td data-label="Languages"><small>{langs(r.languages, 4)}</small></td>
        <td data-label="Sample">{n(r.sample?.read_files)} / {n(r.sample?.planned_files)}<small>{n(r.sample?.strata)} folders · {n(r.sample?.census_strata)} whole · {r.objects_failed ? `${count(r.objects_failed)} failed` : 'no failures'}</small></td>
      </tr>)}</tbody>
    </table></div>
    <EstateContentFolders id={id} folders={c.folders} total={c.folders_total} />
  </div>;
}

export function EstateContentCensus({ report }) {
  const stores = report.stores || {};
  const t = stores.content_total;
  return <section className="estate-section" data-testid="estate-content-census">
    <header className="estate-head"><div><h2>Content census · hours held and speech by language</h2>
      <p>Owner ruling 2 Oct: every object listed and header-measured (facts); a deterministic random sample per folder read byte for byte on both GPU hosts and judged on every two-second window (estimates with 95 % intervals); NAS files read off-peak only. Small folders are read whole and carry no sampling error. Stores the key cannot read are noted — counted, never estimated — and the whole sample budget goes to what can be read. Progress below is the live, verified state.</p></div></header>
    {t && <div className="estate-tiles" data-testid="estate-content-total">
      <Tile id="total-hours" label="Estate hours held" value={hours(t.hours_held?.est)} note={`${hours(t.hours_held?.lo)}–${hours(t.hours_held?.hi)} · ${count(t.media_objects)} media files · ${bytes(t.media_bytes)}`} tone="sage" />
      <Tile id="total-speech" label="Estate speech hours (95%)" value={hours(t.speech?.est)} note={`${interval(t.speech)} · music ${interval(t.music)}`} tone="brass" />
      <Tile id="total-languages" label="Estate speech by language" value={langs(t.languages, 1) || '—'} note={langs(t.languages, 8)} />
      <Tile id="total-sample" label="Files read in full" value={`${count(t.sample_read_files)} / ${count(t.sample_planned_files)}`} note={`OBS egress so far ${usd(t.egress_usd)} (assumed tariff)`} />
    </div>}
    <div style={{ marginTop: 28 }}><Store id="obs" title="OBS object store" c={stores.obs?.content} /></div>
    <div style={{ marginTop: 32 }}><Store id="nas" title="NAS file shares" c={stores.nas?.content} /></div>
    <p className="estate-note" data-testid="estate-content-method">Facts: listed sizes and counts; header durations read from each file (every audio file; a per-folder sample of video files, the rest extrapolated by that folder's seconds-per-byte with its standard error). Estimates: the admitted music detector and the current audio language model judge every two-second window of a seeded, nested random sample of files per folder; ratio estimators with finite-population correction give the 95 % intervals; a folder whose interval stays wider than ±5 points receives a nested top-up. Hours are model detections, not human labels; what counts as clean, eligible speech is decided in the report, not by the reader. Files the key cannot read are counted, never estimated.</p>
  </section>;
}
