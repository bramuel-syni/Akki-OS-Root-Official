import React, { useEffect, useState } from 'react';
import { Download } from 'lucide-react';
import { artifactBlob, downloadArtifact, releaseClass, stamp } from './useStudio';
import { DeckThumbnails } from './DeckThumbnails';
import { documentTitle, PresentationDetails, readableText } from '../shared/PresentationDetails';

function ReviewPreview({ commission, build }) {
  const [url, setUrl] = useState(null);
  const [error, setError] = useState('');
  const html = build.outputs.find(o => o.format === 'html');
  useEffect(() => {
    let active = true; let objectUrl = null; setUrl(null); setError('');
    if (html && build.status === 'released') artifactBlob(commission.commission_id, build.build_id, html.name).then(blob => { if (!active) return; objectUrl = URL.createObjectURL(blob); setUrl(objectUrl); }).catch(() => { if (active) setError('Preview unavailable. Try downloading the review page.'); });
    return () => { active = false; if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [commission.commission_id, build.build_id, build.status, html]);
  if (!html || build.status !== 'released') return null;
  return <PresentationDetails id="studio-preview" title="Original review page">
    {error ? <p role="alert" data-testid="studio-preview-error">{error}</p> : url ? <iframe title="Original review page" src={url} sandbox="" data-testid="studio-preview-frame" style={{ width: '100%', height: 560, border: '1px solid var(--line)', background: '#fff' }} /> : <p data-testid="studio-preview-loading">Loading preview…</p>}
  </PresentationDetails>;
}

export function CommissionBuilds({ commission, canOperate, busy, onBuild, onExport, onThumbnails }) {
  const builds = commission.builds || [];
  const [open, setOpen] = useState(null), [error, setError] = useState('');
  useEffect(() => { setOpen(null); setError(''); }, [commission.commission_id]);
  const build = builds.find(b => b.build_id === open) || builds[builds.length - 1];
  const download = async name => {
    setError('');
    const filename = `${documentTitle(commission).replace(/[\\/:*?"<>|]/g, '-')} - v${build.content_version}${name === 'build-manifest.json' ? ' - build evidence' : ''}.${name.split('.').pop()}`;
    try { await downloadArtifact(commission.commission_id, build.build_id, name, filename); } catch (e) { setError(readableText(e.message)); }
  };
  return <section className="estate-section" data-testid="studio-builds">
    <div className="estate-head"><div><h2 data-testid="studio-document-title">{documentTitle(commission)}</h2>{build && <p data-testid="studio-build-summary">Version {build.content_version} · {stamp(build.at)} · {build.status === 'released' ? 'Ready to download' : readableText(build.status)}</p>}</div>
      {canOperate && <button className="estate-btn" onClick={onBuild} disabled={Boolean(busy)} data-testid="studio-build-btn">{busy === 'Build' ? 'Building…' : builds.length ? 'Rebuild document' : 'Build document'}</button>}</div>
    {!build && <p data-testid="studio-builds-empty">This document has not been built yet.</p>}
    {error && <p className="estate-alert" role="alert" data-testid="studio-download-error">{error}</p>}
    {build && <div data-testid="studio-build-detail">
      {build.blockers?.length > 0 && <ul className="estate-errors" data-testid="studio-build-blockers">{build.blockers.map((e, i) => <li key={i}>{readableText(e.message || e.rule)}</li>)}</ul>}
      {build.status === 'released' && <div className="studio-output-list" data-testid="studio-outputs-table">
        {build.outputs.map(o => <button key={o.name} className="estate-btn" onClick={() => download(o.name)} data-testid={`studio-download-${o.format}`}><Download size={14} />{o.format.toUpperCase()}</button>)}
        {build.exports?.pdf?.exported && <button className="estate-btn" onClick={() => download('review.pdf')} data-testid="studio-download-pdf"><Download size={14} />PDF</button>}
        {canOperate && !build.exports?.pdf?.exported && <button className="estate-btn" onClick={() => onExport(build.build_id)} disabled={Boolean(busy)} data-testid="studio-export-pdf">{busy === 'Export PDF' ? 'Exporting…' : 'Export PDF'}</button>}
      </div>}
      {build.exports?.pdf && !build.exports.pdf.exported && <p className="estate-alert" role="alert" data-testid="studio-pdf-error">PDF unavailable: {readableText(build.exports.pdf.refusal)}</p>}
      <DeckThumbnails commission={commission} build={build} canOperate={canOperate} busy={busy} onRender={onThumbnails} />
      <PresentationDetails id="studio-quality" title="Quality checks & build history">
        <p data-testid="studio-reproducibility">{build.prove ? build.prove.byte_identical ? 'Rebuild matched the original files.' : 'Rebuild did not match. Review required.' : 'Reproducibility has not been checked.'}</p>
        <p data-testid="studio-check-status">Validation: {build.validate?.status || 'Not checked'} · Quality: {build.qa?.status || 'Not checked'}</p>
        {[['validate', build.validate?.blockers], ['qa', build.qa?.blockers], ['review', build.validate?.review]].map(([key, rows]) => rows?.length > 0 && <ul key={key} data-testid={`studio-${key}-questions`}>{rows.map((row, i) => <li key={i}>{readableText(row)}</li>)}</ul>)}
        <ul className="estate-list" data-testid="studio-build-list">{builds.slice().reverse().map((b, i) => <li key={b.build_id}><button className="studio-version-button" onClick={() => setOpen(b.build_id)} aria-pressed={build.build_id === b.build_id} data-testid={`studio-build-${b.build_id}`}>Build {builds.length - i} · Version {b.content_version} · {stamp(b.at)} <span className={`estate-status ${releaseClass(b.status)}`}>{b.status}</span></button></li>)}</ul>
        <button className="estate-btn" onClick={() => download('build-manifest.json')} data-testid="studio-download-manifest"><Download size={14} />Download build evidence</button>
      </PresentationDetails>
      <ReviewPreview commission={commission} build={build} />
    </div>}
  </section>;
}