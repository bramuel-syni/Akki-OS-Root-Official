/*
 * WorkDocuments.jsx — v2 OS · Work tab · WORKSTUDIO · Documents · LIVE (M6 · doc-studio).
 *
 * The production studio for finished documents: commissions built from receipted content models, prove-builds with hash
 * evidence, validate/QA reports, downloads (pptx · docx · html · pdf export), revisions with strike detection and re-verdict.
 * Every document in view carries its lineage: brief, direction verdict, manifest, receipts and the environment of record.
 */
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { CensusAccess } from '@/components/census/CensusAccess';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { censusRequest } from '@/components/census/useCensusWorkspace';
import { CommissionList, StudioSkill } from '@/components/studio/CommissionList';
import { CommissionBuilds } from '@/components/studio/CommissionBuilds';
import { CommissionDirection, CommissionRevisions } from '@/components/studio/CommissionRevisions';
import { useStudio, stamp } from '@/components/studio/useStudio';
import '@/components/census/census.css';
import '@/components/estate/estate.css';

export default function WorkDocuments() {
  const session = usePrototypeSession();
  const signedIn = Boolean(session.data);
  const canOperate = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const initial = new URLSearchParams(useLocation().search).get('commission');
  const studio = useStudio(signedIn, initial);
  const { skill, commissions, selected, commission, loading, busy, error, notice, reload, select, act, fail } = studio;
  const commissionLatest = async () => {
    try {
      const { report } = await censusRequest('/estate-intelligence/report');
      if (!report) throw new Error('No verified estate intelligence census is on record for your tenant.');
      await act('Commission board pack', `/producers/estate-intelligence/${report.job_id}`, {});
    } catch (e) { fail(e.message); }
  };
  return <div className="estate" data-testid="work-documents-surface">
    <header className="estate-header">
      <div>
        <div className="estate-crumb" data-testid="work-documents-breadcrumb">WORKSTUDIO · Documents{skill?.tenant_id ? ` · ${skill.tenant_id}` : ''}</div>
        <h1 className="estate-title" data-testid="work-documents-title">Documents</h1>
        <p className="estate-lead" data-testid="work-documents-lead">Every document in view carries its lineage: who prepared it, what admits it, what it depends on. Nothing floats without a source — decks, papers and review pages are produced deterministically from one receipted content model, in a recorded creative direction.</p>
        {skill && <div className="estate-meta" data-testid="work-documents-meta"><span>studio <code>{skill.skill} v{skill.version}</code></span><span>{(commissions || []).length} commission{(commissions || []).length === 1 ? '' : 's'}</span><span>{skill.environment?.libreoffice}</span><span>installed {stamp(skill.installed_at)}</span></div>}
      </div>
      {signedIn && <div className="estate-actions">
        <Link className="estate-btn" to="/os/work/media" data-testid="work-documents-media-library">Media library</Link>
        <button className="estate-btn" onClick={() => reload(selected)} disabled={loading} data-testid="work-documents-reload">{loading ? 'Reading…' : 'Re-read'}</button>
        {canOperate && <button className="estate-btn primary" onClick={commissionLatest} disabled={Boolean(busy)} data-testid="work-documents-commission-census">{busy === 'Commission board pack' ? 'Commissioning…' : 'Commission board pack from latest census'}</button>}
      </div>}
    </header>
    {!signedIn && <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />}
    {signedIn && <div className="estate-body">
      {error && <p className="estate-alert" role="alert" data-testid="work-documents-error">{error}</p>}
      {notice && <div className="estate-running" data-testid="work-documents-notice">{notice}</div>}
      {commissions && <CommissionList commissions={commissions} selected={selected} onSelect={select} />}
      {commission && <>
        <CommissionBuilds commission={commission} canOperate={canOperate} busy={busy} onBuild={() => act('Build', `/commissions/${commission.commission_id}/build`)} onExport={buildId => act('Export PDF', `/commissions/${commission.commission_id}/builds/${buildId}/export-pdf`)} onThumbnails={buildId => act('Render pages', `/commissions/${commission.commission_id}/builds/${buildId}/thumbnails`)} />
        <CommissionRevisions commission={commission} canOperate={canOperate} busy={busy} onRevise={changes => act('Revise', `/commissions/${commission.commission_id}/revise`, { changes })} onReverdict={() => act('Re-verdict', `/commissions/${commission.commission_id}/reverdict`)} />
        <CommissionDirection commission={commission} />
      </>}
      <StudioSkill skill={skill} />
    </div>}
  </div>;
}
