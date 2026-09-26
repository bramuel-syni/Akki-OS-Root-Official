import { stamp } from './evidence';

export const operationForPath = path => ({ processed: 'processed_intelligence', finetune: 'fine_tune_model', skill: 'develop_skills', raw: 'download_raw_data' }[path.split('/').pop()]);
const titles = { processed_intelligence: 'Processed intelligence', fine_tune_model: 'Trained models', develop_skills: 'Callable skills', download_raw_data: 'Raw data' };

export function dapWorkModel({ work, data, path, draft, setDraft, units, setUnits, params, setParams, search, setSearch, sections, setSections, navigate }) {
  const operation = operationForPath(path);
  const terms = work.entitlement;
  const selected = work.selected;
  const open = row => setParams({ request: row.request_id });
  const reset = () => { setDraft(''); setUnits([]); work.resetKey(); work.setError(''); setParams({}); };
  const rows = work.rows.filter(r => `${r.request_id} ${r.objective_text} ${r.state}`.toLowerCase().includes(search.toLowerCase()));
  const toggle = key => setSections(v => ({ ...v, [key]: !v[key] }));
  return {
    isExtract: Boolean(operation), isOverview: path === '/dap/requests', isContract: path === '/dap/governance/contract',
    showPageHead: true, pageEyebrow: operation ? 'Extract' : 'Data access', pageTitle: titles[operation] || (path === '/dap/requests' ? 'Your requests' : 'Contract & access terms'),
    pageSub: work.error || (work.loading ? 'Loading authoritative records…' : 'Frozen requests and governing records for your admitted identity.'),
    isFinetune: false, howOpen: sections.how, howToggle: () => toggle('how'), howChev: sections.how ? '' : 'rotate(-90deg)',
    profileRows: [{ l: 'Request', v: 'Objective and scope frozen.', notLast: true }, { l: 'Admission', v: 'Rights, terms and approval checked.', notLast: true }, { l: 'Execution', v: 'Only through an admitted engine.', notLast: false }],
    practiceBg: 'var(--surface)', practice: 'Submission records intent. It is not approval, execution, or a release grant.',
    hasChatLog: true, chatLog: [{ text: 'An admitted assistance executor is not available. No generated advice or approval is being supplied.', align: 'flex-start', border: 'var(--line)', bg: 'var(--surface)', hasTag: false }],
    jobShaping: true, setupOpen: sections.setup, setupToggle: () => toggle('setup'), setupChev: sections.setup ? '' : 'rotate(-90deg)',
    composeCardOpacity: '1', composeCardPointer: 'auto', composeSubmitBusy: work.busy || !data?.can_run,
    objDraft: draft, objChange: event => setDraft(event.target.value), objPlaceholder: 'State the objective for this request',
    objHint: 'The submitted objective and selected source references cannot be widened.',
    scopeChips: (data?.sources || []).map(s => ({ key: s.source_id, label: s.label, meta: s.source_id, cursor: work.busy ? 'wait' : 'pointer', opacity: '1',
      border: units.includes(s.source_id) ? 'var(--blue)' : 'var(--line)', bg: units.includes(s.source_id) ? 'rgba(22,39,74,.08)' : '#fff', color: 'var(--ink)',
      onClick: () => !work.busy && setUnits(v => v.includes(s.source_id) ? v.filter(u => u !== s.source_id) : [...v, s.source_id]) })),
    modeFields: [], termsId: terms?.licence?.terms_identifier || 'Unresolved', meterUnit: 'not yet established',
    apprColor: 'var(--brass)', apprHead: 'Admission unresolved', apprWhy: 'No recorded operation-specific approval or execution grant is inferred from census access.',
    hasSubmitError: Boolean(work.error), submitErrorMsg: work.error,
    submitBtnOpacity: work.busy || !data?.can_run ? '.55' : '1', submitBtnCursor: work.busy ? 'wait' : 'pointer', submitBtnLabel: !data?.can_run ? 'Operator access required' : work.busy ? 'Recording…' : 'Submit request',
    freeze: async () => {
      if (!draft.trim() || !units.length) { work.setError('Enter an objective and select at least one source.'); return; }
      const created = await work.submit({ objective_text: draft, operation, units });
      if (created) { setDraft(''); setUnits([]); work.resetKey(); open(created); }
    },
    railChat: true, railIsNotes: false, railIsChat: true, resetJob: () => operation ? reset() : navigate('/dap/extract/processed'),
    railStatsOpen: sections.stats, railToggleStats: () => toggle('stats'), railStatsChev: sections.stats ? '' : 'rotate(-90deg)',
    railStatsRow: ['All', 'Routing', 'Executing', 'Ready'].map(label => ({ label, count: label === 'All' ? work.rows.length : work.rows.filter(r => r.state === label.toLowerCase()).length,
      bg: '#fff', ring: '1px solid var(--line)', numColor: 'var(--ink)', onClick: () => setSearch(label === 'All' ? '' : label.toLowerCase()) })),
    railSearch: search, railSearchChange: e => setSearch(e.target.value), railEmpty: !work.loading && !rows.length,
    railRequests: rows.map(r => ({ key: r.request_id, id: r.request_id, objective: r.objective_text, status: r.state === 'routing' ? 'Routing · held' : r.state,
      color: 'var(--brass)', bg: 'var(--surface)', slotRows: '1fr', enterOpacity: '1', enterTransform: 'none', highlightBg: '#fff', onView: () => open(r), noAction: true,
      showTimestamp: true, timestamp: stamp(r.created_at), timestampColor: 'var(--ink3)' })),
    railDrawerOpen: Boolean(selected), railCloseDrawer: () => setParams({}),
    railDrawerVM: selected ? { id: selected.request_id, statusLabel: selected.state === 'routing' ? 'Routing · held' : selected.state, statusColor: 'var(--brass)', statusBg: 'var(--surface)',
      agreement: terms?.licence?.terms_identifier || 'Terms unresolved', submitted: stamp(selected.created_at), hasDetail: true, objective: selected.objective_text, scope: selected.units.join(', '), otherStatus: true } : {},
    ovEyebrow: 'Work history', ovTitle: 'Your frozen requests.', ovLede: work.error || (work.loading ? 'Loading…' : `${work.rows.length} persisted requests. Execution remains subject to admission.`),
    ovRows: rows.map(r => ({ n: r.request_id, title: r.objective_text, line: stamp(r.created_at), right: r.state, color: 'var(--brass)', onClick: () => open(r) })),
    ovNote: 'The same work identifier is used in Akki OS and the Data Access Portal.',
    govContractRows: [
      { l: 'Licence', v: terms?.licence?.plan_identifier || 'Unresolved — no owner-admitted licence is available.' },
      { l: 'Status', v: terms?.status || 'Loading' }, { l: 'Terms', v: terms?.licence?.terms_identifier || 'Unresolved' },
      { l: 'Allowance', v: terms?.allowance_state ? `${terms.allowance_state.credits_remaining} credits · ${terms.allowance_state.period_iso}` : 'Unresolved — not a zero balance or free grant.' },
      { l: 'Catalog', v: terms?.status === 'resolved' ? `${terms.rows.length} admitted listed models` : 'No admitted model picker is available.' },
    ],
  };
}