import { useCallback, useEffect, useState } from 'react';
import { apiRequest } from '../models/useModelApproval';

// ARMI reads: the tenant register and one operational profile at a time. Every lifecycle action re-reads the profile it changed.
export function useArmi(signedIn) {
  const [state, setState] = useState({ overview: null, agents: null, agent: null, selected: null, loading: false, busy: null, error: null, notice: null });
  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const [overview, agents] = await Promise.all([apiRequest('/api/armi/overview'), apiRequest('/api/armi/agents')]);
      setState(s => ({ ...s, overview, agents: agents.agents, loading: false }));
    } catch (error) { setState(s => ({ ...s, loading: false, error: error.message || 'The agent register could not be read.' })); }
  }, []);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const select = useCallback(async agentId => {
    if (!agentId) { setState(s => ({ ...s, selected: null, agent: null })); return; }
    setState(s => ({ ...s, selected: agentId, agent: s.agent?.agent_id === agentId ? s.agent : null, error: null }));
    try { const r = await apiRequest(`/api/armi/agents/${agentId}`); setState(s => (s.selected === agentId ? { ...s, agent: r.agent } : s)); }
    catch (error) { setState(s => ({ ...s, error: error.message })); }
  }, []);
  const act = useCallback(async (label, path, body, agentId) => {
    setState(s => ({ ...s, busy: label, error: null, notice: null }));
    try {
      const r = await apiRequest(path, { method: 'POST', body: JSON.stringify(body || {}) });
      const [overview, agents] = await Promise.all([apiRequest('/api/armi/overview'), apiRequest('/api/armi/agents')]);
      const agent = agentId ? (await apiRequest(`/api/armi/agents/${agentId}`)).agent : null;
      setState(s => ({ ...s, busy: null, overview, agents: agents.agents, agent: agent || s.agent, selected: agentId || s.selected, notice: `${label} recorded.` }));
      return r;
    } catch (error) { setState(s => ({ ...s, busy: null, error: error.message || `${label} could not be recorded.` })); return null; }
  }, []);
  return { ...state, reload: load, select, act, dismiss: () => setState(s => ({ ...s, notice: null, error: null })) };
}

export const pct = v => (v == null ? 'not measured' : `${Math.round(v * 1000) / 10}%`);
export const hoursLabel = h => (h == null ? 'not metered' : `${Math.round(h * 100) / 100} GPU-h`);
export const STATUS_TONE = { active: ['var(--sage)', 'rgba(29,122,110,.08)'], onboarded: ['var(--brass)', 'rgba(176,141,46,.09)'], suspended: ['#7e6418', 'rgba(176,141,46,.16)'], revoked: ['var(--oxblood)', 'rgba(184,57,91,.08)'] };
export const slug = id => String(id).replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase();
