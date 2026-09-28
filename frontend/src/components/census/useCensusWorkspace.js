import { useCallback, useEffect, useRef, useState } from 'react';

export async function censusRequest(path, options = {}) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portal/census${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  });
  const body = await response.json();
  if (!response.ok) {
    const error = new Error(typeof body.detail === 'string' ? body.detail : 'The census service could not complete this request.');
    error.status = response.status;
    throw error;
  }
  return body;
}

export function useCensusWorkspace() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const pendingRead = useRef(null);
  const reload = useCallback(async () => {
    if(pendingRead.current && !pendingRead.current.signal.aborted && pendingRead.current.token === sessionStorage.getItem('akki_access_token')) return;
    pendingRead.current?.abort();
    const controller = new AbortController();
    pendingRead.current = controller;
    const token = sessionStorage.getItem('akki_access_token');
    controller.token = token;
    if (!token) {
      setData(null);
      setError(Object.assign(new Error('Sign in to view your admitted estate.'), { status: 401 }));
      setLoading(false);
      pendingRead.current=null;
      return;
    }
    const current = () => !controller.signal.aborted && sessionStorage.getItem('akki_access_token') === token;
    setLoading(true);
    try {
      const overview = await censusRequest('/overview', { signal: controller.signal });
      if (current()) { setData(overview); setError(null); }
    } catch (e) { if (current()) { setError(e); setData(null); } }
    finally { if (current()) setLoading(false); if(pendingRead.current===controller)pendingRead.current=null; }
  }, []);
  useEffect(() => {
    reload();
    window.addEventListener('akki-session-changed', reload);
    return () => { pendingRead.current?.abort(); window.removeEventListener('akki-session-changed', reload); };
  }, [reload]);
  // Read-only polling of actual in-flight work, never a timer-driven completion.
  const pending = data?.runs?.some(r => r.status === 'PENDING');
  useEffect(() => {
    if (!pending) return undefined;
    const timer = setInterval(reload, 3000);
    return () => clearInterval(timer);
  }, [pending, reload]);
  return { data, error, loading, reload };
}

export const number = value => value == null ? 'Not measured' : new Intl.NumberFormat('en').format(value);
export const date = value => {
  if (!value) return 'Not recorded';
  const normalized = value.replace(/^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z$/, '$1-$2-$3T$4:$5:$6Z');
  return Number.isNaN(Date.parse(normalized)) ? 'Timestamp not verified' : new Date(normalized).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC' }) + ' UTC';
};