import React, { useEffect, useState } from 'react';
import { Library, Server } from 'lucide-react';
import { mediaRequest } from '@/components/media/useMediaLibrary';

export const CorpusCard = ({ lab, canOperate, isRms }) => {
  const [busy, setBusy] = useState(false), [error, setError] = useState(''); const m = lab.corpus;
  const dispatch = async () => { setBusy(true); setError(''); try { await lab.post('/corpus-measurements', { host: 'akki-vm', workers: 16, max_seconds: 5400, max_files_per_language: 0 }); } catch (e) { setError(e.message); } finally { setBusy(false); } };
  const langs = m?.result?.per_language || {};
  return <section className="lab-card" data-testid="lab-corpus-card">
    <header><h2><Server size={18} />Staged corpus on the Akki workers</h2><p>Every authorized staged recording measured on the GPU host. Readings only; no training, no media leaves the host.</p></header>
    {canOperate && isRms && <button className="estate-btn" onClick={dispatch} disabled={busy || m?.status === 'running'} data-testid="lab-corpus-dispatch">{m?.status === 'running' ? 'Measuring on the host…' : busy ? 'Dispatching…' : m?.status === 'completed' ? 'Measure again' : 'Measure the staged corpus'}</button>}
    {error && <p className="media-error" role="alert" data-testid="lab-corpus-error">{error}</p>}
    {!m && <p className="media-note" data-testid="lab-corpus-empty">Not measured yet.</p>}
    {m && <div className="lab-run" data-testid="lab-corpus-status">
      <p className="lab-status">{m.status === 'running' ? `Running · ${m.progress?.files ?? 0} of ${m.progress?.of ?? '…'} files · ${Math.round((m.progress?.elapsed_s || 0) / 60)} min` : m.status === 'completed' ? `Completed · ${m.result.measured} of ${m.result.files} files measured in ${Math.round(m.result.compute_seconds / 60)} min` : `${m.status}${m.reason ? ` · ${m.reason}` : ''}`}</p>
      {m.status === 'completed' && <table data-testid="lab-corpus-table"><thead><tr><th>Language</th><th>Files</th><th>Hours</th><th>Reads as</th><th>Music windows</th><th>Files for review</th><th>Channel</th></tr></thead>
        <tbody>{Object.entries(langs).map(([lang, v]) => <tr key={lang} data-testid={`lab-corpus-lang-${lang}`}><td>{lang}</td><td>{v.measured}{v.decode_failures ? ` (+${v.decode_failures} unreadable)` : ''}</td><td>{v.hours}</td><td>{Object.entries(v.reads_as).map(([k, n]) => `${k} ${n}`).join(' · ')}</td><td>{v.music_windows} of {v.windows}</td><td>{v.files_with_music_windows}</td><td>{Object.entries(v.channel_condition).map(([k, n]) => `${k.replace('_', ' ')} ${n}`).join(' · ')}</td></tr>)}</tbody></table>}
    </div>}
  </section>;
};

export const ReferenceCard = ({ canOperate }) => {
  const [state, setState] = useState(null), [busy, setBusy] = useState(false), [error, setError] = useState('');
  const load = async () => { try { setState(await mediaRequest('/reference/import')); } catch (e) { setError(e.message); } };
  useEffect(() => { load(); }, []);
  useEffect(() => { if (state?.import?.status !== 'running') return undefined; const t = setInterval(load, 8000); return () => clearInterval(t); }, [state?.import?.status]);
  const start = async () => { setBusy(true); setError(''); try { await mediaRequest('/reference/import', { method: 'POST' }); await load(); } catch (e) { setError(e.message); } finally { setBusy(false); } };
  const items = state?.import?.items || []; const done = items.filter(i => ['imported', 'already_imported'].includes(i.status)).length;
  return <section className="lab-card" data-testid="lab-reference-card">
    <header><h2><Library size={18} />Public-domain reference recordings</h2><p>Speech from LibriVox readers in four languages and solo piano from Musopen, kept apart from your music and never counted as training data.</p></header>
    {canOperate && <button className="estate-btn" onClick={start} disabled={busy || state?.import?.status === 'running'} data-testid="lab-reference-import">{state?.import?.status === 'running' ? 'Importing…' : busy ? 'Starting…' : 'Import reference recordings'}</button>}
    {error && <p className="media-error" role="alert" data-testid="lab-reference-error">{error}</p>}
    {state?.import && <div className="lab-run" data-testid="lab-reference-status"><p className="lab-status">{state.import.status === 'running' ? `Importing · ${done} stored so far` : `${done} reference recordings in the library`}{items.some(i => i.status === 'failed' || i.status === 'unavailable') ? ` · ${items.filter(i => i.status === 'failed' || i.status === 'unavailable').length} could not be fetched` : ''}</p>
      {items.length > 0 && <ul className="lab-list">{items.map((i, k) => <li key={k} className={i.status}><span>{i.title || i.identifier}</span><small>{i.label || ''} · {i.status.replace('_', ' ')}</small></li>)}</ul>}</div>}
    {state && !state.import && <p className="media-note" data-testid="lab-reference-empty">Nothing imported yet. {state.catalogue.length} catalogue items are ready.</p>}
  </section>;
};
