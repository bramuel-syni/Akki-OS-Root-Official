import React, { useCallback, useEffect, useRef, useState } from 'react';
import { apiRequest, stamp } from './useModelApproval';

const LANG = { kik: 'Kikuyu', kam: 'Kamba', swa: 'Kiswahili' };
const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };

async function fetchAudio(taskId) {
  const token = sessionStorage.getItem('akki_access_token');
  const r = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/training/malpha/review/tasks/${taskId}/audio`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!r.ok) throw new Error('Segment playback unavailable right now.');
  return URL.createObjectURL(await r.blob());
}

// Native-reviewer confirmation panel: two independent listeners per sealed admission segment, adjudication on disagreement. No transcript is ever shown.
export function NativeReview({ canOperate }) {
  const [panel, setPanel] = useState(null), [brands, setBrands] = useState([]), [lang, setLang] = useState('kik'), [task, setTask] = useState(null), [audio, setAudio] = useState(null);
  const [picked, setPicked] = useState([]), [entry, setEntry] = useState(''), [busy, setBusy] = useState(false), [error, setError] = useState(null), [done, setDone] = useState(0), [disagreements, setDisagreements] = useState([]);
  const audioRef = useRef(null);
  const load = useCallback(() => Promise.all([apiRequest('/api/training/malpha/review/panel'), apiRequest('/api/training/malpha/review/brands'), apiRequest('/api/training/malpha/review/tasks?status=disagreement')])
    .then(([p, b, d]) => { setPanel(p); setBrands(b.brands || []); setDisagreements(d.tasks || []); }).catch(e => setError(e.message)), []);
  useEffect(() => { load(); }, [load]);
  const next = useCallback(async (l = lang) => {
    setBusy(true); setError(null); setPicked([]); setEntry(''); if (audio) URL.revokeObjectURL(audio); setAudio(null);
    try { const r = await apiRequest(`/api/training/malpha/review/next?language=${l}`); setTask(r.task); if (r.task) setAudio(await fetchAudio(r.task.task_id)); }
    catch (e) { setError(e.message); }
    setBusy(false);
  }, [lang, audio]);
  const submit = async body => {
    if (!task) return; setBusy(true); setError(null);
    try { await apiRequest(`/api/training/malpha/review/tasks/${task.task_id}/annotate`, { method: 'POST', body: JSON.stringify(body) }); setDone(d => d + 1); await load(); await next(); }
    catch (e) { setError(e.message); setBusy(false); }
  };
  const adjudicate = async (t, body) => { setBusy(true); try { await apiRequest(`/api/training/malpha/review/tasks/${t.task_id}/adjudicate`, { method: 'POST', body: JSON.stringify(body) }); await load(); } catch (e) { setError(e.message); } setBusy(false); };
  const addBrand = name => { const b = brands.find(x => x.toLowerCase() === name.trim().toLowerCase()); if (b && !picked.includes(b)) setPicked(p => [...p, b]); setEntry(''); };
  const per = panel?.panel?.per_language || {}; const pre = panel?.preflight || {};
  return <section className="estate-section" data-testid="native-review" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Native review · confirmation panel</h2>
      <p>Independent reference for the sealed brand-listener read: two native listeners label each held-out segment without seeing any transcript; disagreements go to a third identity. Seal v{pre.split_version || '—'} · independence {pre.independence_verified ? 'verified' : 'not verified'} · reference {pre.reference_verified ? 'verified' : 'pending'} · sealed read {pre.ready ? 'unlocked' : 'locked'}.</p></div></header>
    {error && <p className="estate-alert" data-testid="native-review-error">{error}</p>}
    {!panel?.panel ? <p className="estate-note" data-testid="native-review-empty">No confirmation panel yet — it opens automatically when the admission split is re-sealed.</p> : <>
      <div className="estate-table-wrap"><table className="estate-table" data-testid="native-review-progress"><thead><tr><th>Language</th><th>Segments</th><th>Open</th><th>Second listener needed</th><th>Disagreements</th><th>Final</th><th>Listeners</th><th>Agreement</th></tr></thead>
        <tbody>{Object.entries(per).map(([l, v]) => <tr key={l} data-testid={`native-review-row-${l}`}><td data-label="Language">{LANG[l] || l}</td><td data-label="Segments">{v.tasks}</td><td data-label="Open">{v.open}</td><td data-label="Second listener needed">{v.partial}</td><td data-label="Disagreements">{v.disagreement}</td>
          <td data-label="Final">{v.agreed + v.adjudicated}{v.complete ? ' · complete' : ''}</td><td data-label="Listeners">{v.distinct_annotators}</td><td data-label="Agreement">{v.agreement_rate == null ? '—' : `${Math.round(v.agreement_rate * 100)}%`}</td></tr>)}</tbody></table></div>
      <p className="estate-note">Panel opened {stamp(panel.panel.opened_at)} · {panel.panel.verified ? `verified ${stamp(panel.panel.verified_at)}` : 'annotating'} · you have labelled {done} segment{done === 1 ? '' : 's'} this visit.</p>
      {canOperate && <div data-testid="native-review-workbench" style={{ marginTop: 12, padding: 14, border: '1px solid var(--line)', borderRadius: 10, background: '#fff' }}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <select data-testid="native-review-language" style={{ ...field, width: 'auto' }} value={lang} onChange={e => { setLang(e.target.value); setTask(null); }}>{Object.entries(LANG).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
          <button className="estate-btn primary" data-testid="native-review-next" disabled={busy} onClick={() => next(lang)}>{busy ? 'Working…' : task ? 'Skip to another segment' : 'Listen to the next segment'}</button>
        </div>
        {task && <div style={{ marginTop: 12 }} data-testid="native-review-task">
          <p className="estate-note" data-testid="native-review-task-meta">Segment {task.seg_id} · {Math.round(task.duration_s)} s · {LANG[task.language]}. Listen as many times as you need. Name every brand you hear; the transcript is not shown.</p>
          {audio ? <audio ref={audioRef} data-testid="native-review-audio" controls src={audio} style={{ width: '100%', maxWidth: 520 }} /> : <p className="estate-note">Fetching the segment from the estate host…</p>}
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center', marginTop: 10 }}>
            <input list="native-review-brand-list" data-testid="native-review-brand-entry" style={{ ...field, maxWidth: 320 }} placeholder="Type a brand you heard…" value={entry} onChange={e => setEntry(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addBrand(entry); } }} />
            <datalist id="native-review-brand-list">{brands.map(b => <option key={b} value={b} />)}</datalist>
            <button className="estate-btn" data-testid="native-review-add-brand" type="button" onClick={() => addBrand(entry)} disabled={!entry.trim()}>Add</button>
            {picked.map(b => <span key={b} className="estate-chip" data-testid={`native-review-picked-${b.replace(/[^A-Za-z0-9]+/g, '-')}`} style={{ padding: '4px 10px', border: '1px solid var(--line)', borderRadius: 999, fontSize: 12 }}>{b} <button type="button" aria-label={`remove ${b}`} onClick={() => setPicked(p => p.filter(x => x !== b))} style={{ border: 0, background: 'none', cursor: 'pointer' }}>×</button></span>)}
          </div>
          <div className="estate-actions" style={{ marginTop: 12 }}>
            <button className="estate-btn primary" data-testid="native-review-submit-brands" disabled={busy || !picked.length} onClick={() => submit({ brands: picked })}>Submit {picked.length ? `${picked.length} brand${picked.length === 1 ? '' : 's'}` : 'brands'}</button>
            <button className="estate-btn" data-testid="native-review-no-mention" disabled={busy} onClick={() => submit({ no_mention: true })}>No brand mentioned</button>
            <button className="estate-btn" data-testid="native-review-unsure" disabled={busy} onClick={() => submit({ unsure: true })}>Unsure</button>
          </div>
        </div>}
        {!task && !busy && <p className="estate-note" data-testid="native-review-idle">Pick a language and press “Listen to the next segment”. Each segment is a few seconds of radio; you will never be given the same segment twice.</p>}
      </div>}
      {disagreements.length > 0 && <div style={{ marginTop: 14 }} data-testid="native-review-disagreements"><h3 style={{ fontSize: 13, margin: '0 0 6px' }}>Disagreements awaiting a third listener ({disagreements.length})</h3>
        {disagreements.slice(0, 8).map(t => <div key={t.task_id} data-testid={`native-review-disagreement-${t.task_id}`} style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', padding: '6px 0', borderTop: '1px solid var(--line)' }}>
          <span style={{ fontSize: 12 }}>{LANG[t.language]} · {t.seg_id} · {Math.round(t.duration_s)} s</span>
          <button className="estate-btn" disabled={busy} onClick={async () => { try { setAudio(await fetchAudio(t.task_id)); setTask(null); } catch (e) { setError(e.message); } }}>Listen</button>
          <input data-testid={`native-review-adjudicate-entry-${t.task_id}`} style={{ ...field, maxWidth: 260 }} placeholder="Brands heard (comma-separated) or leave empty" onKeyDown={e => { if (e.key === 'Enter') adjudicate(t, { brands: e.target.value.split(',').map(s => s.trim()).filter(Boolean) }); }} />
          <button className="estate-btn" data-testid={`native-review-adjudicate-none-${t.task_id}`} disabled={busy} onClick={() => adjudicate(t, { brands: [] })}>Decide: no brand</button>
        </div>)}</div>}
    </>}
  </section>;
}
