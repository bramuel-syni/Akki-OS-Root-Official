import React from 'react';
import { stamp } from './evidence';

export function workDetailCopy(work) {
  const selected = work.selected;
  return <>
    <p data-testid="dap-work-detail-reason">{selected?.reason}</p>
    <p data-testid="dap-work-detail-hash">Objective SHA-256: {selected?.objective_hash}</p>
    <p data-testid="dap-work-detail-engine">Governing engine: {selected?.governing_engine}. Execution verified: {selected?.execution_verified ? 'yes' : 'no'}.</p>
    {selected?.history.map((h, i) => <p data-testid={`dap-work-history-${i}`} key={`${h.receipt_hash}-${i}`}>{stamp(h.at)} · {h.event} · {h.state}<br />Receipt: {h.receipt_hash}</p>)}
  </>;
}

export const dapWorkCopy = work => ({
  361: 'Rates and consumption are not inferred. A submission is not metered source use.',
  624: 'Only owner-admitted terms and receipted usage establish allowance. Missing records remain unresolved.',
  695: 'The same frozen work records are visible in Akki OS.',
  1055: 'Recorded history',
  1056: 'Frozen objective, lifecycle events, and canonical receipt references.',
  1085: workDetailCopy(work),
});