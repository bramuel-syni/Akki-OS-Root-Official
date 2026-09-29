import { count } from './evidence';

const tile = (key, label, cell, index, state, setState, tone='var(--ink)') => ({
  key, label, value: cell ? count(cell.value) : '—', note: cell?.note || 'Awaiting records', tone: cell && cell.value ? tone : 'var(--ink3)',
  radius: index === 0 ? '10px 0 0 10px' : '0', showDetail: state.gmDetail === key && Boolean(cell?.lines?.length),
  popLeft: index === 2 ? 'auto' : '0', popRight: index === 2 ? '0' : 'auto', detailLines: (cell?.lines || []).map(t => ({ t })),
  onEnter: () => setState(s => ({ ...s, gmDetail: key })), onLeave: () => setState(s => ({ ...s, gmDetail: null })),
});

const bars = (rows, fill) => {
  const top = Math.max(1, ...rows.map(r => r.value));
  return rows.map(r => ({ key: r.label, label: r.label, size: count(r.value), pct: Math.round(100 * r.value / top), fill }));
};

export function watchStateModel({ data, error, state, setState, show }) {
  if (!data) return error ? { gmTopOneliner: error } : {};
  const t = data.tiles || {};
  const chart = state.chart || 'activity';
  const rows = data.charts?.[chart] || [];
  const witness = () => show({ title: 'Is the watch itself working', code: data.witness?.identity ? 'Measured' : 'Not placed',
    body: `${data.witness_status}. ${count(data.witness?.attestations)} digest attestations · ${count(data.witness?.tamper_alarms)} tamper alarms · placement: ${data.witness?.placement}. ${data.learning?.label}.`,
    next: data.never_all_clear });
  return {
    gmTopEyebrow: 'The Watch — State',
    gmTopOneliner: `${data.never_all_clear} Detectors run under ${data.learning?.label}.`,
    gmStats: [tile('waiting', 'Waiting for you', t.waiting, 0, state, setState, 'var(--blue)'), tile('actors', 'People and agents', t.actors, 1, state, setState), tile('sessions', 'Open sessions', t.sessions, 2, state, setState)],
    gmStatsG2: [tile('allowed', 'Allowed', t.allowed, 0, state, setState), tile('refused', 'Refused', t.refused, 1, state, setState, '#7a1f1f'), tile('flagged', 'Flagged', t.flagged, 2, state, setState, 'var(--blue)')],
    gmStatsG3: [tile('checks', 'Checks passed', t.checks, 0, state, setState), tile('exceptions', 'Exceptions', t.exceptions, 1, state, setState, '#7a1f1f'), tile('recovery', 'Recovery', t.recovery, 2, state, setState)],
    gmG2Sub: 'Crossings the gates admitted or refused, and the verdicts minted from them.',
    gmG3Sub: 'Witness attestations, break-in measurements and releases — not a self-reported health claim.',
    gmVisualOneliner: 'Counts from the tenant feed; no trend is inferred beyond what was recorded.',
    gmChartTitle: chart === 'activity' ? 'Crossings by protected boundary' : 'Responses by action class',
    gmChartCaption: `${count(data.counts?.gate_crossings)} crossings · ${count(data.counts?.gate_effects)} effects · ${count(data.counts?.gate_releases)} releases`,
    gmChartRows: bars(rows, chart === 'activity' ? 'var(--blue)' : '#7a1f1f'),
    gmVisualFoot: `${(data.protected_boundaries || []).length} protected boundaries observed with mark checks on every pass · console reads receipted: ${count(data.counts?.console_reads)}`,
    gmTableOneliner: 'Every acted row carries its evidence walk: signal → verdict → policy row → action → outcome → witness.',
    gmHeadEyebrow: 'What is happening right now',
    gmRailSub: 'Evidence and actions from the same record',
    openBriefGmVisual: witness,
  };
}
