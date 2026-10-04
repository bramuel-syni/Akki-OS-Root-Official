import React, { useState } from 'react';
import { stamp } from '../models/useModelApproval';
import { readableText } from '../shared/PresentationDetails';
import { STATUS_TONE, productTitle } from './useCaas';
import { GrantForm, ReasonForm, TransitionForm } from './CaasForms';

const Status = ({ id, status }) => { const [color, bg] = STATUS_TONE[status] || STATUS_TONE.superseded; return <span className="estate-status" data-testid={id} style={{ background: bg, color }}>{status}</span>; };
const Tile = ({ id, label, value, note, tone }) => <div className={`estate-tile${tone ? ` ${tone}` : ''}`} data-testid={`caas-tile-${id}`}><span className="estate-label">{label}</span><b>{value}</b><small>{note}</small></div>;

function SecretOnce({ secret, onClose }) {
  const [copied, setCopied] = useState(false);
  return <div className="estate-alert" data-testid="caas-secret-once" style={{ borderColor: 'var(--brass)', background: 'rgba(176,141,46,.07)', marginTop: 12 }}>
    <b>Key {secret.key_id} issued — the secret is shown once and is not stored in clear.</b>
    <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', marginTop: 6 }}>
      <code data-testid="caas-secret-value" style={{ fontFamily: 'var(--mono)', fontSize: 12, overflowWrap: 'anywhere' }}>{secret.secret}</code>
      <button type="button" className="estate-btn" data-testid="caas-secret-copy" onClick={() => { navigator.clipboard?.writeText(secret.secret); setCopied(true); }}>{copied ? 'Copied' : 'Copy'}</button>
      <button type="button" className="estate-btn" data-testid="caas-secret-dismiss" onClick={onClose}>I have stored it</button>
    </div>
    <small style={{ display: 'block', marginTop: 6 }}>The client application sends it as <code>X-CaaS-Key</code> to <code>GET /api/caas/client/licence</code>, <code>POST /api/caas/client/deliver</code> and <code>GET /api/caas/client/deliveries</code>. No estate login is involved.</small>
  </div>;
}

function Licences({ client, products, canOperate, busy, form, setForm, onIssueKey, onRevokeLicence }) {
  const rows = client.licences || [];
  if (!rows.length) return <p className="estate-note" data-testid="caas-licences-empty">No licence granted yet; the client has no access.</p>;
  return <div className="estate-table-wrap"><table className="estate-table" data-testid="caas-licences-table">
    <thead><tr><th>Licence · purpose</th><th>State</th><th>Products</th><th>Allowance</th><th>Terms</th>{canOperate && <th />}</tr></thead>
    <tbody>{rows.map(l => <tr key={l.licence_id} data-testid={`caas-licence-row-${l.licence_id}`}>
      <td data-label="Licence · purpose" style={{ whiteSpace: 'normal', maxWidth: 320 }}><b>{l.licence_id}</b><small>{l.terms.purpose}</small><small>granted {stamp(l.issued_at)}{l.supersedes ? ` · supersedes ${l.supersedes}` : ''}</small></td>
      <td data-label="State"><Status id={`caas-licence-status-${l.licence_id}`} status={l.status} />{l.retired_reason && <small>{l.retired_reason}</small>}</td>
      <td data-label="Products" style={{ whiteSpace: 'normal' }}><small>{l.terms.products.map(p => productTitle(products, p)).join(' · ')}</small></td>
      <td data-label="Allowance">{l.terms.allowance.deliveries_per_period}<small>per {l.terms.allowance.period}</small></td>
      <td data-label="Terms" style={{ whiteSpace: 'normal' }}><small style={{ fontFamily: 'var(--mono)', overflowWrap: 'anywhere' }}>{l.terms_identifier}</small><small>{l.terms.frontier_exposure}</small></td>
      {canOperate && <td data-label="Actions">{l.status === 'active' && <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        <button className="estate-btn primary" data-testid={`caas-issue-key-${l.licence_id}`} disabled={Boolean(busy)} onClick={() => onIssueKey(l.licence_id)}>Issue key</button>
        <button className="estate-btn" data-testid={`caas-revoke-licence-${l.licence_id}`} disabled={Boolean(busy)} onClick={() => setForm(form?.id === l.licence_id ? null : { kind: 'revoke_licence', id: l.licence_id })}>Revoke</button>
      </div>}</td>}
    </tr>)}</tbody>
  </table>{form?.kind === 'revoke_licence' && <ReasonForm id="revoke-licence" title={`Why licence ${form.id} is withdrawn (keys stop at once; memory is frozen)`} label="Revoke licence" busy={busy} onCancel={() => setForm(null)} onSubmit={async reason => { if (await onRevokeLicence(form.id, reason)) setForm(null); }} />}</div>;
}

