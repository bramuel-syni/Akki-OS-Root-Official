import React from 'react';
import { bytes, count, stamp } from './useEstateReport';

const STATE = { denied: 'Key refused GetObject', archived: 'Archive class · restore needed' };

export function EstateContentAccess({ id, blocked, readable, classes }) {
  if (!blocked?.sources?.length) return null;
  const pct = Math.round((blocked.share_of_media_objects || 0) * 1000) / 10;
  return <div className="estate-alert" data-testid={`estate-content-access-${id}`} style={{ marginTop: 18 }}>
    <div className="estate-head"><div>
      <h4 style={{ margin: 0 }} data-testid={`estate-content-access-heading-${id}`}>Listed but not readable · {count(blocked.sources.length)} stores · {count(blocked.media_objects)} media files · {bytes(blocked.media_bytes)} ({pct}% of the media files listed here)</h4>
      <small className="estate-note">The census notes what it cannot reach and measures what it can: {count(readable?.media_objects)} readable media files ({bytes(readable?.media_bytes)}) in {count(readable?.sources)} stores carry the whole sample budget.{classes?.archive_pct_of_bytes != null ? ` ${classes.archive_pct_of_bytes}% of the listed bytes already sit in Archive class.` : ''}</small>
    </div></div>
    {blocked.denied_grant && <p className="estate-note" data-testid={`estate-content-access-grant-${id}`}><b>Grant required ({count(blocked.denied_sources)} buckets):</b> {blocked.denied_grant}</p>}
    {blocked.archived_note && <p className="estate-note" data-testid={`estate-content-access-archived-${id}`}><b>Restore required ({count(blocked.archived_sources)} buckets):</b> {blocked.archived_note}</p>}
    <div className="estate-table-wrap"><table className="estate-table" data-testid={`estate-content-access-table-${id}`}>
      <thead><tr><th>Store</th><th>State</th><th>Media files</th><th>Audio · video</th><th>Bytes</th><th>Refused since</th></tr></thead>
      <tbody>{blocked.sources.map(s => <tr key={s.label} data-testid={`estate-content-access-row-${s.label}`}>
        <td data-label="Store"><b>{s.label}</b></td>
        <td data-label="State">{STATE[s.access] || s.access}</td>
        <td data-label="Media files">{count(s.media_objects)}</td>
        <td data-label="Audio · video"><small>{count(s.audio_objects)} audio · {count(s.video_objects)} video</small></td>
        <td data-label="Bytes">{bytes(s.media_bytes)}<small>{s.archive_bytes ? `${bytes(s.archive_bytes)} in Archive class` : ''}</small></td>
        <td data-label="Refused since"><small>{s.since ? stamp(s.since) : 'this run'}</small></td>
      </tr>)}</tbody>
    </table></div>
  </div>;
}
