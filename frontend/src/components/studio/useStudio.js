import { useCallback, useEffect, useState } from 'react';

export async function studioRequest(path, options = {}) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/studio${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  });
  const body = await response.json();
  if (!response.ok) {
    const error = new Error(typeof body.detail === 'string' ? body.detail : 'The studio could not complete this request.');
    error.status = response.status;
    throw error;
  }
  return body;
}

// Authenticated artefact fetch → Blob (downloads and the inline review page both need the bearer token).
export async function artifactBlob(commissionId, buildId, name) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/studio/commissions/${commissionId}/builds/${buildId}/artifact/${name}`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!response.ok) throw new Error('That artefact is not on record.');
  return response.blob();
}

export async function downloadArtifact(commissionId, buildId, name, downloadName = name) {
  const blob = await artifactBlob(commissionId, buildId, name);
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href: url, download: downloadName });
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

export function useStudio(signedIn, initialCommission) {
  const [state, setState] = useState({ skill: null, commissions: null, selected: null, commission: null, loading: false, busy: null, error: null, notice: null });
  const load = useCallback(async (selectId) => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const [skill, list] = await Promise.all([studioRequest('/skill'), studioRequest('/commissions')]);
      const id = selectId || initialCommission || list.commissions[0]?.commission_id || null;
      const detail = id ? await studioRequest(`/commissions/${id}`).catch(() => null) : null;
      setState(s => ({ ...s, skill, commissions: list.commissions, selected: detail ? id : null, commission: detail?.commission || null, loading: false }));
    } catch (error) {
      setState(s => ({ ...s, loading: false, error: error.message }));
    }
  }, [initialCommission]);
  useEffect(() => { if (signedIn) load(); }, [signedIn, load]);
  const select = useCallback(async id => {
    setState(s => ({ ...s, selected: id, loading: true, error: null }));
    try { const detail = await studioRequest(`/commissions/${id}`); setState(s => ({ ...s, commission: detail.commission, loading: false })); }
    catch (error) { setState(s => ({ ...s, loading: false, error: error.message })); }
  }, []);
  const act = useCallback(async (label, path, body) => {
    setState(s => ({ ...s, busy: label, error: null, notice: null }));
    try {
      const result = await studioRequest(path, { method: 'POST', body: JSON.stringify(body || {}) });
      const commission = result.commission;
      const list = await studioRequest('/commissions');
      setState(s => ({ ...s, busy: null, commissions: list.commissions, selected: commission.commission_id, commission, notice: `${label}: ${commission.release.state} — ${commission.release.reason}` }));
      return commission;
    } catch (error) {
      setState(s => ({ ...s, busy: null, error: error.message }));
      return null;
    }
  }, []);
  return { ...state, reload: load, select, act, fail: message => setState(s => ({ ...s, error: message, busy: null })) };
}

export const stamp = iso => (iso ? new Date(iso).toLocaleString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC' : 'not recorded');
export const short = sha => (sha ? `${sha.slice(0, 12)}…` : '—');
export const releaseClass = state => (state === 'clear' || state === 'released' || state === 'PASS' ? 'complete' : state === 'unbuilt' || state === 'declared' ? 'partial' : 'blocked');
