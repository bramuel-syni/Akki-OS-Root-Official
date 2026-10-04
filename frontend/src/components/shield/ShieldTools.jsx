import React, { useState } from 'react';

const field = { width: '100%', padding: '8px 10px', border: '1px solid var(--line)', borderRadius: 7, fontSize: 12.5, fontFamily: 'inherit', background: '#fff', boxSizing: 'border-box' };
const Row = ({ label, children }) => <label style={{ display: 'block', marginBottom: 10 }}><span className="estate-label">{label}</span>{children}</label>;
const list = v => v.split(/[\n,]/).map(s => s.trim()).filter(Boolean);

export function AuthorCategoryForm({ busy, onSubmit, onCancel }) {
  const [v, setV] = useState({ name: '', kind: 'contextual', action: 'abstract', enforcement: 'enforced', description: '', cues: '', patterns: '', values: '', targets: 'PROPER_NOUN,ORG,PERSON' });
  const set = k => e => setV(s => ({ ...s, [k]: e.target.value }));
  return <form data-testid="shield-author-form" className="estate-section" style={{ marginTop: 16 }} onSubmit={e => { e.preventDefault(); onSubmit({ name: v.name, kind: v.kind, action: v.action, enforcement: v.enforcement, description: v.description, cues: list(v.cues), patterns: list(v.patterns), values: list(v.values), targets: v.kind === 'contextual' ? list(v.targets) : [] }); }}>
    <h2 style={{ font: '400 20px var(--head)', margin: '0 0 12px' }}>Declare a category</h2>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))', gap: '0 16px' }}>
      <Row label="Name (snake_case)"><input data-testid="shield-author-name" style={field} value={v.name} onChange={set('name')} required pattern="^[a-z][a-z0-9_]+$" maxLength={80} /></Row>
      <Row label="Classification"><select data-testid="shield-author-kind" style={field} value={v.kind} onChange={set('kind')}><option value="exact">By name (literal values)</option><option value="pattern">By pattern (regular expressions)</option><option value="contextual">By context (meaning signalled by cues)</option></select></Row>
      <Row label="Treatment"><select data-testid="shield-author-action" style={field} value={v.action} onChange={set('action')}><option value="abstract">Abstract to a typed placeholder, rebind the reply</option><option value="remove">Withhold entirely</option><option value="generalise">Generalise</option></select></Row>
      <Row label="Scope"><select data-testid="shield-author-enforcement" style={field} value={v.enforcement} onChange={set('enforcement')}><option value="enforced">Enforced on every model crossing</option><option value="advisory">Advisory · receipted; enforced in confidential workflows</option></select></Row>
    </div>
    <Row label="What it protects"><input data-testid="shield-author-description" style={field} value={v.description} onChange={set('description')} required maxLength={600} /></Row>
    {v.kind === 'contextual' && <><Row label="Cues (comma-separated words that signal the meaning, any language)"><input data-testid="shield-author-cues" style={field} value={v.cues} onChange={set('cues')} required /></Row>
      <Row label="Targets inside a cued sentence"><input data-testid="shield-author-targets" style={field} value={v.targets} onChange={set('targets')} placeholder="PROPER_NOUN, ORG, PERSON, MONEY, NUMBER, PERCENT, SENTENCE" /></Row></>}
    {v.kind === 'pattern' && <Row label="Regular expressions (one per line)"><textarea data-testid="shield-author-patterns" style={{ ...field, minHeight: 56 }} value={v.patterns} onChange={set('patterns')} required /></Row>}
    {v.kind === 'exact' && <Row label="Literal values (one per line) — held in the register only"><textarea data-testid="shield-author-values" style={{ ...field, minHeight: 56 }} value={v.values} onChange={set('values')} required /></Row>}
    <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="shield-author-submit" disabled={Boolean(busy)}>{busy ? 'Recording…' : 'Put into force'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="shield-author-cancel">Cancel</button></div>
  </form>;
}

