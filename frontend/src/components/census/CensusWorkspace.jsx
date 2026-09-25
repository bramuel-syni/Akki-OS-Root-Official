import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ArrowUpRight, Database, History, Play, RefreshCw, ShieldCheck, TriangleAlert } from 'lucide-react';
import { useCensusWorkspace, number, date } from './useCensusWorkspace';
import { CensusAccess } from './CensusAccess';
import { CensusRunDialog } from './CensusRunDialog';
import { CensusRecordDrawer } from './CensusRecordDrawer';
import './census.css';

export const CensusWorkspace = ({ surface = 'dap', initialTab = 'overview' }) => {
  const { data, error, loading, reload } = useCensusWorkspace();
  const [params, setParams] = useSearchParams();
  const [runOpen, setRunOpen] = useState(false);
  const tab = params.get('tab') || initialTab;
  const latest = data?.latest;
  const title = surface === 'os' ? 'Registry' : 'Data Estates';
  const openRecord = record => setParams({ tab: 'records', record: record.record_id });
  return <div className="census-workspace" data-testid="census-workspace">
    <header className="census-header">
      <div><p className="census-eyebrow" data-testid="census-breadcrumb">{surface === 'os' ? 'MANAGE ESTATE / REGISTRY' : 'DATA ACCESS PORTAL / ESTATE'}</p>
        <h1 data-testid="census-title">{title}</h1><p className="census-lead" data-testid="census-lead">What the estate holds. What the evidence establishes.</p></div>
      {data && <div className="census-actions"><button data-testid="census-refresh" aria-label="Refresh census records" title="Refresh census records" className="census-icon-button" onClick={reload} disabled={loading}><RefreshCw size={17} className={loading ? 'census-spin' : ''} /></button>
        {data.can_run && <button data-testid="census-open-run" className="census-button primary" onClick={() => setRunOpen(true)}><Play size={14} />Run census</button>}</div>}
    </header>
    {!data ? <CensusAccess error={error} loading={loading} retry={reload} /> : <>
      <div className="census-context"><span className="census-tenant" data-testid="census-tenant"><ShieldCheck size={15} />{data.tenant_id} estate</span>
        <span data-testid="census-last-observed">{latest ? `Last recorded ${date(latest.finished_at)}` : 'No tenant-attributed census yet'}</span></div>
      <nav className="census-tabs" aria-label="Census views">{[['overview', 'Overview'], ['records', 'Census records'], ['runs', 'Run history']].map(([key, label]) => <button key={key} data-testid={`census-tab-${key}`} aria-current={tab === key ? 'page' : undefined} className={tab === key ? 'active' : ''} onClick={() => setParams({ tab: key })}>{label}{key === 'records' && <span>{data.records.length}</span>}</button>)}</nav>
      {tab === 'overview' && <>
        <div className="census-metrics">{[['databases', 'Databases', latest?.database_count, 'Recorded inventory'], ['tables', 'Tables', latest?.table_count, 'Recorded inventory'], ['rows', latest?.row_count_estimate != null ? 'Estimated rows' : 'Counted rows', latest?.row_count_estimate ?? latest?.row_count_measured, latest?.row_count_estimate != null ? 'Database metadata estimate' : 'Recorded count'], ['volume', 'Data volume', latest?.volume_bytes, 'No volume measurement recorded']].map(([id, label, value, note]) => <section key={id} className="census-metric"><p>{label}</p><strong data-testid={`census-metric-${id}`} className={value == null ? 'unmeasured' : ''}>{number(value)}</strong><small data-testid={`census-metric-${id}-basis`}>{note}</small></section>)}</div>
        <div className="census-body-grid"><section>
          <div className="census-section-heading"><h2>The current reading</h2><Database size={18} /></div>
          {latest ? <button data-testid="census-open-latest" className="census-reading" onClick={() => openRecord(latest)}><div><span className="census-caption">{latest.census_number ? `CENSUS #${latest.census_number}` : 'VERIFIED RUN'}</span><h3>{latest.scope}</h3><p>{latest.execution_verified ? 'Akki-owned execution with retained evidence.' : 'Historical record. Not a fresh source verification.'}</p></div><ArrowUpRight size={21} /></button> : <p data-testid="census-no-records" className="census-empty">No census with established ownership is available for this estate.</p>}
          <h2 className="census-measures-title">Measurement coverage</h2>
          <div className="census-coverage">{['Quality', 'Verified share', 'Personal-data share', 'External-use rights'].map((label, i) => <div key={label}><span>{label}</span><span data-testid={`census-coverage-${i}`}>Not measured</span></div>)}</div>
        </section><aside className="census-evidence-note"><TriangleAlert size={20} /><h2>Unknown stays unknown.</h2><p data-testid="census-evidence-note">{data.measurement_note}</p><p data-testid="census-omission-note">{data.omission_note}</p><div className="census-schedule" data-testid="census-schedule"><History size={16} /><span>On demand<br /><small>No automatic schedule is active.</small></span></div></aside></div>
      </>}
      {tab === 'records' && <section data-testid="census-record-list"><div className="census-section-heading"><h2>Every retained reading</h2><span data-testid="census-record-count">{data.records.length} records</span></div>
        {data.records.length === 0 && <p className="census-empty" data-testid="census-records-empty">No tenant-attributed census records.</p>}
        {data.records.map(record => <button key={record.record_id} className="census-record-row" data-testid={`census-record-${record.record_id}`} onClick={() => openRecord(record)}><span><strong>{record.census_number ? `Census #${record.census_number}` : 'Census run'}</strong><small>{date(record.finished_at)}</small></span><span data-testid={`census-record-tables-${record.record_id}`}>{number(record.table_count)} tables</span><span className="census-caption">{record.execution_verified ? 'Execution verified' : 'Historical record'}</span><ArrowUpRight size={18} /></button>)}</section>}
      {tab === 'runs' && <section data-testid="census-run-history"><div className="census-section-heading"><h2>Commissioned work</h2><span>{data.runs.length} runs</span></div>
        {!data.runs.length && <p data-testid="census-runs-empty" className="census-empty">No operational census has been commissioned for this estate.</p>}
        {data.runs.map(run => <article className="census-run-row" key={run.census_run_id} data-testid={`census-run-${run.census_run_id}`}><header><strong>{run.census_run_id}</strong><span data-testid={`census-run-status-${run.census_run_id}`} className={`census-status ${run.stage}`}>{run.stage === 'executing' ? 'Running' : run.stage.replaceAll('_', ' ')}</span></header><p>{date(run.created_at)}</p>
          {run.reason_code && <p data-testid={`census-run-reason-${run.census_run_id}`} className="census-error">{run.reason_code.replaceAll('_', ' ')}</p>}
          <ul>{run.outcomes.map((outcome, i) => <li data-testid={`census-run-outcome-${run.census_run_id}-${i}`} key={outcome.source_id}><span>{data.sources.find(s => s.source_id === outcome.source_id)?.label || outcome.source_id}</span><span>{outcome.status === 'complete' ? `${number(outcome.table_count)} tables · verified` : `Blocked · ${(outcome.reason_code || 'Execution not verified').replaceAll('_', ' ').toLowerCase()}`}</span></li>)}</ul>
          {run.proof_ref && <p className="census-proof" data-testid={`census-run-proof-${run.census_run_id}`}>{run.proof_ref}</p>}
          {run.status === 'COMPLETE' && <button data-testid={`census-run-result-${run.census_run_id}`} className="census-button" onClick={() => openRecord({ record_id: run.census_run_id })}>View result <ArrowUpRight size={14} /></button>}
        </article>)}</section>}
      <CensusRunDialog open={runOpen} onClose={() => setRunOpen(false)} data={data} onQueued={() => { setParams({ tab: 'runs' }); reload(); }} />
      <CensusRecordDrawer recordId={params.get('record')} onClose={() => setParams({ tab: 'records' })} />
    </>}
  </div>;
};