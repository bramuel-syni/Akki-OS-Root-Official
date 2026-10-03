import React from 'react';
import { bytes, count } from './useEstateReport';
import { hours, interval, langs } from './contentFormat';

const STATUS = { census: 'read whole', sampled: 'sample complete', reading: 'reading', planned: 'planned', merged: 'merged' };

export function EstateContentFolders({ id, folders, total }) {
  const [open, setOpen] = React.useState(false);
  if (!folders?.length) return null;
  const shown = open ? folders : folders.slice(0, 12);
  return <div data-testid={`estate-content-folders-${id}`}>
    <div className="estate-head" style={{ marginTop: 18 }}><div><h4 style={{ margin: 0 }}>Folders · ranked by estimated speech hours</h4>
      <small className="estate-note">{count(total)} folders stratified{total > folders.length ? `; the ${count(folders.length)} largest shown` : ''}. Hours held are header-measured per folder; speech, music and languages are 95 % interval estimates from the files read in full.</small></div>
      {folders.length > 12 && <button className="estate-btn" onClick={() => setOpen(o => !o)} data-testid={`estate-content-folders-toggle-${id}`}>{open ? 'Show fewer' : `Show all ${count(folders.length)}`}</button>}
    </div>
    <div className="estate-table-wrap"><table className="estate-table" data-testid={`estate-content-folder-table-${id}`}>
      <thead><tr><th>Folder</th><th>Files</th><th>Hours held</th><th>Speech (95%)</th><th>Music</th><th>Languages</th><th>Sample</th></tr></thead>
      <tbody>{shown.map(f => <tr key={`${f.label}|${f.folder}`} data-testid={`estate-content-folder-row-${id}`}>
        <td data-label="Folder"><b>{f.folder}</b><small>{f.label}{f.kinds ? ` · ${Object.entries(f.kinds).map(([k, v]) => `${count(v)} ${k}`).join(', ')}` : ''}</small></td>
        <td data-label="Files">{count(f.files)}<small>{bytes(f.bytes)}</small></td>
        <td data-label="Hours held">{hours(f.hours?.est)}<small>{f.hours?.se ? `± ${hours(1.96 * f.hours.se)} · ` : ''}{count(f.hours?.probed_files)} probed</small></td>
        <td data-label="Speech (95%)">{hours(f.estimates?.speech?.est)}<small>{interval(f.estimates?.speech)}</small></td>
        <td data-label="Music">{hours(f.estimates?.music?.est)}<small>silence {hours(f.estimates?.silence?.est)}</small></td>
        <td data-label="Languages"><small>{langs(f.estimates?.languages, 4)}</small></td>
        <td data-label="Sample">{count(f.sample?.read)} / {count(f.sample?.target)}<small>{STATUS[f.sample?.status] || f.sample?.status}{f.sample?.speech_share_halfwidth != null ? ` · ±${Math.round(f.sample.speech_share_halfwidth * 100)} pts` : ''}</small></td>
      </tr>)}</tbody>
    </table></div>
  </div>;
}
