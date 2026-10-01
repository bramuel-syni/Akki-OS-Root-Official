import { useCallback, useEffect, useRef, useState } from 'react';
import { labRequest } from '@/components/training/useTrainingLab';

const run = id => `/board/${encodeURIComponent(id)}`;

export function useTrainModels(identity) {
  const [board, setBoard] = useState(null), [error, setError] = useState(''), [loading, setLoading] = useState(false), [pending, setPending] = useState({});
  const alive = useRef(true);
  const reload = useCallback(async () => {
    if (!identity) return;
    try { const data = await labRequest('/board'); if (alive.current) { setBoard(data); setError(''); } }
    catch (exc) { if (alive.current) setError(exc.message); }
  }, [identity]);
  useEffect(() => {
    alive.current = true; setBoard(null); setPending({});
    if (identity) { setLoading(true); reload().finally(() => { if (alive.current) setLoading(false); }); }
    return () => { alive.current = false; };
  }, [identity, reload]);
  const live = Boolean(board?.runs.some(r => r.progress || ['In training', 'Testing', 'Queued'].includes(r.status) || r.messages.some(m => m.widget === 'status')));
  useEffect(() => { if (!live) return undefined; const timer = setInterval(reload, 20000); return () => clearInterval(timer); }, [live, reload]);
  const mutate = useCallback(async (path, body, method = 'POST') => {
    try { return await labRequest(path, { method, body: body === undefined ? undefined : JSON.stringify(body) }); }
    finally { await reload(); }
  }, [reload]);
  const send = useCallback(async (id, text) => {
    setPending(p => ({ ...p, [id]: text }));
    try { return await mutate(run(id) + '/messages', { text }); }
    finally { setPending(p => { const next = { ...p }; delete next[id]; return next; }); }
  }, [mutate]);
  return { board, error, loading, pending, reload, send,
    act: (id, action, value) => mutate(run(id) + '/actions', { action, ...(value ? { value } : {}) }),
    create: body => mutate('/board/new', body || {}),
    remove: id => mutate(run(id), undefined, 'DELETE') };
}
