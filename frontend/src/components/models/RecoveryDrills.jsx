import React from 'react';
import { stamp, statusClass } from './useModelApproval';
import { readableText } from '../shared/PresentationDetails';

function measure(r) {
  const m = r.measured || {};
  if (m.work_lost_steps != null) return `${m.work_lost_steps} steps ≈ ${m.work_lost_seconds}s lost · RPO ${m.rpo_bound_seconds}s · five carriers ${m.five_carriers_restored ? 'restored' : 'NOT restored'}`;
  if (m.restore_seconds != null) return `${r.integrity_checks?.row_count_restored?.toLocaleString('en-GB')} rows restored in ${m.restore_seconds}s · chain ${r.integrity_checks?.chain_intact ? 'intact' : 'BROKEN'} · ${m.committed_rows_after_archive_total} rows committed after archive · countersigned ${r.countersign?.verified_in_e1 ? 'and verified' : 'NOT verified'}`;
  if (r.phases) return `outage probes refused: ${Object.values(r.phases.outage?.probes || {}).map(p => p.code ?? 'no reply').join(', ')} · head unchanged ${r.phases.recovery?.head_unchanged_by_outage ? 'yes' : 'NO'} · recovery ${r.phases.recovery?.seconds_to_ledger_read}s`;
  return '';
}

export function RecoveryDrills({ drills, policy }) {
  const rows = drills || [];
  const tiers = policy?.tiers ? Object.entries(policy.tiers) : [];
  return <section className="estate-section" data-testid="models-recovery">
    <div className="estate-head"><div><h2>Recovery checks</h2></div>
      {policy && <span className="estate-status" data-testid="models-policy-ref">tiers ratified · 2026-09-30</span>}</div>
    {!rows.length && <div className="estate-note" data-testid="models-recovery-empty">No drill receipt on record.</div>}
    {rows.length > 0 && <ul className="estate-list" data-testid="models-drill-list">{rows.slice().reverse().map((r, i) => <li key={r.receipt_path} data-testid={`models-drill-row-${i}`}><span><b>{readableText(r.drill)}</b><small>{measure(r)}</small><small>{stamp(r.at)}</small></span><small><span className={`estate-status ${statusClass(r.verdict)}`}>{r.verdict || 'recorded'}</span></small></li>)}</ul>}
    {tiers.length > 0 && <>
      <h3>Ratified recovery tiers</h3>
      <div className="estate-tiles" data-testid="models-tiers">{tiers.map(([key, t]) => <div key={key} className={`estate-tile ${key.includes('tier_4') ? 'brass' : 'sage'}`} data-testid={`models-tier-${key}`}>
        <b>{t.rpo?.statement || `${t.rpo?.value_seconds}s`}</b>
        <small>{t.asset_class}</small>
        <small>RTO {t.rto?.same_host_seconds ? `${t.rto.same_host_seconds}s same host · ${t.rto.lost_host_seconds}s lost host` : t.rto?.seconds ? `${t.rto.seconds}s` : t.rto?.statement}{t.regime ? ` · ${t.regime}` : ''}</small>
        {t.standby_site && <small>{t.standby_site}</small>}
      </div>)}</div>
      {policy?.deferred_by_owner && <ul className="estate-legend" style={{ marginTop: 12 }} data-testid="models-deferred">{Object.entries(policy.deferred_by_owner).map(([k, v]) => <li key={k}><i style={{ background: 'var(--brass)' }} />{k}<small>{v}</small></li>)}</ul>}
    </>}
  </section>;
}
