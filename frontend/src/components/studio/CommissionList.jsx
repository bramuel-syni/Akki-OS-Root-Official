import React from 'react';
import { releaseClass, stamp } from './useStudio';

export function CommissionList({ commissions, selected, onSelect }) {
  const rows = commissions || [];
  return <section className="estate-section" data-testid="studio-commissions">
    <div className="estate-head"><div><h2>Commissions</h2><p>One content model, many formats, byte-identical rebuilds, a recorded creative direction. Every row is a commission directory the studio built from receipted facts; nothing here was authored by a model.</p></div>
      <span className="estate-status" data-testid="studio-commissions-count">{rows.length} on record</span></div>
    {!rows.length && <div className="estate-note" data-testid="studio-commissions-empty">No commission is on record for your tenant. “Commission board pack” on Estate intelligence produces the first one from the verified census.</div>}
    {rows.length > 0 && <div className="estate-table-wrap"><table className="estate-table" data-testid="studio-commissions-table">
      <thead><tr><th>Commission</th><th>Source</th><th>Direction</th><th>Outputs</th><th>Version</th><th>Release</th><th>Last build</th></tr></thead>
      <tbody>{rows.map(c => <tr key={c.commission_id} data-testid={`studio-row-${c.commission_id}`} onClick={() => onSelect(c.commission_id)} style={{ cursor: 'pointer', background: selected === c.commission_id ? 'var(--surface2)' : undefined }}>
        <td><b>{c.title}</b><small>{c.commission_id}</small></td>
        <td>{c.producer}<small>{c.source_ref}</small></td>
        <td>{c.adopted_direction} · {c.voice}<small>{c.frame_ref} · {c.purpose}</small></td>
        <td>{(c.outputs || []).join(' · ')}</td>
        <td>v{c.current_content_version}<small>{c.builds} builds · {c.revisions} revisions</small></td>
        <td><span className={`estate-status ${releaseClass(c.release?.state)}`} data-testid={`studio-release-${c.commission_id}`}>{c.release?.state}</span></td>
        <td>{c.last_build ? <>{c.last_build.status}<small>{stamp(c.last_build.at)}</small></> : <small>unbuilt</small>}</td>
      </tr>)}</tbody>
    </table></div>}
  </section>;
}

export function StudioSkill({ skill }) {
  if (!skill) return null;
  const env = skill.environment || {};
  return <section className="estate-section" data-testid="studio-skill">
    <div className="estate-head"><div><h2>The studio</h2><p>{skill.description}</p></div><span className={`estate-status ${skill.edit_within_approval ? 'complete' : 'blocked'}`} data-testid="studio-skill-version">{skill.skill} v{skill.version}</span></div>
    <div className="estate-columns">
      <div>
        <h3>Installed skill</h3>
        <ul className="estate-list">
          <li><span><b>{skill.files} files</b><small>owner zip {skill.owner_zip_sha256?.slice(0, 16)}… · skill zip {skill.skill_zip_sha256?.slice(0, 16)}…</small></span><small>{stamp(skill.installed_at)}</small></li>
          <li><span><b>Changed from v1.0</b><small>{(skill.changed_from_v1_0 || []).join(', ') || 'nothing'}</small><small>{skill.edit_statement}</small></span><small><span className={`estate-status ${skill.edit_within_approval ? 'complete' : 'blocked'}`}>{skill.edit_within_approval ? 'within approval' : 'OUTSIDE approval'}</span></small></li>
          <li><span><b>Voices</b><small>{(skill.voices || []).join(' · ')}</small></span><small>themes {(skill.themes || []).join(' · ')}</small></li>
          <li><span><b>Direction stage</b><small>routine: {skill.direction_stage?.routine}</small><small>non-routine: {skill.direction_stage?.non_routine}</small><small>LLM path: {skill.direction_stage?.llm_chokepoint_path}</small></span></li>
        </ul>
      </div>
      <div>
        <h3>Environment of record</h3>
        <ul className="estate-list" data-testid="studio-environment">
          <li><span><b>LibreOffice</b><small>{env.libreoffice}</small></span></li>
          <li><span><b>python-pptx {env['python-pptx']}</b><small>python-docx {env['python-docx']} · openpyxl {env.openpyxl} · matplotlib {env.matplotlib} · Python {env.python}</small></span></li>
          <li><span><b>Office tools</b><small>recalc: {env.office_tools?.recalc}</small><small>validate: {env.office_tools?.validate}</small></span></li>
        </ul>
        <h3 style={{ marginTop: 14 }}>Limits</h3>
        <ul className="estate-list">{(skill.limits || []).map((l, i) => <li key={i}><span><small>{l}</small></span></li>)}</ul>
      </div>
    </div>
  </section>;
}
