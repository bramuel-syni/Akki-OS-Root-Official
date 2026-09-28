import { stamp } from './evidence';
import { workSections } from './osHierarchy';

export function osWorkModel({ work, navigate, setParams, disclosure, toggle, section = 'records', search = '' }) {
  const selected = work.selected;
  const counts = ['routing', 'executing', 'ready'].map(state => ({ label: state, value: work.recordsAvailable ? work.rows.filter(r => r.state === state).length : '—',
    color: 'var(--ink)', subline: work.recordsAvailable ? 'Persisted work records' : work.loading ? 'Loading records…' : 'Records unavailable' }));
  return {
    isRegistryGroup: false, isRegEstate: false, isTasksActive: true, appTitle: 'My Work', appGroupLabel: 'WorkStudio',
    exitApp: () => navigate('/os?nav=work&app=tasks'), tmListMode: true, prodIsWork: true, prodIsToday: false,
    perfLevelsView: [{ label: 'My admitted identity', color: 'var(--ink)', bg: '#fff', onClick: work.reload }],
    prodTabsView: workSections.map(view => ({ key: view.key, label: view.label, color: view.key === section ? 'var(--blue)' : 'var(--ink3)',
      border: view.key === section ? 'var(--blue)' : 'transparent', onClick: () => navigate(view.path + search), active: view.key === section })),
    setTaskTabCreate: () => navigate('/dap/extract/processed'), taskStats: counts,
    tmSecWorkOpen: !disclosure.work, tmSecWorkLabel: disclosure.work ? 'Show' : 'Hide', tmSecWorkMb: '14px', toggleTmWork: () => toggle('work'),
    tmFilteredEmpty: work.recordsAvailable && !work.loading && !work.rows.length,
    tmFilterTabsView: [{ label: work.loading ? 'Loading…' : 'Refresh', bg: '#fff', border: 'var(--line)', color: 'var(--blue)', onClick: work.reload }],
    tmFilteredView: work.rows.map(r => ({ key: r.request_id, requestId: r.request_id, name: r.objective_text, status: r.state === 'routing' ? 'Routing · held' : r.state,
      statusColor: 'var(--brass)', meta: `${r.work_id} · ${stamp(r.created_at)}`, pct: r.execution_verified ? 100 : 0,
      evidence: r.execution_verified ? 'Verified execution' : 'Execution not verified', barColor: 'var(--ink3)', onOpen: () => setParams({ request: r.request_id }) })),
    tmSecAkkiOpen: !disclosure.receipts, tmSecAkkiLabel: disclosure.receipts ? 'Show' : 'Hide', tmSecAkkiMb: '14px', toggleTmAkki: () => toggle('receipts'),
    tmRail: selected?.history.map((h, i) => ({ num: String(i + 1), tag: h.event, color: 'var(--brass)', text: `${stamp(h.at)} · ${h.state}${h.reason_code ? ` · ${h.reason_code}` : ''} · ${h.receipt_hash}` })) || [],
    tmSecDivideOpen: Boolean(disclosure.division), tmSecDivideLabel: disclosure.division ? 'Hide' : 'Show', tmSecDivideMb: '14px', toggleTmDivide: () => toggle('division'),
    tmDivideReading: 'Counts reflect persisted states, not execution progress or output quality.',
    tmDivideBars: counts.map(c => ({ label: c.label, size: String(c.value), w: `${work.recordsAvailable && work.rows.length ? c.value * 100 / work.rows.length : 0}%`, fill: 'var(--brass)' })),
    prodRailIsWork: true, prodRailNotWork: false,
    tmRailHead: work.error || (selected ? `${selected.reason_code} · ${selected.reason}` : work.loading || work.detailLoading ? 'Loading authoritative records…' : 'Select a work record to inspect its evidence.'),
    tmRailLines: selected ? [{ label: 'Work identifier', value: selected.work_id, note: 'Same identifier in DAP' }, { label: 'Engine', value: selected.governing_engine, note: selected.next_action || (selected.execution_verified ? 'Measured execution recorded; delivery remains separately checked.' : 'Execution is not live-verified.') }, { label: 'Objective SHA-256', value: '', note: selected.objective_hash }] : [],
  };
}

export const osWorkCopy = {
  2411: 'Work records for —', 2422: '+ New request', 2429: 'The work — recorded requests',
  2430: 'Requests remain held until their actual rights, terms, approval authority and executor resolve.',
  2445: 'Open a record to inspect its immutable objective and banked history.',
  2471: '{{ t.evidence }}', 2485: 'Recorded history', 2486: 'Events for the selected request. Receipt hashes refer to the same canonical ledger as DAP.',
  2511: 'Counts by recorded lifecycle state.', 2910: 'Selected request and governing evidence',
};