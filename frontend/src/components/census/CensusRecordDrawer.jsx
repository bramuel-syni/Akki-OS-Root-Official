import React, { useEffect, useState } from 'react';
import { Check, Copy, FileCheck2 } from 'lucide-react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import { censusRequest, number, date } from './useCensusWorkspace';

export function CensusRecordDrawer({ recordId, onClose }) {
  const [record, setRecord] = useState(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    let live = true; setRecord(null); setError(''); setCopied(false);
    if (recordId) censusRequest(`/records/${encodeURIComponent(recordId)}`).then(d => live && setRecord(d.record)).catch(e => live && setError(e.message));
    return () => { live = false; };
  }, [recordId]);
  return <Sheet open={Boolean(recordId)} onOpenChange={open => !open && onClose()}>
    <SheetContent data-testid="census-record-drawer" className="census-drawer">
      <SheetHeader><SheetTitle data-testid="census-record-title">{record?.census_number ? `Census #${record.census_number}` : 'Census record'}</SheetTitle>
        <SheetDescription data-testid="census-record-date">{record ? date(record.finished_at) : 'Reading the governing record…'}</SheetDescription></SheetHeader>
      {error && <p role="alert" data-testid="census-record-error" className="census-error">{error}</p>}
      {record && <>
        <div className="census-tenant" data-testid="census-record-tenant"><FileCheck2 size={16} />{record.tenant_id} · {record.scope}</div>
        <dl className="census-details">{[['Databases', record.database_count], ['Tables', record.table_count], ['Estimated rows', record.row_count_estimate], ['Counted rows', record.row_count_measured], ['Data volume', record.volume_bytes]].map(([label, value]) => <div key={label}>
          <dt>{label}</dt><dd data-testid={`census-detail-${label.toLowerCase().replaceAll(' ', '-')}`}>{number(value)}</dd></div>)}</dl>
        <h2>Evidence</h2>
        <p data-testid="census-record-execution">{record.execution_verified ? 'Akki-owned execution verified.' : 'Historical evidence; current execution not re-verified.'}</p>
        {record.status === 'PARTIAL' && <p data-testid="census-record-partial" className="census-error">Partial coverage: some commissioned sources were not read.</p>}
        <p data-testid="census-record-proof" className="census-proof">{record.proof_ref}</p>
        <code data-testid="census-record-hash" className="census-proof">{record.proof_sha256}</code>
        <button className="census-button" data-testid="census-copy-proof" onClick={async () => {
          try { await navigator.clipboard.writeText(`${record.proof_ref}\nSHA-256 ${record.proof_sha256}`); setCopied(true); }
          catch { setError('The browser could not copy the proof reference. It remains visible above.'); }
        }}>{copied ? <Check size={14} /> : <Copy size={14} />}{copied ? 'Copied' : 'Copy proof reference'}</button>
        <h2>What this census does not establish</h2><ul data-testid="census-record-limitations" className="census-limitations">{record.limitations.map((note, i) => <li key={i}>{note}</li>)}</ul>
      </>}
    </SheetContent>
  </Sheet>;
}