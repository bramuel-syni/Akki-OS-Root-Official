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
  return <div className="estate" data-testid="estate-intelligence-surface">
    <header className="estate-header">
      <div>
        <div className="estate-crumb" data-testid="estate-breadcrumb"><a href="/os/admin/estate?app=registry" data-testid="estate-back-registry">MANAGE ESTATE · Registry</a> · Estate intelligence{session.data?.tenant_id ? ` · ${session.data.tenant_id}` : ''}</div>
        <h1 className="estate-title" data-testid="estate-title">Estate intelligence</h1>
        <p className="estate-lead" data-testid="estate-lead">{report ? report.reading : 'What the estate holds, how much of it repeats, decays or carries risk, what it could become, and what it costs to keep — measured on the estate, reported as aggregates.'}</p>
        {report && <div className="estate-meta" data-testid="estate-meta"><span>census <code>{report.job_id}</code></span><span>status {report.status}</span><span>measured {stamp(report.measured_at)}</span><span>report built {stamp(report.built_at)}</span><span>row values retained: none</span></div>}
      </div>
      {signedIn && <div className="estate-actions">
        <button className="estate-btn" onClick={reload} disabled={loading} data-testid="estate-reload">{loading ? 'Reading…' : 'Re-read report'}</button>
        {report?.brief_path && <a className="estate-btn" href={report.brief_path} target="_blank" rel="noopener noreferrer" data-testid="estate-download-brief">Download the brief (.md)</a>}
        {report && canCompose && <button className="estate-btn primary" onClick={commissionPack} disabled={pack.busy} data-testid="estate-commission-pack">{pack.busy ? 'Commissioning…' : 'Commission board pack'}</button>}
      </div>}
    </header>
    {!signedIn && <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />}
    {signedIn && <div className="estate-body">
      {pack.error && <p className="estate-alert" role="alert" data-testid="estate-pack-error">{pack.error}</p>}
      {pack.commission && <div className="estate-running" data-testid="estate-pack-result">{pack.created ? 'Board pack commissioned' : 'Board pack already on record for today'}: <code>{pack.commission.commission_id}</code> · {pack.commission.release.state} — {pack.commission.release.reason}. <a href={`/os/work/documents?commission=${pack.commission.commission_id}`} data-testid="estate-pack-open">Open in Documents</a></div>}
      {running && <div className="estate-running" data-testid="estate-running">Census <code>{running.job_id}</code> is measuring the estate now ({running.databases_done} databases so far); this report stays on the last verified receipt until the new one is banked.</div>}
      {error && <p className="estate-alert" role="alert" data-testid="estate-error">{error}</p>}
      {!report && !loading && !error && <div className="estate-empty" data-testid="estate-empty">No verified estate intelligence census is on record for your tenant. Figures stay unmeasured until a census completes and its receipt is digest-verified; the Registry's “Run census” commissions one.</div>}
      {report && <>
        <EstateHeadline report={report} />
        <EstateDatabases report={report} />
        <EstateDuplication report={report} />
        <EstateStores report={report} />
        <EstateQuality report={report} />
        <EstateProducts report={report} />
        <EstateStrategies report={report} />
        <EstateDossier report={report} canCompose={canCompose} composing={composing} refusal={refusal} onCompose={compose} />
        <EstateMethod report={report} />
      </>}
    </div>}
  </div>;
}
