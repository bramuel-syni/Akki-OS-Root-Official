import React from 'react';

const n = (v) => (v === null || v === undefined) ? '—' : Number(v).toLocaleString();

export function TurnWorking({ turn }) {
  const ev = turn.evidence || {};
  const reads = ev.reads || {};
  const win = ev.window;
  const mem = ev.memory;
  const detail = turn.decision_detail || {};
  const grounding = ev.grounding || {};
  const budget = win ? win.window_tokens - win.reserved_tokens : null;
  const excluded = win ? Object.entries(win.excluded_counts || {}).filter(([, c]) => c).map(([k, c]) => `${c} ${k}`).join(', ') : '';
  return <details className="workchat-working" data-testid={`workchat-working-${turn.turn_id}`}>
    <summary data-testid={`workchat-working-toggle-${turn.turn_id}`}>See the working</summary>
    <div className="workchat-grid">
      <div className="workchat-fact" data-testid={`workchat-fact-source-reads-${turn.turn_id}`}><b>{n(reads.source_dispatches)}</b><span>source dispatches · {n(reads.source_rows_read)} source rows read</span></div>
      <div className="workchat-fact" data-testid={`workchat-fact-store-${turn.turn_id}`}><b>{n(reads.qualified_store_calls)}</b><span>qualified-store reads · {n(reads.qualified_bytes_read)} bytes · {n(reads.candidates_returned)} candidates of {n(reads.matched_total)} matched / {n(reads.units_total)} units</span></div>
      {win && <div className="workchat-fact" data-testid={`workchat-fact-window-${turn.turn_id}`}><b>{n(win.tokens_in_window)} / {n(budget)}</b><span>tokens in window · {n(win.selected_refs?.length)} whole units{excluded ? ` · excluded by budget: ${excluded}` : ' · nothing excluded'}</span></div>}
      {mem && <div className="workchat-fact" data-testid={`workchat-fact-memory-${turn.turn_id}`}><b>{n(mem.hits)} hit · {n(mem.misses)} miss</b><span>working set {n(mem.hot_refs_before)} → {n(mem.hot_refs_after)} hot refs · {n(mem.evicted)} evicted</span></div>}
      {turn.receipt_id && <div className="workchat-fact" data-testid={`workchat-fact-model-${turn.turn_id}`}><b>{n(turn.tokens_in)} in · {n(turn.tokens_out)} out</b><span>{turn.model_id} · {turn.latency_ms} ms model · {turn.latency_ms_total} ms turn</span></div>}
      {ev.grounding && <div className="workchat-fact" data-testid={`workchat-fact-grounding-${turn.turn_id}`}><b>{grounding.grounding}</b><span>{grounding.sufficient ? 'window sufficient' : 'answered narrowly'}{grounding.citations_dropped ? ` · ${grounding.citations_dropped} citation(s) outside the window dropped` : ''}</span></div>}
    </div>
    <ul className="workchat-lines">
      <li><b>Decision</b> {detail.decision} · {detail.reason} · ledger row {detail.ledger_row_id}</li>
      <li><b>Subject</b> {detail.sub_objective} · qualified regions {detail.scope_regions?.length ? detail.scope_regions.join(', ') : 'none'}</li>
      {detail.slice && <li><b>Missing slice</b> {detail.slice.database}.{detail.slice.table} · {n(detail.slice.row_count)} rows · {n(detail.slice.column_count)} columns{detail.draft ? ` · draft ${detail.draft.draft_id} (${detail.draft.state})` : ''}</li>}
      {win && <li><b>Window rule</b> {win.tokenizer} · loss statement: {win.loss_statement}</li>}
      {grounding.unsupported && <li><b>Not supported by the window</b> {grounding.unsupported}</li>}
      {reads.failures?.length > 0 && <li><b>Unreadable artefacts</b> {reads.failures.map(f => `${f.artifact_ref} (${f.reason_code})`).join('; ')}</li>}
      {turn.receipt_id && <li><b>Receipt</b> {turn.receipt_id}{turn.critic_verdict ? ` · critic seam ${turn.critic_verdict.seam_attested ? 'attested' : 'not attested'} · ${n(turn.critic_verdict.findings_count)} finding(s)` : ''}</li>}
      <li><b>Terms</b> {(ev.terms || []).join(', ') || 'none'}</li>
    </ul>
  </details>;
}
