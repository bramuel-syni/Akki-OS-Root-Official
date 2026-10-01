import { useCallback, useEffect, useRef, useState } from 'react';
import { mediaRequest } from './useMediaLibrary';

const pending = m => m && (m.status === 'queued' || m.status === 'measuring');

export function useMediaAcoustics(identity) {
  const [byFile, setByFile] = useState({}), [register, setRegister] = useState(null), [error, setError] = useState('');
  const alive = useRef(true);
  const reload = useCallback(async () => {
    if (!identity) return;
    try {
      const data = await mediaRequest('/acoustics');
      if (alive.current) setByFile(Object.fromEntries(data.measurements.map(m => [m.file_id, m])));
    } catch (e) { if (alive.current) setError(e.message); }
  }, [identity]);
  useEffect(() => {
    alive.current = true; setByFile({}); setError('');
    if (identity) { reload(); mediaRequest('/acoustics/register').then(r => { if (alive.current) setRegister(r); }).catch(() => {}); }
    return () => { alive.current = false; };
  }, [identity, reload]);
  const busy = Object.values(byFile).some(pending);
  useEffect(() => { if (!busy) return undefined; const timer = setInterval(reload, 4000); return () => clearInterval(timer); }, [busy, reload]);
  const request = useCallback(async fileId => { const data = await mediaRequest(`/files/${fileId}/acoustics`, { method: 'POST' }); await reload(); return data; }, [reload]);
  const batch = useCallback(async ids => { const data = await mediaRequest('/acoustics/batch', { method: 'POST', body: JSON.stringify({ file_ids: ids }) }); await reload(); return data; }, [reload]);
  const profile = useCallback(fileId => mediaRequest(`/files/${fileId}/acoustics`), []);
  return { byFile, register, error, reload, request, batch, profile, measuring: busy };
}
