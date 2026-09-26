import { useCallback, useEffect, useRef, useState } from 'react';
import { tryGet, submitPortalRequest } from '@/lib/apiClient';

const errorText = response => typeof response.data?.detail === 'string' ? response.data.detail : `The record could not be verified (${response.status || 'connection unavailable'}).`;

export function useOperationalWork(principalId, surface, selectedId) {
  const [rows, setRows] = useState([]);
  const [entitlement, setEntitlement] = useState(null);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [version, setVersion] = useState(0);
  const key = useRef(null);
  const inFlight = useRef(false);
  const identity = useRef(principalId);
  identity.current = principalId;
  const reload = useCallback(() => setVersion(v => v + 1), []);
  useEffect(() => { key.current = null; }, [principalId]);
  useEffect(() => {
    let active = true;
    setRows([]); setSelected(null); setEntitlement(null); setError('');
    if (!principalId) return undefined;
    setLoading(true);
    const root = surface === 'os' ? '/api/os/work' : '/api/portal/requests';
    Promise.all([tryGet(root), tryGet('/api/portal/entitlement/allowance'), selectedId ? tryGet(`${root}/${encodeURIComponent(selectedId)}`) : Promise.resolve(null)])
      .then(([work, terms, detail]) => {
        if (!active) return;
        if (work.ok) setRows(work.data.rows); else setError(errorText(work));
        if (terms.ok) setEntitlement(terms.data); else setError(errorText(terms));
        if (detail?.ok) setSelected(detail.data); else if (detail) setError(errorText(detail));
        setLoading(false);
      });
    return () => { active = false; };
  }, [principalId, surface, selectedId, version]);
  const submit = async body => {
    if (inFlight.current || !principalId) return null;
    const frozen = JSON.stringify(body);
    if (key.current?.body !== frozen) key.current = { body: frozen, value: crypto.randomUUID() };
    inFlight.current = true; setBusy(true); setError('');
    try {
      const response = await submitPortalRequest({ ...body, idempotency_key: key.current.value });
      if (identity.current !== principalId) return null;
      if (!response.ok) { setError(errorText(response)); return null; }
      reload();
      return response.data;
    } finally { inFlight.current = false; setBusy(false); }
  };
  return { rows, selected, entitlement, loading, busy, error, setError, reload, submit,
    resetKey: () => { if (!inFlight.current) key.current = null; } };
}