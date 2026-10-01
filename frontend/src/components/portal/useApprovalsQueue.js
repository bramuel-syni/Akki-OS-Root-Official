import { useCallback, useEffect, useState } from 'react';
import { tryGet, tryPost } from '@/lib/apiClient';
import { failure } from '@/components/prototype/useCommissionJourney';

/** Requests whose pending approval groups seat the signed-in approver, and the decision that records their signature. */
export function useApprovalsQueue(enabled) {
  const [rows, setRows] = useState(null), [requests, setRequests] = useState({}), [loading, setLoading] = useState(false), [error, setError] = useState(''), [busy, setBusy] = useState(false);
  const reload = useCallback(async () => {
    if (!enabled) { setRows(null); return; }
    setLoading(true); setError('');
    const queue = await tryGet('/api/portal/approvals/queue');
    if (!queue.ok) { setError(failure(queue, 'The approvals queue could not be loaded.')); setRows([]); setLoading(false); return; }
    const list = queue.data.rows || [];
    const details = await Promise.all(list.map(r => tryGet(`/api/portal/requests/${encodeURIComponent(r.request_id)}`)));
    setRequests(Object.fromEntries(list.map((r, i) => [r.request_id, details[i].ok ? details[i].data : null])));
    setRows(list); setLoading(false);
  }, [enabled]);
  useEffect(() => { reload(); }, [reload]);
  const decide = useCallback(async (requestId, group, decision, reason) => {
    setBusy(true); setError('');
    const r = await tryPost(`/api/portal/approvals/${encodeURIComponent(requestId)}/decide`, { group, decision, reason });
    if (!r.ok) setError(failure(r, 'The decision could not be recorded.'));
    await reload(); setBusy(false);
    return r.ok;
  }, [reload]);
  return { rows, requests, loading, error, busy, reload, decide };
}
