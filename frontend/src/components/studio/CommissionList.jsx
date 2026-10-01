import React from 'react';
import { releaseClass, stamp } from './useStudio';
import { documentTitle, PresentationDetails } from '../shared/PresentationDetails';

export function CommissionList({ commissions, selected, onSelect }) {
  const rows = commissions || [];
  return <section className="estate-section" data-testid="studio-commissions">
    <div className="estate-head"><h2>Your documents</h2><span className="estate-status" data-testid="studio-commissions-count">{rows.length} documents</span></div>
    {!rows.length && <p data-testid="studio-commissions-empty">No documents yet. Create a board pack from the latest estate census.</p>}
    <ul className="studio-document-list" data-testid="studio-commissions-table">{rows.map(c => <li key={c.commission_id} data-testid={`studio-row-${c.commission_id}`}>
      <button className="studio-document-button" data-testid={`studio-select-${c.commission_id}`} aria-pressed={selected === c.commission_id} onClick={() => onSelect(c.commission_id)}>
        <span><b>{documentTitle(c)}</b><small>Version {c.current_content_version} · {(c.outputs || []).map(f => f.toUpperCase()).join(' / ')} · {stamp(c.updated_at || c.created_at)}</small></span>
        <span className={`estate-status ${releaseClass(c.release?.state)}`} data-testid={`studio-release-${c.commission_id}`}>{c.release?.state === 'clear' ? 'Ready to download' : c.release?.state || 'Not built'}</span>
      </button>
    </li>)}</ul>
  </section>;
}

export function StudioSkill({ skill }) {
  if (!skill) return null;
  return <PresentationDetails id="studio-skill" title="Document production checks">
    <p data-testid="studio-skill-version">Document studio · v{skill.version} · {skill.edit_within_approval ? 'Approved installation' : 'Installation needs approval'}</p>
    <ul data-testid="studio-skill-limits">{(skill.limits || []).map((limit, i) => <li key={i}>{limit}</li>)}</ul>
  </PresentationDetails>;
}