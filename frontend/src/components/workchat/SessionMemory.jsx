import React from 'react';

export function SessionMemory({ session, memory, onCompact, onReload, onArchive }) {
  const compaction = memory?.compaction || session.compaction;
  const open = session.turns.filter(t => !t.compacted).length;
  const objective = session.objective || {};
  const intent = [...session.turns].reverse().find(t => t.evidence?.intent)?.evidence?.intent;
  return <div className="workchat-memory" data-testid="workchat-memory-bar">
    {objective.artifact_id && <div className="workchat-objective" data-testid="workchat-objective" style={{ flexBasis: '100%' }}>
      <span className="workchat-label">Objective (frozen before anything crossed)</span>
      <span data-testid="workchat-objective-bounded">{objective.bounded_objective}</span>
      <span className="workchat-badge neutral" data-testid="workchat-objective-ref" title={`Captured ${objective.captured_at} by the contained reader; artefact ${objective.artifact_id}`}>intent · {objective.intent}</span>
      {intent && <span className={`workchat-badge ${intent.diverged ? 'refused' : 'warm'}`} data-testid="workchat-objective-divergence">
        {intent.diverged ? `conduct diverged: ${intent.divergent.map(d => d.flag).join(', ')}` : `conduct matches the declared objective · ${intent.observations} observed`}
      </span>}
    </div>}
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
