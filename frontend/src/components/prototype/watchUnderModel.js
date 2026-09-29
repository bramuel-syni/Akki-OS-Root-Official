import React from 'react';
import { stamp } from './evidence';

const curve = points => {
  const top = Math.max(1, ...points);
  const path = points.map((v, i) => `${(i * 100) / (points.length - 1)},${28 - (24 * v) / top}`).join(' ');
  return <svg viewBox="0 0 100 30" preserveAspectRatio="none" aria-label={`Refusals over nine days: ${points.join(', ')}`} style={{ width: 120, height: 30, flex: '0 0 auto' }}>
    <polyline points={path} fill="none" style={{ stroke: points.at(-1) > points[0] ? '#7a1f1f' : 'var(--blue)' }} strokeWidth="2" vectorEffect="non-scaling-stroke" /></svg>;
};

export function watchUnderModel({ data, error, show, act, navigate }) {
  if (!data) return error ? { mirageCopy: error, markedCopy: error } : {};
  const run = (label, promise) => promise.then(body => show({ title: label, code: 'Recorded', body: body.notice?.text || body.decision?.title || 'Recorded on the tenant feed.',
    next: body.decision ? 'Routed to Decisions; dual control applies.' : 'A notice is a record of what was said, not a restriction.',
    actions: body.decision ? [{ label: 'Open Decisions', bg: 'var(--blue)', color: 'var(--paper)', border: 'var(--blue)', onClick: () => navigate('/os/admin/greymirror/watch/decisions') }] : [] }))
    .catch(e => show({ title: label, code: 'Refused', body: e.message }));
  const held = (data.marked || []).filter(m => m.standing === 'held');
  const patterns = (data.patterns || []).map(p => ({
    key: p.principal_id, text: `${p.subject_ref} · ${p.refusals_9d} refused crossing(s) in nine days · ${p.effects} Watch effect(s)`,
    meta: `${p.last_detector ? `Last detector: ${p.last_detector}` : 'No verdict minted'}${p.redeclaration_requested ? ' · re-declaration requested' : ''}`,
    curveEl: curve(p.curve),
    onCloser: () => show({ title: 'Watch closer', subtitle: p.subject_ref, code: 'Read only', body: `Daily refused crossings, oldest first: ${p.curve.join(' · ')}. ${p.effects} effect receipt(s). Detectors act on their own thresholds; looking closer changes nothing.`, next: 'Promotion into the mirage is not autonomous until the owner rules the entry threshold.' }),
    onDeclare: () => run('Ask for an updated declaration', act('/api/portal/watch/requests/redeclaration', { subject_ref: p.subject_ref })),
    onWalk: () => navigate(`/os/admin/greymirror/watch/record`),
  }));
  const m = data.mirage || {};
  return {
    patternsView: patterns,
    mirageCopy: `${m.live ?? 0} decoy(s) live · ${m.touches ?? 0} touch(es) · isolation ${m.isolation_passed === null || m.isolation_passed === undefined ? 'not yet measured' : m.isolation_passed ? 'measured disjoint from production' : 'FAILED'}. Construction and placement are never shown here.`,
    mirageFindings: (m.findings || []).map((text, i) => ({ key: String(i), text })),
    markedCopy: held.length ? `${held.length} subject(s) carry a live mark from a structural conviction. De-marking is a human, dual-control act routed to Decisions.` : `No subject carries a live mark. ${(data.marked || []).length} historical mark(s) de-marked by dual control remain on record.`,
    markedLines: (data.marked || []).map(k => `${k.subject_ref} · marked ${stamp(k.minted_at)} · ${k.standing} · ${k.dimensions_bound} dimensions bound${k.notice_sent ? ' · subject notified' : ''}`),
    onRequestDemark: () => held.length ? run('Request removal of the mark', act('/api/portal/watch/requests/demark', { subject_ref: held[0].subject_ref }))
      : show({ title: 'Request removal of the mark', code: 'Nothing to request', body: 'No subject carries a live mark in your tenant.' }),
    watchEmpty: !patterns.length,
  };
}
