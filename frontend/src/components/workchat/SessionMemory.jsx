import React from 'react';

export function SessionMemory({ session, memory, onCompact, onReload, onArchive }) {
  const compaction = memory?.compaction || session.compaction;
  const open = session.turns.filter(t => !t.compacted).length;
  return <div className="workchat-memory" data-testid="workchat-memory-bar">
    <span className="workchat-label">Conversation memory</span>
    <span data-testid="workchat-memory-turns">{session.turns.length} exchanges · {open} not summarised</span>
    {compaction
      ? <span data-testid="workchat-memory-compaction">{compaction.compacted_turns} exchanges saved in a summary · {compaction.claims} claims retained</span>
      : null}
    {memory?.kind === 'reload' && <span className={`workchat-badge ${memory.status === 'verified' ? 'warm' : memory.status === 'none' ? 'neutral' : 'refused'}`} data-testid="workchat-memory-reload">
      {memory.status === 'verified' ? 'Saved memory verified' : memory.status === 'none' ? 'No saved summary yet' : 'Memory could not be verified'}
    </span>}
    {memory?.kind === 'compact' && memory.status === 'nothing_to_compact' && <span className="workchat-badge neutral" data-testid="workchat-memory-nothing">{memory.reason}</span>}
    <span style={{ flex: 1 }} />
    <button className="workchat-btn" data-testid="workchat-compact" onClick={onCompact}>Summarise memory</button>
    <button className="workchat-btn" data-testid="workchat-reload" onClick={onReload}>Verify saved memory</button>
    <button className="workchat-btn quiet" data-testid="workchat-archive" onClick={onArchive}>Archive</button>
  </div>;
}
