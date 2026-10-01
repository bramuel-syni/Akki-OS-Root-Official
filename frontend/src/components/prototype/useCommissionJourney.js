import { useCallback, useEffect, useRef, useState } from 'react';
import { tryGet, tryPost } from '@/lib/apiClient';

const C = '/api/portal/commission';
const R = '/api/portal/requests';
const ACTIVE = new Set(['routing', 'executing', 'interrupted']);
export const failure = (response, fallback) => {
  const detail = response?.data?.detail ?? response?.data;
  if (typeof detail === 'string') return detail;
  if (detail && typeof detail === 'object') return detail.reason || detail.next_action || detail.reason_code || fallback;
  return fallback;
};

/** The ordinary commission journey over the real control plane: draft → review → freeze → approvals → run → result → delivery. */
export function useCommissionJourney(principalId, selectedId, { canRun } = {}) {
  const [rows, setRows] = useState([]), [drafts, setDrafts] = useState([]), [entitlement, setEntitlement] = useState(null), [destinations, setDestinations] = useState(null);
  const [selected, setSelected] = useState(null), [run, setRun] = useState(null), [approvals, setApprovals] = useState(null), [deliveries, setDeliveries] = useState({});
  const [review, setReview] = useState(null), [busy, setBusy] = useState(false), [error, setError] = useState(''), [loading, setLoading] = useState(false), [version, setVersion] = useState(0);
  const owner = useRef(principalId); owner.current = principalId;
  const key = useRef(null), inFlight = useRef(false);
  const reload = useCallback(() => setVersion(v => v + 1), []);

  useEffect(() => {
    let active = true;
    if (!principalId) { setRows([]); setDrafts([]); setEntitlement(null); setDestinations(null); return undefined; }
    setLoading(true);
    Promise.all([tryGet(R), tryGet(`${C}/drafts`), tryGet('/api/portal/entitlement/allowance'), tryGet(`${C}/destinations`)]).then(([work, draft, terms, dest]) => {
      if (!active) return;
      setRows(work.ok && Array.isArray(work.data?.rows) ? work.data.rows : []);
      setDrafts(draft.ok && Array.isArray(draft.data?.rows) ? draft.data.rows : []);
      setEntitlement(terms.ok ? terms.data : null);
      setDestinations(dest.ok ? dest.data : { rows: [], count: 0 });
      if (!work.ok) setError(failure(work, 'Your requests could not be loaded.'));
      setLoading(false);
    });
    return () => { active = false; };
  }, [principalId, version]);

  const loadSelected = useCallback(async id => {
    const [detail, journal] = await Promise.all([tryGet(`${R}/${encodeURIComponent(id)}`), tryGet(`${R}/${encodeURIComponent(id)}/run`)]);
    if (owner.current !== principalId) return null;
    setSelected(detail.ok ? detail.data : null);
    setRun(journal.ok ? journal.data : null);
    if (!detail.ok) setError(failure(detail, 'This request could not be opened.'));
    if (detail.ok && detail.data.state === 'routing') { const r = await tryGet(`/api/portal/approvals/${encodeURIComponent(id)}`); setApprovals(r.ok ? r.data : null); } else setApprovals(null);
    return detail.ok ? detail.data : null;
  }, [principalId]);

  useEffect(() => {
    setSelected(null); setRun(null); setApprovals(null);
    if (principalId && selectedId) loadSelected(selectedId);
  }, [principalId, selectedId, loadSelected, version]);

  const advance = useCallback(async id => {
    const r = await tryPost(`${C}/${encodeURIComponent(id)}/advance`);
    return r;
  }, []);

  // One bounded step at a time while the open request is still moving: the same idempotent slot a refresh uses.
  useEffect(() => {
    if (!selected || !ACTIVE.has(selected.state) || !canRun) return undefined;
    const approved = selected.state !== 'routing' || approvals?.state === 'approved';
    if (!approved) return undefined;
    let stop = false;
    const tick = async () => { if (stop) return; await advance(selected.request_id); if (!stop) await loadSelected(selected.request_id); if (!stop) reload(); };
    const timer = setTimeout(tick, selected.state === 'routing' ? 400 : 8000);
    return () => { stop = true; clearTimeout(timer); };
  }, [selected, approvals, canRun, advance, loadSelected, reload]);

  const guard = async fn => {
    if (inFlight.current) return null;
    inFlight.current = true; setBusy(true); setError('');
    try { return await fn(); } finally { inFlight.current = false; setBusy(false); }
  };

  const saveDraft = body => guard(async () => {
    const r = await tryPost(`${C}/drafts`, body);
    if (!r.ok) { setError(failure(r, 'The draft could not be saved.')); return null; }
    setReview(r.data); return r.data;
  });
  const loadDraft = useCallback(async draftId => { const r = await tryGet(`${C}/drafts/${encodeURIComponent(draftId)}`); if (r.ok) setReview(r.data); return r.ok ? r.data : null; }, []);
  const freeze = draftId => guard(async () => {
    if (key.current?.draft !== draftId) key.current = { draft: draftId, value: crypto.randomUUID() };
    const r = await tryPost(`${C}/drafts/${encodeURIComponent(draftId)}/freeze`, { idempotency_key: key.current.value });
    if (!r.ok) { setError(failure(r, 'The request could not be submitted.')); return null; }
    key.current = null; setReview(null); reload(); return r.data;
  });
  const withdrawDraft = draftId => guard(async () => { const r = await tryPost(`${C}/drafts/${encodeURIComponent(draftId)}/withdraw`); if (!r.ok) setError(failure(r, 'The draft could not be withdrawn.')); else setReview(null); reload(); return r.ok; });
  const stop = id => guard(async () => { const r = await tryPost(`${R}/${encodeURIComponent(id)}/stop`); if (!r.ok) setError(failure(r, 'The request could not be stopped.')); await loadSelected(id); reload(); return r.ok; });
  const retry = id => guard(async () => { const r = await tryPost(`${R}/${encodeURIComponent(id)}/retry`); if (!r.ok) setError(failure(r, 'The request could not be resumed.')); await loadSelected(id); reload(); return r.ok; });
  const retrieve = (id, artifactRef) => guard(async () => {
    const result = await tryGet(`${R}/${encodeURIComponent(id)}/result`);
    if (!result.ok) { setDeliveries(d => ({ ...d, [id]: { state: 'held', reason: failure(result, 'The result is not currently releasable.'), code: result.data?.detail } })); return null; }
    const r = await tryPost(`${R}/${encodeURIComponent(id)}/delivery`, { artifact_ref: artifactRef, idempotency_key: `ui-${id.slice(-12)}-${artifactRef.length}` });
    const view = r.data || {};
    setDeliveries(d => ({ ...d, [id]: { state: r.ok ? view.state : 'held', reason: r.ok ? '' : failure(r, 'Delivery could not be prepared.'), code: view.reason_code, view } }));
    await loadSelected(id);
    return r.ok ? view : null;
  });

  return { rows, drafts, entitlement, destinations, selected, run, approvals, deliveries, review, setReview, busy, loading, error, setError, reload,
    saveDraft, loadDraft, freeze, withdrawDraft, stop, retry, retrieve, advance };
}
