import { useCallback, useEffect, useState } from 'react';
import { tryGet, tryPost } from '@/lib/apiClient';

const failure = (r, fallback) => (r.status === 409 && r.data?.reason) ? `${r.data.reason} ${r.data.next_action || ''}`.trim()
  : r.data?.detail || r.data?.reason || r.error || fallback;

export function useChatSessions(enabled) {
  const [rows, setRows] = useState([]);
  const [active, setActive] = useState(null);
  const [pending, setPending] = useState('');
  const [error, setError] = useState('');
  const [memory, setMemory] = useState(null);

  const refresh = useCallback(async () => {
    const r = await tryGet('/api/chat/sessions');
    if (r.ok) setRows(r.data.rows); else setError(failure(r, 'Conversations could not be read.'));
  }, []);

  useEffect(() => { if (enabled) refresh(); else { setRows([]); setActive(null); } }, [enabled, refresh]);

  const open = useCallback(async (id) => {
    setError(''); setMemory(null);
    const r = await tryGet(`/api/chat/sessions/${id}`);
    if (r.ok) setActive(r.data); else setError(failure(r, 'That conversation could not be opened.'));
  }, []);

  const ask = useCallback(async (question) => {
    setError(''); setPending(question);
    const r = await tryPost('/api/chat/ask', { question, session_id: active?.session_id || null });
    if (!r.ok) { setPending(''); setError(failure(r, 'The question could not be answered.')); return null; }
    await open(r.data.session_id); await refresh();
    setPending('');
    return r.data;
  }, [active, open, refresh]);

  const compact = useCallback(async () => {
    if (!active) return;
    const r = await tryPost(`/api/chat/sessions/${active.session_id}/compact`);
    if (!r.ok) { setError(failure(r, 'Compaction was refused.')); return; }
    await open(active.session_id);
    setMemory({ kind: 'compact', ...r.data });
  }, [active, open]);

  const reload = useCallback(async () => {
    if (!active) return;
    const r = await tryGet(`/api/chat/sessions/${active.session_id}/reload`);
    if (r.ok) setMemory({ kind: 'reload', ...r.data }); else setError(failure(r, 'Reload was refused.'));
  }, [active]);

  const archive = useCallback(async () => {
    if (!active) return;
    const r = await tryPost(`/api/chat/sessions/${active.session_id}/archive`);
    if (r.ok) { setActive(null); setMemory(null); refresh(); } else setError(failure(r, 'Archive was refused.'));
  }, [active, refresh]);

  const fresh = useCallback(() => { setActive(null); setMemory(null); setError(''); }, []);
  return { rows, active, pending, error, memory, open, ask, compact, reload, archive, fresh, dismiss: () => setError('') };
}
