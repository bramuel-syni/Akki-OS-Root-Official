import React, { useState } from 'react';
import { Play, ShieldCheck } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { censusRequest } from './useCensusWorkspace';

export function CensusRunDialog({ open, onClose, data, onQueued }) {
  const [selected, setSelected] = useState([]);
  const [key, setKey] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function submit(event) {
    event.preventDefault(); setBusy(true); setError('');
    const submissionKey = key || crypto.randomUUID();
    setKey(submissionKey);
    try {
      await censusRequest('/run', { method: 'POST', body: JSON.stringify({ source_ids: selected, idempotency_key: submissionKey }) });
      setKey(null); setSelected([]); onQueued(); onClose();
    } catch (e) { setError(e.message); }
    finally { setBusy(false); }
  }
  return <Dialog open={open} onOpenChange={value => !busy && !value && onClose()}>
    <DialogContent data-testid="census-run-dialog" className="census-dialog">
      <DialogHeader><DialogTitle data-testid="census-run-title">Run census</DialogTitle>
        <DialogDescription data-testid="census-run-boundary">Read-only, bounded metadata checks. Source data stays within Akki’s execution perimeter.</DialogDescription></DialogHeader>
      <div className="census-tenant" data-testid="census-run-tenant"><ShieldCheck size={16} />{data.tenant_id} · identity-bound</div>
      <form onSubmit={submit} data-testid="census-run-form">
        <fieldset disabled={busy}><legend>Sources</legend>
          {data.sources.map(source => <label className="census-source-choice" key={source.source_id}>
            <input data-testid={`census-source-${source.source_id}`} type="checkbox" checked={selected.includes(source.source_id)} onChange={e => {
              setSelected(e.target.checked ? [...selected, source.source_id] : selected.filter(s => s !== source.source_id));
              setKey(null);
            }} />
            <span data-testid={`census-source-label-${source.source_id}`}>{source.label}<small>{source.scope}</small></span>
          </label>)}
        </fieldset>
        <p className="census-caption" data-testid="census-run-limit">No content extraction, quality score or release permission is implied. Unavailable sources return a recorded blocked outcome.</p>
        {error && <p data-testid="census-run-error" role="alert" className="census-error">{error}</p>}
        <div className="census-actions"><button data-testid="census-run-cancel" type="button" className="census-button" disabled={busy} onClick={onClose}>Cancel</button>
          <button data-testid="census-run-submit" className="census-button primary" disabled={busy || !selected.length}><Play size={14} />{busy ? 'Submitting…' : 'Run census'}</button></div>
      </form>
    </DialogContent>
  </Dialog>;
}