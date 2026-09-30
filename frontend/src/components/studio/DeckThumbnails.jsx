import React, { useEffect, useState } from 'react';
import { stamp } from './useStudio';

const token = () => sessionStorage.getItem('akki_access_token');
const thumbUrl = (commissionId, buildId, n) => `${process.env.REACT_APP_BACKEND_URL}/api/studio/commissions/${commissionId}/builds/${buildId}/thumbnail/${n}`;

function usePageBlobs(commissionId, buildId, pages) {
  const [urls, setUrls] = useState({});
  useEffect(() => {
    let active = true; const made = [];
    setUrls({});
    Promise.all(pages.map(async p => {
      const response = await fetch(thumbUrl(commissionId, buildId, p.n), { headers: token() ? { Authorization: `Bearer ${token()}` } : {} });
      if (!response.ok) return [p.n, null];
      const url = URL.createObjectURL(await response.blob()); made.push(url);
      return [p.n, url];
    })).then(entries => { if (active) setUrls(Object.fromEntries(entries)); });
    return () => { active = false; made.forEach(u => URL.revokeObjectURL(u)); };
  }, [commissionId, buildId, pages]);
  return urls;
}

export function DeckThumbnails({ commission, build, canOperate, busy, onRender }) {
  const thumbs = build.exports?.thumbnails;
  const pages = thumbs?.pages || [];
  const urls = usePageBlobs(commission.commission_id, build.build_id, pages);
  const [focus, setFocus] = useState(null);
  useEffect(() => { setFocus(null); }, [build.build_id]);
  if (build.status !== 'released') return null;
  const deck = build.outputs.find(o => o.format === 'pptx');
  if (!deck) return null;
  const focused = focus && pages.find(p => p.n === focus);
  return <div className="studio-thumbs" data-testid="studio-thumbnails">
    <div className="estate-head" style={{ marginTop: 14 }}>
      <div><h3>Pages · {deck.name}</h3><p>Every page of the released deck, rendered from the recorded pptx through the environment of record so a reviewer can answer the review questions without downloading. A visual-QA export — outside the byte-identity contract.</p></div>
      {thumbs?.rendered && <span className="estate-status complete" data-testid="studio-thumbnails-count">{thumbs.count} page{thumbs.count === 1 ? '' : 's'} · {thumbs.dpi} dpi</span>}
    </div>
    {!thumbs && <div className="estate-actions" style={{ marginTop: 10, justifyContent: "flex-start" }}>
      <span className="estate-note" style={{ margin: 0 }} data-testid="studio-thumbnails-empty">No page thumbnails on record for this build.</span>
      {canOperate && <button className="estate-btn" onClick={() => onRender(build.build_id)} disabled={Boolean(busy)} data-testid="studio-render-thumbnails">{busy === 'Render pages' ? 'Rendering pages…' : 'Render page thumbnails'}</button>}
    </div>}
    {thumbs && !thumbs.rendered && <p className="estate-alert" role="alert" data-testid="studio-thumbnails-refusal">Thumbnails refused: {thumbs.refusal} · {stamp(thumbs.at)}</p>}
    {thumbs?.rendered && <>
      <ol className="studio-thumb-grid" data-testid="studio-thumbnail-grid">
        {pages.map(p => <li key={p.n} className={focus === p.n ? 'on' : ''} data-testid={`studio-thumbnail-${p.n}`}>
          <button type="button" onClick={() => setFocus(focus === p.n ? null : p.n)} aria-label={`Open page ${p.n}`} data-testid={`studio-thumbnail-open-${p.n}`}>
            {urls[p.n] === undefined ? <span className="studio-thumb-wait">Rendering…</span>
              : urls[p.n] === null ? <span className="studio-thumb-wait">Not on record</span>
                : <img src={urls[p.n]} alt={`Page ${p.n} of ${deck.name}`} loading="lazy" />}
          </button>
          <small><b>{p.n}</b> · {p.sha256.slice(0, 10)}…</small>
        </li>)}
      </ol>
      {focused && urls[focused.n] && <figure className="studio-thumb-focus" data-testid="studio-thumbnail-focus">
        <div className="estate-actions" style={{ justifyContent: "flex-start" }}>
          <button className="estate-btn" onClick={() => setFocus(Math.max(1, focused.n - 1))} disabled={focused.n === 1} data-testid="studio-thumbnail-prev">‹ Previous</button>
          <span className="estate-status" data-testid="studio-thumbnail-focus-label">Page {focused.n} of {pages.length}</span>
          <button className="estate-btn" onClick={() => setFocus(Math.min(pages.length, focused.n + 1))} disabled={focused.n === pages.length} data-testid="studio-thumbnail-next">Next ›</button>
          <button className="estate-btn" onClick={() => setFocus(null)} data-testid="studio-thumbnail-close">Close</button>
        </div>
        <img src={urls[focused.n]} alt={`Page ${focused.n} of ${deck.name}, enlarged`} />
        <figcaption><code>{focused.name}</code> · sha256 <code>{focused.sha256}</code> · {focused.size?.toLocaleString('en-GB')} B · rendered {stamp(thumbs.at)}</figcaption>
      </figure>}
    </>}
  </div>;
}
