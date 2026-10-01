import { useCallback, useEffect, useRef, useState } from 'react';

const ROOT = `${process.env.REACT_APP_BACKEND_URL}/api/media`;
export const bytes = n => n < 1000 ? `${n} B` : n < 1000000 ? `${(n / 1000).toFixed(1)} KB` : `${(n / 1000000).toFixed(1)} MB`;
export async function mediaRequest(path, options = {}) {
  const token = sessionStorage.getItem('akki_access_token');
  const response = await fetch(ROOT + path, { ...options, headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...options.headers } });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : 'The request could not be completed.');
  return body;
}

export function useMediaLibrary(identity) {
  const [files, setFiles] = useState([]), [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(false), [error, setError] = useState('');
  const [queue, setQueue] = useState([]), [uploading, setUploading] = useState(false);
  const epoch = useRef(0), xhrs = useRef(new Set()), alive = useRef(true);
  const reload = useCallback(async () => {
    if (!identity) return;
    const gen = epoch.current; setLoading(true);
    try {
      const [data, settings] = await Promise.all([mediaRequest('/files'), mediaRequest('/config')]);
      if (gen === epoch.current && alive.current) { setFiles(data.files); setConfig(settings); setError(''); }
    } catch (e) { if (gen === epoch.current && alive.current) setError(e.message); }
    finally { if (gen === epoch.current && alive.current) setLoading(false); }
  }, [identity]);
  useEffect(() => {
    alive.current = true; epoch.current += 1; setFiles([]); setQueue([]); setConfig(null); setError(''); setUploading(false); reload();
    return () => { alive.current = false; epoch.current += 1; xhrs.current.forEach(x => x.abort()); xhrs.current.clear(); };
  }, [identity, reload]);
  const patchQueue = (key, fields, gen) => { if (gen === epoch.current && alive.current) setQueue(old => old.map(q => q.key === key ? { ...q, ...fields } : q)); };
  const send = async (items) => {
    if (uploading) return;
    setUploading(true); const gen = epoch.current;
    for (const item of items) {
      if (!alive.current || gen !== epoch.current) break;
      try {
        patchQueue(item.key, { status: 'Preparing', progress: 0, error: '' }, gen);
        const digest = await crypto.subtle.digest('SHA-256', await item.file.arrayBuffer());
        const sha256 = [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('');
        if (gen !== epoch.current || !alive.current) break;
        const response = await mediaRequest('/uploads', { method: 'POST', headers: { 'Idempotency-Key': item.key }, body: JSON.stringify({ filename: item.file.name, size_bytes: item.file.size, sha256, storage_permission_confirmed: true }) });
        if (gen !== epoch.current || !alive.current) break;
        if (response.file.status !== 'available') {
          patchQueue(item.key, { status: 'Uploading' }, gen);
          await new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest(); xhrs.current.add(xhr);
            xhr.open('PUT', `${ROOT}/files/${response.file.file_id}/content`);
            xhr.setRequestHeader('Authorization', `Bearer ${sessionStorage.getItem('akki_access_token')}`);
            xhr.setRequestHeader('Content-Type', 'application/octet-stream'); xhr.timeout = 180000;
            xhr.upload.onprogress = event => { if (event.lengthComputable) patchQueue(item.key, { progress: Math.round(event.loaded / event.total * 100), status: event.loaded === event.total ? 'Saving securely' : 'Uploading' }, gen); };
            xhr.onload = () => { xhrs.current.delete(xhr); if (xhr.status >= 200 && xhr.status < 300) resolve(); else { let message = 'Upload failed. You can retry this file.'; try { message = JSON.parse(xhr.responseText).detail || message; } catch {} reject(new Error(message)); } };
            xhr.onerror = xhr.ontimeout = () => { xhrs.current.delete(xhr); reject(new Error('Connection interrupted. Retry this file.')); };
            xhr.onabort = () => { xhrs.current.delete(xhr); reject(new Error('Upload cancelled')); };
            xhr.send(item.file);
          });
        }
        patchQueue(item.key, { status: 'Stored', progress: 100 }, gen);
      } catch (e) { patchQueue(item.key, { status: 'Failed', error: e.message }, gen); }
    }
    if (gen === epoch.current && alive.current) { setUploading(false); await reload(); }
  };
  const upload = async fileList => {
    const items = Array.from(fileList).map(file => ({ file, key: crypto.randomUUID(), name: file.name, status: 'Queued', progress: 0 }));
    setQueue(items); await send(items);
  };
  const download = async file => {
    const token = sessionStorage.getItem('akki_access_token');
    const response = await fetch(`${ROOT}/files/${file.file_id}/download`, { headers: { Authorization: `Bearer ${token}` } });
    if (!response.ok) { const data = await response.json().catch(() => ({})); throw new Error(data.detail || 'Download unavailable'); }
    const blob = await response.blob();
    if (sessionStorage.getItem('akki_access_token') !== token || !alive.current) return;
    const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
    anchor.href = url; anchor.download = file.filename; document.body.appendChild(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return { files, config, loading, error, setError, reload, queue, uploading, upload, retry: () => send(queue.filter(q => q.status === 'Failed')), download };
}