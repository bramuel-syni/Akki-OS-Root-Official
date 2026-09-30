/*
 * AdminModelAdmission.jsx — v2 OS · admin tab · APPROVALS Model Approval leaf · LIVE.
 *
 * Registry of trained adapters with their admission on record, re-adjudication decisions under the owner's
 * per-stratum ruling, the G9 capability account, and the M8 failure/recovery drill receipts against the ratified
 * recovery tiers. Everything is read from banked records under /api/training/m9/* and /api/continuity/*;
 * the only live action is a health read against a served model.
 */
import React from 'react';
import { CensusAccess } from '@/components/census/CensusAccess';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { ModelRegistry } from '@/components/models/ModelRegistry';
import { ModelAdmissions, ModelCapabilities } from '@/components/models/ModelAdmissions';
import { RecoveryDrills } from '@/components/models/RecoveryDrills';
import { useModelApproval, stamp } from '@/components/models/useModelApproval';
import '@/components/census/census.css';
import '@/components/estate/estate.css';

export default function AdminModelAdmission() {
  const session = usePrototypeSession();
  const signedIn = Boolean(session.data);
  const { models, capabilities, drills, policy, readjudications, loading, error, health, checking, reload, checkHealth } = useModelApproval(signedIn);
  const adapters = models?.trained_adapters || [];
  const served = adapters.filter(m => m.serving?.status === 'running').length;
  const loaded = Boolean(models || capabilities || drills || policy || readjudications);
  return <div className="estate" data-testid="admin-modeladmission-surface">
    <header className="estate-header">
      <div>
        <div className="estate-crumb" data-testid="admin-modeladmission-breadcrumb">APPROVALS · Model Approval{models?.tenant_id ? ` · ${models.tenant_id}` : ''}</div>
        <h1 className="estate-title" data-testid="admin-modeladmission-title">Model Approval</h1>
        <p className="estate-lead" data-testid="admin-modeladmission-lead">New models seeking admission. Each carries its evaluation, its lineage, its declared purpose and the authority admitting it — and, once admitted, the evidence that it survives failure, withdrawal and recovery without losing the Ledger.</p>
        {models && <div className="estate-meta" data-testid="admin-modeladmission-meta"><span>registry <code>{models.registry_version}</code></span><span>{adapters.length} admitted adapter{adapters.length === 1 ? '' : 's'}</span><span>{served} served</span><span>{(drills || []).length} drill receipt{(drills || []).length === 1 ? '' : 's'}</span>{capabilities?.as_of && <span>capability account {stamp(capabilities.as_of)}</span>}</div>}
      </div>
      {signedIn && <div className="estate-actions">
        <button className="estate-btn" onClick={reload} disabled={loading} data-testid="admin-modeladmission-reload">{loading ? 'Reading…' : 'Re-read records'}</button>
      </div>}
    </header>
    {!signedIn && <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />}
    {signedIn && <div className="estate-body">
      {error && <p className="estate-alert" role="alert" data-testid="admin-modeladmission-error">{error}</p>}
      {!loaded && loading && <div className="estate-empty" data-testid="admin-modeladmission-loading">Reading the registry, admission records, capability account and drill receipts…</div>}
      {loaded && <>
        <ModelRegistry models={models} health={health} checking={checking} onCheck={checkHealth} />
        <ModelAdmissions records={readjudications} />
        <ModelCapabilities capabilities={capabilities} />
        <RecoveryDrills drills={drills} policy={policy} />
      </>}
    </div>}
  </div>;
}
