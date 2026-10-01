/*
 * EstateIntelligence.jsx — v2 OS · Admin tab · MANAGE ESTATE · Registry › Estate intelligence report, LIVE.
 *
 * The full estate-handling report behind the Registry's estate intelligence tiles: condition, duplication, quality,
 * degradation and trend, dimensional monetisation candidates with licensable grain, cost-reduction strategies with
 * evidence, method and limits, and the governed dossier. Everything is read from the banked, digest-verified census
 * report (aggregates only); nothing here measures, extracts or grants rights.
 */
import React from 'react';
import { CensusAccess } from '@/components/census/CensusAccess';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { EstateHeadline } from '@/components/estate/EstateHeadline';
import { EstateDatabases } from '@/components/estate/EstateDatabases';
import { EstateDuplication } from '@/components/estate/EstateDuplication';
import { EstateStores } from '@/components/estate/EstateStores';
import { EstateQuality } from '@/components/estate/EstateQuality';
import { EstateProducts } from '@/components/estate/EstateProducts';
import { EstateStrategies } from '@/components/estate/EstateStrategies';
import { EstateDossier, EstateMethod } from '@/components/estate/EstateDossier';
import { useEstateReport, stamp } from '@/components/estate/useEstateReport';
import { studioRequest } from '@/components/studio/useStudio';
import { PresentationDetails, readableText } from '@/components/shared/PresentationDetails';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import '@/components/census/census.css';
import '@/components/estate/estate.css';

export default function EstateIntelligence() {
  const session = usePrototypeSession();
  const signedIn = Boolean(session.data);
  const canCompose = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const { report, running, loading, error, composing, refusal, reload, compose } = useEstateReport(signedIn);
  const [pack, setPack] = React.useState({ busy: false, commission: null, error: null });
  const commissionPack = async () => {
    setPack({ busy: true, commission: null, error: null });
    try {
      const result = await studioRequest(`/producers/estate-intelligence/${report.job_id}`, { method: 'POST', body: JSON.stringify({}) });
      setPack({ busy: false, commission: result.commission, error: null, created: result.created });
    } catch (e) { setPack({ busy: false, commission: null, error: e.message }); }
  };
  return <OwnerWorkspace session={session} title="Estate intelligence" group="Registry" returnTo="/os/admin/estate"><div className="estate" data-testid="estate-intelligence-surface">
    <header className="estate-header">
      <div>
        <div className="estate-crumb" data-testid="estate-breadcrumb"><a href="/os/admin/estate?app=registry" data-testid="estate-back-registry">MANAGE ESTATE · Registry</a> · Estate intelligence{session.data?.tenant_id ? ` · ${session.data.tenant_id}` : ''}</div>
        <h1 className="estate-title" data-testid="estate-title">Estate intelligence</h1>
        {report && <div className="estate-meta" data-testid="estate-meta"><span>Measured {stamp(report.measured_at)}</span><span>{report.status === 'complete' ? 'Census complete' : 'Partial coverage'}</span></div>}
      </div>
      {signedIn && <div className="estate-actions">
        <button className="estate-btn" onClick={reload} disabled={loading} data-testid="estate-reload">{loading ? 'Refreshing…' : 'Refresh'}</button>
        {report?.brief_path && <a className="estate-btn" href={report.brief_path} target="_blank" rel="noopener noreferrer" data-testid="estate-download-brief">Download the brief (.md)</a>}
        {report && canCompose && <button className="estate-btn primary" onClick={commissionPack} disabled={pack.busy} data-testid="estate-commission-pack">{pack.busy ? 'Commissioning…' : 'Commission board pack'}</button>}
      </div>}
    </header>
    {!signedIn && <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />}
    {signedIn && <div className="estate-body">
      {pack.error && <p className="estate-alert" role="alert" data-testid="estate-pack-error">The board pack could not be created. Refresh this report and try again.</p>}
      {pack.commission && <div className="estate-running" data-testid="estate-pack-result">{pack.created ? 'Board pack created' : 'Today’s board pack is available'} · {readableText(pack.commission.release.state)}. <a href={`/os/work/documents?commission=${pack.commission.commission_id}`} data-testid="estate-pack-open">Open in Documents</a></div>}
      {running && <div className="estate-running" data-testid="estate-running">Census in progress · {running.databases_done} databases checked. Showing the last verified report.</div>}
      {error && <p className="estate-alert" role="alert" data-testid="estate-error">The latest report could not be refreshed. {report ? 'The last loaded report remains below. ' : ''}Try Refresh; if it still fails, ask your estate operator to review source access.</p>}
      {loading && !report && <p data-testid="estate-loading">Loading the latest report…</p>}
      {!report && !loading && !error && <div className="estate-empty" data-testid="estate-empty">No verified report yet. <a href="/os/admin/estate?app=registry" data-testid="estate-empty-registry">Open Registry</a> to review census coverage.</div>}
      {report && <>
        <EstateHeadline report={report} />
        <EstateStrategies report={report} />
        <PresentationDetails id="estate-duplication-evidence" title="Compare duplicate table locations"><EstateDuplication report={report} /></PresentationDetails>
        <PresentationDetails id="estate-storage-evidence" title="Object stores & file shares"><EstateStores report={report} /></PresentationDetails>
        <PresentationDetails id="estate-quality-evidence" title="Quality issues & changes since the last census"><EstateQuality report={report} /></PresentationDetails>
        <PresentationDetails id="estate-product-evidence" title="Potential data products & what blocks them"><EstateProducts report={report} /></PresentationDetails>
        <PresentationDetails id="estate-database-evidence" title="Database inventory"><EstateDatabases report={report} /></PresentationDetails>
        <PresentationDetails id="estate-written-brief" title="Written assessment"><EstateDossier report={report} canCompose={canCompose} composing={composing} refusal={refusal} onCompose={compose} /></PresentationDetails>
        <PresentationDetails id="estate-method-evidence" title="Coverage & measurement limits"><EstateMethod report={report} /></PresentationDetails>
      </>}
    </div>}
  </div></OwnerWorkspace>;
}