export function ProposeForm({ busy, onSubmit, onCancel }) {
  const [text, setText] = useState(''), [ref, setRef] = useState('');
  return <form data-testid="shield-propose-form" className="estate-section" style={{ marginTop: 16 }} onSubmit={e => { e.preventDefault(); onSubmit(text, ref || null); }}>
    <h2 style={{ font: '400 20px var(--head)', margin: '0 0 6px' }}>Propose declarations from a document</h2>
    <p className="estate-note" style={{ margin: '0 0 12px' }}>The document is read inside the boundary only. The register proposes drafts — the exact values it recognised, and passages the document itself marks confidential that nothing covers. Drafts protect nothing until adopted.</p>
    <Row label="Document text"><textarea data-testid="shield-propose-text" style={{ ...field, minHeight: 120 }} value={text} onChange={e => setText(e.target.value)} required /></Row>
    <Row label="Source reference (optional)"><input data-testid="shield-propose-ref" style={field} value={ref} onChange={e => setRef(e.target.value)} maxLength={200} /></Row>
    <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="shield-propose-submit" disabled={Boolean(busy) || !text.trim()}>{busy ? 'Reading…' : 'Propose drafts'}</button><button type="button" className="estate-btn" onClick={onCancel} data-testid="shield-propose-cancel">Cancel</button></div>
  </form>;
}

export function TestPassage({ busy, preview, onTest, onClear }) {
  const [text, setText] = useState('');
  const spans = preview?.classify?.spans || [];
  return <section className="estate-section" data-testid="shield-test" style={{ marginTop: 16 }}>
    <header className="estate-head"><div><h2>Test a passage</h2><p>See what the register recognises and exactly what an external model would receive. Nothing here is sent to a model.</p></div></header>
    <form onSubmit={e => { e.preventDefault(); onTest(text); }}>
      <Row label="Passage"><textarea data-testid="shield-test-text" style={{ ...field, minHeight: 80 }} value={text} onChange={e => setText(e.target.value)} required /></Row>
      <div className="estate-actions"><button type="submit" className="estate-btn primary" data-testid="shield-test-submit" disabled={busy === 'Test' || !text.trim()}>{busy === 'Test' ? 'Checking…' : 'Check'}</button>{preview && <button type="button" className="estate-btn" onClick={onClear} data-testid="shield-test-clear">Clear</button>}</div>
    </form>
    {preview && <div style={{ marginTop: 16 }} data-testid="shield-test-result">
      <h3>What the model would receive</h3>
      <p data-testid="shield-test-safe" style={{ fontSize: 13, lineHeight: 1.6, background: 'var(--surface)', border: '1px solid var(--line)', borderRadius: 8, padding: '10px 12px', overflowWrap: 'anywhere' }}>{preview.reconstruct.safe_text}</p>
      <div className="estate-meta"><span data-testid="shield-test-categories">categories: {preview.classify.categories.join(', ') || 'none'}</span><span>bindings held inside: {preview.reconstruct.bindings_held_inside}</span><span data-testid="shield-test-joint">joint disclosure: {preview.reconstruct.joint_disclosure?.passes ? 'passes' : 'generalised'}</span></div>
      {spans.length ? <div className="estate-table-wrap" style={{ marginTop: 10 }}><table className="estate-table" data-testid="shield-test-spans"><thead><tr><th>Category</th><th>How</th><th>Treatment</th><th>Scope</th><th>Cue</th></tr></thead>
        <tbody>{spans.map((s, i) => <tr key={i}><td data-label="Category"><b>{s.category}</b>{s.also?.length ? <small>also {s.also.join(', ')}</small> : null}</td><td data-label="How">{s.kind}</td><td data-label="Treatment">{s.action}</td><td data-label="Scope">{s.enforcement}</td><td data-label="Cue"><small style={{ maxWidth: 320 }}>{s.cue}</small></td></tr>)}</tbody></table></div> : <p className="estate-note">Nothing in this passage is protected by the register.</p>}
    </div>}
  </section>;
}
