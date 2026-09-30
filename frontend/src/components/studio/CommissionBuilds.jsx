import React, { useEffect, useState } from 'react';
import { artifactBlob, downloadArtifact, releaseClass, short, stamp } from './useStudio';

function ReviewPreview({ commission, build }) {
  const [url, setUrl] = useState(null);
  const html = build.outputs.find(o => o.format === 'html');
  useEffect(() => {
    let active = true; let objectUrl = null;
    if (html && build.status === 'released') artifactBlob(commission.commission_id, build.build_id, html.name).then(blob => { if (!active) return; objectUrl = URL.createObjectURL(blob); setUrl(objectUrl); }).catch(() => setUrl(null));
    return () => { active = false; if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [commission.commission_id, build.build_id, build.status, html]);
  if (!html || build.status !== 'released') return null;
  return <div style={{ marginTop: 12 }} data-testid="studio-preview">
    <h3>Review page · {html.name}</h3>
    {url ? <iframe title="Review page" src={url} sandbox="" data-testid="studio-preview-frame" style={{ width: '100%', height: 560, border: '1px solid var(--line)', borderRadius: 8, background: '#2b2b2b' }} /> : <div className="estate-note">Reading the review page…</div>}
  </div>;
}

export function CommissionBuilds({ commission, canOperate, busy, onBuild, onExport }) {
  const builds = commission.builds || [];
  const [open, setOpen] = useState(null);
  const shown = open || builds[builds.length - 1]?.build_id;
  const build = builds.find(b => b.build_id === shown);
  return <section className="estate-section" data-testid="studio-builds">
    <div className="estate-head"><div><h2>Builds</h2><p>Each build runs the studio twice and asserts byte-identical outputs — the determinism contract, tested, not assumed. Blockers stop release; review questions are for a human, never auto-fixed.</p></div>
      {canOperate && <button className="estate-btn" onClick={onBuild} disabled={Boolean(busy)} data-testid="studio-build-btn">{busy === 'Build' ? 'Building…' : 'Rebuild current version'}</button>}</div>
    {!builds.length && <div className="estate-note" data-testid="studio-builds-empty">No build yet.</div>}
    {builds.length > 0 && <ul className="estate-list" data-testid="studio-build-list">{builds.slice().reverse().map(b => <li key={b.build_id} onClick={() => setOpen(b.build_id)} style={{ cursor: 'pointer', background: shown === b.build_id ? 'var(--surface2)' : undefined }} data-testid={`studio-build-${b.build_id}`}>
      <span><b>{b.build_id}</b> <small>content v{b.content_version} · {stamp(b.at)}{b.prove ? ` · ${b.prove.byte_identical ? 'byte-identical across two builds' : 'NOT reproducible'}` : ''}{b.error ? ` · ${b.error}` : ''}</small></span>
      <small><span className={`estate-status ${releaseClass(b.status)}`} data-testid={`studio-build-status-${b.build_id}`}>{b.status}</span></small></li>)}</ul>}
    {build && <div data-testid="studio-build-detail">
      <h3 style={{ marginTop: 14 }}>Outputs · {build.build_id}</h3>
      {build.blockers?.length ? <ul className="estate-errors" data-testid="studio-build-blockers">{build.blockers.map((e, i) => <li key={i}><b>{e.receipt || e.rule}</b> {e.message}</li>)}</ul> : null}
      {build.outputs.length > 0 && <div className="estate-table-wrap"><table className="estate-table" data-testid="studio-outputs-table"><thead><tr><th>Output</th><th>SHA-256</th><th>Size</th><th /></tr></thead>
        <tbody>{build.outputs.map(o => <tr key={o.name}><td><b>{o.format}</b><small>{o.name}{o.changed_from_previous === false ? ' · unchanged from previous' : o.changed_from_previous ? ' · changed' : ''}</small></td><td><code>{short(o.sha256)}</code></td><td>{o.size?.toLocaleString('en-GB')} B</td>
          <td><button className="estate-btn" onClick={() => downloadArtifact(commission.commission_id, build.build_id, o.name)} data-testid={`studio-download-${o.format}`}>Download</button></td></tr>)}
        {build.exports?.pdf?.exported && <tr><td><b>pdf</b><small>review.pdf · export · furniture {build.exports.pdf.check?.survives ? 'survives' : 'LOST'}</small></td><td><code>{short(build.exports.pdf.sha256)}</code></td><td>{build.exports.pdf.size?.toLocaleString('en-GB')} B</td><td><button className="estate-btn" onClick={() => downloadArtifact(commission.commission_id, build.build_id, 'review.pdf')} data-testid="studio-download-pdf">Download</button></td></tr>}
        <tr><td><b>manifest</b><small>build-manifest.json · inputs, outputs and environment hashes</small></td><td><code>{build.manifest?.build_stamp}</code></td><td /><td><button className="estate-btn" onClick={() => downloadArtifact(commission.commission_id, build.build_id, 'build-manifest.json')} data-testid="studio-download-manifest">Download</button></td></tr>
        </tbody></table></div>}
      <div className="estate-columns" style={{ marginTop: 12 }}>
        <div><h3>Validate · {build.validate?.status || '—'}</h3>
          {build.validate?.blockers?.length ? <ul className="estate-errors" data-testid="studio-validate-blockers">{build.validate.blockers.map((b, i) => <li key={i}>{b}</li>)}</ul> : <div className="estate-note">No blockers.</div>}
          {build.validate?.review?.length ? <><h3 style={{ marginTop: 10 }}>Review questions</h3><ul className="estate-list" data-testid="studio-review-questions">{build.validate.review.map((q, i) => <li key={i}><span><small>{q}</small></span></li>)}</ul></> : null}</div>
        <div><h3>QA · {build.qa?.status || '—'}</h3>
          {build.qa?.blockers?.length ? <ul className="estate-errors" data-testid="studio-qa-blockers">{build.qa.blockers.map((b, i) => <li key={i}>{b}</li>)}</ul> : <div className="estate-note">No mechanical blockers.</div>}
          {build.look && <><h3 style={{ marginTop: 10 }}>Look (seeded)</h3><div className="estate-dims" data-testid="studio-look">{Object.entries(build.look).map(([k, v]) => <span key={k}>{k.replace(/_/g, ' ')} {v}</span>)}</div></>}
          {build.environment && <div className="estate-note" data-testid="studio-build-environment">environment · {build.environment.libreoffice} · python-pptx {build.environment['python-pptx']} · matplotlib {build.environment.matplotlib}</div>}
          {canOperate && build.status === 'released' && !build.exports?.pdf?.exported && <button className="estate-btn" style={{ marginTop: 10 }} onClick={() => onExport(build.build_id)} disabled={Boolean(busy)} data-testid="studio-export-pdf">{busy === 'Export PDF' ? 'Exporting…' : 'Export review page as PDF'}</button>}
          {build.exports?.pdf && !build.exports.pdf.exported && <p className="estate-alert" role="alert">PDF export refused: {build.exports.pdf.refusal}</p>}
        </div>
      </div>
      <ReviewPreview commission={commission} build={build} />
    </div>}
  </section>;
}
