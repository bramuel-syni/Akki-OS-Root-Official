import React from 'react';

export function SessionMemory({ session, memory, onCompact, onReload, onArchive }) {
  const compaction = memory?.compaction || session.compaction;
  const open = session.turns.filter(t => !t.compacted).length;
  return <div className="workchat-memory" data-testid="workchat-memory-bar">
    <span className="workchat-label">Durable memory</span>
    <span data-testid="workchat-memory-turns">{session.turns.length} turn{session.turns.length === 1 ? '' : 's'} · {open} open</span>
    {compaction
      ? <span data-testid="workchat-memory-compaction">compacted {compaction.compacted_turns} turn(s) → artefact {compaction.artefact_hash.slice(0, 16)}… · {compaction.claims} claims · ledger {compaction.chain_row_id}</span>
      : <span data-testid="workchat-memory-compaction">not compacted yet</span>}
    {memory?.kind === 'reload' && <span className={`workchat-badge ${memory.status === 'verified' ? 'warm' : memory.status === 'none' ? 'neutral' : 'refused'}`} data-testid="workchat-memory-reload">
      reload {memory.status}{memory.status === 'verified' ? ` · ${memory.bytes} bytes · sha ${memory.verified_sha256.slice(0, 12)}…` : memory.reason ? ` · ${memory.reason}` : ''}
    </span>}
    {memory?.kind === 'compact' && memory.status === 'nothing_to_compact' && <span className="workchat-badge neutral" data-testid="workchat-memory-nothing">{memory.reason}</span>}
    <span style={{ flex: 1 }} />
    <button className="workchat-btn" data-testid="workchat-compact" onClick={onCompact} disabled={open === 0}>Compact now</button>
    <button className="workchat-btn" data-testid="workchat-reload" onClick={onReload}>Verify reload</button>
    <button className="workchat-btn quiet" data-testid="workchat-archive" onClick={onArchive}>Archive</button>
  </div>;
}
