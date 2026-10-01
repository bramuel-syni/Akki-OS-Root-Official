import React from 'react';

const when = (iso) => iso ? new Date(iso).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }) : '';

export function SessionRail({ rows, active, onOpen, onFresh }) {
  return <aside className="workchat-rail" data-testid="workchat-session-rail" aria-label="Your conversations">
    <div className="workchat-rail-head">
      <span className="workchat-label">Conversations</span>
      <button className="workchat-btn primary" data-testid="workchat-new-session" onClick={onFresh}>New</button>
    </div>
    {rows.length === 0 && <div className="workchat-empty" data-testid="workchat-session-empty">No conversations yet.</div>}
    {rows.map(row => <button key={row.session_id} data-testid={`workchat-session-${row.session_id}`}
      className={`workchat-session${active?.session_id === row.session_id ? ' active' : ''}`} onClick={() => onOpen(row.session_id)}>
      <span className="workchat-session-title">{row.title}</span>
      <span className="workchat-session-meta">{when(row.updated_at)}{row.compaction ? ' · compacted' : ''}</span>
    </button>)}
  </aside>;
}
