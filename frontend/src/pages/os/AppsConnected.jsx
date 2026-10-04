/*
 * AppsConnected.jsx — v2 OS · Apps · Connected · LIVE (Context-as-a-Service, Mα MA-27/28).
 *
 * The supplied "Connected" list is bound to the estate's CaaS client register (/api/caas/*): every admitted client application, its licences,
 * keys, deliveries and metering. Operators admit clients, grant/supersede/revoke licences, issue keys (secret shown once) and revoke keys or
 * clients. The client side authenticates with its own key — no estate login — and receives derived, governed context only.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { readableText } from '@/components/shared/PresentationDetails';
import { useCaas, STATUS_TONE, slug } from '@/components/caas/useCaas';
import { CaasClient } from '@/components/caas/CaasClient';
import { CaasDeliveries, CaasMetering } from '@/components/caas/CaasMetering';
import { AdmitForm } from '@/components/caas/CaasForms';
import '@/components/estate/estate.css';

const TABS = [['new', 'New Apps'], ['frequent', 'Frequent Apps'], ['connected', 'Connected Apps'], ['requests', 'App Requests']];

function Products({ products }) {
  return <section className="estate-section" data-testid="caas-products" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Context products</h2><p>What a licence can cover. Aggregates are derived deterministically from native records; authored deliverables are planned by the frontier role from the licensed aggregates and the client brief only, then checked so that no figure outside the licensed context appears.</p></div></header>
    <div className="estate-products">{Object.entries(products || {}).map(([id, p], i) => <div className="estate-product" key={id} data-testid={`caas-product-${id.replace(/[^A-Za-z0-9]+/g, '-')}`}>
      <div className="estate-product-head"><span className="estate-rank">{i + 1}</span><span className="estate-product-title" style={{ minWidth: 0, overflowWrap: 'anywhere' }}>{p.title}</span><span className="estate-status">{p.kind}</span></div>
      <div className="estate-product-body"><small style={{ fontFamily: 'var(--mono)' }}>{id}</small><p style={{ margin: '6px 0 0' }}>{p.deliverable}</p>{p.sections && <small>sections · {p.sections.join(', ')}</small>}</div>
    </div>)}</div>
  </section>;
}

export default function AppsConnected() {
  const session = usePrototypeSession(), navigate = useNavigate();
  const canOperate = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const { overview, clients, client, selected, metering, deliveries, loading, busy, error, notice, secret, clearSecret, reload, select, act } = useCaas(Boolean(session.data));
  const [admitting, setAdmitting] = useState(false);
  const products = overview?.products;
  const banner = error || notice || (loading ? 'Reading the client register…' : '');
  const model = {
    isThirdpartyGroup: true, isAppsRequests: false, appsRequestOpen: false, appsRequestsView: [], hasSessionBanner: Boolean(banner), sessionBanner: readableText(banner), sessionBannerColor: error ? 'var(--oxblood)' : 'var(--ink3)',
    appsTabsView: TABS.map(([k, label]) => ({ key: k, label, border: k === 'connected' ? 'var(--accent)' : 'transparent', color: k === 'connected' ? 'var(--ink)' : 'var(--ink3)', onClick: () => navigate(`/os/apps/${k}`) })),
    appsListView: (clients || []).map(c => { const [connColor] = STATUS_TONE[c.status] || STATUS_TONE.superseded; return { key: slug(c.client_id), id: c.client_id, name: readableText(c.name), desc: c.application, connLabel: c.status, connColor, selected: selected === c.client_id, onOpen: () => select(selected === c.client_id ? null : c.client_id) }; }),
  };
  const on = (label, path, body, id) => act(label, path, body, id ?? selected);
  return <OwnerWorkspace session={session} title="Connected Apps" group="Apps" section="apps" model={model}
    enhance={{ 167: { 'data-testid': 'workspace-title' }, 8085: (c, props) => ({ ...props, 'data-testid': `apps-tab-${c.t.key}` }), 8091: (c, props) => ({ role: 'button', tabIndex: 0, 'data-testid': `caas-client-row-${c.ap.key}`, 'aria-pressed': c.ap.selected, onClick: c.ap.onOpen, onKeyDown: e => { if (['Enter', ' '].includes(e.key)) { e.preventDefault(); c.ap.onOpen(); } }, style: { ...props.style, cursor: 'pointer', borderColor: c.ap.selected ? 'var(--blue)' : undefined, background: c.ap.selected ? 'var(--surface)' : '#fff' } }) }}>
    <div className="estate" data-testid="caas-surface" style={{ maxWidth: 1180, marginTop: 24 }}>
      {session.data && clients && !clients.length && <p className="estate-note" data-testid="caas-clients-empty">No client application is connected yet.{canOperate ? ' Admit the first one below.' : ''}</p>}
      {overview && <section className="estate-section" data-testid="caas-overview">
        <header className="estate-head"><div><h2>Context as a Service</h2><p>External applications licensed to draw governed context from this estate. The raw estate stays under estate custody; clients receive derived aggregates and authored deliverables, metered before return, and withdrawn the moment a licence or client is revoked.</p></div>
          <div className="estate-actions" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button className="estate-btn" data-testid="caas-reload" onClick={reload} disabled={loading}>{loading ? 'Reading…' : 'Refresh'}</button>
            {canOperate && <button className="estate-btn primary" data-testid="caas-admit-open" onClick={() => setAdmitting(v => !v)}>{admitting ? 'Close' : 'Admit client'}</button>}
          </div></header>
        <div className="estate-tiles">
          <div className="estate-tile" data-testid="caas-overview-clients"><span className="estate-label">Clients</span><b>{overview.clients}</b><small>{overview.clients_by_status?.active ?? 0} active · {overview.clients_by_status?.suspended ?? 0} suspended · {overview.clients_by_status?.revoked ?? 0} revoked</small></div>
          <div className="estate-tile sage" data-testid="caas-overview-licences"><span className="estate-label">Licences</span><b>{overview.licences?.active ?? 0} active</b><small>{overview.licences?.superseded ?? 0} superseded · {overview.licences?.revoked ?? 0} revoked</small></div>
          <div className="estate-tile brass" data-testid="caas-overview-deliveries"><span className="estate-label">Deliveries</span><b>{overview.deliveries}</b><small>{overview.metered_events} metered events · {metering?.cost_usd == null ? 'no rate card, money not invented' : `$${metering.cost_usd}`}</small></div>
          <div className="estate-tile oxblood" data-testid="caas-overview-custody"><span className="estate-label">Custody</span><b>Raw estate never exported</b><small>{overview.custody?.frontier_exposure}</small></div>
        </div>
      </section>}
      {admitting && canOperate && <AdmitForm busy={busy} onCancel={() => setAdmitting(false)} onSubmit={async body => { const r = await on('Admission', '/api/caas/clients', body, null); if (r) { setAdmitting(false); select(r.client.client_id); } }} />}
      {selected && !client && !error && <p className="estate-note" data-testid="caas-client-loading">Reading the client…</p>}
      {client && <CaasClient client={client} products={products} canOperate={canOperate} busy={busy} secret={secret} clearSecret={clearSecret}
        onTransition={body => on(body.action[0].toUpperCase() + body.action.slice(1), `/api/caas/clients/${client.client_id}/transition`, body)}
        onGrant={body => on('Licence grant', `/api/caas/clients/${client.client_id}/licences`, body)}
        onIssueKey={licenceId => on('Key issue', `/api/caas/licences/${licenceId}/keys`, {})}
        onRevokeLicence={(licenceId, reason) => on('Licence revocation', `/api/caas/licences/${licenceId}/revoke`, { reason })}
        onRevokeKey={(keyId, reason) => on('Key revocation', `/api/caas/keys/${keyId}/revoke`, { reason })} />}
      {overview && <Products products={products} />}
      {deliveries && <CaasDeliveries deliveries={selected ? deliveries.filter(d => d.client_id === selected) : deliveries} products={products} clients={clients} />}
      {metering && <CaasMetering metering={metering} products={products} clients={clients} />}
      {!canOperate && session.data && <p className="estate-note" data-testid="caas-readonly-note">Admission, licensing and revocation need an admitted operator; this view is read-only for your role.</p>}
    </div>
  </OwnerWorkspace>;
}
