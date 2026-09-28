import { useCallback, useEffect, useRef, useState } from 'react';
import { tryGet, submitPortalRequest } from '@/lib/apiClient';

const errorText = response => typeof response.data?.detail === 'string' ? response.data.detail :
  typeof response.data?.detail?.reason === 'string' ? response.data.detail.reason : `The record could not be verified (${response.status || 'connection unavailable'}).`;

export function useOperationalWork(principalId, surface, selectedId) {
  const [rows, setRows] = useState([]);
  const [entitlement, setEntitlement] = useState(null);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState('');
  const [rowsOwner, setRowsOwner] = useState(null);
  const [recordsAvailable, setRecordsAvailable] = useState(false);
  const [detailOwner, setDetailOwner] = useState(null);
  const [loadedId, setLoadedId] = useState(null);
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
    setError('');
    if (!principalId) { setRows([]); setRowsOwner(null); setRecordsAvailable(false); setEntitlement(null); setLoading(false); return undefined; }
    setLoading(true);
    const root = surface === 'os' ? '/api/os/work' : '/api/portal/requests';
    Promise.all([tryGet(root), tryGet('/api/portal/entitlement/allowance')])
      .then(([work, terms]) => {
        if (!active) return;
        setRowsOwner(principalId);
        setRecordsAvailable(work.ok && Array.isArray(work.data?.rows));
        if (work.ok && Array.isArray(work.data?.rows)) setRows(work.data.rows); else { setRows([]); setError(errorText(work)); }
        if (terms.ok) setEntitlement(terms.data); else { setEntitlement(null); setError(errorText(terms)); }
        setLoading(false);
      });
    return () => { active = false; };
  }, [principalId, surface, version]);
  useEffect(() => {
    let active = true;
    setSelected(null); setDetailError(''); setDetailOwner(null); setLoadedId(null);
    if (!principalId || !selectedId) { setDetailLoading(false); return undefined; }
    setDetailLoading(true);
    const root = surface === 'os' ? '/api/os/work' : '/api/portal/requests';
    tryGet(`${root}/${encodeURIComponent(selectedId)}`).then(response => {
      if (!active) return;
      setDetailOwner(principalId); setLoadedId(selectedId);
      if (response.ok) setSelected(response.data); else setDetailError(errorText(response));
      setDetailLoading(false);
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
  return { rows: rowsOwner === principalId ? rows : [], selected: detailOwner === principalId && loadedId === selectedId ? selected : null,
    entitlement: rowsOwner === principalId ? entitlement : null, recordsAvailable: Boolean(principalId && rowsOwner === principalId && recordsAvailable), loading, detailLoading, busy,
    error: (detailOwner === principalId && loadedId === selectedId ? detailError : '') || (rowsOwner === principalId ? error : ''),
    setError, reload, submit,
    resetKey: () => { if (!inFlight.current) key.current = null; } };
}