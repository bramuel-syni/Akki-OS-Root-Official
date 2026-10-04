import { useCallback, useEffect, useState } from 'react';
import { apiRequest } from '../models/useModelApproval';

// CaaS licensor reads: register, metering and deliveries together; one client profile at a time. Every action re-reads what it changed.
async function readAll() {
  const [overview, clients, metering, deliveries] = await Promise.all([apiRequest('/api/caas/overview'), apiRequest('/api/caas/clients'), apiRequest('/api/caas/metering'), apiRequest('/api/caas/deliveries')]);
  return { overview, clients: clients.clients, metering, deliveries: deliveries.deliveries };
}

export function useCaas(signedIn) {
  const [state, setState] = useState({ overview: null, clients: null, client: null, selected: null, metering: null, deliveries: null, loading: false, busy: null, error: null, notice: null, secret: null });
  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }));
    try { const r = await readAll(); setState(s => ({ ...s, ...r, loading: false })); }
    catch (error) { setState(s => ({ ...s, loading: false, error: error.message || 'The client register could not be read.' })); }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const select = useCallback(async clientId => {
    if (!clientId) { setState(s => ({ ...s, selected: null, client: null, secret: null })); return; }
    setState(s => ({ ...s, selected: clientId, client: s.client?.client_id === clientId ? s.client : null, secret: null, error: null }));
    try { const r = await apiRequest(`/api/caas/clients/${clientId}`); setState(s => (s.selected === clientId ? { ...s, client: r.client } : s)); }
    catch (error) { setState(s => ({ ...s, error: error.message })); }
  }, []);
  const act = useCallback(async (label, path, body, clientId) => {
    setState(s => ({ ...s, busy: label, error: null, notice: null }));
    try {
      const r = await apiRequest(path, { method: 'POST', body: JSON.stringify(body || {}) });
      const id = clientId || r.client?.client_id || r.licence?.client_id || r.key?.client_id || null;
      const [rest, client] = await Promise.all([readAll(), id ? apiRequest(`/api/caas/clients/${id}`).then(x => x.client) : null]);
      setState(s => ({ ...s, ...rest, busy: null, client: client || s.client, selected: id || s.selected, notice: `${label} recorded.`, secret: r.shown_once ? { key_id: r.key.key_id, secret: r.secret } : s.secret }));
      return r;
    } catch (error) { setState(s => ({ ...s, busy: null, error: error.message || `${label} could not be recorded.` })); return null; }
  }, []);
  const clearSecret = useCallback(() => setState(s => ({ ...s, secret: null })), []);
  return { ...state, reload: load, select, act, clearSecret };
}

export const STATUS_TONE = { active: ['var(--sage)', 'rgba(29,122,110,.08)'], suspended: ['#7e6418', 'rgba(176,141,46,.16)'], revoked: ['var(--oxblood)', 'rgba(184,57,91,.08)'], superseded: ['var(--ink3)', 'rgba(91,98,112,.12)'] };
export const slug = id => String(id).replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase();
export const productTitle = (products, id) => products?.[id]?.title || id;
