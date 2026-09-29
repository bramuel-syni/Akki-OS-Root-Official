import React from 'react';
import { stamp } from './useEstateReport';

// Minimal Markdown → blocks for the governed dossier (headings, lists, paragraphs, bold); no HTML is ever injected.
function inline(text) {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).filter(Boolean).map((part, i) => part.startsWith('**') ? <b key={i}>{part.slice(2, -2)}</b> : part.startsWith('`') ? <code key={i}>{part.slice(1, -1)}</code> : part);
}

export function Markdown({ text, testId }) {
  const blocks = [];
  let list = null;
  for (const raw of String(text || '').split('\n')) {
    const line = raw.trimEnd();
    const item = line.match(/^\s*(?:[-*]|\d+[.)])\s+(.*)$/);
    if (item) { (list ||= { ordered: /^\s*\d/.test(line), items: [] }).items.push(item[1]); continue; }
    if (list) { blocks.push(list); list = null; }
    if (!line.trim()) continue;
    const head = line.match(/^(#{1,4})\s+(.*)$/);
    blocks.push(head ? { level: head[1].length, text: head[2] } : { text: line });
  }
  if (list) blocks.push(list);
  return <div className="estate-md" data-testid={testId}>{blocks.map((b, i) => b.items
    ? (b.ordered ? <ol key={i}>{b.items.map((t, j) => <li key={j}>{inline(t)}</li>)}</ol> : <ul key={i}>{b.items.map((t, j) => <li key={j}>{inline(t)}</li>)}</ul>)
    : b.level ? React.createElement(`h${Math.min(6, b.level + 2)}`, { key: i }, inline(b.text)) : <p key={i}>{inline(b.text)}</p>)}</div>;
}

export function EstateDossier({ report, canCompose, composing, refusal, onCompose }) {
  const d = report.dossier;
  return <section className="estate-section" data-testid="estate-dossier">
    <header className="estate-head"><div><h2>Estate-handling dossier</h2>
      <p>A narrative brief composed by a governed model from these aggregates only — no row, cell or identifier value crosses the chokepoint. It cites the figures above; where a figure is unmeasured it says so.</p></div>
      {canCompose && <button className="estate-btn primary" onClick={onCompose} disabled={composing} data-testid="estate-compose-dossier">{composing ? 'Composing…' : d ? 'Recompose dossier' : 'Compose dossier'}</button>}
    </header>
    {refusal && <p className="estate-alert" role="alert" data-testid="estate-dossier-refusal">The chokepoint refused: {refusal}</p>}
    {d ? <>
      <p className="estate-note" data-testid="estate-dossier-meta">Model {d.model_id} via {d.provider} · receipt <code>{d.receipt_id}</code> · {stamp(d.at)} · {d.tokens_in} tokens in / {d.tokens_out} out · prompt sha {String(d.prompt_sha256).slice(0, 12)}…</p>
      <Markdown text={d.text} testId="estate-dossier-text" />
    </> : <p className="estate-note" data-testid="estate-dossier-empty">No dossier has been composed for this census yet.{canCompose ? ' Composing sends the aggregate figures — never rows — through the governed chokepoint and banks the receipt.' : ' An admitted operator can compose it.'}</p>}
  </section>;
}

export function EstateMethod({ report }) {
  return <section className="estate-section" data-testid="estate-method">
    <header className="estate-head"><div><h2>Method, coverage and limits</h2></div></header>
    <p>{report.method_note}</p>
    <p>{report.coverage_note}</p>
    <ul className="estate-list plain">
      {report.connections.map(c => <li key={c.source_ref}><span><b>{c.label}</b><small>{c.database_count} databases · {c.table_count} tables</small></span><em className={`estate-status ${c.status}`}>{c.status}</em>{c.reason_code ? <small>{c.reason_code}</small> : null}</li>)}
    </ul>
    {report.errors?.length ? <ul className="estate-errors" data-testid="estate-errors">{report.errors.map((e, i) => <li key={i}><b>{e.connection}</b>{e.database ? ` · ${e.database}` : ''}: {e.code}</li>)}</ul> : null}
    <p className="estate-note">Row values retained: {report.row_values_retained ? 'yes' : 'none'} — the census returned aggregates, sketches and hashes only.</p>
  </section>;
}
