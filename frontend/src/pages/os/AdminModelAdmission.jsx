/*
 * AdminModelAdmission.jsx — v2 OS · admin tab · APPROVALS Model Approval leaf · LIVE.
 *
 * Registry of trained adapters with their admission on record, re-adjudication decisions under the owner's
 * per-stratum ruling, the G9 capability account, and the M8 failure/recovery drill receipts against the ratified
 * recovery tiers. Everything is read from banked records under /api/training/m9/* and /api/continuity/*;
 * the only live action is a health read against a served model.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { ModelRegistry, modelName } from '@/components/models/ModelRegistry';
import { ModelAdmissions, ModelCapabilities } from '@/components/models/ModelAdmissions';
import { useModelApproval, stamp } from '@/components/models/useModelApproval';
import { PresentationDetails, readableText } from '@/components/shared/PresentationDetails';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import '@/components/census/census.css';
import '@/components/estate/estate.css';

export default function AdminModelAdmission() {
  const session = usePrototypeSession();
  const navigate = useNavigate();
  const [evaluation, setEvaluation] = useState(null);
  const signedIn = Boolean(session.data);
  const { models, capabilities, drills, policy, readjudications, loading, error, health, checking, reload, checkHealth } = useModelApproval(signedIn);
  const adapters = models?.trained_adapters || [];
  const served = adapters.filter(m => m.serving?.status === 'running').length;
  const loaded = Boolean(models || capabilities || drills || policy || readjudications);
  const records = readjudications || [];
  const jobs = [...new Set(records.map(r => r.job_id))];
  const model = { isApprovalsGroup: true, approvalsTitle: 'Model Approval', approvalsOneliner: capabilities?.as_of ? `Updated ${stamp(capabilities.as_of)}` : '',
    hasSessionBanner: Boolean(error || loading), sessionBanner: error ? 'Some model records could not be loaded. Refresh to try again.' : 'Loading model records…', sessionBannerColor: error ? 'var(--oxblood)' : 'var(--ink3)',
    approvalsTilesView: [['Spend Requests', '/os/admin/spendreq'], ['Rules Updates', '/os/admin/rulesupd'], ['Model Approval', '/os/admin/modeladmission']].map(([label, path]) => ({ key: path, label, border: label === 'Model Approval' ? 'var(--blue)' : 'var(--line)', bg: label === 'Model Approval' ? 'var(--blue)' : '#fff', color: label === 'Model Approval' ? '#fff' : 'var(--ink2)', onClick: () => navigate(path) })),
    approvalsStats: [{ v: models ? adapters.length : '—', l: 'registered models' }, { v: models ? served : '—', l: 'serving' }, { v: readjudications ? records.length : '—', l: 'recorded evaluations' }, { v: capabilities ? capabilities.activated.length : '—', l: 'active capabilities' }],
    approvalsRows: records.map((r, i) => { const m = adapters.find(a => a.model_id === r.model_id); const failed = Object.values(r.per_stratum || {}).filter(s => !s.passes).length; return { key: `${r.model_id}-${i}`, text: `${m ? modelName(m) : `Language candidate ${jobs.indexOf(r.job_id) + 1}`} · ${r.variant === 'pruned' ? 'Reduced' : 'Full'}`, state: r.readjudicated?.outcome || 'Not decided', stateColor: r.readjudicated?.outcome === 'admitted' ? 'var(--sage)' : 'var(--oxblood)', stateBg: r.readjudicated?.outcome === 'admitted' ? 'rgba(29,122,110,.08)' : 'rgba(184,57,91,.08)', meta: `${stamp(r.at)} · ${failed ? `${failed} language${failed === 1 ? ' needs' : 's need'} improvement before resubmission.` : readableText(r.readjudicated?.refusal_note || 'Evaluation checks passed. Serving is managed separately.')}`, onApprove: () => { setEvaluation(r); requestAnimationFrame(() => document.querySelector('[data-testid="models-evaluation-detail"]')?.scrollIntoView({ block: 'nearest' })); } }; }) };
  return <OwnerWorkspace session={session} title="Model Approval" group="Approvals" section="approvals" model={model} returnTo="/os?nav=admin" replace={{ 4307: records.length ? 'Recorded evaluation decisions' : 'No evaluation decisions recorded', 4316: 'View evaluation' }} enhance={{ 4317: { hidden: true }, 4296: { 'data-testid': 'admin-modeladmission-title' }, 4316: c => ({ 'data-testid': `models-view-evaluation-${c.rw.key}` }) }}><div className="estate" data-testid="admin-modeladmission-surface" style={{ maxWidth: 1180, marginTop: 24 }}>
      <button className="estate-btn" onClick={reload} disabled={loading} data-testid="admin-modeladmission-reload">{loading ? 'Refreshing…' : 'Refresh records'}</button>
      {evaluation && <div data-testid="models-evaluation-detail"><ModelAdmissions records={[evaluation]} models={models} /><button className="estate-btn" data-testid="models-close-evaluation" onClick={() => setEvaluation(null)}>Close evaluation</button></div>}
      {loaded && <>
        <ModelRegistry models={models} health={health} checking={checking} onCheck={checkHealth} />
        <PresentationDetails id="models-capabilities" title="Capabilities & activation requirements"><ModelCapabilities capabilities={capabilities} /></PresentationDetails>
      </>}
  </div></OwnerWorkspace>;
}
