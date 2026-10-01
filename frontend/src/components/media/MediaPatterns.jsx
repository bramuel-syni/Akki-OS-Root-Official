import React, { useEffect, useState } from 'react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { mediaRequest } from './useMediaLibrary';
import { CLASS_NAMES, formatValue } from './acousticFormat';

const Row = ({ row }) => <tr data-testid={`work-media-pattern-${row.key.replace(/\./g, '-')}`}><th scope="row">{row.label}</th><td>{formatValue(row.median, row.unit)}</td><td>{formatValue(row.p10, row.unit)} – {formatValue(row.p90, row.unit)}</td></tr>;

export const MediaPatterns = ({ onClose }) => {
  const [data, setData] = useState(null), [error, setError] = useState('');
  useEffect(() => { let active = true; mediaRequest('/acoustics/patterns').then(d => { if (active) setData(d); }).catch(e => { if (active) setError(e.message); }); return () => { active = false; }; }, []);
  return <Dialog open onOpenChange={value => !value && onClose()}><DialogContent className="media-dialog wide" data-testid="work-media-patterns-dialog">
    <DialogTitle data-testid="work-media-patterns-title">Sound patterns</DialogTitle>
    <DialogDescription data-testid="work-media-patterns-summary">{data ? `${data.measured_files} measured recordings, grouped by how they read` : 'Reading measured recordings…'}</DialogDescription>
    {error && <p className="media-error" role="alert" data-testid="work-media-patterns-error">{error}</p>}
    {data && !data.measured_files && <p className="media-note" data-testid="work-media-patterns-empty">Measure a few recordings first. Patterns appear once profiles exist.</p>}
    {data?.most_separating?.length > 0 && <section className="sound-separating" data-testid="work-media-patterns-separating"><h3>What separates the groups most</h3>
      <table><thead><tr><th>Measurement</th>{Object.keys(data.most_separating[0].medians).map(k => <th key={k}>{CLASS_NAMES[k]}</th>)}</tr></thead>
        <tbody>{data.most_separating.map(s => <tr key={s.key} data-testid={`work-media-separating-${s.key.replace(/\./g, '-')}`}><th scope="row">{s.label}</th>{Object.values(s.medians).map((v, i) => <td key={i}>{v == null ? '—' : v}</td>)}</tr>)}</tbody></table></section>}
    {data?.classes.map(group => <section key={group.reads_as} className="sound-class" data-testid={`work-media-patterns-class-${group.reads_as}`}>
      <h3>{CLASS_NAMES[group.reads_as]} <small>{group.file_count} {group.file_count === 1 ? 'recording' : 'recordings'}</small></h3>
      <p className="sound-class-files">{group.files.map(f => f.title).join(' · ')}</p>
      <table><thead><tr><th>Measurement</th><th>Typical</th><th>Range (10th–90th)</th></tr></thead><tbody>{group.observables.map(row => <Row key={row.key} row={row} />)}</tbody></table>
    </section>)}
    {data && data.human_review.reviewed_files > 0 && <p className="sound-agreement" data-testid="work-media-patterns-agreement">Human-reviewed labels agree with the reading on {data.human_review.agreements} of {data.human_review.reviewed_files} recordings.</p>}
    {data?.measured_files > 0 && <p className="media-note" data-testid="work-media-patterns-method">Typical values are medians across the group. Separation compares group medians against the spread inside each group.</p>}
  </DialogContent></Dialog>;
};