function Keys({ client, canOperate, busy, form, setForm, onRevokeKey }) {
  const rows = client.keys || [];
  if (!rows.length) return <p className="estate-note" data-testid="caas-keys-empty">No key issued.</p>;
  return <div className="estate-table-wrap"><table className="estate-table" data-testid="caas-keys-table">
    <thead><tr><th>Key</th><th>State</th><th>Licence</th><th>Issued</th><th>Use</th>{canOperate && <th />}</tr></thead>
    <tbody>{rows.map(k => <tr key={k.key_id} data-testid={`caas-key-row-${k.key_id}`}>
      <td data-label="Key"><b>{k.key_id}</b></td><td data-label="State" style={{ whiteSpace: 'normal' }}><Status id={`caas-key-status-${k.key_id}`} status={k.status} />{k.revoked_reason && <small>{k.revoked_reason}</small>}</td>
      <td data-label="Licence"><small>{k.licence_id}</small></td><td data-label="Issued"><small>{stamp(k.issued_at)}</small></td>
      <td data-label="Use">{k.uses || 0}<small>{k.last_used_at ? `last ${stamp(k.last_used_at)}` : 'never used'}</small></td>
      {canOperate && <td data-label="Actions">{k.status === 'active' && <button className="estate-btn" data-testid={`caas-revoke-key-${k.key_id}`} disabled={Boolean(busy)} onClick={() => setForm(form?.id === k.key_id ? null : { kind: 'revoke_key', id: k.key_id })}>Revoke</button>}</td>}
    </tr>)}</tbody>
  </table>{form?.kind === 'revoke_key' && <ReasonForm id="revoke-key" title={`Why key ${form.id} is withdrawn`} label="Revoke key" busy={busy} onCancel={() => setForm(null)} onSubmit={async reason => { if (await onRevokeKey(form.id, reason)) setForm(null); }} />}</div>;
}

export function CaasClient({ client, products, canOperate, busy, secret, clearSecret, onTransition, onGrant, onIssueKey, onRevokeLicence, onRevokeKey }) {
  const [form, setForm] = useState(null);
  const lic = client.licences || [], keys = client.keys || [];
  const transitions = client.status === 'revoked' ? [] : [client.status === 'active' ? ['suspend', 'Suspend'] : ['reinstate', 'Reinstate'], ['revoke', 'Revoke client']];
  return <section className="estate-section" data-testid="caas-client" style={{ marginTop: 16 }}>
    <header className="estate-head"><div>
      <span className="estate-label">client · {client.client_id}</span>
      <h2 data-testid="caas-client-name">{readableText(client.name)}</h2>
      <p data-testid="caas-client-application">{client.application}{client.contact ? ` · ${client.contact}` : ''}</p>
    </div><div style={{ textAlign: 'right' }}>
      <Status id="caas-client-status" status={client.status} />
      <div className="estate-meta" style={{ justifyContent: 'flex-end' }}><span>admitted {stamp(client.admitted_at)}</span></div>
    </div></header>
    <div className="estate-tiles">
      <Tile id="licences" label="Licences" value={`${lic.filter(l => l.status === 'active').length} active`} note={`${lic.filter(l => l.status === 'superseded').length} superseded · ${lic.filter(l => l.status === 'revoked').length} revoked`} tone="sage" />
      <Tile id="keys" label="Keys" value={`${keys.filter(k => k.status === 'active').length} active`} note={`${keys.filter(k => k.status === 'revoked').length} revoked · ${keys.reduce((n, k) => n + (k.uses || 0), 0)} uses`} />
      <Tile id="deliveries" label="Deliveries" value={String(client.deliveries ?? 0)} note="metered before return; derived context only" tone="brass" />
      <Tile id="custody" label="Raw estate exported" value="never" note="Mode B — licensed aggregates and the client brief only" tone="oxblood" />
    </div>
    {secret && <SecretOnce secret={secret} onClose={clearSecret} />}
    <h3>Licences</h3>
    <Licences client={client} products={products} canOperate={canOperate} busy={busy} form={form} setForm={setForm} onIssueKey={onIssueKey} onRevokeLicence={onRevokeLicence} />
    <h3>Keys</h3>
    <Keys client={client} canOperate={canOperate} busy={busy} form={form} setForm={setForm} onRevokeKey={onRevokeKey} />
    {canOperate && <div style={{ marginTop: 18 }}>
      <div className="estate-actions" data-testid="caas-client-actions" style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {client.status === 'active' && <button className="estate-btn primary" data-testid="caas-action-grant" onClick={() => setForm(form?.kind === 'grant' ? null : { kind: 'grant' })} disabled={Boolean(busy)}>Grant licence</button>}
        {transitions.map(([a, label]) => <button key={a} className="estate-btn" data-testid={`caas-action-${a}`} onClick={() => setForm(form?.kind === a ? null : { kind: a })} disabled={Boolean(busy)}>{label}</button>)}
        {client.status === 'revoked' && <span className="estate-note" style={{ margin: 0 }} data-testid="caas-revoked-note">A revoked client cannot change state; admit a new client identity.</span>}
      </div>
      {form?.kind === 'grant' && <GrantForm products={products} licences={lic} busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onGrant(body)) setForm(null); }} />}
      {['suspend', 'reinstate', 'revoke'].includes(form?.kind) && <TransitionForm action={form.kind} busy={busy} onCancel={() => setForm(null)} onSubmit={async body => { if (await onTransition(body)) setForm(null); }} />}
    </div>}
    <h3>Lifecycle record</h3>
    <ul className="estate-list" data-testid="caas-lifecycle">{(client.lifecycle || []).slice().reverse().map((e, i) => <li key={i}><span><b>{e.action}</b>{e.note ? ` — ${e.note}` : ''}</span><small>{stamp(e.at)} · {readableText(String(e.by))}</small></li>)}</ul>
  </section>;
}
