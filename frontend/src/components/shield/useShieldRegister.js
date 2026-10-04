import { useCallback, useEffect, useState } from 'react';
import { apiRequest } from '../models/useModelApproval';

// Shield register reads and DPO acts. Every act re-reads the register; values of protected spans never come back from the API.
export function useShieldRegister(signedIn) {
  const [state, setState] = useState({ register: null, crossings: null, loading: false, busy: null, error: null, notice: null, forbidden: false, preview: null });
  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const [register, crossings] = await Promise.all([apiRequest('/api/shield/register?include_removed=true&include_drafts=true'), apiRequest('/api/shield/crossings?limit=40')]);
      setState(s => ({ ...s, register, crossings, loading: false, forbidden: false }));
    } catch (error) { setState(s => ({ ...s, loading: false, forbidden: error.status === 403, error: error.status === 403 ? null : error.message || 'The register could not be read.' })); }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const act = useCallback(async (label, path, body, method = 'POST') => {
    setState(s => ({ ...s, busy: label, error: null, notice: null }));
    try {
      const r = await apiRequest(path, { method, ...(body !== undefined ? { body: JSON.stringify(body) } : {}) });
      const register = await apiRequest('/api/shield/register?include_removed=true&include_drafts=true');
      setState(s => ({ ...s, busy: null, register, notice: `${label} recorded.` }));
      return r;
    } catch (error) { setState(s => ({ ...s, busy: null, error: error.message || `${label} could not be recorded.` })); return null; }
  }, []);
  const test = useCallback(async text => {
    setState(s => ({ ...s, busy: 'Test', error: null, preview: null }));
    try {
      const [classify, reconstruct] = await Promise.all([apiRequest('/api/shield/classify', { method: 'POST', body: JSON.stringify({ text }) }), apiRequest('/api/shield/reconstruct', { method: 'POST', body: JSON.stringify({ text, mode: 'abstract' }) })]);
      setState(s => ({ ...s, busy: null, preview: { classify, reconstruct } }));
    } catch (error) { setState(s => ({ ...s, busy: null, error: error.message })); }
  }, []);
  return { ...state, reload: load, act, test, clearPreview: () => setState(s => ({ ...s, preview: null })) };
}

export const KIND_LABEL = { exact: 'By name', pattern: 'By pattern', contextual: 'By context' };
export const ENFORCEMENT_LABEL = { enforced: 'enforced on every crossing', advisory: 'advisory · receipted, enforced in confidential workflows' };
export const TONE = { active: ['var(--sage)', 'rgba(29,122,110,.08)'], draft: ['var(--brass)', 'rgba(176,141,46,.09)'], removed: ['var(--oxblood)', 'rgba(184,57,91,.08)'], superseded: ['var(--ink3)', 'var(--surface2)'] };
