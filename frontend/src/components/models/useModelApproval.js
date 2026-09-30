import { useCallback, useEffect, useState } from 'react';

export async function apiRequest(path, options = {}) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  });
  const body = await response.json();
  if (!response.ok) {
    const error = new Error(typeof body.detail === 'string' ? body.detail : 'The model service could not complete this request.');
    error.status = response.status;
    throw error;
  }
  return body;
}

// One read per visit: registry, capability account, drill receipts and the ratified recovery policy are all banked records.
export function useModelApproval(signedIn) {
  const [state, setState] = useState({ models: null, capabilities: null, drills: null, policy: null, readjudications: null, loading: false, error: null, health: {}, checking: null });
  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const [models, capabilities, drills, policy, readjudications] = await Promise.all([
        apiRequest('/api/training/m9/models'), apiRequest('/api/training/m9/capabilities'), apiRequest('/api/continuity/drills'),
        apiRequest('/api/continuity/policy'), apiRequest('/api/training/m9/readjudications'),
      ]);
      setState(s => ({ ...s, models, capabilities, drills: drills.receipts, policy, readjudications: readjudications.records, loading: false }));
    } catch (error) {
      setState(s => ({ ...s, loading: false, error: error.message || 'The model records could not be read.' }));
    }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const checkHealth = useCallback(async modelId => {
    setState(s => ({ ...s, checking: modelId }));
    try {
      const result = await apiRequest(`/api/training/m9/serving/${modelId}/health`);
      setState(s => ({ ...s, checking: null, health: { ...s.health, [modelId]: result } }));
    } catch (error) {
      setState(s => ({ ...s, checking: null, health: { ...s.health, [modelId]: { status: 'unreachable', error: error.message } } }));
    }
  }, []);
  return { ...state, reload: load, checkHealth };
}

export const short = sha => (sha ? `${sha.slice(0, 12)}…` : '—');
export const stamp = iso => (iso ? new Date(iso).toLocaleString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC' : 'not recorded');
export const statusClass = status => (['admitted', 'serving', 'PASS', 'matches'].includes(status) ? 'complete' : ['recalled', 'withdrawn', 'refused', 'FAIL', 'diverges', 'revoked'].includes(status) ? 'blocked' : 'partial');
