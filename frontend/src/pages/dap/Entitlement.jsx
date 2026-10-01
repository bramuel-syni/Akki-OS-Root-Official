import React, { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { useAuth } from '@/pages/dap/DAPLayout';
import { tryGet } from '@/lib/apiClient';
import { readableText } from '@/components/shared/PresentationDetails';
import '@/components/estate/estate.css';

const label = value => {
  if (value == null) return 'Not recorded';
  if (typeof value === 'object') return Object.entries(value).map(([k, v]) => `${k.replaceAll('_', ' ')}: ${label(v)}`).join(' · ');
  return readableText(value).replaceAll('_', ' ').replaceAll('.', ' · ');
};
const issue = (data, what) => data?.reason_code === 'PERIOD_UNRESOLVED' ? 'The billing period needs to be reconciled. Contact your account administrator.' : `${what} is not available. Contact your account administrator to review access.`;

function ReadState({ state, id, children }) {
  if (state.loading) return <p data-testid={`${id}-loading`}>Loading…</p>;
  if (state.error) return <p className="estate-alert" role="alert" data-testid={`${id}-error`}>Could not load this information. Refresh to try again.</p>;
  return children;
}

export default function Entitlement() {
  const { user } = useAuth();
  const [reads, setReads] = useState({}), [revision, setRevision] = useState(0);
  useEffect(() => {
    if (!user) return;
    let active = true;
    const paths = { licence: 'licence', allowance: 'allowance', catalog: 'catalog/listed', badges: 'badges' };
    setReads(Object.fromEntries(Object.keys(paths).map(key => [key, { loading: true }])));
    Object.entries(paths).forEach(([key, path]) => {
      tryGet(`/api/portal/entitlement/${path}`).then(res => { if (active) setReads(old => ({ ...old, [key]: { data: res.ok ? res.data : null, error: !res.ok, loading: false } })); }).catch(() => { if (active) setReads(old => ({ ...old, [key]: { error: true, loading: false } })); });
    });
    return () => { active = false; };
  }, [user, revision]);
  const state = key => reads[key] || { loading: true };
  const licence = reads.licence?.data?.licence, allowance = reads.allowance?.data?.allowance_state;
  const rows = reads.catalog?.data?.rows || [], badges = reads.badges?.data?.badges || [];
  return <main className="estate" data-testid="entitlement-page">
    <header className="estate-header"><div><div className="estate-crumb" data-testid="entitlement-breadcrumb">ACCOUNT</div><h1 className="estate-title" data-testid="entitlement-title">Entitlement</h1></div>
      {user && <button className="estate-btn" onClick={() => setRevision(v => v + 1)} disabled={Object.values(reads).some(s => s.loading)} data-testid="entitlement-refresh"><RefreshCw size={15} />Refresh</button>}</header>
    {!user ? <p data-testid="entitlement-signin-needed">Sign in to view your licence, credits and available services.</p> : <div className="estate-body">
      <div className="estate-columns"><section className="estate-section" data-testid="licence-card"><div className="estate-head"><h2>Licence</h2></div><ReadState state={state('licence')} id="licence">
        {licence ? <><p data-testid="licence-status">{label(licence.status)} · {label(licence.plan_identifier || licence.name || 'Licence on record')}</p>
          <dl className="entitlement-facts">{[['Seats', licence.seat_count], ['Compute', licence.compute_dial], ['External models', licence.frontier_dial], ['Renewal', licence.renewal_date ? new Date(licence.renewal_date).toLocaleDateString('en-GB') : null]].map(([key, value], i) => <div key={key}><dt>{key}</dt><dd data-testid={`licence-fact-${i}`}>{label(value)}</dd></div>)}</dl></> : <p data-testid="licence-empty">No licence on record. Ask your account administrator to confirm your access.</p>}
      </ReadState></section>
      <section className="estate-section" data-testid="allowance-card"><div className="estate-head"><h2>Credits</h2></div><ReadState state={state('allowance')} id="allowance">
        {allowance ? <dl className="entitlement-facts"><div><dt>Period</dt><dd data-testid="allowance-period">{allowance.period_iso}</dd></div><div><dt>Allowance</dt><dd data-testid="allowance-credits">{allowance.credits_allowance}</dd></div><div><dt>Used</dt><dd data-testid="allowance-used">{allowance.credits_debited}</dd></div></dl> : <p data-testid="allowance-unavailable">{issue(reads.allowance?.data, 'Credit information')}</p>}
      </ReadState></section></div>
      <section className="estate-section" data-testid="catalog-picker"><div className="estate-head"><h2>Available services</h2></div><ReadState state={state('catalog')} id="catalog">
        {rows.length ? <ul className="estate-list">{rows.map((row, i) => <li key={row.row_id || i} data-testid={`catalog-row-${i}`}><span><b>{readableText(row.name || `Service ${i + 1}`)}</b>{row.description && <small>{readableText(row.description)}</small>}</span>{row.badge && <span className="estate-status" data-testid={`catalog-row-badge-${i}`}>{row.badge}</span>}</li>)}</ul> : <p data-testid="catalog-empty">{issue(reads.catalog?.data, 'Services for this account')}</p>}
      </ReadState>
      {reads.badges?.error && <p className="estate-note" role="alert" data-testid="catalog-badges-error">Service pricing labels could not be loaded. Refresh to try again.</p>}
      {badges.length > 0 && <div className="estate-inline-facts" data-testid="catalog-badges">{badges.map((badge, i) => <span className="estate-status" key={i} data-testid={`catalog-badge-${i}`}>{badge.badge || badge.name || badge}</span>)}</div>}
      </section>
    </div>}
  </main>;
}