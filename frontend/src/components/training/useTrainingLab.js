import { useCallback, useEffect, useRef, useState } from 'react';

const ROOT = `${process.env.REACT_APP_BACKEND_URL}/api/training/lab`;

export async function labRequest(path, options = {}) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(`${ROOT}${path}`, { ...options, headers: { Authorization: `Bearer ${token}`, ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(options.headers || {}) } });
  if (!response.ok) {
    let detail = 'The training lab is unavailable right now.';
    try { const body = await response.json(); detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail); } catch { /* keep default */ }
    throw new Error(detail);
  }
  if (response.status === 204) return null;
  return response.json();
}

export function useTrainingLab(identity) {
  const [baselines, setBaselines] = useState([]), [corpus, setCorpus] = useState(null), [weak, setWeak] = useState(null), [plans, setPlans] = useState([]), [error, setError] = useState('');
  const alive = useRef(true);
  const reload = useCallback(async () => {
    if (!identity) return;
    const results = await Promise.allSettled([labRequest('/baselines/music'), labRequest('/corpus-measurements'), labRequest('/languages/weak'), labRequest('/languages/reinforcement')]);
    if (!alive.current) return;
    const [b, c, w, p] = results;
    if (b.status === 'fulfilled') setBaselines(b.value.runs); if (c.status === 'fulfilled') setCorpus(c.value.measurement);
    if (w.status === 'fulfilled') setWeak(w.value); if (p.status === 'fulfilled') setPlans(p.value.runs);
    const failed = results.find(r => r.status === 'rejected'); setError(failed ? failed.reason.message : '');
  }, [identity]);
  useEffect(() => { alive.current = true; setError(''); if (identity) reload(); return () => { alive.current = false; }; }, [identity, reload]);
  const busy = corpus?.status === 'running' || baselines.some(r => r.status === 'waiting_measurements') || plans.some(r => ['queued', 'reviewing'].includes(r.status));
  useEffect(() => { if (!busy) return undefined; const timer = setInterval(reload, 15000); return () => clearInterval(timer); }, [busy, reload]);
  const post = useCallback(async (path, body) => { const data = await labRequest(path, { method: 'POST', headers: { 'Idempotency-Key': crypto.randomUUID() }, body: JSON.stringify(body || {}) }); await reload(); return data; }, [reload]);
  return { baselines, corpus, weak, plans, error, reload, post, busy };
}

export const pct = (interval, digits = 0) => interval == null ? '—' : typeof interval === 'number' ? `${(interval * 100).toFixed(digits)}%` : `${(interval.estimate * 100).toFixed(digits)}% (${(interval.low * 100).toFixed(0)}–${(interval.high * 100).toFixed(0)})`;
