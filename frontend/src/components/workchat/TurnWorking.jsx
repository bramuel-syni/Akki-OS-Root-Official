import React, { useState } from 'react';
import { readableText } from '../shared/PresentationDetails';

export function TurnWorking({ turn }) {
  const [copy, setCopy] = useState('');
  const ev = turn.evidence || {}, detail = turn.decision_detail || {};
  const grounding = ev.grounding || {};
  const refs = ev.cited_refs || [];
  return <details className="workchat-working" data-testid={`workchat-working-${turn.turn_id}`}>
    <summary data-testid={`workchat-working-toggle-${turn.turn_id}`}>Sources & answer limits</summary>
    <ul className="workchat-lines" data-testid={`workchat-answer-limits-${turn.turn_id}`}>
      <li><b>Decision</b> {readableText(detail.reason || turn.refusal_reason || 'No explanation recorded.')}</li>
      {detail.slice && <li><b>Data needed</b> {detail.slice.database}.{detail.slice.table}{detail.draft ? ' · Request drafted, not sent.' : ''}</li>}
      {ev.window?.loss_statement && <li><b>Context limits</b> {readableText(ev.window.loss_statement)}</li>}
      {grounding.unsupported && <li><b>Not supported</b> {readableText(grounding.unsupported)}</li>}
      {ev.reads?.failures?.length > 0 && <li><b>Unavailable sources</b> {ev.reads.failures.length}. The answer may be incomplete.</li>}
      {turn.critic_verdict && <li><b>Review</b> {turn.critic_verdict.findings_count} findings · {turn.critic_verdict.seam_attested ? 'Checked' : 'Not verified'}</li>}
      <li><b>Sources cited</b> {refs.length}</li>
    </ul>
    {refs.length > 0 && <><button className="workchat-btn" data-testid={`workchat-copy-sources-${turn.turn_id}`} onClick={async () => { try { await navigator.clipboard.writeText(refs.join('\n')); setCopy('Source references copied'); } catch { setCopy('Could not copy source references.'); } }}>Copy source references</button>{copy && <p role="status" data-testid={`workchat-copy-status-${turn.turn_id}`}>{copy}</p>}</>}
  </details>;
}